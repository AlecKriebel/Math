# Turn 1: traffic local finiteness from route-length moments

**Scoped theorem; the full ordinary-axiom case remains unresolved.** This is substantive author turn 1 of 5 for 9700031. The 2012 question is Open Problem 31; the published 2014 question is Open Problem 5, Section 8.3. The theorem gives an affirmative answer under explicit moment regularity, and a subrange under the original first-moment bound. It does not assert that these extra moments hold for every SIRSN.

## 1. Setup and exact conclusions

Use a planar SIRSN as in Aldous (2014), with route length D=len R(0,(1,0)), E D<infinity, and major-road intensity p(1)=p<infinity. Write E_r=E(infinity,r). This is the union, over an increasing independent space-time Poisson sample, of route portions whose Euclidean distances from both endpoints exceed r. In particular E_r is not a speed-threshold network. The known intensity scaling is

 E H^1(E_r intersect A)=(p/r)|A|,

for bounded Borel A. Here H^1 is ordinary length and |A| is area.

We impose the following continuum regularity explicitly:

**(JM)** The routes have a jointly measurable realization in the environment and the two endpoints, with rectifiable non-self-intersecting route images, so that their length kernels and intersections with the countably sampled major-road sets are measurable. The realization has the prescribed finite-dimensional laws and Euclidean covariance in distribution. Null sets of endpoint pairs may be ignored.

The original paper formulates the process through finite-dimensional distributions and discusses continuum extensions. This proof does not assume that a bare finite-dimensional construction automatically supplies (JM). On such a realization define, off the diagonal,

 T_{beta,r}(A)= integral integral |y-x|^(-beta)
     H^1(R(x,y) intersect E_r intersect A) dx dy.                (1)

All integrals are nonnegative extended integrals. They define measures before finiteness is proved.

**Theorem.** Under (JM), if E D^s<infinity for some s>=1, then, for

             2<beta<4-2/(s+1),                                 (2)

T_{beta,r} is almost surely locally finite, simultaneously for every r>0. Consequently the untruncated traffic measure T_beta is sigma-finite on the union of the E_r, and its spatial push-forward satisfies

             (sigma_c)_# T_beta  has law  c^(beta-5) T_beta.     (3)

In particular:

- The usual first-moment hypothesis gives 2<beta<3, with only the explicitly stated continuum-version regularity added.
- If all finite positive moments of D exist, (1) is locally finite for every 2<beta<4.
- A deterministic uniform route-stretch bound implies the latter moment condition. Aldous's binary-hierarchy stretch estimate is a credited instance of such regularity, not a property asserted for general SIRSNs.

There is a supplementary endpoint statement: E[D log(1+D)]<infinity suffices for beta=3. No claim is made here for 3<=beta<4 using only E D<infinity.

## 2. Typical continuum routes are supported on the sampled major roads

For a fixed r and two independent space-time Poisson samples, let E_r^(1), E_r^(2) be their major-road sets, and let E_r^(12) be the set constructed from their union. The superposed sample, after deterministic time reparametrization, has the same law as the original sample. Thus E_r^(12) has intensity p/r, as does E_r^(1), while E_r^(1) is a subset of E_r^(12). Finiteness of expected length in bounded windows gives

 H^1((E_r^(12) minus E_r^(1)) intersect B)=0 almost surely      (4)

for every bounded B, simultaneously over a countable exhaustion.

Every route between points of the second sample has its r-truncated portion in E_r^(12). Hence its r-truncated portion outside E_r^(1) has zero length. Apply the elementary factorial Campbell formula to pairs in the second sample at time 1, independent of the first sample and of the route environment. On any bounded endpoint window Q this gives

 E integral_{Q x Q} H^1(R(x,y)^(r) minus E_r^(1)) dx dy=0.       (5)

Here R(x,y)^(r) denotes the route points at distance greater than r from both endpoints. Formula (JM) makes this nonnegative integral legitimate. Increasing Q and using a countable set of rational r proves: almost surely, for Lebesgue-almost every endpoint pair, all their rationally truncated route portions lie in E_r up to length-null sets. No continuity of routes in their endpoints is used.

This is the only continuum-support consequence needed below. It agrees with the intrinsic-major-road discussion and planted-point consequence in Aldous, Section 6.3. Finite-intensity superposition and Campbell/Tonelli are credited standard tools.

## 3. Far-away endpoints eventually cannot send a route through a fixed window

Fix R>=1 and consider traffic inside the disc B_R about zero. Let M_j=2^j with M_j>=4R, and put

             L_j=H^1(E_{M_j/2} intersect B_{2R}).

The intensity formula gives

             E L_j = 8 pi p R^2/M_j,
             P(L_j>=R)<=8 pi p R/M_j.                          (6)

The sum over j is finite. By the first Borel–Cantelli lemma, almost surely some finite j has L_j<R.

For that j, consider a typical endpoint pair satisfying |x|,|y|>=M_j. If its route meets B_R, a portion of the route from such a meeting point toward either endpoint must cross from B_R to the boundary of B_{2R}, and hence has length at least R in B_{2R}. Every point of that portion is at distance at least M_j-2R>=M_j/2 from both endpoints. To avoid any equality issue, choose M_j>4R; the resulting strict inequality puts this portion in R(x,y)^(M_j/2). By (5), it contributes at least R to L_j, a contradiction.

Therefore there is an almost surely finite random M such that, for almost every pair whose route has positive length in B_R, at least one endpoint lies in B_M. This is a uniform statement about typical pairs in that realization, derived from the sampled major-road length, not an unjustified inference from absence of one doubly infinite geodesic.

For any fixed epsilon>0 and r>0, writing L=H^1(E_r intersect B_R)<infinity, the contribution to (1) from |y-x|>=epsilon is consequently at most

 L integral integral |y-x|^(-beta) 1{|y-x|>=epsilon}
            [1{x in B_M}+1{y in B_M}] dx dy
       = L * 4 pi^2 M^2 epsilon^(2-beta)/(beta-2)<infinity       (7)

when beta>2. No moment of M or of the right side is required.

## 4. A deterministic tubular-neighborhood estimate for major roads

Fix r>0 and put a=r/8. Cover a bounded set A by finitely many discs B(q,a). For one such disc define

 K_q=E_r intersect B(q,a),
 J_q=H^1(E_{r/2} intersect B(q,2a))+4 pi a.

Every point w of K_q belongs to a sampled route with both endpoints farther than r from w. Follow this route from w until its first exit from B(q,2a). All points on the resulting connector are at distance at most 3a from w, and therefore farther than r-3a=5r/8>r/2 from the endpoints. The connector is contained in E_{r/2} intersect B(q,2a) and joins w to the outer circle.

For 0<delta<=a, choose a maximal delta-separated finite subset w_1,...,w_N of K_q. Such a finite maximal set exists by Euclidean packing in the bounded disc, even if K_q is not closed. Join these finitely many points to the outer circle by the connectors just described, and adjoin the whole outer circle. This makes a connected finite union of rectifiable curves, of length at most J_q. Inside each of the disjoint balls B(w_i,delta/3), that union has length at least delta/3: the distance from w_i along its connector runs through the interval [0,delta/3]. Therefore

             N<=3J_q/delta.

Maximality covers K_q by the delta-balls about these points. Its open delta-neighborhood is covered by N balls of radius 2delta, so

             |(K_q)^delta|<=12 pi J_q delta.                    (8)

Summing over the finite covering discs gives

 |(E_r intersect A)^delta|<=C_{A,r} delta,  0<delta<=r/8,        (9)

where C_{A,r}=12 pi sum_q J_q is finite almost surely. Moreover it has finite expectation by the major-road intensity formula. The proof controls possibly infinitely many tiny road components without assuming a finite component count or a locally finite vertex set. It does not apply the tube formula for one smooth curve to an arbitrary disconnected set.

## 5. Moment control of the short-trip singularity

Let A be bounded. For a displacement z of length t>0 put

 I_r(z)=E integral H^1(R(x,x+z) intersect E_r intersect A) dx.

Fix K>=1 with tK<=r/8, and split according to whether the full route length is at most tK.

On the short-length event, a positive contribution requires x to be within distance tK of E_r intersect A. Each contributing route has length at most tK. Hence (9) gives

 I_r(z; length<=tK) <= tK E|(E_r intersect A)^(tK)|
                    <= c_{A,r} t^2 K^2,                       (10)

where c_{A,r}=E C_{A,r}<infinity. There is no independence assumption between the route and E_r.

For the complementary event, discard E_r. Translation invariance and Tonelli give the mass-transport identity

 E integral H^1(R(x,x+z) intersect A) 1{len R(x,x+z)>tK} dx
   = |A| E[len R(0,z) 1{len R(0,z)>tK}]
   = |A| t E[D 1{D>K}].                                      (11)

To verify the first equality, translate the route at x to the origin inside the expectation and then integrate the indicator that a point of that translated route lands in A; the integral over x is exactly |A| for each route point. The last equality uses rotation and scale invariance, not an independent copy of the major-road process.

If E D^s<infinity for s>=1, then E[D 1{D>K}]<=K^(1-s) E D^s. Choose

             K=t^(-1/(s+1))

for sufficiently small t<1, so tK<=r/8. Equations (10)–(11) yield, uniformly in the direction of z,

             I_r(z)<=C t^(2s/(s+1)).                           (12)

Thus the expected short-trip contribution is bounded by

 2 pi C integral_0^epsilon t^(1-beta+2s/(s+1)) dt,

which is finite precisely in the strict range (2). Nonnegative finite expectation implies almost sure finiteness. Combining this with the pathwise large-trip estimate (7) proves local finiteness on bounded windows.

The same conclusion is obtained on a countable exhaustion by discs and rational r. Nestedness extends it to every r>0. If all moments are finite, take a countable sequence of s tending to infinity. Choose also a countable sequence of admissible beta exponents increasing to 4. On trips shorter than one, finiteness for a larger exponent implies finiteness for every smaller exponent. Together with (7), this gives one probability-one event of local finiteness for every beta in (2,4), not just one preselected exponent.

## 6. The beta=3 logarithmic endpoint

For beta=3 choose K=t^(-a) with any fixed 0<a<1/2. The integral of the contribution (10) is bounded by a constant times

             integral_0^epsilon t^(-2a) dt<infinity.

For (11), Tonelli and the substitution u=t^(-a) give

 integral_0^epsilon t^(-1) E[D 1{D>t^(-a)}] dt
    = (1/a) integral_{epsilon^(-a)}^infinity E[D 1{D>u}] du/u
    = (1/a) E[D log(D epsilon^a)_+],                            (13)

which is finite if E[D log(1+D)]<infinity. Here log(v)_+ means max(log v,0). This proves the endpoint statement under that stated additional moment condition.

## 7. Sigma-finiteness and scaling

By (5), almost every prescribed route, apart from its two endpoints and length-null sets, is contained in the union of E_{1/k}. The unrestricted nonnegative traffic integral therefore gives zero measure to the complement of that union. Its restriction to E_r equals (1), by Tonelli. The sets E_{1/k} intersect B_m form a countable cover of the support and each has finite traffic mass. This proves sigma-finiteness; the full traffic measure need not be locally finite in the ambient plane.

For a realization scaled by c, change variables x=cu,y=cv in the source-destination integral. The two endpoint area elements supply c^4, the kernel supplies c^(-beta), and route length supplies c. The resulting identity is

             T_beta[scaled network](A)
                  =c^(5-beta) T_beta[original network](A/c).

The network's scaling invariance in distribution then gives (3). For the locally finite restricted measures the corresponding relation pairs E_r with E_{cr}; this avoids treating the cutoff r as invariant under scaling.

## 8. Scope, comparison and remaining gap

The proof supplies general sufficient route-length moment regularity, not merely a calculation on one construction. It proves the local-finiteness assertion for every 2<beta<4 in the all-moments subclass, and therefore includes bounded-stretch constructions with a jointly measurable version. The binary-hierarchy stretch bound is existing source material. Kahn's established moments below gamma-1 yield only beta<4-2/gamma by this theorem, not the full interval for that model; the stronger moment conjecture in his Remark 5.1 is not used.

For the ordinary first-moment SIRSN assumptions, the range 3<=beta<4 remains open in this attempt. No implication to higher or logarithmic moments is asserted. In addition, existence of the jointly measurable route realization (JM) is explicitly distinguished from a process specified only by its finite-dimensional laws. The positive conclusion is a conditional answer of the type the 2012 question allows; it must not be advertised as an unconditional solution for all SIRSNs.

The proof uses credited intensity scaling, superposition/Campbell identities, Tonelli, elementary curve packing, Markov/Borel–Cantelli, and moment truncation. No historical-priority claim is made. Author count: 1/5. Best-guess completion of the unrestricted original-axiom goal: 45%, with the exact moment and continuum-version gaps stated above. Independent review is pending.
