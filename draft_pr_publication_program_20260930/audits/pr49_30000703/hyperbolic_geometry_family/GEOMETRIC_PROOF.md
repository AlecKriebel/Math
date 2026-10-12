# Universal proof and exact scope

The theorem below is a new audit derivation applying a credited theorem, not a new mathematical result or proof-search attempt. Its forward reflection step imports the precisely authenticated arc theorem; that import is identified instead of concealed as a computational inference.

**Claim.** For every holomorphic f:D→D, the ordinary unrestricted limit

    Φ_f(z)=(1−|z|²)|f′(z)|/(1−|f(z)|²) → 1 as z→1

holds if and only if f has a holomorphic extension across some open unit-circle arc containing 1, carrying that arc into the unit circle. The same conclusion follows from a strictly positive unrestricted liminf at 1. The extension has η=f(1)∈∂D and α=conj(η)f′(1)>0. No global injectivity, finite-Blaschke conclusion, or derivative normalization α=1 follows.

## The imported analytic result and the forward application

Roth's original [OWR9/2007 contribution](https://ems.press/content/serial-article-files/46093), printed pp.528–530, Theorem1, gives the equivalence for an open arc Γ of positive unrestricted liminf of Φ_f at every fixed ξ∈Γ and holomorphic extension across Γ carrying Γ into ∂D. The attribution is Kraus–Roth–Ruscheweyh, [J. Analyse Math.101(2007),219–256](https://link.springer.com/article/10.1007/s11854-007-0009-x). The later [Gumenyuk–Kourou–Moucha–Roth v1](https://arxiv.org/pdf/2410.13965v1), §8.2, p.31, eq.(8.3), explicitly states the exact one-point equivalence and credits the same reference57, listed on p.40. The complete 2007 journal proof is not independently audited here.

Choose c>0 and 0<δ<1 with Φ_f(z)>c whenever z∈D and |z−1|<δ. Such choices follow from either stated one-point hypothesis. For Γ={ξ∈∂D:|ξ−1|<δ/2}, fix any ξ∈Γ and put ε=δ−|ξ−1|>0. If |z−ξ|<ε, triangle inequality gives |z−1|<δ, so the unrestricted liminf at ξ is at least c. Every point of Γ therefore satisfies the imported theorem's hypothesis. This proves the extension conclusion. It transfers a lower bound, not a uniform limit over Γ. A radial segment, Stolz angle or arbitrary single sequence gives no such full neighborhood at neighboring ξ.

The pullback metric is λ_f=|f′|/(1−|f|²), with λ_D=1/(1−|z|²). Thus Φ_f=λ_f/λ_D and λ_f≥cλ_D in the collar. Because the ratio is positive, f′ has no zeros there, and λ_f is a metric of curvature −4. The 2024 source uses twice this density, curvature −1; both source and target densities scale equally, so its distortion is exactly the same Φ_f.

One can verify local completeness of this pullback metric without an invalid comparison of global image distances. Fix ξ∈Γ and a small r>0 with B(ξ,r)⊂B(1,δ) and 0∉B(ξ,r). For z∈D near ξ and any path from0 toz, its final crossing of the circle |w−ξ|=r yields a final segment contained in B(ξ,r). The λ_f-length of that segment is at least c times its λ_D-length. In the −4 normalization,

    sinh d_D(w,z)=|w−z|/sqrt((1−|w|²)(1−|z|²)).

For |z−ξ|<r/2 and such w, |w−z|≥r/2 and 1−|w|²≤1, so its length is at least

    c arsinh(r/(2 sqrt(1−|z|²))) → ∞.

Taking the infimum over all paths preserves that bound. Thus the pullback metric is locally complete along Γ even if it degenerates at critical points elsewhere. This is a statement about intrinsic pullback distance, not a lower bound on the target distance d_D(f(0),f(z)); target paths need not lift and images of paths need not be shortest paths. Completeness explains the geometric mechanism behind the imported reflection theorem but does not independently prove that theorem.

## Noncriticality and orientation without assuming Hopf's lemma

Here is an elementary local alternative to the submitted Hopf argument. After extension, choose a zero-free neighborhood and let η=f(1). Straighten the source circle with w=(1−z)/(1+z), so z=(1−w)/(1+w), and define

    g(w)=−log(conj(η) f((1−w)/(1+w)))

using the holomorphic logarithm whose value at0 is0. Then Re g>0 on the nearby right half-plane and Re g=0 on the imaginary axis. The germ is not constant. Suppose its first nonzero term is c_n w^n. If n≥2, as θ ranges over (−π/2,π/2), Re(c_n e^(inθ)) takes a strictly negative value. On that fixed ray and small positive radius, the leading term would make Re g negative, a contradiction. Hence n=1. The imaginary-axis identity implies c_1 is real, and positivity on the positive real ray implies c_1>0. Differentiation gives g′(0)=2 conj(η)f′(1), so α=conj(η)f′(1)>0. This proves nonvanishing, positive orientation, local inverse and the Taylor expansion. It also independently confirms that the signs and smoothness requirements of the submitted Hopf argument produce the same result.

The same argument at every ξ∈Γ gives α_ξ=conj(f(ξ)) ξ f′(ξ)>0 and |f′(ξ)|=α_ξ. Zeros cannot approach1 under the extension because f(1) is unimodular; shrinking the neighborhood avoids them. Critical points elsewhere, such as0 for z², are allowed.

## Tangential-safe converse and reflection

Suppose conversely that the stated extension F and circle mapping hold. The preceding argument gives the same noncriticality and orientation; it uses only F(D∩U)⊂D. Write z=ρe^(it) near1 and N(ρ,t)=1−|F(ρe^(it))|². Since N(1,t)=0,

    Q(ρ,t)=N(ρ,t)/(1−ρ²)
          =−(1/(1+ρ)) ∫_0^1 ∂_ρN(1+s(ρ−1),t) ds

extends continuously and real analytically toρ=1. Its boundary value is α_(e^it)>0. Consequently Φ_f=|f′|/Q→1 for every interior approach to1. This is genuine unrestricted convergence. Dividing an arbitrary O(|z−1|²) Taylor remainder by1−|z|² would not establish it; e.g. z(t)=(1−t^m)e^(it), m>2, has |z−1|²/(1−|z|²) asymptotic to t^(2−m)/2, which diverges.

In a sufficiently small neighborhood, the exterior reflection is 1/conj(f(1/conj z)). The inverse/conjugate expression is holomorphic there and its denominator is nonzero. It agrees with F on the circle arc, so the identity theorem gives the same continuation. This local formula makes no assertion over zeros or singularities outside that neighborhood.

## Sharpness and excluded boundary cases

Constants intoD have Φ=0. Constants on∂D are excluded by the codomainD, so no denominator0 case exists inside the stated class. Schwarz–Pick permits Φ≤1; boundary limiting equality does not invoke the interior equality case that would force an automorphism.

The map z² has Φ=2|z|/(1+|z|²) and meets the exact limit at1 but is globally two-to-one. For |η|=1 and a>0,

    f_a(z)=η exp(−a(1−z)/(1+z)),
    u=Re((1−z)/(1+z))=(1−|z|²)/|1+z|²,
    Φ_fa=a u/sinh(a u),    f_a′(1)=aη/2.

Thus u>0 insideD and u→0 unrestrictedly at1, proving the exact hypothesis. Every positive derivative coefficient occurs. The exponent has a nonremovable pole at−1 and its exponential has an essential singularity there, so this family rules out a global finite-Blaschke or whole-circle continuation conclusion. Neither example challenges the local criterion.

The only non-elementary forward step is the imported arc reflection theorem. Primary sources authenticate its exact hypotheses and its known credit; this report does not claim a fresh full-journal-proof certificate, an exhaustive priority search, an answer for weaker approach hypotheses, or an answer to the neighboring Problem2.
