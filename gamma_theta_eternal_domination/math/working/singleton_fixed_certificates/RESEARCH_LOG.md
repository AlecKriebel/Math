# Research log: singleton fixed certificates

- **2026-07-28 PDT.** Isolated the two immediate false-constant sources
  left by C-119: a singleton demand in an anchor-fixed projection component
  and a cross-type edge whose exact-two endpoints are both anchor-fixed.
- **2026-07-28 PDT.** Exhaustively probed the greatest two-guard kernels of
  every unlabeled graph through order nine satisfying the parameter-two
  equality filters.  No retained pair occupied one side of a connected
  bipartite-complement component.  Random co-bipartite tests through order
  sixteen also found no exception.  These were discovery checks only.
- **2026-07-28 PDT.** Proved the component-transversal lemma directly by a
  shortest even complement path and one attack at its second internal
  vertex.  The length-two successor is nondominating; the other successor
  contradicts minimality.
- **2026-07-28 PDT.** Applied the lemma to frozen pair families.  A
  singleton marker in an anchor component is forced onto its demanded
  anchor side.  An exact-two vertex in its omitted-color anchor component
  would create two retained projected pairs forcing it onto both anchor
  sides, a contradiction.
- **2026-07-28 PDT.** Concluded that the C-119 immediate branch is empty:
  singleton anchor substitutions are true, exact-two endpoints are always
  free, and cross-type edges remain genuine binary clauses.  Arbitrary
  unit chains and residual bicycles remain open.
- **2026-07-28 PDT.** Selected `FCpbO` as the sharp all-anchor-fixed
  singleton control and `LFzJbZYhdrDZdM` as the free exact-two/cross-clause
  equality control.  The independent verifier reconstructed both greatest
  kernels, all five parameters, all 1,468 one-guard obligations, every
  response list and frozen component, ten free/free cross-type edges, and
  the exact response-coloring counts.  The final verdict was `PASS`.
