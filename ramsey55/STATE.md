# Research state

Last updated: 2026-07-23T23:36:47Z.

## Current certified mathematical status

- **CERTIFIED:** `data/exoo42_constructed.canonical.json` is a
  \((5,5;42)\)-graph. Two independent verifier paths find no homogeneous
  five-set, so \(R(5,5)\geq43\).
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

## Strategies rejected or paused

- The remaining preregistered 16-seed constructive sweep inside the original
  237-edge boundary is cancelled. Exact UNSAT certification proves that no
  seed can reach \(E=0\) there, saving an estimated 427.2 CPU-seconds.
- The generic in-repository DPLL is retired for the 237-edge formula; its
  timeout was a solver limitation, not evidence about satisfiability.
- A blind aggregate radius-seven Glucose budget increase is paused after the
  strict 120-second replay timed out. The timeout makes no UNSAT claim.
- An interrupted CaDiCaL radius-seven attempt is an infrastructure failure
  because that wrapper did not support limited interruption; it is not a
  mathematical result.

## Next selected experiment

Build a small preregistered portfolio of radius-seven cuts chosen by
complementary rules: proof-core occurrence rank, vertex coverage, low overlap,
and deterministic diversity. For each cut, free the same 237 boundary edges
plus exactly seven core edges, reconstruct the CNF independently, and use the
pinned proof pipeline. A SAT model will be exported and checked as a full
graph; each UNSAT result will remain scoped to its exact 659-edge fixed core.
The already executed top-ranked cut is the first portfolio member and is
certified UNSAT.
