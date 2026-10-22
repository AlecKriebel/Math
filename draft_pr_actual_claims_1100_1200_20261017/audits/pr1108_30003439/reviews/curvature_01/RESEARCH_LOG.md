# Curvature audit research log

Effort: PR1108 / 30003439 / OWR-15219-008, exact negative-third-derivative certificate.
Frozen proof revision: `148130ab93ab46a3459d7bc98a11a1ca79052d65`.

| Authoritative UTC timestamp | Assigned-scope completion estimate | Checkpoint |
| --- | --- | --- |
| 2026-10-17 17:09:49 UTC | 10% | Pinned proof retrieved; derivative reconstruction begun independently of the old mathematical audit. Default and bundled Python lacked SymPy. Local storage was full, so no file writes were attempted. |
| 2026-10-17 17:11:56 UTC | 95% | Stdlib exact sparse-polynomial checker reproduced NC1–NC5, t=1 and e_x; independent logarithm-series derivative checks also passed. Automorphism, cone reduction and sign ranges checked analytically. |
| 2026-10-17 17:12:50 UTC | 100% | Curvature-specific adversarial verdict complete: universal inequality verified, no remaining gap found. Added explicit forbidden-direction, reversed-sign and omitted-log-z falsification controls. Nothing persisted while disk was full. |
| 2026-10-17 17:14:29 UTC | 100% | Parent authorized persistence after storage recovered. Began writing only the assigned reviews/curvature_01 artifacts. |
| 2026-10-17 17:15:04 UTC | 100% | Complete checker saved with explicit optimized-mode rejection. Two normal runs returned identical final JSON after all 315 independent logarithm-series checks and controls; optimized mode failed at startup as required. Saved results and execution evidence. |

| 2026-10-17 17:16:43 UTC | 100% | Final analytical report and research log saved; all six evidence artifacts hashed in SHA256SUMS. No commits, pushes or PR mutations performed. |

The earlier informal message saying “17:14 UTC” before the 17:11:56 checkpoint was an estimated timestamp and was explicitly corrected. It is not an authoritative checkpoint.

Mechanism family: direct exact logarithmic derivative tensor, supplemented by an independently evaluated bivariate logarithm-series derivative mechanism.
Evidence: universal analytic positivity certificates, exact polynomial identities, 45 rational parameter cases, 315 independent contractions and three successful negative controls.
Status: verified within assigned curvature scope.
Strongest result: \(D^3F(a)[h,u,u]\le0\) for every interior base point, every closed-cone direction and every real vector \(u\).
Remaining assigned-scope gap: none found.
Excluded scope: self-concordance, nonhyperbolicity, target-source interpretation, novelty and priority.
