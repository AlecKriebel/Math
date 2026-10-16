# Potential selection and a boundary-case counterexample

This note tests whether convergence of the transport density and vanishing energy dissipation suffice for convergence of the entire mean-zero potential. It gives a precise obstruction after strict positivity of the initial density is dropped. It is not a counterexample to the original strictly positive-density conjecture. It does not exploit an additive-constant gauge or change the topology of the domain.

## A necessary property of any strong potential limit

Suppose a global regular solution has μ₀>0 continuous, uniformly bounded total mass, and ∇u(t) converges uniformly to ∇u_∞ on the closure of its domain. Then |∇u_∞|≤1 everywhere.

If instead |∇u_∞(x₀)|>1, continuity and uniform convergence produce an interior set B of positive volume, a time T, and η>0 such that |∇u(t,x)|≥1+η on B for all t≥T. The reaction equation gives

    μ(t,x)≥μ(T,x)e^{η(t−T)}  on B.

Since μ(T) has a positive minimum on B, its mass diverges, a contradiction. A boundary point with gradient norm greater than one also produces such an interior set by continuity. This observation identifies a property of an already existing strong limit. It supplies neither compactness nor convergence to that limit.

## Exact nonconvergent potentials in the enlarged degenerate class

Take Ω=(0,1), and set

    ρ(x)=[(x−1/4)(1/2−x)]²,  for 1/4≤x≤1/2,
    ρ(x)=0,                 otherwise,
    f(x)=−ρ'(x).

Then ρ is C1 and nonnegative, f is bounded with compact support in Ω, and ∫f=0. Define the continuous piecewise-linear function

    h(x)=4x,      0≤x≤1/4;
    h(x)=1,       1/4≤x≤1/2;
    h(x)=3−4x,    1/2≤x≤3/4;
    h(x)=0,       3/4≤x≤1.

Let V(x)=∫₀ˣh(s)ds and let V₀ be V with its spatial mean subtracted. Finally set

    w(x)=(x−3/4)²(1−x)²,  for 3/4≤x≤1,
    w(x)=0,              otherwise,
    w₀=w−∫₀¹w(x)dx.

The function w is C1, nonconstant, and has derivative supported in [3/4,1]. With s=x−3/4 and L=1/4,

    w'=2s(L−s)(L−2s),
    |w'|≤2(L²/4)L=1/128.

For any differentiable a:[0,∞)→[−1,1], put

    μ(t,x)=ρ(x),       u(t,x)=V₀(x)+a(t)w₀(x).

Both potentials are mean zero. Where ρ>0, h=1 and w'=0, hence u_x=1. Everywhere else ρ=0. Thus

    μu_x=ρ,
    −(μu_x)'=f,
    μ_t=0=μ(|u_x|−1),

and the zero-flux boundary conditions hold. Moreover |u_x|≤1: where h is nonzero, w'=0 and 0≤h≤1; where w' is nonzero, h=0 and |a w'|≤1/128. Every u(t) is therefore an MK potential and every pair (ρ,u(t)) satisfies the displayed degenerate DMK equations. The density has already reached its optimal value and all density-energy dissipation vanishes.

Choose a(t)=sin(log(1+t)). Along

    t_k=exp(π/2+2πk)−1,
    s_k=exp(3π/2+2πk)−1,

the potentials are respectively V₀+w₀ and V₀−w₀. Since w₀ is nonconstant, these limits differ in every Lp and in the uniform norm. There is no whole-potential convergence, despite the fixed mean-zero gauge. Even ∫₀∞||u_t||²₂dt is finite, because |a'(t)|≤1/(1+t).

This is an exact counterexample only to a broadened statement permitting μ₀ to vanish. It is excluded by min μ₀>0 in the original local theory. No approximation or limiting argument here upgrades it to a positive-initial-density counterexample.

## Consequence for the proof programme

The elliptic problem ceases to determine the potential on open sets where the limiting conductivity vanishes. Density convergence, optimality, and weighted gradient estimates do not alone settle that selection issue. Strictly positive finite-time conductivity might enforce additional selection; proving that mechanism for general data remains necessary.

Together with the continuation and variational gaps, this prevents promotion of the conditional entropy estimate or fixed-flux special cases to a full resolution. The unrestricted original target remains unresolved by this work.

## Source context

The strict positivity and mean-zero normalization used for the original local problem are from Facca–Cardin–Putti, https://arxiv.org/abs/1610.06325 and https://doi.org/10.1137/16M1098383. The original OWR question is in Mario Putti's contribution, printed pp. 2398–2400 of https://doi.org/10.4171/owr/2018/39. All constructions above are authored mathematical checks; no novelty claim is made.
