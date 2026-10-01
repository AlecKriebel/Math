# Author turn 4: an l1 stochastic-approximation bridge

**Partial theorem for summably decaying rates. It does not prove stochastic percolation.**

The failure of uniform relative entry in turn3 need not destroy every stochastic-approximation approach. This turn establishes a weaker-topology bridge for the actual unit-start process. It applies to the constructed rate field and, more generally, to the following class.

Let G be a countable graph with no isolated vertices and maximal degree D<infinity, with strictly positive rates p(v) and sum_v sqrt(p(v))<infinity. Take alpha=2 and all initial tallies one. Let P=sum_v p(v)<infinity, lambda_e=p(u)+p(v) for e={u,v}, and define A_e(t)=N_e(t)-1 and Z_e(t)=A_e(t)/t for t>0. The rates and degree ensure the standard WARM construction is well-defined. Summability makes the total clock process finite-rate.

## 1. l1 noise is sublinear

Write

A_e(t)= integral_0^t f_e(N(s)) ds + M_e(t),

where f_e is the actual conditional reinforcement intensity, and M_e the compensated counting martingale. The edge intensity is at most lambda_e, so its predictable quadratic variation has expectation at most lambda_e t. Doob's L2 inequality and Cauchy–Schwarz give

E[sup_(s≤T)|M_e(s)|] ≤ 2 sqrt(lambda_e T).

Moreover,

sum_e sqrt(lambda_e) ≤ sum_e [sqrt(p(u))+sqrt(p(v))] ≤ D sum_v sqrt(p(v)) < infinity.

Tonelli therefore yields an l1 maximal bound C sqrt(T), with finite C. Markov's inequality on dyadic T=2^k has a summable bound C/(epsilon sqrt(T)). Borel–Cantelli, first for rational epsilon>0 and then by monotonicity between dyadic times, proves

||M(t)||_1/t →0 almost surely,

with the analogous uniform estimate on every interval[t,ct] for fixed finite c. This argument does not assume independence between edge martingales. They are all driven by the interacting process; only their compensator bounds are used.

For a fixed logarithmic-time window h∈[0,H], integration by parts consequently gives

sup_h || integral_t^(t exp(h)) dM(s)/s ||_1 →0.

Indeed it is bounded by the two endpoint ratios plus the integral of ||M(s)||_1/s², which is at most(2+H) sup_(s≥t)||M(s)||_1/s.

## 2. Asymptotic compactness and the correct domain

The total number of rings divided by t converges almost surely to P. Since every ring increments exactly one edge, ||Z(t)||_1→P. If Q_v(t) is the number of rings at v, then

A_e(t)≤Q_u(t)+Q_v(t),

sum_(e incident to v) A_e(t)≥Q_v(t).

Thus any coordinatewise limit x satisfies x_e≤lambda_e and sum_(e incident to v)x_e≥p(v).

The family Z(t), for large t, is precompact in l1. To see this, take a finite vertex set B and retain every edge incident to B, a finite set. Any omitted edge has both endpoints outside B, so its total increment count is at most D sum_(v outside B) Q_v(t). The latter sum is a Poisson process with finite rate sum_(v outside B)p(v). Along a countable exhaustion, its strong law holds simultaneously. The resulting limsup tail bound tends to zero as B increases. Together with bounded total mass and finite-coordinate boundedness, this is precisely asymptotic l1 compactness.

Every limit belongs to the set

K={x in l1(E): 0≤x_e≤lambda_e; sum_e x_e=P; sum_(e incident to v)x_e≥p(v) for every v}.

K is convex and compact in l1: it is closed, and the coordinate envelope lambda is summable. The constructed equilibrium of turn2 belongs to K. In general K is nonempty because the preceding precompactness argument supplies a limit point. Also dist_l1(Z(t),K)→0; otherwise a subsequence bounded away from K would have a limit in K.

## 3. The infinite ODE is well-posed on K

For x in K let S_v(x)=sum_(e incident to v)x_e². Its local sum is at least p(v)>0, so S_v(x)>0. Define

f_e(x)=sum_(v incident to e) p(v)x_e²/S_v(x), and F(x)=f(x)-x.

The map f sends K to K. Nonnegativity and the bound f_e≤lambda_e are immediate. Summing by vertices gives sum_e f_e=P. Summing incident to one vertex v includes all of v's own contribution, exactly p(v), plus nonnegative neighbor contributions, giving the required local lower bound.

It is also globally Lipschitz on K in l1, with constant at most8D. For one vertex v and incident coordinate j, the l1 norm of the column derivative of its probability vector a_e=x_e²/S_v is

4x_j(1-a_j)/S_v ≤ 4D / sum_(e incident to v)x_e.

Here S_v≥(sum x_e)²/D and x_j≤sum x_e. Multiplication by p(v) bounds that column contribution by4D on K. Each edge coordinate belongs to two vertices, so the full column bound is8D. Integrate along the segment in convex K and use Tonelli to obtain the l1 Lipschitz estimate. Therefore F has Lipschitz constant at most1+8D.

Euler steps with step size at most1 are convex combinations of x and f(x) and remain in K. Standard Picard/Euler arguments on this closed convex invariant domain give a unique global forward flow in K. No uniform positive lower bound on p is needed.

## 4. The unit baseline produces a vanishing l1 drift error

The true reinforcement probabilities depend on N_e(t), equivalently on Z_e(t)+1/t. Define f(Z) using the same local formula when a vertex has nonzero incident sum, and choose the uniform distribution at an all-zero star. This auxiliary definition outside K only supplies a bounded finite-time formula; no continuity there is asserted.

For each fixed vertex v, its own clock guarantees

sum_(e incident to v) Z_e(t)≥Q_v(t)/t→p(v)>0.

Adding1/t to each incident coordinate therefore changes its finite probability vector by a quantity tending to zero. The l1 difference of any two such probability vectors is at most2. Dominated convergence with the summable vertex weights p(v) gives

||f(Z(t)+1/t)-f(Z(t))||_1→0 almost surely.

The notation Z+1/t is coordinatewise and need not define an l1 vector; the intensity expression is still meaningful and summable because its total mass is P. This distinction avoids an illicit infinite-baseline norm calculation.

## 5. Limiting paths solve the ODE

Set t=exp(tau). Counting-process integration gives the exact integral equation on bounded tau windows with drift F, the vanishing baseline error above, and the vanishing integrated martingale noise from Section1. The l1 drift norm is bounded by P+||Z||_1, hence is eventually bounded. Together with asymptotic compactness, this gives asymptotic equicontinuity of the shifted paths.

Given any tau_n→infinity, a further subsequence of Z(exp(tau_n+h)) converges uniformly on every fixed bounded h interval to a K-valued continuous path. The intensity map is continuous along this convergence: for finitely many vertices the positive limiting local sums make the rational expressions continuous uniformly in h, and the remaining contribution has norm at most the summable tail of p. Passing to the integral equation shows that the limit path solves x'=F(x).

Equivalently, after choosing points of K at vanishing l1 distance from each starting state, these shifted paths asymptotically follow the unique K-flow on every fixed logarithmic-time interval. This is the precise stochastic-approximation conclusion established here. It is not a claim of convergence to a particular equilibrium.

## 6. Application and remaining gap

The rates in turn2 satisfy sum sqrt(p)<infinity by geometric summation on the line and off-line lattice. Thus this theorem genuinely applies to the unit-initialized candidate process. It bypasses the impossible relative-basin entry by using l1 and a compact invariant domain instead.

The unresolved step is substantial: the percolating equilibrium's attraction was proved only in a relative neighborhood on its invariant support face, not in an l1 neighborhood of K. Far-tail changes can have very small l1 norm while being order-one relative changes, and the eventual graph may be altered by them. The present theorem does not show positive probability of percolation, uniqueness of an infinite component, or convergence to any prescribed equilibrium.

Four substantive author turns are complete. One remains unless the original stochastic target is resolved sooner. Completion estimate20%. Next substantive route: analyze an l1-valid Lyapunov or stability criterion on K and determine whether it can distinguish the percolating equilibrium from finite-component alternatives.
