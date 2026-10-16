# Accepted corrected partial packet and independent audit

The general conjecture remains unresolved after five mechanisms. The accepted current report is `../current/REPORT.md`.

The original unqualified floor-slack inequality was false for real lower bounds. `AUDIT.md` gives the exact counterexample, correction, complete proof review and source qualifications. `CORRECTION.patch` records the correction in context: deleted hunks are superseded. The full rejected original is omitted; only its external byte/hash pins are retained.

`check_independent.py` is a separate rational linear-system and affine-dependence geometry implementation. It does not import the supplied checker. Run `python -B check_independent.py --require-readonly` from this directory, and repeat with `-O` and `-OO`, using UID 1000 with this directory and `../current` permission-read-only. Omit the read-only flag for mathematical checks on writable copies. `--output` must name a new file outside both payload directories. `--mutant NAME` deliberately breaks one semantic assertion and must fail.

`AUDIT_PINS.json` pins every other audit file. `ORIGINAL_PINS.json` identifies all eight original files without reproducing source bodies. `SOURCE_VERIFICATION.json` contains public scholarly-source metadata only. The external acceptance receipt pins both manifest files and records actual runs and denied write attempts.

No new proof-search approach, general resolution, global extremum certificate, novelty or best-known result is claimed. No publication was performed by this audit.
