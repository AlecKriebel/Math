# Independent full five-turn review: 30005016

2026-10-02. **PASS_SCOPED_PARTIAL_RESULTS; ORIGINAL_UNRESOLVED_5_OF_5.** No mandatory mathematical correction was found. The exact unrestricted minimum has not been determined. Preserve the field-specific conclusions and do not promote the restricted four-/six-space results into an unrestricted lower bound of five.

This verdict binds author commit `3e86c9c69a92b2df5bfd3ff276399e5272e6ca92` and FINAL_FROZEN_MANIFEST.json SHA256 `1f89b422356091ee6b1516cdbe0ffa33fbec3427c585557159ffe7cf82c86c4d`. All 28 manifest-bound files and the manifest itself match exact remote readback. All five historical manifests match. No author file was edited. This is independent AI-assisted mathematical review, not human peer review, formal verification, or a historical-priority certificate.

## 1. Source and quantifiers

The interpolation paragraph on printed p. 423 of [OWR 7/2022](https://ems.press/content/serial-article-files/46948) was visually inspected in full. It fixes a characteristic-zero field, asks about fixed four-dimensional polynomial subspaces, and requires interpolation on every four-point subset. It imposes no degree, monomial, generic-position or directional restriction. The neighboring spline problem is separately headed and does not belong to this target.

The packet correctly distinguishes m_4(K), a field-specific minimum, from the least bound valid across all characteristic-zero fields with families allowed to depend on the field. A construction for one field is not a full answer for another field or a determination of the worst-case minimum. The source's three-point preamble needs qualification, but that does not make the four-point optimization meaningless or solve it.

## 2. Turn 1: field example, real obstruction and five-space cover

The elementary injection lemma is correct. A nonconstant polynomial h has linearly independent powers by distinct total degrees, and injectivity on K² makes their evaluation matrix a nonzero Vandermonde matrix on every n distinct points. The argument genuinely concerns bivariate data.

I inspected Cornelissen's [Proposition 8](https://webspace.science.uu.nl/~corne102/docs/abc.pdf), printed pp. 6–7, including its continuation and proof. For K=Q(t), the projective line is smooth, proper and irreducible, with genus zero; the extension over Q(t) is the identity and hence separable. The only nonzero valuations of t are at zero and infinity, so N_t=2. The threshold is 64(2+5)=448, and m=449 is an allowed odd exponent. Constants algebraic over Q in Q(t) lie in Q, so there is no nontrivial 449th root of unity; valuation one at t=0 excludes t from the 449th powers. These are all the required hypotheses. The credited conclusion h=x^449+t y^449 is injective and therefore m_4(Q(t))=1. The same lemma explains the three-point preamble issue.

The real determinant-sign obstruction is sound. The two moving points exchange along opposite semicircles without colliding with one another or the two fixed points. A determinant assumed everywhere nonzero would change sign along a continuous real path. This proves only m_4(R)≥2; it is not a complex-valued intermediate-value argument.

The five-space upper bound is valid over every characteristic-zero field. Collinear configurations are separated by a nonconstant coordinate and Vandermonde. For a noncollinear configuration, each point has a quadratic cardinal polynomial formed from two lines, so degree-at-most-two evaluation has rank four. Since affine evaluation has rank three, at least one of x², xy, y² raises it to four. The five exclusive witnesses only establish indispensability inside that particular family.

The number-field implication remains conditional. [Poonen's Theorem 1.1 and Remark 1.2](https://math.mit.edu/~poonen/papers/QQ.pdf) explicitly obtain polynomial injections under the relevant Bombieri–Lang hypothesis. They do not give an unconditional result over Q.

## 3. Turn 2: unrestricted algebraically closed lower bound

The determinant ideal argument is correct for algebraically closed K. Each determinant vanishes on every collision diagonal. A covering family makes their common zero set exactly the collision locus. Nullstellensatz gives radical equality with the intersection of the six diagonal ideals. Radical invariance and the length-s bound of the Čech complex then imply that s covering spaces force local cohomology to vanish above degree s. This reasoning allows arbitrary degrees and arbitrary bases.

The arrangement input was checked in the [primary 2003 paper](https://web.mat.upc.edu/josep.alvarez/pdf/aim03.pdf), Theorem 1.2 and Corollary 1.3, with the displayed filtration on manuscript p. 10 also visually inspected. Its poset is ordered by inclusion of intersection subspaces; the homology index is exactly h(p)−r−1. The filtration need not split, and the packet uses only a nonzero associated-graded contribution.

For the full diagonal, h=6. Independently generating intersections from all nonempty subsets of the six collision components gives 14 nonambient intersections. Removing the full diagonal leaves 13 interval vertices and 18 comparabilities. The interval is a connected graph, with boundary rank 12 and first homology dimension six. The ambient partition is correctly excluded; there are no two-simplices. Therefore r=4 gives h−r−1=1, not an off-by-one neighboring group.

The six coordinate differences generate the full-diagonal ideal after an invertible linear change of variables. Their inverse product represents a nonzero top Čech class: no localization omitting one of the six variables contains its Laurent monomial with all six exponents negative. Thus H^6 of that support is nonzero; tensoring with the six-dimensional interval homology gives a nonzero graded contribution to H_I^4. Hence s≥4.

The resulting range 4≤m_4(K)≤5 is accepted for algebraically closed characteristic-zero fields, and yields the same worst-case range. It does not transfer to R or Q: covering rational points need not determine the algebraic zero locus over an algebraic closure. This limitation is explicit and essential.

## 4. Turn 3: the quadratic mixed-family obstruction

The three realization branches correctly cover every nonzero projective quadratic-determinant direction. I independently derived both symbolic determinant vectors. In the V≠0 branch, the finite forbidden-value set leaves a nonzero choice in any infinite field, and all four points are distinct. In the V=0, UW≠0 branch, choosing r²≠U and t²≠−W makes the displayed multiplier nonzero. The one-coordinate cases are valid rational configurations.

The common kernel of two quadratic coefficient vectors always contains a nonzero vector, including dependent or zero coefficient vectors. Affine terms contribute nothing to the fourth-column determinant. Repeated coordinates defeat the retained directional cubics, so every proposed family of this particular mixed form fails. Invertible affine-coordinate changes preserve the argument; dependent coordinate directions can be defeated on a common fiber. This proves the claimed class obstruction, not a theorem about arbitrary four subspaces.

## 5. Turn 4: directional minimum six and complete certificate

The Vandermonde/kernel-direction reformulation is exact. The construction realizing five arbitrary distinct directions uses intersections of nonparallel lines. Its four points are distinct for the stated reasons, including when one direction is vertical. I independently tested all 720 five-direction assignments from six projective directions including a vertical one.

For the upper bound, simultaneous failure of the six listed directions would assign those six distinct finite slopes bijectively to the six pairs of four points. I independently constructed the full six-equation, eight-coordinate incidence matrix for every one of the 720 assignments. Deleting the two translation columns gives a nonzero determinant in every row, with constant sign opposite to the packet's reduced determinant. Its absolute values and all 48-fold frequencies agree with the complete CSV. Thus only coincident point configurations solve those slope equations. Every integer certificate remains nonzero in characteristic zero.

The restricted minimum is exactly six. Since arbitrary spaces already admit a five-member cover, this conclusion cannot be an unrestricted answer or unrestricted lower bound.

## 6. Turn 5: arbitrary high-degree completions in the stated mixed family

The common-kernel mechanism is correct: p=x²−By−T² belongs to both V_1 and V_3, and q=y²−Dx−T² belongs to both V_2 and V_4. They are nonzero, regardless of the high-degree fourth generators. Four distinct common zeros therefore defeat all four spaces; a lower-dimensional member cannot help.

Over R, each signed square is mapped into itself because the radicands lie between 11L² and 21L², strictly inside the squared-radius bounds 9L² and 25L². The sup-norm Lipschitz constant is below 1/6. Completeness and contraction give one solution in each of four disjoint squares. This supplies real solutions rather than merely complex Bézout intersections.

Over an algebraically closed field, the B=0 branch correctly excludes T=0,±D. For B≠0, elimination is reversible and the quartic is monic. I independently recomputed its discriminant from a symbolic 7×7 Sylvester determinant. It agrees with the stated expression and has leading coefficient 256B⁴ in T, so only finitely many T are excluded. Four simple roots yield four distinct point solutions. Nothing proves four rational solutions, and the packet appropriately makes no such claim.

## 7. Reproduction, limits and disposition

All five author outputs replay byte-for-byte, including the entire 720-row CSV; the author count totals 20,944 exact assertions. The separate reviewer checker imports no author code and passes 5,796 exact algebra/combinatorial assertions. These checks supplement the analytical and source review; they do not certify the cited deep theorems by computation.

The final accepted claims are: the credited exact Q(t) value one; the conditional number-field implication; the uniform upper bound five; the algebraically closed and worst-case interval [4,5]; the real interval [2,5]; and the expressly restricted construction obstructions. No unrestricted four-space construction or lower bound excluding every four-space family has been supplied. The original outcome remains **unsolved after 5/5**.

The limited literature comparison, including incomplete access to later Shekhtman material, does not establish worldwide priority or current open status. This review accepts the packet's mathematical partial results and its honest nonresolution. No additional author search is needed to correct this packet; no mathematical revision is required.
