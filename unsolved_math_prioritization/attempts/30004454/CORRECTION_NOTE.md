# Portable publication context

The complete original authored addendum follows this preamble unchanged. Its original-file preservation, 115 executions across five modes, 12 optimized original-checker false PASS results, source retrievals and original-layout links describe the earlier audit. The assertion-only original checker, original status/README, historical harness, original outputs and full legacy packet are excluded here. Their portable replay is NOT_RUN. This delivery freshly runs only the accepted hardened checker, independent checker and current semantic controls in normal, -O and -OO modes. Source-body replay and a new source search were not performed during packaging. The five mathematical proof files and source audit remain byte-for-byte unchanged. Current layout and noncircular verification are documented in README.md and VERIFICATION.md.

---

# Original-preserving verification correction

The five mathematical arguments are accepted without a theorem correction. A checker's PASS must nevertheless depend on checks that actually execute.

The original `verify_calculations.py` contains 11 Python assert statements and prints PASS unconditionally after its two test functions return. Python -O/-OO and PYTHONOPTIMIZE=1/2 remove all of those assert statements. Three genuine corruptions (a reflection coefficient, triangle divisor, and initial vector) therefore produce 12 optimized false PASS results across the four optimized modes.

`verify_calculations_hardened.py` mechanically replaces each original assert by an explicit `require` call whose false branch raises RuntimeError. It preserves the same arithmetic predicates and test ranges. No original file is edited. All three corruptions now fail in all five modes.

`independent_verify.py` additionally supplies independent exact tests of the relevant calculations and boundary conditions. `run_readonly_audit.py` reproduces the optimized, unoptimized, UID/EUID, mutation, and denied-write checks, requiring a new output directory on each run. See `test_results.json` and `INDEPENDENT_MATHEMATICAL_AUDIT.md` for results and limitations.

This correction affects verification reliability. It neither solves the full target nor adds a sixth substantive mathematical approach.
