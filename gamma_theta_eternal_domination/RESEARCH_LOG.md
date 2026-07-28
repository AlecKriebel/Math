# Research Log

Timestamps use America/Los_Angeles unless explicitly marked otherwise.

## 2026-07-25

### 13:02 — Campaign initialization

- Began day 1 of the 27-day program.
- Detected MacBookPro18,1, 10 CPU cores, 16 GiB physical memory, and
  approximately 11 GiB free disk.
- Found the requested repository worktree on an unrelated feature branch and
  found `main` checked out in a separate, dirty worktree.
- Chose the least-collision path consistent with repository policy: isolate
  all work in a new directory in the existing `main` worktree and never stage
  unrelated paths.
- Established independent evaluator, proof, literature, certificate, and
  result directories.
- Recorded the policy conflict concerning outreach: repository instructions
  control, so no message or draft outreach will be produced.

### 13:18 — Independent evaluator differential gate

- Completed two exact implementations of the one-guard game: verifier A uses
  bit masks and greatest-fixed-point deletion, while verifier B uses
  `frozenset` configurations and an explicit colored configuration digraph.
- The two implementations agreed on all parameters and greatest eternal
  families at every tested guard count for 1,100 labeled graphs through order
  5 and 1,000 seeded random graphs of orders 6--10.
- Hostile review subsequently tested connected order-8 graphs, random graphs
  through order 12, malformed Graph6 inputs, and malformed eternal-family
  certificates. All reported parser/checker defects were fixed and re-audited.

### 13:31 — Exact MMV 2022 catalog reproduced

- Extracted all 56 Graph6 records from the arXiv TeX of MMV Table 9: two
  order-10 and 54 order-11 graphs.
- Both evaluator stacks reproduced the full parameter table. Exactly 55 have
  \(\alpha=\gamma^\infty=3<\theta=4\), but all 55 fail
  \(\gamma=\alpha\): two have \(\gamma=1\), and 53 have \(\gamma=2\) with
  explicit dominating witnesses.
- Saved an exhaustive complement non-3-colorability trace and a direct
  4-coloring for each graph. A separate checker and hostile review replayed
  every trace.

### 13:47 — Small-graph exhaustive regression through order 8

- Exhaustively checked all 12,113 connected unlabeled graphs of orders 1--8.
  Evaluators A and B agreed on all five parameters and every tested greatest
  eternal family. No graph in this regression has
  \(\gamma^\infty<\theta\).
- Peak resident memory for the order-8 run was about 27 MiB; wall time was
  70.45 seconds. This supports two low-memory order-9 shards without
  threatening the 16 GiB resource envelope.

### 14:00 — First structural proof checkpoint

- Completed and hostile-reviewed the required parameter, equality-collapse,
  component-additivity, imperfection, induced-subgraph, and \(k\geq3\)
  reductions.
- Proved the maximum-independent-state lemma and its private-region
  obstruction: in an eternal \(k\)-family, every independent \(k\)-set is a
  state, and a failed required swap certifies
  \(\gamma^\infty\geq\alpha+1\).
- Proved a complement-side dictionary for the \(k=3\) synthesis lane,
  translating domination, well-coveredness, legal moves, and eternal closure
  into clique/nonedge statements in the complement. Both new lemmas survived
  independent mathematical and exhaustive small-graph audits.

### 14:15 — Phase 0 literature audit checkpoint

- Traced the conjecture to the flawed Theorem 14 of
  Klostermeyer--MacGillivray (2009), the explicit correction and Question 7.1
  of Klostermeyer--Mynhardt (2015), and later naming/formulation.
- Reconciled the dissertation's apparent 54/53 count with MMV's 56/55:
  54/53 are exactly the order-11-only counts, while both sources' appendices
  include the two order-10 graphs.
- No universal resolution was located through 2026-07-25. The April 2026
  Kimura--Matsumoto--Sato paper was obtained and checked; it gives
  maximum-demand results for narrower planar/critical classes, not a
  universal result.
- The advertised \(C_4\)-free restriction currently traces to an unavailable
  2018 manuscript. It remains provisional and is not a certified hard filter.
- The July 2026 Cayley paper uses the all-guards-move parameter
  \(\gamma_{\rm all}^\infty\) and was excluded from the one-guard ledger.

### 14:20 — Near-miss engine and order-9 gate

- Proved that all connected one-vertex extensions of the 55 near misses form
  a raw universe of 110,537 neighborhood masks, of which 106,443 extensions
  of domination-two hosts reach the decisive filter.
- Implemented a resumable SQLite search engine with global canonical
  deduplication, origin provenance, exact \(\gamma/\alpha\) filters, both
  eternal solvers at \(k=3\), and atomic freezing of a first candidate. The
  full extension run has not yet been launched.
- Began the final evaluator-validation item: eight resumable residue shards
  covering all 261,080 connected unlabeled order-9 graphs, with two workers
  and roughly 27 MiB resident memory per worker.

### 14:39 — Extension engine hostile gate accepted

- Closed every critical, high, and medium issue found in the independent
  hostile review of the one-vertex-extension engine.
- Bound the exact `labelg` executable, nauty source archive, engine, private
  obstruction module, both evaluator stacks, and Python runtime identity into
  the immutable resume configuration.
- Verified fail-closed candidate handling, transactional initialization and
  final-host commits, exact-mask replay after injected failure, path-role
  separation, and finite resource controls.
- The focused extension suite passed 16 of 16 tests and the full campaign
  suite passed 77 of 77.  The engine was accepted for a validation-gated run,
  but no finite claim is permitted until a separately written checker
  reconstructs and audits the completed ledger.

### 14:54 — Connected order-9 validation gate complete

- Completed all eight nauty residue partitions, covering exactly 261,080
  connected unlabeled order-9 graphs.
- Both exact implementations agreed on all five parameters and on the
  greatest eternal family at every guard count for every graph.  No graph
  has `gamma-infinity < theta`.
- The aggregate reproduced the published counts exactly: 4,515 graphs have
  `gamma=alpha`, and 2,265 have
  `gamma=gamma-infinity=theta`.
- The eight graph-stream hashes, shard file hashes, residue coverage, and
  ordered shard-set hash are bound in
  `results/logs/unlabeled-n09-all.json`.  Peak resident memory was about
  28 MiB per worker.

### 14:55 — Stronger parameter-three template reduction

- Proved that the classical value `gamma-infinity(C7)=4`, combined with
  induced-subgraph monotonicity, eliminates an induced
  `complement(C7)` from the complement of a parameter-three counterexample.
- Consequently the Strong Perfect Graph Theorem should reduce an order-12
  parameter-three synthesis to hub-free induced `C5`, `C7`, or `C9` branches,
  rather than the previously accepted four-branch split.  This strengthening
  is awaiting a separate hostile audit before claim promotion.
- Located and archived Goddard--Hedetniemi--Hedetniemi (2005), which records
  the general odd-cycle value and attributes it to Burger et al.  The cycle
  value is therefore classical; only the complement-side synthesis
  combination is treated as a campaign contribution.

### 15:10 — Complete one-vertex-extension kill test

- Exhausted all 110,537 nonempty one-vertex extensions of the 55 published
  near-miss hosts. Global canonicalization reduced these to 54,216 graphs.
  The search found no graph with the required equality.
- Exactly 391 canonical graphs reached the closest static target
  `gamma=alpha=3`; both original one-guard implementations rejected every
  one at three guards. The remaining graphs split into 52,447 with
  `gamma<3` and 1,378 with `alpha=4`.
- A separately written coverage checker reconstructed every host and
  neighborhood mask, independently proved each raw-to-canonical isomorphism,
  and reconciled all 110,537 origins and 54,216 multiplicities. Its passed
  report cryptographically binds the production database and exports.

### 15:20 — Independent per-row mathematical certificates

- A third implementation, importing neither search code nor evaluator A/B,
  generated and replayed a certificate for every canonical extension row.
- It supplied explicit domination witnesses for all 52,447 `gamma<3` rows,
  exhaustive pair/five-set streams plus witnesses for all 1,378
  `gamma=3, alpha=4` rows, and full greatest-fixed-point deletion traces for
  all 391 `gamma=alpha=3` rows.
- Those 391 traces delete all 46,898 dominating triples in two through seven
  simultaneous rounds, using only unoccupied attacks and exactly one
  edge-moving guard. No candidate survives this delimited universe.
- This is a certificate-backed finite result about extensions of the
  published hosts, not an enumeration of all order-12 graphs and not a
  resolution of the universal conjecture.

### 15:25 — Proof-producing synthesis toolchain and first consistency check

- Pinned and locally built CaDiCaL 3.0.1 and the independently developed
  DRAT-trim checker from content-hashed source archives. A bundled
  pigeonhole-instance proof passed an end-to-end `s VERIFIED` smoke test.
- Implemented the initial order-12, parameter-three complement CNF for the
  four certified SPGT templates. The three odd-hole base instances are
  satisfiable before coloring cuts; the induced `complement(C7)` base
  instance is already UNSAT, with a DRAT-trim-verified temporary proof.
- The latter result is presently a consistency check only. The CNF generator
  and template encoding remain under hostile review, and no synthesis
  negative result has been promoted.

### 15:34 — Hostile pre-launch checks remain effective

- The edge-toggle engine covers the bounded next universe of 391 seeds and
  25,641 single-edge toggles, but its first hostile review found a real
  nondefault output-path collision capable of replacing an SQLite file with
  JSON. Production launch was correctly blocked.
- The engine author repaired the derived checkpoint-path validation and
  added exact overwrite, nesting, and symlink regressions. A separate
  re-review accepted the repaired engine: all 25,641 toggle semantics retained
  their independent digest, the former SQLite-overwrite assignment and nine
  adjacent aliases now fail before output creation, and no high or medium
  finding remains. No edge-toggle production run has started.
- The synthesis generator audit independently found unsafe output/input path
  aliases. The generator was repaired to reject direct, symlink and hard-link
  collisions before writes; ingest strict JSON once; bind sources, runtime,
  working directory and required environment; and rehash installed bytes.
  The final hostile replay executed the exact recorded command under an empty
  environment and reproduced the artifacts byte-for-byte. The base encoding
  and generator are accepted; the resumable CEGAR orchestrator remains to be
  built and reviewed.

### 16:00 — Complete single-edge-toggle production ledger

- Exhausted every unordered-pair edge toggle of the 391 closest canonical
  extension seeds: 25,641 raw seed/pair origins and 19,136 global canonical
  graphs. Every graph is connected and no candidate was frozen.
- The search implementations classify every row by strict
  `gamma < gamma-infinity`. The unique/raw parameter distribution is:
  8,587/12,225 with `(gamma,alpha,gamma-infinity,theta)=(3,3,4,4)`;
  6,751/8,615 with `(2,3,4,4)`; 2,615/3,488 with `(3,4,4,4)`;
  1,143/1,246 with `(2,3,3,3)`; and 40/67 with `(2,3,3,4)`.
- Runtime was 724.27 seconds wall and 709.44 seconds CPU; peak resident
  memory was 75.92 MiB. The database, checkpoint, provenance and unique
  exports are hash-bound in manifest ART-066--069.
- This remains an unpromoted finite search result until a standalone checker
  independently reconstructs all toggles and a third mathematical
  implementation certifies `gamma < gamma-infinity` on every canonical row.

### 16:23 — Single-edge-toggle universe independently certified

- A standalone coverage checker independently reselected the 391 seeds,
  reconstructed all 25,641 add/delete origins, directly verified a saved
  raw-to-canonical isomorphism for every origin, and reconciled all 19,136
  canonical multiplicities and first-origin records.  A separate hostile
  implementation replayed the entire ledger and accepted the exact coverage
  claim with no critical, high, or medium finding.
- A third mathematical checker, sharing no domination or transition core
  with the search or evaluators A/B, proved `gamma < gamma-infinity` for
  every canonical row.  It found 7,934 rows with `gamma=2` and 11,202 with
  `gamma=3`; complete simultaneous fixed-point traces delete all 1,235,981
  dominating configurations at `k=gamma` in 37,552 rounds.  An independent
  frozenset implementation replayed every blocker and deletion round.
- The exact finite statement is promoted as claim C-019.  It concerns only
  single-edge toggles of the 391 specified seeds; it neither covers all
  order-12 graphs nor resolves the universal conjecture.
- During hostile testing, one default-path completed-state replay rewrote
  only the coverage report's runtime/timestamp fields.  The receipt database,
  origin chain, binding, and conclusions remained byte-identical.  The
  resulting report was frozen at SHA-256 `82c6918f...`, the mathematical
  checker binds those exact bytes, and the incident is recorded in the
  hostile review.
- As workload evidence only, a throwaway CEGAR dry run of the accepted
  order-12 `C9` template reached solver `UNSAT` after 170 valid coloring
  cuts in 22.7 seconds.  The `C7` and `C5` probes reached 594 and 543 cuts,
  respectively, at their separate 90-second gates without a terminal.
  These probes retained no proof logs and support no mathematical claim;
  production awaits the audited resumable orchestrator.

### 16:52 — Online two-step obstruction proved and measured

- Proved that the descending online transition kernels stabilize at the
  greatest eternal family.  When `alpha=gamma-infinity=k`, every maximum
  independent `k`-set must survive two adaptive attacks.  A failed first
  attack, together with a named second attack defeating every legal first
  response, is a compact private-region certificate that
  `gamma-infinity>=k+1`.
- The theorem is strictly stronger than the prior one-step condition:
  `C7` passes security at every maximum independent triple but a specified
  first attack has no secure successor.  An independent hostile review
  accepted the proof, complement translation, certificate checker, and
  model semantics with no critical, high, or medium finding.
- On the 8,587 closest edge-toggle rows with
  `(gamma,alpha,gamma-infinity,theta)=(3,3,4,4)`, one step rejects 4,169,
  the second step rejects 3,892 more, and only 526 survive.  The same filter
  rejects all 5, 78, and 1,569 static `gamma=alpha=3<theta` targets at
  connected-unlabeled orders 7, 8, and 9.  A standalone implementation
  reproduced every count; they remain observations, not an order-bounded
  nonexistence certificate.
- A terminology refresh located and archived Burger et al.'s 2004 finite-
  and infinite-order papers.  Their finite smart-\(q\) definition is
  offline: the full attack sequence is known before the defender sequence
  is chosen.  The campaign kernel is adaptive online, with alternating
  attack/response quantifiers.  The note now cites this predecessor,
  states the distinction explicitly, and makes no categorical general
  novelty claim.
- The proof-producing `(12,3)` CEGAR runner passed 15 focused tests and the
  full 195-test campaign suite.  Its independent hostile pre-launch audit is
  still active; no production synthesis run has been launched.

### 17:35 — Recursive horizon certificates and the third-ply kill test

- Proved the exact recursive duality between finite online-kernel membership
  and survival/failure trees.  A finite failure tree rooted at one forced
  maximum independent \(k\)-set is a direct certificate that no eternal
  \(k\)-family exists.
- The hierarchy does not collapse at two plies.  On \(C_{15}\), all 15
  maximum independent 7-sets survive two attacks but fail by the third.
  The frozen witness contains a 73-node positive tree and an eight-node,
  four-leaf negative tree with a short human-readable attack strategy.
- Of the 526 hardest edge-toggle rows surviving the two-ply test, 518 fail
  at a forced triple in \(\mathcal K_3\).  Seven of the remaining eight first
  fail in \(\mathcal K_5\), and the deepest first fails in
  \(\mathcal K_6\); every complete three-guard kernel is empty by
  \(\mathcal K_7\).
- Stored 518 recursive failure trees totaling 5,540 nodes and 3,174
  non-domination leaves.  A fresh frozenset implementation imported no
  campaign module, replayed every tree, recomputed all 8,587 source
  profiles, checked all 64,893 selected deletion ranks, and rejected 14
  decisive mutations.  The independent hostile verdict is accepted with no
  critical, high, or medium issue.
- The repaired CEGAR runner reached 21 focused and 208 full-suite tests, but
  production remains blocked.  Re-audit found that historical auxiliary
  model checks still replayed every prior cut, leaving quadratic resume
  work.  That is an operational/provenance defect rather than a flaw in the
  globally sound coloring cuts, and a second repair round is active before
  launch.

### 17:43 — Radius-two robustness of the deepest local near-miss

- Exhausted the exact edge-toggle ball of radius at most two around
  `Kun_w{vRrblV`: \(1+66+\binom{66}{2}=2,212\) labeled origins and 1,076
  pinned-`labelg` canonical classes, with all multiplicities retained.
- Evaluators A and B agree on \(\gamma,i,\alpha,\gamma^\infty,\theta\), the
  eternal decisions, and normalized winning families for every class.
  There is no candidate.  All 411 classes with \(\gamma=3\) still have
  \(\gamma^\infty=4\); 354 have \(\alpha=3\), and 57 have \(\alpha=4\).
- A root-run deep audit repeated live canonicalization and complete
  two-stack evaluation and matched the frozen 1.9 MB result.  The 35.98
  second run used about 36.2 MB peak RSS.
- The claim remains `OBSERVED`: the same implementation generates and
  audits coverage, and no proof-producing coloring traces were retained.
  The search stopped at the preset radius-two yield gate.

### 18:07 — Proof-producing CEGAR launch gate accepted

- Froze the repaired order-12, parameter-three CEGAR runner at SHA-256
  `411fffff34c0122d679ee710aff0e3856a7ff166bff30c69edb1f0044defce8c`,
  with protocol SHA-256
  `c51db6d865557f4dcc3147772dbaa1c86d3c6c6d3544ab0090f0f89267a9de31`
  and complete runtime-source-set SHA-256
  `8c4e811bc4250c3e2b0b7edeb8afd07f7509ebda3cbae3db1b3ca82c07b35299`.
- The final independent hostile audit returned `ACCEPT for bounded
  production`.  It rejected the original SAT-to-fabricated-UNSAT exploit,
  six rebound cross-field mutations, and a later-checkpoint chronology
  forgery; it also checked read-only audit behavior, global and per-run
  locking, synchronous signal cleanup, exact linear history counters, and a
  live pinned DRAT replay.
- A separate mathematical reviewer accepted the complement direction,
  static constraints, online one-guard closure, and global validity of every
  coloring cut.  The candidate path remains quarantined and is not treated
  as a clique-cover certificate.
- The focused suite passed 23 of 23 tests.  The independent root run of the
  complete campaign suite passed 218 of 218 tests in 27.156 seconds.
- One low operational caveat remains documented: the session-wall setting
  is a conservative admission budget over Python-side overhead rather than
  a preemptive deadline.  Every solver/checker child remains hard-bounded,
  and the campaign's external sprint supervision remains mandatory.
- No production synthesis run had been launched at this freeze.  Any
  terminal `UNSAT` must still undergo a read-only
  `--deep-reconstruct --verify-terminal-proof` audit, and all three accepted
  hole templates are required for a finite `(n,k)=(12,3)` conclusion.

### 18:12 — First production `hole9` cut committed and deeply audited

- Launched exactly one iteration from pushed commit `149378de` under seed
  zero, 60-second and 2,048 MiB child limits, a 4,096 MiB disk reserve, a
  256 MiB child-file cap, and a 1 MiB retained-attempt cap.
- CaDiCaL returned a complete SAT assignment in 0.028558 seconds using about
  4.86 MiB peak RSS.  The runner directly checked every CNF clause, decoded
  graph/family condition, proper complement three-coloring, and falsity of
  the resulting 19-literal same-color cut.  The cut was atomically
  committed.
- The checkpoint now has one attempt, one cut, status `running`, and no
  terminal.  Its SHA-256 is
  `075bdb8e168d1b6edeca6470a56fdc00be4624adaa7f80433b053306b49eb90e`.
- A separate `--audit-only --deep-reconstruct` run returned
  `running_audit_passed`.  The complete ten-file run tree had SHA-256
  `691838bced032e72ab037d13f547c2dbfe9eb4351c8c486814c166a8feb7c847`
  both before and after audit.  The retained tree is 39,706 file bytes.
- This is a production-integrity milestone only.  One coloring cut proves
  no template-level or graph-level nonexistence statement.

### 18:15 — `hole9` bounded batch 001 reaches 33 cuts

- Resumed the pushed one-cut checkpoint for 32 iterations.  All 32 children
  returned complete SAT assignments, supplied directly validated proper
  three-colorings, and atomically committed distinct globally sound cuts.
- The batch took 16.9724 seconds end to end.  Solver children used 0.8871
  seconds total wall time; the largest child peak RSS was 5,324,800 bytes.
  There were no timeouts, unknown outcomes, memory events, or terminal.
- The new checkpoint has 33 attempts and 33 cuts, with SHA-256
  `0bf9fabdaf6d69974b698e66fdb731a19a04ed64f4d0bdbda878ce6dc2cb624c`.
  Its complete 234-file tree contains 1,146,858 bytes.
- A separate deep read-only audit passed.  The complete tree SHA-256 was
  `32418469c3c2e6ea5e5b1895e6dbf268092ceb4d2231a1774212957c3326ee73`
  both before and after the audit.
- Preserved the old one-cut checkpoint as an immutable snapshot because the
  live transactional checkpoint advances on every resume.  Batch 001 still
  proves no nonexistence statement; it records 32 additional sound cuts.

### 18:18 — `hole9` bounded batch 002 reaches 65 cuts

- Added and directly validated 32 further SAT/coloring cuts.  The run now
  contains 65 attempts and 65 cuts with no timeout, unknown outcome, memory
  event, candidate, or UNSAT terminal.
- Batch wall time was 17.5134 seconds.  The largest solver child took 0.055
  seconds and used 5,423,104 bytes peak RSS.
- Deep read-only reconstruction passed.  The 458-file, 2,257,731-byte tree
  retained SHA-256
  `3e763ccd9d833f8c4b6deb492ec2bc2ccdf87c777e3cfe86ccc8096d17b48bc5`;
  checkpoint SHA-256 is
  `2f092df32138fa14bc2c97cf2ec819a38064d050325eff018cd1b5ef657dcd87`.
- This remains a running proof-search prefix, not a nonexistence result.

### 18:21 — `hole9` bounded batch 003 reaches 129 cuts

- Added 64 further complete, directly validated SAT/coloring attempts.  The
  run now contains 129 distinct sound cuts and no terminal or resource
  event.
- The batch took about 30.00 seconds end to end.  Solver children used 2.66
  seconds total wall time; the maximum child peak RSS was 6,225,920 bytes.
- Deep read-only reconstruction passed and preserved the 906-file,
  4,475,400-byte tree at SHA-256
  `f844ead52f7e719b9ec23b74165ee5a3f31ce4b55cc6b1a433533df4be79c85e`.
  Checkpoint SHA-256 is
  `9f0b91e483f255f2e18b7383811cf4e2937b76d0590be4e9dc5cfcb36dcc51f1`.
- The healthy scaling justifies one more 64-iteration batch after
  publication.  A running prefix still proves no nonexistence statement.

### 18:27 — `hole9` reaches a candidate UNSAT formula; checker fails closed

- The next session committed 41 more colorable attempts, reaching an audited
  checkpoint of 170 cuts.  The following solver call returned `UNSAT` twice
  and wrote a 512,071-byte ASCII DRAT proof, but the configured
  `DRAT-trim -I -f -W` call exited 80.  The runner raised an exception,
  wrote no attempt manifest or terminal marker, and did not advance the
  checkpoint.  No UNSAT claim is accepted.
- The exact cause is compatibility, not a timeout or memory event.
  Verbose bounded replay shows the hard warning at pinned
  `drat-trim.c:809--811`: forward mode ignores a pseudo-unit deletion
  instruction, and `-W` exits immediately on that otherwise optional
  deletion warning.
- Bounded read-only diagnostics show that the unchanged CNF/proof verifies
  with exit zero and exactly one `s VERIFIED` when either the hard-warning
  policy is removed or `-p` is added to ignore all deletion information.
  The latter retains `-W` and emitted no warning, but it is outside the
  frozen protocol and therefore remains only a recovery candidate pending
  independent soundness and implementation review.
- The clean committed checkpoint has SHA-256
  `9cc9cdee08fb1fcd7a8772b09cdf9ba9ced802cb0b31be35ab292244e5f286b7`.
  A deep read-only audit passed and preserved the 1,205-file,
  6,946,580-byte tree at SHA-256
  `bd13c4fdc3629ee02fa510eda09bd503234daf4318a33c562e0ab3427d89fd8b`.
- Froze the unreferenced candidate proof, both UNSAT result files, CNF,
  cuts, generator manifest, and failed checker logs.  A separately written
  recovery verifier and an independent plain-mode audit are now active.

### 18:50 — Two portable failure cores accepted

- Proved the certificate-level lifting rule: a ranked attack DAG rooted at
  any independent \(k\)-set remains valid in every induced supergraph.  This
  is a portable finite witness formulation of the already accepted
  independent-set forcing and induced-subgraph monotonicity results.
- The 11-vertex graph `J@l|bfNuVK_` has three-guard kernel profile
  `110,105,100,88,64,10,0`; the 12-vertex graph `Kun_w{vRrblV` has profile
  `147,143,136,128,119,93,28,0`.  Direct ranked attack DAGs and nonempty
  stable four-guard kernels certify
  \((\gamma,\alpha,\gamma^\infty)=(3,3,4)\) for both.
- Six explicit order-12 embeddings show that the other six rows in the
  previously measured eight-row deep tail contain induced `J`.  A separate
  raw-Graph6/frozenset replay found induced `J` in exactly 37 of the fixed
  526 C-023 graphs: 30 fail at rank three and seven at rank five.  The
  second core is the sole remaining row beyond rank three.
- The complete 2,047-neighborhood one-vertex extension sweep over `J`
  reports 623 pinned-`labelg` keys and no rank beyond five.  This broader
  classification remains `OBSERVED`, because the independent audit checks
  every raw-to-key isomorphism but does not itself prove distinct-key
  nonisomorphism.
- Root replayed the installed deterministic audit and all eight focused
  tests.  The separate hostile review found and closed two low-level parser
  gaps before freezing the package, and accepted it with no unresolved
  critical, high, or medium defect.
- In parallel, the independently written `hole9` recovery verifier produced
  a deletion-free 4,705-addition RUP package and passed its author audit.
  It remains pending a new hostile review and supports no claim yet.

### 18:54 — `hole7` production reaches 64 cuts

- Launched the second required order-12 parameter-three template from pushed
  commit `2c6ce8da`, using the frozen seed-zero configuration, 60-second and
  2,048 MiB child bounds, 4 GiB disk reserve, 256 MiB child-file cap, and
  1 MiB retained-attempt limit.
- All 64 iterations returned complete SAT assignments, directly validated
  candidate semantics and proper complement three-colorings, and atomically
  committed 64 distinct globally sound coloring cuts.  There was no timeout,
  unknown outcome, memory event, candidate, or UNSAT terminal.
- Solver children used 2.9442 seconds total wall time; the slowest took
  0.0693 seconds and the largest peak RSS was 6,733,824 bytes.  The complete
  batch spanned about 33.76 seconds.
- The checkpoint has SHA-256
  `5677bd2323dca1f78c330555d0e2ed443d5993f63c546ad0d22479de5c886a2f`
  and history head
  `72021c3740968419ba495565f59cb8e2ce1d0a64925379ad1c9e4076136aeada`.
- A separate deep read-only audit passed.  The 451-file, 2,233,086-byte run
  tree retained SHA-256
  `6ce2af652b3bcd91184ec2d3cef73822b9de226bff0979ed7e444ba810c149ee`
  before and after replay.  The branch remains open; this prefix proves no
  nonexistence result.

### 18:58 — `hole7` production reaches 128 cuts

- Resumed the published 64-cut checkpoint for 64 more iterations.  Every
  child again returned a complete SAT assignment and a directly checked
  proper complement three-coloring, yielding 64 new distinct sound cuts.
- The new solver children used 3.2106 seconds total wall time and
  2.0567 seconds total CPU.  The slowest child took 0.0707 seconds and peak
  RSS stayed below 6.9 MB.  There was no timeout, unknown result, memory
  event, candidate, or UNSAT terminal.
- The 128-cut checkpoint has SHA-256
  `37eb33e4d35084d8a7e930b88be94d71e3b602f8f4ed10c2e7b2e5fbecf5afe2`
  and history head
  `237a3e6d8d8dd7f38c4ba6a7c73f1969352866d02ec4713338c65c5b6a430154`.
- Deep read-only reconstruction passed and left the 899-file,
  4,456,636-byte tree unchanged at SHA-256
  `b8f038f5bdebde5d457b785bc38339c11e3e2f658d8a3f262a9b7dd30a6a8231`.
  The template remains open.

### 19:02 — `hole7` production reaches 192 cuts

- Added and directly validated 64 further SAT/coloring cuts.  The run now
  contains 192 attempts and 192 distinct globally valid cuts with no
  terminal or resource event.
- New solver children used 3.1560 seconds total wall time and 1.9795 seconds
  total CPU; maximum child wall time was 0.0711 seconds and maximum RSS was
  6,946,816 bytes.
- The checkpoint SHA-256 is
  `70ed71127081efae5e9e85f3bd9c6a2ddefcccf3db992d416d795f3edd1f6d84`,
  with history head
  `d3e4b1083b8903e90bd01b2e29a720888694c3eec906b5285c31a58e4c0e30f6`.
- Deep audit passed and preserved the 1,347-file, 6,685,492-byte tree at
  SHA-256
  `8ccae877b89b167a859bdd7f6dcd42937110fe7a0b725c0425fe2e24c15dd800`.
  The branch is still open.

### 19:05 — `hole7` production reaches 256 cuts

- Added 64 further complete SAT/coloring attempts, bringing the branch to
  256 distinct globally sound cuts with no terminal, timeout, unknown
  result, or memory event.
- The new children used 3.4802 seconds total wall time and 2.2882 seconds
  total CPU.  Maximum child wall time was 0.0639 seconds and maximum RSS was
  6,995,968 bytes.
- The checkpoint SHA-256 is
  `d3dd1138286340b7ec9667596b98998d17ea9937b332e8dfa1b1dcb81e4f4ca6`,
  with history head
  `fcb5b2b2a7c35abbfe103c734e905989a6ca03ab66c753742e646ad0eb2506ad`.
- Deep reconstruction passed and preserved the exact 1,795-file,
  8,907,069-byte tree at SHA-256
  `e699cfa165062acf890be869beaf97dadf3a1b90ff1bb58cab2bd57df00ca1e3`.
  The branch remains open and another bounded batch is warranted.

### 19:09 — `hole7` production reaches 384 cuts

- A larger 128-iteration resume added 128 complete, directly validated
  SAT/coloring attempts.  There is still no terminal or resource event.
- The 128 solver children used 6.5493 seconds total wall time and
  4.8789 seconds total CPU.  The maximum child wall time was 0.0943 seconds
  and maximum RSS was 7,864,320 bytes.
- The checkpoint SHA-256 is
  `81f62e83cf6a910c6b9baabe0edff7ab26543e787cad91a7e261323ae52e18c6`,
  with history head
  `92eeecdbd46e9fcb151f398a073f1275929df589a06a60a07fc882c88f8cdc6a`.
- Deep read-only reconstruction passed and preserved the 2,691-file,
  13,353,372-byte tree at SHA-256
  `43ca4d29ea369900480d5cf90ab52e53b77b5600d03d4d0d5eba37402f1a7b3c`.
  The branch is taking more coloring cuts than `hole9`, but per-child cost
  remains tiny and no scaling gate has fired.

### 19:12 — `hole5` production reaches 64 cuts

- Opened the third and final structural template from pushed commit
  `eea8aece` under the same frozen seed-zero resource configuration.
- All 64 iterations returned complete SAT assignments and directly
  validated complement three-colorings, committing 64 distinct globally
  sound cuts.  There was no terminal, timeout, unknown result, or memory
  event.
- Solver children used 4.1468 seconds total wall time and 3.1141 seconds
  total CPU.  Maximum child wall time was 0.0940 seconds and maximum RSS was
  8,159,232 bytes.
- The checkpoint SHA-256 is
  `02bbf56a292c734fcd886af55b9482439e29a263c8acc1e904883242da5e12dc`,
  with history head
  `ad645794d30eff7a425bb1b898a07c1321dce3012ae38a5392dfa65b408d6a76`.
- Deep read-only reconstruction passed and preserved the exact 451-file,
  2,224,274-byte tree at SHA-256
  `73384b72019434b9d1a60aab38773257035e4e7464a3ea9088d31941e6f57b55`.
  This is a running prefix, not a template result.

### 19:22 — `hole5` production reaches 192 cuts

- A bounded 128-iteration resume added 128 complete SAT/coloring attempts,
  taking `hole5` from 64 to 192 distinct globally valid cuts.  There was no
  terminal, timeout, unknown result, or memory-limit event.
- New solver children used 9.1903 seconds total wall time and 6.7850 seconds
  total CPU.  Maximum child wall time was 0.2007 seconds and maximum RSS was
  11,894,784 bytes.
- The checkpoint SHA-256 is
  `1596f9194d44b90be5a1ec583f68e8da8a3050aa0a584fc733ce920ccd441b89`,
  with history head
  `8dce61c5d51502476c454bc5c29ea685a28a7f5d19b504ba065a4e42c4b5033e`.
- Frozen deep reconstruction and a separate read-only audit both passed,
  preserving the exact 1,347-file, 6,688,922-byte tree at SHA-256
  `143a09afb4124c8ad4580f7a38bb3bd9312f2a99e89649cba28d99fe5eec050c`.
  This branch remains open.

### 19:24 — recovered `hole9` certificate accepted

- Promoted the recovered exact-CNF result to claim C-028 after a fresh
  independent mathematical-scope audit and an `ACCEPT WITH TWO VALIDATED
  ERRATA` hostile verdict.
- The exact formula has 6,886 variables, 20,030 base clauses, and 170
  globally valid coloring cuts.  Its 4,705-addition deletion-free proof ends
  in the empty clause.  The independent standard-library checker replayed
  every addition as RUP, all 170 checkpoint/cut chronology links, and 2,210
  artifact bindings; it rejected 11 decisive mutations.
- The result excludes every connected 12-vertex graph with
  \(\gamma=\alpha=\gamma^\infty=3<\theta\) whose complement contains a
  hub-free induced \(C_9\).  By the accepted odd-wheel theorem, a survivor
  has no induced \(C_9\) at all; it must lie in the remaining hub-free
  \(C_5\) or \(C_7\) branches.
- The source run remains byte-identical with checkpoint status `running` and
  no terminal marker.  The recovery is publication-bound as a separate
  certificate, not represented as a retroactive terminal.
- Root replayed the sealed-package audit, all 12 focused tests, and the
  independent hostile proof checker successfully.  A full 238-test replay
  had 227 passes and 11 resource-gate errors: all 11 synthesis smoke tests
  refused admission because current free disk was below their conservative
  reserve-plus-session requirement.  There were no assertion failures, and
  that first invocation is not labeled passing.
- Free space then rebounded from approximately 6.3 GB to 9.9 GB when
  unrelated local activity released storage.  The unchanged full suite was
  rerun in one invocation and passed all 238 tests in 57.44 seconds, with
  peak RSS 115,965,952 bytes.  The earlier refusal remains part of the
  resource log because it confirms that the production guard failed closed.

### 19:49 — `hole5` reaches 448 cuts

- One bounded 256-iteration resume added 256 complete SAT/coloring attempts,
  bringing `hole5` to 448 distinct globally valid cuts.  The branch remains
  `running`; there was no terminal, candidate, timeout, unknown result, or
  memory event.
- The new checkpoint SHA-256 is
  `ca4556b6d8b931d71b7b143d1e8b7c3aab4475fa1edae90a83c7acb107100b55`,
  with history head
  `70f446f1b7e14b863a64108bfffe519a3ffb58c6e45c45f1c77e967dba6c3baf`.
- Frozen deep reconstruction and a separate standard-library audit checked
  all 448 chronology, artifact, command, limit, and compact-prefix records.
  The exact 3,139-file, 15,610,294-byte run tree remained at SHA-256
  `cf12c4c0a7923a849d837ddaaabc186e688f2f5368e858d6fa5bb4b8a2b445b4`.
- The 256 solver children used 16.6234 seconds total wall time and
  12.7135 seconds total CPU; maximum child wall time was 0.1514 seconds and
  maximum RSS was 17,399,808 bytes.

### 19:52 — exact template-coloring bank identified

- Independent read-only analyses of the published `hole5` and `hole7`
  trajectories derived the exact number of nontrivial three-coloring cuts
  compatible with each forced odd-hole template:
  \[
    M_\ell=(2^\ell-2)3^{11-\ell}/6.
  \]
  The resulting counts are 3,645 for `hole5`, 1,701 for `hole7`, and 765
  for `hole9`.
- The proof uses only the forced template: an odd \(C_\ell\) has
  \(2^\ell-2\) labeled proper three-colorings; the external common neighbor
  of rim edge \(01\) is forced to the third color; the remaining vertices
  are free; and the forced triangle makes the six color-name permutations
  act freely.
- Adjoining the standard positive same-color edge clause for every
  compatible partition is exactly equivalent, relative to the template
  units, to requiring \(\chi(H)>3\).  Thus the full `hole5` and `hole7`
  formulas have only 23,653 and 21,718 clauses respectively.
- The existing adaptive cuts are highly symmetry-redundant.  The first
  192 `hole5` cuts occupy 31 template-symmetry orbits whose closures contain
  2,832 of all 3,645 compatible partitions.  The 384 `hole7` cuts occupy 59
  orbits covering 986 of 1,701 partitions.  Individual candidate graphs
  generally have only one or two proper colorings, so enumerating more
  colorings of the same candidate is not the useful batching mechanism.
- Measured gate decision: preserve and pause the append-only CEGAR prefixes,
  implement a deterministic full-bank generator, independently enumerate
  and audit its universe, and compare proof-producing one-shot SAT runs.
  No bank theorem or finite exclusion is claimed before those gates pass.

### 20:24 — exact coloring-bank theorem and implementation accepted

- Proved and independently reviewed the exact template-coloring-bank theorem.
  Relative to the forced positive `hole5`, `hole7`, and `hole9` template
  edges, the complete first-use bank is equivalent to
  \(\chi(\overline G)>3\).  Exact bank sizes are 3,645, 1,701, and 765.
- Froze a deterministic generator and bounded proof-runner.  It refuses
  overwrite, symlinked and protected paths, unpinned tools, excessive
  resource requests, and missing validation gates.  Every launched solver or
  checker failure produces an explicit nonclaim outcome.  A SAT model is
  checked directly against the exact CNF and decoded graph/family semantics;
  UNSAT is promoted only after a nonempty proof receives one warning-free
  `s VERIFIED` from pinned DRAT-trim.
- Two independent reviewers accepted the frozen theorem and implementation.
  The standalone reviewer imports no campaign module, exhausts all
  \(3^{12}=531{,}441\) assignments for each template, reconstructs all 6,886
  variables and every base-plus-bank clause independently, and rejects eight
  semantic mutations.
- Root replay passed 12 focused tests in 62.578 seconds with peak RSS
  61,865,984 bytes, and all 250 campaign tests in 121.953 seconds with peak
  RSS 106,971,136 bytes.
- All 170 accepted `hole9` cuts are exact members of the 765-row complete
  bank.  The accepted 4,705-addition RUP proof therefore remains valid under
  the 595 extra axioms.  Pinned DRAT-trim replayed it directly against the
  complete development formula in 0.083 seconds, with one warning-free
  `s VERIFIED`.
- Development bank/CNF fixtures passed independent reconstruction but
  correctly fail the production source-to-`HEAD` gate.  Publish the frozen
  source first, regenerate retained packages from the committed snapshot,
  and require `runtime_sources_match_head=true` before novel `hole7` or
  `hole5` production.

### 20:39 — retained packages accepted; provisional `hole7` UNSAT

- Committed and pushed the exact bank implementation at `2e68a639`, then
  regenerated `hole9`, `hole7`, and `hole5` packages.  All manifests bind
  that commit with `runtime_sources_match_head=true` and no mismatch.
- An author audit and a separate standard-library production audit
  reconstructed every bank and CNF byte and exhausted all \(3^{12}\)
  colorings per template.  The independent verdict on all three retained
  packages is `ACCEPT`.
- The first bounded complete-bank `hole7` run returned solver-level UNSAT in
  11.381 seconds and produced a 35,285,574-byte proof.  The integrated
  checker stopped with exit 80 before `s VERIFIED` because `-W` treats a
  deletion-related forward-checking warning as terminal.  The preserved run
  therefore remains an explicit nonclaim.
- A diagnostic replay without `-W` verified the proof, reporting zero RAT
  lemmas.  Independent work is now producing an addition-only proof and
  requiring warning-free `-I -f -W -U` replay.  No `hole7` mathematical
  exclusion is accepted before that artifact and the graph-to-CNF bridge
  pass hostile review.

### 21:11 — `hole7` excluded; only `hole5` remains for \((12,3)\)

- Promoted C-030 to `CERTIFIED-FINITE`.  The exact complete-bank `hole7`
  formula is UNSAT: its 18,093,724-byte addition-only proof contains 284,317
  RUP additions and passed two warning-fatal, RUP-only DRAT-trim replays.
  The independent audit also reconstructed all 1,701 bank clauses,
  exhausted \(3^{12}\) colorings, checked the graph-to-CNF implication, and
  rejected ten proof mutations.
- Diagnosed the original checker exit 80 exactly.  A source proof line asks
  to delete a clause currently retained as a pseudo-unit reason; forward
  checking safely ignores that optimization, while `-W` turns the resulting
  implementation warning into exit 80.  Removing all deletion records is
  monotone for RUP and the resulting proof passed strict checking directly.
- Directly replayed the accepted `hole9` 4,705-addition proof against the
  retained 20,795-clause full-bank formula.  The replay was warning-free and
  an independent multiset audit proved the older 20,200 clauses are an exact
  subset with 595 added bank clauses.
- The complete-bank `hole5` run hit a 512 MiB ASCII-proof limit after
  153.478 seconds without a solver result.  Controlled proofless trials
  using the default configuration for 600 seconds and the UNSAT preset for
  300 seconds both returned `c UNKNOWN`, using less than 66 MiB peak RSS.
  The branch remains open.
- A hostile symmetry audit refuted the tempting shortcut of retaining one
  coloring clause per template-coloring orbit: 442 of the 448 historical
  candidates satisfy all 72 representatives, with an explicit candidate
  and missed coloring retained.  Color-orbit representatives cannot be
  chosen independently of a single graph relabeling.
- Selected a sound stronger mechanism instead.  The full `hole5` CNF is
  exactly invariant under permutations of the six unmarked vertices
  \(6,\ldots,11\).  Sorting their adjacency signatures to fixed vertices
  \(0,\ldots,5\) uses 315 auxiliary-free comparator clauses and preserves a
  representative of every model.  Implementation, exhaustive comparator
  testing, covariance audit, and written proof are the next production
  gates.

### 21:30 — `hole5` signature symmetry accepted for source freeze

- Proved that the retained complete-bank `hole5` formula is invariant under
  the full \(S_6\) action on vertices \(6,\ldots,11\), including transport
  of edge, witness, eternal-family, and move variables.  Sorting the six
  core-adjacency signatures therefore preserves a model in every labeled
  orbit and is an equisatisfiable symmetry breaker.
- Derived the exact auxiliary-free comparator: 63 clauses and 642 literals
  per adjacent signature pair, hence 315 clauses and 3,210 literals total.
  The strengthened formula has 6,886 variables, 23,968 clauses, and 192,169
  literals.
- The author generator retains the complete source CNF body byte-for-byte
  after the changed header, appends only the breaker stream, refuses
  overwrite, binds exact retained-package hashes, audits all 20,480
  comparator assignments, and checks covariance under all five generating
  transpositions.
- A clean-room reviewer independently reconstructed the full variable
  allocation, base, bank, \(S_6\) action, and comparator.  Its header-free
  stream SHA-256 `ddd32969...` equals the author stream.  The review also
  retained a concrete countermodel showing why one coloring cut per
  graph-label orbit would be unsound.
- A separate clean-room binary-DRAT audit rejected 20 malformed streams and
  accepted exact deletion stripping plus strict `-i -f -W -U` smoke.  It
  found malformed-varint and literal-range gaps in the pinned checker
  boundary, so independent canonical preparse with maximum variable 6,886
  is mandatory for any production proof.
- Root passed 8 focused tests and all 258 campaign tests.  Freeze and publish
  the source/audits next; production generation remains closed until the
  committed Git bytes are rebound.

### 21:52 — committed binding and retained `hole5` signature package accepted

- Commit `10acf379329411d9d05267b3411d6703047e705e` froze and
  published the signature theorem and implementation.  A postcommit
  clean-room binding audit confirmed that the author note, source, tests,
  and validation log are byte-identical to their Git objects.
- The author's 11,424-byte comparator stream exactly equals the independent
  stream at SHA-256 `ddd32969...`.  Independent and author constructions
  produce the same 754,323-byte CNF at SHA-256 `c6a0811c...`, with 6,886
  variables, 23,968 clauses, and 192,169 literals.
- Generated the retained three-file package from committed sources.  The
  manifest SHA-256 is `da33bc17...`, the tree SHA-256 is `dd9ac46f...`,
  and all six runtime sources match the recorded Git revision.
- A separate standard-library auditor reconstructed the entire package
  byte-for-byte without importing the author or synthesis modules.  It
  accepted the source-body prefix, exact 315-clause suffix, manifest, Git
  bindings, filesystem constraints, and replay of the independent \(S_6\)
  probe.
- Promoted C-031 as `PROVED`, with the explicit boundary that
  equisatisfiability is only a sound reduction.  No `hole5` SAT/UNSAT claim
  exists.
- The next gate is to freeze and hostile-test a binary-proof runner, then
  launch one bounded seed-0 solve against this exact package.  A residual
  rim-reflection reduction is being audited independently as a fallback if
  the sorted parent remains hard.

### 22:12 — residual reflection and conditional `hole5` coverage accepted

- Independently reconstructed the residual rim reflection
  \(\rho=(0\ 1)(2\ 4)\) on all 6,886 edge, common-neighbor, family, and
  move variables.  It is a role-preserving involution and preserves the
  exact base, complete coloring bank, and full \(F_5\) clause multisets.
- Proved C-032:
  \[
  F_5\text{ is satisfiable}\iff F_5\land S\land T\text{ is satisfiable},
  \qquad T=(-24,39).
  \]
  If \(T\) fails, reflection swaps \(e_{25}\) and \(e_{45}\); sorting the
  outer vertices afterward preserves \(T\) because the outer \(S_6\) action
  fixes the six core vertices.
- The source units \(e_{05}=e_{15}=1\), the vertex-5 no-hub clause, and
  \(T\) leave exactly five exhaustive
  \((e_{25},e_{35},e_{45})\) representatives:
  `000`, `001`, `010`, `011`, and `101`.
- The canonical exact \(F_5\land S\land T\) construction has 6,886
  variables, 23,969 clauses, 192,171 literals, 754,332 bytes, and SHA-256
  `441e54c28fdf6005f0f17fb951bf37c7ff46e222f3e605b7e715fabeec8f64d4`.
- Proved C-033 as a conditional realization statement.  A connected
  order-12 parameter-three counterexample whose complement contains a
  hub-free induced \(C_5\) supplies explicit assignments satisfying every
  clause of the exact retained \(F_5\): graph edges, one common-neighbor
  witness per pair, a nonempty one-guard eternal family, one legal response
  per selected state and unoccupied attack, connected cuts, and all complete
  coloring-bank clauses.  Accepted symmetry supplies strengthened models.
- The certificate premise remains explicitly unfilled: there is no accepted
  checked proof here that the exact strengthened CNF is UNSAT.  Therefore
  no `hole5` exclusion and no \((12,3)\) slice claim were made.  No solver,
  checker, or runner was invoked for this checkpoint.

### 22:36 — fail-closed binary production runner accepted for source freeze

- Froze a bounded binary-proof runner for the exact retained
  signature-sorted `hole5` package.  It preserves the raw CaDiCaL proof,
  invokes the independent binary parser under isolated Python, verifies the
  canonical addition-only stream, and accepts UNSAT only after a strict,
  warning-fatal, RUP-only DRAT-trim replay.  SAT is deliberately retained as
  a candidate rather than a mathematical claim.
- The first hostile audit accepted the proof/result/resource/post-write
  boundary, but a second independent auditor found that `cegar.py` imported
  `coloring.py` and `generate.py` outside the declared Git-bound runtime
  source set.  This was a real pre-launch provenance defect, so the solve
  remained stopped.
- The repaired runner binds the exact eight-module local import closure and
  carries a recursive AST closure regression.  It also recomputes the exact
  hashes of both pinned executables and both source archives through a
  separately bound hashing implementation.  Eight independent tool/archive
  mutations and the original dependency-gap construction are rejected.
- Final hashes are runner `02e8a13d...`, tests `e622ef08...`, hostile probe
  `06261bbc...`, canonical hostile log `f9ca64c9...`, and hostile review
  `63af7f25...`.  The primary verdict is
  `ACCEPT_FOR_COMMIT_WITH_MANDATORY_POSTCOMMIT_HEAD_GATE`; the second audit is
  `ACCEPT_NO_BLOCKER`.
- Root passed 30 focused tests and all 271 campaign tests.  The full run took
  204.18 seconds, 194.10 CPU seconds, and at most 115,851,264 bytes RSS.
  Manifest ART-199--204 binds the source, tests, hostile artifacts, and
  validation record.
- No production solver was launched.  The audited bytes must first be
  committed on `main`, pushed, and replayed against the exact current Git
  `HEAD`; a fresh resource/lock gate is also mandatory before the bounded
  seed-0 attempt.

### 23:27 — complete order-12, parameter-three slice certified empty

- Committed and pushed the exact accepted binary-production source at
  `6f3ef0a0`, passed its mandatory current-`HEAD` and resource gates, and
  ran one seed-0 production attempt against the retained
  signature-sorted `hole5` package.  The untouched 12-file result directory
  is frozen at commit `dff45f42`.
- The exact 6,886-variable, 23,968-clause CNF returned
  `s UNSATISFIABLE` in 6.151 seconds.  The raw binary proof was
  12,524,020 bytes; independent canonical parsing removed 245,439 deletion
  records and retained 247,981 additions in a 6,337,621-byte
  addition-only proof.
- Pinned DRAT-trim accepted that proof under warning-fatal, forward,
  RUP-only checking (`-i -f -W -U`) in 57.729 seconds.  It reported exactly
  one `s VERIFIED`, zero RAT lemmas, and 10,912,555 resolution steps.
  Root independently repeated the parser and checker replay before
  promotion.
- A clean-room post-run probe reconstructed the exact CNF without importing
  either the production runner or synthesis core, parsed both binary
  streams, confirmed exact deletion stripping, bound the source and frozen
  artifact commits, and performed another strict replay.  Its verdict was
  `ACCEPT_C5_UNSAT_CERTIFICATE_FOR_C033`.  A second clean-room package
  auditor bound all 12 run files, 23 runtime sources, both pinned tools,
  exact Git trees, and three byte-identical complete replays.
- Promoted C-034: the hub-free induced-\(C_5\) branch of the order-12,
  parameter-three search is empty.  This fills the separate certificate
  premise in the already proved graph-to-\(F_5\) realization theorem C-033.
- Wrote the complete slice theorem and closed the disconnected case
  explicitly using additivity and the minimum-parameter theorem.  Together
  with the accepted \(C_7\) and \(C_9\) branch certificates and the
  SPGT-based structural split, this proves C-035:
  \[
  \nexists\,G,\ |V(G)|=12,\qquad
  \gamma(G)=\gamma^\infty(G)=3<\theta(G).
  \]
  Two independent mathematical reviewers returned
  `ACCEPT_COMPLETE_ORDER12_K3_EXCLUSION` and `ACCEPT_NO_BLOCKER`.
- This is a substantial `CERTIFIED-FINITE` campaign result, not a universal
  resolution.  The order-12 \(k\geq4\) slice and all larger orders remain
  open.
- The main practical discovery was that a proved 315-clause \(S_6\)
  signature ordering transformed the last branch from a 512 MiB
  proof-file-cap failure into a 6.151-second solve with a compact checked
  proof.  The audit stack also caught and forced repair of a missing
  dependency binding and a nondeterministic temporary-path leak before
  acceptance.

### 2026-07-26 01:05 — manuscript/replay package and exact \(k=4\) frontier

- Converted C-035 into a nine-page submission-oriented manuscript with the
  exact coverage proof, branch formula and RUP-proof hashes, explicit
  one-guard convention, disconnected reduction, finite-scope warning, and a
  one-command replay appendix.  A final wording audit caught and repaired an
  abstract overstatement: the \(C_9\) instance contains 170 valid coloring
  clauses implied by non-three-colorability, not a complete coloring bank.
- Built the corrected manuscript twice from clean directories under the
  fixed epoch.  Both PDFs are byte-identical at SHA-256 `f84430ee...`; the
  final source is `dddf4a1b...`, the document has nine US-Letter pages, and
  the logs contain no actual warnings, unresolved references, or bad boxes.
  Author metadata and a permanent archive identifier remain explicit
  pre-submission placeholders.
- Added a fail-closed C-035 replay wrapper.  It binds the exact theorem,
  three accepted formula/proof branches, reviews, checker programs, and Git
  objects.  Fast mode is explicitly metadata-only.  Full mode is sequential,
  resource-gated, cleans up timed-out process groups, and accepts only after
  every independent branch audit succeeds.  Fifteen bounded tests and a
  hostile mutation/resource review passed.
- Proved C-036 from the classical Payan--Xuong/Fink--Jacobson--Kinch--Roberts
  half-order characterization: a connected counterexample satisfies
  \(n\geq2k+1\).  At order 12 this removes \(k=6\); combined with C-035 it
  leaves only \(k=4,5\).  The note and hostile review make no novelty claim
  for this classical corollary.
- Derived and implemented the exact connected order-12 \(k=4\) complement
  target C-037.  The permanent anchored parent has 18,381 variables, 114,742
  clauses, 1,180,016 literals, and SHA-256 `adbe0c01...`.  Its complete
  anchored four-coloring bank has 65,536 rows, and the sound \(S_8\) outer
  signature ordering has 105 clauses.
- A clean-room hostile probe reconstructed the entire \(k=4\) formula
  byte-for-byte without importing the synthesis core, checked every
  coloring-bank row and comparator case, exhausted a 512-graph small-model
  universe, killed seven deliberate mutations, and reproduced the
  permanent package.  Nine focused constructor tests passed.  No solver was
  invoked, so this is exact target infrastructure rather than a \(k=4\)
  existence or exclusion result.
- The machine remained deliberately unsaturated by this campaign.  Other
  local work held load averages above 20 and free disk space near 18 GiB, so
  the full proof replay and any heavy \(k=4\) solve were deferred by their
  resource gates.

### 2026-07-26 02:00 — structural \(k=4\) reduction and candidate verifier accepted

- Proved and independently accepted C-038.  If
  \(H=\overline G\) satisfies the complement-side three-set witness property
  forced by \(\gamma(G)=4\), and \(G\) is connected, every induced hole in
  \(H\) leaves at least four vertices outside it.  The proof handles
  \(r=0,1,2,3\) separately and uses connectedness at the exact complement
  sign.
- At order 12 this eliminates induced \(C_9\) and \(C_{11}\) holes.  SPGT,
  the clique-number bound on antiholes, and the accepted one-guard cycle
  values leave exactly three overlapping complement templates:
  \(C_5,C_7,\overline{C_7}\).  This is a structural reduction, not a
  \((12,4)\) exclusion.
- A clean-room probe exhausted every fixed induced-\(C_5\) graph with at most
  three outside vertices.  The \(r=3\) layer contained 262,144 graphs; all
  274 satisfying P3 had a hub and none had connected complement.  A separate
  literal one-guard fixed-point implementation reproduced the cycle and
  anticycle values used in the proof.
- Built a standard-library-only decoded-candidate verifier.  Acceptance is
  based only on graph identity, exact \(\gamma=4\), a literal nonempty
  one-guard eternal family, and exhaustive failure of all 65,536
  anchor-normalized complement four-colorings.  Connectedness,
  \(\alpha=i=4\), well-coveredness, class restrictions, a Wagner minor, and
  an odd-hole/antihole witness are independently checked but cannot erase a
  definition-level counterexample.
- The hostile verifier audit ran thousands of independent graph, parameter,
  transition, coloring, and trace comparisons.  It found a deeply nested
  valid-JSON input that escaped the documented malformed-input exit path.
  The loader now translates that exact recursion failure into a structured
  error; the 1,000,001-byte reproducer and all 13 authored tests pass.
- The compressed literature refresh found no direct resolution.  It
  confirmed that the 2026 Cayley paper uses the all-guards-move parameter:
  one guard reaches the attacked vertex while every remaining guard may also
  move.  Its results were kept only in the variant ledger.
- A draft 16-leaf proof runner was deliberately rejected before source
  freeze.  A real two-variable proof showed that forward-mode `drat-trim`
  verification cannot simultaneously be trusted to emit LRAT accepted by
  the pinned `lrat-check`.  The same hostile pass found two unrecoverable
  crash windows, an unchecked attempt-config hash, and a production API test
  hook capable of fabricating child results.
- None of those runner defects affects C-035, C-037, C-038, or the candidate
  verifier, and no \(k=4\) solver was launched.  The required repair is a
  four-stage solver/forward-DRAT/backward-LRAT/LRAT-replay pipeline with
  exact crash reconciliation and no injectable production child.
- At the checkpoint resource probe, load and disk passed but reclaimable
  memory did not meet the conservative 4 GiB child plus 2 GiB reserve gate.
  The next real proof job will therefore wait.  Once the repaired runner is
  committed and independently accepted, the trivially inconsistent `1111`
  Boolean leaf is the first low-cost end-to-end production target.

### 2026-07-26 02:30 — hub theorem and repaired \(k=4\) runner accepted

- Proved C-039 as a structural necessary condition.  For
  \(\gamma=\gamma^\infty=4\), the vertices complete in the complement to an
  induced odd-hole rim form an independent set.  The three-set witness
  property further bounds their number by \(r-2\) when the hole has \(r\ge2\)
  outside vertices.  An induced complement \(\overline{C_7}\) has no outside
  hub.  The order-12 \(C_5,C_7,\overline{C_7}\) bounds are therefore
  respectively five, three, and zero.
- The hostile proof review returned `ACCEPT_WITHOUT_SCOPE_INFLATION`.  A
  clean-room one-guard implementation checked the value-one lemma,
  induced-subgraph monotonicity on 32,767 pairs, component additivity on 121
  pairs, P3 equivalence, the cycle/anticycle inputs, and all fixed-\(C_5\)
  extensions at \(r=2,3\), including 262,144 graphs in the latter layer.
  The theorem remains a necessary filter and does not exclude a branch.
- The rejected production runner was repaired without launching the
  order-12 solver.  Its final protocol uses four distinct children:
  CaDiCaL binary-DRAT production, warning-fatal forward raw verification,
  backward LRAT conversion, and fresh `lrat-check` replay.  The two former
  crash windows now reconcile append-only to retryable nonclaims; the
  attempt-config hash is enforced; the public injectable child hook is gone.
- Independent hostile review returned
  `ACCEPT_PRODUCTION_READY_ENGINEERING_NO_AGGREGATE_CLAIM`.  It reconstructed
  all 16 Boolean leaves, matched every CNF hash, reran the real tiny
  four-stage proof chain, preserved the old broken combined `-f -L` mode as
  a rejection regression, and exercised both crash windows and binding
  mutations.  Root independently reran all 17 tests in 56.974 seconds and
  the hostile probe in 23.95 seconds; both passed.
- The claim boundary is unchanged: zero production leaves have run and no
  order-12 \(k=4\) SAT or UNSAT result exists.  Even 16 runner-level verified
  leaves would remain pending a separate aggregate checker with fresh LRAT
  replay.
- At 02:27 the Apple M1 Pro had load averages 2.80/3.46/3.90, 16 GiB physical
  memory, about 4.73 GB reclaimable by the runner probe, and about 26.4 GiB
  free disk.  This is adequate for a conservative 3 GiB child plus 1 GiB
  reserve gate, but source bytes must first be committed and the aggregate
  checker remains under independent development.

### 2026-07-26 02:46 — real initializer finds and closes Git-path defect

- After checkpoint 033 was committed, the first real production initializer
  failed closed during source provenance binding.  No run directory was
  created and no solver process was started.
- The campaign lives in a subdirectory of the Git worktree.  The runner used
  `git rev-parse HEAD:src/...`, which Git interprets from the repository
  root.  The command returned 128 before initialization.  Both creation and
  verification now use the campaign-relative revision form
  `HEAD:./src/...`.
- Added an unmocked regression that creates and rechecks a real committed
  source binding from the campaign directory.  Root reran 18/18 tests in
  57.058 seconds and the updated hostile probe in 24.31 seconds.
- A different hostile reviewer reproduced the old exit 128, matched the
  corrected revision blob to the worktree blob, and reran 18/18 tests plus
  the complete tiny-proof, crash, mutation, and provenance probe.  Verdict:
  `ACCEPT_PRODUCTION_READY_ENGINEERING_NO_AGGREGATE_CLAIM`.
- The corrected runner itself must now be committed byte-for-byte.  Until
  then, the same provenance gate intentionally refuses initialization
  because the reviewed worktree blob differs from `HEAD`.  Zero production
  leaves have run, so the exact order-12 parameter-four status is unchanged.

### 2026-07-26 02:56 — `1111` smoke test exposes LRAT conversion gap

- Committed source binding succeeded under exact campaign commit
  `9b24d9ff...`.  The immutable run
  `results/order12_k4_production_seed0` initialized all 16 leaves with source
  set SHA-256 `ea6d74e6...`, partition `0cf81297...`, and initial checkpoint
  `0355d092...`.  A read-only audit returned 16 pending leaves and
  `INCOMPLETE_NONCLAIM`.
- Authorized only case `1111`, the deliberately retained anchored
  complement-\(K_5\) contradiction.  CaDiCaL returned exit 20 in 0.062
  seconds and retained a 215,475-byte binary DRAT proof.  Warning-fatal
  forward replay returned exactly one `s VERIFIED`.
- The separate backward converter then exited 80 on
  `backward mode ignores deletion of (pseudo) unit clause [0] 14 0` and
  emitted an empty LRAT.  The runner preserved every byte, appended its
  completion checkpoint, made the leaf retryable, and returned
  `LRAT_CONVERSION_REJECTED_NONCLAIM`.  No checker ran and no leaf UNSAT
  status was promoted.
- Post-attempt read-only audit passed with 15 pending leaves, one retryable
  nonclaim, zero active attempts, and one completed attempt.  The v2 run is
  now frozen for diagnosis; it will not be retried under changed source
  bytes.
- A strict exploratory parse found 9,690 additions and 6,956 deletions.  The
  unique empty addition is record 16,643; the only later records delete unit
  clauses 14, 23, and 31.  In a temporary, explicitly non-certificate
  experiment, truncating logically after the empty clause and stripping
  deletions produced a 106,318-byte addition-only stream.  It passed forward
  `-U`, backward LRAT conversion, and fresh `lrat-check`; the temporary LRAT
  hash was `90787a09...`.
- Version three must therefore retain the raw proof, normalize it with a
  separately bounded strict parser, verify the exact addition-only stream as
  RUP, convert that stream to LRAT, and freshly replay it.  This observation
  is not a certified `1111` result until the transformation, pipeline,
  schemas, and independent aggregate checker are implemented and reviewed.

### 2026-07-26 03:12 — anti-\(C_7\) near-hub restriction accepted

- A local two-spoke theorem was proved directly from the one-guard
  definition.  If two vertices outside an induced \(C_7\) each have exactly
  one cycle neighbor and the ambient graph has
  \(\gamma^\infty\leq4\), then the outside pair is adjacent and their cycle
  neighbors coincide.
- In the complement target, vertices adjacent to exactly six vertices of an
  induced \(\overline{C_7}\) are therefore mutually nonadjacent and share
  one missing rim vertex.  Three P3 test triples then show that order 12
  permits at most three such near-hubs: four force the sole remaining
  outside vertex to be a forbidden hub, and five violate P3 directly.
- The independent reviewer checked the exact one-guard attack table,
  complement direction, and scope, and independently enumerated all 98
  two-spoke cases, 49 deleted-pair cases, and 896 cap cases.  Verdict:
  `ACCEPT_PROVED_LOCAL_LEMMAS_WITHOUT_SCOPE_INFLATION`.
- This is C-041, a proved necessary condition and precise incidence
  subbranch exclusion.  The full anti-\(C_7\) branch and the order-12
  parameter-four slice remain open, and no novelty claim is made before a
  literature comparison.

### 2026-07-26 04:30 — v3 case `1111` certified as one exact leaf

- The v3 author candidate passed 29/29 tests, including the real tiny
  six-stage proof chain, binary-normalizer hostile inputs, interruption
  recovery, v2 refusal, provenance mutations, and unmocked Git binding.
  Exact committed bytes at `f4ccb167...` then received the independent
  verdict `ACCEPTED_ENGINEERING_DESIGN_NO_MATHEMATICAL_CLAIM`; the committed
  hostile replay independently passed 29/29 tests.
- A new immutable source-bound run was initialized at
  `results/order12_k4_production_v3_seed0`.  Only case `1111` was authorized.
  Its exact leaf appends units \(4,14,23,31\) to the C-037 parent and has
  18,381 variables, 114,746 clauses, 1,180,020 literals, and SHA-256
  `aafc85341993ed030fe72ba222a4efaa5a02f6ea6fa95519a9dd2ed755b94d1f`.
- All six production children completed successfully: solver, raw forward
  proof check, strict normalization, normalized RUP-only forward check,
  RUP-only LRAT conversion, and fresh LRAT replay.  The retained raw proof is
  `a50b814d...`, the exact addition-only stream is `f3401ad8...`, and the
  converted LRAT is `90787a09...`.  Outcome `00e3c191...` and certificate
  `7c9705f5...` record `UNSAT_LRAT_VERIFIED`.
- A separate postrun reviewer reconstructed the leaf CNF byte-for-byte
  without importing runner transition or proof logic, independently rescanned
  the binary streams, and freshly replayed the LRAT on private copies under
  the campaign lock.  No solver was launched and no retained byte changed.
  Verdict: `CERTIFICATE_REPLAY_PASSED_ONE_LEAF_ONLY`.
- This promotes C-042 as `CERTIFIED-FINITE` for **exactly cube `1111`**.
  Fifteen cubes remain `PENDING`, the aggregate remains
  `INCOMPLETE_NONCLAIM`, and neither the full connected parent, the
  \((12,4)\) slice, nor the universal conjecture is settled.  Commit
  `92f5ed2b...` preserves the production package.
- The earlier aggregate-checker prototype was bound to the rejected v2
  schemas and is not accepted for this package.  Its v3 repair is in
  progress; it must freshly replay completed LRATs and independently verify
  partition coverage before any aggregate theorem is possible.

### 2026-07-26 05:00 — exact \(k=4\) parent reduced to four canonical cubes

- Connectedness gives every anchor vertex a \(G\)-neighbor outside the
  anchored independent four-set.  For anchor 0 this supplies an outer
  signature whose first \(H\)-adjacency bit is zero; the accepted
  lexicographic outer ordering therefore forces \(e_{0,4}=0\).
- This short argument logically excludes all eight `1***` leaves.  The
  hostile reviewer parsed the exact parent, exhaustively checked all
  comparator truth rows and all 490,314 nondecreasing eight-signature
  sequences, and returned `ACCEPT EXACT LOGICAL REDUCTION`.
- A second argument uses the full anchor \(S_4\) action.  Relabel an anchor
  permutation together with every semantic variable and the four color
  names, then re-sort the outer signatures.  Choose the lexicographically
  least concatenated signature word in this orbit.  An adjacent `10`
  inversion in its first signature could be swapped to `01`, contradicting
  minimality.  No-\(K_5\) then leaves exactly `0000`, `0001`, `0011`, and
  `0111`.
- The independent review regenerated and matched the exact 65,536-clause
  coloring bank, checked all \(24\cdot65,536=1,572,864\) anchor/color
  actions, all 458,752 adjacent outer actions on the bank, and all 319,770
  admissible signature multisets.  Verdict:
  `ACCEPT EXACT FOUR-CUBE ORBIT REDUCTION`.
- These are C-043 and C-044.  They do not change the immutable production
  histogram: case `1111` remains the sole certified leaf and the other 15
  remain recorded as pending.  Mathematically, however, deciding the exact
  parent now requires only the four canonical leaves.  The discarded
  zero-first leaves are orbit-redundant, not individually UNSAT.
- The independent aggregate verifier simultaneously passed its author gate:
  18/18 tests and a fresh private replay of case `1111`, correctly returning
  a one-of-16 incomplete nonclaim under an external append-only ledger.
  Hostile exact-byte review remains mandatory before a second production
  leaf.
- A further DoubleLex idea was frozen as a proposal: choose the row-major
  least \(S_8\times S_4\) anchor--outer matrix, which has both sorted rows
  and sorted eight-bit columns.  The proposed auxiliary-free strengthening
  adds 765 clauses and 10,758 literals.  It is not yet reviewed or used.

### 2026-07-26 05:15 — independent v3 aggregate-verifier gate accepted

- The repaired verifier independently reconstructs the exact
  18,381-variable, 114,742-clause parent without importing the search,
  synthesis, production-runner, or earlier verifier cores.  It derives cube
  variables \(4,14,23,31\), reconstructs all 16 leaf bytes, enumerates the
  16 coverage assignments, and checks all 120 pairwise cube conflicts.
- Its static audit additionally validates the complete immutable v3 layout:
  run and tool bindings, checkpoint chain, exact attempt inventories,
  schemas, raw and normalized binary-DRAT structure, normalization report,
  six child records and resource reports, outcome, certificate, and retained
  aggregate boundary.
- After a hostile wording finding, the incomplete report was repaired to say
  explicitly that it makes no aggregate claim and validates exactly one of
  16 leaves.  Final source set `9ea4397d...` and test source `f7489c39...`
  passed 18/18 author tests; root independently reproduced 18/18.
- The author then performed one authorized checker-only replay from private
  CNF, LRAT, and checker copies.  Its current-source manifest is
  `9039e2b6...`, record `5ec39210...`, and final report `b526a205...`.
  Resume launched zero children and recovered the same record.
- A hostile reviewer started from another new empty external ledger.  The
  current-source manifest is `da860fd3...` and record `0a7e6d41...`.
  Exactly one bounded `lrat-check` child exited zero with `c VERIFIED`;
  the next invocation resumed without a child.  No CaDiCaL process launched,
  and whole-production-tree content and metadata digests remained unchanged.
- Verdict:
  `PASS_EXACT_INCOMPLETE_SCOPE_NO_AGGREGATE_CLAIM`.  The result remains
  exactly `INCOMPLETE_1_OF_16_VERIFIED_NONCLAIM`, with 15 pending leaves and
  CLI exit 3.  This is an accepted verification gate and a second independent
  replay of C-042, not a parent UNSAT result.
- With this gate closed, the next authorized production action is one bounded
  attempt on canonical leaf `0111`.  Its outcome must be preserved and
  independently replayed before any further leaf is launched.

### 2026-07-26 05:25 — DoubleLex accepted; two UNSAT proofs enter certification

- The DoubleLex theorem was hostile-reviewed against exact source bytes.
  Choose the row-major least image of the \(8\times4\) anchor--outer matrix
  under the full \(S_8\times S_4\) action.  A row inversion or adjacent
  column inversion strictly decreases that image, so the same representative
  has both sorted rows and sorted columns.
- The independent probe checked all 18,381 semantic-variable actions and all
  114,637 pre-sort clauses under the ten adjacent group generators.  It
  independently regenerated the three eight-bit comparators, exhausted all
  65,536 assignments, and matched the exact output bytes.
- The accepted DoubleLex suffix has 765 clauses, 10,758 literals, and SHA-256
  `328eeeaadc688bbce63fd3ffd952f86a4eb9209e6d0abf5542979fe54ebdbbe0`.
  The exact strengthened formula has 18,381 variables, 115,507 clauses,
  1,190,774 literals, and SHA-256 `14284db1...`.  This is C-045, a proved
  equisatisfiable strengthening and not an UNSAT result.
- The authorized production attempt on canonical cube `0111` then returned
  solver UNSAT in 3.316 seconds, but the raw warning-fatal forward checker
  exited 80 without a success marker.  The runner preserved outcome
  `1aaba96b...` as `RAW_FORWARD_REJECTED_NONCLAIM`, leaving that production
  leaf retryable.
- A separate strict diagnostic scan accepted the complete 6,481,140-byte raw
  stream: 158,688 additions, 232,381 deletions, and one empty addition as the
  final record.  The exact 2,632,766-byte deletion-free stream (`b1bc9b3a...`)
  passed warning-fatal forward RUP checking in 28.406 seconds.  This strongly
  localizes the failure to the raw checker's deletion handling, but no leaf
  claim is made until a sealed LRAT recovery and hostile replay pass.
- CaDiCaL seed 0 was also run once on the exact accepted DoubleLex formula.
  It returned UNSAT in under one minute and retained a 32,987,136-byte raw
  binary proof with SHA-256 `ed3975c5...`.  This is an exploratory candidate
  result only.  A second bounded lane is building its strict
  normalization/RUP/LRAT certificate without rerunning the solver.
- If the DoubleLex proof certifies, C-037 and C-045 would turn it into a
  complete connected order-12 parameter-four exclusion.  That implication
  remains pending and must receive its own adversarial audit.

### 2026-07-26 07:10 — exact order-12 frontier accepted and replayed

- The complete DoubleLex certificate chain closed.  Strict normalization
  produced a 15,783,377-byte addition-only RUP stream (`2741335a...`).
  Warning-fatal forward and backward checks passed with zero RAT lemmas, and
  the resulting 228,381,671-byte LRAT (`0e04eb63...`) passed a separate
  checker.
- An independent hostile reviewer reconstructed the exact
  18,381-variable, 115,507-clause formula and normalized proof byte for
  byte, ran both proof directions, produced a fresh identical LRAT, replayed
  retained and fresh copies, and killed six proof/formula mutations.  Its
  verdict is `ACCEPT_EXACT_DOUBLELEX_CNF_UNSAT_ONLY`.
- A publication-sized V2 package stores the same LRAT as a
  64,288,636-byte zstd stream (`edc0f6b...`).  Its one-command verifier binds
  the exact formula, compressed and recovered proof, checker, author
  certificate, and hostile evidence.  A separate V2 package review replayed
  it privately and killed 13 mutations, including both metadata-integrity
  regressions found in V1.
- The separately reviewed C-037/C-045 transfer turns exact formula UNSAT
  into the complete connected order-12 \(k=4\) exclusion C-047.  It does
  not assert a disconnected, higher-order, or universal result by itself.
- A simplicial closed-neighborhood theorem and its leaf specialization
  passed independent proof review and exhaustive testing through order
  eight.  A minimum counterexample has no simplicial vertex and hence
  minimum degree at least two.  McCuaig--Shepherd then gives
  \(n\geq\lceil5k/2\rceil\) outside its order-four and order-seven
  exceptions, excluding order-12 \(k=5\).
- The only possible order-12 parameters are \(3,4,5\).  C-035, C-047, and
  the analytic \(k=5\) exclusion exhaust them.  The assembled theorem
  `adb27204...` therefore advances the published counterexample frontier to
  order 12, retaining MacGillivray--Mynhardt--Virgile's through-order-11
  computation as an explicit published premise.  One independent review
  returned `ACCEPT_ORDER12_FRONTIER_WITH_EXPLICIT_PUBLISHED_PREMISE` with no
  blocking defect; a second remains active.
- The machine-readable C-050 acceptance record (`e3b09308...`) binds 21
  theorem, source, review, formula, and proof artifacts.  Root replayed both
  metadata and full-LRAT modes; full mode returned
  `VERIFIED_ORDER12_FRONTIER_BINDINGS_AND_EXACT_LRAT` in 4.1 seconds without
  launching a SAT solver.
- The complete campaign regression suite then passed 359 of 359 tests in
  345.862 seconds with `PYTHONWARNINGS=error`.
- The independent-antineighborhood projection theorem passed its complete
  quantifier audit and a clean-room probe of all 13,598 unlabeled graphs
  through order eight, including 14,421 eligible independent sets and 56,166
  one-guard attack obligations.  The literature lane found important overlap:
  Taletskii's planar minimum-counterexample Lemma 13 already contains
  essentially the local minimum-counterexample conclusion.  The campaign
  theorem is therefore accepted only as a general
  equality-graph/arbitrary-eternal-family extension, with low-to-moderate
  novelty confidence and the unavailable 2018 manuscript caveat.

### 2026-07-26 08:15 — frontier wrapper, manuscript, and order-13 plan sealed

- A new C-050 wrapper reviewer copied the decisive artifacts into a private
  tree, checked all 21 unique bindings and the exact DIMACS census, ran
  metadata and full-LRAT modes, and required seven corruptions plus
  duplicate-key and nonfinite JSON to reject.  Verdict:
  `ACCEPT_EXACT_FROZEN_C050_WRAPPER`; no blocking defect.
- Root reran that audit program and both direct C-050 modes.  The exact
  228,381,671-byte LRAT again passed after decompression; no SAT solver was
  launched.
- The order-12 manuscript was rebuilt with
  `SOURCE_DATE_EPOCH=1785074656`.  Two independent clean builds under
  Tectonic 0.16.9 produced identical BBL and PDF bytes.  The final PDF has 17
  pages, 130,406 bytes, and SHA-256 `1084efc8...`.
- The first complete visual pass found no layout defect but exposed an
  incorrectly parsed BibTeX suffix for Warren A. Hunt, Jr.  The entry was
  corrected, the manuscript was rebuilt deterministically, and the changed
  bibliography page was re-inspected at full resolution.
- A fresh independent manuscript audit checked the theorem transfers,
  published-premise boundary, one-guard quantifiers, complement signs,
  certificate counts/hashes/commands, bibliography, disclosures, two clean
  builds, and all 17 rendered pages.  Verdict:
  `ACCEPT_FROZEN_MANUSCRIPT_WITH_EXPLICIT_PRESUBMISSION_PLACEHOLDERS`.
  Only human author metadata and a permanent archive identifier remain
  before external submission.
- The bounded order-13 strategy passed a separate clean-room audit.  It
  independently reconstructed the proposed `hole5`, `hole7`, `hole9`, and
  `hole11` formula bytes and all generic \(k=3,4,5\) counts.  The corrected
  proved reduction is C-052: an order-13 counterexample is connected with
  \(k\in\{3,4,5\}\), and at \(k=3\) its complement lies in the hub-free
  \(C_5,C_7,C_9,C_{11}\) union.
- The historical proofless `hole11` run remains only `OBSERVED`.  Its v2
  record now says explicitly that argv, CPU time, and transcripts were not
  retained, cannot be reconstructed, and make the historical invocation
  nonreplayable.  The later byte reconstruction is recorded without
  promoting its UNSAT return.
- Two fresh full campaign runs passed all 359 tests with warnings fatal.
  The retained second run took 331.489 test seconds and 331.78 wall seconds,
  peaked at 148,242,432 bytes RSS, and is frozen in
  `results/logs/full-regression-checkpoint042.{log,json}`.  No solver or
  checker remains running.

### 2026-07-26 08:48 — near-spanning odd-hole mechanism found

- Clause-family ablation on the exact proposed order-13 `hole11` semantics
  remained satisfiable through all static graph, domination, and coloring
  constraints, but became UNSAT only when the one-guard transition closure
  was added.  This is an exploratory mechanism probe, not a certified
  formula result.
- A direct structural analysis then removed the solver from the argument.
  If \(H=\overline G\) consists of an induced odd rim \(C_\ell\), for odd
  \(\ell\geq5\), plus exactly two outside vertices \(x,y\), hub-freeness
  makes their rim nonneighborhoods \(X,Y\) nonempty.  The failure of every
  two-set to dominate \(G\) forces every cross pair in \(X\times Y\) to be
  at rim distance two.  Up to swapping \(x,y\) and dihedral rim symmetry,
  this leaves only
  \(X=\{0\},Y=\{2\}\) and
  \(X=\{0\},Y=\{-2,2\}\).  The bound
  \(\alpha(G)\leq\gamma^\infty(G)=3\) forces \(xy\notin E(H)\), except for
  one \(\ell=5\) pattern that is eliminated by a separate one-step attack.
- For odd \(\ell\geq9\), both patterns admit the same short one-guard attack
  argument.  Every
  eternal three-family must contain the independent state
  \(\{4,5,x\}\).  Attack 0.  One successor dies immediately at attack 2;
  the other is forced through states \(\{0,j,x\}\) with odd
  \(j=5,7,\ldots,\ell-4\), attacking \(j+2\) each time, until both final
  moves leave an explicit rim vertex undominated.  Complete short attack
  trees handle every \(\ell=5,7\) pattern.
- At \(\ell=11\), the two resulting graphs \(G\) have Graph6 strings
  `LUzvvz}~r~O?G@` and `LUzvvz}~r~O?GD`.  Independent evaluator A reports
  \(\gamma=i=\alpha=3\) and
  \(\gamma^\infty=\theta=4\) for each.  Their empty three-guard fixed
  points have round profiles \(27+37+36\) and \(31+38+41\), respectively.
- Structurally independent evaluator B, using an explicit colored
  configuration digraph and ordinary set-valued neighborhoods, reproduced
  both Graph6 strings, all five parameters, well-coveredness, and the empty
  three-guard family.
- The clean-room hostile audit independently checked the two-pattern
  classification for all odd lengths through 51, every uniform attack
  transition through length 201, all five exceptional small attack trees,
  the exact infinite-family parameters, every abstract CNF clause family,
  and twelve deliberate model mutations.  Its revised-byte verdict is
  `ACCEPT_REVISED_BYTES_MATHEMATICS_UNCHANGED`.
- Claims C-053--C-055 now record the accepted structural theorem, the two
  infinite exact near-miss families, and the abstract order-13 graph-to-CNF
  equivalence.  Novelty and priority remain explicitly unresolved, and no
  live order-13 branch is yet excluded.

### 2026-07-26 09:40 — proof-runner hostile audit rejects before launch

- A dedicated order-13 constructor and a clean-room constructor independently
  generated identical DIMACS bytes for all four templates, identical complete
  coloring banks, and identical clause-family streams.  The final integration
  audit rejected formula, bank, source-binding, package-exclusivity, and
  run-plan mutations.  It launched no solver.
- The first production runner added exclusive attempts, source/tool/formula
  bindings, one-child resource limits, raw binary DRAT checking,
  addition-only normalization, RUP-only forward checking, LRAT conversion,
  and a separate LRAT replay.  Before any real use, root noticed and repaired
  missing transitive-source bindings and missing human-readable tool
  identities.
- The independent hostile runner review then produced a decisive false
  acceptance.  It appended two checkpoints to a real initialized run but
  pointed their bindings at malformed files outside the run tree.  With
  `attempts/` still empty and no child or proof, the read-only audit reported
  `UNSAT_LRAT_VERIFIED_PENDING_HOSTILE_AUDIT`.  The defect was an absent
  checkpoint-to-attempt path/count crosslink.
- A second exploit rebound the manifest's CaDiCaL role to arbitrary executable
  bytes while leaving the accepted policy mapping unchanged.  Because the
  loader did not compare the tool binding back to the policy hash and the
  displayed identity was static, the audit still labeled and accepted the
  fake executable as the pinned CaDiCaL build.
- A third status-transition defect allowed an interrupted-recovery event to
  carry a success or SAT-candidate status instead of a mandatory nonclaim.
- The runner is rejected until all three exploits and the broader coordinated
  mutation suite fail closed on revised bytes.  No SAT solver, DRAT checker,
  or LRAT checker was launched.  The defects affect only prospective
  production infrastructure; they do not affect C-053--C-055 or any accepted
  earlier certificate.

### 2026-07-26 10:41 — second runner revision rejected on restartability

- A new independent referee, without changing the original rejection bundle,
  verified that the repaired runner closed four further defects: an
  attempt-local formula could no longer differ from the frozen run formula;
  every proof producer/consumer edge was hash-crosslinked before and after
  each child; certificate and outcome shapes were exact; and a durable
  uncheckpointed outcome could never be promoted.
- The referee then injected process loss at four adjacent prefixes before the
  durable `RUN_STARTED` checkpoint: after attempt-directory creation, after
  formula copy and fsync, after attempt-config write, and immediately before
  the checkpoint append.  All four states failed closed, but audit, ordinary
  retry, and explicit recovery all rejected the orphan attempt.  Manual tree
  editing was the only continuation.
- Because the campaign requires every computation to restart safely after an
  interruption, this narrower gap was treated as a decisive rejection even
  though it could not forge a claim.  Again no real solver or checker ran.

### 2026-07-26 11:05 — final runner accepted; parameter-five reduction accepted

- Final runner revision v3 adds non-destructive opaque recovery.  Explicit
  recovery recognizes only one exact next-numbered real attempt directory
  when the previous state is runnable, moves the entire untrusted directory
  intact into an exclusive sibling quarantine, launches no child, and leaves
  the run auditable for a fresh attempt with the correct number.  Partial or
  complete uncheckpointed outcome bytes receive the same opaque treatment and
  are replaced by a canonical recovered nonclaim.
- The independent v3 referee injected all four pre-`RUN_STARTED` crashes,
  partial and success-shaped outcomes, seven crashes during quarantine, six
  malformed structural envelopes, all six original metadata attacks, and all
  four adjacent producer/consumer mutations.  Every unsafe case rejected or
  recovered as a retryable nonclaim; a success-shaped uncheckpointed outcome
  was never promoted.  The 22-test read-only suite passed.
- Root independently reran the final v3 evidence generator.  Its output was
  byte-identical with SHA-256
  `7e86ee0692125e6782e4a9e7c5ff673f6a0dc92bdb73cae52aa7f8329b75a23f`,
  and root separately reproduced all 22 read-only tests.  Verdict:
  `ACCEPT_FINAL_V3_PRODUCTION_RUNNER`.  This authorizes bounded production;
  it is not a template UNSAT result, and the review launched no real solver or
  proof checker.
- The independent parameter-five lane also closed.  Relative to C-050,
  C-048, and C-051, every order-13 parameter-five counterexample has a
  degree-two root, a ten-vertex equality kernel, two bounded attachment masks,
  and a parameter-three common-nonneighbor kernel.  Exact clique insertion,
  707 domination tests, full independent-anchor projections, and forced-state
  response filters were proved.  The strongest new pruning is
  \(|A|=|B|=6\Rightarrow A=B\), with
  \(R\cong K_2+2K_1\).  Two hostile replays accepted the final bytes as C-056.
- C-056 is a structural reduction and coverage design only.  No canonical
  ten-vertex kernel enumeration was executed, so the \((13,5)\) slice remains
  open.  No novelty or priority claim is made.
- The complete warning-fatal campaign regression then passed 389 of 389 tests
  in 360.213 test seconds and 360.56 wall seconds, with peak RSS
  192,397,312 bytes.  The retained log SHA-256 is
  `97aa30c0c233c0bcb29ddb50ddab157fb0a20a7cb38b2b387b6ac171c3b323ff`;
  the separate JSON binding recomputed the hash, count, and terminal result.

### 2026-07-26 11:19 — exact `hole9` production tree initialized

- The accepted checkpoint was committed and pushed on `main` as
  `20eca759c2b0919366c2355d859e62a0933542dd`.  Staged-scope review found only
  the 73 intended campaign paths; all 55 new manifest hashes reproduced from
  the staged bytes.  Provisional certificates, replay locks, and unrelated
  research remained untracked and outside the commit.
- The dedicated order-13 constructor generated
  `instances/order13_k3_hole9` from fresh bytes.  Its exhaustive
  reconstruction reports 9,802 variables, 32,108 clauses, 281,028 literals,
  and 2,295 complete coloring-obstruction rows.  Formula SHA-256
  `3fff100cbfe66b422f9148fda66b6d1ccf6060a4ffbcdb37a54bde415e95e9ea`,
  coloring-bank SHA-256
  `a0f47a0aaa3be4659ce483f27a963d351f3a13424cac6a6a99ef6ac9e0c872f1`,
  and constructor-manifest SHA-256
  `8f55019121df7280368528c1b7c0808d3cc06e7bd0f871be516057763c87ad5b`
  exactly match the previously accepted independent-constructor evidence.
- A fresh clean `git archive` of exact commit `20eca759` independently
  reconstructed the package in private storage and compared all three live
  files byte-for-byte.  The package-set binding is
  `ba05d99b67816c1f1eeac2569b694ec1fc4412a584e95f359452bdfe12eaad6a`;
  verdict `ACCEPT_LIVE_HOLE9_PACKAGE_PREFLIGHT`.  Root reproduced the
  retained read-only audit output exactly.
- The final-v3 runner initialized
  `results/order13_k3_hole9_production` exclusively and launched no child.
  Run manifest SHA-256 is
  `40fe9e77e4da79e8b70f3d3f836d3a595e1d3b8bae25c4c607a2e1f63dc4be54`;
  checkpoint-zero SHA-256 is
  `106afa51de8197303dbd762a4d234dd0a5bb32b687bb5d655848687f5027358e`.
  Its read-only structural audit returns `accepted=true`, `status=PENDING`,
  and `attempt_count=0`.
- The frozen limits are seed 0; one child; 1,800 seconds for the solver and
  every postprocessing child; 2,048 MiB child memory; 1,024 MiB per output
  file; 8,192 MiB disk reserve; 2,048 MiB reclaimable-memory reserve; and
  load ceiling 7.5.  The reduced file ceiling preserves the 8-GiB safety
  reserve on the 96%-used local volume.  No SAT, UNSAT, or finite exclusion
  is claimed at initialization.

### 2026-07-26 11:42 — first `hole9` attempt fails closed; LRAT candidate recovered

- The prelaunch checkpoint was committed and pushed as
  `a3af5a7de4d32f8421011334b6f2e013fea8d2d5`.  An immediate source, package,
  tool, load, disk, memory, and lock check passed, and the runner durably wrote
  `RUN_STARTED` before launching its only child.
- CaDiCaL returned exit 20 in 0.999 seconds with 0.943 user CPU seconds,
  0.014 system CPU seconds, and 24,920,064 bytes maximum RSS.  The strict
  result is `s UNSATISFIABLE`; the retained 1,900,168-byte binary proof has
  SHA-256
  `ecfb35ba56b5ce2a04437f381e357525581f3bcb6403290272984700d805dbeb`.
  These facts alone remain an observation.
- The raw forward checker then returned exit 80 in 0.124 seconds.  The
  orchestrator durably recorded
  `RETRYABLE_NONCLAIM` / `RAW_FORWARD_REJECTED_NONCLAIM`, outcome SHA-256
  `aa943916e4bb3e46cc2dd2d00f0593f959ad52e45c14202c497f968cd0ab915f`,
  and terminal checkpoint SHA-256
  `be3aa0a50f31a61ba7655c5795f21b4e88468eacd348183ada2f2a6e38c368d4`.
  A read-only final-v3 audit accepts the exact nonclaim tree.
- Two independent read-only diagnoses found the same cause.  drat-trim's
  `-W` option maps any warning to exit 80.  Immediately after adding unit
  `-954`, the proof asks to delete a clause used as its current propagation
  reason; drat-trim deliberately ignores that pseudo-unit deletion, then
  aborts solely because warnings are fatal.  A complete verbose replay found
  2,604 warnings, all this exact class, zero failed additions or other
  warnings, and otherwise verified the proof.
- In a private fresh directory, the accepted strict normalizer consumed the
  entire canonical stream: 117,926 records, 45,281 additions total (45,280
  nonempty plus one final empty), 72,645 deletions, maximum variable 9,802,
  and no later record.  The exact additions-only output is 742,337 bytes with
  SHA-256
  `af216ef2d7698db2b1d1c55411bc05025bfe25f10c16f2e85c5301f7a88bdd5f`.
- A new warning-fatal forward process checked that output with `-U` and
  returned `s VERIFIED`; its core used zero RAT lemmas.  A separate backward
  RUP-only conversion returned `s VERIFIED` and produced an 8,546,664-byte
  LRAT file with SHA-256
  `f6ef614f2acee4cf43aa3b75372b354912c50248a13c3f863479cdc49b061805`.
  The separately compiled pinned lrat-check then returned exact
  `c VERIFIED` with empty stderr.
- These bytes are copied into
  `certificates/order13_k3_hole9_attempt000001_lrat` with a candidate-only
  manifest.  The original attempt remains untouched and remains a nonclaim.
  An independently written standalone verifier and hostile mathematical
  coverage review are mandatory before promoting exact-formula UNSAT to a
  certified `hole9` template exclusion.
- The narrow prospective runner repair is a deletion-agnostic first replay:
  `drat-trim instance raw -i -f -p -W -U -t 1800`.  It checks all additions
  as warning-fatal RUP while ignoring deletion hints, and the exact retained
  proof passes.  The existing strict normalization, second RUP replay, LRAT
  conversion, and lrat-check remain unchanged.  Focused tests pass 24/24,
  but the repair is unaccepted until the v4 hostile regression completes.

### 2026-07-26 12:05 — verifier B and runner v4 independently accepted

- A structurally separate 39,193-byte verifier B was written without
  importing the constructor, search, runner, normalizer, or candidate-manifest
  logic.  It independently parses the exact DIMACS and binary RUP stream,
  checks byte equality with the accepted constructor formula, copies both
  proofs and proof checkers into a fresh private directory, and requires
  strict warning-clean RUP and LRAT transcript grammars.
- The retained evidence is deterministic at SHA-256
  `3de45d16b906e52c3960e4b2e75604908c8cacf356b84d7337db721f4fa49af8`.
  It rejects 24/24 deliberate corruptions, including formula and proof bit
  flips, binary encoding errors, deletions, early or post-empty records,
  checker changes, a RAT core, and mathematical-source or constructor-review
  changes.  Root reproduced the complete evidence and all seven focused
  tests.
- An external exact-byte code audit independently rebuilt `drat-trim` and
  `lrat-check` from the retained C sources.  The fresh executables are
  byte-identical to the decisive retained binaries and both proofs verify.
  The audit found that an initial supporting source-provenance JSON had two
  stale clean-build hashes.  The exact rebuild values were corrected to
  `31df522b...` and `5d7d77a5...`; formula, proofs, decisive binaries, and
  successful proof checks were unchanged.  Final verdict:
  `ACCEPT_WITH_CAVEATS_NO_SOUNDNESS_BLOCKER`.
- The independent production referee accepted v4.  Its formal
  deletion-agnostic RUP argument is that every retained addition follows from
  the original formula plus previous retained additions, so discarding
  deletions preserves the model set inductively.  The exact attempt-one raw
  proof passes; all inherited provenance, crash, quarantine, and
  producer/consumer mutations remain rejected.  Referee and root each
  reproduced 25/25 tests.  This accepts future runner bytes only; the v3
  attempt remains its original nonclaim.

### 2026-07-26 12:18 — C-057 mathematical implication accepted

- A clean-room mathematical audit reconstructed all 9,802 variables and
  every clause family of the exact `hole9` formula.  Its ordered DIMACS bytes
  exactly equal the certified formula, so no signature sort, reflection,
  DoubleLex, unrelated anchor, or other unsafe graph symmetry is hidden in
  the instance.
- The audit enumerated all \(3^{13}=1,594,323\) named colorings.  Exactly
  13,770 respect the forced template edges, and quotienting the free
  six-element color-name action gives exactly the retained 2,295
  first-use-canonical rows.  Thus the non-three-colorability bank is
  complete and imposes no vertex symmetry.
- It separately rechecked the complement signs, external pair witnesses,
  connected-cut encoding, domination clauses, attacks only on unoccupied
  vertices, exactly one guard traversing one \(G\)-edge, and successor-family
  closure.  The named triangle \(\{0,1,9\}\) follows from the chosen rim edge
  and a guaranteed external common neighbor; it is a relabeling, not an
  automorphism assumption.
- Verdict:
  `ACCEPT_EXACT_HOLE9_TEMPLATE_EXCLUSION_AND_C5_C7_REDUCTION`.
  Relative to C-050 and C-055, no order-13 parameter-three counterexample has
  a hub-free induced complement \(C_9\).  Combining this with C-053 leaves
  only the overlapping `hole5` and `hole7` branches.  No complete
  parameter-three, order-13, lower-bound-14, or universal claim follows.

### 2026-07-26 12:37 — C-057 promotion wrapper and release regression accepted

- The immutable candidate manifest remains
  `CANDIDATE_PENDING_INDEPENDENT_HOSTILE_AUDIT`; the original production
  outcome remains `RETRYABLE_NONCLAIM` and
  `RAW_FORWARD_REJECTED_NONCLAIM`.  A new 8,249-byte acceptance record,
  SHA-256
  `f9ee1ce8657206a23353f52cc64210fb015149f12fdb3f7eeeac11a6948c32b7`,
  is the sole promotion to C-057.
- The one-command C-057 replay checks 25 distinct exact artifact paths, runs
  verifier B, rebuilds and replays both proof checkers through the external
  audit, reconstructs the formula and coloring bank through the mathematical
  audit, and explicitly reports that no SAT solver ran.  Root reproduced its
  terminal verdict
  `VERIFIED_C057_HOLE9_TEMPLATE_EXCLUSION_BINDINGS_AND_PROOFS`.
- A separate wrapper audit used descriptor-stable reads in private mutation
  copies and rejected 13/13 attacks: acceptance and artifact bit flips,
  scope overclaim, duplicate/nonfinite JSON, candidate and production-status
  rewrites, symlink substitution, and coordinated acceptance/artifact or
  acceptance/wrapper changes.  Verdict:
  `ACCEPT_EXACT_C057_ACCEPTANCE_WRAPPER`.  Its three caveats—loaded-code
  self-authentication, static-path races under a concurrent local attacker,
  and inherited Python environment—are nonblocking under the campaign's
  quiescent single-user replay model; isolated minimal-environment replay
  also passes.
- The complete warning-fatal release regression passed 398/398 tests in
  375.163 test seconds and 375.48 wall seconds.  Maximum RSS was 189,136,896
  bytes and the 61,124-byte log SHA-256 is
  `2e7f27c39d91f12b8196db7a26a2d1ac6d7e92ab19ade30d76e4ca2bf5e375bd`.
  No campaign worker remains active.

### 2026-07-26 13:17 — `hole7` frozen; order-12 release and universal-proof pivot

- The exact order-13 parameter-three `hole7` package was generated from
  accepted C-055 sources but deliberately not given to a SAT solver.  Its
  1,372,338-byte formula has 9,802 variables, 34,903 clauses, 349,248
  literal occurrences, and SHA-256
  `3e1c86ccbcfc1e04b3ec4de29ec5b7d342cf909553655f959b1c35de0a36c340`.
  The complete 5,103-row coloring bank has SHA-256
  `efafa89d6096d81bc0ae5a1860be4d0ce69b56f4e4957c8bd307316c121e692d`.
- An independent preflight reconstructed the package once from clean
  committed constructor bytes and once with a separate clean-room
  constructor.  Both matched exactly.  It bound the C-055 mathematics,
  re-enumerated the coloring bank, checked the strict DIMACS census and
  rejected ten package/source/symlink/hardlink mutations.  Verdict:
  `ACCEPT_EXACT_HOLE7_PACKAGE_PREFLIGHT`.  This is input integrity, not an
  UNSAT result or mathematical exclusion.
- The order-12 frontier manuscript was converted from its accepted
  presubmission state to a public edition.  The sole author is Alec Kriebel;
  the exact release and human-readable project URLs replace the two
  placeholders.  Two fresh Tectonic 0.16.9 builds are byte-identical.  The
  17-page PDF is 130,163 bytes with SHA-256
  `b35d4bd795ddfbfa61be18bdd60ddb6d23492b0a63a7449e2ec0190170e6e9d2`.
  Every page was rendered and inspected, including the revised title and
  data-availability page.  The embedded author, title, subject, and keyword
  metadata were then checked explicitly; all 17 final rendered page images
  remained pixel-identical to the inspected layout.
- Fresh C-050 full-LRAT and C-057 RUP/LRAT/coverage replays both passed,
  invoking no SAT solver.  The public research page and paper page were then
  prepared as static GitHub Pages artifacts.  Local serving returned exact
  source bytes for the home page, both new pages, the PDF, and CSS; all local
  links and IDs and both JSON-LD blocks passed, and the sitemap is valid XML.
  Public commit, tag, release, Pages build, and live-byte verification remain
  gated on independent final audits.
- Portfolio decision: no solver launch follows the successful preflight.
  Before proceeding to order 14, the campaign gives primary effort to a
  universal minimum-counterexample argument centered on the C-051 projection,
  exact eternal-family transitions, and private-neighborhood structure.
  Order-13 synthesis remains a bounded fallback and a source of
  counterexamples to proposed lemmas.

### 2026-07-26 13:51 — final release-byte and site audits accepted

- The independent final manuscript audit reproduced two clean deterministic
  Tectonic builds, the warning-free logs, the 17-page rendering inspection,
  Alec Kriebel metadata, exact public-PDF equality, and the restricted
  source diff from the accepted presubmission manuscript. Verdict:
  `ACCEPT_RELEASE_BYTES_CONDITIONAL_ONLY_ON_ATOMIC_TAG_PUSH`.
- The independent final public-site audit strictly parsed both JSON-LD
  documents and the XML sitemap, checked all local references and fragments,
  found no duplicate IDs or unexpected package entry, and accepted the exact
  one-guard model, clique-cover notation, authorship, and conditional claim
  scope. Verdict:
  `ACCEPT_SITE_BYTES_CONDITIONAL_ONLY_ON_ATOMIC_TAG_PUSH`.
- Both retained audit scripts now have a post-publication mode that verifies
  the accepted bytes directly from the annotated release tag. The sole
  remaining publication condition is an atomic push of the release commit
  and `gamma-theta-order12-frontier-v1.0.0`, followed by live Pages and
  release-asset byte verification.
- The `hole7` preflight was made durable across documentation-only branch-tip
  changes: its checker continues to bind constructor and C-055 source bytes
  to frozen baseline commit
  `b9b74a38415dac6ef11bb7cbc55badf224affadd`, while still rejecting any live
  source, accepted-chain, formula, bank, or manifest drift. The deterministic
  preflight replay passes after this correction; no solver or proof checker
  ran.

### 2026-07-26 14:08 — order-12 frontier publicly released and live-verified

- A concurrent cyclic-Bell publication moved `origin/main` four commits
  during the final audit. The accepted gamma-theta commit was first frozen
  locally, then rebased onto that remote tip. The only conflicts were the
  repository README, Pages homepage, and sitemap; the resolution preserved
  both publications, raised the visible current-paper count to eight, and
  produced 19 unique sitemap locations.
- The independent site auditor rechecked the integrated bytes, including both
  paper cards and both new publication packages, and again returned
  `ACCEPT_SITE_BYTES_CONDITIONAL_ONLY_ON_ATOMIC_TAG_PUSH`. All decisive
  C-050, C-057, `hole7` preflight, manuscript, site, XML, and byte-equality
  replays then passed on rebased commit
  `16dd2a7803d21fda02fa28e26561d652b7f3b595`.
- The annotated tag
  `gamma-theta-order12-frontier-v1.0.0` was created only after those checks.
  Both release audits verified the exact tagged tree and promoted their local
  verdicts to `ACCEPT_RELEASE_BYTES_TAG_BOUND` and
  `ACCEPT_SITE_BYTES_TAG_BOUND`. Commit and tag were pushed atomically.
- The public GitHub release was published at `2026-07-26T21:04:57Z` with the
  exact PDF and checksum assets. Their server-reported and downloaded
  SHA-256 values are
  `b35d4bd795ddfbfa61be18bdd60ddb6d23492b0a63a7449e2ec0190170e6e9d2`
  and
  `184df74e9e4d5dc3165ef807fde9f1fa35831b2c0aad325397fea1d40c74faeb`.
- GitHub Pages build `1116371323` completed from the tagged commit with no
  error. Fresh HTTPS downloads of the homepage, workstream page, paper page,
  PDF, checksum file, sitemap, and release PDF all matched the accepted local
  bytes exactly. Verdict:
  `ACCEPT_PUBLIC_ORDER12_FRONTIER_RELEASE_AND_LIVE_BYTES`.
- The finite result remains conditional on the published through-order-11
  premise and does not resolve the universal conjecture. With publication
  complete, the campaign now executes the proof-first pivot before any
  order-14 work.

### 2026-07-26 15:02 — first universal-proof portfolio gate

- Three independent proof attacks reached their declared two-iteration
  gates.  None resolved the universal conjecture, but all produced concrete
  definition-level mathematics and explicit counterexamples to tempting
  shortcuts.
- The transition/private-neighborhood lane proved a restoration lemma and
  the viable-list Hall theorem: relative to an independent eternal
  \(k\)-state \(S\), every independent outside set \(X\) satisfies
  \[
    \left|\bigcup_{x\in X}L_S(x)\right|\geq |X|.
  \]
  It also proved the exact equivalence between a \(k\)-clique partition and
  a compatible viable-list clique-fiber coloring.  A separate hostile proof
  review returned `ACCEPT_MATHEMATICS`.  The ordinary-set replay through
  order nine reproduced 3,585 equality graphs, 37,358 reference states, and
  zero Hall violations.  Root accidentally rewrote the evidence's
  nondeterministic elapsed-time field by replaying to its default path; the
  mathematical payload remained identical, and the official log was rebound
  to the resulting frozen JSON SHA-256
  `771738d7f2d3b0f384c2276f4ac4bb7fc1da18c285f169f7c606184539f09841`.
- The complement/private-block lane independently found the same Hall
  mechanism and then sharpened it.  Private blocks are cliques, shared
  vertices carry exact family-response lists, collision transfer prevents an
  edge conflict from being trapped between two identical singleton lists,
  and any counterexample has a connected minimal uncolorable response-list
  core with degree, leaf, clique-Hall, and collision restrictions.  For the
  greatest eternal family, colorability of this core is equivalent to the
  desired clique partition.  The clean-room hostile audit returned `ACCEPT`
  and reproduced 6,605 Hall and 312 collision obligations.
- The local-balance/holonomy referee constructed an infinite stress-test
  family.  For every simple triangle-free cubic class-II graph \(F\), all
  dominating triples of \(\overline{L(F)}\) form a one-guard eternal family,
  yet
  \[
    \gamma=2<i=\alpha=\gamma^\infty=3<\theta=4.
  \]
  A diameter-two classification shows that the only cubic host in this
  family with \(\gamma=3\) is \(K_{3,3}\), which has no coloring gap.
  Independent proof and evaluator reviews accepted the result.  The sole
  typographical defect was corrected and the review rebound to note SHA-256
  `382f7af69da1f0d2c81faaa4fe0569c6b3c54529580b3ddb001fe0850664b198`.
- The proof lanes also refuted raw response territories being cliques,
  physical guard-label invariance, simple connectivity of the complement
  clique complex, and facet-only path independence.  The exact remaining
  obstruction is global compatibility across overlapping response-list
  cliques.  Treating that compatibility as an assumption would simply rename
  the original conjecture, so the general lanes stop there.
- A structured follow-up checked the 27-vertex Schläfli graph, whose
  complement is the point graph of \(GQ(2,4)\).  Preliminary exact data give
  the static near-miss \(\gamma=i=\alpha=3<\theta=6\), with 1,125 dominating
  triples, 45 secure line triples, and an empty second kernel.  A separate
  bounded audit is preparing the human two-attack obstruction.  Until that
  artifact is accepted, this remains `OBSERVED` and is not promoted to the
  claim registry.
- No SAT solver, proof-production runner, order-13 synthesis job, or
  order-14 computation ran during this proof interval.

### 2026-07-26 15:22 — Schläfli stress test accepted and proof-first gate frozen

- The bounded \(GQ(2,4)\) lane reconstructed the 27-vertex Schläfli graph
  \(G\) from the 27-line intersection graph
  \(H=\operatorname{srg}(27,10,1,5)\).
- A self-contained proof gives
  \(\gamma(G)=i(G)=\alpha(G)=3\).  It classifies the 1,125 dominating
  triples as the 45 \(H\)-triangles and 1,080 induced \(H\)-paths.  Every
  path has four immediately lethal attacks, while every legal dominating
  response from a triangle is a path.  Therefore every three-guard strategy
  loses within two attacks and \(\gamma^\infty(G)>3\).
- Independent bit-mask and ordinary-set implementations reproduced the
  synchronous kernel sizes \(1125\to45\to0\).  Their frozen outputs have
  SHA-256 values
  `d50d01db88689bee6ef42e30ca3ad8062031813eabe19a551a2d1f5859de4cc5`
  and
  `7c1af42d52293409158543809799ce62f1885cf587bad12ebf6b605b1853ff34`.
- Two independent complete coloring searches give
  \(\theta(G)=6\): an 8,003-node DSATUR rejection of five colors and a
  separate stable-set coverage proof over 72 stable six-sets and 756
  disjoint pairs.  Because no SAT proof log is supplied, the exact finite
  coloring result is registered as `CERTIFIED-FINITE`, separately from the
  human two-attack theorem.
- The accepted result is a high-value near-miss diagnosis, not a
  counterexample: it meets every static equality and has a large
  clique-cover gap, but fails precisely at the one-guard eternal equality.
- A disposable stdin prototype accidentally called a brute-force
  order-27 independence routine and remained CPU-bound after a blank yielded
  cell.  Root found and terminated PID `33724` after about 57 minutes.  The
  process produced no accepted artifact; the frozen replacements each finish
  in under one second, and a final process scan was clean.
- The literature ledger now records targeted no-match searches for the
  restoration/Hall theorem, the cubic line-graph-complement family, and the
  Schläfli two-attack result.  These do not establish novelty or priority.
- Claims C-061 and C-062, the acceptance binding, state, and manuscript
  registry were updated.  Order 14 remains unstarted; the universal
  shared-response-core lane stays primary.
- The bounded \(k=3\) static-list follow-up reached its stop gate.  Applying
  the classical degree-choosability/Gallai-tree structure to a minimal
  uncolorable core shows that tight blocks are cliques or odd cycles; in the
  entirely tight 2-connected case, clique-Hall excludes the triangle and the
  remaining obstruction is an odd cycle with a common two-color list.
  High-degree and cut-block cores remain, and local closure did not eliminate
  the odd cycle.  No new claim is promoted from this observation: another
  single-reference static-list iteration would be equivalent to the original
  global coloring obstruction.  The next universal route must compare lists
  across different maximum independent states or introduce a genuinely
  dynamic invariant.

### 2026-07-26 15:34 — proof-pivot package and live workstream update released

- The accepted C-058--C-062 package was committed, rebased over two
  unrelated concurrent `main` commits, replayed, and pushed as
  `7a0c926ef7ef7d0dab8cb8aabcdbd7a8d4e2494d`.
- GitHub Pages run `30223360034` completed successfully.  A cache-busted
  HTTPS fetch of the active gamma-theta workstream page is byte-identical to
  `docs/research/gamma-theta-conjecture/index.html`, with SHA-256
  `cad4d253d6196b994416d229753a481ac6132db69043be321e4b486f98849717`.
- The live page gives Alec Kriebel's attribution, the exact unoccupied-attack
  one-guard model, the order-12 finite frontier, the restoration/Hall and
  shared-response-core progress, the line-graph and Schläfli stress tests,
  and the explicit unresolved boundary.
- The already tagged order-12 frontier paper remains the only current paper.
  No second paper was issued from the proof-pivot results at this stage.
- Exact deployment and live-byte evidence are frozen in
  `results/proof_pivot_public_workstream_acceptance.json`.

### 2026-07-26 16:31 — frozen-color induction and cross-state exchange gate

- The cross-state lane proved that any two independent \(k\)-states in the
  same eternal family admit a retained monotone path for every ordering of
  the target positions.  If two states share \(k-1\) vertices, transposing
  the exchanged positions transports the complete family-response incidence
  system exactly.  A closed ridge path therefore induces an automorphism of
  that incidence relation, not necessarily the identity.
- The strongest new mechanism is the frozen-color projection.  Fixing an
  independent family state \(S\) and one position \(u\), retain the other
  anchors and the attacks whose family or static response lists omit \(u\).
  The states which keep \(u\) occupied project to a literal eternal
  \((k-1)\)-family on the retained induced graph.  If
  \(\gamma(G)=\gamma^\infty(G)=k\), then the projected graph satisfies
  \[
    \gamma=\alpha=\gamma^\infty=k-1.
  \]
  Thus the conjecture has an exact parameter-induction interface.
- At \(k=3\), the already accepted parameter-two theorem applies
  unconditionally to every frozen projection.  Each corresponding
  complement is bipartite, which eliminates an odd response-core cycle
  whose lists share one omitted color.  In particular, the formerly live
  tight common-two-list odd-cycle branch of C-059 is now closed.
- An independent hostile review re-derived every one-guard obligation and
  returned `ACCEPT` after one important scope correction.  On `FCZbg`, the
  frozen family has four states while the greatest projected family has six.
  Therefore a lower-parameter family state cannot automatically be lifted
  into the original family-response lists.  The static clique-partition lift
  remains valid.
- The residual obstruction is sharply delimited by the abstract complement
  path with lists
  \(\{a\},\{a,c\},\{b,c\},\{b\}\).  It is minimally uncolorable although
  every missing-color projection is colorable.  The exact graph `FDzro`
  realizes those lists in a proper 21-state one-guard eternal family and has
  \(\gamma=2<\alpha=\gamma^\infty=\theta=3\).  Thus restoration, tight
  states, co-state closure, and ridge covariance do not eliminate the
  pattern without using \(\gamma=3\).  In an equality realization, the
  middle pair forces an external clique \(W\) of maximum-independent family
  states with unique moves and exact ridge covariance.  A lightweight
  exhaustive probe over all connected unlabeled graphs through order nine
  found no realization in a **greatest** eternal equality family.  This is
  evidence, not a finite theorem about all orders or a statement about every
  proper subfamily.
- Two falsifiers stopped stronger exchange claims.  The smallest abstract
  non-base-orderable expansion/restoration system has rank three and twelve
  states; it is realized as a genuine eternal family on \(K_{3,3}\) minus an
  edge, but there \(\gamma=2<\alpha=3\).  The exact equality graph `FCXfO`
  refutes pairwise reciprocity in an arbitrary eternal family, although its
  displayed family still has a base ordering.  Existence of some base
  ordering under equality remains open.
- Root replayed the through-order-eight cross-state and frozen-color probes
  from frozen sources into fresh temporary directories.  After removing
  only nondeterministic resource metadata, the normalized result hashes were
  respectively
  `b37e94d86f0ad4755a1dff4e6edf2f3f9b46bc23ca94fd212d0faa849d70653a`
  and
  `0c792c200c319c1c23ed8a314076ba4de066416185cf1fa2c6b5571fb7230b4c`.
- No order-14 work, SAT production, or memory-heavy job ran.  The laptop has
  approximately 19 GiB free, so the proof lane remains preferable both
  mathematically and operationally.
- The final cross-state hostile review returned clean `ACCEPT` after
  re-deriving the endpoint-reversal duality, checking 100 displayed
  state/attack obligations, and independently exhausting all 5,653 valid
  labeled rank-three abstract systems.  A separate mixed-path audit checked
  all 84 obligations of the `FDzro` family and caught the proper-versus-
  greatest-family scope distinction before acceptance.
- The full campaign regression suite passed all 398 tests in 373.148
  seconds.  The claim boundary and exact artifact hashes are frozen in
  `results/cross_state_proof_acceptance.json`.

### 2026-07-26 16:57 — cross-state proof package and public page released

- The independently accepted C-063--C-068 package was committed and pushed
  to `main` as `224af249d423419a887e737e6941b58f512c82a4`.
- GitHub Pages run `30226281225` completed successfully.  The cache-busted
  live active-workstream page is byte-identical to the committed source,
  SHA-256
  `0254ec939c9359dee80bf0db321ea4ce3781a7cd1993c74d5c98ab2beccee209`.
- The public page preserves Alec Kriebel's authorship and research
  leadership, the exact one-guard definition, the existing order-12
  frontier, and the explicit statement that the universal conjecture is
  unresolved.  It now records the frozen-color induction, cross-state
  covariance, the proper-family `FDzro` falsifier, and the equality-only
  external witness clique.
- The order-12 frontier paper remains the only current paper.  These
  universal structural lemmas are public research artifacts but are not yet
  issued as a second manuscript.
- Deployment and live-byte evidence are frozen in
  `results/cross_state_public_workstream_acceptance.json`.

### 2026-07-26 18:00 — exact 2-SAT gluing and forced-\(C_5\) proof gate

- The three frozen-color projections at \(k=3\) were glued exactly.  When
  every family-response list has size one or two, choosing the orientation
  of each non-anchor bipartite component is equivalent to solving a
  specifically constructed 2-CNF formula.  Singleton lists impose parity
  units, while complement edges between distinct two-lists impose the
  clauses that forbid their shared-color collision.  Satisfiability is
  equivalent to a compatible anchored coloring of the complement, hence to
  the desired three-clique partition.
- The mixed response-list path
  \(\{a\},\{a,c\},\{b,c\},\{b\}\) is the smallest obstruction of the form
  two forced orientations plus one conflicting clause.  Successful
  colorings transport across independent-state ridges with their unlabelled
  clique partition literally unchanged.  The exact gamma-two families
  `FDzro` and `HDzruf]` show that full closure and two witness layers do not
  force the formula satisfiable; neither contains a nontrivial independent
  ridge pair, so they do not nonvacuously test covariance on an
  unsatisfiable instance.  Full-list vertices are invisible to the three
  projections and remain a separate obstruction.
- A second analytic pass used the missing equality \(\gamma=3\) directly.
  For every middle-pair witness \(w\), both endpoint colors occur in its
  response list and \(w\) sees both path ends.  The middle color also sees
  both ends.  Three forced family states then share the end ridge
  \(\{x_0,x_3\}\).  Since that pair cannot dominate, its common complement
  neighborhood \(Z\) is a nonempty external clique; unique one-guard
  responses force every \(z\in Z\) to close
  \(x_0x_1x_2x_3\) to an induced complement \(C_5\).  The accepted
  odd-wheel theorem makes each such \(C_5\) hub-free.  Each original witness
  also forces a second external co-state clique \(Y_w\).
- Independent hostile reviews accepted both proofs.  The projection review
  checked all 46,656 three-outside-vertex abstract list systems, with exact
  direct-coloring agreement on all 40,113 systems whose frozen projections
  are bipartite.  It also replayed every named graph and family.  The
  mixed-witness review independently checked the nine-vertex gamma-two
  diagnostic `HFzvvf]`, its parameters, 55 retained states, all 330
  unoccupied attack obligations, and the exact response lists.
- A complementary exact synthesis enumerated all 2,048 and 524,288 labelled
  completions of the distinguished order-eight and order-nine templates.
  Among 62 and 8,985 graphs with \(\gamma=\alpha=3\), respectively, none
  admits an arbitrary proper eternal family with the prescribed six positive
  and six negative direct swaps.  A clean-room implementation reproduced
  every count, mask digest, checkpoint field, fixed-point profile, and
  bounded base-orderability CEGAR result.  This is C-071 `OBSERVED`, not an
  order-nine frontier theorem or a higher-order exclusion.
- The hostile synthesis review found two wording defects: a completed resume
  changes only the regenerated `completed_at` field rather than reproducing
  byte-identical JSON, and the zero banned-state-kernel count applies only
  inside the \(\gamma=\alpha=3\) frontier.  Both were corrected; the reviewer
  rebound the new hashes and returned an unconditional pass.
- A provisional fixed 10-vertex cap extension count was rejected rather than
  promoted.  The independent reconstruction verified the cap itself but
  exposed that the 239-type exploratory count had no frozen admissibility
  predicate.  Filtering against the entire 75-state cap kernel would be
  unsoundly strong for an arbitrary specified family.  No order-13 result is
  claimed from this lane.
- Order 14 remains unstarted.  The universal proof lane now targets the
  compatibility of an inconsistent 2-SAT bicycle with its forced hub-free
  \(C_5\) and \(W,Y_w,Z\) witness systems, plus the separate full-list slice.

### 2026-07-26 18:05 — mixed-core package and public workstream released

- Claims C-069--C-071, their independent reviews, exact evidence, failed-cap
  boundary, claim registry, checkpoint, and active-workstream update were
  committed and pushed to `main` as
  `edc9c248baa08fd999dc8318b10ad58ab95d09eb`.
- GitHub Pages run `30228901346` completed successfully.  A cache-busted
  HTTPS fetch of the active gamma-theta page is byte-identical to the
  committed source, SHA-256
  `55e39483236d6d9fb6dd0babdbecd7735f8ecaa3667416aef470e274b76e02ae`.
- The live page identifies Alec Kriebel as author and research lead,
  discloses heavy AI assistance, preserves the exact unoccupied-attack
  one-guard model, and states prominently that the universal conjecture
  remains unresolved.  It records the exact 2-SAT gluing theorem and forced
  hub-free complement \(C_5\), while labelling the order-eight/order-nine
  proper-family scans as bounded evidence.
- The certified order-12 frontier paper remains the sole current paper.
  These new structural results are public source artifacts, but a second
  manuscript would be premature before they close the \(k=3\) case or form a
  more self-contained class theorem.
- Exact source, deployment, live-byte, attribution, scope, and sole-paper
  evidence is frozen in
  `results/mixed_core_public_workstream_acceptance.json`.  Order 14 remains
  unstarted.

### 2026-07-26 19:35 — mixed-path floor, full-list link, and 2-SAT terminal gate

- A third attack pass on the exact mixed response path forced nonempty
  end-edge common-complement cliques \(P_L,P_R\).  Ridge covariance and
  restoration prove \(P_L\cap P_R=\varnothing\), and a two-ridge transport
  proves that every co-state witness clique \(Y_w\) is disjoint from both.
  Choosing one vertex from each of \(W,Z,P_L,P_R,Y_w\) gives five pairwise
  distinct external witnesses beyond the seven reference/path vertices.
  Thus this exact arbitrary-family equality pattern has order at least 12.
  A hostile reviewer reconstructed every move, covariance permutation,
  restoration exclusion, and the \(7+5\) count and returned `PASS`.
- The separate full-family-list branch is now exact.  Avoiding a vertex in
  the graph and family preserves an eternal triple-family and every other
  response list.  After the full vertices are colored, extension over the
  non-full vertices is precisely the accepted projection-gluing formula with
  added units.  A single full vertex therefore leaves exactly three
  augmented 2-SAT tests.
- A full target forces three nonempty disjoint clique spokes, forced spoke
  states, and a second external clique layer.  Its complement link is
  bipartite without isolates.  Response covariance makes each spoke
  side-pure in every link component; a longer ridge transport proves that
  different spoke types cannot occupy the same side.  Consequently every one
  of the three colors is locally feasible.  The unresolved issue is global
  extension through the residual implication core.
- An independent ordinary-set implementation replayed all 273,193 connected
  unlabeled graphs through order 9.  All nine graph-stream hashes and every
  count match the target scan.  There are 24 static-full incidences inside 15
  equality graphs, zero greatest-family-full incidences, and all 24 bounded
  lists have size one.  This narrow connected-unlabeled predicate is
  `CERTIFIED-FINITE`; it is not a new counterexample frontier.
- The order-12 positive control with canonical graph6
  `K{eYptMJynEn` independently has
  \((\gamma,\alpha,\gamma^\infty,\theta)=(3,3,3,3)\), all 127 dominating
  triples in its greatest eternal family, 1,143 obligations, one genuine full
  response list, and exactly one compatible anchored coloring.  It refutes
  every proposed universal no-full-list shortcut while showing the local
  link theorem on the positive side.
- Inclusion-minimal unsatisfiable 2-CNF formulas were classified into a
  two-unit chain, one-unit lollipop, or unit-free opposite-path bicycle.
  Projection implication paths expand into alternating complement edges and
  parity-prescribed frozen-component connectors.  Full one-guard closure
  excludes the canonical shortest one-unit tail-triangle and canonical
  two-variable bicycle.  A clean-room audit checked all 512 and 256
  unspecified-edge completions, respectively, with zero surviving exact
  safe kernels.
- The graph `GFznc{` supplies the exact gamma-two boundary: its 35-state
  family meets all 175 obligations, both ridge-end response formulas are
  unsatisfiable, and covariance is nonvacuous.  Its parameters are
  \((2,3,3,3)\), so it is not a counterexample.  A separate order-exactly-8
  scan was independently reproduced with zero unit-free obstructions in the
  tested slices; that scan remains `OBSERVED`.
- A publication-scope audit recommends a public active-workstream update but
  no second paper.  The order-12 frontier paper remains the sole current
  manuscript.  The page continues to attribute Alec Kriebel as author and
  research lead, disclose heavy AI assistance, state the exact one-guard
  model, and keep both the universal conjecture and order-13 residual slices
  explicitly open.  Order 14 remains unstarted.

### 2026-07-26 19:41 — global-2-SAT localization package released

- Claims C-072--C-077, their three hostile reviews, independent finite
  replays, machine acceptance record, claim registry, checkpoint, and active
  page update were committed and pushed to `main` as
  `018101d4c53cf4a8a3619c3a8b72fadd8f74277b`.
- GitHub Pages run `30232689337` completed successfully.  A cache-busted
  HTTPS fetch of the active workstream is byte-identical to the committed
  page, SHA-256
  `fedda36619dd1fb3878547f1c5df021a312c46d5ed557ee749e76da8c51c0508`.
- The live page retains Alec Kriebel's exact authorship and research-lead
  attribution, heavy-AI disclosure, the standard unoccupied-attack
  one-guard model, and a prominent unresolved-conjecture notice.  It does not
  claim a lower bound of 14, a complete order-13 exclusion, or a universal
  proof.
- The order-12 frontier paper remains the sole current paper.  The new
  structural proof notes are public and independently auditable, but the
  longer global implication connectors remain open, so no second manuscript
  was issued.
- Exact source, deployment, live-byte, attribution, scope, and sole-paper
  evidence is frozen in
  `results/k3_global_2sat_public_workstream_acceptance.json`.  No campaign
  job is running.

### 2026-07-27 21:46 — resumed-report audit and cap-and-escape proof gate

- The pasted external-AI report was treated as an intake lead rather than
  evidence.  No underlying source, graph, solver proof, manifest, or checker
  artifact was found.  Its order-12 narrative is obsolete relative to the
  accepted complete C-050 frontier, and the reported 15-vertex 395-state
  near-miss was identified exactly as the already accepted Petersen member
  of C-060.  The imported half-order conclusion duplicates C-036, while its
  assertion that the complement of a maximum independent set is forced
  independent is invalid as written.  A current resolution refresh found no
  universal proof or certified counterexample.
- A fresh reduction proved that an adjacent true twin can be deleted from
  any equality graph while preserving
  \(\gamma,\alpha,\gamma^\infty,\theta\).  Maximum-independent-state forcing
  guarantees that the restricted eternal family is nonempty.  A hostile
  proof review passed, and an independent scan found zero failures among
  6,279 twin-pair incidences through connected order eight.
- The canonical one-unit lollipop attack tree was extended from its shortest
  edge to every odd vertex-distinct connector inside one omitted-color
  projection when both terminal clauses share one physical complement port.
  The proof allows arbitrary extra complement edges and distinguishes
  missing family membership from graph nonadjacency at every step.
  Independent SAT controls were UNSAT for lengths one, three, and five, with
  the terminal-edge relaxations SAT; the universal theorem rests on the
  symbolic successor exhaustion.
- The single-full branch now has an exact deletion trichotomy, pairwise
  Kempe linkage in the critical deletion, a forced cross-part one-guard
  response for every deletion clique partition, and an augmented-formula
  fork that excludes a newly created unit-free bicycle.  Distinct-spoke
  terminals either dominate the deletion or force a residual
  common-complement-neighbor witness.  A separate hostile review replayed
  the order-12 positive control and accepted every conditional statement.
- Automatic lifting from a logical lollipop to the odd physical fan was
  then refuted exactly.  The graph `HFzvvn{` has a 65-state proper eternal
  family, all 390 one-guard obligations, a satisfiable base formula, and a
  one-unit inclusion-minimal augmented obstruction.  Its terminal clauses
  use separated vertices and no fan embedding exists.  Its parameter tuple
  is \((2,3,3,3)\), so it isolates rather than removes the need for
  domination equality.
- The gamma-three mechanism was proved next.  Every dynamic omitted-color
  connector edge acquires a nonempty \(G\)-clique of complement-triangle
  caps; every cap recovers the omitted response color.  Applying the odd-fan
  theorem at path length one makes each cap \(G\)-complete to all other
  vertices supporting that color.  In the exact separated core this forces
  a new positive residual cap and a further omitted-color link escape.  The
  escape cannot see both connector endpoints without producing a complement
  \(K_4\).  The two forced vertices give an exact-pattern order floor of 11.
  Two independent symbolic reviewers returned `PASS`.
- Three bounded extension universes were independently replayed.  The
  512 one-vertex and 13,824 one-edge local scopes contain 817 exact
  augmentation-sensitive cases, all with a dominating singleton or pair.
  Among all 524,288 induced two-vertex extensions, only six reach the static
  \(\gamma=\alpha=3\) target, and all six have empty eternal triple kernels
  with the anchor state deleted in round two.  These data are C-084
  `OBSERVED`, not a universal theorem or frontier increase.
- A color-restricted safe-kernel probe proved
  \(\theta=3\Rightarrow\) some safe full-target color and selected the unique
  correct color in the order-12 equality control.  The MMV-021 near-miss has
  a surviving safe kernel but no compatible coloring, proving that the
  invariant alone is weaker than the desired conclusion when \(\gamma=3\)
  is absent.
- The day-3 portfolio review rebalanced the campaign toward structural
  proof: approximately 65% proof, 20% exact countermodel synthesis, and 15%
  audit/publication.  The primary target is now finite iteration of the
  cap-and-escape ladder inside the bipartite full-vertex link.  Order 14
  remains unstarted, and the certified order-12 frontier manuscript remains
  the sole current paper.
- Release validation at 22:04 PDT passed all 398 campaign tests with
  warnings fatal in 403.477 seconds.  The 31-artifact acceptance hash audit,
  CSV/JSON parsing, Python syntax parsing, and public-page anchor/JSON-LD
  checks also passed.

## 2026-07-27 22:06 PDT — public Day-3 proof checkpoint verified

- Commit `716f17f557fb820057fdcc627264f1bcee1ffbbb` was rebased cleanly
  over an unrelated concurrent research commit and pushed to `main`.
- GitHub Pages run `30330574121` succeeded.  The cache-bypassed live
  gamma--theta workstream page and committed HTML have identical SHA-256
  `543884bdfc24d66b9ebedf4330b2b57d66d8d9d73f14d8e881118e70671974f5`.
- Live attribution and scope were checked directly: Alec Kriebel is the
  research lead; heavy AI assistance is disclosed; the universal conjecture
  is unresolved; the finite frontier remains 13 relative to the published
  through-order-11 premise; order 14 is unstarted; and the order-12
  manuscript remains the sole current paper.
- Frozen deployment provenance:
  `results/day3_cap_escape_public_workstream_acceptance.json`.

## 2026-07-27 23:32 PDT — full-response squeeze and physical two-list gate

- Three failed colors at one full target were confined to fixed
  inclusion-minimal terminal sets of size at most two.  Their union has at
  most six vertices and every compatible deletion coloring has a rainbow
  transversal.  The terminal cube forces a cross-label response at level two
  or three, while a three-singleton obstruction is impossible.  Independent
  proof review accepted the fixed-core quantifiers and attack cases.
- Kempe connectors were converted into an exact edge-or-hub-free-odd-ear
  alternative.  A separate side-purity theorem confines all positive
  neighbors of one hub in an omitted-color component to one bipartition
  side.  The equality control `GCXfVG` then refuted the proposed shortcut
  that a repeated cap alone must create an odd fan, complement \(K_4\), or
  dominating pair: one cap closes consistently around an even complement
  \(C_4\).
- The exact two-color separated-port ladder was proved to require two
  additional distinct caps.  This first raised its order floor to 13 and
  forced a singleton identification in the tight order-13 case.  A
  109-state gamma-two bow-tie control delimits exactly where domination
  equality enters.
- A 14-clause SAT core exposed a stronger human attack.  At a full response,
  every second-layer witness is adjacent in the complement to exactly one
  anchor; witness layers for distinct anchors are pairwise disjoint; and
  each witness carries both cross-anchor responses.  Three spokes and three
  second-layer witnesses are therefore distinct, proving
  \(|V-(S\cup Q_S)|\ge6\) and raising the exact separated-port floor to 15.
- A bounded order-13 full-response formula was then simplified by jointly
  removing uniqueness of the full target, connectivity, the witness bound,
  and redundant maximum-independent-state clauses.  The remaining exact
  formula has 9,802 variables and 85,409 clauses and is UNSAT.
  `drat-trim` accepted its 19,874,489-byte proof in RUP-only mode.
- A hostile checker independently allocated every variable and reconstructed
  all 85,409 clauses byte for byte.  It truth-tabled all 2,048 adjacent
  signature pairs, proved the \(S_9\) sorter covers every orbit, replayed the
  full proof and reduced core, and checked the SAT ablations.  A
  reproducibility defect in its first result writer—temporary paths and
  timing changed hashes—was caught on root replay.  The reviewer normalized
  all volatile data, added two internal rounds and an external determinism
  manifest, and the corrected artifacts now reproduce byte identically.
  This promotes C-090:

  \[
  \text{no order-13 parameter-three counterexample has a full
  family-response target at a maximum independent triple.}
  \]

  This is a conditional branch exclusion, not a complete order-13 theorem.
- The theta-gap ablation produced the positive equality control
  `LF\|ul\XzVsaqJ`.  Both independent evaluator stacks give
  \((\gamma,\alpha,\gamma^\infty,\theta)=(3,3,3,3)\); all 157 dominating
  triples survive and vertex 3 is the unique full target at the reference
  state.  Thus the certified contradiction genuinely uses
  non-3-colorability of the complement.
- A broader human lemma now converts every neutral two-response vertex into
  a pure two-vertex complement spoke and a physical terminal with the same
  response pair and a genuine omitted-anchor graph nonedge.  Hence every
  exact two-list has a physical representative.  Two possibly equal neutral
  vertices with overlapping response pairs force six nonneutral witnesses,
  proving the exact separated-port \(n\ge15\) floor without using the full
  target.  A clean-room reviewer accepted the proof and independently
  reproduced the 14-vertex static boundary graph
  `MFzvvn{feBKbM{gZ_}` with
  \((\gamma,i,\alpha,\gamma^\infty,\theta)=(3,3,3,4,4)\).
- The exact complementary no-full-list order-13 formula has 9,802 variables
  and 85,413 clauses.  One CaDiCaL run reached the 120-second cap without a
  decision.  No claim is made.  Its 389 MiB incomplete proof stream was
  deleted, while the generator, frozen instance, timeout record, and resume
  command were retained.
- The universal proof target is now narrower: a neutral two-list and its
  physical representative are joined by an even complement path in the same
  omitted-color component, so they represent the same Boolean sign.  What
  remains is to transport or replace the physical cross-list connector
  geometry needed by the one-guard attack, not merely its truth value.

## 2026-07-27 23:57 PDT — sound no-full census and failed edge transport

- The first no-full counting draft was challenged before promotion.  Its
  assertion that every anchor pair forces an outside double-signature
  witness was false because the third anchor already witnesses
  nondomination.  The derived \(|A|\ge7,|Q|\le3\) bound was retracted and
  does not appear in the accepted ledger or public result.
- A corrected human decomposition proves that a non-3-colorable no-full
  response system has at least two exact two-list types.  Each type omitting
  anchor \(i\) forces two distinct pure-\(i\)-signature vertices joined in
  the complement.  A neutral vertex forces complement neighbors covering
  all three anchor signatures.  Therefore an order-13 no-full
  counterexample has \(|A|\ge5,|Q|\le5\), improving to \(6,4\) for three
  types.
- In the tight \(5+5\) case, four nonneutral vertices are the two forced
  pure-signature pairs.  The fifth has a two-anchor signature, is
  complement-adjacent to every neutral vertex, and has the remaining
  singleton response list.  This is C-093, a structural reduction rather
  than an order-13 exclusion.
- Literal physicalization was completed exactly.  Every exact two-list port
  has a same-list representative on the same bipartition side of the
  omitted-color projection; a dynamic omission gives an explicit
  length-two complement path.  The two vertices therefore represent the
  identical Boolean port event (C-094).
- The stronger physical-edge inference is false.  The connected 13-vertex
  equality graph `LFzJbZYhdrDZdM` has an explicit 142-state eternal family,
  \((\gamma,i,\alpha,\gamma^\infty,\theta)=(3,3,3,3,3)\), and no full list.
  A complement cross-edge \(qv\) supports a response clause, but the unique
  same-sign physical representative \(r\) of \(q\) has \(rv\in E(G)\).
  The independent bit-mask reviewer reconstructed the graph, greatest
  three-kernel, all 1,420 family obligations, all 78 pair-nondomination
  witnesses, every response list, projection bipartiteness, and
  representative uniqueness.  This refutes only automatic clause-edge
  transport (C-095), not the gamma--theta conjecture.
- The complete campaign test suite passed 398 of 398 tests in 385.723
  seconds, with peak resident memory 185,417,728 bytes and no swaps.
- The universal conjecture remains unresolved; no counterexample has been
  found, the complete order-13 search is unfinished, and the global
  certificate-backed frontier remains 13.

## 2026-07-28 00:18 PDT — checkpoint 061 public release

- The 66-file, strict-whitelist checkpoint was committed on `main` as
  `8bae62baaa6b1c496c88ef741d6973f5ad824a58` and pushed to `origin/main`.
  The final staging audit excluded every retracted `tight-*`/`six-*`
  no-full formula, every nonexhaustive `a4-*` control, active proof drafts,
  caches, legacy partial certificates, and unrelated workstream files.
- GitHub Pages run `30337777612` completed successfully.  A cache-bypassed
  download of the live active-workstream page is byte-for-byte equal to the
  accepted local page; both have SHA-256
  `f13ecdfd470ab112d3ac1d65084e8c8ae82178227e03c547971673109a445086`.
- The existing order-12 frontier paper remains the sole issued paper.  Its
  live PDF still has SHA-256
  `b35d4bd795ddfbfa61be18bdd60ddb6d23492b0a63a7449e2ec0190170e6e9d2`.
  No second paper was created for the conditional order-13 branch result.
- Frozen deployment provenance:
  `results/day3_full_response_no_full_public_workstream_acceptance.json`.

## 2026-07-28 00:51 PDT — order-13 parameter-three slice certified empty

- The resumed audit of the tight \(5+5\) no-full form produced a much
  smaller obstruction than the original structured formula.  On 13
  vertices, literal one-guard closure, pair nondomination, one independent
  retained triple, four neutral vertices, and two distinct ports carrying
  overlapping positive response pairs are already inconsistent.
- The production formula has 1,222 variables and 24,694 unique clauses.
  Its DIMACS SHA-256 is
  `3d1a1379eb2a90ffd399e5a830b1a81881ed527c6e9db06574a390085cb5c1e0`;
  the 78,697-addition proof SHA-256 is
  `c4f1989ac80474a86b75ba939e494bde5928b2727fd61297eb695f3937222eee`.
  A hostile checker independently reconstructed every byte, exhaustively
  truth-tabled the closure gadget, replayed strict forward RUP, generated
  and checked fresh LRAT, and verified a sharp three-neutral SAT control.
- C-093 gives at least two response types in the no-full theta-gap branch,
  and C-091/C-093 supply distinct nonneutral physical representatives.
  Therefore any candidate with four neutral vertices maps into the small
  formula.  This certifies \(|Q|\le3,|A|\ge7\) at order 13 by a new dynamic
  route.  It does not rehabilitate the earlier false static derivation,
  whose retraction remains part of the record.
- A structured residual formula then named pure-signature pairs for two
  response types, sorted the other six anchor signatures, and encoded
  \(|Q|\le3\) by requiring the fourth residual signature to be nonzero.
  CaDiCaL returned UNSAT in about eleven seconds.  The formula has 9,802
  variables, 84,614 clauses, no duplicates, no tautologies, and SHA-256
  `76ff2768c7afd95ee535f8684515b0b15319b1f5ca69085447a1f7eba66393e1`.
- The decisive deletion-free proof has 156,205 additions, 8,878,465 bytes,
  and SHA-256
  `c985ce0a602a91a0d323594e3aeecf210fa5131027ef4b6c9b6e4d4b628f1848`.
  It passed strict `-I -f -W -U` replay with zero RAT lemmas.  A clean-room
  generator reconstructed the complete formula byte for byte, checked all
  six ordered anchor-type normalizations and all 1,716 sorted residual
  signature sequences, and found a clause-satisfying SAT model when the
  theta-gap block was removed.
- Combining this residual certificate with the already certified C-090
  full-response branch proves C-097:
  \[
    \text{no order-13 counterexample has common parameter three.}
  \]
  The global finite frontier remains 13 because parameter four and five at
  order 13 remain open.  The all-order \(k=3\) theorem and the universal
  conjecture also remain open.
- Independently, original cross-edge analysis proved that every failed
  physical incidence produces a virtual-rainbow cap.  The exact third-color
  two-list is the sole cap list without a local unit consequence.  Two
  equality controls with greatest eternal families refute both simultaneous
  two-edge retention and joint-endpoint physicalization.  Thus the remaining
  universal problem is genuinely global composition of tight third-color
  gates inside an inclusion-minimal unsatisfiable response formula.

## 2026-07-28 01:46 PDT — odd-return theorem and radius-two localization

- The tight third-color gate now has an exact binary chirality.  Gate
  constraints preserve chirality, while a same-type connector in one frozen
  projection flips it exactly when its complement-path length is odd.  The
  associated type-word calculation makes every literal-preserving closed
  walk even and every physical closure of a path from a literal to its
  complement odd.
- A direct attack proof goes beyond the parity bookkeeping.  In an arbitrary
  eternal triple-family, two tight caps sharing the required physical port
  cannot be connected back by any odd path contained in one omitted-color
  projection.  Every attack is unoccupied and moves exactly one adjacent
  guard; the proof does not use \(\gamma=3\).  The hostile reviewer accepted
  all odd subdivisions and independently checked the sharp even-return
  equality control `MEXrtIdmdjLQqztC?`, whose 172-state greatest family
  satisfies all 1,892 attack obligations.  This promotes C-100.
- The theorem does not collapse an arbitrary unit-free 2-SAT bicycle:
  physical ports may be separated and odd holonomy may be distributed
  across multiple projection components.  That is now the primary universal
  proof target.
- Independently, the C-097 residual certificate was weakened from full
  eternal closure to closure only at retained triples meeting the reference
  independent state.  The resulting radius-two formula removes exactly
  8,400 clauses, leaving 9,802 variables and 76,214 clauses.  Its
  168,880-line deletion-free proof passed strict RUP-only replay with zero
  RAT lemmas after clean-room byte reconstruction.  This promotes C-101.
- Radius one and all three two-of-three single-anchor slice relaxations are
  SAT.  Direct checkers ignore the SAT move variables, recompute every
  partial one-guard response and exact graph parameter, and obtain
  \((\gamma,i,\alpha,\gamma^\infty,\theta)=(3,3,3,4,4)\) in each
  two-slice control.  Each fails in the omitted slice.  This refutes the
  proposed two-projection shortcut (C-102) and shows that the finite
  contradiction is genuinely three-way at depth two.
- The order-13 parameter-three manuscript was strengthened by making
  domination of each frozen projected state explicit.  Two fixed-epoch
  builds are byte-identical, all ten rendered pages were visually inspected,
  and the build logs are clean.  Publication remains gated on an independent
  hostile manuscript audit and the final aggregate replay.
- A compressed prepublication search across current arXiv, primary journal
  records, author-index results, and citing papers located no universal
  resolution, certified counterexample, or prior order-13 parameter-three
  exclusion.  This is a search result, not proof of novelty; the manuscript
  retains its explicit no-worldwide-priority disclaimer.
- No universal proof, counterexample, complete order-13 exclusion, or
  order-14 lower bound is claimed.

## 2026-07-28 02:09 PDT — separated two-gate odd bigons excluded

- A second arbitrary-length attack theorem synchronizes the parities of two
  vertex-disjoint complement paths in different frozen projections.  If
  \(P=x_0\ldots x_m\subseteq W_c\) and
  \(Q=y_0\ldots y_n\subseteq W_a\), the initial responses are positive, and
  the two boundary states \(\{b,x_0,y_0\}\) and
  \(\{b,x_m,y_n\}\) are absent, then \(m\equiv n\pmod2\).
  The proof launches two forced boundary states and propagates a retained
  \(b\)-state two path edges at a time.  It needs no \(\gamma=3\) or
  coloring hypothesis.
- Two tight third-color gates supply the required absent boundary states
  through their cap nonadjacencies.  In a unit-free no-full bicycle,
  projection components of different types are physically disjoint: an
  intersection omits two anchor colors and therefore has a singleton list,
  creating a unit.  Hence every two-gate odd-holonomy bigon is impossible,
  even with four separated ports and arbitrary subdivisions.
- The hostile reviewer caught one finite-audit mismatch before acceptance:
  the discovery checker had omitted length-zero paths while its prose said
  all paths.  The checker was extended rather than the claim weakened.
  Independent enumeration now checks \(86+150+246+396=878\) qualifying
  path pairs across four equality controls, including length-zero cases,
  with zero parity violations.  All 7,851 one-guard obligations in the four
  controls were independently rebuilt.  Dropping either dead-boundary
  hypothesis yields explicit opposite-parity controls.
- The final hostile verdict is unconditional `PASS`, promoting C-103.  The
  exact remaining tight-gate holonomy problem is an inclusion-minimal odd
  signed cycle through at least three gates.  This is not yet the complete
  \(k=3\) theorem.
- The complete 398-test campaign suite passed in 381.812 seconds, with
  maximum resident set size 182,550,528 bytes and zero swaps.

## 2026-07-28 02:38 PDT — order-13 paper passes exact-byte release audit

- A hostile prepublication audit found one genuine attribution defect before
  release.  Klostermeyer--Mynhardt (2015) identifies the gap in the 2009
  argument and reopens the assertion as an explicit question, but does not
  itself use the gamma--theta name.  The paper and public page now distinguish
  the 2009 assertion, the 2015 correction/question, and terminology used in
  subsequent literature.
- The corrected manuscript was rebuilt twice with fixed source epoch.  Both
  builds are byte-identical; the final ten-page PDF has SHA-256
  `6768cecf0d46672f7d56cbda2715b49ef18470e5d60b3c7912fc9999843ae5a4`.
  Pages 1--2 were re-rendered after the correction, and the independent
  reviewer rendered and inspected all ten current pages.
- The exact-byte hostile release verdict is unconditional `PASS`.  It covers
  theorem scope, the human one-guard arguments, C-090/C-096/C-097 binding,
  certificate shapes and hashes, symmetry counts, controls, citations,
  disclosure, deterministic build, and rendering.
- The compact C-097 wrapper passed again from the staged package.  Formula
  reconstruction, strict RUP-only replay, six anchor permutations, 1,716
  residual signature multisets, the equality control, and the satisfiable
  theta-gap ablation all passed.
- Local web QA passed at desktop and 390-pixel mobile width.  The apparent
  narrow full-page capture was isolated to screenshot stitching: DOM
  measurements show full viewport width and no horizontal overflow, and the
  ordinary viewport capture is correct.  The page has no browser warnings.
- Only the commit/tag/release/Pages/live-byte gates remain.  A bounded proof
  lane has simultaneously resumed at the exact universal target left by
  C-103: a minimal odd signed cycle through at least three tight gates.

## 2026-07-28 02:41 PDT — tagged release and live Pages bytes verified

- Committed the audited 119-file release bundle as
  `883e796cb163f360d8052e94ae507d3cbb3e6599`.  Unrelated dirty research
  files, transient TeX auxiliaries, exploratory certificates, and lock files
  were not staged.
- Created annotated tag `gamma-theta-order13-k3-v1.0.0` and pushed `main`
  plus the tag atomically.  The peeled tag points to the exact audited
  commit.
- Published the GitHub release with the PDF, checksum, C-097 acceptance
  record, and publication QA record.  GitHub's reported SHA-256 digest for
  every asset matches the local file.
- The legacy Pages webhook did not enqueue automatically after the large
  atomic push, so an explicit Pages build was requested through GitHub's
  build endpoint.  Actions run `30347479445` completed successfully on the
  tagged commit.
- Cache-bypassed downloads of the home page, active workstream, paper page,
  checksum, and PDF are byte-identical to the repository source.  The live
  PDF retains SHA-256
  `6768cecf0d46672f7d56cbda2715b49ef18470e5d60b3c7912fc9999843ae5a4`.
  A final live browser rendering is clean and produces no console warning or
  error.
- Publication changes only availability, not mathematical scope: order-13
  parameters four and five, arbitrary-order parameter three, and the
  universal conjecture remain open.

## 2026-07-28 02:58 PDT — release cross-audits and three-gate proof target

- Two additional independent hostile audits of the tagged order-13
  parameter-three release returned unconditional `PASS`.  The first checked
  every manuscript proof, one-guard move, certificate statistic, coverage
  count, graph6 control, citation, disclosure, and rendered page.  The
  second independently rebuilt the deterministic PDF and checked the tagged
  source and release hashes.  No additional publication blocker was found.
- A direct boundary-cycle formula was built only as a proof-discovery tool.
  It encodes an arbitrary eternal family of triples, an independent retained
  anchor state, three or more tight-gate dead boundaries, and connector paths
  in the appropriate omitted-color projections.  With
  \(\gamma(G)\ge3\), all tested odd-total connector parities are UNSAT for
  three, four, and five gates; tested even totals are SAT.  The shortest odd
  system is SAT when the \(\gamma\ge3\) condition is dropped.  These are
  `OBSERVED` controls, not a finite theorem or universal proof.
- The smallest proof core exposes the intended mechanism.  Without spare
  vertices a particular pair of gate ports has no common complement
  neighbor and therefore dominates.  A spare common neighbor can postpone
  that contradiction, but one-guard closure forces a new deficient pair.
  Larger cores continue this witness cascade.  The required human step is
  to prove that the cascade is a genuine finite descent rather than infer it
  from bounded UNSAT.
- In the actual unit-free/no-full 2-SAT branch, every outside vertex has a
  nonempty proper nonsingleton response list, hence an exact two-list and a
  unique omitted-anchor type.  This turns the possible common-neighbor
  witnesses into a three-case analysis and is now the primary proof
  simplification.
- A separate bounded proof lane resumed the full-response-list extension
  problem.  No order-14 computation has begun.

## 2026-07-28 03:23 PDT — canonical three-gate witness theorem accepted

- Two explicit symmetric one-guard attack trees now prove that any
  nondisplayed common complement neighbor of a critical pair in the
  canonical length-one three-gate boundary contains both colors of the
  third response type.  In the unit-free no-full branch it is therefore an
  exact third-type almost-cap.
- The hostile reviewer identified a real scope omission before acceptance:
  \(\gamma\ge3\) guarantees a common complement neighbor but does not make
  it external to the displayed boundary.  A new collision lemma exhausts
  all twelve displayed candidates.  Anchors and endpoints cannot witness;
  displayed third-type vertices are already physical caps; two unused
  wrong-type caps are handled by the original trees; and the two genuine
  endpoint collisions have separate three-attack contradictions.
- After that repair, the hostile review returned unconditional `PASS`.
  Its clean-room bitmask/queue implementation reconstructs the control
  `KBn]r]vj]lnZ`, exact parameters
  \((2,2,3,3,3)\), all 181 greatest-family states, 1,629 unoccupied
  attacks, 2,934 legal moves, response lists, dead boundaries, dominating
  pairs, graph6 round-trip, and both frozen hashes.  This promotes C-104.
- A separate Boolean obstruction audit proves that the two physical arms
  of the forced almost-cap resolve to only one endpoint implication.  They
  do not supply the reverse implication needed for tight-gate chirality
  equality, so a raw gate-count or connector-length shortening is unsound.
  The remaining no-full target is an oriented paired-repair lemma that
  tracks both contradiction paths in a minimal unsatisfiable 2-CNF.
- The full-list lane independently derived a propagation theorem along
  ridge-connected maximum-independent triples and is testing its exact
  global consequence.  No universal theorem, counterexample, complete
  order-13 exclusion, or order-14 bound is claimed.

## 2026-07-28 03:31 PDT — one-sided almost-cap obstruction accepted

- An independent reviewer reconstructed the exact chirality table for a
  third-type almost-cap.  Its two complement arms existentially eliminate
  to one oriented endpoint clause; they do not reproduce the two
  implications of a tight-gate equality.  The displayed counterassignment
  proves that raw chord substitution is logically unsound.
- The first draft overstated what the accepted physicalization controls
  proved.  It was repaired to distinguish C-095/C-099 incidence-transport
  countercontrols from the conditional C-098 cap theorem and to make no
  monotonicity claim for connector length or physicalization distance.  The
  hostile re-audit then returned unconditional `PASS`, promoting C-105.
- The remaining no-full proof target is narrower and oriented: preserve
  both marked contradiction paths while repairing one-sided implications.
  A shortest odd XOR triangle already ties rather than decreases clause
  count, and resolution-derived logical units do not automatically become
  singleton family-response lists.
- The full-target facet-propagation note is frozen and under independent
  hostile review.  No universal theorem, counterexample, complete
  order-13 exclusion, or order-14 bound is claimed.

## 2026-07-28 03:38 PDT — full-target vertex-star propagation accepted

- A two-attack argument proves that, for a fixed target, response
  membership of a physical guard is invariant across any maximum
  independent triples containing it, even when the triples share only that
  one vertex.  This defines a global active set meeting every deletion
  facet.
- Proper three-colorings of the deletion complement turn the active set
  into a nonempty responder-color set on each ridge component.  A common
  color extends over the target.  Therefore the equality-critical
  full-target branch requires at least three components with empty global
  responder-color intersection, while the full-state component carries all
  three colors and no complement neighbor of the target.
- The hostile reviewer reconstructed every forced move and support-coverage
  argument and returned unconditional `PASS`.  A clean-room exhaustive
  audit of 9,021 arbitrary eternal subfamilies and 282,156 coloring
  instances found zero failures; the order-12 full-list control and
  \(\overline{L(K_{3,3})}\) boundary were independently replayed.
- The accepted theorem is C-106.  It isolates a concrete global
  responder-color intersection target but does not prove that the
  intersection exists, the complete \(k=3\) theorem, or the universal
  conjecture.

## 2026-07-28 03:54 PDT — local paired-repair descent refuted

- The exact oriented replacement calculation shows that two almost-cap
  arms replace \(d\) implication arcs by two.  Strict descent occurs only
  for \(d>2\); shortest contradiction paths do not force this.
- A new 19-vertex gamma-two control realizes the failure physically.  Its
  703-state eternal family has only exact two-lists and three tight gates
  of odd holonomy.  The selected dynamic almost-cap subdivides an already
  essential clause: the unique minimum unit-free core grows from 9 to 10
  clauses and one marked path grows from 4 to 5 arcs while the reverse
  path remains length 5.
- The independent hostile checker reconstructed the graph6 record,
  \((\gamma,i,\alpha,\gamma^\infty,\theta)=(2,2,3,3,3)\), all 11,248
  obligations, the complete response formula, both unique cores,
  chirality, resolvent orientation, and path lengths, returning
  unconditional `PASS`.  This promotes C-107.
- Because the control has a dominating pair, it leaves a narrower
  gamma-three route: witnesses must be applied at several critical pairs
  and forced either to grow indefinitely, collide into an excluded
  geometry, or expose a dominating pair.  Bounded all-pairs probes are
  encouraging but remain `OBSERVED`.
- The universal conjecture, the complete \(k=3\) case, and the complete
  order-13 exclusion remain open.

## 2026-07-28 04:03 PDT — target-response propagation generalized to every \(k\)

- The two-attack vertex-star mechanism from C-106 was recognized as an
  arbitrary-\(k\) exchange theorem.  Starting at \(T-v+x\), attack the
  vertices of \(T'-T\) in sequence.  A guard already in \(T'\) has no move
  edge, while moving \(x\) leaves every guard nonadjacent to \(v\);
  closure therefore replaces one old vertex at each step and ends at
  \(T'-v+x\).
- Under equality this defines a global, family-relative active set meeting
  every maximum independent \(k\)-set.  Proper deletion \(k\)-colorings
  give componentwise responder-color sets and exact inactive-set color
  identities.  The inactive complement is \(K_k\)-free, a common responder
  color extends over the target, and a critical full target forces at
  least three ridge components.
- An independent hostile reviewer checked all proof dependencies and edge
  cases, including \(k=1\), arbitrary rather than greatest families, and
  overlapping states.  A clean-room enumeration of all labeled graphs
  through order five, all guard numbers, 60,011 eternal subfamilies,
  57,622 forced paths, and 336,298 colorings found zero failures.
- The unconditional `PASS` promotes C-108.  This is the first campaign
  structural theorem here stated uniformly for every \(k\), but it leaves
  the global responder-color intersection open and does not resolve the
  conjecture.
