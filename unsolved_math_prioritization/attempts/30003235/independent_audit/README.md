# Independent audit of problem 30003235

Read ACCEPTANCE.md for the decision and FULL_REPORT.md for the complete mathematical review. REQUIRED_PATCH.md records that no mathematical correction is required. The general endpoint remains unsolved.

The audit is separate from and does not modify the 17-file frozen author packet. It is anchored to that packet's manifest digest. Source documents are not included or needed for the control replay.

With Python's standard library, run:

    python run_independent_controls.py --root /path/to/frozen_v1

The runner checks the independent checker in normal, -O and -OO modes, runs 24 negative controls in each, and creates an actually read-only relocated copy in a temporary directory. It writes only temporary files and JSON to stdout. A write-capable root/superuser environment may deliberately fail the effective-write-protection test; that is not a mathematical failure.

INDEPENDENT_CONTROLS.json and AUTHOR_REPLAY.json record the controls actually run. Finite arithmetic is not a substitute for the proofs or credited infinite theorems. The original author's checker was also replayed but is not imported by the independent checker.

AUDIT_MANIFEST.json gives byte counts and hashes for the audit payloads. As with any unsigned manifest, external anchoring of its digest is needed to identify the exact reviewed version.
