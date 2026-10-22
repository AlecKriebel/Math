# Independent audit of KP-3.77

## Decision and exact scope

ACCEPT_CORRECTED_RESTRICTED_PARTIAL. The reviewed outcome is an unsolved, stopped partial investigation of catalog ID 2875, rank 916, after four of five allowed substantive approaches. No witness, counterexample, universal nonexistence theorem, novelty claim, or exhaustive worldwide status determination is accepted or implied.

All six original authored members were inspected. Their mathematical content is sound under the ordinary connected-ambient convention. A minimal clarification in Proposition 4.1 makes that convention explicit and removes a premise that was tacit in the converse. The accepted target is the exact corrected six-member archive identified in ACCEPTANCE.json, not an arbitrary later edit. The complete original archive and external manifest remain included without alteration. The correction is independently replayed from the original using CORRECTION.patch. Only proof.md changes.

The authored report still contains its historical statement that independent audit was pending. This audit is a separate, subsequent acceptance record; that historical provenance has not been silently rewritten. The correction does not change the unsolved 4/5 disposition or add an approach.

## Exact target and inherited material

The target agrees with modern K3 Problem 3.77 on printed p.186: the entire boundary of a compact orientable hyperbolic 4-manifold is one hyperbolic rational homology 3-sphere. The proof keeps dimension, compactness, curvature normalization, rational coefficients, orientability and connectedness visible. Extra closed components of a putative filling can be discarded. No rational-homology-ball, simply-connected, arithmetic, spin or fixed-volume condition is silently imposed. A cusp, an immersion, one boundary component among several, or a merely smooth separator is insufficient. This is not the differently numbered 1997 problem.

All bytes of the three supplied corpora were independently rehashed, and both catalog and complete-problem inputs contain exactly one ID-2875 record. The catalog rank is 916. The complete record and associated empty report reproduce the specified pair digest using the stipulated default sorted JSON serialization. The statement digest agrees as well. The inherited record contains literature triage, not an inherited proof or computation. These identity checks establish provenance; they do not validate a mathematical assertion in the data.

## Involution obstruction and attribution

Proposition 2.1 is correct. A rational homology 3-sphere is connected and orientable. For a free orientation-reversing involution, the quotient is a closed connected nonorientable 3-manifold. Transfer over Q injects the quotient's homology into the covering space's homology because the projection-transfer composite is multiplication by two. Thus its intermediate rational Betti numbers vanish; its top rational homology vanishes by nonorientability, contradicting Euler-characteristic multiplicativity.

An independent check uses Lefschetz: an orientation-reversing self-map has trace 1 on H_0 and -1 on H_3, and no intermediate homology. Its Lefschetz number is 1-(-1)=2, so it has a fixed point. This also shows why the obstruction is stronger than an involution-only argument. It does not exclude every possible orientable filling.

The collar orientation test has sign -deg(tau), because the normal coordinate reverses when the two half-collars meet. A free involution supplies a manifold local model, and orientability requires the forbidden orientation-reversing tangential sign. FKR's Introduction, Lemma 3.1 and Lemma 7.10 explicitly contain the construction, orientability issue and rational-homology obstruction. The author's attribution is accurate. FKR's Theorem A is not misreported as constructing orientable fillings. [FKR](https://math.rice.edu/~ar99/FKR_Trans.pdf)

## Covers and restricted gluings

Proposition 3.1 is valid without a regular-cover or boundary-pi_1-injectivity assumption. The boundary normal line is globally trivial. Since the boundary is orientable, the orientation character of the ambient manifold restricts trivially to its peripheral image. The connected orientation double cover therefore has precisely two boundary copies. Every connected orientable finite cover factors through it, and surjectivity supplies a nonempty preimage over each boundary component.

For an independent algebraic formulation, let G=pi_1(W), let P be the image of pi_1(M), let w:G -> Z/2 be the surjective orientation character, and let H <= ker(w) classify the cover. Components of the lifted boundary correspond to double cosets H\G/P. Because H and P lie in ker(w), the rule HgP -> w(g) is well-defined and surjective. There are at least two double cosets. For normal H the count is [G:HP], which is even; that ordinary index formula must not be substituted for the double-coset count in arbitrary covers. The authored argument correctly asserts only at least two in general. It does not assert that higher lifted boundaries retain rational-homology-sphere homology.

Proposition 3.2 is valid for exactly its permitted operations. An orientation on the final manifold restricts to orientations on the original piece interiors; hence no relabeling of piece orientations can repair a forbidden whole-boundary self-identification. With only pair gluings left, a final connected component assembled from pieces of boundary counts 2r_i has boundary count 2 sum(r_i)-2e. Initial pieces cannot split under these quotient gluings. The parity conclusion is therefore componentwise. New cuts, arbitrary higher covers, corners, partial-boundary identifications, pieces with odd counts, and other geometric constructions are outside the proposition. No broader obstruction is inferred.

## Double and cut clarification

Proposition 4.1's intended equivalence is correct. The original statement did not explicitly say that the closed ambient manifold is connected, and its converse began by referring to an orientable hypersurface before deriving that fact for a general closed hyperbolic M. Under the usual meaning of a separating hypersurface in its ambient connected component, these are convention/proof-clarity issues rather than a counterexample to the intended theorem.

The derivative makes two changes only: it requires a closed connected orientable hyperbolic 4-manifold; and its converse explicitly states that a connected separating embedded hypersurface is two-sided, hence orientable, and has exactly two complementary components. The correction is not an extra assumption on a hypothetical witness: doubling a connected witness already yields a connected ambient manifold.

For the forward direction, gluing W to its oppositely oriented copy along the entire boundary gives an oriented closed double. Reflection in the hyperbolic local boundary model makes the metric smooth with curvature -1. Compactness gives completeness. The seam is isometric to M and separates the two interiors. Conversely, global side labels supply a trivial normal line for a connected separating hypersurface; the ambient orientation then orients M. Each side closure is a compact oriented hyperbolic manifold with sole geodesic boundary M. The requirement is an embedding, not an immersion, and isometric refers to the specified metric.

## Tubing and the 2024 separating L-space result

BFS Lemma 3.11 supplies a disconnected geodesic separator made of copies of a dodecahedral rational homology sphere. Proposition 3.13 Step 3 connects the copies with tubes. The resulting connected separator is a connected sum with equally many copies of the two orientations. That published application establishes a smooth separating L-space; it does not claim that the connected sum is a totally geodesic hyperbolic boundary. The arXiv v2 source and live primary abstract page agree on the 2024 journal reference. [BFS](https://arxiv.org/abs/2208.01542)

Proposition 4.2 is correct. Connected sum preserves the rational homology of a sphere in this setting, but not the needed geometry. Each closed hyperbolic summand has infinite fundamental group. Puncturing does not change that group, and van Kampen gives the free product across the connected-sum sphere. Splitting at any sum sphere with at least one summand on each side leaves both sides with nontrivial fundamental groups, so neither is a ball. The sphere is essential. A closed hyperbolic 3-manifold has universal cover H^3, which is irreducible, and Hatcher's covering criterion descends irreducibility. This rules out every hyperbolic metric on the connected sum. The Gauss equation then rules out total geodesicity in a hyperbolic 4-manifold. One summand and tubing schemes creating additional S^1 x S^2 factors are not being silently included in the rational-homology assertion. [Hatcher, Proposition 1.6](https://pi.math.cornell.edu/~hatcher/3M/3M)

## Numerical conditions and their limitations

Proposition 5.1 is valid for a connected compact oriented W with exactly one rational-homology-sphere boundary, equipped with the hypothesized hyperbolic metric and geodesic boundary.

The relative fundamental-class boundary map H_4(W,M;Q) -> H_3(M;Q) is an isomorphism. The exact sequence and vanishing H_2(M;Q) then give H_3(W;Q) = H_3(W,M;Q); duality gives b_3=b_1. Vanishing H_2(M;Q) and H_1(M;Q) gives H_2(W;Q) = H_2(W,M;Q), hence a nondegenerate rational intersection pairing. Together with b_0=1 and b_4=0, this yields chi(W)=1-2b_1+b_2.

The Long-Reid signature identity uses the boundary orientation and their eta normalization: signature(W)=-eta(M). The proof specifically addresses the nonproduct metric near the boundary, with zero second fundamental form removing the boundary correction and hyperbolic conformal flatness killing the relevant Pontryagin form. No inference is made from the closed signature-zero theorem to signature(W)=0 for a filling. Integrality, absolute-value rank bounds and parity follow: b_2 >= |eta(M)| and b_2 congruent to eta(M) mod 2. The minus sign has no effect on parity. [Long-Reid, pp.173-175](https://arxiv.org/pdf/math/0007197)

Doubling gives both twice the volume and twice the Euler characteristic because chi(M)=0. Closed four-dimensional Chern-Gauss-Bonnet therefore implies Vol(W)=(4 pi^2/3)chi(W)>0. Since chi(W) is integral, b_2>=2b_1 follows. The formal data assigned for each integer e satisfy precisely these displayed necessary numerical conditions, including e=0 and the zero-dimensional nonsingular form. They are not asserted to be realized by a manifold, by a prescribed eta invariant, or by a metric. Integral eta alone is not a filling theorem, and a rational-homology-ball condition would be an unauthorized strengthening of the problem.

## Sources and evidence limits

The five PDF byte counts and hashes agree exactly with the source metadata. Fresh pdftotext extraction succeeded for each and agrees byte-for-byte with retained extracted text. K3 p.186, FKR p.1982, BFS p.21 and Long-Reid p.174 were also visually inspected. Hatcher was inspected as text. SOURCE_INSPECTION.json gives exact boundaries of source review and the live BFS publication check. The known wrong Long-Reid download is excluded by the required correct PDF hash. The live catalog's historical HTTP 403 was not retried or bypassed. Historical author retrieval records are not a claim that this auditor independently repeated every earlier search or download.

This audit did not rerun the research papers' group, manifold or L-space computations, audit their complete proofs, compute an eta invariant, or construct a hyperbolic metric. A bounded current-source search found no full resolution; this is not proof of worldwide openness or novelty. [Modern K3](https://math.berkeley.edu/sites/default/files/surv-295-ruberman-watermarked-author-pdf.pdf)

## Artifact and execution meaning

The original mathematical packet is non-executable. The added Python programs check exact bytes, inventories, status fields, patch derivation, and source pins. Normal and optimized Python runs must agree; corruption controls must reject. Such runs are software-integrity tests, not mathematical computations or machine proofs of the propositions. Mathematical acceptance rests on the analytical review above and the specifically identified literature inputs.

Only authored mathematics, the minimal authored patch, verification code, and public bibliographic/hash/size/inspection/status metadata are packaged. No source PDF, source extract/image, dataset contents, private source, private coordination material, or queue is included. No publication or external state change was performed by this audit.
