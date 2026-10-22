# Five-turn partial result: trace-reinforced ant walks

**The original target remains unresolved after five substantive author turns.** Recommended eventual queue disposition: `unsolved`, 5/5, after separate review of these partial claims. No claim of novelty or priority.

## What is proved in this packet

1. TURN_1.md gives the exact general trace-probability drift through a killed-edge Dirichlet Laplacian and a rank-two formula. It keeps terminal edges and conductance Green functions explicit.
2. TURN_2.md proves a deleted-edge occupation-time representation. Each edge's probability divided by its own conductance is strictly decreasing when other weights are fixed. This gives coordinate equilibrium uniqueness, not global uniqueness.
3. TURN_3.md proves that the natural per-capita field is not a gradient, even after fixed positive diagonal reweighting, on a simple triangle. A finite ODE search is inconclusive and is labeled as such.
4. TURN_4.md proves almost-sure deterministic limits on every ordinary finite tree. The N–F path edges have limit one. A reachable branch edge at depth k from a path attachment a has limit ((d−1)/d)^k, with d the distance from a to F. It proves stochastic boundary exclusion where required, and handles zero branches and inaccessible components separately.
5. TURN_5.md proves almost-sure deterministic positive limits for any finite connected cyclic core rooted at N when food is attached by a fresh path of length d≥2. The limits are the unique positive solution of an effective-conductance system. Equilibrium uniqueness, global ODE attraction, and stochastic persistence are proved separately.

## Exact remaining gap

For a general finite graph with competing routes to food, the trace-probability drift need not be cooperative, the coordinate uniqueness argument is insufficient, and no general Lyapunov function or exact counterexample was obtained. The finite numerical search does not resolve these issues. Neither the tree theorem nor the cyclic-core theorem settles all admissible finite graphs.

The separate several-food question is also not solved in its intended generality. Absorption at any food and selection of a target food before each walk are distinct possible models. Wiring food vertices may create excluded parallel food edges, so the original single-food conjecture cannot simply be transferred. The source states no precise optimality criterion for a “meaningful” extension.

The source's no-parallel-food qualification is preserved. The already known parallel-edge Pólya/Dirichlet example is not offered as a new counterexample. The 2026 two-nest result uses loop-erased reinforcement and is not a solution of this trace-reinforced question.

## Verification and artifacts

`python verify_exact.py` supplies finite exact algebra, network, and drift controls. `OPENBLAS_NUM_THREADS=1 python explore_turn_3.py` reproduces the fixed-seed finite ODE diagnostics. Their receipts state the limitations. The analytic and stochastic proofs, not finite controls, carry the scoped theorem claims.

The full source PDFs stay outside this portable folder. SOURCE_AUDIT.md and source_manifest.json identify versions, model conventions and access. The source gate consumed no proof turn. turn_history.jsonl preserves all five substantive attempts, including the failed potential route and incomplete general result. The global queue has not been regenerated.
