# Conflict-block follow-up on 22 catalog-derived E=2 graphs

Evidence label: **REPRODUCIBLE COMPUTATIONAL OBSERVATION**

The preregistered portfolio completed all 22 runs.  It found no \(E=0\) or
\(E=1\) graph.  Every retained final remained at \(E=C_5+I_5=2\), so this is a
bounded search observation and not an order-43 \(R(5,5)\) construction,
nonexistence result, or basin-exhaustion claim.

## Frozen scope

The complete set of 22 distinct raw graph6 outputs from the independently
replayed catalog-seed search was registered before execution.  Its initial
color-side distribution was balanced:

- 11 graphs with \(C_5=0,I_5=2\);
- 11 graphs with \(C_5=2,I_5=0\).

Each line received one unique fresh seed, 2026082201 through 2026082222 in the
registered line order.  The retained conflict-hypergraph ProbSAT/block
algorithm used the same move sampling, noise, degree penalty, breakout,
multi-conflict shake, restart, and full-audit parameters as the ten-run pilot.
Only the preregistered budget changed to 5,000 selected moves in each of two
restarts, or 10,000 per graph and 220,000 total.

The frozen plan is
`results/benchmark_plans/conflict_block_catalog22_followup_v1.json`, SHA-256
`0348b6342395492414fb1a1b350ce6200c2c38b2f207826b25479b6f0b94ab35`.

The preregistered mobility hypothesis required at least 16 of 22
positive-Hamming \(E=2\) finals and at least one color-side transition.  It did
not preregister a positive minimum for the exploratory \(E=0\) or \(E=1\)
rates.

## Exact coverage

| Catalog line | Seed | Initial side | Final side | Final \(E\) | Hamming from start |
|---:|---:|---|---|---:|---:|
| 1 | 2026082201 | I5-only | C5-only | 2 | 37 |
| 2 | 2026082202 | C5-only | C5-only | 2 | 38 |
| 3 | 2026082203 | I5-only | C5-only | 2 | 37 |
| 4 | 2026082204 | C5-only | C5-only | 2 | 38 |
| 11 | 2026082205 | I5-only | C5-only | 2 | 37 |
| 14 | 2026082206 | I5-only | C5-only | 2 | 37 |
| 18 | 2026082207 | C5-only | C5-only | 2 | 38 |
| 24 | 2026082208 | I5-only | I5-only | 2 | 38 |
| 44 | 2026082209 | C5-only | C5-only | 2 | 38 |
| 131 | 2026082210 | I5-only | C5-only | 2 | 37 |
| 144 | 2026082211 | I5-only | C5-only | 2 | 37 |
| 152 | 2026082212 | C5-only | C5-only | 2 | 38 |
| 163 | 2026082213 | I5-only | C5-only | 2 | 37 |
| 177 | 2026082214 | I5-only | C5-only | 2 | 37 |
| 183 | 2026082215 | C5-only | C5-only | 2 | 38 |
| 253 | 2026082216 | C5-only | C5-only | 2 | 38 |
| 278 | 2026082217 | I5-only | C5-only | 2 | 37 |
| 316 | 2026082218 | C5-only | C5-only | 2 | 38 |
| 325 | 2026082219 | C5-only | C5-only | 2 | 38 |
| 326 | 2026082220 | I5-only | C5-only | 2 | 37 |
| 327 | 2026082221 | C5-only | C5-only | 2 | 38 |
| 328 | 2026082222 | C5-only | C5-only | 2 | 38 |

Coverage is 22/22 registered lines, each exactly once with its preregistered
seed and full 10,000-selected-move budget.

## Constructive and mobility rates

| Outcome | Count | Rate |
|---|---:|---:|
| \(E=0\) | 0/22 | 0% |
| \(E=1\) | 0/22 | 0% |
| Positive-Hamming \(E=2\) escape | 22/22 | 100% |
| Positive-Hamming \(E\leq2\) mobility | 22/22 | 100% |

The mobility hypothesis passed: 22 escapes exceeded the registered threshold
of 16, and color-side transitions occurred.

## Color-side transitions

- \(C_5\)-only \(\to C_5\)-only: 11/11.
- \(I_5\)-only \(\to C_5\)-only: 10/11.
- \(I_5\)-only \(\to I_5\)-only: 1/11, catalog line 24.

Thus 21 of 22 final graphs are \(C_5\)-only, while line 24—the unusual
454-edge member of the input corpus—remains \(I_5\)-only.  The side imbalance
is an empirical property of this labeled, fixed-seed portfolio and is not
claimed as an algorithmic invariant.

## Hamming diversity

Distances from each retained final to its own registered start have minimum
37, maximum 38, mean 37.5454545455, and median 38.  There are 22 distinct raw
final graph6 payloads.

Across all 231 pairs of retained finals, labeled edge Hamming distances have
minimum 124, maximum 490, mean 436.9220779221, and median 440.  The input
corpus's corresponding figures were minimum 115, maximum 488, mean
435.4761904762, and median 439.  The mutation therefore preserved broad
labeled diversity while moving every individual start by a similar local
distance.

## Comparison with the ten-run pilot

The original pilot's three \(E=2\) incumbents produced positive-Hamming
\(E=2\) escapes in all 6/6 start-seed runs.  This follow-up reproduced the
escape rate on a much more diverse corpus at 22/22.  Both experiments had
best objective \(E=2\), with zero \(E=0\) and zero \(E=1\) outcomes.

The earlier pilot also reduced its catalog-derived \(E=104\) start to \(E=2\)
twice but failed to improve a global \(E=231\) start.  The current result
strengthens the evidence that this mutation moves readily among nearby
\(E=2\) states, but supplies no evidence that it can cross the final
\(E=2\to E=1\) barrier.

## Execution and verification

The portfolio executed 220,000 selected moves, evaluated 5,091,883 candidate
moves, applied 352 multi-conflict shakes, and used 475.396043 aggregate search
seconds.

Every final graph passed all three retained checks:

1. direct Python enumeration of every five-set and all ten pairs;
2. the separately compiled C++ recursive-bitset graph/complement verifier;
3. an independent audit of objective counts, degree penalty, Hamming distance,
   graph6 payload, improvement trace, and step budget.

No \(E=0\) graph appeared.  The runner was configured to write any such graph
immediately, stop the active run and all later registered runs, repeat the
direct and structural verifications, then perform canonical export and the
adversarial construction audit.

The output directory contains 110 compact files totaling 105,381 bytes, below
the registered 20,000,000-byte limit.

Machine-readable results are in
`results/verification/conflict_block_catalog22_followup_summary.json`,
SHA-256
`55b09b6f5c020b43eb892076e3768712dcba2fa754753523ca9fc10fa2ebea66`.
