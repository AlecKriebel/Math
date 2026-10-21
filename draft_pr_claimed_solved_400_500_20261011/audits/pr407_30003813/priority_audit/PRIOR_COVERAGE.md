# A checkable prior-coverage certificate for the literal signed path question

The frozen PR head is `e3f8838a8eac68bbd186fc0234ac2e2a49194626`. The audited source asks for a combinatorial interpretation of the h-star polynomial for every choice of weak adjacent-sum inequalities in the unit cube. It does not prescribe a particular permutation statistic. This certificate verifies coverage by a prior general theorem; it does not assert that the source authors recognized or announced the resulting specialization.

## The target and an integral change of coordinates

For every integer n >= 1 and every sign word epsilon of length n-1, let Q_epsilon consist of x in [0,1]^n with x_i+x_(i+1) <= 1 for a minus sign and >= 1 for a plus sign. Define

\[
y_0=0,\qquad y_i=x_1+\cdots+x_i\quad (1\le i\le n).
\]

The cumulative-coordinate matrix is triangular with diagonal 1. Its inverse is x_i=y_i-y_(i-1). It is therefore a linear isomorphism of Z^n, on every nonnegative integer dilation including m=0. The image C_epsilon is defined by

\[
0\le y_i-y_{i-1}\le1\quad(1\le i\le n),
\]

and

\[
y_{i+1}-y_{i-1}\le1\quad\hbox{or}\quad
y_{i+1}-y_{i-1}\ge1
\]

according to the same sign. Every supporting hyperplane is y_a-y_b=k with integer k and indices in {0,...,n}. Boundedness follows from 0 <= y_i <= i. The polytope is full dimensional: equivalently reflect every even x-coordinate; the resulting inequalities orient a path, which is acyclic, and an increasing assignment along any linear extension gives a point satisfying every inequality strictly. Thus C_epsilon is a proper type-A alcoved lattice polytope in the exact coordinates and lattice used in the prior theorem.

## The prior theorem already supplies all coefficient counts

[Benedetti–Knauer–Valencia-Porras, arXiv:2303.10458v1](https://arxiv.org/pdf/2303.10458v1), publicly posted 18 March 2023, defines its arrangement in Section 2, PDF pp.3–4, by y_i-y_j=l, i,j in {0,...,n}, with y_0=0. Its **Theorem 2.6, PDF/printed p.7**, states that for any such alcoved polytope P,

\[
h^*_k(P)=\#\{A\in\Delta(P):\operatorname{indeg}_{A_0}(A)=k\}.
\]

Here Delta(P) is the finite alcove triangulation; two cells are adjacent when they share a facet. Fix any root alcove A_0 and orient adjacency from smaller to larger graph distance from A_0. The right side counts alcoves with exactly k incoming arcs. Proposition 2.2 and Lemma 2.4 give a connected bipartite graph and this orientation; Proposition 2.5 supplies a shelling. Theorem 2.6 then uses the standard h-star formula for a shellable unimodular triangulation. Its domain is all alcoved polytopes, despite the paper's main application being matroids.

Applying that already stated theorem to C_epsilon gives, without any unproved new result,

\[
\boxed{h^*_{Q_\epsilon}(z)
  =\sum_{A\in\Delta(C_\epsilon)}
     z^{\operatorname{indeg}_{A_0}(A)}.}
\]

This provides a finite combinatorial rule for every coefficient, for every n and sign word. The theorem counts the entire closed lattice polytope; equality boundaries are handled by its shelling and half-open decomposition, rather than discarded as measure zero. For n=1 there is one alcove and the numerator is 1.

The current September 2026 v2 of that arXiv identifier has a different title and omits the earlier longer Ehrhart treatment. It explicitly describes the preliminary longer version as containing the detailed triangulation and Ehrhart analysis. This certificate cites the immutable v1 and does not silently substitute its theorem numbers into v2. The general mechanism also appears independently in [Bullock–Jiang, arXiv:2412.02787v2](https://arxiv.org/pdf/2412.02787v2), Theorem 5.4, PDF p.8. For our type-A integer arrangement every alcove is unimodular and every facet weight is 1; their numerator therefore specializes to the same graph statistic. The exact-coordinate 2023 theorem suffices on its own and avoids any ambiguity about the ambient lattice of other root systems.

## A relation to the original cyclic-order objects

[Ayyer–Josuat-Vergès–Ramassamy 2020](https://ahl.centre-mersenne.org/item/10.5802/ahl.33.pdf), Section 4, Lemma 4.1 and Proposition 4.6, printed pp.283–285, already identifies generic signed cube regions by the circular order of the fractional cumulative coordinates (0,{y_1},...,{y_n}). Its signed identity is Proposition 4.6, equation (4.2). Thus the alcoves used above can also be indexed by the original signed circular-extension class. Their additional statistic is incoming degree in a specified finite graph; this is not the raw descent statistic from AJR's separate upper-bound-family theorem. This observation is not required for the literal coefficient-counting criterion, but shows that prior coverage need not be limited to unrelated lattice-point objects.

## Independent reproduction and its limits

The accompanying `reproduce_alcoved_coverage.py` imports no PR verifier or order-poset/natural-label code. It constructs integer alcove vertices from fractional cumulative-coordinate orderings, checks unit determinants and all signed closed inequalities, computes facet adjacency, orients it by breadth-first distance, and compares incoming-degree coefficients against direct original-coordinate integer counts.

Both normal and optimized Python runs pass all **255** sign words in dimensions 1 through 8, **46,233** alcoves, **813** choices of root, and **2,813** direct Ehrhart evaluations. It rejects raw fractional-order descents as a universal substitute, distinguishes the centered type-B lattice by the 3-versus-6 lattice-point triangle control, and distinguishes the 2026 period-two upper-bound model by its 9-versus-8 four-dimensional count. These finite checks support the application and expose convention errors. The all-dimension coverage rests on the displayed integral map and the already stated prior theorem.

## Disposition and exact historical gap

**Recommendation: `already_solved` for the literal target that this PR claims to answer.** A prior publicly available general theorem already states a complete coefficient-counting rule on a class containing every target polytope, and the inclusion is the explicit integral substitution above. This is positive evidence of full prior coverage, not an inference from absence of a paper naming the OWR question.

No publication was located explicitly announcing that this exact 2018 question was closed, or printing the PR's particular relative-descent formula for all signed adjacent-sum polytopes. That is the remaining historical-attribution gap. It does not invalidate prior mathematical coverage of the accepted literal criterion. A stricter criterion demanding a specially preferred statistic, or an explicitly named historical closure, would be a different evidentiary condition and must be stated as such. The present audit neither supplies that preference nor treats it as part of the source statement.
