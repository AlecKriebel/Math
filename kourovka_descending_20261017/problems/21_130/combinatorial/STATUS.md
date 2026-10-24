# Combinatorial research status

Latest checkpoint discovery estimate:15%. Full Kourovka21.130 is **unresolved**. No arbitrary-n theorem or counterexample was found. Historical partial-result priority is unassessed. Publication gate is closed. No novelty claim or external publication has been made. No live processes remain.

| Family | Strongest artifact | Status | Exact gap |
|---|---|---|---|
| Symbolic collision relations | Universal n=3,...,7 finite certificates, checked by two different arithmetic implementations | Candidate bounded-cardinality theorem; adversarial agent review pending | Arbitrary n; n=8 bounded run incomplete |
| Monotone2-opt score | Complete landscapes on617selected instances through n=10 all reach rainbow cycles without score decrease | Empirical mechanism remains open | No universal monotonicity proof; some repairs require two neutral steps |
| Fixed-size identity trades | Proven p≤2^(k−1) bound for k-support color-preserving trades | Bounded-support route blocked | Need unbounded support or changed color set |
| Two-successor cycle merging | Proved impossible for any full-group rainbow permutation | Naive route blocked | A materially different merge operation |
| One-vertex cycle insertion | Proved impossible from G\{x} to G | Naive induction blocked | A different induction invariant |
| Generic proper/no-bichromatic-C4 coloring | Universal n≤5 certificate; six-vertex coloring obstruction | Generic abstraction blocked beyond5 | Must use additional additive consistency |

Read `universal_small_proof.md` for the exact theorem, proof, certificate interpretation, and reproduction. `universal_7_certificate.json` is the largest complete saved proof DAG. `verify_certificate_minors.py` verifies the certificates without HNF/saturation imports. Every n=3,...,7 has native and independent verification output JSON.
