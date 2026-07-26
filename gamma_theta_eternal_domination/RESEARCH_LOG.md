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
