# Authored global geometric verification

This document independently checks the global construction in the original candidate. It treats existence of one positive compact-support suspension block as a classical input whose stated compatibility has separately been authenticated in Tsuboi 1981, printed pp. 1–3 and 6. It does not replace that input with a ball plug, torus surgery, or an unspecified flexibility principle.

## 1. Relative interval-bundle trivialization

Let G = Diff∞_c(R), let Σ be a closed connected oriented surface, and let ρ:π₁Σ→G be any homomorphism. Choose a finite generating set. The union K of its generators' supports is compact; generators and inverses fix R outside K. Every word fixes R outside K, so the full image fixes common endpoint collars after compactifying R to (0,1).

The action on the universal cover times I is free and properly discontinuous because it is so on the universal-cover factor. The quotient E is a smooth oriented interval bundle over Σ with flat transition functions. The endpoint collars are canonically products because all transitions there are identity.

For a finite bundle atlas with increasing local fiber coordinates s_i and a base partition of unity λ_i, define τ(e)=Σ_i λ_i(π(e))s_i(e). Terms extend smoothly by zero outside their base chart. For every positive vertical vector v,

    dτ(v)=Σ_i λ_i ds_i(v)>0.

The weights sum to one, τ is 0 and 1 at the two endpoints, and on the common collars all s_i agree with the canonical coordinate. Thus (π,τ):E→Σ×I is a smooth fiberwise bijection, a local diffeomorphism, and has a smooth inverse. It is the given product coordinate on both collars. This proves the relative trivialization rather than presuming the flat connection is globally a product.

## 2. Complete classification needed for the all-leaf test

For u∈I let H_u={g∈π₁Σ:ρ(g)u=u}. A leaf of the suspension is the image of Σ̃×{u}; it is naturally Σ̃/H_u and its projection to Σ is the covering determined by H_u. In particular every leaf projects onto all of Σ, regardless of whether its orbit in I is dense, discrete, recurrent, or accumulates on fixed levels.

This supplies the crucial all-leaf statement: for every p∈Σ, every leaf meets π⁻¹(p). Path lifting cannot escape the fiber interval in finite time because all transition maps act on the entire closed I; more directly the covering description gives the endpoint over any prescribed p.

A compact leaf gives a finite-sheeted cover, hence a finite orbit of u. Every increasing permutation of a finite totally ordered set is the identity. Therefore every point of a finite orbit is fixed by every group element, the orbit has one point, H_u=π₁Σ, and the leaf projects with degree one. In the relative product trivialization it is a graph over Σ, hence isotopic to a fiber. No compact leaf inside a block is a torus when genus(Σ)≥2. Every noncompact leaf is also π₁-injective: its covering projection gives H_u↪π₁Σ.

Boundary collar leaves are full copies of Σ. A leaf from a block interior cannot cross such a leaf to reach a neighboring block: in a product collar, each level is already a complete compact leaf, and uniqueness of foliation plaques forbids crossing it. Gaps and seam neighborhoods are foliated entirely by copies of Σ. This exhausts every leaf after stacking, including limiting and interface leaves.

## 3. Disk fixing and a hyperbolic mapping torus

Penner's original-paper Theorem 3.1, read in the author-uploaded body, applies to two essential multicurves, internally disjoint in each collection, intersecting efficiently, whose union fills the closed surface. A word using every positive twist from the first collection and every negative twist from the second has pseudo-Anosov isotopy class. Take smooth Dehn twists in sufficiently narrow annular neighborhoods. A small disk around a point in the complement of the finite curve union misses every annulus. The smooth representative fixes that disk pointwise. Its disk boundary is inessential in the closed surface, so fixing it does not produce the essential reducing curve excluded by the pseudo-Anosov condition.

Thurston's actual Theorem 0.1 and Proposition 2.6 in math/9801045v1, together with the complete proof in §5, apply to a compact surface bundle with negative Euler characteristic. For a closed Σ_g with g≥2 and pseudo-Anosov monodromy class, the mapping torus has a complete finite-volume hyperbolic structure; compactness makes it closed. The theorem depends on the isotopy class, so it applies to the smooth disk-fixed representative rather than requiring that representative itself to preserve singular measured foliations pointwise.

Fix this diffeomorphism φ and one metric once. Changing the foliation inside Σ×(0,1) changes neither the quotient identification (x,1)∼(φ(x),0), the differentiable manifold, nor its chosen metric. There is no Dehn filling or filling slope, no covering degree, and no parameter-dependent hyperbolization step.

## 4. One common smooth positive transversal

Choose p in the disk fixed pointwise by φ. The curve γ(t)=[p,t] is embedded and smooth at the mapping-torus seam: in the disk the seam map is literally (x,t)↦(x,t−1). Its derivative is the vertical vector V=∂t, which descends globally.

On each transported suspension block, the interval fibers are still the vertical fibers because the trivialization preserves fibers. Hence V is transverse to its foliation. On all gaps, collars, and seam regions V is transverse to the fiber foliation. Every suspension leaf meets the block's vertical interval at p by §2. Every remaining leaf is a surface fiber meeting γ. Consequently this single γ meets every leaf of every finite stacked foliation, in precisely Calegari's Definition 1.1 sense.

There is no need to extend ρ to a representation of π₁(M) respecting the semidirect-product relation with φ: ρ is holonomy within one saturated slab bounded by product leaves, and the seam holonomy is trivial. A foliation's holonomy is defined along leafwise paths; the transverse path γ is not an additional leafwise generator. Requiring φ-equivariance of ρ would be an extra and inapplicable condition.

As a separate consistency check, the fibration exact sequence gives π₁Σ↪π₁M. Since E↪M induces this injection and each leaf in E injects into π₁Σ, all block leaves inject into π₁M. The product leaves do too. Thus no nontrivial leaf loop becomes nullhomotopic in the ambient manifold. This supports the absence of Reeb-component or vanishing-cycle obstructions, although the explicit transversal already proves tautness.

## 5. Smooth gluing and the quantitative quantifiers

For every integer N≥1 choose, for j=1,…,N,

    a_j=(2j−1)/(2N+1),  b_j=2j/(2N+1),  ℓ=1/(2N+1).

The closed blocks are disjoint and all intervening/end gaps have positive length ℓ. Let h_j(x,t)=(x,(t−a_j)/ℓ). For defining forms α(V)=1 and dα=α∧η on the original block, set

    α_j=ℓh_j*α,  η_j=h_j*η.

On an open collar α=ds and η=0, so α_j=dt and η_j=0 there, with equality of all derivatives. These forms therefore glue as ordinary smooth differential forms, not merely continuous plane fields, to dt and zero on the gaps and seam. Moreover α_N(V)=1 globally, so the defining form never vanishes.

Locally write α=ds+Σ A_i(x,s)dx_i. The transported horizontal coefficients are ℓ A_i(x,(t−a_j)/ℓ), with

    ∂t^k(ℓA_i(x,(t−a_j)/ℓ)) = ℓ^(1−k)(∂s^k A_i)(x,(t−a_j)/ℓ).

For each finite N these and every higher derivative are finite and smooth. Bounds need not remain uniform as N→∞, and no infinite accumulation of blocks or limiting foliation is asserted. In fact the α_N can approach dt in C⁰ while second transverse derivatives grow; the ordinary GV invariant has no C⁰ continuity assumption in the question.

Because h_j is orientation preserving,

    ∫block_j η_j∧dη_j = ∫Σ×I η∧dη = a.

The integrand is zero off the blocks. Therefore GV(F_N)=Na on this one fixed M, and its volume V₀ is the same positive finite number for every N. For any proposed finite value B(V₀), taking N>B(V₀)/a contradicts GV(F_N)≤B(V₀); it also contradicts an absolute-value bound. No limit interchange is used.

## 6. Independent holonomy consistency reformulation

Let c_j:I→[a_j,b_j] be affine. For g∈π₁Σ define f_{j,g} to be c_jρ(g)c_j⁻¹ on block j and identity elsewhere. The product collars make it smooth, and supports for different j are disjoint. Thus

    ρ_N(g)=∏_j f_{j,g},   ρ_N(gh)=ρ_N(g)ρ_N(h).

The relation ∏[A_i,B_i]=1 is preserved separately in every factor, and factors commute. This describes the stacked slab as one flat interval suspension and independently checks that inserting several blocks has not broken a surface-group holonomy relation. It is the same mechanism expressed algebraically, not an appeal to a stronger unknown realization theorem.

## 7. Falsification boundaries

Removing identity collars would invalidate the prescribed smooth gluing; allowing merely a germ action would undermine complete path lifting; using decreasing interval maps would invalidate the finite-orbit argument and coorientation; allowing infinitely many blocks at one N would require a new regularity proof; taking a surface of genus one would lose hyperbolic mapping-torus applicability. The actual candidate avoids each defect explicitly. Replacing this by a torus connect sum or a ball plug is unnecessary and would create a different argument requiring separate validation.

This global family found no counterexample and requires no mathematical repair. It does not independently reprove classical Mather–Thurston or hyperbolization. Penner's original theorem and its §3 proof were read as primary full-text body, but the original PDF remained inaccessible (403), and no visual check of Penner's figures is claimed. No historical priority claim is made.
