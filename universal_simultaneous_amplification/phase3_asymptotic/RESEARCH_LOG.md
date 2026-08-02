# Phase-3 research log

All times America/Los_Angeles.  No literature search or external contact was
performed.

## 2026-08-01

- 16:35 -- Isolated the quantifier gap: the finite strong-selection theorem
  does not exclude an asymptotic fixed-fitness family, because its
  graph-dependent crossover thresholds are not uniformly controlled and
  might diverge.
- 16:50 -- Derived a monotone graphical coupling for dB in fitness and mutant
  set inclusion.  Combined it with the exact strong limit to obtain the
  finite-fitness support-degree upper bound.
- 17:05 -- Proved the necessary condition
  `average_i 1/(support_degree_i+1) -> 0` for any all-fixed-fitness dB
  amplifier.  This rules out bounded-degree graphs and repeated satellite
  constructions only when a positive fraction of vertices retains bounded
  total support degree after connection; windmills satisfy that hypothesis.
- 17:20 -- Derived the rare-mutant two-/finite-type branching process for
  dense equitable blow-ups.  Found the invariant class distribution and the
  Jensen inequality bounding average dB survival by `1-1/r`.
- 17:30 -- Characterized strictness: equality requires all limiting weighted
  degrees equal.  Hence every fixed-class, positive-proportion dense family
  with a fixed irreducible limiting kernel and unequal limiting degrees is
  eventually dB-suppressing at each fixed fitness.
- 17:40 -- Implemented and ran quotient-chain scans for two-class and windmill
  families.  Both show the expected Bd-positive/dB-negative tradeoff in the
  sampled regimes.  These computations are explicitly not used as proof.
- 17:45 -- Added an exact `Fraction` full-state checker verifying strong
  lumpability for both family partitions and both update rules.
- 17:49 -- Wrote the claims-labelled report.  Remaining cases include both
  mesoscopic non-diffuse structures and diffuse asymptotically isothermal
  perturbations, as well as vanishing-proportion and reducible-kernel
  finite-type boundary regimes.
- 18:10 -- Applied the hostile-audit repairs.  Added the exact stopped rates,
  corrected the uniform error to `O_K(eta_n+1/n)`, proved the Perron root and
  positivity of branching survival, supplied the finite killed-generator
  hitting lemma and nonexplosion passage `p_K -> survival`, displayed the
  Jensen equality average, replaced limiting-gap language by a positive
  `liminf` statement, and narrowed every gadget/fixed-type/corridor summary to
  the hypotheses actually proved.
