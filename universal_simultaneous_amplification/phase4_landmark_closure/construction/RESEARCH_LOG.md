# Construction track research log

All times are America/Los_Angeles.  Claims are labelled as `PROVED`,
`EXACTLY COMPUTED`, `RIGOROUSLY BOUNDED`, `NUMERICALLY OBSERVED`, or `OPEN`.
No literature search or external contact is used during discovery.

## 2026-08-01 19:05 — initialization

- Read the inherited Phase 3 report and exact lumped-chain implementation.
- Accepted the fixed-graph and finite-type obstructions as inherited facts;
  they will not be rederived.
- Construction targets: dense asymptotically regular perturbations, vanishing
  classes, weakly completed mesoscopic modules, and multiscale core--periphery
  graphs.  Every candidate will be evaluated for both Bd and dB from the
  defining transition rules.
- Discovery-goal completion estimate: **3%**.

## 2026-08-01 19:35 — exact sparse reconnaissance infrastructure

- Added a residual-checked sparse solver for two equitable classes and an
  unrestricted small-graph absorbing-chain scanner.
- Broad two-class scans (vanishing class, square-root class, fixed proportion,
  weak completion, and power-law orbit weights) produced no simultaneous sign.
  This is `NUMERICALLY OBSERVED`, not an obstruction.
- Built a general equitable-class quotient solver and independently matched it
  against the inherited two-class implementation.
- Discovery-goal completion estimate: **12%**.

## 2026-08-01 20:05 — rooted satellite modules

- Derived exact histogram quotients for clique fans, subdivided stars, and a
  general two-vertex module joined to a common hub by two spoke weights.
- Fine scans resolved a very narrow near-neutral crossing in paired fans: the
  Bd and dB zeroes approach one another but occur in the wrong order.  Coarse
  scans can falsely suggest an overlap, so all candidate testing now resolves
  both zeroes separately.
- `NUMERICALLY OBSERVED`: paired, subdivided, and asymmetric two-vertex fans
  contain no simultaneous region in the tested sizes and fitnesses.
- Discovery-goal completion estimate: **20%**.

## 2026-08-01 20:35 — a genuinely surviving diffuse family

- Focused on `F_{M,L}(s)`, a hub joining `M` growing unit cliques.  Proved its
  exact lumpability into hub type plus the histogram of module occupancies and
  wrote all Bd/dB quotient transitions directly from the update rules.
- Proved that for `s=Theta(1/M)` and `L->infinity`, uniform-vertex temperature
  heterogeneity vanishes, the collision functional is `O(1/L)`, and every
  support degree diverges.  Thus this is genuinely outside the inherited
  fixed-class and bounded-support exclusions.
- Exact quotient solutions nevertheless show dB suppression whenever Bd is
  positive; the weighted-regular point ties Bd and suppresses dB.
- Discovery-goal completion estimate: **33%**.

## 2026-08-01 21:00 — two-type first-correction identity

- Derived the leaf/hub rare-mutant process through order `1/L`, including the
  vanishing probability of a hub initial mutant.
- `PROVED ALGEBRA WITHIN THE REDUCED PROCESS`: its dB comparison coefficient is

      D = -(r-1)/r - sigma/r + sigma*r/(1+M*sigma*(r-1)).

  With `x=M*sigma`, its sign is that of
  `-x^2+[(r+1)-M(r-1)]x-M`, which is strictly negative for every
  `M>1`, `r>1`, `sigma>0`.
- The analogous Bd coefficient cancels at order `1/L`; its comparison begins
  at order `1/L^2`.  Exact quotient data converge to the predicted dB
  coefficient.
- `OPEN`: a uniform `o(1/L)` control from rare-process survival through full
  fixation is still needed before this becomes a rigorous family exclusion.
- Discovery-goal completion estimate: **43%**.  The positive-construction
  corridor has narrowed substantially, but Alternative U is not resolved by
  this track.

## 2026-08-01 21:15 — independent verification checkpoint

- Added `verify_clique_fan_lumping.py`.  It builds every subset transition with
  exact `Fraction` arithmetic and verifies strong lumpability plus every
  quotient formula for `(M,L)=(2,2),(2,3)` under both rules.
- Verification output: four `PASS` lines; no mismatch.
- Wrote `CONSTRUCTION_REPORT.md` with claim labels and the precise limitation
  on the formal fixation asymptotic.
- Added a separate symbolic verifier for the two-type first-order equations,
  comparison coefficient, quadratic numerator, and regular-spoke
  specialization; all four identities pass exactly.
- Discovery-goal completion estimate: **46%**.
