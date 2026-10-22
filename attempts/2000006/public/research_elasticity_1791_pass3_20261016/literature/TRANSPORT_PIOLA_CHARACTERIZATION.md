# A reduced intrinsic characterization of the E-6322 inverse class

16 October 2026. This strengthens the characterization in `EXACT_INVERSE_CLASS.md`: the range, a.e. bijection and exact transport conditions can themselves be derived from the full-boundary Piola identities. The underlying mathematical target remains unresolved.

## The exact class

Let D=G(Ω) and V be the transformed density in the companion report. Define P_g to be the maps v∈W^{1,9/5}(D;R³) with finite ∫_D V(Dv) and such that, for every scalar ψ smooth near Dbar and every φ∈C_c∞(R³;R³),

∫_D [ψ(z)K(z) div φ(v(z)) + φ(v(z))·(cof Dv(z))Dψ(z)] dz
=∫_{∂Ω} ψ(G(x)) φ(x)·ν_Ω(x) dS(x),                  (P)

where K=det Dv. These are well-defined conditions: finite V gives K>0, K∈L³, and cof Dv∈L^{9/4}, while all the tests and their derivatives are bounded on the relevant sets.

**Theorem.** P_g is exactly the set B_g of a.e. inverses of original full-class primal competitors. Thus a primal global minimizer is equivalent to a dual global minimizer on P_g. The range restriction v∈Ω a.e., a.e. injectivity, the full inverse trace, and a genuine W^{1,6} primal inverse are conclusions, not additional assumptions in this definition.

The condition that is still imposed is (P), up to the full boundary. It has not been deduced from finite dual energy alone.

## Proof of the added implication

Necessity of (P) for B_g was proved by change of variables and primal integration by parts in the companion report. We prove that finite V and (P) imply all its compatibility conditions.

### 1. The Jacobian pushforward measure

Define the finite positive Borel measure μ=v_#(K dz) on R³, taking a measurable representative of v. Set ψ=1 in (P). The divergence theorem for the smooth domain Ω gives

∫_{R³} div φ dμ = ∫_Ω div φ dx

for every φ∈C_c∞(R³;R³). Hence the finite signed measure λ=μ−1_Ω dx has every distributional derivative zero on R³. To see that λ=0 without a support assumption, convolve with a compactly supported smooth mollifier. Each λ*ρ_ε is smooth, has zero gradient and lies in L¹(R³), so it is the zero constant. Letting ε→0 proves λ=0.

Consequently

∫_D f(v(z))K(z) dz=∫_Ω f(x) dx                         (T)

for every nonnegative Borel f. In particular ∫_{v∉Ω}K=0. Since K>0 a.e., v∈Ω a.e. The desired range bound is therefore automatic.

### 2. Multiplicity one from the general area formula

Sobolev v is approximately differentiable a.e. Choose a Borel full-measure set D_* of good approximate differentiability points, decomposed into countably many Borel pieces on which v is Lipschitz, with K>0 and approximate derivative equal to its weak gradient. Apply the area formula on those pieces (made disjoint), or equivalently the general formula on this good set. No Lusin N property of a representative on the discarded null set is assumed. This gives

∫_D f(v(z))K(z) dz=∫_{R³} f(x)N(v,D_*,x) dx.

Comparing with (T) yields N(v,D_*,x)=1_Ω(x) a.e. Thus almost every x∈Ω has exactly one preimage in D_*. Choose a Borel full-measure subset Ω₀⊂Ω of such points, discarding a Borel null superset of the exceptional target set if necessary. Formula (T) and K>0 show that D₀=D_*∩v⁻¹(Ω₀) has full measure in D. The restriction v:D₀→Ω₀ is a bijection.

Its inverse is measurable. For instance, apply the measurable weighted-sum part of the area formula to each coordinate function z_i on D₀; the sum over its unique fiber is precisely the i-th coordinate of the inverse. Thus (T) and this bijection give condition C2 of the companion report.

The exact primary area formula used here is Proposition 2.1, p.5, and equation (2.3), in Barchiesi–Henao–Mora-Corral–Rodiac, *A relaxation approach to the minimisation of the neo-Hookean energy in 3D*, arXiv:2311.02952v2, 20 May 2024. Its hypothesis is approximate differentiability a.e.; it is not restricted to H¹ or to the paper's later elastic class. Definition 2.2 and the following discussion supply the full-measure good set. The theorem and formula were checked both in the PDF text and in the rendered page:

https://arxiv.org/pdf/2311.02952v2

### 3. Recovering the primal map

We now have C1 and C2, and (P) gives C3. Tests smooth near Ωbar in the companion report can be extended and cut off to global smooth compactly supported tests, since v∈Ω a.e. The already proved coordinate-test argument yields

y=v⁻¹∈W^{1,6}(Ω),  Dy=(Dv)⁻¹∘y,  Tr y=G,  I(y)=∫_D V(Dv).

Thus y∈A_g and v∈B_g. Pass 2 then gives the full inverse trace Tr v=G⁻¹. This proves P_g=B_g.

## Consequences and limits

The weak compactness, lower semicontinuity and finite-cost relaxation statements in `EXACT_INVERSE_CLASS.md` apply to P_g as well. They are obtained by lifting to the primal class; no general inverse-minor weak continuity below exponent two is claimed.

A candidate additive comparison v+tζ would have to retain positive determinant, finite dual energy and the full-boundary identities (P). The theorem removes the need to separately verify the inverse's Sobolev regularity once these conditions hold, but does not prove that ordinary additive perturbations preserve them. That is the remaining admissibility issue for unrestricted dual Euler–Lagrange arguments.
