# A2: prep/exec/post 分段 prompt 對照實驗

> **角色**: **主案例**——展示完整的對照實驗管線  
> **狀態**: CLOSED [E-]（ceiling-limited，科學門 FAIL）  
> **審查**: Codex GPT-5.5 ×4 + Qwen3.7-Max ×3 + Kimi-K2.7 ×1，0 未閉合發現  
> **跨模型復現**: Qwen3.7-Max（48/48 收集，Codex 盲評 Δ=−0.014，方向一致）

---

## 實驗設計

| 參數 | 值 |
|------|-----|
| 任務域 | 程式碼審查 |
| 研究問題 | prep/exec/post 分段格式是否優於一體式編號列表？ |
| A 組（對照） | 一體式編號列表 prompt |
| B 組（實驗） | prep/exec/post 分段 prompt |
| 主 DV | correctness_rate（0-1 連續比例） |
| 模型 | GPT-5.5 temp=0 (Codex CLI) |
| 樣本量 | n=24/臂（train/test 分層分割） |

### 設計檔案

- 實驗設計: `design/a2_revised_experiment_design_v2.md`（來源倉庫）
- 兩組 prompt: [`prompt_A.md`](prompt_A.md) / [`prompt_B.md`](prompt_B.md)

---

## 結果

### 工程門: PASS ✅
資料收集正常、評分腳本正確、manifest 完整。

### 科學門: FAIL ❌

> **註**：以下數字均為 test-set-only（n_test=12/臂）。原始實驗使用 train/test 分層分割，train 僅用於 prompt 迭代，test 用於假設檢驗。

| 門 | 結果 |
|----|------|
| 統計顯著 | FAIL（n_nonzero=4 < 5，Wilcoxon 功效不足） |
| 效應量 | Δ=0.019（遠低於最小興趣閾值） |
| 方向一致 | FAIL（A=0.954 > B=0.935，方向與 H1 相反） |
| 評分者一致性 | FAIL（κ 未達閾值，exec_severity 維度不一致率 37.5%） |

**整體**: 格式效應在 GPT-5.5 temp=0 程式碼審查域不可檢測。成熟度 [E-] ceiling-limited。

### Qwen 跨模型復現
- Qwen3.7-Max 復現：A=0.806, B=0.792, Δ=−0.014
- 方向一致（均為陰性），presence 天花板復現

---

## 關鍵教訓

1. **樣本量規劃錯誤**：評分分歧導致 n_nonzero < 5，Wilcoxon 無法執行。教訓：功效分析用 n_nonzero_expected 而非 n_total
2. **評分者分歧**：exec_severity 維度上 GPT-5.5 和 DeepSeek-V4-Pro 評分不一致率 37.5%
3. **IV 汙染**：B 組實際包含 A 組沒有的檢查維度（INVENTORY 不等價）
4. **反編造測試暴露模型傾向**：GPT-5.5 在無 bug 程式碼中編造缺陷

---

## 資料檔案

- [`test_set.json`](test_set.json) — 24 條測試用例（train/test 分層）
- [`scoresheet.csv`](scoresheet.csv) — 雙評分者評分資料
- [`prompt_A.md`](prompt_A.md) / [`prompt_B.md`](prompt_B.md) — 兩組 prompt

### 復現命令

```bash
python analyze_experiment.py scoresheet.csv --tier 0
python analyze_experiment.py scoresheet.csv --tier 1 --test-set test_set.json
```

---

*原始實驗執行: 2026-06-17 ~ 2026-06-20 · 來源倉庫: prompt-tdd*
