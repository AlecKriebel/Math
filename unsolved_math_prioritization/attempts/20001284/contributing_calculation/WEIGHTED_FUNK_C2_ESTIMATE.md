# Contributing calculation: C² control of the weighted Funk derivative

This is author-attempt support, not an independent final audit. Ambient dimension is three. The point on S² is x and the section normal is u. All surface measures below are unnormalized.

## Conclusion

For positive even radial functions ρ with ||ρ/R−1||_{C²(S²)} sufficiently small, the perimeter derivative extends to an isomorphism

D P_ρ : L²_even(S²) → H^{1/2}_even(S²).

More importantly, uniformly over arbitrary harmonic bandwidth,

||D P_ρ−F||_{L²→H^{1/2}} ≤ C ||ρ/R−1||_{C²}.

Consequently the difference of two sufficiently C²-close radial functions is controlled in L² by the H^{1/2} norm of their perimeter-data difference. This statement does not require high derivatives in x and does not follow merely from small pointwise weight. The extra ingredient is high regularity in the *normal variable u*, which the geometric formula supplies using only two x derivatives.

## 1. Exact Funk spaces

Use spectral Sobolev norms

||f||²_{H^s} = Σ_{l≥0} Σ_{m=−l}^l (1+l(l+1))^s |f_{lm}|².

For real L²-normalized spherical harmonics, F Y_{lm}=λ_l Y_{lm}, where

λ_l=2π P_l(0), λ_{2j}=2π(−1)^j (2j)!/[2^{2j}(j!)²], λ_{2j+1}=0.

The central-binomial-coefficient estimate gives |λ_{2j}| ≍ (1+j)^{−1/2}. Hence F:L²_even→H^{1/2}_even is a bounded isomorphism, with constants independent of harmonic cutoff. No bound for F^{-1}:L²→L² is asserted.

## 2. A separated-normal-variable weighted-Funk lemma

Let E(x,u) be even separately in x and u, measurable in x, C⁴ in u, and suppose

B = ess sup_{x∈S²} ||(1−Δ_u)² E(x,·)||_{L∞(S²_u)} < ∞.

Define, initially for continuous even h,

(T_E h)(u)= ∫_{x·u=0} E(x,u) h(x) ds_x.

Then T_E has a unique bounded extension L²_even→H^{1/2}_even and

||T_E h||_{H^{1/2}} ≤ C B ||h||_{L²}.

Proof. Expand E in the normal variable alone:

E(x,u)=Σ_{l,m} a_{lm}(x) Y_{lm}(u).

Integration by parts in u gives

||a_{lm}||∞ ≤ (4π)^{1/2} B (1+l(l+1))^{−2}.

Each a_{lm} is even in x, and odd l vanish by evenness in u. Addition-theorem bounds give

||Y_{lm}||∞ ≤ [(2l+1)/(4π)]^{1/2},
||∇Y_{lm}||∞ ≤ [l(l+1)(2l+1)/(4π)]^{1/2}.

Multiplication obeys

||b g||_{H^{1/2}} ≤ C ||b||_{C¹} ||g||_{H^{1/2}}.

One direct proof is boundedness on L² and H¹, followed by Hilbert-space interpolation. Thus each separated term obeys

||Y_{lm} F(a_{lm}h)||_{H^{1/2}}
 ≤ C (1+l)^{3/2} ||a_{lm}||∞ ||h||₂.

Summing the 2l+1 orders m produces a convergent series because

Σ_l (2l+1)(1+l)^{3/2}(1+l(l+1))^{−2} < ∞

(the summand is O(l^{−3/2})). The expansion converges in operator norm L²→H^{1/2}. It also converges uniformly as a function of (x,u), since the corresponding C⁰ majorant is summable. Consequently for continuous h its operator sum is the original great-circle integral. Evenness preserves the spaces required for inversion by F. This proves the lemma.

Remarks: A full C⁴_u norm can replace B. No x derivatives of E are used. In particular, this is not a generic rough-amplitude pseudodifferential theorem. The exponent four is convenient rather than optimized.

## 3. Geometric weight supplies the lemma hypothesis

For a positive C² radial function ρ, let g(x)=∇_{S²}ρ(x), H(x)=Hess_{S²}ρ(x), and t=u×x. Define on the full product S²_x×S²_u

W_ρ(x,u) = ρ(x) [ρ(x)² + 2(g(x)·t)² − ρ(x)H(x)[t,t]]
             / [ρ(x)² + (g(x)·t)²]^{3/2}.

On incidence x·u=0, t is a unit tangent to the section great circle, so this equals the proposed weight

w=ρ(ρ²+2ρ_s²−ρρ_{ss})/(ρ²+ρ_s²)^{3/2}.

Off incidence no geometric interpretation is required. The extension is a rational smooth function of u, with denominator bounded away from zero when ρ≥R/2. Normalize r=ρ/R. Because W_{cρ}=W_ρ, its finite-dimensional parameters are r(x), ∇r(x), Hess r(x). At the ball they are (1,0,0), and W=1. Repeated differentiation with respect to u differentiates only t=u×x and never differentiates these parameter fields in x. Smoothness of this finite-dimensional formula on a compact parameter neighborhood therefore gives, for every fixed k,

sup_x ||W_ρ(x,·)−1||_{C^k_u} ≤ C_k ||ρ/R−1||_{C²_x}.

This remains valid for C² (not C^∞) radial functions. For even ρ, g(−x)=−g(x) and the ambient tangent Hessian is even under x↦−x; the displayed quadratic formula is even separately in x and u.

Applying the lemma with E=W_ρ−1 gives the claimed bound on D P_ρ−F.

## 4. Differentiation and integration by parts

For h∈C²_even and ρ>0,

D P_ρ[h](u) = ∫_{C_u} [ρh+ρ_s h_s]/sqrt(ρ²+ρ_s²) ds.

Periodic integration by parts gives

D P_ρ[h](u) = ∫_{C_u} W_ρ(x,u)h(x) ds.

The weight computation is exact:

ρ/sqrt(ρ²+ρ_s²) − ∂_s(ρ_s/sqrt(ρ²+ρ_s²))
 = ρ(ρ²+2ρ_s²−ρρ_{ss})/(ρ²+ρ_s²)^{3/2}.

Hence the extension derived above agrees with the actual derivative on smooth variations.

## 5. Uniform nonlinear two-point estimate

Let ρ_0,ρ_1 be positive even C² functions with ||ρ_i/R−1||C²≤δ, and put h=ρ_1−ρ_0, ρ_t=(1−t)ρ_0+tρ_1. The same bound applies uniformly along the segment. The perimeter formula and the fundamental theorem of calculus give

P(ρ_1)−P(ρ_0)=Fh + ∫_0^1 T_{W_{ρ_t}−1}h dt

as an equality in H^{1/2}, initially also pointwise. Strong continuity in t follows directly from the C⁴_u parameter estimate in the lemma. Thus

||P(ρ_1)−P(ρ_0)−Fh||_{H^{1/2}} ≤ Cδ ||h||₂.

If c_F||h||₂≤||Fh||_{H^{1/2}}, then

(c_F−Cδ)||h||₂ ≤ ||P(ρ_1)−P(ρ_0)||_{H^{1/2}} ≤ (C_F+Cδ)||h||₂.

Choose δ<c_F/C. Equality of all perimeter data forces h=0. This is uniform in harmonic frequency and provides a direct two-point proof, without claiming a Banach inverse-function theorem on C².

## 6. Why mere pointwise closeness would have been insufficient

For even N≥2 let b_N(u)=Re(u_1+i u_2)^N. This is a degree-N spherical harmonic with ||b_N||∞=1 and ||b_N||₂ ≍ N^{−1/4}. Set E_N(x,u)=εb_N(u). Then ||E_N||∞=ε, but

F^{-1} T_{E_N}1 = ε(2π/λ_N)b_N,

so

||F^{-1}T_{E_N}||_{L²_even→L²_even} ≥ c ε N^{1/4}.

Thus there is no universal estimate ||F^{-1}T_E||≤C||E||∞. The positive weight 1+E_N remains strictly positive when ε<1. (This does not claim that these particular weighted transforms fail injectivity; it only disproves the invalid norm estimate.) The normal-derivative control above is the precise missing hypothesis that the actual perimeter geometry happens to furnish.

## Scope

This calculation addresses only the analytic estimate for local C²-near-ball injectivity and its appropriate function spaces. It does not establish novelty, solve global uniqueness, validate other portions of an author manuscript, or replace independent final review.
