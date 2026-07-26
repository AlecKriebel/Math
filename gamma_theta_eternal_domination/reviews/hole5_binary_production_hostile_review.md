# Hostile review of the `hole5` binary production runner

## Verdict

**ACCEPT FOR COMMIT, WITH A MANDATORY POST-COMMIT HEAD GATE.**

The frozen runner is fail-closed at the boundaries reviewed here.  It may be
used for one bounded production attempt only after the exact audited files are
committed on `main`, the current repository HEAD is independently recorded,
and the runner confirms that every declared runtime source has exactly its Git
object bytes at that HEAD.  Until that post-commit check passes, this review
does **not** authorize a solver launch.

No production solver was launched during this audit.  The mocked UNSAT tests
used only an eleven-byte binary-DRAT fixture and the already-audited clean-room
parser.  This review makes no SAT or UNSAT claim for the retained `hole5`
instance and no claim about the universal gamma--theta conjecture.

Review date: 2026-07-25 PDT.

This is the second frozen-byte audit.  It supersedes the earlier runner,
test, probe, log, and review hashes.

## Frozen target bytes

| artifact | bytes | SHA-256 |
|---|---:|---|
| `src/synthesis_k3/hole5_binary_production.py` | 54,328 | `02e8a13d806593017071ca0ad89680ece8c947e0c24d7579e6a779bc25ba044f` |
| `tests/test_hole5_binary_production.py` | 24,425 | `e622ef081da50fa7f6dc917f3b0af76f3cda34a67e5642128779b47e8c234072` |
| `reviews/hole5_binary_production_hostile_probe.py` | 34,907 | `06261bbc95c30e84c2fa459a7694e23400d9f35c1d996949794cdbc8b66fa00d` |
| `reviews/hole5_binary_production_hostile_probe_log.json` | 13,336 | `f9ca64c9b4c884b465aa7a5d6ab21e11ffb36215e266394a5aad0f9ae306b0d3` |

The probe log is canonical JSON and was reproduced byte-for-byte by a second
stdout-only execution.  It records
`ACCEPT_FOR_COMMIT_WITH_POSTCOMMIT_GATE` and
`production_solver_launched=false`.

The runner predeclares the probe, log, and this review in
`RUNTIME_SOURCE_RELATIVE_PATHS`.  Thus changing any of these audit artifacts
after the production commit makes `runtime_sources_match_head` false and
blocks the run.  The current pre-commit/untracked state intentionally cannot
pass that gate.

## Exact retained inputs and tools

The runner independently reconstructs and audits the retained formula before
creating an output directory.  The accepted identities are:

| role | SHA-256 |
|---|---|
| retained CNF | `c6a0811c718ff8e9352f253e4ce225ce2826def9c3e4a9cd55f0b0152703d104` |
| signature breaker | `62ce8f60ecfe74f58bcd113166009637f854d7d663aea2e59395ae224682d18a` |
| retained manifest | `da33bc1708f7d21b92ceedc68710d5433a1aacbe6e32b8a7432bbab45d8cc788` |
| source full-bank CNF | `76bf36ecb663cd37272acded2208206fdba6aa571dd5f2e757cc132bd533e0b7` |
| source coloring bank | `b3c24db61e7a33c3d8803e2bbadcdda92b950fb04445e59e7930330e92b74a00` |
| source manifest | `99a56197074ad3373691578527e41baff4d76eb1e86141366c4edf8bc5871402` |
| CaDiCaL 3.0.1 binary | `51c3c82b354f455c925fc60b37c701e8498afcf0f3bfab9a06e62149485df5f6` |
| CaDiCaL source archive | `2dccd6ecc1878348dd70194d51df6b69006bf86439b5b3c395a5c5dd8863201e` |
| `drat-trim` binary | `31df522b8b2b71acd357723b0e826cf488826ed78ad9e3a7bcad241271812beb` |
| `drat-trim` source archive | `2ac28cd9e38e050b4f78fbff0efd4a1aa2349d157aef08c9b1fb6c7139949108` |
| clean-room binary parser | `02c3c00faf7afb91a3217f5b738d0dacf7699875928162d01ce2df97e600007d` |
| parser hostile log | `2674cf53eecd881535c6bc4bc2732d669562d7a86816e7bc9057222aadeb3ca8` |
| retained-package hostile review | `b675ed1ba1e83a37069af4f3f526a98b3c627d1133300b1e5764fe933fa7b5ed` |

The derived formula has exactly 6,886 variables, 23,968 clauses, and 192,169
literals.  The input-package paths are read-only bindings, and an output path
inside either package is rejected before creation.

After the pre-existing pinned-tool verifier succeeds, the production runner
performs a second gate using its own four hard-coded expected hashes and the
separately source-bound streaming hash implementation in
`template_color_bank.py`.  It rehashes both binaries and both source archives
and compares both the fresh bytes and the returned binding records.  The
hostile probe independently recomputed all four hashes with its own
`hashlib` implementation.  It then changed each copied artifact's bytes and
each binding hash field separately; all eight mutations were rejected.

## Complete local import closure

An independent recursive AST walk began with the production module and package
initializer, followed every static relative or `synthesis_k3` import, and
found exactly these eight executed local modules:

```text
src/synthesis_k3/__init__.py
src/synthesis_k3/cegar.py
src/synthesis_k3/coloring.py
src/synthesis_k3/encoding.py
src/synthesis_k3/generate.py
src/synthesis_k3/hole5_binary_production.py
src/synthesis_k3/hole5_signature_breaker.py
src/synthesis_k3/template_color_bank.py
```

All eight are present in `RUNTIME_SOURCE_RELATIVE_PATHS`.  No dynamic import,
`exec`, or `eval` surface was found.  In particular, the formerly implicit
`coloring.py` and `generate.py` dependencies are now source-to-HEAD bound;
their hashes are respectively
`9791599aaca6b9f7ec5e6fed8cfce41a5c5bec825a350e5e493a0d1aa06d3713`
and
`456029e08a199e3cc8d4aa6070e3209d6884901fc6c3db8486b80862614430e1`.
The frozen regression test independently repeats the recursive closure walk.

## Commands and proof boundary

The normalized solver invocation contains the exact options

```text
--seed=N --binary --no-colors -q -t SECONDS -w RESULT CNF RAW_PROOF
```

with `0 <= N <= 2,000,000,000`, the documented CaDiCaL seed range.  Larger
values, negative values, booleans, and non-integers fail before the output
directory is created.

The clean-room parser is a bounded child under an isolated Python interpreter:

```text
python -I -B PARSER strip --proof RAW --output ADDITIONS --max-var 6886
```

The runner requires canonical parser JSON, empty parser stderr, exact hashes
and sizes for both proof streams, one final empty addition, no record after it,
internally consistent record/byte/addition/deletion counts, no variable above
6,886, zero deletions in the stripped stream, and exact preservation of every
addition byte in order.  The probe changed eight independent report fields;
all eight mutations were rejected before acceptance.

The only accepted checker command is:

```text
drat-trim CNF ADDITIONS -i -f -W -U -t SECONDS
```

Acceptance requires exit zero, empty stderr, ASCII output, no warning
substring, exactly one `s VERIFIED` status, and exactly one report beginning
with the exact integer zero in `c 0 RAT lemmas in core`.  The semicolon suffix
is allowed only to tolerate the pinned checker's redundant-literal statistic;
nonzero/ambiguous RAT counts, duplicate RAT reports, duplicate or wrong
statuses, warnings, stderr, and non-ASCII bytes were all rejected.

The raw binary proof is hashed before parsing, remains a read-only child input,
is checked after parsing and replay, is never replaced by the stripped proof,
and is included separately in the certificate.  The addition-only proof is
reparsed by the independent parser and accepted mathematically only after
binary, forward, warning-fatal, RUP-only replay.

## Post-write and claim-boundary audit

Three hostile end-to-end mocked mutations were injected after initial
structured-artifact creation:

| mutation | terminal status | claim status | activation artifact map |
|---|---|---|---|
| change certificate to assert a standalone claim | `FINAL_OUTPUT_VALIDATION_NONCLAIM` | `NO_MATHEMATICAL_CLAIM` | empty |
| change SAT candidate to assert a counterexample | `FINAL_OUTPUT_VALIDATION_NONCLAIM` | `NO_MATHEMATICAL_CLAIM` | empty |
| change run configuration to clear the hostile gate | `FINAL_OUTPUT_VALIDATION_NONCLAIM` | `NO_MATHEMATICAL_CLAIM` | empty |

The runner freezes canonical bytes for the run configuration, SAT candidate,
and replay certificate; rechecks them before the outcome; revalidates the
final SAT model or UNSAT replay artifacts as applicable; and compares two
complete output-artifact maps around final validation.  A replay certificate
explicitly has `NO_STANDALONE_MATHEMATICAL_CLAIM`; it activates only through a
matching final outcome whose artifact map binds the certificate hash.

SAT is always `CANDIDATE_ONLY`, even after a complete satisfying assignment is
checked against the exact CNF.  Every timeout, memory limit, file limit,
signal, unexpected exit, malformed result, parser/checker failure, warning,
input mutation, output mutation, or incomplete phase is a nonclaim.  The
probe enumerated 22 terminal status literals and exercised timeout, memory,
file-limit, and signal classification independently for solver, parser, and
checker phases.

## Resource and filesystem audit

The runner permits at most:

- 3,600 seconds for the solver;
- 1,800 seconds for each post-processing phase;
- 4,096 MiB per child and no more than 25% of detected physical RAM;
- 600 MiB per child-created file;
- one campaign-wide heavy child at a time;
- a 4,096 MiB free-disk reserve plus conservative remaining-file slots.

The exact inherited child supervisor,
`src/synthesis_k3/cegar.py`, has SHA-256
`411fffff34c0122d679ee710aff0e3856a7ff166bff30c69edb1f0044defce8c`,
the same bytes accepted by its prior hostile review.  A focused live
non-solver test reconfirmed that its campaign-global lock rejects a second
child and that signal cleanup leaves no descendant.

All decisive runs use a new mode-0700 output directory.  Existing directories,
symlinked components, protected source trees, and children of input packages
are refused.  Structured files use exclusive creation.  Every immutable input
is a regular, single-link file whose size and hash are rechecked after child
execution and during final output validation.

## Test results

The exact frozen production test file passed:

```text
Ran 13 tests in 50.945s
OK
```

The focused campaign-lock test passed:

```text
Ran 1 test in 0.164s
OK
```

The standalone hostile probe passed twice with byte-identical canonical output.
It performed no production solve.

## Mandatory post-commit gate

Before any production launch, all of the following remain mandatory:

1. Commit the exact runner, tests, probe, log, and review bytes on `main`.
2. Record the resulting commit ID and confirm that the working copies of every
   `RUNTIME_SOURCE_RELATIVE_PATHS` entry equal their Git objects at that commit.
3. Supply that exact current commit ID as `--expected-head`.
4. Recheck the four frozen hashes in the first table and record this review's
   post-write hash.
5. Confirm the exact retained package, pinned tools, available-memory gate,
   disk gate, and absence of another campaign heavy child immediately before
   launch.

If any one of these conditions fails, the launch is not authorized.
