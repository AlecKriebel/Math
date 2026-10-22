# Audit corrections and scope

No new mathematical correction is required to the substantive partial claims. Apply the packet's existing n>=2 exclusions to the stationary-optimizer analysis and two-simplex formula.

Important clarified counts:
- Turn 2/5 six-normal example: 20 invertible bases, 14 feasible bases, five distinct vertices; squared norms 3 and 6.
- Turn 4 ten-normal example: 252 bases = 4 singular + 189 invertible infeasible + 59 invertible feasible; 34 distinct vertices. Active-facet counts: 32 vertices with five, one with six, one with seven. The normal hull has 34 actual facets, but its floating-point triangulation has 40 simplices.
- A triangulated-facet count is not automatically a true facet count.

Scope warnings retained:
- Equal-weight centering and isotropy are extra assumptions.
- The optimizer identity is necessary only under its regular hypotheses; it is not an optimality certificate or global theorem.
- The combinatorial weighted-facet counterexample has no claimed spherical/isotropic structure.
- Formula (D) needs all bases nonsingular as written; singular Cramer terms may survive.
- Formula (V) is unproved and sufficient, not established equivalent to the conjecture.
- Both numerical scripts are finite floating-point diagnostics.

Reproducibility clarification: all five exact checks and Turn 4 diagnostics replayed exactly. Turn 3 diagnostics agree in counts and conclusions but have maximum floating-point discrepancy 3.3306690738754696e-15.

Historical status clarification: the pinned author's statement that independent review had not yet occurred was true at its freeze. The present audit checks scoped validity only, without changing exhausted/unresolved status, author-turn count, or novelty status.

No remote changes were made.
