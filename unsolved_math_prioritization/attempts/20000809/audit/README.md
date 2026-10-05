# Independent audit of problem 20000809

Verdict: **PASS_SCOPED_PARTIAL**. The frozen author's mathematical claims pass under their explicit hypotheses. The general projective AIM question remains unresolved here, with five approach families examined.

- `AUDIT_REPORT.md`: full adversarial audit, accepted claims, boundaries, and optional hardening notes
- `independent_verify.py`: independent border-commutator, Macaulay-neighbor, distraction, and interpolation checks
- `independent_verification.json`: deterministic output of 310 assertions and eight rejected false alternatives
- `input_integrity.json`: freeze, dataset hash, canonical fingerprint, and cross-implementation match metadata
- `source_verification.json`: public source metadata and precisely bounded inspection history
- `audit_summary.json`: machine-readable verdict and accepted scope
- `verify_audit.py`: strict inventory, integrity, and deterministic replay verifier
- `MANIFEST.json`: SHA-256 and byte inventory

Run `python3 -B verify_audit.py`. No source PDFs, extracted text, images, raw corpus records, or private coordination files are included. No network access, third-party Python package, or author directory is needed for replay. This is an independent AI audit, not human peer review or formal verification.
