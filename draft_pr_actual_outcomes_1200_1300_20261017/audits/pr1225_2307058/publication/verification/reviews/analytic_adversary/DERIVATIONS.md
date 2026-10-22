# Independent adversarial derivations for PR1225 / 2307058

These are newly authored checks of the pinned proof, not a transcription of the historical audit. The supplied PROOF.md/AUDIT.md were read before these checks, so this is candidate-aware adversarial verification. No findings from the separate source-question family were consulted. Mathematical review date: 2026-10-17 UTC.

## 1. Pointwise majorization survives dense infinite values

Let h be any nonnegative Borel integrable function on the compact rectangle Q. For A_k={h>2^k}, outer regularity gives relatively open O_k containing A_k with excess area at most 2^(-2k-4). Define H=1+sum_(k>=0) 2^(k+1) 1_(O_k). Each summand is lower semicontinuous, and an increasing supremum of lower semicontinuous functions is lower semicontinuous. For 2^m<h<=2^(m+1), the terms k=0,...,m already sum to 2^(m+2)-2, which exceeds h-1. At exact dyadic endpoints the sum k=0,...,m-1 is 2^(m+1)-2; together with 1 it dominates h=2^m for m>=1. The case h<=1 is immediate. If h=infinity, every term is present. Conversely the dyadic sum on A_k is at most 4h. Hence integral H <= |Q|+4 integral h+1/4. This verifies all thresholds, including infinite h.

An explicit stress class is r=infinity on D=Q intersect (rational x rational), zero elsewhere. D is dense and area-null. Choose open covers O_k of D with |O_k|<=2^(-2k-4). The same H is lower semicontinuous, infinite at every point of D, and integrable. In fact limsup O_k is null because sum |O_k| is finite; outside that limsup only finitely many summands are nonzero. There is no contradiction with density: a lower semicontinuous function may be infinite on a dense residual null set and finite on a meagre set of full area. Lower semicontinuity controls lower, not upper, neighboring values. An attempted objection that dense infinite values force infinite energy therefore fails.

The same construction handles infinity on the whole real-axis segment, or a dense union of rational vertical lines. Such densities cannot be replaced merely almost everywhere in an all-curves argument; the candidate retains them pointwise.

## 2. Expanded weighted-length compactness

For a continuous nonnegative a on Q, a rectifiable alpha:[0,1]->Q, and a partition P, set

S_P(alpha)=sum_i min_[t_(i-1),t_i](a composed alpha) times |alpha(t_i)-alpha(t_(i-1))|.

Always S_P<= integral_alpha a ds. Refinement increases S_P: each refined minimum is at least the old minimum, and the refined chord lengths dominate the old chord length. To see equality after taking the supremum, first choose a coarse time partition on whose intervals a composed alpha oscillates at most epsilon. On each interval choose further partition points whose chord sums approximate its total variation. This produces a lower sum within epsilon times length(alpha), plus an arbitrarily small variation approximation error times max a, of the weighted integral. Let both errors tend to zero. The minima and chords are continuous under uniform convergence of alpha, so the weighted integral is a supremum of continuous functions and hence lower semicontinuous.

For lower semicontinuous extended g>=0, define a_m(x)=min(m, inf_y(g(y)+m|x-y|)). The inner infimum, if finite, is m-Lipschitz. In the application g is finite somewhere because g is L2. The truncated expression is finite, continuous, nonnegative, and increasing in m. Also a_m<=g. If a_m(x) fails to tend to g(x), there is a finite C<g(x) and arbitrarily large m with a_m(x)<=C. For m>C the truncation is inactive. Choose y_m with g(y_m)+m|x-y_m|<=C+1/m. Nonnegativity forces y_m->x, whereas lower semicontinuity gives g(x)<=liminf g(y_m)<=C, a contradiction. This proof works also at g(x)=infinity. Monotone convergence on the arclength measure gives integral g=sup_m integral a_m, so its lower semicontinuity follows.

For distance sublevel sequences, g>=1 gives an ordinary-length bound. Curves of length at most K admit K-Lipschitz parametrizations on [0,1], including constant curves. Arzela-Ascoli yields a uniformly convergent subsequence. Compactness of E preserves the initial endpoint; compact Q prevents escape; lower semicontinuity of weighted length preserves the cost bound. Thus the extended path distance d really is lower semicontinuous, including at d=infinity. This step needs neither attainment of every infimum nor measurable selection of paths.

## 3. Actual line representatives and the trace

The path inequality is |u(x)-u(y)|<=integral_segment g ds for every coordinate segment. On any horizontal or vertical line where integral g is finite, take finitely many disjoint subintervals of total length delta. The sum of the corresponding u-increments is bounded by integral g over their union. Absolute continuity of the Lebesgue integral makes this arbitrarily small as delta->0. Thus the original pointwise u is absolutely continuous on the entire line segment, including its actual value at height zero. It is not merely equal almost everywhere to an unrelated line representative.

The coordinate derivative bounds give integral |gradient u|^2<=2 integral g^2. Borel bounded u is in L2; Fubini and line integration by parts give its weak derivatives. Multiplication by the smooth compact cutoff and extension by zero therefore yield w in W^(1,2)(R2). At every x on a good vertical line, the exact plate values give w(x,0)=1_E(x), including x outside [0,1] where either u=1 on the axis inside Q or the cutoff vanishes.

For compactly supported vertical ACL v, the elementary estimate

|v(x,0)|^2 <= 2 integral_(0,infinity) |v v_y| dy <= integral_(0,infinity)(|v|^2+|v_y|^2)dy

proves L2 convergence of actual traces under W1,2 mollification. Hence the smooth Fourier trace calculation transfers to this actual trace. No claim about conformal capacity of exceptional vertical lines is made. If E is null, all x in E may be exceptional without contradiction; the next argument is precisely what recovers the capacity conclusion.

For smooth compactly supported w, horizontal Fourier transformation gives

|xi| |W(xi,0)|^2 <= integral_(y>0)(xi^2 |W|^2+|W_y|^2)dy.

The factor at xi=0 is zero; no division is used. Plancherel and the trace-convergent mollification then give integral |xi| |fhat(xi)|^2 <= integral_(y>0)|gradient w|^2 for the general w. Tonelli, Plancherel and t=xi h yield

integral_R ||f(.+h)-f||_2^2 / h^2 dh = C integral_R |xi| |fhat(xi)|^2 dxi,

where C=integral_R |exp(it)-1|^2/t^2 dt is positive and finite. All quantities are nonnegative, so Tonelli remains valid before finiteness is known.

## 4. Independent translation rigidity check

Put A(h)=||1_E(.+h)-1_E||_1, equal to the squared L2 difference. For 0<h<1 and N=ceil(2/h), f and its Nh translate have disjoint supports because E is contained in [0,1] and Nh>=2. Translation invariance and telescoping give 2|E|<=N A(h). Since N<=3/h, A(h)>=2|E|h/3. Thus the critical seminorm dominates (2|E|/3) integral_(0,1) dh/h. This is infinite for every positive-length measurable E, including sets with no intervals. The argument imposes no boundary regularity on E and contains no geometric approximation of a fat Cantor set.

## 5. Initial endpoints, loops, singular parametrization, and finite augmented cost

Suppose a continuous connector, merely locally rectifiable on the interior of its parameter interval, has finite q-length with q>=1 before its first hit of S2. Every compact interior subcurve then has ordinary length at most the total q-cost. Taking expanding interior subintervals bounds their total variations uniformly. Adding endpoint limits preserves this bound: any partition including an endpoint can be approximated by interior partitions using continuity. Therefore the stopped curve is globally rectifiable, even if the original parametrization has singular speed or infinite endpoint variation was initially allowed.

Reparametrizing a continuous rectifiable curve by its cumulative variation removes constant intervals and yields an arclength curve alpha:[0,L]->R2 with length(alpha|[0,t])=t for every t. Line integrals of any nonnegative Borel density, including infinite values, are preserved. A curve of this kind cannot be constant on [0,t] for t>0. Thus m(t)=max_(s<=t)|alpha(s)-e|>0. For every radius 0<r<m(t), the first-exit time tau(r) is at most t. This proves tau(r)->0 as r->0 without simplicity, a nonzero derivative at the endpoint, monotone radial motion, or finitely many returns to e.

If integral q(alpha(s))ds is finite, absolute continuity of this one-dimensional integral gives integral_(0,tau(r)) q(alpha(s))ds->0. Infinite q values at isolated or arclength-null visits do not change it. If q=infinity on a positive arclength set, finite-cost supposition already fails. Initial pauses have zero arclength and contribute zero even when q(e)=infinity.

A concrete hostile path is a concatenation, beginning at time zero, of small loops at e with sizes 2^(-k) in reverse order k=infinity,...,1, followed by a connector to S2. The total loop lengths are summable, yet every initial parameter neighborhood contains infinitely many loops and returns to e. The m(t) argument still proves first-exit times tend to zero. If loop lengths instead have a divergent sum, q>=1 makes the cost infinite and the proof never reparametrizes under a false finite-cost assumption.

## 6. Good radii and every endpoint

Fix the actual e in E used by the hypothetical finite-cost connector. Polar integration about this particular point gives integral_(0,delta) A(r)dr<infinity for A(r)=integral_circle(e,r) q^2 ds. The set of radii with e+r in E is null because it is a translate of E intersected with (0,infinity). The set where A(r)=infinity is also null. Let G be the remaining full-measure set of radii. If, for some epsilon,delta>0, r A(r)>=epsilon on G intersect (0,delta), then integral A(r)dr>=epsilon integral_(G intersect (0,delta)) dr/r=infinity. Removing a Lebesgue-null set does not change the integral on any interval bounded away from zero, hence does not remove its logarithmic divergence. Contradiction.

Choose recursively r_j in G with r_j<min(1/j,r_(j-1)/2) and r_j A(r_j)<1/j^2. Each full-circle q-length is at most sqrt(2 pi r_j A(r_j))<=sqrt(2 pi)/j. Combine it with the initial finite-cost segment from e to the first exit. Their sum tends to zero. Either circular arc from that exit point to e+r_j is globally rectifiable and has no larger cost than the full circle. The concatenation is an actual E-to-F connector. If the exit point is already e+r_j, the circular part may be constant and has zero cost.

The proof fixes e before selecting radii. No exceptional set of endpoints, uniform family of radii, trace pointwise continuity, or simultaneous polar Fubini claim over E is needed. The density may have infinite values on arbitrary area-null sets, but finite A(r_j) ensures circle Cauchy-Schwarz remains valid; any infinities left on an arclength-null part have zero integral.

## 7. Limiting and consistency checks

Empty E: the outer connecting family is empty, so zero density gives zero modulus and the positive premise is false.

Singleton E={0}: take rho(z)=1/(|z| log(1/|z|)) for 0<|z|<exp(-1), rho(0)=infinity, and zero outside this disk. Its planar energy is 2 pi integral_(0,exp(-1)) dr/(r log^2(1/r))=2 pi. Every connector from 0 to any nonzero point has infinite rho-length: for any annular truncation use the primitive of this radial profile and the one-Lipschitz radial function to bound curve cost below by the radial integral, then let the inner radius tend to zero. Thus a nonempty polar compact set can admit finite-energy E-to-F densities. This does not contradict the theorem: every E-to-S2 connector has infinite cost as well, and rho/n proves its outer modulus is zero. Merely putting rho=infinity at the endpoint, with no radial halo, would not have this effect.

Interval E=[0,1]: for r in (0,1), the upper semicircle about 0 joining r in E to -r in F is an admissible test curve. Cauchy-Schwarz forces integral_arc rho^2 ds>=1/(pi r); polar integration over r makes every admissible energy infinite. This independently confirms a nontrivial positive-length boundary case, but is not used to infer the general positive-length case.

Final scaling: q=rho+1_B(0,3) obeys integral q^2 <=2 integral rho^2+18 pi<infinity. Every E-to-S2 curve has infinite q-cost by the preceding argument. For each integer n>=1, its q/n cost is still infinity, so q/n is admissible for the entire outer family. Its energy is n^(-2) integral q^2, tending to zero. The admissible family is never weakened by removing curves or switching to almost-every-curve admissibility. Finite outer-cost candidates force global rectifiability before the circle argument; infinite augmented-cost curves already satisfy final admissibility.

## 8. Scope

The analytic chain validates the full compact-set implication under the manuscript's stated curve and extended-Borel-density conventions. It actually needs only globally rectifiable E-to-F test curves, and it tests every locally rectifiable-away-from-endpoints E-to-S2 curve. It therefore proves both explicitly stated consistent conventions. The original source does not separately formalize every endpoint convention; additional interpretations of undefined terminology, arbitrary non-locally-rectifiable parametrized paths, and priority questions are not silently certified.

No numerical experiment or finite enumeration was performed: no such check can establish the universal analytic claims here. The explicit examples above are falsification attempts and boundary consistency derivations, not replacements for proof. No repairable or irreparable mathematical flaw was found.
