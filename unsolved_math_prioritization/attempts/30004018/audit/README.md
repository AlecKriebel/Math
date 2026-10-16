# Independent DS/socle acceptance supplement

This source-free supplement independently accepts the unchanged original six-file frozen v2 packet as a correct partial audit. It does not solve the full category-O conjecture. The unresolved inclusion remains A_k ⊆ S_k for k≥2.

- `INDEPENDENT_ACCEPTANCE.md`: complete mathematical reconstruction, category/parity bridge, normalized known inclusion, scope decisions, and current version checks.
- `independent_checks.py`: separately implemented exact finite examples and eight explicit mutation modes; no import of the author checker.
- `verify_frozen.py`: external literal pins for the complete six-file original packet.
- `run_acceptance.py`: read-only original-packet tests and disposable authored-file mutation controls.
- `INDEPENDENT_VERIFICATION.json`: all subprocess stdout/stderr and return codes, actual UID/EUID, read-only denial receipts, complete before/after snapshots, and local PDF byte-identity checks.
- `SOURCE_REVIEW.json`: public source metadata and bounded inspection history.
- `MANIFEST.json`: hashes and sizes for this supplement's files other than itself.

Run `python3 -B run_acceptance.py ORIGINAL_PACKET OUTPUT_JSON [SOURCE_PDF_DIRECTORY]` under actual UID/EUID 1000. Keep the original packet directory mode 0555 and files 0444; the receipt destination must be outside it. The optional source-directory argument verifies locally available PDF bytes without copying or publishing them. Normal, −O and −OO modes are all exercised automatically.

The original author-self-audit labels remain historical facts. The new report is the independent acceptance decision; it does not rewrite those labels. No third-party source files, source text, datasets, or private coordination files belong in this supplement.
