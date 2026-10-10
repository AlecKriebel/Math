# Attempt 2: a short-span restriction kernel

3 October 2026. Outcome: a codimension-one extension of the short-span bound
and an exact residual-kernel formulation. General target unresolved.
Discovery-goal completion estimate: 15% (subjective).

## Mechanism

Attempt 1 prevents assuming a uniformly short full basis. Instead retain
the part that is short and bound what acts invisibly on it.

Let G=S_x(2R), choose t=ar<=2R, and put

    P=C_x(t)-x,    V=span(P),    k=dim V,    N=|P|.

Assume k>=1. Every g in G preserves P, since it preserves distance from x.
Thus V and V-perp are invariant. Restriction gives an exact sequence

    1 --> K --> G --> H --> 1,

where H<=O(V) preserves P and K embeds faithfully in O(V-perp). No assumption
that K is a Delone cluster group in the lower dimension is made.

Choose a basis p_1,...,p_k from P. The H-action is determined by its images
on that basis. These are distinct nonzero members of P. Hence

    |H| <= (N-1)_k <= (N-1)^k,
    |G| <= (N-1)_k |K|.                                  (1)

Here (n)_k=n(n-1)...(n-k+1). The kernel embeds in O(V-perp), because an
orthogonal map equal to the identity on both summands is the identity.

## Intrinsic-dimensional packing

The open k-balls of radius r in V centered at P are disjoint: their centers
still have ambient, equivalently intrinsic, separation at least 2r. They
all lie in the intrinsic ball of radius (a+1)r. Therefore

    N <= (a+1)^k.

This counts in dimension k, not the ambient dimension d. Equations (1)
imply the convenient less sharp estimate

    |G| <= (a+1)^(k^2) |K|.                              (2)

Both inequalities hold for any Delone set and any center with this rank;
2R-regularity is not needed. The 2R-cluster spans R^d by the standard
covering argument, so G and K are finite.

## Codimension one is enough

If k=d, K is trivial and (2) is the familiar full-span bound. If k=d-1,
O(V-perp)=O(1) has order two, so

    |S_x(2R)| <= 2(a+1)^((d-1)^2).                       (3)

Thus the fixed-scale spanning hypothesis can be weakened to codimension
at most one. A centered cluster equivalence restricts to every smaller
radius, so in a 2R-regular set the rank condition at one center holds at
all centers. For d=4, rank three at radius ar gives the explicit estimate
2(a+1)^9.

## Why the kernel cannot simply be discarded

Already O(2) contains cyclic groups of every order. A finite point-set
model makes the problem concrete. Take k independent short coordinate
vectors in R^k, their negatives, and a regular m-gon of much larger radius
in a perpendicular plane, together with the origin. The short subcluster
spans R^k. Rotation of the polygon acts trivially there but has order m.
All distances in this finite configuration are positive, and it spans
R^(k+2). Therefore rank plus finiteness alone cannot bound |K|.

This model is deliberately only a finite configuration. It is not claimed
to extend to a 2R-regular Delone set, and so is not a counterexample to the
AIM problem. Precisely the missing global compatibility must control K.

## What failed to finish

In dimension four, rank two leaves a finite subgroup of O(2), whose
rotation subgroup has index at most two. Bounding its cyclic order would
suffice for this case. Rank one leaves an O(3) kernel. The known theorem
about genuine three-dimensional Delone cluster groups does not apply:
neither V-perp intersect X nor the projection of X has been proved to be
a lower-dimensional Delone set with matching centered clusters and the
required radius. That inheritance is the exact unproved step, not a
routine induction.

These elementary refinements are not claimed as new literature results.
