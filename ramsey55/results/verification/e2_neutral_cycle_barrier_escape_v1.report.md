# E=2 neutral-cycle and forced-barrier escape audit

## Outcome

No order-43 Ramsey graph was found. The retained 44-graph E=2 corpus has a
much more rigid labeled structure than the earlier mobility summaries showed:
the 22 catalog starts generate 22 pairwise-disjoint neutral cycles, each of
length 86, and every corresponding conflict-block final lies on the same
cycle as its start. Thus the prior positive-Hamming E=2 motion did not cross
between neutral components.

This is a reproducible computational observation about this corpus only. It is
not a theorem about every E=2 graph, is not a construction, and is not a
global nonexistence result for order 43.

## Exact neutral geometry

An independent Python checker used recursive bitset clique enumeration rather
than the C++ search implementation. It replayed all 44 stored graphs and, at
every generated neutral state, recomputed the outcome of all six shared-core
edge flips.

- There are 22 pairwise-disjoint labeled cycles and 1,892 total states.
- Every state has exactly two neutral shared-core edges and four worsening
  shared-core edges.
- A neutral flip changes the conflict color and again produces two
  same-color forbidden 5-sets intersecting in four vertices.
- Each 86-step cycle toggles exactly 43 distinct graph edges, each exactly
  twice.
- The two alternating barrier profiles are exactly
  `(9,9,9,38)` and `(10,10,12,15)`, each occurring at 946 states.
- No shared-core flip in these 1,892 states reaches E=0 or E=1.
- The 22 conflict-block finals occur at oriented cycle positions
  37, 38, 48, or 49; their stored Hamming distances all replay exactly.

The independent audit is
`results/verification/e2_neutral_cycle_audit_v1.json`
(SHA-256
`13a5ff1f9572f385d86d89751ff935a8289a321310f40cf5969f5250a731936e`).

## Deliberate barrier crossings

The new in-memory C++ route avoids neutral-cycle trapping by forcing a
worsening shared-core edge, then using exact bitset objective deltas, tabu
repair, and repeated forced barriers.

A deterministic all-22 exploratory run performed 7,568 forced-barrier
rollouts and 910,881 repair steps, including 7,977 repeated barrier
crossings. It observed no E=0, E=1, or off-cycle E=2 state. Its retained
record is
`results/verification/e2_barrier_escape_walk_all22_v1.json`
(SHA-256
`26d42dac33b76a6bdf40920ef512b714831315b23fe3655de29cb9a5aea7b6b9`).
This run is heuristic and carries no negative conclusion.

## Exact short atomic bridges

The deterministic atomic scan covers all 1,892 audited neutral states.

- It checked all 6,826,336 ordered two-flip paths whose first flip is one of
  the four worsening shared-core edges and whose second flip is any other
  graph edge. The minimum two-flip objective was E=9.
- Retaining all 549,626 unique pair states through E=15, it checked
  32,465,774 targeted third flips. The only E=2 endpoints were the 1,892
  already-known neutral states; the new low endpoints comprised 16,082 E=3
  and 18,920 E=4 states.
- It checked all 903 fourth edges from every unique retained E≤4 triple
  state: 33,315,282 fourth-edge checks. Again, all E=2 endpoints were known;
  no E=0 or E=1 appeared.
- It then closed the resulting low region under all flips that touch a
  current conflict and remain at E≤4. The closure completed below its
  250,000-state cap with exactly 16,082 E=3 and 73,788 E=4 labeled states.
  It contained no E=0, E=1, or off-cycle E=2 state.

The exact scope matters: the first two flips have the specified
barrier-first form; third flips are taken from the retained pair state's
conflict-edge union; fourth flips are unrestricted; and the final complete
closure uses current-conflict edges only. Nothing here excludes paths outside
that finite neighborhood.

The retained result is
`results/verification/e2_barrier_escape_atomic_ceiling15_v1.json`
(SHA-256
`ee5b937b138f8c63dab8362ac269fda2550e2cd4e75f25810dc8f3d129c67948`).
The binding/count checker accepted every check; its output is
`results/verification/e2_barrier_escape_atomic_ceiling15_v1.check.json`
(SHA-256
`4d5de21f423b40672b98367382534ec35282a586f17504bcdb14b684a39666ea`).

## Reproducibility bindings

- Search source:
  `src/search43_e2_barrier_escape.cpp`,
  SHA-256
  `3c8f97d2dbff5b7736768b891c1b40f4f627ec0d353bb3d67f31154db4ea9c69`.
- Independent cycle checker:
  `verify/e2_neutral_cycle_audit.py`,
  SHA-256
  `9e2ad4abf1e4702222b6255c2d7f7d2461c3f26d96e50637ba8ed3df164fc6ad`.
- Cycle-checker tests:
  `tests/e2_neutral_cycle_audit_tests.py`,
  SHA-256
  `dbd5bb82f89df1873304c6a2a75b7bcdbf3c7af9ec35a789f7617077b4134d04`.
  All three tests passed.
- Result checker:
  `verify/e2_barrier_escape_result_check.py`,
  SHA-256
  `b0d0d022fdb30e06d46aae5a681cb0984d906a1e23c8fd57715e7f0bb4f0f076`.
- Result-checker tests:
  `tests/e2_barrier_escape_result_tests.py`,
  SHA-256
  `440871d024d9d580f4762042b0a94b96c44ce1853a7a49a95b2fc15f070cee2d`.
  Both tests passed, including a deliberate coverage-count tamper rejection.
- The C++ exact-delta self-check passed all 903 base-edge flips and a
  200-flip random sequence.

## Next constructive route

The useful frontier is no longer neutral E=2 motion. A follow-up should start
from canonical representatives of the 73,788 E=4 closure states and force a
second, explicitly out-of-closure barrier before repair, or use a bounded SAT
completion whose assumptions exclude all 1,892 known neutral states. Either
route directly targets component changes rather than rediscovering the
86-cycles.
