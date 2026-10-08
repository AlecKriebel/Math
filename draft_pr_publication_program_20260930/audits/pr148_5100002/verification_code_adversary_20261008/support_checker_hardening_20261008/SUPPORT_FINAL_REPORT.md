# Additional independent-support checker guard audit

Both independently authored support checkers reproduce their original outputs exactly. Both require assertion hardening: optimized Python accepts false polynomial identities, incompatible quadratic-field operations, false expected scientific values, irrational-to-rational extraction, and unsupported negative powers, then emits PASS. The geometry checker also accepts an inexact rational square root under optimization. Copied candidates now reject every tested false case in normal and optimized modes while preserving all original mathematical calculations and outputs.

This is an operational repair nomination for existing independent mathematical evidence, not a new proof approach or publication clearance. It supplements the completed original-code audit without altering it.

## Immutable originals and minimal candidates

All work is confined to this new owned subfolder. Both original reviewer source files and their existing review receipts remained unchanged; the frozen original20 and the earlier completed audit's 22 inventoried artifacts also remained unchanged. These facts are checked by `check_guard_only_transformation.py` and recorded in `SUPPORT_INTEGRITY_CHECK.json`.

| Checker | Original SHA-256 | Guard candidate SHA-256 | Assertions replaced |
|---|---|---|---:|
| Analytic `check_analytic_family.py` | 0dcbf4432c2108a90d5c7e862be00135085f8aee61193dc2cf1da39cb1127185 | 7209a6bc74fe5680df5eede6fbb526c6747321b1cff5b06e32db481a01915704 | 19 |
| Geometry `independent_geometry.py` | ee72567733d3065af5c6ab01637fa4b1e9258977210fdc32ce09b7276ce19e57 | b7309c40750b268df5f852f3000d5d8c2234e0c62702ebc62a0755ee759e2dec | 36 |

Candidates are `guarded_candidates/analytic/check_analytic_family.py` and `guarded_candidates/geometry/independent_geometry.py`. Reviewable source changes are in `guard_repair_candidates.diff`. Each `assert condition[, message]` became `if not (condition): raise RuntimeError(message)`, with a source-line label where the original had no message. An exact syntax-tree comparison against this sole transformation proves that every other executable expression, algorithm, input, and output schema remains unchanged. No assert nodes remain. The original mathematical predicate is preserved even for multiline conditions.

The analytic repair covers field compatibility, division norm, integer/nonnegative powers, rational extraction, polynomial identity, homogeneous tangency, third-point antipodality, positive angular/normal/half-sine values, area and sine-product expectations, angle/perimeter controls, exact difference, and ancillary product controls.

The geometry repair covers its field/rational/power/norm and exact-square-root guards, all convexity/contact/reflection/angle/outer-polygon/area/orientation requirements, polynomial divisibility/reconstruction, confocal constants, and final difference/common-control conditions.

## True reproductions and adversarial matrix

All executions used `/opt/homebrew/opt/python@3.14/bin/python3.14 -E -S -B -P`, with `-O` added for optimized runs. Each original owned source copy and its guard candidate was run in both modes. All eight true baselines PASS, with mathematical receipts byte-identical to the independently authored originals. Analytic stdout matches preserved `exact_check_output.json`; the geometry full output file matches preserved `independent_geometry_results.json`.

| Meaningfully false condition | Original normal | Original optimized | Candidate normal and optimized |
|---|---|---|---|
| Add constant 1 to one polynomial identity side / division numerator | Rejects | PASS with false claimed identity | Rejects without PASS |
| Add sqrt(5) and sqrt(2) in the single-field implementation | Rejects field mismatch | Accepts incompatible field arithmetic, then PASS | Rejects without PASS |
| Analytic H expected sine product 124/324 rather than 125/324; geometry expected incident component 1/4 rather than actual 1/3 | Rejects | PASS despite false scientific expectation | Rejects without PASS |
| Extract rational value from sqrt(5) | Rejects | Silently returns rational coefficient zero, then PASS | Rejects without PASS |
| Raise Q(2) to unsupported exponent −1 | Rejects | Empty range returns 1, then PASS | Rejects without PASS |
| Geometry square root of twice the genuine product square | Rejects | Truncated integer roots become an incorrect rational product, then PASS | Rejects without PASS |
| Divide by zero quadratic-field norm | Rejects | Fraction naturally raises ZeroDivisionError | Explicit guard rejection without PASS |

There are 60 matrix runs: 8 true baselines and 52 adversarial runs. The original optimized copies produce 11 false PASSes. All 26 candidate false runs return nonzero and emit no PASS. All normal original false conditions also reject. The zero-divisor controls show that assertion removal does not make every erroneous input silently succeed; they nevertheless verify the candidate explicit norm guards in both modes.

The polynomial changes are genuinely false identities, not only altered output flags. False field and rationality probes exercise the arithmetic domain assumptions before the unchanged scientific verification. The value probes supply false expected scientific quantities. All probe sources and their exact hashes are retained under `mutation_runs/`; each process receipt states the mutation and observed behavior.

## Checkable receipts and ROOT nomination

`SUPPORT_RUNS_SUMMARY.json` records the complete matrix. `raw_runs/<label>/stdout.txt`, `stderr.txt`, and `process_receipt.json` preserve complete output, exact command/cwd, PID/PGID, UTC start/end, return code, byte counts and SHA-256, successful waiting/reaping, and absent process group after completion. The matrix plus the independent minimal-transformation/integrity validator give 61 bounded closed child runs. Each used a 60-second limit and 524288-byte combined output cap; no limit was hit, no output was truncated, and no child group remained.

`SUPPORT_SOURCE_MANIFEST_BEFORE.json` pins original sources, candidate sources, and original mathematical receipts. `SUPPORT_FINAL_SUMMARY.json` binds the outcome; `SUPPORT_ARTIFACT_INVENTORY.json` pins the deliverable files. Root may nominate these copied candidates after independently inspecting the diffs and receipts. The global wrapper should bind the new source SHA values and current successful run/fresh output, rather than label repaired source byte-identical to its original. These candidates intentionally perform only minimal assertion enforcement changes; global frozen-source/receipt binding remains ROOT's responsibility.

Original effort remains one reported approach out of five; zero new central proof-search turns were added. No original/reviewer/completed-audit file, real Git/index/ref/cache, provider, or research-program state outside this owned subfolder was modified. No external communication was made. No novelty, human peer review, new mathematical theorem, or publication authorization is claimed. Completion estimate: 100% of this supplemental hardening audit.
