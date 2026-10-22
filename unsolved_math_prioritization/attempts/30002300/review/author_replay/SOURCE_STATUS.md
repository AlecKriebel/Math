# Signed simplex representations without general position

**The affine-spanning hypothesis can be removed completely. This is a published result, not a new discovery.** Akopyan–Bárány–Robins, Theorem 1 (2017), gives the required signed representation with vertices in an even smaller allowed set. The 2018 published version of *On moments of a polytope* explicitly acknowledges this resolution. Separate source and mathematical review is pending. No new proof-search attempt was used.

## 1. Exact affirmative statement

For d≥1, let P⊂Rᵈ be a compact finite union of convex polytopes, and let V(P) be the intersection of the vertex sets of its triangulations, as in the original report. Write

\[
\lambda_P(E)=\operatorname{Vol}_d(E\cap P).
\]

There are finitely many nondegenerate d-simplices T with vertices in V(P), and integers a_T, such that

\[
\boxed{\quad \lambda_P=\sum_T a_T\lambda_T.\quad}
\tag{1}
\]

No condition on the affine span of every (d+2)-subset, or every (d+1)-subset, is needed. Each simplex that actually occurs still has d+1 affinely independent vertices. The simplices may overlap and need not be contained in P. Their signed measures cancel where necessary; (1) is not a vertex-only triangulation claim.

For a positive-volume P, if “uniform” is normalized to mean probability measure, put ν_P=λ_P/Vol(P). Then the same statement is

\[
\boxed{\quad
\nu_P=\sum_T a_T\frac{\operatorname{Vol}(T)}{\operatorname{Vol}(P)}\,\nu_T.
\quad}
\tag{2}
\]

These coefficients are real and sum to one, and may be negative. The existence question is therefore unchanged by either normalization. Integer coefficients in (1) must not be asserted for the probability normalization in (2).

## 2. Original question and a normalization wrinkle

The target is **Question 3**, printed p.639, following Theorem 2 on p.638 of Dmitrii Pasechnik's complete contribution, pp.637–640, in [OWR 11/2013](https://ems.press/content/serial-article-files/46446). Theorem 2 assumes |V|≥d+2 and that each (d+2)-subset spans Rᵈ, and allows arbitrary real signed coefficients on spanning (d+1)-subsets of V. Question 3 asks whether the spanning condition can be removed or weakened. Formula (1), or (2) if probability normalization is used, removes it.

The source first specifies unit-density measures for its Fantappiè formulas, but uses the words “uniform probability measure” immediately before Theorem 2. Its informal unweighted-sum wording and subsequent ±1 question should not be used to conceal this switch. Equations (1)–(2) treat both conventions explicitly. The requested existence of real signed coefficients is valid in either case, so this terminology does not leave the assigned question unresolved.

All indicator equalities used here are almost everywhere with respect to ambient d-dimensional Lebesgue measure. Equivalently, (1) is equality of Borel measures. Boundary values and lower-dimensional pieces carry no mass. A zero-volume P has the zero unit-density measure and the empty decomposition; its ambient uniform probability measure is undefined. No intrinsic surface or atomic measure on a degenerate simplex is being introduced.

## 3. Published theorem and the allowed vertices

The primary result is Akopyan–Bárány–Robins, [*Algebraic vertices of non-convex polyhedra*](https://arxiv.org/abs/1508.07594v2), **Advances in Mathematics 308 (2017), 627–644**, [DOI 10.1016/j.aim.2016.12.026](https://doi.org/10.1016/j.aim.2016.12.026), Theorem 1 and its proof in Section 3.

A point v is an algebraic vertex when the indicator of the tangent cone at v cannot be expressed, almost everywhere, as a finite real linear combination of line-cone indicators. A line-cone is invariant in some nonzero direction. Let A(P) be this set. The published theorem supplies

\[
\mathbf 1_P=\sum_T a_T\mathbf 1_T\quad\text{almost everywhere},
\qquad a_T\in\mathbb Z,
\qquad \operatorname{Vert}(T)\subseteq A(P).
\tag{3}
\]

Its assumptions are those of a generalized polytope, namely a bounded finite union of convex polyhedra; there is no general-position restriction.

To match the source's exact vertex convention, it suffices to check

\[
A(P)\subseteq V(P).
\tag{4}
\]

Take any finite triangulation of P and suppose v is not a vertex of any of its simplices. For a simplex containing v, the minimal face containing v has positive dimension, and the tangent cone is invariant along that face's linear span. It is therefore a line-cone. A simplex not containing v contributes zero. Adding the tangent-cone indicators over the triangulation expresses the tangent indicator of P at v as a sum of line-cones, up to null boundaries. Thus v is not algebraic. Since this applies to every triangulation, (4) follows.

This argument requires no identification of convex-hull vertices, geometric vertices, or the vertices of one chosen triangulation. Combining (3) with (4), and integrating indicator functions, proves the exact source match (1). Positive-volume simplices have d+1 affinely independent vertices; any lower-dimensional terms can simply be omitted in ambient measure.

The same inclusion is explained in the related [denominator-source audit, PR 58](https://github.com/AlecKriebel/Math/pull/58). It is used here only to match the separate signed-representation target, not presented as another discovery.

## 4. Why the published proof does not hide a genericity assumption

The complete proof of Theorem 1 was checked, including its extension to compactly supported polyhedral step functions. It proceeds by induction on dimension using signed jumps across facet hyperplanes. Algebraic vertices of a nonzero signed section are algebraic vertices of the original function. One then cones the lower-dimensional simplex representations to an algebraic vertex of the original function. For integer-valued indicators, the section coefficients and hence the final coefficients stay integral.

Two details are relevant to the question's degeneracies. A line-cone's signed section either vanishes or is a signed combination of line-cones in the section hyperplane, so the vertex-inclusion argument survives cancellations. Also, when the chosen apex lies on a facet hyperplane, its cone over that section is lower-dimensional and contributes zero almost everywhere. Such facets may be omitted from the full-dimensional ray calculation. Facets not through the apex are oriented toward it; the jumps along a generic ray telescope because the function has bounded support. No perturbation of the vertex set is needed.

This describes the mechanism of the credited proof. It is not a new simplex-decomposition theorem or a replacement of the signed conclusion by an unsigned triangulation.

## 5. Explicit published acknowledgment and remaining separate questions

The later published [Gravin–Pasechnik–Shapiro–Shapiro, *On moments of a polytope*, Analysis and Mathematical Physics 8 (2018), 255–287](https://link.springer.com/article/10.1007/s13324-018-0226-8), calls its **Conjecture 7** a corollary of Akopyan–Bárány–Robins Theorem 1. It states the decomposition for arbitrary spanning vertex sets and notes the integer-coefficient strengthening. Its Theorem 9 is the older weak-nondegeneracy result. Retaining the historical label “Conjecture 7” therefore does not mean that removal of the hypothesis remained open in that publication.

The same article immediately formulates a stronger **Conjecture 8** about a decomposition using a set of simplices with coefficients ±1. Integer coefficients do not settle that stronger restriction. The neighboring source Question 2, record **30002299**, is not resolved or reclassified by this package. The vertex-factored denominator question, **30002298**, is separately treated by the companion audit. These are related targets sharing sources, not three independent new discoveries.

This package also does not assert a new inversion algorithm, an unsigned decomposition without extra vertices, a canonical coefficient choice, or an analogous statement for arbitrary singular densities.

## 6. Exact controls and disposition

The checker uses a nonconvex planar U-shaped polygon with four collinear genuine boundary vertices, violating the d+2 condition in dimension two. In cyclic order those vertices are (0,0), (3,0), (3,2), (2,2), (2,1), (1,1), (1,2), (0,2). A signed fan from (0,0) uses only these eight vertices. Its product with [0,1] violates the condition in dimension three and is represented by eighteen signed tetrahedra using only the sixteen product vertices.

Exact integer/rational controls check nondegeneracy of the occurring simplices, signed coverage away from their boundaries, moments through total degree three, and both the unit-density and probability coefficient normalizations. All 699 exact assertions pass. These small examples illustrate the theorem's scope; they do not prove the general published theorem or the separate ±1 conjecture.

Recommend **already_solved**, with credit to Akopyan–Bárány–Robins (2017), corroborated explicitly by Gravin–Pasechnik–Shapiro–Shapiro (2018). **Zero new substantive proof attempts** were used. No historical-priority claim is made.
