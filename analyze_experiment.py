#!/usr/bin/env python3
"""
实验分析脚本
============
读取双评分者多标签打分 (scoresheet.csv)，输出配对比较、效应量、Cohen's κ。

用法:
    # Tier 0: 仅描述性统计
    python analyze_experiment.py scores/scoresheet.csv --tier 0

    # Tier 1: 完整分析（含 Wilcoxon + bootstrap CI + κ）
    python analyze_experiment.py scores/scoresheet.csv --tier 1

    # 指定输出
    python analyze_experiment.py scores/scoresheet.csv --tier 1 -o analysis/analysis_output.json

输入格式 (scoresheet.csv):
    case_id, prompt_arm, rater, step, presence, correctness, note

输出:
    - 终端: 配对比较摘要 + κ 报告
    - JSON: 完整分析结果（机器可读）
    - MD:  分析报告（人类可读，可选）

依赖:
    pip install numpy scipy
    (无额外依赖也可运行描述性统计——仅需标准库)
"""

import argparse
import csv
import json
import statistics
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional


# ============================================================
# 数据加载
# ============================================================

def load_scoresheet(path: str) -> list[dict]:
    """加载评分工作表 CSV。"""
    rows = []
    with open(path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            row["presence"] = int(row.get("presence", 0))
            # correctness can be 0, 1, or "NA" (when presence=0)
            corr = row.get("correctness", "NA")
            if corr != "NA" and corr != "":
                row["correctness"] = int(corr)
            else:
                row["correctness"] = None
            rows.append(row)
    return rows


# ============================================================
# 派生指标计算
# ============================================================

def compute_presence_coverage(rows: list[dict], arm: str, rater: str) -> dict[str, float]:
    """
    计算每个 case 的 presence_coverage。
    presence_coverage = 出现的步骤数 / 应出现的步骤数
    返回 {case_id: coverage}
    """
    # 按 case 聚合
    case_steps: dict[str, dict[str, int]] = defaultdict(dict)
    for r in rows:
        if r["prompt_arm"] != arm or r["rater"] != rater:
            continue
        case_steps[r["case_id"]][r["step"]] = r["presence"]

    coverage = {}
    for case_id, steps in case_steps.items():
        total = len(steps)
        present = sum(steps.values())
        coverage[case_id] = present / total if total > 0 else 0.0
    return coverage


def compute_correctness_rate(rows: list[dict], arm: str, rater: str) -> dict[str, float]:
    """
    计算每个 case 的 correctness_rate。
    correctness_rate = 正确步骤数 / 出现的步骤数（仅当 presence>0 时计算）
    返回 {case_id: rate}，无出现步骤的 case 为 None
    """
    case_steps: dict[str, list[tuple[int, Optional[int]]]] = defaultdict(list)
    for r in rows:
        if r["prompt_arm"] != arm or r["rater"] != rater:
            continue
        case_steps[r["case_id"]].append((r["presence"], r["correctness"]))

    rates = {}
    for case_id, steps in case_steps.items():
        present_steps = [(p, c) for p, c in steps if p == 1]
        if not present_steps:
            rates[case_id] = None  # 无出现步骤
        else:
            correct = sum(1 for p, c in present_steps if c == 1)
            rates[case_id] = correct / len(present_steps)
    return rates


# ============================================================
# 描述性统计（Tier 0 和 Tier 1 共用）
# ============================================================

def descriptive_stats(
    rows: list[dict],
    arm_a: str = "A",
    arm_b: str = "B",
    rater: str = "rater_human",
) -> dict:
    """纯描述性统计，无显著性检验。"""
    cov_a = compute_presence_coverage(rows, arm_a, rater)
    cov_b = compute_presence_coverage(rows, arm_b, rater)

    # 配对 case
    common_cases = sorted(set(cov_a.keys()) & set(cov_b.keys()))

    deltas = {}
    for c in common_cases:
        deltas[c] = cov_b[c] - cov_a[c]

    n = len(common_cases)
    mean_delta = sum(deltas.values()) / n if n > 0 else 0.0
    median_delta = statistics.median(deltas.values()) if n > 0 else 0.0
    # R2_F10 修复：偶数 n 下 statistics.median 返回中间两个值的平均，
    # 而非上中位数。例: [0,0,1,1] → 0.5（正确），而非 1.0（旧实现）

    # 方向一致性
    b_better = sum(1 for d in deltas.values() if d > 0)
    a_better = sum(1 for d in deltas.values() if d < 0)
    tied = sum(1 for d in deltas.values() if d == 0)

    return {
        "n_pairs": n,
        "arm_a_label": arm_a,
        "arm_b_label": arm_b,
        "rater": rater,
        "mean_coverage_a": sum(cov_a.values()) / len(cov_a) if cov_a else 0.0,
        "mean_coverage_b": sum(cov_b.values()) / len(cov_b) if cov_b else 0.0,
        "median_delta": median_delta,
        "mean_delta": mean_delta,
        "direction": {
            "b_better": b_better,
            "a_better": a_better,
            "tied": tied,
        },
        "per_case": {
            c: {
                "coverage_a": cov_a.get(c),
                "coverage_b": cov_b.get(c),
                "delta": deltas.get(c),
            }
            for c in common_cases
        },
    }


# ============================================================
# Wilcoxon signed-rank + bootstrap CI（Tier 1）
# ============================================================

def wilcoxon_signed_rank(deltas: list[float]) -> dict:
    """配对 Wilcoxon signed-rank 检验。需要 scipy。"""
    try:
        from scipy.stats import wilcoxon
        # 过滤 delta=0 的 tied pairs
        nonzero = [d for d in deltas if d != 0]
        if len(nonzero) < 5:
            return {
                "test": "Wilcoxon signed-rank",
                "statistic": None,
                "p_value": None,
                "n_nonzero": len(nonzero),
                "warning": "非零差值对 < 5，统计功效不足，仅报告描述性结果",
            }
        stat, p = wilcoxon(nonzero)
        # scipy 的 wilcoxon 可能返回多种格式
        if hasattr(p, 'pvalue'):
            p = p.pvalue
        return {
            "test": "Wilcoxon signed-rank",
            "statistic": float(stat) if hasattr(stat, '__float__') else stat,
            "p_value": float(p) if hasattr(p, '__float__') else p,
            "n_nonzero": len(nonzero),
        }
    except ImportError:
        return {
            "test": "Wilcoxon signed-rank",
            "error": "scipy 未安装。安装: pip install scipy",
        }


def bootstrap_median_ci(deltas: list[float], n_bootstrap: int = 10000,
                        ci_level: float = 0.95) -> dict:
    """Bootstrap 中位数差值置信区间。"""
    import random
    random.seed(42)

    n = len(deltas)
    if n < 5:
        return {"error": "样本量 < 5，不执行 bootstrap"}

    medians = []
    for _ in range(n_bootstrap):
        sample = [random.choice(deltas) for _ in range(n)]
        medians.append(statistics.median(sample))

    medians.sort()
    alpha = (1 - ci_level) / 2
    lo_idx = int(alpha * n_bootstrap)
    hi_idx = int((1 - alpha) * n_bootstrap)

    return {
        "n_bootstrap": n_bootstrap,
        "ci_level": ci_level,
        "median": statistics.median(deltas),
        "ci_lower": medians[lo_idx],
        "ci_upper": medians[hi_idx],
    }


# ============================================================
# Cohen's κ
# ============================================================

def cohens_kappa(rater1: list[int], rater2: list[int]) -> dict:
    """计算二分类 Cohen's κ。"""
    n = len(rater1)
    if n != len(rater2) or n == 0:
        return {"error": "评分者数据长度不匹配或为空"}

    # 混淆矩阵
    a = sum(1 for i in range(n) if rater1[i] == 1 and rater2[i] == 1)
    b = sum(1 for i in range(n) if rater1[i] == 1 and rater2[i] == 0)
    c = sum(1 for i in range(n) if rater1[i] == 0 and rater2[i] == 1)
    d = sum(1 for i in range(n) if rater1[i] == 0 and rater2[i] == 0)

    total = a + b + c + d
    if total == 0:
        return {"error": "无有效评分"}

    p_o = (a + d) / total  # observed agreement
    # expected agreement
    p_yes = ((a + b) / total) * ((a + c) / total)
    p_no = ((c + d) / total) * ((b + d) / total)
    p_e = p_yes + p_no

    if p_e == 1.0:
        # R2_F12 修复: 全 0/全 1 时 κ 分母为 0，κ 不可估计
        # 不应设为 1.0（那会误报"几乎完全一致"）
        return {
            "kappa": None,
            "observed_agreement": round(p_o, 4),
            "expected_agreement": 1.0,
            "n_ratings": total,
            "confusion_matrix": {"a": a, "b": b, "c": c, "d": d},
            "warning": "kappa undefined — one or both marginal distributions are degenerate (all 0 or all 1). Report observed agreement only.",
            "interpretation": "不可估计 (degenerate marginals)",
        }
    kappa = (p_o - p_e) / (1 - p_e)

    return {
        "kappa": round(kappa, 4),
        "observed_agreement": round(p_o, 4),
        "expected_agreement": round(p_e, 4),
        "n_ratings": total,
        "confusion_matrix": {"a": a, "b": b, "c": c, "d": d},
        "interpretation": _interpret_kappa(kappa),
    }


def _interpret_kappa(kappa: float) -> str:
    if kappa < 0.0:   return "低于偶然一致"
    if kappa < 0.2:   return "轻微一致 (slight)"
    if kappa < 0.4:   return "一般一致 (fair)"
    if kappa < 0.6:   return "中等一致 (moderate) — 低于接受门槛"
    if kappa < 0.8:   return "高度一致 (substantial)"
    return "几乎完全一致 (almost perfect)"


def compute_all_kappas(rows: list[dict],
                       rater_a: str = "rater_human",
                       rater_b: str = "rater_codex") -> dict:
    """对每个 step 计算评分者间 κ。"""
    # 聚合：每个 step 的所有评分
    step_ratings: dict[str, dict[str, list[int]]] = defaultdict(
        lambda: defaultdict(list)
    )
    for r in rows:
        step_ratings[r["step"]][r["rater"]].append((r["case_id"], r["prompt_arm"], r["presence"]))

    results = {}
    for step, rater_data in step_ratings.items():
        ratings_a = rater_data.get(rater_a, [])
        ratings_b = rater_data.get(rater_b, [])

        # 按 (case_id, arm) 对齐
        key_to_presence_a = {(c, arm): p for c, arm, p in ratings_a}
        key_to_presence_b = {(c, arm): p for c, arm, p in ratings_b}

        common_keys = sorted(set(key_to_presence_a.keys()) & set(key_to_presence_b.keys()))
        if not common_keys:
            results[step] = {"error": "无共同评分项"}
            continue

        a_list = [key_to_presence_a[k] for k in common_keys]
        b_list = [key_to_presence_b[k] for k in common_keys]

        results[step] = cohens_kappa(a_list, b_list)

    return results


# ============================================================
# 主分析
# ============================================================

def load_test_set_splits(test_set_path: Optional[str]) -> dict[str, str]:
    """
    从 test_set.json 加载每个 case 的 split 标签 (train/test)。
    返回 {case_id: split}。若文件不存在或无 split 字段，返回空 dict。
    """
    if not test_set_path:
        return {}
    p = Path(test_set_path)
    if not p.exists():
        return {}
    with open(p, "r", encoding="utf-8") as f:
        ts = json.load(f)
    splits = {}
    for t in ts.get("tests", []):
        if "id" in t and "split" in t:
            splits[t["id"]] = t["split"]
    return splits


def get_expected_steps(test_set_path: Optional[str]) -> Optional[dict[str, list[str]]]:
    """
    从 test_set.json 读取每个 case 的 expected_steps，用于校验完整网格。
    返回 {case_id: [step_name, ...]}。
    """
    if not test_set_path:
        return None
    p = Path(test_set_path)
    if not p.exists():
        return None
    with open(p, "r", encoding="utf-8") as f:
        ts = json.load(f)
    expected = {}
    for t in ts.get("tests", []):
        if "id" in t and "expected_steps" in t:
            steps = []
            for phase in t["expected_steps"].values():
                steps.extend(phase)
            expected[t["id"]] = steps
    return expected if expected else None


def validate_grid(rows: list[dict], expected_steps: dict[str, list[str]],
                  arms: list[str], raters: list[str]) -> list[str]:
    """
    校验完整网格: case_id × arm × rater × expected_step。
    返回缺失项列表（空列表 = 通过）。
    """
    missing = []

    # 构建已有的 (case_id, arm, rater, step) 集合
    existing = set()
    for r in rows:
        existing.add((r["case_id"], r["prompt_arm"], r["rater"], r["step"]))

    cases = sorted(expected_steps.keys())
    for case_id in cases:
        for arm in arms:
            for rater in raters:
                for step in expected_steps[case_id]:
                    key = (case_id, arm, rater, step)
                    if key not in existing:
                        missing.append(f"{case_id}/{arm}/{rater}/{step}")

    return missing


def sign_test(deltas: list[float]) -> dict:
    """
    配对符号检验 (exact sign test)。
    双侧 p = 2 × min(P(X ≥ n_positive), P(X ≤ n_positive))
    其中 X ~ Binomial(n_nonzero, 0.5)
    """
    nonzero = [d for d in deltas if d != 0]
    n = len(nonzero)
    if n < 5:
        return {
            "test": "sign test",
            "n_nonzero": n,
            "warning": "非零差值对 < 5，不执行符号检验",
        }

    n_positive = sum(1 for d in nonzero if d > 0)

    # exact binomial CDF
    import math
    def binom_pmf(k, nn, p=0.5):
        return math.comb(nn, k) * (p ** k) * ((1 - p) ** (nn - k))

    # P(X ≤ n_positive) under H0: p=0.5
    p_le = sum(binom_pmf(k, n) for k in range(0, n_positive + 1))
    p_ge = sum(binom_pmf(k, n) for k in range(n_positive, n + 1))
    p_two_sided = 2 * min(p_le, p_ge)
    p_two_sided = min(p_two_sided, 1.0)

    return {
        "test": "sign test (exact binomial)",
        "n_nonzero": n,
        "n_positive": n_positive,
        "n_negative": n - n_positive,
        "p_value": round(p_two_sided, 6),
    }


def kappa_bootstrap_ci(rater1: list[int], rater2: list[int],
                       n_bootstrap: int = 5000) -> dict:
    """Bootstrap 95% CI for Cohen's κ。"""
    import random
    random.seed(42)
    n = len(rater1)
    if n < 5:
        return {"error": "样本量 < 5"}

    kappas = []
    for _ in range(n_bootstrap):
        idx = [random.randint(0, n - 1) for _ in range(n)]
        s1 = [rater1[i] for i in idx]
        s2 = [rater2[i] for i in idx]
        k = cohens_kappa(s1, s2)
        if k.get("kappa") is not None:
            kappas.append(k["kappa"])

    if not kappas:
        return {"error": "bootstrap 未产生有效 κ 值"}

    kappas.sort()
    alpha = 0.05
    lo = int(alpha / 2 * len(kappas))
    hi = int((1 - alpha / 2) * len(kappas))

    return {
        "n_bootstrap": n_bootstrap,
        "mean_kappa": statistics.mean(kappas),
        "ci_lower": kappas[lo],
        "ci_upper": kappas[hi],
    }


def compute_all_kappas_with_ci(rows: list[dict],
                               rater_a: str = "rater_human",
                               rater_b: str = "rater_codex") -> dict:
    """对每个 step 计算 κ + bootstrap 95% CI。"""
    step_ratings: dict[str, dict[str, list[int]]] = defaultdict(
        lambda: defaultdict(list)
    )
    for r in rows:
        step_ratings[r["step"]][r["rater"]].append(
            (r["case_id"], r["prompt_arm"], r["presence"])
        )

    results = {}
    for step, rater_data in step_ratings.items():
        ratings_a = rater_data.get(rater_a, [])
        ratings_b = rater_data.get(rater_b, [])

        key_to_a = {(c, arm): p for c, arm, p in ratings_a}
        key_to_b = {(c, arm): p for c, arm, p in ratings_b}

        common_keys = sorted(set(key_to_a.keys()) & set(key_to_b.keys()))
        if not common_keys:
            results[step] = {"error": "无共同评分项"}
            continue

        a_list = [key_to_a[k] for k in common_keys]
        b_list = [key_to_b[k] for k in common_keys]

        k_result = cohens_kappa(a_list, b_list)
        if k_result.get("kappa") is not None:
            k_result["kappa_ci"] = kappa_bootstrap_ci(a_list, b_list)
        results[step] = k_result

    return results


def analyze(rows: list[dict], tier: int = 0,
            arm_a: str = "A", arm_b: str = "B",
            rater_primary: str = "rater_human",
            rater_secondary: str = "rater_codex",
            test_set_path: Optional[str] = None,
            categories: Optional[list[str]] = None) -> dict:
    """主分析入口。"""
    result: dict = {
        "meta": {
            "analyzed_at": datetime.now(timezone.utc).isoformat(),
            "tier": tier,
            "n_rows": len(rows),
            "arms": [arm_a, arm_b],
            "raters": list(set(r["rater"] for r in rows)),
        }
    }

    # ---- R2_F9: split 过滤 ----
    splits = load_test_set_splits(test_set_path)
    if tier >= 1:
        if not splits:
            result["error"] = (
                "Tier 1 需要 test_set.json 中的 split 字段来过滤 train/test。"
                "请用 --test-set 参数指定 test_set.json 路径。"
            )
            return result
        test_ids = {cid for cid, s in splits.items() if s == "test"}
        if not test_ids:
            result["error"] = "test_set.json 中没有 split=='test' 的用例"
            return result
        rows_test = [r for r in rows if r["case_id"] in test_ids]
        if not rows_test:
            result["error"] = f"过滤后无 test 集数据。test_ids={test_ids}"
            return result
        result["meta"]["split_filter"] = "test_only"
        result["meta"]["n_test_cases"] = len(test_ids)
        result["meta"]["n_rows_after_filter"] = len(rows_test)
        rows_for_analysis = rows_test
    else:
        if splits:
            result["meta"]["split_filter"] = "none (Tier 0, all data)"
        rows_for_analysis = rows

    # ---- R2_F11: 完整网格校验 ----
    expected_steps = get_expected_steps(test_set_path)
    if expected_steps:
        raters_present = list(set(r["rater"] for r in rows_for_analysis))
        arms_present = [arm_a, arm_b]
        # 只校验 test set 中的 case（如果提供了 splits）
        if splits and tier >= 1:
            expected_steps = {k: v for k, v in expected_steps.items()
                            if k in test_ids}
        missing_grid = validate_grid(rows_for_analysis, expected_steps,
                                     arms_present, raters_present)
        if missing_grid:
            result["error"] = (
                f"网格校验失败: {len(missing_grid)} 个预期项缺失。"
                f"示例: {missing_grid[:5]}。"
                f"请确保 scoresheet 包含所有 case × arm × rater × step 组合。"
            )
            result["missing_grid"] = missing_grid[:20]
            return result
        result["meta"]["grid_validation"] = "passed"
        result["meta"]["n_expected_steps_per_case"] = {
            k: len(v) for k, v in expected_steps.items()
        }

    # ---- 描述性统计 ----
    desc = descriptive_stats(rows_for_analysis, arm_a, arm_b, rater_primary)
    result["descriptive"] = desc

    # ---- κ + CI ----
    raters_in_data = set(r["rater"] for r in rows_for_analysis)
    if rater_secondary in raters_in_data:
        kappas = compute_all_kappas_with_ci(
            rows_for_analysis, rater_primary, rater_secondary
        )
        result["kappa"] = kappas
        valid_kappas = [v["kappa"] for v in kappas.values()
                       if "kappa" in v and v["kappa"] is not None]
        result["kappa_summary"] = {
            "n_steps": len(kappas),
            "n_valid": len(valid_kappas),
            "n_undefined": len(kappas) - len(valid_kappas),
            "mean_kappa": statistics.mean(valid_kappas) if valid_kappas else None,
            "min_kappa": min(valid_kappas) if valid_kappas else None,
            "pass_threshold_0_6": (
                all(k >= 0.6 for k in valid_kappas)
                if valid_kappas and len(valid_kappas) == len(kappas)
                else False
            ),
            "note": (
                "有 undefined κ (degenerate marginals)，已从 pass_threshold 中排除"
                if len(valid_kappas) < len(kappas) and valid_kappas
                else None
            ),
        }

    # ---- correctness_rate ----
    corr_a = compute_correctness_rate(rows_for_analysis, arm_a, rater_primary)
    corr_b = compute_correctness_rate(rows_for_analysis, arm_b, rater_primary)
    common_corr = sorted(set(corr_a.keys()) & set(corr_b.keys()))
    if common_corr:
        corr_deltas = {}
        for c in common_corr:
            if corr_a[c] is not None and corr_b[c] is not None:
                corr_deltas[c] = corr_b[c] - corr_a[c]
        valid_corr = [v for v in corr_deltas.values() if v != 0]
        result["correctness"] = {
            "mean_rate_a": statistics.mean(
                [v for v in corr_a.values() if v is not None]) if corr_a else None,
            "mean_rate_b": statistics.mean(
                [v for v in corr_b.values() if v is not None]) if corr_b else None,
            "median_delta": statistics.median(corr_deltas.values()) if corr_deltas else None,
            "n_comparable": len(corr_deltas),
        }

    # ---- Tier 1: 推断统计 ----
    if tier >= 1:
        all_deltas = [desc["per_case"][c]["delta"] for c in desc["per_case"]]
        # Sign test (更稳健的主检验)
        result["sign_test"] = sign_test(all_deltas)

        # Wilcoxon (敏感度检查)
        nonzero_deltas = [d for d in all_deltas if d != 0]
        if len(nonzero_deltas) >= 5:
            result["wilcoxon"] = wilcoxon_signed_rank(all_deltas)
            result["bootstrap"] = bootstrap_median_ci(all_deltas)
        else:
            result["wilcoxon"] = {"warning": "非零差值对 < 5，仅报告描述性结果"}

        # ---- 分层分析 ----
        if categories:
            stratified = {}
            for cat in categories:
                cat_cases = {t["id"] for t in json.load(
                    open(test_set_path, "r", encoding="utf-8")
                ).get("tests", []) if t.get("category") == cat}
                cat_rows = [r for r in rows_for_analysis
                           if r["case_id"] in cat_cases]
                if cat_rows:
                    d = descriptive_stats(cat_rows, arm_a, arm_b, rater_primary)
                    stratified[cat] = {
                        "n_pairs": d["n_pairs"],
                        "median_delta": d["median_delta"],
                        "direction": d["direction"],
                    }
            result["stratified"] = stratified

    return result


# ============================================================
# 报告输出
# ============================================================

def print_report(result: dict) -> None:
    """终端友好输出。"""
    desc = result["descriptive"]
    print()
    print("=" * 60)
    print("  实验分析报告")
    print(f"  Tier: {result['meta']['tier']}")
    print(f"  分析时间: {result['meta']['analyzed_at'][:19]}")
    print("=" * 60)

    print(f"\n  配对样本数: {desc['n_pairs']}")
    print(f"  {desc['arm_a_label']} 组平均 coverage: {desc['mean_coverage_a']:.3f}")
    print(f"  {desc['arm_b_label']} 组平均 coverage: {desc['mean_coverage_b']:.3f}")
    print(f"  中位数 Δ: {desc['median_delta']:+.3f}")
    print(f"  方向: {desc['direction']['b_better']} 例 B 更优 / "
          f"{desc['direction']['a_better']} 例 A 更优 / "
          f"{desc['direction']['tied']} 例持平")

    # 逐条矩阵
    print(f"\n  Per-case:")
    print(f"  {'Case':<20} {'A':>8} {'B':>8} {'Δ':>8}")
    print(f"  {'-'*44}")
    for c, v in desc["per_case"].items():
        print(f"  {c:<20} {v['coverage_a'] or 0:>8.3f} "
              f"{v['coverage_b'] or 0:>8.3f} {v['delta'] or 0:>+8.3f}")

    # κ
    if "kappa_summary" in result:
        ks = result["kappa_summary"]
        print(f"\n  Cohen's κ (评分者间信度):")
        print(f"  步骤数: {ks['n_steps']}, 有效 κ 数: {ks['n_valid']}, 不可估计: {ks.get('n_undefined', 0)}")
        if ks['mean_kappa'] is not None:
            print(f"  平均 κ: {ks['mean_kappa']:.3f}")
        if ks.get('note'):
            print(f"  备注: {ks['note']}")
        print(f"  κ ≥ 0.6: {'[PASS]' if ks['pass_threshold_0_6'] else '[FAIL] — rubric 需重设计或 undefined κ 需人工审查'}")

    # Correctness
    if "correctness" in result:
        cr = result["correctness"]
        if cr["median_delta"] is not None:
            print(f"\n  Correctness rate (次因变量):")
            print(f"  A 组: {cr['mean_rate_a']:.3f}  B 组: {cr['mean_rate_b']:.3f}  "
                  f"Δ: {cr['median_delta']:+.3f}")

    # Sign test (Tier 1 primary)
    if "sign_test" in result:
        st = result["sign_test"]
        if "p_value" in st:
            sig = "显著" if st["p_value"] < 0.05 else "不显著"
            print(f"\n  Sign test (主检验): p={st['p_value']:.4f} ({sig})")
            print(f"  非零对: {st['n_nonzero']}, B更优: {st['n_positive']}, "
                  f"A更优: {st['n_negative']}")

    # Wilcoxon
    if "wilcoxon" in result:
        w = result["wilcoxon"]
        if "p_value" in w:
            sig = "显著" if w["p_value"] < 0.05 else "不显著"
            print(f"  Wilcoxon (敏感度检查): p={w['p_value']:.4f} ({sig})")
        elif "warning" in w:
            print(f"  Wilcoxon: {w['warning']}")

    # Bootstrap
    if "bootstrap" in result:
        b = result["bootstrap"]
        if "ci_lower" in b:
            print(f"  Bootstrap 95% CI: [{b['ci_lower']:+.3f}, {b['ci_upper']:+.3f}] "
                  f"(median={b['median']:+.3f})")

    # Stratified
    if "stratified" in result and result["stratified"]:
        print(f"\n  分层分析:")
        for cat, s in result["stratified"].items():
            print(f"  {cat}: n={s['n_pairs']}, median Δ={s['median_delta']:+.3f}, "
                  f"B更优={s['direction']['b_better']}")

    # 判定
    print(f"\n  {'─' * 60}")
    print(f"  判定逻辑（对照 §9 分析计划）:")
    print(f"  1. 方向一致性: {'[PASS]' if desc['direction']['b_better'] > desc['direction']['a_better'] else '[CHECK]'}")
    if "kappa_summary" in result:
        print(f"  2. κ ≥ 0.6:    {'[PASS]' if result['kappa_summary']['pass_threshold_0_6'] else '[FAIL]'}")
    if result["meta"]["tier"] >= 1:
        threshold = 0.15
        above_threshold = abs(desc['median_delta']) >= threshold
        st_passed = ("sign_test" in result and "p_value" in result["sign_test"]
                    and result["sign_test"]["p_value"] < 0.05)
        print(f"  3. |Δ| ≥ 15pp: {'[PASS]' if above_threshold else '[FAIL]'} "
              f"(|{desc['median_delta']:.3f}| {'≥' if above_threshold else '<'} {threshold})")
        print(f"  4. Sign test:  {'[PASS]' if st_passed else '[FAIL]'} "
              f"(p={result.get('sign_test', {}).get('p_value', 'N/A')})")


# ============================================================
# CLI
# ============================================================

def main():
    parser = argparse.ArgumentParser(
        description="实验分析脚本 — 读取双评分者 scoresheet.csv，输出配对比较和 κ。",
    )
    parser.add_argument("scoresheet", help="scoresheet.csv 路径")
    parser.add_argument("--tier", "-t", type=int, default=0, choices=[0, 1],
                        help="分析层级: 0=仅描述性, 1=含 Wilcoxon+bootstrap+sign_test+κ (默认: 0)")
    parser.add_argument("--test-set", default=None,
                        help="test_set.json 路径（Tier 1 必需：提供 split 和 expected_steps）")
    parser.add_argument("--arm-a", default="A", help="A 组标签 (默认: A)")
    parser.add_argument("--arm-b", default="B", help="B 组标签 (默认: B)")
    parser.add_argument("--rater-primary", default="rater_human",
                        help="主评分者标签 (默认: rater_human)")
    parser.add_argument("--rater-secondary", default="rater_codex",
                        help="第二评分者标签 (默认: rater_codex)")
    parser.add_argument("--categories", nargs="*", default=None,
                        help="分层分析的类别列表 (如: off_by_one null_pointer)")
    parser.add_argument("--output", "-o", default=None,
                        help="JSON 输出路径")
    parser.add_argument("--report", "-r", default=None,
                        help="Markdown 报告输出路径")
    args = parser.parse_args()

    # Tier 1 强制要求 --test-set
    if args.tier >= 1 and not args.test_set:
        print("错误: Tier 1 需要 --test-set 参数来过滤 train/test split")
        print("用法: python analyze_experiment.py scores.csv --tier 1 --test-set test_set.json")
        sys.exit(1)

    # 加载
    path = Path(args.scoresheet)
    if not path.exists():
        print(f"错误: 文件不存在: {path}")
        sys.exit(1)

    rows = load_scoresheet(str(path))
    if not rows:
        print("错误: scoresheet 为空")
        sys.exit(1)

    print(f"加载 {len(rows)} 条评分记录")
    print(f"  Arms: {set(r['prompt_arm'] for r in rows)}")
    print(f"  Raters: {set(r['rater'] for r in rows)}")
    print(f"  Steps: {len(set(r['step'] for r in rows))}")

    # 分析
    result = analyze(
        rows, tier=args.tier,
        arm_a=args.arm_a, arm_b=args.arm_b,
        rater_primary=args.rater_primary,
        rater_secondary=args.rater_secondary,
        test_set_path=args.test_set,
        categories=args.categories,
    )

    # 检查是否有致命错误
    if "error" in result:
        print(f"\n[FAIL] 分析中止: {result['error']}")
        if "missing_grid" in result:
            print("  缺失项示例:")
            for m in result["missing_grid"][:10]:
                print(f"    - {m}")
        sys.exit(1)

    # 输出
    print_report(result)

    # 保存 JSON
    output_path = args.output
    if not output_path:
        stem = path.stem
        output_path = str(path.parent / f"analysis_{stem}.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    print(f"\n  JSON 已保存: {output_path}")

    # 可选 Markdown 报告
    if args.report:
        _write_md_report(result, args.report)
        print(f"  MD 报告已保存: {args.report}")


def _write_md_report(result: dict, path: str) -> None:
    """写 Markdown 格式报告。"""
    desc = result["descriptive"]
    lines = [
        "# 实验分析报告",
        "",
        f"> 分析时间: {result['meta']['analyzed_at'][:19]}",
        f"> Tier: {result['meta']['tier']}",
        f"> 配对数: {desc['n_pairs']}",
        "",
        "## 主结果",
        "",
        f"| 指标 | {desc['arm_a_label']} 组 | {desc['arm_b_label']} 组 | Δ |",
        f"|---|---|---|---|",
        f"| 平均 coverage | {desc['mean_coverage_a']:.3f} | {desc['mean_coverage_b']:.3f} | {desc['mean_delta']:+.3f} |",
        f"| 中位数 coverage | — | — | {desc['median_delta']:+.3f} |",
        "",
        f"- B 更优: {desc['direction']['b_better']} 例",
        f"- A 更优: {desc['direction']['a_better']} 例",
        f"- 持平:   {desc['direction']['tied']} 例",
    ]

    if "kappa_summary" in result:
        ks = result["kappa_summary"]
        lines += [
            "",
            "## 评分者间信度",
            "",
            f"- 平均 κ: {ks['mean_kappa']:.3f}",
            f"- κ ≥ 0.6: {'[PASS]' if ks['pass_threshold_0_6'] else '[FAIL]'}",
        ]

    if "wilcoxon" in result and "p_value" in result["wilcoxon"]:
        w = result["wilcoxon"]
        lines += [
            "",
            f"## 统计检验",
            "",
            f"- Wilcoxon signed-rank: p = {w['p_value']:.4f}",
        ]

    if "bootstrap" in result and "ci_lower" in result["bootstrap"]:
        b = result["bootstrap"]
        lines += [
            f"- Bootstrap 95% CI: [{b['ci_lower']:+.3f}, {b['ci_upper']:+.3f}]",
        ]

    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


if __name__ == "__main__":
    main()
