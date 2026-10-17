# Verification summary: rooted cyclic-block insertion

The proof packet establishes a one-sided cyclic-block insertion theorem, explicit rooted half-plane models for both vertex orbits of the source nonplanar block, a dimension-three degree-four cyclic-core fixture, and a uniform dimension-three family with cyclic-core degree 3k. The general triangle-representation problem remains unresolved.

The complete mathematical report has 19,046 bytes and SHA-256 `a96576d966ac56a2d899ecb5f7f6a743e123f91068504d3da5884aea02f9f8db`.

## Exact checks

- 2,788 tested subfamilies, each checked by exact rational polygon clipping and independently implemented active-line intersection enumeration.
- Both rooted half-plane models: all 31 nonempty subfamilies per model.
- Both explicit wedge models: full nerves for one and two blocks, and all pairs/triples plus declared edges for three blocks.
- Actual recursive insertion at rational private side points, first rooting a fresh block at vertex 5 and then rooting another at vertex 1: the nine-vertex intermediate full nerve and the thirteen-vertex pair/triple nerve are correct, with every old triangle unchanged. Incidence dimension is not asserted for this auxiliary regression.
- Strict common interior witnesses for every displayed maximal edge.
- Complete incidence-order comparisons for root-1 wedges with k=1,2,3,5,10,30 and the separate root-5 two-block certificate, including all 420 ordered pairs for the latter.
- Exact 2-core degree and K3,3-subdivision checks.
- Five independent geometric controls include lower-dimensional point/segment contacts and disjointness.

The canonical checker passes under normal Python, `-O`, and `-OO`. Its three output files are byte-identical; their operational identity is retained separately rather than distributed.

Seven genuine disposable-source mutations are each rejected in all three modes, giving 21 required failures. They reverse the rooted half-plane, collide different blocks, erase reverse block order, move a required root witness outside, remove the reach of thin triangles, disable the explicit gates, and corrupt a raw incidence order. Every failure has the intended deterministic diagnostic. Four embedded negative controls additionally test cross-block collision, a root witness outside the old root, invalid block order, and an explicit failing gate. No timeout is interpreted as rejection.

## Reproducibility and limits

The complete author payload, including the previously accepted proof/review inputs, exact data, scripts and diagnostics, is sealed in a per-file byte-count/SHA-256 manifest. The preservation workflow creates an actual recovery archive and content-addressed byte store, restores each into a fresh directory, compares complete file inventories and bytes, and reruns the checker in all three modes and the mutation harness from each restored payload. The final preservation receipt and its external hash pin record those outcomes.

Finite computations certify the displayed examples and implementation. The universal claims depend on the full proofs: local half-plane substitution, rational scaling into a private side neighborhood, explicit rooted models and full-nerve stability, and the uniform complete pair-type realizer argument. No general dimension-preservation theorem for rooted gluing is assumed, and no geometric impossibility is inferred from order-search limitations.
