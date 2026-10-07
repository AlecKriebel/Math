# 30005994: general-potential scope remains unsolved

Read `REPORT.md` for the exact source scope, five mathematical approaches, complete proofs of restricted results, and two exact failures of tempting extensions.

The standard quartic-potential case is covered by the September 2026 Ignat–Nguyen preprint. That credit does not resolve the broader convex-potential question inherited from the Oberwolfach setup. No new full solution or actual counterexample is claimed.

- `SOURCE_METADATA.json`: public provenance and source-inspection limits
- `verify_exact.py`: 43 exact mathematical controls, Python 3 + SymPy
- `EXACT_RESULTS.json`: recorded successful output
- `AUTHOR_MANIFEST.json`: frozen payload hashes
- `verify_packet.py`: membership/hash checks and independent normal/optimized replays

Run `python -I -B verify_packet.py` from any working directory. The replay requires SymPy 1.14.0 to reproduce the recorded version field exactly. These checks do not replace analytic review or verify the full cited preprints.

Review status at freeze: awaiting independent review. Publication has not been performed by the author worker.
