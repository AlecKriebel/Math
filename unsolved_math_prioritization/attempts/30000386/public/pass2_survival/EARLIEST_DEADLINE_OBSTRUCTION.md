Scope: an authored mathematical partial result for the exact two-dimensional king-move Time-Bomb game. The unrestricted conjecture is not resolved. No novelty claim is made. Original contract SHA-256: 1be42b4f13460a91a71948fc532c135b7453f56811566ed5c3f918f8976c5c4c.

## 3. Fixed-size earliest-deadline memory is insufficient

This obstruction concerns a precisely restricted deterministic policy. At Angel move n, call a deadline pending when t≥n. The policy retains only the k earliest distinct raw pending deadlines and the bombs at those deadlines. Its move may depend on time, its previous moves, and the successive retained-history projections, but not on discarded deadline data or hidden summaries of those data. If two histories have identical such projections, the policy makes the same move. This definition does not cover a policy that first removes spatially irrelevant bombs and then selects k remaining deadlines.

**Theorem 2.** For each fixed k≥1, every such policy is defeated by a legal Devil, even though the policy may inspect retained timestamps arbitrarily far into the future.

Let M=(2k+1)² and T=2k+M+1. During rounds 1,...,k, announce one fixed decoy bomb at each of the k distinct times T−k,...,T−1. Their positions may all be the origin. There is no detonation during these first k rounds.

For the remaining construction, simulate the policy through its move at time T−k using only this retained decoy history. Up to and including that move all k decoys are still pending under the t≥n convention, so bombs at time T are excluded from the retained history. Thus their positions do not affect this simulated path. If a decoy would kill the policy, the Devil has already succeeded; otherwise let a_* be its simulated position at time T−k.

In rounds k+1,...,k+M, announce the M pairs (p,T) for all p in a_*+[−k,k]², in any fixed order. These announcements are complete by

k+M = T−k−1.

They remain hidden from the restricted policy through its move at T−k. The actual and simulated positions up to that move therefore agree unless there has already been a fatal decoy collision. At the next move the first decoy is expired and deadline T may become retained, but only k moves remain between position a_* at time T−k and time T. Every possible endpoint lies in a_*+[−k,k]², all of which is bombed at T. Hence the policy loses no later than T.

The schedule is determined in advance once the deterministic policy is fixed; no future Angel choices are observed. The argument does not defeat policies capable of using unboundedly many pending deadlines, or randomized policies outside this precise sensitivity class. It supplements, rather than replaces, the earlier bounded time-distance-lookahead obstruction.
