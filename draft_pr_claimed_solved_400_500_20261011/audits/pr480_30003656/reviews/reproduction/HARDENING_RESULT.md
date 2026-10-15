# PR480 checker hardening addendum

Completed 2026-10-12T03:48:41.934775Z (2026-10-11, America/Los_Angeles).
Completion estimate: 100% of the separately requested runtime repair.

The independent finite-code verdict was recorded before this repair in
`INDEPENDENT_VERDICT.md`. This addendum fixes its one runtime weakness in a
**separate derived copy**. The frozen author snapshot remains byte-for-byte
unchanged.

The repaired program is `hardened/check_exact.py`. All nine original `assert`
statements are replaced by calls to an explicit `check` helper, which raises
`AssertionError` on failure even under Python `-O`. Conditions are evaluated at
the same points and in the same order. The formula definitions, arrow
enumeration, quotient algorithm, output schema, and successful-result values
are unchanged. The patch is `hardened_check_exact.patch`.

Both normal and optimized honest runs exit zero and reproduce the original
`exact_results.json` byte-for-byte, including cache counts 57 and 85. Both
outputs have SHA-256
`4e33a0884d0de172397e4a5693316508767e14eae1bf7041dd865be562277831`.

Actual copies were mutated in two ways and run in both modes:

| Mutation | Normal result | Optimized result |
| --- | --- | --- |
| Replace both categories by discrete identity-only categories | Rejected at original check line 62 | Rejected at original check line 62 |
| Replace the equality closure by an all-true relation | Rejected at original check line 95 | Rejected at original check line 95 |

All four failures are explicit `AssertionError`s, and none writes a successful
result artifact. Together with the seven mechanism controls on the pre-existing
audit program, the repaired finite verification programs have no unresolved
failure-detection finding from this audit.

`hardening_receipt.json` records commands, interpreter, run times, file hashes,
replaced original line numbers, successful-output equality, failure labels,
and all before/after frozen-source manifest checks. The derivation and tests
can be repeated with `python3 -B harden_and_test.py` from this review directory.

Derived program SHA-256:
`67d74b3901774bece28400c43a47296c154b71e261de3c9fca3f69c10e4d8ae7`.
Patch SHA-256:
`1517d3a65608cd34a2c3cef53e789606832cc17f41ef1a68aa544add97000c10`.
Original program SHA-256:
`9e8d6c12771302a9bc99cb567c373c3bdf470978a6b87e07081712ede454365c`.

If adopted for a publication package, record the derived program's hash in
that package's manifest and retain the frozen-author provenance separately.
The finite scope disclaimers remain necessary: this repair certifies execution
of finite checks, not the unbounded theorem, novelty, or resolution of the
specific historical open problem. This reviewer recommends the derived copy
for supporting verification if the independent mathematical and priority gates
also pass.

The `mutations` folders intentionally contain invalid verification programs.
They are adversarial test fixtures, not result-bearing publication source.
