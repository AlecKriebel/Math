# PR195 independent exact-algebra audit log

All times UTC on 2026-10-15. Percentages concern this assigned independent reproduction family.

- 11:23 — Read only CANDIDATE_PROOF.md to fix the claim and coordinate conventions. Began a fresh standard-library exact implementation without reading candidate or archived implementations. Estimate: 10%.
- 11:25:15 — Froze the independent implementation and first certificate in INDEPENDENCE_FREEZE_01.json before inspecting archived implementations or certificates. All proof-critical ranks and the displayed syzygy passed. Independently constructed a degree-(1,2,3) Hilbert–Burch matrix; all signed maximal minors are the ambient binary polars times 50/1336401. Estimate: 75%.
- 11:28 — Completed exact Gröbner and falsification controls: all 21 binary Buchberger pairs vanish; explicit rational GL4 initial ideals through degree 7 show the predicted third-variable obstruction; twelve open flags pass; excluded characteristic 7 and a degenerate ternary flag drop rank to 11 as expected. These finite checks were explicitly kept separate from the algebraic genericity proof. Estimate: 90%.
- 11:29:02 — Replayed the old standard-library verifier only in a private copy. All six independent matrices agree after ordering conversion; archived certificates reproduce; all 23 original files retain their hashes. Estimate: 95%.
- 11:32 — Completed the written adversarial proof audit, runnable instructions, exact safe allowlist, and terminal manifest. Verdict PASS, no unresolved assigned-scope issues. Estimate: 100%. Parent priority, whole-package review, and publication workflow remain separate and active.
