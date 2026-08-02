# Research log: mesoscopic pair construction

All times are America/Los_Angeles.  No literature search or external contact
is used.  Numerical calculations are discovery aids only.

## 2026-08-02 08:07 — balanced pair branching reduction

- Began from the exact balanced first-handoff window and the incompatible
  guard-load limits in the pair-windmill audit.
- Derived the full early mutant-pair burst processes for arbitrary diffuse
  portal masses `p_i` and strong-pair ratios `lambda_i`, retaining the whole
  geometric center episode rather than replacing establishment by its mean.
- Both mean progeny matrices have Perron value `r^3`, but their survival laws
  weight the reciprocal ratio `x_i=lambda_i/p_i` in opposite ways.
- Jensen in the Bd child law and reciprocal Jensen in the dB child law give
  sharp common-environment bounds.  A one-variable odds-product calculation
  then proves that the two uniform establishment probabilities cannot both
  reach the infinite-complete baseline when
  `r>(1+sqrt(3))/2`.
- The obstruction grants global fixation as soon as the local process reaches
  an unbounded number of mutant pairs, so no rarer intermodule handoff or
  post-establishment macrograph can repair the deficit.
- **PROVED WITHIN THE SPECIFIED SEPARATED MESOSCOPIC CLASS:** the full
  cross-rule no-go, in particular for every fixed `r>3/2` below `2`; for
  `r>2`, dB already has the one-half entrance cap.
- **OPEN:** the endpoint `r=2` at vanishing finite-size scale, nonseparated
  intermodule coupling, and modules whose protected states are not strong
  pairs around a single portal.
- Hostile audit found and repaired a quantifier gap: convergence through
  every fixed mutant-pair cutoff does not by itself justify sending the
  cutoff to infinity while the type law changes.  The graph corollary now
  assumes uniformly balanced ratios.  Compactness then gives a uniform
  extinction bound `q_*<1`, and a slowly diverging cutoff makes the tail
  rigorous.  The arbitrary-heterogeneity statement is retained only for the
  exact abstract burst tradeoff.
- Independently rebuilt the full homogeneous chain by the exact lump
  `(portal type, heterotypic-pair count, mutant-pair count)`.  Symbolic
  microstate enumeration verifies every Bd and dB lumped rate.  Sparse full
  chains at 10, 20, 40, and 80 blades converge to the derived compound-
  branching formulas.
- Completion estimate for this bounded track: **98%** (proof, hostile audit,
  exact symbolic verifier, and full-chain diagnostic complete; parent audit
  remains).

## 2026-08-02 08:25 — clean verification and final hostile audit

Clean commands from the repository root:

```text
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python universal_simultaneous_amplification/phase4_landmark_closure/construction/higher_threshold/mesoscopic_pair_construction/verify_mesoscopic_pair_tradeoff.py
PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 .venv/bin/python universal_simultaneous_amplification/phase4_landmark_closure/construction/higher_threshold/mesoscopic_pair_construction/check_full_homogeneous_windmill.py
git diff --check -- universal_simultaneous_amplification/phase4_landmark_closure/construction/higher_threshold/mesoscopic_pair_construction
```

Exact output:

```text
PASS: Bd and dB burst fixed-point identities
PASS: homogeneous Jensen envelopes
PASS: constant-odds-product curvature identity
PASS: exact maximizer and L_max formula
PASS: radical derivative certificate and threshold
PASS: generic two-state protected-module extension
PASS: exact symbolic microstate lumpability for Bd and dB
predicted limits at r=1.5, c=0.5: Bd=0.333333333333, dB=0.287878787879
s= 10: Bd=0.330394620271, dB=0.288693276722
s= 20: Bd=0.331707137525, dB=0.288478053096
s= 40: Bd=0.332488744364, dB=0.288239039183
s= 80: Bd=0.332902959708, dB=0.288074692944
PASS: full lumped chains converge toward the proved limits (diagnostic)
```

`git diff --check` returned no output.

Hostile finite-graph coupling audit:

- The finite graph is coupled to the independent branching process only up
  to the first local hit of `0` or `K_s`; it is never asserted that branching
  independence remains true at positive graph density.
- At level `K_s`, the *branching* particles have independent descendant
  trees, so extinction is at most `q_*^K_s`.  Uniform balance of
  `x_i=lambda_i/p_i`, compact total load, and fixed `r>1` give `q_*<1`:
  the fixed-point derivative at zero is `r^3>1`, while its second derivative
  is uniformly bounded on this compact parameter class.
- A diagonal `K_s -> infinity` is chosen slowly enough that the stopped-chain
  error still vanishes.  The rarer intermodule scale is assumed to make an
  outer event before this stopping time `o(1)`.  Once level `K_s` is hit,
  global success is granted, so later finite-graph dependence can only make
  the stated upper bound more generous.
- The full homogeneous lump includes every heterotypic pair and every portal
  switch.  Thus overlapping introductions are not discarded.  At the early
  scale, pair resolution has `O(1)` duration while all further events
  involving that particular pair have probability `o(1)`; successful
  introductions may therefore be thinned by `r/(r+1)` under Bd and `1/2`
  under dB even if the portal switches before resolution completes.
- The post-establishment equality claimed only for the homogeneous model is
  separately audited by the exact full lump.  Heterotypic pairs form a fast
  `O(1)` population, the portal is fast relative to the `1/s` density jumps,
  and the averaged forward/backward density ratio is `r^3` under both rules.
- Remaining caveats are explicit: arbitrary ratios are proved only for the
  abstract burst tradeoff; the finite-graph corollary uses uniform balance;
  nonseparated outer coupling, multiple active portals, the endpoint `r=2`,
  and the universal value of `R_sim` remain open.

- Completion estimate for this bounded track: **100%**.  Mission-level
  completion is unchanged because this is a class obstruction, not
  Alternative U or Alternative O.
