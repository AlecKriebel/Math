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
