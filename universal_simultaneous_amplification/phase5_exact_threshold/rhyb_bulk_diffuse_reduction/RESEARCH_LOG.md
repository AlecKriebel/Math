# Research log: bulk/root diffuse reduction

## 2026-08-13 15:47 PDT — exact root-to-adjoint cutoff implication

- Worked proof-first; no graph search, literature search, or external
  communication was used.
- Returned to the whole graph at physical root termination and wrote the
  exact Bd/dB linear branching pair.  Undirectedness realizes it as a
  reversible kernel and its uniform adjoint, with no fixed-rank compactness
  assumption.
- Computed the exact maximal-coupling defect hazards for both update rules.
  Their source-weighted killed-Green integral is the precise probability
  that the physical and branching chains separate before extinction or a
  population cutoff.
- Proved the quantitative alternative: unless the finite `1/n` layer,
  collision/competition Green budget, or false-establishment tail is of
  response scale, an endpoint simultaneous amplifier forces positive
  `D+(R_hyb-1)B` charge in a finite diffuse adjoint branching kernel.
- Identified the one closing diffuse theorem as
  `T_Rhyb>=0`, equivalently
  `(bar s-p0)+(R_hyb-1)(bar b-p0)<=0`.  The previously proved
  fitness-dependent support identity shows that `K_Rhyb>=0` is a stronger
  sufficient ground-energy target.
- Diagnosed exactly why `C(G)->0` and `t->1` in uniform `L1` do not finish
  the argument: they control the first source event, not its killed-Green
  occupation at the first response scale.  The balanced weak-cut theorem
  also shows the unavoidable `epsilon=Theta(1/n)` collision layer.
- Hostile-audited every `P`/`P^T` orientation and added an independent exact
  rational replay.  It reconstructs the physical, branching, and killed
  coupling generators on a nonregular weighted graph, checks the Green
  hitting bound, and separately reconstructs both complete-graph fixation
  baselines.
- Applied a second hostile-audit precision pass: replaced asymptotic
  “of-order” wording by the explicit lower constant, described the result as
  an aggregate cutoff implication rather than a mutually exclusive
  trichotomy, supplied the finite-band absorption proof that branching
  survival equals unbounded growth, stated the Bd/dB state-time
  normalizations, and checked that the singleton identity has no duplicated
  defect term.

The primary agent approved commit after the audit and exact replay.
