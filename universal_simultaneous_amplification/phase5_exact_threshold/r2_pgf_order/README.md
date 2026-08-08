# Uniform-baseline stationary PGF order at fitness two

This branch tests the strictly weaker stationary marked-cache conjecture

\[
  E_\mu[t^{|C|}]\ge ((1+t)/2)^{n-1},\qquad 0\le t\le1,
\]

where `mu` is the stationary law of the exact one-sample marked chain.  It
is not the already-refuted comparison of the stationary PGF with its
two-step value.

Status: **EXACTLY REFUTED**.  The canonical proof and independent exact
certificate are:

- `UNIFORM_PGF_REFUTATION_AND_INTEGRATED_REDUCTION.md`;
- `verify_uniform_pgf_refutation.py`.

The refutation leaves the required `psi`-weighted integral positive.  The
note isolates a narrower two-lemma frontier consisting of partial active-rank
CDF order away from the singleton cut and a mean--singleton inequality.
Both are **OPEN**.
