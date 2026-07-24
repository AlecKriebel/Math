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

Certified within its explicit scope.  This rules out the centered
quarter-grid spectral layer \(Q=2362\), not all centered quarter-grid
codes and not any off-grid or noncentered code.

## 2026-07-24 00:05 PDT

- Observed that the endpoint proof uses only \(Q=2362\), so it excludes
  the entire selector \(X=40V=2\), not just one edge vector.  Added an
  exact repeatable spectral-selector no-good and exact disjunctive
  edge-vector no-goods to the discovery MILP.
- Checked the apparent next selector \(X=7\).  It is arithmetically
  impossible before any solver is used: centering gives
  \(Q=\sum k^2E_k\equiv\sum kE_k=-82\equiv0\pmod2\), hence
  \(X=5Q-11808\equiv2\pmod {10}\).
- With \(X=2\) excluded, the next search returned \(X=12\), with
  \(E=(6,72,102,174,181,34,251)\), \(Q=2364\), \(P=19591\), and
  \(Y=-51\).  Congruence and the sharp skew inequality allow
  \(Y\in\{-51,24\}\); the stored value is strictly interior, with exact
  residual \(9X^3-2Y^2=10350\).  Therefore the equality-spectrum
  mechanism cannot iterate past this point.
- Added an independent standard-library verifier for this interior
  pseudomarginal.  It rebuilds all 9,882 allowed row types and 51 triangle
  types; checks the exact first/second degree marginals, pair moments
  through degree 60, all 20 capacity rows, the degree-zero radial PSD
  block, and ten rank/frame PSD blocks.  The minimum positive pair moment
  is \(9/128\), and the degree-zero radial block has exact rank six.
- Pinned the imported theorem \(\tau(4)=24\) to Musin's primary Annals
  paper, including the publisher PDF SHA-256 and the exact closed-boundary
  convention.

## Updated status

The \(X=2\) centered quarter-grid endpoint is certified impossible.  The
same finite relaxation has a certified strict-interior shadow at \(X=12\).
No conclusion follows for a labeled matrix, an off-grid code, or a
noncentered code.
