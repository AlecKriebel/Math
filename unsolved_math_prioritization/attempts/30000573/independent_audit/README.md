# Independent audit package

Problem 30000573, rank 813. Decision: accept the scoped partial results; the original problem remains unsolved after five approaches.

- `AUDIT_REPORT.md`: mathematical review, source qualifications, reproducibility results, and limits.
- `ACCEPTANCE.json`: machine-readable decision and scope.
- `PUBLIC_VERIFICATION.json`: public dataset hashes and source verification metadata only.
- `AUDIT_CHECKS.json`: deterministic independent replay and mutation results.
- `audit_checks.py`: standard-library-only reproduction of the integrity, replay, and mutation checks.
- `MANIFEST.json`: audit-member byte counts and SHA-256 hashes.

To reproduce, keep the public-safe author ZIP outside this audit directory and run:

    python3 -B audit_checks.py --author-zip /path/to/CHAOTIC_NUCLEAR_30000573_AUTHOR_PUBLIC_SAFE.zip

Repeat with `python3 -O -B` to check the independent auditor under optimized Python. Both commands should produce JSON matching `AUDIT_CHECKS.json` exactly. The script itself also invokes the author verifier in normal and optimized modes, in original and relocated temporary directories. It checks 36 negative controls and two expected-pass scope diagnostics.

The public-safe author ZIP is externally pinned within the script; an unexpected ZIP is rejected before any archive member is executed. All mutation work is performed in temporary directories. No private source documents or corpus files are required to reproduce these computational checks.

Validate this audit's own manifest against the external audit receipt before trusting its files. Mathematical acceptance rests on the separate written arguments, not on a passing replay or a file hash.
