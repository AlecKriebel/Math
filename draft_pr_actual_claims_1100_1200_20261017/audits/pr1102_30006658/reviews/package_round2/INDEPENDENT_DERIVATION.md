# Fresh independent derivation — package round 2

Recorded 2026-10-17 16:47 UTC, before reading any package_round1 reasoning. Review scope: only PR1102 / problem30006658 and its final publication package. No changes to final artifacts, branch, remote, or external systems. Initial progress estimate: 30% of this bounded full-package review.

## Exact claim reconstructed

For a compact Lie group G, a prime p, and any field k of characteristic p, put X=(BG)^∧_p and A=C_*(ΩX;k). If π₀G has no normal p-complement, the canonical map Γ_k A→A is zero on every homology group. This does not claim that the map is a zero morphism in D(A). Completion must precede looping. The mathematical task is to establish both proxy-smallness and infinite total dimension for the specified algebra, then use a completely algebraic criterion.

## Algebra, reconstructed independently

For an ordinary Hopf algebra B, let I≠0 be a finite-dimensional right ideal. The coefficient envelope J=span{(1⊗f)Δ(i)} is finite-dimensional, contains I by the right counit, and satisfies ΔJ⊂J⊗B by coassociativity. The coefficient formula in the paper is correct: expanding its right side gives Σ i₁ b₁ f(i₂ b₂ S(b₃)), which contracts to Σ i₁ b f(i₂). Thus J is a right ideal without requiring S to be invertible.

The shortened finish is valid. If ε vanishes identically on J, applying (ε⊗1) to ΔJ annihilates every element of J, contradicting I≠0. Scale j∈J to ε(j)=1. Since every first factor of Δj lies in J, Σj₁S(j₂)=1 lies in the right ideal J. Therefore J=B and dim B<∞. For left ideals, B^{op,cop} is an ordinary Hopf algebra with the SAME antipode: its two antipode equations are precisely the original two equations in reversed order. There is no hidden use of an inverse antipode.

For graded H, characteristic 2 erases all Koszul signs, including for negative degrees. Otherwise parity bosonization on H⊗kC₂ uses (h#gⁱ)(a#gʲ)=(-1)^{i|a|}ha#g^{i+j}; Δ(h#gⁱ)=Σ(h₁#g^{|h₂|+i})⊗(h₂#gⁱ); and S(h#gⁱ)=(1#g^{i+|h|})(S_H(h)#1). The cross sign in multiplicativity is |h₂||a₁|+i|a|, equal to the combined signs of the two tensor-factor products. For an odd primitive x, Δ_Bx=x⊗1+g⊗x and S_Bx=xg=-gx, which checks the potentially dangerous antipode convention. A graded right or left ideal I gives the same-sided ideal I⊗kC₂; multiplying basis tensors never changes ideal membership. No finite-dimensionality of homogeneous pieces is needed.

## Classwise compact approximation

Given a proxy K, K is compact and Loc(K)=Loc(k). Compact Morita theory realizes any M in this localizing category as N⊗_E^L K, E=REnd_A(K), for a right E-module N. A semi-free resolution of N can be well-ordered so each generator's differential is a finite combination of earlier generators. Starting from finitely many generators and closing under these dependencies yields a finite set: otherwise its finitely branching dependency tree has an infinite branch, contradicting well-founded descent in the ordering. The finite dependency-closed free stages form a filtered union, which computes the filtered homotopy colimit. Tensoring carries the stages into thick_A(K). Because filtered colimits of vector spaces are exact, each homology class of M comes from a stage P. Since K∈thick_A(k), each P has finite-dimensional TOTAL k-homology, including under cones and retracts.

An A-linear map P→A induces an H_*(A)-linear map on homology, so its image is a graded left ideal and is finite-dimensional. The Hopf result kills it. Every cellular class factors in this way, so EVERY map M→A with cellular source vanishes on homology. This does not assert bounded homology for M or compactness of k and does not need a single finite stage for all classes.

## Topological reduction and falsifiable input checks still due

A loop-group model supplies multiplication, diagonal, inverse, and hence a Hopf algebra on homology; ΩX need not be connected, and field Künneth has no finite-type requirement. Scalar extension F_p→k commutes with chains and derived tensor, preserving compact construction and localizing construction. Extending a proxy from F_p therefore suffices for arbitrary characteristic-p fields. Infinite F_p-dimension remains infinite after extending scalars, as is seen by extending a basis. No infinite cochain-dual exchange is used.

The two critical external claims to inspect directly are DGI §5.7 (proxy-smallness over completed loop chains for EVERY compact Lie G, with its completion hypotheses) and Ishiguro Proposition 1.3(a) (finite total loop homology implies p-nilpotent component group). Their exact texts, the literal OWR Q2.2, current cited literature, package hashes, PDF consistency, and effective negative controls remain to be checked. No algebraic counterexample or circular step has been found in this first reconstruction.

## Final independent sign/source checkpoint

2026-10-17 16:54 UTC; 100% of assigned bounded review complete. All topological/source obligations above were discharged directly. Fresh primary downloads matched the cached OWR, DGI, Ishiguro and Lomp PDFs; BIS's published Lemma 4.1 proof supports the approximation; current Greenlees v3 and actual published Lemma 6.5/Remark 6.6 retain the restricted scopes credited in the note. No package_round1 reasoning was read.

For the bosonization antipodes, write |h|=d, |h_1|=a, |h_2|=b modulo two. In m_B(S_B tensor 1)Delta_B(h#g^i), multiplication contributes combined sign (-1)^((d+i)(a+b))=(-1)^((d+i)d), independent of the term. The remaining sum is epsilon_H(h)1#g^d. A nonzero counit forces d=0, giving epsilon_H(h)1#1. In m_B(1 tensor S_B)Delta_B(h#g^i), the two signs (-1)^((i+b)b) cancel and the group powers cancel. The result is sum h_1 S_H(h_2)#1=epsilon_H(h)1#1. No inverse antipode occurs. Coassociativity has common threefold expression (h_1#g^{b+c+i}) tensor (h_2#g^{c+i}) tensor (h_3#g^i). Counits follow because a factor with nonzero counit has parity zero.

The actual archived verifier passed and refused optimized Python. Five review-only formula mutations failed assertions. The rebuilt source and distributed PDF had identical extracted text and identical page PNG bytes for all four pages, and all pages were visually inspected. Hash receipts and test results are retained; redundant reading copies were removed to recover disk space. REVIEW.md and VERDICT.json record the final PASS, exact hashes, completed checks, and limits. No actionable issue or remaining mathematical proof gap was identified, and all frozen publication artifact hashes remained unchanged.
