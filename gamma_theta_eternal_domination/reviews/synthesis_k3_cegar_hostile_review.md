# Hostile audit of the proof-producing \((12,3)\) CEGAR runner

## Final verdict

**ACCEPT for bounded production**, 2026-07-25.

This verdict applies only to the frozen bytes listed below.  The repaired
runner correctly implements the named template instances, rejects every
previously demonstrated forged-history or forged-terminal attack, and has
adequate fail-closed resource and checkpoint controls for the laptop
campaign.  No critical-, high-, or medium-severity defect remains.

An accepted runner is not a negative result.  A template is excluded only
after it reaches `unsat_verified` and its retained final CNF and DRAT proof
pass a publication audit with both `--deep-reconstruct` and
`--verify-terminal-proof`.  Excluding the whole \((n,k)=(12,3)\) slice also
requires the separately accepted template-coverage theorem and a verified
terminal for every required template.

## Frozen review boundary

| Artifact | SHA-256 |
|---|---|
| `src/synthesis_k3/cegar.py` | `411fffff34c0122d679ee710aff0e3856a7ff166bff30c69edb1f0044defce8c` |
| `tests/test_synthesis_k3_cegar.py` | `56101dee36685e476ace516fc30b31f7f0d3dc2a5efd11b3e25387038b0146fb` |
| `math/synthesis_k3_cegar_protocol.md` | `c51db6d865557f4dcc3147772dbaa1c86d3c6c6d3544ab0090f0f89267a9de31` |
| complete runtime source set | `8c4e811bc4250c3e2b0b7edeb8afd07f7509ebda3cbae3db1b3ca82c07b35299` |
| `src/synthesis_k3/encoding.py` | `fda94aeb7a2c48e64f1b9a975c27263b100542359c13264f4a625f115ff563c6` |
| `src/synthesis_k3/coloring.py` | `9791599aaca6b9f7ec5e6fed8cfce41a5c5bec825a350e5e493a0d1aa06d3713` |
| `src/synthesis_k3/generate.py` | `456029e08a199e3cc8d4aa6070e3209d6884901fc6c3db8486b80862614430e1` |
| `math/synthesis_k3_cegar_design.md` | `57d82b9dabdc9c8f66950a3f9c483f3cb58e35a11e243a8880c173b5724a09b8` |
| pinned CaDiCaL binary | `51c3c82b354f455c925fc60b37c701e8498afcf0f3bfab9a06e62149485df5f6` |
| pinned DRAT-trim binary | `31df522b8b2b71acd357723b0e826cf488826ed78ad9e3a7bcad241271812beb` |
| final hostile probe | `b622bb361e2fc5976d41a06040cbf87ebd827151fae044ef42381e5bf907d6ba` |

The probe checks these three primary artifact hashes and the complete runtime
source-set hash before doing any work.  The frozen source, test, and protocol
files were not modified during this review.

## Executed checks

The focused CEGAR suite passed **23/23** tests in 14.908 seconds:

```text
PYTHONPATH=src python3 -m unittest -v tests.test_synthesis_k3_cegar
```

The complete campaign suite passed **218/218** tests in 27.153 seconds:

```text
PYTHONPATH=src python3 -m unittest discover -s tests -v
```

The final hostile probe completed in 9.895 seconds and returned
`"verdict": "ACCEPT"`:

```text
PYTHONPATH=src python3 reviews/synthesis_k3_cegar_hostile_probe.py
```

Its acceptance gates all passed:

- frozen source and tool bindings;
- independent complement, static-template, domination, and one-guard-family
  checks on a real SAT model;
- exact same-color cut construction and falsity in its source model;
- deep reconstruction;
- byte-tree-preserving read-only audit;
- rejection of six hash-rebound cross-field mutations;
- rejection of the former complete SAT-to-fake-UNSAT mutation;
- rejection of a forged later `checkpoint_before_sha256`;
- fail-closed orphan terminal marker behavior;
- per-run and campaign-global lock behavior;
- synchronous process-group cleanup after orchestrator `SIGTERM`;
- linear eight-attempt history validation; and
- a fresh pinned DRAT-trim verification of a generated nonempty DRAT proof.

An additional read-only mathematical review, independent of the author and
of the mutation probe, also returned `ACCEPT`.

## 1. Mathematical encoding

### Complement dictionary and static parameters

The edge variables consistently encode \(H=\overline G\).

- The no-\(K_4\) clauses give \(\omega(H)\leq3\), hence
  \(\alpha(G)\leq3\).
- Every template forces an \(H\)-triangle, hence
  \(\alpha(G)\geq3\).
- For every pair \(\{a,b\}\), a true witness certifies a vertex adjacent in
  \(H\) to both.  That vertex is outside the pair and is adjacent in \(G\) to
  neither guard, so no two-set dominates \(G\).
- A nonempty selected family of dominating triples gives
  \(\gamma(G)\leq3\).

Consequently any SAT model has
\(\gamma(G)=\alpha(G)=3\).  The cut clauses over every proper vertex cut
containing vertex 0 require a \(G\)-edge across the cut, exactly expressing
connectedness of \(G\).

The fixed odd-hole and fallback antihole clauses match their documented
induced subgraphs.  The hub-free and labeled common-neighbor constraints are
sound relabelings under the separately reviewed structural template theorem.
The CEGAR protocol correctly declines to claim that the runner itself proves
template coverage.

### Exact online one-guard game

For a selected triple \(T\), every outside vertex \(x\) receives the clause

\[
 \neg f_T\vee\neg e_{xa}\vee\neg e_{xb}\vee\neg e_{xc},
\]

so \(T\) dominates \(G\).  For every unoccupied attack \(r\notin T\), the
response clause requires at least one move witness \(m_{T,r,u}\), with

\[
 m_{T,r,u}\Rightarrow \neg e_{ur}
 \quad\text{and}\quad
 m_{T,r,u}\Rightarrow f_{(T-\{u\})\cup\{r\}}.
\]

Thus exactly one named guard traverses one edge of \(G\) to the attacked
vertex, and the successor is another selected dominating triple.  Several
true move variables encode alternative legal responses; they do not move
several guards.  Occupied vertices generate no attack requirement.

The maximum-independent-triple strengthening is sound: when
\(\alpha=\gamma^\infty=3\), the standard sequential attack argument forces
every maximum independent triple into every closed three-family.

Therefore a SAT model supplies an explicit eternal three-family and proves
\(\gamma=\alpha=\gamma^\infty=3\).

### Coloring cuts

For a proper three-coloring \(c\) of the current \(H\), the learned clause is

\[
 \bigvee_{u<v,\ c(u)=c(v)} e_{uv}.
\]

It is false in the source model because that model is properly colored.
Every non-three-colorable \(H\) satisfies it, since every assignment of three
colors has a monochromatic edge.  Each cut is therefore globally valid for
the target universe; accumulating such cuts cannot remove a genuine target.

If DSATUR returns no coloring, the runner quarantines the SAT graph as a
candidate.  It does not treat that oracle result as a publication
certificate for \(\theta>3\).

## 2. SAT models and proof semantics

The DIMACS parser accepts one exact header and an exact clause stream.  The
solver-result parser requires an outcome-compatible status and, for SAT, one
complete nonduplicated assignment of every declared variable.  The live
generation path evaluates that assignment against the entire generated CNF.

On audit, each historical coloring model is checked against every fixed base
clause, including auxiliary witness and move clauses.  Its decoded graph and
family are checked directly, its coloring is checked directly, and its own
cut is reconstructed and shown false in that model.  The cut ledger is then
checked once as a separate sequence of globally sound clauses.  Rechecking
every older cut against every later historical model is unnecessary for
soundness and would create quadratic work.

A decisive candidate or UNSAT attempt retains its raw complete CNF.  The
audit reconstructs that CNF exactly from the frozen base encoding and the
accepted cut prefix.  For UNSAT:

1. the initial CaDiCaL run must return exit 20 and exact `UNSAT`;
2. a second identical-CNF run must again return `UNSAT` while writing a
   nonempty ASCII DRAT proof;
3. pinned DRAT-trim is invoked with the exact command containing
   `-I -f -W`;
4. it must exit zero, emit exactly one `s VERIFIED`, and emit no warning;
5. the CNF and proof hashes must remain unchanged.

Stored checker text is intentionally not the final trust boundary.
Publication audit with `--verify-terminal-proof` launches pinned DRAT-trim
again against the retained CNF and proof, under the same heavy-child lock and
resource limits.  The hostile probe independently exercised this live path
on a tiny contradictory CNF.

## 3. Outcome schemas, artifact roles, and commands

Every outcome has an exact manifest-key set and an exact storage-role set.
Coloring, candidate, UNSAT, unknown, timeout, and memory-limit outcomes cannot
borrow one another's artifact layout.

Each logical role has a fixed basename inside its attempt directory.
Retained, compressed, and reconstructible roles must have distinct canonical
paths; symlinks, nonregular files, and existing hard-link aliases are
rejected.  Hash, size, gzip round-trip, removed-raw-path, generator-manifest,
and cut-prefix reconstruction fields are all checked.

Child records must have exactly the `ChildResult` schema, positive
configuration-matching limits, correct executable hashes, consistent
signals/resource flags, and logs bound to the correct roles.  The
orchestrator command and every solver/checker command must equal a freshly
constructed canonical command, not merely possess a rebound command hash.

These checks reject the former attack in which coloring and ordinary solver
bytes were relabeled as a proof, proof result, and checker logs.  They also
reject negative limits, a contradictory exit code, an extra solver flag,
cross-role aliasing, and a model with a falsified auxiliary clause.

## 4. Checkpoint chronology and crash behavior

The checkpoint is the sole commit point and is written by flush, atomic
replace, and directory `fsync`.  A fresh attempt directory is created under
`attempts/`, after which that parent is also `fsync`ed.

Every attempt records both:

- the predecessor history-chain head; and
- a domain-separated digest of the complete prior logical checkpoint state.

Validation starts from the initial state and walks attempts in chronological
order.  It recomputes the expected predecessor, cut count, streamed cut
prefix, history step, terminal status, and next logical-state digest after
each attempt.  A rebound hash on a later attempt therefore cannot skip or
rewrite chronology.

A coloring attempt is the source of exactly one correspondingly indexed cut.
A non-coloring attempt cannot source a cut.  Candidate and verified-UNSAT
outcomes are permitted only as the final attempt and only when checkpoint
status and the top-level terminal marker agree.

The terminal marker is installed before the checkpoint transition.  If a
crash leaves the marker orphaned, its fully validated attempt still blocks
all later solver work.  Half-written or unreferenced attempt directories do
not advance the checkpoint.

## 5. Resource and process discipline

The configuration rejects a solver or checker ceiling above 75% of physical
RAM.  A campaign-global advisory lock permits only one heavy solver/checker
child across templates.  While holding it, the runner measures current
reclaimable memory and requires the child ceiling plus 512 MiB.

Children receive:

- an absolute pinned executable;
- empty environment and closed stdin;
- a separate process group;
- hard CPU and file-size limits;
- `RLIMIT_AS` where supported;
- a wall-clock deadline; and
- on macOS, direct `libproc` RSS polling with process-group kill on excess.

Temporary handlers for `SIGTERM`, `SIGHUP`, and `SIGINT` kill and synchronously
reap the active process group before releasing locks.  The hostile subprocess
probe observed no surviving child after `SIGTERM`.

Disk preflight reserves the configured do-not-use floor, the requested
retained-attempt budget, nine maximum child files for a terminal proof/check
peak, and generation workspace.  Intermediate attempts are deterministically
compressed and checked against both a per-attempt retained-byte ceiling and
the actual post-manifest directory size.

### Low-severity operational caveat

`session_wall_seconds` is a conservative admission gate, not an OS-level
preemptive deadline over Python-side history validation, CNF generation,
compression, and checkpointing.  Before an iteration, the runner reserves
two complete solver limits, one checker limit, and five seconds of local
overhead; every heavy child remains individually hard-bounded.  A pathological
very long history or unusually slow local filesystem could therefore make
total orchestrator wall time modestly exceed the named session budget.

This does not affect mathematical soundness, memory limits, disk reserve, or
resumability, and it is not a production blocker for the current small
prefixes.  Operational supervision should still use the campaign's external
90-minute sprint boundary.  If a later long-history run approaches that
boundary, add a remaining-time check after generation or wrap the invocation
in an external hard deadline before continuing.

## 6. Linear audit work

The repaired audit computes all cut-prefix hashes in one streaming pass,
builds the fixed base encoding once, validates each historical model against
that fixed base once, validates its own cut once, and validates every cut
ledger record once.

On an eight-cut run, hostile instrumentation recorded exactly:

| Work counter | Count |
|---|---:|
| attempt semantic validations | 8 |
| historical base-CNF validations | 8 |
| historical own-cut validations | 8 |
| cut-ledger record validations | 8 |
| decisive CNF reconstructions | 0 |
| growing-prefix forensic replays | 0 |

The old triangular replay count would have been 28.  A requested deep audit
reconstructs the latest reconstructible prefix once.  A decisive terminal
CNF is reconstructed once, and a requested terminal proof audit launches one
fresh proof-checker process.

## Production decision

The frozen runner may enter the validation-gated production sequence:

1. launch one iteration for the selected template and inspect the installed
   checkpoint and attempt;
2. resume only in bounded multi-iteration sessions;
3. quarantine any candidate immediately for the independent counterexample
   protocol; and
4. for any UNSAT terminal, require
   `--audit-only --deep-reconstruct --verify-terminal-proof` before making a
   mathematical claim.

No production search was launched by this review.
