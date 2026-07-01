# 啟動前檢查表 (Printable Pre-Flight Checklist)

> 列印或複製此清單。每次啟動新實驗前逐項確認。

---

## 實驗前 (Pre-Experiment)

### 設計門

- [ ] CK1: H0/H1 已明確陳述，統計檢驗方法已指定
- [ ] CK2: DV 定義明確，評分 rubric 已凍結（git commit）
- [ ] CK3: 功效分析完成，min_n_per_arm ≥ 計算值

### 等價性門

- [ ] CK4: 雙組 prompt 產出清單已逐項核對（INVENTORY 等價）
- [ ] CK4: inventory hash 已凍結

### 測試門

- [ ] CK5: test_set.json 已建立，train/test 分割明確
- [ ] CK5: test 集不會用於 prompt 選擇或參數調整
- [ ] CK6: 如 DV 為 0/1 或比例 → 已嵌入天花板探測用例

### 預註冊

- [ ] .lock 檔案已建立（假設 + 分析計劃 + 停止規則 + test_set_sha256）
- [ ] .lock 檔案已 git commit（commit hash: ________）

---

## 實驗中 (During Experiment)

### Tier 0

- [ ] 小樣本（n=4-8/臂）收集完成，無異常
- [ ] 評分腳本執行正確，manifest 完整
- [ ] 描述性統計方向合理，效應量粗略估計
- [ ] **工程門判決**: PASS / FAIL → ________

### Tier 1（僅工程門 PASS 後執行）

- [ ] raw_outputs/ 只增不覆蓋
- [ ] 雙評分者 A（作者模型）執行完畢
- [ ] 雙評分者 B（不同後端）在裸環境中執行完畢
- [ ] 評分前評分者不知分組
- [ ] analyze_experiment.py --tier 1 執行完畢

---

## 實驗後 (Post-Experiment)

### 科學門

- [ ] 統計顯著？ p < ________
- [ ] 效應量 ≥ 最小興趣閾值？ Δ ≥ ________
- [ ] 方向一致？ 方向 = ________
- [ ] **科學門判決**: PASS / FAIL → ________

### 審查

- [ ] 異後端獨立審查 ≥ 1 輪
- [ ] 審查者與實驗執行者不同後端
- [ ] 審查者在裸環境中審閱
- [ ] 審查發現已修正或記錄

### 閉合

- [ ] 成熟度已標註（[E] / [E-] / [F·1域]）
- [ ] 侷限宣告已寫入報告
- [ ] 方法論片段已提取（如有）
- [ ] 陰性結果已誠實報告（如適用）

---

*檢查清單來源：prompt-tdd A2+A3 實驗的實戰方法論*
