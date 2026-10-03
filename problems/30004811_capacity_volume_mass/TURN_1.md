# Turn1: the unrestricted all-AF statement is false

One substantive author turn. AI-assisted proof candidate; independent review pending. The standard nonnegative-scalar-curvature/empty-or-minimal-boundary conjecture is already resolved by PRIOR_RESOLUTION.md. This calculation addresses only the broader literal formulation. Historical novelty is unverified.

## 1. Smooth complete metric without singularity or boundary

Choose smooth χ:[0,∞)→[0,1], identically0 forr≤2 and1 forr≥3. Set u(x)=1−χ(|x|)/|x|, interpreting the quotient as0 near0, and

    M=R³,             g=u⁴δ.

This is Euclidean near0, hence smooth. Everywhere1/2≤u≤1, so g is positive and uniformly equivalent to the complete Euclidean metric. It is connected, one-ended, complete, with empty boundary. Forr≥3,

    u=1−1/r,          g=(1−1/r)⁴δ.

This is the negative-mass Schwarzschild end with m_ADM=−2. Direct substitution of g_ij=u⁴δ_ij into the ADM integral gives

    m_ADM = lim_{r→∞} −2r²u³u_r = −2.

All derivatives have order1 AF decay. R_g=−8u^−5Δu is smooth and supported in the compact transition annulus, hence integrable. Nonnegative scalar curvature there is not claimed. This is a smooth complete AF example, not a singular Schwarzschild manifold.

## 2. Nested smooth exhaustion

ForR≥6 take a_R=(R/2)e₁ and K_R=closedB(a_R,R). Each containsB(0,R/2), so they exhaustR³. IfS≥R,

    |a_S−a_R|+R=(S−R)/2+R≤S,

hence K_R⊂K_S. The exterior is inr≥R/2≥3 and the entire modified core is inside. Thus every sequenceR_j↑∞ is admissible in the exact mass definition.

## 3. Exact capacity and the actual metric energy

Let f_R=1−R/|x−a_R| outsideK_R, extended0 inside. In dimension3,

    |∇φ|²_g dV_g=u²|∇φ|²_δ dx,
    Δ_gφ=u^−6 div_δ(u²∇φ).

Bothu andf_R are Euclidean harmonic outsideK_R. Therefore

    div(u²∇(f_R/u))=uΔf_R−f_RΔu=0.

The quotient vanishes on∂K_R and tends to1, so uniqueness makes it the metric capacitary potential. At infinity, withR fixed,

    f_R/u=[1−R/r+O(r^−2)]/[1−1/r]
          =1−(R−1)/r+O(r^−2).

Its normalized flux isR−1, giving the exact identity

    cap_g(K_R)=R−1.                                      (1)

This is the specialization of Jauregui §5 equation(41), cap_g(K)=cap_δ(K)+m/2 for an enclosing set in a harmonically flat end. That credited capacity identity precedes and does not use the nonnegative-mass assumption in his subsequent volume estimate.

As a separate check of the conformal factor, testing withf_R itself gives
(4π)^−1∫_{outsideK_R}(1−2/r+1/r²)R²/|x−a_R|⁴ dx.
Newton's shell integral makes the first two termsR−1. Since r≥|x−a_R|/2, the last is≤4/(3R). Thus the direct variational bound is consistent with(1); Euclidean energy has not replaced metric energy.

## 4. Volume and the compact-fill error

Outside the core,u⁶=1−6/r+O(r^−2). Replacing the true integrand by1−6/r in the core changes its integral by a fixed finite number, since1/r is locally integrable. AlsoK_R⊂B(0,3R/2), so∫_{K_R}r^−2dx≤6πR. Consequently

    vol_g(K_R)=(4π/3)R³−6∫_{B(a_R,R)}|x|^−1dx+O(R).       (2)

For d=|a|<R, the elementary solid-ball Newton potential is
∫_{B(a,R)}|x|^−1dx=2π(R²−d²/3).
Indeed, the angular mean on a shell centered ata is1/max(d,ρ), and integration gives

    4π[∫_0^d ρ²/d dρ+∫_d^R ρ dρ]=2π(R²−d²/3).

Atd=R/2 the integral is(11π/6)R². Thus

    vol_g(K_R)=(4π/3)R³−11πR²+O(R),
    (3vol_g(K_R)/(4π))^(1/3)=R−11/4+O(R^−1).             (3)

The latter is the cube-root expansion at1. All compact-fill and higher conformal terms contribute onlyO(R^−1) to the radius.

## 5. Strict failure of equality

By(1) and(3), this admissible exhaustion has limit

    lim [(3vol_g(K_R)/(4π))^(1/3)−cap_g(K_R)]=−7/4.

Taking the supremum over exhaustions gives

    m_CV(M,g)≥−7/4>−2=m_ADM(M,g).

This disproves the unrestricted all-AF statement. It does not evaluate m_CV, and requires no optimality of these balls. The gap is at least1/4.

For generalm<0 and fixed0<λ<1, B(λRe₁,R) has deficit limitm(1−λ²/2)>m by the same computation. The explicitm=−2,λ=1/2 example suffices.

## Scope and credit

The physical-class conjecture has a positive prior resolution; the broader literal sentence has the negative example above. They must remain side by side. Jauregui's capacity identity and classical Newton potential are credited. No new nonnegative-scalar-curvature theorem or priority claim follows. Author search stops after this complete first-turn candidate pending independent review.
