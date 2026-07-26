# Certified-production partition for the exact order-12, parameter-four target

## Claim boundary

This note proves the coverage identity used by the production workflow for
the exact connected \((n,k)=(12,4)\) parent formula.  It does **not** say
that the parent or any leaf is satisfiable or unsatisfiable.  No production
solver run has been made.

The parent is
`instances/order12_k4_connected_parent/instance.cnf`, with SHA-256

```text
adbe0c01614bae6cd3aed4ccdcd45a757ca56e7ef9c4f2f280f2d8ef200e40ac
```

and exact census

```text
18,381 variables; 114,742 clauses; 1,180,016 literals.
```

Its edge variables describe \(H=\overline G\).  The exact mathematical
meaning of the parent, including the one-guard transition clauses, is proved
in `order12_k4_synthesis_target.md`.

## The 16 disjoint cubes

The edge variables were allocated in lexicographic order on pairs.  In the
parent DIMACS numbering,

| variable | graph meaning |
|---:|---|
| \(4\) | \(e_{0,4}\) |
| \(14\) | \(e_{1,4}\) |
| \(23\) | \(e_{2,4}\) |
| \(31\) | \(e_{3,4}\) |

Write these variables as \(x_0,x_1,x_2,x_3\).  For
\(b=(b_0,b_1,b_2,b_3)\in\{0,1\}^4\), let

\[
 C_b=\bigwedge_{j=0}^3
 \begin{cases}
 x_j,&b_j=1,\\
 \neg x_j,&b_j=0.
 \end{cases}
\]

The production partition contains all 16 bit strings, including \(1111\).
The latter leaf is deliberately retained even though the anchored
\(H\)-\(K_4\), together with \(x_0=x_1=x_2=x_3=1\), makes
\(\{0,1,2,3,4\}\) an \(H\)-\(K_5\).  Keeping it makes coverage a direct
Boolean identity rather than an optimization that depends on simplifying
the parent.

### Coverage lemma

For every CNF \(F\), and in particular for the frozen parent,

\[
 F\ \equiv\ \bigvee_{b\in\{0,1\}^4}(F\wedge C_b).
\]

Moreover, the 16 disjuncts are pairwise inconsistent.

**Proof.**  Every total Boolean assignment gives the four named variables
one unique bit string \(b\), and hence satisfies exactly one cube \(C_b\).
If it satisfies \(F\), it therefore satisfies exactly one displayed
disjunct.  Conversely, every displayed disjunct contains \(F\).
Distinct bit strings disagree in some coordinate, so their cubes contain
opposite literals of the corresponding variable. \(\square\)

It follows that the parent is UNSAT if and only if all 16 leaf formulas are
UNSAT.  In DIMACS, a leaf is formed by changing only the clause count in the
parent header and appending the four cube literals as unit clauses.  Thus
every leaf has 18,381 variables, 114,746 clauses, and 1,180,020 literals.
The initializer records the exact SHA-256 of every resulting leaf.

This proof does not use the Strong Perfect Graph Theorem, the no-\(K_5\)
shortcut for \(1111\), a heuristic symmetry assumption, or a claim that the
16 leaves have similar computational difficulty.

## Leaf outcome protocol

Each case is append-only and may be retried after an interrupted or
resource-limited attempt.  No previous raw artifact is overwritten.

1. A pinned CaDiCaL executable receives one fixed seed and writes both its
   raw result file and raw binary DRAT proof.
2. A `SATISFIABLE` result is parsed as a complete assignment and checked
   against every clause of the exact leaf CNF.  Even after that check its
   status is only `SAT_CANDIDATE_PENDING_INDEPENDENT_VERIFICATION`.  It is
   not a counterexample certificate.
3. An `UNSATISFIABLE` result is not accepted by itself.  The pinned
   `drat-trim` first verifies the retained raw binary DRAT proof under
   `-i -f -W`.  This is a warning-fatal **forward** proof check and does not
   request or produce LRAT.
4. A separately bounded, source-bound normalizer parses the complete binary
   proof with canonical bounded varints.  It requires exactly one empty
   addition, permits only deletions after that record, strips all deletions,
   and writes `proof.normalized.rup.bdrat` plus an exact hash-and-count report.
   This transformation by itself makes no proof claim: retaining a deleted
   clause can make a later RAT step fail.
5. A fresh pinned `drat-trim` process verifies the normalized addition-only
   stream under `-i -f -W -U`.  The explicit `-U` makes every retained
   addition pass the stronger RUP-only check, closing the soundness gap in
   deletion stripping.
6. Another fresh pinned `drat-trim` process reads the same leaf CNF and
   normalized stream under `-i -W -U -L`, without `-f`.  This separate
   **backward** pass must itself return exactly one clean `s VERIFIED` and
   produce a nonempty `proof.converted.lrat`.
7. A separately pinned `lrat-check` executable replays that exact LRAT file
   against that exact leaf CNF.  Only then may the leaf status become
   `UNSAT_LRAT_VERIFIED`.
8. Timeouts, signals, malformed output, missing files, warnings, hash
   changes, and resource-gate failures are nonclaims.

The distinction between forward verification and backward conversion is
essential for the pinned tools.
On a real two-variable UNSAT regression, LRAT emitted by the combined
forward `-f -L` mode is rejected by the pinned `lrat-check`, whereas the
separate backward conversion is accepted.  The production protocol is
therefore identified as
`binary-drat-raw-forward-normalize-rup-forward-backward-lrat-v3`.

The decisive leaf inventory binds the exact files
`instance.cnf`, `solver.result`, `solver.stdout`, `solver.stderr`,
`proof.raw.bdrat`,
`raw-forward.stdout`, `raw-forward.stderr`,
`normalizer.stdout`, `normalizer.stderr`,
`normalization-report.json`, `proof.normalized.rup.bdrat`,
`normalized-forward.stdout`, `normalized-forward.stderr`,
`lrat-conversion.stdout`, `lrat-conversion.stderr`,
`proof.converted.lrat`, `lrat-check.stdout`, `lrat-check.stderr`,
the six per-phase resource reports, `attempt-config.json`, and
`certificate.json`.  The attempt outcome binds every retained file by path,
size, and SHA-256.  The certificate separately binds all six child records,
resource reports, decisive proof artifacts, and logs; no successful phase
substitutes for another.

Even if all 16 leaf statuses become `UNSAT_LRAT_VERIFIED`, the workflow
labels the aggregate only
`ALL_LEAVES_VERIFIED_PENDING_INDEPENDENT_COVERAGE_AUDIT`.  A publication
claim requires a separate checker to bind the parent, reconstruct the 16
leaf CNFs, replay their proofs, and verify the coverage lemma's concrete
manifest.

## Resume and resource discipline

The immutable run manifest binds the exact parent bytes, parent generator
manifest, runtime-source Git blobs and SHA-256 values, the three proof-tool
executables, the Python normalizer runtime, tool-source archives, hardware
report, fixed seeds, and limits.
The partition is immutable.  State changes are new numbered checkpoint
files linked by SHA-256; no checkpoint is overwritten.

Every reservation checkpoint binds the exact SHA-256 of its
`attempt-config.json`, and read-only audit compares that binding with the
active or completed file as well as reconstructing every frozen command.
The public `run-next` API always invokes the pinned bounded-child
implementation; it has no caller-supplied child-runner hook.

Two durable-write crash windows have explicit, fail-closed reconciliation:

- an attempt directory and configuration written before its reservation
  checkpoint is recorded as
  `ORPHAN_ATTEMPT_RECONCILED_NONCLAIM`; and
- an outcome written after reservation but before its completion checkpoint
  is recorded as
  `OUTCOME_CHECKPOINT_RECONCILED_NONCLAIM`.

In both cases all bytes are preserved, the exact configuration and remaining
checkpoint chain are audited, the process table must show no child naming
the attempt directory, and a new append-only checkpoint makes the case
retryable.  A torn decisive outcome is deliberately **not** promoted; it
must be rerun in a new exclusive attempt directory.  A mutation or any
layout other than these exact one-attempt tears makes recovery refuse to
act.

Before each of the four child processes, the runner checks:

- one-minute load average against the stored ceiling;
- currently reclaimable memory against the child limit plus a reserve;
- each child memory limit against 75% of physical RAM;
- free disk against a retained reserve and the worst-case live proof/log
  budget; and
- exclusive campaign and per-run locks.

Each child runs in its own process group under wall, CPU, memory, and
per-file limits.  Timeout or an orchestrator termination signal terminates
and reaps the process group.  The campaign-wide heavy-child lock is shared
with the earlier production runner, so the laptop does not intentionally run
two proof jobs from this campaign at once.

The first version implements only the 16 top-level cubes.  A future
refinement of a hard leaf is sound only if the parent leaf is replaced by
both children \(C\wedge y\) and \(C\wedge\neg y\), with both recorded in a
new coverage manifest.  Dropping one child because it appears unpromising
would be unsound and is not implemented here.
