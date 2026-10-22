# Independent derivation — concave duality and regularity

This file was derived before reading the archived implementation or favorable original review. It separates a complete scalar lemma from its geometric/PDE prerequisites. The initial mechanism freeze records the input boundary.

## 1. Scalar lemma, including global maximizers

Let a be a finite concave real function on (0,1), with endpoint values given by finite envelope limits or by values that preserve concavity. Let 0<T<1. Assume a is C² on (T−ε,T), a'(t)→κ0<0 and a''(t)→L∈(−∞,0) as t↑T. Assume a'_+(T)≤b<κ0. Concavity and interior finiteness imply both one-sided slopes at T are finite: the slopes are trapped between secant slopes to fixed points on either side. No differentiability of the post-contact branch is required.

For t<T the secant inequality is

    a(t)−a(T) ≤ κ0(t−T).

For t>T it is

    a(t)−a(T) ≤ b(t−T).

Consequently, for b<κ<κ0,

    a(t)−κt − [a(T)−κT] < 0  (t≠T).

Thus T is the unique global maximizer, including endpoint competitors. This is a support-line proof and does not rely on searching branches numerically. It remains true if an endpoint envelope value is −∞. A finite endpoint value above its limiting value would break concavity, so that case is excluded by the envelope construction.

Since a'' is strictly negative near T, a' is strictly decreasing there. For κ>κ0 close enough there is a unique tκ∈(T−ε,T) with a'(tκ)=κ. The tangent-line inequality for concave a makes tκ a global maximizer. Were a second global maximizer present, concavity would make a−κt constant on their intervening interval, contradicting strict concavity in a neighbourhood of tκ. Hence tκ is globally unique. This rules out an unknown post-contact branch taking over.

Define F(κ)=κ+sup_{0≤t≤1}[a(t)−tκ]. For κ∈(b,κ0), F=a(T)+(1−T)κ. At κ=κ0 the same formula holds, with unique maximizer T (strict concavity immediately to the left excludes earlier ties). For κ>κ0 close,

    F'(κ)=1−tκ,       F''(κ)=−1/a''(tκ).

The inverse relation yields tκ−T=(κ−κ0)/L+o(κ−κ0). Therefore

    F'(κ0+h)=1−T−h/L+o(h)    (h>0),
    F'(κ0+h)=1−T              (h<0 sufficiently small).

F is C¹ across κ0 and the difference quotients of F' have limits −1/L>0 and 0. F''(κ0) does not exist. More strongly,

    F(κ0+h)=F(κ0)+(1−T)h−h²/(2L)+o(h²)  (h>0),
    F(κ0+h)=F(κ0)+(1−T)h                 (h<0).

The absence of a common quadratic coefficient also rules out a second-order Peano/Taylor expansion, avoiding an ambiguity between failure of C² and failure of twice differentiability.

## 2. Exact independent normal form

Put x=t−T and choose

    a(t)=A+κ0 x+(L/2)x²  (x≤0),
    a(t)=A+βx+(M/2)x²    (x≥0),

where 0<T<1, β<κ0<0, L<0, M≤0. Both branches are concave and the slope decreases at T, so a is globally concave. On β<κ<κ0 the objective relative to its T value is (κ0−κ)x+Lx²/2 on x≤0 and (β−κ)x+Mx²/2 on x≥0; both are strictly negative for x≠0. At κ=κ0+h, 0<h<(−L)T, its left-branch maximum occurs at x*=h/L and the exact global objective improvement is −h²/(2L)>0. Completing the square gives the gap L(x−x*)²/2≤0. The right branch is below the T value and cannot overtake. Thus

    F(κ)=A+(1−T)κ                      (β<κ≤κ0),
    F(κ)=A+(1−T)κ−(κ−κ0)²/(2L)         (κ0<κ<κ0+(−L)T).

The accompanying stdout-only standard-library verifier checks exact polynomial coefficient identities, support signs, optimizer location and six invalid-hypothesis controls. Rational values are corroboration for the algebra, while the identities above prove the assertion for all real parameters satisfying the hypotheses.

## 3. Boundary, zero and infinite curvature controls

At T=1 the κ<κ0 plateau need not represent an interior contact and construction of the post-contact slope gap is unavailable. At κ0=0 the corresponding disc radius is 1, hence boundary. At the pole w=0, κ0=−∞ and τ=0, and the smooth twist relation on the punctured disc is unavailable. These points must be excluded.

A gap without finite nonzero L is insufficient for the stated second-derivative jump. If a(T+x)=A+κ0x−c|x|^p for x<0 and β<κ0 on the right, then on the left branch x scales as −(κ−κ0)^(1/(p−1)), and F'−(1−T) has the same scaling. For 1<p<2 (infinite negative a''), F'' at κ0 exists and equals zero from both sides; higher smoothness may fail. For p>2 (L=0), F' has an infinite right difference quotient and F is not twice differentiable, but the finite jump formula is false. Thus the candidate correctly requires −∞<L<0. A single polar contact point likewise supplies no strict Green-domain gap.

## 4. Conditional Green curvature mechanism

Suppose the pre-contact domains are conformal injective projections of a C∞ family U_t of smoothly bounded simply connected domains on a fixed Riemann surface, up to t=T. The lifted pole p and lifted w are fixed; choose any smooth conformal coordinate near p. The Green singularity log|ζ−ζ(p)|² is independent of t. Smooth domain dependence implies the derivative H=∂tG_t at T− is finite and harmonic on U_T, with its pole removable. Differentiating G_t(x_t,p)=0 gives

    H=−V ∂nG_T on ∂U_T.

For an increasing strong Hele-Shaw family V>0, while Hopf's lemma for the negative Green function gives ∂nG_T>0. Thus H<0 on the boundary. The maximum principle gives H(w)<0, finite. If ∂tψ_t(w)=G_t(w,p), this is precisely L=a''_−(T)∈(−∞,0).

The derivative identity follows by differentiating the harmonic equation for ψ_t+ρ inside the fluid: ∂tψ_t has one fixed logarithmic pole, is harmonic elsewhere, and vanishes on the moving boundary because ψ_t=φ and ∇ψ_t=∇φ there. Uniqueness of the Green Dirichlet problem identifies it. Smoothness of ψ_t in t can alternatively be obtained by solving its Dirichlet problem on the smooth lifted family and adding the smooth obstacle/background terms. This must be checked in the cited construction, rather than assumed from the projected singular boundary.

## 5. Coordinate transfer and actual second differentiability

For a finite w*≠0 and finite κ0<0 put τ*=exp(κ0/2), z*=w*/τ*. Then 0<τ*<1, z* is finite, and the smooth curve

    c(κ)=(w* exp(−κ/2), exp(κ/2))

lies inside P1×D near κ0. It is a real smooth curve, and the map (z,τ)↦(τz,τ) is biholomorphic on P1×D*.

If an ambient real function has a second-order Taylor expansion at c(κ0), composing that expansion with c gives one common quadratic coefficient in h of either sign. Adding a smooth function changes both one-sided quadratic coefficients equally. Therefore the incompatible coefficients in §1 contradict ambient second differentiability. In the classical C¹-neighbourhood definition the usual second derivative chain rule gives the same contradiction. The argument uses a curve at an interior point; no boundary derivatives are being inferred.

For f(z,τ)=φ(τz), |τ|=1, rotations z↦τz act smoothly on P1 and preserve ω_FS. Thus f is C∞ jointly in z and τ and ω_FS+ddc_z f is the pullback of the positive form ω_FS+ddcφ. Strict Kähler positivity follows. The exact smooth correction in the source duality is recorded in the final report.
