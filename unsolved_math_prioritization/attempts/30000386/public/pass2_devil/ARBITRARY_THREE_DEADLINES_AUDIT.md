# Independent audit: three arbitrary known detonation times

## Verdict

Accepted. The frozen proof establishes online survival for any three prescribed known positive integers U<V<W, against every adaptive Devil restricted to those time coordinates, under the exact two-dimensional king-move game. It does not establish survival for arbitrary finite or unrestricted timestamp sets.

Artifact audited:

- `pass2_deadlines/THREE_DEADLINES.md`
- SHA-256 `8f28f7e3c47dae09fb1fa3067dccaa940b7e2862eda756f8f6020d5d4d386403`

No required correction was identified in this artifact. The small case a=c=1 uses D=45/7 and has cost exactly 4/5; using D=7 there would be incorrect.

## 1. Endpoint geometry and timing

Independently reconstructed E_0={−1,0,1}² and the four disjoint child translates by 2^k(±1,±1). At scale a=2^k the radius is 2a−1 and the cardinality is 9a². For k≥1 the current center reaches any child center in exactly a diagonal king steps, leaving a−1 moves, the child's required radius.

The maximum initial wait is 2a−1. Traversal lengths sum to 2a−2, so waiting plus all traversals consumes r−1 moves. The remaining final king move reaches every point of E_0. Hence every charged update occurs before the terminal Angel move. There is no assumption of viewing the update after that move.

At each branch the four equal-size disjoint endpoint sets partition the parent endpoint set, justifying the least-average choice. Intermediate traversals need not stay inside the endpoint set; this is harmless because the theorem permits no intermediate lethal times within a phase.

## 2. Weighted and concentration estimates

The global mass contribution is beta[w/(9a²)+(4/9)(1−1/a)]. With w≤2a−1 this is at most beta[4/9−(2a+1)/(9a²)]. Thus beta≤9/4 gives strict terminal hazard below one from zero.

For an update with total mass beta and peak alpha, every 9b²-point endpoint set receives average at most min(beta/(9b²),alpha). This remains valid for sparse endpoint sets, arbitrary translations, and adaptive updates. The waiting and traversal bound follows by summing only the updates after the phase's starting boundary announcement.

The backward denominator reserves 2a C_a because the boundary announcement plus the wait requires at most w+1≤2a updates on the initial set. Strict preboundary mass below D therefore remains strict at the downstream endpoint. Both lethal boundaries U and V are covered in this way.

## 3. Last-gap reserve

With later gap scale c, the conservative denominator is D_c=5c²+2c and the normalized mass is B_c=9c/(5c+2). The two downstream update types have bounds (1,1) and (B_c,1/D_c).

At dyadic b<c one has b≤c/2 and 9b²<D_c, so the point kernel gives the larger profile. At b≥c the future kernel's mass bound gives the larger profile. This establishes exactly the two profile bands used in the backward calculation.

## 4. Independent derivation of the earlier reserve and first-phase bounds

For earlier scale a<c, every relevant boundary and traversal scale is below c, giving D=5a²+2a. The three first-phase profile bands are the point kernel for b<a, the middle kernel for a≤b<c, and the far kernel for b≥c. Their infinite cost is

    (4/9)[1+(B_a−1)/a+B_a(B_c−1)/c].

The bounds (B_a−1)/a≤2/7, B_a<9/5, and (B_c−1)/c≤1/4 for c≥2 yield a cost strictly below 27/35.

For a≥c, direct summation gives

    D=a²[5−4(B_c−1)/c]+2B_c a.

The far kernel dominates the middle kernel in both mass and peak. Writing

    lambda(c)=(25−6/c+8/c²)/9,

one obtains D/B_c=lambda(c)a²+2a. The inequalities 8/3≤lambda(c)≤3 hold for dyadic c: the lower one reduces to (c−2)(c−4)≥0, and the upper one to (c+4)(c−1)≥0. The dyadic assumption is important in the lower inequality.

At scales b<a the point kernel dominates; at b≥a the far kernel dominates. The infinite cost is

    F=4/9−4/(9a)+4/[lambda(c)a+2].

For a=c=1 this is exactly 4/5. For a≥2, replacement of lambda by 8/3 gives a strict bound below 4/5. Independently expanding the claimed numerator gives 128a²−284a+120, equal to 4[32(a−2)²+57(a−2)+16], positive for a≥2. Thus all cases are strictly below one.

The initial deadline U can be arbitrary: its finite wait/traversal cost is bounded by the applicable infinite dyadic cost. The input times and denominators are known before play, but all target locations and child choices are handled online.

## 5. Chronology and scope

The first hazard starts at zero and consists of nonnegative linear smoothings of the observed bomb indicators. A fresh bomb contributes at most one translated kernel of its prescribed type; a duplicate contributes less. Hazard below one at U both avoids the U bomb and certifies a robust phase to V after every possible round-U announcement. Hazard below one at V does the same for W after every possible round-V announcement. Past-time announcements are irrelevant. After W the game has no further lethal allowed time.

No averaging over unknown future target locations, safe path selected after a complete schedule, or preloaded-state forcing assumption is used.

## Supplementary finite checks

`check_three_deadline_constants.py` independently checks endpoint sizes, radii, child disjointness through scale16, and exact rational identities/bounds on121 pairs of dyadic scales through1024. Its replay is `three_deadline_constants_replay.json`. These checks passed and are not substitutes for the universal argument above.
