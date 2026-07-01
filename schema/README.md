# 数据契约 / Data Schema

## scoresheet.csv

实验评分数据。`analyze_experiment.py` 的输入。

| 列名 | 类型 | 说明 |
|------|------|------|
| `case_id` | str | 用例唯一标识 |
| `prompt_arm` | str | 分组标签：`A` 或 `B` |
| `rater` | str | 评分者标识 |
| `step` | str | 被评分的步骤/维度名 |
| `presence` | int | 0/1 — 该步骤是否被覆盖 |
| `correctness` | int | 0/1 — 该步骤是否正确 |
| `note` | str | 评分备注（可选） |

## test_set.json

测试用例定义。对照实验的冻结输入。

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

## .lock 文件（预注册锁）

实验执行前冻结的元数据文件。包含：

- `hypothesis`: 假设声明
- `analysis_plan`: 分析计划（检验方法、效应量阈值、停止规则）
- `test_set_sha256`: test_set.json 的 SHA256 hash——git commit 后不可修改
