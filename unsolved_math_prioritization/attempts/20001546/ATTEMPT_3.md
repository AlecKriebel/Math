# Attempt 3: arbitrary line cocycles and real-tree fibers

Recorded 2026-10-03 UTC. Outcome: a broader nonproperness theorem for
fiber-preserving repairs of the Deligne model; not a group-level obstruction.
Original question unresolved. Budget: 3/5.

## Proposed repair

The old catalogue attempt excludes global character-diagonal actions on X x R.
It is natural to allow the action on the fiber to depend on the base point,
permit reflection as well as translation, or replace the line by a real tree.
This is substantially broader than a global character twist. We test whether
such a repair could retain the useful Helly geometry while making the action
proper.

## An embedded rank-two subgroup

Let P=<a,b> in A. It is isomorphic to B_3=<a,b | aba=bab> without needing a
parabolic-injectivity theorem: the homomorphism A -> B_3 given by a->a, b->b,
c->a is a retraction of the natural homomorphism B_3 -> A. All three defining
relations are respected. Put z=(ab)^3 and h=[a,b]. The element z is central
in P and has infinite order because exponent sum sends it to 6.

The element h also has infinite order. Under the homomorphism P -> SL_2(Z)

    a -> [[1,1],[0,1]],    b -> [[1,0],[-1,1]],

the braid relation holds and h maps to [[1,1],[1,2]]. Its trace is 3 and its
largest eigenvalue is (3+sqrt(5))/2>1, so no positive power is the identity.

## Proposition: no proper P-action on a complete real tree

Consider an isometric action of P on a nonempty complete real tree T. By the
elementary classification of tree isometries, z either fixes a point or has a
unique translation axis.

If z fixes a point, that point has infinite stabilizer <z>. Otherwise z has
an axis L. Since z is central, all of P preserves L. Every element of P
commutes with the nontrivial translation induced by z, so its restriction to L
is a translation (a reflection would reverse that translation). The restriction
P -> Isom(L) has abelian image; hence h fixes every point of L. Again some
point has the infinite stabilizer <h>. Either case contradicts properness.

This proof only uses the usual elliptic/hyperbolic dichotomy and unique-axis
property of isometries of a real tree. It applies in particular to lines and
to simplicial trees, allowing edge inversions after subdivision.

## Corollary: no tree-fiber Deligne repair

Let Y be an A-space with an A-equivariant projection pi:Y -> X to the Deligne
coset model. Suppose the fiber above the vertex x=P is a nonempty complete
real tree and the stabilizer P acts on that fiber by its tree isometries.
Then the A-action on Y is not proper: the proposition supplies a point of
that fiber with an infinite stabilizer, which is also a stabilizer in Y.
No product metric or globally constant character is assumed.

In particular, every fiber-preserving isometric skew-product action

    g(x,t) = (gx, rho(g,x)(t))

on X x R is nonproper, whenever rho is an Isom(R)-valued cocycle. On the fiber
above x=P, the cocycle law makes rho restricted to P a genuine homomorphism.
This covers base-dependent shifts and reflections, beyond the prior report.

For the line case one can say more directly that h fixes the entire fiber.
In any homomorphism P -> Isom(R), the braid relation forces the orientations
of a,b to agree. If both act as translations t->t+u and t->t+v, the relation
forces 2u+v=u+2v. If both act as reflections t->-t+u and t->-t+v, it forces
2u-v=2v-u. In both cases u=v, so the image is cyclic and kills [P,P].

## Boundary of the argument

The conclusion depends on preserving the equivariant projection and on having
tree fibers. It gives no obstruction to fibers which carry proper B_3-actions
in dimension two or higher, or to unrelated Helly graphs. In particular B_3
itself is Helly, so its presence as a stabilizer before replacement is not an
obstruction to a suitably elaborate resolution of stabilizers. Constructing
such resolutions with compatible Helly gluing remains entirely open here.

The next attempt asks whether A x Z being Helly can be used more abstractly,
avoiding the particular Garside quotient and these fiber restrictions.
