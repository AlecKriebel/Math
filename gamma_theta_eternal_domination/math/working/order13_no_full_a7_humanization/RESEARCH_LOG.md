# Research log

## 2026-07-28 (PDT)

- Extracted the original 18,143-clause DRAT input core and mapped clauses to
  domination, closure, coloring, response-list, signature, and symmetry
  blocks.
- Found and corrected a local clause-labeling error: representative
  signature, list, and mate blocks are interleaved in the production
  generator.  Early representative-only ablation outputs made before the
  correction were excluded and rerun.
- Proved the semantic redundancy of the explicit alpha, selected-state
  domination, family-nonempty, response-implied edge, signature-implied
  negative-list, and known-nonneutral no-full clauses.  The reduced formula
  remains UNSAT.
- Tested anchored closure radius.  Radius one is SAT; radius two is UNSAT;
  closure on states disjoint from the reference triple is unnecessary.
- Generated an addition-only RUP proof for the radius-two formula and replayed
  it successfully with pinned DRAT-trim.
- Tested the three two-of-three anchor-slice relaxations.  All are SAT.
- Wrote and ran a standalone direct checker for the three controls.  Each
  control has exact parameters \((3,3,3,4,4)\), satisfies every imposed
  partial one-guard obligation, and fails closure in the omitted
  single-anchor slice.
- Conclusion: no universal theorem emerged, but the “two anchor slices
  suffice” route is sharply refuted.  The order-13 residual contradiction is
  a genuinely three-way depth-two interaction.
- Estimated completion of this proof-humanization lane: **100%**.  Estimated
  completion toward a universal resolution of the gamma--theta conjecture:
  **well below 50%**; this result localizes a mechanism but does not settle
  the conjecture.
