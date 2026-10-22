# A rectifiable projective-Anosov limit circle that is not C¹

## Conclusion and attribution

For every closed oriented surface S of genus at least 2, there is a representation
ρ: π₁(S) → PGL(4, ℝ) whose projective limit set is a rectifiable embedded circle and is not a C¹ submanifold. It therefore is not C^{1,α} for any α > 0.

This answers the existence question in Tengren Zhang's Problem 10, printed p. 2527 of [OWR]. This is a reconstruction of established examples, with no novelty claim. The published introduction of Pozzetti–Sambarino–Wienhard [PSW, p. 3304] describes the corresponding product-Fuchsian boundary graph and its non-C¹ property when the factors are not conjugate. Glorieux–Monclair [GM, Theorem 1.3] proves the general C¹ rigidity theorem for AdS quasi-Fuchsian limit sets. The argument below explicitly passes from the product boundary to projective three-space and verifies the required Anosov property.

Here C¹ and C^{1,α} refer to regular embedded submanifolds, as in the cited literature. No regularity of a particular chosen boundary parametrization is assumed.

## 1. Choose the hyperbolic structures

Write Γ = π₁(S). Choose an oriented pants decomposition with an essential cuff c. Construct a marked hyperbolic metric m₁ by taking all cuff lengths to be 1 and all twist parameters to be 0. Construct m₂ in the same way except that the length of c is 2. The hyperbolic pants construction and gluing of equal-length boundaries produce closed hyperbolic surfaces with the same oriented marking. Let

jᵢ: Γ → PSL(2, ℝ),  i = 1, 2,

be their cocompact Fuchsian holonomies. If γ represents c, their translation lengths satisfy ℓ₁(γ) = 1 and ℓ₂(γ) = 2. More generally, the proof needs only a choice with 0 < ℓ₁(γ) < ℓ₂(γ).

The orbit quasi-isometries identify each visual boundary with ∂Γ. Since the markings have the same orientation, their boundary identifications give an orientation-preserving homeomorphism

h: ℝP¹ → ℝP¹,  h ∘ j₁(δ) = j₂(δ) ∘ h  for δ ∈ Γ.

We identify ∂Γ with the first copy of ℝP¹.

## 2. The projective tensor representation

Put V = ℝ² ⊗ ℝ² and define

ρ(δ) = [A₁(δ) ⊗ A₂(δ)] ∈ PGL(V),

where Aᵢ(δ) is either determinant-one representative of jᵢ(δ). Changing either representative's sign changes the tensor by a scalar. Also, the possible sign error in multiplying representatives is a scalar after tensoring. Thus ρ is a well-defined homomorphism. We do not need to choose coherent lifts Γ → SL(2, ℝ).

Let aᵢ(δ) ≥ 0 be defined by the singular values e^{aᵢ(δ)}, e^{-aᵢ(δ)} of Aᵢ(δ), using Euclidean norms and the induced tensor-product norm. The tensor singular values are the pairwise products of the factor singular values. In decreasing order their logarithms are

a₁ + a₂,  |a₁ − a₂|,  −|a₁ − a₂|,  −a₁ − a₂.

Consequently,

log(σ₁(ρ(δ))/σ₂(ρ(δ))) = 2 min(a₁(δ), a₂(δ)).                 (1)

Fix a finite symmetric generating set of Γ and let |δ| be ordinary word length. The cocompact orbit maps satisfy

d_H²(oᵢ, jᵢ(δ)oᵢ) ≥ cᵢ |δ| − Cᵢ

for constants cᵢ > 0 and Cᵢ ≥ 0. Choose the basepoints associated with the Euclidean norms. In curvature −1 normalization their displacements equal 2aᵢ(δ). With c = min(c₁,c₂) and C = max(C₁,C₂), equation (1) therefore gives

σ₂(ρ(δ))/σ₁(ρ(δ)) ≤ exp(C) exp(−c|δ|)  for every δ ∈ Γ.     (2)

The dominated singular-value criterion, stated as Definition 2.3 in the published [PSW, p. 3315], says precisely that (2) is the projective, or 1-Anosov, condition. This argument uses displacement and ordinary word length, not translation length and conjugacy length.

## 3. Identify the limit curve and its dual

The Segre embedding is

F: ℝP¹ × ℝP¹ → ℝP³,  F([u],[v]) = [u ⊗ v].

It is injective, smooth, and an immersion; compactness makes it an embedding. Define

ξ(x) = F(x,h(x)).

This is a continuous, injective, ρ-equivariant map. Every nontrivial δ is hyperbolic in both factors. Its top tensor eigenline is the tensor product of their attracting eigenlines. Hence ξ(δ⁺) is the attracting eigenline of ρ(δ). Attracting fixed points are dense in ∂Γ, so ξ is the projective-Anosov boundary map. Equivalently, one can identify the limits of leading singular lines along geodesic rays in the two factors.

For a direct check of dual transversality, let ω be the standard nondegenerate alternating form on ℝ² and set B = ω ⊗ ω. Then B is symmetric, nondegenerate, has signature (2,2), and is preserved by every A₁ ⊗ A₂. For x ≠ y,

B(u_x ⊗ v_{h(x)}, u_y ⊗ v_{h(y)})
  = ω(u_x,u_y) ω(v_{h(x)},v_{h(y)}) ≠ 0.

Thus η(x) = ξ(x)^{⊥_B} is a continuous equivariant hyperplane map and ξ(x) is transverse to η(y) whenever x ≠ y. At a fixed point δ⁺, η(δ⁺) is the attracting dual hyperplane; the repelling hyperplane for ρ(δ) itself is η(δ⁻). This distinction avoids a sign or attracting/repelling convention ambiguity.

The limit set Λ = ξ(∂Γ) is consequently the Segre image of the embedded circle Graph(h).

## 4. Rectifiability, with an explicit length bound

Give each ℝP¹ its round metric with circumference π. An increasing lift H: ℝ → ℝ of h satisfies

H(t+π) = H(t)+π.

The graph over one period is traced by t ↦ (t,H(t)). For any ordered partition of [0,π], the product-distance increment is bounded by the sum of the increments of the two coordinates. Summing and taking the supremum gives

Length(Graph(h)) ≤ π + π = 2π.                              (3)

Give ℝP³ the standard round quotient metric induced from the unit sphere in V. In unit-vector representatives, the derivative of F sends a tangent pair (u′,v′) to

u′ ⊗ v + u ⊗ v′.

Because u′ ⟂ u and v′ ⟂ v, the squared norm is ||u′||² + ||v′||². Therefore F preserves the induced infinitesimal product metric and curve length. In particular,

Length(Λ) ≤ 2π.                                            (4)

All smooth Riemannian metrics on the compact ambient projective space are uniformly comparable, so finite length does not depend on this convenient normalization.

There is even a local Lipschitz-submanifold statement, which does not assert that h itself is Lipschitz in its original coordinate. In an increasing affine chart, set s = x+h(x) and t = h(x)−x. For x₂ > x₁,

|t(x₂)−t(x₁)| ≤ s(x₂)−s(x₁).

The s-coordinate is strictly increasing, so the graph becomes the graph of a 1-Lipschitz function of s. Rotating both coordinates by the factor 1/√2 gives the same Lipschitz constant in orthonormal coordinates.

## 5. The limit curve cannot be C¹

Conjugate the two actions by separate projective coordinate changes so that the attracting and repelling fixed points of the chosen γ are 0 and ∞. The equivariant homeomorphism h fixes these two points. On the affine line the actions are

x ↦ λ₁x and y ↦ λ₂y, where λᵢ = e^{-ℓᵢ(γ)}.

Thus 0 < λ₂ < λ₁ < 1 and

h(λ₁x) = λ₂h(x).                                           (5)

Let r = ℓ₂(γ)/ℓ₁(γ) > 1, so λ₂ = λ₁^r. On the compact set

E = {u ∈ ℝ : 1 ≤ |u| ≤ λ₁^{-1}},

h is finite and continuous, because h^{-1}(∞) = ∞. Put

M = max_{u∈E} |h(u)|/|u|^r < ∞.

Every sufficiently small nonzero x can be written x = λ₁^n u with n ≥ 0 and u ∈ E. Iterating (5) yields the two-sided bound

|h(x)| = λ₂^n |h(u)| ≤ M |x|^r,

and hence

|h(x)/x| ≤ M |x|^{r−1} → 0.                               (6)

For the concrete pants choice r = 2. Equation (6) shows that all secants of Graph(h) approaching (0,0) tend to the horizontal line.

Suppose Graph(h) were a C¹ embedded submanifold of ℝP¹ × ℝP¹. Its tangent at (0,0) would then be horizontal. Let

L_(x,y) = T_xℝP¹ × {0}

be the global horizontal line distribution. Every product projective transformation (j₁(δ),j₂(δ)) preserves L and preserves Graph(h). The tangent to Graph(h) is therefore horizontal at every point in the Γ-orbit of (0,0). The boundary action of a cocompact Fuchsian group is minimal, so this orbit is dense in Graph(h).

A C¹ embedded curve has a continuous tangent-line map. Since L is continuous, equality of the two line fields on a dense subset forces equality everywhere on the graph. The differential of the second projection restricted to this C¹ curve is then zero at every point. In local C¹ coordinates this projection is constant, and connectedness makes it globally constant. But its restriction to Graph(h) is surjective onto ℝP¹. This is a contradiction.

Finally, if Λ were a C¹ embedded curve in ℝP³, it would also be a C¹ embedded curve in the smooth Segre surface containing it. Local submanifold charts for that surface, followed by F^{-1}, would make Graph(h) C¹. The contradiction above therefore proves that Λ is not C¹ in ℝP³. In particular Λ cannot be C^{1,α} for any α > 0.

## 6. Scope

The representation preserves B, so its image lies in PO(2,2). No full-PGL Zariski-density statement is made or needed. The printed question imposes no irreducibility, ambient Zariski-density, fixed dimension, or higher-root Anosov hypothesis. The example answers that exact question in dimension 4.

The product homomorphism (j₁,j₂) used in the flag-space literature and the projective representation ρ = j₁ ⊗ j₂ are related by the Segre embedding. The block direct sum j₁ ⊕ j₂ is a different linear representation and is not the construction used here. The identical-factor case is also excluded: its diagonal boundary graph is smooth.

## References

[OWR] R. Penner, compiler, Problem Session, in New Trends in Teichmüller Theory and Mapping Class Groups, Oberwolfach Reports 40/2018; Tengren Zhang's Problem 10, printed p. 2527, PDF p. 53. https://ems.press/content/serial-article-files/46762 . DOI: https://doi.org/10.4171/OWR/2018/40 .

[PSW] M. B. Pozzetti, A. Sambarino and A. Wienhard, Anosov representations with Lipschitz limit set, Geometry & Topology 27(8) (2023), 3303–3360. Published p. 3304 gives the product-Fuchsian example and its conjugacy exception; p. 3315, Definition 2.3 gives the singular-value criterion; p. 3344, Definition 8.1 and Proposition 8.2 discuss the AdS class. https://doi.org/10.2140/gt.2023.27.3303 . Published PDF: https://msp.org/gt/2023/27-8/gt-v27-n8-p06-s.pdf . Preprint history: https://arxiv.org/abs/1910.06627 .

[GM] O. Glorieux and D. Monclair, Regularity of limit sets of AdS quasi-Fuchsian groups, Mathematical Research Letters 31(2) (2024), 429–439. Theorem 1.3 of the inspected arXiv v2, PDF p. 2, is the C¹ rigidity result. https://arxiv.org/abs/1809.10639 ; https://arxiv.org/pdf/1809.10639v2 . Publication metadata: https://doi.org/10.4310/MRL.241024233904 and the author's publication list at https://www.imo.universite-paris-saclay.fr/~daniel.monclair/research.html . The journal PDF was not successfully obtained; no claim of inspecting its typeset theorem numbering is made.
