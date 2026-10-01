# Recovered substantive turn 1: conformally radial slit-flow obstruction

2026-10-01 UTC. This is the first documented substantive response after recovery. The pre-interruption count is unknown and is not reset. The original interior non-C² target remains unresolved by this turn.

## Exact target retained

We seek smooth boundary data f on P¹×∂D such that each f(·,τ) is ω_FS-plurisubharmonic (semipositivity is allowed), and the continuous solution Φ of

    π*ω_FS + dd^c Φ >= 0,
    (π*ω_FS + dd^c Φ)^2 = 0

fails to be C² at a point of P¹×D. The equation is understood in the Bedford–Taylor sense. A merely local example on a ball, nonsmooth boundary data, failure confined to the boundary, or loss of maximal rank without a regularity proof does not meet this target.

## Mechanism tested

Try to prescribe simply connected Hele–Shaw domains by dilating within a fixed Riemann map to a slit plane, then flatten a radial density to obtain smooth boundary data. The map is the Koebe map

    g(ζ) = ζ/(1−ζ)^2,    g'(ζ) = (1+ζ)/(1−ζ)^3.

It maps D biholomorphically onto Ω = C\(−infinity,−1/4]. Write ζ(w)=g^{-1}(w) on Ω, with ζ(0)=0. In P¹ the complementary slit is an arc with endpoints −1/4 and infinity.

Let q(s)>0 for 0<=s<1 be smooth and infinitely flat at 1, normalized by integral_0^1 q(s) ds=1. For example normalize exp(−1/(1−s)). Put

    t(s) = integral_0^s q(v) dv,
    χ'(s) = t(s)/s,    χ(0)=0,
    δ(s) = χ(s)−log s−χ(1),    0<s<=1.

Then δ(1)=0, δ'(s)=(t(s)−1)/s, and δ is infinitely flat at 1. Extend χ for s>=1 by χ(1)+log s, or equivalently extend δ by zero there. χ is smooth at zero because t(s)/s is smooth.

On Ω set

    ψ(w)=χ(|ζ(w)|²)+log|w/ζ(w)|²
         =log|w|²+χ(1)+δ(|ζ(w)|²),

and extend by log|w|²+χ(1) across the slit. At w=0 use the first expression, since w/ζ(w) is holomorphic and nonzero. The density of dd^cψ is, up to the fixed positive normalization of area,

    q(|ζ|²)/|g'(ζ)|².

This is positive off the slit. It extends smoothly as zero across the slit, including its endpoints: the inverse map has only algebraic square-root singularities at the endpoints, while δ and q vanish faster than every power of their distance to the unit circle. In the chart at infinity the same argument applies after subtracting log|w|². Hence φ=ψ−log(1+|w|²) is a smooth semipositive potential on P¹.

## Exact candidate solution and why it fails the target

For 0<|τ|<1, where τz lies in Ω and |ζ(τz)|<|τ|, set

    U(z,τ)=χ(|ζ(τz)/τ|²)+log|τz/ζ(τz)|².

Everywhere else use U(z,τ)=log|z|²+χ(1). Near τ=0 define η(z,τ)=ζ(τz)/τ by its holomorphic removable extension η(z,0)=z, and use the first expression where |η|<1. The second expression is used where |η|>=1. The apparent singularity at z=0 is removable in the first expression. Near z=infinity the second expression applies.

The two expressions differ by δ(|η|²). Thus they glue to **C-infinity** across |η|=1. For an interior point with τz on the slit, |ζ|=1>|τ|, so a neighborhood lies on the second branch; the branch singularity of ζ causes no interior regularity loss. At τ=0 and finite z, η is holomorphic. These observations cover the entire interior P¹×D after subtracting the Fubini–Study local potential.

On the first branch, U is the pullback of the subharmonic one-variable potential χ(|η|²) by a holomorphic function, plus a pluriharmonic term. Its Levi form is semipositive of rank at most one. On the second branch the Levi form is zero. Smooth gluing therefore gives (dd^cU)^2=0 everywhere locally. Consequently

    Φ(z,τ)=U(z,τ)−log(1+|z|²)

is a smooth-interior solution of the stated HCMA problem. On |τ|=1 the boundary value is φ(τz), which is smooth and semipositive. The construction is completely degenerate on an open set, but **does not produce interior failure of C²**.

The calculation uses the same fixed-map geometry as a conformally radial Hele–Shaw flow: the domains are g(D_sqrt(s)), with area parameter t(s). It can be checked directly from the local rank-one potential, so no unproved general flow-smoothing theorem is being invoked.

## Why simply choosing nonflat q does not repair it

If q(1)>0, the factor |g'(ζ)|^{-2} blows up at ζ=−1, giving nonsmooth boundary data at the slit tip. Bounded smooth density forces q(1)=0. It then vanishes along the open slit, where g' has a nonzero finite one-sided limit.

Suppose q has a first nonzero finite-order Taylor term at 1, of order m. Along the real radial path ζ=−1+a with a>0 small, w+1/4 is of order a² and |g'|² is of order a². The density is consequently of order a^(m−2), or of order (w+1/4)^(m/2−1). But a smooth density which is identically zero on the slit to the left of the endpoint must be infinitely flat along this real axis at that endpoint. Such a nonzero finite-order asymptotic is impossible. Thus within this radial ansatz smoothness requires flatness, which also smooths the interior gluing above.

## Outcome and next target

This specific mechanism is blocked: radial flattening fixes the boundary defect but removes the interior second-derivative defect as well. This is a diagnostic obstruction for the ansatz, not a nonexistence theorem for the original problem. No novelty claim is made.

A subsequent substantive turn must change the mechanism, for example by a genuinely nonradial flow with endpoint-localized density control, or by a different exact HCMA construction. Source lookup and finite checks are not additional proof turns. Independent review of any eventual claimed solution remains required.
