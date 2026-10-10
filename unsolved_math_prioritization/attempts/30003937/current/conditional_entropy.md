# Conditional entropy estimates for the continuum DMK flow

## Scope and attribution

This note does not prove global existence or full density/potential convergence for the multidimensional Dynamic Monge–Kantorovich (DMK) system. Every statement below is conditional on the indicated regular solution existing. The local theory and the Lyapunov identity are from Facca–Cardin–Putti and Facca–Daneri–Cardin–Putti. Optimal-transport duality and the uniqueness characterization of the transport density are imported results. Relative-entropy arguments for finite-dimensional Physarum dynamics precede this note, notably Bonifaci's work. The continuum calculation below is supplied with its hypotheses and proof; no priority or novelty claim is made.

## Setting

Let Ω be a bounded smooth connected domain. Let f be bounded with integral zero. On [0,T), suppose that

    -div(μ ∇u) = f,       μ_t = μ (|∇u| - 1),
    μ(0) = μ₀ > 0,       μ ∂ₙu = 0,       ∫Ω u = 0,

has the regularity μ ∈ C¹([0,T); C^δ(Ω̄)), μ(t)>0 on Ω̄, and the elliptic regularity required to differentiate its weak equation and energy. They are hypotheses here, not an independently established local or global existence conclusion. The original source reports a local classical theorem; the caveat in `continuation.md` identifies an unjustified generic Hölder-norm step in its inspected proof. No extension to T=∞ is inferred. Equivalently one may assume the energy identity below and enough local integrability to justify the entropy chain rule.

Suppose an optimal feasible flux q_* ∈ L¹(Ω;R^d) is available with μ_*:=|q_*|, C:=∫Ω μ_*,

    ∫Ω q_*·∇φ = ∫Ω f φ

for the test functions used below, and suppose C is the minimum L¹ cost over feasible fluxes. Assume

    H₀ := ∫Ω [μ_* log(μ_*/μ₀) - μ_* + μ₀] < ∞,

where 0 log 0 is zero. A bounded optimal density and a strictly positive continuous μ₀ imply this condition on a bounded domain. In the standard convex-domain transport setting these objects come from the known transport-density and duality theory.

Write g=|∇u|, q=μ∇u, and

    M=∫Ω μ,    A=∫Ω μg²,    P=∫Ω μg,
    S=(A+M)/2,    R=S-P=(1/2)∫Ω μ(g-1)².

Feasibility gives P≥C. The inequality 2g≤g²+1 gives P≤S. In particular S≥C.

## Theorem 1: energy gap on the entire interval of existence

For every 0<t<T,

    0 ≤ S(t)-C ≤ H₀/t,
    H(t) + ∫₀ᵗ [S(s)-C+R(s)] ds ≤ H₀,

where H(t)=∫Ω[μ_*log(μ_*/μ(t))-μ_*+μ(t)].

### Proof

Differentiating the weak elliptic equation gives

    ∫Ω μ∇u_t·∇u = -∫Ω μ_t |∇u|².

Consequently A'=−∫Ω μ_t g². Thus the previously known dissipation identity is

    S'=(1/2)∫Ω μ_t(1-g²)
       =−(1/2)∫Ω μ(g+1)(g-1)² ≤ 0.

All these identities are on compact subintervals of [0,T), where μ has a positive lower bound. The entropy chain rule yields

    H'=∫Ω(1-μ_*/μ) μ_t
      =P-M-∫Ω μ_*g+C.

Testing the feasible optimal flux with the current u gives

    A=∫Ω f u=∫Ω q_*·∇u ≤ ∫Ω μ_*g.

It follows that

    H' ≤ P-M-A+C = C-S-R.

The pointwise inequality a log(a/b)-a+b≥0 for a≥0,b>0 gives H≥0. Integrate the last differential inequality. Since S−C is nonnegative and nonincreasing,

    t[S(t)-C] ≤ ∫₀ᵗ[S(s)-C]ds ≤ H₀.

This proves the theorem. Notice that T=∞ has not been proved or used. □

## Corollary 2: consequences if the regular solution is global

If T=∞, then S(t)→C. In fact t[S(t)-C]→0, because the nonincreasing nonnegative gap is integrable: (t/2)[S(t)-C]≤∫_{t/2}^t[S(s)-C]ds→0.

For every t>0, letting ε(t)=S(t)-C,

    C ≤ ∫Ω|q(t)| ≤ C+ε(t),
    ||μ(t)-|q(t)||₁ ≤ 2 sqrt(S(0) ε(t)),
    |M(t)-C| ≤ 2 sqrt(S(0) ε(t)).

For the second bound use Cauchy–Schwarz and R≤ε:

    ∫Ω μ|g-1| ≤ [M∫Ω μ(g-1)²]^(1/2)
               ≤ [2Mε]^(1/2),    M≤2S(0).

For the mass bound, P²≤MA and P≥C imply

    (M-C)²/M = M-2C+C²/M ≤ M-2C+A = 2ε.

The case C=0 is included.

If u_* is any Kantorovich potential with |∇u_*|≤1 almost everywhere and ∫Ω f u_*=C, then

    ∫Ω μ(t)|∇u(t)-∇u_*|² ≤ 2ε(t).

Indeed testing the elliptic equation with u_* and expanding the square gives the exact decomposition

    S-C = (1/2)∫Ω μ|∇u-∇u_*|²
          +(1/2)∫Ω μ(1-|∇u_*|²).

Both terms are nonnegative. This is a μ(t)-weighted estimate. It is not an unweighted H¹ estimate, and does not control the potential on regions whose density tends to zero.

## Corollary 3: conditional weak convergence of the density

Assume additionally that on the nonnegative finite Borel measures over the compact space Ω̄ the extended functional

    S_ext(ν)=sup_{φ∈C¹(Ω̄)} {∫Ω fφ−(1/2)∫Ω̄ |∇φ|² dν}
             +(1/2)ν(Ω̄)

has μ_* dx as its unique minimizer, with value C, and agrees with S for the positive regular densities considered above. This is a separate variational characterization; it is not deduced from the evolution equation. Under this hypothesis and T=∞,

    μ(t) dx ⇀* μ_* dx  as finite measures on Ω̄.

Proof: M≤2S(0) gives sequential weak-* compactness. S_ext is weak-* lower semicontinuous, being a supremum of continuous affine functionals plus continuous total mass. Every limit point ν therefore satisfies S_ext(ν)≤liminf S(t)=C, hence ν=μ_*dx. Uniqueness of every subsequential limit on a compact metrizable mass-bounded set gives full weak-* convergence. □

The compact-domain measure formulation and uniqueness hypothesis must be checked in any application, including whether boundary measures are admitted. One cannot replace them silently by uniqueness only within a smaller L¹ class.

## What remains unproved

1. Global continuation of the original Hölder-density solution in dimensions greater than one.
2. Compactness and identification strong enough to obtain an appropriate whole-trajectory, mean-zero potential limit.
3. Strong L¹ density convergence under the original hypotheses, if that stronger topology is requested.

The entropy and Lyapunov estimates do not supply a uniform Hölder norm, an unweighted gradient bound, or a positive density lower bound independent of time. They therefore do not settle the original OWR convergence conjecture.

## References

- Facca, Cardin, Putti, Towards a stationary Monge–Kantorovich dynamics: the Physarum Polycephalum experience, SIAM J. Appl. Math. 78 (2018), 651–676. https://doi.org/10.1137/16M1098383 ; https://arxiv.org/abs/1610.06325
- Facca, Daneri, Cardin, Putti, Numerical Solution of Monge–Kantorovich Equations via a Dynamic Formulation, J. Sci. Comput. 82 (2020), 68. https://arxiv.org/abs/1709.06765
- Facca, Piazzon, Putti, L¹ Transport Energy, Applied Mathematics & Optimization 86 (2022), 21. https://doi.org/10.1007/s00245-022-09880-1 . The inspected public preprint has two authors and an earlier title: Facca and Piazzon, Transport Energy, https://arxiv.org/abs/1909.04417v2 . Its Proposition 2.1 concerns the variational characterization; its metric flow is not the original DMK reaction equation.
- Bonifaci, On the Convergence Time of a Natural Dynamics for Linear Programming, Algorithmica 82 (2020), 300–315. https://doi.org/10.1007/s00453-019-00615-3 ; https://arxiv.org/abs/1611.06729 . This is prior finite-dimensional entropy methodology, not a continuum existence theorem.
