---
name: derivative-repo-review
description: Independent cross-review of a derivative repository against its source materials — checks faithfulness, naming drift, scope mismatches, and quick-start executability across multiple dimensions with a structured verdict.
source: auto-skill
extracted_at: '2026-07-01T08:31:20.371Z'
---

# Derivative Repo Review

A methodology for independently auditing a *derivative* repository (casebook, handbook, port, refactor, spin-off) against its *source* materials. Unlike a generic code review, this focuses on **faithfulness to provenance** — did the derivative honestly represent what the source said, or did it drift, conflate, or silently rewrite concepts?

Use when the user asks you to:
- "Independently review" / "cross-check" / "audit" a new repo against a source
- Verify a methodology extraction, casebook, port, or refactor
- Assess whether a derivative artifact is ready to publish

## Review shape (5 phases)

### Phase 1 — Target inventory (read everything)
Read **all** files in the derivative repo, in this order:
1. README + top-level positioning docs
2. Core artifacts (SOP / main docs / analysis scripts)
3. Examples / case files (every one)
4. Supporting artifacts (glossary, checklists, appendices, schema)

Do NOT summarize yet. Just build a complete picture.

### Phase 2 — Source inventory (read the provenance)
Read the source materials the derivative claims to be derived from. Prioritize:
- The source's top-level README / project_status
- The specific reports / files the derivative cites (autopsy reports, experiment reports, retrospectives)
- If a source file is large (>30KB), grep its heading structure first (`^#{1,3}\s`), then selectively read sections referenced by the derivative

### Phase 3 — Cross-reference verification
For every specific claim in the derivative (numbers, labels, lists, citations), trace it back to the source with **grep**, not memory. Watch for these recurring failure modes:

| Pattern | What to grep for | Example |
|---|---|---|
| **Naming drift** | Labels/IDs the derivative reuses (e.g. `PM-1`, `CK-4`, section numbers) | Derivative renumbers source's `PM-1..PM-6` to mean different things — reader cross-referencing the source gets confused |
| **Scope mismatch** | Aggregate stats vs subset stats (train/test, full/pilot) | "n=24, A=0.954" — but 0.954 came from test-set-only (n=12) |
| **Schema drift** | Key names in JSON/YAML/CSV that the derivative references | `.lock` file field names, CSV column labels, JSON keys |
| **Phantom assets** | Files the derivative claims exist in a directory | README says `scoresheet.csv` is here; `ls` shows it isn't |
| **Conflation** | Counts of "total" things drawn from multiple classification levels | "21 methodology fragments" = 11 + 3 + 7 from three different layers |
| **Stale dependencies** | `requirements.txt` / `package.json` entries not actually imported | `pandas>=1.5` declared but never imported |
| **Default-vs-demo mismatch** | CLI defaults vs demo data | Default `--rater rater_human` but demo CSV uses `rater_a` |

### Phase 4 — Static-execution of quick-start
The README's quick-start is the new visitor's 30-second trust test. Even if the runtime environment is unreliable, **walk the code path statically**:

1. Find the exact command the README recommends
2. Open the entry point (e.g. `main()`, CLI parser)
3. Trace: what defaults does it use? Does the demo data match those defaults?
4. Check: what happens when data is empty / missing? (Off-by-one, ZeroDivision, early exit with no stderr)
5. Verify declared dependencies (`requirements.txt`) match actual imports

If the quick-start can silently fail (exit code ≠ 0 but no output), flag it **CRITICAL** — this is usually the first thing a new reader will try.

### Phase 5 — Render verdict

For each review dimension the user defined, output:
1. **Overall rating** (one line)
2. **Specific findings** as a table: `severity | file/section | finding`
3. **Fix suggestions**

Severity scale:
- **CRITICAL** — breaks first-run trust or causes naming/language split with source
- **MAJOR** — misrepresents source data or drops a load-bearing concept
- **MINOR** — wording ambiguity, missing optional context, stale refs

Then render a **terminal verdict** using this scale:
- **Keep** — ready to publish
- **Minor** — small fixes needed
- **Major** — conditional accept; fix CRITICAL+MAJOR before publishing
- **Discard** — fundamental misalignment with source

Pair the verdict with a **fix-priority table** (P0/P1/P2 + estimated time). This is what the author actually acts on.

## Things this review is NOT

- Not a code-quality review — the analysis script's algorithm is out of scope unless it affects quick-start executability
- Not a copy-edit — focus on provenance fidelity, not prose style
- Not a feature wishlist — judge against the derivative's *stated* positioning, not what it could have been

## Red flags that indicate naming drift

When the derivative uses the *same label* as the source for *different content*, this is the highest-cost bug because every future reader who cross-references will trip. Always check:

- Numbered lists (PM-1..N, CK-1..N, MF-1..N) — does the derivative's item N mean the same as source's item N?
- Section references (`see §4.3`) — does the derivative's §4.3 match the source's §4.3 content?
- Acronyms reused with different definitions
- Citation counts ("17+ rounds", "21 fragments") — can you decompose the number back to source's sub-counts?

If you find drift, the fix is either:
(a) **Align** the derivative's labels with the source's (preferred when source is canonical), OR
(b) **Rename** the derivative's labels and explicitly disclaim ("this list does not correspond to source's §X.Y") — required when the derivative is intentionally re-scoping.

Never let both versions coexist silently.
