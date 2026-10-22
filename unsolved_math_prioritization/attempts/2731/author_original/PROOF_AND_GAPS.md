# Equilateral polygon locking

## Outcome

Problem 2731, K3 Problem 1.72, remains unresolved in this investigation. Three substantive approaches were examined; the stopping condition is a stalled partial result, at 3 of the permitted 5 approaches. No equilateral stuck unknot and no universal unlocking theorem is claimed. These are unrefereed, AI-assisted mathematical notes. The elementary results below are not claimed to be novel.

The question concerns an embedded closed polygon in three-dimensional Euclidean space whose initial knot type is the unknot. Every individual edge must keep its length, all these lengths are equal, and the moving polygon must remain embedded throughout. The target is an embedded planar polygon, which can subsequently be convexified by the planar Carpenter's Rule theorem. The number and cyclic order of the edges remain fixed. There is no positive-thickness constraint and no added bracing. This is different from an open linkage, a polygon whose edge lengths may vary, or a diagram with immobilized crossings.

The primary K3 author version presents the question on printed pages 67–68. It attributes the question to Jason Cantarella and the write-up to Daniel Ruberman. Its discussion treats the unequal-length locked examples and the planar theorem as background, rather than answers to the equilateral spatial question [K3].

## Existing results and the precise target

Calvo's author preprint defines the unit-edge embedding space separately from the variable-edge embedding space. On PDF page 4 it states that the unit-edge hexagon space has five components: one containing the unknots and four containing trefoils. Thus an equilateral hexagonal unknot can reach a planar representative while remaining embedded and preserving its edge lengths. The text credits the earlier unknot-component result to Millett and Orellana. The complete hexagon classification is published in Calvo's 2001 paper [Calvo]. The same source attributes connectedness for n ≤ 5 to Randell, so any counterexample would require at least seven edges. Its classification of variable-edge heptagons must not be substituted for an equilateral-heptagon theorem.

The current source check located no full solution. This bounded search is not evidence of novelty or proof that no unpublished or unindexed answer exists. Two recent apparent matches concern different models: diagram crossings with imposed local rigidity [Diamantis] and simplification or re-embedding of hard unknots [CSS]. Neither supplies the needed fixed-individual-edge-length isotopy theorem.

For the remainder normalize all edge lengths to one. A polygon is an ordered cyclic list

\[
 P=(v_0,\ldots,v_{n-1}),\qquad v_i\in\mathbb R^3,
 \qquad \|v_{i+1}-v_i\|=1,
\]

with indices taken modulo \(n\). Embedded means that nonadjacent closed edges are disjoint, and adjacent closed edges meet only at their prescribed common endpoint. Collinear consecutive edges pointing forward are allowed; overlapping backtracking edges are not.

## Approach 1 Subdivision does not preserve the coarse bar constraints

One possible route to an example is to subdivide long edges of a known unequal-length locked polygon until all small bars have the same length. The obstacle is that the inserted vertices become additional free joints. A legal motion of the refined linkage need not be a motion of the original linkage.

Here is an exact example of the lost constraint. For \(0\leq r\leq 1/2\), put

\[
 c(r)=\frac{1-r^2}{1+r^2},\qquad
 s(r)=\frac{2r}{1+r^2}.
\]

Define the six vertices

\[
 (0,0,0),\ (c,0,s),\ (2c,0,0),\ (2c,1,0),\
 (c,1,-s),\ (0,1,0).
\]

**Proposition 1.** This is a continuous family of embedded unit-edge hexagons. At \(r=0\), it is a rectangle with its two length-two sides subdivided. During the motion the corresponding coarse side lengths become \(2c(r)\), so they are not preserved.

**Proof.** The identity \(c^2+s^2=1\) proves that the four slant bars have unit length; the two remaining bars have unit length because their endpoints differ by \((0,1,0)\). Throughout the parameter interval, \(c\geq 3/5>0\). The bottom two bars lie in the plane \(y=0\), the top two in \(y=1\), and within each pair the coordinate \(x\) progresses strictly between \(0,c,2c\). The other two bars lie at \(x=0\) and \(x=2c\), respectively, and have \(z=0\). Consequently nonadjacent bars do not meet and adjacent bars meet only at their shared vertex. The two coarse chords have length \(2c\), which equals \(2\) at \(r=0\) and \(6/5\) at \(r=1/2\). The family begins planar, so all its members are unknotted. ∎

This is an obstruction to a proposed proof strategy, not a counterexample to any theorem saying that every subdivision of a locked polygon unlocks. No such theorem is asserted. To transfer an unequal-length lock by subdivision, one must prove that the lock survives all added-joint motions, or devise an equilateral construction with an independent global obstruction. Proposition 1 shows why inherited coarse lengths cannot simply be assumed.

## Approach 2 Uniform flattening works for a restricted class

Write \(v_i=(p_i,z_i)\), with \(p_i\in\mathbb R^2\). Suppose the projected polygon \((p_i)\) is embedded, with nonzero projected edges, and suppose every vertical increment has the same absolute value:

\[
 |z_{i+1}-z_i|=h<1.
\]

The projection then has constant edge length \(\sqrt{1-h^2}\).

**Proposition 2.** Under these hypotheses the polygon has an explicit embedded unit-edge motion to a planar polygon.

**Proof.** For \(0\leq a\leq1\), set

\[
 L(a)=\sqrt{1-h^2+a^2h^2},\qquad
 V_i(a)=\frac{(p_i,a z_i)}{L(a)}.
\]

The original configuration is \(V(1)=P\). For every edge, the squared length before the common rescaling is \(1-h^2+a^2h^2=L(a)^2\), and \(L(a)>0\). Thus every final edge has length one. The planar projection of \(V(a)\) is the original embedded projected polygon multiplied by a positive scalar. If two spatial points on the polygon coincided, their projected points would coincide; injectivity of the projected polygon excludes this except at the prescribed shared endpoints. Thus the motion is embedded, including at \(a=0\), where it is planar. ∎

This elementary sufficient condition is not claimed to extend the known simple-projection literature. It is useful here because every point of the isotopy can be checked directly.

The same formula does not solve the general simple-projection case. If the vertical increments are \(h_i=z_{i+1}-z_i\), the squared edge lengths after flattening, before scaling, are

\[
 1-(1-a^2)h_i^2.
\]

At any \(a<1\), a common scalar can make all these lengths one only if all \(h_i^2\) are equal.

The limitation already occurs for a unit hexagon with a convex projection. Begin with

\[
 (0,0,0),(1,0,0),(1,1,0),(1,1,1),(0,1,1),(0,0,1)
\]

and apply the orthogonal matrix

\[
 R=\frac13
 \begin{pmatrix}2&2&1\\-2&1&2\\1&-2&2\end{pmatrix}.
\]

The projected successive edge directions are

\[
 (2,-2)/3,(2,1)/3,(1,2)/3,
 (-2,2)/3,(-2,-1)/3,(-1,-2)/3.
\]

They occur in strictly increasing angular order around the boundary; equivalently, the projected vertices are

\[
 (0,0),(2,-2)/3,(4,-1)/3,(5,1)/3,(3,3)/3,(1,2)/3,
\]

and each directed edge has every other vertex strictly to its left. Therefore the projection is a strictly convex hexagon. The vertical increments are

\[
 1/3,-2/3,2/3,-1/3,2/3,-2/3.
\]

At \(a=1/2\), the flattened squared edge lengths include both \(11/12\) and \(2/3\). No common rescaling preserves all six edge lengths. The original polygon is unknotted because it has an embedded projection; Calvo's result also rules out a six-edge lock. This is a failure of this particular deformation formula, not a locked example.

The unresolved step for this approach is a motion that controls unequal projected lengths while preserving closure and avoiding all collisions. A flattening argument that only preserves total length is insufficient.

## Approach 3 A finite exact problem for each fixed number of edges

The global question can be separated from a precise finite-dimensional decision problem. This gives an exact formulation and local stability facts, but does not compute the required components.

Fix \(n\geq3\), fix \(v_0=0\), and let \(X_n\) be the space of based embedded unit-edge polygons as defined above. Let \(A_n\subset X_n\) be the planar locus.

**Proposition 3.** The set \(X_n\) is a smooth semialgebraic manifold of dimension \(2n-3\). It has finitely many connected components, each path connected. The planar locus is semialgebraic. A component consists of stuck unknots precisely when its polygons are topologically unknotted and it does not meet \(A_n\).

**Proof of the smoothness assertion.** Define edge vectors \(e_i=v_{i+1}-v_i\) and constraint functions \(F_i=\|e_i\|^2-1\). Suppose a linear dependence among their differentials has coefficients \(\lambda_i\). Comparing coefficients of each free vertex \(v_j\) gives

\[
 \lambda_{j-1}e_{j-1}=\lambda_j e_j,
 \qquad j=1,\ldots,n-1.
\]

Consequently all the vectors \(\lambda_i e_i\) agree. If this common vector were nonzero, every edge would be parallel to it, so the entire closed polygon would lie in a line. No closed polygon embedded as a circle lies in a line. Hence the common vector is zero, and since each edge has length one, every \(\lambda_i\) is zero. The Jacobian has rank \(n\). The implicit function theorem gives dimension \(3(n-1)-n=2n-3\) for the unit-edge constraint set near every embedded configuration. Embeddedness is open in the vertex coordinates, so the same holds for \(X_n\).

**Proof of the semialgebraic assertions.** The unit-edge constraints are polynomial equations with rational coefficients. Parameterize edge \(i\) by

\[
 E_i(s)=v_i+s(v_{i+1}-v_i),\qquad 0\leq s\leq1.
\]

For each pair \(i<j\), require that every solution of \(E_i(s)=E_j(t)\) in the parameter square is the permitted shared endpoint: \((s,t)=(1,0)\) if \(j=i+1\); \((s,t)=(0,1)\) if \((i,j)=(0,n-1)\); and no solution for a nonadjacent pair. These are first-order formulas over the reals with rational polynomial equalities and inequalities. Real quantifier elimination shows that their conjunction is semialgebraic. Planarity is equivalent to all three-by-three determinants of the based vertex vectors vanishing. Standard semialgebraic decomposition gives finitely many connected components, path connectivity of each, and real-algebraic sample points [BPR].

A path in \(X_n\) is exactly a continuous fixed-unit-edge polygonal isotopy. Such an isotopy preserves the ordinary knot type, by isotopy extension. It reaches a planar polygon exactly when its component meets \(A_n\). Conversely, any component that meets \(A_n\) consists of unknots. This proves the stated characterization. ∎

The preceding proposition yields a finite decision procedure for each fixed \(n\): compute the semialgebraic components and test which meet \(A_n\), then decide the ordinary knot type of one sample from each remaining component. Ordinary unknot recognition is decidable [HLP]. A real-algebraic polygon can be replaced by a sufficiently close rational polygon for the latter test without requiring that the replacement retain unit edges: only its knot type is being determined. The quantitative argument below supplies the needed embedding stability.

**Embedding stability.** For a unit-edge embedded polygon, let \(\delta>0\) be the least distance between nonadjacent closed edges; use \(\delta=1\) if there are no such pairs. Let

\[
 \mu=\min_i\|e_{i-1}+e_i\|>0.
\]

Positivity of \(\mu\) excludes backtracking, which would violate embeddedness. If each vertex is changed by less than

\[
 \epsilon<\min(1/4,\delta/4,\mu/16),
\]

the straight interpolation between the original and changed vertices stays embedded. Indeed, each interpolated edge is within \(\epsilon\) pointwise of its original edge, so nonadjacent distances remain greater than \(\delta-2\epsilon>0\). Each edge vector changes by less than \(2\epsilon\), remains nonzero, and its unit direction changes by at most \(4\epsilon\). The sum of the two consecutive unit directions therefore remains nonzero because it changes by less than \(8\epsilon<\mu\). Thus adjacent edges cannot overlap. Their only common point is their common vertex. This proves the claimed isotopy. All the positive margins can be effectively bounded for real-algebraic input.

This also explains the exact limitation of configuration-space volume heuristics. Local flexibility, positive-dimensional families, or a large total volume do not establish that all unknot configurations lie in a component meeting \(A_n\). The obstruction, if it exists, is global connectivity after the self-intersection set has been removed.

**Unresolved step.** No component decomposition, cylindrical algebraic decomposition, or exhaustive fixed-\(n\) search was executed. A finite algorithm for each specified \(n\) does not bound the \(n\) required for a counterexample and does not settle the assertion for all \(n\). Enumeration of \(n\) would halt on a counterexample if one exists, but supplies no terminating negative proof. This is the stopping gap.

## Reproducibility and limits

The accompanying standard-library checker verifies exact rational samples of Proposition 1, a four-edge instance of Proposition 2, the orthogonal matrix and convex projection of the nonuniform-height hexagon, and the two unequal squared lengths after flattening. It also tests rejection of deliberately invalid configurations. These finite calculations supplement the written continuum proofs; they do not certify every point of an arbitrary isotopy, compute configuration-space components, or establish the global conjecture. The checker has explicit failure branches and behaves the same under Python optimization.

## References

- [K3] R. İnanç Baykur, Robion C. Kirby, and Daniel Ruberman, *K3 — A New Problem List in Low-Dimensional Topology*, author's preliminary version, Problem 1.72, printed pp. 67–68. https://math.berkeley.edu/sites/default/files/surv-295-ruberman-watermarked-author-pdf.pdf
- [Calvo] Jorge Alberto Calvo, *Geometric knot spaces and polygonal isotopy*, author preprint, especially PDF pp. 3–4. https://arxiv.org/abs/math/9904037. For the full hexagon classification: *The embedding space of hexagonal knots*, Topology and its Applications 112 (2001), 137–174. https://doi.org/10.1016/S0166-8641(99)00229-1
- [Diamantis] Ioannis Diamantis, *Stuck Knots: Rigidity, Invariants, and Unsticking Distance*, 2026. https://arxiv.org/abs/2602.18129
- [CSS] Jason Cantarella, Henrik Schumacher, and Clayton Shonkwiler, *Hard unknots are often easy from a different perspective*, 2026. https://arxiv.org/abs/2607.28772
- [BPR] Saugata Basu, Richard Pollack, and Marie-Françoise Roy, *Algorithms in Real Algebraic Geometry*, second edition, Springer, 2006. https://link.springer.com/book/10.1007/3-540-33099-2. For a primary component-description algorithm, see the same authors, *Computing the First Betti Number and Describing the Connected Components of Semi-algebraic Sets* (2006), https://arxiv.org/abs/math/0603248
- [HLP] Joel Hass, Jeffrey C. Lagarias, and Nicholas Pippenger, *The computational complexity of knot and link problems*, Journal of the ACM 46 (1999), 185–211. https://arxiv.org/abs/math/9807016

Primary-source retrieval and inspection date: 2026-10-06. Source documents are cited, not redistributed.
