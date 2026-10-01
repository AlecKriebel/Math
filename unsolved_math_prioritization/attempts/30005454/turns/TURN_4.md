# Substantive turn 4: conservative diffusion and deterministic phase envelopes

2026-10-01 06:50–07:00 UTC. Unit-initialized critical WARM on Z. Unreviewed partial reductions. The missing temporal convergence is not proved. Estimated full-target completion: 55%.

The previous turn proves Z_i+Z_{i+1}->2 almost surely, where Z_i=N_i/(t+1). This turn analyzes the remaining time-dependent alternating phase without treating a weak limit as ergodic.

## 1. The pathwise envelopes are deterministic

For every fixed i, telescoping adjacent sums gives Z_{i+2}-Z_i->0. Thus the liminf values on all even edges agree pathwise, and their limsup values also agree. Both are measurable functions of the iid marked-clock environment that are invariant under spatial translation by two. That transformation is ergodic. Therefore there are deterministic constants a_-,a_+ with

    liminf Z_(2i)(t)=a_-,  limsup Z_(2i)(t)=a_+

almost surely for every i. Adjacent-sum convergence gives odd-edge envelopes 2-a_+ and 2-a_-. The original law is also invariant under translation by one, so

    a_+=2-a_-,    0<=a_-<=1<=a_+<=2.

This is a valid use of ergodicity of actual pathwise envelopes. It does not force a_-=a_+, and does not imply a uniform spatial approximation along a subsequence. A nonconvergence scenario would have to oscillate through the same deterministic envelope interval at every fixed location.

## 2. Exact parabolic form of the limiting ODE

In logarithmic time the deterministic normalized drift is

    z_i'=z_i[1/(z_(i-1)+z_i)+1/(z_i+z_(i+1))-1].

Set s_i=(-1)^i and u_i=s_i(z_i-1). Direct algebra gives

    u_i' = sum_(j=i-1,i+1) a_ij(u)(u_j-u_i),
    a_ij(u)=z_i/[2(z_i+z_j)] >0.                    (1)

Thus this is a cooperative nearest-neighbor diffusion in the staggered affine variable. The two directed coefficients of an edge satisfy a_ij+a_ji=1/2. The maximum principle holds whenever a bounded positive deterministic solution is considered. In particular an initial bound epsilon<=z_i<=2-epsilon is preserved: then u_i lies between -1+epsilon and 1-epsilon, and comparison with these constant staggered equilibria preserves those bounds.

This is **not** yet a representation of the stochastic solution by a fixed heat kernel. Its coefficients are endogenous. The current stochastic estimates do not provide one spatially uniform positive lower bound on all z_i at all late times, so a uniformly elliptic infinite-volume estimate cannot simply be assumed.

Linearization at z_i=1 gives

    y_i'=-(y_(i-1)+2y_i+y_(i+1))/4,
    u_i'=(u_(i-1)-2u_i+u_(i+1))/4.

The infinite-line Fourier decay rate is sin^2(theta/2), which has no positive spectral gap. On an even cycle of length L the smallest nonzero rate is sin^2(pi/L). Hence relaxation estimates based on a fixed finite-cycle spectral gap are not uniform as L grows; logarithmic-time relaxation can cost order L^2 already in the linearized problem. This calculation diagnoses a nonuniform-limit obstacle, not a proof of the nonlinear stochastic convergence rate.

## 3. Conservative logarithmic coordinates

For a positive ODE solution set v_i=s_i log z_i and

    F_i(v)=s_i[1/(z_i+z_(i+1))-1/2].

Then exactly

    v_i'=F_i-F_(i-1).                              (2)

The flux is nonincreasing in v_i and nondecreasing in v_(i+1):

    partial_(v_i) F_i=-z_i/(z_i+z_(i+1))^2,
    partial_(v_(i+1)) F_i=z_(i+1)/(z_i+z_(i+1))^2.

Thus the logarithmic system is cooperative and conservative. Its local convex potential can be written

    phi_i(v)=exp(s_i v)-s_i v,
    phi_i'(v)=s_i(z_i-1)=u_i,
    F_i=(u_(i+1)-u_i)/[2(z_i+z_(i+1))].

These identities explain the dissipative structure, but they do not supply an infinite-volume Poincare inequality or an integrable local neutral drift.

For finite even periodic systems the alternating sum of the logarithmic coordinates is conserved by the deterministic ODE. In the actual integer-count process the exact counterpart is the harmonic martingale from turn 3; it is not legitimate to replace it with an exactly conserved stochastic log product.

## 4. Precise one-coordinate convergence criterion

The exact harmonic difference satisfies

 h(N_0(t))-h(N_1(t))
   =M_0(t)-M_1(t)+ integral_0^t [1/S_(-1)(s)-1/S_1(s)] ds.   (3)

Because the two martingales converge, the following condition is sufficient for the desired full conclusion in the unit model:

    integral_0^t [1/S_(-1)(s)-1/S_1(s)] ds
    has a finite limit almost surely.                       (4)

Indeed (3) would then make log(N_0/N_1) converge to a finite value, since both counts diverge and h(n)-log n->gamma. Together with Z_0+Z_1->2, this gives limits for Z_0 and Z_1 in (0,2); the adjacent-sum theorem propagates them to every edge. Turn 1 then forces the limit to be one by shift-two ergodicity. Conversely, the full desired convergence makes the harmonic difference converge, so (3) forces the boundary integral to converge as well. Thus this is an exact reduction, not an independently established solution.

The previous L2 estimates do not prove (4). For example the deterministic function cos(log(1+tau))/(1+tau) is square-integrable on the positive half-line, but its indefinite integral sin(log(1+tau)) has no limit. This is only a counterexample to the proposed inference from L2 to convergence, not a counterexample to WARM.

## What was attempted and remains blocked

The conservative/monotone representation suggests an infinite-volume contraction or a spatial-averaging argument. Fixed heat-kernel estimates cannot be transplanted without controlling endogenous degeneracy; finite-cycle limits cannot be interchanged with infinite volume using a nonuniform spectral gap; and vanishing local drift does not integrate automatically. No existing primary theorem was verified whose hypotheses close these gaps for the present stochastic field.

The fifth turn will combine the exact alternating block martingales with the finite pair-dissipation integral, looking for a controlled simultaneous space-time limit. If that gives only a subsequence theorem, it must remain a partial result rather than be described as full almost-sure convergence.
