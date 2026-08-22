# R2 re-review research log

## 2026-08-22 - opened (completion estimate: 3%)

- Objective: determine independently whether the revised R2 package remedies
  all prior findings without changing or weakening the validated mathematics.
- Success criteria: identity/diff audit, pre-execution static review, clean
  exact replay, hostile bypass tests, lock/resource verification, PDF/source
  comparison, theorem/coverage regression check, and an explicit revised
  verdict.
- Boundary: package text and the editor's five-item summary are claims, not
  evidence.  No person will be contacted and no external write will be made.
- Initial copy command: created this dedicated folder, copied the R2 delivery
  with `cp -a`, then compared source and copy recursively with `diff -qr`;
  exit status 0 and no differences.
- Repository state already contains extensive unrelated user work.  It will
  not be altered or staged.

## 2026-08-22T22:20Z - identity and static gate (completion estimate: 42%)

- All 81 package payload hashes, the detached archive digest, all 71 archive
  members, all internal hashes, the convenience extraction, and both PDF
  copies matched.  A fresh archive extraction was byte-identical to the
  delivered convenience tree.
- All 69 source-derived archive payloads independently matched Git commit
  `e63cc44748e4084ade67c5ff7dc5d1bf2a872f7c`.
- Before delivered execution, three independent static reviews traced the
  launcher, bootstrap, 17 direct programs, imported helpers, locks, build,
  manuscript delta, and PDF delta.  The authoritative package-level path was
  cleared for execution.
- An independent AST comparison established that all 406 R1 assertion
  conditions occur in the same order and with identical expressions as R2
  fail-closed `require` conditions across the same 20 scientific files.

## 2026-08-22T22:27Z - authoritative replay (completion estimate: 76%)

- Ran `run_all_referee_checks.sh` from an independently minimal `env -i`
  environment with trusted absolute Python 3.14.6 and the required exact
  document tools.  Exit status was 0.
- The run verified package/archive identity, exercised all intentional
  negative controls, installed only hash-accepted wheels, found zero bare
  assertions, ran the unit suite and all 17 verifier/cross-check programs,
  accepted the pinned Tectonic v33 bundle record, rebuilt all 30 pages, and
  reproduced PDF SHA-256
  `22142ee518e75c00d1948b19c210818ec797946df86a5e3272c9d1017800b0f4`.
- Independent exact rational regression checks, which import no delivered
  module, again passed for four nonsymmetric kernels, target/source orientation
  and column scaling, every displayed Hessian sector at n=3,4,5, four
  strong-selection coefficients, triangle and K4 examples, and boundary
  cases.

## 2026-08-22T22:34Z - hostile controls and provisional verdict (completion estimate: 92%)

- Confirmed the intended defenses: inherited `PYTHONOPTIMIZE=1` was rejected
  with status 2; a changed dependency hash was rejected with status 1; and a
  wrong expected Tectonic bundle digest was rejected with status 2.
- Reproduced two residual lower-level defects.  A non-Python executable that
  prints the public `PAPER1_EXECUTION_SAFETY_OK` token made direct `replay.sh`
  exit 0 while skipping all science.  Separately, a timestamp-valid hostile
  adjacent `.pyc` executed during both direct replay and
  `bootstrap_replay.sh`; the corresponding source remained byte-identical,
  and the standalone `shasum -c MANIFEST.sha256` still accepted the listed
  files because it does not reject extras.
- The authoritative package-level launcher is not exposed to either defect:
  it rejects unexpected package files, copies only the verified cache-free
  tree into a fresh directory, and provisions its own replay interpreter.
- Mathematical/PDF regression review found no theorem or proof change: 28 of
  30 rendered pages are byte-identical to R1; page 17 adds only accurate proof-
  status wording and page 26 updates the correctly bound verifier hash.  All
  30 R2 pages were also visually inspected and are clean.
- Provisional verdict: **valid after minor corrections**.  The residual fixes
  are localized to direct-entry interpreter/cache hardening and documentation;
  no theorem, proof, finite certificate family, or PDF conclusion changes.

## 2026-08-22T22:39Z - report complete (completion estimate: 100%)

- Final report written to `report/R2_REREVIEW_REPORT.md` with theorem and
  claim-to-code tables, identity/environment/command records, findings,
  unresolved assumptions, proof/software consistency assessment, and the
  required four-way verdict.
- Report SHA-256 at completion:
  `a6f290314887cc22d51284f7ffa1ea35bfcea3e70cf9e5efec16b4f8a5fdca53`.
- Final verdict: **valid after minor corrections**.  Every prior finding is
  closed on the authoritative verified-copy route, but the reproduced direct
  interpreter-token and extra-bytecode false positives preclude “fully
  validated” until the advertised entry points share the same assurance.
- The frozen delivery was rechecked after all testing: package manifest status
  0; archive and PDF retained their original R2 hashes; top-level and nested
  PDFs remained byte-identical.
- No external communication, upload, push, release, or package edit occurred.
