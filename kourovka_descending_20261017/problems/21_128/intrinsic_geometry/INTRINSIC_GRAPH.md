# A graph and a spectrum that really survive finite-index passage

Research lemma, 2026-10-24. These constructions do **not** recognize Artin
parabolics and do **not** settle 21.128. No originality claim is made.

For any group G, let R(G) be the set of internal commensurability classes of
infinite cyclic subgroups. Two infinite cyclic groups represent the same vertex
exactly when they have a common finite-index infinite cyclic subgroup. Give two
distinct vertices an edge when representatives have nonzero powers that commute
and generate a copy of Z^2. The generating-Z^2 clause is automatic for distinct
vertices once the powers commute: any nontrivial integral relation would make
the original cyclic groups commensurable. Defining it explicitly also covers
ambient groups with torsion without any root assumption.

This is well-defined. Replacing either cyclic representative by a commensurable
one allows passage to a common finite-index cyclic subgroup, and taking further
powers preserves commutation and rank two.

**Finite-index lemma.** If H has finite index in G, inclusion induces a graph
isomorphism R(H) -> R(G).

Every infinite cyclic subgroup C of G has C intersect H of finite index in C, so
surjectivity holds. Two cyclic subgroups of H are internally commensurable in H
if and only if they are so in G: their intersection is the same actual subgroup,
and the relevant indices are unchanged. This proves injectivity. Edges persist
under inclusion. Conversely, take powers witnessing an edge in G and then
further nonzero powers lying in H. They still generate Z^2. This proves reflection
of edges. Any abstract isomorphism H -> K induces a graph isomorphism as well.
Consequently abstract commensurability of G and G' forces isomorphic graphs.

There is useful additional decoration. For an infinite-order g define

    SC_G(g) = union_{m >= 1} C_G(g^m).

It is a subgroup by the least-common-multiple argument. It is unchanged under
nonzero powers or a change of cyclic representative within the same vertex.
If g^r belongs to H, then

    SC_H(g^r) = H intersect SC_G(g),

which has finite index in SC_G(g). Thus a vertex can be decorated by the abstract
commensurability class of SC_G(g). It can also be decorated by the class of
SC_G(g)/VZ(SC_G(g)), where VZ denotes the virtual center, because for any
finite-index L <= J we have VZ(L)=L intersect VZ(J). These decorations are carried
by every finite-index isomorphism. This is a **set/graph** assertion; raw
multiplicity of selected conjugacy classes is not asserted invariant.

For the groups at issue, Q_T is biorderable: Marin (2007), Theorem3, proves
biorderability of the pure groups, and the genuine split P_T=Q_T x Z embeds
Q_T in P_T. Soroko, arXiv:2009.10471v4, Proposition3, records these facts directly.
See centralizer_recognition/RESULTS.md and its primary-source manifest. In a biordered
group x^m=y^m implies x=y for every positive integer m (if x<y, two-sided
invariance gives x^m<y^m). Therefore C(g^m)=C(g) for every m nonzero. Moreover,
VZ(J)=Z(J) for every subgroup J: an element centralizing a finite-index subgroup
centralizes a power of each element, hence each element itself. The universal
construction above does not depend on this extra simplification.

## What would still be needed for a negative answer

The maximal irreducible parabolic-center forward lemma supplies vertices of
R(Q_H4) whose stable centralizers are P_H3. Commensurability would require a
vertex of R(Q_F4) with stable centralizer abstractly commensurable to P_H3.
Neither the graph definition nor its finite-index lemma excludes that vertex.
An exhaustive calculation or intrinsic recognition theorem is still needed.

Even restricting to the chosen parabolic-center vertices is insufficient:
F4 rank-one centers have centralizers involving the restricted 13-plane
arrangement, besides the B3 maximal-parabolic profile. Rank-two centers give
product profiles. An arbitrary vertex need not belong to any of those selected
families. Calling the chosen bordification nerve 'algebraic' does not prove that
arbitrary isomorphisms of finite-index subgroups preserve it. The exact
Davis--Huang scope audit is in centralizer_recognition/DAVIS_HUANG_SCOPE_AUDIT.md.
