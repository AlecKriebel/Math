# Turn 1: a zero-probability obstruction to the equiangular, length-preserving lift

Problem 30006025 / OWR-14298589-010. First substantive author turn. **The original geometric Chapuy question remains unresolved.** This turn excludes one precise direct construction: retaining the continuously sampled metric-map edge lengths while demanding a geodesic, equiangular hyperbolic polygon with 120-degree corners. Smooth cubic vertices alone do not require equal corner angles, so this is not a universal geometric impossibility theorem.

The known decorated-tree sampling of trivalent metric maps is credited to Chapuy–Féray–Fusy and to Barazer–Giacchetto–Liu (2025), Section 6, https://doi.org/10.1017/fms.2025.31 . The source normalization and the distinction from a Weil–Petersson surface law are in SOURCE_GATE.md. The proof uses the established Hermite–Lindemann theorem, not a new transcendence result; an explicit primary statement is Theorem A in E. Delaygue, https://arxiv.org/abs/2210.12046v2 .

## 1. Exact class and metric normalization

Fix genus g>=2. A trivalent one-face orientable map has

    E=6g−3 edges,       V=4g−2 vertices,       N=2E=12g−6 sides.   (1)

Choose any pairing of the N cyclic side positions which gives such a map. A positive edge-length vector l=(l_1,...,l_E) induces a boundary word of N side lengths, with every edge length appearing twice. Fix total face perimeter P>0, so

    l_e>0,           sum_e l_e=P/2.                       (2)

The source's metric-map model has P=12g. Conditional on the combinatorial map, its metric has a density on the open simplex (2), specifically the scaled Dirichlet(1,...,1) law in the one-face trivalent model. The polygon boundary perimeter is twice the sum of graph edge lengths; omitting this factor would change the theorem's normalization.

We ask whether the cyclic boundary word can be realized by a closed geodesic polygon in the curvature-minus-one hyperbolic plane, with every interior angle 2pi/3, retaining the given side lengths. This condition is necessary for the particular construction that glues such a convex equiangular polygon into a smooth cubic surface: three polygon corners meet at each map vertex and their total angle is then 2pi. We fix the curvature and length units; rescaling the curvature is not allowed inside this class.

**Theorem.** If P is a positive algebraic real number, the vectors in (2) admitting such a polygon have Lebesgue measure zero in that simplex. In particular, for the source value P=12g, a metric sampled with any density on (2) almost surely admits no such length-preserving equiangular polygon, for any side pairing.

The theorem permits arbitrary random or length-dependent selection from the finitely many side pairings and orderings at this fixed size. It does not exclude changing the edge lengths, allowing variable corner angles, changing the polygon/spine, or using a different geometric correspondence.

## 2. Framed holonomy is a necessary closure condition

Use the upper half-plane model and PSL_2(R), which acts freely and transitively on oriented unit tangent frames. Moving an oriented frame forward by a geodesic distance x is represented by

    T(x) = diag(exp(x/2), exp(−x/2)).

Rotating it counterclockwise through the exterior angle pi/3 is represented by

    R = [ sqrt(3)/2    1/2       ]
        [ −1/2        sqrt(3)/2 ].

Both matrices have determinant one. Starting from a frame, traversing a side of length x and turning by pi/3 right-multiplies its representing matrix by T(x)R. Thus, for a fixed side word w=(w_1,...,w_N), the product

    H_w(l)=product_{j=1}^N [T(l_(w_j)) R]                 (3)

must be the identity in PSL_2(R) if the polygon closes with its initial tangent frame. In SL_2(R) this means H_w=I or −I. In particular the real-analytic scalar function

    F_w(l)=(trace H_w(l))²−4                              (4)

must vanish.

Only necessity is used. A parabolic matrix also makes (4) vanish without being the identity, and even identity holonomy alone is not asserted to ensure a simple convex polygon. Enlarging the set by the necessary scalar condition is harmless for the measure-zero argument.

## 3. The necessary analytic equation is not identically zero

The simplex (2) is connected. At its barycenter every edge length, and hence every polygon side length, equals

    x=P/N.

The pairing and cyclic ordering disappear from (3), which becomes A^N with A=T(x)R. Its trace is

    z=trace A=sqrt(3) cosh(P/(2N)).                       (5)

Let C_0(Z)=2, C_1(Z)=Z, and C_n(Z)=Z C_(n−1)(Z)−C_(n−2)(Z). Cayley–Hamilton gives trace(A^n)=C_n(trace A); for n>=1, C_n is a monic integer polynomial of degree n.

Since P/(2N) is nonzero algebraic, Hermite–Lindemann says exp(P/(2N)) is transcendental. Its hyperbolic cosine is also transcendental: an algebraic value c would make that exponential a root of Z²−2cZ+1, hence algebraic. Therefore z in (5) is transcendental. The nonzero integer polynomial C_N(Z)²−4 cannot vanish at z. Consequently

    F_w(P/N,...,P/N) != 0                                (6)

for every side word, proving that the restriction of F_w to the simplex is not identically zero.

No approximate floating-point computation or inferred equality of lengths is used in (6). The argument works for every g>=2 at once. It also explains why the algebraicity restriction on P is explicit rather than silently omitted.

## 4. The probability conclusion and finite choices

A nonzero real-analytic function on a connected open subset of R^d has a zero set of Lebesgue measure zero. One standard proof uses convergent power series and induction on dimension: outside the lower-dimensional zero sets of a nonzero coefficient function, each one-variable slice has isolated zeros; Fubini then applies, and a countable cover by coordinate boxes finishes the argument. Apply this to (4) in E−1 independent coordinates of the simplex.

For each fixed pairing/order, its realizable set is contained in that measure-zero zero set. There are only finitely many pairings and orders of N positions. Their union is still measure zero. Thus allowing the combinatorial choice to depend measurably on the sampled lengths cannot rescue the stated construction class. A distribution with a density on the simplex assigns the union probability zero.

This applies to the scaled Dirichlet law at P=12g used in the published metric-map sampler. It does not require that the choices of tree and pairing be independent of the lengths: any joint law whose conditional length distributions are absolutely continuous within these finitely many combinatorial cases has the same conclusion.

## 5. What is and is not ruled out

The source does not impose equiangular corners. At a cubic vertex, smoothness requires only the sum of its three incident corner angles to be 2pi; their individual values may differ. A successful geometric adaptation could exploit exactly those additional variables, alter lengths, or use a different spine or polygon construction. No such possibilities are ruled out here.

The theorem also does not identify the metric-map probability law with Weil–Petersson measure or disprove any large-genus coupling under a different construction. Nor does the lack of an exact lift imply that approximate polygon closure or a controlled correction is impossible. Those are separate quantitative questions.

For N>6, a regular hyperbolic N-gon with interior angles 2pi/3 has side length 2 arcosh(2 cos(pi/N)/sqrt(3)) and hence perimeter 2N arcosh(2 cos(pi/N)/sqrt(3)). The exponential of half that nonzero side length is algebraic, so Hermite–Lindemann makes this perimeter nonalgebraic. Such a polygon does exist. Thus the conclusion is not a blanket nonexistence of equiangular polygons. The current result concerns a measure-zero constraint at every fixed algebraic perimeter, including the precise source normalization.

## 6. Exact controls and next step

The checker verifies the determinant/trace and Chebyshev recurrences symbolically, enumerates all 64 rotation choices of a labelled K_(3,3) graph as a concrete cubic-map control, and checks the 24 resulting one-face genus-two words with exact arithmetic in Q(sqrt(3)). These are structural controls, not a finite numerical proof of the measure-zero theorem. Hermite–Lindemann and analytic zero-set theory are explicit established inputs.

Author turns completed: 1/5. Original question unresolved. Subjective completion estimate: 8%. The next turn will examine the finite, algebraic-length version of the geometric obstruction and distinguish it from the continuous metric-map regime.
