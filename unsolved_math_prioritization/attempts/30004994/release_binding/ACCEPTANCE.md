# Safe-public projection: binding acceptance

Target: 30004994 / OWR-9790354-005. Checked 2026-10-04 UTC.

**ACCEPTED.** The reviewed publication projection satisfies the outstanding scope qualification in the independent audit, while preserving the mathematical result and all audited proof/test bytes.

This acceptance binds exactly to:

- RELEASE_MANIFEST.json SHA-256: `b828a79f789a9dc45bc5323758f65db892bfebe3b7534a66738355393944161b`
- Top-level SHA256SUMS SHA-256: `9f8d2d124b55e04bb94cf1254a3a9ad9af33339f82d76760be81c7e738d435f3`
- verification.md SHA-256: `fdc52dcef5f14b22ec347680c581235ee0feb33c1041b315ad5df98f51792b23`

## Checks completed

The release contains exactly 18 regular files, with no symbolic links, hidden additions, binary attachments, or unlisted payloads. Its 16 ordinary manifest entries, plus the manifest and top-level checksum file, account for the complete inventory. Every recorded size and SHA-256 agrees with the actual bytes. Both checksum manifests verify.

The three mathematical files, all eight independent-audit files, and the README are byte-identical to the reviewed originals. The changes to source_map.md and research_log.md remove administrative content without removing any mathematical hypothesis, argument, citation needed for the result, or limit on the conclusion. Changes to result.json are restricted to removing two internal identifiers and recording the completed audit and turn-count metadata. The release note distinguishes the historical audit input from this publication projection and correctly describes the review as an AI audit rather than human peer review.

The public inventory was read and scanned. It contains no source PDF, source-page image, extracted source full text, raw source-corpus record, private coordination snapshot, or redaction ledger. Historical hashes and descriptions of excluded categories do not reproduce their contents. The outstanding instruction to omit the coordination section has now been fulfilled. Its appearance as a historical requirement in the unchanged audit is reconciled by this acceptance.

Both control programs were replayed from the release itself. The author's 191,386 checks produced an exact byte match to controls.json. The independent program's 1,853 checks, also executed with Python optimization enabled, produced an exact byte match to audit/independent_results.json.

## Conclusion and limits

The classification remains `already_solved`: a prior negative resolution of the unrestricted universal equivalence, attributed to Meyerovitch. No new result, finitely generated counterexample, or broader classification is asserted. The exact entropy formula, positive lower bound, and absence of distinct whole-group asymptotic pairs are unchanged.

The release metadata records one substantive research turn out of five, not five completed approaches. This review verifies those metadata values and their consistency with the stated prior-result disposition; it does not independently query or mutate any external research tracker.

No further publication-scope correction is required for these exact bytes. This acceptance does not authorize an external publication or a remote write. Any later byte change requires a new binding check. The frozen originals, original audit, and release were preserved unchanged; this supplemental acceptance was written separately.
