# Offline handoff preflight — 10 September 2026

**Preflight passed. Bell source is still uncompiled and not kernel-verified.**
No mathematical completion certificate, successful compiler run, or online
repository modification is claimed. This status supersedes earlier execution
instructions; the earlier source-writing and provenance documents are retained.

## Concrete source repair

`Bell/ConeCompression.lean` used `finite_functional_coordinates`, defined in
`Bell/FiniteLinearAlgebra.lean`, without importing its defining module through
its dependency chain. The missing `import Bell.FiniteLinearAlgebra` is now added.
A regression test detects the missing-import situation and accepts the repaired
transitive import graph. This is a textual dependency check, not Lean resolution.

All **58 mathematical modules** are preserved. Of them, **57 are byte-identical**
to the incoming end-to-end ZIP and one has the import repair. For every module,
all comment-free non-import source is unchanged. In particular, this phase does
not weaken a theorem statement or add a main-theorem premise. There remain
681 theorem/lemma source attempts, of which 672 are public and nine private.
The mathematical source now has 10,376 lines, one more than the incoming draft.
Counts describe source text, not declarations accepted by Lean.

The main source interfaces continue to expose actual complex fixed-qubit
strategies, arbitrary finite dependent output alphabets, ordinary convex hulls,
and a finite common mixture of complete PVM strategies. No independently
established counterexample or definite new mathematical gap was found in this
preflight. This is not an exhaustive mathematical referee review; a successful
static scan is no guarantee that the large analytic proof bodies work.

## Verification runner repairs

The old shell runner could leave a stale passed `axiom_audit.json` after an early
failure. The new Python-backed wrapper archives earlier receipts and clears all
success flags at the start; any failure clears them again. Each run has an
exclusive lock, unique identifier, separate logs, command exit codes, and source
hashes. Tests cover early failures, partial serial builds, interruption, bad
compiler identity, missing reports, forbidden axioms, source changes, statement
failures and invalid-proof controls.

The runner enforces the compiler version **and full compiler commit**, all pinned
dependency revisions and tracked-file cleanliness. It preserves old local project
build outputs and requires a new full project build rather than trusting reused
local `.olean` files. Dependency caches are retained. The allowlisted standard
axioms are recorded, and all 672 public theorem dependencies are queried.
Private helper dependencies are traversed through their public clients.

There are **14 independent Lean statement-contract examples** in
`validation/Statements.lean`. These are new validation source, not new
mathematical assumptions. They must actually elaborate after the full build;
textual presence or `#check` alone does not count. They remain uncompiled here.

The source-token audit now excludes intentionally invalid smoke-test files in
run-report directories, tracks namespace/section scopes separately, and screens
additional local metaprogramming/kernel-bypass mechanisms. It is a conservative
text policy, not a substitute for Lean's parser/kernel or a security boundary.

## Packaging and reproducibility repairs

The packager preserves nested historical checksum manifests instead of dropping
every file named `SHA256SUMS.txt`. It verifies every ZIP member against the new
root manifest, checks for extra/duplicate entries, preserves original line endings
and executable modes, writes atomically, and rejects unsafe paths, symlinks,
active-run snapshots and probable credential files. Build caches and font files
are excluded. The shipment verifier and one-command compiler-free preflight are
included. The complete incoming ZIP remains byte-identical at
`preservation/input_before_preflight.zip`.

Optional test dependencies are explicit in `requirements-preflight.txt`. The
handoff guide distinguishes online cache acquisition, already-prepared offline
execution, native host architectures, and the separate Linux x86_64 export bundle.
This source archive does not include a compiler or Mathlib build cache.

## Executed evidence

The complete compiler-free suite is replayable with `bash scripts/preflight.sh`.
The evidence is in `reports/preflight/validation_summary.json` and its named logs.

- **44** static/parser/runner-control tests passed. Runner subprocess outputs are
  mocked in temporary roots; no mock proof-success receipt is shipped as real.
- **10** retained dependency-log parser tests passed on explicitly mock text.
- **17** real temporary-file packaging/integrity/safety tests passed.
- **21** retained environment-transport and embedding tests passed.
- The original **122** exact algebra/finite checks and **1,215** rational
  transportation regressions passed, comparing **43,740** probability entries.
- The rational SOS identity, all three support cases, five corrupted-certificate
  controls, and the independent twelve-leading-minor positivity check passed.
- **230** deterministic-gap polynomial identities passed, including every
  declared-table identity and the transpose negative control.
- The expanded-source checker passed **69** symbolic identities, **474** rational
  regressions, and its incorrect-transpose negative control.

The 92 software/transport tests and the finite algebra have distinct scopes.
None proves Lean elaboration, the analytic reductions, the full equality theorem,
or correct manuscript interpretation. Historical reports outside the current
preflight directory remain historical evidence for their own stages.

## Next step

Read `OFFLINE_RUN.md`, verify the shipment bytes, prepare the pinned toolchain,
and run `bash scripts/check.sh --serial` (or add `--bootstrap` while online).
The next substantive proof gate is the actual Lean build, statement-contract
elaboration and dependency audit, followed by repairs exposed by that run.
Further blind source expansion is not a replacement for that gate.
