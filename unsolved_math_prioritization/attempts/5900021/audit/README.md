# Equal-pressure foam independent audit

Accepted scope: restricted partial lemmas and route obstructions for problem 5900021. The full global foam target and its two-faced continuation remain unresolved after five approaches.

Read `AUDIT.md`, the corrected `../current/RESULTS.md`, and `CORRECTION.patch`. `SOURCE_VERIFICATION.json` records public source provenance and independently checked hashes. `ORIGINAL_PINS.json` identifies the unchanged original authored inputs.

Reproduce from the full source-free bundle:

- `python -B audit/check_independent.py --require-readonly`
- `python -B -O audit/check_independent.py --require-readonly`
- `python -B -OO audit/check_independent.py --require-readonly`

The payload directories should have mode 0555 and their files mode 0444 for the read-only preflight. The checker's true UID/EUID 1000 requirement applies only when that preflight is requested. Integrity and exact arithmetic still run without it. Reports go to stdout by default; an explicit `--output` must name a new path outside both payload directories.

`--mutant NAME` intentionally alters a tested claim and must exit with rejection. The available names are listed by `--help` and in successful JSON reports. Sixteen mutants are independently exercised in each optimization mode by the acceptance harness. Scope guards are separately identified in the audit and are not computational geometric existence proofs.

The bundle intentionally omits all source PDFs, extracted source text, rendered source pages, private research records, and private work copies. No source is needed to execute the verification checks. No publication or queue mutation is performed.
