# Deductive adversarial models

These are exact metric examples and derivations. No finite-model computation or
empirical pass is used to establish the universal lemma.

## 1. Metric circle: coefficient 4 is optimal

Let `C>0`, and put the usual intrinsic arc-length metric on the circle
`S_C=R/CZ`. Use a coordinate `t in [-C/2,C/2]` centered at `o=0`; the two
endpoints represent the antipode. The center distance is `|t|`.

For two endpoints with coordinates of the same sign, choose the coordinate
interval; it is minimizing and its center radius never exceeds the endpoint
maximum. For opposite signs, write the coordinates as `A,-B`, with
`A,B in [0,C/2]`. If `A+B<=C/2`, choose the minimizing arc through `o`, whose
radial maximum is `max(A,B)`. At equality this choice also resolves the two
minimizing geodesics. If `A+B>C/2`, the unique shorter arc crosses the antipode.
Its radial maximum is `C/2`, whereas `max(A,B)>C/4`. Hence every pair has a
chosen minimizing arc satisfying (H) with `c=C/4`. Rotation gives the same
constant for every center.

This is the least possible uniform constant: take
`A=B=C/4+epsilon`, `0<epsilon<C/4`. The unique minimizing arc crosses the
antipode, giving radial excess `C/4-epsilon`. These excesses approach `C/4`.

Now choose `0<k<C/2` and `R=(C-k)/2<C/2`. The closed ball around `o` is exactly
the embedded coordinate arc `[-R,R]`. Its endpoints `x=-R,y=R` have ambient
distance `k`, via the missing complementary arc of length `k`. Every continuous
path in the ball must pass through coordinate zero, by the intermediate value
theorem. Its length is therefore at least
`d(x,o)+d(o,y)=2R`, and the radial path attains that length. Thus

\[
 d_{\overline B(o,R)}^{\rm int}(x,y)=2R=C-k,
 \qquad d(x,y)=k,
 \qquad d_{\overline B(o,R)}^{\rm int}(x,y)-d(x,y)=C-2k=4c-2k.
\]

As `k` tends to zero, the additive excess approaches `4c`. For every proposed
universal coefficient `A<4`, choosing
`0<k<min(C/2,(4-A)C/8)` contradicts a replacement conclusion
`Len <= d(x,y)+A c`. This verifies that the factor 4 is optimal under the exact
abstract hypothesis. It does not assign historical novelty to this observation.

## 2. Multiplicative radial quasiconvexity cannot replace additive control

Every geodesic metric space satisfies a universal multiplicative radial bound
with factor 2, even for every minimizing segment. Indeed, let
`p=d(o,a)`, `q=d(o,b)`, and `ell=d(a,b)`. At arclength time `t` along a minimizing
segment,

\[
 d(o,z)\le\min(p+t,q+\ell-t)
 \le (p+q+\ell)/2\le p+q\le2\max(p,q).
\]

The penultimate inequality uses `ell<=p+q`.

Fix `k=1`, take `R_n=n+1`, and form the metric bouquet, at a common point `o`,
of circles of circumferences `C_n=2R_n+1`. Its metric is the usual path metric:
within one circle the shorter arc realizes distance, and between distinct
circles a minimizing path goes through `o`. Thus it is a geodesic metric space.

On circle `n`, choose points of coordinates `-R_n,R_n`. They have ambient
distance 1, and both are on the sphere of radius `R_n` around `o`. The ball
intersects that circle in the arc `[-R_n,R_n]`, leaving its complementary
length-1 arc out. Removing `o` disconnects the two sides of this arc; every other
circle meets it only at `o`. Hence every continuous in-ball path between these
points must pass through `o` and has length at least `2R_n`. This grows without
bound for fixed ambient endpoint distance 1 in a single geodesic space.

The bouquet still has the uniform multiplicative factor 2 above. It has no
all-radius fixed-k intrinsic detour bound. The submitted additive hypothesis is
therefore doing essential work; multiplicative quasiconvexity is not a substitute.

## 3. Center-dependent finite additive constants do not give all-center bounds

A flat cone supplies a single-space counterexample to this weakening, while
retaining exact minimizing geodesics. Fix a total cone angle `alpha=pi/2`.
Glue the boundary rays of a Euclidean sector of angle `alpha`, with its induced
length metric; call the tip `v`. Polar coordinates have `r>=0` and
`theta in R/alpha Z`.

For radii `r,s` and shortest angular separation
`Delta in [0,alpha/2]`, distance is

\[
 d((r,\theta),(s,\phi))
 =\sqrt{r^2+s^2-2rs\cos\Delta}. \tag{1}
\]

Here is a direct justification. A path avoiding `v` lifts its angle to a real
coordinate. If the endpoint angle difference has absolute value below `pi`,
developing the lift into the Euclidean plane bounds length below by the chord
for that angle; the straight chord itself lifts and attains it. Chord length
increases with the absolute angular difference on `[0,pi]`, so the smallest
representative `Delta<=alpha/2` is best. If a lifted path's endpoint angle
difference has absolute value at least `pi`, it first reaches the opposite ray,
at some radius `rho`. Its length up to there is at least `r+rho`; the remaining
length is at least `|s-rho|`, giving a lower bound `r+s`. A path through `v`
also has length at least `r+s`. Those bounds cannot beat the chord for `Delta`.
Formula (1) follows and supplies minimizing segments.

Relative to `v`, these straight developed segments have radius at most the
maximum endpoint radius, because the Euclidean norm is convex along a segment.
Thus `c(v)=0`. For any other center `p`, choose such a tip-radially controlled
minimizing segment. Then

\[
 d(p,z)\le d(p,v)+d(v,z)
 \le d(p,v)+\max(d(v,a),d(v,b))
 \le\max(d(p,a),d(p,b))+2d(p,v). \tag{2}
\]

Every center therefore has a finite additive constant `c(p)=2d(p,v)` independent
of radius and endpoints.

Nevertheless, there is no single all-center bound for fixed distance `k=1`.
Let `delta_n=1/(n+2)` for integers `n>=1`, so
`0<delta_n<alpha/2`, and put

\[
 \theta_n=(\alpha-\delta_n)/2,\qquad
 h_n=\frac{1}{2\cos\theta_n\sin(\delta_n/2)},\qquad
 p_n=(h_n,0),\qquad R_n=h_n\sin\theta_n,
 \qquad r_n=h_n\cos\theta_n.
\]

The center is `p_n`. Choose `x_n=(r_n,theta_n)` and
`y_n=(r_n,-theta_n)`. Formula (1) shows that both lie on the radius-`R_n`
sphere about `p_n`. Their shortest angular separation across the glued ray is
`alpha-2theta_n=delta_n`, so

\[
 d(x_n,y_n)=2r_n\sin(\delta_n/2)=1. \tag{3}
\]

Because `theta_n<alpha/2`, we have
`R_n<h_n sin(alpha/2)<h_n`. The whole ball about `p_n` is the image of the
ordinary closed Euclidean disk of radius `R_n` about `(h_n,0)`, entirely within
the open unrolled wedge `-alpha/2<theta<alpha/2`. To verify this statement,
(1) gives the usual disk inequality in these coordinates; minimizing distance
from `(h_n,0)` to a ray at angle `theta` gives `h_n sin|theta|`. Therefore the
disk has angular extent exactly `[-theta_n,theta_n]`, strictly inside the
identified boundary rays. The projection on this disk is injective.

The unrolling is a local isometry there. Its inverse is continuous, and the
compact disk stays at positive angular and radial distance from the cut rays
and tip. Consequently lengths of continuous paths in this ball equal their
Euclidean lengths: refine a partition enough that each subpath lies in one
local isometry neighborhood; lengths are local under finite concatenation.
Thus the restricted intrinsic distance is exactly the Euclidean chord length,
since the disk is Euclidean convex:

\[
 d_{\overline B(p_n,R_n)}^{\rm int}(x_n,y_n)
 =2r_n\sin\theta_n
 =\frac{\sin\theta_n}{\sin(\delta_n/2)}\longrightarrow\infty. \tag{4}
\]

Equations (2)-(4) establish the counterexample: finite additive constants exist
at every center, but one uniform fixed-k all-center bound does not. The lemma
with a fixed center still gives `d+4c(p)`; only the uniform conclusion fails.

## 4. Other extensions deliberately not inferred

The valid construction does not prove convexity of balls, continuity or a
Lipschitz bound for a global radial retraction, minimizing geodesics for the
intrinsic ball metric, bounds uniform over topological types, or almost
convexity of a quasiisometric model. None of these conclusions is required by
the exact submitted abstract lemma.
