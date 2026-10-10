# Sticky Cantor sets: source-aligned classification

The known classification is: sticky embedded Cantor sets in R^n exist exactly for n >= 4. This packet documents a prior result; it claims no new mathematical discovery.

Read REPORT.md for the exact statement, direct low-dimensional and controlled-isotopy arguments, and declared imported theorems. SOURCE_AUDIT.md distinguishes an inspected primary construction from a theorem known through an inspected scholarly attribution. In particular, Sher's original proof was not retrieved.

Run `python3 -B check_claims.py` for exact finite supporting calculations and payload hash checks. On the frozen read-only copy, run `python3 -B check_claims.py --require-readonly`. Python's `-O` and `-OO` modes are also supported. The read-only option requires UID 1000 and actually attempts a forbidden file creation and write-opens existing payload files. No content is written to any payload file. By default results go to stdout; `--output /an/external/path.json` is available.

PAYLOAD_PINS.json binds every other file by byte count and SHA-256; the external freeze receipt additionally binds the pin file and packaged archive. VERIFICATION.md describes checks and their limits. No external dependencies or network are needed to run the checker.

The packet contains only authored analysis, software, status, and public bibliographic/verification metadata. It contains no scholarly PDFs, copied source text, private dataset bodies, or private coordination files.
