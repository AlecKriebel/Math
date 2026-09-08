# Certificate review of v1.0.11

Reviewed commit: `137ffa9f1a340f621651395ad0236cf1bdadb51c`.

**The previous C1 finding is closed. All shipped coefficient tables remain correct.** A separate malformed-scalar/coercion edge is recorded in `SCALAR_RENDERING_NOTE.md`; it is not a failure of the repaired mixed-field case or an error in the published certificate data.

## Verification of the repair

The generator now chooses the coefficient parameter explicitly for each known table (`computation/generate_tables.py:125–129`). Its row reader requires the designated key and rejects the alternate recognized coefficient key (`:69–87`). The exact mode and exposition readers apply equivalent checks through `coefficient_values` and `_coefficient_values`, respectively (`independent_verifier/frontier_verify_mode_certificates.py:25–44`; `frontier_verify_exposition_identities.py:32–51`).

The prior witness is rejected: adding `coefficient_in_U_ascending: ["1"]` to spatial row `[6,1,0]` while retaining `coefficient_in_A_ascending: ["8281/24300"]` raises the intended conflicting-field diagnostic in both mathematical readers and the generator. The reverse case in the homogeneous U table also rejects. The actual no-check regeneration command was run in isolated copies in both directions; it rejects before changing any of the three generated artifacts.

The bounded campaign covers 21 cases and 63 direct reader/generator calls:

- Original valid data and unused descriptive metadata accept. The metadata leaves generated TeX unchanged.
- Different-valued and identical-valued competing recognized fields, a sole wrong parameter field, a missing required field, and swapped variable declarations reject at all three relevant boundaries.
- Wrong coefficient values and reversed coefficient lists reject in both exact mathematical readers. The formatting generator is not misrepresented as a substitute for mathematical equality checking.
- Wrong B bounds and the declared homogeneous coefficient parameter reject in the dedicated mode reader. The aggregate includes that reader; lack of a duplicate metadata check in the exposition reader is not treated as a separate mathematical defect.

All 26 relevant current unpacked implementations and all 12 reader copies in the seven current ZIP bundles are byte-identical to the corrected canonical implementations. Named historical packages are outside this current-release comparison.

Evidence and reproducer: `check_certificate_repair.py`, `REPAIR_RESULTS.json`.

## Shipped coefficient preservation

A restricted-grammar TeX parser using Python exact rational arithmetic, without importing project generation or verification code, checks all four printed tables against their expected coefficient arrays. It uses the table position to select U or A explicitly.

All 218 rows (35, 77, 22 and 84) agree exactly. Both JSON certificates and all 218 rendered expressions are unchanged from v1.0.10. Canonical, portable, arXiv, bioRxiv and journal copies of `certificate_tables.tex` are identical. Three negative controls reject a changed numerator, the wrong parameter letter, and restored ambiguous fraction notation.

Evidence and reproducer: `check_shipped_coefficients.py`, `SHIPPED_COEFFICIENT_RESULTS.json`.

No fresh broad theorem or numerical campaign was needed to establish this local repair. Other review lanes handle builds and current mathematics. No live source, frozen snapshot, release or Git state was changed.
