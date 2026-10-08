# Explicit fixed-flux cases: an interval and radial data on a ball

These are separately identified special cases of the continuum DMK problem. They do not settle unrestricted multidimensional convergence. The calculation is elementary and no novelty or priority is claimed. The underlying model and local regularity framework are credited to Facca–Cardin–Putti, https://doi.org/10.1137/16M1098383 and https://arxiv.org/abs/1610.06325.

## Interval theorem

Let Ω=(a,b), f∈L∞(a,b), ∫f=0, and μ₀∈C^δ([a,b]) with min μ₀>0, 0<δ<1. Set

    F(x)=−∫ₐˣ f(s)ds,           ρ(x)=|F(x)|,
    μ(t,x)=e^(−t)μ₀(x)+(1−e^(−t))ρ(x),
    u_x(t,x)=F(x)/μ(t,x),       ∫ₐᵇu(t,x)dx=0.

These formulas give a global solution in the local theory's regularity class on every finite time interval. The Neumann elliptic equation implies (μu_x)'=−f and μu_x(a)=0, hence μu_x=F. The other endpoint condition follows from ∫f=0. Therefore the density equation is the linear pointwise equation μ_t=|F|−μ, whose solution is the displayed formula. Positivity holds at every finite time. Since F is Lipschitz and μ₀ is Hölder, μ(t) is Hölder and u(t) is C^(1,δ) for finite t. These calculations also prove uniqueness in this class.

As t→∞,

    ||μ(t)−ρ||_{C^δ}=e^(−t)||μ₀−ρ||_{C^δ},
    u_x(t,x)→v(x):=sign F(x), with sign 0=0,
    u(t)→u_* uniformly and in W^(1,p), for every finite p≥1,

where u_* is the mean-zero primitive of v. For the gradient claim, convergence is pointwise. For t≥log 2,

    |F|/μ(t) ≤ 1/(1−e^(−t)) ≤2,

so dominated convergence gives convergence in every finite Lp. For primitives, subtracting their spatial means bounds the sup norm by twice the L1 norm of the gradient difference. The limit is 1-Lipschitz, and ρu_*'=F almost everywhere. It solves the MK equations. Primal-dual equality is explicit:

    ∫ f u_* = ∫ Fv = ∫|F|.

Consequently F is an optimal feasible flux and ρ is its transport density.

This is not a uniform-gradient convergence assertion. Sign changes of F can give a discontinuous limiting gradient. On an open interval where F=0, the dynamics selects u_*'=0. Other mean-zero 1-Lipschitz MK potentials can have different derivatives there; no uniqueness of the whole potential is presumed.

## Radial theorem on a ball

Let Ω=B_R(0)⊂R^d, d≥2. Assume f(x)=h(|x|) is bounded and radial with zero total integral, and μ₀(x)=m₀(|x|)>0 is radial and C^δ. Define

    Q(r)=−r^(1−d)∫₀ʳ s^(d−1)h(s)ds,     r>0,
    Q(0)=0,          ρ(r)=|Q(r)|.

The zero-mean condition gives Q(R)=0. Also |Q(r)|≤||h||∞r/d, and

    Q'(r)=−h(r)−(d−1)Q(r)/r

almost everywhere, so Q is Lipschitz. The displayed formulas below directly construct a radial solution. Any already existing regular solution with these radial data is radial as well: compare it with each rotation and use the L2 uniqueness estimate proved in `continuation.md`. This argument uses positivity and elliptic gradient bounds on compact time intervals, not the source's disputed generic C^δ modulus-Lipschitz step. The radial divergence equation and regularity at the origin force

    μ(t,r)u_r(t,r)=Q(r).

Thus exactly as on the interval,

    μ(t,r)=e^(−t)m₀(r)+(1−e^(−t))|Q(r)|,
    u_r(t,r)=Q(r)/μ(t,r),

with the additive constant chosen so that ∫_{B_R}u=0. The formula supplies global continuation and the same exponential C^δ density convergence. At finite times u_r=O(r) near the origin, so the radial gradient is continuous there; the standard Hölder quotient estimates give the local regularity class.

The mean-zero potential converges uniformly and in W^(1,p)(B_R) for every finite p. Uniform convergence follows by integrating the radial derivative difference on [0,R], where it is bounded by an integrable constant for large t. The limit has radial derivative sign Q and is 1-Lipschitz on the ball.

The limiting radial flux q_*=Q(r)e_r is feasible, has zero normal component on the boundary, and satisfies q_*·∇u_*=|Q| almost everywhere. Therefore

    ∫_{B_R} f u_* = ∫_{B_R}|q_*|.

This certifies optimality against all feasible fluxes, not only radial competitors: for any feasible q, testing with the 1-Lipschitz u_* gives ∫f u_*≤∫|q|. The explicit radial density is consequently an optimal transport density for the full spatial problem.

## Why this route stops short

In one dimension and in the radial class, divergence and boundary conditions fix the flux independently of μ. In general dimensions they do not: divergence-free components remain, and the conductivity-dependent elliptic problem selects among them. The exact linear density evolution used here is therefore unavailable for unrestricted data. It would be incorrect to promote either theorem to a resolution of the original multidimensional conjecture.
