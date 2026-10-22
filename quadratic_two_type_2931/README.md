# Quadratic 2-types and homotopy classification: audited partial

Problem 2931 / KP-4.55, rank 920. **Unsolved, 5/5 approaches.** The accepted result is a corrected stalled partial. No solution, counterexample, new classification theorem, or novelty claim is made. The mathematical audit is AI-assisted review, not human peer review.

Start with the [accepted proof](corrected/PROOF.md), [research report](corrected/REPORT.md), [mathematical audit](audit/MATHEMATICAL_AUDIT.md), [source audit](audit/SOURCE_AUDIT.json), and [current exact-byte acceptance](audit/EXACT_ACCEPTANCE.md).

## Result and remaining gap

Ordinary homotopy equivalence implies that the fundamental-class images in a common Postnikov 2-stage lie in the same orbit under all self-homotopy equivalences and both signs. This is a necessary condition only. A failed identification alone does not suffice to exclude every equivalence.

Nonzero torsion parameterizing a nonempty realized polarized Poincare-type torsor does not prove multiple ordinary-homotopy orbits. Distinct Poincare types also need manifold realizations before they can refute this manifold classification problem. Neither missing step has been supplied.

The accepted source corrections specify the odd-prime and compatible-form hypotheses in Pavlov, the exact 4-periodic/Sylow conditions, the realized/nonempty torsor setting, and the HKPR theorem location. Bibliographic caveat: the frozen proof's final HKPR reference still retains “Section 1.1”; the correct pointer is the Introduction and Section 2.1, Theorem 2.1, as recorded in its corrected main text and the current audit. The accepted bytes are preserved.

## Preserved artifacts and review provenance

- `original/` preserves all eight original author files. Their historical pending-audit wording is retained.
- `corrected/` is the exact eight-file accepted derivative. [CORRECTIONS.patch](audit/CORRECTIONS.patch) was actually applied to a clean original extraction and reproduced every corrected byte.
- `audit/` is the exact 17-member extraction of `QUADRATIC_TWO_TYPE_2931_UPDATED_INDEPENDENT_AUDIT_SAFE.zip`, with its external manifest and historical receipt at this folder's root. Only this updated audit is the current accepted audit.
- [REVIEW_PROVENANCE_CORRECTION.patch](audit/REVIEW_PROVENANCE_CORRECTION.patch) documents the replacement of inaccurate human-review wording with AI-assisted review. It was replayed against the sealed earlier audit; only the three documented files changed. The earlier audit is not distributed in this publication.

Historical statements that publication or queue editing had not occurred describe the earlier research/audit stage. This draft publication updates only the target queue row's Status and Turns; Findings and all unrelated bytes remain unchanged.

## Reproduction and limits

Use Python 3 and the standard library plus the system `patch` program. Obtain trusted SHA-256 anchors for `PUBLICATION_MANIFEST.json` and `verify_publication.py` from the authenticated commit or publication receipt, and verify the wrapper before running it:

    python3 -I -S -B /path/to/verify_publication.py --expected-manifest TRUSTED_SHA256

The wrapper checks the complete inventory and exact-byte bindings before executing frozen code in an authenticated temporary snapshot. It replays the mathematical correction patch, checks the exact acceptance, and runs all 36 bounded artifact tests. Optimized `-O` and `-OO` execution is intentionally rejected, including by the wrapper; a rejection is an expected artifact-test result, never an optimized mathematical pass. Tests establish byte/schema consistency, not mathematical truth or manifest authenticity against replacement of both artifact and trust anchor.

[Publication checks](PUBLICATION_CHECKS.json) record fresh full hashing of the three corpus inputs, the complete 4,542-byte selected record/report pair, and four cached PDF fingerprints. Those source inputs are excluded here, and the wrapper does not rehash absent source bytes or claim fresh-download identity. Ten source entries, inspection/retrieval limits, and public manuscript status are recorded in the audit. Imported theorem proofs, Gamma and surgery computations were not independently re-proved or rerun. Literature searches do not establish completeness or novelty.

This folder includes only authored mathematical analysis, code, correction patches, audit/acceptance reports, and public verification metadata. It excludes third-party PDFs, source extracts, datasets, screenshots, and private coordination material. The draft is not a release, DOI, merge, or human peer-reviewed result.
