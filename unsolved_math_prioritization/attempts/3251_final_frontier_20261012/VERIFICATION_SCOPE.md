# Exact finite coverage and vacuity

These are bounded regression checks supporting all-size proofs. Original authored and independent programs are not distributed here. Their audit reports preserve exactly what was run; this prose edition is not a standalone replay package. All stated runs use normal Python, -O and -OO with identical mathematical outputs and explicit, optimization-stable gates.

## Main projection universe

The full original selected-subfamily definition is compared to complete dual components for each eligible prescribed set, then every partial assignment is compared with a direct full-coloring oracle. Graph cliques mean maximum cardinality, and eligible P contains every vertex of original incidence at least three. Empty families, empty graphs and vacuous assignments are included within the declared universes.

| Universe | Objects | Prescribed sets | Partial colorings | Successes | Failures |
| --- | ---: | ---: | ---: | ---: | ---: |
| Rank-tagged uniform families on at most five vertices | 1,078 | 7,694 | 90,569 | 55,235 | 35,334 |
| Nonuniform families on at most four vertices | 37 | 341 | 1,891 | 1,611 | 280 |
| Eligible graphs among all 1,100 labelled graphs on at most five vertices | 660 | 19,288 | 149,013 | 133,611 | 15,402 |

The total is 241,473 partial colorings and 51,016 failures. Exactly 4,014 definition-tree instances have overlapping boundary unions and are discarded. Nine targeted fixtures and three out-of-scope rejection inputs are described in the complete audit. The source's eight limitation checks have their own fixed scope and are not an additional exhaustive graph universe.

## Authored chordal realization fixtures

These are 19 specific path, star and broom fixtures, not all graphs or all trees of their orders. Each row checks all indicated core assignments, exact reconstructed maximum cliques, incidences, chordality and explicit successful full-graph witnesses. Exactly two assignments fail per fixture.

| Tree | k | Nodes | Graph vertices | Core vertices | Maximum cliques | Core assignments |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| path | 3 | 1 | 15 | 3 | 7 | 8 |
| path | 3 | 2 | 21 | 4 | 10 | 16 |
| path | 3 | 3 | 27 | 5 | 13 | 32 |
| path | 3 | 4 | 33 | 6 | 16 | 64 |
| path | 3 | 5 | 39 | 7 | 19 | 128 |
| path | 3 | 6 | 45 | 8 | 22 | 256 |
| path | 3 | 7 | 51 | 9 | 25 | 512 |
| path | 4 | 1 | 28 | 4 | 9 | 16 |
| path | 4 | 2 | 43 | 6 | 14 | 64 |
| path | 4 | 3 | 58 | 8 | 19 | 256 |
| path | 4 | 4 | 73 | 10 | 24 | 1,024 |
| path | 4 | 5 | 88 | 12 | 29 | 4,096 |
| path | 5 | 1 | 45 | 5 | 11 | 32 |
| path | 5 | 2 | 73 | 8 | 18 | 256 |
| path | 5 | 3 | 101 | 11 | 25 | 2,048 |
| star | 3 | 4 | 33 | 6 | 16 | 64 |
| star | 4 | 5 | 88 | 12 | 29 | 4,096 |
| broom | 3 | 7 | 51 | 9 | 25 | 512 |
| broom | 4 | 7 | 118 | 16 | 39 | 65,536 |

The total is 79,016 core assignments: 78,978 successes and 38 failures. The largest graph has 118 vertices. A separate independent universe reconstructs 433 labelled-tree/rank fixtures of orders one through five for ranks three, four and five with maximum degree at most the rank, plus longer paths through twelve nodes and rank-sized stars: 457 graphs and 43,514 vertices in aggregate. All 7,400 assignments in its at-most-three-node fixtures are enumerated. An independent exact-source fixture oracle separately checks all 79,016 assignments in the 19 authored fixtures. These totals overlap in scope and are not summed as a single unique universe.

## Separate repeated leaf supplement

| k | Graph vertices | Base vertices | Core vertices | Maximum cliques | Odd base subsets searched | All core assignments enumerated independently |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 4 | 58 | 13 | 9 | 20 | 3,797 | 512 |
| 5 | 105 | 17 | 13 | 27 | 64,839 | 8,192 |
| 6 | 166 | 21 | 17 | 34 | 0 | not enumerated |
| 7 | 241 | 25 | 21 | 41 | 0 | not enumerated |

The two exhaustive odd-base-subset searches inspect 68,636 subsets and find no odd hole. These are subsets of the base graphs, not of the full 58- and 105-vertex graphs. At k=6,7 the zero subset count means no such exhaustive search, not a zero-hole computational result. The all-size hole proof and exact simplicial reductions apply. The independent reduced-graph cycle enumeration finds respectively 6, 8, 10 and 12 induced four-cycles and no longer holes.

At k=4,5 every one of the 8,704 combined core assignments is checked against all sixteen low-vertex assignments and successful full-graph witnesses; two fail at each rank. At k=6,7 all core assignments are not individually enumerated: the exact symbolic projection and the sixteen low assignments under the bad prescription are checked. All four fixtures are specific family members, not all graphs at those orders.

## Structural graph universe

| Order | Labelled graphs | Odd hole free | Antineighborhood hypothesis | Indivisible | Gap bound cases | Universal boundary cases |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 0 | 1 | 1 | 0 | 0 | 0 | 0 |
| 1 | 1 | 1 | 0 | 0 | 0 | 0 |
| 2 | 2 | 2 | 1 | 0 | 0 | 14 |
| 3 | 8 | 8 | 1 | 0 | 0 | 108 |
| 4 | 64 | 64 | 4 | 0 | 0 | 1,240 |
| 5 | 1,024 | 1,012 | 58 | 12 | 0 | 22,950 |
| 6 | 32,768 | 30,824 | 1,658 | 612 | 0 | 0 |

There are 33,868 labelled graphs on orders zero through six, including 31,912 odd-hole-free graphs, 1,722 satisfying the antineighborhood hypothesis, 624 indivisible graphs, and 91 vertex-critical graphs under the source convention (including the empty graph). The 624 indivisible graphs are outside the odd-hole-free target class. The antineighborhood equality implication with positive chromatic gap is exercised 12 times. Universal-vertex boundary flexibility is checked on 24,312 admissible boundary colorings only through order five; the order-six zero means that boundary enumeration was not performed there.

The strengthened odd-hole-free chromatic-gap hypothesis q>=r+2 occurs zero times in the entire order-at-most-six universe. That finite implication is vacuous there. It is not finite evidence for existence or sharpness of the equality forms. Seven larger named benchmarks and 10,814 exact critical-factor parameter tuples exercise separate constraints, and 3,213 arithmetic instances cover k=4 through 30 and up to eight cutset components. Parameter tuples are not claims of graph realizability.

The seven benchmarks are C5, C7, the seven-antihole, K1 joined to the seven-antihole, the Mycielski graph of K4, two joined seven-antiholes, and two joined five-cycles. A separate C5[C5] fixture has 25 vertices, clique number four, chromatic number eight, 125 maximum cliques and core size 25. Its 32 local colorings and 243 global state patterns show indivisibility, but it contains an induced odd hole and is not a target counterexample.

These checks do not reprove Gallai or CRST, replay the published Folkman enumeration, or settle the conjecture. The structural audit additionally verifies all 580,542 vertex-critical induced-subset instances, including the harmless empty computational case. Its graph and boundary streams and all bounded arithmetic records agree exactly with the authored data. The k>=3 indivisibility and core-gap implications are vacuous in the small graph universe.

## Original audit integrity coverage

The main projection audit independently required 85 mutation scenarios and 165 program rejections per mode, 495 total. The separate repeated-leaf audit required 71 scenarios and 138 rejections per mode, 414 total. Both include re-manifested and re-pinned semantic mutants, all source members, dependency failures, symlinks, missing arguments and false mathematical obligations. The structural audit separately reruns 65 authored and 67 independent negative controls per mode; these include a false mathematical gate under every optimization mode. Authored controls and audit controls are distinct evidence, not pooled as independent proofs. No acceptance gate relies on Python assertions. The complete audits specify their exact static-security limits.
