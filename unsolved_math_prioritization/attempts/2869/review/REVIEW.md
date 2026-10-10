# Independent review of KP 3.71: integral-to-mod-2 cobordism

**Verdict: PASS_UNRESOLVED_OBSTRUCTION_AND_CONTROL_PACKAGE.** The standard necessary conditions and smooth negative controls in the frozen artifact are correct. They do not determine whether the homomorphism in the original question has a nonzero kernel. The appropriate status remains **unsolved**, with two substantive approaches recorded and no new theorem or novelty claim.

Reviewed independently on 30 September 2026 using GPT-6 Astra at xhigh reasoning effort. The reviewed `OBSTRUCTION.md` has SHA-256
`d69ac3dccbe2d725d89f7e9f0cb26f44881095d6fb56b5b0f048a87ee9563fa6`.
No mandatory correction was identified. This is an AI review, not human peer review.

## Original target and coefficient conventions

I inspected the complete statement and remarks on printed pp.182–183 of the [April 2026 K3 problem list](https://bpb-us-e2.wpmucdn.com/websites.umass.edu/dist/b/22144/files/2026/04/K3-problem-list-watermarked.pdf), including the rendered pages. Problem 3.71 requires an integral homology three-sphere that bounds a smooth mod-2 homology four-ball but no smooth integral homology four-ball. Its remark expressly excludes the familiar rational-ball example Σ(2,3,7) through its Rokhlin invariant. The neighboring Problem 3.72 concerns the rational cobordism kernel and is distinct; Problem 3.73 concerns the topological category. The artifact preserves these distinctions.

For either coefficient system, being zero in the smooth homology-cobordism group is equivalent to bounding the corresponding smooth homology ball: cap the standard sphere end of a cobordism with a standard ball, or puncture a filling. Thus the artifact's boundary formulation is exact. A compact mod-2 homology ball is automatically a rational homology ball, since the universal coefficient theorem precludes any positive-dimensional free integral homology. The reverse implication fails.

## Audit of the homological and spin obstructions

Let W be a compact oriented rational homology four-ball whose boundary Y is an integral homology sphere. All positive-dimensional integral homology groups are finite. Consequently H¹(W;Z)=0. The isomorphism H⁰(W;Z)→H⁰(Y;Z), followed by the cohomology sequence of the pair, gives H¹(W,Y;Z)=0; duality gives H₃(W;Z)=0. The nonempty boundary gives H₄(W;Z)=0.

The homology sequence of the pair identifies H₂(W;Z) with H₂(W,Y;Z). Duality and the integral universal coefficient theorem then identify the latter with Ext(H₁(W;Z),Z): the Hom term from finite H₂ is zero. For a finite abelian group A, this Ext group is canonically Hom(A,Q/Z). These are integral statements, so odd torsion has not been discarded during the calculation.

For a prime ℓ, put rℓ=dim(A/ℓA). The tensor term and the preceding Tor term give the three positive Betti numbers (rℓ,2rℓ,rℓ). At ℓ=2, all three vanish exactly when A has odd order. They vanish integrally exactly when A=0. In a hypothetical witness to the original question, every mod-2 filling must therefore have nonzero odd-order A; otherwise that particular filling would already be an integral ball. This says nothing about finiteness or odd order of the fundamental group.

The spin argument is also sound. For a mod-2 ball, H²(W;F₂)=0 removes the obstruction w₂, and H¹(W;F₂)=0 makes the spin structure unique. Rational acyclicity forces signature zero. The induced unique spin structure on an integral homology sphere has normalized Rokhlin invariant μ=σ(W)/8 mod 2, hence μ=0. [Bohr–Lee, Section 2](https://arxiv.org/abs/math/0104042), uses the signature-mod-16 convention R; on integral homology spheres this is R=8μ. There is no normalization conflict.

The three-handle observation is correct for an ordinary finite handle decomposition. If there are no three-handles, H₂ is the kernel of the map out of the free two-handle group, hence free. Its finiteness then forces H₂=0 and A=0. This necessary condition is already explicitly stated in [Akbulut–Larson's introduction](https://arxiv.org/abs/1704.07739). It concerns a chosen nonintegral filling and does not prohibit a different integral filling of its boundary.

## Audit of the spun lens-space control

The construction is the ordinary spin, with the identity gluing in [Meier, Section 2.1](https://arxiv.org/abs/1708.01214). A compact punctured lens space X is smooth and oriented. Smoothing the corners of X×D² gives a compact smooth five-manifold, whose boundary is

M = (X×S¹) ∪ (S²×D²),

with overlap S²×S¹. No trisection theorem, classification theorem, or exotic-ball assertion is needed.

I recomputed the integral Mayer–Vietoris maps. The punctured lens space has H₁(X)=Z/p and no higher positive homology. For U=X×S¹ the groups in degrees 1,2,3 are Z/p⊕Z, Z/p,0. For V=S²×D² only H₂(V)=Z is positive-dimensional. The generator of H₁(S²×S¹) maps injectively to the free circle summand of H₁(U). The degree-two map sends a to (0,±a), because the boundary sphere is nullhomologous in X and is the generator in V. Both maps are injective. The degree-zero map is injective as well, so it contributes no additional free H₁.

Exactness now gives H₁(M)=H₂(M)=Z/p, H₃(M)=0 and H₄(M)=Z. In particular the upper-degree portion is consistent: the generator of H₄(M) maps isomorphically to H₃(S²×S¹), which maps to zero in U and V. Van Kampen gives the same group as the original lens space, since the extra circle generator in π₁(X)×Z is killed by the gluing. These conclusions agree with Meier's Remark 2.2.

Removing a **coordinate** four-ball gives an actual smooth manifold W with standard sphere boundary. In the pair (M,W), the fundamental class maps isomorphically onto H₄(M,W)=Z by its local orientation. The exact sequence therefore makes H₄(W)=H₃(W)=0 and preserves H₁,H₂. For odd p>1, W is a mod-2 ball with nonzero integral torsion, while its boundary also bounds the standard D⁴. Thus its boundary class is zero for an explicit geometric reason.

Boundary connected sums preserve smoothness, give the connected sum of the boundaries, and add positive-dimensional homology. Decomposing an arbitrary finite odd abelian group into cyclic factors therefore gives all the stated torsion controls with boundary S³. In particular a two-primary summand cannot be erased by this operation. The calculation validates the negative control; it does not manufacture a witness to the kernel question.

## Literature qualifications

[Akbulut–Larson, Theorem 1](https://arxiv.org/abs/1704.07739), treats the two stated Brieskorn families and computes μ=1 for odd parameters. Those subfamilies cannot bound mod-2 balls, irrespective of which rational filling is exhibited. For [Şavk, Theorem 1.1](https://arxiv.org/abs/1912.04654v3), the specified even parameters have the integer lift μ̄=1. Its reduction modulo 2 is the normalized Rokhlin invariant, so the same exclusion applies. The proof's plumbing calculation gives signature −n−5 and characteristic Wu-square −n−13 in that parity, whose difference divided by eight is 1. Neither argument settles the unexcluded parameters. Şavk's Theorem 1.2 also recalls distinct known integral-ball families; the artifact does not mistake them for witnesses.

[Lee–Şavk, arXiv:2508.15384v2](https://arxiv.org/abs/2508.15384v2), Theorem 1.2 and its Section 3 formulation, concerns Seifert spheres with positive Fintushel–Stern R-invariant and the specified restrictions on their exponent products and associated local-equivalence representatives. Its stated rational-cobordism independence makes the selected differences unsuitable for the mod-2 kernel, even though their local-equivalence data vanish. The artifact correctly restricts the attribution to the theorem's hypotheses and designated families. This audit checks that source implication; it does not independently certify the entire recent instanton-theoretic proof.

All six primary PDF files matched the author's recorded hashes and byte lengths. The arXiv version records were checked independently. The current targeted searches supplied no verified resolution of the exact mod-2 kernel question. That limited search is not an exhaustive certificate of present-day openness.

## Reproduction and disposition

The author's frozen checker reproduced its receipt **byte for byte: 312 exact assertions on 24 group models**. It tests algebraic chain complexes and elementary Mayer–Vietoris coordinates; it is correctly described as an algebraic diagnostic. It does not encode a smooth handle realization or a nonzero boundary class.

The independent standard-library checker imports no author code. It directly enumerates 455 finite abelian group presentations, their multiplication kernels and quotients, and the standard Q/Z character pairing. It also constructs the cellular mapping-cone matrices for the displayed Mayer–Vietoris maps, checks that the integer differential squares to zero, and enumerates finite-field images for 200 cases (p=1,…,25, both gluing signs, and coefficients F₂,F₃,F₅,F₇). Boundary-sum controls check the persistence of two-primary homology. **All 118,054 assertions pass.** These controls support the exact algebra; the written geometric construction establishes smooth realizability and the standard boundary.

Run `python3 independent_checks.py` from this review directory and compare its output with `independent_results.json`. The author replay can be reproduced separately by running `python3 author_replay/verify_torsion.py`; its frozen artifact is included because the checker records that artifact's hash.

The exact remaining gap is unchanged: produce a smooth mod-2 filling of an integral homology sphere and an obstruction to **every** smooth integral filling of the same sphere, or prove that no such boundary exists. Neither approach in this package supplies that combination or establishes injectivity. It is suitable for publication as a carefully delimited unsuccessful attempt, with the original problem marked **unsolved**. No source edit is required for this verdict, and no third-party PDF or rendered page should be included in the review bundle.
