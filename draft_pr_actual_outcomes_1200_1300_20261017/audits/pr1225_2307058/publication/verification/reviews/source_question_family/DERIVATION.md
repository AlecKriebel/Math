# A direct potential and path argument

Written independently from the original question only. No submitted proof or project analysis was inspected.

## 1. Claim and conventions

Let E be compact in [0,1]×{0} and let C={z:|z|=2}. For disjoint sets A,B, let Γ(A,B) contain all nonconstant continuous curves γ:[0,1]→R² with γ(0)∈A and γ(1)∈B (orientation is immaterial). First restrict to globally rectifiable curves. For a Borel density ρ:R²→[0,∞], define its curve integral using arclength measure, and

    M₂(Γ)=inf { ∫ρ² dA : ∫γρ ds ≥1 for every γ∈Γ }.

Values ∞ are allowed, including on area-null sets. A value at an endpoint is integrated against arclength and carries no point mass. The infimum of the empty admissible class is ∞. We prove

    M₂(Γ(E,C))>0  ⇒  M₂(Γ(E,R\E))=∞.                 (1)

The same proof works when curves are only locally rectifiable on (0,1), have the stated endpoint limits, and the integral is defined by exhaustion of interior subcurves. Every polygonal curve used below is globally rectifiable; every smooth test density used below is admissible also for that larger curve class.

Assume toward contradiction that a Borel ρ of finite area energy is strongly admissible for Γ(E,R\E).

## 2. A pointwise lower-semicontinuous majorant

On any fixed bounded open square Q containing [-2,2]², ρ has a lower-semicontinuous majorant g≥ρ with finite L²(Q); we may also require g≥1 on [-2,2]².

Here are the details, including null-set values. Extend ρ1_Q by zero outside Q. For each integer k put A_k={ρ1_Q>2^k}. By outer regularity choose open U_k⊃A_k with |U_k\A_k|=δ_k so small that

    Σ_{k∈Z} 2^k sqrt(δ_k)<1.

The nonnegative sum g₀=Σ_k2^k1_{U_k} is lower semicontinuous. The dyadic geometric series shows g₀≥ρ1_Q pointwise, even at infinite values, and

    ||g₀||₂ ≤2||ρ1_Q||₂+Σ_k2^k sqrt(δ_k)<∞.

Adding the indicator of a slightly smaller open square containing [-2,2]² gives g≥1 there while preserving finite local energy. We retain the pointwise inequality, not merely an almost-everywhere replacement.

## 3. Finite admissible energy forces |E|₁=0

Put D=[-2,2]² and F_D=([-2,2]×{0})\E. Define

    d(z)=inf {∫γg ds : γ is a rectifiable path in D from F_D to z},
    u(z)=min(1,d(z)).

Then u=0 on F_D, u=1 on E, and for every rectifiable path σ in D with endpoints z,w,

    |u(z)-u(w)| ≤ ∫σg ds.                            (2)

The inequality follows by concatenation and truncation; it remains true if an infimum is infinite.

For completeness u is Borel, so the following use of Fubini does not hide a measurability assumption. Exhaust F_D by compact sets

    K_j={ (t,0): |t|≤2, dist((t,0),E)≥1/j }.

For a compact K_j, the sublevel sets of g-distance from K_j are compact. Indeed g≥1 makes Euclidean lengths bounded by g-lengths; constant-speed parametrizations lie in a compact uniformly Lipschitz family, and weighted length for a lower-semicontinuous nonnegative weight is lower semicontinuous under uniform convergence. The latter follows first for a continuous weight by partition sums, then by increasing continuous approximation of g. Thus {d<a} is a countable union of compact sublevel sets for K_j and rational thresholds below a.

By Fubini, g is integrable on almost every vertical and horizontal line segment in D. Inequality (2) makes u absolutely continuous on each such segment, with |∂_xu|≤g and |∂_yu|≤g almost everywhere. Hence u∈W^{1,2}(int D). On almost every vertical line its pointwise value at height zero is its ordinary continuous slice value.

Choose η∈C_c^∞(int D), equal to 1 on a neighborhood of E. Extend v=ηu by zero outside D. Then v∈W^{1,2}(R²), and its upper-half-plane trace is precisely

    f(t)=v(t,0)=1_E(t)  almost everywhere.            (3)

There is no assumption that pointwise Sobolev values on E are automatically traces: the almost-everywhere statement (3) follows from the vertical absolute continuity just proved.

Here is the required trace fact without invoking any touching-plate condenser equivalence. For a smooth compactly supported v, Fourier transformation in x and integration in y>0 give, for each ξ,

    |ξ| |v̂(ξ,0)|²
      ≤ ∫₀^∞ (|∂_yv̂(ξ,y)|²+ξ²|v̂(ξ,y)|²)dy.

This is integration of -∂_y|v̂|² followed by 2ab≤a²+b². Integrating ξ and using Plancherel proves that f has finite homogeneous H^{1/2}(R) seminorm. Approximation proves the same for v∈W^{1,2}; its trace agrees with the continuous vertical slice values. Equivalently, by Plancherel applied to translations,

    ∬ |f(t)-f(s)|²/|t-s|² dt ds <∞.                 (4)

A compactly supported characteristic function with finite seminorm (4) must vanish almost everywhere. To see this, let

    D(h)=||1_E(·+h)-1_E||₁=||1_E(·+h)-1_E||₂².

Equation (4) gives ∫₀¹D(h)h^{-2}dh<∞. Thus there is h_n↓0 with D(h_n)/h_n→0. For every smooth compactly supported test function ψ, the difference-quotient formula yields

    |∫1_E ψ'| ≤ ||ψ||∞ lim_n D(h_n)/h_n=0.

Therefore the distributional derivative of 1_E is zero. It is a constant almost everywhere, and its bounded support forces that constant to be zero. Consequently

    |E|₁=0.                                        (5)

## 4. Positive original modulus supplies a finite-potential point

Set O=B(0,3/2) and define f=g1_O, with value zero outside O. This is a nonnegative lower-semicontinuous L² function of compact support; it agrees with g on a neighborhood of E. Write

    I₁f(x)=∫ f(z)/|z-x| dA(z).

We claim that there exists x∈E with I₁f(x)<∞. Suppose instead it is infinite everywhere on E.

There are increasing nonnegative continuous compactly supported f_n≤f with f_n↑f. For example take

    f_n(z)=min(n, inf_w(f(w)+n|z-w|)).

Lower semicontinuity gives pointwise convergence. Since f=0 off O, every f_n is zero there as well. Put v_n=I₁f_n. Each v_n is continuous, and v_n↑∞ pointwise on E. Compactness of E and monotonicity imply that for every T>0 some n has v_n>2T throughout E.

The Fourier transform of |z|^{-1} in R², with convention exp(-iz·ξ), is 2π|ξ|^{-1}. Thus, in the distributional sense and by Plancherel,

    ||∇v_n||₂=2π||f_n||₂≤2π||f||₂.                 (6)

This identity can also be obtained by writing |z|^{-1} as a positive integral of Gaussians and transforming those Gaussians; no potential-theory or condenser duality is assumed.

Fix η₀∈C_c^∞(B(0,2)) equal to 1 near E. On its support, v_n is the convolution of f_n with the truncated kernel 1_{|z|<4}/|z|. The latter has L¹ norm 8π, so Young's inequality gives

    ||v_n||_{L²(supp η₀)}≤8π||f||₂.

Combining this with (6) yields

    ||∇(η₀v_n)||₂≤C||f||₂                          (7)

for a constant independent of n and T. The continuous compactly supported function η₀v_n is >2T on E. Smooth it at a sufficiently small scale; uniform approximation preserves a lower bound T on a neighborhood of E, and the gradient L² norm does not increase. The smoothing scale can be chosen to keep its support inside B(0,2). Dividing by T produces a smooth function φ_T supported in B(0,2), with φ_T≥1 near E, and

    ∫|∇φ_T|² dA≤C²||f||₂²/T².                     (8)

The density |∇φ_T| is admissible for all curves from E to C. The ordinary chain rule gives integral at least the endpoint change, which is ≥1. The same holds along locally rectifiable curves by applying the chain rule on interior subcurves and passing to endpoint limits. Equation (8) would force M₂(Γ(E,C))=0, contrary to the hypothesis. Therefore a point x∈E with finite I₁f(x) exists.

## 5. Small polygonal paths contradict admissibility

Fix this x=(x₀,0). For small r>0 let

    I_r=(x₀-r,x₀+r)×{0},
    Q_r=(x₀-r,x₀+r)×(0,r).

They lie inside O. Choose y uniformly in I_r\E and z uniformly in Q_r. By (5), removing E does not change line integrals or the normalization |I_r\E|₁=2r. Join x to z and then z to y by straight segments. The resulting curve has all interior points in the open upper half-plane and is globally rectifiable.

For the first segment, the substitution w=x+t(z-x), its Jacobian t², and |z-x|≤√2r give

    average_z ∫_[x,z] f ds
      ≤ ∫_{B(x,√2r)} f(w)/|w-x| dA(w).              (9)

For clarity, after bounding the segment speed by √2r, its averaged parameter integral is at most

    (√2/(2r)) ∫ f(w) [∫_{|w-x|/(√2r)}¹t^{-2}dt]dA(w),

which is bounded by the right side of (9).

For the second segment one has the scale-invariant estimate

    average_{y,z} ∫_[y,z] f ds ≤10||f||_{L²(Q_r)}.  (10)

Here are explicit kernel details. Scale to r=1, x=0, and replace f(w) by f_r(w)=r f(x+rw), preserving its L² norm. Write y∈(-1,1), z=(a,b)∈(-1,1)×(0,1). Segment speed is ≤√5, and its point at parameter t is ((1-t)y+ta,tb). Substituting w for (a,b) has Jacobian t². For fixed w,t, the allowable y-interval has length at most 4t when t≤1/2 and at most 2 otherwise. The resulting averaging kernel is bounded by

    4 log(1/w₂)+8,  0<w₂<1.

Its squared integral on (-1,1)×(0,1) is 320. Multiplying its L² norm by the averaging/speed factor √5/4 gives 10. Cauchy–Schwarz proves (10). All substitutions apply to nonnegative Borel functions by Tonelli, including infinite values on area-null sets.

Since I₁f(x)<∞, the right side of (9) tends to zero as r↓0. Absolute continuity of the area integral makes the right side of (10) tend to zero as well. Thus the average f-length of these polygonal E-to-(R\E) curves tends to zero. For sufficiently small r, at least one such curve has f-length <1. It lies in O, where f=g≥ρ pointwise, and so its ρ-length is <1. This contradicts admissibility and proves (1).

## 6. Exceptional families and boundary conventions

The argument did not replace ρ by an almost-everywhere equivalent density: the lsc majorant dominates it at every point. In particular ∞ values on a null line, a null compact set, or a dense area-null set remain covered. Segment averaging uses exact arclength integrals and Tonelli; endpoints carry zero arclength mass.

If admissibility is required only outside a family Γ₀ of modulus zero, choose Borel h_j admissible for Γ₀ with ||h_j||₂≤2^{-j}. Then h=Σ_jh_j is in L² and ∫γh=∞ for every γ∈Γ₀. For every ε>0, ρ+εh is strongly admissible and has finite energy whenever ρ does. The impossibility of finite strong admissible energy therefore also rules out finite weak admissible energy.

For globally rectifiable curves, all arguments above apply literally. For locally rectifiable curves with endpoint limits, target admissibility implies admissibility for the polygonal subfamily; the smooth densities in Section 4 are admissible for the larger capacity family by endpoint limits. Thus the same implication holds for both conventions without asserting an unproved equality between their moduli.

No assertion is made for a nonstandard convention that charges endpoint point masses, or defines a line integral by arbitrary representative changes along curves. Those differ from arclength modulus.

## 7. Logical dependency summary

The proof uses outer regularity and Tonelli, elementary weighted path-length compactness, the ACL characterization of W^{1,2}, Plancherel and the Fourier transform of the planar Riesz kernel, smoothing, and the ordinary smooth chain rule. The path-potential measurability, trace rigidity, finite-potential endpoint, and short-curve averaging are supplied above. No equality between touching-plate condenser energy and curve modulus, or between logarithmic and conformal capacities, is used.
