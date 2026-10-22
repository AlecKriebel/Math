# Substantive turn 4: an exact planar obstruction to unchanged-suffix splicing

**Unreviewed partial counterexample to a proof mechanism.** Date: 2026-10-01. There is a simple, dynamically admissible single-wall prefix with nondecreasing fire-arrival trace, and a shorter replacement of an earlier negative-curvature arc, for which:

- both endpoints of the replaced arc and the entire suffix stay fixed;
- the modified prefix through the arc remains admissible;
- simplicity and nondecreasing arrival time are preserved;
- every arrival on the suffix advances by exactly the length saving Delta;
- the unchanged suffix becomes inadmissible, with terminal budget defect −(sigma−1)Delta.

Thus the Delta/sigma arrival-loss bound needed in Turn 3 is false for general single-wall prefixes. This example is not confining and is not claimed optimal for any global objective. It does not disprove the OWR automatic-convexity question.

## 1. Explicit geometry

The initial fire is the open unit disk centered at O=(0,0), spreading with unit speed. Put

    sigma=23/20,  A=(4,0),  C=(5,0),
    beta0=arccos(1/5),  d=sqrt(24),
    B=beta0+7/10,
    U=d-1+7/10,
    G=sigma*U-(3+B),  a=sqrt(2G).                  (1)

Here B is an angle, not a point. The rational certificates below establish

    1.369438 < beta0 < 1.369439,
    0.21938685 < G < 0.219389,
    0<a<7/10,
    beta0 < 1.38 < 1.39 < B-a.                    (2)

The barrier has three consecutive pieces, all reparametrized together by arc length:

1. The segment P from (1,0) to A, of length three.
2. The clockwise circular arc

       gamma(beta)=(5-cos(beta), sin(beta)),  0<=beta<=B.

   Its unit tangent is t(beta)=(sin(beta),cos(beta)), its curvature is −1, and its speed in beta is one.
3. The involute segment, traversed with v decreasing from B to B-a,

       W(v)=gamma(v)+(B-v)t(v).                   (3)

   Its length from gamma(B) to W(v) is (B-v)^2/2. Its total length is a^2/2=G.

The involute lies strictly outside the circle except at its starting point: |W(v)-C|^2=1+(B-v)^2. It is simple, stays in the upper half-plane, and does not meet the segment P. The whole barrier is consequently simple. Although W'(B)=0 in the v parameter, its arc-length parametrization is Lipschitz with a well-defined initial tangent. It has no self-intersection or extra branch at that point.

The initial tangent is e1, so both displayed initial-angle conditions hold: its angle with e1 is zero and with e2 is pi/2. This construction does not exploit the source's axis discrepancy.

## 2. Exact arrival times

First consider only P and the circular arc. Its arrival trace is

    u(gamma(beta)) = sqrt(26-10 cos(beta))-1,              0<=beta<=beta0,
    u(gamma(beta)) = d-1+beta-beta0,                      beta0<=beta<=B.       (4)

Both pieces are strictly increasing and agree at beta0. The trace on P is x-1.

Here is the shortest-path justification, including the possible other side of the thin wall. The upper tangent from O to the circle meets it at gamma(beta0), and the tangent segment has length d. Before that point the direct radial segment reaches gamma(beta) without crossing the wall. After tangency, the upper exterior shortest path consists of that tangent segment and the clockwise circle arc. Starting from the unit disk subtracts one from its length. The elementary convex-obstacle shortest-path description follows by straightening any free segment, tangency at a smooth contact, and projection onto the convex boundary between contacts.

Any competing path which crosses the horizontal axis to the right of A has length at least

    min_(x>=4) [x-1+|q-(x,0)|] = 3+|q-A|                 (5)

for an upper-half-plane target q. The minimum is at x=4, since the derivative of the expression in brackets is strictly positive. A path entering the disk through its upper unblocked boundary must first get around the terminal arc endpoint; before that entry its exterior length is at least the exterior arrival at gamma(B). Paths entering from below fall under (5). These alternatives exhaust ways to leave the upper exterior component without crossing the wall.

For gamma(beta), beta0<=beta<=B, the difference between the lower bound (5) and the exterior candidate is

    3+2 sin(beta/2) - (d-1+beta-beta0).

It decreases in beta, and at B it is greater than 1/10 by the rational certificate. Thus no lower-side route wins. Going around the later endpoint cannot improve an earlier exterior arrival, since the exterior arrivals increase up to B. This proves (4).

For q=W(v), its incoming tangent from the circle is exactly the segment displayed in (3). Its upper exterior arrival is

    d-1+(v-beta0)+(B-v)=U.                              (6)

The alternative bound 3+|W(v)-A| is strictly greater than U. Indeed it is already greater than U by more than 1/10 at v=B, and |W(v)-A| increases as v decreases: its derivative has the sign of

    (B-v)(cos(v)-1)<0.

An upper-side path entering the circle beyond the terminal endpoint has already spent at least U, so cannot beat (6). Adding the involute itself does not change these traces: its incoming rays have arrival strictly below U until their final contact, while the entire added arc is on the level U. The first-contact argument from Turn 3 applies. Earlier circle arrivals are likewise unchanged. Hence the full barrier trace increases along P and gamma and is constant along W.

## 3. Admissibility of the original prefix

On P the length budget is immediate since sigma>1. Along the circle, cumulative construction length is 3+beta. For 0<=beta<=beta0, the checker rigorously establishes

    sigma*(sqrt(26-10 cos(beta))-1)-(3+beta) > 1/20.     (7)

This is a continuum certificate, not a sampled claim: alternating rational Taylor bounds for cosine are checked on the grid i/100, 0<=i<=140. At every grid point the margin exceeds 61/1000. The margin function is Lipschitz with constant at most sigma+1=43/20, because radial distance has derivative of magnitude at most the circle's unit speed. Its distance to the nearest grid point is at most 1/200. Therefore the margin throughout [0,1.4] is at least

    61/1000-(43/20)/200 = 201/4000 > 1/20.

The certified beta0 is less than 1.4. After beta0, formula (4) shows that the margin increases with derivative sigma−1. Its value at B is G. On the involute the arrival stays U while the length increases by at most G, so the margin decreases from G to zero. The final point is exactly saturated:

    total length = 3+B+G = sigma*U.                    (8)

Since the trace is nondecreasing, these ordered prefix inequalities are exactly the static construction budget, including the entire final level-set plateau. Thus the original wall is admissible.

## 4. A smooth shortening inside the shared geodesic arc

Let l=1.38, h=1.39, w=h-l=1/100. Define a C3 bump

    eta(beta)=[4z(1-z)]^4 for z=(beta-l)/w in [0,1],
    eta(beta)=0 otherwise.

It is nonnegative, nonzero and has maximum one. On this small interval replace the circle by

    gamma_epsilon(beta)=C+(1-epsilon*eta(beta))(-cos(beta),sin(beta)).         (9)

All other parts of the wall, including its endpoints and involute, stay fixed. This moves that piece into the circle. A full closed oval obtained by applying the same change to the unit circle remains strictly convex for sufficiently small positive epsilon and lies inside the original disk. Its boundary, and all derivatives needed here, agree with the original circle outside [l,h].

One explicit valid choice is

    epsilon = 1/10158080008.

For a transparent exact bound, let A_eta=integral eta, B_eta=integral eta'^2 and let M2 bound |eta''|. The checker obtains

    A_eta=32/7875,  B_eta=5242880/9009,
    epsilon < min(1/100, A_eta/(4 B_eta), 1/(4(1+M2))).

The numerator of the oval's unsigned curvature is at least

    (1-epsilon)*(1-epsilon-epsilon*M2)>0.

The new speed on the changed interval is sqrt((1-epsilon eta)^2+epsilon^2 eta'^2). Using sqrt(R^2+y^2)<=R+y^2/(2R) and R>=1/2 proves that the length saving Delta satisfies

    Delta >= epsilon*A_eta-epsilon^2*B_eta > epsilon*A_eta/2 > 0.           (10)

The total absolute change of length on any partial segment is at most epsilon*(A_eta+2), using the total variation integral |eta'|=2.

## 5. The suffix arrival advances by exactly Delta

The initial tangent contact beta0 lies before l, and every involute contact v lies after h, by (2). Because the perturbed body is strictly convex and a subset of the old disk, the old tangent support lines at these unchanged contact points remain supporting lines, with the same unique contacts. Every upper exterior path to an involute point therefore traverses the entire changed boundary interval, then follows exactly the same remaining arc and tangent segment as before. Its arrival is exactly

    u_new(W(v))=U-Delta.                             (11)

No new shorter competing path is hidden in (11). The lower-route bounds at the fixed suffix remain greater than U. On changed arc points, moving the target changes the lower-route bound by at most epsilon, and changing the exterior boundary portion changes its length by at most epsilon*(A_eta+2). Their old gap exceeds 1/10 and the certified epsilon keeps it positive. Upper-side routes entering through the unblocked part beyond gamma(B) have already spent at least its new exterior arrival U-Delta. The preceding shortest-path classification consequently applies to the new oval as well.

The new arrival trace is still nondecreasing: before tangency it is unchanged, along the modified shadowed boundary it increases exactly by the new arc length, and on the fixed involute it is the constant U-Delta. Appending that involute does not alter the earlier traces, by first-contact causality. Simplicity persists because the modified arc lies inside the old disk and the involute is outside it.

The modified prefix through gamma(B) is still admissible. On the shadowed circle portion, the changes of arrival and cumulative length are the same partial boundary-length change, so its margin changes by (sigma−1) times that quantity. Equations (7) and (10) and the partial-length bound give

    new margin >= 1/20-(sigma−1)*epsilon*(A_eta+2)>0.

The earlier segment and visible circle part are unchanged. Thus the failure below occurs in the retained suffix, rather than because the local replacement was already impossible.

## 6. Exact failure of the splice condition

The new total length is sigma*U-Delta, while its terminal arrival is U-Delta. Therefore

    sigma*u_new(end)-new total length
       = sigma*(U-Delta)-(sigma*U-Delta)
       = -(sigma-1)*Delta < 0.                     (12)

Every point of the modified barrier has been reached by that terminal time, because its trace is nondecreasing. Thus (12) violates the static length budget as well as the ordered construction schedule. The relevant arrival loss is Delta, not at most Delta/sigma.

This is an actual planar example with the original isotropic unit-disk initial fire, not an abstract network fixture. It disproves the proposed universal quantitative splice estimate for simple arrival-ordered prefixes, even with a smooth perturbation and a still-admissible changed prefix. A global proof must exploit extra optimality information, modify the continuation as well, or use a different comparison. No conclusion about an optimal confining spiral follows from this nonconfining example.

The local negative-curvature part here is followed tangentially by minimizing fire paths. It is precisely outside the transverse free-ray-chart hypothesis of Turn 3. Thus the example is consistent with the conditional local convexity theorem, while showing why that theorem cannot simply be extended by retaining an arbitrary saturated continuation.

There is still no implication from a length comparison to a comparison of the weighted burned-area-plus-construction objective J. The example leaves both original initial-angle conventions satisfied, but does not settle automatic existence or orientation of tangents in a general optimal strategy.

`turn_4_check.py` supplies 158 exact rational assertions, including certified continuum budget bounds, tangent/support ordering, positive route gaps and the explicit perturbation constants. The geometric shortest-path argument is part of this written proof; the checker does not replace it.

Substantive author turns: **4/5**. Estimated completion toward the original target: **12%**; the estimate decreases because the natural unchanged-suffix route now has an exact obstruction. Original automatic convexity/A1 remains unresolved. This partial counterexample awaits independent review.
