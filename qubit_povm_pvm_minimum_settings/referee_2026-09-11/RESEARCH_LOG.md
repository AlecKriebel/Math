# Independent referee research log

## 2026-09-12 03:55 UTC — Scope and baseline (5% complete)

User requests full refereeing of `bell_lean/`, coverage of every mathematical claim in the primary paper, and certification of the universal two-input convex-hull equality. Treat these as distinct hypotheses. Success requires fresh source compilation, dependency/trust audit, semantic model correspondence, and claim-by-claim coverage; a successful build alone does not establish manuscript correspondence.

Baseline main branch commit: `98c98aaad27ebaeb038efe95e74da86900364e84`. Existing changes in `bell_lean/reports/` and unrelated projects predate this review and will not be staged. All review work stays in this dedicated folder. No external communications or immutable release is planned. Independent approach families: physical model/endpoints, reductions/cone circuits, incidence/rank closure, separation/certificates, manuscript coverage and harness review.

A fresh isolated source copy will reuse the installed pinned Lean and dependency cache, with that trust assumption stated explicitly. Source hashes will be checked before and after. Completion percentages measure the referee assignment, not a presumption that the mathematical claim is true.

## 2026-09-12T03:58:00.532829+00:00 — Source-review checkpoint (40% complete)

Five independent review families have found no semantic blocker to the central equality in source. They distinguish unconditional endpoints from omitted or specialized paper lemmas: general POVM duality/KKT, full smooth-manifold and Hessian-inertia package, generic cone/extremal-POVM statements, and explicit model-convention bridges. A possible manuscript error in the scalar characterization of the Lorentz domain is under exact verification; the Lean closure carries an actual Gram frame and does not assume that characterization.

Fresh run is in progress in `work/bell_lean`. An initial copy omitted a historical baseline ZIP required by the runner and failed before Lean invocation; that packaging failure was preserved under `work/initial_copy_evidence` and repaired in `reproduce.py`. Production sources were untouched. A sixth adversarial reviewer is independently challenging the emerging verdict.
