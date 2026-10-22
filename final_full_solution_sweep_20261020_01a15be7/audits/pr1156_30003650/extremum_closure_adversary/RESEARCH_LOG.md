# PR1156 extremum and closure adversary research log

Scope: independent proof audit of the pinned candidate, especially finite conic reduction, compactness, semicontinuity, extrema on exact ordinary-rank strata, and singular boundaries. No candidate or service mutations, no external communication, no priority claim.

## 2026-10-22 00:15:41 UTC - checkpoint (20% complete)

- Preproof publication-lead gate: read parent `PR1156_PUBLICATION_LEADS.json`, checked at 2026-10-22T00:14:15.439269+00:00: 181 ledger rows, zero matching identifier/CP-plus/positive-factor-rank leads. This is a scope gate, not a novelty finding.
- Read the complete immutable candidate proof at head `57c07523247d0de1a2fbb76f3243d0369caff682`, path `unsolved_math_prioritization/attempts/30003650/PROOF.md`. No historical audit or acceptance was consulted.
- Freshly opened both original primary PDFs. Original target has separate maximum-gap and maximum-finite-CP-plus questions. The present audit must judge the latter separately.
- Initial reconstruction: bounded factor sets are compact after trace control; resulting local inequality is CP-rank >= its value at the base point. No unsupported upper-semicontinuity assertion is required.
- Next: independently prove each congruence direction, adversarially test exact-rank attainment and exceptional cases, then reconcile all credited low-order and gap statements.

## 2026-10-22 00:18:25 UTC - checkpoint (80% complete)

- Independently reconstructed both congruence proofs. `I+tJ` turns every nonzero nonnegative column positive; closedness of the bounded-CP-rank sublevel set prevents a local drop. `I-tJ` preserves a chosen finite positive factor for `0<t<=alpha/2`, and its positive inverse turns a minimal factor of the image into a positive factor of the original matrix.
- Fixed-rank extrema are attained by a finite integer-value argument, not by compactness of a rank stratum. Both congruences preserve ordinary rank, including singular cases.
- Fresh primary PDF rendering verified the separate original questions at printed pp. 3082-3083; Corollary 3.4, Theorem 4.9, and Theorem 5.1 of the 2014 author manuscript were checked in full relevant pages. Theorem 4.9 is restricted to the interior; Theorem 5.1 separately treats boundary and interior maxima. Journal metadata confirms 2015, volume 482, pp. 191-206, DOI 10.1016/j.laa.2015.05.021.
- Authored and inspected 17 exact-rational finite controls. Executed only new read-only private copies in normal, `-O`, and `-OO` modes, with identical successful output and no stderr. Controls include n=1, rank one, zero-row input, singular rank two, identical columns, strict conic reduction, the inverse formula, row duplication, a deliberately unsafe uniform-parameter countercontrol, and nonclosed-domain examples. No general CP-rank was inferred numerically.
- No counterexample or unsupported central assumption found. The nonclosed positive-factor domain and rank strata are real boundary hazards, but neither is used as a compact maximizing set.
- Remaining: seal the authored report, explicit claim table, and file manifest. Audit completion estimate 80%; discovery of the maximum-gap function remains outside the established result.

## 2026-10-22T00:20:47.727847+00:00 - final checkpoint (100% audit complete)

- Central unrestricted and exact-ordinary-rank extrema independently validated; no defect or counterexample found. The report contains complete checkable reconstructions and explicit failed obstruction families.
- Credited small-order/gap statements reconciled with fresh primary theorem scopes; no separate gap-resolution requirement was imposed on Question (2).
- Strongest validated result: candidate Theorem 4 in both congruence directions, including singular matrices, and its attained maximum equalities for every n and exact ordinary rank.
- Exact remaining research gap: determine the separate maximum-gap function in general. No priority or publication-readiness conclusion.
- Final authored report, claim table, source pins, controls, and execution pins are complete. Third-party PDFs/text/renders and raw execution outputs remain private. A separate manifest is generated after this checkpoint and omits its own hash; its digest is reported externally.
- No candidate/service/Git-index/ref/PR/GWS mutations, external communications, or sibling-agent contact occurred.
