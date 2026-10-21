# Local packaging acceptance, 2026-10-21 UTC

This is a packaging self-check, not a second independent mathematical review. Mathematical acceptance is limited to INDEPENDENT_AUDIT.md and the preserved draft it identifies. The problem remains UNSOLVED.

Both standard and optimized Python runs pass. Complete mathematical stdout is frozen in replay/; root JSON outputs are byte-replayed in isolated temporary copies. Conversion is verified against the complete original AST, with only the documented assertion lowering and fixed required-input prefix allowed. No assertion-dependent acceptance checks remain in the root mathematical programs or packaging controls.

Executable negative controls, repeated in normal and optimized mathematical execution:

1. Incorrect certificate ambient interval.
2. Duplicate mark.
3. Incorrect pair sum.
4. Missing omitted-point blocker.
5. Corrupt triple witness equation/anchor.
6. Corrupt midpoint witness.
7. Unknown witness kind.
8. Missing certificate.
9. Missing author results.
10. Corrupt finite minimum crosscheck.
11. Actual blocker-algorithm mutation removing midpoint handling.

All 22 executions reject. Inventory controls reject an extra root file, extra nested file, nested manifest, file symlink, directory symlink, deleted required file, changed file, unlisted empty directory, unsafe manifest path, and duplicate manifest key. Separately, AST comparison rejects a shortened enumeration domain. The test suite itself passes in both normal and optimized mode.

Publication boundary: only authored mathematical text, scripts, result/certificate data, audit records, and public bibliographic/inspection metadata are included. No retrieved source document, private source extraction, dataset content, private coordination file, or private extraction fingerprint is included. Public source PDF/DVI hashes in source metadata are identified as public retrieval/inspection metadata. The N144 witness certificate is an authored independently verified mathematical construction deliverable, not reproduced source prose.

Historical hashes remain associated with original/ files; the recursive MANIFEST.json binds every current public file except itself. An external receipt binds the manifest. Passing these checks certifies reproducibility and the stated negative controls, not an asymptotic theorem, finite optimality, novelty, or an exhaustive literature search.
