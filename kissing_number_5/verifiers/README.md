# Verifiers

Verification programs must be materially simpler than discovery programs and
must reject malformed, rounded, or incomplete certificates.

Run these assertion-based verifiers with ordinary Python, not `python -O`,
which disables the checks.

`verify_d5.py` uses exact integer arithmetic.  It treats each stored row \(r\)
as \(r/\sqrt2\), so normalization and the \(1/2\) pair bound reduce respectively
to `r·r == 2` and `r·s <= 1`.

`verify_fixed41_bv_degree5.py` uses exact rational arithmetic to verify the
fixed-cardinality three-point pseudo-distribution. It also verifies the exact
negative principal minor showing that these particular weights fail at total
degree 6. The same verifier accepts the separately reoptimized exact
degree-6/two-point-degree-30 certificate and the full-radial harmonic-degree-8
and harmonic-degree-16 certificates.

`verify_fixed41_bv_all_harmonics.py` strengthens that audit to all degrees.
It performs exact normalized LDL decompositions through harmonic degree 505,
then verifies exact even/odd limiting matrices and a rigorous Chebyshev tail
bound. It independently checks every ordinary two-point moment by a finite
exact computation and an analytic Gegenbauer tail estimate.

`verify_degree2_bv_barrier.py` reconstructs the relabeled 41-vertex
pseudo-object, checks its pair and triple marginals, all \(3\times3\) Gram
minors, every total-degree-two BV block, the exact negative degree-three
residual-vector square, and its labeled-wedge contribution table.

`verify_max_volume_semialgebraic.py` uses only the Python standard library. It
checks the auxiliary Gegenbauer polynomial, projected-code bound, strict frame
constant, Cauchy--Binet determinant constant, variable count, and the complete
count of maximum-volume coefficient minors.

`verify_local_links.py`, `verify_antipodal_bound.py`, and
`verify_negative_tail_graph.py` check the exact local-link, restricted
antipodal, and forced-negative graph arithmetic.

`verify_tverberg_moment_barrier.py` checks the exact 18-point rank-five
counterexample to the degree-two Tverberg shortcut.

`verify_local_hybrid_barrier.py` checks the all-degree Gegenbauer tail estimate,
every rational threshold cell in the common-center cuts, the Pfender margin,
and the rank-deficit margin for the surviving mass-41 pseudo-measure.

The weighted-residual and degree-three local-hybrid verifiers reconstruct all
pair/triple incidences, BV blocks, wedge cells, rank-five moment residuals,
color-degree covariance values, graphical degree sequences, and same-color
three-vertex motif counts in exact rational arithmetic.

`verify_rank_five_spectral_moment.py` checks the exact spectral identities,
witness violations, and four-cycle partition.  The improved frame verifier
reconstructs its \(S^3\) polynomial and closed-slab bound exactly.

`verify_sparse_deep_graph_stability.py` and
`verify_quantitative_root_system_stability.py` check the sparse graph,
quadratic-field, row-energy, determinant-rounding, and robust-gap constants.

The two split-kernel verifiers check their exact feature spectra.  The
full-interval verifier uses directed rational Machin and Taylor enclosures;
no floating-point cosine sign is trusted.
