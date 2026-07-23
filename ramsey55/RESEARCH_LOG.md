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
