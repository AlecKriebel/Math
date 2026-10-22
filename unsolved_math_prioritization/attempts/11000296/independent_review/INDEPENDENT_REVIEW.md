# Independent source/specialization review: 11000296

**Verdict: PASS_CREDITED_PREPRINT_SPECIALIZATION_WITH_EXPLICIT_DETERMINANT_CONVENTION. Recommended campaign status: already_solved, 0/5.**

This verdict binds the unchanged author FROZEN_MANIFEST.json SHA-256 `f4f1e350b68d07ab99d261a0b4e2e841a76570e1cfc44e84b931764f0d11128c`, SOURCE_AUDIT.md SHA-256 `1775949f1046393d23112d72bb28373012954d074ffc3e90481c0986b10a892f`, and STATUS_CORRECTION.md SHA-256 `4f3c9163f8ef7330e98beca3747c0802ad7e25256d5c061d2443f253d9c778b0`.

The determinant-line reconciliation is an essential part of this review. The verdict does not certify a bare scalar reading of the coproduct display with incompatible bracket normalizations. The invariant construction and the resulting exact specialization are checked below and in CONVENTION_RECONCILIATION.md. No mathematical author-file change is required when that note is retained with the review.

## 1. Exact target and attribution

The rendered [original source](https://www.math.uchicago.edu/~farb/papers/mcgbook.pdf), Chapter20, printed pp.329–330, identifies the second Morita class in H_8(Out(F_6);Q) and asks whether its image under the abelianization-induced map to H_8(GL_6(Z);Q) is nonzero. The 8 is visibly a homological subscript. A neighboring discussion of cohomology does not create a covariant cohomology map. The underlying map factors Aut(F_6) -> Out(F_6) -> GL_6(Z).

[Kupers–Miller–Patzt, arXiv:2609.12951v1](https://arxiv.org/abs/2609.12951v1), Theorem A and Section5.1, addresses exactly this image for k=2 and explicitly recognizes the Bridson–Vogtmann question under another edition's numbering. The submission date is 11 September 2026; the PDF's internal date is 14 September. On 1 October 2026, the [author research page](https://math.ou.edu/~ppatzt/research.html) lists both KMP and the AMP input as preprints. This is a credited recent preprint result. No journal-acceptance, peer-review or community-validation assertion is made.

I did not contribute to the author's original source-correction route. I read the complete KMP proof, inspected AMP's relevant chain maps and Hopf/primitive arguments, and checked both CHKV editions. The elementary convention clarification arose during this independent audit; it does not constitute a new campaign proof-search turn or a claim to a new Morita theorem.

## 2. The exact class and map match

The [published CHKV paper](https://ems.press/journals/cmh/articles/14310), Section5.1/Proposition5.4 and Remark9.5, supplies the original Morita class and its Aut lift. Its earlier author edition numbers these Section4.1/Proposition4.4 and Remark8.5. The assembly sends the top generator of the indicated abelian subgroup to the Morita class, and the based construction projects to the unbased class. The graphical-cocycle discussion identifies this with the original Morita family.

After renaming the free basis, the eight generators are left multiplication of x_i by x_5 and right multiplication of x_i by x_6, for i=1,...,4. At the same moving index left and right multiplication commute; at different indices the operations commute because x_5,x_6 are fixed. The basis changes, torus orientation and any harmless nonzero rational normalization do not change the nonvanishing assertion.

With column vectors and reordered basis (x_5,x_6,x_1,x_2,x_3,x_4), the image is the full subgroup U={[[I_2,B],[0,I_4]]}, B in Mat_(2,4)(Z). Every integer entry is independently realized, so this is Z^8, not an unidentified finite-index sublattice. Applying the theorem with a=2,b=4 avoids the opposite block order displayed elsewhere in KMP. Both ranks are even and unequal; the exceptional congruence for equal blocks imposes no condition here.

Inner automorphisms act trivially on abelianization. Thus nonvanishing of the Aut cycle's image in GL is nonvanishing of the image of the original Out class. No different lift or merely nearby class is substituted.

## 3. Full detection and the convention issue

The source's invariant detection has the correct degrees and coefficients. Rational Bieri–Eckmann duality uses St_n tensor det for even n. The classes t_2,t_4 dual to the ordinary degree-zero units have Steinberg homological degrees 1 and 6. Their product has rank6 and degree7, and its dual has ordinary cohomological degree 15-7=8. The determinant twist is in the dualizing module, not in the target homology question.

The full AMP Hopf statement and top-degree primitiveness give an isolated t_2 tensor t_4 term in the (2,4) coproduct. The swapped term lies in ranks (4,2), so it cannot cancel. The unipotent orientation character det(A)^4 det(C)^(-2) is trivial. Under the invariant restriction/Reeder comparison and fiber integration, the dual degree-eight class restricts to a nonzero top class on U. Its evaluation on [U] is nonzero, up to the allowed overall orientation sign. This is the full needed specialization, not just a check of the preprint's title or abstract.

During the audit I found that the ordinary scalar shuffle sign cannot be applied literally while all apartment brackets are normalized by their own basis wedges: swapping e_2,e_3 in rank6 leaves the twisted input unchanged but reverses the displayed span(e_1,e_2) output. CONVENTION_RECONCILIATION.md preserves that exact witness and explains the natural resolution. Tensor the ordinary coproduct with the canonical determinant-line decomposition. The additional determinant shuffle sign cancels in wedge-normalized brackets; fixed-generator brackets retain the ordinary sign.

The note verifies that this is AMP's invariant coproduct by comparing the standard-subspace component in compatible generators and using equivariance, then identifies its projection with the determinant-twisted Reeder restriction map. Consequently the nonzero (2,4) pairing is unchanged. The review does not silently assume the problematic scalar reading is correct, and does not infer that the theorem fails from that notational reading. The general duality, restriction and Hopf theorems are credited primary inputs, not reproved from scratch here.

## 4. Boundaries and verification

The k=1 case is excluded from the nonzero GL-image conclusion: equal blocks (2,2) give the repeated odd-primitive cancellation, consistent with the stated zero H_4(GL_4(Z);Q). This does not affect k=2. The audit does not address all generalized Morita cycles, generation of rational homology, integral primitivity, torsion, or stabilization images.

All ten author entries and five full source-PDF hashes match. The 15,707-control author output reproduces byte-for-byte. The independent program passes 100,009 exact determinant/permutation, block-matrix, dimension and parity controls. It includes the failing bare-display interpretation and the corrected invariant coefficients. These finite controls do not prove the homological theorems; the written invariant argument supplies the logical comparison.

The author's exact prior-work gate and source provenance are consistent with the record. Source PDFs, extracted text, page images and raw imported records are excluded from the portable review. The manuscript's recent-preprint limitation and this determinant-line convention must remain visible in the final packet. Parent retains publication authorization.
