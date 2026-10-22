# Independent post correction review of Jiang Su perturbation estimates

Problem 30002218 / OWR-12175-007. Review date: 2026-10-06 UTC.

## Decision and exact scope

Accept the frozen corrected derivative at its expressly stated scope. The new retained-factor bound and the strict-parameter repair are mathematically sound. No additional correction to the seven-file patch is required.

This is a new review of the changes, separate from the auditor who prepared them. The reviewed corrected archive is `JIANG_SU_30002218_CORRECTED_SAFE.zip`, 16522 bytes, SHA-256 `932abd7f31010821788cd1079bd99e7d3871ec6a76bcd760a94816297573d894`. The complete first independent report and the actual patch were read, and the new analytic deduction was reconstructed below. This review does not adopt an arithmetic test as a substitute for proof.

The accepted quantitative assertion is:

    A and B are common-unit unital C*-subalgebras of B(H),
    A is Z-stable, and d(A,B) < 1/16000000
      imply d_cb(A,B) < 1/42
      and isomorphism of their scaled Cuntz semigroups.

The ordinary metric is the Hausdorff distance of closed norm unit balls. The complete metric is its supremum over all finite matrix levels. The common unit may be a proper projection of B(H). The zero-algebra case is immediate. No nuclearity or simplicity assumption on A or B is inserted.

The published number 1/6422957 remains a source-attributed assertion; this review does not independently certify it. The original absorption problem remains unresolved in this work, with five completed approaches and their stopping points retained. Nothing here asserts a counterexample to a published conclusion or a novel result.

## The primary parameter discrepancy

The published PTWW paper, printed pages 944 and 945, was inspected both as freshly extracted text and as freshly rendered page images. Its Lemma 4.11 supplies a coefficient 96kα(600k+1). Replacing α by 11γ produces 1056k(600kγ+γ), which is also the coefficient appearing in Lemma 4.12. Proposition 4.13 instead uses 1056(600kγ+γ). The same mismatch is present in the supplied arXiv version. It is not an OCR ambiguity. [PTWW]

The correction retains the larger coefficient when k=5/2. It does not simply invoke the disputed quantitative statement of Proposition 4.13. Its conservative deduction can be obtained from Lemma 4.12, Proposition 4.2, the established D-property of Z-stable algebras, and the local distance argument in CSSW Lemma 4.3. Those ingredients are used as established inputs, rather than claiming to reprove the entire literature behind Lemma 4.12. [PTWW, CSSW]

## Full analytic check of the retained bound

### Common support and nondegeneracy

Let e be the common unit of A and B in B(H). Every element is supported on eH; restricting to eH gives faithful unital representations. This restriction is isometric at every matrix level, so neither ordinary distance nor complete distance changes. Consequently the final applications of PTWW Proposition 4.2 meet its nondegeneracy hypothesis. This reduction would not justify arbitrary different supports, and none is claimed.

Choose γ with d(A,B)<γ<1/16000000. Put k=5/2 and set

    β(γ) = 1056k(600k+1)γ,
    η(γ) = 10γ + 2β(γ) + 13200kγ(1+β(γ)),
    q = 1-2η(γ)-2kγ.

The arithmetic check below establishes the necessary smallness inequalities and q>0. PTWW Corollary 4.9 supplies property D_k for A. In this unital subcase one can also apply Proposition 4.8 directly to the commuting factors A⊗1 and 1⊗Z in A⊗Z and transport the conclusion through the absorption isomorphism.

### Extending an arbitrary representation of B

To prove a global property D for B, it is insufficient to treat its given representation alone. Fix any nondegenerate representation π:B→B(K). Since B is unital, π is unital. Regard B as a unital subalgebra of C=C*(A,B), whose unit is e.

The usual extension-of-representations theorem provides a unital representation ρ:C→B(L), with K a reducing subspace for ρ(B), such that π is the corresponding summand. For completeness, extend π to a unital completely positive map C→B(K) by the operator-system extension theorem, then take a unital Stinespring representation. Because the map is multiplicative on B, for b∈B the identities for b*b and bb* force both Stinespring defects to vanish. Thus ρ(b)V=Vπ(b) and ρ(b*)V=Vπ(b*) for the Stinespring isometry V:K→L. In particular VV* commutes with ρ(B). This proves the reducing-summand assertion without requiring π to extend as a homomorphism on K itself. It is also the extension step invoked in CSSW Theorem 4.4. [CSSW]

Write A₀=ρ(A) and B₀=ρ(B). Both are unital and nondegenerate on L. The quotient map from A onto A₀ preserves property D_k: any nondegenerate representation of A₀ composes with this quotient to give a nondegenerate representation of A with exactly the same image. Its derivation norm and commutant are therefore the same. This verifies the needed permanence directly.

Also d(A₀,B₀)≤d(A,B)<γ. To see the inequality without assuming ρ faithful, lift an element of the unit ball of A₀ through the quotient A→A₀ with norm arbitrarily close to 1, normalize it, and use a contraction of B approximating that lift. Applying the contractive map ρ and then letting the lifting error tend to zero gives the first directed Hausdorff estimate. Interchanging A and B gives the second. There is no extra factor 2 here.

Apply Lemma 4.12 to the actual image distance δ=d(A₀,B₀). For δ>0 its hypotheses follow from δ<γ; the polynomial η is strictly increasing, so

    d(A₀′,B₀′) ≤ η(δ) < η(γ).

If δ=0, the algebras and their commutants agree and the same strict upper bound holds. Thus the local-distance transfer argument really has the required slack.

### Deriving the denominator

Here is the local argument, included to check the factors independently. For x∈B(L), let h=||ad(x)|B₀||. If h=0, x lies in B₀′ and the desired inequality is immediate. Otherwise subtract a best approximant from B₀′ and divide by h. Such an approximant exists because a commutant is ultraweakly closed and its bounded balls are ultraweakly compact. We may thus suppose

    ||ad(x)|B₀||=1 and r=||x||=dist(x,B₀′).

Approximating each contraction of A₀ by a contraction of B₀ within γ gives

    ||ad(x)|A₀|| ≤ 1+2γr.

For any t∈A₀′ with ||x-t||≤r, one has ||t||≤2r. The commutant-distance estimate supplies s∈B₀′ with ||t-s||≤η(γ)||t||, or with an arbitrarily small additional error. Hence

    ||x-t|| ≥ dist(x,B₀′)-||t-s|| ≥ (1-2η(γ))r.

Elements t with ||x-t||>r cannot lower this last bound, so

    (1-2η(γ))r ≤ dist(x,A₀′)
                ≤ k||ad(x)|A₀|| ≤ k+2kγr.

It follows that r≤k/q. Undoing the normalization proves the local distance property LD_{k/q} for B₀. In particular the denominator is 1-2η-2kγ; replacing its last term by kγ is not justified. This reconstructs the operative part of CSSW Lemma 4.3 and avoids its later theorem's printed denominator typo. [CSSW]

### Passing the local bound to π

Identify L=K⊕K⊥ and write ρ(b)=π(b)⊕π₁(b). For T∈B(K), put X=T⊕0. Then

    ||ad(X)|B₀|| = ||ad(T)|π(B)||.

Indeed the commutators are [T,π(b)]⊕0, and the quotient maps onto the two representation images let their unit balls be used without changing the supremum. If S∈B₀′, its compression S₀ to K belongs to π(B)′ and

    ||T-S₀|| ≤ ||X-S||.

Taking infima and using LD_{k/q} for B₀ yields

    dist(T,π(B)′) ≤ (k/q)||ad(T)|π(B)||.

This works for every nondegenerate π, so B has property D_{k/q} in the precise convention of PTWW Definition 4.1. The projection onto K need only belong to the commutant of ρ(B); it need not be central in ρ(B). No centrality assumption is used.

### Complete near inclusions and the unit ball factor

Return to the original common-support representations of A and B. Their ordinary distance supplies near inclusions in both directions, with uniform slack below γ. Proposition 4.2 therefore gives, for every n,

    M_n(A) ⊆_{2kγ} M_n(B),
    M_n(B) ⊆_{2(k/q)γ} M_n(A).

These near inclusions permit unrestricted target elements, unlike the Hausdorff metric. If x is a contraction and ||x-y||≤a, replace y by y/max(1,||y||). The normalization changes y by at most a, and the resulting target contraction is within 2a of x. This is the only factor 2 needed for this conversion; it applies uniformly in n. Since 0<q<1,

    d_cb(A,B) ≤ 2 max(2kγ,2(k/q)γ)
              = 4kγ/q = 10γ/(1-2η(γ)-5γ).

Thus the corrected expression is analytically supported, including its representation quantifier, quotient step, compression, nondegeneracy requirement, and distinction between unrestricted and unit-ball approximation. [PTWW]

## Exact arithmetic and what it establishes

At k=5/2 the retained coefficients are

    β(γ) = 3962640γ,
    η(γ) = 7958290γ + 130767120000γ².

Using √2<3/2, the first smallness coefficient is less than 1344. With M=16000000,

    1344·2200 = 2956800 < M,
    M²-15917005M-261534240000 = 1066385760000 > 0.

The polynomial 15917005γ+261534240000γ² is strictly increasing for γ≥0. Consequently γ<1/M implies

    2η(γ)+425γ < 1,
    q = 1-2η(γ)-5γ > 420γ > 0,
    10γ/q < 1/42.

The earlier smallness hypothesis and q>0 are therefore both established before the analytic estimate is invoked. Finally, choose α strictly between d_cb(A,B) and 1/42 and apply PTWW Theorem 3.10 to obtain the scaled Cuntz-semigroup isomorphism. The theorem's intermediate parameter is available because the complete-distance conclusion is strict. [PTWW]

The printed-parameter remainder 3427616 is also correct, but concerns a smaller β. At γ=1/7000000 the retained expression 2η(γ)+5γ equals 2791940731/1225000000>1. This is a failure of the proof's sufficient estimate inside the larger printed radius, not an example of algebras violating the published conclusion. No optimality conclusion follows.

## Independent check of the central sequence repair

Assume the corrected conditional theorem's hypotheses: A and B are separable, unital, share the unit of C, A is Z-stable, and every contraction of F_A=Q(A)∩A′ has the stipulated approximation in F_B=Q(B)∩B′ at a parameter γ<1/12600000.

The inclusions Q(A),Q(B)→Q(C) are isometric: the quotient norm of a bounded sequence is its limsup norm, which is unchanged by either inclusion. Both relative commutants are unital C*-subalgebras of this ambient algebra. Since M(A)=A, TW Theorem 2.2 gives a unital homomorphism ρ:Z→F_A. It is injective by simplicity of Z. [TW]

Choose γ<γ₁<1/12600000. The pointwise premise implies a non-strict near inclusion ρ(Z)⊆_γF_B, and γ itself is the uniformly smaller witness required for ρ(Z)⊂_{γ₁}F_B. If “within γ” is read merely as an infimum bound without attainment, insert an additional parameter γ₂ with γ<γ₂<γ₁ and use γ₂ as that witness. Either reading gives the required strict uniform relation. This prevents the invalid inference that pointwise strict errors automatically make their supremum strictly smaller than γ.

Faithfully represent Q(C) on a Hilbert space and apply CSSWW Corollary 4.7 to the copy ρ(Z), prescribing the finite set {1}. The result σ:Z→F_B satisfies

    ||σ(1)-1|| < 152√γ₁ < 1,

because 152²=23104<12600000. The projection σ(1) must equal 1: otherwise the nonzero projection 1-σ(1) has norm 1. TW Theorem 2.2 now applies to the separable unital B and proves B≅B⊗Z. The target F_B may be nonseparable; the embedding result does not require target separability. No lifting of σ to coordinate homomorphisms is used. [CSSWW, TW]

The repair is valid without changing the premise or conclusion. The conditional premise still has not been deduced from ordinary closeness. In particular, proximity to Q(B) and proximity to a commutant do not automatically give proximity to F_B.

## The nonunital explanatory paragraph

The first report's explanation of property D_{5/2} for nonunital Z-stable algebras is consistent with the narrower quantitative acceptance. In a nondegenerate representation of A⊗Z, the commuting multiplier images of A and Z can be used after adjoining the unit to the A image. The resulting unital algebra E contains the represented tensor product. Conversely its extra generators are strong limits of tensor-product elements, by an approximate unit of A. Thus E and the represented tensor product have the same von Neumann closure and commutant. Kaplansky density identifies their derivation norms, so the distance estimate for E passes to the original representation. This justifies the property-D discussion without putting 1_A inside a nonunital A.

It does not establish the quantitative near-inclusion comparison for arbitrary nonunital pairs on arbitrary supports. This review retains the correction's common-unit unital restriction.

## Diff review and acceptance limits

The actual patch changes exactly seven files. Exact replay from the frozen original produces the corrected archive entries, and reverse replay recovers the originals. The remaining three approach files are unchanged. The propagation removes the independent-certification overclaim, records the retained-factor conservative radius and its restricted scope, and inserts the central-sequence parameter enlargement. No missing sixth approach or new solution claim is introduced. See `ACTUAL_DIFF_REVIEW.md` and `DIAGNOSTICS.json`.

The correction's compact mathematical audit cites the source proof scheme rather than spelling out every extension and compression step. The full independent reconstruction above supplies those details and supports acceptance of the existing frozen files without another patch. The first auditor's report also identifies these analytic steps explicitly.

This review is deliberately limited to the new corrections and their propagation. It does not rerun corpus identification, repository prior-attempt searches, the survey's current-status search, or every unchanged mathematical route. It does not assert that all earlier verification history was freshly reproduced. The three earlier frozen archives and their manifests remain unchanged. No publication has been performed by this review.

## Public references

- [PTWW] F. Perera, A. Toms, S. White, W. Winter, *The Cuntz semigroup and stability of close C*-algebras*, Analysis & PDE 7 (2014), 929–952. https://eprints.gla.ac.uk/90387/1/90387.pdf ; https://arxiv.org/abs/1210.4533
- [CSSW] E. Christensen, A. M. Sinclair, R. R. Smith, S. A. White, *Perturbations of C*-algebraic invariants*, Geometric and Functional Analysis 20 (2010), 368–397, Lemma 4.3 and Theorem 4.4. https://eprints.gla.ac.uk/25426/1/25426.pdf ; https://arxiv.org/abs/0910.1368
- [CSSWW] E. Christensen, A. M. Sinclair, R. R. Smith, S. A. White, W. Winter, *Perturbations of nuclear C*-algebras*, Acta Mathematica 208 (2012), 93–150, Definition 2.2 and Corollary 4.7. https://arxiv.org/abs/0910.4953 ; https://doi.org/10.1007/s11511-012-0075-5
- [TW] A. S. Toms, W. Winter, *Strongly self-absorbing C*-algebras*, Theorem 2.2. https://arxiv.org/abs/math/0502211
