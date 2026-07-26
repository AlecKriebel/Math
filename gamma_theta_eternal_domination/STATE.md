# Campaign State

## Checkpoint 037 — 2026-07-26 04:30 PDT

- Campaign day: 2 of 27; branch `main`; exact one-leaf production package
  preserved at `HEAD` `92f5ed2b6db1e88ac5776bdb60ebcb6490b85c8d`.
- **New certified finite result (C-042):** exact parent cube `1111`, with
  units \(4,14,23,31\), is UNSAT.  The independently reconstructed leaf has
  18,381 variables, 114,746 clauses, 1,180,020 literals, and SHA-256
  `aafc85341993ed030fe72ba222a4efaa5a02f6ea6fa95519a9dd2ed755b94d1f`.
- The accepted v3 chain retained raw binary DRAT `a50b814d...`, exact
  addition-only RUP stream `f3401ad8...`, and converted LRAT `90787a09...`.
  The durable outcome `00e3c191...` and certificate `7c9705f5...` both record
  `UNSAT_LRAT_VERIFIED` for this leaf and no aggregate claim.
- An independent postrun review imported no runner transition or proof logic,
  reconstructed the leaf CNF byte-for-byte, rescanned both binary proofs, and
  freshly replayed the retained LRAT with the pinned checker on private
  copies.  It launched no solver and changed no production, runtime-source,
  v2, or provisional byte.  Verdict:
  `CERTIFICATE_REPLAY_PASSED_ONE_LEAF_ONLY`.
- The current exact boundary is **one verified leaf and 15 pending leaves**;
  the run aggregate is `INCOMPLETE_NONCLAIM`.  The connected parent, complete
  order-12 \(k=4\) slice, order-12 \(k=5\) slice, and universal conjecture
  remain open.
- Before production, the v3 author suite passed 29/29 tests and the exact
  committed bytes received hostile engineering acceptance at commit
  `f4ccb167...`.  The source-bound run was initialized under that commit and
  the one-leaf package was preserved at `92f5ed2b...`.
- The aggregate checker's v2-bound prototype is rejected for this v3 package.
  Repair against the v3 schemas is in progress and remains unaccepted; no
  aggregate theorem may use it.
- No campaign solver or proof checker is running.  At checkpoint time the
  Apple M1 Pro has 10 logical CPUs and 16 GiB RAM, load averages
  1.65/2.16/2.15, and about 24 GiB free disk.

### Approach registry

| Route | Status | Exact gate/obstruction |
|---|---|---|
| Literature/status audit | active-weekly | No direct resolution found |
| Order-12 \(k=3\) | exhausted-certified | Complete slice C-035 preserved |
| Order-12 \(k=4\) exact target | active-one-of-sixteen | C-042 certifies `1111`; 15 cubes pending |
| Order-12 \(k=4\) structural lane | active | C-041 removes the four/five-near-hub anti-\(C_7\) subbranch |
| Proof-producing runner v2 | rejected-superseded | Frozen failed-closed forensic run preserved |
| Proof-producing runner v3 | accepted-production | One exact leaf completed and independently replayed |
| Aggregate negative-result audit | repairing-v3 | v2-bound prototype rejected; v3 schema repair and hostile audit required |
| Order-12 \(k=5\) | pending | No encoding or outcome yet |

### Running jobs and resume state

- No campaign solver or proof checker is running.
- Preserve both production directories unchanged.  Never resume the v2
  directory `results/order12_k4_production_seed0`.
- The v3 directory
  `results/order12_k4_production_v3_seed0` is resumable, but no second leaf
  should launch until the current package/documentation integration and
  repaired aggregate-checker gate are reviewed.

### Next three highest-value actions

1. Repair and hostile-review the independent aggregate checker against the
   exact v3 schemas; require it to return an incomplete nonclaim on the
   current one-of-16 package while freshly replaying the completed LRAT.
2. After that gate, authorize one additional partition leaf under the
   existing resource limits and checkpoint discipline.
3. Continue the C-041 anti-\(C_7\) structural lane in parallel without
   claiming a full-template exclusion.

## Checkpoint 036 — 2026-07-26 03:12 PDT

- Campaign day: 2 of 27; branch `main`; pre-integration `HEAD`
  `dd6cd3f83b83d5726d4f743a009bbc8d30e23a87`.
- **New proved local restriction (C-041):** in the order-12 parameter-four
  target, if \(H=\overline G\) contains an induced
  \(\overline{C_7}\), all outside vertices adjacent in \(H\) to exactly six
  rim vertices are pairwise nonadjacent in \(H\), miss the same rim vertex,
  and number at most three.
- The proof combines a definition-level two-attack obstruction on a
  nine-vertex induced \(C_7\) extension with the accepted P3 and no-hub
  properties.  Four near-hubs force the unique fifth outside vertex to be a
  forbidden full hub; five near-hubs violate P3 immediately.
- Independent hostile review returned
  `ACCEPT_PROVED_LOCAL_LEMMAS_WITHOUT_SCOPE_INFLATION`.  Its separate
  `frozenset` configuration-digraph evaluator checked all 98 two-spoke
  graphs, all 49 stable-triple cases, the three attack tables, and all 896
  P3-cap cases.  The author regression and hostile replay both pass.
- This excludes only the anti-\(C_7\) incidence subbranch with four or five
  near-hubs.  It does not exclude the full template, settle the
  \((12,4)\) slice, establish novelty, or resolve the universal conjecture.
- The immutable v2 failed-closed run was committed and pushed as
  `dd6cd3f8...`.  Version-three proof-pipeline implementation is active; no
  new solver or checker has been launched and no \(k=4\) leaf is certified.

### Approach registry

| Route | Status | Exact gate/obstruction |
|---|---|---|
| Literature/status audit | active-weekly | No direct resolution found |
| Order-12 \(k=3\) | exhausted-certified | Complete slice C-035 preserved |
| Order-12 \(k=4\) exact target | active | Parent accepted; zero certified leaves |
| Order-12 \(k=4\) structural lane | active | C-041 removes the four/five-near-hub anti-\(C_7\) subbranch |
| Proof-producing runner v2 | rejected-superseded | Frozen failed-closed forensic run preserved |
| Proof-producing runner v3 | active-implementation | Normalizer and five-stage certificate bindings still under construction |
| Aggregate negative-result audit | paused-schema | Resume only after v3 source and schema freeze |
| Order-12 \(k=5\) | pending | No encoding or outcome yet |

### Running jobs and resume state

- No campaign solver or proof checker is running.
- The v3 author is changing only its new source files and tests.  It must
  pass hostile review before a new immutable production directory is
  initialized.
- Preserve `results/order12_k4_production_seed0` unchanged and never resume
  its v2 `run-next`.

### Next three highest-value actions

1. Freeze and independently review the v3 strict binary normalizer and
   normalized-RUP/LRAT/replay pipeline.
2. Initialize a new source-bound v3 run and certify the deliberately trivial
   `1111` smoke leaf before authorizing any other leaf.
3. Use C-041 as a proved filter in the anti-\(C_7\) structural branch while
   the exact certificate lane runs.

## Checkpoint 035 — 2026-07-26 02:56 PDT

- Campaign day: 2 of 27; branch `main`; shared-repository pre-integration
  `HEAD` `ffd414254e5f0a1e8e5636449b38753dd8483091`.
- The exact \(k=4\) run initialized successfully under source commit
  `9b24d9ff...`.  Its manifest is `782862eb...`, its exact 16-leaf partition
  is `0cf81297...`, and its source-set binding is `ea6d74e6...`.
- **First production attempt failed closed:** case `1111` attempt one returned
  `LRAT_CONVERSION_REJECTED_NONCLAIM`.  CaDiCaL exited 20 in 0.062 seconds;
  its 215,475-byte raw binary proof (`a50b814d...`) passed the separate
  warning-fatal forward proof check.
- Backward `drat-trim -i -W -L` exited 80 when it encountered deletion of
  pseudo-unit clause 14 and wrote an empty LRAT.  The runner retained all
  artifacts, checkpointed the outcome `0a8789b6...`, and did not launch
  `lrat-check` or promote the leaf.
- A post-attempt read-only audit passed: 15 leaves are pending, `1111` is a
  retryable nonclaim, zero attempts are active, and the aggregate remains
  `INCOMPLETE_NONCLAIM`.
- A temporary feasibility experiment, explicitly not a certificate, parsed
  the raw proof into 9,690 additions and 6,956 deletions.  Only three unit
  deletions follow the unique empty addition.  An exact 106,318-byte
  addition-only stream passed forward RUP checking, backward LRAT conversion,
  and fresh `lrat-check`.  This establishes a concrete v3 repair direction,
  not an accepted leaf result.
- The v2 run is frozen.  A v3 pipeline needs a bounded strict normalizer,
  addition-only forward RUP replay, backward LRAT conversion, and fresh LRAT
  replay, all with new source/schema bindings and hostile review.  The
  aggregate auditor is paused until that schema freezes.
- **Mathematical frontier unchanged:** no \(k=4\) leaf is certified, the
  order-12 \(k=4,5\) cases remain open, C-035/C-039 remain accepted, and the
  universal conjecture remains open.

### Approach registry

| Route | Status | Exact gate/obstruction |
|---|---|---|
| Literature/status audit | active-weekly | No direct resolution found |
| Order-12 \(k=3\) | exhausted-certified | Complete slice C-035 preserved |
| Order-12 \(k=4\) exact target | active | Parent accepted; `1111` is a nonclaim only |
| Order-12 \(k=4\) structural lane | active | Anti-\(C_7\) near-hub theorem proposed; independent review pending |
| Proof-producing runner v2 | rejected-superseded | Backward converter rejects raw pseudo-unit deletions |
| Proof-producing runner v3 | active-design | Strict normalization plus addition-only RUP and LRAT chain demonstrated only in temporary experiment |
| Aggregate negative-result audit | paused-schema | Must bind and independently replay final v3 artifacts |
| Order-12 \(k=5\) | pending | No encoding or outcome yet |

### Running jobs and resume state

- No campaign solver or proof checker is running.
- Preserve `results/order12_k4_production_seed0` unchanged as the v2 forensic
  run.  Do not invoke `run-next` on it.
- Version-three implementation and a separate anti-\(C_7\) proof review are
  active.  No heavy computation is authorized before both relevant gates.

### Next three highest-value actions

1. Commit and push the exact v2 initialization, failed attempt, hash manifest,
   and explicit nonclaim diagnostic.
2. Implement and hostile-review the bounded v3 normalization/RUP/LRAT
   pipeline, then initialize a new immutable run rather than mutating v2.
3. Hostile-review the proposed anti-\(C_7\) near-hub branch exclusion and
   resume the aggregate auditor only after v3 schema freeze.

## Checkpoint 034 — 2026-07-26 02:46 PDT

- Campaign day: 2 of 27; branch `main`; pre-integration `HEAD`
  `e3c85a891231038b22ac8727f0434c8c8d05037b`.
- The first real \(k=4\) initializer failed closed before creating its run
  directory or launching any solver.  The exact cause was a provenance-only
  path error: from the campaign subdirectory, `git rev-parse HEAD:src/...`
  searches the repository root rather than the campaign tree.
- Both source-binding creation and later reverification now use
  `HEAD:./src/...`.  An unmocked regression proves the corrected lookup
  equals `git hash-object` and successfully creates and rechecks a real
  committed binding.
- New frozen runner SHA-256 is `8c1939ed...`; new 18-test SHA-256 is
  `87250792...`.  Root passed 18/18 in 57.058 seconds at 117,653,504 bytes
  maximum RSS and passed the updated hostile probe in 24.31 seconds at
  141,410,304 bytes.
- Independent hostile review reproduced the old exit 128 and the corrected
  exit zero, reran 18/18 tests in 58.132 seconds, and reran the full hostile
  probe including the real tiny proof.  Verdict remains
  `ACCEPT_PRODUCTION_READY_ENGINEERING_NO_AGGREGATE_CLAIM`.
- **Operational gate:** the corrected runner/test bytes are deliberately
  uncommitted at this pre-integration checkpoint, so full initialization
  still refuses.  They must be committed exactly before retry.
- **Mathematical frontier unchanged:** zero production leaves have run; no
  order-12 \(k=4\) SAT or UNSAT result exists; the universal conjecture
  remains open.  C-035 and C-039 are unaffected.

### Approach registry

| Route | Status | Exact gate/obstruction |
|---|---|---|
| Literature/status audit | active-weekly | No direct resolution found |
| Order-12 \(k=3\) | exhausted-certified | Complete slice C-035 preserved |
| Order-12 \(k=4\) exact target | active | Parent accepted; zero leaf outcomes |
| Order-12 \(k=4\) structural lane | active | C-038/C-039 accepted; anti-\(C_7\) near-hub lemma proposed and unreviewed |
| Proof-producing runner | accepted-engineering-pending-commit | Narrow Git-path repair accepted; exact reviewed bytes must enter `HEAD` |
| Aggregate negative-result audit | active-development | Being repinned to repaired runner SHA `8c1939ed...` |
| Order-12 \(k=5\) | pending | No encoding or outcome yet |

### Running jobs and resume state

- No campaign solver or proof checker is running.
- No `results/order12_k4_production_seed0` directory exists.
- After the repair commit, rerun the exact conservative initializer from
  checkpoint 033, audit its immutable manifest, and recheck live resources
  before authorizing only case `1111`.

### Next three highest-value actions

1. Commit and push the exact Git-path repair, updated hostile package, and
   this no-outcome incident record.
2. Retry initialization and read-only audit; run `1111` only if the 3 GiB
   child plus 1 GiB reserve gate still passes.
3. Independently review the proposed anti-\(C_7\) near-hub lemma and complete
   the aggregate auditor against the final runner hash.

## Checkpoint 033 — 2026-07-26 02:30 PDT

- Campaign day: 2 of 27; branch `main`; shared-repository pre-integration
  `HEAD` `b3e251efaac169ec5583e0083b6d7095e9c9a31a`.
- **Certified frontier preserved:** C-035 still excludes the complete
  order-12, parameter-three slice, including disconnected graphs.  The
  universal conjecture and both remaining order-12 parameters \(k=4,5\)
  remain open.
- **New proved necessary conditions (C-039):** for
  \(\gamma=\gamma^\infty=4\), complement-side hubs of an induced odd hole
  are independent, and P3 bounds their number by \(r-2\) when \(r\ge2\)
  vertices lie outside the rim.  An induced \(\overline{C_7}\) has no
  outside hub.  Thus the surviving order-12
  \(C_5,C_7,\overline{C_7}\) templates permit at most five, three, and zero
  hubs respectively.  The hostile proof verdict is
  `ACCEPT_WITHOUT_SCOPE_INFLATION`; no branch exclusion is claimed.
- The independent hub probe checked 1,099 labeled graphs through order five,
  32,767 induced-subgraph pairs, 121 component pairs, 1,096 P3-equivalence
  graphs, the exact cycle/anticycle inputs, 2,048 \(r=2\) and 262,144
  \(r=3\) fixed-\(C_5\) extensions.  Root replay passed in 2.20 seconds at
  20,283,392 bytes maximum RSS.
- **Repaired runner accepted as engineering only:** the frozen 16-leaf
  workflow now separates CaDiCaL binary-DRAT production, forward raw proof
  verification, backward LRAT conversion, and fresh `lrat-check` replay.
  Both previously fatal crash windows reconcile append-only to retryable
  nonclaims; attempt configurations are hash-bound; the public child
  injection hook is absent.
- The runner hostile verdict is
  `ACCEPT_PRODUCTION_READY_ENGINEERING_NO_AGGREGATE_CLAIM`.  It independently
  reconstructed all 16 leaf CNFs and exercised the real four-stage tiny
  proof, old combined-mode rejection, crash recovery, resource, mutation,
  and provenance boundaries.  Root reran 17/17 tests in 56.974 seconds at
  117,882,880 bytes maximum RSS and the hostile probe in 23.95 seconds at
  134,938,624 bytes.
- **No production leaf has run.**  The exact \((12,4)\) parent remains
  unsolved.  Even 16 runner-level `UNSAT_LRAT_VERIFIED` leaves would be only
  `ALL_LEAVES_VERIFIED_PENDING_INDEPENDENT_COVERAGE_AUDIT`.
- The separate aggregate auditor has independent parsing, parent/leaf
  reconstruction, checkpoint-chain checks, and fresh replay logic in
  development.  It is not yet tested, accepted, or usable for a mathematical
  claim.
- Resource observation at 02:27: Apple M1 Pro, 10 logical CPUs, 16 GiB
  physical RAM, load averages 2.80/3.46/3.90, about 4.73 GB reclaimable by
  the runner probe, and about 26.4 GiB free disk.  A conservative 3 GiB child
  plus 1 GiB reserve configuration presently fits, but it is not frozen
  until the accepted runtime sources are committed.

### Approach registry

| Route | Status | Exact gate/obstruction |
|---|---|---|
| Literature/status audit | active-weekly | No direct resolution found; all-guards Cayley result quarantined |
| Order-12 \(k=3\) | exhausted-certified | Complete slice C-035 remains accepted |
| Order-12 \(k=4\) exact target | active | Parent C-037 accepted; zero leaf outcomes |
| Order-12 \(k=4\) structural lane | active | C-038/C-039 leave \(C_5,C_7,\overline{C_7}\) with new hub filters |
| Decoded candidate verification | accepted-ready | Conditional verifier accepted; no candidate exists |
| Proof-producing runner | accepted-engineering | Must be committed before immutable initialization; makes no aggregate claim |
| Aggregate negative-result audit | active-development | Exact runner hash now frozen; tests and independent acceptance still required |
| Order-12 \(k=5\) | pending | Begins after the \(k=4\) production gate is stable or measured evidence redirects effort |

### Running jobs and resume state

- No campaign solver or proof checker is running.
- The accepted runner, partition proof, hub theorem, and both hostile packages
  are ready for exact-file integration.
- The aggregate auditor is being completed against runner SHA-256
  `4e65bc62...`; it must return an incomplete nonclaim for any proper subset
  of the 16 leaves.

### Next three highest-value actions

1. Commit and push the exact accepted runner/hub bytes and checkpoint
   metadata without staging provisional proof artifacts or unrelated work.
2. Initialize the immutable 16-leaf run with committed source bindings and,
   if the live gate still passes, certify only the trivially inconsistent
   `1111` leaf as a real end-to-end pipeline test.
3. Finish and hostile-review the separate aggregate auditor; use it to audit
   the one-leaf run while retaining `INCOMPLETE_NO_MATHEMATICAL_CLAIM`.

## Checkpoint 032 — 2026-07-26 02:00 PDT

- Campaign day: 2 of 27; branch `main`; shared-repository pre-integration
  `HEAD` `1775c93345559d005eca19acd23eabec5f1a0538`.
- **Certified frontier preserved:** C-035 still excludes the complete
  order-12, parameter-three slice, including disconnected graphs.  The
  universal conjecture remains open, and no order-12 parameter-four SAT or
  UNSAT result is claimed.
- **New proved structural reduction (C-038):** for connected
  \(\gamma=\gamma^\infty=4\), every induced hole in the complement leaves at
  least four outside vertices.  Thus an order-12 parameter-four target has an
  induced \(C_5\), \(C_7\), or \(\overline{C_7}\) in its complement; the
  former \(C_9\) branch and \(C_{11}\) are impossible.  An independent
  proof review returned
  `ACCEPT_PROVED_RELATIVE_TO_STATED_ACCEPTED_INPUTS`.
- The clean-room structural probe exhausted every fixed-induced-\(C_5\)
  incidence graph with zero through three outside vertices.  In the largest
  \(r=3\) layer it checked all 262,144 graphs; 274 satisfy P3, all 274 have a
  hub, and none has connected complement.  It independently reproduced
  \(\gamma^\infty(C_n)=3,4,5,6\) and
  \(\gamma^\infty(\overline{C_n})=3\) for
  \(n=5,7,9,11\).
- The independent decoded \((12,4)\) candidate verifier is accepted.  Its
  definition-level core checks exact \(\gamma=4\), a literal nonempty
  one-guard eternal four-family, and every one of the 65,536
  anchor-normalized colorings of the complement.  Ancillary restrictions
  cannot erase a definition-level witness.
- Thirteen authored tests pass.  The hostile verifier audit separately
  checked 2,048 Graph6 cases, 256 static-parameter cases, 4,096 literal
  one-guard families, 64 coloring cases, 131,072 trace rows, and the complete
  decisive/ancillary truth table.  It found one malformed-deep-JSON CLI
  defect; the exact 1,000,001-byte reproducer is now a regression that exits
  2 with a structured error.  Final verdict: `ACCEPT`.
- The current literature refresh has 38 model-tagged rows and found no
  universal proof or certified counterexample.  The July 2026 Cayley paper
  is explicitly \(\gamma_{\mathrm{all}}^\infty\), where other guards may
  also move, and supplies no theorem in the campaign's one-guard model.
- **Draft runner rejected before launch:** a real two-variable proof probe
  showed that the pinned `drat-trim -i -f -W -L` combination emits LRAT that
  the pinned `lrat-check` rejects.  The audit also found two crash-recovery
  windows, a missing attempt-configuration recheck, and an overpowered
  injectable test hook.  All findings are confined to uncommitted,
  unlaunched production infrastructure.  The repair must separate raw
  forward DRAT verification, backward LRAT conversion, and fresh LRAT
  replay.
- A separate aggregate verifier is being written without importing the
  production runner.  It will reconstruct all 16 leaves, audit Boolean
  coverage, and freshly replay every LRAT before any complete-slice claim.
- Resource observation at 02:00: Apple M1 Pro, 10 logical CPUs, 16 GiB
  physical RAM, one-minute load about 3.55, and about 26.9 GiB free disk.
  The production gate still refused because only about 4.54 GB was
  reclaimable against a 6 GiB child-plus-reserve requirement.  No heavy
  solver was launched.

### Approach registry

| Route | Status | Exact gate/obstruction |
|---|---|---|
| Literature/status audit | active-weekly | Current refresh complete; no direct resolution found; all-guards Cayley result quarantined |
| Order-12 \(k=3\) | exhausted-certified | Complete slice C-035 remains accepted |
| Order-12 \(k=4\) exact target | active | Parent C-037 accepted; no SAT/UNSAT result |
| Order-12 \(k=4\) structural lane | active | C-038 reduces SPGT obstruction to \(C_5,C_7,\overline{C_7}\) |
| Decoded candidate verification | accepted-ready | Conditional verifier and hostile audit accepted; no candidate exists |
| Proof-producing runner | rejected-repairing | Four concrete pre-launch findings must be closed and re-audited |
| Aggregate negative-result audit | active-development | Must remain implementation-independent and bind repaired final schema |
| Order-12 \(k=5\) | pending | Begins after the \(k=4\) production gate is stable or measured evidence redirects effort |

### Running jobs and resume state

- No campaign solver or proof checker is running.
- The runner repair and its hostile review are active against the four exact
  reproducer classes listed above.
- The independent aggregate auditor is active but must fail closed until the
  repaired certificate schema is frozen.

### Next three highest-value actions

1. Freeze and publish C-038, the candidate verifier, their independent
   audits, and this explicit rejection record without staging any draft
   runner or provisional proof artifact.
2. Repair and cross-audit the four-stage proof pipeline and both interruption
   windows; require exact current-byte hashes before source freeze.
3. After a committed source-binding gate and a safe memory window, initialize
   the immutable 16-leaf run and certify the trivial `1111` leaf first as a
   real, low-resource end-to-end proof-pipeline test.

## Checkpoint 031 — 2026-07-26 01:05 PDT

- Campaign day: 2 of 27; branch `main`; shared-repository pre-integration
  `HEAD` `069b06ed2801e72cf3c9e53fc8a29e15415f657a`.
- The complete checkpoint was integrated and pushed in commit
  `9f192cb85866b06811a970c9b7b346ee06f5554e`.
- **Certified frontier unchanged and preserved:** C-035 excludes the complete
  order-12, parameter-three counterexample slice, including disconnected
  graphs.  The universal conjecture remains open.
- **New proved search reduction (C-036):** the classical characterization of
  graphs with domination number half their order implies that every connected
  counterexample with order \(n\) and common parameter \(k\) satisfies
  \(n\geq2k+1\).  Thus \(k=6\) is impossible at order 12; after C-035, only
  connected \(k=4,5\) remain there.  This is explicitly recorded as a
  classical corollary, not a novelty claim.
- **New exact order-12, parameter-four target (C-037):** the connected
  anchored parent CNF has 18,381 variables, 114,742 clauses, 1,180,016
  literals, and SHA-256 `adbe0c01...`.  A clean-room implementation imports
  neither synthesis core, reconstructs every clause byte-for-byte, checks all
  65,536 coloring-bank rows and all 1,792 comparator cases, exhausts a
  512-graph small anchored universe, and rejects seven deliberate mutations.
  The accepted boundary is exact formula infrastructure only: no solver has
  been invoked and no \(k=4\) SAT/UNSAT result is claimed.
- A fail-closed one-command replay package for C-035 now binds 91 exact files
  and 87 accepted Git objects.  Its bounded 15-test suite passes.  Fast mode
  is metadata-only and returns `NO_MATHEMATICAL_CLAIM`; full mode runs the
  independent \(C_5,C_7,C_9\) proof audits sequentially and promotes C-035
  only after all succeed.
- A nine-page submission-oriented C-035 manuscript has been built
  deterministically.  The final source SHA-256 is `dddf4a1b...` and two clean
  builds give the same PDF SHA-256 `f84430ee...`.  The abstract now says
  accurately that the formulas contain valid coloring clauses implied by
  non-three-colorability; it does not imply that the 170-row \(C_9\) subset
  is a complete coloring bank.  The only external-submission blockers are
  the deliberately visible author-metadata and permanent-archive-ID
  placeholders.
- The exact \(k=4\) implementation passed all 9 focused tests.  Its
  independent hostile probe reran in 13.60 seconds, 13.42 CPU seconds, with
  peak RSS 129,581,056 bytes and byte-identical canonical output.
- No new heavy solve or full C-035 proof replay was launched.  At this
  checkpoint the one-minute load average was about 20.6 because other local
  campaigns were active; physical memory is 16 GiB and free disk space is
  about 18 GiB.  The replay and solver gates correctly refuse to compete for
  the machine in this state.
- Approach registry: order-12 \(k=3\) **exhausted and certified empty**;
  order-12 \(k=4\) **exact target ready, unsolved**; order-12 \(k=5\)
  **active but not yet encoded**; half-order \(k=6\) **proved impossible**;
  structural and literature lanes **active**; universal resolution
  **open**.
- Next three highest-value actions:
  1. integrate and push the manuscript, replay wrapper, half-order reduction,
     and exact \(k=4\) parent with their independent reviews;
  2. write an independent decoded-candidate verifier and a proof-producing,
     resumable partition plan for the \(k=4\) parent;
  3. when the load and disk gates permit, run a bounded exploratory \(k=4\)
     probe, then freeze either a candidate for independent verification or
     proof-producing subinstances—never an unlogged solver assertion.

## Checkpoint 030 — 2026-07-25 23:27 PDT

- Campaign day: 1 of 27; branch `main`; pre-integration repository `HEAD`
  `7cece508d9b2a179324624a40c393460bd440847`.
- The complete theorem, acceptance record, manifest, and audit stack were
  integrated and pushed in commit
  `36d8191ac72c4c04291184f2a6854fa76e181712`.
- **New certified finite theorem (C-035).**  No finite simple graph \(G\) on
  12 vertices satisfies
  \[
  \gamma(G)=\gamma^\infty(G)=3<\theta(G).
  \]
  This is the complete \((n,k)=(12,3)\) slice, including disconnected
  graphs.  It does **not** exclude order-12 counterexamples with \(k\geq4\),
  any higher-order counterexample, or resolve the universal conjecture.
- The last open structural branch, a hub-free induced \(C_5\) in
  \(\overline G\), is empty (C-034).  The exact retained
  \(F_5\land S\) instance has 6,886 variables, 23,968 clauses, 192,169
  literals, and SHA-256 `c6a0811c...`.  CaDiCaL returned exact
  `s UNSATISFIABLE` in 6.151 seconds at 59.66 MiB peak RSS.
- The preserved addition-only binary proof is 6,337,621 bytes at SHA-256
  `c6c24853...`; it has 247,981 additions, 4,372,774 addition literals,
  maximum variable 6,886, and a final empty clause.  Strict pinned
  DRAT-trim replay under `-i -f -W -U` returned exactly one
  `s VERIFIED`, zero RAT lemmas, and 10,912,555 resolution steps in
  57.729 seconds at 81.5 MiB peak RSS.
- The run used the exact audited source commit
  `6f3ef0a0970b7214c34018fe32ea1ceeb5764d17` and was frozen untouched at
  commit `dff45f4239e4acabc461533a0a213beec18ec56d`.  Its Git tree is
  `aaef13bb...`, and its length-delimited payload tree hash is
  `16f7e62e...`.
- Two clean-room post-run audits independently reconstructed the exact CNF,
  parsed the raw and addition-only binary proofs, checked deletion stripping,
  bound 23 runtime sources and both pinned tools, and freshly replayed the
  strict checker.  Three complete package-auditor runs were byte-identical.
  The accepted verdicts are
  `ACCEPT_C5_UNSAT_CERTIFICATE_FOR_C033` and
  `PASS_EXACT_RETAINED_PACKAGE`.
- The full slice implication is written in
  `math/lemmas/order12_k3_exclusion.md`.  It combines the previously
  accepted \(C_7\) and \(C_9\) certificates with the new \(C_5\)
  certificate, the SPGT-based structural split, and an explicit component
  argument.  Two independent mathematical reviews returned
  `ACCEPT_COMPLETE_ORDER12_K3_EXCLUSION` and `ACCEPT_NO_BLOCKER`.
- The decisive efficiency discovery was the proved 315-clause \(S_6\)
  signature-ordering symmetry break: the unsorted run had hit a 512 MiB
  proof-file cap without a result, whereas the sound strengthened instance
  solved in 6.151 seconds and yielded a 6.34 MiB checked proof.
- Audit work also caught two real infrastructure defects before acceptance:
  an incomplete runtime import-closure binding and nondeterministic temporary
  paths in a draft audit.  Both were repaired and regression-tested before
  the certified run was promoted.
- Current exhaustive frontier: connected unlabeled graphs through order 9;
  the published order-at-most-11 near-miss catalog; all one-vertex extensions
  of its 55 closest hosts; their complete one-edge-toggle neighborhood; and
  now the complete order-12, parameter-three slice.  No counterexample has
  been found.
- Resource state: Apple M1 Pro, 10 CPU cores, 16 GiB physical RAM, about
  23 GiB filesystem space free.  Other research programs currently have
  several CPU-heavy jobs active, so no new campaign-heavy solve is being
  launched at this checkpoint.  The completed gamma-theta run remained far
  below the 75% memory ceiling.
- Approach registry: `hole5`/`hole7`/`hole9` template split **exhausted and
  certified empty** for \((12,3)\); near-miss extension/toggle lane
  **exhausted at its declared radii**; direct synthesis **active**, next at
  \((12,4)\); structural proof lane **active**; literature/reproducibility
  lane **active**.  The universal conjecture remains open.
- Next three highest-value actions:
  1. freeze this theorem, acceptance record, manifest, and checkpoint in Git;
  2. prepare a compact arXiv-ready manuscript and one-command certificate
     replay for C-035;
  3. design and gate the \((12,4)\) synthesis/structural program, using
     partitioned proof-producing cases rather than blind enumeration.

## Checkpoint 029 — 2026-07-25 22:36 PDT

- Campaign day: 1 of 27; branch `main`.
- The exact bounded binary-proof runner for the retained `hole5`
  signature-sorted package is accepted for source freeze, but its mandatory
  post-commit `HEAD` gate is not yet satisfied.  No production solver was
  launched at this checkpoint.
- A second independent audit found a genuine pre-launch defect in the first
  frozen version: `cegar.py` executed local dependencies `coloring.py` and
  `generate.py` that were absent from the runtime-source manifest.  The
  runner now binds the complete eight-module local import closure, a recursive
  AST regression test enforces that closure, and a separate exact hash gate
  recomputes the CaDiCaL and DRAT-trim binary and source-archive hashes.
- The final runner SHA-256 is `02e8a13d...`; its test SHA-256 is
  `e622ef08...`.  The independent probe, canonical log, and review have
  hashes `06261bbc...`, `f9ca64c9...`, and `63af7f25...`.
  The primary verdict is
  `ACCEPT_FOR_COMMIT_WITH_MANDATORY_POSTCOMMIT_HEAD_GATE`; a second auditor
  reports `ACCEPT_NO_BLOCKER`.
- The runner preserves the raw binary proof, runs the already accepted parser
  in isolated bounded mode, reparses the addition-only stream, and promotes
  UNSAT only after warning-fatal `drat-trim -i -f -W -U` replay.  SAT remains
  candidate-only.  Every timeout, resource limit, malformed artifact,
  mutation, or incomplete phase is an explicit nonclaim.
- Root replay passed 30 focused runner, breaker, and encoding tests in
  95.08 seconds with peak RSS 82,886,656 bytes.  The full campaign suite
  passed 271 of 271 tests in 204.18 seconds with peak RSS 115,851,264 bytes.
  Exact validation evidence is manifest ART-199--204.
- Current pre-freeze repository `HEAD` is
  `7bfd268c4b0dd24c4207645d66373c47278e10cf`.  The launch gate requires a
  new commit containing the exact audited bytes, an exact current-`HEAD`
  runtime-source replay, and a fresh resource check.  This checkpoint does
  not satisfy that gate.
- The next actions are: commit and push only the accepted campaign files;
  replay the post-commit source/tool/package bindings; then, only if the
  machine is responsive and the campaign-global heavy-child lock is free,
  launch one bounded seed-0 production attempt into a new `results/`
  directory.

## Checkpoint 028 — 2026-07-25 22:12 PDT

- Campaign day: 1 of 27; branch `main`.
- Claim C-032 is `PROVED`.  For the retained complete-bank `hole5` formula
  \(F_5\), the residual rim reflection
  \(\rho=(0\ 1)(2\ 4)\) was reconstructed on all 6,886 semantic variables
  and preserves the exact base, bank, and full clause multisets.  It swaps
  \(e_{25}\) and \(e_{45}\), while the accepted outer \(S_6\) action fixes
  both.
- Consequently
  \(F_5\) is satisfiable if and only if
  \(F_5\land S\land T\) is satisfiable for
  \(T=(-24,39)\): reflect first if \(T\) fails, then sort the outer
  signatures.  The exact strengthened formula has
  \((6{,}886,23{,}969,192{,}171)\), is 754,332 bytes, and has SHA-256
  `441e54c2...`.
- The source units \(e_{05}=e_{15}=1\), the vertex-5 no-hub clause, and
  \(T\) reduce the exhaustive
  \((e_{25},e_{35},e_{45})\) representatives to exactly
  `000`, `001`, `010`, `011`, and `101`.
- Claim C-033 is `PROVED` only as a conditional realization theorem.  Any
  connected order-12 parameter-three counterexample whose complement has a
  hub-free induced \(C_5\) produces a satisfying assignment of the exact
  retained \(F_5\), including explicit common-neighbor, nonempty
  one-guard-family, and move witnesses; accepted symmetry then supplies
  models of the strengthened formulas.
- The separate premise “the exact strengthened CNF is UNSAT by an accepted,
  independently checked certificate” is **unfilled**.  No `hole5` exclusion,
  no \((12,3)\) slice result, and no SAT/UNSAT result is recorded at this
  checkpoint.
- Exact evidence is in
  `reviews/hole5_rim_reflection_coverage_hostile_probe.py`,
  `reviews/hole5_rim_reflection_coverage_hostile_probe_log.json`,
  `reviews/hole5_rim_reflection_coverage_hostile_review.md`,
  `math/lemmas/hole5_template_exclusion_conditional.md`, and
  `reviews/hole5_template_exclusion_conditional_hostile_review.md`.
  Manifest rows ART-194–198 bind all five files.
- No solver or proof checker was run for these results.  No campaign heavy
  child is active, and runner files were outside this integration.

## Checkpoint 027 — 2026-07-25 21:52 PDT

- Campaign day: 1 of 27; branch `main`.
- Commit `10acf379329411d9d05267b3411d6703047e705e` froze and
  published the `hole5` \(S_6\) theorem, generator, tests, and independent
  mathematical and binary-proof audits.
- A postcommit reviewer bound all four author artifacts to their Git objects
  at that revision.  Its independent comparator stream is byte-identical to
  the author stream at SHA-256 `ddd32969...`; both constructions give the
  exact 754,323-byte derived CNF at SHA-256 `c6a0811c...`.  All five
  covariance generators and all 20,480 comparator assignments pass.
- The retained package
  `results/synthesis_k3_hole5_signature_package/` was generated from
  committed sources at revision `126071c7...`.  It has exactly three
  regular, single-link files and tree SHA-256 `dd9ac46f...`; its manifest
  SHA-256 is `da33bc17...` and records
  `runtime_sources_match_head=true`.
- A second clean-room package auditor imported no author or synthesis code
  and reconstructed the source body, 315-clause suffix, final CNF, complete
  manifest, Git bindings, and package tree byte-for-byte.  Its verdict is
  `ACCEPT` as exact formula infrastructure.
- Claim C-031 is now `PROVED`: the original complete-bank `hole5` formula is
  satisfiable exactly when this signature-sorted formula is satisfiable.
  This is a semantic symmetry theorem, not a SAT/UNSAT result.

### Production gate

- The package remains correctly solve-disabled.  A new binary-proof runner
  is being implemented separately and must be committed, source-bound, and
  hostile-tested before launch.
- A production UNSAT result must preserve the raw binary proof, pass the
  independent canonical parser at maximum variable 6,886, produce and
  reparse a new addition-only artifact, and replay warning-free with pinned
  DRAT-trim under `-i -f -W -U`.  Any failed gate remains an explicit
  nonclaim.
- The machine remains an Apple M1 Pro with 10 CPU cores and 16 GiB physical
  RAM.  Approximately 10 GiB disk is free.  No campaign heavy child is
  active; the next run retains the one-heavy-child rule and 4 GiB disk
  reserve.

## Checkpoint 026 — 2026-07-25 21:30 PDT

- Campaign day: 1 of 27; branch `main`.
- The last open \((12,3)\) branch now has a proved and independently
  reconstructed \(S_6\) label-symmetry reduction.  Vertices
  \(6,\ldots,11\) are undistinguished in the complete `hole5` formula.
  Sorting their six-bit \(H\)-adjacency signatures to fixed vertices
  \(0,\ldots,5\) preserves at least one labeling of every model.
- The auxiliary-free encoding has exactly 315 clauses and 3,210 literals.
  It strengthens the retained formula from
  \((6{,}886,23{,}653,188{,}959)\) to
  \((6{,}886,23{,}968,192{,}169)\).  The independently generated clause
  stream and author stream agree at SHA-256 `ddd32969...`; the deterministic
  derived CNF is 754,323 bytes at SHA-256 `c6a0811c...`.
- A clean-room standard-library probe reconstructed all 6,886 semantic
  variables and proved exact full-CNF covariance under the five adjacent
  transpositions generating \(S_6\).  It checked all 20,480 signature-pair
  assignments with zero mismatch and rejected coordinatewise ordering,
  one-sided prefix clauses, edge-only transport, unsorted witness keys, and
  the unsound coloring-orbit-representative shortcut.
- The focused author suite passed 8 of 8 tests in 26.44 seconds.  A fresh
  root full-suite run passed all 258 tests in 157.41 seconds with peak RSS
  115,818,496 bytes.
- A second clean-room audit accepted canonical binary-DRAT parsing and
  deletion stripping after rejecting 20 malformed-proof mutations.  It
  found that pinned DRAT-trim alone is too permissive at malformed varint and
  variable-range boundaries.  Production must therefore preparse with
  maximum variable 6,886, preserve the immutable raw proof, emit and reparse
  an exact addition-only artifact, and only then require strict
  `-i -f -W -U` replay.

### Production gate

- The theorem note, generator, tests, and both independent audit stacks are
  accepted for commit.  No `hole5` SAT/UNSAT claim exists.
- Commit and push these frozen files.  Then bind their Git-object bytes,
  regenerate a retained derived package with
  `runtime_sources_match_head=true`, and keep its production solve gate
  closed until the binary runner and parser invocation are source-bound.
- The rejected `hole7` v1 recovery and the incomplete 512 MiB `hole5` proof
  remain local and must not be staged as accepted artifacts.
- No campaign solver or checker is active.  The next production run remains
  one heavy child with a 4 GiB disk reserve.

## Checkpoint 025 — 2026-07-25 21:11 PDT

- Campaign day: 1 of 27; branch `main`.
- Claim C-030 is accepted as `CERTIFIED-FINITE`: no connected 12-vertex
  graph with
  \(\gamma=\alpha=\gamma^\infty=3<\theta\) has a complement containing a
  hub-free induced \(C_7\).  Relative to C-014, C-017, and C-028, the
  hub-free induced-\(C_5\) branch is now the only surviving branch of the
  exhaustive \((12,3)\) split.
- The accepted `hole7` certificate binds the exact 6,886-variable,
  21,718-clause full-bank CNF and an 18,093,724-byte addition-only RUP proof.
  The proof contains 284,317 additions and passed two strict pinned
  DRAT-trim replays with `-I -f -W -U`, exit zero, one warning-free
  `s VERIFIED`, and zero RAT lemmas.  A separate auditor reconstructed the
  formula, stripped exactly 263,162 deletion records, rejected ten proof
  mutations, and audited the graph-to-CNF implication.
- The original `hole7` solve remains byte-for-byte preserved with its
  correct nonclaim outcome.  Its checker exit 80 came from DRAT-trim's
  documented forward-mode handling of a pseudo-unit reason deletion, not
  from a failed inference.  Only the separately sealed `_v2` recovery is
  authoritative.
- The retained complete `hole9` formula also received a direct,
  warning-free replay of the already accepted 4,705-addition proof.  The
  independent audit proved exact clause-multiset inclusion of the earlier
  formula and all 170 cuts, with exactly 595 new clauses.  This strengthens
  the artifact binding for C-028 without changing its scope.

### Remaining `hole5` branch

- The first full-bank proof-producing run hit its exact 512 MiB ASCII proof
  cap after 153.478 seconds and 67.77 MiB peak RSS.  No result file or
  checker run exists, so its status is
  `INCONCLUSIVE_SOLVER_FILE_LIMIT`.
- A controlled proofless default run returned `c UNKNOWN` at 600.027
  seconds and 65.25 MiB peak RSS.  A second proofless run using CaDiCaL's
  UNSAT preset returned `c UNKNOWN` at 300.025 seconds and 62.52 MiB peak
  RSS.  An earlier shell-controlled probe was interrupted after macOS
  rejected the requested virtual-memory limit; it is recorded as an
  aborted control event, not a search result.
- Binary proof encoding is approximately 2.60 times smaller on the frozen
  512 MiB prefix, but the proofless timeout shows that format alone will not
  terminate the same seed/configuration.
- Measured next route: prove and append 315 auxiliary-free clauses sorting
  the six external vertices \(6,\ldots,11\) by their six-bit adjacency
  signatures to the fixed core \(0,\ldots,5\).  The full `hole5` formula is
  invariant under this \(S_6\) relabeling, so every model has a sorted
  representative.  Exhaustively audit every comparator and all generating
  transpositions before production.  If that parent remains hard, split it
  into the seven exhaustive assignments to \(e_{25},e_{35},e_{45}\) other
  than `111`, with a separate checked proof per leaf.
- No campaign solver or checker is active.  Approximately 10 GiB disk is
  free; every next run retains the 4 GiB reserve and one-heavy-child rule.

## Checkpoint 024 — 2026-07-25 20:39 PDT

- Campaign day: 1 of 27; branch `main`.
- The three retained complete-bank input packages passed the independent
  production audit.  Their exact bytes, exhaustive coloring semantics,
  manifest bindings, Git-object source bindings, paths, link counts, and
  combined nine-file tree were reconstructed without importing the author
  implementation.  Verdict: `ACCEPT`.
- A bounded seed-0 `hole7` production run terminated UNSAT after 11.381
  seconds using 43.44 MiB peak RSS and wrote a 35,285,574-byte ASCII proof
  with SHA-256 `7ceb4a63...`.
- The integrated strict checker exited 80 before verification because its
  forward-mode `-W` policy stops at a warning associated with the
  deletion-bearing proof.  The run therefore correctly records
  `UNSAT_UNVERIFIED_CHECKER_EXIT` and `NO_MATHEMATICAL_CLAIM`.
- A read-only diagnostic replay without the stop-on-warning flag reached
  exactly one `s VERIFIED` in 18.127 seconds and reported 220,217 core
  lemmas, 9,087,640 resolution steps, and zero RAT lemmas.  This is strong
  evidence but is not promoted: an independent reviewer is stripping only
  deletion lines and requiring warning-free `-I -f -W -U` replay against
  the frozen CNF.

### Publication and next gate

- Commit and push the accepted retained input packages, pinned-tool smoke,
  production hostile review, and this explicit provisional boundary.
- Preserve the original `hole7` run byte-for-byte.  Promote nothing until
  the addition-only proof, graph-to-CNF implication, and independent replay
  are accepted and hash-bound.
- Then recheck the single-heavy-child resource gate and run the complete
  `hole5` package under the same bounded nonclaim protocol.  No campaign
  solver or checker is active at this checkpoint.

## Checkpoint 023 — 2026-07-25 20:34 PDT

- Campaign day: 1 of 27; branch `main`.
- Commit `2e68a6396735381ee634a572dda409610b40891f` is pushed to
  `origin/main` and freezes the accepted exact coloring-bank theorem,
  generator, focused tests, and two independent reviews.
- Retained packages were generated from that commit for `hole9`, `hole7`,
  and `hole5`.  Their manifest SHA-256 values are respectively
  `e36e7ab0...`, `7c46b015...`, and `99a56197...`; each records
  `runtime_sources_match_head=true` and an empty mismatch list.
- Root exhaustive package audit passed all \(3^{12}\) labeled color
  assignments per template.  The retained CNF SHA-256 values are
  `baea7205...` (`hole9`), `6a011e68...` (`hole7`), and `76bf36e...`
  (`hole5`).
- A retained pinned-tool smoke run checked both an exact SAT model and a
  warning-free DRAT proof.  CaDiCaL and DRAT-trim hashes remain
  `51c3c82b...` and `31df522b...`.

### Bounded production launch

- Independent retained-package and `hole9` proof-replay audits are running;
  they are read-only with respect to the three packages.
- Subject to those fail-closed audits, the next single heavy child is a
  `hole7` complete-bank solve with seed 0, 600-second solver and checker
  bounds, 2,048 MiB child-memory bounds, a 512 MiB file bound, and a
  4,096 MiB disk reserve.  At this checkpoint the machine has 10 CPU cores,
  16 GiB physical RAM, approximately 4.16 GB immediately available memory,
  and approximately 10.3 GiB free disk.  No campaign solver or proof checker
  is active.
- Any timeout or resource limit is an explicit nonclaim.  A SAT result must
  pass independent graph-parameter verification; an UNSAT result must pass
  an independent graph-to-CNF audit and warning-free proof replay before
  promotion.
- After `hole7`, run the same bounded gate on `hole5`; then update the claim
  boundary, manifest, research log, and source checkpoint before publishing.

## Checkpoint 022 — 2026-07-25 20:24 PDT

- Campaign day: 1 of 27; branch `main`.
- Latest pushed campaign checkpoint at validation start:
  `f667fb289fed6c9cfe380645140133ecb4a29b14`.
- Claim C-029 is accepted as `PROVED`: relative to each forced odd-hole
  template, the complete first-use coloring bank is exactly equivalent to
  \(\chi(\overline G)>3\), with exact sizes 3,645 (`hole5`), 1,701
  (`hole7`), and 765 (`hole9`).
- The frozen generator, theorem note, and focused tests are bound at
  SHA-256 values `dc69687f...`, `abc9568d...`, and `cc89c891...`.
  Independent theorem and implementation reviews both returned `ACCEPT`.
- Root replay passed 12 of 12 focused tests in 62.578 seconds and all 250
  campaign tests in 121.953 seconds.  The independent standard-library
  probe exhausted all \(3^{12}\) labeled assignments for every template,
  independently reconstructed every one of the 6,886 variables and every
  base-plus-bank clause, and rejected eight semantic mutations.
- All 170 accepted `hole9` cuts are exact members of the complete 765-row
  bank.  The prior 20,200-clause formula is a clause subset of the complete
  20,795-clause formula, so its accepted addition-only RUP proof remains
  valid under strengthening.  Pinned DRAT-trim directly replayed that proof
  against the complete development formula, exiting zero with one
  warning-free `s VERIFIED`.

### Production gate

- Disposable development packages for all three templates passed independent
  bank and CNF reconstruction, but correctly record that the new runtime
  source was not present at their precommit `HEAD`.  They are not production
  artifacts.
- Commit and push the frozen source and reviews.  Then regenerate retained
  packages from that `HEAD`, require
  `runtime_sources_match_head=true`, preserve a retained `hole9` proof replay,
  and only then launch bounded proof-producing `hole7` and `hole5` work.
- No `hole5` or `hole7` UNSAT claim, counterexample, or complete
  \((12,3)\) result exists at this checkpoint.

## Checkpoint 021 — 2026-07-25 19:52 PDT

- Campaign day: 1 of 27; branch `main`.
- Latest pushed campaign checkpoint: `07683181`.
- `hole5` advanced from 192 to 448 complete attempts and globally valid
  coloring cuts.  Its status remains `running`, with no candidate, UNSAT
  terminal, timeout, unknown result, or memory event.
- The new `hole5` checkpoint SHA-256 is
  `ca4556b6d8b931d71b7b143d1e8b7c3aab4475fa1edae90a83c7acb107100b55`;
  its history head is
  `70f446f1b7e14b863a64108bfffe519a3ffb58c6e45c45f1c77e967dba6c3baf`.
  Frozen deep reconstruction and a separate standard-library audit passed,
  preserving the exact 3,139-file, 15,610,294-byte tree at SHA-256
  `cf12c4c0a7923a849d837ddaaabc186e688f2f5368e858d6fa5bb4b8a2b445b4`.
- The 256 new solver children used 16.6234 seconds total wall time and
  12.7135 seconds total CPU.  Maximum child wall time was 0.1514 seconds and
  maximum RSS was 17,399,808 bytes.  No heavy campaign child was active at
  checkpoint creation.

### Measured strategy pivot

- Two independent read-only trajectory analyses found that the odd-hole
  template units reduce the complete three-coloring universe to exactly
  3,645 partitions for `hole5`, 1,701 for `hole7`, and 765 for `hole9`.
  Relative to each template, adjoining the ordinary same-color clause for
  every compatible partition is exactly equivalent to
  \(\chi(\overline G)>3\); incompatible partitions already violate a forced
  template edge.
- The exact count is
  \[
    M_\ell=(2^\ell-2)3^{11-\ell}/6
    \quad(\ell\in\{5,7,9\}).
  \]
  The forced odd cycle has \(2^\ell-2\) labeled proper colorings, the
  external common neighbor of rim edge \(01\) is forced to the third color,
  the other \(11-\ell\) vertices are free, and the forced triangle makes
  division by all six color-name permutations exact.
- The current one-cut-at-a-time route is sound but inefficient.  At the
  published prefixes, the 192 `hole5` cuts occupy only 31 template-symmetry
  orbits and the 384 `hole7` cuts only 59.  Orbit closure covers respectively
  2,832 of 3,645 and 986 of 1,701 compatible partitions.
- Further unchanged CEGAR production is therefore suspended while a new,
  separately audited proof-producing template-bank path is implemented.
  The append-only CEGAR runs remain frozen and resumable as corroborating
  evidence.

### Claim boundary and next actions

- The 448-cut `hole5` prefix is not a mathematical nonexistence result.
- The coloring-bank theorem and implementation are not promoted until a
  self-contained proof, deterministic generator, independent enumerator,
  mutation audit, and proof-producing trial all pass.
- Publish this checkpoint.  Then complete the independent bank audits and
  run bounded full-bank instances, freezing any SAT candidate and requiring
  a fresh independently checked RUP/DRAT proof for every UNSAT result.

## Checkpoint 020 — 2026-07-25 19:24 PDT

- Campaign day: 1 of 27; branch `main`.
- Latest pushed campaign checkpoint: `1119231a`.
- Claim C-028 is now accepted as `CERTIFIED-FINITE`: no connected
  12-vertex graph with
  \(\gamma=\alpha=\gamma^\infty=3<\theta\) has a complement containing a
  hub-free induced \(C_9\).  By C-014 this removes induced \(C_9\) entirely
  from a surviving order-12 parameter-three counterexample complement; by
  C-017, only the overlapping hub-free \(C_5\) and \(C_7\) branches remain.
  The self-contained graph-to-CNF implication received a separate
  line-by-line hostile `ACCEPT` review.
- The accepted recovery binds the exact 6,886-variable, 20,200-clause CNF,
  170 globally valid coloring cuts, and a deletion-free proof of 4,705 RUP
  additions ending in the empty clause.  A fresh standard-library checker
  independently replayed all additions, all 170 chronology links, and 2,210
  artifact bindings and rejected 11 hostile mutations.
- The original `hole9` checkpoint deliberately remains `running`; no
  terminal marker was retroactively created.  The recovered certificate,
  two validated documentation errata, sealed package, outer certificate,
  hostile review, and standalone probe are bound together in
  `results/synthesis_k3_hole9_orphan_recovery_acceptance.json`.
- `hole5` advanced cleanly from 64 to 192 attempts/cuts.  Its checkpoint
  SHA-256 is
  `1596f9194d44b90be5a1ec583f68e8da8a3050aa0a584fc733ce920ccd441b89`;
  deep audit preserved the 1,347-file, 6,688,922-byte tree at SHA-256
  `143a09afb4124c8ad4580f7a38bb3bd9312f2a99e89649cba28d99fe5eec050c`.
  The branch remains open.  `hole7` remains open at 384 cuts.

### Verification and resource event

- Root replayed the sealed-package audit, all 12 focused recovery tests, and
  the independent hostile RUP probe successfully.
- A new full-suite invocation ran 238 tests: 227 passed and 11 synthesis
  smoke tests did not execute because their intended disk preflight gate
  rejected the current free-space envelope.  There were zero assertion
  failures.  This first invocation is not recorded as a passing full suite.
- After unrelated local activity released disk space, free space rebounded
  to approximately 9.9 GB.  The unchanged full suite was rerun in one
  complete invocation and passed all 238 tests in 57.44 seconds, with peak
  RSS 115,965,952 bytes.  The earlier refusal remains recorded as evidence
  that the fail-closed resource gate worked.
- No campaign solver or proof-checker child was active at checkpoint
  creation.

### Claim boundary and next actions

- C-028 excludes one of the three exhaustive order-12 parameter-three
  branches.  It does not exclude `hole5` or `hole7`, does not certify the
  complete \((12,3)\) slice, and does not resolve the conjecture.
- Commit and push the complete accepted `hole9` recovery bundle and the
  resumable 192-cut `hole5` checkpoint.
- After publication, continue human-readable structural analysis and
  proof-extraction from the remaining \(C_5/C_7\) cut populations.  Resume
  bounded production only when each fresh resource preflight passes and
  continues to preserve the 4 GiB reserve.

## Checkpoint 019 — 2026-07-25 19:12 PDT

- Campaign day: 1 of 27; branch `main`.
- Latest pushed campaign checkpoint: `eea8aece`.
- All three required direct-synthesis templates now have production
  artifacts: `hole9` has a candidate recovered terminal under review,
  `hole7` is running at 384 cuts, and `hole5` is running at 64 cuts.
- The new `hole5` checkpoint SHA-256 is
  `02bbf56a292c734fcd886af55b9482439e29a263c8acc1e904883242da5e12dc`.
  Deep reconstruction preserved its 451-file, 2,224,274-byte tree at
  SHA-256
  `73384b72019434b9d1a60aab38773257035e4e7464a3ea9088d31941e6f57b55`.
- No timeout, unknown result, candidate, UNSAT terminal, or resource event
  occurred in the 64 `hole5` attempts.  No heavy child was active at
  checkpoint creation.

### Claim boundary and next actions

- Neither open prefix is a mathematical result, and `hole9` is not accepted
  before hostile review.
- Publish the first `hole5` checkpoint.  Continue both open branches in
  measured batches, prioritizing the branch with the faster terminal yield.
- Complete and integrate the independent `hole9` RUP audit and both explicit
  errata without changing the frozen source run.

## Checkpoint 018 — 2026-07-25 19:09 PDT

- Campaign day: 1 of 27; branch `main`.
- Latest pushed campaign checkpoint before this batch: `58d3b363`.
- `hole7` has 384 complete SAT/coloring attempts and globally valid cuts,
  checkpoint SHA-256
  `81f62e83cf6a910c6b9baabe0edff7ab26543e787cad91a7e261323ae52e18c6`,
  and status `running`.
- Deep reconstruction preserved the 2,691-file, 13,353,372-byte tree at
  SHA-256
  `43ca4d29ea369900480d5cf90ab52e53b77b5600d03d4d0d5eba37402f1a7b3c`.
- The branch has required more cuts than `hole9`, but all 128 new solver
  children remained below 0.095 seconds and 7.9 MB RSS.
- The `hole9` recovery and its explicit ART-115/prose errata remain under
  independent hostile review.  No heavy child was active at checkpoint
  creation.

### Claim boundary and next actions

- The 384-cut `hole7` prefix proves no template nonexistence.
- Publish this checkpoint.  Continue with another bounded batch while
  monitoring cut yield and audit time; stop or redesign only at a measured
  scaling gate.
- Integrate `hole9` only after the independent RUP replay returns a final
  verdict.

## Checkpoint 017 — 2026-07-25 19:05 PDT

- Campaign day: 1 of 27; branch `main`.
- Latest pushed campaign checkpoint before this batch: `c64779c1`.
- `hole7` has reached 256 complete SAT/coloring attempts and cuts, with
  checkpoint SHA-256
  `d3dd1138286340b7ec9667596b98998d17ea9937b332e8dfa1b1dcb81e4f4ca6`.
  Its status is still `running`; there is no terminal or resource event.
- Deep read-only reconstruction preserved the 1,795-file, 8,907,069-byte
  tree at SHA-256
  `e699cfa165062acf890be869beaf97dadf3a1b90ff1bb58cab2bd57df00ca1e3`.
- The `hole9` author package and two narrow provenance/prose errata are
  frozen.  The independent hostile audit, including a fresh RUP
  implementation, is still running.
- No heavy child was active at checkpoint creation.

### Claim boundary and next actions

- A 256-cut prefix remains only resumable search progress.
- Publish it, continue `hole7` with another bounded batch, and retain the
  4 GiB disk reserve.
- Do not promote `hole9` before the hostile audit accepts the proof package
  and both errata.

## Checkpoint 016 — 2026-07-25 19:02 PDT

- Campaign day: 1 of 27; branch `main`.
- Latest pushed campaign checkpoint before this batch: `5d0a13f8`.
- `hole7` now has 192 complete SAT/coloring attempts and globally sound
  cuts.  Its checkpoint SHA-256 is
  `70ed71127081efae5e9e85f3bd9c6a2ddefcccf3db992d416d795f3edd1f6d84`;
  status remains `running`.
- Deep read-only reconstruction preserved the exact 1,347-file,
  6,685,492-byte run tree at SHA-256
  `8ccae877b89b167a859bdd7f6dcd42937110fe7a0b725c0425fe2e24c15dd800`.
- The `hole9` recovery author package is frozen and has passed 12 focused
  and 238 full-suite tests, but independent review remains active.  That
  review found a one-digit truncation in ART-115's manually transcribed
  `cuts.json` hash; the immutable log is retained and a narrow machine-
  readable erratum now supplies the correct binding.
- No heavy child was active when this checkpoint was written.

### Claim boundary and next actions

- Neither the 192-cut `hole7` prefix nor the author-verified `hole9`
  recovery is yet a template-level theorem.
- Publish this prefix.  Continue `hole7` in bounded batches while the fresh
  independent RUP implementation and erratum audit finish.
- Accept or reject `hole9` only on the final hostile verdict; if accepted,
  register it as one of three required overlapping templates, not as the
  complete \((12,3)\) slice.

## Checkpoint 015 — 2026-07-25 18:58 PDT

- Campaign day: 1 of 27; branch `main`.
- Latest pushed campaign checkpoint before this batch: `f7994c26`.
- `hole7` now has 128 complete SAT/coloring attempts and 128 globally sound
  cuts.  Its checkpoint SHA-256 is
  `37eb33e4d35084d8a7e930b88be94d71e3b602f8f4ed10c2e7b2e5fbecf5afe2`;
  status remains `running`.
- Deep reconstruction passed and preserved the 899-file, 4,456,636-byte
  tree at SHA-256
  `b8f038f5bdebde5d457b785bc38339c11e3e2f658d8a3f262a9b7dd30a6a8231`.
- No timeout, unknown outcome, memory event, candidate, or UNSAT terminal
  occurred.  No heavy child was active when this checkpoint was written.

### Claim boundary and next actions

- The branch is healthy but still proves no nonexistence statement.
- Publish the 128-cut prefix, then run another bounded `hole7` batch.
- Continue the independent `hole9` recovery audit concurrently; retain the
  original runner and run directories byte-for-byte.

## Checkpoint 014 — 2026-07-25 18:54 PDT

- Campaign day: 1 of 27; branch `main`.
- Latest pushed campaign checkpoint: `2c6ce8da`.
- The new `hole7` production run has 64 complete SAT/coloring attempts and
  64 globally sound cuts.  Its checkpoint SHA-256 is
  `5677bd2323dca1f78c330555d0e2ed443d5993f63c546ad0d22479de5c886a2f`;
  status remains `running`, with no terminal or resource event.
- Deep read-only reconstruction passed and preserved the exact 451-file,
  2,233,086-byte run tree at SHA-256
  `6ce2af652b3bcd91184ec2d3cef73822b9de226bff0979ed7e444ba810c149ee`.
- The accepted portable-core package is pushed.  The separate `hole9`
  recovery package remains pending an independent hostile audit.
- No solver or proof-checker child was active when this checkpoint was
  written.

### Claim boundary and next actions

- Sixty-four valid coloring cuts do not exclude the `hole7` template.
- Publish this resumable prefix before another bounded batch.
- Continue `hole7`; in parallel, finish the independent `hole9` RUP audit.
  Start `hole5` after a published checkpoint or a terminal, subject to the
  4 GiB disk reserve.

## Checkpoint 013 — 2026-07-25 18:50 PDT

- Campaign day: 1 of 27; branch `main`.
- Latest pushed campaign checkpoint before this checkpoint: `31586830`.
- The portable-failure-core package is independently accepted.  Root reran
  its installed audit and all eight focused tests successfully.
- Two finite obstruction cores, `J@l|bfNuVK_` and `Kun_w{vRrblV`, have
  independently replayed three-guard failure DAGs and stable four-guard
  kernels.  They compress the eight deepest C-023 failures to two induced
  cores; exactly 37 of the fixed 526 rows contain induced `J`.
- The 623-key one-vertex-extension sweep over `J` is retained only as
  `OBSERVED`; it does not raise the exhaustive order frontier.
- A separate `hole9` recovery package has been produced and passes its author
  audit.  It binds a 4,705-addition deletion-free RUP proof, but remains
  outside the claim registry while a fresh independent implementation and
  hostile review are running.
- No synthesis solver or proof-checker child was active at checkpoint
  creation.  Approximately 8.2 GiB of disk remained, including the campaign's
  4 GiB do-not-use reserve.

### Active gate and claim boundary

- Claims C-025--C-027 delimit the portable-core theorem, exact finite core
  facts, and the broader observation respectively.  None resolves the
  conjecture or proves an order bound.
- The original `hole9` runner still has status `running`; its orphan proof is
  not retroactively promoted.  Only a separately frozen recovery certificate
  may support a template-level claim, and only after hostile acceptance.

### Next three highest-value actions

1. Commit and push the accepted portable-core package.
2. Complete the independent `hole9` RUP replay and hostile audit; accept or
   reject the template certificate without modifying the frozen run.
3. If accepted, launch separate bounded `hole7` and `hole5` production runs
   under the same immutable resource discipline.

## Checkpoint 012 — 2026-07-25 18:27 PDT

- Campaign day: 1 of 27; branch `main`.
- Latest pushed campaign checkpoint before this session: `2c935e45`.
- The clean `hole9` checkpoint has 170 complete SAT/coloring attempts and
  170 globally sound cuts.  SHA-256:
  `9cc9cdee08fb1fcd7a8772b09cdf9ba9ced802cb0b31be35ab292244e5f286b7`.
- The next formula returned `UNSAT` twice and has a nonempty DRAT proof, but
  the frozen production checker exited 80 on a hard warning.  The runner
  failed closed: there is no terminal, no referenced attempt 170, and no
  accepted UNSAT claim.
- Verbose bounded diagnosis identifies a pseudo-unit deletion warning in
  pinned DRAT-trim forward mode.  Adding documented plain mode `-p` causes
  the unchanged proof to verify with exit zero, exactly one `s VERIFIED`,
  and no warning, but this route is not trusted until separately audited.
- Deep audit of the committed prefix passed.  The preserved 1,205-file,
  6,946,580-byte tree has SHA-256
  `bd13c4fdc3629ee02fa510eda09bd503234daf4318a33c562e0ab3427d89fd8b`.
  ART-115 binds the incident and every decisive orphan-artifact hash.

### Active gate and claim boundary

- `hole9` production is paused.  Retrying the unchanged frozen runner would
  only reproduce the same warning and is not useful.
- A separately written recovery verifier must reconstruct the exact
  base-plus-170-cut CNF, verify both UNSAT result files and all hashes, and
  replay the pinned proof under a hostile-reviewed deletion policy.
- An independent reviewer is auditing the mathematical soundness of ignoring
  DRAT deletion instructions.  Until both reviews accept, the proof remains
  a candidate artifact and the `hole9` template remains open.
- No solver/checker child was active when this checkpoint was written.

### Next three highest-value actions

1. Commit and push the 170-cut checkpoint and frozen failed terminal attempt.
2. Complete and hostile-review the independent terminal-recovery verifier;
   accept or reject the candidate proof without changing the frozen runner.
3. In parallel, finish the portable induced-failure-core theorem and its
   exact two-core certificates.

## Checkpoint 011 — 2026-07-25 18:21 PDT

- Campaign day: 1 of 27; branch `main`.
- Latest pushed campaign checkpoint before this batch: `fec94bbe`.
- `hole9` has reached 129 complete SAT/coloring attempts and 129 globally
  sound cuts.  Checkpoint SHA-256:
  `9f0b91e483f255f2e18b7383811cf4e2937b76d0590be4e9dc5cfcb36dcc51f1`.
- Deep read-only reconstruction passed; the exact 906-file, 4,475,400-byte
  tree retained SHA-256
  `f844ead52f7e719b9ec23b74165ee5a3f31ce4b55cc6b1a433533df4be79c85e`.
- There is no terminal, timeout, unknown result, or resource event.  The
  template and conjecture remain unresolved.
- No synthesis child was active at checkpoint creation.
- Next actions: publish this prefix; run one more bounded 64-iteration
  session; separately package and hostile-review the portable induced-core
  lemma and the exact two-core explanation of the deepest near-misses.

## Checkpoint 010 — 2026-07-25 18:18 PDT

- Campaign day: 1 of 27; branch `main`.
- Latest pushed campaign checkpoint before this batch: `f8a53384`.
- `hole9` now has 65 complete SAT/coloring attempts and 65 globally sound
  cuts.  Checkpoint SHA-256:
  `2f092df32138fa14bc2c97cf2ec819a38064d050325eff018cd1b5ef657dcd87`.
- A separate deep read-only audit passed and preserved the exact 458-file,
  2,257,731-byte tree, SHA-256
  `3e763ccd9d833f8c4b6deb492ec2bc2ccdf87c777e3cfe86ccc8096d17b48bc5`.
- No terminal, timeout, unknown result, or resource event occurred.  The
  conjecture and the `hole9` template both remain unresolved.
- No synthesis child was active when this checkpoint was written.
- Next actions: publish this checkpoint; resume a bounded 64-iteration
  batch; independently freeze and review the portable induced-obstruction
  lemma emerging from the two deep local cores.

## Checkpoint 009 — 2026-07-25 18:15 PDT

- Campaign day: 1 of 27; 26 campaign days remain.
- Repository branch: `main`.
- Latest pushed campaign checkpoint before this batch: `2e144ffb`.
- Completion estimate for the campaign work plan: **47%**.
- Completion estimate toward an actual universal resolution: **10%**.
  The conjecture remains unresolved; neither estimate is a mathematical
  probability.

### Verified production state

- `hole9` batch 001 added 32 validated coloring cuts.  The run now contains
  33 complete SAT/coloring attempts and 33 distinct globally sound cuts.
- Live checkpoint SHA-256:
  `0bf9fabdaf6d69974b698e66fdb731a19a04ed64f4d0bdbda878ce6dc2cb624c`;
  history-chain SHA-256:
  `37497c92f25530c1955c614d94ed5d7069a258de77a78620c5acfab90189eafa`.
- A deep read-only audit passed.  The 234-file, 1,146,858-byte run tree had
  SHA-256
  `32418469c3c2e6ea5e5b1895e6dbf268092ceb4d2231a1774212957c3326ee73`
  both before and after audit.
- Batch wall time was 16.9724 seconds.  No solver child exceeded 0.030
  seconds or 5.08 MiB peak RSS; no timeout, unknown outcome, memory event,
  candidate, or UNSAT terminal occurred.
- ART-112 binds the batch.  The original one-cut checkpoint is now preserved
  immutably as ART-110 rather than pointing at the advancing live file.

### Claim boundary and active routes

- The 33 cuts are each sound, but a running CEGAR prefix proves no
  nonexistence result.
- The direct synthesis route remains active and healthy; another bounded
  batch is justified after publishing this checkpoint.
- The structural lane has provisionally found that seven of the eight
  deepest transition-kernel rows contain one common induced 11-vertex
  obstruction, while the deepest row is a second vertex-minimal core.
  Exact embeddings, proof wording, and independent artifacts remain under
  preparation; no new claim has yet been registered.

### Running jobs and resume state

- No synthesis child was active when this checkpoint was written.
- Resume `hole9` from cut 33 using the immutable configuration and a
  32-iteration budget.  The full command is identical to Checkpoint 008
  except for the already advanced checkpoint.

### Next three highest-value actions

1. Commit and push the 33-cut production checkpoint and batch audit.
2. Resume another bounded `hole9` batch, deep-audit it, and continue until a
   terminal or a measured yield/resource gate.
3. Freeze and hostile-review the induced-obstruction lifting lemma and the
   exact two-core explanation of the eight deepest near-misses.

## Checkpoint 008 — 2026-07-25 18:12 PDT

- Campaign day: 1 of 27; 26 campaign days remain.
- Repository branch: `main`.
- Accepted runner commit: `149378de`, pushed before launch.
- Completion estimate for the campaign work plan: **47%**.
- Completion estimate toward an actual universal resolution: **10%**.
  The conjecture remains unresolved; neither estimate is a mathematical
  probability.

### Verified production state

- The first bounded `hole9` production iteration is committed and
  read-only-audited.  It produced one complete SAT model, one proper
  complement three-coloring, and one globally sound 19-literal coloring
  cut.
- Checkpoint SHA-256:
  `075bdb8e168d1b6edeca6470a56fdc00be4624adaa7f80433b053306b49eb90e`.
  Run-manifest SHA-256:
  `73869e60bdefc547a91139ab3bfb0673ee8168acada62485089eb371a9d7c15d`.
- The exact ten-file run tree contains 39,706 bytes.  Its canonical
  length-prefixed SHA-256 was
  `691838bced032e72ab037d13f547c2dbfe9eb4351c8c486814c166a8feb7c847`
  both before and after `--audit-only --deep-reconstruct`.
- The solver child took 0.028558 seconds and about 4.86 MiB peak RSS.  The
  checkpoint remains `running`, with one attempt, one cut, and no terminal.
  ART-108--111 bind the trial log, run manifest, checkpoint, and attempt.

### Claim boundary

- A colorable SAT iteration only supplies a globally sound cut.  It excludes
  neither the `hole9` template nor any graph class.
- No proof-producing UNSAT or candidate exists yet.
- Every future resume must use the immutable accepted configuration.  Any
  terminal UNSAT still requires deep reconstruction and a fresh pinned DRAT
  replay before it can support a claim.

### Running jobs and resume command

- No synthesis child was active when this checkpoint was written.
- Resume from cut 1 with:

```text
PYTHONPATH=src PYTHONWARNINGS=error python3 -m synthesis_k3.cegar \
  --validation-gate-open --template hole9 \
  --run-dir results/synthesis_k3_runs/hole9 \
  --max-iterations 32 --seed 0 \
  --solver-wall-seconds 60 --solver-memory-mib 2048 \
  --checker-wall-seconds 60 --checker-memory-mib 2048 \
  --session-wall-seconds 7200 --disk-reserve-mib 4096 \
  --child-file-limit-mib 256 --retained-attempt-limit-mib 1
```

### Next three highest-value actions

1. Commit and push this first production checkpoint before resuming.
2. Resume `hole9` in a bounded 32-iteration batch, then deep-audit and
   checkpoint regardless of terminal status.
3. Continue the independent induced-subgraph analysis of the eight deepest
   transition-kernel near-misses.

## Checkpoint 007 — 2026-07-25 18:07 PDT

- Campaign day: 1 of 27; 26 campaign days remain.
- Repository branch: `main`.
- Latest published campaign commit before this checkpoint:
  `52ba220e` (full hash recorded in Git).
- Completion estimate for the campaign work plan: **46%**.
- Completion estimate toward an actual universal resolution: **10%**.
  The conjecture remains unresolved; neither estimate is a mathematical
  probability.
- Literature audit date: 2026-07-25.  No prior resolution has been found;
  exact first-use wording in the unavailable 2020 chapter remains pending.

### Verified facts and artifacts

- The order-12, parameter-three proof-producing CEGAR runner is frozen and
  independently accepted for bounded production.  The source, 23 focused
  tests, protocol, hostile review, and independent mutation probe are bound
  as ART-103--107.
- The frozen CEGAR source SHA-256 is
  `411fffff34c0122d679ee710aff0e3856a7ff166bff30c69edb1f0044defce8c`;
  its complete runtime-source-set SHA-256 is
  `8c4e811bc4250c3e2b0b7edeb8afd07f7509ebda3cbae3db1b3ca82c07b35299`.
- The independent hostile audit rejected the former fabricated-UNSAT
  exploit, all six rebound field mutations, and a later-checkpoint forgery.
  It verified exact outcome schemas, chronological predecessor digests,
  read-only audits, linear history work, crash markers, per-run/global
  locks, synchronous signal cleanup, resource gates, and a live pinned DRAT
  proof.
- A separate mathematical audit accepted the complement/static/game/cut
  semantics.  Root independently reran the complete campaign suite:
  218 of 218 tests passed in 27.156 seconds.
- Previously published C-022--C-024 remain unchanged.  This launch
  acceptance is not itself a new mathematical claim or a finite
  nonexistence result.

### Claim and review boundary

- No production template has yet reached a terminal.  An accepted runner
  does not exclude even one graph or template.
- A template-level `UNSAT` is acceptable only after exact final-CNF
  reconstruction and a fresh pinned proof replay with
  `--deep-reconstruct --verify-terminal-proof`.
- Excluding the complete `(n,k)=(12,3)` slice requires verified terminals
  for all three accepted `hole5`, `hole7`, and `hole9` branches together
  with the already reviewed structural coverage theorem.
- A DSATUR no-color model is only a quarantined candidate; it requires the
  campaign's entirely separate counterexample certificate workflow.

### Approach registry

| Route | Status | Exact gate/obstruction |
|---|---|---|
| Literature/status audit | active-weekly | 2020 chapter text, unavailable `C4`-free manuscript, and general constructive well-covered generators remain gaps |
| Exact evaluators/certificates | complete-for-current-artifacts | A/B, full fixed-point traces, recursive trees, and proof-producing synthesis audit accepted |
| MMV one-vertex extensions | complete-certified | C-018 covers 110,537 origins and 54,216 canonical graphs |
| Single-edge toggles of closest seeds | complete-certified | C-019 covers 25,641 origins and 19,136 canonical graphs |
| Direct synthesis `(12,3)` | active-production-open | Runner accepted; exact one-iteration `hole9` trial and read-only audit are next |
| Structural `k=3` lane | active-high-yield | Eight deep transition graphs are under common-structure analysis |
| General well-covered generation | blocked | No audited complete constructive generator/catalog for orders 12--16 |

### Running jobs and resume state

- No production solver or search process was active when this checkpoint was
  written.
- The next run directory is
  `results/synthesis_k3_runs/hole9`; it does not yet exist.
- The accepted one-iteration launch uses seed 0, 60-second
  solver/checker child limits, 2,048 MiB child ceilings, a 7,200-second
  session admission budget, a 4,096 MiB disk reserve, a 256 MiB child-file
  cap, and a 1 MiB retained-attempt cap.

### Resource usage

- Host: MacBookPro18,1, Apple M1 Pro, 10 cores, 16 GiB RAM.
- Root full campaign suite: 218 of 218 tests in 27.156 seconds.
- Final hostile probe: 9.895 seconds; focused suite: 23 of 23 in 14.908
  seconds.
- Free disk is approximately 8.3 GiB.  Production retains a 4 GiB reserve,
  permits only one heavy child globally, and requires the child ceiling plus
  512 MiB of currently reclaimable memory.
- The session wall is an admission budget over local orchestration overhead;
  individual solver/checker children have hard wall and memory limits.

### Next three highest-value actions

1. Commit and push the accepted frozen runner and audit artifacts before
   creating any production directory.
2. Run exactly one `hole9` CEGAR iteration, inspect every generated role,
   then perform a separate read-only deep audit.
3. If clean, resume `hole9` in bounded batches to a candidate or
   proof-verified terminal while continuing structural analysis of the eight
   deepest near-misses.

## Checkpoint 006 — 2026-07-25 17:35 PDT

- Campaign day: 1 of 27; 26 campaign days remain.
- Repository branch: `main`.
- Latest published campaign commit before this checkpoint:
  `7215b4db` (full hash recorded in Git).
- Completion estimate for the campaign work plan: **44%**.
- Completion estimate toward an actual universal resolution: **10%**.
  The conjecture remains unresolved; neither estimate is a mathematical
  probability.
- Literature audit date: 2026-07-25.  The University of North Florida
  institutional record now verifies the 2020 chapter metadata, but no
  lawful full text was obtained; exact first use of the name
  “Gamma-Theta Conjecture” remains pending.

### Verified facts and artifacts

- Claim C-022 is proved and hostile-review accepted.  Recursive online
  survival and failure trees exactly characterize every finite kernel
  \(\mathcal K_h\), and one finite failure tree at a forced maximum
  independent state proves a strict eternal-domination lower bound.
- The \(C_{15}\) certificate proves strict separation:
  \((|K_0|,|K_1|,|K_2|,|K_3|)=(765,120,15,0)\).  Its positive \(K_2\)
  tree has 73 nodes and its negative \(K_3\) tree has eight.
- Claim C-023 is a certificate-backed finite result on the exact 526
  edge-toggle rows surviving \(K_2\).  Direct third-ply trees eliminate
  518.  Seven remaining graphs first lose a forced triple at \(K_5\), one
  at \(K_6\), and all full kernels are empty by \(K_7\).
- The 518 serialized trees total 5,540 nodes and 3,174 leaves.  A fully
  separate frozenset verifier replayed them all, independently recomputed
  all 8,587 source profiles and 64,893 selected configuration ranks, checked
  exact 518-plus-8 coverage, and rejected 14 decisive mutations.
- The theorem, source, tests, result, two certificate files, hostile review,
  independent probe, and probe log are bound as ART-090--098.

### Claim and review boundary

- C-022 is a universal certificate theorem and necessary condition, not a
  universal proof of the Gamma-Theta Conjecture.
- C-023 covers only the recorded edge-toggle-derived family.  It does not
  enumerate all graphs of order 11 or 12 and does not raise the published
  global order frontier.
- The proof-producing `(n,k)=(12,3)` runner remains blocked from production.
  Its repaired security paths pass 21 focused and 208 full-suite tests, but
  hostile re-audit identified remaining quadratic historical cut replay and
  two provenance checks requiring a second repair and re-audit.

### Approach registry

| Route | Status | Exact gate/obstruction |
|---|---|---|
| Literature/status audit | active-weekly | 2020 institutional metadata improved; chapter text, unavailable `C4`-free manuscript, and general well-covered generators remain gaps |
| Exact evaluators/certificates | complete-for-current-artifacts | A/B, full fixed-point traces, and recursive-tree hostile replay accepted |
| MMV one-vertex extensions | complete-certified | C-018 covers 110,537 origins and 54,216 canonical graphs |
| Single-edge toggles of closest seeds | complete-certified | C-019 covers 25,641 origins and 19,136 canonical graphs |
| Direct synthesis `(12,3)` | active-hostile-repair | Security blockers closed; ordinary history audit must become linear and provenance chronology must be exact before production |
| Structural `k=3` lane | active-high-yield | C-023 removes 98.5% of the 526 two-ply survivors at the third ply; eight deep graphs retained for structure/local robustness |
| General well-covered generation | blocked | No audited complete constructive generator/catalog for orders 12--16 |

### Running jobs and resume state

- No production solver or search process is active.
- The CEGAR second repair/re-audit round is active.  There is still no
  `results/synthesis_k3_runs/` production checkpoint.
- A small deterministic radius-two toggle-ball measurement around the
  deepest graph is being packaged separately as an observation.

### Resource usage

- Host: MacBookPro18,1, Apple M1 Pro, 10 cores, 16 GiB RAM.
- Third-ply production measurement: 23.77 seconds wall, 23.69 seconds CPU,
  about 53.4 MiB peak RSS.  Independent complete replay: 13.10 seconds.
- CEGAR repaired focused suite: 21 of 21 in 12.79 seconds; the author's full
  repository run passed 208 of 208 in 24.70 seconds.
- Free disk is approximately 8.7 GiB.  Production retains a 4 GiB reserve,
  a campaign-global heavy-child lock, and a current-memory headroom gate.

### Next three highest-value actions

1. Close the linear-history and provenance findings, obtain a final hostile
   acceptance on frozen CEGAR bytes, and commit the runner before launch.
2. Run and inspect exactly one proof-producing `C9` iteration, then resume
   bounded batches to a terminal and independently replay any DRAT proof.
3. Complete the bounded radius-two robustness measurement and analyze the
   eight deep transition graphs for a human-readable parameter-three lemma.

## Checkpoint 005 — 2026-07-25 16:52 PDT

- Campaign day: 1 of 27; 26 campaign days remain.
- Repository branch: `main`.
- Latest published campaign commit before this checkpoint:
  `d4e08098` (full hash recorded in Git).
- Shared-main HEAD observed during checkpoint preparation:
  `0addfeed` (unrelated research advanced `main` after the last campaign
  commit).
- Completion estimate for the campaign work plan: **41%**.
- Completion estimate toward an actual universal resolution: **10%**.
  The conjecture remains unresolved; neither estimate is a mathematical
  probability.
- Literature audit date: 2026-07-25.  The audit was refreshed out of cycle
  for finite-order, infinite-order, offline, and adaptive-online terminology.

### Verified facts and artifacts

- Claim C-020 is proved and hostile-review accepted.  The finite transition
  kernels descend to the greatest eternal family, and equality
  `alpha=gamma-infinity=k` forces every maximum independent `k`-set into
  the second online kernel.  The resulting two-ply private-region
  obstruction is a compact lower-bound certificate.
- The `C7` example proves strict separation from the earlier one-step
  condition.  Six focused tests compare the implementation with a
  transparent second-kernel oracle on every labeled graph through order 5;
  the complete campaign suite passes 195 of 195 tests.
- Claim C-021 records the filter measurement conservatively as `OBSERVED`.
  Of 8,587 selected edge-toggle near-misses, 8,061 fail within two steps and
  526 survive.  A fresh ordinary-set implementation independently reproduced
  these counts and the complete connected-unlabeled order-5-through-9
  measurements.
- Burger et al.'s 2004 finite- and infinite-order primary papers are locally
  archived and hash-bound as ART-081--082.  The finite smart-\(q\) model has
  offline quantifiers with the complete attack sequence known in advance;
  the campaign kernels are adaptive online.  The theorem note and hostile
  review explicitly preserve that distinction and make no broad novelty
  claim.
- The theorem, implementation, tests, measurement, hostile review, standalone
  replay, and mutation suite are bound as ART-083--089.

### Claim and review boundary

- C-020 is a universal necessary condition, not a proof of the
  Gamma-Theta Conjecture and not a sufficient characterization of eternal
  domination.
- C-021 measures fixed recorded populations.  It does not prove a complete
  nonexistence result for order 10 or above, and the 526 survivors have not
  been classified by the two-step test.
- The proof-producing `(n,k)=(12,3)` runner is implemented and passes 15
  focused tests plus the 195-test full suite, but it remains under an
  independent hostile pre-launch audit.  No production CEGAR run or proof
  package exists yet.

### Approach registry

| Route | Status | Exact gate/obstruction |
|---|---|---|
| Literature/status audit | active-weekly | Offline/online finite-horizon refresh complete; unavailable `C4`-free manuscript and general well-covered generators remain gaps |
| Exact evaluators/certificates | complete-for-current-artifacts | A/B plus independent finite-search and two-step hostile replays passed |
| MMV one-vertex extensions | complete-certified | C-018 covers 110,537 origins and 54,216 canonical graphs |
| Single-edge toggles of closest seeds | complete-certified | C-019 covers 25,641 origins and 19,136 canonical graphs |
| Direct synthesis `(12,3)` | active-hostile-prelaunch | Runner built and tested; proof/cut/resume/path/resource audit must accept its exact hash before production |
| Structural `k=3` lane | active-high-yield | C-020 removes 93.9% of the selected hardest near-misses within two plies; analyze the 526 survivors or a third kernel round |
| General well-covered generation | blocked | No audited complete constructive generator/catalog for orders 12--16 |

### Running jobs and resume state

- No production search or solver process is active.
- The independent CEGAR-runner hostile audit is active.  No
  `results/synthesis_k3_runs/` production checkpoint exists.
- The two-step source-bound measurement and independent replay are complete
  at the hashes in ART-086 and ART-088.  Reproduction commands are recorded
  in `README.md`.

### Resource usage

- Host: MacBookPro18,1, Apple M1 Pro, 10 cores, 16 GiB RAM.
- Two-step measurement: 94.03 seconds wall, 91.91 seconds CPU, 25.06 MiB
  peak RSS.  Independent replay: 61.71 seconds wall, 25.11 MiB peak RSS.
- CEGAR focused tests and full campaign suite: 21 of 21 and 195 of 195
  passed in 4.29 and 16.01 seconds.
- Free disk is approximately 8.4 GiB.  The CEGAR runner defaults to a 4 GiB
  do-not-use reserve and permits only one solver/checker child at a time.

### Next three highest-value actions

1. Finish the independent hostile audit of the CEGAR runner and close every
   critical, high, and medium pre-launch finding.
2. Commit the accepted runner, launch one proof-producing `C9` iteration,
   inspect it, and then resume to a verified terminal before `C7` and `C5`.
3. Analyze the 526 depth-two survivors for a third-ply obstruction or a
   human-readable parameter-three structural lemma.

## Checkpoint 004 — 2026-07-25 16:24 PDT

- Campaign day: 1 of 27; 26 campaign days remain.
- Repository branch: `main`.
- Latest published campaign commit before this checkpoint:
  `ace5d109` (full hash recorded in Git).
- Shared-main HEAD observed at checkpoint creation:
  `a915e9d5b46b184b9ec5bf8b2f44c02886ffb82b`.
- Completion estimate for the campaign work plan: **36%**.
- Completion estimate toward an actual universal resolution: **8%**.
  The conjecture remains unresolved; neither estimate is a mathematical
  probability.
- Literature audit date: 2026-07-25.  No new terminology requiring an
  out-of-cycle refresh arose in this checkpoint.

### Verified facts and artifacts

- The single-edge-toggle search around the 391 closest extension seeds is
  now independently certified as claim C-019.  Its exact universe comprises
  25,641 seed/pair origins and 19,136 isomorphism classes.
- The standalone coverage audit reconstructed every toggle, checked an
  explicit raw-to-key isomorphism for every origin, and reconciled all
  multiplicities.  A separate hostile reconstruction accepted the result
  with no critical, high, or medium finding.
- A third mathematical implementation proves `gamma < gamma-infinity` on
  every canonical row: 7,934 rows have `gamma=2`, 11,202 have `gamma=3`,
  and complete simultaneous fixed-point traces delete all 1,235,981
  dominating configurations at `k=gamma`.  An independent frozenset replay
  checked every domination blocker and one-guard deletion round.
- The final coverage report, receipt state, mathematical certificates, audit
  report, checker source sets, and both hostile reviews are manifest-bound as
  ART-070--080.  Read-only replay commands are documented in `README.md`.

### Claim and review boundary

- C-019 is a certificate-backed negative result only for one edge toggle of
  each of the specified 391 seeds.  It is not a complete order-12
  enumeration, does not improve the published all-graph order frontier, and
  does not resolve the conjecture.
- The accepted three-template reduction and base CNF stack make a complete
  `(n,k)=(12,3)` result possible if all three proof-producing CEGAR branches
  terminate and their coverage/cut/proof packages pass independent audit.
- A temporary `C9` dry run reached unlogged solver `UNSAT` after 170 cuts;
  `C7` and `C5` hit their 90-second exploratory gates at 594 and 543 cuts.
  These are workload observations only and are not claims.

### Approach registry

| Route | Status | Exact gate/obstruction |
|---|---|---|
| Literature/status audit | active-weekly | Current refresh complete; unavailable `C4`-free manuscript and general well-covered generators remain gaps |
| Exact evaluators/certificates | complete-for-current-artifacts | A/B plus independent coverage, mathematical, and hostile replays passed |
| MMV one-vertex extensions | complete-certified | C-018 covers 110,537 origins and 54,216 canonical graphs |
| Single-edge toggles of closest seeds | complete-certified | C-019 covers 25,641 origins and 19,136 canonical graphs |
| Direct synthesis `(12,3)` | active-orchestrator-audit | Base encoding accepted; resumable proof-producing runner is being completed before hostile launch review |
| Structural `k=3` lane | active | C-017 accepted; a stronger transition-kernel condition is under independent development |
| General well-covered generation | blocked | No audited complete constructive generator/catalog for orders 12--16 |

### Running jobs and resume state

- No production search or solver process is active.
- All extension and edge-toggle production artifacts and their independent
  replays are complete at the hashes in manifest ART-042--080.
- The CEGAR runner and its tests/protocol are under construction; no
  production synthesis run directory or checkpoint exists yet.
- The exploratory `C5`, `C7`, and `C9` dry runs ended and retained no
  certificate artifacts.

### Resource usage

- Host: MacBookPro18,1, Apple M1 Pro, 10 cores, 16 GiB RAM.
- Edge-toggle search: 724.27 seconds wall, 709.44 seconds CPU, 75.92 MiB
  peak RSS.
- Independent coverage reconstruction/replay: 16.10/4.96 seconds wall,
  approximately 64.2/73.33 MiB peak RSS.
- Third mathematical certificate generation plus two replays: 46.19 seconds
  wall, 35.44 MiB peak RSS; separate hostile replay took 19.81 seconds.
- Free disk is approximately 8.6 GiB.  No more than two memory-heavy jobs
  remain permitted; current work is source review and low-memory testing.

### Next three highest-value actions

1. Finish and hostile-audit the resumable CEGAR orchestrator, including its
   crash, path, model, cut, proof, and terminal-state semantics.
2. Launch the proof-producing `C9` branch, verify its DRAT proof
   independently, then run bounded resumable `C7` and `C5` branches.
3. Audit the proposed transition-kernel lemma and use it either as a proved
   structural filter or record a precise counterexample/failed route.

## Checkpoint 003 — 2026-07-25 15:35 PDT

- Campaign day: 1 of 27; 26 campaign days remain.
- Repository branch: `main`.
- Latest published campaign commit before this checkpoint:
  `e99bd46e` (full hash recorded in Git).
- Shared-main HEAD observed at checkpoint creation:
  `2360a0ce46bce55988a2beff084e7248a15bbec5`.
- Completion estimate for the campaign work plan: **30%**.
- Completion estimate toward an actual universal resolution: **6%**.
  The conjecture remains unresolved; neither estimate is a mathematical
  probability.
- Literature audit date: 2026-07-25, including a targeted novelty search for
  the parameter-three odd-wheel/odd-antihole restrictions.

### Verified facts and artifacts

- The complete one-vertex-extension production ledger contains all 110,537
  nonempty extensions of the 55 MMV near-miss hosts and 54,216 unique
  canonical graphs. No candidate indicator occurs.
- The independent coverage checker passed on every origin and canonical
  multiplicity. Its report, state database, input hashes, exact-isomorphism
  receipts, and origin-chain hash are recorded in manifest ART-046--048.
- A third, mathematically independent checker passed all 54,216 rows and
  emitted 7.36 MB of replayable per-row certificates. It proves:
  52,447 rows have `gamma<3`; 1,378 have `gamma=3, alpha=4`; and the closest
  391 have `gamma=alpha=3` but empty one-guard three-state greatest fixed
  point. No counterexample survives this delimited extension universe.
- The parameter-three odd-antihole elimination is accepted and promoted as
  claim C-017. Its one low-severity omitted lower-bound sentence was repaired,
  and the final hostile review plus independent C7 probe are manifest-bound.
- CaDiCaL 3.0.1 and DRAT-trim are content-pinned and locally built. A
  solver/checker smoke proof passed.

### Claim and review boundary

- The extension result is fully bound by independent coverage and
  mathematical certificates, and the frozen coverage package passed a full
  hostile replay. It is promoted as exactly delimited claim C-018.
- The initial order-12 CNF, all four template/relabeling arguments, coloring
  cuts, exact coloring oracle, strict generator, and replay manifest are
  hostile-review accepted. The induced `complement(C7)` base template
  produced a verified temporary UNSAT proof consistent with the human
  theorem; that temporary proof is not yet a promoted finite certificate.
- The one-edge-toggle production run is complete: 25,641 origins, 391 seeds,
  and 19,136 canonical connected graphs, with no candidate. Every stored row
  has strict `gamma < gamma-infinity`; independent coverage and mathematical
  audits are running before claim promotion.
- No result at this checkpoint resolves the universal conjecture or raises
  the complete all-graph order frontier beyond the published order 11.

### Approach registry

| Route | Status | Exact gate/obstruction |
|---|---|---|
| Literature/status audit | active-weekly | Current refresh complete; unavailable `C4`-free manuscript and general well-covered generators remain gaps |
| Exact evaluators/certificates | complete-for-current-artifacts | A/B, theta traces, order-9, extension coverage, and third mathematical replay passed |
| MMV one-vertex extensions | complete-certified | Exact search, independent coverage, hostile full-ledger replay, and third mathematical certificates support C-018 |
| Single-edge toggles of closest seeds | complete-audit-pending | 25,641 origins and 19,136 canonical graphs complete; independent coverage and third mathematical replay running |
| Direct synthesis `(12,3)` | active-orchestrator | Exact base encodings and generator accepted; resumable proof-producing CEGAR orchestration is the remaining launch gate |
| Structural `k=3` lane | active | Three-template theorem accepted as C-017; cautious novelty assessment remains search-limited |
| General well-covered generation | blocked | No audited complete constructive generator/catalog for orders 12--16 |

### Running jobs and resume state

- No search process is active; the single-edge-toggle production run
  completed in 724.27 seconds.
- The extension search and both independent replays are complete and
  immutable at the hashes in manifest ART-042--051.
- Active work consists of bounded post-run audits and CEGAR-orchestrator
  construction. No production synthesis checkpoint exists.

### Resource usage

- Host: MacBookPro18,1, Apple M1 Pro, 10 cores, 16 GiB RAM.
- Extension search: 140.45 seconds wall, 36.06 MiB peak RSS.
- Independent coverage replay: 71.94 seconds wall, 40.63 MiB peak RSS.
- Independent mathematical certificate generation plus two replays:
  40.23 seconds wall, 28.59 MiB peak RSS; separate verify-only replay passed.
- Free disk is approximately 9.7 GiB. No more than two heavy jobs remain
  permitted; current jobs are low-memory reviews/tests.

### Next three highest-value actions

1. Finish the independent coverage and mathematical audits of the completed
   25,641-origin single-edge-toggle search.
2. Launch and independently audit the now-accepted 25,641-toggle search while
   closing the still-pending synthesis-generator repairs.
3. Complete the proof-audited CEGAR orchestrator and begin the three
   hub-free odd-hole branches for the full `(n,k)=(12,3)` slice.

## Checkpoint 002 — 2026-07-25 14:56 PDT

- Campaign day: 1 of 27; 26 campaign days remain.
- Repository branch: `main`.
- Latest published campaign commit before this checkpoint:
  `68e1c1fe7b4e339fea6199af165b3ba3a2ec3f81`.
- Shared-main HEAD observed at checkpoint creation:
  `edd7d9c693c8bc7cd3470eb2860f32c8455f6f10`.
- Completion estimate for the campaign work plan: **21%**.
- Completion estimate toward an actual universal resolution: **4%**.
  The conjecture remains unresolved; neither estimate is a mathematical
  probability.
- Literature audit date: 2026-07-25, refreshed for the classical one-guard
  odd-cycle theorem.

### Verified facts and artifacts

- The complete connected-unlabeled order-9 validation gate is finished:
  261,080 graphs across all eight nauty residues.  Evaluators A and B agree
  on every parameter and greatest eternal family at every guard count.
  No graph has `gamma-infinity < theta`.
- The aggregate reproduces the published order-9 table exactly:
  `gamma=alpha` for 4,515 graphs and
  `gamma=gamma-infinity=theta` for 2,265 graphs.  Shard, graph-stream, and
  ordered shard-set hashes are in
  `results/logs/unlabeled-n09-all.json`.
- The exact 110,537-origin one-vertex-extension engine passed 16 focused
  tests and the complete 77-test campaign suite.  Its hostile review accepts
  the exact source hash with no open critical, high, or medium issue.
- The accepted structural lane proves that an induced odd wheel in the
  complement obstructs `gamma-infinity=3` and gives an exhaustive order-12
  SPGT template split.
- A stronger three-branch split is now proved in
  `math/lemmas/k3_antihole_elimination.md`: the classical
  `gamma-infinity(C7)=4` removes the induced `complement(C7)` branch.  It
  remains unpromoted pending its independent hostile audit.

### Literature and restriction status

- No universal proof or certified counterexample was located through
  2026-07-25.
- Goddard--Hedetniemi--Hedetniemi (2005, Theorem 3, attributing Burger et
  al.) verifies the exact one-guard odd-cycle and odd-antihole values; its
  author-hosted PDF and hash are archived.
- The planar, subcubic, and triangle-free restrictions retain their prior
  status.  The unavailable 2018 `C4`-free manuscript remains provisional and
  is not a hard search filter.
- No all-guards, eviction, occupied-attack, or other variant result has been
  imported into the one-guard campaign.

### Approach registry

| Route | Status | Exact gate/obstruction |
|---|---|---|
| Literature/status audit | active-weekly | Current refresh complete; unavailable `C4`-free manuscript and general well-covered generators remain source gaps |
| Exact evaluators/certificates | validation-complete | A/B, coloring trace, MMV catalog, and connected order-9 gates accepted |
| Required reductions | complete | All core reductions hostile-reviewed |
| MMV near-miss extensions | active-launch | Search engine accepted; independent post-run checker is in final integration before production launch |
| Direct synthesis `(12,3)` | pending-next | Opens after the near-miss kill test; three-template reduction awaits hostile audit |
| Structural `k=3` lane | active | Odd-wheel theorem accepted; odd-antihole elimination under review |
| General well-covered generation | blocked | No audited complete constructive generator/catalog for orders 12--16 |

### Running jobs and resume state

- All order-9 workers completed cleanly; there is no residual regression
  process.
- No extension or synthesis process was running at checkpoint creation.
- The independent extension coverage checker is being integrated and tested.
  The production extension database does not yet exist.

### Resource usage

- Host: MacBookPro18,1, Apple M1 Pro, 10 cores, 16 GiB RAM.
- The order-9 gate used at most two CPU cores and about 56 MiB aggregate
  resident memory; the largest per-worker resident set was 28,033,024 bytes.
- Free disk is approximately 9.9 GiB.
- The extension launch remains one process with a 1 GiB advisory memory gate,
  45-minute resumable wall gate, and transactional batches of 256 origins.

### Next three highest-value actions

1. Finish the standalone post-run reconstruction/isomorphism/evaluation
   checker, then launch the full 110,537-origin near-miss extension search.
2. Independently audit the `C7`/odd-antihole elimination and, if accepted,
   replace the four-branch order-12 split by hub-free `C5`, `C7`, and `C9`.
3. Audit the extension result and begin direct `(n,k)=(12,3)` synthesis using
   the proved complement dictionary and template restrictions.

### Claim boundary

No checkpoint-002 result resolves the conjecture.  The connected order-9
enumeration is a validation result below the published order-11 frontier.
The extension search has not yet run, and the stronger three-template
reduction is not yet hostile-reviewed.

## Checkpoint 001 — 2026-07-25 14:28 PDT

- Campaign day: 1 of 27; 26 campaign days remain.
- Repository branch: `main`.
- Published campaign commit:
  `e05d451eb4edb6d67c26aab7286950d50c39bf59`.
- Completion estimate for the campaign work plan: **15%**.
- Completion estimate toward an actual universal resolution: **3%**.
  The conjecture remains unresolved; neither estimate is a mathematical
  probability.
- Literature audit date: 2026-07-25, including a direct current-search refresh
  and the full April 2026 Kimura--Matsumoto--Sato article.

### Verified facts and artifacts

- Required reductions are proved in `math/reductions.md` and accepted in
  `reviews/reductions_hostile_review.md`.
- Exact evaluator A and structurally independent evaluator B are implemented
  and hostile-reviewed. The deliberate model-error probes distinguish
  one-guard movement, unoccupied attacks, domination checks, and \(G\) from
  \(\overline G\).
- The exact 56-record MMV Table 9 catalog is reproduced. Both evaluators agree
  on every parameter and greatest eternal family at every \(k\); all 56
  values \(\theta=4\) have independently replayed non-3-colorability traces
  and direct 4-colorings.
- The 55 graphs with
  \(\alpha=\gamma^\infty=3<\theta=4\) all fail explicitly because
  \(\gamma<\alpha\): two have a universal vertex and 53 have a recorded
  dominating pair.
- New proved tools: the maximum-independent-state/private-region obstruction
  and the complement-side \(k=3\) dictionary, each with an independent hostile
  review and exhaustive small-graph audit.
- Current fully completed exhaustive frontier: all 12,113 connected unlabeled
  graphs through order 8. No \(\gamma^\infty<\theta\) graph occurs there.

### Literature and restriction status

- No universal proof or certified counterexample was located through
  2026-07-25.
- The original assertion is Theorem 14 of
  Klostermeyer--MacGillivray (2009); its proof was explicitly corrected in
  Klostermeyer--Mynhardt (2015), which posed the open question.
- Subcubic and triangle-free restrictions are primary-source verified.
  Taletskii's all-planar theorem statement is verified but its long proof
  remains queued for hostile audit.
- The \(C_4\)-free result still traces only to an unavailable 2018 manuscript.
  The purported 4-cycle restriction is provisional and is not a hard filter.
- The July 2026 Cayley work concerns
  \(\gamma_{\rm all}^\infty\), not the one-guard parameter, and is excluded.

### Approach registry

| Route | Status | Exact gate/obstruction |
|---|---|---|
| Literature/status audit | active-weekly | Phase 0 checkpoint complete; 2020 chapter, unavailable \(C_4\)-free manuscript, and general well-covered generators remain source gaps |
| Exact evaluators/certificates | active-validation | A/B and coloring-trace hostile audits accepted; connected order-9 partition is running |
| Required reductions | complete | All requested core reductions accepted; class-citation qualifications remain separate |
| MMV near-miss extensions | active-prelaunch | Exact 110,537-case scope accepted; engine is under hostile crash/candidate-state repair; full run not launched |
| Direct synthesis `(12,3)` | pending | Opens only after order-9 validation and near-miss kill test |
| Structural \(k=3\) lane | active | Two proved mechanisms obtained; next structural lemma is under independent development |
| General well-covered generation | blocked | No audited complete constructive generator/catalog for orders 12--16 yet |

### Running jobs and resume state

- Order-9 shard `1/8` is complete (35,236 graphs).
- Shards `0/8` and `6/8` are running with atomic checkpoints in
  `results/checkpoints/`; each uses one CPU core and roughly 27 MiB resident
  memory. No more than two workers run concurrently.
- Remaining order-9 shards are queued by descending estimated cost. Resume
  uses the same `search.unlabeled_regression` command and existing checkpoint.
- No extension, synthesis, SAT, or other novel exhaustive job is running.

### Resource usage

- Host remains MacBookPro18,1, Apple M1 Pro, 10 cores, 16 GiB RAM.
- Current campaign workers use about 54 MiB aggregate resident memory and two
  CPU cores. Free disk is approximately 10 GiB.
- The one-vertex-extension engine has a 1 GiB memory gate and 45-minute
  resumable wall gate; it remains closed pending hostile acceptance.

### Next three highest-value actions

1. Finish and aggregate all eight order-9 validation shards; compare the
   261,080 total and parameter counts to the published table.
2. Close every hostile extension-engine finding, run the independent review,
   and only then launch the 110,537-case one-vertex-extension kill test.
3. Build the standalone post-run coverage/isomorphism checker while continuing
   the structural \(k=3\) proof lane.

### Claim boundary

No checkpoint-001 result resolves the conjecture. The order-at-most-11
statement remains the published MMV frontier rather than a newly certified
campaign enumeration, and the extension universe has not yet been searched.

## Checkpoint 000 — 2026-07-25 13:02 PDT

- Campaign day: 1 of 27.
- Repository branch: `main`.
- Repository commit at campaign start:
  `87e9672b4fabecc9fd59bd42c0da8d27d97d1c6f`.
- Completion estimate toward the full conjecture-resolution goal: **1%**.
  This is a deliberately low prior and may move non-monotonically.
- Literature audit date: initiated 2026-07-25; no campaign claims accepted yet.
- Verified facts: none newly produced by this campaign.
- Current exhaustive frontier: none.
- Certificate status: no campaign certificates yet.

### Machine and resource envelope

- Model: MacBookPro18,1 (Apple M1 Pro).
- CPU: 10 physical/logical cores.
- Physical memory: 17,179,869,184 bytes (16 GiB).
- Free filesystem space at start: approximately 11 GiB.
- Policy: at most two memory-heavy jobs; aggregate target below 12 GiB; keep
  interactive load responsive; no blind order-12 graph enumeration.

### Repository isolation

The `main` worktree contained unrelated dirty research before this campaign
started. All campaign artifacts are isolated in
`gamma_theta_eternal_domination/`. Checkpoints stage only this directory.
Existing unrelated modifications are not to be edited, staged, or committed.

### Approach registry

| Route | Status | Current gate |
|---|---|---|
| Literature/status audit | active | Verify original attribution, 2022 catalog, later citations, and current resolution status |
| Exact evaluator A | active | Implement directly from the greatest-fixed-point definition |
| Exact evaluator B | active | Implement independent colored configuration digraph |
| Required reductions | active | Produce self-contained proofs, then hostile review |
| Near-miss extensions | pending | Requires evaluator validation and exact appendix data |
| Direct synthesis `(12,3)` | pending | Requires 72-hour validation gate |
| Structural `k=3` proof lane | pending | Begin after reductions and literature restrictions are fixed |

### Running jobs

None at checkpoint creation.

### Resume

1. Read `STATE.md`, `CLAIMS.md`, and the latest entries of
   `RESEARCH_LOG.md`.
2. Inspect `git status --short -- gamma_theta_eternal_domination`.
3. Run the test command recorded in the most recent checkpoint.

### Next three highest-value actions

1. Complete the primary-source literature audit and obtain the 2022 appendix
   Graph6 data.
2. Finish two independent exact evaluator stacks and unit tests.
3. Prove and adversarially audit the parameter chain, equality collapse,
   component reduction, imperfection obstruction, and minimum-parameter facts.

### Known constraints and risks

- Only about 11 GiB of disk was free at launch.
- `main` is a shared dirty worktree, so commits must be path-scoped.
- The repository policy forbids preparing or initiating outside outreach,
  despite the campaign brief's later publication wish list.
