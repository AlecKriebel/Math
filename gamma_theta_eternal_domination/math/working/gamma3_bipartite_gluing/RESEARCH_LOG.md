# Research log: \(\gamma=3\) bipartite gluing gate

## 2026-07-28 (PDT)

- Read C-108, C-123, the accepted full-list slice, and the full-response
  witness lemmas in full.
- Derived the exact target translation.  With
  \(B=N_{\overline G}(x)\), once deletion pairs already have complement
  common neighbors, \(\gamma(G)\ge3\) is equivalent to \(B\) totally
  dominating \(H'=\overline{G-x}\).  In the C-108 setting \(B\subseteq R\).
- Derived the full-root refinements: every \(B\)-vertex sees at most one
  root anchor, the three anchor spokes in \(B\) are nonempty and disjoint,
  and \(H'[B]\) is isolate-free (and bipartite when \(H'[R]\) is).
- Replayed the existing candidate databases under the strengthened target
  condition.  No witness occurred among 8,587 edge-toggle rows or 391
  extension rows.  These are OBSERVED bounded probes only.
- Tested the sharp C-123 \(L(K_{3,3})\) control under two-vertex
  extensions.  Fixed-marking variants failed ridge covariance.
- Enumerating exact covariance-class markings inside that bounded
  two-vertex template found the explicit target-order-12 witness
  `KxU[ISrR}NP^`.
- Wrote a standalone ordinary-set verifier.  It independently checks the
  graph data, common-neighbor witnesses, total domination, bipartition,
  maximal triangles, nonvacuous covariance classes, all 18 one-step
  successors, unique deletion coloring, exact parameters, greatest
  one-guard kernels, and an adaptive rank-three attack tree.
- Conclusion: the strongest static \(\gamma=3\) gluing shortcut is
  refuted.  Full multi-step eternal closure remains the exact missing
  mechanism; the universal conjecture is unresolved.
