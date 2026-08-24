# Research log

## 2026-08-23 - Post-submission AI referee handoff initiated

- Objective: provide one neutral, self-contained package from which an AI
  journal referee can read the submission, inspect proof and verifier code,
  execute compact and exhaustive qualification, perform independent attacks,
  and reach its own scientific verdict.
- Copied rather than moved the complete 448-member sealed referee tree from
  the deterministic source archive.  The original project and archive remain
  unchanged.
- Added an outer integrity boundary, neutral prompt, clean five-source build
  gate, mutation checks, deterministic archive builder, and one all-verifier
  execution entrypoint.
- Best-guess completion toward the referee handoff: **70%**.  Remaining work:
  seal the outer manifest, run clean-room quick qualification, audit prompt
  neutrality and command coverage, build the transfer archive twice, and
  checkpoint the final hashes.

## 2026-08-23 - Clean-room dependency closure repaired

- The first copied quick run passed outer integrity, outer mutations, and the
  clean manuscript build, then failed the article static audit because the old
  448-member archive omitted four `work/...` aliases used by the printed
  certificate replayers.
- Two missing files had byte-identical copies under the sealed portable proof
  tree.  The current four-port residual and quartic files did not; their exact
  current bytes are instead bound to source commit `078b573d` by the outer
  package.  Added all four required paths without altering any inner sealed
  file and recorded the distinction explicitly.
- The initial defect was missing execution closure.  No mathematical
  discrepancy has yet been found, but the two current-only dependencies must
  be treated as outer-package evidence and independently audited.  Best-guess
  handoff completion remains **70%** pending a fresh end-to-end quick run and
  final adversarial audit.
- The next keep-going quick run passed 20 of 21 gates, including the final
  theorem quick replay and outer release mutations.  The only failure showed
  that `output/referee/REFEREE_BUNDLE_CONTENTS.json`, used by the
  theorem-artifact crosswalk producer, was also omitted from the old inner
  archive.  Copied and outer-bound its current tracked bytes as the fifth
  supplemental execution dependency.

## 2026-08-23 - Clean copied quick qualification passed

- Reran the unified runner from the dependency-complete copied handoff.
  All 21 commands passed: outer integrity and mutations, isolated five-source
  builds, article audit, both crosswalk checkers and mutations, proof
  compression and equivalence, family coverage, printed templates,
  restoration, probe reconstruction, weak sharpness, release lock, theorem
  quick replay, and outer release mutations.
- Total wall time was 820.64 seconds.  The execution ledger SHA-256 is
  `5ce51ccd79ec859904e12d3020dcdcae20729d870c0b84ef4346fd012d216fb4`.
  Copied the ledger and all 21 per-command logs under
  `reference_qualification/`; they are reference evidence, not a substitute
  for the referee's own execution.
- A separate prompt-bias audit returned PASS: counts and stored PASS reports
  are consistently labelled assertions, ACCEPT/HOLD/REJECT are all available,
  and human metadata is separated from the scientific verdict.
- Best-guess handoff completion: **95%**, pending final package audit,
  deterministic double archive build, hashes, commit, and push.

## 2026-08-23 - Referee handoff closed

- Independent final package audit returned PASS with no load-bearing blocker.
  It checked the outer and inner ledgers, all five supplemental dependency
  disclosures, every copied quick-run log hash, command coverage through the
  35-layer full path, clean source compilation, mutation gates, environment
  instructions, and live/archive byte agreement.
- Independent prompt audit also returned PASS.  The prompt treats every count,
  hash, stored replay, and prior verdict as an assertion; permits ACCEPT,
  HOLD, and REJECT; requires independent falsification; and separates the
  scientific verdict from human metadata.
- The deterministic transfer archive is built twice and compared byte for
  byte after the outer manifest is frozen.  Its SHA-256 is intentionally
  supplied by an external adjacent sidecar to avoid self-reference.
- Handoff construction and validation: **100%**.  The package is ready to give
  to an independent AI referee.  The referee's own mathematical conclusion is
  intentionally not predetermined by this checkpoint.
