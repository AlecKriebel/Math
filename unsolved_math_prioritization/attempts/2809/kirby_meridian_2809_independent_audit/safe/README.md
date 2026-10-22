# Independent audit packet: 2809 / KP-3.11

Verdict: the conditional mathematical results pass; a mandatory literature correction is required before accepting author v2. The original meridian conjecture remains unresolved at 5/5.

- `AUDIT.md`: full proof, hypothesis, source, prior-attempt, and artifact audit
- `REQUIRED_CORRECTIONS.json`: exact correction locations, replacement text, and v2 acceptance gate
- `SOURCE_AUDIT.json`: public provenance metadata and verification limits
- `independent_controls.py`, `INDEPENDENT_RESULTS.json`: independent 10,768-check reconstruction plus 3,399 supplementary checks
- `audit_packet.py`, `PACKET_RESULTS.json`: frozen-author replay, archive validation, and temporary mutations
- `verify_audit.py`, `MANIFEST.json`: mandatory recursive audit-package validation

From any directory, run `python3 path/to/verify_audit.py` and `python3 -O path/to/verify_audit.py`. To repeat the original-author audit, supply its unchanged archive as `python3 path/to/audit_packet.py path/to/KIRBY_MERIDIAN_2809_AUTHOR_SAFE_FREEZE.zip`. Optional `--author-directory path/to/original/safe` also compares live original files. The author archive is not duplicated inside this audit ZIP.

All scripts use the Python standard library. Checks stay active under optimized Python. No source PDFs, source extracts, images, raw datasets, or private coordination records are packaged. All original author files are preserved. This is AI-assisted review, not human peer review or formal certification. Future v2 changes need separate delta acceptance.
