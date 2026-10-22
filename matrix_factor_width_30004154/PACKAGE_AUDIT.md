# Independent package and harness audit

Date: 21 October 2026. Catalogue row 1834, ID 30004154.

**Verdict: PASS for the reviewed package normalization and verification harness.** This is separate from the restricted mathematical audit in AUDIT.md. Neither review establishes a general solution, novel priority, or complete literature coverage. Final snapshot integrity must be checked against the rebuilt MANIFEST.json and its externally recorded hash.

## Guard normalization and provenance

Compared each packaged exact script against its hash-identified original. After removing the added require helper and converting each require call back to its original assertion, the abstract syntax trees are identical, including all mathematical expressions and surrounding control flow. Counts: 2 guards in verify_exact.py, 13 in verify_low_rank.py, 21 in replay.py, for 36 total. Independently generated unified diffs exactly match GUARD_NORMALIZATION.patch. Original-script stdout in ordinary Python matches the complete packaged expected-output files byte for byte.

Thus the calculations, tested conditions and successful outputs are preserved. Failure behavior intentionally changes from AssertionError to RuntimeError and checks remain active under optimization. This is not a claim of identical exception classes or module introspection metadata: the helper precedes two original module docstrings. Neither distinction affects these executable certificate tests.

Report edits were reviewed separately. They replace local replay/source locations with package-relative commands and public citations, remove coordination wording and an uninspected search hit, and update the prior pending-audit statement to reflect the completed mathematical audit. The mathematical statements, examples and proofs are unchanged. Source/priority limitations remain essential: scalable-frame credit, preview-only access for the latest factor-width-rank paper, and no exhaustive literature or novelty certification.

## Successful replay and negative controls

Independently ran run_checks.py. All three exact scripts pass in ordinary and optimized Python, with empty stderr and complete stdout equality to their frozen transcripts: six successful replay cases. This is stronger than checking a success substring or a process exit alone.

Independently ran test_corruption_controls.py. Its four mathematical mutations change:

1. The author's separating matrix H.
2. A coefficient of the positive rank-two factorization.
3. An entry of the explicit ambient dual certificate.
4. The repeated-row family parameter q.

Each mutated script is written alone into a temporary directory and executed directly. No manifest, inventory gate, expected-output file or package harness is present in that directory. All four mutations fail at an explicit mathematical certificate require check in both ordinary and optimized Python: eight negative certificate cases. Therefore their rejection is not merely a manifest mismatch or missing-file rejection.

Seven separate integrity mutations alter a file byte, remove a file, add a file, alter a manifest hash, alter the manifest total, duplicate a manifest path, or insert parent-directory traversal. All are rejected in both modes: fourteen negative integrity cases. Pristine manifest baselines succeed in both modes. These are representative controls, not a proof against every malicious program rewrite.

## Integrity and disclosure boundaries

The inventory validator checks exact file membership, byte counts, SHA-256 hashes, totals, duplicates, forbidden parent traversal, symlinks, frozen report versions, and provenance links. The manifest is deliberately not self-hashed; an externally recorded manifest hash is required to authenticate a snapshot. A coherently rewritten untrusted manifest and package are outside this integrity mechanism's protection.

The reviewed package contains authored mathematics, verification code, audit reports and public-source verification metadata. It contains no source PDFs, copied source texts, corpus records or private coordination files. Public corpus hashes describe local recovered copies, not a fresh upstream retrieval. Source titles, public URLs and inspection limits do not establish novel mathematical priority.

Finite exact computations verify the displayed certificates and selected family parameters. They do not replace the uniform proofs of the all-k construction, full-spark criterion or rank-two classification. The overall problem remains UNSOLVED after five approaches.

## Reviewed executable hashes

- run_checks.py: 481fba3b824255f7e14a2413abc657bc1c4bd3bd0970b78f4948fc5fbd60c30a
- test_corruption_controls.py: 4bc18e9393696996585f2426dde06eb817c596760b07f8fe6f959d12e73d86a9
- verify_manifest.py: 9bf99186eeeb7139970d524298081bf8850dbadb9626631f32cf8e4bb6867ccd
- verify_exact.py: 66f7ece81a799a912125eb52b6d51d6236d090f3c713257aca5f928460a306f7
- verify_low_rank.py: dab77ab004f710cd407dee45dc593a73ccd16b2444ae7686f76914532bab24df
- replay.py: 6b76cfc12b2ab5d0c8212bd4bfb9f952552e8fa55c1456145fe79cbce5999597

Later executable edits require review of the changed behavior. Report and final manifest additions do not change these tested scripts.
