# Run the preserved Lean draft

**The source has not been compiled here.** The compiler-free preflight is passed,
but there is no successful Bell proof-checking run. Compilation repairs and
possibly mathematical repairs can still be required. No time estimate is implied.

## 1. Verify the shipment before it changes

Extract the ZIP and enter its `bell_lean` directory. Before regenerating reports:

```bash
python3 scripts/verify_files.py
```

This checks shipment hashes, not Lean proofs. Tests and builds legitimately
rewrite reports, so the original shipment manifest will no longer describe the
whole working tree afterward. The incoming complete source archive remains in
`preservation/input_before_preflight.zip`.

## 2. Prepare dependencies before disconnecting

The source ZIP does **not** contain a compiler or a compiled Mathlib cache.
Use the project-pinned **Lean 4.19.0** and the exact dependency manifest. Do not
run `lake update`, change versions, or delete the manifest just to get a build.
A compiler for the machine's own architecture is required. The supplied
`environment/` export workflow produces a **Linux x86_64** bundle; it is not a
native Apple-silicon Mac toolchain. The Lean source itself is not platform-specific.

For a machine already equipped with the pinned toolchain and Internet access,
this command acquires the dependency cache and then attempts the complete run:

```bash
bash scripts/check.sh --bootstrap --serial
```

Prepare optional Python checks while online with:

```bash
python3 -m pip install -r requirements-preflight.txt
```

The real Lean runner needs only Python's standard library, Git, Bash, and the
pinned Lean/Lake installation and dependencies. SymPy and PyYAML are for the
separate compiler-free checks. Python 3.10 or newer is required by the helpers.

## 3. Run with the environment already present

```bash
bash scripts/check.sh --serial
```

Without `--bootstrap`, the runner checks dependency checkout presence, exact
commits and tracked-file cleanliness before invoking Lake. It does not issue a
cache-acquisition command. This is not network isolation: Lake or an elan shim
retains its normal behavior. For an air-gapped run, prepare the full toolchain
and caches first, disconnect externally, and use the same command.

`--serial` builds project modules in dependency order and keeps one named log
per module. It does not mean a subset result is sufficient. Omitting the flag
lets Lake schedule the aggregate build normally. No unsupported Lake `-j` flag
is used.

Each run preserves the preceding local `.lake/build` directory under
`.lake/preflight-builds/<run_id>/` and creates fresh project build outputs.
Dependency caches under `.lake/packages/` are not removed. These local backups
can occupy disk space; they are omitted from source ZIPs. Never remove them while
a run is active. The compiled dependency cache and compiler producer remain
trust assumptions; this workflow does not independently rebuild Mathlib from
first principles.

## 4. What the runner requires for success

A fresh run gets its own `reports/runs/<run_id>/` directory. The runner requires:

1. Configuration/source checks; exact compiler version and full Git hash; exact
   dependency commits and no modified tracked dependency files.
2. A valid polynomial smoke proof accepted and an invalid `False` proof rejected
   with a type error, rather than a crash or missing-import failure.
3. A fresh complete `Bell` build, then actual Lean elaboration of the 14 examples
   in `validation/Statements.lean`.
4. One dependency report for every public theorem in the generated inventory,
   including every required main theorem. The allowlist is `propext`,
   `Classical.choice`, and `Quot.sound`; `sorryAx`, unapproved axioms, missing or
   duplicate reports, and compiler error diagnostics fail the run.
5. Identical project source/configuration hashes before and after the checks,
   and a final exact dependency check.

The independent statement examples spell out actual complex 2-by-2 operators,
valid density matrices/PVMs, ordinary convex hulls of physical strategy ranges,
one common random variable selecting complete projective strategies, boundary
alphabets, the attained radical value, and quantitative separation/minimality.
They are source attempts until Lean accepts them. They do not prove on their
own that every modelling choice faithfully matches the manuscript.

## 5. Read the current run, not an inherited report

The authoritative entry point is `reports/latest_run.json`, which identifies
one run directory. Its `kernel_report.json`, `axiom_audit.json`, and
`statement_audit.json` must refer to the same run. Top-level copies are provided
for convenience. Old reports are archived under `previous/` before new checks
start. Failure or interruption clears success flags in all top-level reports.

A static check, smoke test, single module, or statement check alone is **not** a
full success. The full receipt must have `status: "passed"`,
`last_stage: "complete"`, and true full-build/statement/dependency flags.

No such successful receipt is supplied in this shipment. Its current failure
receipt demonstrates the missing-compiler path only; no Lean process ran.

## 6. On the first error

Read the first relevant module log in the run directory. Repair the source,
then rerun the full wrapper. For isolated diagnosis, `lake build Bell.ModuleName`
is useful but is not a full verification run. Do not replace a failing proof by
an axiom, `sorry`, an assumed conclusion, or a weakened target just to obtain a
green build. Substantial errors may be elaboration/API issues or genuine proof gaps.

Some inherited algebraic proofs disable heartbeat limits and may run for a long
time. Ctrl+C leaves the current run unverified and preserves logs. A crash may
leave `reports/.lean-run.lock`; confirm no previous process is active before
removing that stale lock. Do not disable locking for simultaneous runs.

To preserve the source and diagnostics after a run:

```bash
python3 scripts/package.py ../bell_lean_after_run.zip
```

The package includes the current source, configuration and run logs; excludes
compiler/dependency caches, Git metadata, build products and font files; and
refuses symlinks or likely credential files. Review logs before sharing them.

## Compiler-free checks only

```bash
bash scripts/preflight.sh
```

These execute Python tests and independent exact algebra, never Lean or Lake.
Mocked subprocesses in the runner tests exist only in temporary directories and
are explicitly labelled; they are not proof-verification evidence.
