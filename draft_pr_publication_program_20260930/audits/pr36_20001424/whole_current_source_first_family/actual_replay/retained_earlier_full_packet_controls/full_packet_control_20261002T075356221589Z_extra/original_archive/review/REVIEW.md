# Independent review: PCF field-of-moduli counterexample, 20001424

**Verdict: PASS for the proposed full negative answer to the canonical question.** The specified plane graph gives a degree-11 critically fixed rational-map class over the algebraic numbers, with trivial holomorphic automorphism group, real field of moduli, and no real model. No fatal mathematical gap was identified.

This is an independent adversarial AI review, not a formal proof certificate or a historical novelty finding. Reviewed on 2026-09-30 using GPT-6 Astra at xhigh reasoning.

Frozen CANDIDATE.md SHA-256:

aa598dc779b4115c9a7522335b364a5d9dcddf11ceec707fd46943984e8ffabf

The candidate can remain unchanged. Section 6 below makes explicit one standard implication concerning algebraic conjugators that is implicit in its final field-of-moduli step.

## 1. Target and source scope

The pinned canonical AIM problem is the unqualified question:

> Are all PCF maps defined over their field of moduli?

It concerns conjugacy classes of rational self-maps of the projective line, with conjugacy by a single projective linear coordinate change. The odd-cardinality condition in the imported title belongs to the earlier partial criterion, not to the original question. The proposed example has ten reduced postcritical points and therefore does not contradict that odd-divisor criterion.

**Source-access limitation:** I independently retried both HTTP and HTTPS versions of the AIM problem-list page, as well as its parent page; they returned errors. Thus the exact wording above was checked against the user-authorized pinned canonical record and its preserved original statement, not a newly recovered live copy. The official workshop announcement and report were accessible and confirm the rational-map, Möbius-conjugacy and rigidity context. The candidate's source audit already discloses this limitation accurately. [Official 2014 announcement](https://aimath.org/pastworkshops/finitedynamics.html), [official workshop report](https://aimath.org/pastworkshops/finitedynamicsrep.pdf)

An algebraic counterexample in degree eleven suffices to disprove the universal question. The proof need not compute its coefficient field or its exact field of moduli, and it does not claim either. The graph specifies one Möbius class through an established injective realization correspondence, so this is an exact existence construction rather than an unresolved search for a rational map with a desired portrait.

## 2. Established inputs and their hypotheses

I read Hlushchanka's current version, especially Theorem 2, the orientation convention in Section 2, Corollary 6 and Section 5. The classification is for connected loopless plane graphs with at least one edge; multiple edges are allowed. Graph isomorphisms are induced by orientation-preserving sphere homeomorphisms. The blow-up realization has degree one plus the number of edges and critical local degree one plus the vertex valence. Its inverse uses the fixed internal rays, with one charge edge chosen in each complementary Tischler face. These faces have exactly two distinct critical boundary points; all charge graphs are connected. The candidate's graph satisfies these hypotheses. [Hlushchanka, Theorem 2 and Section 5](https://arxiv.org/pdf/1904.04759v2)

The published Hlushchanka–Prochorov paper also explicitly describes the charge graph as unique up to isotopy relative to the critical set, and recalls the connected-graph realization. Its March 2026 publication metadata was independently verified. [Proceedings of the London Mathematical Society 132, e70129](https://londmathsoc.onlinelibrary.wiley.com/doi/full/10.1112/plms.70129)

The real-model/reflection criterion is consistent with Hidalgo–Quispe's Lemma 4, and the trivial-automorphism case with an imaginary reflection is their Theorem 6. The candidate supplies the needed elementary argument instead of relying on a broader unproved descent assertion. [Hidalgo–Quispe, Sections 2.1, 2.5 and 4.2](https://arxiv.org/pdf/1502.05306v4)

## 3. Exact graph and symmetry audit

The graph has four cycle vertices, four leaves, and two intermediate pendant vertices. There are ten edges and ten vertices, and its cycle rank is one. The unique cycle is the four-cycle; its attached path lengths are \(1,2,1,2\).

Every abstract automorphism must preserve this cycle and these lengths. The only possible actions on the cycle are the identity, the half-turn, and the two reflections preserving the length pattern. Each action uniquely determines the images of every pendant vertex. An independent adjacency-preserving backtracking search confirms that these are exactly the four automorphisms.

I derived the rotation system from the actual rational coordinates and exact tangent vectors, rather than reading the candidate's rotation data into the checker. At a cycle vertex \(v\), the forward cycle tangent is \(iv\), the backward tangent is \(-iv\), and the pendant tangent is inward for the first two roots and outward for the last two. Exact angular ordering gives precisely the displayed cyclic orders.

The four orientation-sign lists at the trivalent vertices are
\[
(+,+,+,+),\quad(-,+,-,+),\quad(+,-,+,-),\quad(-,-,-,-).
\]
A sphere homeomorphism has one global orientation sign. Hence only the identity can be induced by an orientation-preserving homeomorphism of this embedded graph, and only the half-turn \(h\) by an orientation-reversing one. The mixed-sign abstract reflections cannot occur.

The latter action is genuinely realized, not merely combinatorially permissible:
\[
J(z)=-1/\overline z
\]
maps the specified coordinates, quarter-circle edges, and radial pendant edges to their prescribed partners. It exchanges interior and exterior. It is an involution with no fixed point on the sphere: a finite nonzero fixed point would satisfy \(|z|^2=-1\), while zero and infinity are exchanged. Its action fixes neither a graph vertex nor an edge setwise. The two complementary faces are exchanged.

The distinction between the abstract graph and the embedding is essential. An independent negative control placing all four pendants on the same side gives two positive and two negative symmetries, including reflections with fixed vertices. Thus ignoring the inside/outside decoration would invalidate the argument; the actual candidate keeps it.

Realization now gives degree eleven and local degrees
\[
2,2,2,2,\quad 3,3,\quad 4,4,4,4.
\]
Their ramification sum is twenty, equal to \(2\cdot11-2\). There are ten distinct critical points, all fixed, so the reduced postcritical set has size ten. No point has local degree eleven, which excludes a polynomial representative.

## 4. Naturality and the automorphism group

The proof does not infer equivariance from an arbitrary bijection of isomorphism classes. The actual inverse construction supplies the needed naturality.

A Möbius transformation commuting with \(f\) carries a critical immediate basin to a critical immediate basin of the same local degree. In Böttcher coordinates the induced disk automorphism fixes zero, so it is a rotation. Commutation with \(z\mapsto z^m\) restricts the rotation to an \((m-1)\)-st root of unity. It consequently permutes all fixed internal rays, including their landing points. An antiholomorphic commuting map similarly becomes a disk anti-rotation and has the same permutation property.

Therefore every holomorphic or antiholomorphic dynamical automorphism acts on the intrinsic Tischler graph and its complementary faces. A face determines the endpoints of its charge edge. At a critical vertex, the cyclic order of the charge edges is the order of the incident face sectors. This incidence-and-rotation information is independent of the actual arcs chosen inside the faces.

This gives a well-defined combinatorial action on any charge graph class, preserving or reversing all cyclic orders according to the ambient orientation. There is no assertion that every graph automorphism automatically lifts to a dynamical automorphism. Only the necessary action of an already existing automorphism is used.

For the graph at hand, a holomorphic automorphism must induce the identity. It thus fixes every critical point and, in particular, three distinct points of the sphere. It is the identity Möbius transformation. Hence \(\operatorname{Aut}(f)=1\).

Complex conjugation carries the actual fixed rays of \(f\) to those of \(\overline f\), and carries its charge graph class to the mirror class. Since \(J\) reverses orientation and preserves \(G\), \(cJ\) is an orientation-preserving isomorphism from \(G\) to \(cG\). Classification gives a Möbius conjugacy
\[
\overline f=L f L^{-1}.
\]
Consequently \(A=L^{-1}c\) commutes with \(f\). It is antiholomorphic and must induce the unique negative graph action \(h\).

The square \(A^2\) is a holomorphic dynamical automorphism, hence is identity. Any two antiholomorphic commuting transformations differ by a holomorphic one, so \(A\) is unique. This establishes the involution property before the equivariant arc choices are made; the dependency is not circular.

## 5. Actual equivariant graph and exclusion of a real model

This part closes the main potential gap.

Charge edges correspond to Tischler faces. The action \(h\) has no setwise-fixed charge edge, so \(A\) has no fixed Tischler face. In this example the charge graph is simple, so even its endpoint action alone identifies each edge unambiguously. The ten Tischler faces therefore form five pairs.

For a pair \(Q,A(Q)\), choose a charge arc in one face and its actual image under \(A\) in the other. Because \(A^2=1\), the choices are consistent. Distinct face interiors are disjoint, and each arc has the required two critical endpoints, so their union is a charge graph in the sense of the source. It is connected by the charge-graph theorem. The choices can be taken as tame arcs in the indicated face sectors; the resulting rotation data are the prescribed ones.

This graph is setwise \(A\)-invariant. It contains no fixed point of \(A\): no vertex is fixed, and a fixed point in an edge interior would belong to two distinct edge interiors, which is impossible.

If \(A\) had a fixed point, an antiholomorphic Möbius involution of that type is conjugate to complex conjugation. Its fixed circle separates the sphere into two components that it interchanges. A nonempty connected invariant graph disjoint from that circle cannot exist: connectedness puts the graph in one component, and invariance would put it in the other. Therefore \(A\) is fixed-point-free.

Finally, a real representative \(g=MfM^{-1}\) would make \(M^{-1}cM\) a reflecting antiholomorphic dynamical automorphism of \(f\). It would have to equal \(A\), contradicting fixed-point-freeness. Thus the class has no real model.

An isotopy class by itself would not prove the assertion about the fixed circle. The candidate explicitly constructs the actual invariant graph needed for that assertion.

## 6. Algebraicity and the absolute field of moduli

The passage from a complex realized class to an algebraic representative is valid.

There are finitely many connected loopless plane graphs with ten edges up to planar isomorphism. Indeed, connectedness bounds the number of vertices by eleven, the edge multiplicities are bounded by ten, and a finite graph has only finitely many rotation systems. Classification therefore gives finitely many degree-eleven critically fixed Möbius classes.

Normalize any ordered triple of distinct critical points to \(0,1,\infty\). Each class gives finitely many normalized maps: there are finitely many such triples, and the normalizing Möbius transformation for a specified triple is unique. The candidate class has ten critical points, so this normalization is available.

In homogeneous coordinates, take the binary ramification form \(W_f\) and fixed-point form \(H_f=YF-XG\). Their degrees are twenty and twelve. On the nonzero-resultant characteristic-zero locus, \(W_f\) is nonzero, and the critical-fixed condition is equivalent to the support of \(W_f\) lying in the zero set of \(H_f\). Thus
\[
W_f\mid H_f^{20}
\]
is sufficient and necessary: every root multiplicity of \(W_f\) is at most twenty, while every root of \(H_f\) acquires multiplicity at least twenty in that power.

The divisibility relation can be expressed by polynomial coefficient equations with an auxiliary homogeneous quotient of degree 220. Its projection is constructible over \(\mathbb Q\); resultant nonvanishing and the three critical-point conditions are also defined over \(\mathbb Q\). On each projective coefficient chart this gives a finite constructible set defined over \(\mathbb Q\). Its points have algebraic coordinates. This proves existence of a representative in \(\overline{\mathbb Q}(z)\). Rational coordinates in a drawing of the graph play no role in this argument.

There is no flexible-Lattès issue. The graph finiteness proof already suffices. Alternatively, the ten fixed critical points all have infinite orbifold weights, so the orbifold Euler characteristic is \(2-10<0\).

**Explicit algebraic-conjugator clarification.** After the algebraic representative is selected, both \(f\) and \(\overline f\) have algebraic critical points. Any complex Möbius conjugator between them maps an ordered triple of distinct critical points to another such algebraic triple. The unique Möbius transformation carrying one algebraic triple to the other has coefficients in \(\overline{\mathbb Q}\). Thus the complex conjugacy supplied above is also a conjugacy over \(\overline{\mathbb Q}\), as needed for the absolute Galois stabilizer. This elementary implication is implicit in the candidate and is made explicit here.

Let \(E\) be a number field containing the coefficients. The stabilizer of the algebraic conjugacy class contains \(\operatorname{Gal}(\overline{\mathbb Q}/E)\), an open subgroup, so it is itself open and its fixed field \(K\) is a number field. Complex conjugation belongs to this stabilizer. Hence \(K\) lies in \(\mathbb R\) in the chosen embedding. This does not assert that \(K\) is totally real.

A representative over \(K\) would then be a representative over \(\mathbb R\), already ruled out. Therefore \(K\) is not a field of definition. No computation of \(K\), quaternion algebra, or explicit coefficient list is missing from this implication.

## 7. Independent diagnostics

The original graph verifier was replayed separately and reproduced its receipt byte for byte. All source hashes in the supplied manifest were also checked.

The independent standard-library checker does not load the candidate's rotation data. It derives local orders from exact rational coordinates and quarter-circle tangent vectors, exhausts adjacency-compatible vertex bijections by backtracking, and independently computes the face permutation. It then constructs the corner-labeled radial incidence graph, retaining bridge multiplicities, and verifies the pairing of its quadrilateral faces.

All **183 exact assertions pass**, including:

- Four abstract automorphisms, only one of each global orientation type
- Exact coordinate action of the antipodal involution and no fixed vertex or edge
- Two primal faces of boundary length ten, exchanged by the involution
- Twelve radial vertices, twenty edges with multiplicity, and ten paired faces
- The critical-degree and ramification counts
- A negative embedding control that restores reflections if all pendants are placed on the same side

These are finite graph diagnostics. They do not numerically construct or approximate the rational map, and they do not replace the realization, naturality, algebraicity or descent arguments.

Reproduce the independent receipt from the review directory with:

    python independent_checks.py > independent_results.json

The review deliverables are REVIEW.md, review_summary.json, independent_checks.py and independent_results.json. Reference images and the author's replay directory are not publication deliverables.

## 8. Prior work and limits of this verdict

Silverman's descent theorems cover even-degree classes and polynomial classes. This odd-degree nonpolynomial example is consistent with them; the known odd canonical-divisor mechanism is also consistent with its even postcritical cardinality. [Silverman, Theorems 2.1 and 5.1](https://www.numdam.org/item/CM_1995__98_3_269_0/)

The candidate correctly does not use the withdrawn Bresciani preprint as an established theorem. Its arXiv withdrawal notice explicitly identifies a gap confusing ramification degrees with vanishing orders. [Withdrawal notice](https://arxiv.org/abs/2405.03612)

Pseudo-real rational maps, antipodal dynamics, and postcritically finite centers in antipode-preserving cubic families are prior work. The bounded search did not verify a prior occurrence of this precise decorated graph or this precise counterexample statement, but it cannot establish historical novelty or minimal degree. In particular, the existing cubic families must not be dismissed as irrelevant merely because the present example has degree eleven. [Bonifant–Buff–Milnor](https://arxiv.org/abs/1512.01850)

The mathematical conclusion of the frozen candidate passes: a graph-defined algebraic PCF class has field of moduli contained in the reals and no real model, so not every PCF class is defined over its field of moduli. The precise number field, explicit coefficients, smallest possible degree, and novelty remain unclaimed.
