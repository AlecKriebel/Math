# Zero-weight extension attack

## 2026-07-24T09:02:00Z

- Began after freezing the exact common-source checkpoint one directory
  above.
- For zero-weight vertices \(y\), retained the full mixed moments
  \[
  \sum_i p_i\langle x_i,y\rangle=0,\qquad
  \sum_i p_i\langle x_i,y\rangle^2=1/5,
  \]
  and, for two zero-weight vertices \(y,z\),
  \[
  \sum_i p_i\langle x_i,y\rangle\langle x_i,z\rangle
  =\langle y,z\rangle/5\leq1/10.
  \]
- First adversarial target: construct an exact model satisfying all of
  these scalar one- and two-zero-point conditions, plus the strict-tail
  mass bounds, while having rank greater than five.  Such a model would
  prove that any successful extension argument must explicitly retain
  common rank-five realization.

## 2026-07-24T09:18:00Z

- Strengthened the countermodel to pass every relevant triangle PSD
  condition using the actual sparse \(D_5\) support Gram matrix.
- The revised 29 profiles have exact rank seven.  Thus all one-point
  moments, pairwise zero-zero moments, strict tails, and both
  support-support-zero and support-zero-zero \(3\)-by-\(3\) Gram
  determinants still admit formal total size 41.
- In the same ternary height alphabet, imposing \(4\)-by-\(4\) Gram
  determinants with three support points reduces 2,310 triangle-feasible
  profiles to the 20 profiles satisfying the exact support column-space
  projection.  This finite-alphabet observation is discovery evidence
  only; no finite-alphabet assumption is valid for the original problem.
- Proved a continuous, alphabet-free realization criterion.  For a
  proposed height vector \(h\), weighted norm \(h^{\mathsf T}Ph=1/5\)
  always gives
  \(h^{\mathsf T}PSPh\leq1/25\), and equality is equivalent to
  \(h=5SPh\), hence to realization by a unit vector in the common
  five-dimensional support span.
