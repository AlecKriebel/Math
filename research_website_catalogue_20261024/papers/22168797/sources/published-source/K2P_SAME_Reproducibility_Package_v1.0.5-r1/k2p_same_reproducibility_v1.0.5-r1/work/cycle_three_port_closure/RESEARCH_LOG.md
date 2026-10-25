# Research log — three-port cycle closure

## 2026-08-21 — topology-only repair falsified

- Regenerated all 13,440 primitive cycle directions.
- Confirmed 7,452 strict tree/sunlet rows, 24 no-dummy terminals, and 5,964
  dummy-bearing equal-topology roots.
- Expanded one restored role: 48,924 children, including 5,100 equal-topology
  nonterminals.  In particular, 132 one-dummy roots remain nonterminal after
  complete restoration, disproving the proposed general first-child quartet
  lemma.
- Best estimate of completion toward the cycle local theorem: **55%**.

## 2026-08-21 — fixed-full all-role mechanism

- Replaced recursive selected-parent lifting by the logically valid fixed-full
  construction: fix the actual full network pair first and restore all actual
  omitted labels simultaneously.
- Derived the exact root multiplicities 324, 1,896, 2,784, 960 and the physical
  completion total 536,364.
- Independent scan found 535,920 quartet rows, 300 tree/sunlet rows, 132
  equal-topology nonterminals, and 12 labelled isomorphisms.
- Best estimate: **82%**.

## 2026-08-21 — exact algebra and transports

- Reduced the 132 rows to 54 canonical descriptor pairs (42 doubletons and 12
  quadruples).
- Found and directly replayed an exact target-vanishing/source-nonvanishing
  multihomogeneous quadratic for every class.
- Bound an exact rational strict-\(\mathcal D_+\) source witness to every class.
- Constructed unique exact labelled transports for all 24 base terminals and
  all 12 restored isomorphisms.
- Best estimate: **95%**.

## 2026-08-21 — independent replay and mutation closure

- Independent verifier regenerated and compared all 549,804 ledger rows with
  zero unresolved.
- Mutation tests rejected omitted rows/roles, wrong placements, reassigned
  quadratics, and broken transports.
- The first optimized-mode run exposed hash-seed-sensitive serialization of
  incidence edge nodes.  Replaced it with structural set encoding, regenerated
  every dependent hash, and passed the complete `python -O` replay.
- Cycle local theorem and reproducibility goal: **100% complete**.
- Global K2P theorem remains conditional on the separately owned all-primitive
  coherent-probe and final assembly gates.
