# Campaign State

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
