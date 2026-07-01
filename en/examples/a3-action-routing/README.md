# A3: Controlled Experiment on Declarative vs NL Routing Descriptions

> **Role**: **Counterexample case**: how to honestly close an experiment that cannot squeeze out more signal  
> **Status**: CLOSED [E-] (the experiment design failed to test the hypothesis; the hypothesis was not falsified)  
> **Review**: 10 rounds (Codex GPT-5.5 ×5 + Qwen3.7-Max ×3 + merge/alignment ×1 + consultation ×1), 0 unclosed findings

---

## ⚠️ Read Before Continuing

A3's autopsy conclusion is: **the hypothesis was not falsified; the experiment design failed to test the hypothesis**.

- Ceiling effect (GPT-5.5 was near-perfect on the routing task)
- Insufficient sample size (Pilot 15 cases, 95% confidence upper bound ~18%)
- GT definition dispute (operationalization of "correct routing" lacked an external anchor)
- DV degradation (binary accuracy was insensitive to format effects)

A3's **teaching value** is not in "what it proved," but in showing when an experiment should be closed, how to honestly record the reason for closure, and how to extract methodology assets from "failure."

---

## Experiment Design

| Parameter | Value |
|------|-----|
| Task domain | Agent routing decision |
| Research question | Is a declarative structured routing description better than an NL compact description? |
| Arm A (control) | NL compact routing description (length-controlled) |
| Arm B (experimental) | Declarative structured routing description |
| Primary DV | strict accuracy (0/1, with meta action exemption) |
| Model | GPT-5.5 temp=0 (Codex CLI) |

### Experiment Trajectory

| Stage | Sample | Result | Decision |
|------|------|------|------|
| v1 | n=10/arm, 6 actions | Δ=0 | Add Hard Mode (increase ambiguity) |
| Hard Mode | n=10/arm | Δ=0 | Discordant rate = 0% |
| Pilot | 15 cases, 15 actions | Δ=0/30 calls | Close after evaluating three options |

### A3 v2 Design (Not Executed)
Dual-backend review by Codex + Qwen found DV degradation + format × quantity confounding, so it was not executed.

---

## Results

### Core Data
- Three stages had Δ=0 and discordant rate = 0%
- Pilot 95% confidence upper bound ~18% (Rule of 3)
- Scoring bug (double use of acceptable_paths + meta action penalty) → after correction, conclusion unchanged

### Science Gate: FAIL

The reason was not "H1 was falsified," but "the experiment design failed to create the conditions for detecting H1":
1. The ceiling was too high: GPT-5.5 was near-perfect on the routing task
2. DV was insensitive: binary accuracy could not distinguish format effects
3. GT lacked an external anchor: "correct routing" was defined by the experimenter without independent validation

---

## Key Lessons

1. **Not every experiment can test its hypothesis**: when the experiment design cannot create detection space, adding more samples is wasteful; honest closure is more valuable than "producing a significant result"
2. **The autopsy matters more than the result**: A3's value is not Δ=0, but the identification of four root causes (ceiling / DV choice / GT absence / underpowered)
3. **The stop-loss value of a pilot**: A3 v2's design review found DV degradation. If v2 had been run, it would have wasted 5× the API calls + scoring + review time

---

## Data Files

Pilot-stage scoring data (15 cases × 2 arms) is retained in the source repository at `tests/pocketflow_assets/a3_action_routing/pilot/scores/`. It is not directly included in the current public version. A3 is positioned as a counterexample case; its teaching focus is the autopsy analysis and closure decision process, not data reproduction. For complete data, consult the source repository.

---

*Original experiment execution: 2026-06-19 ~ 2026-06-20 · Source repository: prompt-tdd*  
*A3 autopsy report: `methodology_extraction/autopsy_a3.md`*
