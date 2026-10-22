# Attempt 5 of 5: a unit-chain barrier to greedy endpoint induction

## Goal and result

Try an induction that straightens the first joint by moving only the first
endpoint, while keeping every other vertex fixed, then freezes that joint and
continues. This induction is false. We construct a strict eight-unit-bar chain
whose first joint cannot be straightened with its tail fixed. The obstruction
is a closed curve of forbidden directions on the endpoint sphere.

This does **not** prove the entire chain locked: the other seven bars are
artificially held fixed in this test, whereas the AIM problem lets them move.

## Five unit bars whose radial image is a closed loop

Put `h=1/4`, `R=1/(2 sin(pi/5))`, and

    q_k=(R cos(2pi k/5), R sin(2pi k/5), h),  0<=k<=4.

These are the vertices of a regular unit-sided pentagon in the plane `z=h`.
All lie strictly inside the unit ball centered at the origin, since

    R²+h² = (5+sqrt(5))/10 + 1/16 < 1.                 (1)

For `t<1` sufficiently close to one, retain `q_0,q_1,q_2,q_3`, put
`q_5(t)=t q_0`, and choose `q_4(t)` with height `th` and

    |q_4(t)-q_3|=|q_4(t)-q_5(t)|=1,
    q_4(t) -> q_4 as t -> 1.                           (2)

Here is an explicit continuous choice. In the horizontal coordinate plane set

    A=(q_3x,q_3y), B=(tR,0), D=B-A, L²=|D|²,
    r²=1-h²(1-t)²,
    alpha=(r²-1+L²)/(2L²),
    beta=sqrt(r²/L²-alpha²),
    Q=A+alpha D-beta J D,     J(x,y)=(-y,x),
    q_4(t)=(Q_x,Q_y,th).                               (3)

At `t=1` the circles intersect transversely at the regular pentagon vertex
and a second point: their center distance is the golden ratio, strictly
between zero and two. Thus the radicand in (3) is strictly positive near one.
The minus sign selects the regular vertex with negative y-coordinate.
The usual two-circle calculation proves (2) exactly.

For `t<1` close enough, all six ring vertices remain inside the open unit ball,
and all their z-coordinates are positive. Their radial images form a closed
simple curve: project centrally to `z=1` by

    G(x,y,z)=(x/z,y/z).

The endpoint images agree, `G(q_5(t))=G(q_0)`. At `t=1` the five distinct
images form a regular convex pentagon surrounding the origin. Strict convexity
and containment of the origin persist for nearby `t`; hence the projected
five-edge loop is a convex polygon. Central projection sends each spatial
segment to the whole segment between its projected endpoints because z stays
positive. The spatial ring is nevertheless an open, embedded five-bar chain:
the only repeated projected direction is at its two endpoints, and those
endpoints have different radii when `t<1`.

## Attach a two-bar stem and the trapped first bar

Let `rho²=R²+h²` and put

    c=rho²/(2R), s=sqrt(1-c²), b=(c,s,0),
    N=(0,0,1), O=(0,0,0).

Both `c` and `s` are positive. The complete ordered chain is

    N, O, b, q_0, q_1, q_2, q_3, q_4(t), q_5(t).      (4)

It has eight bars. The first two are unit, and

    |b-q_0|²=1+rho²-2Rc=1.

The next three regular-pentagon sides and the two sides in (2) are unit too.

To check strict simplicity, the ring is embedded by the radial argument above.
The stem `O b` lies in `z=0`, while the ring lies in `z>0`. The segment `b q_0`
has positive x and nonnegative y and lies below `z=h` except at `q_0`. It misses
the three fixed ring bars in `z=h` except at its intended joint. The two
perturbed final ring bars have negative y in their interiors for nearby `t`,
so they also miss `b q_0`; their endpoint `q_5(t)` has y zero but is not on
`b q_0`, whose only y-zero point is `q_0`. Finally `O N` is the positive
z-axis. The ring's convex radial polygon has the origin strictly inside, not
on its boundary, so no ring point lies on that axis. Both stem bars meet the
axis only at their intended incidence, if any. No adjacent backtracking occurs.

All required strict inequalities also hold at the explicit algebraic parameter
`t=99/100`; the companion verifier checks these using rational interval
arithmetic with outward bounds for every square root. The proof itself only
needs a sufficiently small positive value of `1-t`.

## Why the first joint cannot be straightened with the tail fixed

Keep `O,b,q_0,...,q_5(t)` fixed. The first endpoint may move only on `S²`.
Let `C` be the radial image of the five-bar ring on that sphere. It is a
simple closed curve entirely in the upper hemisphere. Its cap-side component
contains `N`, because the associated gnomonic polygon contains the origin.
Every equatorial point is on the other side.

For each `v in C` there is a ring point `lambda v` with `0<lambda<1`, by
(1) and its persistent strict version. Thus the moving first bar `[O,v]`
would meet the fixed ring. Every point of `C` is forbidden.

The first joint at `O` is straight exactly when its first endpoint is `-b`:
the ordered triple must be `-b,O,b`. This target lies on the equator.
Any continuous endpoint motion from `N` to `-b` crosses `C` by the Jordan
separation theorem on the sphere, and so causes a forbidden intersection.
No first-endpoint-only straightening exists for (4).

## Final status and exact unresolved assertion

This rules out the proposed greedy induction, not arbitrary simultaneous
motion. No invariant survives when the fixed tail is allowed to move, and no
global locking claim is made for (4).

After five substantive attempts, the remaining assertion is still:

    For every n and every strict embedded open unit-bar chain in R3,
    there is a continuous strict embedded unit-bar motion to a straight chain.

The work proves a linear test and direct motion for one sufficient class,
explicitly separates that class from all unlocked chains, establishes a rational
counterexample reduction, and identifies a genuine obstacle to fixed-tail
endpoint induction. It establishes neither the universal assertion nor its
negation. The outcome is **unsolved, 5/5**, with partial method results and no
novelty claim. Retrieval, computation, review, and packaging are not additional
proof-attempt turns.
