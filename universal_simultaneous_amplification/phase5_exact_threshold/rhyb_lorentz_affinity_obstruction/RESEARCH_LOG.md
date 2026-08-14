# Research log: two-root Lorentz cone and path affinity

## 2026-08-13 — Lorentz bridge and unmarked-support obstruction

- Put the exact orientation-preserving pair criterion into rapidities.  The
  diagonal rapidity at root `i` is determined by the full Kac return rewards:

  ```text
  alpha_i=arcosh(1/[r^(3/2) sqrt(R_B(i)R_D(i))]).
  ```

- Proved the new scalar comparison

  ```text
  cosh(A)cosh(B)cosh(D)+sinh(A)sinh(B)
    >= cosh(sqrt((A+B)^2+D^2)).
  ```

  Therefore `epsilon^2 <= (alpha_i+alpha_j)^2+delta_ij^2` is a rigorous
  sufficient condition for the exact pair test.  It retains the swapped
  root-assignment orientation term.
- Built the unmarked path-affinity subgenerator
  `H_AB=sqrt(Q_B(A,B)Q_D(A,B))` off diagonal, with averaged diagonals.
  Its row killing and drift have exact square decompositions.
- Proved the full-rank rowwise supersolution `H(|A|-1)<=0`.  Every common
  Bd/dB state edge is rank-nonincreasing: a Bd selective birth retains the
  occupied target, whereas a loopless dB burst deletes it and cannot
  resample it.
- The same support fact is fatal to the intended Green comparison.  There
  is no common singleton-to-higher-rank edge, so `H_SR=0` and every
  higher-rank affinity excursion reward from a singleton is exactly zero.
- Exact unweighted-`P3` Kac data at `r=3/2` have strictly positive rewards
  for both rules at every root, showing that the zero affinity reward is a
  proof-route obstruction on an active physical example, not a vacuous
  target regime.
- Positive diagonal/degree conjugation preserves the zero support.  A future
  Hellinger construction would require a marked phase, operation, target,
  or source-history state.  No marked-history search was performed.
- Audited only the canonical marked `2 by 2` lift.  Its diagonal likelihood
  cocycle is exact, but multiplying it by the scalar Hellinger weight simply
  recovers the two original path weights.  The additive Kac reward instead
  occupies the off-diagonal entry of a triangular cocycle, which is not
  positive on the physical negative-reward cycles.  A positive exponential
  Feynman--Kac lift contains the reward only as its derivative at zero.
- Universal MP and the physical Lorentz cone remain open.  The unmarked
  path-space Hellinger and canonical positive marked-`2 by 2` routes are
  stopped exactly.
