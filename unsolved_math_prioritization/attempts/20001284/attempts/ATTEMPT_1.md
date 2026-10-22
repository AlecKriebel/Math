# Author attempt 1: uniform C² local uniqueness by a weighted Funk estimate

2026-10-03 UTC. Status: substantive written proof, pending independent challenge.
Goal: eliminate the fixed finite-harmonic-band restriction near the ball. This cannot resolve the original global question.

## Setting
On S² with area measure dσ and great-circle arclength ds, let ρ>0 be even and C². Its central-section perimeter is
P(ρ)(θ)=∫_{u·θ=0} (ρ(u)²+(∂sρ(u))²)^(1/2) ds.
All Sobolev spaces below use the spectral norm
||f||_{H^s}²=Σ_{l,k}(1+l(l+1))^s |f_{lk}|²
for real L²(dσ)-orthonormal spherical harmonics Y_lk. Put Fh(θ)=∫_{u·θ=0}h(u)ds.

The classical Funk–Hecke formula gives F Y_lk=λ_l Y_lk, λ_l=2π P_l(0). On even l=2j,
λ_{2j}=2π(-1)^j (2j)!/(2^(2j)(j!)²).
Consequently there exist absolute 0<c_F≤C_F<∞ such that, for every even L² function h,
c_F||h||_2 ≤ ||Fh||_{H^(1/2)} ≤ C_F||h||_2.
For explicit nonoptimal constants one may take c_F=π and C_F=2√2π. Write b_j=binom(2j,j)/4^j. For j≥1, elementary induction using b_{j+1}/b_j=(2j+1)/(2j+2) proves 1/(2√j)≤b_j≤1/√(j+1). The lower induction reduces to (2j+1)²≥4j(j+1); the upper one reduces to (2j+1)²(j+2)≤4(j+1)³. Combining these with 4j²≤1+2j(2j+1)≤4(j+1)² gives the stated bounds; j=0 is immediate. The upper bound also holds without parity because odd degrees are killed.

## Exact linearization, with no derivative on the unknown
Let a=ρ, b=∂sρ, c=∂s²ρ and q=(a²+b²)^(1/2) along a great circle. Differentiation followed by periodic integration by parts gives
DP_ρ[h](θ)=∫[(a/q)h+(b/q)∂sh]ds=∫w_ρ(θ,u)h(u)ds,
w_ρ=a(a²+2b²−ac)/(a²+b²)^(3/2).
Check: (b/q)'=(a²c−ab²)/(a²+b²)^(3/2), so subtracting from a/q gives exactly the displayed numerator.

Extend this weight OFF incidence to all S²_θ×S²_u by putting
v=θ×u, a=ρ(u), b=∇ρ(u)·v, c=Hess_{S²}ρ(u)[v,v]
and using the same rational formula. On incidence |v|=1 and its integral curves are great circles, so the extension agrees with the exact derivative. For each fixed u it is smooth in θ even when ρ is only C² in u. The extension is even in θ and, if ρ is even, even in u. At every constant ρ=R the extension equals 1 on the entire product sphere, not just on incidence.

Set b_ρ=w_ρ−1 and M(b)=sup_{θ,u}|(1−Δ_θ)² b(θ,u)|. There is an absolute C_* such that
M(b_ρ)≤C_* ||ρ/R−1||_{C²}
when ||ρ/R−1||_{C²}≤1/2, for any fixed standard C² norm controlling function, gradient and covariant Hessian. Explanation: rescale to R=1. The formula is a smooth finite-dimensional function of (a,g,H,θ,u) on compact a∈[1/2,3/2], |g|,|H|≤1/2, θ,u∈S². Its θ derivatives up to order four require no u derivatives of g or H. They vanish at (a,g,H)=(1,0,0). The mean value theorem on this compact parameter set gives the bound. Pure a variation in fact leaves w=1.

## Weighted operator bound
For any continuous b(θ,u) with four continuous θ derivatives and finite M(b), expand only in θ:
b(θ,u)=Σ_{l,k}Y_lk(θ)a_lk(u),
a_lk(u)=∫_{S²}b(θ,u)Y_lk(θ)dσ(θ).
Integration by parts twice with 1−Δ_θ gives
||a_lk||_∞ ≤ sqrt(4π) M(b)/(1+l(l+1))².
Let A_l=sqrt((2l+1)/(4π)) [1+sqrt(l(l+1))]. The addition theorem and its differentiated version imply
||Y_lk||_∞≤sqrt((2l+1)/(4π)),
||∇Y_lk||_∞≤sqrt(l(l+1)(2l+1)/(4π)).
Thus multiplication by Y_lk is bounded on L² and H¹ by at most A_l (use the product rule, and the L²⊕gradient L² Hilbert norm). Hilbert-scale interpolation gives the same bound on H^(1/2).

It follows that T_bh(θ)=∫_{u·θ=0}b(θ,u)h(u)ds satisfies
||T_bh||_{H^(1/2)} ≤ K M(b)||h||_2,
K=C_F sqrt(4π) Σ_{l≥0}(2l+1)A_l/(1+l(l+1))² <∞.
The summand is O(l^(−3/2)); no truncation or constant depending on a harmonic cutoff occurs. An explicit majorant is K≤C_F[1+9√3(1+√2)]: for l≥1, use 2l+1≤3l, 1+sqrt(l(l+1))≤(1+√2)l, 1+l(l+1)≥l², and Σ_{l≥1}l^(−3/2)≤3. Initially the identity T_bh=ΣY_lk F(a_lk h) is for continuous h: the series for b converges uniformly, and the H^(1/2) series converges absolutely by the displayed bound. It extends to L² by density. No u-derivative of a_lk is needed because it multiplies the input in L². Parity of a_lk is useful but not needed for the upper estimate.

## Two-body conclusion
For positive even C² functions ρ_0,ρ_1 with ||ρ_i/R−1||_{C²}<ε, let h=ρ_1−ρ_0 and ρ_t=ρ_0+t h. The segment remains in that C² ball. The fundamental theorem of calculus yields
P(ρ_1)−P(ρ_0)=Fh+T_{bbar}h,
bbar=∫_0^1(w_{ρ_t}−1)dt,
M(bbar)≤C_* ε.
Hence
||P(ρ_1)−P(ρ_0)||_{H^(1/2)}≥(c_F−KC_*ε)||ρ_1−ρ_0||_2.
Choose ε<min(1/2,c_F/(2KC_*)). This proves local two-body injectivity and the stability bound
||ρ_1−ρ_0||_2 ≤ (2/c_F)||P(ρ_1)−P(ρ_0)||_{H^(1/2)}.
The C² neighborhood is uniform over all spherical-harmonic cutoffs. Convexity is not used. There is no statement about C¹ neighborhoods, global uniqueness, or finite data for arbitrary C² functions.

## Attempt outcome and remaining gap
This yields a stronger local theorem than the imported bandlimited argument if the weighted-operator proof survives audit. The global problem is unchanged: positivity alone supplies no small M(w−1), and general star bodies may have negative section curvature. No historical novelty claim is made. The norm estimate and its unusual one-variable regularity are the central points for independent review.
