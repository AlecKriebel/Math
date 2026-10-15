# PR173 independent path/diagonal adversarial audit

Head audited: `eb68ee2ecda39a8ec2748796d716c7a7598b7bc6`. This family assessed protected paths, irreversible competition, deterministic diagonal quantifiers, expectation-to-fraction transfer, seed resources and parity repair. A substantive first assessment was sealed before checker or reviewer code was read. No other family's findings or review verdict was consumed.

**Result:** No in-scope mathematical counterexample or central logical failure was found in this family. The protected-path lemma, all-n diagonal construction, expectation identity and resource bounds withstand the audit. The supplied checker acceptance functions require repair because Python optimization disables them. This computational defect does not invalidate the written argument.

## Exact scope and strongest verified result

The model has iid integer degrees at least two, finite second moment and unbounded support; degree-based weak seed selection precedes matching and weights; the strong root is uniform in a fixed positive-probability degree class; rates are fixed and positive. The candidate proves an existential growing-seed regime, not a single-hub or fixed-seed theorem.

For any finite undirected multigraph with nonnegative type-specific edge lengths and disjoint initial seeds, actual strong infection ancestors certify that a vertex infected by time T lies in the unopposed strong ball of radius T. A weak path of total time at most T whose entire vertex set avoids that closed ball is protected: cumulative-time induction makes every vertex weak by its path time. Zero weights and either tie convention are harmless under the full closed-ball avoidance hypothesis. Loops add no new vertex; each parallel edge remains a separate channel; undirected reversal preserves its length. This deterministic lemma is independently verified analytically and by exact bounded controls.

The supplied fixed-parameter local exploration estimate yields a deterministic N_j with a probability bound valid for EVERY n>=N_j. Enlarging N_j preserves that bound while imposing a seed-count floor and log N_j>=jT_j. Consequently J(n)->infinity and T_{J(n)}/log n<=1/J(n), without ever applying a fixed-time approximation to growing parameters. Arbitrarily thin unbounded degree tails enlarge the schedules; they do not obstruct existence.

For an independent uniform test vertex, E[unweak fraction] equals its probability of missing weak infection. Markov's inequality gives convergence of the fraction without independent infection indicators. The original seed count has mean at least 4J(n)^2, giving divergence by Chebyshev; its fraction vanishes by the degree tail. Integrability makes the normalized seed degree mass vanish. Single-vertex parity repair increases seed count by at most one and adds at most D_repair+1 to seed degree mass, including threshold crossing. Since total degree is at least 2n, the seed half-edge fraction vanishes.

## Reproduced computation and adversarial controls

| Control | Ordinary Python | Optimized Python | Exact bounded scope |
|---|---:|---:|---|
| Supplied author checker | PASS: 11,561 checks | Reports the same counters | 2,800 competitions; 6,736 protected witnesses |
| Supplied independent checker | PASS: 62,001 checks | Reports the same counters | 9,999 competitions; 20,278 protected witnesses |
| Own explicit-exception checker | PASS: 159,474 checks | PASS: 159,474 checks | 20,016 competitions; 25,176 protected witnesses |
| Supplied checkers with weak conclusion changed to strong | Both reject | Both falsely accept/report original counters | Confirms assert removal, using preserved copies |
| Nine own semantic false variants | All reject | All reject | Endpoint-only, open-ball, Voronoi, parallel collapse, repair mass, rate, count floor, root uniformity, logarithmic schedule |

Own controls use boundary recomputation for competition, Bellman-Ford distance relaxation, exact rational weights and explicit exception enforcement. They exhaust all three-vertex simple topologies (including disconnected/empty graphs) with edge lengths 0, 1 or 2 for both types, all nonempty disjoint source choices and both fast-first and weak-first tie conventions. Additional four-vertex controls cover loops, parallel edges, disconnected components and fractional weights. Arithmetic controls cover all repair vertices for specified bounded degree lists and thresholds, resource/Markov inequalities, and a sparse-spike degree law P(D=2^m)=7/8^m with finite second moment. Symbolic giant schedules for that law verify that small tails do not create an arithmetic contradiction; they do not supply the unknown local-convergence thresholds.

An explicit endpoint/Voronoi counterexample has weak seed 0, strong root 3, path 0–1–2 with weak edge lengths 4 and 1, strong root-to-1 length 1 and root-to-2 length 10. Weak unopposed distance to 2 is 5 and strong distance is 10, yet strong captures the intermediate vertex at time 1 and target at time 10. Thus endpoint avoidance or Voronoi comparison cannot replace full path protection. A separate equal-time example falsifies replacing the closed ball by the open ball; the candidate uses the correct closed ball.

## Original checker assessment and required repair

Both original `ck` functions consist of `assert predicate` followed by an unconditional counter increment. Under `python -O`, the assertions disappear. Intentionally reversing the protected-path colour conclusion to type 2 still produces the original acceptance counters and the independent checker's PASS status. Replace those acceptance tests with explicit conditional exceptions and require semantic false-variant rejection in ordinary and optimized execution. Originals and first seals were preserved unchanged.

Other implementation limits are bounded-scope limits: the author distance routine uses a finite 10^9 sentinel and the independent Floyd routine uses 10^8, so these are not general arbitrary-weight/infinity certificates. Their hard-coded finite tests remain safely below those sentinels. The author's controls omit zero weights and alternate tie priorities; the original independent controls include zeros but one fixed tie priority. Their process initializers rely on supplied tests having disjoint sources. Own controls enforce disjointness and nonnegative lengths, use actual infinity, and test both tie priorities. These observations narrow computation, not the written universal lemma.

## Exact gaps and route status

| Mechanism | Evidence/status | Exact remaining gap |
|---|---|---|
| Irreversible protected path | Analytic deduction and finite adversarial tests: verified | No discovered gap under stated model |
| All-n diagonal and o(log n) | Independent quantifier reconstruction and arithmetic controls: verified | Existence only; no effective or sharp schedule |
| Seed vertex/half-edge resources and repair | Analytic deductions and exact repair controls: verified | No discovered gap under assumptions |
| Uniform root to macroscopic fraction | Exact identity plus Markov: verified | Nonuniform/adaptive root choices are outside this identity |
| Fixed-time joint exploration | Independent reconstruction supports candidate proof | Finite tests cannot prove this universal stochastic input; full exposure proof remains the theorem's essential dependency |
| Endpoint-only/Voronoi/open-ball routes | Explicit counterexamples: blocked | Reopen only with a new mechanism; these cannot replace protected paths |
| Fixed seed count, prescribed budgets, adversarial strong root | Outside claimed theorem | Separate unresolved problems |
| Source provenance and novelty | Not assessed by this family | No priority or source-scope verdict supplied |

No weakening of degree/rate assumptions was silently inferred. Bounded support makes diverging-threshold seeds impossible but violates the candidate assumptions. Degree-one laws remove the guaranteed forward ray; infinite-second-moment laws remove this finite-mean nonexplosion argument. Adaptive root choice after seeing matching or weights is outside the theorem. A literal finite-n fallback convention on the negligible missing-degree-class event can be stated explicitly if needed; it has no effect on the asymptotic bounds.

This family is complete. It supports the stated path/diagonal deductions and identifies a checker repair, while reserving the universal local exploration and source/novelty questions for their appropriate independent evidence. All retained source/raw material is private by default. Only this report is public-allowlisted; no publication action was taken. The recursive inventory lists every retained own file, with final read-only modes. First seals are unchanged.
