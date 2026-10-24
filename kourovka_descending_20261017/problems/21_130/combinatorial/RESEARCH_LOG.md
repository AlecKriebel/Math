# Combinatorial approach research log

## 2026-10-24T19:30:02.907574+00:00 — opening checkpoint

**Discovery completion estimate: 5%.** Exact target: every subset A, |A| = n > 2, of every finite odd-order abelian group has a cyclic enumeration with pairwise distinct adjacent sums. The sum coloring of K_A is proper. No 4-set supports two repeated opposite-edge pairs, because two such equations force a nonzero element of order 2.

Primary mechanism families: (1) switch rainbow cycle covers into one cycle, (2) augment maximal rainbow paths/cycles, (3) exploit local parallelogram restrictions and exact small-instance searches. A rainbow cycle cover is not a solution; all claimed merges will be proved or falsified explicitly. Original work in this folder only; no other new approach folder has been read. No external communication or publication authorized in this delegated work.

## 2026-10-24T19:33:52.627925+00:00 — local mechanisms falsified and bounded

**Discovery completion estimate: 8%.** Proved in `local_barriers.md`: two-successor switches cannot work at all on a full-group rainbow permutation; one-vertex insertion cannot extend any rainbow cycle on G minus one element to G; identity color-preserving trades need support k with p <= 2^(k-1), where p is the smallest prime divisor of |G|. These rule out naive cycle-cover merging and fixed-size identity-switch proofs. Exact small-prime connected trade search recorded in `local_trades.py/json`: minimum supports 3,4,5,5,6 for p=3,5,7,11,13. The determinant/adjugate argument is a checkable partial lemma and needs independent adversarial review before promotion. Full Hamilton-cycle existence remains the exact gap.

## 2026-10-24T19:43:43.812585+00:00 — universal symbolic n≤7 checkpoint

**Discovery completion estimate: 15%.** Developed an exact collision-relation search that applies to arbitrary finite odd-order abelian groups, rather than searching selected groups. `universal_small.py` exhausted n=6 (385 states, 0.86 s) and n=7 (2367 states, 65.85 s). `universal_fast.py`, using only a per-node child cache optimization, reproduced the same n=7 counts in 5.23 s. This is a candidate computer-assisted proof for n≤7; independent adversarial review is pending. No full-quantifier conclusion in n is claimed.

Mechanism: normalize the first vertex to zero; encode sum collisions as integer relations in n−1 variables; keep the relation lattice saturated at 2. A forced vertex equality is exactly membership of its difference in this saturated lattice. Branch on every possible disjoint-edge sum collision in a currently uncovered Hamilton cycle. Surviving relation quotients would have a finite odd quotient separating all vertices, so the symbolic formulation is exact, not an odd-prime-only relaxation.

`validate_lattice.py` passed 2700 independent membership checks in dimensions1–6 using rational rank and determinantal divisors rather than HNF. It also checked invariance under unimodular row operations and relation multiplication by powers of2. A faulty validation-input generator that scaled coordinates separately was corrected; the lattice implementation did not fail. Parent independently obtained a n=6 relation-cover result by a different implementation; I have not read that code.

Separate plateau family: 617 complete Hamilton-cycle landscapes through selected n=10 instances all have nondecreasing-score paths to rainbow cycles. Some states require two neutral steps before an improvement. This remains empirical evidence and no universal monotonicity lemma is proved. The generic no-bichromatic-C4 abstraction proves n≤5 via all243 symbolic collision assignments, but fails at6 for proper colorings not necessarily additive.

Current live work: bounded n=8 saturated search (240-second cap; at least9000states, incomplete at checkpoint); explicit proof DAG certificate for n=7. Exact remaining gap: arbitrary n. Novelty has not been assessed here.

## 2026-10-24T19:48:22.198948+00:00 — proof certificates independently checked

**Discovery completion estimate: 15%.** Saved explicit finite proof DAGs for each n=3,4,5,6,7: node counts1,3,16,317,1632. Native exact verifier passed all. The separately implemented `verify_certificate_minors.py` imports no HNF/saturation helpers and independently passed every branch of all five certificates using rational ranks, Bareiss determinants, and determinantal-divisor lattice indices; n=7 checks2304child edges and20544forced-equality leaves in7.64s, plus explicit acyclicity. Independent adversarial review by another agent remains pending.

The n=8 bounded search stopped at240.01s with34848states, maxdepth7, and12461dead-cycle leaves. Status is **incomplete**; no absence conclusion is permitted. No live search remains. Full arbitrary-n target remains unresolved. Positive control without2-saturation correctly retained a four-vertex obstruction in a group with2-torsion.

## 2026-10-24T19:48:32.146428+00:00 — family closing checkpoint

**Discovery completion estimate: 15%.** Family work stopped with no live processes. Strongest completed result is exact universal n≤7 via saved proof certificates checked by two distinct arithmetic implementations. The full arbitrary-n target is unresolved; n=8 is incomplete; plateau monotonicity is conjectural. Historical partial-result priority is unassessed. The root's adversarial reviewer is examining the latest proof DAG. Publication gate remains closed; no Git operation, external message, release, or publication was performed by this agent.
