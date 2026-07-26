# Order-13 k=3 single-template proof-production protocol

## Claim boundary

This protocol concerns one exact CNF template at a time.  Even a completed
template proof is not an order-13 exclusion until the mathematical template
cover and every remaining template have separately accepted proofs.  Solver
`UNSAT`, a timeout, an incomplete proof, or a checker message without all
bound artifacts is not a result.  `SAT` is only a candidate pending a
standalone verifier.

## Frozen inputs

`initialize` first exhaustively reconstructs and audits a constructor package.
It then exclusively creates a run directory containing copies of the exact
DIMACS formula, coloring bank, and constructor manifest.  The run manifest
binds:

- all copied artifacts by path, size, and SHA-256;
- the current bytes of the constructor, normalizer, runner, and bounded-child
  implementation;
- four distinct executable files for CaDiCaL, drat-trim, lrat-check, and the
  normalizer Python interpreter;
- human-readable identities alongside the authoritative hashes: CaDiCaL 3.0.1
  at commit `c60730422e758ef1cebe7aeddf2dda31c996bf04`,
  drat-trim/lrat-check at commit
  `2e5e29cb0019d5cfd547d4208dca1b3ec290349f`, and the exact Python
  implementation, version, platform, path, and executable hash;
- seed, exact resource ceilings, hardware census, and normalized resume/audit
  invocations.

The three production binaries must match the campaign-pinned accepted SHA-256
policy, and each role's actual binding must match its corresponding accepted
hash.  The normalizer interpreter must be the interpreter running the
orchestrator, with the same resolved path and current executable hash.
Human-readable identities are accepted only after those relational checks.
Local source hashes are discovered at initialization rather than treated as
trusted constants.  Every phase rechecks the complete source set and the full
tool-policy relationship before and after its child.

## Resource and interruption policy

Only one child is active.  The shared campaign heavy-child lock and the
per-run lock both fail closed.  Defaults cap every child at 2 GiB memory and
every individual output file at 2 GiB.  Before each child the runner requires:

- one-minute load at most 7.5;
- reclaimable memory at least the child ceiling plus 2 GiB;
- free disk sufficient for five maximum-sized live files plus an 8 GiB
  post-run reserve and 64 MiB metadata allowance.

This five-file accounting is intentionally conservative.  With roughly
19 GiB free at the present checkpoint, a retained raw proof of around 1 GiB
may make the next postprocessing gate refuse to launch.  That refusal is a
safe retryable nonclaim; it is not a reason to reduce the 8 GiB reserve.

The exact command for all six phases is written before the first child.
Checkpoint `RUNNING_UNFINISHED_NONCLAIM` is durable before launch.  Each
completed child immediately gets a record containing exact argv, executable
hash before and after, exit/signal state, wall time, user/system CPU, RSS,
limits, and stdout/stderr hashes.

An interrupted attempt cannot silently resume.  `run --recover-interrupted`
only records a retryable nonclaim, and is allowed only after the operator has
checked that no child from the old attempt remains active.  A later `run`
starts a fresh exclusive attempt directory.

Checkpoint bindings are relational, not free-standing hash references.
Attempt `j` must bind exactly
`attempts/attempt-j/attempt-config.json`, and its terminal checkpoint must bind
exactly that attempt's `outcome.json`.  Checkpoint sequence, event, attempt
count, directory count, and outcome status are cross-checked.  In particular,
`INTERRUPTED_RECOVERED` can only produce checkpoint
`RETRYABLE_NONCLAIM` and outcome
`INTERRUPTED_ATTEMPT_RECOVERED_NONCLAIM`; it can never promote a success or
candidate.  External or traversal paths, missing or extra outcomes, and
malformed claim-status mappings are audit failures.  An ordinary audit also
rejects an attempt directory created before its `RUN_STARTED` checkpoint.
After the operator confirms that no child remains active, explicit recovery
moves exactly that next-numbered orphan directory intact into a new exclusive
sibling quarantine directory and returns a retryable nonclaim without
launching a child.  The run tree is then auditable again, and a later ordinary
`run` starts the same attempt number from fresh bytes.  Empty, instance-only,
and complete-config precheckpoint crash windows are all handled this way.

Every attempt-local formula must also have exactly the size and SHA-256 of the
run-level frozen formula.  Its path remains the distinct canonical path inside
that attempt.  This content relation is checked both immediately after copying
and in every later audit; refreshing an attempt configuration cannot substitute
a different CNF beneath the frozen template label.

A crash can also occur while `outcome.json` is being written or after it is
durable but before its terminal checkpoint.  Explicit recovery treats any
such bytes as opaque: without parsing or promoting them, it moves the file
intact into a new exclusive sibling quarantine directory, writes a canonical
`INTERRUPTED_ATTEMPT_RECOVERED_NONCLAIM` outcome, and appends
`INTERRUPTED_RECOVERED` with status `RETRYABLE_NONCLAIM`.  The external
quarantine contains a canonical move record and preserves the original bytes
for manual inspection.  A later attempt starts fresh.  Ordinary audit rejects
both partial and complete uncheckpointed outcomes.

The process launcher is the existing `synthesis_k3.cegar.run_bounded_child`.
Its complete import-time local dependency set is hash-bound in each run
manifest: `synthesis_k3/__init__.py`, `encoding.py`, `coloring.py`,
`generate.py`, and `cegar.py`.  Before freezing this runner, its local tests
were rerun for exact command/log/CPU/RSS records, the macOS RSS kill gate,
direct/symlink/hard-link role collisions, the campaign-wide child lock, and
signal cleanup.  The production wrapper also checks its returned command hash,
executable hash before and after, exact limits, timestamps, CPU/RSS fields, and
stdout/stderr bindings before accepting any phase.

## Required UNSAT chain

The only successful chain is:

1. CaDiCaL returns exit 20, writes strict `s UNSATISFIABLE`, and retains a
   nonempty raw binary DRAT stream.
2. drat-trim reinterprets the raw stream in deletion-agnostic plain mode and
   checks every addition forward with `-i -f -p -W -U`.  Thus pseudo-unit
   deletion hints cannot create checker-specific warnings, while every
   retained addition must be RUP.  The `-W` flag requests warning-fatal
   checking, and the runner independently rejects nonzero exit, any stderr,
   any warning or error text, or anything other than exactly one clean
   `s VERIFIED`.
3. The bound normalizer parses the entire canonical binary stream, requires a
   unique empty addition and no later additions, strips deletions, and emits
   the exact addition stream whose final record is the unique empty addition.
4. A fresh drat-trim process checks the normalized stream forward with
   `-i -f -W -U`, making the retained stream RUP-only and subject to the same
   independent clean-output policy.
5. A separate drat-trim process performs backward RUP-only LRAT conversion
   with `-i -W -U -L`; the LRAT file must be nonempty.
6. The separately hash-bound lrat-check executable replays the LRAT against
   the frozen formula; stderr must be empty and stdout must contain exactly one
   clean `c VERIFIED`.

The soundness of plain mode here does not depend on the semantic validity of
any deletion hint.  Ignoring every deletion defines a new proof sequence
consisting of the original formula followed by the additions in their original
order.  With `-U`, drat-trim requires each such addition to be RUP relative to
the original formula and all preceding retained additions.  Every RUP addition
preserves satisfiability, and the final empty addition therefore proves the
original formula unsatisfiable.  The strict normalizer independently emits
that exact addition sequence, and phase 4 checks it again.  Hence an ignored
pseudo-unit deletion cannot weaken the checked formula or create an accepted
lemma.

Each child is retained inside an exact-shape phase record.  In addition to the
child argv, executable, resource, and stdout/stderr data, that record binds
every read-only input by canonical path, size, and SHA-256 both before and
after execution.  It also binds the immediately produced solver result, raw
proof, normalized proof/report, or converted LRAT where applicable.  Thus the
final LRAT named by the certificate must be the same bytes recorded as input
to lrat-check, and the raw and normalized proof stages have the analogous
crosslinks.

Only after all six phases does the runner write
`UNSAT_LRAT_VERIFIED_PENDING_HOSTILE_AUDIT`.  The read-only `audit` operation
then revalidates the checkpoint chain, every artifact hash, exact commands,
resource reports, child records, normalization transform, success markers,
and certificate bindings.  It does not itself freshly execute lrat-check, and
reports that limitation explicitly.

The run manifest has an exact key set and an initialization-only nonclaim
status.  Positive timestamp and hardware fields and exact normalized
invocations are required; coordinated rehashing cannot introduce extra claim
metadata.  The success certificate itself also has an exact key set, an exact
non-global claim boundary, and an outcome details object containing exactly
that certificate.  A SAT terminal state is likewise reconstructed from the complete
solver assignment, checked against the frozen CNF and direct graph/game
semantics, and tied to a clean solver resource gate before it is accepted even
as candidate-only.

## CLI

From the campaign root:

```text
PYTHONPATH=src python3 -m search.order13_k3.production initialize \
  --package-directory <AUDITED_CONSTRUCTOR_PACKAGE> \
  --run-directory results/order13_k3_hole9_production \
  --cadical tools/cadical_3_0_1/build/cadical \
  --drat-trim tools/drat_trim_2023_05_22/drat-trim \
  --lrat-check tools/drat_trim_2023_05_22/lrat-check \
  --validation-gate

PYTHONPATH=src python3 -m search.order13_k3.production run \
  --run-directory results/order13_k3_hole9_production \
  --production-gate

PYTHONPATH=src python3 -m search.order13_k3.production audit \
  --run-directory results/order13_k3_hole9_production
```

No production command may be launched until the independent constructor and
graph-to-CNF audits accept the exact bytes.
