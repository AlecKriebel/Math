# Research state

Last updated: 2026-07-24T05:49:15Z.

## Current certified mathematical status

- **CERTIFIED:** `data/exoo42_constructed.canonical.json` is a
  \((5,5;42)\)-graph. Two independent verifier paths find no homogeneous
  five-set, so \(R(5,5)\geq43\).
- **CERTIFIED, FINITE-CATALOG SCOPE:** among the 328 supplied order-42
  Ramsey graphs, exactly lines 42 and 256 admit one-vertex extensions with
  \(E\le2\). The other 326 formulas have checked DRAT proofs. Each
  exceptional core has exactly two optimum neighborhoods, all with \(E=2\).
- **CERTIFIED, LOCAL SCOPE:** the full labeled Hamming ball of radius nine
  around `results/best_candidates/core_kick_seed_20260731.g6` is UNSAT.
  The independently reconstructed CNF and streamed DRAT-to-LRAT proof both
  verify. The radius-ten solve timed out and has no mathematical conclusion.
- **CERTIFIED, FINITE-CORPUS SCOPE:** 22 independently replayed \(E=2\)
  candidates collapse to three isomorphism classes and two classes modulo
  complement. Their 88 shared-core deletions collapse to the two catalog
  classes represented by lines 42 and 256.
- **CERTIFIED STRUCTURAL SUBCLASS EXCLUSIONS:** eleven prime-order
  automorphism cycle types are excluded, including all prime-order types
  with prime at least 23. Fifty-four prime-order types remain uncovered.
- **CERTIFIED EXACT DECOMPOSITIONS, NOT EXCLUSIONS:** the global root-degree
  19 and 20 branches each have an independently checked 143-cube
  \(S_4\times S_4\) anchor cover. The preferred union formulas remain
  unsolved. The \(3^{14}1\) automorphism type likewise has a checked
  two-case normalizer quotient but no UNSAT proof.
- **CERTIFIED:** the fixed Exoo42 graph has no one-vertex extension. All 42
  labeled one-vertex replacements are also impossible, and the first bounded
  two-vertex replacement case (deleting vertices 0 and 1) is impossible.
  These are fixed-core statements only.
- **CERTIFIED:** the four earlier residual neighborhoods with 19, 66, 80, and
  86 free edges are UNSAT under their exact fixed boundaries.
- **CERTIFIED:** the complete 237-edge neighborhood around residual vertices
  \(\{3,4,7,38,41,42\}\) is UNSAT when the other 666 edges equal the original
  \(E=2\) base graph. The original 60-second DPLL timeout is superseded by a
  Glucose3 DRAT proof accepted by `drat-trim` and a derived LRAT accepted by
  `lrat-check`.
- **CERTIFIED:** a second 237-edge neighborhood is UNSAT. It frees every edge
  incident to the constructive candidate's residual clique union
  \(\{2,4,24,25,26,42\}\) and fixes the other 666 edges to that candidate.
- **CERTIFIED:** the aggregate radius-six formula is UNSAT: all 237 original
  boundary edges may change arbitrarily, and at most six of the remaining
  666 core edges may differ from the original \(E=2\) graph. Thus a valid
  graph in this labeled framework would have to change at least seven core
  edges.
- **CERTIFIED:** the first proof-guided radius-seven cut is UNSAT. It frees the
  237 original boundary edges plus core edges
  \((0,32),(18,33),(18,20),(24,26),(1,10),(9,29),(27,29)\), fixing the
  other 659 core edges. This closes only that selected seven-edge cut.
- **CERTIFIED:** the unrestricted direct \(n=43\) CNF has been generated and
  independently reconstructed clause-by-clause: 65,403 variables and
  2,052,132 clauses. This certifies the encoding only; it has not been solved.
- **REPRODUCIBLE COMPUTATIONAL OBSERVATION:** current primary sources report
  \(43\leq R(5,5)\leq46\). The upper-bound computation has not been replayed
  or certificate-checked in this repository.
- No 43-, 44-, or 45-vertex construction has been found here.
- No global order-43 UNSAT certificate exists here. None of the local
  certificates changes the public Ramsey-number bounds.

## Best verified candidates

Two independently verified invalid order-43 graphs tie at \(E=C_5+I_5=2\):

1. `results/best_candidates/exoo_seed_20260724.canonical.json`
   - 454 edges; degree sequence \(20^{14},21^{10},22^{19}\)
   - \(C_5=0,\ I_5=2\)
   - residual sets
     \(\{3,4,7,41,42\}\) and \(\{3,4,38,41,42\}\)
   - graph6 SHA-256
     `f5adf13e5791bb8fe4c58941e3d797c283223013290a2376935f1e1eef4ef31a`
2. `results/best_candidates/incident_lns_seed_20260726.canonical.json`
   - 455 edges; degree sequence \(20^{13},21^{10},22^{20}\)
   - \(C_5=2,\ I_5=0\)
   - residual cliques
     \(\{2,4,24,25,42\}\) and \(\{4,24,25,26,42\}\)
   - graph6 SHA-256
     `c0a8d2de5e7efa1abc6848c71e61019579ff31d8958fcce70f257d725792c337`

The restricted constructive run changed 135 of 237 free edges while
preserving all 666 fixed edges, yet the same two-conflict/four-vertex-overlap
shape reappeared on the complement side. Both the exhaustive Python verifier
and independent C++ bitset verifier reject both graphs.

## Latest executed experiments

### All-328 \(E\le2\) catalog extension proof census

- Frozen catalog SHA-256
  `067902e853d87b49bcef0d1d4c0e3bbadd238ee18bc65341b079a3ca4780eccb`.
- 328 independently reconstructed formulas; 8,335,860 clauses in total.
- SAT with exhaustive full-graph checks on lines 42 and 256 only.
- 326/326 remaining lines returned UNSAT with DRAT accepted by pinned
  `drat-trim`; total retained proof size 158,998,676 bytes.
- End-to-end two-worker runtime 220.9611118 seconds.
- Result SHA-256
  `1534f38464bd55180c60981b019258799512595a984011906b8d49a27eef2355`.

### Global exact decomposition pilots

- Degree-19 and degree-20 anchor covers each reduce 35,714 feasible cross
  matrices to exactly 143 symmetry orbits; both materialized union formulas
  independently match 2,061,223 clauses.
- Matched 50,000-conflict MapleChrono pilots exhausted their budgets with no
  model or proof. The lean formulas were 4.97x and 3.91x faster than the
  exact-branch baselines.
- The \(3^{14}1\) automorphism cover and its \(m=6,7\) greedy normalizer
  quotients independently validate. All completed solves exhausted budgets;
  two later jobs ended on external signal 15. No exclusion follows.

### Restricted constructive search

- Seed 20260726; four restarts; 75,000 moves per restart
- tabu 9; random walk 0.04; breakout interval 250; restart perturbation 12
- 300,000 moves and 1,528,975 exact delta evaluations
- 27.084184 internal seconds
- best \(E=2\), with 135/237 free edges changed and 666/666 fixed edges
  preserved
- self-check: 674 ordinary/weighted incremental comparisons passed

### Proof-producing exact completion

- Original 237-variable CNF: 49,461 clauses, certified UNSAT in 0.283349
  solver seconds.
- Alternative 237-variable CNF: 49,677 clauses, certified UNSAT in 0.275337
  solver seconds.
- Aggregate radius six: 5,544 variables and 1,934,472 clauses, certified
  UNSAT in 78.839855 solver seconds. The retained 68,702,255-byte compressed
  DRAT reproduces the checked raw proof hash.
- Aggregate radius seven: 6,203 variables and 1,935,789 independently matched
  clauses; the strict 120-second replay returned `TIMEOUT`. This is neither
  SAT nor UNSAT.
- Proof-guided top-seven cut: 244 variables and 52,148 independently matched
  clauses, certified UNSAT in 0.458771 solver seconds.

## Current hypotheses

- **CONJECTURE OR HEURISTIC:** the repeated four-vertex overlap after 135
  boundary changes is a structural obstruction rather than an accident of
  one search trajectory.
- **CERTIFIED FINITE-CORPUS STRUCTURE:** the apparent plateau is exactly two
  complement classes in the retained 22-candidate corpus, and each
  exceptional supplied order-42 core has only two optimum extensions.
- **CONJECTURE OR HEURISTIC:** deleting vertices from the shared-conflict
  cores and solving exact three-vertex replacement problems is more likely
  to cross the structural basin boundary than additional single-edge or
  neutral-cycle search.
- **CERTIFIED LOCAL CONSEQUENCE:** arbitrary rewiring of the six-vertex
  boundary cannot work unless at least seven of the 666 original core edges
  also change.
- **CONJECTURE OR HEURISTIC:** proof-core incidence is useful for choosing
  radius-seven cuts, but the failure of its top seven edges shows that raw
  incidence rank alone is not a sufficient repair rule.
- **CONJECTURE OR HEURISTIC:** a portfolio of diverse seven-to-twelve-core-edge
  cuts has higher information value than another immediate budget increase
  of the aggregate radius-seven solve.

## Strategies tried

1. Random-start and Exoo42-seeded min-conflicts/tabu baselines.
2. Breakout-weight mutation and exhaustive Hamming-radius-two search.
3. Fixed-core exact extension and replacement formulas.
4. Residual fixed-boundary formulas with 19, 66, 80, 86, and 237 free edges.
5. A standalone constructive kernel over exactly the 237 incident edges.
6. Candidate conflict-union exact completions with materialized unit
   assumptions and checked LRAT.
7. Pinned Glucose3 → DRAT → LRAT certification of both 237-edge boundaries.
8. An aggregate sequential-counter encoding through six core-edge changes.
9. Independent reconstruction of the DRAT input core and ranking of all 666
   fixed core edges.
10. One preregistered proof-core-guided cut at the first admissible shell,
    radius seven.
11. Stratified search from 22 catalog seeds, conflict-block walks, exact
    neutral-cycle auditing, and a complete current-conflict \(E\le4\) atomic
    barrier scan.
12. Full-graph Hamming certificates through radius nine; radius ten timed
    out under its frozen cap.
13. Exact \(E\le2\) extension classification over all 328 supplied cores.
14. Exact root-degree 19/20 anchor covers and prime-automorphism quotient
    encodings.

## Strategies rejected or paused

- The remaining preregistered 16-seed constructive sweep inside the original
  237-edge boundary is cancelled. Exact UNSAT certification proves that no
  seed can reach \(E=0\) there, saving an estimated 427.2 CPU-seconds.
- The generic in-repository DPLL is retired for the 237-edge formula; its
  timeout was a solver limitation, not evidence about satisfiability.
- A blind aggregate radius-seven Glucose budget increase is paused after the
  strict 120-second replay timed out. The timeout makes no UNSAT claim.
- Radius ten is paused after its 300-second Glucose replay timed out on the
  independently checked formula.
- Blind conflict-block and neutral-cycle budget increases are paused because
  exact auditing showed that all retained \(E=2\) starts occupy only two
  complement classes with closed low-barrier regions under the tested moves.
- An interrupted CaDiCaL radius-seven attempt is an infrastructure failure
  because that wrapper did not support limited interruption; it is not a
  mathematical result.

## Next selected experiment

Run two constructive exact-completion programs in parallel:

1. From one representative of each certified \(E=2\) complement class,
   delete vertex triples and add three unconstrained vertices, screening the
   resulting 40-vertex fixed cores for a genuine order-43 completion.
2. Extend the moving-boundary track beyond the completed seven- and
   eight-incident-vertex screens with a preregistered, structurally diverse
   portfolio of wider incident boundaries.

Any SAT result will be exported immediately and checked by both independent
graph verifiers. Unchecked negative solver results remain observations. In
parallel, finish the order-five automorphism certificate attempt and retain
only proof-checked exclusions.
