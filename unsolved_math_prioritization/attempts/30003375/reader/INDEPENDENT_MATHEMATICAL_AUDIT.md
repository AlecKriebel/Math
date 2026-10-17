# Independent audit: harmonic circle fibrations

13 October 2026. Target: 30003375 / OWR-15208-029, adopted formulation E.

## Verdict

**Accept the frozen proof for E, with no unresolved mathematical blocker.** Every closed connected smooth manifold homeomorphic to S¹ × CP³, in either primitive integral first-cohomology class, admits an unrestricted smooth metric whose harmonic circle representative is a smooth fibration with connected fibres.

This is a credited prior-result consequence. The appropriate qualified disposition is `already_solved` for E, with result classification `prior_result`. This audit does not establish the original author's intended metric quantifier, a new theorem, a historical priority claim, or any arbitrary-metric, prescribed-metric, or curvature-constrained assertion.

The accepted proof is exactly `PROOF.md`, 16,025 bytes, SHA256 `776ef606f87874d2e2c6b83eea5ad98be6995cac863709ca0c316c2cf37db203`. Its general metric proposition expressly requires positive-dimensional fibre. The six-dimensional application satisfies that requirement.

## 1. Imported smooth-topological theorem

Browder–Levine's definitions 1.1–1.3 and Theorem 1.4, printed pp.153–154 of *Fibering manifolds over a circle*, were independently visually inspected. Their fibre maps are smooth submersions and locally trivial smooth bundles. The theorem prescribes a nonzero integral first-cohomology class, assumes a compact smooth manifold of dimension greater than five with infinite cyclic fundamental group and finitely generated homotopy groups, and allows a boundary extension problem. The boundary requirement is vacuous for a closed manifold. There is no missing product-diffeomorphism, trivial-monodromy, or specified-metric assumption. [Primary institutional copy](https://www.maths.ed.ac.uk/~v1ranick/papers/browlev.pdf), [DOI](https://doi.org/10.1007/BF02564368).

The application checks each hypothesis:

- The manifold is smooth and closed of dimension seven.
- Its homeomorphism type gives fundamental group Z and orientability.
- In every degree i ≥ 2, its homotopy group is isomorphic to that of CP³.
- CP³ is a simply connected finite CW complex. Its integral homology is finitely generated in every degree, so the required homotopy groups are finitely generated.
- Either primitive generator of H¹(M;Z) is nonzero.

For the finite-generation implication, Serre's Proposition 1 on printed p.491 of *Homologie singulière des espaces fibrés. Applications* was independently checked in the primary PDF's extracted text. The preceding regularity condition poses no restriction for CP³, a compact smooth manifold and finite polyhedron. This is degreewise finite generation; finiteness of the groups themselves or of their total direct sum is unnecessary. [Primary institutional copy](https://www.college-de-france.fr/media/jean-pierre-serre/UPL7235285843586540944_Serre_The_se.pdf).

The proof correctly uses a theorem about each given smooth M. It never transports a smooth metric through the possibly nonsmooth homeomorphism to the product.

## 2. Fibre connectedness and orientation

The cohomology class u corresponds to a homomorphism π₁(M) → Z. Because π₁(M)=Z and u is primitive, the bundle map induces an isomorphism, with sign determined by the chosen generator.

For a bundle over a circle with connected total space, the action of π₁(S¹) on fibre components is transitive, and the stabilizer of one component is the image of π₁(M). Therefore the number of components is the index of that image. Surjectivity gives one component. The homotopy exact sequence then gives π₁(F)=0, since π₂(S¹)=0 and π₁(M) → π₁(S¹) is injective. The resulting F is a closed connected smooth six-manifold.

Orienting M and the base orients the vertical tangent bundle: place the positive base direction before an oriented vertical frame. This orientation is intrinsic and survives transport around the base. Consequently the monodromy preserves the fibre orientation. This justifies both the equality of volume integrals used in Moser's argument and the global orientation used for the Hodge star. No smooth classification of F is needed.

## 3. Moser sign, composition, and isotopy

The metric argument is checked directly. Write the bundle as the mapping torus with convention (x,1) equivalent to (φ(x),0), and choose a positive volume form μ on F. The difference φ*μ−μ has integral zero, hence is exact because F is connected, oriented, and closed. Let it equal dη.

For μ_s=(1−s)μ+sφ*μ, positivity is preserved. Defining the time-dependent vector field by contraction ι_Xs μ_s=−η is valid in every positive fibre dimension. Its smooth flow exists throughout the compact time interval because F is compact. Since dμ_s=0, the derivative of a_s*μ_s is

    a_s*(dη+d(ι_Xs μ_s))=0.

The minus sign is correct. It follows that a₁*φ*μ=μ. The required monodromy is ψ=φ∘a₁, because pullbacks reverse composition. Thus ψ*μ=μ. The path φ∘a_s proves the claimed isotopy. Reversing the order to a₁∘φ would not generally preserve μ.

This is the standard volume-form method associated with Moser, with the required special case fully supplied in the proof. The audit does not import an additional unproved metric-existence conclusion from Moser. [Moser, *On the volume elements on a manifold*](https://doi.org/10.1090/S0002-9947-1965-0182927-5).

## 4. The same bundle and the same projection

Changing the monodromy up to isotopy alone would need a bundle-isomorphism argument. The proof supplies it explicitly:

    D:Tψ→Tφ,  [x,t]↦[a_χ(t)(x),t],

where χ is constant at 0 and 1 on endpoint collars. At the upper seam the image is identified with (φa₁(x),0)=(ψ(x),0), which agrees with the image of the corresponding lower-seam point. The inverse is induced by a_χ(t)⁻¹ and satisfies the analogous relation.

All seam derivatives are covered, not just values. In a lower-seam coordinate z=ψ(x), the upper-collar expression for D becomes φa₁ψ⁻¹(z)=z, while the lower-collar expression is the identity. Both are constant in the transverse coordinate. Thus the expressions agree on collars, and every transverse and mixed derivative agrees. Smoothness of the inverse follows identically. The interior maps are diffeomorphisms varying smoothly with t.

Since D leaves t unchanged, it covers the identity of S¹. Transferring the metric through this map changes neither the original projection p nor its integral cohomology class. This is stronger than merely obtaining some unrelated harmonic fibration on a diffeomorphic total space.

## 5. Fixed-volume interpolation and metric descent

The endpoint metrics are h₀ and h₁=ψ*h₀. Their volume forms agree pointwise because ψ*μ=μ. Positive-definiteness is preserved by convex interpolation k_t. The smooth positive ratio r_t=vol(k_t)/μ is globally defined on the cylinder.

For m=dim F>0, conformal rescaling by r_t^(−2/m) gives

    vol(r_t^(−2/m)k_t)=r_t^(−1)vol(k_t)=μ.

The exponent is correct. A real positive power of a smooth positive function is smooth. The endpoint ratios are one, and χ's constant collars make the metric family exactly h₀ and ψ*h₀ on those collars. The restriction to m>0 avoids division by zero. There is no such scope issue in the application m=6.

The full metric G=dt²+h_t has no mixed terms and is positive-definite. Across the gluing map, dt is unchanged and the vertical metric pulls back by ψ. The relation h₁=ψ*h₀ establishes agreement as tensors on seam collars. It therefore matches all spatial, transverse, and mixed jets. No isometry of one fixed fibre metric is assumed. A time-dependent family is precisely what permits general monodromy.

Volume preservation does not assert det(Dψ)=1 in arbitrary coordinates. It asserts the appropriate density-weighted identity. The proof is coordinate-free and does not confuse these statements; the finite matrix checks use volume-normalized frames.

## 6. Hodge star and transfer of harmonicity

With orientation dt∧μ, the form dt has norm one and is orthogonal to the vertical cotangent space. Hence its Hodge star is exactly μ. The sign is positive because the base factor was placed first in the orientation.

The form μ descends because ψ*μ=μ, is independent of t, and has fibre-top degree. Consequently its full exterior derivative is zero: the transverse derivative vanishes, and its vertical derivative has degree greater than dim F. Both dt and its Hodge star are closed. Therefore dt is co-closed and closed, hence harmonic. The sign convention in the codifferential or Laplacian cannot affect this zero conclusion.

For the fibre-preserving diffeomorphism J:Tψ→M, the metric g=(J⁻¹)*G makes J an isometry. Pullback gives J*(p*dθ)=dt. The naturality of exterior differentiation and the Hodge star under this oriented isometry transfers the harmonicity calculation to the original p. Even reversing the global orientation would only reverse the relevant star convention and would not alter co-closedness.

## 7. Circle-valued harmonic maps and uniqueness

Hodge theory supplies a unique harmonic real one-form α in the image of u. Its periods remain integral because it represents u, so integration modulo Z defines a smooth circle-valued map in that class. A local real lift is harmonic exactly when its differential is co-closed; closedness is automatic. Thus harmonic maps to the flat circle correspond to harmonic integral-period one-forms.

The constructed p has the harmonic one-form p*dθ in class u, so it is a harmonic representative. Any other harmonic map in that class has the same differential by Hodge uniqueness. Their circle-valued difference has zero differential and is constant on connected M. Therefore every harmonic representative in that fixed class and constructed metric is p followed by a rotation, and is a fibration. Primitivity supplies connected fibres, not harmonic-map uniqueness itself. Negating p*dθ gives the same conclusion for −u with the very same metric.

## 8. Reproduced checks and targeted counterchecks

The frozen author script is 4,667 bytes, SHA256 `6f70b3fcd598ddbf7685ec1b6150fba1d6278d8f57cfd3c10355ee14cd5327d2`. Running it independently reproduced all 60 exact-rational interpolation checks. Standard output matched the frozen 555-byte `CHECK_RESULTS.json` byte-for-byte, SHA256 `cb322f9782106b74a5aa65de207943e8e12004870d65bf3f1cb55325c8e5e7a6`.

The accompanying independent `check_adversarial_sanity.py` also passes. It records exact algebraic witnesses for the following pitfalls:

1. Even equal-volume positive endpoint metrics can have a variable-volume convex interpolation. For endpoints I and diag(4,1/4,1,1,1,1), at t=1/4 the determinant is 91/64 and the logarithmic volume derivative is 36/91. The normalized derivative is zero.
2. The exponent −2/m cancels volume variation; replacing it by −1/m does not. Dimensions one through nine are checked as sanity cases, while the proof gives the general identity.
3. Density-weighted volume preservation works with a coordinate Jacobian of four; unimodularity in arbitrary coordinates is unnecessary.
4. For the circle diffeomorphism φ(x)=x+sin(2πx)/(4π), let R translate by 1/2 and a=φ⁻¹∘R. Then φ∘a=R preserves dx, whereas a∘φ has derivative three at zero and does not. This confirms the importance of composition order.
5. Endpoint equality alone misses seam derivatives: the factor 1+t(1−t) has equal endpoint values and opposite endpoint first derivatives.
6. Even constant total fibre volume is insufficient. On T⁶, the positive density ρ=1+(1/2)sin(2πt)cos(2πx₁) integrates to one on every fibre. For h_t=ρ^(1/3)I, the product-cylinder projection nevertheless has nonzero Laplacian at t=x₁=0. Pointwise fixed volume is the sufficient condition used by the proof.

These are exact finite arithmetic checks coupled to explicitly stated examples. They are not numerical proofs of global smooth existence, classifications of exotic structures, checks of infinite jets, or counterexamples to the arbitrary-metric assertion about the harmonic representative itself. The global arguments are in Sections 1–7 above and in the accepted proof.

## 9. Scope, prior credit, and limits of acceptance

The original report's Day 5 paragraph on printed p.164 was independently visually inspected. It leaves the metric quantifier and the harmonic map's homotopy class unstated. Thus E's existential metric and primitive-class normalization must remain explicit editorial choices. The neighbouring curvature discussion does not authorize discarding or retaining curvature as authenticated author intent. [Oberwolfach primary report](https://ems.press/content/serial-article-files/46667).

Katz's printed p.39 was independently visually inspected: it credits Calabi for intrinsic harmonicity and explicitly includes the nonsingular closed-one-form case. This supports the proof's prior-result attribution. Calabi's complete original chapter was not inspected. The explicit mapping-torus argument makes reliance on an inaccessible original proof unnecessary for this special case. [Katz, *Harmonic forms and near-minimal singular foliations*](https://ems.press/content/serial-article-files/42917).

No arbitrary or prescribed metric is analyzed by replacing it with the constructed one. No curvature sign is preserved by the conformal normalization. No classification or existence proof for a particular exotic-sphere connected sum is needed: the conclusion quantifies over every smooth total space in the stated homeomorphism class. The audit neither proves that a nonstandard sphere summand yields an exotic total space nor identifies classification indices from different references.

The substantial imported topological theorem and Serre's finite-generation theorem are accepted as credited literature, with their statements and applications checked; their complete proofs are not independently rederived or formally verified. Standard de Rham, Hodge, flow, and bundle theory remain dependencies. There is no remaining gap in E at that ordinary mathematical standard.

**Final acceptance: affirmative E only, by prior results and the explicit valid construction. The broader historical source is not unconditionally certified as solved.**
