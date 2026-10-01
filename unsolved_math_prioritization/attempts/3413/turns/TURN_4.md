# Turn 4: connected free-quotient completion and exact cyclic-extension tests

**Unreviewed partial; original realization classification unresolved4/5.**

Two different obstacles are addressed separately. Classical excellent-knot theory supplies a connected hyperbolic completion when the prescribed ambient action is free, without certifying the full group. In the signed case, a finite arithmetic criterion can instead rule out extra cyclic source symmetries once a hyperbolic completion exists. The signed one-component equivariant completion remains unproved. No novelty is claimed.

## 1. A classical connected-completion theorem for free ambient actions

**Theorem4.1.** Suppose a finite cyclic group G=C_m acts freely, smoothly and orientation preservingly on S3 and preserves an unlink U. There is a G-invariant knot L0, disjoint from U, for which L=L0 union U is hyperbolic. The group G preserves the orientation of L0 and injects into the full source group A_L. The action on U is unchanged. The theorem does not assert that A_L equals G.

Proof. Choose a G-invariant open tubular neighborhood N(U) and write E=S3\N(U). This connected compact oriented manifold has torus boundary (or empty boundary when U is empty). Since G is free, Q=E/G is an ordinary compact oriented three-manifold and E->Q is a connected regular covering with deck group G. Every boundary component of Q is a torus: its cover consists of tori, and the boundary orientations are preserved.

Covering monodromy gives a surjection pi_1(Q)->G. Choose an element mapping to a generator. It can be represented by a smoothly embedded knot J in the interior of Q, by general position in dimension3. Apply Myers's Theorem1.1 to this single-component J. There are no sphere or projective-plane boundary components of Q, so its boundary-intersection hypotheses are vacuous. The theorem gives a knot K homotopic to J whose exterior is excellent. A homotopy of this one-manifold keeps one circle as its domain; it does not add components. Since the monodromy class is unchanged, the full lift L0 of K to E is connected: the image of pi_1(K) is all of G.

The exterior of K has only torus boundary. Its excellence gives irreducibility, boundary incompressibility, atoroidality and absence of essential annuli, with an incompressible surface as in Myers's definition. The torus-boundary case of Thurston's hyperbolization theorem therefore supplies a complete finite-volume hyperbolic metric on its interior. Pulling that metric back to the finite covering gives such a metric on the exterior of U union L0. The original U was never changed.

The deck group acts on this hyperbolic metric by isometries, so its injection into mapping classes is faithful by Mostow rigidity (the source's Proposition3.2). Its restriction to the invariant circle L0 preserves orientation: a nonidentity orientation-reversing circle map would fix a point, contrary to freeness of the ambient action. Thus G embeds into precisely the orientation-preserving, oriented-L0 source group. QED.

This is a checked application of classical Myers/Thurston inputs, not an invocation of an unspecified equivariant hyperbolization theorem. It applies to all the free-action unlink models of Turn2. Possible extra source symmetries remain an independent issue in this unsigned case.

## 2. Why this proof does not transfer to the negative-cycle case

A negative cycle entails an involution reversing an unlink component. Its fixed axis meets that component twice, so the group action on the unlink exterior has fixed arcs. The quotient is an orbifold, not the ordinary manifold covering used in Theorem4.1. For a strongly inverted component, the quotient of its boundary torus is a sphere with four cone points of order2; its underlying topological surface is a sphere.

For clarity, the boundary quotient can be checked directly from the standard solid-torus involution (theta,z)->(-theta,conjugate(z)). Its boundary map has four fixed points. The orientation-preserving degree-two quotient surface satisfies 0=2 chi(quotient)-4, giving chi=2. The four marked points have orbifold Euler characteristic 2-4(1-1/2)=0, appropriate to a cusp cross section. Discarding their orbifold information is not harmless.

Myers's ordinary-manifold Theorem1.1 requires a proposed 1-manifold to meet every sphere boundary in at least two points. An interior closed knot meets it zero times. Thus the direct ordinary-manifold application fails in precisely this boundary situation. Nor does excellentness of the underlying space certify the required branched lift to be hyperbolic.

The published Paoluzzi–Porti Proposition1 realizes a given finite ambient group as the full symmetry group of some hyperbolic link, but its construction adds a full orbit of nontrivial asymmetric knots and an auxiliary invariant link. It neither keeps the prescribed unlink as the entire complement of one distinguished component nor controls that added invariant link to have one component. Its Theorem1 concerns the isometry group of the complement, which also need not preserve meridian slopes or extend to S3. These are not substitutes for the source target.

Their Section4 gives a useful local method: a chosen quotient knot crosses fundamental-domain faces often, its arcs are homotoped relative endpoints using Myers, and an excellent gluing lemma is applied. In that application the starting quotient knot is deliberately null-homotopic, so its lift consists of separate translates. Replacing it by a generator loop in a general singular quotient still requires a complete construction with the correct branch strata and gluing hypotheses. That step is not asserted here. In particular, no generic-decoration argument is used to declare the missing completion or exact full group solved.

## 3. Negative-cycle multiplicity bounds every larger full source group

Let a hyperbolic completion L=L0 union U contain a prescribed cyclic action H=C_m preserving ambient and L0 orientations. Suppose its signed representation has k>=1 negative cycles. Thus m is even and those cycles all have length m/2 by Turn1. Because a negative cycle has order m as a signed block, H injects into the source group even without using a metric for its original action.

Let the full source group be A_L=C_M. Since H is a subgroup, M=mq for a positive integer q. Choose a generator of A_L; its q-th power generates H. Changing a cyclic generator does not alter the signed-cycle conjugacy class, as proved in Turn1, so this loses no representation data.

The full signed representation must have a negative cycle: powers of a signed permutation whose every cycle is positive still have only positive cycle signs. By the necessary source theorem, every negative full-group cycle has length M/2=q(m/2). Taking the q-th power splits each such cycle into exactly q cycles of length m/2, and their signs remain negative. Conversely, positive full-group cycles cannot produce negative cycles in the restriction. Hence

    k=q K, where K is the number of negative full-group cycles.  (4.1)

**Theorem4.2.** The index [A_L:H]=q divides k. In particular, if the prescribed action has exactly one negative cycle, every hyperbolic completion preserving that action automatically has full source group exactly H.

This conclusion controls the source group A_L, not every isometry of the complement or every orientation-reversing symmetry. Existence of the completion is still a hypothesis.

## 4. Exact algebraic test for Turn1-compatible cyclic extensions

Let c_d be the number of positive H-cycles of length d, where necessarily d divides m. Fix q dividing k, and put M=mq. Define

    q[d] = product over primes p dividing d of p^(v_p(q)).       (4.2)

Equivalently q[d] is the largest divisor of q all of whose prime factors divide d; q[1]=1.

**Proposition4.3.** There is an abstract signed representation of C_M whose restriction to its order-m subgroup has the given signed cycle data and whose negative cycles all have length M/2 if and only if

    q[d] divides c_d for every positive cycle length d.          (4.3)

This is an exact algebraic extension criterion, not a geometric realization theorem. The assumption q divides k is part of its statement.

Proof. A positive full-group cycle of length D splits under the q-th power into s=gcd(D,q) positive cycles of length d=D/s. Therefore a group of H-cycles of common length d can arise from one full cycle exactly when

    s divides q and gcd(ds,q)=s,

or equivalently gcd(d,q/s)=1. These conditions force s to contain the full p-primary part of q for every prime p dividing d; hence q[d] divides s. Conversely s=q[d] satisfies the conditions. Every c_d is a sum of such group sizes s, so divisibility in(4.3) is necessary and sufficient: group the positive d-cycles into batches of q[d] and replace each batch by one positive cycle of length d q[d]. This length divides mq because d divides m and q[d] divides q.

For the negative cycles, group the k cycles into k/q batches of size q and replace each batch by one negative cycle of length M/2. Such a block has order M and restricts to exactly the specified q negative m/2-cycles. Combining these disjoint blocks gives a homomorphism C_M->B_n with the required restriction and with order exactly M. Signed-cycle conjugacy from Turn1 identifies its restriction with the given representation. QED.

The complete finite list of arithmetically possible indices is therefore

    { q dividing k : q[d] divides c_d for every d }.             (4.4)

It includes1. If it has no larger element, any existing hyperbolic completion has exactly the prescribed full source group. Additional geometric tests from Turn3 may rule out some algebraically possible extensions; formula(4.4) does not incorporate those tests or assert they are sufficient.

Examples:

- k=1 always gives only q=1, regardless of the positive cycles.
- For m=4, two negative2-cycles and one positive2-cycle permit only q=1. The possible proper index2 would require an even number of positive2-cycles.
- For m=6, three negative3-cycles and one positive3-cycle similarly exclude index3.
- More generally, if every prime divisor of k divides m, adding exactly one positive m-cycle to the signed data eliminates all q>1 in(4.4).
- The condition has real limits. For m=2 and k=3, q=3 remains arithmetically possible whatever the positive multiplicities: every positive length divides2 and q[d]=1. Geometry or a separate construction can still suppress an actual larger group, but the signed permutation alone does not do so through this test.

## 5. Source validation and remaining task

Myers, *Excellent1-manifolds in compact3-manifolds*, Topology Appl49(1993),115–127, DOI10.1016/0166-8641(93)90038-F: the full primary PDF was recovered from Oklahoma State's repository. Definition of excellentness, Theorem1.1 on printed116, and the gluing Lemma2.1 on118 were read. The boundary sphere/projective-plane conditions and the preservation of the chosen 1-manifold's homotopy class are exactly the inputs used above. Aitchison arXiv1008.1311 Theorem7 independently reproduces the same statement, but is not needed in place of the recovered original.

Paoluzzi–Porti, *Hyperbolic isometries versus symmetries of links*, Topology Appl156(2009),1140–1147, DOI10.1016/j.topol.2008.10.008: the full author-hosted published PDF was read at Introduction/Theorem1/Proposition1 and the Section4 gluing argument. Its results are credited and their hypotheses/output compared above; no stronger one-component relative theorem is attributed to it.

This turn establishes one classical connected-completion result in the free case and a rigorous, finite exact-group test in the signed case. It does not bridge the signed completion gap, settle every unsigned ambient pattern, or classify all source representations. Original unresolved4/5; estimated completion45%. The final substantive turn will attack the remaining equivariant one-component completion or isolate a precise validated gluing criterion without silently assuming its existence.
