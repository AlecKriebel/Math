# Research accounting

All timestamps are 3 October 2026 UTC. Completion percentages are subjective estimates of progress toward a correct full resolution, not calibrated correctness probabilities.

## Approach 1: classical obstruction and scope separation

15:56–15:59. Completion estimate: 20%.

Recovered and visually checked the original conjecture. Established that the existing PL-source theorem and the reconstruction theorem are distinct from the unrestricted topological target. Proved the d=1 edge-count case and identified the exact stellar-subdivision family whose augmented skeleton is the Flores complex. Later exact checks certify the deleted-product cycle and its odd moment-curve evaluation in dimensions 1–4. This route alone does not address non-PL source triangulations.

A direct Alexander-duality linking attempt isolates a genuine issue: a cycle in the vertex complement that links the missing-face boundary must be completed to a deleted-product witness. Linking alone does not establish invariance under arbitrary re-embeddings. No unrestricted proof was claimed from that observation.

## Approach 2: face-ring dimension jump and metastable embedding

15:59–16:06. Completion estimate: 70%.

Derived the Koszul exact-sequence lemma: after the 2d+1 generic ambient parameters, adding a missing d-face raises degree d+1 by exactly one while preserving degree d. The regularity argument is necessary; a raw count of monomials would leave a gap. Combined the lemma with unchanged-complex ambient extension and middle Lefschetz surjectivity. This proves no PL embedding for every source triangulation. The Haefliger–Weber existence bound then gives full topological non-embeddability for d≥3, but explicitly fails at d=2.

A separate targeted mathematical check confirmed the Koszul degree bookkeeping, ambient quotient map, simultaneous parameter choice, and metastable range. The final proof uses the published Karu–Xiao characteristic-zero anisotropy theorem on integral homology spheres.

## Approach 3: flag base and four-dimensional bistellar transfer

16:02–16:10. Completion estimate: 95% before full independent review.

Derived a replacement for the global standard-PL-sphere hypothesis in the dimension-four Nevo–Wagner proof. Any triangulated topological 4-sphere is a combinatorial 4-manifold, without asserting that its PL structure is standard. The complement of a bistellar 4-ball is a collared simply connected acyclic PL manifold, hence contractible. This suffices for the general-position filling maps used in obstruction transfer; an embedded filling disk and a PL-standard complementary ball are unnecessary.

The barycentric subdivision is flag and has no missing triangles. Pachner connects it to the original triangulation within the same PL class. The local transfer theorem, with the checked replacement hypotheses, propagates the nonzero obstruction from this vacuous base. The two new-missing-face cases use only chain algebra and linking in the explicit bistellar ball. A separate targeted check found no further global PL-standardness input.

Together with Approach 2 and the low-dimensional cases, this yields the complete candidate proof. Stopped proof search early after three substantive approaches; the remaining budget was not spent manufacturing extra attempts. Fresh whole-packet adversarial review is still required.

## Exact controls and freeze

16:11–16:14. Completion estimate: 95%, unchanged pending review.

The standard-library checker passed. It verifies the stellar example, h-vector symmetry, the exact dimension jump over F_101 for d=1,2, four explicit Flores witness cycles, absence of missing triangles in the barycentric control, and the metastable bound. The controls support bookkeeping and do not replace the universal proof. Source visual QA confirmed the original target. Public files were separated from locally retained source documents. No remote mutation, DOI, release, or external communication was performed.
