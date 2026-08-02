# dB fitness-two collision reduction

This folder contains an exact aggregate reduction of the open conjecture

\[
\rho_{\rm dB}(G,2)\le\rho_{\rm dB}(K_n,2).
\]

- `R2_GREEN_COLLISION_REDUCTION.md` gives the proof and states the remaining
  stationary cut-versus-dispersion inequality.
- `verify_green_collision_reduction.py` is the independent exact verifier.
- `RESEARCH_LOG.md` records the discovery status.
- `aggregate_odds/` gives an exact Farkas obstruction to the sufficient
  nonnegative additive-potential certificate; it leaves the component and
  aggregate odds conjectures open.

The verifier also certifies that a proposed pairwise stationary-correlation
shortcut is false, both on the unweighted path `P4` and across a positive
edge of a regular weighted `K4`.  These counterexamples do not refute the
surviving summed component-odds conjecture.

The reduction is proved.  The final universal sign is open.
