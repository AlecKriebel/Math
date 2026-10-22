# A bounded audit of the Mori dream global-cone question

## 1. Exact question and outcome

Work over the complex numbers. For every smooth projective Mori dream space X, is there a complete admissible flag **on X** such that its global Newton–Okounkov cone is rational polyhedral?

Here an admissible flag X = Y_0 ⊃ Y_1 ⊃ ... ⊃ Y_n = {p} has irreducible members of codimension i, all smooth at p. The global object is a closed convex cone in R^n × N^1(X)_R; a divisor's Newton–Okounkov body is a fiber over its numerical class when the divisor is big. A bounded polytope and the global cone must not be conflated.

**Outcome.** No universal flag construction or counterexample to the existence question is established here. The positive announcement in the original source is important prior literature, but this audit leaves its applicability and proof uncertified. The results below isolate precise obstacles and valid sufficient conditions. They are not claimed to be new theorems of the subject.

## 2. Source correction and scope of the announced answer

The official Oberwolfach report contains the question on printed p. 2653 and an affirmative announcement in Theorem 6 on p. 2654 [OWR]. The closely related manuscript is Postinghel–Urbinati, arXiv:1612.03861v4, whose latest listed revision is 2018-01-25 [PU]. The unrelated identifier arXiv:1306.2028 belongs to an astronomy paper [WRONG-ID].

The affirmative claim is explicitly about X: [OWR, Theorems 5–6] and [PU, Theorems 1.2–1.3 and Corollary 4.7] must not be summarized as merely announcing a birational-model variant. In the detailed construction, however, [PU, Lemma 4.2 and Remark 4.4] put the flag on a birational model X-bar; the remark calls these infinitesimal flags for X. A valuation on the common function field can be used to define bodies of divisors on X by pullback, but that convention alone does not exhibit an admissible flag of subvarieties on X. Theorem 4.5 relies on a coordinate-projection identity for the ambient toric body. This audit does not independently validate the passage from that construction to the exact flag-on-X conclusion.

The printed index m−n+i in Lemma 4.2 is inconsistent with the prose describing truncation to the first n elements when m>n. The interpretation using the first ambient boundary intersections is supported by the manuscript itself: Section 5.1.1, p. 12, works with a surface flag obtained from the first ambient divisor and then a codimension-two intersection. Accordingly the index mismatch should be treated as a likely typographical/expository defect with a source-supported intended repair, not as a standalone refutation of the theorem. Local admissibility and compatibility of restricted valuations still need to be checked under the actual special-construction hypotheses.

A later source [KMR, arXiv v2, p. 2] explicitly attributes the flag-on-X global-polyhedrality result to Postinghel–Urbinati. This is important corroboration of the prior affirmative claim; it is not an independent proof of the construction steps being audited. The critical printed pages and the example were inspected as images because text extraction loses the bars. No correction or withdrawal, and no journal version of [PU], was verified in the bounded search. Neither the absence of such a record nor this audit's inability to certify a proof establishes the mathematical community's current open/solved consensus.

The remaining sections are this audit's mathematical analysis, not a report of a published criticism.

## 3. Restriction surjectivity does not give coordinate projection

### Proposition 3.1: a smooth conic diagnostic

Let Z = P^2_C with homogeneous coordinates [x:y:z], let H = O_Z(1), and let

    C = {x^2 + y^2 + z^2 = 0} ⊂ Z.

Use the torus-invariant admissible ambient flag

    Z ⊃ L = {x=0} ⊃ q = [0:0:1].

Let p = [0:1:i] ∈ C ∩ L, and use the intrinsic curve flag C ⊃ {p}. Both varieties are smooth Mori dream spaces. Each coordinate line meets C transversely in two points, and C avoids all three torus-fixed points.

Then

    Δ_ambient(H) = {(a,b): a≥0, b≥0, a+b≤1},
    π_1(Δ_ambient(H)) = [0,1],
    Δ_p(H|_C) = [0,2].

The restriction map H^0(Z,O_Z(m)) → H^0(C,O_C(m)) is surjective for every integer m≥0. Thus even complete restricted series, equality of restricted and intrinsic volumes, and proper transverse boundary intersections do not imply the displayed coordinate-projection identity.

**Proof.** For a homogeneous polynomial of degree m, the first ambient valuation coordinate is the largest power of x dividing it. After removing x^a and restricting to L, the second coordinate is the order at q. Its possible values are precisely nonnegative integral pairs (a,b) with a+b≤m, witnessed by monomials x^a y^b z^(m-a-b). Taking scaled convex hulls gives the triangle.

The conic is isomorphic to P^1 and H|_C has degree 2. A degree-2m complete linear series on P^1 has every vanishing order from 0 through 2m at p. Its Newton–Okounkov interval is therefore [0,2].

The ideal sequence of C is

    0 → O_Z(m-2) → O_Z(m) → O_C(m) → 0.

Since H^1(P^2,O(k))=0 for all integers k, restriction is surjective. Consequently its restricted volume equals the intrinsic degree 2, whereas the projected ambient interval has length 1.

For a concrete cancellation, the tangent line section t = y + i z has intrinsic vanishing order 2 at p but ambient valuation (0,0). Indeed, on the chart y=1 the conic equation gives

    (1+i z)(1-i z) = 1+z^2 = -x^2,

and 1-i z is a unit at p. Neither y nor z vanishes at p. Their linear combination acquires the extra order. This is exactly the cancellation that a monomial projection fails to record. ∎

### What the example does, and does not, refute

This proves failure of the general inference “surjective restriction or restricted-volume equality implies a coordinate-projected toric body.” It is **not asserted to be a counterexample satisfying every hypothesis of the complete special construction in [PU]**, and is not a disproof of Corollary 4.7.

In particular, the intrinsic endpoint p differs from the toric endpoint q. The printed formula in Lemma 4.2 takes the intersection with Y^Z_(m-n+i); for m=2,n=1,i=1 this is the toric endpoint, which C avoids. Thus that literal formula does not even produce this curve flag. The first-boundary interpretation requires correcting the displayed index, but it is supported both by the lemma’s prose and by the explicit flag in [PU, Section 5.1.1, p. 12]. The conic comparison therefore remains a diagnostic for the general inference, not a counterexample to the intended special construction. In the latter setting the admissible flag and the required valuation compatibility must be justified. Proposition 3.1 shows why restricted-volume equality by itself cannot supply the projection identity: it concerns the intrinsically valued restricted series, not the Euclidean volume of the coordinate-projected ambient body.

No assertion is made that the conic embedding is the particular chosen Cox presentation and tropical refinement required by that manuscript. Its Picard and effective cones do agree over Q with those of the ambient plane, but this numerical agreement is insufficient to identify the full construction.

## 4. A precise criterion for descent from a birational model

### Proposition 4.1: descent in the isomorphism locus

Let h: X' → X be a proper birational morphism of smooth projective n-folds. Let Y'_• be an admissible flag on X' with endpoint p'. Suppose p' lies in an open set on which h is an isomorphism onto an open subset of X. Put Y_i = h(Y'_i).

Then Y_• is an admissible flag on X and, for every Cartier divisor D on X and every nonzero section s of O_X(D),

    ν_(Y'_•)(h^*s) = ν_(Y_•)(s).

Under id × h^*, their global cones satisfy

    (id × h^*) Δ_(Y_•)(X)
      = Δ_(Y'_•)(X') ∩ (R^n × h^*N^1(X)_R).

In particular, a rational-polyhedral global cone on X' with such a flag gives a rational-polyhedral global cone on X.

**Proof.** Each Y'_i meets the isomorphism locus because it contains p'. Its proper image is irreducible and has the same dimension. Near p=h(p'), the image flag is identified with the original flag, so it is smooth and admissible. The sequential local orders defining the valuation agree under that identification.

Normality of X gives h_*O_(X')=O_X. The projection formula identifies H^0(X',h^*O_X(D)) with H^0(X,O_X(D)); the identification is pullback. Thus all section valuations of pullback divisors agree.

For a big real divisor class d on X, h^*d is big and the corresponding bodies agree. The assertion is first obtained for rational classes from sections and then for real big classes by continuity. To extend from big fibers to the entire displayed slice, take (v,h^*d) in the right-hand side. Its class is pseudoeffective; pushing forward effective approximations shows d is pseudoeffective. Fix an ample class a on X and a point w in Δ_(Y'_•)(h^*a). Since a global cone is closed under addition, for every ε>0,

    (v+εw, h^*(d+εa)) ∈ Δ_(Y'_•)(X').

The class d+εa is big. The point therefore belongs to the left-hand side by big-fiber equality. Let ε tend to zero and use closedness. The other inclusion follows directly from pullback sections and closure. The slice is a rational linear section of a rational-polyhedral cone, and h^* is an injective rational linear map. This proves the final assertion. ∎

### Why the extra hypothesis cannot be dropped from the flag argument

For h: Bl_p(P^2) → P^2, the flag X' ⊃ E ⊃ {q'} with E the exceptional divisor is admissible. Its first image is the point p, of codimension 2. The images are not a complete flag on P^2. Its first valuation is the order along E, which is the multiplicity at p of a pulled-back local function. Such a valuation has center of codimension 2 on P^2, whereas the first coordinate of a flag on P^2 is the order along a divisor, with codimension-1 center. Consequently this particular flag valuation cannot simply be declared an admissible-flag valuation on X.

This does not rule out a different flag on X or another argument transferring polyhedrality. It identifies the missing task: prove that a suitable polyhedral flag lies in an isomorphism locus, or give a genuinely different descent construction.

Correct intersection dimensions alone also do not establish admissibility: in the smooth plane, the cusp y^2=x^3 has codimension 1 and meets the line x=0 in codimension 2, but the cusp is singular at their intersection. An admissibility proof must check local smoothness, beyond dimension counts or a combinatorial normal-crossings condition.

## 5. Polyhedrality is strictly weaker than finite generation, even on P^2

### Proposition 5.1: an explicit value semigroup

Let X=P^2_C, let C⊂X be a smooth plane cubic, and choose p∈C so that

    η = O_C(1) ⊗ O_C(-3p)

is non-torsion in Pic^0(C). Such points exist: after fixing an origin on the elliptic curve, p↦η is a translate of multiplication by -3, a finite surjective map, while torsion points are countable and C(C) is uncountable.

For the admissible flag X ⊃ C ⊃ {p}, write

    Γ = {(m,a,b): m≥0, s∈H^0(X,O_X(m))\{0}, ν(s)=(a,b)}.

Its exact description is as follows. Set q=m-3a. Then a is a nonnegative integer, q≥0, and

- if q=0, precisely b=0 occurs;
- if q≥1, precisely the integers 0≤b≤3q-1 occur.

Consequently

    Δ_(C,p)(O_X(1)) = conv{(0,0),(1/3,0),(0,3)},

and the global cone is rational polyhedral. Nevertheless Γ is not finitely generated.

**Proof of the exact values.** A section with first order a is F_C^a times a degree-q polynomial g whose restriction to C is nonzero. This accounts for q=m-3a≥0. When q=0 the residual section is constant. For q≥1, restriction H^0(P^2,O(q)) → H^0(C,O_C(q)) is surjective, by the cubic ideal sequence and H^1(P^2,O(q-3))=0.

Put d=3q and M=O_C(q). On an elliptic curve, a positive-degree line bundle of degree e has h^0=e, by Riemann–Roch and the absence of sections in negative degree. Therefore

    h^0(M(-bp)) = d-b      for 0≤b≤d-1.

At b=d the degree-zero bundle is η^q, nontrivial by the non-torsion choice. A nontrivial degree-zero line bundle has no section: a nonzero section would have an effective divisor of degree zero and hence trivialize the bundle. Thus the filtration drops by one at every b=0,...,d-1 and then vanishes. Every listed exact order occurs, and none higher does. Surjective restriction lifts these orders to g. Multiplication by F_C^a completes the description.

**Proof of the body and global cone.** All normalized pairs satisfy a/m≥0, b/m≥0 and

    3(a/m) + (b/m)/3 ≤ 1.

The values (0,0) and (1/3,0) are realized, while (0,3-1/m) occurs for every m≥1. Their closed convex hull is the stated triangle. Since N^1(P^2)_R has the single generator H, the global cone is the cone over this triangle at degree 1; explicitly it is generated by

    (0,0,1), (1/3,0,1), (0,3,1).

**Proof of non-finite generation.** Every nonzero Γ element has m>0 and b/m<3. If Γ were generated by a finite set, the largest of these finitely many ratios would be some c<3. The ratio of a sum is a degree-weighted average of the summands' ratios, so every element would satisfy b/m≤c. The elements (m,0,3m-1) contradict this for large m. ∎

This is a concrete version of the familiar semigroup phenomenon discussed in [LM, Example 1.8 and Problem 7.1]. It neither contradicts the target, which only asks for a rational-polyhedral cone, nor prevents other flags on P^2 from having finitely generated semigroups.

## 6. What finite Cox generation would have to be strengthened to

### Proposition 6.1: a sufficient associated-graded condition

Choose Cartier divisors D_1,...,D_ρ whose numerical classes form a Q-basis of N^1(X)_Q, put Λ=⊕_i Z D_i, and use the full multisection ring

    R = ⊕_(D∈Λ) H^0(X,O_X(D)).

Multiplication uses these actual Cartier representatives, so R is a domain embedded in a Laurent polynomial ring over the function field of X. Fix an admissible flag on X, and record both the lattice multidegree and the flag value. Suppose finitely many homogeneous sections s_1,...,s_N have initial forms generating the associated graded algebra of R for this combined grading/valuation. The full numerical-span hypothesis is essential for a conclusion about the entire global cone; a ring using only a smaller degree set would control only that degree region.

Then the value-and-degree semigroup is generated by

    (ν(s_1),deg(s_1)), ... , (ν(s_N),deg(s_N)),

and the numerical global Newton–Okounkov cone is rational polyhedral.

**Proof.** The initial form of any nonzero homogeneous section is a nonzero polynomial in these initial forms. Keep only terms in its degree and valuation component; at least one nonzero monomial remains. Its value and degree are the sum of those of its factors. Conversely every product of the s_i is nonzero because the section ring is a domain, and multiplicativity adds values and degrees. This proves semigroup equality. Its closed cone is finitely generated by integral vectors. Because Λ spans the full numerical divisor space, every rational numerical class has an integral multiple represented in Λ; the usual numerical invariance for big divisors and closure therefore identify its numerical image with the full global Newton–Okounkov cone. The image is a finitely generated rational cone and hence already closed. This proves rational polyhedrality. ∎

Finite generation of R as an algebra does not provide this associated-graded hypothesis. Cancellation can change an initial form, as Proposition 3.1 illustrates, and Proposition 5.1 exhibits failure of finite semigroup generation for a flag on a variety with finitely generated Cox ring. The sufficient condition is stronger than the question and is not claimed to be necessary.

The established good-flag criterion of Schmitz–Seppänen supplies rational polyhedrality when every flag member is itself a Mori dream space, consecutive members are Cartier cuts by sections, and each small Q-factorial modification has exceptional locus meeting the next flag member properly [SS-B, Definition 3.5 and Theorem 3.6]. Surfaces with rational-polyhedral effective cone are covered by a separate theorem [SS-P, Corollary 2]. Neither reference supplies those flag hypotheses for every smooth Mori dream space.

## 7. Final boundary

For this investigation to certify a resolution of the exact task, it would have to supply or independently verify one of the following:

1. A proof of existence of a suitable admissible flag on every original X, including the missing local smoothness, restriction-valuation, and descent steps; or
2. A smooth Mori dream space for which every admissible flag on X fails rational polyhedrality.

Neither has been provided. Bad flags, non-finite semigroups, or polyhedral cones on birational models are not substitutes. The current contribution is a bounded, reproducible mathematical audit of that distinction.

## References

[OWR] M. Fulger, A. Küronya, B. Lehmann (organizers), *Mini-Workshop: Positivity in Higher-dimensional Geometry: Higher-codimensional Cycles and Newton–Okounkov Bodies*, Oberwolfach Reports 14 (2017), 2631–2657, published 2018. Stefano Urbinati's contribution, joint with Elisa Postinghel, pp. 2652–2654. https://doi.org/10.4171/OWR/2017/43

[PU] E. Postinghel, S. Urbinati, *Newton-Okounkov bodies and Toric Degenerations of Mori dream spaces via Tropical compactifications*, arXiv:1612.03861v4, 2018. https://arxiv.org/abs/1612.03861v4

[LM] R. Lazarsfeld, M. Mustaţă, *Convex bodies associated to linear series*, Ann. Sci. Éc. Norm. Supér. 42 (2009), 783–835. https://doi.org/10.24033/asens.2109

[SS-P] D. Schmitz, H. Seppänen, *On the polyhedrality of global Okounkov bodies*, Adv. Geom. 16 (2016), 83–91. https://arxiv.org/abs/1403.4517 and https://doi.org/10.1515/advgeom-2015-0042

[SS-B] D. Schmitz, H. Seppänen, *Global Okounkov bodies for Bott–Samelson varieties*, J. Algebra 490 (2017), 518–554. https://arxiv.org/abs/1409.1857v2 and https://doi.org/10.1016/j.jalgebra.2017.07.018

[WRONG-ID] A. Cucchiara et al., *Gemini Spectroscopy of the Short GRB 130603B Afterglow and Host*. https://arxiv.org/abs/1306.2028

[KMR] A. Küronya, C. Maclean, J. Roé, *Concave transforms of filtrations and rationality of Seshadri constants*, arXiv:1901.00384v2, 2019, p. 2. https://arxiv.org/abs/1901.00384v2
