# A2: prep/exec/post 分段 prompt 对照实验

> **角色**: **主案例**——展示完整的对照实验管线  
> **状态**: CLOSED [E-]（ceiling-limited，科学门 FAIL）  
> **审查**: Codex GPT-5.5 ×4 + Qwen3.7-Max ×3 + Kimi-K2.7 ×1，0 未闭合发现  
> **跨模型复现**: Qwen3.7-Max（48/48 收集，Codex 盲评 Δ=−0.014，方向一致）

---

## 实验设计

| 参数 | 值 |
|------|-----|
| 任务域 | 代码审查 |
| 研究问题 | prep/exec/post 分段格式是否优于一体式编号列表？ |
| A 组（对照） | 一体式编号列表 prompt |
| B 组（实验） | prep/exec/post 分段 prompt |
| 主 DV | correctness_rate（0-1 连续比例） |
| 模型 | GPT-5.5 temp=0 (Codex CLI) |
| 样本量 | n=24/臂（train/test 分层分割） |

### 设计文档

- 实验设计: `design/a2_revised_experiment_design_v2.md`（源仓库）
- 两组 prompt: [`prompt_A.md`](prompt_A.md) / [`prompt_B.md`](prompt_B.md)

---

## 结果

### 工程门: PASS ✅
数据收集正常、评分脚本正确、manifest 完整。

### 科学门: FAIL ❌

> **注**：以下数字均为 test-set-only（n_test=12/臂）。源实验使用 train/test 分层分割，train 仅用于 prompt 迭代，test 用于假设检验。

| 门 | 结果 |
|----|------|
| 统计显著 | FAIL（n_nonzero=4 < 5，Wilcoxon 功效不足） |
| 效应量 | Δ=0.019（远低于最小兴趣阈值） |
| 方向一致 | FAIL（A=0.954 > B=0.935，方向与 H1 相反） |
| 评分者一致性 | FAIL（κ 未达阈值，exec_severity 维度不一致率 37.5%） |

**整体**: 格式效应在 GPT-5.5 temp=0 代码审查域不可检测。成熟度 [E-] ceiling-limited。

### Qwen 跨模型复现
- Qwen3.7-Max 复现：A=0.806, B=0.792, Δ=−0.014
- 方向一致（均为阴性），presence 天花板复现

---

## 关键教训

1. **样本量规划错误**：评分分歧导致 n_nonzero < 5，Wilcoxon 无法执行。教训：功效分析用 n_nonzero_expected 而非 n_total
2. **评分者分歧**：exec_severity 维度上 GPT-5.5 和 DeepSeek-V4-Pro 评分不一致率 37.5%
3. **IV 污染**：B 组实际包含 A 组没有的检查维度（INVENTORY 不等价）
4. **反编造测试暴露模型倾向**：GPT-5.5 在无 bug 代码中编造缺陷

---

## 数据文件

- [`test_set.json`](test_set.json) — 24 条测试用例（train/test 分层）
- [`scoresheet.csv`](scoresheet.csv) — 双评分者评分数据
- [`prompt_A.md`](prompt_A.md) / [`prompt_B.md`](prompt_B.md) — 两组 prompt

### 复现命令

```bash
python analyze_experiment.py scoresheet.csv --tier 0
python analyze_experiment.py scoresheet.csv --tier 1 --test-set test_set.json
```

---

*原始实验执行: 2026-06-17 ~ 2026-06-20 · 源仓库: prompt-tdd*
