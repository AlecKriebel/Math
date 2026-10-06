# PR305 publication operations independent adversarial review criteria

Frozen UTC: 2026-10-05T01:28:24.245655+00:00

This review examines operational preparation only. It confers no publication authority and does not adjudicate the mathematical result. The current clearance, operational clearance, final write lease, and release verification are intentionally absent. Frozen shared state and held sets must not be mutated.

Success criteria fixed before source inspection:
1. All five operator source sizes and SHA256 values and all four submission/frozen inputs match the specified review targets. Operator gate calls bind exact source identities, modes, package, metadata, and prospective independently created clearance fields. Missing, expired, mismatched, malformed, or self-issued clearance must fail closed before external writes.
2. A fresh cooperative OS lock, tightly bounded write window, independently approved actual origin and fixed mode constrain mutations. URL validation and rewriting cannot leak secrets or create out-of-scope writes; no source/input or policy mutation can manufacture authority.
3. Production Zenodo kit execution uploads exactly the reviewed metadata and two reviewed byte sequences, requires exact record confirmation for publication, and avoids retries after an ambiguous write. Command construction, cwd, timeouts, partial outcomes, and recovery must be explicit and bounded.
4. Public verification independently checks the anonymous record, all file bytes, DOI identity, and the exact public deposit/record identity. Unknown or unverified state cannot authorize tracker append.
5. Google Workspace preparation targets the actual spreadsheet and GID 1254632077 / Math Puzzles, performs full 43-column FORMULA-mode duplicate and header verification, writes one RAW four-cell row, checks the entire post-write sheet and preexisting rows, and never contacts any individual. Failure and ambiguity behavior must preserve truthful state.
6. Isolated stdlib inspection and mocks may verify material edge cases, but must never invoke real service writes. Tests preserve exact native argv, cwd, start/end UTC, exit status, full stdout/stderr, and tested source hashes. Fixtures do not falsely represent actual clearance.
7. Final report separates mandatory correctness issues from optional hardening, states assumptions and exact gaps, inventories every reviewed input and produced output with hashes, and stops local writes after sealing the measured output inventory.

Boundary cases: stale/replaced source files, unexpected mode, malformed JSON and field types, missing/future/expired authority, concurrent lock holders, invalid or modified URLs, failed/partial/ambiguous subprocess writes, missing or divergent public metadata/files/DOI, duplicate matching rows, formulas or values beyond first four cells, prior-row changes, and changed post-write headers.
