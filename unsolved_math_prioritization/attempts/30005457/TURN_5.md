# Author turn 5: Lyapunov control and nearby nonpercolating equilibria

**Final scoped partial results. The original stochastic existence and uniqueness questions remain unresolved after five substantive author turns.**

This final turn attacks the remaining inference from l1 limiting dynamics to a percolating random support. Two precise results emerge: a strict deterministic Lyapunov function on the compact domain, and an obstruction to inferring percolation from proximity to the explicit infinite-component equilibrium.

## 1. A continuous strict Lyapunov function on K

Use the assumptions and compact invariant domain K of turn4, and alpha=2. Define

L(x) = -sum_e x_e + (1/2) sum_v p(v) log S_v(x),

where S_v(x)=sum_(e incident to v)x_e². The rate weights are essential; this formula is verified directly and does not import an unweighted finite-graph expression for unequal rates.

Let pmax=sup_v p(v)<infinity. On K,

p(v)²/D ≤ S_v(x) ≤ D(2pmax)².

Also sum_v p(v)|log p(v)|<infinity: for small p, p|log p| is bounded by a constant times sqrt(p), and only finitely many rates exceed any fixed positive threshold. Hence the series defining L converges uniformly on K, by a summable bound independent of x. It is a continuous real-valued function there.

For an edge e, define

g_e(x)=-1+sum_(v incident to e) p(v)x_e/S_v(x).

This is meaningful also at x_e=0, where it equals-1. The flow satisfies F_e(x)=x_e g_e(x). The same local-star lower bounds as in turn4 give |g_e(x)|≤1+2D. Along any K-valued ODE solution, termwise differentiation is justified: the absolute derivative of the v term is bounded by p(v)(1+2D), and the edge terms are summable. Therefore

dL/dtau = sum_e F_e(x)g_e(x) = sum_e x_e g_e(x)².

This is nonnegative and vanishes precisely at an equilibrium. The dissipation is continuous on K, since each summand is continuous and bounded by(1+2D)² lambda_e with a summable envelope.

It follows by the compact-domain LaSalle argument that every deterministic K-flow orbit has all its omega-limit points in the equilibrium set. Indeed a nonequilibrium limit point would have a neighborhood with positive dissipation, and repeated visits of a uniformly positive duration would force unbounded increases of the bounded function L.

This deterministic conclusion is not automatically a stochastic LaSalle theorem. Turn4 identifies all finite-window limiting paths, but without additional control it does not prove that the random trajectory selects an equilibrium or that its whole limit set lies at one Lyapunov level. In particular, no finiteness or discreteness of critical values in this infinite system has been established.

## 2. Finite-component equilibria arbitrarily close to the percolating one

Keep exactly the alpha2, q=1/16 rates of turn2; do not change them with the approximation index. Let x* be that turn's percolating equilibrium. For each integer M≥2, replace its line support by:

- one finite central path on the vertices(-M,0),..., (M,0)
- dimers pairing(M+1+2j,0) with(M+2+2j,0), for j≥0
- reflected dimers on the negative tail

All off-line dimers remain unchanged. All other edges have weight zero. We now prove that this support carries an equilibrium y^(M), with the central path weights close to x*.

### 2.1 Existence of the central path equilibrium

Write x^M for the restriction of x* to the2M central edges. Use the finite WARM drift with the original rates at the2M+1 central vertices. The only changes at x^M are at the two endpoint vertices: each now gives all its reinforcement to its sole retained edge instead of the fraction1/(1+q²).

Consequently the residual on each of the two endpoint edges is

r_M = p(M,0) q²/(1+q²) = q^(M+1)/(1+q),

and every other residual is zero. The corresponding relative residual is

r_M / q^(M-1) = q²/(1+q) = 1/272.

Consider the relative box |h_e|≤eta=1/100 about x^M. At the endpoint vertices, the derivative of the reinforcing term is now zero. At every other vertex it is the same two-edge derivative as in turn2. Removing an endpoint derivative cannot increase the positive diagonal correction plus the absolute off-diagonal row sum. Thus the relative l-infinity logarithmic norm remains at most-2/3 throughout this box.

The upper right derivative of ||h||_infinity is therefore at most

-(2/3)||h||_infinity + 1/272.

At the box boundary this is strictly negative, since1/272<1/150. Hence the compact box is positively invariant. Its time-one map is a strict contraction and maps the box to itself, so it has a unique fixed point. Every time-s flow maps that fixed point to another time-one fixed point; uniqueness forces it to be stationary. Thus the finite path has a positive equilibrium y^M inside the box.

### 2.2 An l1 bound that tends to zero

A relative-box bound alone would not suffice, since its radius is independent of M. We also need an absolute estimate. For this finite path the sum of all reinforcement intensities is constant, the sum of its vertex rates. Therefore each column of the drift Jacobian sums to-1. Its off-diagonal entries are nonpositive, and if D_e(h) is the nonnegative diagonal correction, its l1 column measure is exactly-1+2D_e(h).

The same ratio bounds used in turn2 give

2D_e(h) ≤ [2Dmax/(1-eta)] [(1+eta)/(1-eta)]^4 <1/3,

with Dmax=32/257. Thus the ordinary l1 logarithmic norm is also at most-2/3 on the relative box. Comparing the trajectory started at x^M to the constant reference x^M, whose residual has l1 norm2r_M, and then passing to the equilibrium gives

||y^M-x^M||_1 ≤ (3/2)(2r_M) = 3q^(M+1)/(1+q).

This estimate follows directly from the differential inequality u'≤-(2/3)u+2r_M. The reference and the trajectory remain in the convex box, so the uniform Jacobian estimate applies to their segment.

### 2.3 Extend over the tails and compare

Each tail dimer with endpoints u,v has exact equilibrium weight p(u)+p(v). Give all unused edges zero weight, and retain every off-line dimer of x*. Every vertex still has a positive supported incident edge, so every denominator in the full lattice drift is positive. The assembled y^(M) is an exact equilibrium of the full unchanged-rate system. Its components are the finite central path and dimers; none is infinite.

The old weights on both discarded line tails have total2q^M/(1-q), including the two cut edges. The new tail dimer weights have total2Cq^M/(1-q), where C=(1+q²)/(1+q). Therefore

||y^(M)-x*||_1 ≤ 3q^(M+1)/(1+q) + 2(1+C)q^M/(1-q) →0.

Every such equilibrium belongs to K by the general equilibrium identities. Thus **the percolating equilibrium is an l1 limit of nonpercolating equilibria with exactly the same rates**.

## 3. Consequence for the attempted stochastic construction

No l1 neighborhood of x* can force infinite support components, and no l1 neighborhood can be a basin in which every deterministic trajectory converges to x*, because it contains other stationary points y^(M). This explains why the relative-face attraction theorem from turn2 does not supply the missing open percolating basin in turn4's stochastic topology.

It does not prove that the random process converges to one of the finite-component equilibria, nor exclude percolation by a different mechanism. The actual stochastic support selection may depend on tail events not settled by the deterministic Lyapunov or compactness results. No probability of attaining x* or of avoiding it has been established.

## 4. Final disposition

The strongest completed package comprises the geometric tree-transfer obstruction, an explicit face-stable percolating deterministic equilibrium, a precise finite-time relative-entry obstruction, an l1 stochastic limiting-trajectory theorem, and the Lyapunov/nearby-finite-equilibrium results above.

There is still no construction of an infinite surviving component with positive probability from standard all-one tallies on any Z^d, and no impossibility proof for the allowed bounded positive rate fields with infimum zero. The source's additional uniqueness question also remains unanswered. The original target is therefore **unsolved after5/5 substantive author turns**, pending independent review of these scoped partial results. No fresh search route should be continued beyond this frozen budget without a materially new authorized basis. Completion estimate20% toward the original question; all five attempted routes have precise endpoints.
