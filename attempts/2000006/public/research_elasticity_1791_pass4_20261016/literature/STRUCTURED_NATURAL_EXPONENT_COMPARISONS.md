# Structured comparisons at the natural inverse Sobolev exponent

16 October 2026. This is an auxiliary theorem for E-6322 with its original full primal class and entire-boundary smooth diffeomorphic datum. It repairs the inverse-class issue for natural cutoff expressions, conditional on their transformed energy being finite. It does not prove that those cutoffs preserve orientation or have finite energy.

## Statement

Put D=G(Ω), and let v=y⁻¹ be the a.e. inverse of any original competitor y∈A_g. Thus v∈W^{1,9/5}(D), v∈Ω a.e., and y∈W^{1,6}(Ω) is continuous on the closure with trace G.

Let Φ(z,x) be smooth on a neighborhood of Dbar×Ωbar. Assume Φ(z,x)=x whenever z lies in a fixed neighborhood of ∂D and x∈Ωbar. Define

u(z)=Φ(z,v(z)).

**Theorem.** If ∫_D V(Du)<∞, then u belongs to the exact inverse class B_g. Consequently, when y is a primal global minimizer,

∫_D V(Dv)≤∫_D V(Du).

The condition on V includes det Du>0 a.e. Infinite-energy comparisons satisfy the inequality trivially. No W^{1,9/4} regularity of u−v is required.

In particular this applies to

u(z)=θ(z)v(z)+(1−θ(z))ℓ(z),

where θ is smooth, θ=1 near ∂D, and ℓ is affine (indeed, ℓ can be any smooth map). The resulting difference is generally only W^{1,9/5}. Thus the theorem strictly expands the proved structured comparison mechanism beyond the sufficient addition exponent used in pass 3.

## Proof

Write F=Dy, j=det F, H=Dv, and K=det H. The Sobolev chain rule gives u∈W^{1,9/5}, since v is bounded and the derivatives of Φ are bounded on the relevant compact set.

Define the primal-coordinate auxiliary map

k(x)=Φ(y(x),x).

It belongs to W^{1,6}(Ω). Because y is uniformly continuous up to ∂Ω and y(∂Ω)=∂D, k(x)=x on a full source collar of ∂Ω. No barrier integrability or injectivity of k is needed below.

Set A=D_zΦ(y(x),x) and B=D_xΦ(y(x),x). At almost every good point,

Dk=AF+B,    Du(y(x))=A+BF⁻¹=Dk F⁻¹.

The a.e. inverse identities and the area formula transfer these relations between source and target. In particular

(det Du)(y(x))j(x)=det Dk(x),

(cof Du)(y(x))j(x)=(cof Dk(x))F(x)ᵀ.              (1)

To invoke the exact inverse-class characterization, it remains to verify its full-boundary transported Piola identity. Let ψ be smooth near Dbar and φ∈C_c∞(R³;R³). Changing variables z=y(x) and using (1) transforms its volume expression into

∫_Ω [ψ(y) det Dk divφ(k)
       + φ(k)·(cof Dk)D(ψ∘y)] dx.                (2)

This is a high-exponent primal identity. Specifically, approximate k−id and y−G strongly in W^{1,6} by smooth functions compactly supported in Ω, writing the resulting maps as k_m and y_m. Their boundary traces remain exactly id and G. Strong W^{1,6} convergence gives uniform convergence, strong L³ convergence of cof Dk_m, and strong L² convergence of det Dk_m. The derivatives D(ψ∘y_m) converge strongly in L⁶. These bounds pass every product in (2) to the limit.

For the smooth approximations, ordinary Piola and the divergence theorem give

∫_Ω [ψ(y_m) det Dk_m divφ(k_m)
       + φ(k_m)·(cof Dk_m)D(ψ∘y_m)] dx
=∫_{∂Ω}ψ(G(x))φ(x)·ν_Ω(x) dS.

Passing to the limit proves that u satisfies the required full-boundary transported Piola identity. Its finite V now supplies the other hypothesis of the reduced characterization from pass 3. That theorem gives u∈B_g, with an actual primal W^{1,6} inverse and the complete prescribed traces. This proves the result.

## Why the argument avoids the missing low-exponent step

No mollification of v is used, and no equality between its distributional second-order minors and pointwise cofactors is silently assumed. The only smoothing is of the W^{1,6} maps y and k, where the quadratic and cubic minors converge strongly in the stated Lebesgue spaces. The rank-one cutoff algebra can therefore be bypassed entirely.

The standard weak pullback calculus is consistent with this choice: Hajłasz–Schikorra–Tyson, arXiv:1301.4978v3 (28 November 2013), Lemma 4.1(2), pp.11–12, assumes p≥ℓ+1 for commuting pullback with exterior differentiation of an ℓ-form. Part (3) assumes p≥2 for the bilinear product rule. The primal p=6 satisfies these thresholds; the generic inverse p=9/5 does not. The proof above gives the relevant boundary passage directly.

https://arxiv.org/pdf/1301.4978v3

## Remaining obstruction

The theorem is conditional on the final map's finite dual energy. Smoothness of θ, a bound 0≤θ≤1, and positivity of the endpoint determinants do not by themselves imply det D[θv+(1−θ)ℓ]>0. Nor do they control the reciprocal determinant in V. Establishing an energy-finite comparison and a useful upper energy estimate remains a separate task.

An arbitrary compactly supported W^{1,9/5} difference is not necessarily a smooth graph transformation Φ(z,v(z)). No unconditional extension to every such finite-energy difference is asserted here.
