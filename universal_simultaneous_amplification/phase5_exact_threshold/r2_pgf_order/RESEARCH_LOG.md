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
root of `Q`, a negative unweighted derivative integral, or a negative
collision integral.  This is finite numerical evidence only.

## 2026-08-08: exact likelihood-ratio correction

- Derived
  `[t^(k-1)]A=((N-k)q_k-kq_(k+1))/2`, so coefficientwise positivity after
  the constant term is exactly descent of `q_k/q_k^K` from rank two onward.
- **EXACTLY REFUTED:** that likelihood-ratio descent.  The historical
  six-vertex path `1-0-2-4-5-3` with weights `(30,4,64,1,1860)` has exact
  derivative-coefficient signs `(+,-,+,+)`.
- **PROVED ON THE WITNESS:** its full `A(t)` is nevertheless positive on
  `[0,1]`, since the positive constant already dominates its sole negative
  monomial there.  Functional one-crossing remains open.

## 2026-08-08: active PCDF exactly refuted

- Built a singularly coupled connected rational family from five copies of
  the weighted path `0--(10)--1--(1)--2`, joined through portal `2`.
- Solved the isolated six-state proper-subset chain exactly:
  `H(z)=58z/63+5z^2/63`, `m_H=68/63`,
  `Q_H(z)=29z/34+5z^2/34`, `alpha=1/12`, `s=1/42`.
- Derived the first-order reduced odds directly from the update rule:
  `R=(2alpha-s/2)/(s/2)=13`, hence module vacancy `a=1/14`.
- **PROVED:** as the portal coupling tends to zero, the active rank PGF is
  `Q_*(z)=Q_H(z)[a+(1-a)H(z)]^4`.
- **EXACTLY REFUTED:** the active CDF through rank two has exact defect
  `-6530729/10532745216` relative to `K_15`, hence `c_1<0` for every
  sufficiently small positive coupling.  Tree/rational continuity supplies
  connected rational finite witnesses.
- **OPEN:** `N+pi_1-2m>=0`; its exact limit on this family is the positive
  rational `1151848/289597`.
