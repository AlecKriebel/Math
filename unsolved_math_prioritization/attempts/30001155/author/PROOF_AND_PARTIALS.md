# Area-refined Dirichlet spectral gaps: checked partial results

Problem 30001155 / OWR-3389-006. Research date: 2026-10-04.
Status: the full conjecture remains unresolved in this work. Five substantive approach families were attempted. No historical novelty claim is made for the special cases below. AI-assisted, unrefereed research notes; independent audit pending.

## 1. Exact target and conventions

Let K be a bounded open convex subset of R² with nonempty interior. Let A be its area and d its Euclidean diameter. Eigenvalues are those of the **Dirichlet Laplacian −Δ**, defined by the H₀¹(K) min–max principle, counted with multiplicity: 0 < λ₁ < λ₂ ≤ λ₃ ≤ … . Write γ(K)=λ₂−λ₁. There is no potential. Convex domains with corners are allowed; smoothness is not part of the conjecture. An infinite strip itself has continuous spectrum and is not an admissible bounded-domain equality case.

Let B₁ be a disk of area one, g=γ(B₁), and set

B(A,d) = 12π²g / {3π³d² + (4g−3π³)√(d⁴−16A²/π²)}.

The question is whether γ(K)≥B(A,d) for every such K, with finite equality only for disks and a sharp elongated-strip limit. The source is Freitas's contribution to the 2009 Oberwolfach report, printed p.395, Conjecture 2. Its preceding Conjecture 1 is just γ≥3π²/d². The source explicitly specifies Dirichlet eigenvalues. The radicand contains π⁻²; omitting it would make it negative at a disk. This factor was verified visually in the publisher PDF. The corrected upstream record already has it.

For bounded convex planar domains, the usual Sobolev Dirichlet realization is well-defined without C² boundary. The boundary is Lipschitz. Smooth approximation, when needed, must preserve the limiting eigenvalues; none of our explicit special cases requires treating corners as smooth.

## 2. Normalization and why the known fundamental gap is insufficient

Let x=j₀,₁², y=j₁,₁², Δ=y−x, so the unit-radius disk has gap Δ and g=πΔ. Put

q=4A/(πd²), s=√(1−q²), θ=1−3π²/(4Δ).

The isodiametric inequality gives 0<q≤1. Algebra transforms the target into

d²γ(K) ≥ F(q),  F(q)=3π²/[1−θ(1−√(1−q²))].                 (2.1)

The rational certificates in §6 prove 0<θ<1/2. Approximate values, used only for orientation, are Δ≈8.8987846792, θ≈0.1681781763 and F(1)=4Δ≈35.5951387167. Thus F is strictly increasing on (0,1), with F(0)=3π² and F(1)=4Δ. The target has correct scaling: both sides of the original inequality scale as length⁻². A disk of radius R has A=πR², d=2R and γ=Δ/R², and attains equality exactly.

Andrews–Clutterbuck prove d²γ≥3π² for convex domains, even with a convex potential. This is strictly weaker than (2.1) whenever A>0. It does not prove the area refinement.

Theorem 1 of Amato–Bucur–Fragalà, arXiv:2407.01341v2, proves, for bounded open convex domains, γ≥3π²/d²+c w⁶/d⁸, where w is minimal width and c>0 depends only on dimension. This also proves strictness of the fundamental-gap lower bound for genuine two-dimensional domains. It neither supplies the conjectured constant nor its required power. Since A≤dw, it implies the area-form estimate γ≥3π²/d²+c A⁶/d¹⁴. Meanwhile expansion of (2.1) at q=0 gives

B(A,d)=3π²/d²+24θ A²/d⁶+O(A⁴/d¹⁰).

The powers do not match. On thin rectangles of length one and width ε, a fixed multiple of w⁶/d⁸ is O(ε⁶), while B−3π²/d² is a positive multiple of ε². Therefore the quoted quantitative theorem **alone** cannot establish the target by comparing its right-hand side. This is a failure of that inference, not a counterexample to either theorem.

Strictness of γ>3π²/d² does not settle equality in γ≥B(A,d): B is already larger than 3π²/d². The two rigidity questions must remain separate.

## 3. All rectangles, strictly; sharp rectangular degeneration

**Proposition 3.1.** Every nondegenerate rectangle satisfies γ>B(A,d).

Proof. Let its side lengths be a≥b>0 and r=b/a≤1. Separation of variables gives λ₁=π²(a⁻²+b⁻²), λ₂=π²(4a⁻²+b⁻²) (allowing the square's multiplicity), and hence d²γ=3π²(1+r²). Also q=4r/[π(1+r²)]. For 0<q<1,

θ(1−√(1−q²)) = θ q²/(1+√(1−q²)) < q²/2
= 8r²/[π²(1+r²)²] < r²/(1+r²),

where θ<1/2 and π²>8 were used. Consequently the denominator in (2.1) is greater than 1/(1+r²), giving F(q)<3π²(1+r²). This proves the proposition for the entire continuous family, not only a finite sample. ∎

As r→0, both d²γ and F(q) tend to 3π²; their ratio tends to one. With fixed b and a→∞, centered rectangles converge locally to an infinite strip and are asymptotically sharp in the meaningful relative/diameter-normalized sense. Their unnormalized gap is 3π²/a². This proves one precise strip-saturation mechanism, not a classification of all extremizing sequences.

## 4. Every triangle follows from an existing theorem

Lu–Rowlett, *The fundamental gap of simplices*, Theorem 3, prove d²γ(T)≥64π²/9 for every triangle, with equality precisely for the equilateral triangle. As F(q)≤4Δ<6π²<64π²/9, every triangle satisfies the area refinement strictly. This is a corollary of their published result, not a new triangle theorem. The bound 4Δ<6π² is certified in §6. Even the equilateral triangle does not attain equality in this much weaker area bound.

The cited theorem includes a computer-assisted part in its original proof. We inspected its statement and relevant scope, not a fresh reconstruction of that paper's entire computational proof. Our result is explicitly conditional on accepting the cited theorem as established literature.

## 5. A certified near-circular ellipse range

**Proposition 5.1.** An ellipse with semiaxes a≥b and b/a≥√15/4 satisfies the conjectured inequality. It is strict unless a=b.

Proof. Scale to a=1 and put t=b/a, u=√(1−t²). The pullback to the unit disk turns its Dirichlet Rayleigh quotient into

Q_t(v) = ∫_D (|∂ₓv|²+t⁻²|∂ᵧv|²) / ∫_D |v|².

Since Q₁≤Q_t≤t⁻²Q₁, min–max implies λ₂(E)≥y and λ₁(E)≤x/t². Thus

d²γ(E) ≥ 4[Δ−xu²/(1−u²)].

For this ellipse d=2 and q=t. Subtracting F(t)=4Δ(1−θ)/(1−θ+θu), the obtained lower bound for the difference is

4u P(u)/[(1−θ+θu)(1−u²)],

where

P(u)=Δ−3π²/4 − [3π²x/(4Δ)]u − θyu².                 (5.1)

All coefficients subtracted on the right are positive. It suffices to bound (5.1) from below at u=1/4. The exact rational calculation in §6 gives P(u)>273124119/3618160000>0 for 0≤u≤1/4. Thus strictness holds for 0<u≤1/4; at u=0 the domain is a disk and equality was computed above. The condition u≤1/4 is equivalent to t≥√15/4. ∎

Keeping the exact Bessel constants rather than the convenient rational certificate extends this sufficient comparison up to the unique positive root of P, numerically u≈0.2728809632, or t≈0.9620478054. This numerical threshold is not substituted for the certified √15/4≈0.9682458366 range. The comparison loses usefulness for thinner ellipses; a negative lower estimate there says nothing about the actual gap.

## 6. Exact constant certification and how to replay it

The code verify_exact.py uses only the Python standard library and exact rational arithmetic. It does not numerically solve the PDE. The classical rational bounds 157/50<π<22/7 are used.

Write J_n(z)=(z/2)^n Σ_{k≥0}(−1)^k (z²/4)^k/[k!(k+n)!]. Alternating-series bounds give:

J₀(12/5)>0, J₀(241/100)<0, J₁(383/100)>0, J₁(96/25)<0.

J₁(z)≥(z/2)(1−z²/8)>0 for 0<z≤241/100, so J₀ decreases strictly there and its first positive zero lies between 12/5 and 241/100. To identify the first J₁ zero, not just some zero, form the upper alternating truncation P₈(t)=Σ_{k=0}^8(−1)^k t^k/(k!)². Its nine Bernstein coefficients on t∈[(241/100)²/4,(96/25)²/4] are all strictly negative; the exact fractions are output by the verifier. Therefore J₀(z)<0 throughout z∈[2.41,3.84]. At any zero of J₁ in that interval, the identity J₁'=J₀−J₁/z makes its derivative strictly negative. All such crossings would be downward, so there can be only one. The positive value at 3.83 and negative value at 3.84 identify that first zero. This proves

x∈(5.76,5.8081), y∈(14.6689,14.7456), Δ∈(8.8608,8.9856).

These rational brackets imply Δ>3π²/4 and Δ<3π²/2, hence 0<θ<1/2 and 4Δ<6π². For the ellipse, let Δ_−=8.8608, Δ_+=8.9856, x_+=5.8081, y_+=14.7456, p_−=157/50, p_+=22/7 and θ_+=1−3p_−²/(4Δ_+). Then, for u≤1/4,

P(u) > Δ_−−3p_+²/4 − 3p_+²x_+/(16Δ_−) − θ_+y_+/16
=273124119/3618160000>0.

The strict inequalities follow from strict brackets; the displayed rational lower number is also positive. The finite r-grid in the script is an algebraic sanity control only. The continuum rectangle proof is §3. Running `python3 verify_exact.py` prints the exact receipt with 2,031 assertions.

## 7. A limit warning proved using a primary asymptotic theorem

Local convergence to a strip does **not**, by itself, force asymptotic saturation of the diameter-normalized inequality. Here is a concrete convex family, distinct from a counterexample to the conjectured bound:

K_L = {(X,Y): −L<X<L, 0<Y<2−(X/L)²}, L→∞.

It is convex (intersection of a vertical strip, a half-plane and a concave function's hypograph), has area (10/3)L, diameter d_L with d_L/(2L)→1, and converges locally to the strip 0<Y<2.

Let Ω_ε={(x,y): −1<x<1, 0<y<ε(2−x²)}. Then K_L=LΩ_{1/L}. Friedlander–Solomyak Theorem 1.1 applies to h(x)=2−x²: h is positive on [−1,1], has a unique global maximum M=2 at 0, and has exponent m=2 with c_+=c_−=1. Its effective operator is −d²/dx²+(π²/4)x². The first two effective eigenvalues are π/2 and 3π/2. Consequently

λ_j(Ω_ε)=π²/(4ε²)+μ_j/ε+o(ε⁻¹),
γ(K_L)=π/L+o(L⁻¹).

Thus d_L²γ(K_L)~4πL→∞, whereas q_L→0 and F(q_L)→3π². In particular γ(K_L)/B(A_L,d_L)→∞. This rules out interpreting the informal strip clause as “every locally strip-convergent sequence saturates.” It leaves the intended existence of sharp strip-like sequences fully intact.

Also, absolute asymptotic equality is too weak a convention: dilating any fixed bounded domain multiplies both sides and their difference by L⁻². A useful equality/limit classification must specify relative or diameter-normalized saturation.

## 8. Numerical challenge and exact remaining gaps

numerical_challenge.py assembles standard P1 finite-element stiffness and consistent mass matrices on explicitly constructed radial triangulations. It probes 13 convex polygon families/parameters at two resolutions, including inscribed ellipses, rectangles, stadiums and convex support-function perturbations h=1+εcos(kθ). Boundary values are zero. Matrices, eigenpairs and algebraic residuals are replayable. The generated polygon's area and diameter, not an unverified smooth-domain substitution, enter F.

Every tested Ritz-gap margin is positive, but this is **not a certified lower bound**: both Ritz eigenvalues are upper bounds individually, and subtracting them need not bound the true gap. Small algebraic residuals only certify the discretized eigenproblem. The elongated stadium is conspicuously underresolved in this radial mesh; refine_stadium.py records the large mesh dependence rather than hiding it. Curved domains and their inscribed polygons also differ. These tests neither prove the conjecture nor exclude an untested counterexample.

The full inequality for arbitrary convex planar domains, the exclusion of all non-disk equality cases, and an exact description of all normalized extremizing sequences remain open in this attempt. No proof of full resolution, independent audit, exhaustive numerical certification or historical novelty is claimed.

## References

- P. Freitas, contribution in *Low Eigenvalues of Laplace and Schrödinger Operators*, Oberwolfach Reports 6 (2009), 355–428, p.395, Conjecture 2. https://doi.org/10.4171/OWR/2009/06
- P. Antunes and P. Freitas, *A numerical study of the spectral gap*, J. Phys. A 41 (2008), 055201. https://doi.org/10.1088/1751-8113/41/5/055201 (bibliographic origin; not relied upon as a proved general inequality).
- B. Andrews and J. Clutterbuck, *Proof of the fundamental gap conjecture*, J. Amer. Math. Soc. 24 (2011), 899–916. https://arxiv.org/abs/1006.1686
- V. Amato, D. Bucur and I. Fragalà, *The geometric size of the fundamental gap*, arXiv:2407.01341v2. https://arxiv.org/abs/2407.01341v2
- Z. Lu and J. Rowlett, *The fundamental gap of simplices*, Comm. Math. Phys. 319 (2013), 111–145, Theorem 3. https://arxiv.org/abs/1109.4117
- L. Friedlander and M. Solomyak, *On the spectrum of the Dirichlet Laplacian in a narrow strip*, Israel J. Math. 170 (2009), 337–354, Theorem 1.1. https://arxiv.org/abs/0705.4058
