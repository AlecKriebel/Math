# Research log: genuinely higher-rank portal incidence

## 2026-08-02 11:02 PDT — Higher-rank continuation opened

- Began from the independently verified full labelled portal-subset trace
  and the completed rank-one theorem.
- Kept all new work in separate files so the inherited checkpoint could be
  committed without overlap.
- No literature search or external contact.

## 2026-08-02 11:12 PDT — Load-fraction reduction and first searches

- Reparameterized each portal row by its total load `B_a` and type fractions
  `f_at=2*pi_t*lambda_at/B_a`.
- Found that the multitype extinction vectors are independent of the blade
  proportions in these coordinates.  For one fitness value, the optimal
  type mixture is therefore an exact two-affine-function linear program
  whose optimizer uses at most two types.
- Independently compared the specialized no-direct-portal equations with
  the full labelled solver in 90 random cases; the maximum discrepancy was
  below `2e-11`.
- Differential-evolution searches through `Q=6,T=5` found no positive gap.
  These are numerical observations only.

## 2026-08-02 11:27 PDT — Exact two-class lumping and growing boundary

- Derived an exact `(k_0,k_1)` count lumping for two equal portal classes,
  with distinct within-class weights, a cross-class weight, unequal loads,
  and a rank-two blade incidence.
- Checked the count-lumped episode transforms and extinction vectors against
  the full labelled chain for class sizes 1, 2, and 3 in 60 independent
  cases.
- Derived the growing-class boundary trace when within-class edges scale as
  `H_gg/(q-1)` and cross edges as `H_01/q`.  The portal episode becomes a
  two-type continuous-time branching process nested inside the blade trace.
- Verified finite-to-boundary convergence directly.  At class size 12, the
  test-case Bd extinction error was below `1e-4`; the dB error was below
  `0.004`, with monotone `O(1/q)` decay visible across sizes 2,4,8,12.
- No positive simultaneous hit was found.  The best growing two-class value
  found at `r=8/5` was approximately `-0.02667812`; this is not an
  optimality certificate.

## 2026-08-02 11:46 PDT — Affine supersolution breakthrough

- Independently identified the typewise affine separation
  `x_D <= 4(r-1)/r - 2r*x_B/(r+1)` for `r>=3/2` in the no-direct-portal
  model.  A separate diagnostic by the parent agent found the same map.
- Reduced the multitype statement to a scalar portal inequality involving
  the two harmonic responses
  `B*m/(B+r^2*m/(r+1))` and
  `B*n/(1+r*B*n/2)`.
- The Bd fixed-point odds cancel exactly after summing the scalar inequality,
  leaving a dB supersolution.  This is a genuine reciprocal-incidence
  separation, not a rank-one reduction.

## 2026-08-02 11:54 PDT — Exact certificate completed

- Proved the scalar lemma on its complete domain by compactifying
  `r,x,m,B` to a unit four-cube and splitting once at the clipping threshold
  `m=m_0`.
- The exact numerator multidegrees are `(14,2,1,3)` and `(16,2,2,3)`.
  Fixed rational Bernstein covers require only 6 and 11 boxes, with maximum
  depths 3 and 6.  Every terminal coefficient is nonnegative.
- Added an independent exact verifier that also reconstructs and solves the
  full seven-state labelled portal system for rational `Q=3,T=2` data.
- The verifier passes every symbolic, labelled-chain, denominator-sign, and
  Bernstein check.
- Result proved: arbitrary finite positive higher-rank incidence with no
  direct portal edges satisfies `alpha_B+alpha_D<2(1-1/r)` for
  `3/2<=r<=2`, and cannot simultaneously amplify for any `r>=3/2`.
- Direct portal networks remain open; no universal mission claim is made.
- Recorded the precise next conjecture for the full subset resolvent:
  `S_D^h(J(s))<J(S_B^h(s))`.  It survived random tests through `Q=4,T=3`
  and global optimization at `Q=T=2`, but remains numerical evidence only.

## 2026-08-02 12:14 PDT — Independent hostile audit passed

- An independent agent rederived every atomic normalization and the affine
  map comparison, reconstructed the full Bernstein tensors, and ran exact
  endpoint and high-dynamic-range fixed-point tests.
- No mathematical counterexample or certificate defect was found.
- The final audit verdict is PASS.  Two editorial range/strictness issues
  were corrected, and the verifier was hardened to reject nonintegral
  source coefficients or empty physical faces.
- Residual scope remains explicit: fixed finite `Q,T`, fixed positive data,
  and no direct portal edges.
