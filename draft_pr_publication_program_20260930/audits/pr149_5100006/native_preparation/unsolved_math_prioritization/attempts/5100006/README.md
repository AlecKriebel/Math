# 5100006 / k114: exact least-period focal-product criterion

Private native-preparation candidate, 11 October 2026. This folder is prepared for possible later integration; it is not a whole-package R1 acceptance, native merge, publication or Zenodo deposit. ROOT reports that package R1 passed after a reference-text repair; fresh R2 review remains active. This preparation creates no acceptance gate. Publication reference: *An exact period criterion for focal-distance products in elliptic billiards*, pending final review.

PROOF.md gives the full analytic theorem: for a noncircular ellipse with a strictly nested nondegenerate confocal elliptical caustic, either ordinary vertex-to-fixed-focus product is constant exactly when the **least period n is 2 modulo 4**. It covers every primitive star winding and both orientations. Both focal products agree at every phase for every even n. Repetition raises the positive primitive product to an integer power and preserves its constancy status. A circle has product a^N directly. Hyperbolic and degenerate caustics are excluded.

The source/database statement is historical. Its k114 row recorded an unproved observation, without explicitly resolving least period versus an unrestricted return length N. The least-period interpretation is proved; the unrestricted N=2 modulo 4 interpretation is classified and partly false. The exact doubled-triangle six-event products differ by 180√30. SOURCE_RESOLUTION.md explains the distinction and the bounded priority assessment. No new-method or exclusive first-priority claim is made; a related 2023 Dragović–Gajić paper has uninspected full-text sections.

Run the current finite exact controls with Python 3.10 or newer:

    python3 verify.py

The checker is byte-identical to publication_package_v1/verification/verify_exact.py, uses only the standard library and prints JSON without writes or network access. It uses explicit exceptions, so its checks remain active under Python -O. verification.json is its actual replayed output: 21,508 exact checks, least periods 3–101, both foci, 1,053 odd / 255 two-mod-four / 263 zero-mod-four primitive rotations, repeats 2/3/4, the doubled-triangle example and a physical four-period control. Finite exact checks support the written proof; they do not prove its analytic inputs or all-period conclusion.

The retained files source_record.json, prior_imported_report.json and source_manifest.json describe the historical intake, source status and submitted primitive theorem. All eight files under independent_review/ are retained unchanged historical controls and reviews for that valid **primitive n=2 modulo 4 theorem**. Their verdicts have not been expanded to the strengthened theorem.

For old proof hashes, receipts and counts, the authoritative immutable intake is the repository path:

    draft_pr_publication_program_20260930/audits/pr149_5100006/original_submission/files/unsolved_math_prioritization/attempts/5100006

Its PROOF.md hash is f70821b0d44e96f6be9427f906cecc5d1aff8bbd7ab09a71ddec9d75d31ef2d5. The historical submitted/author-replay receipt records 29,397 exact assertions and 210 numerical diagnostics; the historical independent receipt records 5,198 exact controls. These are **not** current verification.json counts or hashes of the new PROOF.md. If replaying historical code, use a scratch copy of the archive; its author verifier requires SymPy and mpmath and writes a receipt.

RESEARCH_LOG.md preserves the earlier entries and appends dated private-preparation checkpoints. SHA256SUMS covers every current file in this candidate except itself, including the unchanged historical files. Extensive AI assistance does not constitute conventional human peer review; the work is unrefereed.
