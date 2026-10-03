# Attempt 4: remove the extra central factor abstractly

Recorded 2026-10-03 UTC. Outcome: the general direct-factor/retract argument is
false; a precise sufficient retraction criterion remains unavailable for A.
Original problem unresolved. Budget: 4/5.

## Attempted implication

Since A x Z is Helly, one might try to deduce that its direct factor A is Helly
by projecting to A, taking a zero-height slice, or taking a central quotient.
This would avoid the failures of the specific models tested so far. We test the
underlying permanence statement rather than assuming it.

## Exact counterexample to the general permanence statement

Let

    L={(u,v,w) in Z^3 : u+v+w=0},
    W=L semidirect S_3,

where S_3 permutes coordinates. This is the affine Coxeter group of type A~_2.
Let K be the graph with vertex set Z^3 and edges between distinct points at
supremum distance at most 1. Its graph distance is the supremum distance.
Every ball is a Cartesian product of three integer intervals. A pairwise
intersecting family of such balls gives pairwise intersecting integer intervals
in each coordinate, and those intervals have a common integer. Thus K is Helly.
This argument also handles infinite families: any one bounded integer interval
makes the descending-intersection question finite.

Define an action of W x Z on K by

    (ell, sigma, n).x = sigma(x)+ell+n(1,1,1).

It is a graph-automorphism action. It is proper: the finite permutation group
and the discrete translation lattice give only finitely many elements moving
a fixed finite set to intersect itself. It is cocompact: L+Z(1,1,1) consists
of exactly those integer triples whose coordinate sum is divisible by 3 and
has index 3 in Z^3. Therefore W x Z is Helly.

On the other hand W is not Helly. Its real two-dimensional point representation
contains a rotation of order 3. Hoda's Theorem 7.1 says that a virtually abelian
Helly group's point group must be conjugate into the linear isometry group of
l_infinity of the same dimension. The latter group in dimension 2 has order 8
(the signed coordinate permutations), so has no element of order 3. This rules
out W. Source: https://arxiv.org/html/2010.07407v2, Theorem 7.1.

Consequently a direct factor, central quotient, and algebraic retract of a
Helly group need not be Helly. The example realizes all three failures at once.
It also shows why passing to a quasi-isometrically embedded or quasi-isometrically
retracted copy is insufficient: coarse injectivity/Hellyness is sensitive to
the specific metric and equivariance, not just these coarse embeddings.

## A valid sufficient replacement

Suppose a Helly graph Y carries an A-action, and Z is an A-invariant connected
subgraph with its induced path metric. Suppose there exists a 1-Lipschitz map
r:Y -> Z restricting to the identity on Z, and the A-action on Z is proper and
cocompact. Then Z is Helly and answers AIM 4.2.

Indeed, the retraction and inclusion imply that Z is isometrically embedded:
for u,v in Z, d_Y(u,v)<=d_Z(u,v)<=d_Y(u,v). A family of pairwise intersecting
balls in Z is therefore a family of pairwise intersecting balls in Y. Choose
a common vertex y using Hellyness of Y. Then r(y) lies in every original ball
because r is 1-Lipschitz and fixes all their centers.

For a restriction of a geometric (A x Z)-action on Y, properness of the
restricted A-action is automatic. Cocompactness is the difficult additional
condition: one would need the image to stay in a uniformly bounded band in
the removed direction, while retaining the 1-Lipschitz retract property.
No such retract has been constructed for a geometric Helly model of A x Z.
The exact Bestvina quotient of Attempt 1 cannot itself be such a metric retract,
since it already fails Hellyness.

## Scope and next step

The counterexample W has torsion. It does not disprove a carefully formulated
permanence theorem with additional torsion-free hypotheses, nor does it prove
anything negative about A itself. No such stronger theorem is supplied here.
Attempt 5 investigates the Helly hull of Q and states the exact bounded-hull
criterion needed to turn that remaining natural construction into a solution.
