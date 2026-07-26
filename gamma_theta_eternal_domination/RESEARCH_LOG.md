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
