# KP 2 28 independent audit and verifier correction

Mathematical disposition: partial and unresolved after five routes. The original seven-file edition remains unchanged.

- `AUDIT_REPORT.md`: full authored mathematical and executable audit.
- `verify_exact_corrected.py`: optimization-safe original checks, stdout by default.
- `VERIFIER_CORRECTION.patch`: minimal verifier changes against the frozen original.
- `SCOPE_CLARIFICATIONS.patch`: optional Runnels and ambient finite-index wording only.
- `independent_exact_check.py` and `INDEPENDENT_EXACT_RESULTS.json`: independent finite-check implementation and results.
- `run_readonly_audit.py`, `readonly_core_runner.py`, and `EXECUTION_AUDIT.json`: genuine UID 1000 read-only, optimization and mutation reproduction.
- `ORIGINAL_FREEZE_RECHECK.json`, `SOURCE_IDENTITY_RECHECK.json`, and `SOURCE_EXTRACTION_RECHECK.json`: identity evidence without source bodies.
- `AUDIT_MANIFEST.json`: hashes and byte counts of all audit payloads.

Run the corrected verifier from any readable location:

```sh
python3 -B verify_exact_corrected.py
python3 -B -O verify_exact_corrected.py
python3 -B -OO verify_exact_corrected.py --output /tmp/raag-verification.json
```

The first two commands emit complete JSON on stdout and need no writable input/current directory. The last command requires its explicitly selected output destination to be writable.

Run the independent implementation with `python3 -B independent_exact_check.py`. To repeat the full execution audit as genuine UID 1000, run `python3 -B run_readonly_audit.py /absolute/path/to/the/original/public` and capture stdout in a writable destination. It creates and removes temporary read-only specimens; it does not modify the original packet.

This packet contains authored mathematics, authored code, public bibliographic/hash metadata and test outcomes. It contains no third-party source documents or source extracts, private material, or global queue file. It has not been published or committed by this audit.
