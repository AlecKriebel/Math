# Hemminger Theorem 4.1: a local correction of the bottom-row argument

**Authorship and review status:** This authored report was prepared with AI assistance and is unrefereed, with no proof-assistant certification. Its mathematical acceptance is scoped to the explicitly named foundations. This report's status is distinct from the bibliographically confirmed journal publication of Hemminger's prior result.

## Verdict and scope

The paragraph on arXiv:1911.03033v2, printed page 16, contains a false centralizer identification. If the representation of `im(ρ)` has character multiplicities `m_χ`, its centralizer in `GL_n` is `∏_χ GL_{m_χ}`, not in general `GL_{n−r} × G_m^r` for `r = rank(im(ρ))`. For example, a nontrivial scalar character in dimension two has rank-one image and centralizer `GL_2`; the displayed source formula would give `G_m × G_m`.

The bottom-row exactness nevertheless has a complete local repair using the same flag-bundle computation and faithfully flat descent already used in Lemmas 4.6–4.7. One must preserve the actual `C_G(λ)` action, discard empty transporters, and include the mixed pairs of nonempty components. The following replacement proves precisely that missing step. It does not claim that the source paragraph is correct as printed, that the journal text has been inspected, or that every other argument in the paper has been audited.

All Chow groups below have coefficients in `F_p`. The assumptions are `char(k) ≠ p` and `μ_p ⊂ k`. The target case is a finite constant group `G` and `X = Spec(k)`. The argument below also works for the smooth equivariant schemes and quotients used in the source, whenever the usual equivariant Chow constructions apply.

## 1. The fixed-point components and their rational points

Fix an embedding `G → H = GL_n`, the subgroup `S = (μ_p)^n` of diagonal matrices, an elementary abelian `p`-group `V`, and a homomorphism `λ: V → G`. Write

- `C = C_G(λ)`;
- `Z = X^λ`;
- `K = H/S`;
- `Y_ρ = {a ∈ H : a⁻¹ λ(v) a = ρ(v) for every v ∈ V}` for `ρ: V → S`;
- `I = {ρ : Y_ρ ≠ ∅}`.

Here nonemptiness can be tested geometrically. The set of all `ρ: V → S` is finite.

Because `p` is invertible and all `p`th roots of unity lie in `k`, each representation of `V` is a direct sum of its `k`-rational character spaces. This follows either from simultaneous diagonalization or from the character idempotents

`e_χ = |V|⁻¹ ∑_{v∈V} χ(v)⁻¹ λ(v)`.

A transporter `Y_ρ` is nonempty over an extension field exactly when the `λ` and `ρ` character spaces have equal dimensions for every `χ`. Those dimensions do not change under extension. In that case choose a `k`-linear isomorphism from each `ρ` character space to the corresponding `λ` character space. Their direct sum is a matrix `a_ρ ∈ GL_n(k)` satisfying `a_ρ⁻¹ λ a_ρ = ρ`. Thus every nonempty transporter has a `k`-point. Moreover, `I` is nonempty: a character basis for `λ` gives at least one diagonal `ρ`.

There is a disjoint-union decomposition

`K^λ = ⨿_{ρ∈I} Y_ρ/S`.

To see this also for scheme-valued points, lift a fixed coset in `H/S` fppf-locally to `a`. For each `v`, the element `a⁻¹ λ(v) a` lies in `S`. Changing the lift by an element of the abelian group `S` does not change these elements. They therefore define a locally constant homomorphism `V → S`, giving the stated finite decomposition. Conversely such a transporter point produces a fixed coset.

For `c ∈ C`,

`(ca)⁻¹ λ(v) (ca) = a⁻¹ λ(v) a`.

Consequently `C` preserves each individual `ρ` component. It does not permute them.

## 2. The correct centralizer and the transported action

Set `L_ρ = C_H(ρ)`. With `m_{ρ,χ}` the multiplicity of the character `χ` in `ρ`, the character decomposition gives an isomorphism of group schemes

`L_ρ = ∏_{χ : m_{ρ,χ}>0} GL(W_{ρ,χ}) ≅ ∏_χ GL_{m_{ρ,χ}}`.

The coordinate torus `T = G_m^n` and its `p`-torsion subgroup `S` lie in `L_ρ`. Relative to the coordinate blocks,

`T = ∏_χ T_χ`, `S = ∏_χ S_χ`, and `L_ρ/S ≅ ∏_χ (GL_{m_{ρ,χ}}/S_χ)`.

The map `l ↦ a_ρ l` identifies `L_ρ` with `Y_ρ`, equivariantly for the right `S` action. It identifies the left `C` action with multiplication through the homomorphism

`φ_ρ: C → L_ρ`, `c ↦ a_ρ⁻¹ c a_ρ`.

The target is indeed `L_ρ` because `c` centralizes `λ`. Thus `Y_ρ/S ≅ L_ρ/S` as `C`-schemes when the latter action is defined by `φ_ρ`. The action on `Z` stays the original `C` action.

This step does not replace `C_G(λ)` by `C_H(λ)`. It also makes no assumption that `C` acts transitively on `L_ρ/S`. Any additional orbit or double-coset geometry remains inside the equivariant quotient for this actual subgroup action.

## 3. Blockwise equivariant flag-bundle formula

Let `R = CH_C^*(Z)`. For each `ρ∈I`, put

`A_ρ = CH^*(BL_ρ) = F_p[c_{ρ,χ,i} : 1 ≤ i ≤ m_{ρ,χ}]`,

`B_ρ = CH^*(BS) = F_p[y_{ρ,χ,j} : 1 ≤ j ≤ m_{ρ,χ}]`.

The map `A_ρ → B_ρ` sends `c_{ρ,χ,i}` to the `i`th elementary symmetric polynomial in the variables of the `χ` block. The map `A_ρ → R` is induced by `φ_ρ` and the structural map `Z → Spec(k)`. In other words, its Chern classes are those of the block representations of the actual group `C`.

The blockwise version of Lemma 4.6 gives a natural isomorphism

`D_ρ := CH_C^*(Z × Y_ρ/S) ≅ R ⊗_{A_ρ} B_ρ`.

Here is the geometric computation, including the point on which equivariance matters. On a finite-dimensional free approximation to `[Z/C]`, let `E_{ρ,χ}` be the vector bundles associated to the block representations of `C`. The associated `L_ρ/T` bundle has the same Chow ring as the product of the complete flag bundles of the `E_{ρ,χ}`. The comparison is the usual iterated affine-bundle comparison between `L_ρ/T` and `L_ρ/B`, applied in each block. Iterating the projective-bundle formula gives

`R[y_{ρ,χ,j}] / (e_i(y_{ρ,χ,*}) − c_i(E_{ρ,χ}))`.

The associated `L_ρ/S` bundle maps to the `L_ρ/T` bundle as a torsor under `T/S`. Identifying `T/S` with `G_m^n` by the `p`th-power map, its line bundles are the `p`th powers of the tautological line bundles. Localization for the complement of each zero section therefore imposes the additional relations

`c_1(L_{ρ,χ,j}^{⊗p}) = p y_{ρ,χ,j} = 0`.

These relations already vanish modulo `p`, proving the displayed formula. This is a blockwise repetition of the source's Lemma 4.6, not an assumption that ordinary nonequivariant Chow triviality lets one remove a torus carrying a group action. Choosing approximations with arbitrarily high complement codimension establishes the formula in every Chow degree.

The same computation with two families of bundles gives, for every ordered pair `(ρ,σ)∈I²`,

`CH_C^*(Z × Y_ρ/S × Y_σ/S)`

`≅ R[y_ρ,y_σ]/(e(y_ρ)−c_ρ, e(y_σ)−c_σ)`

`≅ D_ρ ⊗_R D_σ`.

Under this isomorphism, the two projections induce `d ↦ d⊗1` and `d′ ↦ 1⊗d′`, respectively. This compatibility follows from the same tautological line bundles and not merely from an abstract ring isomorphism.

## 4. Freeness over the symmetric polynomial rings

For a block of size `m`, the polynomial ring `F_p[y_1,…,y_m]` is finite free of rank `m!` over `F_p[e_1,…,e_m]`, in every characteristic. For completeness, start with the universal monic polynomial

`f(t) = t^m − c_1 t^{m−1} + ⋯ + (−1)^m c_m`.

Adjoin a first root `y_1`, a free extension of rank `m`. Divide by `t−y_1`, adjoin a root `y_2` of the resulting monic polynomial of degree `m−1`, and continue. The final root is determined. The resulting algebra is

`F_p[c_1,…,c_m,y_1,…,y_m]/(e_i(y)−c_i)`.

Eliminating the `c_i` identifies it with `F_p[y_1,…,y_m]`. Its displayed construction supplies the basis

`y_1^{a_1} ⋯ y_m^{a_m}`, where `0 ≤ a_j ≤ m−j`.

The basis contains `1`. Taking tensor products over all character blocks proves that `B_ρ` is free over `A_ρ` of positive rank `∏_χ m_{ρ,χ}!`, with a basis containing `1`. Thus `D_ρ` is faithfully free over `R` with a basis containing `1`. No division by a factorial, Noetherian hypothesis, or assumption `p ∤ |G|` is involved.

In particular, both `R → D_ρ` and `R → D_ρ ⊗_R D_σ` are injective: in the above bases, the coefficient of `1`, or of `1⊗1`, recovers the input.

## 5. Exactness including all mixed components

The desired fixed-`λ` row is now

`0 → R → ∏_{ρ∈I} D_ρ → ∏_{(ρ,σ)∈I²} (D_ρ ⊗_R D_σ)`,

where the last map sends `(d_ρ)` to `(d_ρ⊗1 − 1⊗d_σ)_{ρ,σ}`. All the component sets here are finite. The map from `R` is injective by restriction to any nonempty component.

Suppose `(d_ρ)` lies in the kernel. Taking the diagonal pair `(ρ,ρ)` gives

`d_ρ⊗1 = 1⊗d_ρ` in `D_ρ ⊗_R D_ρ`.

Write `d_ρ` in the free basis of `D_ρ` that contains `1`. Comparing coefficients in the tensor-product basis shows that all coefficients except the coefficient of `1` vanish. Thus `d_ρ` is the image of a unique `r_ρ∈R`. Equivalently, this is the degree-zero faithfully flat descent assertion used in Lemma 4.7.

Now use every mixed pair `(ρ,σ)`. Its equality becomes equality of the images of `r_ρ` and `r_σ` in `D_ρ ⊗_R D_σ`. The injectivity established above implies `r_ρ = r_σ`. Hence every component is the pullback of one common `r∈R`. Conversely, the pullbacks of any common `r` plainly satisfy all these equalities. This proves exactness.

The mixed-pair step is essential: separate same-component equalizers by themselves would allow unrelated classes `r_ρ` on different components. Nor may one require the same-component sequence for an empty transporter; its first map would be `R → 0`.

Applying this argument to each `λ` proves the bottom-row exactness needed in Theorem 4.1. If `Z` is empty the corresponding row is trivially zero. For the finite-group target, there are also only finitely many conjugacy classes of homomorphisms `V → G`, so passage to the full product in `λ` presents no additional issue.

## Consequence for the prior-applicability audit

This particular source-proof defect is repairable under exactly the field hypotheses already stated by Hemminger; it is not an unresolved obstruction to applying the downstream localization theorem to a finite group with `X = Spec(k)`. The repair introduces no stronger assumption such as algebraic closure, `p ∤ |G|`, or distinct character weights. It supplies only the missing descent step in an existing prior proof. Other dependencies of Proposition 6.1, including the Chow grading convention and nilpotent-filtration argument, must still be checked separately in the accompanying mathematical audit.

## Sources actually inspected

- David Hemminger, *Lannes's T-functor and equivariant Chow rings*, arXiv:1911.03033v2, https://arxiv.org/abs/1911.03033v2. Inspected the local text of Lemmas 4.6–4.7 and Theorem 4.1, printed pages 14–16; also rendered and visually inspected printed page 16 of the local PDF. The arXiv landing page associates this version with the 2021 journal article, but this audit does not claim journal-PDF inspection.
- The Stacks Project, Tag 03OA, https://stacks.math.columbia.edu/tag/03OA, states the faithfully flat descent assertion used by the source. The elementary free-basis verification above suffices for the exactness needed here without additional citation-dependent hypotheses.
