# Independent audit of 30006336

Verdict: **pass as an unresolved checkpoint; not a solution**. Keep the
prior-announcement hold and the exact separated-prismatic target.

- `AUDIT_REPORT.md`: mathematical and source audit
- `CORRECTIONS.md`: no mandatory corrections; optional precision improvements
- `AUDIT_STATUS.json`: machine-readable disposition
- `AUTHOR_BINDING.json`: all 12 original author files, exact sizes and hashes
- `SOURCE_CHECKS.json`: primary-source URLs, fresh PDF fingerprints and scope
- `independent_controls.py`, `INDEPENDENT_RESULTS.json`: 655 finite controls
- `REPLAY_RESULTS.json`: both original verifier runs and the independent run
- `verify_audit.py`: exact binding and reproducible replays
- `AUDIT_SHA256SUMS.json`: hashes of the other audit files

With `audit/` and the original `author/` as sibling directories, run:

    python3 audit/verify_audit.py

For another layout, supply the original packet directory explicitly:

    python3 verify_audit.py --author /path/to/original/author

No third-party packages, network or downloaded source files are needed. Original
source PDFs are research inputs, excluded from this portable audit. Publish only
this audit's listed files alongside the unchanged author packet; do not copy
surrounding research directories. No source full text or catalogue corpus is
redistributed. These programs do not mechanically prove the geometric theorem.

Substantial AI assistance. This review is not expert peer review.
