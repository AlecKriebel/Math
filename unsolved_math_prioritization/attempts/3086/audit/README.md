# Independent audit: OPG-37327 / UnsolvedMath 3086

Verdict: PASS within the frozen partial-result scope. The original all-n
unit-square covering conjecture remains unresolved in this work.

The central certificate independently refutes the unrestricted local grid bound
in Lemma 2 of arXiv:2609.15876v1. It identifies a proof gap, not a disproof of the
n=4 conclusion. The audit also verifies the supplementary elementary proofs and
public-source identities. No novelty or journal-acceptance claim is made.

Files:
- AUDIT_REPORT.md: findings, independent derivations, source scope and limitations
- CORRECTIONS.md: no blocking correction; required limits on future summaries
- independent_check.py: standalone exact checker, with no author-code imports
- independent_results.json: exact output checked by replay
- provenance.json: public hashes, byte counts, match results and retrieval metadata
- audit_checks.json: audit execution and scope summary
- verify_manifest.py and manifest.json: safe allowlist and integrity checks

Reproduce with Python 3.9 or newer:

    python3 independent_check.py
    python3 -O independent_check.py
    python3 verify_manifest.py

No third-party Python dependencies are required. Original author files are not
modified. This package contains no PDFs, source extracts, images, raw datasets,
private coordination files or private local paths.
