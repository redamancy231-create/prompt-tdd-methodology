# 資料契約 / Data Schema

## scoresheet.csv

實驗評分資料。`analyze_experiment.py` 的輸入。

| 欄位 | 型別 | 說明 |
|------|------|------|
| `case_id` | str | 用例唯一識別碼 |
| `prompt_arm` | str | 分組標籤：`A` 或 `B` |
| `rater` | str | 評分者識別碼 |
| `step` | str | 被評分的步驟/維度名 |
| `presence` | int | 0/1 — 該步驟是否被覆蓋 |
| `correctness` | int | 0/1 — 該步驟是否正確 |
| `note` | str | 評分備註（可選） |

## test_set.json

測試用例定義。對照實驗的凍結輸入。

```json
{
  "cases": [
    {
      "id": "case_001",
      "description": "...",
      "expected_steps": ["step_a", "step_b"],
      "split": "train"
    }
  ],
  "metadata": {
    "domain": "代码审查 | 路由决策 | ...",
    "model": "GPT-5.5",
    "temperature": 0,
    "date": "YYYY-MM-DD"
  }
}
```

## .lock 檔案（預註冊鎖）

實驗執行前凍結的後設資料檔案。包含：

- `hypothesis`: 假設宣告
- `analysis_plan`: 分析計劃（檢驗方法、效應量閾值、停止規則）
- `test_set_sha256`: test_set.json 的 SHA256 hash——git commit 後不可修改
