# A2: Controlled Experiment on prep/exec/post Segmented Prompts

> **Role**: **Main case**: demonstrates the complete controlled experiment pipeline  
> **Status**: CLOSED [E-] (ceiling-limited, science gate FAIL)  
> **Review**: Codex GPT-5.5 ×4 + Qwen3.7-Max ×3 + Kimi-K2.7 ×1, 0 unclosed findings  
> **Cross-model replication**: Qwen3.7-Max (48/48 collected, Codex blind scoring Δ=−0.014, direction consistent)

---

## Experiment Design

| Parameter | Value |
|------|-----|
| Task domain | Code review |
| Research question | Is the prep/exec/post segmented format better than a single numbered list? |
| Arm A (control) | Single numbered-list prompt |
| Arm B (experimental) | prep/exec/post segmented prompt |
| Primary DV | correctness_rate (0-1 continuous proportion) |
| Model | GPT-5.5 temp=0 (Codex CLI) |
| Sample size | n=24/arm (stratified train/test split) |

### Design Documents

- Experiment design: `design/a2_revised_experiment_design_v2.md` (source repository)
- Two prompt arms: [`prompt_A.md`](prompt_A.md) / [`prompt_B.md`](prompt_B.md)

---

## Results

### Engineering Gate: PASS ✅
Data collection was normal, the scoring script was correct, and the manifest was complete.

### Science Gate: FAIL ❌

> **Note**: All numbers below are test-set-only (n_test=12/arm). The source experiment used a stratified train/test split: train was used only for prompt iteration, and test was used for hypothesis testing.

| Gate | Result |
|----|------|
| Statistical significance | FAIL (n_nonzero=4 < 5, insufficient Wilcoxon power) |
| Effect size | Δ=0.019 (far below the minimum threshold of interest) |
| Direction consistency | FAIL (A=0.954 > B=0.935, opposite to H1) |
| Inter-rater reliability | FAIL (κ did not reach the threshold; exec_severity dimension inconsistency rate 37.5%) |

**Overall**: The format effect is undetectable in the GPT-5.5 temp=0 code-review domain. Maturity: [E-] ceiling-limited.

### Qwen Cross-Model Replication
- Qwen3.7-Max replication: A=0.806, B=0.792, Δ=−0.014
- Direction consistent (both negative); presence ceiling replicated

---

## Key Lessons

1. **Sample-size planning error**: scoring disagreements led to n_nonzero < 5, so Wilcoxon could not be run. Lesson: use n_nonzero_expected rather than n_total for power analysis
2. **Rater disagreement**: GPT-5.5 and DeepSeek-V4-Pro had a 37.5% inconsistency rate on the exec_severity dimension
3. **IV contamination**: Arm B actually contained check dimensions not present in Arm A (INVENTORY not equivalent)
4. **Anti-fabrication tests exposed model tendency**: GPT-5.5 fabricated defects in bug-free code

---

## Data Files

- [`test_set.json`](test_set.json) — 24 test cases (stratified train/test)
- [`scoresheet.csv`](scoresheet.csv) — dual-rater scoring data
- [`prompt_A.md`](prompt_A.md) / [`prompt_B.md`](prompt_B.md) — two prompt arms

### Reproduction Commands

```bash
python analyze_experiment.py scoresheet.csv --tier 0
python analyze_experiment.py scoresheet.csv --tier 1 --test-set test_set.json
```

---

*Original experiment execution: 2026-06-17 ~ 2026-06-20 · Source repository: prompt-tdd*

*English translation: GPT-5.5 (via Codex CLI) · 2026-07-01*
