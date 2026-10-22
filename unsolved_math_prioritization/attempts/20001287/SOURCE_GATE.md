# Source, scope, and historical-priority gate

Checked 2026-10-03 for Problem 20001287 / AIM-CONVEX_GEOMETRY-0019.

## Original statement

The official AIM PDF, printed page 4, identifies the question as **23**, attributed to **H. Koenig**. Its spherical dual uses `⟨x,y⟩ ≥ 0`. The product is bounded above, conjecturally in that list, by the positive orthant's product. The text explicitly asserts ambient dimension `n=3`.

The PDF page was downloaded, text-extracted, rendered, and visually inspected. The extracted record's initial “3”, strict “>”, and “6” are respectively the lost leading digit, an incorrect inequality, and the damaged `≤` sign. The original spherical dimension is `n−1` in ambient `R^n`. The symbol denotes a spherical simplex, understood as a convex chamber, not a union of arrangement chambers.

The problem landing page was attempted first but could not be opened by the web reader. The current queue title describes an earlier wedge–orthant partial result. That title does not replace the original universal question. The original source controls this note:

https://aimath.org/WWN/mahlerduality/mahlerduality.pdf

## Literature that closes the mathematical question

1. Fradelizi–Meyer, *Some functional forms of Blaschke–Santaló inequality*, Math. Z. 256 (2007), 379–395, DOI 10.1007/s00209-006-0078-z. **Proposition 1** gives geometric-mean Prékopa–Leindler for unconditional measurable functions and the equality characterization by diagonal rescaling. The proposition, its proof, and its hypotheses were read in the arXiv PDF, page 5, and that page was visually inspected. It does not require log-concavity of the functions being compared. Publication metadata was independently checked against the author-hosted journal-copy search result and the authors' laboratory publication listing. The arXiv submission is dated September 2006; the PDF's incidental typesetting date differs and is not being used as a publication date.
   - https://arxiv.org/abs/math/0609553
   - https://doi.org/10.1007/s00209-006-0078-z
   - https://perso.math.u-pem.fr/fradelizi.matthieu/pdf/SantaloMathZ.pdf

2. Lehec, *Partitions and functional Santaló inequalities*, Arch. Math. 92 (2009), 89–94, DOI 10.1007/s00013-008-3014-0. **Lemma 8** is the positive-orthant logarithmic form, and the **proof of Theorem 9**, page 5 of the inspected arXiv version, explicitly applies it to `A=T R_+^n` and `A*=T^{-T}R_+^n`. Its Gaussian specialization gives precisely this problem's sharp constant. The arXiv record was deposited in 2010 and states the earlier 2009 journal publication.
   - https://arxiv.org/abs/1011.2119
   - https://doi.org/10.1007/s00013-008-3014-0

The author-stage search initially missed this elementary functional-inequality route when restricted to spherical-simplex and conic-intrinsic-volume terms. The independent literature search and the direct logarithmic calculation converged on the same proof. The correct conclusion is therefore a **classical theorem deduction**, not a claimed new solution. No exact historical first attribution of the spherical formulation has been established.

Related modern sources on conic intrinsic volumes, solid-angle calculation, regular spherical simplices, and the 2026 refined log-concavity preprint do not need to be assumed in the proof. In particular, no unrefereed current preprint is an input to the final result.

## Prior-attempt check

The live main-branch queue had rank 510 at queued, 0/5. Repository file, all-state pull-request, and commit searches for the exact ID, code, and spherical-simplex product phrase returned no additional matching attempt. Those search results are not an exhaustive history certificate: the file index did not even surface the known queue row. The known earlier imported attempt was read in full and is genuinely about this same question. It proves only the wedge–orthant family and product lifting, and it missed the classical all-dimensional implication. That work is treated as prior partial material, not rebranded as a new contribution.

The adjacent Kuperberg question, Problem 20001282 / AIM-CONVEX_GEOMETRY-0014, concerns critical volume products within three-dimensional centrally symmetric combinatorial types. It is a different problem and is not evidence of a previous attempt at this spherical-simplex question.

## Review boundaries

- Verify the original `≥` sign, ambient dimension, spherical normalization, and chamber interpretation.
- Check that the dual is `A^{-T}R_+^n`, that its Gram matrix is `(A^TA)^{-1}`, and that the two determinant factors cancel.
- Check both logarithmic Jacobians. They are essential to the Prékopa–Leindler application.
- Equality uses Fradelizi–Meyer Proposition 1 and continuous unconditional extensions, not mere equality at isolated pointwise pairs.
- The full answer is affirmative; the proper literature status is that established results imply it. Historical first explicit resolution is unverified.
- The auxiliary local Hessian is not required for the full result and carries no novelty claim.
- Only authored notes and verification code/results belong to this package. No downloaded source PDF, full-source extract, complete corpus record, or private retrieval material is included.

No branch, commit, pull request, remote write, or queue edit was performed during the author stage.
