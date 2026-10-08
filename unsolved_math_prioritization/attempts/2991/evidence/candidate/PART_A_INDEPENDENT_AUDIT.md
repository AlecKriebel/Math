# Independent mathematical audit of the proposed answer to KP 4.115(a)

Date: 2026-10-08.

## Verdict and exact scope

**Pass for part (a), with no mathematical correction required.** The audited argument constructs two orientation-preservingly diffeomorphic, non-ambiently-isotopic balanced (3,1)-trisections of the same closed connected oriented smooth four-manifold. The non-isotopy proof also excludes arbitrary permutations of the three sectors. Both trisections have minimal genus.

This verdict applies to the frozen 9,755-byte `PART_A_PROOF.md`, SHA-256

`90be5ae3ab394227e9b22db5db3c49e1798714f70a7c554eed4fadb539ee820b`.

The ambient manifold is the untwisted spin of the explicitly defined quotient L(8,3), and its fundamental group is C8. Consequently this construction does **not** answer part (b). This is a mathematical audit of the supplied argument, not a claim of publication, community acceptance, or novelty. The proof was not modified during this audit.

## 1. Original target and equivalence relation

The actual 2026 K3 source places Problem 4.115 on printed page 286 (PDF page index 285). Its first question asks for a diffeomorphic but non-isotopic pair on one four-manifold. Only its second question adds simple connectivity. The section introduction on printed page 282 defines trisections without imposing simple connectivity. There is no surrounding restriction that would exclude the present example.

Remark (1) of Problem 4.115 discusses orientation-preserving self-diffeomorphisms with nontrivial homology action and warns that such a map may nevertheless be represented by a trisection stabilizer. The candidate addresses that warning rather than assuming it away: it proves that the specific multiplication-by-3 action cannot preserve this trisection, even after a sector permutation.

The fixed-manifold definition in Islambouli, arXiv:1804.06978v2, Section 4.2, page 6, agrees with the candidate: isotopy starts at the ambient identity and ends by carrying each sector to its corresponding sector. The candidate proves a stronger assertion by allowing any correspondence between the three sectors. No equivalence modulo an arbitrary ambient automorphism is being substituted for ambient isotopy.

Sources:

- [K3, 2026 author's preliminary version, Problem 4.115 and Section 4.10](https://bpb-us-e2.wpmucdn.com/websites.umass.edu/dist/b/22144/files/2026/04/K3-problem-list-watermarked.pdf).
- [Islambouli, arXiv:1804.06978v2](https://arxiv.org/pdf/1804.06978v2), Section 4.2 and Proposition 4.5, page 6.

## 2. Lens-space quotient and ambient automorphism

Write zeta = exp(2 pi i/8) and d(z1,z2) = (zeta z1,zeta^3 z2). Every nonidentity power of d is fixed-point-free on S3: either nonzero coordinate forces the relevant exponent to vanish modulo 8, and both 1 and 3 are invertible modulo 8. Thus the quotient is a smooth oriented closed three-manifold with fundamental group C8. The explicit quotient convention eliminates possible ambiguities in the notation L(8,3).

The coordinate swap s(z1,z2) = (z2,z1) has real determinant +1. Its restriction to S3 preserves orientation because the outward normal is also carried to the outward normal. Direct computation gives s d = d^3 s, using 9 = 1 modulo 8. Therefore s descends to an orientation-preserving quotient isometry whose action on the deck group, and hence on H1, is multiplication by 3. A basepoint change only introduces conjugation; C8 is abelian, so it does not alter this action.

The fixed point used in the proof is genuine: the chosen lift (1/sqrt(2),1/sqrt(2)) is fixed by s. On its tangent space to S3, the symmetric imaginary direction is fixed, while the real and imaginary antisymmetric directions are both negated. The derivative on the quotient tangent space is consequently a rotation through pi about a line.

The ball-fixing adjustment is valid in the smooth category. In an injective normal-coordinate ball about the fixed point, an isometry is exactly its derivative in exponential coordinates. The map rotating a vector through an angle depending only on its radius is invertible because radius is preserved; the inverse rotates through the opposite angle. The cutoff is constant near zero, so using the norm introduces no nonsmoothness at zero. It is zero near the edge of the chart, so extension by the identity is smooth. Scaling the angle gives a smooth isotopy to the identity. Composing this adjustment with the swap cancels the pi rotation on a whole smaller neighborhood, not merely on the boundary of a ball.

Thus the resulting f preserves orientation, acts by multiplication by 3 on H1, and equals the identity near a closed embedded three-ball B. No assertion about the mapping class group of a lens space is required.

## 3. Spin, gluing, and naturality

The displayed spin

    X = ((M minus int(B)) x S1) union_id (S2 x D2)

is Meier's untwisted spin. With the induced boundary orientations, the standard product gluing produces an oriented closed smooth manifold. Since f is the identity on an open neighborhood of B, its product with the identity on S1 agrees with the identity map of the cap on a collar. Hence the two maps glue smoothly, including after rounding corners. Their inverses glue in the same way. The resulting F is an orientation-preserving self-diffeomorphism.

The fundamental-group computation has no extra surviving generator. The punctured three-manifold has fundamental group C8; its product with S1 has group C8 x Z. The cap S2 x D2 is simply connected, and the common boundary has group Z mapping exactly to that product's S1 factor. Van Kampen therefore kills precisely that factor and gives pi1(X) = C8. Inclusion of a fixed slice of the punctured M realizes the identification. Because F restricts to f on that slice, F induces multiplication by 3 on H1(X;Z).

The chosen ball lies near the original genus-one Heegaard surface, but this causes no theorem-hypothesis problem. The spin is independent of the location of a small coordinate ball up to diffeomorphism, by moving such a ball through coordinate neighborhoods. Equivalently one may move the Heegaard splitting so that the chosen ball lies in the interior of one handlebody. No claim that this move commutes with f is used. The proof first chooses a trisection on the actual X and subsequently takes its image under the already constructed F.

## 4. Existence theorem and its hypotheses

The two invariant solid tori in S3 descend to a genus-one Heegaard splitting of M. The candidate's mapping-torus argument is correct. An additional direct check is available: on the solid torus with coordinates w = z1/z2 and u = z2/|z2|, the quotient coordinates (w u^6,u^8) identify its quotient with D2 x S1. These are invariant under d, and two points have the same coordinates exactly when they differ by a deck transformation. On the other torus, using w = z2/z1 and u = z1/|z1|, use (w u^(-2),u^8). The common boundary is a torus. This check is optional and does not correct an error in the submitted proof.

Meier's Theorem 1.2 applies to every closed connected orientable three-manifold admitting a genus-k Heegaard splitting. It gives a balanced (3k,k)-trisection of its spin and twisted spin. Taking k=1 gives sectors diffeomorphic to S1 x B3. No irreducibility, simple connectivity, restriction k>=2, extra diagram condition, or naturality under f is a hypothesis of this theorem. The additional diagram condition in Meier's Theorem 1.4 is irrelevant here.

This was checked in both the preprint and published versions:

- [Meier, arXiv:1708.01214v1](https://arxiv.org/pdf/1708.01214v1): Theorem 1.2 on page 1; its proof on pages 5-6; spin definition in Section 2.1, pages 2-3; balanced-trisection convention in Section 2.2, page 4.
- [Meier, published PDF](https://archive.intlpress.com/site/pub/files/_fulltext/journals/mrl/2018/0025/0005/MRL-2018-0025-0005-a007.pdf): Theorem 1.2 on printed page 1498; spin definition on page 1499; trisection definition on page 1502. Publication: Mathematical Research Letters 25 (2018), 1497-1524, [DOI](https://doi.org/10.4310/MRL.2018.v25.n5.a7).

Defining the second trisection to be F(T) makes its diffeomorphism to T immediate. It does not assert that spinning a Heegaard splitting commutes with a chosen diffeomorphism.

## 5. Surjectivity of each sector inclusion

The sector-surjectivity argument works, including for an unbalanced trisection. Fix different indices i,j,k. The pairwise intersection Hij is a handlebody in a Heegaard splitting of the closed three-manifold boundary of Xj. Relative to Hij, that three-manifold is built using handles of indices 2 and 3, so pi1(Hij) surjects onto pi1(boundary Xj). The latter group's inclusion into the four-dimensional one-handlebody Xj is an isomorphism: standard boundary generators map to its one-handle cores, giving the usual free-group bases.

Apply van Kampen to Xi union Xj. Its intersection is connected, and every generator coming from Xj is already represented in the intersection. Consequently Xi surjects onto the group of that union. Its intersection with the remaining Xk is Hik union Hjk, namely the full boundary of Xk. This intersection is connected and surjects onto pi1(Xk), so adjoining Xk adds no generators. Collar thickenings give the requisite open-cover formulation of van Kampen. Thus pi1(Xi) surjects onto pi1(X) for each i, and abelianization gives the asserted H1 surjection.

This direct reasoning also matches Islambouli's discussion immediately before Proposition 4.5, which derives sector surjectivity from a handle decomposition with the selected sector as its zero- and one-handles. It avoids relying on any possible nonabelian basepoint choices in the Nielsen invariant.

## 6. Intrinsic invariant and the marking issue

For a rank-one sector Y, let

    C(Y) = { i_*(u), -i_*(u) } subset H1(X;Z),

where u is either generator of H1(Y;Z), and i is inclusion. This is intrinsically defined in the homology of the fixed ambient manifold. A choice of identification H1(X;Z) with Z/8 is only a convenient notation for comparing these subsets.

Suppose an ambient isotopy h_t starts at the identity and ends by taking Y onto another rank-one sector Z. Homotopy invariance gives h1_* = identity on H1(X;Z). The restriction h1:Y -> Z sends an integral generator to plus or minus an integral generator. Naturality of inclusion therefore gives C(Y) = C(Z). There is no freedom to apply an arbitrary automorphism of ambient homology at this stage. That freedom belongs to diffeomorphism classification, not isotopy in a fixed manifold.

For F, the corresponding naturality equation instead gives C(F(Y)) = F_*(C(Y)), which is multiplication by 3 here. Surjectivity implies that i_*(u) has order 8 and is a unit. It cannot be an element of order 2 or 4. The two possible classes are A={1,7} and B={3,5}, and multiplication by 3 exchanges them.

A different initial identification of the ambient cyclic group merely relabels A and B. Both trisections are relabeled simultaneously; whether their multisets agree is unchanged. Thus this is a distinction between actual embedded sectors, not an artificially supplied marking on otherwise equivalent objects.

For labeled sectors, even one equality C(Xi)=C(F(Xi)) would imply 3r=plus or minus r modulo 8 for a unit r. Multiplying by the inverse of r gives 3=1 or 3=7 modulo 8, both false.

For an arbitrary permutation of sectors, compare multisets. If a sectors of T have class A, then exactly 3-a sectors of F(T) have class A. Equality of the multisets requires a=3-a, impossible for an integer a. This checks all four possible count patterns, not only the case where all spun-sector generators happen to agree. The proof therefore requires no computation of the specific generators in Meier's construction.

## 7. Minimality and stabilization scope

The product-and-cap decomposition gives Euler characteristic 2: the S1 product and common boundary have Euler characteristic zero, while S2 x D2 has Euler characteristic 2. For a (g;k1,k2,k3)-trisection, inclusion-exclusion gives

    chi(X) = 2 + g - k1 - k2 - k3.

Each sector surjects onto nontrivial pi1(X), so every ki is at least 1. It follows that g=k1+k2+k3 is at least 3, even among unbalanced trisections. The displayed genus-three examples are minimal.

The proof's stabilization disclaimer is correct. [Gay and Kirby, arXiv:1205.1565v3](https://arxiv.org/pdf/1205.1565v3), Theorem 11, gives equivalence by an ambient diffeomorphism isotopic to the identity after sufficiently many stabilizations. The rank-one generator argument does not establish persistent distinction after increasing sector rank. The construction explicitly gives diffeomorphic trisections, so it cannot serve as a non-diffeomorphism result.

## 8. Attribution, novelty, and what was not established

The homology argument is a rank-one specialization of the established Nielsen-class method; it should retain the credit already present in the proof. In Islambouli arXiv:1804.06978v2, Proposition 4.5 supplies invariance, Theorem 6.3 relates it to spinning, and Section 7 develops examples with sector rank at least two. No explicit L(8,3) example or this diffeomorphic/non-isotopic pair was found in that inspected version. The publisher's abstract for the [2021 article](https://doi.org/10.1007/s10711-021-00617-y) confirms its Nielsen-class framework, but the publisher's complete subscription text was not available in this audit; its theorem numbering is not asserted here.

Meier's published Section 4.1 discusses spun lens-space trisections. Its Question 4.3, page 1515, asks about diffeomorphism of trisections obtained from different q values. That is a separate question from the present construction using a self-diffeomorphism on one fixed spin. The candidate does not answer that question, and no answer to it is needed.

Targeted searches for L(8,3) trisections, spun-lens non-isotopy, and diffeomorphic/non-isotopic trisections found no primary source explicitly making this same construction. This limited negative search does not establish novelty or exclude prior unpublished knowledge.

The audited mathematical conclusion is therefore narrow and explicit: the argument supplies a valid existence construction for the literal part (a) of the inspected 2026 Problem 4.115. Part (b), novelty, and external acceptance remain outside this audit's affirmative verdict.

## 9. Reproducibility pins

The following are hashes and byte counts of public-source PDFs inspected in this audit. They identify source versions without reproducing source documents.

| Source | Bytes | SHA-256 |
|---|---:|---|
| K3 author's preliminary version, 2026, PDF linked in Section 1 | 6,578,041 | `ae56518166fe38aaaf555c58614329228afe734e743b111badec4060877fa12f` |
| Meier arXiv:1708.01214v1 | 547,617 | `2f84c6c960045ab07a490065469c30f59a98e080828a160372c33aacb9ac44c6` |
| Islambouli arXiv:1804.06978v2 | 426,277 | `63e365eda2060fdf795564c091cd87de000da91ed72c9d9584872e4282ce923d` |
| Gay-Kirby arXiv:1205.1565v3 | 406,364 | `2b394cd9034874aadecbea8e58c3bd289ecac976e9a0f2b51bc6f6613eca1871` |

The K3 question page, Meier's theorem page, and Islambouli's definition/invariance page were also rendered from the pinned PDFs and visually inspected. Published Meier theorem and definition pins were independently checked through the publisher PDF. No source PDF, page image, or copied third-party source text is part of this report.
