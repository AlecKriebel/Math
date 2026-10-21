# Independent audit of the PSC partial results

Audit date: 21 October 2026 (UTC).

## Verdict

**Accepted as precisely scoped partial results, not as a solution of the general Lie-manifold composition problem.**

1. For the standard two-ended b-compactification of `R × Y`, with scalar curvature strictly positive on the entire compactified base and temporal product concordances, each spatial end defines a well-defined map to ordinary PSC concordance classes on `Y`.
2. The product inclusion is a section of that map. Therefore closed concordance classes inject into the quotient by **all concordances allowed by this b-definition**, not merely spatially product concordances.
3. For connected closed spin `Y` of dimension at least five, the established closed based group law transfers to the product-representable image. It does not give a group law on the whole b-concordance set.
4. The separate fixed-exterior compact-core construction is justified by an actual boundary-relative classification theorem. Its equivalence relation must remain exterior-fixed.

The dimensional mismatch in a direct conformal reduction is real. The normalization-and-attachment argument in *A closed-concordance retract at a cylindrical Lie end*, Sections 2–3, repairs it. A direct reduction without that argument is not accepted.

## 1. Frozen normal metric and curvature calculation

Fix a boundary defining function and write its logarithmic normal coordinate as `r`. The normal metric is

`q = f²(dr + α)² + H`,

where `H` is the Schur-complement quotient metric, not the restriction to an arbitrary coordinate section. The central normal direction of the product b-algebroid makes these coefficients independent of `r`.

With `Δ = div grad` and `|F|²_ten = Σᵢⱼ F(eᵢ,eⱼ)²` for `F = dα`, the correct identity is

`scal(q) = scal(H) − (f²/4)|F|²_ten − 2 f⁻¹Δ_H f`.

Using the ordinary exterior-form norm instead replaces `1/4` by `1/2`. Thus the stated norm convention in the theorem is necessary and correct. There is no extra gradient term when the last term is written as `f⁻¹Δf`.

For base dimension `m > 1`, put `u = log f` and `Ĥ = f^{2/(m−1)}H`. The ordinary conformal scalar-curvature formula gives

`f^{2/(m−1)} scal(Ĥ) = scal(H) − 2Δu − ((m−2)/(m−1))|du|²`

`= scal(q) + (f²/4)|F|²_ten + (m/(m−1))|du|²`.

Every sign and exponent checks. In particular, the quotient is PSC when the invariant total metric is PSC. The formula also works at `m = 2`; it does not apply at `m = 1`.

The passage from a smooth b-metric to its normal curvature is valid: applying `x∂ₓ` to a smooth coefficient gives zero at `x = 0`, as do repeated normal b-derivatives. The remaining coefficient and tangential-derivative expressions are exactly those of the invariant normal model. Strict positivity on the compactified base therefore supplies strict positivity of the normal model. Mere pointwise interior positivity, whose infimum could be zero, would not suffice.

Replacing a boundary defining function by `a(y)x + O(x²)` changes the splitting by an exact connection shift. The normal length `f` and quotient metric `H` are unchanged, so the end metric used here is unaffected by that choice. No invariance under arbitrary changes of Lie structure is claimed.

## 2. The normalization path really stays PSC

First scale `α` to zero. The only term that changes in the preceding scalar formula is the nonpositive curvature term, so scalar curvature cannot decrease.

After that stage, set

`f_t = f^{1−t}`, `H_t = f^{2t/(m−1)}H`, `q_t = f_t² dr² + H_t`, for `0 ≤ t ≤ 1`.

The conformal quotient remains exactly `Ĥ`. Independently expanding the scalar formula gives

`scal(q_t) = f^{-2t/(m−1)} [f^{2/(m−1)}scal(Ĥ) − (m/(m−1))(1−t)²|du|²_H]`.

At `t = 0` the bracket is `scal(f²dr²+H) > 0`; at every later parameter the only subtracted term is smaller. This proves positivity, not merely small-perturbation positivity. The endpoint is `dr² + Ĥ`.

One may choose each stage's parameter function constant near its endpoints and join the stages at their common value. This gives a smooth path with no corner in the parameter. The base and parameter interval are compact; positivity, eigenvalue bounds, inverse-metric bounds, and the derivatives needed below are therefore uniform. This argument is valid for each fixed normal metric and needs no global lifting of the path to the original b-manifold.

## 3. Slow invariant concordances and the exponent repair

For a smooth family `q_t` as above, use a smooth function `β:[0,1]→[0,1]`, constant near both endpoints, and put

`K_L = ds² + q_{β(s/L)}` on `R × Y × [0,L]`.

The temporal scalar-curvature formula has the following correction to the slice curvature, writing dots for `s`-derivatives:

`(3/4) tr((q⁻¹ q̇)²) − (1/4)(tr(q⁻¹q̇))² − tr(q⁻¹q̈)`.

Since `q̇ = O(L⁻¹)` and `q̈ = O(L⁻²)`, the correction is uniformly `O(L⁻²)`. Translation invariance in `r` permits this estimate to be checked on the compact quotient `S¹ × Y`. Taking `L` sufficiently large gives a PSC metric with exact temporal products. Thus the normal path produces an invariant PSC concordance.

Now let `d = dim Y`. A b-concordance freezes at a spatial face to a metric `Q` on `R × (Y × I)`. Applying the conformal quotient directly would use exponent `2/d`; individual endpoint metrics instead use `2/(d−1)`. Moreover, direct reduction creates temporal coefficients `f_i^{2/d}ds²`, generally dependent on `y`. Consequently direct reduction alone does not prove that the endpoint construction descends to concordance classes.

The accepted repair is:

1. Normalize each invariant temporal endpoint `q_i` to `dr² + Ĥ_i` using the preceding invariant slow concordance, where `Ĥ_i = f_i^{2/(d−1)}H_i`.
2. Reverse one of these pieces as appropriate and glue both to `Q`. Exact temporal product collars make the gluing smooth and PSC.
3. Apply the quotient identity in dimension `d+1` to this longer invariant concordance. Its temporal endpoints now have `f = 1`, `α = 0`. Hence the quotient collars are exactly `Ĥ_i + ds²`, despite the different interior conformal exponent.

This is a closed PSC concordance between the prescribed endpoint reductions. It proves well-definedness of each end map `E:C_b(R×Y)→C(Y)`.

There is no unit-interval obstruction: a finite interval `[0,L]` can be identified with `[0,1]` by a smooth increasing diffeomorphism that has derivative one in sufficiently small collars of both endpoints. Pulling back preserves scalar curvature and the exact endpoint metrics. A linear rescaling, which would alter those collars, is not required.

## 4. Section, image law, and a genuine obstruction to fixed ends

The product map `j([h]) = [dr²+h]` is well-defined by taking the product of a closed concordance with `R`. At either spatial end it satisfies `Ej = id`. It follows that `j` is injective for the full equivalence relation declared in this b-test case.

The closed theorem of Stolz, as recalled and compared by Xie–Yu–Zeidler, applies to connected closed spin `Y`, `d ≥ 5`, with a chosen PSC reference class. Its free transitive `R^{spin}_{d+1}(Bπ₁Y)` action supplies the based abelian group law. Transport through `j` gives exactly

`j(a) ⋆ j(b) = j(a + b)`

on its image. Representative independence and all group axioms follow from this injective transport. The closed surgery cobordism may be multiplied by `R`; its product PSC metric and temporal collars compactify smoothly in the spatial b-direction. This is a product of the established compact surgery construction, not a general surgery theorem for arbitrary Lie algebroids. [Xie–Yu–Zeidler, introduction and Proposition 4.1](https://arxiv.org/html/1712.03722v3)

The fixed-end obstruction is also valid: if `[h₁] ≠ [h₀]` in `C(Y)`, then `dr²+h₁` cannot be b-concordant to a metric equal to `dr²+h₀` near the selected spatial face, since the end-map values would disagree. The asserted example `Y=S⁷` follows from Xie–Yu–Zeidler Corollary 1.2 with trivial group, `k=2`, `p=0`: its `H₀` summand gives positive rank. No explicit formula for the distinguishing metrics is claimed.

## 5. Fixed-exterior compact-core theorem

The distinct compact-core assertion is accepted with all of these restrictions retained:

- A fixed compact smooth core `W` lies in the ordinary interior.
- The reference metric has a chosen PSC product collar `dr²+h` near `∂W`.
- Both metrics and concordances equal the reference metric, respectively its temporal product, outside `W` and on the common collar germ.
- For the spin torsor formulation, `W` is connected, spin, has dimension at least five, and carries the specified spin and actual fundamental-group classifying data.

Restriction and extension are inverse at metric and concordance levels under these conditions. PSC is local; smooth gluing is ensured by the common germ; completeness survives compact changes. If the category requires uniform PSC, the unchanged reference exterior must already have a uniform positive lower bound.

Rosenberg–Stolz Theorem 5.1 explicitly includes compact manifolds with boundary. Its proof uses relative concordance classes and the side metric `h+dt²`, so this is genuine support for the relative torsor, not an analogy with the closed theorem. No boundary fundamental-group isomorphism hypothesis is inserted. The theorem uses the canonical normal type; in the fixed spin case the relevant group is the spin R-group over the actual `Bπ₁W`. [Rosenberg–Stolz, Theorem 5.1 and proof, PDF pp. 20–24](https://www.math.umd.edu/~jmr/psc.pdf)

If only endpoints have fixed exterior but concordances may vary it, the stated relative classification no longer identifies the equivalence relation. The natural forgetful map is surjective onto the unrestricted classes represented by these endpoints, but no injectivity or group-congruence assertion follows. Neither doubling nor arbitrary hypersurface restriction supplies such an assertion.

## 6. Local deformation facts and their limits

For a fixed smooth Lie algebroid over a compact base, the set of smooth positive-definite metrics whose scalar curvature is strictly positive on the whole base is open in the ordinary `C²` topology. This follows because the Lie scalar curvature is a smooth expression in the metric, inverse metric, fixed algebroid structure functions, and derivatives through order two. Around each such metric there is a sufficiently small convex `C²` neighborhood contained in that set. Straight-line contraction makes this neighborhood contractible.

For a smooth PSC path on the compact base, compactness also gives the uniform estimates needed to turn it into a long PSC concordance on the product algebroid, with temporal product collars. The slow-cylinder estimate above supplies the proof. These facts apply to smooth paths with uniform positivity and bounded parameter derivatives. They do not identify arbitrary concordance with isotopy and do not produce paths between distinct concordance classes.

The local assertions are independently verified here; they must not be used to claim global contractibility or a global group law.

## 7. Claims not established

The following remain blocked by mathematical gaps, not by tool or access failures:

1. A group law on all of `C_b(R×Y)`. The formula `a⋆b=j(E(a)+E(b))` has the proposed unit property only if `jE=id`, which has not been proved.
2. Surjectivity of `j`, triviality of end-map fibers, or classification of their compact/interior information.
3. Independence of the compact-core law from the chosen core, or descent through unrestricted concordances.
4. A general compatible PSC-surgery theorem for arbitrary Lie structures, corners, or noncentral normal algebras.
5. Extension of the end argument to merely pointwise interior PSC without positive boundary limits.
6. A proof that pushing a defect to infinity gives an admissible concordance. Such a limit can fail joint smoothness at the compactification/temporal corner.
7. The original broad OWR research target. The scoped b-retraction and fixed-exterior law are substantial partial statements under explicitly chosen conventions, not a resolution of that target.

## Checks and evidence

- Read the source-recovery report and the complete current cylindrical-end and compact-core manuscripts.
- Independently checked all displayed conformal and normalization coefficients, including the `m=2` case.
- Re-ran the coordinate curvature-check script successfully; separately verified that the full normalization gradient coefficient simplifies to the expression in Section 2. These symbolic checks supplement, rather than replace, the geometric arguments.
- Verified the closed torsor statement and Proposition 4.1 in the primary Xie–Yu–Zeidler article.
- Verified Rosenberg–Stolz Theorem 5.1 and its explicit relative proof.
- Checked Wiemeler Theorem 2.2 and its quotient exponent, and Ebert–Frenck Lemmas 2.4–2.5 for the temporal scalar-curvature calculation. [Wiemeler](https://arxiv.org/abs/1305.2288), [Ebert–Frenck](https://arxiv.org/abs/1807.06311)

No source documents, dataset contents, private source material, or private coordination material are reproduced here.

## Addendum: final five-avenue report

The final *Five avenues for composition of Lie-PSC concordance classes* report was checked separately after the preceding audit. **Avenues 1 and 2 pass; no substantive correction is required.**

### Avenue 1

The temporal scalar formula has the correct coefficients and signs. The equivalent expression `scal(g_t)−|K|²−H²−2∂ₜH` uses the evolving slice metric in both traces. Smooth dependence on the compact base and parameter gives the required uniform bounds; after flattening endpoints, temporal stretching makes every correction `O(L⁻²)`. The product-algebroid structure has no extra mixed bracket terms in a parameter-independent frame. The identity therefore extends from the dense interior to the compact Lie base.

The small convex `C²` neighborhood argument proves local contractibility of the PSC metric space and constancy of its concordance-class projection on that neighborhood. It does not assume global contractibility or concordance implies isotopy. Fixed-germ interpolation is valid because the difference tensors form a vector subspace and each pair has a common smaller fixed collar. Exact temporal product metrics glue smoothly; positivity retains a uniform lower bound; reflection and product cylinders provide symmetry and reflexivity. A collar-preserving reparametrization, rather than linear rescaling, handles the interval convention.

### Avenue 2

Classical codimension-at-least-three PSC surgery is a local construction and can be performed inside a suitably chosen compact interior tube, unchanged outside it. The proposed algebroid extension is legitimate: retain the original algebroid on the complement, use the ordinary tangent algebroid on the changed interior, and identify them on the unchanged open overlap by the original anchor. That anchor is a Lie-algebroid isomorphism on the interior, so it preserves brackets as well as bundles and anchors. These identifications glue a smooth Lie algebroid with the original boundary/corner germ.

The replacement metric is compatible and uniformly PSC because it is positive on the compact modified region and retains the original lower bound outside. Completeness is preserved since escape through any unchanged end still has infinite length. The spin assertion remains conditional on extension across the framed surgery trace. The report correctly makes no claim that integrability, amenability, polynomial growth, or other analytic groupoid hypotheses automatically survive.

### Geometric realization of the product-sector law

The operation is not merely an abstract transported law. Let `V` be the compact four-boundary surgery cobordism realizing the closed based law, with its PSC metric `k` extending the reference and two input metrics and inducing the output metric. On `R×V`, the metric `dr²+k` is PSC and has the required product collars. Compactifying only the `R` direction gives the algebroid `bT(R-bar) ⊕ TV`, where the ordinary finite-distance boundary of `V` remains a regular temporal/bordism boundary. On its four boundary components the metrics are exactly the four product metrics on `R×Y`.

This is a direct geometric realization of the transported law and inherits its representative independence from the closed theorem and product-sector injection. It is a **special product construction**: its surgery loci are generally noncompact products, so it is not an application of Avenue 2's compactly supported surgery theorem. Nor should the algebroid be replaced by the full b-tangent bundle at every boundary face, which would turn the temporal collars into a different category. These distinctions are consistent with the stated concordance convention and should remain explicit in summaries.
