# 30004601: a reviewed seven-hyperplane degree-bound counterexample

**Result:** independent adversarial AI review passed the complete counterexample to the original corrected x2 conjecture. This is unrefereed; historical priority, novelty, and minimality are not certified.

For the essential central arrangement in characteristic zero

    Q = x y (x-y) (x-2y) z w (x+z+w),

the degree-reverse-lexicographic generic initial ideal of its Jacobian has a minimal generator of degree 7 involving the third variable, while the least pure power of the second variable has degree 8. Genericity is established algebraically by counting all linear polar syzygies on generic sections and applying binary Hilbert-Burch. Exact rational matrices and independent rank certificates corroborate the proof.

## Read first

1. CANDIDATE_PROOF.md: complete frozen proof, SHA256 f31cc44405f91c91af044f7d6a8306faa38c9221ad8a23c639d80bba251e4ef9
2. independent_review/INDEPENDENT_REVIEW.md: full separate PASS, no mathematical correction required
3. SOURCE_AUDIT.md and SOURCE_METADATA_ADDENDUM.md: source wording, known results, and verified citation metadata
4. REVIEW_STATUS.json: final scope and exact reviewed hashes

The candidate's original pending-review header and early research log are retained as frozen historical artifacts. The final review and this README record the subsequent PASS without silently rewriting the reviewed proof.

## Source boundaries

The official source threshold uses the **second** variable. The imported first-variable threshold was a transcription error and is not counted as a mathematical discovery. The published three-variable arrangement theorem is credited. This example is four-dimensional: a three-variable section of its ambient Jacobian has four independent polar generators and must not be replaced by the three-generated Jacobian of the restricted plane arrangement.

## Reproduce

Author check, using the installed SymPy 1.14.0 package:

    python3 candidate_rank_check.py
    python3 adversarial_controls.py

Independent checker, Python standard library only:

    python3 independent_review/independent_rank_certificate.py

The independent certificates include each exact Macaulay matrix, an invertible rational transformation E with E*M=R, RREF R, and a nonzero original-matrix minor. All author and independent outputs were rerun byte-for-byte after review. Three additional rational flags, a rejected nongeneric flag, the restricted-arrangement Jacobian, and a six-plane boundary control were checked separately; none is substituted for the algebraic genericity proof.

## Research provenance

This resumes an interrupted effort. Historical author-turn usage remains unknown and nonzero; it is not reset. One documented recovered substantive author turn produced the complete candidate, then proof search stopped for independent review. Review and source recovery are not counted as additional proof-search turns. See turns.json and the preserved research log.

No source code from external research repositories was executed. Classical generic-initial, sectional-matrix, and Hilbert-Burch inputs are credited. Full downloaded source PDFs, extracted article text, and source-page images are excluded from this research package.
