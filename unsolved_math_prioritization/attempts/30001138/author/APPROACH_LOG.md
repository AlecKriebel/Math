# Five-approach research log

Research date 2026-10-04, UTC. Exact target: 30001138 / OWR-3385-009.
Status: five approaches completed; no full resolution. The progress percentages below are rough judgments toward the full mathematical target, not probabilities or certificates.

1. **18:01-18:07, spectral/nullspace route.** Verified the source's actual spatial-linking formulation. Inspected Izmestiev Theorem 2.4, its proof and Appendix A, plus the 1999 nullspace conjecture and the 2015/2017 Strong Arnold paper. Derived the necessary equality mu(G)=4 and the exact implication to the conjectured nullspace-flatness question. This blocks any shortcut from 4-connectivity, path k-linkedness, or Strong Arnold to an unlinked natural embedding. A proposed convex interpolation of admissible matrices was explicitly tested and rejected by the exact 2-by-2 signature countercontrol in the proof and verifier (completed 18:20). It is not a corank-four counterexample or a disconnectedness theorem. General result: unresolved. Completion estimate: 5%.
2. **18:05-18:09, extremal graph theory and simplicial rigidity.** Compared the general K6-minor edge bound m<=4n-10 with the simplicial lower bound and its d>=4 equality case. Supplied a full stacking disk-shortcut proof, excluding every simplicial four-polytope. Checked Kalai's exact dimension condition visually; did not transfer it to simple or arbitrary polytopes. Completion estimate: 12%.
3. **18:06-18:10, facet disks and apex geometry.** Proved that a cycle contained in a facet bounds a disk disjoint from the skeleton, then excluded every pyramid. Implemented a finite sufficient certificate testing whether every disjoint pair has a facet-contained member. This proves splitness without confusing it with vanishing linking number. Completion estimate: 14%.
4. **18:08-18:16, product construction and forbidden minors.** Tested prospective witnesses from products of polygons and vertex truncations. Found fixed, exactly verified Petersen-family minor models for the four-cube, triangle times hexagon, and completely truncated simplex. Exhaustive cycle-mask checks for triangle times triangle, square and pentagon give positive facet-disk certificates. Factor contractions extend these to exclusion of all polygon products. All 7 stored Petersen-family graphs include explicit move derivations; the three used targets use Delta-Y moves only. Partial truncations at 0,1,2 original simplex vertices pass the facial test; 3 truncations do not. Seeded random searches for 2,3,4 truncations each found no minor in 5,000 trials, which is inconclusive and is not used to assert linkless embeddability. A longer redundant search for the triangle-pentagon graph was interrupted after its exhaustive positive certificate had been obtained; it is not evidence for a negative minor result. Completion estimate: 18%.
5. **18:10-18:16, low-order affine-dependency/Gale route.** Gave a complete no-example proof through six vertices, handling zero dependency coefficients by a pyramid reduction and nonzero coefficients by support sizes (2,4) and (3,3). The criterion for an edge is derived from the affine evaluation space rather than assumed from a diagram. The arithmetic is replayed exactly. It does not classify seven or more vertices. Final completion estimate: 18%.

## Additional literature check

The 2025 paper *Linear linkless embeddings: proof of a conjecture by Sachs* and the March 2026 preprint *A Gap in Stanfield's Proof of Sachs' Linear Linkless Embedding Conjecture* were both inspected. The flagged passage in the former agrees with the location described in the latter. The criticism is a proof-gap report, not a counterexample to the claimed theorem. More importantly, neither statement controls a specified natural polytope-boundary embedding. Neither is used as a theorem here.

## Exact limitations

- No full proof, counterexample, or candidate resolving the original existence question.
- No numerical or mod-two linking computation is used as a certificate of splitness.
- Negative random searches prove nothing about missing Petersen minors.
- The facet-cover test is sufficient, not necessary. An uncovered pair need not be linked.
- The verifier certifies finite graph data, not the full lower-bound, Mader, or spectral theorems.
- Literature searches did not verify a general prior solution; absence of a search hit is not a proof of current open status or novelty.
- The newly authored proofs and certificates require a fresh independent audit before any result promotion.
