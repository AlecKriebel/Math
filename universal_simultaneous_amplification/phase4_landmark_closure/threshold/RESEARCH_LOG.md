# Threshold-search research log

Project: asymptotically universal simultaneous amplification  
Track: exact/lower/upper threshold \(R_{\rm sim}\)  
Started: 2026-08-01 (America/Los_Angeles)

## Scope and discipline

This track uses only the update rules and inherited local project materials
during discovery.  No literature search or external contact is performed.
Finite computations are labelled reconnaissance unless converted into an
exact asymptotic argument.

## Checkpoints

### 2026-08-01  — initialization

- Read the inherited weak-selection formulas and phase-3 asymptotic report.
- Confirmed that the local record states the benchmark
  \(R_{\rm sim}\ge 1.2\), but contains no construction parameters from which
  to infer a proof.
- Began independent searches over exactly lumpable graph families, starting
  with two equitable vertex classes and then moving to mesoscopic modules.

Status: **OPEN / discovery in progress**.  Estimated completion toward a
rigorous new threshold result: **5%**.

### 2026-08-01 — separated module searches and corrected clique-star audit

- Built direct quotient solvers for symmetric and asymmetric weighted fans,
  weakly completed pair fans, subdivided stars, arbitrary fixed-length path
  arms, and two-hub theta graphs.  All finite outputs remain labelled
  numerical reconnaissance.
- Replaced the iterative neutral-pair calculation by an independent dense
  exact-equation solver for faster weak-selection searches, and retained a
  sparse iterative implementation for larger bounded-degree candidates.
- **NUMERICALLY OBSERVED:** a two-hub theta graph with seven length-four
  paths (three internal vertices per arm) and endpoint-edge weight about
  `0.206` has both weak-selection coefficients above the complete baselines.
  This is a finite weak-selection lead only; no full-fitness or asymptotic
  theorem is claimed.  The exact quotient chain has 13,728 states.  At
  endpoint weight `0.206`, its finite `r=1.01` Bd excess was approximately
  `3.08e-6`; the remaining full-fitness evaluations were not completed.
- Derived the trace process for a star whose center and leaf modules are
  cliques of unequal sizes.  An initial calculation without the mutant-target
  defense factor suggested a positive interval, but the direct dB rule shows
  that reverse invasion has an essential extra factor `1/r`.
- **PROVED (stated separated-scale limit):** Bd amplification requires the
  center/leaf internal-degree ratio `z>1`, whereas dB amplification requires
  `z<Z_{c,l}(r)<1`.  The exact positive decomposition

  \[
  D_{c,l}(r)=(l-1)(r^c-cr+c-1)
   +(c-1)r^c(r^l-lr+l-1)>0
  \]

  certifies the incompatibility for every `c,l>=2` and `r>1`.
- Added an exact rational verifier for the macro rates, both compact gamma
  formulas, the comparison equivalences, and the polynomial identity.

Status: **PROVED new broad-family no-go; global threshold remains OPEN.**
Estimated completion toward a rigorous global threshold result: **18%**.

### 2026-08-01 — singular-triangle construction and new lower bound

- Considered a clique center and many weakly attached copies of the weighted
  triangle with strong edge `AC=1` and weak edges `AB=BC=delta`.
- **EXACTLY COMPUTED:** as `delta -> 0`, isolated-leaf singleton fixation
  vectors are `(0,1,0)` for Bd and `(1/2,0,1/2)` for dB.  Both uniform
  establishment probabilities tend to `1/3`.
- **EXACTLY COMPUTED:** for dB, the inverse-degree entry sum satisfies
  `J_L(r) -> (r+2)/2` and the full effective forward/reverse factor is
  `r^3(r+2)/(2r+1)`.  This independently confirms the reverse-invasion
  defense factors.
- Derived the rare-migration trace rates directly from both update rules.
  With center size `c`, per-edge center weight `z`, and a three-vertex leaf,
  the leading simultaneous scale window is

  `6 delta/[c(3-2r)] < z < 2 r^2(3-2r)/[c(2r+1)]`

  for every fixed `1<r<3/2`.
- **PROVED:** take `c_N=N`, `M_N=N^2` leaves, `delta_N=N^-4`,
  `z_N=N^-3`, and complete center--leaf edge weight
  `epsilon_N=2^(-2^(N^4))`.  For both rules and every fixed `r>1`, the
  graph fixation probability tends to `1/3`.  Therefore it strictly exceeds
  the complete-graph baseline for every fixed `1<r<3/2` and all sufficiently
  large `N`.
- This gives the new rigorous lower bound `R_sim >= 3/2`, improving the
  inherited `1.2` benchmark.  It does not prove an upper bound.
- Added a from-definitions symbolic certificate and a full proof note.
  `verify_triangle_star.py` passes all exact assertions.

Status: **PROVED `R_sim >= 3/2`; exact global threshold remains OPEN.**
Estimated completion toward a rigorous threshold result: **55%**.
