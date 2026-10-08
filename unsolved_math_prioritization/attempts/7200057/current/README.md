# Crossing minimizers and halving lines

The report gives partial theorems and exact witnesses; it does not settle the general conjecture.

- `REPORT.md`: normalized target, five mechanisms, proofs, explicit gaps and public citations.
- `check_claims.py`: standard-library exact verifier with optimization-resistant guards.
- `SOURCE_AUDIT.md` and `SOURCE_MANIFEST.json`: inspected versions, public-source hashes and retrieval limits. Source bodies are excluded.
- `STATUS.json`: bounded investigation status.
- `VERIFICATION.md`: test scope and read-only verification contract.
- `PAYLOAD_PINS.json`: byte counts and SHA-256 hashes for all other files.

Run `python -B check_claims.py`. For a read-only packet under UID 1000, run `python -B check_claims.py --require-readonly`, and repeat with `-O` and `-OO`. Output defaults to stdout; `--output` accepts only a destination outside this packet. No network access, external packages, or source files are required.

This is the accepted current derivative after independent audit. The simple quantitative floor bound now states its integral-lower-bound hypothesis, and the report also supplies the valid real-bound form. The separate contextual correction patch labels removed hunks as superseded; the original report is not the accepted current version.
