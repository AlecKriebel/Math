# Independent audit: discriminant-localized standard Gaitsgory comparison

## Verdict and precise scope

**Verdict: accept the accompanying mathematical report as a rigorous localized partial theorem. Do not classify the original AIM Problem 4.3 as solved by this work.**

The audited claim concerns characteristic zero, the standard type-A realization at δ=0, every n≥3, and the homogeneous localization S=C[x₁,…,xₙ,Δ⁻¹]. It constructs an actual strong monoidal dg functor to bounded complexes of graded graph S-bimodules. It identifies the localized standard object and the two specified operators, in the homotopy category, with (Sⁿ,diag(x₁,…,xₙ),0). The geometric side is the regular-semisimple open of GNR's semi-nilpotent flag Hilbert scheme FHilbₙ(C), with its own specified derived enhancement.

This is neither a construction of the unlocalized flattening nor an identification through a previously constructed global GNR functor. It excludes the prescribed cyclic arrow, half-braiding, and collision locus. Novelty is not established by this audit; the component mechanisms are standard.

The distributed [mathematical report](MATHEMATICAL_REPORT.md) has 21,601 bytes and SHA-256 `f96ee593965eb3a3a5ffe25bc852adac9b5e899fe7e1c591e781666275f1088b`. Its complete mathematical argument is preserved. This AI-assisted, unrefereed audit is not external human peer review, journal acceptance or formal proof-assistant certification.

## 1. Literal MMV conventions

The comparison must be pinned to chain complexes rather than to the labels of the decategorified evaluation maps. In the retained version of [MMV], equation (60) has Bᵢ in degree zero and the enddot to R⟨1⟩ in degree one. Definition 4.14 defines Tρ as T₁⋯Tₙ₋₁. Equations (116)–(117), at parameters r=s=0, give the rotation image Tρ and the affine-color image Tρ⁻¹B₁Tρ. These agree with the complexes used by the candidate and the positive flattening convention of [Elias, §2.6].

This audit independently inspected the actual diagrams in equations (60) and (116)–(122). Equation (122) identifies the affine dots with the finite dots surrounded by the relevant rotation unit/counit. It supplies the morphism-level input required for the affine Rouquier comparison. The result is not inferred merely from the image of the object B₀ or a braid-group/K-theory equality.

[MMV, Theorem 5.4] is used only as a theorem about a graded additive monoidal functor to a homotopy category. Its extension to arbitrary unlocalized complexes is not assumed. The theorem is stated for n≥3, matching the candidate's scope.

## 2. Realization and scalar specialization

[MMV] uses the root-span realization. Its finite root variables are retained, its affine root maps to minus the sum of the finite roots, and the imaginary root becomes zero in the target homotopy category; compare [MMV, concluding Remark 5.6(2)]. After this quotient, adjoining the invariant GLₙ coordinate c gives C[x₁,…,xₙ], with xᵢ expressed using c/n and the finite roots. In characteristic zero this scalar extension is legitimate.

The order matters: the invariant coordinate is adjoined after δ=0, when rotation fixes c. No claim that δ already vanished for arbitrary chain representatives is necessary. Applying H⁰ to a zero homotopy class gives the literal zero map, so the final actual additive functor factors through the required quotient. Right multiplication by the xᵢ in Hathaway's filtered theorem therefore becomes right multiplication by the same xᵢ in S.

## 3. Split contractions, not enveloping-ring projectivity

The map S⊗_{Sˢ}S→S⊕S_s with components a⊗b↦(ab,a s(b)) is a bimodule isomorphism. Its explicitly stated inverse idempotents are valid because α=xᵢ−xᵢ₊₁ is invertible. Inverting Δ², which is invariant, justifies the compatible two-sided localization. The resulting modules are free on each side; projectivity as S⊗C S-modules is neither needed nor generally true.

The positive crossing becomes a projection differential [S(1)⊕S_s(1)→S(1)]. Its identity-component pair has the explicit contracting homotopy recorded in the candidate. The inverse crossing has differential (α,0), up to the nonzero dot normalization, and contracts using α⁻¹. Its surviving S_s(1) is identified with S_s(−1) by multiplication by α⁻¹. All these maps have the stated homogeneous degrees.

Tensor products of these homotopy equivalences remain homotopy equivalences. This uses the actual split contractions and ordinary cochain tensor signs. It does not replace a quasi-isomorphism by a homotopy equivalence. The positive rightward Jucys–Murphy word has trivial permutation and writhe 2(n−i), so its graph model is S(2(n−i)) in degree zero.

## 4. H⁰ really supplies coherent strictification here

Let C₀ be the full subcategory of Kᵇ(P) whose objects are already homotopy equivalent to degree-zero objects of P. The inclusion P→C₀ is fully faithful because maps between degree-zero complexes have no nonzero chain homotopies. It is essentially surjective by definition.

Consequently H⁰ on C₀ is a quasi-inverse, not merely a cohomology invariant. The natural comparison from H⁰(C)[0] to C is uniquely determined in Kᵇ(P) by inducing the identity on H⁰. The cycle-representative Künneth map is invertible on C₀, and its associativity and unit diagrams commute. Uniqueness supplies compatibility of the comparison maps. This validates the strong monoidal coherence claimed by Lemma 4.1.

The localized images of finite Bott–Samelson generators, rotations, and affine generators lie in C₀ by the contractions and conjugation formulas. Closure under tensor products, internal shifts, sums, and retracts is justified. For retracts, transfer the idempotent to a degree-zero object and split it in P. No general formality claim for arbitrary complexes of graph modules is used.

Thus F₀=H⁰LE is an actual graded additive strong monoidal functor on the specified additive category.

## 5. Actual dg extension and affine Rouquier words

Applying F₀ to each term and to every homogeneous component of a dg Hom element commutes with the dg differential d(f)=d_D f−(−1)^|f| f d_C. This follows from additivity and literal preservation of composition. The termwise tensorator is a chain map for the total tensor differential d_C⊗1+(−1)^i1⊗d_D. Its naturality also respects the Koszul sign for tensor products of homogeneous morphisms. The monoidal coherence diagrams remain the diagrams already satisfied by F₀.

For the affine crossing, the image of its enddot is the conjugated finite enddot followed by the rotation counit. H⁰ turns this homotopy-category statement into an actual map of degree-zero models. Its two-term complex is identified with the localized conjugated finite crossing using the explicit contractions. The startdot is handled by the unit in the same way. Rotation and finite crossings have the required literal images. Tensoring gives the candidate's equation (4.2) on Wakimoto Rouquier words.

This argument is confined to explicit crossings and their words. It does not require an extension of the original MMV functor to arbitrary unlocalized complexes.

## 6. Filtration and χ

[Elias, Theorem 8.40] gives the standard object's Wakimoto filtration with each standard weight occurring once. The functor Kᵇ(F₀) is exact, so it preserves these triangles. When both outer terms are degree-zero models, the connecting group Hom(Q,P[1]) in Kᵇ(P) is zero. Induction splits the filtration. This vanishing is a statement about a homotopy category, not an assertion that all extensions of bimodules in a derived category split.

[Hathaway, Theorem 1.8.1 / 5.1.6] supplies the filtration-preserving χ and its diagonal xᵢ actions. After a filtered splitting, χ is triangular over the commutative ring S. Its characteristic polynomial is ∏ᵢ(z−xᵢ), which annihilates it. The Lagrange expressions eᵢ are therefore genuine pairwise orthogonal, exhaustive degree-zero idempotents. Each has exactly one nonzero filtered subquotient, so its image is the corresponding shifted rank-one module. This also identifies the indexed filtration.

The spectral summands are canonical; a basis for each is not. With the stated convention S(k)_d=S_{d+k}, multiplication by aᵢ⁻¹, where deg aᵢ=2(n−i), correctly gives S(2(n−i))→S. It does not discard the internal grading.

## 7. Monodromy

Once M is homotopy equivalent to a degree-zero object, Hom(M,M(−2)[2]) vanishes. Thus the image of μ is zero in Kᵇ(P). This does not assert that every initial chain representative of its image is literally zero: it may be nonzero and null-homotopic. The candidate makes that distinction.

## 8. Exact classical and derived geometric target

The strict-triangular requirement is indispensable. [GNR, equation (2.16)] sets all diagonal entries of Y to zero. On the pairwise-distinct X locus, the polynomial projectors split the tautological bundle over arbitrary base rings into rank-one eigenbundles compatible with the quotient flag. A commuting Y preserves those lines; its action on every associated flag quotient is zero, so it vanishes on each eigenline. Unrestricted flag Hilbert schemes allow nonzero diagonal Y and would invalidate the conclusion.

The components εᵢ(X)v of the cyclic vector generate the eigenlines. They trivialize the bundle, with X diagonal, Y=0, v=(1,…,1), and the standard quotient flag. This is a functorial construction over rings with invertible eigenvalue differences and has trivial stabilizers. It establishes the scheme identification with U, not just a pointwise assertion.

The commutator target is exactly the strictly lower triangular space n₀ in [GNR, equation (2.9)], or the bundle of nilpotent radicals Adjn in equation (2.10). The Koszul algebra in equation (2.13) consequently has no redundant diagonal directions. On this chart ad_X on n₀ has determinant the product of the eigenvalue differences. It is invertible, so the commutator equations eliminate the Y variables as a regular sequence. The resulting Koszul algebra is quasi-isomorphic to the ordinary quotient. It need not be a split contraction as a module over the entire ambient coordinate ring.

[GNR, §2.7] subsequently uses the projective-tower description. It can be checked independently on U: A=X−x_new is invertible, and with Y=0 the two differentials in (2.25) are Ψ(w)=(0,Aw,0) and Φ(u,w,f)=Au+fv. The kernel modulo image is O, with section f↦(−A⁻¹vf,0,f). The two complementary pairs contract using A⁻¹, with the equivariant twists retained. Derived projectivization of this rank-one degree-zero object adds no derived direction. Induction proves that the actual tower model has the same underived open U.

The projectors are homogeneous of weight zero. The supplied conversion of q and t makes X and Y have precisely the χ and μ degrees; Y is zero on both sides.

## 9. Stress tests and limits

The written audit checks the contraction, spectral-projector and geometric arguments in their stated all-rank scope. Its mathematical boundary cases are explicit: unrestricted commuting Y can retain diagonal components, and a collision can retain a nonzero nilpotent Jordan block. Supplemental programs and computational outputs are not distributed. Acceptance rests on the written arguments and their exact cited inputs; this audit does not independently reprove the complete diagrammatic relations in MMV.

The global obstruction cannot be dismissed: the nonzero complex [R→R] with differential Δ² becomes contractible over S. Agreement after localization therefore cannot recover data supported on the collision divisor. The known rank-two calculations do not establish the missing unlocalized n≥3 comparison, and no neighboring center-generation question is addressed.

## 10. Mathematical safeguards verified

1. Pin the MMV convention by its literal chain formulas, rather than an unsafe inference from the names of the two evaluation maps.
2. Give the morphism-level cone/counit argument for the affine crossing in equation (4.2).
3. State α⁻¹ as the inverse-crossing shift-normalization map.
4. Say the geometric ambient Koszul algebra is quasi-isomorphic to the ordinary quotient, rather than claiming a split ambient-module contraction.
5. Cite the exact nilpotent-radical commutator target and check the projective-tower enhancement directly.

All five safeguards are included in the mathematical report identified above. No further mathematical defect was found in the stated localized theorem. Acceptance is limited to that exact scope and the preserved mathematical argument. The audit does not independently reprove MMV’s complete diagrammatic theorem or establish novelty.

## Primary references

- B. Elias, *Gaitsgory's central sheaves via the diagrammatic Hecke category*, arXiv:1811.06188v1, §§2.6, 4.2, 8.7. https://arxiv.org/abs/1811.06188v1
- M. Mackaay, V. Miemietz, P. Vaz, *Evaluation birepresentations of affine type A Soergel bimodules*, arXiv:2207.02459v2, §§3–5. https://arxiv.org/abs/2207.02459v2
- J. Hathaway, *A special endomorphism of the standard Gaitsgory central object of the affine Hecke category*, dissertation, University of Oregon, December 2023, Theorems 1.8.1 and 5.1.6. https://hdl.handle.net/1794/29277
- E. Gorsky, A. Neguț, J. Rasmussen, *Flag Hilbert schemes, colored projectors and Khovanov–Rozansky homology*, arXiv:1608.07308v1, §§2.2–2.7. https://arxiv.org/abs/1608.07308v1
