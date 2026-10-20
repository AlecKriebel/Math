# Boundary and prime-end obstruction: queue 1820

Date: 2026-10-20 UTC. Research note only; no external publication. Target: the unrestricted transcendental-entire at-most-one completely invariant Fatou component conjecture.

## Outcome

The suggested common-boundary/no-cut-point route is valid, but produces a known necessary condition, not a contradiction: if two completely invariant Fatou components exist, their Julia set is connected **in the plane**, and its spherical compactification has no cut point. An independently proved topological lemma below verifies the potentially delicate infinity step.

There is a particularly decisive obstruction to continuing with topology alone. The corrected 2019 construction can have a full common boundary as well as two connected full preimages. Its domains necessarily lack accessible infinity and have no common point accessible from both. Thus common boundary, connectedness, and prime-end pathology are already compatible with the counterexamples to Baker's topological strategy. Full dynamical invariance remains missing.

No new dynamical sufficient condition beyond the cited compact-singular/accessibility cases, and no resolution of the conjecture, is established here.

## 1. A rigorous topological lemma

**Lemma.** Let K be a continuum in the sphere, and suppose two distinct components U,V of the sphere minus K satisfy boundary(U)=boundary(V)=K. Then K has no cut point.

**Proof.** Fix u in U and v in V. First observe that no proper compact subset L of K separates u and v. Indeed, choose q in K minus L and a connected spherical open disk B containing q and disjoint from L. Since q belongs to both boundaries, B meets both U and V. Join u to a point of U intersect B within U, join v to a point of V intersect B within V, and join these two points inside B. This gives a path avoiding L.

Suppose p is a cut point of K. Write K minus {p}=A disjoint-union B as a separation into two nonempty relatively open-and-closed sets. Their spherical closures K1 and K2 are compact, cover K, and intersect exactly at p. To see the last assertion, their only possible common closure point is p; each has p in its closure, since otherwise the corresponding side would be a nonempty proper clopen subset of the connected set K. Both K1 and K2 are proper subsets of K.

The first paragraph says neither K1 nor K2 separates u and v. Their intersection is connected. Janiszewski's separation theorem therefore says their union K does not separate u and v, contradicting the choice of distinct complementary components. This proves the lemma.

**Source for the exact Janiszewski statement:** Lasse Rempe-Gillen, *On prime ends and local connectivity*, arXiv:math/0309022, PDF p. 6, “Separation theorems and preliminaries”: the statement is for compact subsets of the sphere with connected intersection and separation of a specified pair of points. https://arxiv.org/pdf/math/0309022 . The argument above is an independent application, not a quotation or a reliance on an accessibility assumption.

## 2. Application to two completely invariant Fatou components

Assume f is transcendental entire and U,V are distinct completely invariant Fatou components.

1. Each is invariant and hence simply connected by the standard periodic-component theorem for entire maps.
2. Each is unbounded. Choose a value w in U that is not a Picard exceptional value. It has preimages of arbitrarily large modulus, and all belong to U by complete invariance. The same applies to V.
3. The planar boundary of either component is J(f). For example, choose a nonexceptional w in U. Its iterated backward orbit is contained in U and accumulates on every Julia point, so J(f) is contained in the closure of U. Conversely, the boundary of a Fatou component is contained in J(f).
4. Consequently the spherical boundary of each is K=J(f) union {infinity}. The boundary of a simply connected spherical domain is connected, so K is a continuum. U and V are distinct complementary domains of K.
5. Apply the lemma at p=infinity. It follows that K minus {infinity}=J(f) is connected in the plane.

The lemma also rules out every finite spherical cut point of K. Do **not** strengthen this to “J(f) has no finite cut point”: deleting both infinity and a finite point is a two-point removal, and the lemma does not control that operation.

This necessary condition is not new. Bergweiler–Eremenko, *Meromorphic functions with two completely invariant domains*, arXiv:math/0310495v2, Lemma 1, PDF p. 2, explicitly records planar connectedness for the meromorphic case, citing Baker–Kotus–Lü. https://arxiv.org/pdf/math/0310495 . The independent proof above avoids relying on that paper's separately outdated introductory claims about Baker's entire-function theorem.

## 3. A direct obstruction to upgrading topology to accessibility

Rempe-Gillen–Sixsmith, *On Connected Preimages of Simply-Connected Domains Under Entire Functions*, arXiv:1801.06359v3, Theorem 1.11 and Observation 4.5, construct disjoint simply connected domains U,V with connected full preimages and equal planar boundaries. Section 5 applies the construction to f(z)=exp(z)+z. Remark 1.13 states the common-boundary extension explicitly. https://arxiv.org/pdf/1801.06359

The following consequences are deductions from those results, not additional claims of complete invariance:

- These examples can be taken unbounded: their domains contain infinitely many critical values from the discrete unbounded set {(2m+1)pi i - 1 : m is an integer}.
- Put L=boundary(U)=boundary(V). The spherical boundary K=L union {infinity} is a continuum. Each domain is a complementary component of K, because it is connected, open, and has no boundary outside K. The lemma applies. Hence L is connected and K has no cut point.
- By Theorem 1.3(f), infinity is inaccessible from either U or V. Otherwise the other full preimage would be disconnected.
- By Theorem 1.3(e), no common finite boundary point is accessible from both domains.

Thus even the following collection does not force a contradiction: entire map; disjoint simply connected unbounded domains; connected full preimages; equal connected planar boundaries; no spherical cut points; inaccessible infinity on both sides; and disjoint sets of accessible boundary points. What the examples do not supply is f^{-1}(U)=U, f^{-1}(V)=V, and maximal Fatou-component status.

In particular, density of accessible boundary points on each side does not prove a point accessible from both: two dense subsets can be disjoint, and these constructed domains witness the relevant geometric possibility. Passing to prime ends does not fix this. A boundary point may belong to a nontrivial impression without being the landing point of an access. No trivial impression at infinity follows from the common-boundary lemma.

## 4. Singular-value accumulation: a necessary dichotomy, not a solution

Let S(f) denote the closed set of finite singular values. Under the hypothetical two-component assumption, Theorem 1.3(b) forces S(f) intersect U not to be compactly contained in U, and similarly for V. Consequently, for each component, either:

- singular values in that component escape every bounded subset of the plane; or
- they have a finite accumulation point on the common Julia boundary.

For completeness, if S(f) intersect U is bounded, its closure is compact in the plane. If this closure avoided boundary(U), it would be a compact subset of U, contradicting the stated necessary failure of compact containment. Closedness of S(f) puts any such boundary limit in S(f) intersect J(f).

Thus in class B, both components must have singular values accumulating on their Julia boundary. There is no reason supplied here that the two sets of limit points coincide, that either contains an accessible point, or that singular values can be enclosed by a compact curve inside its basin. Such an enclosure would simply reintroduce the compact-singular hypothesis already known to suffice.

Attracting dynamics alone does not supply that enclosure: local uniform convergence of iterates is uniform only on compact subsets of a basin, whereas precisely the singular values approaching its boundary are outside every such compact exhaustion. An argument upgrading this to uniform control on all singular values would need an additional hypothesis or a new theorem.

## 5. What would be needed next

A successful continuation must use iteration in a way absent from the 2019 common-boundary examples, for example a proved result forcing an access or controlled singular-value enclosure from complete invariance plus attracting/parabolic dynamics. None has been established in this note. Reasserting connectedness of J(f), applying Janiszewski again, or appealing to dense accessible points does not close that gap.

## Inspection record

- Reviewed the public-source context summarized in SOURCES.md and the 2019 author preprint.
- Inspected 2019 Remark 1.13, Observation 4.5, its construction argument, Section 5's exp(z)+z example, and Theorem 1.3(e),(f),(b).
- Opened the primary arXiv papers on prime ends and meromorphic completely invariant domains; checked the exact Janiszewski statement and Lemma 1 respectively.
- This note makes no claim of a new theorem settling the problem.
