# Independent acceptance package

This package accepts the exact author freeze for KP-3.41 / ID 2839 as stalled partial after five approaches. Start with AUDIT_REPORT.md and ACCEPTANCE.json. The original author ZIP and its external manifest are included unchanged; no source PDF, source text, screenshot, dataset record, or private coordination file is included.

Use Python 3.9 or newer. Before extracting or executing any supplied code, compare the entire audit ZIP byte count and SHA-256 with the independent receipt using a trusted hashing tool. The verifier cannot authenticate its own executable code against malicious replacement. Extract the verified audit ZIP to a new empty directory. Obtain the audit external manifest and its SHA-256 from the independent audit receipt. Run:

    python verify_acceptance.py --root EXTRACTED_DIRECTORY --manifest AUDIT_EXTERNAL_MANIFEST --manifest-sha256 TRUSTED_DIGEST

The verifier checks every audit member, both original input pins, each of the six author members, and the author checker under normal, -O and -OO Python. Run the same command under -O and -OO to replay the audit verifier itself.

Optional input replay uses all three arguments together:

    --catalog CATALOG_JSON --problems PROBLEMS_JSON --reports RESEARCH_RESULTS_JSON

Optional source-byte replay uses:

    --source-dir PDF_DIRECTORY

Expected PDF basenames and pins appear in SOURCE_CHECKS.json. These optional source files are not distributed in the audit. The verifier explicitly distinguishes omitted input replay from successfully verified inputs. A source hash proves identity of supplied bytes, not the truth of a theorem or the source's historical retrieval route.

For separately extracted original author files, also provide --author-root AUTHOR_DIRECTORY.

REPLAY_RESULTS.json contains original-author replay and adversarial controls. The external receipt records final frozen audit-package replay, avoiding a circular requirement that a receipt contain its own final digest. Always treat the independent external-manifest digest as a trust anchor; do not substitute a hash offered only by the same untrusted package being tested.
