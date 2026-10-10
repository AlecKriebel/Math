# Mathematical audit addendum: gradient distance, problem 30005995

The unrestricted conjecture remains **UNSOLVED; five approaches completed**. This addendum makes explicit the compactness and representative arguments underlying the frozen report's conditional Theorem F. It does not add the missing hypothesis to the original conjecture, and it does not assert novelty.

Throughout, G: R² → R² is continuous and strictly monotone, u is a locally Lipschitz scalar weak solution of div G(Du)=0 on an open planar domain, and B=D(G)∩S(G) is exactly the closed bad set defined in the frozen report. When discussing a real-valued distance, assume B is nonempty. The case B=R² is immediate. If B is empty, ordinary distance is extended-valued +∞; this is separate from real-valued continuity.

## 1. Strong compactness with nonlinear flux identification

Here is a direct justification of the frozen report's phrase “strict-monotonicity compactness preserves the equation.” Weak-* convergence of gradients alone would not justify substituting the limit into G.

**Lemma.** On a fixed open domain U in Rⁿ, let u_j be solutions of the same autonomous equation div G(Du_j)=0. Suppose u_j→v locally uniformly and that |Du_j|≤L locally, with one L on each relatively compact subdomain. Then Du_j→Dv strongly in Lᵖ_loc for every finite p≥1, G(Du_j)→G(Dv) strongly in Lᵖ_loc for every finite p, and v solves the same equation.

**Proof.** Fix compact K⊂U and a nonnegative smooth cutoff φ compactly supported in U, with φ=1 on K. Work in a relatively compact neighborhood containing supp φ on which all gradients have the bound L. Set M=max_{|a|≤L}|G(a)|. Subtract the equations for u_j and u_k and test with φ(u_j−u_k). This compactly supported Lipschitz test is legitimate by density, since the fluxes are bounded. We obtain

I_jk := ∫ φ [G(Du_j)−G(Du_k)]·(Du_j−Du_k)
       = −∫ (u_j−u_k)[G(Du_j)−G(Du_k)]·Dφ,

and hence

0≤I_jk≤2M ||Dφ||_{L¹} ||u_j−u_k||_{L∞(supp φ)}→0.

For each a>0 for which the following set is nonempty, continuity and strict monotonicity give

m_a := min{[G(p)−G(q)]·(p−q): |p|,|q|≤L, |p−q|≥a}>0.

The minimum is over a compact set separated from the diagonal. Thus

|{x∈K: |Du_j−Du_k|≥a}| ≤ I_jk/m_a→0.

If the defining set for m_a is empty, the gradient superlevel set is empty and no estimate is needed. The gradients are Cauchy in measure on K. For every finite p≥1,

∫_K |Du_j−Du_k|ᵖ ≤ aᵖ|K|+(2L)ᵖ I_jk/m_a.

First let j,k→∞, then a→0. The resulting strong Lᵖ limit is Dv, by distributional differentiation of the locally uniform limit. Uniform continuity and boundedness of G on the closed L-ball give strong local convergence of the fluxes, and the weak equation passes to the limit. An exhaustion proves the local statement. ∎

For blow-ups on expanding domains, apply this lemma on each fixed ball after discarding finitely many terms. Arzelà–Ascoli and a diagonal extraction provide locally uniform entire limits. Strict monotonicity here supplies a positive modulus only at a fixed separation a on a fixed compact set; no uniform ellipticity is being assumed.

## 2. Precise imported input and its scaling

The imported flatness estimate is [LT, (1.7)]. Its relevant content is: for a fixed G, Lipschitz bound L, slope p with |p|≤L, and accuracy η>0, a sufficiently small δ>0 works for **every** solution w with that bound:

||w−p·x||_{L∞(B₁)}≤δ ⇒ ||Dw−p||_{L∞(B_δ)}≤η.

L∞ is essential supremum. The report applies this quantitative statement, not merely continuity of the gradient for one fixed limiting solution. After subtracting w(z) and rescaling B_ρ(z), it gives

sup_{B_ρ(z)}|w(ξ)−w(z)−p·(ξ−z)|≤δρ
⇒ ess sup_{B_{δρ}(z)}|Dw−p|≤η.

Shrinking δ, if needed, shrinks both the admissible error and the output ball, preserving the implication. The slope and accuracy are fixed before δ; δ is independent of the approximating index j. No condition p∉B is needed.

The localization input is [L, Corollary 1.2]. At a point without a unique linear blow-up, every blow-up has gradient in B almost everywhere. The original conjecture is not a conclusion of either imported result.

## 3. Differentiability and affine blow-ups

**Differentiable-point consequence.** If w is differentiable at z with slope p, its first-order error is o(ρ). For each η, choose δ from the flatness estimate, then ρ so that this error is at most δρ. Therefore

lim_{r↓0} ess sup_{B_r(z)} |Dw−p|=0.

In particular, z is a Lebesgue point for the weak gradient with value p. This also implies that a differentiability-point slope belongs to every closed set containing Dw almost everywhere in a neighborhood of that point.

**Affine-blow-up consequence.** If a blow-up of u at x₀ is p·x, fix η and its δ. Local uniform convergence makes one sufficiently far term δ-close to p·x on B₁. Rescaling the flatness estimate back gives |Du−p|≤η almost everywhere on some ball about x₀. Since this is true for every η, u is differentiable at x₀ with derivative p: on a ball with that gradient bound, the continuous function u−p·x is η-Lipschitz. Thus an affine blow-up at a nondifferentiability point is impossible.

This reasoning needs neither uniqueness of the selected affine blow-up nor a pre-existing small-gradient-oscillation regularity threshold.

## 4. Conditional theorem, with all quantifiers retained

**Theorem.** Fix a nondifferentiability point x₀ of u. Assume that every locally uniform blow-up limit of u at x₀ is differentiable at every nonzero point of R². Then

lim_{r↓0} ess sup_{B_r(x₀)} dist(Du,B)=0.

**Proof.** By the localization input and Section 3, every blow-up v at x₀ has Dv∈B almost everywhere. Suppose the conclusion fails. Then for some ε>0 there are points y_j→x₀, y_j≠x₀, at which u is differentiable, Du has its Lebesgue value, and dist(Du(y_j),B)≥ε. Indeed, failure supplies positive-measure gradient-distance superlevel sets, and Rademacher's and Lebesgue differentiation theorems permit these choices.

Take t_j=2|y_j−x₀| and u_j(ξ)=[u(x₀+t_jξ)−u(x₀)]/t_j. Pass to a subsequence with u_j→v locally uniformly and z_j=(y_j−x₀)/t_j→z, where |z|=1/2. The compactness lemma makes v a solution. The hypothesis applies to this particular subsequential limit; one unspecified good blow-up would not suffice.

Let p=Dv(z), which exists since z≠0. Section 3 and Dv∈B almost everywhere imply p∈B, using closedness of B. Fix 0<η<ε, and obtain δ for G,L,p,η. Choose a fixed ρ>0 so that

sup_{B_ρ(z)} |v(ξ)−v(z)−p·(ξ−z)|<δρ/3.

Uniform convergence on the closure of this ball, including convergence at z, makes

sup_{B_ρ(z)} |u_j(ξ)−u_j(z)−p·(ξ−z)|<δρ

for all sufficiently large j. Flatness then gives |Du_j−p|≤η almost everywhere on B_{δρ}(z). Eventually z_j lies strictly inside this fixed ball. It is a Lebesgue point of Du_j, so the same bound holds at its Lebesgue value. Consequently

dist(Du(y_j),B)≤|Du_j(z_j)−p|≤η<ε,

a contradiction. ∎

The order is important: choose the witness subsequence and its limiting nonzero point, then fix p,η,δ,ρ, and only then take j large. An H¹-null exceptional set for each blow-up does not guarantee regularity at this selected limiting point.

## 5. A genuine continuous representative under the global hypothesis

Assume Section 4's extra hypothesis at every nondifferentiability point. Define

d_*(x)=dist(Du(x),B) when u is differentiable at x,
d_*(x)=0 otherwise.

This is a representative of the original almost-everywhere distance. At a singular x₀, Section 4 bounds d almost everywhere in a neighborhood by any prescribed ε. Every differentiability point strictly inside that neighborhood has a Lebesgue gradient value, by Section 3, so its distance also obeys the bound. Other singular points have assigned value zero. Thus d_* is genuinely continuous at x₀, not just essentially small there.

At a differentiability point x with derivative p∈B, Section 3 bounds nearby differentiability-point distances by |Du−p|; singular-point values are zero. Hence d_* is continuous there too.

Finally suppose dist(p,B)=c>0. The flatness consequence supplies a neighborhood with d≥c/2 almost everywhere. It cannot contain a singular point y: Section 4 at y would force the essential distance to tend to zero in balls contained in that neighborhood. Thus all nearby points are differentiability points. Their gradients tend to p by Section 3, and distance, being 1-Lipschitz in gradient space, is continuous at x.

This proves the frozen report's global conditional consequence directly, without needing an additional appeal to [L, Remark 5.3]. Arbitrary values assigned on a null set are not being declared continuous; the representative is the explicitly defined d_*.

## 6. Additional scope checks

- In the finite-bad-set literature statement, the directly cited [LL, Theorem 1.3] uses B∩closed B_L finite for a ball containing all gradient values. The expression “bounded gradient range” should be read with that bound, not as an unproved stronger essential-range variant.
- For G(p,q)=(p+q,q³−p), DG=[[1,1],[-1,3q²]], with determinant 1+3q². Its inverse has symmetric part diag(3q²,1)/(1+3q²). Both degeneracy sets equal {q=0}. Smoothness and bounded derivatives on compact neighborhoods exclude additional points introduced by the closure definitions.
- The skew contribution is constant and disappears from the divergence equation, but remains relevant to the bad-set definitions. This example tests those definitions; it does not produce a singular PDE solution.
- At q=0, vertical increments give Q₋=t² and Q₊=t²/(1+t⁴). These direct quotients confirm the denominator and the zero limiting ellipticity independently of the inverse computation.
- The two-gradient interface contradiction uses both tangential compatibility and normal flux balance. A nonzero jump would violate strict monotonicity. The ridge argument uses strict scalar monotonicity, and equal-trace uniqueness follows from testing the difference. None excludes all singular solutions.
- The spike supports have squared-radius tail 2^(−6m)/252; when 2^(−m)≤2r, this gives the claimed relative area bound (16/63)r⁴. The total Dirichlet energy is 2π. The positive-area plateaus ensure essential supremum one at every scale. It is a Sobolev function, not a solution of the PDE and not a counterexample to the conjecture.
- The whole issue remains the extra all-blow-ups, all-off-center-points assumption, or another PDE-specific no-spike estimate. Approximate continuity, H¹-nullness, and finite W¹,² energy do not supply it.

## References

[L] Thibault Lacombe, *Average gradient localisation for degenerate elliptic equations in the plane*, arXiv:2601.03078v1. https://arxiv.org/abs/2601.03078v1

[LT] Xavier Lamy and Riccardo Tione, *Hyperbolic regularization effects for degenerate elliptic equations*, arXiv:2601.04753v2, 31 March 2026. https://arxiv.org/abs/2601.04753v2

[LL] Thibault Lacombe and Xavier Lamy, *On C¹ regularity for degenerate elliptic equations in the plane*, arXiv:2407.00775v1. https://arxiv.org/abs/2407.00775v1

The cited statements were checked in the primary documents. Their full proofs are imported, not formally verified by this audit or by the finite checks.
