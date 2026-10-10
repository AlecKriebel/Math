# KOU 21.114 independent audit

Mathematical proofs and all 11 finite controls pass. The target remains unresolved after five approaches, with no novelty or solution claim.

A provenance correction is required: the equivalent question is already present in the 22 March 2022 preprint *Weakly-top groups*, arXiv:2203.12021v1, Section 3.3, page 5. This is the earliest source identified in the audit, not absolute priority. A small left/right-coset wording correction is also recommended.

The original author freeze is unchanged. A separately named corrected author v2 and full delta still require independent acceptance before publication.

## Contents

- `AUDIT_REPORT.md`: full proof, code, source, and release-boundary review
- `CORRECTIONS.json`: exact required and recommended old/new changes and v2 acceptance gate
- `independent_verifier.py`: fresh permutation-based verifier, with a different lattice algorithm
- `INDEPENDENT_RESULTS.json`: exact independent results; 114 comparisons match
- `SOURCE_AUDIT.json`: public source, dataset, and bounded repository verification metadata
- `AUDIT_STATUS.json`: concise machine-readable verdict and limits
- `verify_audit_manifest.py` and `AUDIT_MANIFEST.json`: safe-package integrity

## Replay

From this directory, with ordinary Python 3 and no third-party packages or network:

    python3 independent_verifier.py --check INDEPENDENT_RESULTS.json
    python3 verify_audit_manifest.py

To compare with a supplied author result file:

    python3 independent_verifier.py --compare-author /path/to/CHECK_RESULTS.json --output /tmp/independent-comparison.json

Do not run Python with `-O`, because the exact checks use assertions. The independent checker does not import author code or access source PDFs/datasets. Its nine exhaustive subgroup lattices contain 578 subgroups; all 21,347,492 associativity triples across 11 constructed groups are checked. Two wreath examples use explicit disqualifying subgroup certificates instead of full lattices.

No remote write was made. Source documents, source extracts, dataset records, raw service responses, and private coordination are not included.
