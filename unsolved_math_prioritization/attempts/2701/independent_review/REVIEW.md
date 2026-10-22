# Independent adversarial review: KP 1.42 Seifert-form diagnostics

## Verdict

**PASS_SCOPED_ALGEBRA_AFTER_CLARIFICATION.** The saturation, rational isometry, sharp denominator and invariant calculations are correct. One requested clarification concerning S-equivalence has been incorporated and verified. No mandatory correction remains. The original geometric question is **unsolved, 2/5**, in both smooth and locally flat topological concordance.

This report covers the final `PARTIAL_RESULT.md` at SHA-256

`99bcb8b993af2ac3fafadadbf6fae854718cb57c6227d1ef19824d9e3b5632d3`.

The initially submitted hash was `da218f708558d35c4ada8c10cbab5ceb2b48657bc7d57a61546ba15613d42ce3`. The revised text now explicitly acknowledges that the different symmetrized cokernels rule out S-equivalence, while preserving the separate, unresolved concordance question. This is an independent AI review, not human peer review or a novelty certification.

## 1. Source and quantifiers

The full [K3 Problem 1.42](https://aimath.org/pastworkshops/kirbylistrep.pdf), printed pp.44–45, was read and the example on p.45 visually inspected. It asks for forms such that **no pair** of knots realizing them can be concordant. It explicitly retains both concordance categories. The two matrices and the printed vectors match the artifact. Finding selected nonconcordant knots with these forms does not establish the universally quantified statement.

I read the relevant definitions, Section 10 and Conjecture 11.1 in the full [Livingston v1](https://arxiv.org/abs/math/0101035v1), and visually inspected its printed p.27. The conjecture number in K3 is transposed. Section 10 proves an existential result: a specially constructed knot with the first form is not concordant to any knot with the second S-equivalence class. The subsequent conjecture asks for the stronger all-realizations statement. The artifact keeps those quantifiers separate.

The current [unversioned arXiv record](https://arxiv.org/abs/math/0101035) is the shortened v3, *Seifert forms and concordance*, published in 2002. It is not an appropriate substitute for the explicitly cited v1 conjecture. The two full source PDFs have the hashes recorded in the author's manifest:

- K3: `ae56518166fe38aaaf555c58614329228afe734e743b111badec4060877fa12f`
- Livingston v1: `a1cb1c769b2067c15132e0555f633407691389254562e90760323d82e2009ecd`

The live primary abstract of [Liu–Wang v3](https://arxiv.org/abs/2605.25309v3), revised 2026-08-26, was also checked. Its title is *S-Equivalence of Band-Twisted Genus One Knots*. It treats a specified band-twist operation and distinguishes certain S-equivalent knots by Jones polynomials. That is neither a proof of the universal nonconcordance question nor a construction of the desired concordant realizations. No audit of its full proof is needed or claimed for this limited exclusion.

## 2. Integral metabolizer and saturation

Set `W=V1 direct-sum(-V2)`, with the author's columns u and v. Both diagonal evaluations and both mixed evaluations vanish. Their rational span is therefore a two-dimensional null plane.

For `w=(u+v)/2`, the change from the ordered basis `(w,v)` to `(u,v)` has matrix

`[[2,0],[-1,1]]`,

whose determinant is 2. Thus the displayed integral lattice has index 2 in the proposed enlargement. The first and fourth coordinates of `(w,v)` give the unimodular minor `[[1,2],[0,1]]`; equivalently the two columns can be completed by the second and third standard basis vectors to a unimodular four-by-four matrix. Consequently their lattice is a primitive rank-two direct summand.

The explicit coefficient recovery `b=x4`, `a=x1-2x4` proves that every integral point of the rational null plane already lies in this lattice. This establishes exact saturation, not merely the presence of one additional integral vector. Since W vanishes on the plane, the saturation is an integral metabolizer under the primitive direct-summand convention. The printed vectors can be used as a rational null-plane basis but are not a primitive integral basis. Correcting the basis does not change the algebraic-concordance conclusion.

## 3. Rational isometry and sharp denominator

The two coordinate projections of the saturated basis are A and B as printed, with determinant 3 each. Their graph matrix is

`Q=[[-1,-2],[2/3,1/3]]`.

Direct symbolic multiplication gives determinant 1 and `Q^T V2 Q=V1`. Its integral graph domain is exactly `2x1+x2=0 mod 3`; its image is exactly the sublattice with first coordinate divisible by 3. The projection-index assertions follow either from these congruences or the determinants.

For any rational isometry P, taking skew-symmetric parts gives `P^T J P=J`. In dimension two, the left side equals `(det P)J`, so det P is 1. If every entry of P were integral at 3, then its reduction would be invertible over F3. Taking symmetric parts modulo 3 would equate an invertible congruence of a rank-one form with the zero form. Rank cannot change under invertible congruence. This proves the unbounded denominator obstruction; enumerating GL2(F3) is only a control of this rank argument.

Every common denominator therefore contains a factor of 3, and the displayed Q attains common denominator 3. The stated sharp minimum is correct. It is an isometry statement for the forms, not a theorem about all knots realizing them.

## 4. S-equivalence clarification and remaining geometric gap

The initially submitted caveat about S-equivalence was too loose in light of the next section's Smith forms. The final artifact now explicitly states that these forms are not S-equivalent. That conclusion is correct and already consistent with Livingston's Theorem 10.6.

For completeness, an elementary integral S-enlargement symmetrizes to a block of the form

`[[S,a,0],[a^T,2z,1],[0,1,0]]`.

Replacing each old basis vector `e_i` by `e_i-a_i e_last` gives the direct sum of S and `[[2z,1],[1,0]]`. The latter block is unimodular. Thus the symmetrized cokernel is unchanged by enlargement, its inverse reduction, and integral congruence. The two computed groups `Z/3 + Z/9` and `Z/27` cannot be related by S-equivalence. The same distinction can also be seen from the different nullities of the symmetrizations modulo 3, since enlargement adds two to both dimension and rank.

However, concordance is not S-equivalence. The double covers of concordant knots are rationally homology cobordant, which does not force their integral first homology groups to be isomorphic. As a useful prior-work check, I independently verified the two metabolizers in Livingston v1 Theorem 10.7 for the difference linking pairing on `Z/9 + Z/3 + Z/27`. Thus these different abelian groups are compatible with a metabolic difference pairing. This is not evidence of a geometric concordance; it explains why the integral group distinction alone cannot establish its absence.

The final artifact consequently retains exactly the right geometric gap: either construct at least one concordant realization pair, or prove that every such pair is nonconcordant. Neither integral noncongruence nor the denominator calculation settles that gap.

## 5. Polynomial and Hermitian invariants

The skew forms have determinant 1. Symbolic calculation gives `det(Vi-tVi^T)=7t^2-13t+7` for both matrices. Their symmetrizations have determinant 27 and Smith invariants `(3,9)` and `(1,27)`.

Because Q is real and invertible, the rational congruence also gives the displayed Hermitian congruence for every unit complex z. Hermitian inertia and nullity are invariant under such congruence, including degenerate parameters such as z=1. Therefore these signatures and nullities agree. This concerns these Hermitian invariants; it does not erase the separately recorded integral group distinction.

## 6. Exact controls and reproduction

The unchanged author verifier was replayed against the final snapshot. All **5,180** assertions pass and the regenerated receipt is byte-identical to the final author receipt:

`adb083e8b6e6c3d67371875c688960e629a066a55a07878acd9e6143237bf7a2`.

The independent SymPy/rational checker passes **2,679** exact assertions. It independently checks a unimodular completion, index-two change, rational fractional-residue saturation controls, the projection lattices, the general two-by-two determinant identity, local ranks, all 48 invertible matrices over F3, symbolic determinant polynomials, Smith forms, an all-parameter Hermitian identity, the general elementary-enlargement congruence, and the prior source's finite linking metabolizers and annihilators. It does not import the author's verifier.

From the review directory:

```sh
python independent_checks.py
(cd author_replay && python verify.py)
```

The independent script requires SymPy. The submitted verifier uses only the standard library. Both read the included frozen snapshot. No finite computation is being used as a geometric concordance computation or as a substitute for the unbounded local-rank proof.

## 7. Disposition

The final clarified package passes in its explicitly algebraic, unresolved scope. No further mathematical correction is required. Preserve **unsolved, 2/5**, both concordance categories, the distinction between integral S-equivalence and geometric concordance, and the absence of a novelty claim.
