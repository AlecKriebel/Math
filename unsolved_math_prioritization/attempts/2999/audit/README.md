# ID 2999 independent formulation audit

Start with AUDIT_REPORT.md and EXACT_ACCEPTANCE.json. The accepted result is a counterexample to the weak formulation printed in K3; Kronheimer's globally closed-form question remains unresolved by this work. Queue disposition: unsolved, 2/5. No novelty claim.

The original author ZIP and manifest are preserved. The corrected derivative changes only three missing scope guards in check.py; its mathematical proof and other eight authored files are identical. CHECKER_SCOPE_HARDENING.patch is an actual applicable patch. Retained author logs, including the pending-audit field, remain historical. The independent report and exact acceptance record supply the new disposition.

## Verify the corrected derivative

Using trusted pins from the independently delivered receipt:

    python -I -O verify_release.py --archive TAUT_LEAF_GENUS_2999_CORRECTED_SAFE.zip --manifest TAUT_LEAF_GENUS_2999_CORRECTED_EXTERNAL_MANIFEST.json --expected-archive-sha256 00a3f03d3febfb7dc7df0799c50387f6de7d6c57caeec6b3ebeb5f67c1b2e352 --expected-manifest-sha256 829f0d5f4ea9f525a9efaa7bb21afdf4d1db32274ee48c59205bb3c046172d08

The same verifier works on the original and on this audit ZIP with their own external manifests and trusted pins. Verify before extracting. It extracts nothing itself.

## Replay mathematical identities

After extracting the corrected derivative, from any working directory:

    python -I /path/to/taut_leaf_genus_2999/check.py --self-test
    python -I -O /path/to/taut_leaf_genus_2999/check.py --self-test
    python -I /path/to/independent_algebra_check.py
    python -I -O /path/to/independent_algebra_check.py

The author checker uses only the standard library. To verify the full authorized corpus, add all three arguments --catalog PATH --problems PATH --reports PATH. Outputs contain hashes and match results only. Structural controls intentionally used local synthetic fixtures, kept out of this package.

## Contents and boundaries

- AUDIT_REPORT.md: complete independent proof/source/artifact review
- EXACT_ACCEPTANCE.json: exact accepted and excluded claims, disposition, and derivative pins
- CHECKER_SCOPE_HARDENING.patch and PATCH_VALIDATION.json: narrow repair and exact application check
- SOURCE_VERIFICATION.json and CORPUS_VERIFICATION.json: public verification metadata
- Replay/control JSON files: positive and adversarial test results
- independent_algebra_check.py: separate exact tensor calculation
- verify_release.py: archive and manifest integrity verifier
- Original and corrected ZIPs and external records

No third-party PDFs, extracted source text, screenshots, dataset records/contents, private sources, personal data, or private coordination material are included. Source documents were inspected privately and are linked by public URLs. No GitHub writes were performed.
