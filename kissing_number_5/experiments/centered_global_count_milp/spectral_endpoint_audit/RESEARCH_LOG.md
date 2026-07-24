# Research log

## 2026-07-23 23:37 PDT

- Recomputed the endpoint normalization from first principles.  For
  integer colors \(a=4g\), the fixed edge vector has \(Q=2362\), hence
  \(X=40V=2\).  The cubic invariant has the form
  \(Y=800D=3636864-2160Q+75P\), so \(Y\equiv-6\pmod{75}\).
- Proved the sharp five-variable inequality \(20D^2\leq9V^3\), including
  its equality cases.  It forces \(Y=-6\) and spectrum
  \(\{8,(33/4)^4\}\); the fixed edge counts alone force this endpoint,
  independently of the discovery program's chosen triangle counts.
- Derived
  \(G^2=(33/4)G-(1/4)zz^{\mathsf T}\), with
  \(\|z\|^2=8\), \(Gz=8z\), and \(\sum z_i=0\).
- Checked all grid factors: \(z_i z_j\in(1/4)\mathbb Z\),
  \(z_i^2\in\{0,1/4,1/2,3/4,1\}\), and all nonzero squares share one
  rational square class.
- Used centered row parity to exclude square values \(1/4\) and \(3/4\).
  The only alternatives have respectively 33 or 25 zero coordinates.
  In both cases the corresponding code points would give more than 24
  points in \(S^3\), contradicting the established theorem
  \(\tau(4)=24\).  This exactly eliminates the fixed centered
  quarter-grid edge vector.
- Found that the row/triple distribution stored by the discovery run has
  \(\sum q_i^2=555192\), inconsistent with either endpoint distribution
  (\(544400\) and \(544336\)).
- To audit whether aggregate row marginals themselves suffice, constructed
  two new exact nonnegative integer shadows.  Each has the fixed edge
  vector, \(P=19534\), exact edge--triangle incidence, exact first and
  second row-degree moments, and one of the two allowed pointwise row
  energies.  Thus the marginal relaxation remains feasible; the decisive
  step is the common geometric zero-height subspace, not an aggregate
  count contradiction.
- Added a standard-library exact verifier.  Normal and `python -O` runs
  agree, and six baseline/tamper tests pass.  Certificate SHA-256:
  `235ea2dfaf4807adf8d73688bf3a8df0c3a7f770f87dbe64ac9875a84fc7ce65`.
  Verifier SHA-256:
  `2852181f15743c7ae602d0e4439c4631b980702e4710689de5afaaf59c814f08`.

## Status

Certified within its explicit scope.  This rules out one centered
quarter-grid edge distribution, not all centered quarter-grid codes and
not any off-grid or noncentered code.
