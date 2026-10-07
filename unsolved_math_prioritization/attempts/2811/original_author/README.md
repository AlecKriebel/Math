# K3 Problem 3.13 surface immersion audit

Problem 2811 / KP-3.13 remains unresolved in this investigation after three substantive approaches. The packet contains elementary conditional lemmas, an obstruction to small perturbative triple removal, and the exact remaining gaps. No novelty or complete-resolution claim is made. Independent audit is pending.

Read PROOF.md for the mathematics, REPORT.md for source scope, APPROACH_LOG.md for the stopping record, and STATUS.json for the machine-readable disposition. VERIFICATION_METADATA.json records public source and input-integrity metadata without source text or dataset records.

## Reproduction

Python 3.10 or later, standard library only; no network or external packages are used.

Run `python3 check_math.py` to reproduce CHECK_RESULTS.json. Run `python3 -O check_math.py` for the optimized-Python control; checks use explicit exceptions and remain active.

The separately delivered external manifest pins the archive and the internal MANIFEST.json. After extracting the archive to a clean directory, run `python3 verify_package.py --manifest-sha256 HASH`, replacing HASH with `internal_manifest_sha256` from the external manifest. The verifier requires this externally pinned hash, rejects unexpected or missing files and symlinks, checks all payload hashes and sizes, and reruns the exact controls. The internal manifest cannot authenticate itself. Optimized Python is supported and preserves all checks.

Finite controls validate the elementary covering-set and slope arithmetic claims on documented finite domains. They do not verify a manifold, a geometric surface, an infinite theorem, or the target conjecture. The continuous and all-size arguments are in PROOF.md.

No source PDF, source extract, inherited dataset record, private coordination record, or repository mutation is included in this author archive. The external manifest is verification metadata and is intentionally outside the ZIP.
