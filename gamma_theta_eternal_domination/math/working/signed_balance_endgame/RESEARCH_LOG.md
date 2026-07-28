# Research log: signed-balance exact-two-list endgame

- **2026-07-28 PDT.**  Started from accepted C-111.  Proved that
  \(\gamma=3\) gives every physical port a same-type complement mate.
  Combined the mate with C-079 to make projection side-purity universal.
- **2026-07-28 PDT.**  Proved that every cross-type complement edge has
  only third-type outside common neighbors and hence belongs to a literal
  transversal triangle.  Recast the coloring problem as signed balance:
  same-type edges flip chirality and cross-type edges preserve it.
- **2026-07-28 PDT.**  Audited the shortest-cycle argument independently.
  A gamma-supplied outside two-path shortens every unbalanced cycle of
  length at least seven; at length six the edge signs repeat in opposite
  pairs.  Enumerated the five residual skeletons.
- **2026-07-28 PDT.**  Extracted literal one-guard attack trees for
  `0012`, `00011`, and `00121`.  Found a one-transversal attack tree for
  `00102`, with the two potentially confusing misses checked in the
  correct order:
  \(\{a,y,z\}\) misses \(x_2\), while
  \(\{a,x_0,y\}\) misses \(x_1\).
- **2026-07-28 PDT.**  Excluded the last skeleton `00101` using only the
  third-type transversal witnesses on two adjacent cross edges.  If the
  witnesses coincide, a forced state is nondominating; if they are
  distinct, one attack at the third anchor has three explicitly
  nondominating successors.  This audits the complete witness-collision
  partition.
- **2026-07-28 PDT.**  Wrote `verify_symbolic.py`.  It independently
  enumerates the type words, checks every direct response, unoccupied
  attack, blocked move, domination miss, collision case, and coloring
  truth-table row.  Strict execution returned `PASS`.

The frozen theorem is deliberately limited to a chosen independent
retained state at which **every outside list has exact size two**.
Singleton-list and full-list branches remain open, as does the complete
parameter-three case and the universal gamma--theta conjecture.
