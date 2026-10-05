# Independent Euclidean derivations and exact control

Frozen UTC: 2026-10-04T23:07:51.568129+00:00, before candidate/author/inherited-review access.

## Exact reflection-law triangle

Let a²=A, b²=B, c²=A-B and P0=(a,0), P1=(at,bs), P2=(at,-bs), t²+s²=1 with s>0. Equality of incoming and outgoing tangent velocity components at P1 gives

    s[A-(A-B)t] = -b t sqrt((1-t)[A(1-t)+B(1+t)]).

For t<0 both sides are positive. Squaring and dividing by (1-t) gives the nondegenerate factor

    (A-B)t² -2Bt-A = 0,
    t=(B-sqrt(A²-AB+B²))/(A-B).

Take A=8, B=3, so sqrt(A²-AB+B²)=7, t=-4/5, s=3/5. Thus

    P0=(2sqrt2,0), P1=(-8sqrt2/5,3sqrt3/5),
    P2=(-8sqrt2/5,-3sqrt3/5).

The focal coordinates are (±sqrt5,0), the caustic squared axes are (128/25,3/25), and λ=72/25. The latter is strictly in (0,b²), so the caustic is a genuine strictly nested confocal ellipse. All three chord tangencies are certified by h²=α² n_x²+β² n_y². Unit incoming/outgoing directions satisfy vout=vin-2(vin·n)n/(n·n) exactly at every vertex. The triangle is convex, primitive and counterclockwise.

The outer tangent intersections are

    T0=(2sqrt2,3sqrt3), T1=(-5sqrt2/2,0),
    T2=(2sqrt2,-3sqrt3).

Perpendicular projection and exact shoelace calculation yield

    A_± = (96sqrt6 ±24sqrt15)/625,
    A'_± = (12sqrt6 ±3sqrt15)/5.

All four are strictly positive: 4sqrt6>sqrt15 follows on squaring from 96>15. Both ratios equal (37+8sqrt10)/27, and A'_±=(125/8)A_±. Explicit coefficient ratio is (12/5)/(96/625)=125/8. Thus the printed equality is exactly true in this control. A proposed reciprocal correction A_+/A_-=A'_-/A'_+ is false in this same control: its cross difference is 3456sqrt10/3125>0. A simultaneous focus-label swap preserves the equality. The independent code also computes antipedals as a separate construction; they do not define the target.

## Independent direct orbit generator

At P∈E set n=(Px/a²,Py/b²), J=sqrtλ/(ab), τ=(-ny,nx). The outgoing unit velocity

    v= -J n/(n·n) + sqrt((1-J²/(n·n))/(n·n)) τ

satisfies n·v=-J. Its straight next intersection with E is at

    t=-2(Px vx/a²+Py vy/b²)/(vx²/a²+vy²/b²), Q=P+t v.

Reflect at Q with its ellipse normal. This generator uses Euclidean square roots and solves rational winding closure by bisection; it does not depend on the candidate's canonical elliptic parametrization. Tangency, membership, unit velocity, reflection, closure, primality, focal-feet incidence and perpendicularity, circle loci, outer intersections, all four areas, reversal and repetition are measured independently. Decimal phase r uses P=(a(1-r²)/(1+r²),2br/(1+r²)). The numerical results are finite high precision without intervals.

## Implementation correction log

The first exact script attempt failed only at converting exact zero to a diagnostic float (empty sum returned integer); the conversion was corrected. A subsequent deliberately falsifiable assertion expecting a reciprocal relation failed; it was removed and replaced with outcome reporting. Both full streams are retained. The actual exact calculations show the printed target holds for the chosen triangle and its reciprocal does not. No mathematical conclusion depends on the diagnostic float output.
