# Elementary Edrei proof-method attempt record

Problem 30005048; queue row 1839; **UNSOLVED**, five avenues. Research date: 2026-10-21.

The infinite PF-infinity classification is known. The unresolved request is for a more straightforward proof, with no precise elementary toolkit specified. This record reconstructs an existing Okounkov-style necessity argument using finite character theory; it does not demonstrate novelty or a simpler proof. No Edrei/Thoma classification is imported as a black box. Substantial finite representation-theoretic, analytic and compactness dependencies remain explicit.

REPORT.md preserves all five avenues: product sufficiency; reciprocal closure, peeling and rational necessity; polynomial-approximation obstructions; finite-character positive weights and quantitative star-transposition collision bound; exact shortcut counterexamples. INDEPENDENT_AUDIT.md is the original mathematical review, not a fresh package verification. SOURCE_GATE.md and SOURCE_METADATA.json preserve public provenance and bounded-search qualifications. Research input hashes distinguish the frozen research from provenance-only sanitization.

## Replay

From this directory, using Python 3 and the standard library:

    python3 verify_package.py
    python3 -O verify_package.py
    python3 controls.py
    python3 -O controls.py

The verifier checks a closed flat inventory, bytes and SHA-256 hashes, then compares every field and JSON type of the exact-example output with EXACT_CHECKS.json. It runs the examples under both normal and optimized Python. Controls refresh the manifest after deliberately corrupting an exact example, proving rejection occurs at the mathematical validator rather than only the integrity gate. Further controls exercise missing, extra, changed and traversing manifest entries, symlinks and unguarded execution. Temporary copies are outside this directory and removed automatically.

Exact examples are finite sanity checks, not a machine proof of the analytic classification or proof-method novelty. The manifest is an integrity inventory, not an authenticated signature. An attacker who replaces both code and manifest is outside its claim. Scripts resolve their own package directory, accept no alternate path argument, and require a main guard. No downloads, network access, source PDFs, extracted source text or dataset contents are required.
