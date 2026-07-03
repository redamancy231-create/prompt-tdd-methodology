# Data Contract / Data Schema

## scoresheet.csv

Experiment scoring data. Input to `analyze_experiment.py`.

| Column Name | Type | Description |
|------|------|------|
| `case_id` | str | Unique case identifier |
| `prompt_arm` | str | Group label: `A` or `B` |
| `rater` | str | Rater identifier |
| `step` | str | Step/dimension being scored |
| `presence` | int | 0/1: whether the step was covered |
| `correctness` | int | 0/1: whether the step was correct |
| `note` | str | Scoring note (optional) |

## test_set.json

Test case definition. Frozen input for the controlled experiment.

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
    "domain": "Code review | Routing decision | ...",
    "model": "GPT-5.5",
    "temperature": 0,
    "date": "YYYY-MM-DD"
  }
}
```

## .lock File (Pre-Registration Lock)

Metadata file frozen before experiment execution. Contains:

- `hypothesis`: hypothesis statement
- `analysis_plan`: analysis plan (test method, effect size threshold, stopping rule)
- `test_set_sha256`: SHA256 hash of test_set.json; cannot be modified after git commit

*English translation: GPT-5.5 (via Codex CLI) · 2026-07-01*
