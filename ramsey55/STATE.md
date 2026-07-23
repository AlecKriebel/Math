# Research state

Last updated: 2026-07-23T17:50:26Z.

## Current certified mathematical status

- **CERTIFIED:** `data/exoo42_constructed.canonical.json` is a
  \((5,5;42)\)-graph. Two independent verifier paths give zero forbidden
  five-sets. Therefore \(R(5,5)\geq43\).
- **CERTIFIED:** the exact one-vertex-extension CNF for that fixed graph is
  UNSAT. The instance has 42 variables and 2,318 clauses. Two independently
  checked exhaustive tree proofs close all 39 nodes. This proves only that the
  fixed Exoo42 core is nonextendible; it is not outcome D (global
  nonexistence at order 43).
- **CERTIFIED:** for every one of the 42 ways to delete one Exoo42 vertex, the
  remaining fixed 41-vertex induced core cannot be completed to order 43 by
  adding two vertices. All 42 separately labeled 83-variable CNFs are UNSAT;
  no symmetry or isomorphism assumption was used. The independent batch
  checker accepted 104,058 proof records. This exhausts \(k=1\) replacement
  for this witness only, not arbitrary 41-vertex cores.
- **CERTIFIED:** the first bounded \(k=2\) benchmark is UNSAT: delete original
  vertices 0 and 1, preserve the fixed 40-vertex induced core, and add three
  vertices. The exact formula has 123 variables and 13,338 clauses. An
  independent direct five-subset reconstruction matched all clauses, and the
  proof checker accepted 19,734 records. This covers exactly one fixed core;
  the other 860 deletion pairs were not run.
- **CERTIFIED:** four fixed-boundary exact neighborhoods of the current
  \(E=2\) candidate contain no solution. They release 19, 66, 80, and 86
  edges; independent direct-subset reconstruction exactly matched every CNF,
  and all tree proofs checked. All other edges stayed fixed, so these are not
  global nonexistence results.
- **CERTIFIED:** the unrestricted direct \(n=43\) CNF has been generated and
  independently reconstructed clause-by-clause. It has 903 primary edge
  variables, 64,500 degree-counter auxiliaries, and 2,052,132 clauses. This
  certifies the encoding only; no global SAT solve or outcome D is claimed.
- **REPRODUCIBLE COMPUTATIONAL OBSERVATION:** the 237-variable neighborhood
  freeing every edge incident to the six residual-conflict vertices reached
  the strict 60-second cap after 659 nodes. The result is `TIMEOUT`, neither
  SAT nor UNSAT; no proof or candidate exists.
- **REPRODUCIBLE COMPUTATIONAL OBSERVATION:** primary sources retrieved
  2026-07-23 report \(R(5,5)\leq46\), with independent implementations reported
  by Angeltveit and McKay. This repository has not replayed their roughly
  30-CPU-year main computation and has no DRAT/LRAT-style certificate for it.
  Thus the literature status is \(43\leq R(5,5)\leq46\), while the locally
  checked certificate currently covers the lower bound only.
- No 43-, 44-, or 45-vertex construction has been found here.
- No global UNSAT/nonexistence certificate has been generated here.

## Best verified candidate

- Artifact: `results/best_candidates/exoo_seed_20260724.canonical.json`
- Order: 43
- Edges: 454
- Degree sequence:
  \(20^{14},21^{10},22^{19}\)
- Exhaustive counts: \(C_5=0,\ I_5=2,\ E=2\)
- Canonical artifact SHA-256:
  `4c586a4e1026bdd628d04b2c5280dafff7f5dd7f326afa16712c039a2c1b0b65`
- graph6 SHA-256:
  `f5adf13e5791bb8fe4c58941e3d797c283223013290a2376935f1e1eef4ef31a`
- Verifier 1: exact direct-subset recount confirms \(0,2,2\).
- Verifier 2: recursive bitset search finds no \(K_5\) and does find an
  independent 5-set, confirming invalidity.
- Adversarial audit: PASS for deterministic relabeling, complementation,
  both graph-verifier paths, and an independent 28-check reconstruction of
  every JSON artifact representation.

The two residual independent sets are
\(\{3,4,7,41,42\}\) and \(\{3,4,38,41,42\}\). Their intersection has four
vertices and their union has six. Every single flip inside either residual
conflict leaves \(E\geq2\); adding either common pair \(\{3,4\}\) or
\(\{41,42\}\) destroys both independent sets but creates two 5-cliques.
An exhaustive scan of all 903 one-edge and 407,253 two-edge changes
(408,156 exact delta evaluations total) also found no graph with \(E<2\).

Relative to the reconstructed 42-vertex core, the candidate changes four core
edges and adds vertex 42 with degree 21.

## Current hypotheses

- **CONJECTURE OR HEURISTIC:** the repeated \(E=2\) obstruction and the
  237-variable exact timeout indicate that the fully incident neighborhood
  needs a constructive/local-search front end or a different branching
  heuristic, rather than another blind runtime increase of the current DPLL.
- **CONJECTURE OR HEURISTIC:** extension-derived starts are far more informative
  than unconstrained random starts: in the first bounded comparison they
  reduced \(E\) from 231 to 2 with comparable compute.
- **CONJECTURE OR HEURISTIC:** adaptive conflict weights alone are insufficient
  when restricted to one edge of a currently violated five-set.

## Strategies tried

1. Dependency-free random-start min-conflicts with tabu and 3% random moves:
   80,000 accepted flips, four restarts, seed 20260723, 7.00 s; best
   \(E=231\).
2. Same search seeded by the certified Exoo42 graph plus a random new vertex:
   200,000 flips, four restarts, seed 20260724, 17.64 s; best \(E=2\).
   A second run with the current source reproduced the graph byte-for-byte.
3. Breakout-weight mutation from the \(E=2\) graph:
   200,000 flips, four perturbed restarts, 796 penalty updates, seed 20260725,
   31.72 s; best \(E=2\), exactly the same graph.
4. Exact one-vertex extension of the fixed Exoo42 graph:
   42 variables, 1,148 negative 4-clique clauses, 1,170 positive
   independent-4 clauses; certified UNSAT in a 39-node decision tree. The
   deterministic Python solver took 0.131 s internally, and the independent
   compact checker replayed a 52-byte proof.
5. Exhaustive Hamming-radius-2 scan around the \(E=2\) candidate:
   408,156 exact flip-delta evaluations in 2.94 s; no one- or two-edge change
   improves \(E\). The saved result is byte-identical to the input candidate.
6. Exact \(k=1\) core replacement for all 42 vertex deletions of Exoo42:
   42 UNSAT, 0 SAT, 0 timeouts in 84.18 s. Instances have 83 variables and
   6,652–6,702 clauses. Solver runtimes were 1.20–2.32 s. The independent
   checker accepted all proofs in 0.35 s, totaling 3,900 branches, 3,942
   conflict leaves, and 96,216 cited unit steps. A separately written formula
   reconstructor matched all 280,376 clauses with zero missing or extra.
7. First exact \(k=2\) core benchmark, deleting original vertices 0 and 1:
   checked UNSAT in 25.20 s. The 123-variable formula has 13,338 clauses; the
   proof has 19,734 checked records. A separate direct five-subset
   reconstructor matched all 13,338 clauses with zero missing or extra.
8. Residual-focused exact large-neighborhood completion from the \(E=2\)
   candidate. The 19-edge neighborhood was checked UNSAT in 0.000292 s; all
   16 variables needed for its contradiction were forced without a branch.
   The principled expansion to all 66 edges induced by the 12 implicated
   vertices was checked UNSAT in 0.011881 s; 46 unit steps again ended in the
   same residual independent 5-set. Both independent formula checks found
   zero missing or extra clauses.
9. Proof-guided boundary expansion released 14 observed-cycle cut edges
   (80 variables), then six high-incidence proof-trace edges (86 variables).
   Both exact formulas were independently reconstructed and checked UNSAT by
   unit propagation, in 0.030573 s and 0.037582 s.
10. Full incident neighborhood around the six residual vertices:
    237 variables and 49,461 independently matched clauses. The strict
    60-second solve stopped with `TIMEOUT` after 659 nodes, 338 decisions,
    and 320 conflicts. No proof or candidate was produced.
11. Direct unrestricted order-43 encoding:
    65,403 variables and 2,052,132 clauses in a 90,311,307-byte CNF.
    Generation took 8.269 s; an independent checker reconstructed the whole
    formula in 7.032 s. No global solve was launched.
12. Evidence audit replay of all four constructive configurations from current
    source SHA-256 `2f0a1fba...`: all four graphs were byte-identical to their
    historical artifacts and independently reverified. The best remains
    \(E=2\).

## Strategies rejected or paused

- Unconstrained random starts are paused as the primary track because the
  measured best \(E=231\) is two orders of magnitude worse than the
  witness-seeded baseline. They remain useful as a diversity control.
- The present breakout mutation is not rejected after one budget. Its failure
  diagnosis is representation-level: penalties change which single edge is
  chosen but do not release a multi-edge neighborhood capable of crossing the
  observed two-for-two conflict exchange.
- The current generic DPLL branching strategy is paused for the 237-edge
  neighborhood after its first strict timeout. A timeout is not an UNSAT
  result, and its budget will not be doubled without a representation or
  branching change.

## Next selected experiment

The one-vertex extension, all \(k=1\) replacements, and the first \(k=2\)
benchmark are complete and certified UNSAT for their explicitly fixed cores.
A naive linear projection from the first \(k=2\) case is about 6.0 CPU-hours
and 449 MB for all 861 pairs, but runtime variability makes this only a
planning estimate; the full batch has not been launched.

Four smaller residual neighborhoods are closed, while the first neighborhood
that releases the complete six-vertex boundary timed out. The next
constructive action is a restricted min-conflicts/tabu kernel over those 237
incident edges, benchmarked over fixed and fresh seeds, followed by exact
completion of the best partial assignments. This changes the search
representation instead of merely increasing the timed-out DPLL budget. Any
SAT model will be exported and verified as a full graph by both independent
paths; any later UNSAT certificate will remain scoped to its exact boundary.
