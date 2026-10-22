# EP 642 independent audit packet

The elementary partial results are accepted. The general problem remains partial and stalled after three of five approaches. No full solution, asymptotic improvement, or novelty is claimed.

Read audit_report.md, then the separate acceptance_report.json. author_original contains the eight exact frozen author files. corrected contains the assertion-hardened checker and its unchanged results; validation_hardening.patch records the executable correction. source_verification.json contains public metadata only. No source PDFs or dataset contents are included.

Run `python3 verify_audit.py --expected-manifest-sha256 HASH`, using the MANIFEST.json hash from the separate external manifest. The same command works under `python3 -O`. It checks file closure and hashes, then runs relocated copies and an independent subset-DP cycle oracle. Replay outputs go to temporary directories; preserved originals are not rewritten.

Without the externally supplied hash, the verifier only checks consistency against the local manifest, not an externally anchored identity. The original optimized run is reported for reproducibility but is not accepted as active validation. Finite checks do not prove the open conjecture.

Run `python3 mutation_checks.py` to repeat the negative tests (also works under -O). This optional suite uses the system `patch` utility to reconstruct and compare the derivative. All negative-test edits are confined to temporary copies.
