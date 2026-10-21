# Owned-copy mutation findings

Ordinary and optimized runs used Python 3.14.6 at /opt/homebrew/opt/python@3.14/bin/python3.14. Every mutation source, copied artifact, stdout, stderr, return code, command, and input/output hash is preserved within this folder. No supplied original was changed. Expected intentional rejections are evidence, not failed experiments to discard. No implementation pilot crashed or was suppressed.

Unmodified author baseline: exit 0/PASS, 5,618 counted ck calls. Unmodified reviewer baseline: exit 0/PASS, 14,891 counted ck calls. Both also report those counts with -O, when their assert statements have been eliminated. These counts are not active assertion counts under optimization.

| Mutation | Ordinary | Optimized | Scientific significance |
|---|---|---|---|
| author_wrong_b0_factor | reject / exit 1 | PASS / exit 0 | The purported square-root slice now has xy=v, violating its required factor 1/2. |
| author_wrong_complex_square | reject / exit 1 | PASS / exit 0 | The imaginary coordinate of the complex square is incorrectly halved. |
| author_wrong_system_xy | reject / exit 1 | PASS / exit 0 | The printed second equation is changed from xy+b to 2xy+b. |
| author_wrong_path_second_piece | reject / exit 1 | PASS / exit 0 | The path is discontinuous at the seam and no longer ends at -1. |
| author_continuous_hidden_zero | PASS / exit 0 | PASS / exit 0 | A continuous degree-66 polynomial path equals the original on every sampled first-piece point, but vanishes at t=1/128. This defeats the nonzero-path premise between samples. |
| reviewer_wrong_slice_factor | reject / exit 1 | PASS / exit 0 | The scaled candidate no longer solves the claimed slice equation at nonreal parameters. |
| reviewer_wrong_jacobian | reject / exit 1 | PASS / exit 0 | The asserted solution-variable derivative determinant is wrong by factor 3/2. |
| reviewer_wrong_mult | reject / exit 1 | PASS / exit 0 | The complex multiplication imaginary term is given the wrong sign. |
| reviewer_wrong_winding_value | reject / exit 1 | PASS / exit 0 | Positive-ray crossings count twice, producing winding two for the selected polygons. |
| reviewer_corrupt_frozen_artifact | reject / exit 1 | PASS / exit 0 | The text authenticated by the fixed digest is modified; this is an integrity control rather than a theorem counterexample. |
| reviewer_continuous_hidden_zero | PASS / exit 0 | PASS / exit 0 | A continuous radial rational deformation agrees at all 604 rational parameters used by the polygons and at infinity, yet hits zero at t=1/1000. Finite polygon evidence remains true; the interpolated path has a hidden zero. |
| author_explicit_guard_wrong_b0 | reject / exit 1 | reject / exit 1 | Owned proposal: explicit guard rejects the wrong slice in both interpreter modes. |
| reviewer_explicit_guard_wrong_jacobian | reject / exit 1 | reject / exit 1 | Owned proposal: explicit guard rejects the wrong Jacobian in both modes. |
| author_explicit_guard_hidden_zero | PASS / exit 0 | PASS / exit 0 | Owned proposal: robust guards do not fix the finite-sampling blind spot. |
| reviewer_explicit_guard_hidden_zero | PASS / exit 0 | PASS / exit 0 | Owned proposal: robust guards do not fix the finite-sampling blind spot. |

## Two independent hidden-zero constructions

For the author path let T={k/64:0<=k<=64}, P(t)=product over a in T of (t-a), tau=1/128, and h(t)=1-P(t)/P(tau). On [0,1], replace gamma by h(t)*((1-t)+it); leave [1,2] unchanged. The path is polynomial and continuous at t=1 because h(1)=1. Every sampled first-piece point has h=1, while h(tau)=0. The degree-66 path therefore has a genuine zero between samples. Both modes and the explicit-guard proposal report PASS. This is an exact counterexample to inferring a universal nonzero-path claim from the finite controls.

For the reviewer parameterization let T={k/(m-k):5<=m<=44,0<=k<m}; it contains 604 distinct rationals. Let P(t)=product over T of (t-a), tau=1/1000, H(t)=P(t)/(1+t)^605, and h(t)=1-H(t)/H(tau). Multiply the rational unit semicircle root ((1-t²)/(1+t²),2t/(1+t²)) by h(t). At every sampled rational h=1; at tau h=0; as t tends to infinity, h tends to 1. Thus the deformation is continuous even at the appended endpoint -1, yet passes through zero. All checked polygon vertices remain exactly unchanged, so the polygon assertions remain true. Acceptance here exposes a forbidden extrapolation to the whole generating path, not a counterexample to the finite polygon winding calculation.

The supplied programs explicitly disclaim proving topology from finite samples. Their finite diagnostic scope is important: the hidden-zero tests do not invalidate the original written path, whose norm bounds have an all-t elementary proof. They demonstrate why PASS must retain that limited scope.

## Optimization and integrity defect

Nine basic wrong-algebra/path/integrity variants are rejected ordinarily and accepted with -O. In particular, the reviewer corrupted-artifact variant has actual digest aea9ce2d656cc74b0ea9b7a2aba590949b725e7bae7018e28b7f2f959fc01f5d, but the optimized output reports PASS and the expected frozen digest d88322ab825acd97914b898018116f2544dc92c460fe3c37ac86eeab331a8448. The guard was disabled; the printed digest is a constant. This is a real integrity-reporting defect in optimized execution. It does not demonstrate that the unmodified authenticated manuscript was corrupted.

Replacing assert in the owned ck copies with explicit ValueError guards rejects sampled wrong inputs under both modes. These proposals remain local; they preserve original scripts and do not claim to solve sampling incompleteness.

All 30 runs are indexed in execution_evidence/mutation_runs.json. Exact hidden-zero input witnesses are in execution_evidence/hidden_zero_witnesses.json, and the full reviewer normalization rational is stored separately.
