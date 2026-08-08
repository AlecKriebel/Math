# Research log: weighted-leaf scaling

Started: 2026-08-08 (America/Los_Angeles)

No literature search or external contact.

## 2026-08-08: common-hub classification

- Derived the weighted hub-excursion branching chain with rates
  `(r^2,1,r(r-1)C/(mw))` after its common time change.
- **PROVED:** every common-hub scaling has dB correction `-1`; for finite
  excursion parameter its Bd correction interpolates monotonically from
  `1/r` to `1/(r-1)`.  Faster metastable weight scales can only lower it.
- Therefore the original `w=o(C/m)` regime is Pareto optimal and no other
  common weight can raise the hybrid threshold.

## 2026-08-08: distinct-heavy hostile audit

- The local three-state CTMC initially suggested a tunable dB-positive
  mechanism.  A hostile finite orbit solve contradicted it.
- Identified the missing term: each ordinary clique singleton changes by
  `Theta(C^-1)`, and summing over all ordinary starts changes the leading
  defect vector.
- Derived that contribution exactly through the branching-generator Poisson
  equation and reconstructed the full rational Bd/dB corrections.
- **EXACTLY VERIFIED:** labelled subset rows agree with the `(i,h,l)` orbit
  chain; the symbolic generator residual yields the closed formulas; finite
  orbit solves converge to them.
- **PROVED:** the heavy-defect separator is strictly negative for every
  `r>=3/2` by a 34-term nonnegative-coefficient certificate.
- The apparent threshold `1.5776` from the local-only calculation is
  **FALSIFIED** and is not a graph-family result.
