# Controlled Experiment Design SOP (Prompt Experiment Design SOP)

> **Version**: v1.0.0 (extracted from the prompt-tdd project and generalized into a reusable protocol)  
> **Source**: Practical methodology from the A2+A3 experiments, validated through 17+ rounds of cross-backend review  
> **Generated model**: DeepSeek-V4-Pro (via Claude Code CLI) · 2026-07-01

---

## §1 Pre-Experiment Checklist (CK1-CK6)

### CK1-CK3: Tier 1 Hard Gates (Tier 1 cannot be run if any are missing)

| ID | Check Item | Passing Standard |
|------|--------|---------|
| **CK1** | Falsifiable hypothesis | H0/H1 stated clearly + rejection region defined in advance + statistical test method specified |
| **CK2** | Dependent variable operationalized | DV has a clear definition + measurement protocol is reproducible + scoring rubric is frozen |
| **CK3** | Sufficient sample size | power analysis completed + minimum effect size of interest declared + n ≥ min_n_per_arm |

### CK4-CK6: Conditional Triggers (run selectively based on experiment complexity)

| ID | Check Item | Trigger Condition | Passing Standard |
|------|--------|---------|---------|
| **CK4** | INVENTORY equivalence | When the two prompt arms differ in content | Compare the output inventories from both prompt arms item by item + freeze hashes to prevent IV contamination |
| **CK5** | Train/Test separation | When prompt iteration is needed | The test set is not used for prompt selection or parameter tuning before the experiment ends |
| **CK6** | Ceiling probe | When the DV is 0/1 or a proportional metric | Embed anti-fabrication/extreme test cases to evaluate detection space |

---

## §2 Experiment Pipeline: Tier 0 → Tier 1

### 2.1 Tier 0: Descriptive Statistics (Toolchain Validation)

**Purpose**: Validate that the data collection and scoring pipeline is viable before investing in a large sample.

| Step | Operation | Success Criterion |
|------|------|---------|
| 1. Small-sample collection | n=4-8/arm; manually review each raw output | No data collection anomalies (truncation/timeouts/format errors) |
| 2. Scoring pipeline validation | Run the score script and check manifest completeness | Scoring script runs correctly, with no missing scores |
| 3. Descriptive statistics | `analyze_experiment.py --tier 0` | Directional description + rough effect size estimate |
| 4. Engineering gate decision | Decide whether the pipeline can proceed to Tier 1 | PASS → proceed to Tier 1; FAIL → fix and rerun |

**Tier 0 does not upgrade maturity**. It only validates that "the pipeline works"; it does not provide inferential conclusions.

### 2.2 Tier 1: Inferential Statistics (Hypothesis Testing)

**Prerequisites**: Tier 0 engineering gate PASS + all of CK1-CK3 passed.

| Step | Operation | Key Constraint |
|------|------|---------|
| 1. Large-sample collection | n ≥ the value specified by the power analysis | raw_outputs/ is append-only, never overwritten |
| 2. dual-LLM cross-backend blind scoring | Rater A (author model) + Rater B (different backend) | Rater B has no access to A's scores, author self-evaluation, or material sources |
| 3. Unblind + merge | Merge A/B raters and align by case_id | Group assignment is hidden before scoring |
| 4. Statistical inference | `analyze_experiment.py --tier 1 --test-set test_set.json` | Wilcoxon + bootstrap CI + Cohen's κ |
| 5. Science gate decision | Statistically significant + effect size ≥ minimum threshold of interest + consistent direction | All three PASS → support H1; any FAIL → not supported |

---

## §3 Engineering Gate vs Science Gate

A controlled experiment has two independent gates. Confusing them is one of the most common experiment-design errors.

### Engineering Gate

**What it judges**: Is the toolchain usable?  
**Passing standard**: No data collection anomalies + scoring script runs correctly + manifest completeness check passes  
**After failure**: Fix the toolchain → collect again (an engineering gate failure does not affect the scientific conclusion; it is a pipeline problem, not a hypothesis problem)

### Science Gate

**What it judges**: Is the hypothesis supported?  
**Passing standard**: statistically significant + effect size ≥ minimum threshold of interest + consistent direction + inter-rater reliability meets the standard (Cohen's κ ≥ 0.4 or discordant rate < 25%) (**all four**)  
**After failure**: Record honestly: a negative result ≠ experiment failure. A2/A3 both failed the science gate, but still produced valuable negative evidence and methodology assets.

> **Key lesson**: **engineering gate PASS + science gate FAIL = valid negative evidence**. The maturity label is [E-] (ceiling-limited) rather than [E], but it is still an honestly publishable conclusion.

---

## §4 Pre-Registration Lock (.lock)

### 4.1 Why It Is Needed

To prevent post hoc hypothesis adjustment (HARKing: Hypothesizing After Results are Known).

### 4.2 Lock Contents

```yaml
hypothesis: "<H0/H1 声明>"
analysis_plan:
  test_method: "Wilcoxon signed-rank | sign test | ..."
  effect_size_threshold: <最小兴趣效应量>
  stopping_rule: "<停止规则>"
test_set_sha256: "<SHA256 hash of test_set.json>"
lock_date: "<ISO 8601>"
```

### 4.3 Operation

1. Create the `.lock` file before running the experiment
2. Do not modify it after `git commit` (any modification creates a new commit hash and is traceable)
3. The analysis script automatically verifies the test_set SHA256; mismatch causes a hard fail

---

## §5 INVENTORY Equivalence Protocol

### 5.1 Problem

The two prompt arms in a controlled experiment differ in content. But how do we ensure **information equivalence** rather than a **format effect**?

### 5.2 Protocol

1. Run the A and B prompt arms separately on the same inputs
2. Extract the **check-item inventories** produced by the two prompt arms
3. Compare whether the two inventories cover the same check items, item by item
4. Freeze the inventory hashes
5. If they are not equivalent → revise the prompts until they are equivalent → freeze again

> **A2 lesson**: Differences in INVENTORY equivalence caused IV (prompt format) to be confounded with "information quantity differences": Arm B actually contained check dimensions not present in Arm A.

---

## §6 Maturity Labeling System

| Label | Meaning | Upgrade Condition |
|------|------|---------|
| `[Sp]` | Specification: design draft | Initial state |
| `[E]` | Experiment: experiment executed | Tier 1 completed + science gate PASS + cross-backend review closure |
| `[E-]` | Experiment: ceiling-limited | Tier 1 completed + science gate FAIL (negative or ceiling effect) |
| `[F·1域]` | Framework: single-domain integration | [E] conclusion written back to the framework, with task-domain limits marked |
| `[J]` | Journal: academic publication | Peer reviewed |

**Constraint**: A single-domain experiment can upgrade to at most `[F·1域]`. Cross-domain generalization requires support from ≥2 domain experiments.

---

## §7 Review Closure Protocol

### 7.1 Mandatory Conditions

- Closure may be announced only after ≥1 round of independent cross-backend review
- The reviewer must not use the same backend as the experiment executor
- The reviewer must review in a bare environment (no access to experiment execution records, author self-evaluation, or intermediate versions)

### 7.2 Review Focus

| Review Dimension | Check Content |
|---------|---------|
| Design soundness | Did all CK1-CK6 checks pass? |
| Execution correctness | Did the engineering gate PASS? Is the pre-registration lock valid? |
| Analysis correctness | Is the statistical method appropriate? Do conclusions stay within the effect size range? |
| Honest reporting | Are negative results reported truthfully? Are limitations stated sufficiently? |

---

## §8 Common Failure Modes

### 8.1 Ceiling Effect
**Phenomenon**: The model is near-perfect → effect size cannot be detected  
**Detection**: CK6 ceiling probe (embed anti-fabrication/extreme test cases)  
**Handling**: Honestly label [E-] ceiling-limited. This is a valid conclusion, not a failure.

### 8.2 IV Contamination
**Phenomenon**: The prompt information quantity in the control arm is not equivalent → what is detected is an information-quantity effect, not a format effect  
**Detection**: CK4 INVENTORY equivalence protocol  
**Handling**: Revise prompts until they are equivalent → freeze again

### 8.3 Rater Disagreement
**Phenomenon**: Two LLM raters give different scores for the same case  
**Detection**: Cohen's κ < 0.4 or a high discordant rate  
**Handling**: Use a conservative scoring strategy (take the lower score); known limitation: LLM-LLM scoring ≠ human scoring accuracy

### 8.4 HARKing
**Phenomenon**: Adjusting the hypothesis after seeing the results  
**Detection**: The git commit timestamp of the .lock file is before experiment execution  
**Handling**: A pre-registration lock + all four science gate items PASS are required before claiming "supports H1"

### 8.5 DV Degradation (A3v2 Lesson)
**Phenomenon**: DV selection gradually degrades during experiment iteration: from the original construct validity concern to, in later versions, "as long as we can obtain data"  
**Detection** (the four design gates found by the A3v2 review, with dual-backend consensus from Codex + Qwen):
1. **Construct validity gate**: Does the DV truly measure the construct specified by the hypothesis? (A3v2: accuracy degraded into 0/1 and lost the "quality" dimension of routing decisions)
2. **Format × quantity confounding gate**: Is the format difference between the A/B prompt arms orthogonal to the information-quantity difference? (A3v2: declarative format naturally produced more structured fields, making format and information quantity inseparable)
3. **Ceiling-escape gate**: Does the new experiment design create a larger detection space than the previous round? (A3v2: after DV degradation, the detection space became even smaller)
4. **Effect-size interpretability gate**: If Δ is detected, what does it mean? (A3v2: unable to distinguish "format effect" from "structured information effects attached to declarative format")

**Handling**: If any of the four gates fails → do not run the experiment. A3v2 was stopped because all four gates failed. This is a successful design review, not a failed experiment.

---

*Generated model: DeepSeek-V4-Pro (via Claude Code CLI) · 2026-07-01*  
*Methodology source: prompt-tdd A2+A3 experiments (17+ rounds of cross-backend review)*
