# Research log

This is the append-only narrative log for the certificate-first \(R(5,5)\)
program. `STATE.md` is the live summary, `CLAIMS.md` is the evidence ledger,
and `results/experiments.csv` is the machine-readable experiment ledger.
Future research cycles should add dated entries here rather than rewriting
earlier outcomes.

## 2026-07-23 — Stage zero and trusted baseline

- **REPRODUCIBLE COMPUTATIONAL OBSERVATION:** current sources retrieved on
  2026-07-23 report \(43\leq R(5,5)\leq46\). The literature extraction,
  algorithms, catalogs, degree consequences, and source links are recorded in
  `literature.md`.
- **REPRODUCIBLE COMPUTATIONAL OBSERVATION:** the audited machine is an Apple
  M1 Pro with 10 CPU cores and 16 GB memory. No external SAT proof checker,
  nauty/Traces installation, or graph package was available; details are in
  `environment.md`.
- **CERTIFIED:** two independent graph-verification paths were implemented:
  direct enumeration of every 5-subset in Python and recursive bitset clique
  search in C++. Complete, empty, random/complement, \(C_5\), and Paley-17
  tests passed.
- **CERTIFIED:** the edge-flip identity
  \(\Delta E=t-q\) for an addition and \(\Delta E=q-t\) for a deletion was
  proved and checked on all 491,520 flips of all labeled order-6 graphs.

## 2026-07-23 — Reconstructed 42-vertex witness

- **CERTIFIED:** the published cyclic Exoo construction was reconstructed
  locally. The resulting graph has 42 vertices, 435 edges, no 5-clique, and
  no independent 5-set under both verifiers. This proves
  \(R(5,5)\geq43\).
- Graph6 SHA-256:
  `a7db2ac21e14b3652629d0cfc1c47bf7b65f355e1f2fcf9048a075622c5ba75a`.
- Canonical artifact SHA-256:
  `319df4d75fc4c4758a6985b4961be441be5a08c813e3042ba7fcadcea2f9529a`.
- An independently written artifact validator later reconstructed and checked
  all stored representations, schema fields, counts, and serialization.

## 2026-07-23 — Constructive order-43 baselines

- **REPRODUCIBLE COMPUTATIONAL OBSERVATION:** random-start min-conflicts/tabu
  reached \(E=231\) in 7.000013 seconds.
- **REPRODUCIBLE COMPUTATIONAL OBSERVATION:** an Exoo42-derived start reached
  \(E=2\) in 17.641678 seconds, a reduction of 229 conflicts. Breakout
  weighting and deterministic replay retained the same graph.
- The best candidate has 43 vertices, 454 edges, degree sequence
  \(20^{14},21^{10},22^{19}\), \(C_5=0\), and \(I_5=2\). It is invalid and
  proves no new bound.
- The residual independent sets are
  \(\{3,4,7,41,42\}\) and \(\{3,4,38,41,42\}\).
- A later source-recovery audit replayed all four search configurations from
  source SHA-256
  `2f0a1fba656b7550124f2a213a046c5ace42742d4d8e3c36967eefabe16e3674`;
  every graph was byte-identical and independently reverified.

## 2026-07-23 — Fixed-core exact completions

- **CERTIFIED:** the fixed Exoo42 one-vertex extension is UNSAT:
  42 variables, 2,318 clauses, and two checked exhaustive-tree proof paths.
  This is fixed-core nonextendibility, not global order-43 nonexistence.
- **CERTIFIED:** all 42 labeled \(k=1\) replacements are UNSAT:
  83 variables per instance, 104,058 checked proof records, and all 280,376
  clauses independently reconstructed. Coverage-enforcing rechecks require
  deletion labels exactly \(0,\ldots,41\).
- **CERTIFIED:** the first bounded \(k=2\) case, deleting original vertices
  0 and 1 and adding three vertices, is UNSAT: 123 variables, 13,338 clauses,
  and 19,734 checked proof records. The other 860 deletion pairs were not run.

## 2026-07-23 — Residual-focused exact neighborhoods

- **REPRODUCIBLE COMPUTATIONAL OBSERVATION:** exhaustive Hamming-radius-two
  search around the \(E=2\) graph found no improvement in 408,156 exact
  delta evaluations.
- **CERTIFIED:** four explicitly bounded free-edge neighborhoods with 19, 66,
  80, and 86 variables are UNSAT. Independent formula reconstruction and
  exhaustive-tree checking succeeded for every case. Between 817 and 884
  graph edges remained fixed, so these results are not unrestricted local or
  global nonexistence.
- **REPRODUCIBLE COMPUTATIONAL OBSERVATION:** the first neighborhood freeing
  the complete boundary of the six residual vertices has 237 variables and
  49,461 independently reconstructed clauses. The deterministic solver
  returned `TIMEOUT` after 60.003176 seconds, 659 nodes, 338 decisions, and
  320 conflicts. No proof or candidate was produced; this is neither SAT nor
  UNSAT.

## 2026-07-23 — Direct unrestricted encoding

- **CERTIFIED:** the unrestricted order-43 edge-variable CNF was generated
  and independently reconstructed clause-by-clause.
- It contains 903 primary edge variables, 64,500 sequential-counter
  auxiliaries, 1,925,196 Ramsey clauses, 126,936 degree clauses, and
  2,052,132 clauses total.
- CNF SHA-256:
  `141de0a9714fb40e100508031b37fa555bf2fbdefd13c2dee4c04141c159bcb1`.
- The 90,311,307-byte instance was not solved. This certifies the encoding
  identity only and is not a SAT/UNSAT result.

## 2026-07-23T22:16:44Z — Checkpoint

- **CERTIFIED:** the full regression suite passed: 52 tests, the exhaustive
  491,520-case flip audit, and 4,000 independent C++ incremental checks.
- **CERTIFIED:** the Exoo42 witness still passes both graph verifiers; the
  order-43 \(E=2\) candidate is still correctly rejected by both.
- **CERTIFIED:** the direct order-43 CNF and the 237-variable incident
  neighborhood again matched their independent clause reconstructions.
- No outcome A–F has been achieved, and no Ramsey-number bound has changed.
- Next selected constructive experiment: restrict the C++ min-conflicts/tabu
  kernel to the 237 incident edges, benchmark fixed and fresh seeds, and pass
  the best partial assignments to exact completion. The current DPLL strategy
  remains paused after the strict timeout rather than receiving a blind
  budget increase.

## 2026-07-23T22:19:09Z — Durable repository checkpoint

- Commit `9ff504acf4bef068e85df6e14bfbfecd7bfec84f` on
  `codex/h668-theory` records the certificate-first \(R(5,5)\) baseline.
- The commit contains only `ramsey55/` paths. Unrelated Hadamard work in the
  parent repository was left untouched.
- `RESEARCH_LOG.md` is the append-only narrative ledger; `STATE.md` remains
  the replaceable live summary and `results/experiments.csv` the append-only
  machine-oriented experiment ledger.

## 2026-07-23 — Restricted 237-edge constructive search

- **REPRODUCIBLE COMPUTATIONAL OBSERVATION:** a standalone C++ kernel searched
  exactly the 237 edges incident to
  \(\{3,4,7,38,41,42\}\), preserving all 666 other edges.
- Seed 20260726, four 75,000-move restarts, tabu 9, random walk 0.04,
  breakout interval 250, and restart perturbation 12 executed 300,000 moves
  and 1,528,975 exact delta evaluations in 27.084184 seconds.
- No valid graph was found. The retained graph still has \(E=2\), but on the
  complement side: 455 edges, \(C_5=2,\ I_5=0\), degree sequence
  \(20^{13},21^{10},22^{20}\).
- It differs on 135/237 free edges. Its two cliques are
  \(\{2,4,24,25,42\}\) and \(\{4,24,25,26,42\}\), again with a four-vertex
  intersection and six-vertex union.
- **CERTIFIED SOFTWARE CHECK:** all 237 ordinary and all 237 weighted
  single-flip deltas, 100 sequential ordinary flips, and 100 sequential
  weighted flips agreed with exact recounts. The fixed-edge invariant held.
  Both independent full-graph verifiers reject the candidate with the same
  forbidden-type result.
- The preregistered 16-seed schedule was preserved but then cancelled after
  exact certification of the whole boundary made further heuristic sampling
  mathematically redundant.

## 2026-07-23 — Pinned proof-producing toolchain

- **REPRODUCIBLE COMPUTATIONAL OBSERVATION:** Python-SAT 1.9.dev7 was installed
  under isolated Python 3.11.8, and `drat-trim`/`lrat-check` were built at
  commit `2e3b2dc0ecf938addbd779d42877b6ed69d9a985`.
- Every retained result records the exact paths, versions, executable hashes,
  solver statistics, and checker transcripts. The temporary install can be
  rebuilt from `environment.md`.
- A CaDiCaL proof trace was not accepted by `drat-trim` and supports no
  claim. All certified results below use Glucose3 traces accepted by both
  stages of the DRAT-to-LRAT checking chain.

## 2026-07-23 — Both full incident boundaries closed

- **CERTIFIED:** the original 237-variable, 49,461-clause formula is UNSAT.
  Glucose3 used 0.283349 internal seconds; `drat-trim` accepted the
  1,070,726-byte DRAT and `lrat-check` accepted the 1,891,741-byte LRAT.
  This supersedes the earlier DPLL timeout as the formula's current status.
- **CERTIFIED:** the constructive candidate's alternative six-vertex
  boundary is also UNSAT: 237 variables and 49,677 clauses. Glucose3 used
  0.275337 internal seconds; both DRAT and LRAT checkers accepted the proof.
- These are two separately labeled fixed-666-edge exclusions, not a global
  order-43 UNSAT result.
- Candidate conflict-union completions were also materialized as CNFs with
  explicit unit assumptions and accepted through LRAT. They validate the
  exact-completion workflow but are logically narrower than the complete
  237-edge certificates.

## 2026-07-23 — Aggregate core radius six

- **CERTIFIED:** all 237 original boundary edges may be arbitrary and up to
  six of the other 666 core edges may differ from the base, yet the resulting
  formula is UNSAT.
- The direct Ramsey-plus-counter instance has 5,544 variables and 1,934,472
  clauses. An independent checker reconstructed all clauses exactly; a
  separate semantic audit checked the partition, signed difference literals,
  counter semantics, ten repository tests, and 4,096 small-instance primary
  assignments.
- Glucose3 returned UNSAT in 78.839855 internal seconds. `drat-trim` accepted
  a 347,262,937-byte raw DRAT using 169,233,890 resolution steps, and
  `lrat-check` accepted the generated 1,424,628,404-byte LRAT.
- Only a 68,702,255-byte Zstandard DRAT is retained. It passes `zstd -t` and
  decompresses to raw SHA-256
  `1bfc9fc9f8df0b042a3df72e0c422b84c914eb46cc216811b6c9abc147c67e26`.
- Consequence: in this labeled framework a valid graph must change at least
  seven core edges. This remains a local structural statement and does not
  change \(43\leq R(5,5)\leq46\).

## 2026-07-23 — First radius-seven shell experiments

- **REPRODUCIBLE COMPUTATIONAL OBSERVATION:** the independently reconstructed
  aggregate radius-seven formula has 6,203 variables and 1,935,789 clauses.
  A strict 120-second Glucose3 replay returned `TIMEOUT` after 120.080041 wall
  seconds. No proof or model was produced.
- **CERTIFIED SOFTWARE/ARTIFACT CHECK:** an independent proof-core audit
  reconstructed all 49,461 source clauses, uniquely mapped all 6,335 retained
  input-core clauses to their exact five-subsets, and reproduced the full
  ranking of 666 fixed core edges.
- A seven-edge cut was preregistered before formula generation using ranks
  1–7:
  \((0,32),(18,33),(18,20),(24,26),(1,10),(9,29),(27,29)\).
- **CERTIFIED:** that exact cut is UNSAT when combined with all 237 free
  boundary edges. The independently reconstructed formula has 244 variables
  and 52,148 clauses. Glucose3 used 0.458771 internal seconds; `drat-trim`
  and `lrat-check` accepted the DRAT/LRAT chain.
- This closes one selected seven-core-edge cut only. Other radius-seven cuts
  and the aggregate radius-seven formula remain open.

## 2026-07-23T23:36:47Z — Post-continuation regression

- **CERTIFIED SOFTWARE CHECK:** the expanded `make test` suite passed 68 unit
  tests, the exhaustive 491,520-case flip-delta audit, 4,000 general C++
  incremental checks, and 674 restricted-kernel delta checks.
- The new focused suite separately passed 16 tests covering core-radius
  semantics, fail-closed production metadata, exact completion, bounded
  timeout behavior, proof tampering, candidate boundary auditing, and search
  output cross-checking.
- No global claim or Ramsey-number bound changed in this cycle.

## 2026-07-24 — Authoritative order-42 catalog import

- Imported Brendan McKay's 328-line `r55_42some.g6` catalog from the ANU
  Ramsey data page. The source says these are 328 known
  \((5,5;42)\)-graphs and that their complements are the other 328
  historically known examples; it explicitly does not claim completeness.
- Catalog SHA-256:
  `067902e853d87b49bcef0d1d4c0e3bbadd238ee18bc65341b079a3ca4780eccb`.
- **CERTIFIED DATA CHECK:** all 328 distinct entries passed both the
  exhaustive Python five-subset verifier and the independent C++ recursive
  bitset verifier. Exact coverage and all 656 verifier invocations are
  recorded in
  `results/verification/r55_42some_catalog_dual_check.json`, SHA-256
  `6fe9186d25b16efe98029f60b11f4a5f5f8559c7150380cb3dc45b09833c0931`.

## 2026-07-24 — Every historically known order-42 witness is nonextendible

- **CERTIFIED, FIXED-CORE SCOPE:** every one of the 328 imported graphs has
  an UNSAT one-vertex extension formula. All 328 compact exhaustive-tree
  proofs were accepted by an independent decoder, formula reconstructor,
  unit propagator, and proof-tree checker.
- Exact coverage: lines 1–328; SAT 0; UNSAT 328; limits 0; checked proofs
  328. The proof bundle contains 17,246 bytes, 12,982 tree nodes, and 6,655
  leaves.
- Consolidated result SHA-256:
  `5c9ce7bd1789e2496a6bcb0ad7521712a721b99b4154ed1f5f861921cca7a81d`.
- Complementing the core and negating all new-vertex variables swaps the
  two clause families, so the same result covers the 328 complementary
  historical witnesses.
- Fail-closed recovery: the first orchestration attempt stopped only because
  it rejected the solver's conventional UNSAT exit code 20 after all proofs
  had been produced. The retained proofs were not overwritten. A corrected
  recovery wrapper regenerated every proof separately, required all 328
  replays to be byte-identical, then checked the retained proofs. Full
  details and hashes are in
  `certificates/catalog42_extensions_v1.report.md`.
- Limitation: the public source allows unknown order-42 graphs. This closes
  the 656 historically known fixed cores, not all order-42 graphs and not
  unrestricted order 43.

## 2026-07-24 — Global degree branches and symmetry-aware SAT pilots

- **CERTIFIED ENCODING DECOMPOSITION:** complementing if necessary and
  relabeling a chosen vertex reduces the unrestricted order-43 formula to
  four lossless branches in which vertex 0 has degree 18, 19, 20, or 21 and
  its neighbors form a fixed prefix. An independent streaming checker
  matched every branch to the direct CNF plus its intended 42 units.
- MapleChrono pilots at 200,000 conflicts in all four branches returned
  `BUDGET_EXHAUSTED`. No model or proof was produced; all branches remain
  open.
- Built the official SAT Modulo Symmetries toolchain at SMS commit
  `464f12f1fd36b496e7ba9dcbb622b079de02dce4` with its pinned CaDiCaL
  submodule in an isolated temporary tree. The only portability patch added
  a missing standard-library include.
- The official PySMS builder produced an independently reconstructed
  order-43 formula with 44,247 variables, 2,095,476 clauses, and SHA-256
  `20b5440e91512c8f4751016e0111419f747e135b91a7e4738a517c81ad4ec92d`
  as recorded in
  `results/global_exact/sms/order43_encoding.metadata.json`.
- Small controls passed: enumeration of all 11 unlabeled order-four graphs,
  a directly checked \(R(3,3;5)\) SAT model, and an SMS-disabled
  \(R(3,3;6)\) UNSAT LRAT accepted by the independent checker.
- The 120-second order-43 SMS pilot returned
  `INTERNAL_TIMEOUT_UNKNOWN` after 58,373 minimality calls and 36,573
  generated symmetry clauses. Every retained lex-leader witness passed the
  independent permutation audit. This is neither SAT nor UNSAT.

## 2026-07-24 — Dynamic incident expansions beyond the six-vertex barriers

- A preregistered exact moving-boundary screen freed every edge incident to
  each \(E=2\) candidate's six-vertex conflict union plus one additional
  vertex.
- Across three independently obtained \(E=2\) basins, all 111 exact
  seven-incident-vertex boundaries solved UNSAT within the 200,000-conflict
  budget; SAT 0 and limits 0.
- The most structurally different basin was then widened exhaustively to
  every pair of additional vertices: 666 exact eight-incident-vertex
  boundaries, each with 308 free edges. Results were SAT 0, UNSAT 666,
  limits 0. Median solver conflicts were 89,566.5 and the maximum was
  175,177.
- These runs did not retain or independently replay UNSAT proofs, so their
  negative results are **REPRODUCIBLE COMPUTATIONAL OBSERVATIONS**, not
  certified exclusions. They are fixed-boundary results and have no global
  implication.
- Consolidated two-extra-vertex result SHA-256:
  `28fd62f408ce2dd72cb6f91687263d619dde6bb19155221cb57d071e797d6df1`.

## 2026-07-24 — Exact targeted Hamming-distance-three scans

- For each of the three \(E=2\) candidates, enumerated every unordered triple
  of distinct edge flips that intersects both original homogeneous
  five-sets. This necessary condition loses no exact-distance-three
  solution.
- Each four-vertex-overlap conflict pair yields exactly 2,438,883 admissible
  triples. All three complete scans found no improvement at all: the best
  objective remained \(E=2\), and each output graph was byte-identical to
  its base.
- The exhaustive Python counter and independent C++ bitset verifier replayed
  the expected two conflicts for all three retained graphs.
- Evidence category: **REPRODUCIBLE COMPUTATIONAL OBSERVATION**. This is a
  scoped exact-distance result, not a formal UNSAT proof and not global
  nonexistence.

## 2026-07-24T01:20:57Z — Catalog delete-one/add-two projection work

- Generalized the compact proof producer and independent checker so each
  proof binds its catalog line and deleted vertex. Exact coverage is the
  \(328\times42=13{,}776\) family of fixed 41-vertex induced cores completed
  by two new vertices.
- **CERTIFIED PILOT:** 16 preregistered stratified pairs are independently
  proof-checked UNSAT, with no SAT or limit outcomes. This applies only to
  those 16 fixed cores.
- A separate resume-safe constructive screen of all 13,776 pairs is in
  progress. It intentionally does not promote unchecked UNSAT solver
  statuses: any SAT model is preserved before reconstruction and must pass
  both graph verifiers, while negative records remain observations.
- No global claim or Ramsey-number bound has changed.

## 2026-07-24T01:38:20Z — Nine-hundred-second global SMS continuation

- The preregistered official-SMS continuation used one process, the pinned
  SMS/CaDiCaL toolchain, no label-fixing units, and the independently matched
  order-43 degree-18-through-24 formula.
- **REPRODUCIBLE COMPUTATIONAL OBSERVATION:** SMS returned
  `INTERNAL_TIMEOUT_UNKNOWN` after 900.650872 solver seconds
  (952.167797 wall seconds), 280,325 minimality calls, depth 261, and 131,789
  generated symmetry clauses. It returned neither a graph nor an UNSAT
  result.
- The independent row-lex witness checker accepted every retained symmetry
  clause. The 77,314,750-byte transcript has SHA-256
  `89f7f39e411b23b4cd04ddbcf72a57ab157a8e3aacc015af8db517dbf91bad3c`.
- Result artifact:
  `results/global_exact/sms/order43_900s_result.json`. This timeout changes no
  Ramsey bound.

## 2026-07-24T01:59:00Z — Complete delete-one/add-two catalog screen

- The persistent implementation executed the full
  \(328\times42=13{,}776\) family of fixed 41-vertex cores obtained by
  deleting one labeled vertex from each imported order-42 catalog graph.
- **REPRODUCIBLE COMPUTATIONAL OBSERVATION:** all 13,776 exact completion
  solver calls reported UNSAT; SAT 0, limits 0, and errors 0. Exact coverage
  auditing found no duplicate, missing, or extra pair. Runtime was
  103.925976 seconds.
- These negative solver statuses were intentionally not promoted:
  `negative_certified_count=0`. The aborted 1,738-record process-launch
  attempt is separately marked `ABORTED_PARTIAL_NO_RESULT` and was not merged
  into the completed run.
- Summary SHA-256:
  `e5ee5b08d0250a2a9117999b9735823d45651649b2108d9da807813f55918ddf`;
  coverage SHA-256:
  `9b5a8832ff0389f7f84ad212f1cdab38aa54143576e005e3fa65d3a8de6ef697`.
- A preregistered stratified 64-pair proof-bundle sample was then produced and
  independently replayed. **CERTIFIED, FIXED-CORE SCOPE:** all 64 sampled
  cores are UNSAT. The compact bundle is 13,656 bytes with SHA-256
  `7c3d41898f437f571e07612e88e84342467fdde82d6dcdfe49bde227659a7c1f`;
  the coverage audit is valid and explicitly records 13,712 uncertified
  pairs outside the sample.
- A larger proof tranche was not launched because the immutable preflight
  required more than 3 GiB free disk and the machine had less. No global
  order-43 conclusion follows.

## 2026-07-24T02:02:00Z — Full-graph Hamming balls through radius eight

- The core-kick \(E=2\) candidate has 903 possible edges. Empty boundary
  metadata therefore makes the counter measure ordinary labeled graph
  Hamming distance across every edge, not only a selected core.
- **CERTIFIED, LOCAL SCOPE:** no valid \((5,5;43)\)-graph occurs within
  Hamming distance at most 6, 7, or 8 of
  `results/best_candidates/core_kick_seed_20260731.g6`.
- For each radius, an independent checker reconstructed every Ramsey and
  sequential-counter clause before solving. The exact formula and solver
  results were:

  - radius 6: 7,203 variables, 1,937,790 clauses, 40,126 conflicts,
    10.649591 internal solver seconds;
  - radius 7: 8,099 variables, 1,939,581 clauses, 145,701 conflicts,
    29.869302 internal solver seconds;
  - radius 8: 8,994 variables, 1,941,370 clauses, 380,611 conflicts,
    67.974969 internal solver seconds.

- In all three cases `drat-trim` accepted the Glucose3 DRAT and
  `lrat-check` accepted the derived LRAT. Result files are
  `certificates/core_kick_full_hamming_radius{6,7,8}_glucose3.result.json`.
- The byte hashes recorded in those result files are preserved after
  lossless Zstandard archival. Every `.zst` stream passed integrity testing
  and decompressed to the original recorded CNF/DRAT/LRAT SHA-256.
- Consequence: a valid labeled graph, if one exists, differs from this
  candidate in at least nine edges. This is a local exclusion only and does
  not improve \(43\leq R(5,5)\leq46\).

## 2026-07-24T02:15:17Z — Storage-safe proof replay validation

- Conventional radius-eight LRAT materialization reached 1,322,171,098
  bytes, while system-wide free disk fell below 2 GiB. Radius nine was not
  launched under unsafe storage conditions.
- Implemented `src/certify_cnf_glucose_streaming.py`, which sends
  `drat-trim` LRAT output through a FIFO into Zstandard and streams the
  decompressed byte sequence through `lrat-check`, retaining only the
  compressed proof.
- **CERTIFIED SOFTWARE CHECK:** on the previously certified alternative
  237-edge formula, the streaming pipeline reproduced the exact historical
  1,806,516-byte LRAT SHA-256
  `df22449c12fcb20fb2140a1fa3f8ffe3f10bc4716c957e10b4518a0de821c5c3`,
  and both proof checkers returned `VERIFIED`.
- The test establishes byte-exact streaming behavior. A fresh immutable plan
  and safe disk preflight are still required before applying the new pipeline
  to radius nine.

## 2026-07-24T02:18:00Z — Primary-source and public-data adversarial audit

- **REPRODUCIBLE COMPUTATIONAL OBSERVATION:** current primary sources still
  report \(43\leq R(5,5)\leq46\); no public order-43, order-44, or order-45
  construction or globally complete nonexistence certificate was located.
- **CERTIFIED DATA CHECKS:** in addition to the 328 local order-42 catalog
  checks, the audit exhaustively checked all 352,366 public
  \(R(4,5;24)\)-graphs and every published order-21/22/23 extremal slice used
  by the \(R(5,5)\leq46\) computation. Counts and graph properties match the
  paper.
- No public implementation or proof certificates for the full order-46
  computation were located. The paper reports approximately 30 CPU-years for
  the original computation and 50 CPU-years for an independent
  implementation.
- The public ROVEaC order-43 result was confirmed to be conditional: it
  excludes graphs containing at least six vertices of one of the 656 known
  order-42 deletions, not every order-43 graph.
- **CERTIFIED CORRECTION:** exhaustive reconstruction of
  arXiv:2212.12630v3 Example 6.2 gives one red and eleven blue \(K_5\)'s after
  the stated recoloring, not one red and eight blue. Example 6.1 and the
  Exoo42 control reproduce correctly.
- Full report:
  `results/verification/r55_primary_source_audit_20260723.md`, SHA-256
  `f9768602a5062a86f08e3e5ecd487829a135e3cfa8fc49916aabd83879dd8ee2`.

## 2026-07-24T02:19:00Z — Degree-preserving two-switch escape pilot

- A preregistered constructive pilot ran three fixed seeds from each of the
  three independently obtained \(E=2\) candidates.
- Across 9/9 completed runs it accepted 162,000 moves and evaluated 2,099,473
  candidates, including 317,654 compound two-switch moves, with 501 breakout
  updates and 657 full objective audits.
- **REPRODUCIBLE COMPUTATIONAL OBSERVATION:** no run found \(E=1\) or \(E=0\),
  and no positive-Hamming \(E=2\) state survived as a retained best. Every
  final graph was the corresponding input graph.
- All nine finals passed exhaustive Python verification, independent C++
  bitset verification, and a separate labeled degree/search-record audit.
  This is not a local-optimality or nonexistence result.
- Summary SHA-256:
  `8d94e6976c4579385ed0c1de3781c5f7bde14877d2b014ab61750de6debbe9e6`;
  report SHA-256:
  `588b4d3195aacffa61703b4148cde44ec916679a22fb0f478b20518bf2133728`.

## 2026-07-24T02:31:25Z — Delete-two/add-three catalog pilot

- A frozen, storage-gated plan selected 32 fixed 40-vertex cores: two labeled
  deletion pairs on each of 16 catalog graphs. Each completion adds three new
  vertices and has 123 Boolean variables.
- The preflight initially blocked while free disk was below the immutable
  2 GiB reserve. After two Git-reported abandoned temporary objects were
  removed and repository integrity rechecked, the same unchanged plan passed
  its gate and ran.
- **REPRODUCIBLE COMPUTATIONAL OBSERVATION:** exact coverage was 32/32; all 32
  solver calls reported UNSAT, with SAT 0, limits 0, and errors 0. Aggregate
  wall time was 0.740735 seconds, internal solver time 2.778875 seconds, and
  the search visited 41,718 tree nodes.
- No proof was generated or replayed, so
  `negative_certified_count=0`. These are fixed-core observations only.
- Summary SHA-256:
  `635eb6812440986ab9368099635f3b9ad1d8f661c170d66121ea020480bbdf77`;
  independent coverage SHA-256:
  `6d44097fedd40c0d72cbb5432ecc7a535941bb10508f3a59f6848a2ea3b65f39`;
  report SHA-256:
  `6be9737a782ed257d6dd9823077784eb3440566fb99cf70f8071fc395a70c8c1`.
- The pilot supports a compact full 282,408-core constructive screen; that
  larger run requires a separately frozen resume/storage plan.

## 2026-07-24T02:53:55Z — Exact circulant order-43 exclusion

- A preregistered exact encoding covered every undirected circulant graph on
  \(\mathbb Z_{43}\), with one Boolean variable for each of the 21 circular
  distances.
- All \(\binom{43}{5}=962{,}598\) vertex five-sets reduce to 10,437 distinct
  distance signatures. Independent reconstruction matched the resulting
  20,874 clauses exactly. CNF SHA-256:
  `d688450b666ec8722820ba266a572f36ae69e8e0b90c171750b5a8112c01be9a`.
- **CERTIFIED STRUCTURAL SUBCLASS EXCLUSION:** pinned Glucose3 returned UNSAT;
  `drat-trim` accepted the DRAT and produced LRAT, and `lrat-check` accepted
  the LRAT against the independently reconstructed CNF. DRAT SHA-256:
  `1c4f5f6910163d0aa6e6b1b33d5dbb13d83b0170a24495290917b529de006feb`;
  LRAT SHA-256:
  `1d800fbb5c318b58ec538818c4ad974a412ea61511a072efda3a134d172b4d42`.
- This eliminates the entire translation-invariant cyclic/Cayley class at
  order 43. It is not global order-43 nonexistence and changes no Ramsey-number
  bound. Full report: `certificates/circulant43_exact.report.md`.

## 2026-07-24T02:46:19Z — Stratified catalog-seed search and replay

- A preregistered pilot ran the exact-delta min-conflicts kernel from 22
  structurally stratified representatives spanning every catalog edge count
  423 through 430.
- **REPRODUCIBLE COMPUTATIONAL OBSERVATION:** all 22 runs completed and reached
  \(E=2\); no \(E=0\) or \(E=1\) graph was found. Eleven outputs had
  \((C_5,I_5)=(2,0)\), and eleven had \((0,2)\).
- Every stored graph was replayed with exhaustive Python enumeration and the
  independent C++ bitset verifier. The 22 raw labeled graphs are distinct;
  their pairwise labeled edge-Hamming distances range from 115 to 488.
- Production summary SHA-256:
  `83e550395f8c6ba28c8ceb16114cb029dc495327c08fa3fce0215b374506b9da`;
  independent replay SHA-256:
  `b59d0afa958f370715bbfa5379d7edac81b92cbb62e6332383f64458a887f7d9`;
  replay report SHA-256:
  `58f9c4cf83bdfb821973651f36a5b160a6e195e92f9d6f894d60eaea6db7aafb`.
- These are diverse invalid near-misses, not constructions or negative
  evidence.

## 2026-07-24T02:46:05Z — Conflict-hypergraph block search

- A preregistered ten-run pilot replaced the fixed-degree two-switch
  neighborhood by arbitrary one-to-three-edge conflict-block moves, ProbSAT
  selection, and multi-conflict shakes.
- **REPRODUCIBLE COMPUTATIONAL OBSERVATION:** the best objective remained
  \(E=2\), with no \(E=0\) or \(E=1\). All six runs from established \(E=2\)
  starts retained positive-Hamming \(E=2\) graphs at distance 37 or 38.
  Both catalog-derived \(E=104\) runs fell to \(E=2\); both global
  \(E=231\) runs retained their starts.
- All ten outputs passed exhaustive Python, independent C++, and structural
  verification. Summary SHA-256:
  `1c275399e22479f1cebdd1f1d04718530d16ece85936980bd5e516b9e29ecec2`;
  report SHA-256:
  `3bc7990860c322a9350ec19f221be78f79391af545819853dbac0006db191d60`.
- This establishes search mobility across the \(E=2\) plateau, not
  local-optimality or nonexistence.

## 2026-07-24T03:02:30Z — Conflict-block follow-up on all 22 near-misses

- A separately frozen follow-up ran one fresh 10,000-move conflict-block
  trajectory from each independently audited catalog near-miss.
- **REPRODUCIBLE COMPUTATIONAL OBSERVATION:** exact coverage was 22/22.
  Every run retained a positive-Hamming \(E=2\) graph, at distance 37 or 38;
  none found \(E=0\) or \(E=1\). Ten of eleven independent-set-conflict starts
  crossed to clique-conflict finals, confirming robust cross-fiber mobility.
- The 22 finals are raw-label distinct and all passed three verification
  paths. The run executed 220,000 selected moves, evaluated 5,091,883
  candidates, and performed 352 shakes.
- Frozen plan SHA-256:
  `0348b6342395492414fb1a1b350ce6200c2c38b2f207826b25479b6f0b94ab35`;
  summary SHA-256:
  `55b09b6f5c020b43eb892076e3768712dcba2fa754753523ca9fc10fa2ebea66`;
  report SHA-256:
  `44140fd3e7c0c4dd5f1b05473dfec6b0d00368555c96b378b832c0632cbd8bf3`.

## 2026-07-24T03:19:46Z — Targeted delete-three/add-four completions

- Two candidate-motivated fixed 39-vertex cores were preregistered before
  target formulas were generated. Each exact completion has 162 variables:
  156 core-to-new edges and six edges among four new vertices. Independent
  coverage checks matched all 741 fixed pairs for both targets.
- **CERTIFIED, FIXED-CORE SCOPE:** catalog line 327 after deleting original
  labels \(6,19,24\) has no four-vertex completion. Its 22,836-clause formula
  has SHA-256
  `d48d95433aca2f0cff262f4f416fffad1398179d05a68075c80b68a2dd825e94`.
  Glucose returned UNSAT; `drat-trim` and `lrat-check` both returned
  `VERIFIED`. The uncompressed LRAT SHA-256 is
  `40242d8b9335a3037554ca98f9d181323f38f19a2c5700699e518245ead044e7`.
- Catalog line 177 after deleting \(13,19,36\) has an independently matched
  22,624-clause formula, SHA-256
  `3bd0cbf35eeadb3388888f3664fee1ab53b751754981ecdd75e03997b805c21d`.
  Its solver never launched because the unchanged 2,432,696,320-byte storage
  gate failed. It has no SAT or UNSAT conclusion.
- Summary SHA-256:
  `c102799f7dc5c67abfacd464b398dc54c71c4d0e6e035b1a432f55a6cfde556e`;
  report SHA-256:
  `c4d29ca1161b5b62fb349746a9c80e5cc97eaf3e7267266025995e37ae8878a3`.
  No global order-43 claim follows.

## 2026-07-24T03:17:52Z — Full delete-two/add-three screen resource stops

- A frozen compact plan partitions all
  \(328\binom{42}{2}=282{,}408\) fixed 40-vertex cores into four balanced
  shards. Complete retained payload would be 13,555,840 bytes; negative
  statuses are observations, not proof certificates.
- Two hash-identical production attempts passed their initial storage gates,
  then stopped after 450.566053 and 220.970668 seconds when unrelated
  free-space swings breached the immutable 2 GiB live reserve. Neither
  attempt reported SAT, a solver limit, or an error.
- No complete shard was promoted, so registered full coverage remains 0/4.
  Independent prefix audits validated 29,249 record executions across both
  attempts. The second attempt recomputed 8,764 prefixes, leaving 20,485
  distinct fixed-core observations, all `OBSERVED_UNSAT_UNCHECKED`, with zero
  certificates.
- The resume-safe plan remains unchanged and must not be promoted until all
  four shards and all 282,408 records pass exact coverage. Plan SHA-256:
  `7f9d6dfe31e80f186d77d74703961e851b74f2c636c7acf68d98cc77e5ad2334`;
  cumulative diagnostic SHA-256:
  `204a0fb646e3114cfa22a75cb40262ac892f7dd5c949d9f5c76b4048db8963a9`;
  report SHA-256:
  `ae5601be046a31dec6158d1d6c42cf959ba3ac4eb6e1c430a32256b92bc5b6cc`.

## 2026-07-24T03:38:50Z — Order-seven automorphism branch

- An exact orbit encoding covers every order-43 graph admitting an
  automorphism with cycle structure \(7^6 1^1\). It has 129 edge-orbit
  variables and 273,696 clauses obtained from 136,848 distinct five-set
  signatures.
- **CERTIFIED ENCODING CHECK:** an independent implementation reconstructed
  all 129 orbits and every clause exactly. CNF SHA-256:
  `8045d463f68d78a745e18bb02ccc7d49fa02b47176a7282b1ef6f436fb109eb1`;
  checker-result SHA-256:
  `091060845957d7d8cd7b19fbeeee5b9f91f4a96da0828be5617e506ca47b1748`.
- The proof-producing solve was interrupted without a result when its hidden
  proof tempfile crossed the 2 GiB reserve. Three proof-free solvers then
  exhausted registered 500,000-conflict budgets; a fourth lacked limited
  solving support. The class remains SAT/UNSAT unresolved.
- The fixed vertex's degree is a multiple of seven and lies in
  \([18,24]\), hence equals 21. This canonically splits the six cycles into
  three neighbor and three nonneighbor cycles. Fixing audited
  \(R(4,5;21)\)-type side models leaves 63 cross-edge variables per gluing.
- An adversarial audit verified the mathematics and hardened storage,
  toolchain, model, schedule, and verifier bindings. A 256-pair v2 plan is
  frozen but unlaunched because its 2,149,483,648-byte gate fails. Plan
  SHA-256:
  `bdf6b8fecded2cee35a6eb2568d387f5ed844de601a9942ee483a4a3ac1c12a5`.
  Full report: `certificates/order43_automorphism7_six_cycles.report.md`.

## 2026-07-24T03:41:00Z — Exact topology audit of the 44-graph elite corpus

- An exhaustive direct audit enumerated every five-set in the 22 stratified
  catalog near-misses and their 22 conflict-block finals, after checking every
  graph hash against its bound search record.
- **REPRODUCIBLE COMPUTATIONAL OBSERVATION:** all 44 graphs have exactly two
  same-color conflicts whose vertex sets intersect in exactly four vertices.
  The starts split 11 clique pairs and 11 independent-set pairs; the finals
  split 21 clique pairs and one independent-set pair.
- This explains the observed plateau topology but is not a theorem about all
  \(E=2\) graphs. Result SHA-256:
  `f8d506f1161c936e05594aae9f97453537929e4dd5cc14ca3fae657819a78655`;
  checker SHA-256:
  `7542e0281d33afe5379af3b2142c2117b2cc6d4217ae5a524159e0916e9d357a`.

## 2026-07-24T03:34:21Z — Lossless SMS transcript archival

- To relieve shared-disk pressure, the completed 120-second and 900-second
  SMS symmetry transcripts were compressed with pinned Zstandard only after
  their already-recorded raw hashes were rechecked.
- Both archives passed `zstd -t`; streaming decompression reproduced raw
  SHA-256 values
  `32243570f01b3188215a2f29adddf4d1574243ef2212a5a1672f8cb8ec2855b3`
  and
  `89f7f39e411b23b4cd04ddbcf72a57ab157a8e3aacc015af8db517dbf91bad3c`.
  The 96,385,144 raw bytes are exactly recoverable from 5,669,316 archived
  bytes.
- Only the two verified raw copies were removed. Archive-manifest SHA-256:
  `6f3974d54944210c5253d86354e8f9a5816cac1f21fcf9de57166a9115c0c352`.

## 2026-07-24T03:53:46Z — Elite-pool path relinking, partial coverage

- A hash-frozen, topology-neutral two-parent path-relinking portfolio passed
  its preregistration audit, then completed 10/22 directional jobs and exactly
  100,000/220,000 registered repair moves before its immutable 200,000,000-byte
  live disk reserve stopped the run. It was not resumed or overwritten.
- Fresh Python and C++ graph-verifier replays plus the retained independent
  structural audits accepted all ten finals. All were E=2: eight C5-only and
  two I5-only; all retained the same-color, four-vertex-overlap topology.
- **REPRODUCIBLE COMPUTATIONAL OBSERVATION:** no E=0 or E=1 was found in the
  completed fraction. This is neither a construction nor a proof or evidence
  of nonexistence; 12 registered jobs were not executed.
- Partial summary SHA-256:
  `9aa63223f94c1972becb955f0a60d767464999de39ba87cc8062ecf989fcbf44`;
  report SHA-256:
  `00be4704d753371bda7c9f210850a22a10e98838b876cd2f0589d900966ec291`.

## 2026-07-24T04:05:05Z — Exact three-branch global degree cover

- Define
  \(\mu(G)=\min\{\delta(G),42-\Delta(G)\}\), orient by complement to
  realize \(\mu\) as the minimum degree, and relabel a minimum-degree vertex
  to 0. The global degree theorem gives \(\mu\in\{18,19,20,21\}\), with
  every oriented degree in \([\mu,42-\mu]\).
- **CERTIFIED DECOMPOSITION IDENTITY:** \(\mu=21\) would force a
  21-regular graph on 43 vertices, contradicting handshake parity because
  \(43\cdot21=903\) is odd. Thus the unrestricted global formula is exactly
  covered by only three branches:
  degree-0/whole-graph intervals \(18/[18,24]\), \(19/[19,23]\), and
  \(20/[20,22]\).
- The stronger intervals reuse existing forward-counter variables. Branches
  19 and 20 each need 86 auxiliary threshold units in addition to 42 star
  units; branch 18 needs only the 42 star units. No new counter, variable,
  or materialized branch CNF is required.
- An independent checker reconstructed the complete 65,403-variable layout,
  verified threshold semantics for every possible degree, and covered all
  28 possible minimum/maximum pairs. The unique parity case was
  \((21,21)\); result `valid: true`.
- Branch 18 has a further exact 352,366-way split using the complete
  \(\mathcal R(4,5,24)\) antineighbourhood catalog. Each cube fixes 42 star
  and 276 antineighbourhood variables, leaving 585 primary variables.
- Frozen plan SHA-256:
  `f21df79e827b75b1800861d3ca42c088af0ed8cce5a55829036b58e8a9ce8e5b`;
  independent check SHA-256:
  `842a811ca05faa83033b3e8dfdd20189676e782434bdf40e8c377ecde7d44194`.
  This is an exact cover only, not a SAT/UNSAT result.
- A multiplicity audit recorded the exact rooted identity
  \(5M_5=\sum_v(K_4(N(v))+I_4(\overline N(v)))\). Degree-only and
  one-root edge-extremal LP relaxations cannot force \(M_5\ge1\): their
  allowed excess interval contains zero at every degree 18 through 24.
  Any viable finite flag certificate must use joint overlap information.

## 2026-07-24T04:09:22Z — Streamed branch-18 catalog-cube pilot

- The complete \(\mathcal R(4,5,24)\) catalog was streamed through memory
  without retention. Its 352,366 records, 16,913,568 bytes, and SHA-256
  `83ca4028f206b2fa4315ef219b8c2c57c7835209673dd8183d8fb4353bd4fdd0`
  matched the audited identity.
- A deterministic sample selected the first record at each edge count
  \(116,119,122,124,127,129,131,132\). Each exact branch-18 cube fixed
  42 star variables and 276 antineighbourhood variables, leaving 585
  primary variables.
- **REPRODUCIBLE COMPUTATIONAL OBSERVATION:** a persistent CaDiCaL 1.9.5
  solve gave each of the eight 318-assumption cubes 50,000 conflicts. All
  eight exhausted the budget; none returned SAT or observational UNSAT.
  Peak RSS was 2,434,547,712 bytes and total wall time was 71.43 seconds.
- The streamability and memory profile are viable, but the naïve cube solve
  is not fast enough for exhaustive coverage. No proof was requested or
  produced, and no negative conclusion follows.

## 2026-07-24T04:26:06Z — Compact branch-18 residual formulas

- Fixing the degree-18 root and one complete-catalog antineighbourhood leaves
  exactly 585 primary variables: 153 inside the 18-vertex neighbourhood and
  432 cross edges. A new residual generator drops every Ramsey clause
  satisfied by the fixed cube and adds compact degree counters only on the
  remaining incidences.
- **CERTIFIED SEMANTIC CHECK:** for catalog lines 1, 37,900, and 297,776,
  an independent checker streamed and simplified the exact 1,925,196-clause
  primary prefix of the audited global CNF. The resulting deduplicated clause
  sequences matched the production formulas exactly, with SHA-256 values
  `3622f01e00cb171ad488fc76f00a0d4e6bb4b786309128486ce5445ea4170a61`,
  `b817c1f16a5062707e4560cd9a0bc72d507871ea003433ea3b9f6ba2949d639b`,
  and
  `a6a06b3fb1fabbbcd1f5622e303cb3f3f9e272b266f9b7603e40c5acd5ad9a31`.
- Each checked formula has about 33.8k variables and 527k--535k clauses,
  versus 65.4k variables and 2.052M clauses globally. All 504 crafted
  A/B counter-boundary checks passed, as did 36 random Ramsey comparisons
  and 36 full 42-vertex degree-acceptance-vector comparisons.
- A proof-free 50,000-conflict pilot on the three formulas exhausted all
  budgets without SAT or observational UNSAT. Peak RSS fell to 878 MB from
  2.435 GB in the assumption-cube pilot; solve times were 3.94--4.45 seconds.
  This is engineering progress only, not a negative result.

## 2026-07-24T04:26:06Z — Targeted branch-20 exact-assumption pilot

- All 22 verified catalog near-misses lie in exact branch 20 and have ten
  degree-21 vertices. A targeted pilot normalized one E=2 start and its
  complement after cyclic relabelings by offsets 0 and 11, producing four
  exact branch-20 states.
- Each state used the audited 128-unit branch assumptions and three
  progressively broader repair phases freeing all edges incident to 6, 8,
  or 12 vertices around the six-vertex conflict union.
- **HEURISTIC OBSERVATION:** no SAT model was found. All four six-vertex and
  all four eight-vertex phases returned unchecked UNSAT within 50,000
  conflicts. Of the four twelve-vertex phases, one returned unchecked UNSAT
  and three exhausted the budget.
- This 12-job experiment is not a cover. The nine unchecked UNSAT statuses
  and three budget exhaustions imply nothing negative about branch 20 or
  global existence.

## 2026-07-24T04:42:36Z — One true global branch-20 phase job

- To separate preferred phases from fixed-edge local search, a fresh global
  run used only the exact 128 branch-20 assumptions. No candidate edge was
  fixed. All 65,403 solver polarities were initialized from one normalized
  E=2 graph and its canonical degree-counter witnesses.
- **BOUNDED GLOBAL CONSTRUCTIVE OBSERVATION:** CaDiCaL exhausted exactly
  1,000,000 conflicts after 538.674 seconds, with 8,003,512 decisions and
  539,629,892 propagations. It found no SAT model and made no UNSAT
  determination.
- The automatically started second phase variant was manually interrupted
  without a registered status after the first job established the
  nine-minute cost; the third variant did not launch. This interruption is
  an explicit resource boundary, not a solver observation.
- This is a genuine global branch-20 job but only a bounded heuristic one.
  Its budget exhaustion gives no evidence of nonexistence.

## 2026-07-24T04:23:27Z — Exact E=2 neutral cycles and barrier escape

- An independent exact audit found that the 22 retained catalog E=2 starts
  generate 22 disjoint 86-state neutral cycles (1,892 labeled states total);
  each cycle toggles 43 distinct edges twice, and every corresponding
  conflict-block final lies on its seed's cycle. The four one-edge barrier
  heights alternate exactly between `(9,9,9,38)` and `(10,10,12,15)`.
- A new in-memory forced-barrier search found no E=0, E=1, or new E=2
  component in 7,568 excursions and 910,881 repair steps.
- The exact barrier-first atomic scan checked 6,826,336 two-flip paths.
  Its retained E≤4 region closed completely under current-conflict edges at
  16,082 E=3 and 73,788 E=4 states, with no E=0, E=1, or off-cycle E=2.
  This finite corpus result is not a global nonexistence claim.
- Independent audit SHA-256:
  `13a5ff1f9572f385d86d89751ff935a8289a321310f40cf5969f5250a731936e`;
  atomic result SHA-256:
  `ee5b937b138f8c63dab8362ac269fda2550e2cd4e75f25810dc8f3d129c67948`;
  report SHA-256:
  `c32521b650b545dfb377cec112f949833c1baa779d6b07c19613a2dd7e2a5264`.

## 2026-07-24T04:52:09Z — Certified full Hamming ball through radius nine

- The preregistered storage gate passed with 12,349,030,400 free bytes
  against a required 4,294,967,296 bytes. The radius-nine formula was then
  generated with 9,888 variables and 1,943,157 clauses.
- **CERTIFIED, LOCAL SCOPE:** the independent checker reconstructed every
  Ramsey and Hamming-counter clause (`valid: true`), Glucose3 returned
  UNSAT after 760,743 conflicts, `drat-trim` accepted the DRAT, and
  `lrat-check` accepted the exact streamed LRAT.
- The LRAT stream was 2,441,593,384 bytes with SHA-256
  `b72d222fb62e5c523e80c874a3e434815e1c8a66f4f736a92ce55c94d9d52a86`;
  its retained Zstandard archive is 519,855,968 bytes. Lossless CNF and DRAT
  archives also passed integrity tests and reproduced their recorded
  uncompressed hashes.
- Therefore no valid \((5,5;43)\)-graph lies within labeled edge-Hamming
  distance at most nine of the core-kick E=2 candidate; any valid graph
  differs in at least ten edges. This is not a global order-43 exclusion and
  does not improve the Ramsey bound.
- CNF SHA-256:
  `68f1b6dc8713d3bf303b5d07a57327b7536ef72fc943af381ead995049239896`;
  solver-result SHA-256:
  `f9db1488a3c72f6e62cea2be89074cc05091208f5e0c57f6d939a7bcf335be7b`;
  archive manifest:
  `certificates/core_kick_full_hamming_radius9.archive.json`.

## 2026-07-24T04:52:01Z — Certified full-graph Hamming radius nine

- The frozen radius-9 preflight passed with 12,349,030,400 free bytes
  against the required 4,294,967,296 bytes. All pinned generator, checker,
  solver, proof-checker, and compression hashes matched before launch.
- **CERTIFIED, LOCAL SCOPE:** no valid \((5,5;43)\)-graph occurs within
  labeled full-graph Hamming distance at most 9 of
  `results/best_candidates/core_kick_seed_20260731.g6`.
- The independently reconstructed formula has 9,888 variables and
  1,943,157 clauses. Its SHA-256 is
  `68f1b6dc8713d3bf303b5d07a57327b7536ef72fc943af381ead995049239896`;
  the structural checker found zero missing clauses and returned `valid`.
- Glucose3 returned UNSAT after 760,743 conflicts. `drat-trim` accepted the
  237,468,766-byte DRAT, produced a 2,441,593,384-byte LRAT stream, and
  `lrat-check` accepted that exact stream. The compressed LRAT SHA-256 is
  `55459457a516206751fb1e6e32bef01615175bc0e0895020c7e2d2fb4d25663d`.
- The CNF and DRAT were losslessly compressed only after both archives passed
  Zstandard integrity tests and streaming decompression reproduced their
  exact recorded lengths and SHA-256 values. The verified raw copies were
  then removed; all three proof inputs remain exactly recoverable.
- Archive manifest SHA-256:
  `719c251b33706aea5847b198a5aec16b3838eb45bca1fe6bfe465d15d48d7f02`.
  The retained proof payload is 601,434,347 bytes.
- Consequence: any valid labeled graph differs from this candidate in at
  least 10 edges. This does not imply global order-43 nonexistence or improve
  the public Ramsey bounds.

## 2026-07-24T04:47:39Z — Complete order-seven side-pair quotient sweep

- A proof-free exhaustive enumeration found 191,394 assignments of the
  30-variable \(C_7\)-invariant \(R(4,5;21)\) side formula. Independent
  shift/block actions partition them into 664 classes; the common six-element
  multiplier action leaves 122 one-side classes.
- The standalone audit checked all six multiplier maps against the complete
  273,696-clause global CNF. A second audit checked generators for independent
  relabelings on both sides, the common multiplier, and the
  color-complementing side swap, including its signed action on all 37,194
  retained pair assignments.
- **EXACT QUOTIENT REPLAY:** the 440,896 ordered side-class pairs reduce to
  220,780 unordered pairs and then to 37,194 pair orbits. Pair-schedule
  SHA-256:
  `cbcb78bd7c2b58669d2241eb109a0cfb9c5b61bb916a151d953ffdacf03cc1ae`;
  pair-audit result SHA-256:
  `cd29189badf8d01f8f02704c14ad9edb19c63bb96ac4b2402d51e5b03b975294`.
- A one-side search over all 122 cubes exhausted 50,000 conflicts on each
  cube: 122 budget exhaustions, no SAT or solver-reported UNSAT, and 6,100,097
  total conflicts in 314.479 seconds.
- The complete pair schedule then ran in two no-write interleaved shards.
  Each visited 18,597 representatives. All 37,194 outcomes were
  `OBSERVED_UNSAT_UNCHECKED`; there were zero SAT results and zero
  200,000-conflict budget exhaustions. Combined conflicts: 33,414,211.
  Aggregate summary SHA-256:
  `1e68fe4d91dc11359e58ef93edf199e299b6efe925d4013032768c5664792bb2`.
- **CERTIFIED STRATIFIED SAMPLE:** twelve evenly spaced pair representatives
  each passed Glucose3 UNSAT, DRAT verification, DRAT-to-LRAT conversion, and
  LRAT verification. Median zstd-19 sizes were 820,377 bytes for DRAT and
  129,564 bytes for LRAT; the combined median projection for all 37,194 pairs
  is 35,353,510,701 bytes, with a maximum-sample projection of
  49,971,477,984 bytes. The full bundle was not launched because this exceeds
  the safe storage envelope. Sample result SHA-256:
  `816509592ffd17d293e571bf1a857bc7983706926d50168b4d93ed67b10631dc`.
- A second checked run measured indexed cross-proof compression. Concatenated
  zstd-19 LRAT used 1,008,300 bytes versus 1,806,339 bytes for the twelve
  separately compressed LRATs, giving a 3,125,225,850-byte average-scaled
  estimate. The conservative gate instead uses the sample's largest
  individual LRAT: 16,022,580,096 projected retained bytes plus a
  4,294,967,296-byte reserve, for 20,317,547,392 required prelaunch bytes.
  Available space was 12,266,602,496 bytes, so the LRAT-only full run remains
  frozen. Concatenation result SHA-256:
  `f2aac44403c007fc7cef8d72f396e4eff857ef7aef06b3b60721f55285819a97`.
- Claim boundary: the action/quotient replay is exact relative to the
  proof-free side-model enumeration, and the twelve sampled pairs are
  certified. The complete negative sweep has no proof artifacts and does not
  certify nonexistence in the automorphism class or globally.
- Full report SHA-256:
  `bab52528a3c59e3c6df031ebd41bd66d99a3077ea2db4bb1b0ee55ac44a00a2a`.

## 2026-07-24T04:52:16Z — Order-five \(5^8 1^3\) structural split

- Independent orbit builders agree on 183 variables, 192,054 unique five-set
  signatures, 384,108 clauses, and hypothetical DIMACS SHA-256
  `8abb891e769995940c06f403bb261b8d4e4c7c5d03749b7a13ca445182c4b7c6`.
- The degree interval 18--24 forces each of the three fixed vertices to see
  exactly four of the eight moved cycles. Complementation, fixed-vertex
  relabeling, and cycle-block relabeling reduce the exact cover to 21
  edgeless-fixed-triangle types and 38 one-edge types.
- Two complete proof-free sweeps observed UNSAT on 58 of the 59 types in
  union. The common survivor has one fixed edge and all eight membership-cell
  counts equal to one.
- Refining that survivor by the 80 exact internal-C5 orientation orbits gave
  observed UNSAT on 68 orientations in the union of two runs; 12 exhausted
  both budgets. MapleChrono and Glucose4 also exhausted their budgets on the
  unrefined survivor.
- No negative proof was produced. This does not exclude the automorphism
  class. Full report:
  `certificates/order43_automorphism5_eight_cycles_three_fixed.report.md`.

## 2026-07-24T04:52:16Z — Certified exclusion of cycle type \(13^2 1^{17}\)

- Independent builders agree on a 195-variable base orbit formula with
  76,132 unique signatures, 152,264 clauses, and unsymmetrized DIMACS
  SHA-256
  `089d798347c2e991ce4c3c45aa879600e3edceabae7e97bae7079b6f9a7255e3`.
- For every fixed vertex, the degree expression \(13m+d_F\) and global
  interval 18--24 force \(m=1\) and \(5\le d_F\le11\).
- Fixed-vertex relabeling sorts the first-cycle incidence bits; exchange of
  the two moved cycles makes the ninth bit false. The resulting exact
  symmetry-broken formula adds 51 clauses and covers all normalized group
  sizes 0 through 8.
- The independent checker matched all 152,315 clauses. CNF SHA-256:
  `0a333f157833291de463c02bc4632ae9f66c0515b94cbd9e4b2d5a10260cc318`.
- **CERTIFIED UNSAT:** Glucose3 used 265 conflicts. DRAT SHA-256
  `8f299aea27d59c0a3142ebb533a96a70d828b526f964efd57d424da940d2b568`
  passed `drat-trim`; LRAT SHA-256
  `b7c01d9f20673a2433722ab86288430ae2967861b811c99583763ad6aac03032`
  passed `lrat-check`.
- Consequence: no order-43 Ramsey(5,5) graph admits cycle type
  \(13^2 1^{17}\). The distinct type \(13^1 1^{30}\) is outside the scope;
  this is not a global bound. Full report:
  `certificates/order43_automorphism13_two_cycles_symmetry_broken.report.md`.

## 2026-07-24T04:58:20Z — Frozen radius-ten ladder stop

- The preregistered radius-ten storage preflight passed with 12,248,367,104
  free bytes against the required 4,553,221,036 bytes. All pinned source and
  tool hashes matched before launch.
- The independently checked formula has 10,781 variables and 1,944,942
  clauses. CNF SHA-256:
  `cbe399bdce8025691609cbd5ce1cf2f966f6fe1bee38e02d45ac8ab23c0feff5`;
  the structural checker returned `valid` with zero missing clauses.
- Glucose3 exhausted the frozen 300-second solver budget after
  300.087406 seconds. It returned neither SAT nor UNSAT, and therefore wrote
  no DRAT or LRAT proof.
- Result SHA-256:
  `7779e08924e6d149f0681fae9fbd6b3f83863cf3f056fc01fffab9dddf4c4e21`.
  This is a resource boundary only: it provides no evidence for either
  existence or nonexistence at radius ten.
- Per the frozen radius-9--12 plan, the first timeout terminates the ladder.
  Radius eleven was not launched. Radius nine remains the largest certified
  full labeled Hamming ball around this candidate.

## 2026-07-24T04:58:18Z — Radius-ten ladder stop

- The radius-ten formula was generated only after the frozen storage gate
  passed. Its 10,781 variables and 1,944,942 clauses exactly match the
  preregistered counts.
- **CERTIFIED ENCODING ONLY:** the independent structural checker
  reconstructed all 1,925,196 Ramsey clauses and 19,746 Hamming-counter
  clauses, found no missing clause, matched the metadata and DIMACS counts,
  and returned `valid: true`. CNF SHA-256:
  `cbe399bdce8025691609cbd5ce1cf2f966f6fe1bee38e02d45ac8ab23c0feff5`.
- **RESOURCE-LIMITED OBSERVATION:** the pinned Glucose3 proof-producing
  solve reached its preregistered 300-second wall limit. The result is
  `TIMEOUT`; no SAT model, UNSAT result, DRAT, or LRAT was produced.
  Result SHA-256:
  `7779e08924e6d149f0681fae9fbd6b3f83863cf3f056fc01fffab9dddf4c4e21`.
- The frozen execution rule therefore stops the local-radius ladder here.
  Radius ten remains unresolved, and radii eleven and twelve are unrun.
  Nothing negative is inferred from the timeout.

## 2026-07-24T05:16:33Z — Two structural basins behind all 22 E=2 cycles

- **CERTIFIED FINITE-CORPUS CLASSIFICATION:** nauty 2.9.3 dense and sparse
  canonical-labeling paths agree that the 22 independently replayed E=2
  candidates comprise only three graph-isomorphism classes and two classes
  modulo complementation. The complement-class sizes are 10 and 12.
- The eleven clique-conflict candidates form one isomorphism class; the
  exceptional independent-conflict candidate from catalog line 24 is the
  complement of that class. The remaining ten independent-conflict
  candidates form the second complement class.
- Deleting any of the four common conflict-core vertices from each candidate
  produced 88 order-42 graphs. Direct all-five-subset enumeration and a
  recursive-bitset graph/complement search both accepted every deletion.
- The 88 labeled deletions collapse to four isomorphism classes and two
  classes modulo complement. Both complement classes are already represented
  by catalog lines 42 and 256. Thus this exact transformation produces no
  new order-42 seed class, but proves that the apparently diverse near misses
  all funnel back to two existing catalog basins.
- Candidate-class audit SHA-256:
  `07969bcbbfb62fcd1e40ef3d2fb718816b1f5630c71db67c9e9a53322ed2be7b`;
  deletion audit SHA-256:
  `7692195c4fc76d469de1ee204e5f2a0f64612f528af96d7ba0b2ddf4a6099c0e`.
  Full report:
  `certificates/e2_near_miss_isomorphism_collapse_v1.report.md`.
- Scope: this is exact for the fixed 22-candidate corpus only. It neither
  classifies all order-43 E=2 graphs nor changes a Ramsey bound.

## 2026-07-24T05:27:15Z — Exact optimum extensions of basin cores 42 and 256

- **CERTIFIED, FIXED-CORE SCOPE:** catalog lines 42 and 256 each have
  one-vertex extension optimum exactly \(E=2\), and each has exactly two
  optimal 42-bit neighborhoods. One neighborhood produces two five-cliques;
  the other produces two independent five-sets.
- Every core \(K_4\) and independent four-set received a definitional
  conflict variable, an exact counter imposed at most two conflicts, and the
  two observed primary assignments were blocked. Independent checkers
  reconstructed all 25,492 clauses for line 42 and all 25,635 clauses for
  line 256 and directly replayed the four full-graph conflict sets.
- Glucose3 returned UNSAT on both blocked formulas. Both DRAT proofs passed
  `drat-trim`, and both derived LRAT proofs passed `lrat-check`.
- Line-42 CNF/DRAT/LRAT SHA-256:
  `7cbe0a232d3f6d4e1589229161780e85bb125f1150ed367360a582c2ec3a7521`,
  `92eb542bc9cce47dd0db40334416a057b013d20f31c085e6ba12420a7494c119`,
  `0003e1b0cd965f9c3d739b7fb06fa989242109c8765fbc3cfe625590a338f3af`.
- Line-256 CNF/DRAT/LRAT SHA-256:
  `5320d4a265a17099ef9edca1d8b55634429265dfbf37737ba4aadd8ee7766127`,
  `033185af3c4d6207100ed9b41c5453856f5037481e688551d7462a90276c1845`,
  `d84c203204b072f6ea3cf37dfe522b9f557cd203b9d57c90799b4c254bbd2cfe`.
- Canonical labeling sends the two clique-conflict extensions to the same
  near-miss class and the two independent-conflict extensions to the same
  second class. This exactly explains the two dominant attractors in the
  22-candidate corpus.
- A first independent checker run failed closed because it compared a
  four-vertex core constraint with a five-vertex full conflict without
  appending the new vertex. No proof was attempted under that check. The
  corrected checker and regression assertion passed before the proof plan
  was frozen.
- Full report:
  `certificates/catalog42_lines42_256_exact_e2_extensions.report.md`.
  Scope: this does not classify other order-42 cores or arbitrary order-43
  graphs.

## 2026-07-24T05:02:37Z — Certified prime-order cycle types and complete \(p\ge23\) audit

- Generated exact, unsymmetrized edge-orbit CNFs for three complete
  automorphism cycle types. Canonical cycle labeling is justified by
  conjugacy of permutations of the same cycle type; no additional symmetry
  clauses or degree lemmas were used.
- Independent clause-by-clause reconstruction and pinned
  Glucose3 \(\to\) DRAT \(\to\) LRAT certification succeeded:
  - \(19^2 1^5\): 57 variables, 95,752 clauses, CNF SHA-256
    `2ae53ed6f28a776bb72e3d758d740b3ceace08801cf0a6b28088a4a4bb1e5c2f`;
    425 conflicts; DRAT SHA-256
    `a16bc8fdb19d4725f478ddb2461c371703d95636eee43198a9a8595910ec4d41`;
    LRAT SHA-256
    `7180a54dd25009aca4904fcbf4dd1d7b5ea2c917ce031a19aff51f0bc1f7999c`.
  - \(17^2 1^9\): 87 variables, 106,800 clauses, CNF SHA-256
    `c945599f5938385d5ffb918e7ce2c2969de2e9a0d7913d6624db0aeea77ad58f`;
    1,662 conflicts; DRAT SHA-256
    `297239d06317f031a8e9bd385493feb441f308e99757661e99d66dc1db9c655e`;
    LRAT SHA-256
    `387c38f75ebde2c3e7f66a487c97b08082d03afe953bcd930dc8ad93e5f2614a`.
  - \(11^3 1^{10}\): 123 variables, 172,110 clauses, CNF SHA-256
    `2ed2f0f830a63912d879b45237c0a1829a1f829c9074c81e67f4aceb1be46b7c`;
    52,789 conflicts; DRAT SHA-256
    `bc2359707733d91ac922b251f474cfe88e6a01af2bd216a3c1dca038425b2475`;
    LRAT SHA-256
    `20e1cacca12b268ef7a174672ce7acf6f7d7cb5bdbf05737ac5475bd67e07bfa`.
- Formalized the fixed-vertex degree exclusions for
  \(29^1 1^{14}\), \(31^1 1^{12}\), \(37^1 1^6\), \(41^1 1^2\),
  and \(13^3 1^4\).
- Checked the full \(23^1 1^{20}\) argument. If \(L\) denotes fixed
  vertices adjacent to the 23-cycle, cross-edge counting forces
  \(|L|\in\{0,1,19,20\}\). Complementation reduces to 0 or 1; the fixed
  graph then contains a clique of order at least 10 or 19, respectively.
- Together with the existing certified \(43^1\) circulant exclusion, every
  prime-order cycle type with prime at least 23 is now excluded.
- The artifact-bound coverage checker returned `valid: true` over all 65
  prime-order cycle types, 11 covered and 54 uncovered. It explicitly
  reports `classification_complete: false`; no full automorphism
  classification is claimed.
- Coverage checker SHA-256:
  `6e8a84d1a9eda927656bbaf1a69ee0a395efcdb0bbaa26e26ce05ef467864b6f`;
  result SHA-256:
  `2e0997931e300faf3bf3e8a0dc4615ae747f59169b1432edb8d6e09c7b57e7af`;
  four tests pass. Full report:
  `certificates/prime_automorphism_cycle_type_exclusions.report.md`.

## 2026-07-24T05:07:14Z — Degree-strengthened maximal prime-cycle certificates

- Preregistered, generated, and independently reconstructed three
  fixed-degree-strengthened orbit CNFs. The fixed-vertex clauses exhaustively
  forbid all incident-orbit assignments whose weighted degree is outside the
  theorem-implied interval 18--24.
- **CERTIFIED UNSAT:** \(19^2 1^5\) has 57 variables, 95,752 Ramsey clauses,
  160 degree clauses, and 95,912 clauses total. Glucose3 used 428 conflicts.
  CNF SHA-256:
  `f9e3b5f323748138aa53e8480f7887a8ed8aae0bef34762e517202b2ec358643`;
  DRAT SHA-256:
  `f478e3fada3b93f9491a3ce154137ca630ea7a7ac3d9f61453598c54048f48cd`;
  LRAT SHA-256:
  `e0198c9df0d4f02ceb377a50a1cc710a174668cc96bbf68d3c11c1e80fc6034a`.
- **CERTIFIED UNSAT:** \(17^2 1^9\) has 87 variables, 106,800 Ramsey
  clauses, 4,644 degree clauses, and 111,444 clauses total. Glucose3 used
  1,519 conflicts. CNF SHA-256:
  `f08ce8bfb2e5b7d0d82f1cc5893b8df5cb9a7e72c744af2a131a31a55b16d859`;
  DRAT SHA-256:
  `5d8df16b4c5862b68d45ea1340e3d7197f0b432fcd6c666069d7a364a8d2de81`;
  LRAT SHA-256:
  `08b9451eeeeeff0a58efa2ce9e643f2c598e1d56e08b7c9323a4f10be3c7fff5`.
- **CERTIFIED UNSAT:** \(11^3 1^{10}\) has 123 variables, 172,110 Ramsey
  clauses, 38,200 degree clauses, and 210,310 clauses total. Glucose3 used
  24,458 conflicts. CNF SHA-256:
  `5820693762b36869935e3bb16b8ea5bf05f8c221d79b36c999447518f19c9775`;
  DRAT SHA-256:
  `6d1edc45c30c86b83ee98ac7f2868a60863332e533daf7b1d3ac451355cffe5e`;
  LRAT SHA-256:
  `cf2a80990b51d155574a9aa5b93fc60692b27874db4f0706f6d78459df3b77bf`.
- Fresh replay gave 3/3 unit tests, 3/3 structural checks, 3/3 DRAT checks,
  and 3/3 LRAT checks. The preregistered plan SHA-256 is
  `6721a5dac42184ded504af241f79f719e304e1272c2aa9565a314e0fee83d946`.
- A focused arithmetic checker independently confirmed the direct degree
  exclusions for \(13^3 1^4\), \(29^1 1^{14}\), \(31^1 1^{12}\),
  \(37^1 1^6\), and \(41^1 1^2\). It also checked every cross-edge bound in
  the \(23^1 1^{20}\) argument: only \(|L|=0,1,19,20\) survive, and the two
  complement representatives force a \(K_{10}\) or \(K_{19}\).
  Checker/result SHA-256:
  `2c7544b46fc83cc1341457c17c594c6f3f146592a697614547f8693689051254` /
  `0813d383b5c6101304ce7f7f321d910e0cf2bb8c72190fbc8947eb4939c9c8d6`.
- Claim boundary: these artifacts cover exactly the listed cycle types. The
  degree argument does not cover \(43^1\), which has no fixed vertex, and no
  unlisted prime-order cycle type is inferred.
- Full report SHA-256:
  `b87571bf5111346b4f9a0b050f06e0de19fe798561c89f2722e63510d9872be9`.

## 2026-07-24T05:34:00Z — Exact order-3 formula and low-storage maximal-cycle search

- **CERTIFIED ENCODING AND REDUCTION:** the cycle type \(3^{14}1^1\)
  gives 301 size-three edge orbits. Exhaustive in-memory generation found
  320,593 distinct five-set signatures and 641,186 Ramsey clauses. The
  canonical unmaterialized DIMACS SHA-256 is
  `2cb249c2d09d00bd199be27711fc344873785b9e9756dc1cafad8f756084a5e5`.
- A separately written algebraic orbit builder reconstructed the full
  formula and signature histogram. It also checked the fixed-vertex
  reduction: degree 18, 21, or 24 means 6, 7, or 8 neighboring 3-cycles;
  complementation exchanges 6 and 8, so \(t=6,7\), normalized by \(S_{14}\),
  cover the class.
- The independently checked \(R(4,5)\) side formulas for 6, 7, and 8 moved
  cycles have respectively 51/3,831, 70/8,715, and 92/17,626
  variables/clauses. Fixing both side models leaves 144 cross variables for
  \(t=6\) and 147 for \(t=7\).
- **REPRODUCIBLE COMPUTATIONAL OBSERVATION:** three SAT engines, two phase
  seeds, and both normalized raw cases gave 12/12 budget exhaustions at
  100,000 conflicts. A three-stage side-gluing portfolio then tested 448
  distinct pairs in each case, 896 total. It observed 94 solver-UNSAT cubes
  and 802 budget exhaustions after 15,655,882 total raw-plus-gluing
  conflicts. No SAT model was found.
- The 427,468-byte search summary SHA-256 is
  `2de0ceec127b1d66eed4b835ebe709cf7caa7c493a1adef8e421e938b6da7810`.
  The independent result checker reconstructed all schedules and returned
  `valid: true`; checker-result SHA-256:
  `eeb15bf74ebcb1565bb64620272acf69537ce2f4036d58e8d900eb31bc361aef`.
  Formula-audit SHA-256:
  `4cbf533e91341743c13392f69957917639e6d86bf8c0e62c41e50458b6ee38a1`.
  Five structural tests pass.
- A proof-free side diagnostic enumerated at least 5,000 distinct
  \(C_3\)-invariant order-24 \(R(4,5)\) models before deliberate
  interruption, confirming that the tight side pool can be broadened; this
  was not an exhaustive count.
- **CLAIM BOUNDARY:** no negative outcome has a retained proof. The
  \(3^{14}1^1\) class remains unresolved, arbitrary order-43 graphs remain
  outside scope, and the Ramsey bound is unchanged. No CNF, DRAT, or LRAT
  was written. Full report SHA-256:
  `0ac3688146bdeec677b592b1771896e2ad00663cf1059c0ce72c1557bbbf7efb`.

## 2026-07-24T05:30:57Z — Selector-lifted order-seven certificate design

- Implemented selector-guarded proof lifting for the existing twelve
  order-seven pair samples. For cube \(C\), a fresh selector \(s\) encodes
  \(s\leftrightarrow C\); every learned clause \(D\) becomes
  \(D\vee\neg s\). The terminal \(\neg s\) derives the ordinary blocker
  \(\neg C\). The temporary derivation is then deleted and \(\neg s\) is
  rederived from that blocker, so the final selector-cover contradiction
  cannot bypass any blocker.
- Every regenerated cube formula and raw Glucose3 proof matched the prior
  sample byte for byte. Of 3,198,756 proof records, 3,178,562 were deletion
  records and only 20,194 were additions requiring lifting.
- **CERTIFIED TWELVE-CUBE UNION:** the single lifted DRAT stream is 1,353,389
  bytes (222,872 zstd-19). `drat-trim` accepted it and produced an
  8,345,121-byte LRAT (1,190,987 zstd-19), which `lrat-check` accepted.
  DRAT/LRAT SHA-256:
  `21f45915e7bbb84c1bf93292c7aee014947d8e603695edd4a63e50a4a0be413f` /
  `07bd1eadbcfe5c0a19984905449d34bf63334ef78b96ff90b96102c0cfecb264`.
- The independent checker reconstructed the 274,435-clause wrapper exactly,
  audited every segment's guarded clauses, blocker, deletions, and
  blocker-dependent selector rederivation, decompressed both archives, and
  regenerated the identical LRAT. Result/check SHA-256:
  `2961f48127ce5628d69d15b0d586ccefb34f1b0480329fa1abb2446350ab6382` /
  `72be0d62ed38a4aba6d8b3b087894ab38e2e02fe40280b24f2b6eb395f6870a5`.
- Average scaling to 37,194 pairs gives 690,791,764 compressed DRAT bytes,
  versus 3,691,464,207 compressed LRAT bytes. The largest sampled raw
  segment scales to 20,609,604,534 bytes, so raw monolithic retention is
  rejected.
- Audited a separate frozen 128-shard design. The prospective monolithic
  wrapper has 37,323 variables, 2,542,537 clauses, 47,178,247 bytes, and
  SHA-256
  `b04067d3bd3c1e4b68f88a29a4271695128afc8008c9f4768261f4266281dabd`.
  Each shard has 290 or 291 pairs and a wrapper of at most 10,566,888 bytes.
- The new hard storage envelope allows 2 GiB retained compressed pair DRAT,
  512 MiB exact-cover artifacts, 2 GiB transient work, and a 4 GiB reserve:
  9,126,805,504 bytes required. The storage subgate passed with
  12,110,962,688 bytes available. It does not authorize execution.
- The design remains `FROZEN_NOT_LAUNCH_READY`: a side-model exhaustion LRAT,
  a hash-pinned full runner/checker, and one full-size shard pilot are still
  missing. The existing 20,317,547,392-byte conservative gate remains
  unchanged and frozen. No unsampled pair was run.
- Frozen-design/audit-result SHA-256:
  `36bb3b19006df33086857daaac6ab693d6d63a1bb1d14eab2ebc9b13950c78c0` /
  `ecba883848d6f40760c84abbd01c599fd13646f63ca06f84e862bbb43ff3b589`.
- Full report SHA-256:
  `309cf02cbe33f70e9292834dbdebcb18c40960ff38dadd5717ebe49a34b30a3a`.

## 2026-07-24T05:41:48Z — Exact Ramsey-anchor cover for degree branches 19 and 20

- For either normalized root degree \(d=19\) or \(20\), put
  \(A=N(0)\) and \(B=V\setminus(A\cup\{0\})\). By \(R(4,4)=18\),
  `G[A]` contains an \(I_4\) and `G[B]` contains a \(K_4\). Relabeling
  these anchors reduces their \(4\times4\) cross matrix under
  \(S_4\times S_4\).
- **CERTIFIED EXACT COVER:** an independent checker enumerated all 65,536
  matrices, found exactly 35,714 avoiding an all-one row and all-zero
  column, and partitioned them into exactly 143 orbits. It reconstructed all
  143 cubes in each degree branch with zero assumption/hash errors.
- A compact union CNF uses 143 matrix selectors, ten selectors for the
  forced triangle in `A` and independent triple in `B`, and 6,630
  primary-only clauses sorting the remaining eight-bit anchor signatures.
  The checker exhaustively validated the lexicographic template through
  width eight.
- The two preferred formulas each have 65,556 variables and 2,061,223
  clauses. Their SHA-256 values are
  `7540802b0e2b85256e85ed1a67ba6a9ca1736d703a025201ee8a2244c7c10ae8`
  for degree 19 and
  `19f7d3a00ce8b491627cc063cb7b9584fce6619ca94416ada5926a19cf7ea7f6`
  for degree 20. Independent streaming checks matched all 2,052,132 base
  clauses followed by exactly 9,091 reconstructed additions.
- Sound optional internal-degree bounds were also encoded and checked:
  \(d_A\in[1,13]\), \(d_B\in[9,17]\) in branch 19 and
  \(d_A\in[2,13]\), \(d_B\in[8,17]\) in branch 20. The 84 redundant
  counters were slower than the lean encoding in the matched pilot and are
  retained only as an optional strengthening.
- **BOUNDED PERFORMANCE OBSERVATION:** at 50,000 MapleChrono conflicts, the
  lean union used 1.890/2.291 solver CPU seconds in branches 19/20 versus
  9.393/8.958 seconds for exact 128-assumption baselines, reductions by
  factors 4.97 and 3.91. Every job exhausted its budget; no SAT model or
  UNSAT proof was produced.
- A pinned source audit records useful but source-dependent side-edge ranges:
  branch 19 has \(e(A)=57\ldots92\), \(e(B)=131\ldots152\); branch 20 has
  \(e(A)=68\ldots100\), \(e(B)=117\ldots143\). Endpoint completeness was
  not independently re-enumerated, so these ranges were not added to the
  preferred certificate formula.
- Preferred certificate architecture: one checked selector-union CNF and
  DRAT-to-LRAT proof per degree. Alternative: 143 checked cube proofs per
  degree plus the certified cover manifest. Either route covers only
  branches 19 and 20; degree 18 remains separate.
- Plan/check SHA-256:
  `c4f7bc7e1e6191c81006530ca5204ef81e79ddb4403dbc790bedd77865cec28a` /
  `ad3355a578e5688f07706e923d8265db801b96816506960edcddff6ea54eedab`.
  Full report SHA-256:
  `2a6c9936971a6473086e256c86f64a47f1fb51bc0b66683ebfc7a38fe36dc012`.
- **CLAIM BOUNDARY:** this is an exact decomposition and checked encoding,
  not a negative solution. Neither branch is excluded and no Ramsey bound
  changes.

## 2026-07-24T05:41:00Z — Exact 253-profile cover of global branch 20

- For the minmax-degree-20 branch, write
  \((a,b,c)=(n_{20},n_{21},n_{22})\). Handshake parity makes \(b\) even,
  hence \(a+c\) odd and \(a\ne c\). Complementation swaps \(a,c\);
  orienting by \(a>c\) and sorting labels by degree leaves exactly 253
  profiles.
- **CERTIFIED EXACT COVER:** an independent checker enumerated all 506
  parity-admissible triples, verified 253 fixed-point-free complement pairs,
  reconstructed every exact-degree threshold unit, and matched the frozen
  plan with `valid: true`.
- The compact selector union has 65,656 variables and 2,073,891 clauses.
  Its 21,759 additions were independently matched after all 2,052,132 base
  clauses. Materialized CNF SHA-256:
  `ed76ec38bddd848cde9cc681c3b7c5ed18a4bde668e3d899a6a50a8fc7cc964b`;
  materialized-check SHA-256:
  `175fff9f64affd2ea3d262cb41cb1200a0a2ef0586a805d0d80f49461889ee35`.
- A second exact symmetry encoding completed the existing edge counters with
  62,694 reverse clauses and sorted whole-graph degrees independently inside
  the normalized root's two sides. Its independent small-counter and
  materialized-CNF checks pass; degree-20 CNF SHA-256:
  `e5b54bb0f5ceb383f8276852d4e6f285c64c079256d2ea405f53df11828c5956`.
- **PROOF-FREE HARDNESS OBSERVATION:** the selector union exhausted a
  50,000-conflict MapleChrono budget. A persistent CaDiCaL screen exhausted
  5,000 conflicts on each of the 32 profiles nearest a retained \(E=2\)
  profile, 160,015 conflicts total. There was no SAT model or observational
  UNSAT, and 221 profiles were not screened.
- No negative inference follows. These are exact decompositions and bounded
  measurements, not a branch exclusion or a Ramsey-bound change.
- Plan/check/result SHA-256:
  `ad2ae74430f3e979dc711fe35a852bc84bfd431aa9a92ec10bf11f613c50edc7` /
  `db43a3e8f416e720fe04d009628cfb4e7222a8698f5a858d969a8175f21c2064` /
  `287ff92fadcccfcb4ba57e11953c97d33f6e269d77d1b46e7611ec30a8092eda`.
- Full report:
  `certificates/global_degree20_profile_cover.report.md`.

## 2026-07-24T05:46:18Z — Exact 44,275-profile cover of global branch 19

- For the exact minmax-degree-19 branch, write
  \((a,b,c,d,e)=(n_{19},n_{20},n_{21},n_{22},n_{23})\), with
  \(a+e>0\). Handshake parity makes \(a+c+e\) even, while complement maps
  the profile to \((e,d,c,b,a)\).
- A complement-fixed profile would have \(a=e,b=d\), forcing \(c\) odd
  because the order is 43, and therefore violating handshake parity.
  Orienting the fixed-point-free pairs by
  \((a,b)>(e,d)\) and sorting vertices by degree leaves exactly 44,275
  profiles from 88,550 admissible labeled multiplicity profiles.
- **CERTIFIED EXACT COVER AND ENCODING:** an independent checker separately
  enumerated all profiles and complement orbits, reconstructed the 86
  false-threshold units per profile, and exhaustively validated exact-degree
  semantics for degrees 19 through 23. Five structural tests pass.
- The selector union has 109,678 variables and 5,859,783 clauses. Its
  3,807,651 additions have stream SHA-256
  `edae0bba35896250ea245a49ec31fc27a5f578e368b90ccb405d138e692eeea1`.
  The 15,126,076-byte plan SHA-256 is
  `63e385365ee787882a455d419460ec95cbee9f5b4207afc5b33093832ff4a9d5`.
- Independent streaming replay matched all 2,052,132 base clauses and every
  appended clause with zero mismatches. The 151,810,283-byte temporary CNF
  SHA-256 is
  `9d19c71875647f624e2b51f4803473ba5957a0e1fb125101123408b29dd266ef`;
  materialized-check SHA-256:
  `6c6bfbbaddc8ea040f2d67a98ceb4a6c6d80da128d7ceeec008dce789bfa944d`.
- **PROOF-FREE HARDNESS OBSERVATION:** MapleChrono exhausted a
  50,000-conflict budget (50,004 observed conflicts, 561,762 decisions,
  61,864,371 propagations) in 105.581548 solver seconds. Peak resident set
  was 2,424,078,336 bytes. Pilot-result SHA-256:
  `98ad122e356fe627490d884dd772cf1d2784fcaa320f675dca4e88495e3d1016`.
- **CLAIM BOUNDARY:** no model or proof was produced. The branch remains
  unresolved; no profile, graph, or Ramsey case is excluded, and the bound
  is unchanged. Full report SHA-256:
  `eab6653d84ca62769cc98b10d3489a66829cd4631f6a8a91b896b4e5bb7a8199`.

## 2026-07-24T05:45:30Z — Exact certificate strategy for cycle type \(3^{14}1\)

- **CERTIFIED ENCODING AND COVER:** independently generated orbit formulas
  agree on 301 size-three edge orbits, 320,593 unique five-set signatures,
  and 641,186 Ramsey clauses. The exact root-neighborhood argument gives
  \(m=6,7,8\); complementation exchanges 6 and 8, and the \(S_{14}\) block
  action normalizes the remaining cases to prefix lengths 6 and 7. The
  checker exhaustively audited all 9,438 labeled degree-allowed root
  neighborhoods.
- The single cover CNF has 301 variables, 641,201 clauses, and SHA-256
  `513b922ae8d7f4ec5fc68f7bac63d7d8c81ffb681c6d4e5a9cc5bba3abcff946`.
  Its independent checker matched every clause and returned `valid`.
- Exact fixed-case simplification gives 571,377 clauses for \(m=6\) and
  570,808 for \(m=7\). A separately checked weighted degree layer constrains
  one representative from each moved vertex orbit to degree 18--24 using
  14,350 auxiliary variables and 56,155 clauses.
- **FULL NORMALIZER QUOTIENT:** a constructive greedy action of
  \(C_3^{14}\rtimes S_{14}\) chooses a maximal-internal reference cycle and
  then a lexicographically maximal oriented block at every position. The
  independently reconstructed preferred formulas have:
  \(17,393\) variables / 643,989 clauses for \(m=6\), SHA-256
  `7f5ee1c01793a7bfe3d4f8bca19e4e4f8f002eaf940a3d4815bb50e8f9cfecd9`;
  and \(17,150\) variables / 641,963 clauses for \(m=7\), SHA-256
  `1ca75cb8c35155952c9c13c4fccb62dadd5d5e4f80139d25fd8583bad7142405`.
  Sixteen focused structural tests pass.
- **PROOF-FREE OUTCOMES ONLY:** Glucose3 exhausted approximately two
  million conflicts on the combined cover and each reduced case, and
  2,251,748 conflicts on the preferred greedy \(m=6\) formula. CaDiCaL
  exhausted 1,000,001 conflicts on the degree-strengthened \(m=6\) formula.
  A later greedy CaDiCaL run and a 63-case internal-count split were
  externally terminated by signal 15 before result JSON was written.
  Interruption-manifest SHA-256:
  `ffe59f528eedf1a9024aa41d4283a32c9b42b99de362be5c6d5fa9b824af00bc`.
- No complete solver run returned UNSAT, so no DRAT-to-LRAT certificate could
  be generated. **The cycle type \(3^{14}1\) remains unresolved**, and no
  global Ramsey bound changes.
- Full report:
  `certificates/order43_automorphism3_fourteen_cycles_certificate_strategy.report.md`;
  SHA-256:
  `c649247b471b19d7d2494e6dec3597c6e5cd2702c2dd4476e9d556f0cade719a`.

## 2026-07-24T05:49:15Z — Certified all-328 catalog \(E\le2\) extension census

- Froze a proof-production protocol after a proof-free exploratory screen.
  The plan binds the 328-line catalog, production generator, independent
  clause reconstructor, tests, solver, proof checker, timeouts, and a
  fail-closed outcome policy. Plan SHA-256:
  `a42a254a563e726feaf36c42be2f7789c920894e96146d4f23e747feeb638c29`.
- **CERTIFIED FINITE-CATALOG THEOREM:** exactly catalog lines 42 and 256
  admit a one-vertex extension with at most two monochromatic five-sets.
  All other 326 supplied order-42 cores are certified to require at least
  three for every one of their \(2^{42}\) new-vertex neighborhoods.
- Every one of 328 formulas was independently reconstructed clause by
  clause and its core independently checked Ramsey. Formula sizes range
  from 9,227 to 9,363 variables and 25,259 to 25,633 clauses; 8,335,860
  clauses were matched in total.
- The two SAT assignments, on lines 42 and 256, were decoded and checked by
  exhaustive enumeration of all 962,598 five-subsets of the resulting
  order-43 graph. Each has exactly two five-cliques.
- Each remaining line produced a Glucose3 DRAT accepted by pinned
  `drat-trim`. The retained 326-proof bundle occupies 158,998,676 bytes and
  has ordered formula/proof digest
  `96a2319b3d82decb2d6910c9753a614dabf166ba9734d49207e02200dad77329`.
- Result-manifest SHA-256:
  `1534f38464bd55180c60981b019258799512595a984011906b8d49a27eef2355`.
  Full report SHA-256:
  `8b217d3938541cc8148f27177fed8b66aba2c09ed300144d390be2b1d9ac5d2c`.
- Combined with the earlier blocked-enumeration certificates, the four
  recorded optimum neighborhoods of lines 42 and 256 are the complete
  \(E\le2\) extension set across the supplied catalog.
- **CLAIM BOUNDARY:** the 328 supplied graphs are not asserted to be a
  complete catalog of all order-42 Ramsey graphs. This theorem is not
  global order-43 nonexistence and does not change \(43\le R(5,5)\le46\).

## 2026-07-24T06:02:50Z — Exact 143-orbit anchor extension to degree 18

- **CERTIFIED EXACT COVER AND ENCODING:** extended the global Ramsey-anchor
  construction to the normalized degree-18 branch without altering any
  degree-19/20 v1 artifact. For the root partition, \(|A|=18=R(4,4)\)
  forces an `A` independent four-set despite zero slack, while \(|B|=24\)
  forces a `B` four-clique.
- Independently audited the secondary witnesses: \(R(3,5)=14\) forces an
  `A` triangle and a `B` independent triple. Each meets its opposite-type
  four-vertex anchor in zero or one vertex, so the disjoint case plus four
  one-anchor cases make the five selectors per side exhaustive.
- Re-enumerated all 65,536 cross matrices independently: 35,714 are
  feasible and form exactly 143 \(S_4\times S_4\) orbits. The canonical
  representative hash
  `7ac386a677a64b1bfe00226a73ffca27957cc2aa355b552b008e74b3d170d97e`
  exactly matches the earlier v1 cover.
- The lean union has 65,556 variables and 2,061,137 clauses. Its 9,005
  additions have stream SHA-256
  `782dd9bfe9d83d74ccf69939e6cbfff5b3060bed29904f0694a20f4bf223e904`.
  Independent streaming replay matched all 2,052,132 base clauses and every
  addition. The 90,757,889-byte working CNF has SHA-256
  `a14a4951041942c01d8787a381c36ca3d094633255a2d134c7879fbec0af78c7`.
- Plan / plan-check / materialized-check SHA-256:
  `3c653a20a3d985921a3bf5b1b25b3744dbddb82fa43c278007e256ed5b161934` /
  `d368da3f32239487917559a3e2b0943d7bdf73200a4b018ed58ed51fa2f00c36` /
  `be5c00086b5f32e046d25ef0aab24e9c8ab8faa2e6a5195d98388fa3dfaa09cf`.
  Six focused tests pass, and comparator semantics were exhaustively checked
  for widths one through eight.
- The degree-19/20 v1 plan, generator, checker, and tests remain
  byte-identical at their recorded hashes. Full degree-18 report SHA-256:
  `e21ca156a4db8c0af29220710631997991c4f4da29ee3b40f8d410807f12112c`.
- **CLAIM BOUNDARY:** no solver was run and no SAT model, UNSAT conclusion,
  DRAT, or LRAT was produced. Degree 18 remains unresolved; this checkpoint
  changes no Ramsey bound.
