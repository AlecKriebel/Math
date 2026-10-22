# Independent audit of Blaschke compactification comparison

Problem 5300014 / AMR-052-0014, rank 794. Audit date: 2026-10-05.

The target remains UNSOLVED after the five recorded approach families. The auxiliary results are accepted with the corrections and scope clarifications below. No genuinely nonmonomial base in degree greater than two has a proved boundary nonextension witness in this packet. This is an independent mathematical and reproducibility audit, not conventional human peer review or a novelty certificate.

Read AUDIT_REPORT.md and CORRECTIONS.md first. ATTEMPTS_AUDITED.json is the operative status record. The historical completion percentages in author/ATTEMPTS.json are unsupported subjective heuristics, are not mathematical measures, and are explicitly withdrawn from audit conclusions and summaries. No completion percentage is endorsed.

The author freeze is preserved without edits in author/ and byte-for-byte in AUTHOR_SAFE_FREEZE.zip. Its original receipt is AUTHOR_FREEZE_RECEIPT.json. Clarifications do not silently rewrite that historical snapshot.

## Replay

Python 3.10 or newer, standard library only. From any directory:

    python /path/to/verify_audit.py --expected-manifest EXTERNALLY_SUPPLIED_AUDIT_MANIFEST_SHA256

Use the audit manifest SHA-256 in the separate audit receipt. Do not obtain a trust anchor by hashing an untrusted manifest itself. The verifier checks the complete file and directory allowlist, all payload hashes, original author archive and extracted bytes, and exact mathematical outputs under normal Python, -O, and -OO. verify_independent_math.py can also be run alone; its output must match INDEPENDENT_MATH_RESULTS.json exactly.

verify_integrity_controls.py exercises negative controls in temporary copies. Optional source replay uses author/verify_source_inputs.py with separately held public corpora and PDFs, as described in the author README. SOURCE_AUDIT.json records independently recomputed identities and bounded inspection results; no third-party source bytes are supplied.

## Included and excluded material

Included: authored mathematical arguments, audit corrections, executable regression and integrity controls, results, file manifests, and public verification metadata. Excluded: scholarly PDFs, extracted third-party text, page images, raw dataset contents, raw source records, and private coordination material. No remote write or external publication was performed by this audit.

Finite controls check identities and transcription. They do not certify the universal analytic proofs, the full proof of a cited external theorem, or the original problem.
