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

## C14 — Full six-vertex incident neighborhood timed out

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
  Ramsey-bound claim resulted.
