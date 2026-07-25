# Research log

## 2026-07-24T00:33:00-07:00

- Reoptimized the four-feature rooted-edge flag block instead of evaluating
  the previously stored fixed lifts.
- Found and rationalized a positive 57-atom \(K_6\) mixture with the fixed
  triangle marginal.
- Verified exactly that every atom is rank-five PSD and that the resulting
  \(4\times4\) flag matrix is positive definite.
- The former separating direction \(8F_0-3F_1\) is strictly positive on
  this repaired mixture.  Therefore the earlier row rejects particular
  lifts, not the marginal itself.

## 2026-07-24T01:15:00-07:00

- Enumerated the full 18-dimensional symmetric rooted-edge basis through
  degree two.
- Derived 11 exact centered root-sum identities at \(N=41\), leaving a
  seven-dimensional quotient.
- A cutting-plane linear program over an incomplete catalog suggested a
  73-atom positive solution.  Numerical eigenvalues were used only for
  discovery.
- Solved 72 independent affine equations over the rationals after fixing
  one rational free weight.  The resulting 73 weights are all strictly
  positive and satisfy all remaining equations exactly.
- Generated
  `centered_degree2_repair_certificate.json`, SHA-256
  `7b8dd73bfdaced21fe6a6f6acd74231a976b7359bce600cf45c0d1c44db895d6`.
- The exact \(18\times18\) moment has the 11 centered identities as its
  radical and rank seven.  All 127 nonempty principal minors of the
  seven-dimensional quotient are strictly positive.
- A separate verifier recomputed the atomic moments using actual vertex
  pairs and obtained seven strictly positive exact
  \(LDL^{\mathsf T}\) pivots.
- Recorded the precise gap: this is a locally feasible \(K_6\) marginal,
  not a projectively consistent family on overlapping \(K_6\)'s and not a
  41-point construction.

## 2026-07-24T01:35:00-07:00

- Removed all proof-critical bare `assert` statements from the four proof
  checkers and replaced them with always-on verification errors.
- Added optimized-mode success tests and deliberately tampered certificates.
  All four verifiers reject tampering under `python -O`.
