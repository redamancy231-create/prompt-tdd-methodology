# 術語表

| 術語 | 英文 | 定義 |
|------|------|------|
| **Tier 0** | Tier 0 | 小樣本描述性統計階段——驗證工具鏈可行，不升級成熟度 |
| **Tier 1** | Tier 1 | 大樣本推斷統計階段——假設檢驗 + 成熟度升級 |
| **工程門** | Engineering Gate | 判工具鏈可用：資料收集/評分腳本/manifest 完整性 |
| **科學門** | Science Gate | 判假設被支援：統計顯著 + 效應量 ≥ 閾值 + 方向一致（三項全 PASS） |
| **預註冊鎖** | Pre-registration Lock | .lock 檔案——凍結假設/分析計劃/停止規則，git commit 後不可修改 |
| **INVENTORY 等價** | INVENTORY Equivalence | 逐項核對兩組 prompt 產出清單 + hash 凍結，防 IV 汙染 |
| **CK1-CK6** | Checklist 1-6 | 實驗前檢查清單：CK1-CK3 Tier 1 硬門，CK4-CK6 條件觸發 |
| **[Sp]** | Specification | 成熟度——設計草案（初始狀態） |
| **[E]** | Experiment | 成熟度——Tier 1 + 科學門 PASS + 審查閉合 |
| **[E-]** | Experiment (ceiling-limited) | 成熟度——Tier 1 完成 + 科學門 FAIL（陰性/天花板） |
| **[F·1域]** | Framework (single-domain) | 成熟度——寫回框架，標註任務域限制 |
| **DV** | Dependent Variable | 依變項——實驗測量的輸出指標 |
| **IV** | Independent Variable | 自變項——實驗操作的輸入變數（如 prompt 格式） |
| **盲評** | Blind Scoring | 評分者不知道樣本屬於 A 組還是 B 組 |
| **雙 LLM 異後端** | Dual-LLM Cross-Backend | 評分者 A（作者模型）+ 評分者 B（不同後端模型）獨立評分 |
| **HARKing** | Hypothesizing After Results are Known | 看到結果後調整假設——預註冊鎖的對立面 |
| **Cohen's κ** | Cohen's Kappa | 評分者間一致性指標——用於檢測 LLM-LLM 評分分歧 |
| **ceiling probe** | Ceiling Probe | 實驗前探測天花板——嵌入反編造/極端測試用例評估檢測空間 |

*正體中文：OpenCC 轉換 + GPT-5.5 (via Codex CLI) 潤色 · 2026-07-01*
