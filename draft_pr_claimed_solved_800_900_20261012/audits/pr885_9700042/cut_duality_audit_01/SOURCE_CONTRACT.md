# Primary source contract (frozen before candidate inspection)

Timestamp: 2026-10-15T13:51:35Z. Completion estimate: 5% of this finite-geometry audit.

Primary source: [Aldous, discrete Hammersley/oriented flow problem](https://www.stat.berkeley.edu/~aldous/Research/OP/hammersley_flow.html), retrieved independently through the browser tool on this date. The parent retrieval receipt records HTTP 200 at 13:50:30Z; I separately read and hashed the actual downloaded HTML: 3,576 bytes, SHA256 `1c3078bb05b25554b7ab7bc12e6d8567b777407b6c6ad24fecfc89715088a301`. It agrees with the primary browser body. No candidate manuscript or previous audit has been read at this point.

## Exact model

For integer n >= 2, vertices are (i,j), 0 <= i,j <= n-1. Each nearest-neighbor edge points east or north and independently has capacity 1 with probability p and 0 otherwise. Paths share vertices freely but cannot share edges. Source vertices are

S = {(0,j): 0 <= j <= n-2} union {(i,0): 1 <= i <= n-2}.

Sink vertices are

T = {(i,n-1): 0 <= i <= n-1} union {(n-1,j): 0 <= j <= n-2}.

V_n(p) is the maximum count of open directed S-to-T paths, with no stated per-vertex throughput restriction. The normalization is 2n, and the stated limit is V_n(p)/(2n) -> v(p) in L1 for fixed p. The target is (1-v(1-q))/sqrt(2q) -> 1 as q decreases to zero, with the n limit taken first. This limiting order is part of the claim.

The source also proposes a covering-path interpretation and a continuum approximation, explicitly as a heuristic with an interchange-of-limits problem. Neither is accepted here as an exact finite identity without proof. In particular, no continuum statement will silently replace the directed edge-capacity model. Degenerate n=1 will be excluded; all-open and all-closed instances and the four square corners will be checked separately.

## Falsifiable finite criteria fixed in advance

1. Integral max-flow/min-cut must use precisely S,T above (unlimited auxiliary terminal arcs). An S/T separating cut pays only capacities of forward primal edges. Reverse crossings cannot be silently charged as forward ones.
2. A dual representation must specify boundary endpoints, edge orientation, crossing convention, and a rule for four-valent dual-face junctions; it must cover arbitrary cuts or justify reducing them to the represented class.
3. Any deterministic upper bound on flow deficit must hold for every closed-edge configuration, including isolated boundary defects, adjacent defects, fully closed edges, corner cuts, holes, multiple cut components, and self-touching dual contours.
4. A marked-list encoding must be injective enough for its counting inequality, or explicitly overcount with a proved bound; a completion must exist in the actual discrete model and preserve all claimed inequalities.
5. If the finite lemma is true, its use toward the target still requires estimates uniform enough in n at fixed q and an error o(sqrt(q)) after the n limit. A numerical finite check is evidence only for the exact finite range tested, never a proof of the asymptotic claim.

This contract is fixed. Later model corrections must be recorded rather than retroactively altering it.
