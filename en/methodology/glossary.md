# Glossary

| Term | English | Definition |
|------|------|------|
| **Tier 0** | Tier 0 | Small-sample descriptive statistics stage: validates toolchain feasibility and does not upgrade maturity |
| **Tier 1** | Tier 1 | Large-sample inferential statistics stage: hypothesis testing + maturity upgrade |
| **Engineering Gate** | Engineering Gate | Judges whether the toolchain is usable: data collection / scoring script / manifest completeness |
| **Science Gate** | Science Gate | Judges whether the hypothesis is supported: statistically significant + effect size ≥ threshold + consistent direction (all three PASS) |
| **Pre-registration Lock** | Pre-registration Lock | .lock file: freezes the hypothesis / analysis plan / stopping rule; cannot be modified after git commit |
| **INVENTORY Equivalence** | INVENTORY Equivalence | Compare the output inventories of the two prompt arms item by item + freeze hashes to prevent IV contamination |
| **CK1-CK6** | Checklist 1-6 | Pre-experiment checklist: CK1-CK3 are Tier 1 hard gates; CK4-CK6 are conditional triggers |
| **[Sp]** | Specification | Maturity: design draft (initial state) |
| **[E]** | Experiment | Maturity: Tier 1 + science gate PASS + review closure |
| **[E-]** | Experiment (ceiling-limited) | Maturity: Tier 1 completed + science gate FAIL (negative result / ceiling effect) |
| **[F·1域]** | Framework (single-domain) | Maturity: written back to the framework, with task-domain limits marked |
| **DV** | Dependent Variable | Dependent variable: the output metric measured by the experiment |
| **IV** | Independent Variable | Independent variable: the input variable manipulated by the experiment (such as prompt format) |
| **Blind Scoring** | Blind Scoring | Raters do not know whether a sample belongs to Arm A or Arm B |
| **Dual-LLM Cross-Backend** | Dual-LLM Cross-Backend | Rater A (author model) + Rater B (different backend model) score independently |
| **HARKing** | Hypothesizing After Results are Known | Adjusting the hypothesis after seeing the results: the opposite of a pre-registration lock |
| **Cohen's κ** | Cohen's Kappa | Inter-rater reliability metric used to detect LLM-LLM scoring disagreement |
| **ceiling probe** | Ceiling Probe | Pre-experiment ceiling probe: embed anti-fabrication/extreme test cases to evaluate detection space |
