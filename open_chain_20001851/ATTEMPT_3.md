# Attempt 3 of 5: test the certificate at the first unsettled bar count

## Goal and outcome

Try to settle the six-unit-bar case by proving every configuration has a scalar
axis certificate. This route fails: the explicit six-bar chain below is strict,
equilateral, nonplanar, and has no such axis. It nevertheless has a simple
orthogonal projection and is therefore unlocked. Its certificate failure is
stable under small three-dimensional perturbations. This separates certificate
failure sharply from mechanical locking.

## Exact six-bar example

Use the vertices

    p_0=(0,-1,0),
    p_1=(0,0,0),
    p_2=(24/25,0,-7/25),
    p_3=(48/125,96/125,-14/25),
    p_4=(-24/125,0,-21/25),
    p_5=(-24/125,0,4/25),
    p_6=(-149/125,0,4/25).

The four middle directions are

    d_2=(24/25,0,-7/25),
    d_3=(-72/125,96/125,-7/25),
    d_4=(-72/125,-96/125,-7/25),
    d_5=(0,0,1).

Each has squared length one; the terminal directions are `(0,1,0)` and
`(-1,0,0)`, also unit. But

    150 d_2 + 125 d_3 + 125 d_4 + 112 d_5 = 0.          (1)

All coefficients are positive. A functional positive on all four middle
directions would make the left side of (1) positive, a contradiction. By
Attempt 1, no scalar-axis certificate exists.

## Exact verification of a simple projection

Apply the rank-two linear map

    T(x,y,z)=(x-z/10,y).

Its kernel is the line spanned by `(1/10,0,1)`. Thus `T` factors through
orthogonal projection perpendicular to that line by a linear isomorphism.
Injectivity of `T` on the chain is equivalent to simplicity of that orthogonal
projection. The projected vertices are

    (0,-1), (0,0), (247/250,0), (11/25,96/125),
    (-27/250,0), (-26/125,0), (-151/125,0).             (2)

The first edge is vertical below the origin. The second runs right along the
horizontal axis. The next two form an upper arch from its right endpoint to
`(-27/250,0)`; the arch meets the horizontal axis only at its two endpoints,
and its intersection with `x=0` has positive height. The final two edges run
strictly left along the horizontal axis from `-27/250`. Consequently every
nonadjacent pair is disjoint, and adjacent bars meet only at their common
vertex. In particular the final two collinear bars do not backtrack.

The chain is therefore strict-simple in space and has a simple orthogonal
projection. Biedl et al., Theorem 2.1, implies a rigid-bar straightening motion.
No locking conclusion can be drawn from (1).

## Why the obstruction is not confined to a planar degeneracy

The vectors `d_2,d_3,d_5` are linearly independent, and (1) is a strictly
positive dependence among the four middle directions. Hence those four points
are affinely independent and their tetrahedron contains the origin in its
interior. This property persists under sufficiently small perturbations of
the four vectors. Strict simplicity of the original chain also persists under
sufficiently small perturbations, subject to maintaining bar lengths.

For clarity, strict simplicity is open in edge-direction coordinates: compact
nonadjacent segments have positive separation, and each pair of adjacent
directed unit bars is different from an antiparallel pair. The final collinear
pair in (2) is forward, so it causes no overlap instability. The simple-projection
property is likewise open for these directions. Thus an open set of unit-chain
configurations is unlocked while failing every scalar-axis certificate.

## Smaller planar witness and longer examples

A five-unit-bar witness to failure already exists at

    (0,-1,0), (0,0,0), (1,0,0), (2/5,4/5,0),
    (-1/5,0,0), (-6/5,0,0).

Its middle directions obey `6d_2+5d_3+5d_4=0`; the planar chain is simple by
the same upper-arch argument. This planar dependence alone would not establish
an open obstruction in three-dimensional direction space, which is why the
nonplanar six-bar example was constructed separately.

Both examples can be prolonged by unit bars along their final leftward ray.
The same positive middle-direction dependence remains, while the displayed
projection stays simple. Thus failure is not peculiar to a single bar count.

## Remaining gap

The all-six-bar scalar-certificate claim is false. The original six-bar
unlockability statement, and the arbitrary-count AIM problem, are not refuted.
A successful proof must permit configurations outside this ordered-axis class,
for example by reaching it through a nontrivial motion or using a different
certificate. The explicit obstruction here is only to a proposed sufficient
method, not to the allowed motion space. Novelty is not asserted.
