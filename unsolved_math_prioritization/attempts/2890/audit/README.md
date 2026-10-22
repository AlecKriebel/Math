# Independent audit of ID 2890 / modern K3 4.14

**Verdict: limited pass with a controlling definitional addendum. Status: unsolved, 5/5 substantive approaches.** No universal cork or universal obstruction has been proved, and no global literature-openness or novelty certificate is issued.

- `AUDIT.md`: complete claim-by-claim mathematical review and limits
- `CONTROLLING_ADDENDUM.md`: exact correction distinguishing unknown extension existence from nonexistence
- `FREEZE_BINDING.json`: every original authored byte count and hash, including the supplied manifest
- `INDEPENDENT_SOURCES.json`: fresh primary-source retrieval fingerprints and bounded inspection record
- `independent_controls.py` and `INDEPENDENT_RESULTS.json`: 22,339 independent exact finite checks, including 13 deliberate-negative controls
- `verify_audit.py` and `VERIFICATION_RESULTS.json`: original freeze checks, replay of all 226,926 author checks, independent replay, and post-execution freeze verification
- `integrity_negative_controls.py` and `INTEGRITY_NEGATIVE_RESULTS.json`: six tampering/missing-file mutations rejected, using temporary copies only
- `AUDIT_STATUS.json`: machine-readable verdict and publication boundary
- `AUDIT_MANIFEST.json` and `SHA256SUMS`: audit artifact binding

With the unmodified author directory beside this directory, run:

    python3 -B verify_audit.py

An alternative author directory may be supplied as the sole argument. The verifier is read-only and does not fetch literature. Its output should reproduce `VERIFICATION_RESULTS.json` exactly. It validates the frozen packet and saved finite diagnostics, not geometric realizability or the deep source theorems.

This audit directory contains authored review, authored code, and public bibliographic/verification metadata only. No source papers, source extracts, images, dataset contents, or private coordination materials are included. No remote writes were performed by the auditor.
