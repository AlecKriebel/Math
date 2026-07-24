# Claim ledger

Every entry uses exactly one project evidence category.

## C1 — A verified 42-vertex witness

- Category: **CERTIFIED**
- Claim: the graph reconstructed in `src/construct_exoo42.py` has 42 vertices,
  435 edges, no 5-clique, and no independent 5-set.
- Artifacts:
  - `data/exoo42_constructed.canonical.json`
  - `data/exoo42_constructed.g6`
  - `verify/exhaustive_verify.py`
  - `verify/bitset_verify.cpp`
  - `results/verification/exoo42_canonical_artifact_check.json`
- Hashes:
  - canonical JSON:
    `319df4d75fc4c4758a6985b4961be441be5a08c813e3042ba7fcadcea2f9529a`
  - graph6:
    `a7db2ac21e14b3652629d0cfc1c47bf7b65f355e1f2fcf9048a075622c5ba75a`
  - independent multi-representation audit report:
    `f8a8ef6ab549df28d095b51b1397f9458201e3f8ef7eecb6de04ce9bd1915580`
- Consequence: \(R(5,5)\geq43\).

## C2 — Necessary degree interval

- Category: **CERTIFIED**
- Claim: assuming the formally established \(R(4,5)=R(5,4)=25\), every
  \((5,5;n)\)-graph satisfies \(n-25\leq d(v)\leq24\).
- Proof artifact: the derivation in `literature.md` and its direct
  neighborhood/anti-neighborhood argument.
- Consequences: degree intervals 18–24 at \(n=43\), 19–24 at \(n=44\), and
  20–24 at \(n=45\).

## C3 — Exact flip-delta identity

- Category: **CERTIFIED**
- Claim: if \(t\) is the number of triangles in the common neighborhood of
  \(u,v\), and \(q\) the number of independent triples in their common
  non-neighborhood, then adding \(uv\) changes \(E\) by \(t-q\), while deleting
  it changes \(E\) by \(q-t\).
- Proof/check artifacts:
  - elementary affected-five-set derivation in `literature.md`
  - `tests/test_delta_formula.py`, exhaustive over 491,520 flip cases
  - independent incremental implementation self-test in `src/search43.cpp`

## C4 — Best current 43-vertex candidate

- Category: **REPRODUCIBLE COMPUTATIONAL OBSERVATION**
- Claim: the saved 43-vertex candidate has 454 edges,
  \(C_5=0,\ I_5=2,\ E=2\).
- Artifact:
  `results/best_candidates/exoo_seed_20260724.canonical.json`
- Canonical SHA-256:
  `4c586a4e1026bdd628d04b2c5280dafff7f5dd7f326afa16712c039a2c1b0b65`
- Audit:
  `verify/adversarial_audit.py` passed on the original, a random relabeling,
  and the complement.
- Independent artifact audit:
  `results/verification/best43_canonical_artifact_check.json` checked all
  representations and serialization, report SHA-256
  `f7e31e368d37c8050d0e6a40d7ad08fda4d2b08e3bf517441bdd1256b519fac9`.
- Important limitation: this graph is invalid and proves no improved Ramsey
  bound.

## C5 — Seeded-search improvement

- Category: **REPRODUCIBLE COMPUTATIONAL OBSERVATION**
- Claim: on the first fixed configurations, a random start reached \(E=231\)
  in 7.00 s, whereas an Exoo42-derived start reached \(E=2\) in 17.64 s.
- Artifact: `results/experiments.csv`.
- Source-recovery audit:
  `results/reproductions/search43_2f0a1fba656b7550124f2a213a046c5ace42742d4d8e3c36967eefabe16e3674/audit_20260723T172718Z/audit_manifest.json`
  replayed all four configurations from the current source and reproduced
  every historical graph byte-for-byte. Manifest SHA-256:
  `9f8dcc96eb8bb216ea5416d0c9d092f494a77e931f51d1ec100fa19fc2499ccd`.
- Limitation: one configuration pair is not a general performance theorem.

## C6 — Current public bound status

- Category: **REPRODUCIBLE COMPUTATIONAL OBSERVATION**
- Claim: primary/current sources retrieved 2026-07-23 report
  \(43\leq R(5,5)\leq46\).
- Sources: the maintained Small Ramsey Numbers survey and the final
  Angeltveit–McKay paper, linked in `literature.md`.
- Limitation: the upper-bound computation is literature-established but has
  not been certificate-checked in this repository.

## C7 — Search interpretation

- Category: **CONJECTURE OR HEURISTIC**
- Claim: exact large-neighborhood completion around the six-vertex residual
  obstruction has higher expected information gain than further budget
  increases of the current single-edge breakout search.
- Support: the best two conflicts trade for two conflicts under the best single
  moves, and 796 breakout updates produced no improvement.

## C8 — Fixed Exoo42 one-vertex extension is impossible

- Category: **CERTIFIED**
- Claim: no choice of the 42 adjacencies of one new vertex extends the fixed
  graph `data/exoo42_constructed.g6` to a \((5,5;43)\)-graph.
- Encoding artifact: `certificates/exoo42_extension_sat.cnf`
  - 42 variables
  - 1,148 4-clique clauses
  - 1,170 independent-4 clauses
  - SHA-256:
    `ff372bd968015eb1ee027459679ba2528d0a8c566034e51f37d3f9671bb78160`
- Checked proof artifacts:
  - explicit-unit tree:
    `certificates/exoo42_extension_sat.tree`, SHA-256
    `e30cf3871b12322f3627ab1115d66b72078fc52d0fa30f0036ab9668f624bf66`
  - independently reconstructed compact tree:
    `certificates/exoo42_extension_sat_proof.bin`, SHA-256
    `fd8c5e9886c77ae83d604d34a35e11f7c8bde91215719dc627f95daa6e14c232`
- Checker sources:
  `verify/extension_sat_check.py` and
  `verify/extension_sat_proof_check.py`.
- Equivalence proof and exact commands:
  `certificates/exoo42_extension_sat.report.md`.
- Scope limitation: fixed-core nonextendibility is not global nonexistence of
  \((5,5;43)\)-graphs and is not outcome D.

## C9 — Radius-two local barrier

- Category: **REPRODUCIBLE COMPUTATIONAL OBSERVATION**
- Claim: among every graph obtained from the current \(E=2\) candidate by
  changing one or two distinct edges, the minimum exact objective remains 2.
- Execution: 408,156 exact delta evaluations, followed by a trusted full
  recount of the retained minimum, in 2.939512 s.
- Source SHA-256:
  `2f0a1fba656b7550124f2a213a046c5ace42742d4d8e3c36967eefabe16e3674`
- Artifact:
  `results/best_candidates/exoo_seed_20260724_radius2_best.g6`
- Artifact SHA-256:
  `f5adf13e5791bb8fe4c58941e3d797c283223013290a2376935f1e1eef4ef31a`
- Interpretation: supports, but does not prove, the heuristic need for
  three-or-more-edge or exact large-neighborhood moves.

## C10 — All Exoo42 \(k=1\) replacements are impossible

- Category: **CERTIFIED**
- Claim: for each vertex \(v\) of the fixed Exoo42 graph, the induced
  41-vertex core \(H-v\) has no completion to a \((5,5;43)\)-graph obtained by
  adding two new vertices.
- Encoding: 42 separately labeled CNFs, each with 83 variables and
  6,652–6,702 clauses. No isomorphism or automorphism reduction is assumed.
- Generator/check artifacts:
  - `src/core_completion_sat.py`
  - `src/core_completion_batch.py`
  - `verify/core_completion_batch_check.py`
  - `tests/core_completion_sat_tests.py`
- Certificate bundle:
  `certificates/core_completion_all42/`
- Batch summary SHA-256:
  `37f277e236e1f31cec6327eb279f6bccafbdafd32b85b9809fa5735d3e92493b`
- Independent check summary SHA-256:
  `6b1c1caa25ddf546c104aff20bd5856f23b340dda5c6924e961fc0e8a42051e4`
- Independent formula-reconstruction summary SHA-256:
  `88a9b61872192a083e0068011919ea882b83e53bc4455e2f9cb31f9278b44326`
- Coverage-enforcing rechecks require deletion labels exactly \(0,\ldots,41\):
  - proof-check summary SHA-256:
    `2e54833a541382f894c16d92b493bb40434cbbe661ac42ab77ada3b38443e14e`
  - formula-check summary SHA-256:
    `2e31e66986bfcdce5607983b415c27d198075e0b1556614a97c6c067d0b6c5a8`
- Checked totals: 42 instances, 104,058 proof records, 3,900 branches,
  3,942 conflict leaves, 96,216 unit steps, and 280,376 independently matched
  clauses with zero missing or extra.
- Exact commands and encoding proof:
  `certificates/core_completion_report.md`.
- Scope limitation: this exhausts one-vertex replacement only around this
  particular 42-vertex witness. It is neither a global order-43 UNSAT proof nor
  outcome D.

## C11 — One fixed Exoo42 \(k=2\) replacement is impossible

- Category: **CERTIFIED**
- Claim: deleting original vertices 0 and 1 from the fixed Exoo42 graph,
  preserving the resulting 40-vertex induced core, and adding three new
  vertices cannot produce a \((5,5;43)\)-graph.
- Encoding: 123 variables and 13,338 clauses:
  - 6,739 negative clauses forbidding 5-cliques
  - 6,599 positive clauses forbidding independent 5-sets
- Artifacts:
  - `certificates/core_completion_k2_delete_00_01.cnf`
  - `certificates/core_completion_k2_delete_00_01.tree`
  - `certificates/core_completion_k2_delete_00_01.metadata.json`
  - `certificates/core_completion_k2_delete_00_01.report.md`
- Hashes:
  - CNF:
    `d0678b8c71edeaa5a9e3e99170d6d35fb655a1da2873355eda4116208d03488c`
  - checked tree:
    `a469ea000c190c7b639a819ffdaec81a191ba5f2f037a86fbe4f814ba03887a0`
  - metadata:
    `01442e908a53e1ec6027e69ba628d120827380252bef502cb9eb657894ab12fb`
- Independent checks: the direct five-subset checker reconstructed all 13,338
  clauses with zero missing or extra, and the proof checker accepted 19,734
  records: 741 branches, 742 conflicts, and 18,251 unit steps.
- Scope limitation: this is one of 861 labeled two-vertex deletion pairs. It
  says nothing about the other 860 fixed cores and is not global
  nonexistence or outcome D.

## C12 — Four fixed-boundary neighborhoods around the \(E=2\) candidate fail

- Category: **CERTIFIED**
- Claim: none of four explicitly bounded free-edge neighborhoods around the
  current 43-vertex \(E=2\) candidate contains a \((5,5;43)\)-graph:
  - all 15 pairs within the six residual-conflict vertices plus the four
    changed core edges, 19 variables total;
  - all 66 pairs induced by the 12 vertices appearing in those two sets.
  - the preceding 66 plus 14 observed-cycle edges crossing its boundary,
    80 variables total;
  - the preceding 80 plus six proof-trace-selected boundary edges,
    86 variables total.
- Encoding/check artifacts:
  - `src/residual_lns_sat.py`
  - `verify/residual_lns_cnf_check.py`
  - `tests/residual_lns_tests.py`
  - `certificates/residual_lns_report.md`
- 19-edge certificate:
  - 356 clauses
  - CNF SHA-256
    `e055d5ae68b321d4343d5c1966d8a06a740482b5390e8f4443674b2301587462`
  - proof SHA-256
    `5645c314f478a59ac5daf7de314c0b4930526a1573b5b3246a184b3f863d32e1`
  - 17 checked records
- 66-edge certificate:
  - 4,868 clauses
  - CNF SHA-256
    `bb6a8166fa530f511a1d99860a8ed3028e8aa91d5c5204d819fa5fda899426da`
  - proof SHA-256
    `5f646f3a6aeb8049728ed7f6f046ca32581d5458b3160d38ee170f92442e7f6c`
  - 47 checked records
- 80-edge certificate:
  - 5,408 clauses
  - CNF SHA-256
    `29331d96769546f9ca3a8090b42c7d59f506cf86fe97e341ce5189bf4860467f`
  - proof SHA-256
    `76fe3fae159dbc03e0a0f76591be3b63f62b11ccaa55a3c8a770131c0b299350`
  - 77 checked records
- 86-edge certificate:
  - 5,775 clauses
  - CNF SHA-256
    `7e1ea8f550b431dbef4857a181d24a867c43659c6bb97d6d605425eba072ea0f`
  - proof SHA-256
    `7c1d8272dd16b92225e750223ca93339a0d6a8015fbfcd3dddf7dd38831a83f1`
  - 83 checked records
- Independent formula reconstruction matched all four clause sequences exactly,
  with zero missing or extra clauses.
- Scope limitation: between 817 and 884 graph edges were fixed to the invalid
  base candidate. This is neither unrestricted local minimality nor global
  order-43 nonexistence.

## C13 — Direct unrestricted order-43 encoding

- Category: **CERTIFIED**
- Claim: `certificates/direct_ramsey43.cnf` is exactly the direct
  edge-variable CNF for \((5,5;43)\)-graphs with the sound degree bounds
  \(18\le d(v)\le24\).
- Counts:
  - 903 primary edge variables
  - 64,500 sequential-counter auxiliary variables
  - 1,925,196 Ramsey clauses
  - 126,936 degree clauses
  - 65,403 variables and 2,052,132 clauses total
- Artifacts:
  - `certificates/direct_ramsey43_generation.report.md`
  - `certificates/direct_ramsey43.cnf`
  - `certificates/direct_ramsey43.metadata.json`
  - `results/verification/direct_ramsey43_cnf_check.json`
- CNF SHA-256:
  `141de0a9714fb40e100508031b37fa555bf2fbdefd13c2dee4c04141c159bcb1`
- Independent structural-check report SHA-256:
  `7bf6d5847734d54763099ae59ff186086aaf78d8a75545c65ce5518ab31ad007`
- Validation: independent clause-by-clause reconstruction matched all
  2,052,132 clauses; seven tests include all 33,868 labeled graphs through
  order 6 and exhaustive small counter semantics.
- Scope limitation: this certifies the encoding identity only. No global
  solver was run, so it provides no SAT/UNSAT conclusion and is not outcome D.

## C14 — First full six-vertex incident solve timed out

- Category: **REPRODUCIBLE COMPUTATIONAL OBSERVATION**
- Claim: the exact fixed-boundary formula freeing all 237 edges incident to
  residual vertices \(\{3,4,7,38,41,42\}\) reached its strict 60-second cap.
- Formula: 237 variables and 49,461 independently reconstructed clauses.
- Runtime record: 659 nodes, 338 decisions, 320 conflicts, and 11,080
  propagations in 60.003176 seconds.
- Artifacts:
  - `certificates/residual_lns_incident_six.report.md`
  - `certificates/residual_lns_incident_six.timeout.json`
  - `certificates/residual_lns_incident_six.cnf`
- CNF SHA-256:
  `bfa9d9e3edea9a5ac332614fc76984c9d287b1e8bf39d282199a09aab2b9c014`
- Limitation: `TIMEOUT` is neither SAT nor UNSAT. No proof, candidate, or
  Ramsey-bound claim resulted from this first run.
- Supersession: C15 records a later proof-producing run on the same
  byte-identical CNF. The timeout remains a valid solver-performance
  observation but is no longer the formula's current mathematical status.

## C15 — Original full incident-six boundary is impossible

- Category: **CERTIFIED**
- Claim: no assignment of the 237 edges incident to
  \(\{3,4,7,38,41,42\}\) produces a \((5,5;43)\)-graph while the other 666
  edges equal `results/best_candidates/exoo_seed_20260724.g6`.
- Formula: 237 variables and 49,461 independently reconstructed clauses.
- Artifacts:
  - `certificates/residual_lns_incident_six.cnf`
  - `certificates/residual_lns_incident_six_glucose3.drat`
  - `certificates/residual_lns_incident_six_glucose3.lrat`
  - `certificates/residual_lns_incident_six_glucose3.result.json`
  - `certificates/residual_completion_workflow.report.md`
- Hashes:
  - CNF:
    `bfa9d9e3edea9a5ac332614fc76984c9d287b1e8bf39d282199a09aab2b9c014`
  - DRAT:
    `e7c8da6188c304e79ca2ca9bc077d261ed7536b3e4b3ec1181bebb006547c654`
  - LRAT:
    `592d2ce4df932c6332af5b2523b4fbaaf6d394d14aa639c74b303f1bf1195209`
- Verification: Glucose3 returned UNSAT; `drat-trim` accepted the DRAT and
  emitted LRAT; `lrat-check` accepted the LRAT.
- Scope limitation: this fixes 666 labeled edges to one invalid base graph.
  It is not unrestricted order-43 UNSAT and is not outcome D.

## C16 — A structurally different \(E=2\) candidate

- Category: **REPRODUCIBLE COMPUTATIONAL OBSERVATION**
- Claim: a deterministic 300,000-move search over exactly the 237 incident
  edges retained a different order-43 graph with 455 edges,
  \(C_5=2,\ I_5=0,\ E=2\).
- Configuration: seed 20260726; four 75,000-move restarts; tabu 9; random
  walk 0.04; breakout interval 250; restart perturbation 12.
- Runtime/evaluations: 27.084184 internal seconds and 1,528,975 exact delta
  evaluations.
- Artifact:
  `results/best_candidates/incident_lns_seed_20260726.canonical.json`
- Hashes:
  - graph6:
    `c0a8d2de5e7efa1abc6848c71e61019579ff31d8958fcce70f257d725792c337`
  - canonical JSON:
    `51dc724e2ab82293bf604e3d45d0c23b7c7e9984641f8b9e274afaa7e77fff3d`
  - source:
    `556f5550f74b5d835b79646d888979177b710bda7ef5a9b83f4b30fb7fead3fe`
- Validation: the Python exhaustive verifier gives exactly \(2,0,2\); the
  independent C++ bitset verifier finds a 5-clique and no independent
  5-set. All 666 fixed edges were preserved and 135/237 free edges changed.
- Limitation: the candidate is invalid and proves no Ramsey bound.

## C17 — Alternative full incident-six boundary is impossible

- Category: **CERTIFIED**
- Claim: no assignment of the 237 edges incident to
  \(\{2,4,24,25,26,42\}\) produces a \((5,5;43)\)-graph while the other 666
  edges equal the C16 constructive candidate.
- Formula: 237 variables and 49,677 independently reconstructed clauses.
- Hashes:
  - candidate graph6:
    `c0a8d2de5e7efa1abc6848c71e61019579ff31d8958fcce70f257d725792c337`
  - CNF:
    `e470ed2a4a1fe316b8cce77ab2e3f1c4f6ceb9d57b37e1e076f780e77a919867`
  - DRAT:
    `bb7cdeecfaabdddd96117d1bd3463cf5699ffd84959787d5fdcd55d18423bb70`
  - LRAT:
    `df22449c12fcb20fb2140a1fa3f8ffe3f10bc4716c957e10b4518a0de821c5c3`
- Report:
  `certificates/residual_lns_incident_alt_six.report.md`.
- Scope limitation: this is a second fixed 666-edge boundary, not a global
  nonexistence result.

## C18 — Aggregate core Hamming radius six is impossible

- Category: **CERTIFIED**
- Claim: no \((5,5;43)\)-graph exists when all 237 original incident-boundary
  edges are unrestricted and at most six of the other 666 edge values differ
  from `results/best_candidates/exoo_seed_20260724.g6`.
- Encoding:
  - 903 primary edge variables
  - 1,925,196 direct Ramsey clauses
  - 4,641 sequential-counter auxiliaries
  - 9,276 counter clauses
  - 5,544 variables and 1,934,472 clauses total
- Independent validation:
  `results/verification/core_radius6_cnf_check.json` reconstructed every
  clause, and `results/verification/core_radius6_semantic_audit.json`
  independently checked the edge partition, signs, counter semantics, and
  small exhaustive instances.
- Formula SHA-256:
  `34183fc806ec83136001f49c3373b770484168d70f846ba9b08de5fbe2bfea7d`.
- Retained compressed DRAT:
  - 68,702,255 bytes
  - SHA-256
    `0fbd59057b014662a8aa1030c18616836ccfa98734a36bcd11a9195c4042b418`
  - decompressed raw SHA-256
    `1bfc9fc9f8df0b042a3df72e0c422b84c914eb46cc216811b6c9abc147c67e26`
- The 1,424,628,404-byte generated LRAT, SHA-256
  `638e5deb58354931725ef00f8bf670f47eb3cc656fde8b6b4c036cb1bbc8b2f6`,
  was accepted by `lrat-check`; it is regenerated rather than retained.
- Report:
  `certificates/residual_completion_workflow.report.md`.
- Consequence: within this labeled decomposition, any valid graph must differ
  on at least seven of the 666 core edges.
- Scope limitation: the base graph and six-vertex boundary remain fixed as
  the reference structure. This is not global order-43 UNSAT.

## C19 — Proof-core fixed-edge ranking

- Category: **CERTIFIED**
- Claim: mapping the 6,335 retained input clauses in the accepted C15 DRAT
  core back to their unique source five-subsets gives the top fixed-core
  edge occurrences
  \((0,32):104,(18,33):102,(18,20):101,(24,26):101,(1,10):100,
  (9,29):96,(27,29):94,(6,15):94,(1,12):94,(2,25):93\).
- Independent method: directly reconstruct all 49,461 input clauses from the
  graph and metadata, uniquely map the retained core as an ordered
  subsequence, then count fixed-core pairs in the mapped five-subsets.
- Artifacts:
  - `src/proof_core_fixed_edge_rank.py`
  - `results/verification/residual_lns_incident_six_proof_core_edge_rank.json`
- Hashes:
  - source:
    `32d14b3e9aad496f9e3ea63a08f6271b0e7404c7b956f1008789b00bf95e91f9`
  - result:
    `3cd52e8c6f60e7d1923bc53c449a09ca93541eb27593a3f9e840ab76f60e4f65`
- Limitation: occurrence rank is an exact property of this proof core, not a
  theorem that high-ranked edges are the best constructive moves.

## C20 — First proof-guided radius-seven cut is impossible

- Category: **CERTIFIED**
- Claim: no \((5,5;43)\)-graph exists when all 237 original boundary edges
  and the seven C19 occurrence-rank leaders
  \((0,32),(18,33),(18,20),(24,26),(1,10),(9,29),(27,29)\) are free while
  the other 659 core edges equal the original \(E=2\) base graph.
- Preregistration:
  `results/benchmark_plans/proof_core_top7_cut_v1.json`, SHA-256
  `85794252bf8c014a94cb69a31545be5245fc926f5bf42f94ea211c62eed2aab4`.
- Formula: 244 variables and 52,148 independently reconstructed clauses.
- Hashes:
  - CNF:
    `cfbf69f7bb7646235ba195dae92aae38532ee7d869ef4f1b653c074c05cd4b42`
  - DRAT:
    `c1f75abad12de12f2db0e8fa30d3840320f54212a20679f22f42b1f5228ffeae`
  - LRAT:
    `8e4c2ed3f44a55ee205a97015ac9d8a1d405927747bb4b97ffa22b9b9f1d07cc`
- Report:
  `certificates/residual_lns_incident_six_plus_core_top7.report.md`.
- Scope limitation: this closes one selected seven-edge cut, not all
  \(\binom{666}{7}\) radius-seven choices and not global order-43 UNSAT.

## C21 — Aggregate radius-seven replay timed out

- Category: **REPRODUCIBLE COMPUTATIONAL OBSERVATION**
- Claim: the independently reconstructed aggregate radius-seven formula
  reached the strict 120-second Glucose3 cap.
- Formula: 6,203 variables, 1,935,789 clauses, and SHA-256
  `e832e9ff558085c8431f889b1daed8cae2f19ce7a5c04d2c7b4a1873f6777643`.
- Artifacts:
  - `certificates/core_radius7.report.md`
  - `certificates/core_radius7.metadata.json`
  - `results/verification/core_radius7_cnf_check.json`
  - `certificates/core_radius7_glucose3.timeout.json`
- Runtime: 120.080041 wall seconds under a 120-second subprocess cap.
- Limitation: `TIMEOUT` is neither SAT nor UNSAT. No proof or model was
  produced, and no mathematical conclusion follows.

## C22 — Eleven prime-order automorphism cycle types are excluded

- Category: **CERTIFIED**
- Claim: a hypothetical \((5,5;43)\)-graph cannot admit an automorphism with
  any of the following cycle types:
  \[
  11^3 1^{10},\ 13^2 1^{17},\ 13^3 1^4,\ 17^2 1^9,\
  19^2 1^5,\ 23^1 1^{20},\ 29^1 1^{14},\
  31^1 1^{12},\ 37^1 1^6,\ 41^1 1^2,\ 43^1.
  \]
- The \(11^3 1^{10}\), \(17^2 1^9\), and \(19^2 1^5\) formulas encode
  their full cycle types without additional symmetry clauses. Independent
  reconstruction matched every clause; Glucose3 DRAT, `drat-trim`, and
  `lrat-check` all accepted.
- The \(13^2 1^{17}\) and \(43^1\) cases reuse their separately audited
  certified formulas.
- The remaining types follow from the degree interval \(18\)--\(24\) and
  the checked fixed-vertex argument in
  `certificates/prime_automorphism_cycle_type_exclusions.report.md`.
- Coverage audit:
  `results/verification/prime_automorphism_cycle_type_coverage_v1.json`.
- Scope limitation: 54 prime-order cycle types remain uncovered, including
  all involution types and the one-cycle types for primes 11, 13, 17, and
  19. This is not a full automorphism classification or a global Ramsey
  bound.

## C23 — The retained E=2 corpus has only two complement classes

- Category: **CERTIFIED**
- Claim: the 22 independently replayed order-43 E=2 candidates form three
  graph-isomorphism classes and exactly two classes modulo complementation.
  The complement-class sizes are 10 and 12.
- Shared-core consequence: deleting each of the four common conflict-core
  vertices produces 88 dual-verified \((5,5;42)\)-graphs. These reduce to
  four isomorphism classes and two classes modulo complement, both already
  represented by catalog line 42 or 256.
- Validation:
  - direct all-five-subset and recursive-bitset checks accept all 88
    deletions;
  - nauty 2.9.3 dense and sparse canonical-labeling paths give identical
    isomorphism and complement-isomorphism partitions.
- Artifacts:
  - `certificates/e2_near_miss_isomorphism_collapse_v1.report.md`
  - `results/verification/e2_candidate_isomorphism_audit_v1.json`
  - `results/verification/e2_core_deletion_catalog_expansion_v1.json`
- Result hashes:
  - candidate-class audit:
    `07969bcbbfb62fcd1e40ef3d2fb718816b1f5630c71db67c9e9a53322ed2be7b`
  - deletion audit:
    `7692195c4fc76d469de1ee204e5f2a0f64612f528af96d7ba0b2ddf4a6099c0e`
- Scope limitation: this classifies only the fixed 22-candidate corpus and
  its 88 deletions. It does not classify all order-43 E=2 graphs or improve
  a Ramsey bound.

## C24 — Catalog cores 42 and 256 have exactly two optimal extensions

- Category: **CERTIFIED**
- Claim: each labeled order-42 Ramsey graph on catalog line 42 or 256 has
  one-vertex extension optimum exactly \(E=2\), attained by exactly two of
  its \(2^{42}\) new-vertex neighborhoods.
- Structure: for each core, one optimum has exactly two five-cliques and the
  other has exactly two independent five-sets. The two neighborhoods differ
  in one adjacency.
- Proof method: definitional conflict variables encode every core \(K_4\)
  and independent four-set, a checked sequential counter enforces at most
  two conflicts, and the two recorded neighborhoods are blocked. Both
  remaining formulas are certified UNSAT by Glucose3 DRAT, `drat-trim`, and
  `lrat-check`.
- Artifacts:
  - `certificates/catalog42_lines42_256_exact_e2_extensions.report.md`
  - `certificates/catalog42_line042_exact_e2_extensions_glucose3.result.json`
  - `certificates/catalog42_line256_exact_e2_extensions_glucose3.result.json`
- CNF hashes:
  - line 42:
    `7cbe0a232d3f6d4e1589229161780e85bb125f1150ed367360a582c2ec3a7521`
  - line 256:
    `5320d4a265a17099ef9edca1d8b55634429265dfbf37737ba4aadd8ee7766127`
- Scope limitation: this is exact only for fixed cores 42 and 256. It does
  not classify the other known cores, unknown order-42 graphs, or arbitrary
  order-43 graphs.

## C25 — Exactly two supplied catalog cores admit \(E\le2\) extensions

- Category: **CERTIFIED**
- Claim: among the 328 labeled order-42 Ramsey graphs in
  `data/r55_42some.g6`, exactly lines 42 and 256 admit a one-vertex
  extension with at most two monochromatic five-sets. Every other supplied
  core has at least three under every one of its \(2^{42}\) neighborhoods.
- Formula audit: an independent checker validated every core and
  reconstructed all 8,335,860 clauses across the 328 formulas.
- Outcome audit:
  - the two SAT assignments passed exhaustive checks of all
    \(\binom{43}{5}=962{,}598\) five-subsets;
  - the other 326 formulas emitted DRAT traces, all accepted by pinned
    `drat-trim`.
- Artifacts:
  - `certificates/catalog42_all328_e2_extension_screen.report.md`
  - `certificates/catalog42_e2_extension_proof_batch_v1.result.json`
  - `certificates/catalog42_e2_extension_proofs_v1/`
  - `results/benchmark_plans/catalog42_all328_e2_extension_proof_v1.json`
- Hashes:
  - frozen plan:
    `a42a254a563e726feaf36c42be2f7789c920894e96146d4f23e747feeb638c29`
  - result:
    `1534f38464bd55180c60981b019258799512595a984011906b8d49a27eef2355`
  - ordered proof bundle:
    `96a2319b3d82decb2d6910c9753a614dabf166ba9734d49207e02200dad77329`
- Combined consequence with C24: the four recorded optimal neighborhoods of
  lines 42 and 256 are the complete \(E\le2\) extension set across this
  supplied catalog.
- Scope limitation: the 328 graphs are not asserted to be a complete
  catalog of all order-42 Ramsey graphs. This is not a global order-43
  exclusion or a Ramsey-bound improvement.
