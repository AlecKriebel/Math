# Independent audit: AIM Problem 16

**Scoped PASS.** The length-eight signature and projective separator are valid partial progress. The general monomial-signature problem remains unresolved by this work. No mandatory correction was found.

Read `AUDIT_REPORT.md` for the adversarial proof review, source qualifications, exact controls, and optional editorial suggestions. The author freeze was preserved.

## Replay

Run `python3 verify_audit.py` in this directory. It verifies this audit's manifest, independently reruns `code/independent_controls.py`, and compares the result with the saved control output. If the original author directory and ZIP are available, supply `--author-dir PATH --author-zip PATH` to verify their frozen bytes and compare their saved numerical controls.

The independent code uses only the Python standard library. It uses unique lexicographic insertion paths for lower sets, border-basis commutator equations for tangent spaces, exact integer-polynomial multiplication for flat-family controls, and inclusion-exclusion for the projective Hilbert series. It does not import the author's implementation.

`results/input_integrity.json` records the completed independent corpus/record/PDF fingerprint checks. The source bytes and raw corpus records are deliberately absent, so those acquisition-time checks are not rerun by the portable replay. `source_audit.json` distinguishes primary-text inspection, metadata checks, and unresolved access limits.

The finite controls supplement the universal geometric arguments and imported classification; they are not a proof of the general problem.
