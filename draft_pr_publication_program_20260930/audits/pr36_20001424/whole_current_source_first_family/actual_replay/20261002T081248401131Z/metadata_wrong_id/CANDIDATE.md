# 20001424: a graph-defined PCF counterexample to descent

**Status: candidate counterexample awaiting independent adversarial review. No claim of historical novelty or independently verified resolution is made yet.**

## 1. Exact proposed conclusion

There exists a degree-11 rational map \(f\in\overline{\mathbb Q}(z)\) with the following properties:

1. Every critical point of \(f\) is fixed, so \(f\) is postcritically finite.
2. Its holomorphic dynamical automorphism group is trivial.
3. Its conjugacy class is fixed by complex conjugation, but no map in that class has real coefficients.
4. Consequently its absolute field of moduli \(K\) is a real number field and is **not** a field of definition.

Here conjugacy means \(\operatorname{PGL}_2\)-conjugacy of self-maps, not independent coordinate changes on the source and target. The characteristic is zero. A graph plus a standard realization theorem defines the class exactly; coefficients and the precise number field \(K\) are not computed. Neither is needed for the proposed non-descent proof.

This is intended as a negative answer to the original question, “Are all PCF maps defined over their field of moduli?” The extra odd-postcritical-divisor condition in the imported record's title is part of prior partial work, not an assumption in the original question. Our example has ten reduced postcritical points and does not contradict that condition.

## 2. Established input and its precise use

We use Hlushchanka, [*Tischler graphs of critically fixed rational maps and their applications*](https://arxiv.org/abs/1904.04759), Theorem2, Section5, Corollary6, and Lemma7. These provide a bijection between orientation-preserving isomorphism classes of connected loopless plane graphs and Möbius classes of critically fixed rational maps. A graph with \(e\) edges gives degree \(e+1\); a vertex of valence \(m\) gives a fixed critical point of local degree \(m+1\).

The intrinsic Tischler graph consists of all fixed internal rays. Charge edges are chosen inside its complementary faces, joining the two critical boundary points. Any such choice gives the same embedded graph class; the charge graph is connected. Section5 gives the relevant realization and inverse constructions, not merely an abstract counting correspondence.

The known criterion that a rational map admits a real model exactly when it has an antiholomorphic reflection is also discussed by Hidalgo–Quispe, [*On Real and Pseudo-Real Rational Maps*](https://arxiv.org/abs/1502.05306), Lemma4. We give the elementary direction needed below. General pseudo-real maps and antipode-preserving families are prior work; this construction does not claim those ideas as new.

## 3. An exact embedded graph

Let the four cycle vertices, in counterclockwise order on the unit circle, be

\[
v_0=1,\qquad v_1=i,\qquad v_2=-1,\qquad v_3=-i.
\]

The four cycle edges are the successive quarter-circle arcs. Attach the following radial pendant paths:

\[
v_0-\tfrac12,\qquad
v_1-\tfrac i2-\tfrac i3,\qquad
v_2-(-2),\qquad
v_3-(-2i)-(-3i).
\tag{1}
\]

The first two paths lie inside the unit circle and the last two outside. Their interiors are disjoint from each other and the cycle. Thus \(G\) is a connected simple plane graph with ten vertices, ten edges, two faces, and a unique cycle of length four. Its pendant lengths around the cycle are \((1,2,1,2)\).

The map

\[
J(z)=-1/\overline z
\tag{2}
\]

preserves \(G\), swaps \(v_j\) with \(v_{j+2}\), and pairs opposite pendant paths. It has no fixed point on the sphere, no fixed graph vertex, and no setwise-fixed edge. It reverses orientation and exchanges the two complementary faces.

Equivalently, a complete combinatorial specification is the edge list and cyclic-order data in `graph_verification.json`. With \(a_j\) denoting the first pendant edge, \(e_j^+\) the next cycle edge, and \(e_j^-\) the preceding edge, the counterclockwise order is

\[
(e_j^-,e_j^+,a_j)\quad(j=0,1),
\qquad
(e_j^-,a_j,e_j^+)\quad(j=2,3).
\tag{3}
\]

A [diagram of this embedding](graph.svg) is included for orientation; the exact coordinates and cyclic orders above are the definition.

## 4. All graph automorphisms and their orientation types

Every abstract automorphism preserves the unique cycle and the lengths of its attached paths. Its restriction to the cycle is therefore one of exactly four permutations:

\[
\mathrm{id},\qquad h:j\mapsto j+2,\qquad
s_0:j\mapsto-j,\qquad s_2:j\mapsto2-j
\quad(\bmod4).
\tag{4}
\]

Each uniquely extends along the pendant paths. To see completeness, any automorphism of the four-cycle is dihedral, and preserving the alternating distinct lengths requires preserving the parity of \(j\). This leaves precisely (4).

An orientation-preserving homeomorphism of the sphere must preserve the cyclic order at every valence-three vertex; an orientation-reversing one must reverse it at every such vertex. From (3):

- identity preserves all four orders;
- \(h\) reverses all four orders;
- \(s_0\) reverses at \(v_0,v_2\) and preserves at \(v_1,v_3\);
- \(s_2\) does the opposite.

The last two therefore cannot be induced by any sphere homeomorphism preserving the embedded graph. It follows that the only orientation-preserving embedded graph automorphism is identity and the only orientation-reversing one is \(h\), realized by (2). These statements concern induced permutations, not arbitrary homeomorphisms supported away from the graph.

The checker independently exhausts all \(4!\,2!\,4!=1152\) degree-compatible vertex permutations, finding exactly these four abstract automorphisms and their cyclic-order signs.

## 5. Realization and naturality under complex conjugation

Let \([f]\) be the Möbius class corresponding to \(G\) by the established classification. Then

\[
\deg f=11,\qquad
\#\operatorname{Crit}(f)=10,
\]

and its critical local degrees are four copies of 2, two copies of 3, and four copies of 4. All ten critical points are fixed. Their ramification multiplicities sum to

\[
4(2-1)+2(3-1)+4(4-1)=20=2\deg f-2.
\]

No critical point is totally ramified, so this conjugacy class contains no polynomial.

Write \(c(z)=\overline z\) and \(\overline f=c\circ f\circ c\). Conjugating an immediate basin and its fixed internal rays by \(c\) gives exactly the corresponding basin and rays of \(\overline f\). Thus

\[
\operatorname{Tisch}(\overline f)=c(\operatorname{Tisch}(f)),
\]

and a charge graph for \(\overline f\) is the mirror image of a charge graph for \(f\).
Since \(J\) reverses orientation and preserves \(G\), the map \(cJ\) gives an orientation-preserving isomorphism from \(G\) to its mirror. The classification therefore gives a Möbius map \(L\) with

\[
\overline f=L f L^{-1}.
\]

Consequently

\[
A=L^{-1}c
\tag{5}
\]

is an antiholomorphic automorphism commuting with \(f\).

This step uses the naturality of the actual fixed-ray construction. An arbitrary bijection between two sets of isomorphism classes would not suffice.

## 6. Triviality of the holomorphic automorphism group

A Möbius transformation commuting with \(f\) permutes its critical immediate basins and their fixed internal rays. Hence it acts on the intrinsic Tischler graph, its faces, and the associated charge vertices and edges. In Böttcher coordinates a commuting basin isomorphism is a rotation commuting with a monomial; an antiholomorphic one is an anti-rotation. Both carry its fixed radial rays to fixed radial rays. Charge edges correspond to Tischler faces, and their cyclic order at a critical vertex is the order of the incident face sectors. Thus their induced incidence and cyclic-order action does not depend on the chosen arcs. The cyclic order on the resulting charge graph is preserved. Although individual charge arcs are chosen rather than intrinsic, their incidence and cyclic-order data are determined by the Tischler faces, so this induced combinatorial action is well defined.

By Section4 the induced permutation of the charge graph is identity. In particular the transformation fixes all ten critical points. A Möbius transformation fixing three distinct points is identity. Thus

\[
\operatorname{Aut}(f)=1.
\tag{6}
\]

An antiholomorphic automorphism similarly induces a uniformly orientation-reversing action, so it must induce \(h\). In particular it fixes no critical point and no charge edge. Since the square of (5) is holomorphic and commutes with \(f\), equation (6) gives \(A^2=1\). Any other antiholomorphic automorphism would differ from \(A\) by a holomorphic one, so \(A\) is unique.

## 7. An actual invariant graph excludes a reflecting circle

It is not enough to know only an isotopy class of graphs here. We now construct an actual \(A\)-invariant charge graph.

The intrinsic Tischler graph is \(A\)-invariant. Its complementary faces are in bijection with charge edges. The action induced on charge edges is \(h\), which has no setwise-fixed edge. Therefore these Tischler faces are paired without fixed faces.

For each paired pair \(Q,A(Q)\), choose one charge arc \(\gamma_Q\) in \(Q\), joining its two critical boundary points, and choose \(A(\gamma_Q)\) as the charge arc in \(A(Q)\). Since \(A^2=1\), these choices define a consistent \(A\)-invariant charge graph \(G_A\). Arcs in different open faces have disjoint interiors. By the charge-graph theorem, \(G_A\) is connected and belongs to the prescribed graph class. No vertex is fixed by \(A\), and every edge is carried to a different edge; hence no point of \(G_A\) is fixed.

If \(A\) were an antiholomorphic reflection, its fixed set would be a circle separating the sphere into two disks exchanged by \(A\). A connected nonempty invariant graph disjoint from that circle would have to lie in one disk, while its image lies in the other. This is impossible. Thus \(A\) is a fixed-point-free antiholomorphic involution, rather than a reflection.

Now suppose \(f\) had a real model \(g=M f M^{-1}\in\mathbb R(z)\). The transformation \(M^{-1}cM\) would be an antiholomorphic reflection commuting with \(f\), contradicting uniqueness of \(A\) and the preceding paragraph. Therefore

\[
[f]\text{ has no real model.}
\tag{7}
\]

## 8. Algebraicity, with no flexible-Lattès assumption hidden

For a fixed degree there are only finitely many critically fixed Möbius classes. This follows either from the finite plane-graph classification or from Thurston rigidity; in our case there are ten periodic critical points and the orbifold is hyperbolic, so no flexible-Lattès exception is relevant.

Choose three distinct critical points and normalize them to \(0,1,\infty\). There are only finitely many resulting normalized degree-11 critically fixed maps: finitely many conjugacy classes, and finitely many ordered triples of distinct critical points in each class. A Möbius map sending a specified ordered triple to \(0,1,\infty\) is unique.

The condition of being critically fixed and the normalization that \(0,1,\infty\) are critical are algebraic conditions over \(\mathbb Q\). For example, in homogeneous coordinates let \(W_f\) be the ramification form and let \(H_f(X,Y)=YF(X,Y)-XG(X,Y)\) be the fixed-point form. The condition that every zero of \(W_f\) is fixed is the algebraic divisibility condition

\[
W_f\mid H_f^{20},
\]

on the resultant-nonzero degree-11 locus. It can be expressed by introducing the coefficients of the quotient and then eliminating them. The three normalization conditions are algebraic as well. Thus the finite normalized locus is a constructible locus over \(\mathbb Q\); all its complex points have algebraic coordinates.

Equivalently, every automorphism of \(\mathbb C\) over \(\mathbb Q\) permutes the finite normalized set, so each coefficient, after fixing a nonzero projective coefficient to 1, has finite orbit and is algebraic. Hence the class has a representative

\[
f\in\overline{\mathbb Q}(z).
\tag{8}
\]

These statements concern the rational map obtained by realization, not the rational coordinates used to draw the original graph. Graph coordinates alone would not prove (8).

## 9. The absolute field of moduli does not define the map

For the algebraic representative in (8), let

\[
K=\overline{\mathbb Q}^{\{\sigma\in\operatorname{Gal}(\overline{\mathbb Q}/\mathbb Q):
[{}^\sigma f]=[f]\}}.
\]

This is a number field: a finite field containing the coefficients of \(f\) is a field of definition, so the stabilizer contains an open subgroup and its fixed field is finite over \(\mathbb Q\). Complex conjugation lies in this stabilizer by Section5. Therefore \(K\subset\mathbb R\) in the chosen embedding.

If \(K\) were a field of definition, a representative in \(K(z)\) would also be a real representative. This contradicts (7). Thus the PCF class is not defined over its field of moduli.

## 10. What is and is not certified by the computation

`verify_graph.py` uses only Python's standard library and exact combinatorics. It checks all abstract automorphisms, their local orientation signs, the fixed-point-free edge/vertex action, the face cycles and Euler characteristic, the radial/Tischler incidence model, and the degree/ramification counts. It does not numerically approximate \(f\), check an approximate critical orbit, or replace the realization, naturality, and algebraicity proofs.

The proof depends on established graph realization and classification theorems and elementary descent logic. Independent review must challenge especially the induced symmetry action through the intrinsic Tischler graph, the equivariant choice of charge arcs, and the finite normalized algebraic locus. The exact field \(K\), explicit coefficients of \(f\), minimal counterexample degree, and historical novelty are not established by this package.
