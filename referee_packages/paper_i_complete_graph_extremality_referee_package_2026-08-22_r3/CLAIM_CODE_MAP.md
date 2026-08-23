# Claim-to-code inspection map

This file is an index for a referee. It states intended roles only; it does
not certify that any file is correct or sufficient. All paths below are
relative to `source_and_certificates/universal_simultaneous_amplification/`.

| Mathematical component | Primary manuscript location | Programs to inspect |
|---|---|---|
| Forward death--Birth chain and exact absorption | `phase5_exact_threshold/paper_db_extremality/sections/02_model_results.tex` | `src/exact_markov.py`; `tests/test_exact_markov.py`; `verification/verify_obstruction.py` |
| Directed complete-support strong-selection coefficient | `phase5_exact_threshold/paper_db_extremality/sections/05_strong_selection.tex` | `phase1_directed/verify_directed_db_strong.py` (selected `n=3,4` literal-chain checks and equality/gauge controls; Section 5 carries the universal algebra); `phase5_exact_threshold/paper_db_extremality/verify_paper_claims.py` |
| Positive weighted-triangle theorem | `phase5_exact_threshold/paper_db_extremality/sections/06_low_order.tex`; Appendix B | `phase2_triangle/derive_certificate.py`; `phase2_triangle/crosscheck_exact_solver.py`; `phase2_triangle/audit/independent_triangle_audit.py` |
| Two symmetric weighted-\(K_4\) families | `phase5_exact_threshold/paper_db_extremality/sections/06_low_order.tex`; Appendix B | `phase2_n4/derive_lumped_certificates.py`; `phase2_n4/crosscheck_full_chain.py` |
| General replay-only lumpability sanity checks; no Paper I theorem depends on these examples | Not theorem-bearing | `phase3_asymptotic/verify_lumping.py` |
| Fair-geometric dual and collision identities | `phase5_exact_threshold/paper_db_extremality/sections/03_duality_collision.tex` | `phase5_exact_threshold/r2_determinant/verify_r2_determinant.py`; `phase5_exact_threshold/r2_determinant/verify_complete_refresh_forest.py`; `phase4_landmark_closure/obstruction/r2_marked_lift_v2/verify_marked_lift.py`; `phase5_exact_threshold/paper_db_extremality/verify_paper_claims.py` |
| Antisymmetric Hessian sector | `phase5_exact_threshold/paper_db_extremality/sections/04_local_hessian.tex`; Appendix A | `phase5_exact_threshold/r2_determinant/verify_antisymmetric_hessian.py` (finite recurrence checks through `n=40`, literal active chains through `n=7`); `phase5_exact_threshold/r2_determinant/verify_hessian_sectors.py` (finite orbit checks through `n=12`); Appendix A carries the all-order proof |
| Symmetric Hessian sector and finite/analytic range split | Section 4; Appendix A | `phase5_exact_threshold/r2_determinant/verify_true_inverse_rank_symmetric_phase.py`; `phase5_exact_threshold/r2_determinant/verify_hessian_sectors.py` |
| Standard Hessian sector and physical normalization | Section 4; Appendix A | `phase5_exact_threshold/r2_standard_physical_phase/verify_physical_standard_phase.py`; `phase5_exact_threshold/r2_regular_sector/verify_local_complete_hessian.py`; `phase5_exact_threshold/paper_db_extremality/verify_paper_claims.py` |
| Cross-sector decomposition, phase typing, defect gauge, and curvature conversion | Sections 3--5; Appendices A and C | `phase5_exact_threshold/paper_db_extremality/verify_paper_claims.py` |

The sole certified end-to-end entry point is
`./run_all_referee_checks.sh` at the root of the enclosing package. It verifies
the exact package tree, safely extracts the verified source archive to a fresh
directory, provisions the pinned runtime and private empty cache, and then
invokes `submission/bootstrap_replay.sh` and `replay.sh` as internal stages.
The internal replay invokes the unit suite and all seventeen verifier or
cross-check programs directly. Direct lower-stage execution is a development
convenience, not package certification. Three bundled modules are imported on
the internal path, but their guarded command-line suites are not executed:

- `verify_resolvent_identities.py`: `solve()` is called repeatedly by
  `verify_marked_lift.py`; its `main()` examples are not run;
- `verify_direct_flow_screen.py`: only `matrix_from_edges()` is called; its
  finite direct-flow `main()` is not run; and
- `verify_fisher_route.py`: the module is loaded transitively by the preceding
  import, but none of its functions and not its witness `main()` are called.

Those guarded suites concern exploratory/open global routes and are not
load-bearing for a Paper I theorem. Import reachability is not execution or
proof. The referee should trace the actual calls and determine whether every
explicit check matches the manuscript.
