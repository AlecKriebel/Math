# Research log

All dates use America/Los_Angeles.

## 2026-07-23

- Derived the exact centered tight-frame Gram and Lorentzian-transform
  identities, anchored residual spectrum, two-anchor moments, and subset
  spectral bound.
- Constructed and exactly verified the symmetric circulant triangle-PSD
  countermodel.  Its order-four minor on indices
  \(\{0,2,14,16\}\) is \(-27/16\).
- Ran 16 floating-point projected searches over centered unit-norm tight
  frames.  The best maximum inner product was about
  `0.537812703692`; this is numerical evidence only.
- Found a finite-support numerical Bachoc--Vallentin pseudodistribution,
  rationalized it by solving the exact affine constraints, and verified
  all stored weights are strictly positive rationals.
- Completed a standard-library exact verifier for all pair/triple
  marginals, tight-frame trace moments, degrees \(0\) through \(186\) of
  the radial hierarchy, the analytic all-degree tail, all ordinary pair
  harmonics, eleven low-degree frame matrices, and 27 centered-skew rank
  cuts.
- Corrected a normalization point during adversarial checking: the
  unscaled \(W_2\) all-ones kernel becomes \(1-u^2\) after the parity
  congruence used for rational verification.
- Audited the corrected common-pair hierarchy.  Exactly four of 48
  stratified rows fail, with minimum exact slack
  \[
  -689611676751007372091426251/
  105064854935040000000000000.
  \]
  The object is therefore a certified relaxation barrier, not a
  certificate for the stronger hybrid relaxation and not a code.
