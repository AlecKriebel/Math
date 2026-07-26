# Hostile review: repaired order-12, parameter-four production runner

**Verdict:** `ACCEPT_PRODUCTION_READY_ENGINEERING_NO_AGGREGATE_CLAIM`

This accepts the frozen runner as a fail-closed, bounded, resumable engine for
producing the sixteen leaf artifacts.  It does **not** certify any leaf as
SAT or UNSAT, does not establish the order-12 parameter-four slice, and does
not resolve the gamma-theta conjecture.  No production leaf solve was launched
during this review.

## Frozen scope

| author artifact | SHA-256 |
|---|---|
| `src/search/k4_production/runner.py` | `8c1939ed18a89f0afd735958da1a84dbaece1ac4507a5b3dcccf84cbb019642e` |
| `tests/test_k4_production.py` | `87250792bd9a588b9e1c9403c2b124092c368aec570d525045c2a46c2bb0107c` |
| `math/lemmas/order12_k4_partition_plan.md` | `132a1d41c11466b7f4af641049dd7ff10c4622f055d315831254da9978ee1578` |
| `src/search/k4_production/__init__.py` | `d217fa6af4e7273a80cc63ee8ac812e83b6ce8ed64585fef6d2ef8a371dd2c67` |
| `src/search/k4_production/__main__.py` | `a5d3245ca5614aa7b566a1a182d03b48fbc3c40c3ade4d56d9d8114b5dcb432d` |

The final hostile probe is
`reviews/order12_k4_production_hostile_probe.py`, SHA-256
`720e78ac264b3a79f99351e18b84d4284bf702fd0c16fc69a4cf9b079738729e`.

## Defect history and repair verification

The first frozen version was **rejected**.  Its relevant hashes were runner
`3926d909...`, tests `4fb1c11a...`, and partition note `df5bdb96...`.
Hostile execution found four concrete problems:

1. It combined `drat-trim -i -f -W -L`.  The pinned converter printed
   `s VERIFIED` but also said optimized proofs were unsupported in forward
   mode.  It emitted the six-byte LRAT `4 d 0`, which the pinned
   `lrat-check` rejected because no empty clause was reached.
2. A crash after durable attempt-directory/config creation but before the
   reservation checkpoint left an orphan directory that both audit and
   recovery rejected.
3. A crash after durable `outcome.json` but before the completion checkpoint
   likewise left a run that neither audit nor recovery could advance.
4. The public Python API accepted a caller-supplied child runner, and the
   reservation checkpoint's attempt-config digest was not enforced.

The final bytes repair all four:

- raw proof checking and LRAT production are now distinct pinned processes;
- both write-order tears have explicit append-only, nonclaim reconciliation;
- every attempt configuration is reconstructed and checked against its
  checkpoint digest;
- `run_next_case` has no public child-runner injection parameter.

After that engineering acceptance, a real initializer exposed a fifth,
narrow integration defect in runner
`4e65bc62df18e9bd3a7b17810da00f472a1afda21c6d87c1f13a0d06dba635af`.
The campaign is a subdirectory of a larger Git worktree, but both runtime
source lookups used `HEAD:src/...`, which Git interprets from the repository
root.  The old command returned 128 and Git itself suggested the correct
campaign-relative spelling `HEAD:./src/...`.  Frozen runner
`8c1939ed18a89f0afd735958da1a84dbaece1ac4507a5b3dcccf84cbb019642e`
uses that spelling at both creation and verification sites.  The clean-room
probe reproduced the old failure, matched the corrected revision blob to
`git hash-object`, and successfully created and reverified a real source
binding without mocking Git.  The new unmocked regression does the same.

This repair preserves the intended provenance gate: the runner's own new
bytes must be committed before full initialization can succeed.  At review
time `HEAD` still named blob `3e1ba20e...` while the reviewed runner named
worktree blob `1360c935...`, so full initialization correctly failed with
“runtime source is not committed byte-for-byte.”  This is a mandatory staging
prerequisite, not a logic defect in the repaired lookup.

The final clean-room crash probes reproduce each old interruption point.  The
first now ends as `ORPHAN_ATTEMPT_RECONCILED_NONCLAIM`; the second ends as
`OUTCOME_CHECKPOINT_RECONCILED_NONCLAIM`.  Both preserve the attempt bytes,
require a no-live-child process-table check, make the case retryable, and pass
a full read-only audit afterward.  Mutation of an active config makes both
audit and recovery refuse to act.

## Exact 16-leaf coverage

The parent bytes independently parse as:

- SHA-256
  `adbe0c01614bae6cd3aed4ccdcd45a757ca56e7ef9c4f2f280f2d8ef200e40ac`;
- 18,381 variables;
- 114,742 clauses;
- 1,180,016 literals.

The clean-room probe reconstructed the lexicographic edge layout and confirmed
that variables \(4,14,23,31\) are
\(e_{0,4},e_{1,4},e_{2,4},e_{3,4}\).  It enumerated all sixteen truth
assignments, changed only the parent clause count, appended the four exact
unit clauses, and matched every recorded leaf size and SHA-256.  Each of the
sixteen assignments hits exactly one cube.  Dropped-case, duplicate-cube,
literal-flip, and leaf-hash mutations all failed closed.

Thus the concrete coverage identity is correct.  This says only that all
sixteen verified-UNSAT leaves would imply parent UNSAT; it does not say that
any leaf has yet been solved.

## Four-stage proof chain

The frozen pipeline identifier is
`binary-drat-forward-check-backward-lrat-v2`:

1. pinned CaDiCaL receives `--binary`, a fixed seed, the exact leaf CNF, result
   path, and raw proof path;
2. pinned `drat-trim` independently checks that binary proof with
   `-i -f -W`, expressly without `-L`;
3. a fresh pinned `drat-trim` process converts the same CNF/proof with
   `-i -W -L`, expressly without `-f`;
4. separately pinned `lrat-check` replays the resulting LRAT against the same
   leaf CNF.

On a real two-variable UNSAT instance, the exact four commands returned
`[20,0,0,0]`.  The raw binary DRAT was nonempty, backward conversion produced
a 40-byte LRAT with SHA-256
`11fae57fd8e8c4c1234067c683dc2ea7721064a6886298f023496a132692a715`,
and `lrat-check` returned one clean `c VERIFIED`.  A truncated LRAT and empty
raw proof were rejected.  The old combined `-f -L` command was also rerun and
remains rejected, preserving the original defect as a regression test.

Warning, duplicate-status, stderr, non-VERIFIED, timeout, signal, memory,
file-limit, and missing-artifact paths remain nonclaims.  Certificate and
outcome inventories bind the exact CNF, result, raw proof, both drat-trim
records/log pairs, LRAT, checker record/logs, resource reports, configuration,
and certificate.

## SAT, bindings, resources, locks, and cleanup

A SAT solver result is accepted only with one complete assignment over all
declared variables that satisfies every exact leaf clause.  Incomplete and
falsifying models and duplicate status records were rejected.  Even a valid
model freezes the run only as
`SAT_CANDIDATE_PENDING_INDEPENDENT_VERIFICATION`; it is not treated as a
counterexample.

The manifest binds retained parent and generator bytes, partition, committed
runtime Git blobs and SHA-256 values, pinned binaries and source archives,
hardware, seeds, limits, and normalized resume invocation.  Direct file,
tool-record, completed-LRAT, and active-config tampering all failed closed.
Writes are exclusive and directory-fsynced; checkpoints are append-only and
hash-linked.

Before each of the four children, the runner checks load, reclaimable memory
against child plus reserve, physical-memory fraction, and free disk against
reserve plus eleven file-limit slots.  The inherited bounded-child core holds
both a per-run lock and campaign-wide heavy-child lock, uses a separate
process group with wall/CPU/memory/file limits, and terminates and reaps the
whole group on timeout or orchestrator termination.  The real spawned-
grandchild timeout regression passed.

## Test and probe results

I independently reran the frozen author suite: **18/18 passed** in 58.132
seconds of unittest wall time (58.25 seconds process wall), with maximum RSS
117,981,184 bytes and peak memory footprint 106,152,464 bytes.  The separate
hostile probe completed in 23.795 seconds.  Exact commands and outcomes are in
`reviews/order12_k4_production_hostile_probe.log`.

## Mandatory claim boundary

Ordinary `audit_run` deliberately reports `proofs_freshly_replayed: false`.
Even sixteen leaf states equal to `UNSAT_LRAT_VERIFIED` aggregate only to

`ALL_LEAVES_VERIFIED_PENDING_INDEPENDENT_COVERAGE_AUDIT`.

A negative finite theorem still requires a separate checker that binds the
frozen parent, reconstructs all sixteen leaves, freshly replays every LRAT,
and audits the concrete coverage manifest.  A SAT leaf still requires the
standalone candidate verifier and the full graph-parameter certificates.
This engineering acceptance cannot be cited as a mathematical result.
