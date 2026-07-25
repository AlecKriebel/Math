# Research log

## 2026-07-24

- Rationalized the first numerical repair of the original 22-term
  noncentered integer-row separator.
- Generalized the all-harmonics verifier so its finite/tail thresholds are
  certificate-driven rather than tied to the historical witness.
- Exhaustive separation over all 855,168 admissible integer degree rows
  found five additional exact quadratic facets.
- Reoptimized after each exact facet and rationalized each survivor.
- After six total cuts, the separating quadratic LP became infeasible.
  The primal row-mixture LP produced an exact positive 26-atom solution
  matching every first and second row-degree moment.
- Generated the final all-degree certificate: direct harmonic degrees
  through 599, direct pair degrees through 129, and exact analytic tails.
- Added a consolidated exact verifier for all current cap, frame, and
  sharp-rank checks.  Ordinary and tamper tests pass.
- Exact final source SHA256:
  `e0393e4bd28387eed2637b955caf159a05d91fb68ca191fa79d29896be9ae93e`.
