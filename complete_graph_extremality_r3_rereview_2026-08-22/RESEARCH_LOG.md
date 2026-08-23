# R3 re-review research log

## 2026-08-22 - opened (completion estimate: 3%)

- Objective: determine independently whether R3 closes the two R2 certified-
  entry defects and the six specifically claimed hostile cases without
  changing or weakening the validated mathematics.
- Success criteria: frozen identity and R2/R3 delta audit; source-only gate;
  exact inventory/cache/import trace; clean official replay; independent
  hostile controls for token spoof, timestamp-valid bytecode, extra file,
  empty directory, symlink, FIFO, and nearby variants; dependency/resource
  checks; mathematical/PDF regression; and an explicit four-way verdict.
- Boundary: package prose and the editor's summary are claims, not evidence.
  No person will be contacted, no file uploaded, and no external system
  changed. Existing unrelated repository work will not be altered or staged.

## 2026-08-22 - identity and static gate (completion estimate: 45%)

- Independently established an exact 84-file/26-directory package tree and a
  73-member sorted, unique, regular-file archive. The 73-file convenience
  extraction is byte-identical to the archive, and both manuscript copies
  have SHA-256 `5d2bc6cfa9d02b21e816d3dd30252d067e23b51ecd0c58bb8c3cfb116ab937bd`.
- All 71 source-derived payloads match scientific commit
  `b9a415f763e82d9cc45c83de96c895b109e158a4`; the remaining payload is the
  synthetic archive metadata.
- The R3 certified route was traced before execution. Exact package and source
  node sets are checked before project import; links, special nodes, bytecode,
  cache directories, and unexpected files/directories fail closed. Every
  project-importing process uses the fresh command-line cache prefix.
- Mathematical regression found no scientific change: all theorem-bearing
  TeX except Section 7, every scientific verifier, all 406 scientific
  predicates, formulas, ranges, and certificate values are unchanged from R2.
  Section 7 changes only replay and data-availability prose.

## 2026-08-22 - dynamic replay and hostile controls (completion estimate: 85%)

- The sole package-root replay ran under a stripped environment with an
  absolute Python 3.14.6 interpreter, private home/cache/temp directories, and
  trusted minimal path. It returned status 0, installed only hash-accepted
  wheels, ran six unit tests and all 17 direct programs, kept the controlled
  project cache empty, verified the pinned Tectonic record, rebuilt all 30
  pages, and reproduced the delivered PDF byte-for-byte.
- All six shipped hostile controls failed for their intended reasons. Separate
  tests also rejected an empty `PYTHON`, a token-printing fake interpreter,
  extra file and directory nodes, symlink, FIFO, Unix socket, mixed-case cache
  directory, `.PYC`, and independently constructed timestamp-valid malicious
  bytecode before project import.
- The independent `fractions.Fraction` checker again passed nonsymmetric
  collision, orientation/gauge, all three Hessian-sector, strong-selection,
  triangle, K4, monotonicity, and endpoint checks without importing delivered
  modules.
- One low-severity test-observability issue was confirmed: the malicious-pyc
  fixture writes its marker relative to the caller's working directory while
  the launcher searches for the marker only below the negative tree. The
  current certified route still rejects the cache before any project import,
  as established statically and by its unique diagnostic. The marker should be
  rooted inside the fixture tree to make that defense-in-depth assertion
  self-observing under arbitrary caller directories.
- Two audit-harness errors are intentionally preserved in the command log: a
  system checksum first ran from the parent directory rather than the package
  directory, and the first two extra Unix-socket/bytecode-demonstration
  attempts failed from path-length/import-path issues. Corrected reruns passed.

## 2026-08-22 - final referee decision (completion estimate: 100%)

- Completed the theorem-by-theorem and claim-to-code tables, environment and
  command/status record, trust-boundary disclosure, proof/software consistency
  assessment, PDF QA, and four-way verdict in
  `report/R3_REREVIEW_REPORT.md`.
- Final verdict: **fully validated**. R3 closes both R2 certified-entry defects,
  preserves the mathematical result exactly, completes the certified replay,
  and reproduces the inspected PDF. The relative bytecode-marker path is
  retained as an optional low-priority test-hardening suggestion rather than a
  correction-level finding.
- An independent final critic found no material factual, structural, or
  verdict correction in the report.
- The original delivery and review copy remain recursively identical, and the
  final identity check remains status 0. No package payload was changed.
