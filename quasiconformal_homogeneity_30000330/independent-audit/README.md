# Independent review of OWR-1106-004

**PASS for partial research; unresolved, five attempts out of five.** No solution or counterexample is claimed.

- `AUDIT.md`: source scope, five independent derivations, precision notes, and limitations.
- `verify_audit.py`: portable standard-library controls, independent of the author's implementation.
- `audit_results.json`: recorded verification output, including 915 exact parameter cases and frozen-file checks.
- `AUDIT_MANIFEST.json`: checksums for this separate audit package.

Run `python3 verify_audit.py`. If the frozen author directory is available as `../public`, run `python3 verify_audit.py --author-dir ../public --replay-author` to verify all frozen hashes before replaying the original script.

The K-only injectivity upper-bound reading is expressly rejected in the audit. The upper bound is surface-dependent. This package leaves the frozen author files unchanged and should accompany any use of their partial conclusions.
