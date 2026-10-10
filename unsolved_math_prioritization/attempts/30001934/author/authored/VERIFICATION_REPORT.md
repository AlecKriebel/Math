# Exact verification and limitations

General target: unresolved after five substantive approaches. No novelty guarantee. Source bodies are excluded from authored output.

## Reproduction

From this packet's tests directory:

- python test_exact_model.py
- python -O test_exact_model.py
- python -OO test_exact_model.py
- python certify_examples.py
- python check_adversarial_records.py

The mathematical model and core validation suite use only Python's standard library. Discovery scripts for the common-interval MILP and adversarial walk additionally use NumPy/SciPy; they are not needed to establish the proved partial results. No external network operations or repository mutations occur in these scripts.

## Core results

All three validation modes pass, each checking 2,680 points: 1,680 feasible integral K4 points across k=1,2,3,4, plus 1,000 seeded K5 points testing the constructive averaging proof. Their maximum endpoints are recomputed by Fraction arithmetic, verified feasible, and a strictly larger coefficient is verified infeasible. Every runtime guard uses explicit exceptions rather than assert.

Additional explicit positive and negative tests cover:

- k=1 and rank-zero/unique-tree endpoint k;
- loops fixed zero and distinguished parallel edges;
- disconnected input, malformed endpoints, nonintegral input, invalid k, non-tree choices, and negative remaining mass;
- a K4 star with coefficient 3/2 alongside a path with coefficient 3;
- rejection of a fake counterexample that checks one fractional tree but ignores integer-max trees;
- the global-coefficient and unique-maximum-weight-tree selection obstructions;
- exact vertex-subset inequalities at the residual scale k-lambda.

The three selection-rule examples have 157 spanning trees in total. `exact_selection_certificates.json` lists every tree, its exact maximum, and a binding edge/subset/mass constraint; the checker validates feasibility at each endpoint and infeasibility beyond it. These are counterexamples to auxiliary selection rules, not to the original question.

## Finite search coverage

Direct bounded boxes on complete graphs, each filtered by exact total mass and all subset inequalities:

- K4, k=5, weights 1..4: 580 total-mass candidates, 540 feasible
- K4, k=7, weights 2..5: 580 candidates, 576 feasible
- K5, k=6, weights 2..3: 210 candidates, all feasible
- K5, k=7, weights 2..4: 6,765 candidates, all feasible
- K5, k=8, weights 2..5: 82,885 candidates, all feasible

Total feasible bounded-box points: 90,976. Each had an integer-max tree.

Seeded sum-of-tree search: 64 sampled connected graphs, 16 each on 5,6,7,8 vertices, with 2,500 integer points on each and k ranging from 5 through 39. Total: 160,000 points. Each had an integer-max tree. This is sampling, not exhaustive coverage of those graphs' lattice points or of graphs of those orders. A literal maximum of zero counts as integral and occurred in some boundary inputs, in accordance with the stated question.

Adversarial search: exact integer-scaled rational evaluation was used to minimize the number of integer-max trees. The completed K5 and K6 runs retained respectively 54 of 125 and 623 of 1,296 integer-max trees in their best saved points. The K7 run was interrupted after the five-route research budget was spent; the saved best point had 6,909 of 16,807 integer-max trees. These are neither counterexamples nor exhaustive negative results. Each saved point is cross-checked independently using Fraction arithmetic in `adversarial_exact_crosscheck.json`. The `checked` field in a best-point record is the number of evaluated proposals when that best point was first found, not the final total work of the whole run.

Common-unit-interval discovery: floating-point HiGHS MILP searches required all tree maxima to lie in (a,a+1), with integer k<=100. It reported infeasible for (n,a)=(5,1),(5,2),(5,3),(6,1),(6,2); the (7,1) run reached its time limit without a candidate. These statuses are not exact infeasibility certificates. The family is narrower than all possible counterexamples because different trees may have maxima in different unit intervals.

## Limits

The tests support the exact model and the stated finite examples. The proofs of the low-dilation, <=4-vertex, and K5 results are in MATHEMATICAL_REPORT.md; numerical sampling is not used as their logical justification. Neither the theorem for K5 nor this finite search proves an all-graph theorem. The paper-source full text is kept separate, and no third-party text or private coordination is needed to reproduce the authored mathematics.
