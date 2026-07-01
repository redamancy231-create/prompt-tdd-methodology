# Pre-Flight Checklist (Printable Pre-Flight Checklist)

> Print or copy this checklist. Confirm each item before starting a new experiment.

---

## Pre-Experiment

### Design Gate

- [ ] CK1: H0/H1 has been clearly stated, and the statistical test method has been specified
- [ ] CK2: DV is clearly defined, and the scoring rubric has been frozen (git commit)
- [ ] CK3: power analysis is complete, and min_n_per_arm ≥ calculated value

### Equivalence Gate

- [ ] CK4: output inventories from the two prompt arms have been compared item by item (INVENTORY equivalence)
- [ ] CK4: inventory hash has been frozen

### Test Gate

- [ ] CK5: test_set.json has been created, and the train/test split is clear
- [ ] CK5: the test set will not be used for prompt selection or parameter tuning
- [ ] CK6: if the DV is 0/1 or a proportion → ceiling probe cases have been embedded

### Pre-Registration

- [ ] .lock file has been created (hypothesis + analysis plan + stopping rule + test_set_sha256)
- [ ] .lock file has been committed with git (commit hash: ________)

---

## During Experiment

### Tier 0

- [ ] Small-sample collection (n=4-8/arm) is complete, with no anomalies
- [ ] Scoring script runs correctly, and the manifest is complete
- [ ] Descriptive statistics direction is reasonable, with a rough effect size estimate
- [ ] **Engineering gate decision**: PASS / FAIL → ________

### Tier 1 (run only after engineering gate PASS)

- [ ] raw_outputs/ is append-only, never overwritten
- [ ] Dual rater A (author model) has completed scoring
- [ ] Dual rater B (different backend) has completed scoring in a bare environment
- [ ] Raters do not know group assignment before scoring
- [ ] analyze_experiment.py --tier 1 has completed

---

## Post-Experiment

### Science Gate

- [ ] Statistically significant? p < ________
- [ ] effect size ≥ minimum threshold of interest? Δ ≥ ________
- [ ] Direction consistent? direction = ________
- [ ] **Science gate decision**: PASS / FAIL → ________

### Review

- [ ] Independent cross-backend review ≥ 1 round
- [ ] Reviewer uses a different backend from the experiment executor
- [ ] Reviewer reviewed in a bare environment
- [ ] Review findings have been fixed or recorded

### Closure

- [ ] Maturity has been labeled ([E] / [E-] / [F·1域])
- [ ] Limitations statement has been written into the report
- [ ] Methodology fragments have been extracted (if any)
- [ ] Negative results have been reported honestly (if applicable)

---

*Checklist source: practical methodology from the prompt-tdd A2+A3 experiments*
