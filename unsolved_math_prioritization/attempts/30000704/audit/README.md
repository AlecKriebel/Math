# Portable independent audit

Target: 30000704 / OWR-1460-010, rank 660.

Verdict: the intended partial mathematics passes, with required explicit lower-curvature wording in standalone Theorem C. Keep unsolved / exhausted partial, 5/5. No novelty or full-resolution claim is supported.

- AUDIT.md: full adversarial mathematical review and source limitations
- CORRECTIONS.md: required statement clarification, preserving original files
- BINDING.json: exact frozen author manifest and file hashes
- SOURCE_CHECK.json: public retrieval/inspection metadata only
- AUTHOR_CONTROL_REPLAY.json: original 22 checks, reproduced byte-for-byte
- controls/adversarial.py and ADVERSARIAL_RESULTS.json: 27 independent exact stress checks
- SHA256SUMS.json and verify_audit.py: audit inventory and binding validation

Reproduce with Python 3.10+ and SymPy 1.14.0:

    python3 controls/adversarial.py
    python3 verify_audit.py /path/to/original/safe

The first command prints results without changing files. The second verifies this audit's own exact inventory, the original manifest and all original files, and both stored control outputs. It performs no network access. Keep the original safe package unchanged and publish any correction as a separate addendum or an explicitly new version.

The artifact contains authored mathematics and public verification metadata. It excludes all scholarly source files/text, raw datasets, private coordination and credentials. KRR 2007's full text remains uninspected. The primary report's exact disk theorem statement was independently verified. This is a mathematical audit, not a live repository/queue or raw-dataset provenance audit.
