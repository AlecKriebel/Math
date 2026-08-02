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
