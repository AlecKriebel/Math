# Independent audit of KOU-21.42 / 2551

**PASS for the credited prior-literature consequence, with imported-theorem boundaries.**

The original 2003 positive-grading proof was unavailable. Its exact needed assertion is independently corroborated by the inspected Dekimpe–Deré paper. The arbitrary-lattice contraction and faithful-tree-action bridge passes independently. No editorial acceptance or novelty is claimed.

- `AUDIT_REPORT.md`: source scope, proof attacks, resolution, limitations
- `EVIDENCE_METADATA.json`: public source/data pins and read-only verification history
- `verify_independent.py`, `INDEPENDENT_RESULTS.json`: 6,567 exact independent controls
- `verify_audit.py`: author freeze, independent replay, optional source/data checks, five mutation controls
- `REPLAY_RESULTS.json`: full replay receipt
- `AUDIT_MANIFEST.json`: the seven other files' hashes and sizes

Standard-library Python replay:

    python3 verify_independent.py
    python3 verify_audit.py --author-dir AUTHOR_DIRECTORY

Optional evidence flags are `--author-zip`, `--source-dir`, `--problems`, `--research-results`, `--catalog`, and `--queue`. The source directory must contain the replay filenames in `EVIDENCE_METADATA.json`. Without optional inputs, the verifier explicitly reports them untested. No network or changes to supplied inputs are required; mutation tests use temporary copies.

All source PDFs, extracts, raw dataset records, and private coordination files are excluded. The author package remains a separate unchanged eight-file freeze.
