# Research log: global-holonomy static gate

## 2026-07-28 PDT

- Isolated the proposed static implication for \(H=\overline G\):
  \(K_4\)-free, every pair has a common neighbor, and every link is
  bipartite/isolate-free should imply \(\chi(H)\leq3\).
- Built a direct SAT/CEGAR discovery encoding with explicit link-color bits
  and iterative exact three-coloring cuts.
- CaDiCaL found witnesses immediately at orders seven through ten.  The
  first raw order-seven witness had 13 edges in \(H\) and one disconnected
  link.
- Enumerated the order-seven unlabeled boundary as an exploratory
  cross-check.  Found three isomorphism types with 12, 13, and 14 edges.
- Performed the required prior-art-in-repository audit.  C-064 already uses
  \(C_7\)'s seven-facet loop and nontrivial three-cycle to bound ridge
  holonomy, while C-020 already contains its two-attack failure tree.
  Accordingly, this artifact makes no novelty claim for \(C_7\) or the
  basic obstruction.
- Observed that the accepted \(G=C_7,\ H=\overline{C_7}\) control is
  stronger than the raw SAT witness for the newly proposed gate: all seven
  links are connected \(P_4\)'s.
- Repackaged
  \(\operatorname{Cl}(\overline{C_7})=\operatorname{Ind}(C_7)\) as the
  seven-vertex triangulated Möbius band.  Checked its facets,
  \(f\)-vector \((7,14,7)\), one boundary 7-cycle, and Euler characteristic
  zero.
- Computed independently
  \((\gamma,i,\alpha,\gamma^\infty,\theta)(C_7)=(3,3,3,4,4)\).
- Replayed C-020's accepted two-attack non-eternality certificate from the
  forced state \(\{0,2,4\}\): attack 1, then (on the sole dominating branch)
  attack 3.
- Implemented two independent greatest-kernel representations.  Both give
  empty three-guard kernel; the synchronous rank census is \(7+7\) in
  rounds one and two.
- Implemented a standalone verifier that enumerates all 33,867 labeled
  graphs through order six, proving that seven is the first possible order
  for failure of this static implication.
- Added a 64-graph truth-table audit of the SAT base and of all source
  coloring cuts at order four.
- Exploratorily checked the further closed-link condition through order
  nine; no non-three-colorable model appeared.  This is an OBSERVED
  nonclaim and is not used.
- Conclusion: the static/local-holonomy lane is exhausted.  A proof must
  couple link colorings through literal eternal-family survival.
