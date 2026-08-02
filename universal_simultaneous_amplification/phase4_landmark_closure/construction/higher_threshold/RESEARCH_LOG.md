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

## 2026-08-02 10:19 PDT — all exchangeable portal counts closed

- **PROVED CLASS NO-GO:** for every finite number `Q>=2` of exchangeable
  portals joined to diffuse strong-pair blades, the full `Q+1`-state portal
  trace has Bd establishment gain exactly when
  `x=2c/(1-g)>1`.  At and above that boundary, a backward-ratio envelope
  forces strict dB suppression for every `r>1`.
- **PROVED UNIFORM EXTENSION:** the comparison has an explicit positive gap
  depending only on `r`, not on `Q,c,g`.  A stopped-trace coupling therefore
  also excludes `Q_s=o(s)` when `x_s` remains in a fixed positive compact
  interval, even if `Q_s` diverges and the portal-edge fraction tends to one
  arbitrarily fast.
- **EXACTLY DERIVED:** after establishment, the averaged blade
  forward/backward ratio is at least `r^3` under both rules.  The conflict is
  solely in rare-mutant entrance, not in the later sweep.
- **EXACTLY VERIFIED:** symbolic barrier and envelope factorizations pass for
  symbolic `Q,k`; exact tridiagonal transforms pass at rational parameters;
  a separate labelled-state verifier matches all 512 subsets of a
  nine-vertex, three-portal graph to 40 orbit generators under both rules.
- **OPEN:** positive-proportion portal sets, nonexchangeable portal networks,
  portal-specific blade incidence, and genuinely nonseparated multiscale
  structures.  This remains a class theorem and does not change the proved
  lower bound `R_sim>=3/2` or the **59%** landmark-closure estimate.

## 2026-08-02 11:09 PDT — unequal-load rank-one portal route closed

- **PROVED CLASS NO-GO:** for an arbitrary finite set of unequal portal loads,
  no direct portal edges, and an arbitrary positive rank-one portal-by-blade
  incidence matrix, simultaneous Bd/dB establishment is impossible at every
  `r>1`.  Portal identity is retained through the full `2^Q-1` episode.
- The two exact portal scores have a pointwise sum equal to the negative of
  four manifestly positive terms.  Summing over completely unequal loads
  forces one strict establishment deficit, and the stopped-process upper
  bound transfers that deficit to fixation without assuming successful
  establishment implies fixation.
- **EXACTLY VERIFIED:** symbolic sign identities and an independent labelled
  subset solver agree over exact rationals with the exchangeable count solver
  for both rules through `Q=6`.
- **OPEN:** the rank-one hypothesis is substantive.  At `r=8/5`, exact loads
  `1/100` and `2` favor opposite local rules, so a typewise summation cannot
  handle genuinely higher-rank incidence.  That case is now the live portal
  construction route; the landmark-closure estimate remains **59%**.
