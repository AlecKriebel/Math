# Higher-threshold construction research log

All times are America/Los_Angeles.  This track searches for an explicit
fitness-independent construction extending the proved center--singular-
triangle interval `(1,3/2)`.  No literature search or external contact is
used.  Floating-point searches are reconnaissance only.

## 2026-08-01 23:34 — initialization

- Began from the proved separated center/module trace formulas and the exact
  singular-triangle construction.
- Primary targets: singular weighted modules of order four through six,
  optimized nonuniform center attachments, and recursively separated
  multiscale modules.
- A candidate must have both isolated uniform establishment probabilities
  above `1-1/r` and a nonempty exact center-degree window.  These conditions
  are only filters until the full trace process is proved.
- Completion estimate toward a rigorous interval beyond `3/2`: **5%**.

## 2026-08-02 00:26 — exact near-miss and load-aware closure

- `PROVED`: the four-vertex two-strong-edge singular module has dB uniform
  establishment above the infinite-complete baseline up to the unique root
  `1.543689...` of `r^3-2r^2+2r-2`, but the separated clique-center window is
  empty for every `r>1`.  Its endpoints differ by exactly
  `-(r-1)^2(r^2+1)`.
- `PROVED`: the rational `(3,3,2)` triangle, entered at the vertex incident to
  both weight-three edges, has rooted fixation exceeding `1-1/r` under both
  rules at `r=31/20`.  This is a portal primitive, not a uniform construction.
- A nonuniform early-migration model initially produced a large positive local
  score at `r=1.55`.  The candidate was rejected after enforcing the handshake
  load of all resident satellites on the center.
- `EXACTLY DERIVED WITHIN THE BRANCHING LIMIT`: formulas for the first rare-
  satellite coefficient under both rules, including the center-load term.
  Numerical optimization of the exact finite colony chains through five
  vertices found no positive coefficient at `r=1.55`.
- Tested mixtures of Bd-special and dB-special colony types using additivity
  of the first-order coefficients.  The optimized opposing gain/loss products
  remained below one for orders two through five at and above `r=3/2`; no
  convex mixture became simultaneously positive.  This is numerical only.
- No global architecture beyond `3/2` survived.  Completion estimate toward a
  rigorous interval beyond `3/2`: **32%**; completion toward a useful exact
  higher-threshold search report: **95%**.

## 2026-08-02 08:33 PDT — separated mesoscopic pair route closed

- **PROVED CLASS NO-GO:** a growing one-portal module with arbitrarily many
  diffuse strong-pair blades has exact heterogeneous Bd and dB geometric-burst
  extinction equations.  Jensen in the Bd child law and reciprocal Jensen in
  the dB child law give a constant survival-odds-product obstruction.
- For every fixed `r>(1+sqrt(3))/2`, the two uniformly initialized limiting
  establishment probabilities cannot both reach the infinite-complete
  baseline.  With uniformly nondegenerate blade/portal ratios, a slowly
  diverging stopped cutoff and an arbitrarily rarer connected portal
  macrograph turn this into a finite-graph no-go.  Hence this whole separated
  mesoscopic route cannot improve the interval beyond `3/2`.
- **EXACTLY VERIFIED:** an independent symbolic script checks the extinction
  identities, sharp envelopes, scalar maximization and radical sign
  certificate.  A second verifier reconstructs every transition of the exact
  homogeneous lump from the vertex rules and checks its finite-chain
  convergence to the proved limit.
- **OPEN:** nonseparated coupling, multiple active portals, unbalanced graph
  regimes outside the stated compactness hypotheses, and the universal
  threshold.  This closes a construction class but supplies no new lower
  construction beyond `3/2`.

## 2026-08-02 09:41 PDT — symmetric two-portal route closed

- **PROVED CLASS NO-GO:** for two exchangeable portals coupled to a growing
  family of strong-pair blades, the full rare-mutant trace retains both the
  one-portal and simultaneous-two-portal states.  Bd establishment beats the
  large-complete limit exactly when `2c+g>1`.
- After the shift `x=c-(1-g)/2`, the exact dB amplification test is a
  quadratic whose constant, linear, and quadratic terms are all strictly
  negative whenever `x>=0` and `r>1`.  Thus Bd gain forces a strict dB loss
  for `1<r<2`; at `r>=2` the dB one-half entrance factor already fails.
- The proof uses branching survival only as a fixation upper bound through a
  fixed-cutoff stopped-process limit.  It does not identify establishment
  with fixation.  The later density drift is in fact favorable under both
  rules, locating the obstruction entirely at entrance.
- **EXACTLY VERIFIED:** symbolic PGF and sign certificates pass.  A separate
  exact-fraction audit enumerates all 256 labelled subsets of a rational
  eight-vertex instance, proves strong lumpability into 30 states, and checks
  every quotient rate under both update rules.
- **OPEN:** singular parameter scales, nonexchangeable portal incidence, and
  a portal network whose order grows with the blade count.  The many-portal
  extension is under active attack; no threshold beyond `3/2` is claimed.
