# TF-equivalence independent audit

Problem 30005755, rank 801. Accepted scoped partial results; full target remains unresolved after the five-approach investigation.

AUDIT.md gives the independent mathematical review. CLARIFICATIONS.md records the finite-module convention and publication/preprint numbering crosswalk. SOURCE_CHECKS.json contains public verification metadata only. AUDIT_RESULTS.json is reproduced by audit_checks.py. The author/ directory preserves all ten files from the reviewed author freeze byte for byte.

Run:

    python3 verify_audit_manifest.py
    python3 audit_checks.py --check AUDIT_RESULTS.json
    python3 author/verification.py --check author/expected_results.json
    python3 author/verify_manifest.py

All programs use the Python standard library. Their arithmetic results do not replace the all-module textual proof or its established external theorems. The package contains no PDFs, copied third-party source text, screenshots, raw corpora, private sources, or private coordination material.
