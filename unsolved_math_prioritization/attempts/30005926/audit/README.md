# Independent audit: high-genus triangulation distances

Scoped acceptance of the twelve numbered results in the frozen author report. No mathematical correction is required. The diameter constant and conjectured ratio three remain unresolved; the known typical-distance theorem is credited to Lions.

- `AUDIT_REPORT.md`: full result-by-result reasoning, exact certificate-count proof, conditional-probability argument, and limitations
- `AUDIT_VERDICT.json`: machine-readable scoped verdict
- `AUDIT_SOURCE_VERIFICATION.json`: public-source hashes and inspection/status record
- `checks/independent_checks.py`: separately written standard-library combinatorial-map and probability controls
- `checks/INDEPENDENT_RESULTS.json`: 15,042 passing controls, including 1,500 surgeries with repeated-boundary cases
- `checks/AUTHOR_REPLAY.json`: exact replay of 57,304 author controls, including 12 Decimal diagnostics
- `AUDIT_MANIFEST.json`: sizes and SHA-256 hashes of the distributable audit files

From this directory, run `python checks/independent_checks.py` and `python -O checks/independent_checks.py`. Both output the recorded independent result. A separate optional symbolic diagnostic records the endpoint series; it is not required by the independent verifier.

All author bytes are preserved. There is no correction patch because no claim-changing error was found. This is not human peer review, proof-assistant certification, or a re-proof of the imported papers. No source PDFs, copied source text, dataset contents, or private coordination material are included in the distributable manifest or archive.
