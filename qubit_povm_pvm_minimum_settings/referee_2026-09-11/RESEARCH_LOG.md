# Independent referee research log

## 2026-09-12 03:55 UTC — Scope and baseline (5% complete)

User requests full refereeing of `bell_lean/`, coverage of every mathematical claim in the primary paper, and certification of the universal two-input convex-hull equality. Treat these as distinct hypotheses. Success requires fresh source compilation, dependency/trust audit, semantic model correspondence, and claim-by-claim coverage; a successful build alone does not establish manuscript correspondence.

Baseline main branch commit: `98c98aaad27ebaeb038efe95e74da86900364e84`. Existing changes in `bell_lean/reports/` and unrelated projects predate this review and will not be staged. All review work stays in this dedicated folder. No external communications or immutable release is planned. Independent approach families: physical model/endpoints, reductions/cone circuits, incidence/rank closure, separation/certificates, manuscript coverage and harness review.

A fresh isolated source copy will reuse the installed pinned Lean and dependency cache, with that trust assumption stated explicitly. Source hashes will be checked before and after. Completion percentages measure the referee assignment, not a presumption that the mathematical claim is true.

## 2026-09-12T03:58:00.532829+00:00 — Source-review checkpoint (40% complete)

Five independent review families have found no semantic blocker to the central equality in source. They distinguish unconditional endpoints from omitted or specialized paper lemmas: general POVM duality/KKT, full smooth-manifold and Hessian-inertia package, generic cone/extremal-POVM statements, and explicit model-convention bridges. A possible manuscript error in the scalar characterization of the Lorentz domain is under exact verification; the Lean closure carries an actual Gram frame and does not assume that characterization.

Fresh run is in progress in `work/bell_lean`. An initial copy omitted a historical baseline ZIP required by the runner and failed before Lean invocation; that packaging failure was preserved under `work/initial_copy_evidence` and repaired in `reproduce.py`. Production sources were untouched. A sixth adversarial reviewer is independently challenging the emerging verdict.

## 2026-09-12T04:00:58.762219+00:00 — Adversarial review and exact certificates (65% complete)

All six source-review assignments are complete. No fatal defect was found in the central formal equality chain. The manuscript coverage matrix inventories every named result and all appendices and identifies substantial auxiliary omissions/replacements. A standalone Mathlib-only Lean probe has checked the rational strict-domain counterexample; two independent rational derivations agree. The false unqualified reading is avoided by the production physical Gram-frame premises. A direct-source SOS checker independently verifies the rational factorization, positive pivots, full noncommutative identity, and corruption rejection.

Compiler identity and all nine dependency source pins were independently checked; no path override or source shadowing was found. The full fresh build remains in progress. Its final receipt and the expanded matrix-model contract are required before promoting the central equality to this review's final certified status. Supporting checks initially missing the copied PDF/output directory were rerun after supplying those prerequisites; no production files changed.

## 2026-09-12T04:06:29.202194+00:00 — Final compilation checkpoint (90% complete)

The fresh build has passed the exact rational SOS certificate and reached final residual/assembly modules without mathematical proof errors. All supporting algebra and harness suites have successful runs, including 45 runner tests, 10 axiom-parser tests and 1,387 semantic exact checks with 27 distinguished controls. The integrated referee report received an adversarial consistency review; one declaration-line citation was corrected. Final certification is still withheld until the full runner finishes all contracts and transitive axiom checks and the separate expanded matrix contract compiles.

## 2026-09-12T04:12:05.474832+00:00 — Final referee disposition (100% complete)

Fresh build run `20260912T035656Z-0dca7f1e` passed all 58 production mathematical modules and Bell, both statement contracts, all 675 public declaration dependency queries, and final source/dependency consistency checks. The axiom union is exactly propext, Classical.choice, Quot.sound. The independent explicit complex-matrix contract passed with the same axiom set. Original mathematical sources and primary TeX files remained byte-identical.

Final outcome: certify the requested unconditional two-input convex-hull equality under the documented standard trust/model conventions; reject the broader assertion of literal all-mathematics manuscript coverage. Record the strict-domain equivalence qualification with exact counterexample, which does not affect the physical-frame Lean proof. The referee assignment is complete; omitted secondary formalizations and the proposed manuscript wording amendment remain identified findings, not work silently claimed complete. No production proof or manuscript edits were made. Final report and evidence are being committed and pushed on main; no immutable release is created.
