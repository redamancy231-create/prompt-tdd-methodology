# A1: Flow-as-Node Experiment (Not Included as a Main Case)

## Why A1 Is Not in the Case Directory

A1 (Flow-as-Node nested workflow controlled experiment) was historically the third experiment in the prompt-tdd project, but it **did not complete Tier 1**:

| Status | Description |
|------|------|
| Experiment design | ✅ Completed (design documents md+json + dual-backend review + P0 revision 6/7 closed) |
| Data collection | ❌ Not executed: test cases were not generated (project paused after Session 1) |
| Scoring | ❌ Not executed |
| Closure | ❌ Not closed |

## If It Is Not Included, Why Mention It?

**Risk of selective reporting**: the repository status shows that A1 completed the design stage + review. If A1 were not mentioned at release time, readers might mistakenly think the project ran only 2 experiments. That would be selective reporting and would violate the principle of honesty.

## A1's Core Lessons (Even Though It Was Not Completed)

1. **Tension in IV operationalization**: A1 attempted to test "hierarchical workflow description vs flat description," but "hierarchical" as a prompt feature is "thin" (dozens of lines of text), whereas implementing hierarchy in code is "thick" (architectural design). This tension was honestly labeled in design document §3/§5.4/§10.1.

2. **Task-design complexity is a double-edged sword**: A2/A3 tasks were simple (single-step code review / single routing decision), while A1's task was complex (multi-step chained scenario). Complexity improved ecological validity but reduced statistical sensitivity.

3. **Design value of Tier 0 ceiling probes**: Even though A1 completed only the design stage, it had already identified insufficient detection space in 3/5 categories through CK6 ceiling probing. This finding itself has methodology value (showing that "ceiling probes should be done during the design stage").

## Location of Complete A1 Assets

A1's complete assets are retained in the source repository:
- Design documents: `design/a1_experiment_design.md` + `.json` (68 KB + 40 KB)
- Collection script: `collect_a1.py` (742 lines)
- Scoring script: `score_a1.py` (1087 lines)
- Methodology fragments: `methodology_extraction/a1_fragments.md` (5 fragments, reviewed by Codex)
- Closure report (design stage): `tests/pocketflow_assets/a1_flow_as_node/a1_closure_report.md`

These assets are not included in the current release. A1's experiment conclusions have not been validated, and including them would imply "completed." However, A1's design documents and methodology fragments can be added as an "appendix case" in a future version.

---

*Source: prompt-tdd project_status.md + A1 closure report (2026-06-22)*

*English translation: GPT-5.5 (via Codex CLI) · 2026-07-01*
