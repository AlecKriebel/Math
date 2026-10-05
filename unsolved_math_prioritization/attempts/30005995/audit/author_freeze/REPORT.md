# Gradient distance for planar monotone equations

Problem 30005995 · OWR-14298587-010 · rank 803

**Verdict: NO RESOLUTION, five approaches completed.** This report proves restricted statements and identifies a precise remaining step. It does not prove or disprove the full conjecture, claim novelty, or certify a manuscript for publication.

## 1. Exact scope and identity

Let Ω be open in R², G:R²→R² continuous, and

⟨G(p)−G(q),p−q⟩ > 0 whenever p≠q.

Let u∈W¹,∞_loc(Ω) satisfy ∫ G(Du)·Dφ=0 for every φ∈C∞_c(Ω). All conclusions here are interior and local; the report's unit-ball, Lipschitz formulation follows by restriction and scaling. No analogous claim for arbitrary W¹,p solutions or higher dimensions is made.

For nonzero h define

Q₋(p,h)=⟨G(p+h)−G(p),h⟩/|h|²,
Q₊(p,h)=⟨G(p+h)−G(p),h⟩/|G(p+h)−G(p)|².

Put

D=⋂_{λ>0} closure{p: liminf_{h→0} Q₋(p,h)≤λ},
S=⋂_{λ>0} closure{p: liminf_{h→0} Q₊(p,h)≤λ},
B=D∩S.

These closed-set definitions, including the closures and the reciprocal-field denominator, are essential. They come from [LL, (3)] and agree with [LT, (9.1)]. Replacing S by the set where the symmetric derivative of G is unbounded changes the problem. No derivative of G is assumed to exist.

The question is whether d(x)=dist(Du(x),B), initially defined almost everywhere, has a continuous representative. It is not a demand that every assignment on the exceptional null set be continuous. If B is nonempty, d is locally bounded because Du is. If B=R², d=0. If B=∅, the usual distance is +∞, not a real-valued function; the regularity theorem in [LL] yields u∈C¹, and the distance assertion can either use the extended constant +∞ or be stated only for nonempty B.

The source is Xavier Lamy's contribution, joint with Thibault Lacombe, in OWR 37/2024, printed pp. 2138–2139 [OWR]. The workshop occurred in August 2024; EMS lists publication on 14 February 2025. The descriptor's statement SHA-256 exactly equals the independently recomputed UTF-8 hash of the supplied problem's statement. This identifies the record; it is not mathematical evidence of a solution. The live problem page returned HTTP 403 after the web reader failed. The official report PDF was obtained and the relevant pages inspected. The separate research-results dataset contains no matching target record. Full byte counts and hashes are in EVIDENCE.json.

## 2. Current literature and prior-attempt check

[LL] proves C¹ regularity when B meets the bounded gradient range in finitely many points (Theorem 1.3). Its Remark 2.7 also gives distance continuity under a connected-complement condition for small neighborhoods of B. It exhibits a non-C¹ solution for a general monotone field, but that example has Du∈B almost everywhere and hence d=0. It is not a counterexample to this question. The publisher currently lists the paper among forthcoming Analysis & PDE articles.

[L] (January 2026), Theorem 1.1, proves approximate continuity of the distance without structural restrictions. At a point where ordinary continuity is unavailable, the averages of d over shrinking balls tend to zero. Corollary 1.2 localizes gradients of nonaffine blow-up limits in B. Section 6 explicitly distinguishes this from having a continuous representative everywhere.

[LT] v2 (March 2026), Theorem 1.1, shows H¹(Sᵤ)=0 for the nondifferentiability set and controls gradient oscillation at differentiability points. Its flatness estimate (1.7) is available at every slope. Theorems 1.2/9.1 and Proposition 9.6 give stronger conclusions under curve-structure assumptions; the general statement does not eliminate all singular points of all blow-ups away from their centers. A small-oscillation regularity threshold cannot be assumed for arbitrary G (Remark 9.5).

These are stronger partial results than the supplied dated triage records. Neither inspected 2026 primary paper establishes the unrestricted distance-continuity conclusion. Bounded current searches found no later primary resolution. This is a search finding, not a proof that no such result exists.

Repository code, PR, and branch searches for the problem ID, OWR identifier, title terms, and author name found no exact prior proof or attempt. The public root listing also had no exact-target directory. A recursive tree request failed twice with a transport error, so the repository check is not exhaustive. Catalog/queue appearances are not prior mathematical attempts. No skip was triggered.

## 3. Approach one: literature reduction

The exact general question remains after applying the cited theorems. The useful reductions are approximate continuity and localization of singular blow-ups. Finite B and the connected-complement case are already covered by [LL]; they are not new resolutions. The stronger gradient-continuity question is different and is false for general nonpotential G.

For clarity about the potential restriction: if G=DF for F∈C¹ strictly convex, a Lipschitz weak solution minimizes ∫F(Du) among Lipschitz competitors with the same trace on a bounded Lipschitz subdomain. Indeed,

F(Dv)≥F(Du)+DF(Du)·(Dv−Du),

and the integral of the last term vanishes by the weak equation and density of smooth test functions. Conversely, first variation at such a minimizer gives the weak equation; continuity of DF on the compact gradient range justifies differentiation under the integral. General strictly monotone G need not be a gradient. The unrestricted potential case cannot simply be substituted for the stated problem.

## 4. Approach two: exact ellipticity and skew audit

### Proposition A

The polynomial field G(p,q)=(p+q,q³−p) is continuous and strictly monotone, but B={q=0}; its symmetric derivative is locally bounded everywhere. Moreover, its Minty transform is strictly contracting between distinct points but need not have a Lipschitz constant k<1 on any neighborhood of the origin.

**Proof.** For two points (p,q),(r,s), the monotonicity pairing is

(p−r)²+(q−s)²(q²+qs+s²)>0

unless both differences vanish. The symmetric derivative is diag(1,3q²), so D={q=0}. The derivative matrix A=[[1,1],[-1,3q²]] is invertible everywhere. Its inverse has symmetric part diag(3q²,1)/(1+3q²). The local inverse-function formula for Q₊ therefore gives S={q=0}; equivalently Q₊ at q=0 tends to zero in the vertical direction, while away from that line compact local bounds give a positive lower bound. Smoothness gives the upper-degeneracy set defined from unbounded symmetric derivatives as empty.

For the Cayley/Minty transform T=I+G and H=(I−G)∘T⁻¹ on T(R²), strict monotonicity implies |H(Tx)−H(Ty)|<|Tx−Ty|. With x=(0,t), y=(0,0), the square of this ratio is

(2−2t²+t⁴)/(2+2t²+t⁴)→1 as t→0.

Thus strict pointwise contraction cannot provide a uniform k<1, even on a compact neighborhood. A quasiregular estimate requiring a fixed finite distortion constant cannot be invoked from strict monotonicity alone. This is an obstruction to that argument, not a counterexample to the distance conjecture. ∎

## 5. Approach three: jumps, ridges, and localized gluing

### Proposition B: a two-gradient interface is impossible

Suppose a continuous piecewise-affine u has gradients p and q on opposite sides of a straight interface with unit normal n. Continuity forces p−q=an. Weak flux balance forces (G(p)−G(q))·n=0. Their product gives

(G(p)−G(q))·(p−q)=0.

Strict monotonicity forces p=q. Thus a genuine two-state jump cannot solve the equation. In particular, the simple max/min of two different affine functions cannot be a counterexample.

### Proposition C: every one-dimensional ridge solution is affine

On a rotated rectangle, let u(x)=a·x+f(n·x), with |n|=1 and f Lipschitz. Testing by products of functions in the longitudinal and transverse variables gives

(d/dt)[G(a+f′(t)n)·n]=0

in distributions. The bracket is constant almost everywhere. The scalar map s↦G(a+sn)·n is strictly increasing, since its difference multiplied by s−t is the strict-monotonicity pairing. Hence f′ is a single constant almost everywhere, proving the claim.

### Proposition D: equal-trace uniqueness

On a bounded connected Lipschitz domain, two Lipschitz weak solutions with the same trace agree. Their difference belongs to W¹,²₀ and is an admissible test by density, because both fluxes are bounded. Subtracting the equations gives

∫(G(Du)−G(Dv))·(Du−Dv)=0.

The integrand is nonnegative and vanishes only when Du=Dv. Equal trace then fixes the additive constant. In particular, a compactly supported nonlinear bubble cannot be inserted into an affine solution while retaining the same autonomous field and weak equation. ∎

These exclusions cover only the stated constructions. They do not exclude more complicated, non-piecewise-affine singular solutions.

## 6. Approach four: the average-to-uniform gap is genuine

### Proposition E: a Sobolev spike model

There is f∈W¹,²(B₁), 0≤f≤1, continuous off the origin and approximately continuous with approximate value zero at the origin, whose essential supremum is one on every ball centered there. Its discontinuity set is the singleton {0}, hence H¹-null. It has no continuous representative.

**Construction and proof.** For n≥1, let

cₙ=(2⁻ⁿ,0), Rₙ=2⁻³ⁿ⁻⁴, aₙ=Rₙ exp(−2ⁿ).

The closed support discs of radii Rₙ are disjoint and contained in B₁. Define a cap fₙ, with ρ=|x−cₙ|, by

fₙ=1 for ρ≤aₙ;
fₙ=log(Rₙ/ρ)/2ⁿ for aₙ<ρ<Rₙ;
fₙ=0 for ρ≥Rₙ.

Set f=Σfₙ and f(0)=0. The supports are locally finite away from zero, so f is continuous there. Each cap has Dirichlet energy 2π/2ⁿ. Their disjointness gives total energy 2π and a finite L² norm. The partial sums converge strongly in W¹,², proving the Sobolev assertion.

If a support disc meets B_r(0), then its center satisfies |cₙ|<2r, because Rₙ≤|cₙ|/64. Choose the first m with 2⁻ᵐ≤2r. For small r,

|{f≠0}∩B_r|/|B_r| ≤ (Σ_{n≥m}Rₙ²)/r²
=2⁻⁶ᵐ/(252r²) ≤ (16/63)r⁴→0.

Consequently the averages of f tend to zero. Nevertheless each sufficiently small B_r contains an inner disc of positive area where f=1. On the negative horizontal half-plane f=0. Any continuous representative would agree with f on B₁\{0}, because two continuous functions equal almost everywhere on an open set are equal everywhere. The sequences cₙ and −cₙ then contradict continuity at zero. ∎

This is not a PDE solution or a counterexample to the conjecture. It rigorously invalidates the generic inference from approximate continuity, finite W¹,² energy, and an H¹-null exceptional set to ordinary continuity. Any proof must use additional structure of the equation.

## 7. Approach five: a proved blow-up criterion

The following deduction uses the precise localization theorem of [L] and the flatness stability estimate (1.7) of [LT] as imported results. Those results are not reproved or independently formally verified here.

### Theorem F: off-center differentiability of blow-ups suffices

Assume the original planar hypotheses, B≠∅, and x₀∈Ω is a nondifferentiability point of u. Suppose **every locally uniform blow-up limit**

v(z)=lim_j [u(x₀+rⱼz)−u(x₀)]/rⱼ, rⱼ↓0,

is differentiable at every z≠0. Then

lim_{r↓0} ess sup_{B_r(x₀)} dist(Du,B)=0.

Thus setting the distance to zero at x₀ gives continuity there in the essential, representative-independent sense.

**Proof.** All blow-ups have the same local Lipschitz bound. Strict-monotonicity compactness preserves the equation; [L] gives Dv∈B almost everywhere unless v is affine. An affine blow-up at x₀ is impossible: local uniform convergence to that affine map, followed by the flatness estimate of [LT] at arbitrary accuracy, makes the essential oscillation of Du at x₀ vanish and forces u to be differentiable there. Consequently Dv∈B almost everywhere for every blow-up at this singular point.

Suppose the conclusion fails. We can select differentiability and Lebesgue points yⱼ→x₀, yⱼ≠x₀, with dist(Du(yⱼ),B)≥ε for some fixed ε>0. This follows by taking points from positive-measure superlevel sets. Put tⱼ=2|yⱼ−x₀|. Pass to a subsequence such that uⱼ(z)=[u(x₀+tⱼz)−u(x₀)]/tⱼ converges locally uniformly to v and zⱼ=(yⱼ−x₀)/tⱼ→z with |z|=1/2.

By hypothesis v is differentiable at z; let p=Dv(z). The flatness estimate of [LT] implies that Dv has essential limit p at z. Since Dv∈B almost everywhere and B is closed, p∈B.

Fix η>0. Flatness stability supplies δ>0 for G, the local Lipschitz bound, p, and accuracy η. Differentiability of v at z gives a radius ρ>0, with B_ρ(z) in the blow-up domain, such that

sup_{B_ρ(z)} |v(ξ)−v(z)−p·(ξ−z)| < δρ/3.

For all large j, local uniform convergence implies

sup_{B_ρ(z)} |uⱼ(ξ)−uⱼ(z)−p·(ξ−z)| < δρ.

Apply [LT, (1.7)] after translation and scaling. It yields |Duⱼ−p|≤η almost everywhere on B_{δρ}(z), after decreasing δ if necessary. For large j, zⱼ belongs to this ball and is a Lebesgue point of Duⱼ, so |Du(yⱼ)−p|≤η. Taking η<ε contradicts p∈B. ∎

**Global conditional consequence.** If the extra blow-up hypothesis holds at every nondifferentiability point, the original distance has a continuous representative: at those points use the theorem and value zero; at differentiability points use the gradient flatness estimate. If the limiting distance at a differentiability point is positive, the nondegenerate local regularity result in [L, Theorem 5.1 and Remark 5.3] gives a C¹ neighborhood, so no conflicting zero assignments at singular points approach it.

[LT, Proposition 9.6] supplies the required off-center regularity in its stated compact differential-inclusion/curve-component setting. No assertion is made that arbitrary closed B has that structure. In particular, merely knowing that blow-up gradients lie in B is not the additional hypothesis of Theorem F.

## 8. Exact remaining gap

For arbitrary G and arbitrary B, the inspected theorems give small **averages** of d at unresolved singular points; a full proof still needs

∀ε>0 ∃r>0: dist(Du,B)<ε almost everywhere on B_r(x₀).

One sufficient missing estimate is a no-spike implication: at each such point and fixed ε, if ess sup_{B_r}d≥ε, then the proportion of B_{2r} on which d≥ε/2 is bounded below independently of r. The average limit would contradict that estimate. We do not prove it. Alternatively, Theorem F would finish the problem under its extra blow-up regularity assumption, which is likewise not established in full generality.

No quantitative ellipticity, universal finite quasiregular distortion, topological connectedness of bad-set complements, or convex potential has been smuggled into the original hypotheses. The five approaches end here with restricted proofs and this explicit unresolved step.

## References

- [OWR] Xavier Lamy (joint with Thibault Lacombe), contribution in *Calculus of Variations*, Oberwolfach Reports 37/2024, pp. 2138–2139. https://ems.press/journals/owr/articles/14298587 ; official report PDF https://ems.press/content/serial-article-files/50045 .
- [LL] Thibault Lacombe and Xavier Lamy, *On C¹ regularity for degenerate elliptic equations in the plane*, arXiv:2407.00775v1. https://arxiv.org/abs/2407.00775 ; publisher forthcoming list https://msp.org/soon/coming.php?jpath=apde .
- [L] Thibault Lacombe, *Average gradient localisation for degenerate elliptic equations in the plane*, arXiv:2601.03078v1. https://arxiv.org/abs/2601.03078 .
- [LT] Xavier Lamy and Riccardo Tione, *Hyperbolic regularization effects for degenerate elliptic equations*, arXiv:2601.04753v2, revised 31 March 2026. https://arxiv.org/abs/2601.04753 .

Checked 5 October 2026. All source PDFs, extracts, raw datasets, and private coordination materials are excluded from this packet.
