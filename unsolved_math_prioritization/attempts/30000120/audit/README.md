# Independent audit of Chern generators for complete conics

Verdict: PASS_SCOPED_PARTIAL. Problem 30000120 / OWR-744-003 remains unsolved by this work. No mandatory mathematical correction was found. Read AUDIT.md for the full geometric audit and scope, CLARIFICATIONS.md for summary safeguards, and BINDINGS.json for the exact frozen author identity.

This archive contains eight safe files including its manifest. It excludes third-party PDFs/text, source screenshots, raw datasets, and private coordination. The author packet remains separate and unchanged.

From any working directory:

    python3 /path/to/replay_audit.py --expected-manifest AUDIT_MANIFEST_SHA256 --self-test
    python3 -O /path/to/replay_audit.py --expected-manifest AUDIT_MANIFEST_SHA256 --self-test

Both commands must reproduce CHECKS.json byte-for-byte. Supply the externally retained manifest hash. For additional verification against a fresh extraction of the frozen author ZIP, add:

    --author-directory /path/to/extracted-author-files

This checks all author bytes against BINDINGS.json and runs the frozen verifier normally and with -O, including its self-tests. The independent checker uses only Python's standard library, with no network. It does not import author arithmetic code. Nine mathematical false-claim controls are always run; --self-test adds nine integrity mutations. The mathematical proof and current-literature assessment require human-level review; finite tests cannot certify them or solve the general problem.
