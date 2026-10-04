# Portable independent audit

Read `AUDIT.md` for the verdict, claim-by-claim audit, evidence limits, and exact unresolved target. Read `CORRECTIONS.md` for the minor test-hardening note and checker-development correction.

Inputs are the unchanged eight-file packet bound by `input-verification.json`. Its originating external freeze-manifest SHA-256 is c1af53c8f215aff4236e2490d01a81d2502c82e36e6f9c36c5779b00df6972f4.

Dependencies: Python 3, NumPy, SciPy, SymPy. No network is used by either audit script. From any directory:

    python /path/to/audit/run_audit.py --packet /path/to/eight-file-packet --output /path/to/new-output-directory

The driver verifies every input hash, runs both original scripts without bytecode writes, executes the independent 50-check symbolic/RK4 suite, and writes a replay summary. Output must be outside the frozen packet. The independent suite may also be run alone:

    python /path/to/audit/independent_checks.py --packet /path/to/eight-file-packet --output independent-results.json

Different numerical libraries/platforms may change last digits and JSON equality. Every numerical result is nonvalidated corroboration, not an interval certificate or global exclusion.

`AUDIT_MANIFEST.json` binds the deliverable files and the original input-manifest hash. Its own SHA-256 is stored externally in `AUDIT_MANIFEST.sha256`. No source PDF, third-party full text, dataset contents, or private coordination material is included.
