# Proof audit: existing Morse analogue for virtual resolutions

Audit date: 2026-10-21. Queue rank 1857; source identifier 20000012. This is an authored mathematical audit, not a new theorem or a claim of priority. It contains no copied source document or private coordination material.

## 1. Disposition and exact scope

**Accept `already_solved` only in the sense that the original broad existence question has a published affirmative analogue.** The AIM source, *Syzygies and mirror symmetry*, Resolutions, Problem 4.5, asks whether an analogue of cellular-resolution Morse theory exists for virtual resolutions. It does not specify the machine-generated Cox-chart criterion, a global minimization algorithm, arbitrary input modules, perfect matchings, or optimal Betti numbers.

HHL's finite sheaf-valued discrete Morse construction, actually used for toric line-bundle resolutions, supplies such an analogue. Its application is more than a verbal analogy: admissible acyclic matching removes contractible summands, the differential is a signed sum over gradient paths, and the resulting complex is chain-homotopy equivalent to the original. Line-bundle resolutions on smooth toric varieties have Cox-graded virtual-resolution realizations. This justifies the scoped affirmative disposition, without claiming that the AIM maintainers themselves marked the item solved, or that every stronger interpretation has been settled.

**Do not accept the generated specialization wholesale on this basis.** Its finite chartwise exactness criterion and its proposed global lifting/minimization implications are distinct statements. This audit neither proves nor certifies all of them.

## 2. Primary sources and mandatory metadata correction

1. AIM original problem: http://aimpl.org/syzygyms/4/ , Problem 4.5. The recovered original statement and the source gate identify the broad question, not a Cox-chart conjecture.
2. Andrew Hanlon, Jeff Hicks, Oleg Lazarev, *Resolutions of toric subvarieties by line bundles and applications*, Forum of Mathematics, Pi 12 (2024), e24, https://doi.org/10.1017/fmp.2024.21 . Inspected text: arXiv:2303.03763v3, dated 10 August 2024, https://arxiv.org/html/2303.03763v3 . Relevant parts: §§1.1, 3.4–3.5, 4.2, Appendix A, and Theorem 3.5's application of restriction.
3. Zengrui Han, *Minimal resolutions of toric substacks by line bundles*, inspected arXiv:2604.14384v3, dated **17 September 2026**, https://arxiv.org/abs/2604.14384v3 . Relevant parts: §§1.2–1.4, §§3–4, Theorems 1.1, 1.2, 3.9, 4.8, Lemma 4.7, and Remark 4.9.

**Resolved bibliographic correction:** the earlier source gate and metadata incorrectly labeled the inspected Han manuscript v1. The inspected PDF is arXiv:2604.14384v3, dated 17 September 2026. Its unchanged SHA-256 is 7ce5d9eba6e8693da2c75915f5c2282217869ca830b1c97cf79ad9c8c3ec5555 and its size is 436161 bytes. The public gate and metadata now record that inspected version; 15 April 2026 is not used as the inspected-version date. The HHL PDF header identifies v3, 10 August 2024 (698993 bytes, SHA-256 214b7dbeb28fd28e7ab5e78bc81bae434da0a820476994ab47e5070a21b0a393). Han remains a preprint in this audit; no independent publication-status verification or acceptance claim is made. This is an editorial bibliographic correction, not a change to the mathematical proof.

## 3. Exact finite Morse theorem used

Work in an additive category (in particular an abelian category of coherent sheaves) and with a **finite** graded quiver. Each edge lowers degree by one. Supply an orientation and an involution pairing length-two paths with opposite signs, such that the corresponding composites of coefficient morphisms agree. These conditions make the matrix differential square to zero, by pairwise cancellation. There is no need to take infinite coproducts or infinite sums of morphisms.

Choose a partial matching, meaning no vertex is incident to two matched edges. Reverse the matched edges and assume the resulting directed multigraph is acyclic. Require every matched coefficient morphism to be an isomorphism. Its signed coefficient is then also an isomorphism. The critical complex has one summand for each unmatched vertex. Between critical vertices of consecutive degrees, its differential is the sum over alternating paths of ordinary downward edges and reversed matched edges. Each reversed edge contributes the inverse of the original signed coefficient and one minus sign. This is the finite content of HHL Definitions A.1, A.4, A.7 and Theorem A.8 that is accepted here.

Multiple edges cause no hidden pivot issue: if one edge from a matched upper vertex to its matched lower vertex were retained as an unmatched parallel edge, that edge and the reversed matched edge would make a directed two-cycle. Acyclicity excludes this. Thus the matched edge is the full original differential component between its endpoints.

## 4. Independent proof of finite cancellation

Here is a direct verification, not an assertion that HHL supplies a full printed proof. HHL explicitly says the generalized proofs are omitted, relying on modifications of earlier discrete/algebraic Morse arguments.

Consider one matched pair A in degree n and B in degree n−1. Order the adjacent terms as A⊕U and B⊕V and write the differential block as

    d_n = [[a, b], [c, e]],

where a:A→B is the matched isomorphism. Change coordinates in degree n by x_A'=x_A+a^{-1}b x_U, and in degree n−1 by y_V'=y_V−c a^{-1}y_B. In these coordinates d_n is the block diagonal map with components a and e−c a^{-1}b. Since d²=0 and a is invertible, the differential entering A and the differential leaving B vanish in the transformed complex. Consequently A→B is a direct-summand contractible two-term complex. Removing it gives a chain-homotopy equivalent complex, with the reduced differential e−c a^{-1}b. The contraction of the discarded pair is a^{-1}:B→A; all coordinate transformations and the contraction are morphisms in the original additive category.

Iterate this operation over the matching. A matrix entry created by one cancellation records a directed path through the reversed cancelled pair. Inductively, every surviving entry is the sum of such path weights through already cancelled pairs. In particular a surviving matched pivot cannot be altered by the cancellation of other pairs: an extra path from its upper endpoint to its lower endpoint, combined with its own reversed edge, would give a directed cycle in the original reversed graph. Therefore every remaining pivot stays the original isomorphism, and all cancellations are valid.

There are finitely many pairs. A finite directed acyclic graph has only finitely many directed paths, so every resulting matrix entry is a finite sum. Expanding the successive Schur complements gives exactly the alternating-path formula, with one minus sign for each reversed matched edge. Only alternating paths can connect vertices whose degrees differ by one: a reversed step raises degree, an ordinary step lowers it, and partial matching prevents consecutive reversed steps; with critical endpoints the path begins and ends downward, forcing alternation at this degree difference. Thus the final differential is precisely the finite Morse differential described above.

The successive coordinate changes, projections, inclusions, and contractions compose to a chain-homotopy equivalence. It follows both that the final differential squares to zero and that all homology objects are preserved. This proof works for sheaves, not just modules over a field. If an augmentation to a sheaf M is present, compose it with the resulting inclusion map; the reduced augmented complex resolves M whenever the original does. No preservation of an arbitrarily unmodified augmentation is presumed.

## 5. Finiteness is substantive, not cosmetic

HHL Appendix A's displayed abstract definitions do not explicitly impose finite quivers or a summability/well-foundedness condition. This audit does **not** endorse an unrestricted infinite version. Even local finiteness and acyclicity together do not suffice.

For example, over a field k let C_1=⊕_{n≥0} k a_n, C_0=⊕_{n≥0} k b_n, with d(a_n)=b_n−b_{n+1}. Match a_n→b_n for every n. All matched maps are isomorphisms, no vertices are critical, and the reversed graph is the locally finite acyclic ray b_0→a_0→b_1→a_1→⋯. Nevertheless H_0(C)=k: the sum-of-coefficients map on C_0 has kernel equal to im d. A zero critical complex cannot be homotopy equivalent to C. Elimination would require infinite sums outside the direct sum.

Accordingly, for infinite inputs one needs an appropriate termination/local-nilpotence condition or a carefully specified completion and convergence theory; finite valence alone is not a repair. HHL's relevant toric applications arise from finite rational hyperplane arrangements on compact real tori, giving finitely many strata and incidences. In a bounded fundamental domain only finitely many translates of any of the finitely many integral hyperplanes occur. The finite argument above therefore suffices for the accepted application.

## 6. Why this is genuinely a toric virtual-resolution analogue

HHL §§3.4–3.5 attach line bundles to strata of a real torus and boundary morphisms to exit paths. Proposition 3.10 verifies the oriented-quiver and coefficient-composition conditions. Nonregular cell structures are accommodated by multiple incidence edges; regular CW structure is not imposed indiscriminately.

In §4.2, Proposition 4.2 constructs a matching after restriction along the toric open immersion associated to deleting a ray. The matched incidences are the prescribed positive incidences for that ray. The proof verifies the partial-matching property, rules out cycles by lifting paths into a convex stratum of the coarser arrangement and using a strictly monotone linear coordinate, and verifies that matched maps become identities after restriction because the remaining ray data agree. The critical strata and gradient paths identify the Morse complex with the coarser-arrangement complex; orientations give the required signs. The finite theorem therefore provides an actual homotopy equivalence of line-bundle complexes, used in Lemma 3.3 and the proof of Theorem 3.5.

The construction does not merely cancel independently chosen chartwise matrices and then assume that they glue. HHL starts with globally defined line-bundle complexes and proves a restriction compatibility for those complexes. That distinction prevents a false descent argument.

HHL Theorem A constructs a resolution of the pushforward of the structure sheaf of a closed toric substack by sums of Thomsen line bundles, of length its codimension, when the ambient toric stack is covered by smooth stacky charts. The introduction states its results over an algebraically closed characteristic-zero field. In positive characteristic the local-model admissibility requirements in Remark 1.2 and Definition 2.40 must be retained. Corollary C states that a finitely generated Pic(X)-graded B-saturated module over the Cox ring of a smooth projective toric variety has a virtual resolution of length at most dim X. Projectivity is used for the cited vanishing/Fourier–Mukai argument and must not silently disappear.

The algebraic connection is sheafification: a finite graded Cox-free complex representing a resolution by sums of line bundles is virtually exact because its associated sheaf complex is exact. It need not be exact as a Cox-module complex; irrelevant-locus homology is allowed. Morphisms between the line bundles have their standard homogeneous Cox descriptions in the smooth toric setting. This supplies the bridge between the finite Morse operation on line-bundle resolutions and virtual resolutions. Corollary C is an existence result for arbitrary B-saturated modules under its hypotheses, not a Morse-minimization algorithm for every supplied module complex.

## 7. Chart and descent cautions

For a maximal cone σ with complementary monomial u_σ, the affine toric chart has ring (S[u_σ^{-1}])_0. The full graded localization S[u_σ^{-1}] is the Cox-side localization, not the chart coordinate ring itself. Smoothness permits the needed local interpretation of line-bundle twists, but does not erase the distinction.

In a monomial cellular matrix a matched face coefficient is a unit after this localization exactly when all its non-inverted variable exponents vanish, assuming the scalar incidence coefficient is nonzero. Equality of divisor classes alone does not prove this unit condition. In a smooth complete fan, if the same monomial ratio is a unit on every maximal chart then each variable exponent must vanish, because every ray belongs to a maximal cone where its variable is not inverted. Thus this particular globally valid monomial matching forces equal full labels. This elementary statement is not an impossibility theorem for all global reduction procedures.

Independent chartwise critical complexes may have incompatible summands, transition maps or homotopies. Even a sheaf complex assembled from local reductions need not have terms that split as global sums of line bundles. Therefore local cancellations alone do not construct one smaller global free Cox complex. The accepted published analogue does not assert this unjustified lifting step.

## 8. Han's stronger but restricted result

The inspected September 2026 preprint works with complex coefficient vector spaces and standard Hermitian inner products. It decomposes the HHL differential into equal-line-bundle blocks and a strictly decreasing part for a finite Bondal–Thomsen poset. The Moore–Penrose inverses contract each equal-line-bundle block onto its harmonic homology. Lemma 4.7 proves nilpotence of hδ because δ strictly decreases the finite poset while h preserves its label. Thus Theorem 3.9's perturbation sum is genuinely finite. The resulting differential is pΣi, and the perturbed inclusion/projection are not generally the original harmonic inclusion/projection (Remark 4.9).

Theorem 4.8 obtains a resolution with no invertible differential entries within that construction. The Cox-language Theorem 1.2 applies specifically to a **normal closed toric subvariety of a simplicial projective toric variety**, resolving its quotient S/I_Y virtually. Retain this scope and the characteristic-zero/complex framework actually used; do not generalize the Moore–Penrose argument to arbitrary fields without further work. Perfect Morse matching is an optional alternative contraction, not a universally proved existence theorem. Nor does 'minimal' here establish uniqueness or global Betti optimality among all possible virtual resolutions of an arbitrary module.

This later preprint reinforces the existence of constructive reductions but is not required for the affirmative answer to the original broad question. The published finite HHL application already suffices.

## 9. Acceptance boundary

Accepted: an existing, published finite sheaf-valued Morse analogue with signed gradient-path differentials and chain-homotopy invariance, actually used in toric constructions yielding virtual resolutions. This supports `already_solved` for the original existential question only.

Not accepted by this audit: unrestricted infinite-quiver acyclicity, universal perfect matchings, universal virtual minimization, uniqueness of minimal virtual resolutions, arbitrary characteristic for Han's construction, identification of full Cox localization with a toric chart ring, or automatic descent of arbitrary local cancellations. No new proof of the generated Cox-chart criterion is claimed. The Han inspected-version metadata correction is resolved in this package.
