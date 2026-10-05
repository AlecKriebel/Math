# KOU-21.39 independent audit

Verdict: **PASS for scoped partial results; original existence question unresolved, 5/5 approaches.**

Read AUDIT_REPORT.md for the proof review and CORRECTIONS.md for optional clarifications. INDEPENDENT_RESULTS.json is the deterministic full verification output. SOURCE_AUDIT.json records source-inspection scope and public metadata. AUDIT_MANIFEST.json binds this independent payload and identifies the exact frozen author manifest.

## Reproduce

Python 3.10 or newer, standard library only. From this directory, with the author's unmodified payload available elsewhere:

    python -B independent_verify.py --author /path/to/author/safe_output

This performs 2,138,862 independent assertions and a separate byte-exact replay of all 116,329 author assertions. It does not write into the author directory.

For the retained full 2,138,878-assertion output, supply the optional read-only complete inputs:

    python -B independent_verify.py --author /path/to/author/safe_output --source-dir /path/to/source-pdfs --problems /path/to/problems.json --research-results /path/to/research_results.json --catalog /path/to/catalog.json

The source directory should contain primary.pdf, dantas2026.pdf, pseudofinite2025.pdf, and course2026.pdf, with the public hashes recorded in SOURCE_AUDIT.json and INDEPENDENT_RESULTS.json. These external inputs are not part of the publishable audit. No private filesystem location is required by the program.

To check this audit's own manifest:

    python -B verify_audit_manifest.py

Finite tests do not replace the infinite proof review or solve the original problem. No novelty, human peer review, or formal proof-assistant verification is claimed.
