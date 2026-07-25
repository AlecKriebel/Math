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
