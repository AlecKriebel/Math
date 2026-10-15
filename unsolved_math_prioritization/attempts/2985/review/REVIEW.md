# Independent adversarial review: connected non-Weinstein complement

**Verdict: PASS_COMPLETE_COUNTEREXAMPLE.** The frozen construction gives a connected embedded symplectic genus-three surface in a closed connected symplectic four-manifold, with Poincaré dual equal to the integral symplectic class and self-intersection four. Its complement has a connected double cover with nonzero ordinary third homology. Consequently the complement has no two-dimensional CW homotopy model and admits no Weinstein structure, for any symplectic form. No mathematical correction is required.

This independently reviews Kirby Problem 4.109, record 2985, on 30 September 2026 using GPT-6 Astra at xhigh reasoning effort. The exact reviewed `CANDIDATE.md` has SHA-256
`78ab061c9c0c6c16f2e6b249e764001361933782d7381982c733f92cefda3c8f`.
The reviewed bytes are preserved in `author_replay/CANDIDATE.md`. This is an adversarial AI review, not human peer review or a determination of historical priority.

## 1. Original target and prior construction

I read the full original statement and both remarks on printed p.281 of the [K3 problem list](https://math.berkeley.edu/sites/default/files/surv-295-ruberman-watermarked-author-pdf.pdf), including the rendered page. The question concerns the complement of the **given** symplectic surface, whose class is dual to an integer multiple of the symplectic class. It does not impose simple connectivity of the ambient manifold, a sufficiently large degree, or primitivity of the class. The construction satisfies the question with k=1 and also supplies connectedness of both the ambient manifold and the surface. It does not answer the special projective-plane question or the separate existential question about choosing some suitable degree-one representative.

The relevant prior ingredient is [Giroux, Proposition 9, attributed to Auroux](https://arxiv.org/abs/1803.05929v1): disconnected symplectic sections in the four-torus, constructed from two integral orthogonal classes and local smoothing of affine tori. I read the full relevant proof on manuscript pp.8–10. Its broad assertion that unequal translation parameters suffice for disjointness is not needed here; the candidate supplies and checks four specific incompatible affine constraints. The free quotient and connected covering-complement obstruction are evaluated directly below.

## 2. Affine data, orientations and the quotient

The displayed parametrizations of A and B are injective maps of two-tori, and each pulls the standard symplectic form back to du∧dv. Their intersection equations force x₁=0, x₄=1/4 and x₂=x₃ with 2x₂=1/4 modulo one. Thus the two listed points are the complete intersection set, rather than a sample of it. The ordered normal-equation matrix has determinant 2; its normal orientations agree with the stated symplectic orientations. Both local intersections are therefore positive and transverse.

The map τ has square equal to translation by one in x₁, hence has order two on the torus. The half-translation in that coordinate rules out every fixed point, independently of what the other coordinates do. Its linear part preserves dx₁∧dx₂+dx₃∧dx₄ and the symplectic orientation. A′ and B′ are exactly the stated images. Each cross-pair disjointness follows from conflicting values of one common affine function modulo one. These are global exclusions, not deductions from a finite grid.

The two compact nodal unions are disjoint, so a sufficiently small neighborhood U of the first union is disjoint from τU. Local modifications can be confined to U. Once S is constructed, defining S′=τS automatically supplies a compatible second smoothing; there is no fixed-point or equivariant-choice problem to solve inside a common neighborhood.

The action is free and symplectic, so the quotient X is a closed smooth symplectic four-manifold, not an orbifold. The quotient map identifies no two points of S, because any such pair would lie in S∩τS. Thus its restriction to S is a diffeomorphism onto a compact embedded surface Σ, and the full inverse image of Σ is exactly S⊔S′. In particular Σ is connected even though its inverse image has two components.

## 3. Direct audit of the local symplectic smoothing

The affine coordinate change at each node is invertible. In those coordinates, α is the standard positive complex-area form on (z,w), β is Re(dz∧dw), and ω₀=(α+β)/2. The axes are complex curves with the same orientations as the original tori. On zw=ε, β vanishes and α is positive, so the central complex annulus is symplectic for ω₀.

The compactly supported transition is valid as written. To make the argument especially explicit, choose ε>0 real, fix 0<r₀<r₁ inside the coordinate neighborhood, and choose a smooth nonincreasing cutoff χ that is one near r₀ and zero near r₁. The allowed z-side graph can be written

z = r exp(iθ),   w = ρ(r) exp(−iθ),   ρ(r)=εχ(r)/r.

A direct pullback calculation gives

β = 0,   α = (r−ρ(r)ρ′(r)) dr∧dθ.

Since χ≥0 and χ′≤0, one has ρ≥0 and ρ′≤0, so the latter coefficient is strictly positive for r>0. The w-side transition has the same calculation with the variables exchanged. This verifies an allowed choice of the candidate's cutoff even more directly than the general C¹-openness argument; no numerical approximation or unproved smoothing theorem is needed.

Choose ε<r₀². The z-side transition has |z|≥r₀ and |w|<r₀, whereas the w-side transition has the reverse inequalities. The central annulus runs between them with both moduli at most r₀. They are consequently disjoint except for their prescribed matching collars. Since χ is constant near each end, all derivatives match the complex annulus or the original axis. The resulting local surface is smoothly embedded and agrees with the original axes near the neighborhood boundary.

The modification preserves the integral homology class: the difference is a closed two-cycle supported in a ball. It joins the two original tori; resolving the first node connects them and resolving the second adds a handle. Equivalently, deleting four disks from two tori and adding two annuli gives Euler characteristic −4. The resulting surface is connected of genus three. All modifications remain in U, so they introduce no intersection with their translates.

## 4. Integral class, scaling and primitivity

The oriented regular-fiber descriptions correctly give the two summands of α as the Poincaré duals of A and B. Symplectic smoothing preserves their sum. Direct exterior algebra gives

τ*α=β,   α+β=2ω₀,   α²=β²=4 dx₁∧dx₂∧dx₃∧dx₄,   α∧β=0.

Let the descended form be ω̄ and take Ω=2ω̄ as in the candidate. Naturality of the **integral** Poincaré dual under the covering gives p*PD[Σ]=[α+β]. The equality with p*[Ω] is then an equality of real cohomology classes. Transfer makes p* injective over R, so PD[Σ]=[Ω] over R. The integral lift is the already-defined integral class PD[Σ]. No integral injectivity is asserted, and no torsion class is silently cancelled.

There is also a useful independent primitivity check. The invariant torus C={x₃=x₄=0} descends to an embedded torus C̄ in X. Its x₁ period in the quotient is 1/2. Consequently

∫C̄ Ω = (1/2)∫C p*Ω = (1/2)·2 = 1.

Thus the integral lift PD[Σ] cannot be divisible by any integer greater than one. Primitivity is not required by the original question, but the example satisfies it. This does not require identifying the possible torsion in H²(X;Z).

The square calculation also has the correct cover factor:

∫X Ω² = (1/2)∫T⁴ (2ω₀)² = 4.

It agrees with the genus calculation. Restricting the Poincaré dual of Σ to its complement gives zero in real cohomology, so Ω on the complement is exact. The obstruction below is consequently not an accidental failure of this necessary exactness condition or a choice of a bad primitive.

## 5. Connected covering complement and its homology

The complement of a closed embedded real codimension-two submanifold in a connected smooth four-manifold is path connected: a path with prescribed endpoints in the complement can be perturbed relative to those endpoints to be transverse to the submanifold, with empty intersection for dimension reasons. This applies to T⁴ minus S⊔S′. Thus restricting p gives a genuinely **connected** double cover of N=X\Σ.

Choose disjoint disk-bundle neighborhoods and write M for the compact exterior. Radial motion in each punctured normal disk gives a deformation retraction of the open complement onto M. The pair sequence, excision and the oriented Thom isomorphism give

H₄(T⁴;Z) → H₄(T⁴,M;Z) ≅ H₂(S⊔S′;Z) → H₃(M;Z).

The first map is diagonal, sending the ambient orientation class to one copy of each oriented surface fundamental class. Its coefficients are **one**, not the self-intersection numbers: this is restriction of the fundamental class to each relative disk bundle, not the normal Euler-class map. A change of consistent orientation conventions would only change signs and would leave the same free cokernel.

Exactness therefore embeds Z²/⟨(1,1)⟩≅Z in H₃(M;Z). The diagonal is primitive, so this is an actual infinite cyclic subgroup, not merely a rational or torsion class. No assertion about the subsequent map to H₃(T⁴) is needed. The deformation retraction identifies this group with ordinary H₃ of the connected covering complement.

A Weinstein four-manifold has a Morse handle model of index at most two, hence a CW homotopy model of dimension at most two. The index bound is recalled in [Giroux's introduction](https://arxiv.org/abs/1803.05929v1). A connected cover of a CW homotopy model is again such a model of the same dimension. Alternatively, for this finite cover, an exhausting Weinstein Morse function and its structure pull back, preserving properness and indices. Either argument forces the cover's third homology to vanish. The injected Z contradicts that requirement. This obstruction rules out every Weinstein structure on the underlying complement, regardless of symplectic deformation or Liouville primitive.

## 6. Reproducibility, source limitations and recommendation

All three author-manifest hashes matched. The copied verifier reproduced `author_replay/verification.json` byte for byte: **13,236 exact assertions**. I inspected its scope and did not treat its finite grid or derivative samples as proofs of the global topology or smoothing.

The independent standard-library checker imports no author code. It recomputes exterior products using determinants, oriented normal lattices, the complete eighth-lattice affine control, 486 rational polar smoothing samples, the genus and covering factor, the primitive period, and the saturated diagonal cokernel. **All 10,403 assertions pass.** The polar identity and general-position/Thom arguments above establish the general claims; the finite controls supplement them.

Reproduce from this review directory with `python3 independent_checks.py` and `python3 author_replay/verify.py`, comparing stdout with their respective JSON receipts. The copied candidate is required by the author's frozen-hash check. Primary PDFs and rendered pages are excluded from the publication bundle; their hashes and inspected locations are recorded in `source_verification.json`.

Limited current searches also found the [March 2020 discussion of Roux divisors](https://symplectosaurus.wordpress.com/2020/03/06/roux-divisors/), including a connected six-dimensional construction described in a comment attributed to Auroux. That is related prior work, rather than an identified occurrence of this four-dimensional free quotient. The underlying Auroux/Giroux construction and standard topological tools must retain their attribution. Neither this search nor this review establishes historical novelty.

The package is suitable for a **claimed-solved candidate counterexample** to the stated general, prescribed-surface question, with separate AI review passed and human peer review unestablished. The projective-plane case and the existential/effective-degree remarks remain outside its conclusion. Two missing LaTeX spacing backslashes in the frozen coordinate displays are cosmetic only; correcting them would require a narrowly checked new hash, not a mathematical revision. No mathematical gap was found.
