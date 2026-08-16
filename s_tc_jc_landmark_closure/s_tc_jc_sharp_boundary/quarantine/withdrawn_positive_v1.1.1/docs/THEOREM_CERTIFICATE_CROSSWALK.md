# Theorem-to-code and certificate crosswalk

The publication proof is written in the manuscript. The table identifies the
finite or exact computations supporting each computer-assisted step. Hashes
control byte integrity; they are not substitutes for the mathematical
arguments.

| Manuscript result | Primary implementation/certificate | Independent review | Replay command |
|---|---|---|---|
| Automatic triangle bound (Theorem 3.1) | `publication/src/verify_multitriangle_exclusion.py`; `publication/certificates/multitriangle_exclusion.json` | `publication/review/review_multitriangle_exclusion.cpp`; `review/MULTITRIANGLE_STRENGTHENING_REVIEW.md` | `python3 reproducibility/publication/src/verify_multitriangle_exclusion.py`; compile/run the C++ reviewer |
| All-`S_TC` level-2 scope composition | `publication/certificates/all_level2_strengthening.json` plus the hash-locked base theorem certificate | `review/MATHEMATICAL_SCOPE_AND_RELEASE_AUDIT.md` | `python3 reproducibility/publication/review/review_publication_release.py` |
| Analytic bridge peeling and local product theorem (Section 4; Proposition 8.3) | `exact_release/src/build_sharp_boundary_certificate.py`; `exact_release/certificates/final_theorem.json` | `exact_release/review/review_final_synthesis.py` | `python3 reproducibility/exact_release/verify_release.py` |
| Pointwise cut preservation (Theorem 5.1) | `exact_release/certificates/pointwise_cut_certificate.json` | `exact_release/review/review_pointwise_cut.py` | `python3 reproducibility/exact_release/review/review_pointwise_cut.py` |
| Cycle/four-theta core enumeration and bounded support (Proposition 6.1; Theorem 6.6) | `publication/src/regenerate_nonroot_topology_atlases.py`; regenerated topology/count certificates | independent canonicalization inside the publication reviewer | `python3 reproducibility/publication/src/regenerate_nonroot_topology_atlases.py` |
| Five- and six-port theta atlases | `publication/src/regenerate_nonroot_algebra.py`; signature binaries and complete relation TSVs | `publication/review/review_directed_pair_universe.cpp` | `python3 .../regenerate_nonroot_algebra.py --k 5/6`; compile/run reviewer |
| Cycle and cross-generator atlases | `publication/src/regenerate_cycle_algebra.py`; complete relation TSVs | publication release reviewer | `python3 .../regenerate_cycle_algebra.py --k 3/4/5/6` |
| Residual seven-port closure (Theorem 7.5) | `exact_release/src/verify_seven_port_closure.py`; `seven_port_closure.json` | `exact_release/review/review_seven_port_closure.py`; adversarial certificate | `python3 reproducibility/exact_release/src/verify_seven_port_closure.py` |
| Root reduction (Theorem 8.2) | `exact_release/src/verify_root_reduction.py` | `exact_release/review/review_root_reduction.py` | run both scripts |
| Genericity and global classification (Theorem 3.2; Corollary 3.3; Proposition 9.2) | `exact_release/src/build_sharp_boundary_certificate.py`; `final_theorem.json` | `exact_release/review/review_final_synthesis.py`; publication scope audit | `python3 exact_release/src/build_sharp_boundary_certificate.py --check` |
| Canonical structural reconstruction (Theorem 9.3) | Mathematical bridge/local-atlas theorem plus finite canonical mixed-graph encoding | Publication scope audit checks that the output is structural modulo `T`, not a pointwise stochastic-membership list | `python3 reproducibility/publication/review/review_publication_release.py` |
| Theta sharpness (Theorem 3.5; Section 10) | `exact_release/src/verify_theta_sharpness.py`; `theta_sharpness_certificate.json` | exact Fourier and Jacobian replay in the dependency-free verifier | `python3 exact_release/src/verify_theta_sharpness.py` |

The full clean replay is `bash reproducibility/verify_full.sh`; the quick
submission check is `bash reproducibility/verify_quick.sh`.
