# Function Theory 6.10: verification of the Guo–Hu counterexample

Problem **2306010 / AMR-022-6010**, queue rank **581**. Reconstruction dated 2026-10-04.

## Attribution and exact conclusion

This is a verification and expanded reconstruction of the counterexample of **Yuankai Guo and Xiaozhe Hu**, *A Counterexample to a Problem of Pommerenke on Convex Functions in the Class Σ*, [arXiv:2609.04279v1](https://arxiv.org/abs/2609.04279v1), submitted 3 September 2026. The construction and exact certificate below are theirs. Their paper is distributed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). This reconstruction changes the exposition, supplies an explicit elementary geometric bridge, and uses independent standard-library rational controls. No new solution or priority is claimed.

Write E = {z ∈ C : |z| > 1}. The class Σ consists of univalent analytic functions on E with Laurent normalization f(z) = z + b₀ + b₁z⁻¹ + ⋯. Hayman's source additionally fixes b₀ = 0; every function constructed here has that stronger normalization. An exterior-convex member has a convex omitted set C \ f(E). The question is whether exterior convexity of F and G forces exterior convexity of λF + (1−λ)G for every 0 < λ < 1. The answer is **no**. We verify convex F,G ∈ Σ and H = (3/5)F + (2/5)G ∈ Σ whose omitted set is not convex.

The proof does not depend on the correctness or successful compilation of any Lean project, nor on Pommerenke's general convex-combination univalence theorem. Its standard analytic ingredients are Laurent-series differentiation, the binomial power series, the argument principle, the Jordan curve theorem, and the harmonic minimum principle.

## 1. Parameters and analytic construction

Set

q = 1/3 − i/6,  w = 1−q³ = 107/108 + 11i/216,
r = 399/400,  α = 8/9 + 4i/9,  β = w/r³,
z₀ = 1/r = 400/399,  λ = 3/5.

In particular

|α|² = 80/81 < 1,
|w|² = 45917/46656,
r⁶−|w|² = 2785244627851129 / 2985984000000000000 > 0.

Thus |β| < 1. These are exact rational inequalities. Define

F(z) = z + α/z,
G(z) = z + Σ[n≥1] binom(2/3,n)(−β)ⁿ z^(1−3n)/(1−3n).

Choose any ρ with |β|^(1/3) < ρ < 1. The series for G and its derivatives converge locally uniformly on |z| > ρ. This follows from the radius-one binomial power series in β/z³ and termwise integration, or directly from its ratio test. No z⁻¹ term occurs in G′, so the displayed Laurent series supplies a genuinely single-valued primitive; no unjustified integration on a multiply connected domain is needed. We have

G′(z) = exp((2/3) Log(1−βz⁻³)),
G(z) = z + O(z⁻²),
G″(z)/G′(z) = 2βz⁻⁴/(1−βz⁻³).

Here Log is the principal logarithm. For |z| > ρ, the base 1−βz⁻³ lies in the open disk with center 1 and radius 1, hence in the right half-plane. The logarithm is analytic there, and G′ is nonzero. Finally put H = λF + (1−λ)G. Each function is analytic on a neighborhood of the closed exterior {|z| ≥ 1} and has the required Laurent normalization.

## 2. A direct injectivity certificate, including the boundary

Suppose f(z) = z + Σ[j≥1] cⱼ z^(−mⱼ), with positive integer exponents, a convergent Laurent expansion on a neighborhood of the closed exterior, and

S = Σ[j≥1] mⱼ|cⱼ| < 1.

For |z|,|v| ≥ 1, factoring powers of 1/z and 1/v gives

|z^(−m)−v^(−m)| ≤ m|z⁻¹−v⁻¹| ≤ m|z−v|.

Absolute convergence and the triangle inequality imply

|f(z)−f(v)| ≥ (1−S)|z−v|.

Thus f is injective on the closed exterior. Differentiating the locally convergent series also gives |f′(z)−1| ≤ S < 1 there. In particular the derivative never vanishes, including on the unit circle.

For aₙ = |binom(2/3,n)|, n ≥ 1, elementary binomial algebra yields

a₁ = 2/3,
aₙ₊₁ = aₙ(3n−2)/(3n+3).

All aₙ are positive. Set Tₙ = (3n/2)aₙ. Then T₁ = 1 and Tₙ−Tₙ₊₁ = aₙ. Consequently Σ[n=1..N] aₙ = 1−Tₙ₊₁ ≤ 1 for every N, so Σ[n≥1] aₙ ≤ 1. This upper bound alone is sufficient; no limit evaluation of Tₙ is needed.

With b = |β| < 1, we obtain

S_F = |α| < 1,
S_G = Σ[n≥1] aₙbⁿ ≤ b Σ[n≥1] aₙ ≤ b < 1,
S_H = λ|α| + (1−λ)S_G < λ + (1−λ) = 1.

The exponents from F and G are respectively 1 and 3n−1, so the formula for S_H is literal. Therefore F,G,H are injective on the closed exterior, have nonzero derivatives there, and belong to Σ. A useful explicit bound is |α| < 179/180, so S_H < (3/5)(179/180)+2/5 = 299/300. In particular |H′| > 1/300 throughout the closed exterior. This is a continuum conclusion from the series proof, not from a finite sample.

## 3. The geometric bridge proved for these maps

We establish exactly the exterior-convexity implications needed here. Let f be one of the above normalized maps, with weighted tail S < 1, and write

γ(t) = f(e^(it)),  P_f(z) = 1 + zf″(z)/f′(z).

The boundary γ is a regular smooth Jordan curve. Let K be its bounded closed Jordan region.

### 3.1. Identifying the omitted set and orientation

For y off γ and R sufficiently large, the winding number of f(Re^(it)) about y is 1: f(z) = z + O(1) at infinity makes this loop homotopic to the large circle without crossing y. Applying the argument principle to f−y on 1 < |z| < R gives

number of preimages of y in the annulus = 1 − Ind(γ,y).

For y in the bounded region of a Jordan curve, Ind(γ,y) is either +1 or −1. The value −1 would produce two preimages, contradicting injectivity; all zeros are simple because f′ is nonzero. Hence the orientation is counterclockwise and the winding number is +1 inside. The formula now gives zero preimages inside and one outside. Boundary points cannot have a preimage with |z| > 1 because f is injective on the closed exterior. Therefore f(E) = C \ K.

### 3.2. Positive boundary turning makes K convex

Since |f′−1| ≤ S < 1, the principal logarithm of f′ is continuous on the circle and periodic. A continuous tangent-angle lift is

θ(t) = t + π/2 + Im Log(f′(e^(it))).

It satisfies θ(t+2π) = θ(t)+2π. Differentiation gives

θ′(t) = Re P_f(e^(it)).

If this derivative is strictly positive everywhere, fix t₀ and rotate the tangent at γ(t₀) to point along the positive real axis. The signed height

h(t) = Im(e^(−iθ(t₀))(γ(t)−γ(t₀)))

has derivative |γ′(t)| sin(θ(t)−θ(t₀)). As t runs from t₀ to t₀+2π, θ increases strictly through exactly 2π. Thus h first strictly increases until the angle difference is π, then strictly decreases back to h(t₀+2π)=0. It follows that h(t)>0 for every t strictly between the endpoints. Every tangent line therefore supports the entire curve on its left side.

For completeness this implies convexity of the whole Jordan region, not just a local curvature property. Let C be the compact convex hull of γ. The supporting-line conclusion places every point of γ on ∂C. The curve is noncollinear, so C has interior and its boundary is a Jordan curve. A Jordan curve contained in another Jordan curve must equal it: otherwise remove a point of the latter outside the former, embedding a circle into an open interval, which is impossible. Hence γ = ∂C and K=C by the Jordan curve theorem. In particular K is convex.

### 3.3. Convexity forces a nonnegative analytic quantity throughout E

Conversely suppose K is convex. At every regular boundary point its oriented tangent line supports K on the left. For the same h(t), h(t) ≥ 0 near t₀ and h(t₀)=h′(t₀)=0, so

0 ≤ h″(t₀) = |γ′(t₀)|θ′(t₀).

Thus Re P_f ≥ 0 on |z|=1. The function P_f is analytic on the exterior and at infinity, where it equals 1, since f′ never vanishes there and f has the normalized Laurent expansion. The function P_f(1/ζ) extends analytically to ζ=0 and continuously to |ζ|≤1. The harmonic minimum principle applied to its real part gives Re P_f(z) ≥ 0 for every |z|>1.

This proves the needed necessity without assuming that positivity of a sampled interior quantity characterizes arbitrary boundary behavior.

## 4. Convexity of F and G

Direct differentiation gives

P_F(z) = (1+αz⁻²)/(1−αz⁻²),
P_G(z) = (1+βz⁻³)/(1−βz⁻³).

For every complex u with |u|<1,

Re((1+u)/(1−u)) = (1−|u|²)/|1−u|² > 0.

Because |α|,|β|<1, these expressions have strictly positive real part on the entire closed exterior, in particular its unit circle. Section 3.2 therefore shows that the omitted sets of F and G are convex. Both are exterior-convex members of Σ with all hypotheses of the question satisfied.

## 5. Exact nonconvexity certificate for H

At z₀=1/r, βz₀⁻³=w and 1−w=q³. The principal-power branch must be checked before replacing this expression by q². Indeed Re q>0 and Im q<0, while

3(Im q)² = 1/12 < 1/9 = (Re q)².

It follows that −π/6 < arg q < 0, so −π/2 < 3 arg q < 0. Therefore Log(q³)=3 Log(q), and the chosen branch gives

G′(z₀) = (q³)^(2/3) = q² = 1/12−i/9,
z₀G″(z₀) = 2w/q.

Also F′(z₀)=1−αr² and z₀F″(z₀)=2αr². Define

D = H′(z₀) = (3/5)(1−αr²)+(2/5)q²,
N = H′(z₀)+z₀H″(z₀)
  = (3/5)(1+αr²)+(2/5)(2/q−q²).

Exact Gaussian-rational arithmetic gives

D = (184794−557603i)/1800000,
N = (5431206+2285603i)/1800000,
N/D = (−54160961609+690164496000i)/69013985609.

In particular D is nonzero and

Re P_H(z₀) = −54160961609/69013985609 < 0.

If H omitted a convex set, Section 3.3 would force this real part to be nonnegative. This contradiction proves that H is not exterior-convex. All of F,G,H remain univalent and normalized, and λ=3/5 lies strictly between 0 and 1. This settles the exact question negatively.

## 6. Verification boundary

`verify.py` independently calculates the rational certificate with Python `fractions.Fraction`, checks explicit norm/sector inequalities, and exercises supporting algebraic identities and deliberate negative controls. Finite checks are regression controls only. The general analytic, topological and infinite-series claims are proved above; they are not certified by running that script.

The prior author's public Lean repository was inspected at commit `bdc48d75778148730d551812647bfdac82d51df3`, particularly its analytic and geometric end-to-end theorem statements. A Lean compiler and Lake were not installed in this environment, so no local Lean build was performed. No blanket claim about the full formal dependency graph, absence of axioms, or successful kernel checking is made by this packet. The complete conventional proof above is the basis of the proposed `already_solved` classification. A fresh independent audit remains a separate requirement.
