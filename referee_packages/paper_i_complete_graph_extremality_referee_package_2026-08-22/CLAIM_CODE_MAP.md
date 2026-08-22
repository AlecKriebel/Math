# Claim-to-code inspection map

This file is an index for a referee. It states intended roles only; it does
not certify that any file is correct or sufficient. All paths below are
relative to `source_and_certificates/universal_simultaneous_amplification/`.

| Mathematical component | Primary manuscript location | Programs to inspect |
|---|---|---|
| Forward death--Birth chain and exact absorption | `phase5_exact_threshold/paper_db_extremality/sections/02_model_results.tex` | `src/exact_markov.py`; `tests/test_exact_markov.py`; `verification/verify_obstruction.py` |
| Directed complete-support strong-selection coefficient | `phase5_exact_threshold/paper_db_extremality/sections/05_strong_selection.tex` | `phase1_directed/verify_directed_db_strong.py`; `phase5_exact_threshold/paper_db_extremality/verify_paper_claims.py` |
| Positive weighted-triangle theorem | `phase5_exact_threshold/paper_db_extremality/sections/06_low_order.tex`; Appendix B | `phase2_triangle/derive_certificate.py`; `phase2_triangle/crosscheck_exact_solver.py`; `phase2_triangle/audit/independent_triangle_audit.py` |
| Two symmetric weighted-\(K_4\) families | `phase5_exact_threshold/paper_db_extremality/sections/06_low_order.tex`; Appendix B | `phase2_n4/derive_lumped_certificates.py`; `phase2_n4/crosscheck_full_chain.py` |
| General replay-only lumpability sanity checks; no Paper I theorem depends on these examples | Not theorem-bearing | `phase3_asymptotic/verify_lumping.py` |
| Fair-geometric dual and collision identities | `phase5_exact_threshold/paper_db_extremality/sections/03_duality_collision.tex` | `phase5_exact_threshold/r2_determinant/verify_r2_determinant.py`; `phase5_exact_threshold/r2_determinant/verify_complete_refresh_forest.py`; `phase4_landmark_closure/obstruction/r2_marked_lift_v2/verify_marked_lift.py`; `phase5_exact_threshold/paper_db_extremality/verify_paper_claims.py` |
| Antisymmetric Hessian sector | `phase5_exact_threshold/paper_db_extremality/sections/04_local_hessian.tex`; Appendix A | `phase5_exact_threshold/r2_determinant/verify_antisymmetric_hessian.py`; `phase5_exact_threshold/r2_determinant/verify_hessian_sectors.py` |
| Symmetric Hessian sector and finite/analytic range split | Section 4; Appendix A | `phase5_exact_threshold/r2_determinant/verify_true_inverse_rank_symmetric_phase.py`; `phase5_exact_threshold/r2_determinant/verify_hessian_sectors.py` |
| Standard Hessian sector and physical normalization | Section 4; Appendix A | `phase5_exact_threshold/r2_standard_physical_phase/verify_physical_standard_phase.py`; `phase5_exact_threshold/r2_regular_sector/verify_local_complete_hessian.py`; `phase5_exact_threshold/paper_db_extremality/verify_paper_claims.py` |
| Cross-sector decomposition, phase typing, defect gauge, and curvature conversion | Sections 3--5; Appendices A and C | `phase5_exact_threshold/paper_db_extremality/verify_paper_claims.py` |

The top-level replay is
`phase5_exact_threshold/paper_db_extremality/replay.sh`. It invokes the unit
suite and seventeen verifier or cross-check programs through the project
`Makefile` and direct calls. Three bundled modules are reached as imported
helpers rather than separate command-line programs:

- `phase4_landmark_closure/obstruction/r2_entropy_certificate/chi_square_channel/verify_resolvent_identities.py`;
- `phase4_landmark_closure/obstruction/r2_collision_closure/verify_direct_flow_screen.py`;
- `phase4_landmark_closure/obstruction/r2_collision_closure/verify_fisher_route.py`.

The referee should trace those import paths and determine whether each helper
is used consistently. The replay's reachability is not, by itself, proof that
the checked assertions match the manuscript.
