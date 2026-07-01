# Core Lessons: Methodology Accumulated from Two Negative Experiments

> Extracted from `retrospect_a2_a3_combined.md` (60 KB, 17 sections) → ~5 KB core lessons

---

## Three Cross-Experiment Patterns

### P1: The Ceiling Effect Is the Silent Killer of Prompt Experiments

**Observation**: A2 (code review) and A3 (routing decisions) both hit a ceiling under GPT-5.5 temp=0: the model performed too well, and the effect size could not be detected.

**Mechanism**: When baseline accuracy is > 0.9, the detection space for Δ is compressed to < 0.1. Statistical significance then requires a far larger-than-usual sample size or a coarser DV, but a coarser DV itself loses information.

**Key data**: A2 correctness_rate A=0.954, B=0.935, Δ=0.019, n_nonzero=4<5 (science gate FAIL). In both A3 experiments, Δ=0 and the discordant rate=0%.

**Lesson**: A ceiling probe (CK6) is mandatory during experiment design. If the probe shows that the ceiling cannot be broken, adjust the DV or task domain; do not expect that "a larger sample will detect it."

### P2: IV Contamination Is More Dangerous Than Choosing the Wrong Statistical Method

**Observation**: The core threat to a controlled experiment is not the choice of statistical method (Wilcoxon vs t-test), but contamination of the IV (prompt format) by information-quantity differences.

**Key A2 finding**: Arm B (prep/exec/post segmentation) actually contained check dimensions not present in Arm A (single numbered list). The difference was not format, but nonequivalent information quantity.

**Lesson**: The CK4 INVENTORY equivalence protocol is not an optional check; it is the only way to prevent "measuring the wrong thing." If the output inventories of the two prompt arms are not equivalent, the experiment conclusion is invalid, regardless of the p-value.

### P3: A Negative Result ≠ Experiment Failure

**Observation**: A2 and A3 both failed the science gate, yet they produced 21 methodology fragments, 3 experiment-design templates, and a reusable analysis pipeline.

**Lesson**: The value of a negative experiment is not in "supporting H1," but in: (a) ruling out the existence of a format effect under specific conditions; (b) exposing systematic blind spots in experiment design (ceiling effects, DV selection, IV contamination); and (c) accumulating operational knowledge about "how not to run a wrong experiment."

**Honest label**: Both experiments are labeled [E-] (ceiling-limited), not [E], but they remain valid evidence that can be cited.

---

## Six Missing Patterns (PM-1~PM-6, from Adversarial Validation in Source Retrospective §4.3)

The following missing patterns were identified after the A2+A3 retrospective underwent Codex GPT-5.5 devil's-advocate-style adversarial validation. They are not "what the experiment did wrong," but rather "systematic blind spots: what the next experiment should add."

| ID | Pattern | Definition (verbatim meaning from source report) |
|------|------|---------|
| **PM-1** | Model-temperature combination as a universal confounder | Both experiments used only GPT-5.5 temp=0, so the negative conclusion about format effects cannot be generalized to other models/temperatures. **Partially mitigated through Qwen cross-model replication** (A2 direction consistent, Δ=−0.014), but review behavior, methodology transfer, equivalence validation, and other dimensions remain single-point GPT-5.5 only |
| **PM-2** | Experimenter methodology maturity as an upward cross-experiment bias | The experimenter in A2 and A3 (the same person/team) continuously improved in methodology maturity across the two experiments, and A3's design quality was higher than A2's. This confounds claims about "cross-experiment patterns": is the observed improvement due to methodological maturity, or is there a real cross-domain regularity? |
| **PM-3** | Persistent ambiguity between exploratory and confirmatory frames | Tier 0 is essentially exploratory (generating hypotheses), while Tier 1 is confirmatory (testing hypotheses), but the experiment reports did not clearly distinguish their inferential logic or conclusion language |
| **PM-4** | Sensitivity relationship between test-set size and effect-size detection | The joint impact of test-set size and item discrimination on statistical power was not analyzed. We only know that "n=4 is not enough," but not "how much is needed" |
| **PM-5** | Implementation validity of the scoring/analysis tools requires pre-review | A3's scoring bug (double use of acceptable_paths + meta action penalty) was discovered only after collection. The scoring script should undergo pre-review just like the experiment design |
| **PM-6** | Misjudgment risk in independent review itself was not sufficiently discussed | The retrospective went through 10 rounds of cross-backend review, but disagreements among reviewers, review decay, and reviewers' own systematic blind spots were not analyzed. Review is not a God's-eye view |

*Source: retrospect_a2_a3_combined.md §4.3 + §9.1-9.4 (validated through Codex GPT-5.5 R1+R2 closure)*

---

*Source: prompt-tdd A2+A3 deep retrospective report v1.2 (closed through Codex GPT-5.5 R1+R2)*
