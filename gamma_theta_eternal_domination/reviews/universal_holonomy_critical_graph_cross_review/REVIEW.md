# Cross-review: line-graph/holonomy referee lane

Date: 2026-07-26 (PDT)

Target:
`math/working/universal_holonomy_critical_graph_referee.md`

Target SHA-256:
`382f7af69da1f0d2c81faaa4fe0569c6b3c54529580b3ddb001fe0850664b198`

## Verdict

**ACCEPT.**

I found no false proved statement, all-guards substitution, complement
reversal, or circular use of the gamma--theta conjecture.  The note proves a
genuine family exclusion and correctly presents it as a stress test rather
than a resolution.

## Proof checks

1. In a simple triangle-free graph, every pairwise-intersecting edge family
   has a common endpoint.  This validates the maximal-star description of
   cliques in the line graph, the local-link formulas, and
   \(i(\overline{L(F)})=\alpha(\overline{L(F)})=r\).
2. The matching bound is sound in both cases.  A perfect matching has size
   at least \(r\) by the disjoint-neighborhood count around an edge.  If a
   maximum matching leaves \(x\) exposed, the \(r\) neighbors of \(x\)
   occupy distinct matching edges.  Three disjoint \(F\)-edges then dominate
   \(\overline{L(F)}\).
3. Theorem 2's three values of \(q\) exhaust the legal responses.  In the
   \(q=1\) case, failure of both possible moves would make the third edge at
   \(x\) intersect all three original guards, contradicting domination.  In
   the \(q=0\) case, failure of all three moves forces the guards to be the
   full star at one cubic vertex; the removed star edge cannot also meet the
   attacked edge.  Thus at least one adjacent guard move always leaves a
   dominating triple.  Every attack is unoccupied and exactly one guard
   moves.
4. The domination/diameter dictionary is exact: a pair dominates the
   complement precisely when it has no common line-graph neighbor.  Cubicity
   supplies a common neighbor for adjacent line-graph vertices, so the only
   alternatives are \(\gamma=2\) and \(\gamma=3\).
5. In Theorem 3, all edges lie within line-graph distance two of the fixed
   edge, so every other \(F\)-edge meets the four-vertex set \(C\).  The
   degree-slot equation
   \(3|X|+2|E(F[C])|=8\) leaves \(|X|=0\) or \(2\).  The first case is
   \(K_{3,3}\); the second creates two disjoint edges with no common
   line-graph neighbor, contradicting diameter two.  Hence a cubic
   triangle-free class-II host necessarily has \(\gamma=2\), while Theorem
   2 gives \(\gamma^\infty=3\).
6. Proposition 5 correctly identifies the gauge issue: a singleton clique
   overlap fixes one color and leaves an \((r-1)!\)-element stabilizer, so no
   canonical permutation holonomy follows from the overlaps alone.

Before this review was rebound, a malformed “\(ux=vx\)” phrase in Theorem
1's proof was replaced by the intended statement that the distinct edges
\(ux\) and \(vx\) would form a triangle with \(uv\).  This was a
typographical correction only.

## Replay

I reran the independent audit with warnings treated as errors.  Its output
matched the frozen evidence byte for byte.

- Audit SHA-256:
  `ee3225a42d73ed5faf1d699de31076ac454b26cbc81b0e13104cb42f2f4a6b57`
- Evidence SHA-256:
  `97b0274a8c410ac62f35b8451c8459bdfe5543fac4e25a3fe6c9879ca5a0e4c3`

No novelty or publication-priority judgment is made.
