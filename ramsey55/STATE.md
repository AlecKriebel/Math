# Research state

Last updated: 2026-07-24T06:26:46Z.

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
- **CERTIFIED EXACT DECOMPOSITIONS, NOT EXCLUSIONS:** all three normalized
  global root-degree branches 18, 19, and 20 have independently checked
  143-cube \(S_4\times S_4\) anchor covers. The preferred union formulas
  remain unsolved. The \(3^{14}1\) automorphism type likewise has a checked
  two-case normalizer quotient but no UNSAT proof.
- **CERTIFIED FINITE SIDE ENUMERATION:** for the order-seven automorphism
  track, all 191,394 side models and the side-model exhaustion proof replay
  independently. A full-size 291-pair shard pilot also has checked DRAT and
  LRAT, but the remaining 127 shards have not run and the cycle type is not
  excluded.
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

### Structural quotient and all-class second barrier

- Re-exported the exact targeted low-conflict closure: 16,082 labeled
  \(E=3\) states and 73,788 \(E=4\) states.
- Dense/sparse nauty audits and independent bitset recounting collapse the
  89,870 states to 53 classes modulo complement: 9 at \(E=3\), 44 at
  \(E=4\).
- The frozen all-class run exactly replayed 47,675 first barriers outside
  the old move closure, then executed 2,080,964 heuristic repair steps.
- It found no \(E=0\) or \(E=1\), and retained 1,670 labeled \(E=2\)
  endpoints. Every endpoint independently falls back into the same two
  previously known complement-isomorphism classes; zero novel class was
  found.

### Degree-18 exact anchor cover

- The equality case \(|N(0)|=18=R(4,4)\) still forces an independent
  four-set. The complementary side of order 24 forces a four-clique.
- Independent enumeration again gives 35,714 feasible cross matrices and
  exactly 143 \(S_4\times S_4\) orbits.
- The lean degree-18 union has 65,556 variables and 2,061,137 clauses; all
  2,052,132 base clauses and 9,005 additions match independently.
- No solve was attempted, so the branch remains open.

### Prime-automorphism certificate progress

- The order-five all-ones internal split has 17 of 80 leaves fully checked
  through DRAT-to-LRAT. The remaining leaves are active; this is not yet an
  exclusion.
- The order-seven side exhaustion is certified. Its worst 291-pair shard
  pilot completed 291/291 UNSAT with independent byte-exact LRAT
  regeneration. The full 128-shard launch is paused below its frozen
  9.13-GB free-space gate.

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
- **REPRODUCIBLE FINITE-CORPUS STRUCTURE:** 89,870 labeled \(E=3/E=4\)
  frontier states occupy only 53 complement classes, and every one of 1,670
  retained second-barrier \(E=2\) endpoints returns to the same two known
  complement classes.
- **CONJECTURE OR HEURISTIC:** a successor must force at least two
  non-repairing escape edges before allowing conflict-directed repair;
  increasing the completed one-barrier rollout budget is unlikely to add
  information.
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
15. Exact degree-18 anchor cover, completing the common 143-orbit
    decomposition of all normalized global branches.
16. Dense/sparse quotient of the full 89,870-state low frontier and an
    all-53-class, 47,675-barrier repair run.

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
- A larger budget for the same one-forced-edge repair operator is rejected:
  the frozen all-class run covered every retained structural seed and every
  stated first escape edge, yet all 1,670 \(E=2\) endpoints returned to the
  two known classes.
- The order-seven full shard launch is paused until free space again exceeds
  its frozen 9,126,805,504-byte safety requirement.
- An interrupted CaDiCaL radius-seven attempt is an infrastructure failure
  because that wrapper did not support limited interruption; it is not a
  mathematical result.

## Next selected experiment

Freeze and execute a changed constructive move architecture: from every one
of the 53 low-frontier complement classes, force two explicitly
non-repairing escape edges before any conflict-directed repair. Retain and
independently verify any \(E\le1\) state immediately; quotient every \(E=2\)
endpoint before claiming a new basin.

Any SAT result will be exported immediately and checked by both independent
graph verifiers. Unchecked negative solver results remain observations. In
parallel, continue the order-five certificate bundle. Launch the remaining
order-seven shards only after the frozen storage gate passes; retain only
proof-checked exclusions.
