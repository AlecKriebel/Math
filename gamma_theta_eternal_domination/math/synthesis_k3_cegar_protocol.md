# Resumable proof-producing CEGAR protocol for the \((12,3)\) synthesis instances

## Scope and claim boundary

This protocol runs one of the accepted `synthesis_k3` template encodings
through coloring-cut CEGAR.  It does not itself prove that the template list
covers every possible counterexample.  A verified `UNSAT` terminal excludes
only the named template, with exactly the cuts recorded in its checkpoint.
All required templates and their separate coverage proof are needed for a
certified finite negative result.

A satisfiable model whose complement graph is not three-colorable is frozen
as a **candidate pending independent review**.  The runner never calls such a
model a counterexample and never continues the search after freezing it.
The campaign's full counterexample certificate protocol remains mandatory.

## Trusted inputs

The production command accepts only the locally pinned binaries:

- CaDiCaL 3.0.1, commit
  `c60730422e758ef1cebe7aeddf2dda31c996bf04`;
- DRAT-trim, commit
  `2e5e29cb0019d5cfd547d4208dca1b3ec290349f`.

Their source archives and local executables are checked against fixed
SHA-256 values before every session.  The run manifest also binds the Python
runtime and every source or mathematical protocol file used by the runner:
`__init__.py`, `encoding.py`, `coloring.py`, `generate.py`, `cegar.py`, the
encoding design, and this protocol.

Any source, tool, configuration, or hardware-binding mismatch prevents a
resume.  Runtime sources and tool executables are rehashed around child
executions so a mid-session change is fail-closed.

## Directory and path discipline

Each template has a dedicated run directory.  A new run directory must be
empty.  It may not be the campaign root, a protected source/tool directory,
or any ancestor of a trusted input.  Symlinked path components are rejected.
Existing writable artifacts must be regular, single-link files.  Before each
child call, all read and write roles are resolved and checked for direct,
symbolic-link, and existing hard-link aliases.  Resume additionally enforces
an exact filename and a distinct logical and physical path for every
outcome-specific attempt role; a coloring, decoded graph, solver result,
proof, or checker log cannot be rebound as another role.

Audit mode is validation-only: it requires an existing `run.lock`,
`run_manifest.json`, and `checkpoint.json`, opens the existing lock without
`O_CREAT`, and never initializes or repairs a run directory.  Except for
ephemeral system-temporary logs during an explicitly requested live proof
replay, the audited directory tree is byte-for-byte unchanged.

An exclusive advisory lock on `run.lock` prevents two orchestrators from
using the same run directory concurrently.  A second deterministic
campaign-global lock in the resolved system temporary directory permits at
most one solver or checker child across *all* template run directories and
processes.  While holding that global lock and before spawning a heavy child,
the runner measures currently reclaimable memory without spawning a monitor
and requires the requested ceiling plus 512 MiB of headroom.

Every child receives absolute paths, an empty environment, a closed stdin, a
hard wall-clock deadline, and a configured resident-memory ceiling.  On
macOS the runner reads RSS directly through `libproc` and kills the process
group when the ceiling is crossed; on platforms supporting `RLIMIT_AS`, it
also installs that address-space limit.  Final peak RSS is obtained from
`wait4`.  `RLIMIT_FSIZE` bounds every individual child-created model, proof,
or log file.  CaDiCaL is single-process and is invoked with an explicit
deterministic seed.  Temporary SIGTERM, SIGHUP, and SIGINT handlers kill and
reap the active `setsid` process group before the orchestrator exits, so a
solver cannot survive and continue after releasing either lock.

Before solving, the runner obtains current free space from the target
filesystem.  It reserves the configured do-not-use disk reserve (4 GiB by
default), nine maximum-size child files for the UNSAT proof/checker peak
(three first-pass solver files, four proof-pass files, and two checker logs),
16 MiB of generation workspace, and the configured retained-attempt maximum
times the requested iteration budget.  A new session is refused before its
run manifest is installed if this conservative budget is unavailable.  The
check is repeated on every resume.

## Atomic checkpoint and crash semantics

`checkpoint.json` is the sole commit point for progress.  It is written to a
same-directory temporary file, flushed, atomically replaced, and followed by
a directory `fsync`.  It contains:

- the immutable run-manifest hash;
- status (`running`, `candidate_review_pending`, or `unsat_verified`);
- a sequence of immutable attempt-manifest references;
- a list of distinct canonical coloring partitions;
- the exact same-color clause and hashes for every partition;
- an append-only SHA-256 history-chain head whose predecessor is recorded in
  every attempt; and
- an optional terminal marker reference.

The canonical cut-list bytes have their own SHA-256 in the checkpoint.
Checkpoint validation recomputes every coloring, clause, uniqueness
condition, attempt hash, artifact hash, outcome-specific semantic check, and
history-chain step once at the beginning of a resumed session.  Each
subsequent cut in that same bounded process validates and atomically appends
only its new attempt.  A candidate or UNSAT outcome is legal only in the last
attempt reference and only when it matches the terminal checkpoint status.

The predecessor chain is the authoritative append-history binding.
`checkpoint_before_sha256` is the canonical digest of the prior **logical
checkpoint state**, not a hash that requires reserializing every preceding
ledger entry.  Its domain-separated payload contains the configuration and
run-manifest bindings, status, attempt and cut counts, streamed cut-prefix
hash, history-chain head, and terminal binding.  Because the cut-prefix hash
and history-chain head already bind the full ledgers, every later
`checkpoint_before_sha256` can be recomputed and checked in constant work
after its preceding history step.  This makes exact predecessor chronology
compatible with a linear audit.

An attempt is built in a fresh randomly named directory, after which the
`attempts/` parent directory is `fsync`ed.  Its inputs,
outputs, commands, logs, resource record, and validations are written before
the checkpoint is changed.  A crash can therefore leave an unreferenced
attempt directory, but cannot commit half a cut.  Resume starts from the last
atomic checkpoint and ignores unreferenced attempts.

Intermediate colorable attempts are compacted before commit:

- the exact `cuts.json` and CNF hashes, sizes, original paths, template,
  cut-prefix count, cut-prefix hash, and generator-manifest hash are retained;
- raw `cuts.json` and CNF bytes are then removed because they are
  deterministic functions of the accepted sources and checkpoint prefix;
- the solver result/model and stdout/stderr are deterministically gzip
  compressed with `mtime=0`, retaining raw and compressed hashes and sizes;
  and
- decoded graph/family data, coloring, generator manifest, attempt manifest,
  and compressed bytes remain directly available.

Resume checks every compressed stream and prefix recipe.  For each historical
coloring attempt, it evaluates the complete model against the fixed base CNF,
checks the decoded graph/family, verifies the proper coloring, and validates
that attempt's one globally sound same-color cut and that the cut is false in
its source model.  It does not rescan all earlier cuts against every later
historical model: that information is unnecessary for soundness once every
cut is independently established to be globally valid.  The canonical cut
ledger, uniqueness, source-attempt binding, clause, and streamed prefix
hashes are validated once in a separate linear pass.

A publication `--audit-only --deep-reconstruct` rebuilds the latest
reconstructible prefix once from one base encoding and the streamed cut
prefix.  A decisive candidate or UNSAT attempt, which can occur only as the
last ledger entry, retains its raw CNF and is reconstructed exactly once
against the complete accepted cut ledger.  Regenerating every historical
DIMACS prefix would inherently repeat growing prefix output and is
deliberately not presented as a linear audit.

The default retained-attempt ceiling is 2 MiB.  In the bounded three-cut
implementation smoke, raw CNFs were 520,311–520,447 bytes, while complete
compacted attempt directories were 30,592–30,803 bytes (30,728-byte mean).
This measurement is not a future-size guarantee; the enforced ceiling and
disk preflight remain authoritative.

For a candidate or verified `UNSAT`, a top-level immutable terminal marker is
written before the checkpoint transition.  The existence of either marker
blocks every subsequent solver call even if a crash prevented the matching
checkpoint update.

## One iteration

For a checkpoint containing canonical partitions
\(c_0,\ldots,c_{t-1}\):

1. Serialize exactly those partitions to the attempt's `cuts.json`.
2. Call the accepted deterministic generator for the selected template.
   Rehash its source manifest, input, installed CNF, and generated manifest.
3. Parse the DIMACS independently and require exact equality with a fresh
   in-memory reconstruction of the base clauses plus the recorded cuts.
4. Run CaDiCaL once, with the fixed seed and configured wall, memory, and
   file-size limits.  Save and hash the exact argv, stdout, stderr, result
   file, elapsed wall time, CPU time, and `wait4` maximum resident set size.

At creation and again on resume, the result parser requires an
outcome-consistent exit code, positive configured limits, canonical exact
child command, and exactly one complete assignment of
every DIMACS variable, with no duplicate, conflicting, missing, or
out-of-range literal.  Every CNF clause is evaluated directly.  The graph and
eternal family are then decoded and checked by
`validate_decoded_candidate`, independently of the auxiliary SAT variables.
For compacted coloring attempts, resume evaluates the complete assignment
against every clause of the accepted fixed base encoding, including all
auxiliary-variable clauses; it does not infer base-clause satisfaction merely
from the decoded graph.  It then validates the attempt's decoded semantics,
proper coloring, and own same-color cut.  Earlier cuts are not scanned again
for that model.  This is a proof-preserving audit boundary: the final formula
uses only the fixed base and cuts that have each been proved globally sound,
so whether an old source model also satisfies every earlier sound cut is
provenance detail rather than a premise of the final implication.

- If exact DSATUR returns a proper three-coloring, its validity is checked
  directly against the decoded graph.  The coloring is canonicalized by
  first occurrence of color classes.  The runner requires it to be new,
  derives `same_color_cut`, confirms every literal of that cut is false in
  the current model, compacts the intermediate artifacts as above, writes the
  attempt manifest, and atomically appends the cut and attempt reference to
  the checkpoint.
- If exact DSATUR returns no coloring, the decoded graph, family, CNF, model,
  commands, logs, and all hashes are frozen.  The candidate marker is written
  first and the checkpoint is then marked `candidate_review_pending`.  No
  continuation operation exists.

For an initial `UNSAT`, the result is not accepted.  The runner rehashes and
reruns the identical CNF with the same solver parameters and a saved ASCII
DRAT proof.  It requires a second `UNSAT`.  In a later, sequential child
process it invokes DRAT-trim with `-I -f -W`, requires exit status zero,
requires an exact output line `s VERIFIED`, rejects every checker warning,
and verifies that neither CNF nor proof changed during checking.  Only then
does it write `unsat.verified.json` and atomically mark the checkpoint
`unsat_verified`.

Resume derives the single final terminal outcome from the retained raw CNF,
initial and proof-pass result files, nonempty proof, exact commands, child
statuses, and the warning-free stored checker transcript.  It reconstructs
the decisive complete CNF once; terminal-marker checks reuse that validated
attempt rather than repeating its semantic reconstruction.  For a
mathematical or publication audit, `--audit-only --verify-terminal-proof`
launches the pinned DRAT-trim once more under the same global lock and
resource limits against the retained CNF/proof.  Stored `s VERIFIED` text
alone is not treated as an independent certificate check.

Timeouts and solver `UNKNOWN` results append no cut and prove nothing.  Their
attempt data is compacted and may be retained for diagnosis, while the last
committed cut checkpoint remains resumable.

## Cryptographic bindings

The immutable run and attempt manifests jointly bind:

- all runtime sources and protocol documents;
- both pinned source archives and both executable binaries;
- Python implementation, version, and absolute executable;
- normalized resume command and every exact child argv;
- cut input, generated manifest, DIMACS CNF, solver result/model, decoded
  candidate, coloring, DRAT proof, terminal marker, checker output, and every
  stdout/stderr log;
- the pre-attempt checkpoint and the committed cut record; and
- configured limits plus measured wall, user CPU, system CPU, peak RSS, and
  pre-child reclaimable memory.

Hashes establish byte identity and provenance; they are not digital
signatures.  The repository and local filesystem remain within the trusted
computing base.

## Production invocation

Run a bounded, one-hour batch.  History is validated once at session start,
and every completed cut is still committed immediately:

```text
PYTHONPATH=src python3 -m synthesis_k3.cegar \
  --validation-gate-open \
  --template hole5 \
  --run-dir results/synthesis_k3_runs/hole5 \
  --max-iterations 50 \
  --seed 0 \
  --solver-wall-seconds 300 \
  --solver-memory-mib 3072 \
  --checker-wall-seconds 300 \
  --checker-memory-mib 3072 \
  --session-wall-seconds 3600 \
  --disk-reserve-mib 4096 \
  --child-file-limit-mib 256 \
  --retained-attempt-limit-mib 2
```

Before starting another iteration the runner reserves enough session time
for the initial solver, a possible proof rerun, and DRAT-trim; otherwise it
returns `session_wall_exhausted` without changing the checkpoint.  The same
command resumes from the next committed cut.  Use separate run
directories for `hole5`, `hole7`, `hole9`, and, while it remains part of the
certified fallback, `antihole7`.

For a terminal UNSAT publication check, rerun the same configuration with
`--audit-only --verify-terminal-proof` (and optionally
`--deep-reconstruct`).  This launches only the independent proof checker,
never the synthesis solver.

## Limitations

- A verified template-level `UNSAT` is not a universal result without the
  accepted template-coverage proof and all required terminal proofs.
- The DSATUR no-coloring result only triggers candidate quarantine; it is not
  exported as the final clique-cover certificate.
- Memory enforcement is per child process.  On macOS the RSS ceiling is
  polling-based, so a transient overshoot between samples is possible.  The
  pinned tools are single-process; replacing them or wrapping them is
  forbidden by the binary and command checks.
- Current-memory availability is inherently time-varying.  A refused child
  is a resource gate, not a mathematical result; retry after memory pressure
  falls or explicitly review a smaller configured ceiling.
- The disk estimate is intentionally conservative.  A large requested
  iteration budget can be refused even when typical compressed attempts
  would fit; use smaller resumable sessions rather than reducing the reserve
  without an explicit resource review.
- Intermediate CNFs are reconstructible rather than retained.  Publication
  audit should use `--audit-only --deep-reconstruct` for the latest prefix;
  decisive candidate and verified-UNSAT terminals retain and exactly check
  their raw CNF and model/proof data once.  The ordinary audit exposes exact
  work counters used by regression tests: one base-CNF and one own-cut
  validation per historical coloring model, one validation per cut-ledger
  record, and at most one decisive CNF reconstruction.  An
  all-historical-prefix forensic regeneration is outside this linear audit
  and must be labeled quadratic.
- The exclusive lock and atomic-replace guarantees assume a normal local
  filesystem.  They do not defend against a privileged process modifying
  files concurrently.
- Orphan attempt directories after abrupt termination are intentionally
  retained.  They are not part of the checkpointed proof record.
- The runner produces DRAT plus DRAT-trim verification.  Conversion to LRAT
  or packaging all template terminals into a publication archive is a later
  certificate step.
