# Independent audit of the Mori dream global cone investigation

## Decision

Accept the corrected derivative as a bounded mathematical audit, with five substantive approaches and no accepted full resolution. The elementary examples and conditional criteria survive independent review. The associated-graded criterion needs an explicit full numerical-lattice hypothesis, supplied in the correction patch. Source-context wording also needs correction: the first-boundary interpretation of the flag indexing is supported by the manuscript's own example, and a later paper repeats the affirmative flag-on-X result.

Do not classify this as a new solution, a counterexample to the universal existence question, a proof that the earlier theorem is false, or a finding that the problem is currently regarded as open. An affirmative result is explicitly announced in the original report and manuscript. The audit has not independently certified its exact admissible-flag-on-X proof. The disposition is therefore **accepted corrected bounded partial, with prior affirmative literature and source-proof applicability left uncertified**.

Problem identification: 30003596, OWR-15586-007, catalog rank 869. The target quantifier is every smooth complex projective Mori dream space, with a complete admissible flag on that original variety. Its global Newton–Okounkov object is a closed cone in the product of valuation space and numerical divisor space. Rational polyhedrality of that cone is weaker than finite generation of a valuation semigroup.

## Scope and evidence integrity

The author archive was pinned before its contents were used: 12,371 bytes, SHA-256 07a3c99951cb4266f10954c3fa229b926a4349671aa6e5ae62402b3e5a36c12d. Its external manifest has SHA-256 9e3521a582e2f060c05de9a1091289d29c9841f66a1c3525e7daa9dc432fc23c. All five member names, sizes and hashes match that manifest. Every member is a regular, non-executable Markdown or JSON file; there are no symlinks, path escapes, executables, hidden extra members or source PDFs in the archive. The corresponding authored working files match the frozen bytes. No original file was changed.

The full supplied catalog, problem corpus and research corpus were parsed, rather than treating a short excerpt as the record. The target statement hash is 97fab04f8577de56aab711652d4e7546197745c688b9c68112cfffb235bf2629. The research corpus has no entry under OWR-15586-007; the standard default is an empty object, not null. Serializing the complete pair [problem_record, {}] with default Python JSON separators and sort_keys=True produces SHA-256 ccfad7181bf2f5237a1d2195645a05eee521ee1a88024822f2de108ad7b5c55b, exactly the catalog review hash. This matches the requested full-record-pair convention. It is an integrity check, not evidence that the catalog's mathematical status is accurate.

The five supplied mathematical PDFs were available in full and their byte counts and hashes were independently rechecked. The central Postinghel–Urbinati and Oberwolfach PDFs were also independently retrieved again from the public source and matched their pins byte-for-byte. A full later-reference PDF, arXiv:1901.00384v2, was newly retrieved. Public metadata and critical PDF page images were inspected. No copied source PDF, extract, image, corpus record, private coordination material or private checker fingerprint is included in this deliverable. The package records only authored mathematical discussion, public bibliographic metadata and allowed integrity metadata.

## What the original sources actually claim

The Oberwolfach contribution presents the Mori dream question and then an affirmative result in the same contribution. On printed pages 2653–2654, its Theorems 5–6 assert flags on X and the rational-polyhedral conclusion. It is misleading to cite only the question while retaining an unqualified open classification. The corresponding manuscript is Postinghel–Urbinati, arXiv:1612.03861v4, dated 25 January 2018. Its introductory Theorems 1.2–1.3 and Corollary 4.7 also explicitly purport to answer the question. The catalog's arXiv:1306.2028 link is an astronomy paper, Gemini Spectroscopy of the Short GRB 130603B Afterglow and Host, and is not evidence for this mathematics.

There is a genuine distinction between the scope of those announced conclusions and the location of the detailed construction. Lemma 4.2, as printed on manuscript page 7, defines a flag on X-bar. Remark 4.4 again says it is supported there and treats it as an infinitesimal flag for X. These bars were checked in the page image, not inferred from text extraction. The common function field and pullback of line bundles allow bodies of divisors on X to be defined using such a valuation. That does not make its flag members subvarieties of X with the required codimensions. The paper's assertion that properties are preserved cannot, on its own, supply this geometric realization.

The full context also rules out an overly hostile reading of the index error. For an ambient m-fold and an n-fold subvariety, the codimension of the ambient member indexed m−n+i is m−n+i. Proper intersection would have dimension 2n−m−i, rather than n−i. This contradicts the stated dimensions when m>n. But the same lemma's prose describes the first n ambient members, and Section 5.1.1 on page 12 actually induces its surface flag using the first divisor and then a codimension-two boundary intersection. Thus the intended repair is source-supported. The mismatch is a printed typographical/expository defect, not a sufficient argument that the intended theorem is false. Nested components, nonempty intersections and smoothness at the endpoint still have to hold after making that repair.

A further safeguard is the later paper by Küronya, Maclean and Roé, arXiv:1901.00384v2. Its introduction, page 2, expressly attributes a flag-on-X global-polyhedrality result for Mori dream spaces to Postinghel–Urbinati. Its cited reference is the correct manuscript. This later attribution is evidence of reception of the affirmative claim. It does not supply a new proof of the construction or resolve the particular descent and restriction checks in this audit. Only the inspected arXiv version is used for this statement; no assertion is made that the same sentence appears in a journal version.

The current arXiv landing page lists v4 of Postinghel–Urbinati and no journal reference or withdrawal notice. Bounded searches did not verify a correction, retraction, independently repaired general proof or journal version. These negative search results must not be turned into claims of nonexistence, community consensus or theorem falsity.

## Projection and restricted volume

Theorem 4.5 aims to identify the body on the induced flag with a coordinate projection of an ambient toric body. Its argument first asserts the inclusion coming from torus-invariant sections, then invokes restricted-volume equality for ample divisors and approximation through small modifications to obtain equality. The two volume statements that matter are different:

1. The intrinsic Newton–Okounkov body of the restricted linear series has normalized Euclidean volume equal to its restricted volume.
2. The coordinate projection of the ambient body has that same normalized Euclidean volume.

Surjectivity of restriction or equality between restricted and intrinsic divisor volumes can establish the first comparison. It does not establish the second. Additional information relating the ambient valuation, restriction and cancellation is needed. Passing to limits of ample divisors cannot replace a missing comparison at the ample stage.

The author's Proposition 3.1 correctly demonstrates that logical distinction. In P² with homogeneous coordinates x,y,z, use the ambient flag x=0 followed by [0:0:1], and the smooth conic x²+y²+z²=0 with intrinsic endpoint [0:1:i]. For O(1), ambient values are the lattice points (a,b) with a,b≥0 and a+b≤m in degree m. The normalized body is the standard triangle and its first-coordinate projection is [0,1]. On the conic, O(1) has degree two and the complete degree-m series has all orders 0 through 2m at the endpoint, giving [0,2]. Restriction is surjective for all m≥0 because H¹(P²,O(m−2)) vanishes. Thus the intrinsic interval has length two while the ambient projection has length one.

The explicit cancellation is also correct: y+i z has intrinsic order two at [0:1:i], since on y=1 its product with the unit 1−i z equals −x². Its ambient value for the chosen flag is (0,0). All flag varieties here are smooth at the relevant endpoints. The conic meets each coordinate line transversely and avoids the toric fixed points.

This example is not a verified instance of the entire special Cox presentation and tropical-refinement procedure. In particular, no such identification is established merely by agreement of rational Picard or effective cones. The intrinsic endpoint differs from the endpoint completing the ambient flag; that is natural for first-n truncation in different dimensions, and is not itself a contradiction. The literal faulty index would select a toric point absent from this conic, but the manuscript's own example already indicates the intended first-boundary reading. The only accepted negative conclusion is failure of the general projection-from-volume inference. The example does not disprove the intended Theorem 4.5, Corollary 4.7, or existence of a different suitable flag.

Combinatorial intersection codimensions are likewise insufficient, in isolation, to prove local smoothness of every flag member. The cusp diagnostic correctly illustrates that elementary point. It is not a verified counterexample to all tropical-compactification hypotheses or a proof that the source's chosen flag is singular. The review preserves this boundary.

## Birational descent and the global closed cone

Proposition 4.1 is valid as a sufficient condition. Let h:X′→X be a proper birational morphism of smooth projective varieties of the same dimension, and let an admissible flag on X′ end at a point where h is an isomorphism onto an open subset of X. Every flag member meets that open subset, so its reduced proper image is irreducible of the same dimension and is smooth at the image endpoint. These images form an admissible flag on X. The flag valuation is determined by sequential orders in the local flag, so it agrees on pullback sections.

Because X is normal, h_*O_X′=O_X, and the projection formula identifies all spaces of sections of a Cartier line bundle with those of its pullback. Equality of bodies follows first for integral and rational big classes and then for real big classes by continuity. Crucially, the proposition does not confuse a body's boundary-divisor fiber with the valuative body of an arbitrary nonbig divisor.

The asserted equality for the full global-cone slice is justified. Write C and C′ for the two global closed cones, and F=id×h*. Pullback sections imply F(C)⊆C′. For a point (v,h*d) in C′, pushforward of effective approximations shows that d is pseudoeffective. Choose an ample class a on X and w in the body of h*a. For ε>0, cone additivity places (v+εw,h*(d+εa)) in C′. The class d+εa is big, so big-fiber equality places the point in F(C). Finally let ε tend to zero. F(C) is closed: F is an injective linear map between finite-dimensional spaces, hence a homeomorphism onto a closed linear subspace. This proves

    F(C) = C′ ∩ (Rⁿ × h*N¹(X)_R).

If C′ is rational polyhedral, the right-hand side is a rational linear section of a rational-polyhedral cone. The inverse identification then gives rational polyhedrality on X. No closure-of-semigroup versus slice interchange is being assumed without this argument.

The blowup example correctly explains the need for an extra descent condition in that method. For Bl_p(P²)→P², an admissible flag beginning with the exceptional curve maps first to a codimension-two point, not a divisor. Its first valuation is the exceptional divisorial order, whose center on P² is p. It is not the first coordinate of an ordinary flag on P² beginning with a divisor. This does not show that the isomorphism-locus condition is necessary for every possible transfer of polyhedrality, nor does it exclude other flags on X. The proposition is a sufficient criterion, not an if-and-only-if characterization.

The source's X-bar is not automatically a smooth variety carrying a rational-polyhedral global cone in every degree merely because it dominates the small modifications. Applying this proposition to that particular model requires checking its own hypotheses, the flag endpoint and the appropriate cone. The audit does not silently supply these conditions.

## The cubic flag on the plane

Proposition 5.1 is valid, including its endpoint and closure details. Choose a smooth plane cubic C and a point p for which η=O_C(1)⊗O_C(−3p) is nontorsion in Pic⁰(C). Such choices exist over C: the map from p to η is, after choosing an origin, a translate of multiplication by −3, with finite fibers, whereas the torsion subgroup is countable. The flag P²⊃C⊃{p} is admissible.

For a degree-m section with order a along C, divide by the defining cubic to obtain a degree-q polynomial, q=m−3a, whose restriction to C is nonzero. Necessarily a,q≥0. At q=0, the only second order is b=0. For q≥1, the restriction map onto H⁰(C,O_C(q)) is surjective, because H¹(P²,O(q−3))=0.

Set d=3q. Riemann–Roch on the elliptic curve gives h⁰(O_C(q)(−bp))=d−b for 0≤b≤d−1. At b=d the degree-zero bundle is η^q, which is nontrivial, so it has no section. The consecutive dimensions therefore drop by one at every permitted b. The exact possible orders are b=0,…,3q−1. Surjective restriction lifts each to a polynomial with first order exactly a after multiplying by the cubic's a-th power. This proves the entire semigroup description, not just an upper bound.

Every normalized pair lies in the triangle with vertices (0,0),(1/3,0),(0,3). The first two vertices are realized by sections, and (0,3−1/m) occurs in every positive degree m. Taking the closed convex hull supplies the final vertex, which need not be a realized normalized value. Since N¹(P²)_R has the single generator H, the global cone is exactly the cone over this triangle at degree one. It is rational polyhedral.

Finite generation fails for the stated semigroup. Apart from the zero element, m>0 and b/m<3. A finite generating set would have a maximal ratio c<3, and degree-weighted averaging would force b/m≤c for every sum. The elements (m,0,3m−1) violate that bound for large m. The proof does not assume the nonrealized ray is populated. It also makes no claim that every flag on P² has a non-finitely-generated semigroup: the ordinary coordinate flag does not. This is explanatory mathematics consistent with Lazarsfeld–Mustaţă's warning, not a new obstruction to the target existence statement.

## Associated graded generation and the necessary patch

The algebraic argument in Proposition 6.1 is correct once the degree scope is explicit. Take a full lattice of actual Cartier divisors whose numerical classes form a Q-basis of N¹(X)_Q, and form the full multisection ring over that lattice. With coherent multiplication it embeds in a Laurent polynomial ring over the function field and is a domain. The associated graded algebra retains both lattice degree and valuation degree.

If finitely many homogeneous initial forms generate this algebra, the initial form of any nonzero homogeneous section is a polynomial in them. Retaining its combined-degree component leaves at least one nonzero monomial, which expresses its value and degree as a sum of generator values and degrees. Conversely products are nonzero in the domain and have additive values. Thus the value-and-degree semigroup is finitely generated. Its cone and its numerical image are finitely generated rational cones and hence closed.

The full numerical-span hypothesis is material. The phrase “a Cartier lattice” in the author freeze did not explicitly exclude a proper degree subspace or an incomplete set of allowed degrees. A semigroup for a smaller multisection ring controls only that degree region. It cannot, by that argument alone, identify the entire global cone. The correction spells out the full lattice, all lattice degrees and the passage to numerical classes. Every rational numerical class has a multiple represented there; numerical invariance on the big cone and closure identify the resulting numerical image with the full global cone.

This remains only a sufficient condition. Finite algebra generation of the Cox ring does not imply finite generation of the initial algebra for an arbitrary flag. The conic calculation explains the cancellation issue and the cubic example supplies a concrete failure of finite valuation-semigroup generation despite finite Cox generation. No sixth approach or new universal construction is introduced by making the hypothesis precise.

## Known cases and final acceptance limits

The quoted Schmitz–Seppänen results are used with the right scope. Their surface corollary applies to a smooth projective surface with rational-polyhedral effective cone and a general suitable flag. Their good-flag theorem requires each flag member to be a Mori dream space, each successive inclusion to be cut out by the stated global section, and exceptional loci of the relevant small Q-factorial modifications to meet the next member properly. These hypotheses are not automatically part of the definition of an arbitrary Mori dream space. These are valid positive regimes, not a proof of the unrestricted higher-dimensional assertion.

The acceptance has three separate levels:

- Integrity: all original pins and the complete problem/research pair match; the original freeze is unchanged.
- Authored mathematics: the conic diagnostic, isomorphism-locus descent criterion and cubic semigroup calculation are accepted; the associated-graded criterion is accepted with the explicit full-degree hypothesis in the derivative.
- Literature and target: the affirmative source theorem statements, the detailed model-flag construction and the later attribution are verified. This audit does not independently certify the exact general flag-on-X proof, refute it, or establish a current-open classification.

The original bounded nonclaim stance is largely appropriate. Its first-boundary wording and degree-lattice precision should nevertheless be corrected before treating it as the accepted deliverable. CORRECTION.patch records only authored changes. The corrected archive is separately pinned, leaving the five-file original freeze intact. No publication was performed.

## Public references

- Fulger, Küronya and Lehmann, organizers, Mini-Workshop: Positivity in Higher-dimensional Geometry: Higher-codimensional Cycles and Newton–Okounkov Bodies. Oberwolfach Reports 14 (2017), 2631–2657; Urbinati contribution, joint with Postinghel, printed pp. 2652–2654. https://ems.press/journals/owr/articles/15586
- Postinghel and Urbinati, Newton-Okounkov bodies and Toric Degenerations of Mori dream spaces via Tropical compactifications, arXiv:1612.03861v4. https://arxiv.org/abs/1612.03861v4
- Küronya, Maclean and Roé, Concave transforms of filtrations and rationality of Seshadri constants, arXiv:1901.00384v2, p. 2. https://arxiv.org/abs/1901.00384v2
- Lazarsfeld and Mustaţă, Convex bodies associated to linear series, Ann. Sci. Éc. Norm. Supér. 42 (2009), 783–835; Example 1.8, global-cone construction and Problem 7.1. https://doi.org/10.24033/asens.2109
- Schmitz and Seppänen, On the polyhedrality of global Okounkov bodies, arXiv:1403.4517v1; Theorem 1 and Corollary 2. https://arxiv.org/abs/1403.4517v1
- Schmitz and Seppänen, Global Okounkov bodies for Bott–Samelson varieties, arXiv:1409.1857v2; Definition 3.5 and Theorem 3.6. https://arxiv.org/abs/1409.1857v2
- Cucchiara and coauthors, Gemini Spectroscopy of the Short GRB 130603B Afterglow and Host. The wrongly supplied astronomy identifier. https://arxiv.org/abs/1306.2028
