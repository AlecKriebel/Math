# Uniform-baseline stationary PGF order at fitness two

This branch tests the strictly weaker stationary marked-cache conjecture

\[
  E_\mu[t^{|C|}]\ge ((1+t)/2)^{n-1},\qquad 0\le t\le1,
\]

where `mu` is the stationary law of the exact one-sample marked chain.  It
is not the already-refuted comparison of the stationary PGF with its
two-step value.

Status: **EXACTLY REFUTED**.  The canonical proof and independent exact
certificates are:

- `UNIFORM_PGF_REFUTATION_AND_INTEGRATED_REDUCTION.md`;
- `verify_uniform_pgf_refutation.py`;
- `WEAK_MODULE_PCDF_REFUTATION.md`;
- `verify_weak_module_pcdf_refutation.py`.

The first refutation leaves the required `psi`-weighted integral positive.
The weak-module certificate then exactly refutes the residual active-rank CDF
order away from the singleton cut.  The mean--singleton inequality and the
weighted integrated collision sign remain **OPEN**.
