# Result: Rainbow Arborescences Across Arc Partitions

Problem30004008 / OWR-16633-026. Original disposition: **unsolved after five substantive author turns**. The following scoped proofs await independent review. No novelty certification is claimed.

## Strongest structural conclusion

An instance whose underlying simple graph is a **cactus**, with any finite number of cycle blocks and arbitrary input roots, has a rainbow spanning out-arborescence. The proof combines the articulation root-count reduction in Turn2 with the explicitly credited cycle theorem of Bérczi, Király, Yamaguchi and Yokoi, [arXiv:2412.15457v2, Theorem4.9](https://arxiv.org/abs/2412.15457v2). That imported theorem is not reproved here.

At a one-vertex separation with exclusive side sizes a,b, at least one side has enough colors rooted outside it to build that whole side greedily from the shared vertex. Reserve exactly those colors and solve the smaller arbitrary-root instance on the other side. This also proves existence when all blocks have at most six vertices, using the credited small-order theorem. The deductions concern unbounded graph families, with finite controls kept separate.

## Other scoped results

1. Turn1 gives exact localization to the union's unique source strongly connected component, plus greedy lifting and a root-multiplicity capacity sufficient condition
2. Turn3 gives necessary and sufficient color-reservation quotas for outward gluing of pendant pieces, an exact projected-root capacity test for using two-multi-root theory, and a balanced-block reduction
3. Turn4 gives the precise two-vertex forest/color/indegree interface and a valid theta example showing why naive tree restriction or single-directed-arc replacement loses essential information
4. Turn5 proves the standard directed matrix-tree coefficient identity in the chosen orientation and provides exact valid-instance counterexamples to real stability of the natural polynomial and to treating all-root arborescences as one matroid

These do not settle general strongly connected, biconnected input unions. Compatible colorful two-vertex interface states are not proved to exist universally, and the determinant coefficient has no established general positive lower bound.

## Boundaries and reproducibility

- Input classes are spanning out-arborescences; parallel colored arcs remain distinct
- The root of the output is free, not prescribed
- Source small-order computer verification through eight vertices is credited but not independently reproduced here
- Every finite test is a control of stated instances or identities, not a proof of the full conjecture
- The harmless one-vertex empty instance is immediate; nontrivial structural arguments use n≥2
- Run all five `verify_turnN.py` scripts from this directory; each stdout must match its corresponding `TURN_N_CHECKS.json`
- Historical manifests and final replay metadata bind the exact frozen author packet

Best-guess progress toward a full solution:25%, low confidence, as a planning estimate rather than a probability or proof claim.
