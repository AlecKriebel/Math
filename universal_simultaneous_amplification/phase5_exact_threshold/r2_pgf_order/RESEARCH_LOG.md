# Research log

## 2026-08-08: branch opened

- Isolated the uniform-binomial PGF lower envelope from the stronger and
  already-refuted stationary-versus-two-step envelope.
- The target is initially being tested on reversible weighted graphs and,
  diagnostically, on arbitrary loopless row-stochastic kernels.
- The tempting pointwise derivative shortcut
  `E[t^(K-1)(N x-K)]>=0` is already numerically false on the supplied
  five-vertex weighted witness `(7,7,7,31,2,31,1,1,31,7)` at `t=.01` and
  will not be used.

## 2026-08-08: exact refutation

- Independently rebuilt and solved the 192-state marked chain over `QQ` for
  the reversible six-vertex graph with lexicographic weights
  `(1,3,3,1000,30,1000,300,3,1,10,1,30,1,300,30)`.
- **EXACTLY REFUTED:** `F_mu(t)>=((1+t)/2)^N`; already at `t=0` the gap is
  `-0.0007316650347359885...`.
- **PROVED:** stationary parity and normalization factor the difference as
  `D=(1-t^2)Q`, and the exact collision gap is
  `2 sum_j c_j/((j+1)(j+2))` when `Q=sum c_j t^j`.
- **PROVED:** `c_j` is half the active-rank CDF excess through rank `j+1`.
  On the exact witness only the singleton coefficient is negative.
- **PROVED:** signed integration by parts rewrites the collision gap as
  `(2/N) int [1-(1+t)^(-N)] A(t) dt`, where
  `A=E[t^(K-1)(N x-K)]`.
- **EXACTLY REFUTED:** `A(t)>=0` pointwise.  The independent exact marked
  solve on weights `(7,7,7,31,2,31,1,1,31,7)` gives `A(1/100)<0`.
- **OPEN / NUMERICALLY OBSERVED:** all screens retain nonnegative active-rank
  CDF excess at cuts at least two, and retain
  `N+pi_1-2m>=0`.  These two statements together would prove the collision
  theorem by splitting on the sign of the singleton PGF gap.

## Hostile screen scope

- Random reversible searches: 2,000 five-vertex, 2,000 six-vertex, and 500
  seven-vertex weighted graphs with connected sparse and complete supports
  and weights spanning up to eighteen orders of magnitude.
- Diagnostic nonreversible search: 2,000 irreducible six-vertex loopless
  kernels.
- Near-complete perturbation screens at seven logarithmic scales for orders
  four through six.

No screen found a negative non-singleton coefficient, a second positive
root of `Q`, more than one sign variation of the derivative polynomial, a
negative unweighted derivative integral, or a negative collision integral.
This is finite numerical evidence only.
