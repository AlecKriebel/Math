Editorial note: The complete authored text is preserved below. Only references to undistributed operational artifacts, their identities, locations and replay directions have been replaced with descriptive prose. Mathematical arguments, evidence counts, corrections and limitations are retained. This prose edition identifies its distributed files and public scholarly sources. Historical conditions in the source record are distinguished from current dependency status in ACCEPTANCE_AND_DEPENDENCIES.md.

# Exact finite obstruction-cycle search for row 1754 / 3276 / OPG1808

## Result and strict scope

**Bounded computational evidence, not a solution of the all-size conjecture.** Both the incremental transitive-closure engine and a separately implemented adjacency-rebuilt Warshall engine exhaustively find no admissible obstruction-cycle completion for orders 3 through 8. Together with the credited minimal-counterexample reduction and the elementary orders 1 and 2, this verifies the stated tournament assertion for every nonempty tournament with at most 8 vertices, subject to the usual correctness obligations for the supplied programs and their independent audit.

The fixed three-periodic cycle-color pattern 0,1,2,0,1,2,... is also excluded at cycle lengths 3, 6, and 9. Consequently a minimal counterexample with that periodic obstruction cycle would have at least 12 vertices. **General order 9, periodic lengths 12 and higher, and the unrestricted conjecture remain unproved here.** No current-literature, priority, or novelty claim is made.

The original assertion is: a nonempty finite tournament with its arcs colored using at most three colors contains either a **cyclic directed rainbow triangle** or a vertex from which every other vertex is reachable by a monochromatic directed path. The color may depend on the target. Transitive rainbow triangles are allowed. The property is an outgoing universal source, not an incoming universal sink.

## Exact outputs

The six rows below describe the full obstruction-cycle class, modulo only cyclic vertex rotation and global permutation of the three colors. Both closure engines produce the same counts.

| Order | Canonical cycle-color words | DFS states | Dead states | Completions |
|---:|---:|---:|---:|---:|
| 3 | 3 | 0 | 0 | 0 |
| 4 | 6 | 4 | 4 | 0 |
| 5 | 9 | 35 | 16 | 0 |
| 6 | 26 | 1,307 | 495 | 0 |
| 7 | 53 | 83,761 | 32,160 | 0 |
| 8 | 146 | 14,944,184 | 5,728,965 | 0 |

For the single three-periodic word, order 6 uses 74 states / 26 dead states, and order 9 uses 353,866 states / 106,035 dead states. Order 3 is rejected during cycle insertion. Full exact outputs, constraint flags, and control results are in `the original operational record`.

An independent Python direct-BFS enumeration inspects all 46,879 labeled, oriented, three-colored tournaments of orders 1 through 4, with zero counterexamples. It does not use the obstruction-cycle reduction or either C++ closure engine. The Python orbit checker constructs all raw color words through length 9 and minimizes over the literal full color-permutation/rotation group; at length 9 there are 369 orbits. **That word count is not a search of all order-9 tournament completions.**

## Credited mathematical dependency

The only external mathematical reduction used for the all-tournament bound is Shen's minimal-counterexample Hamilton-cycle lemma, reproved as Lemma 2.1 in Agelos Georgakopoulos and Philipp Sprüssel, *On 3-coloured tournaments*, arXiv:0904.1967v2, https://arxiv.org/pdf/0904.1967v2. An explicit reconstruction and all enumeration/symmetry arguments are in `FINITE_PROOFS.md`.

No other source theorem is used as a pruning rule. In particular, interval-local reachability, all-three-color incidence, and nonmonochromatic incoming/outgoing neighborhoods are **not assumed by this search**. The search permits any completion satisfying just: the displayed directed Hamilton cycle, no cyclic rainbow triangle, and failure of each vertex to reach its predecessor in every color. It need not satisfy reachability of all other vertices or induced minimality. Thus it searches a superset of the candidates supplied by the reduction.

Section 2 of the inspected arXiv source explicitly leaves its three-color periodic obstruction-cycle question unresolved. This packet only checks the finite lengths stated above; it does not settle that source question. `the original operational record` records the inspected public source's hashes and scope without redistributing source text.

## Replay and audit

Requirements: Python 3 standard library, a C++17-capable `g++`, and ordinary local process execution. No network, solver, numerical library, or installation is needed.

1. Run the original externally pinned integrity check to validate the pinned manifest and every file hash.
2. Run the original normal-mode audit/replay operation to recompile the engine into a fresh temporary directory, reproduce both closure methods at every claimed bound, rerun independent raw enumeration and orbit checks, and test explicit failure gates. Expected completion is about one minute on the original machine; hardware affects time, not scope.
3. Optimization-mode replays are supported by the original optimized-mode audit/replay operation and the original optimized-mode audit/replay operation. All proof-related guards use explicit exceptions/exit checks, not Python `assert`.

The independent auditor should inspect the credited reduction, the two closure algorithms, the triangle predicate, the canonical-word proof, and completeness of DFS, rather than treating hash consistency alone as mathematical verification. Read-only hash validation does not replay search. Neither engine uses floating-point arithmetic or an external SAT solver. No formal proof-assistant or DRAT certificate is claimed.

## Hostile controls and failure behavior

- A transitive rainbow triple is accepted by the direct theorem checker and has its actual source.
- A cyclic rainbow triple has no monochromatic universal source; removing only the rainbow restriction makes the fixed-cycle search find it.
- A rainbow triple feeding a fourth sink has an incoming universal sink and no outgoing universal source, testing directionality explicitly.
- An all-red directed triangle reaches predecessors by multi-edge paths; removing only the predecessor restriction restores excluded candidates.
- Singleton, invalid empty tournament, malformed arc vectors, invalid colors, invalid CLI input, incompatible periodic/symmetry scope, and out-of-range orders are checked explicitly.
- Mutated result copies with a nonzero solution, missing bound row, inflated order, disabled rainbow test, periodic scope changed to unrestricted, corrupted count, omitted raw word, or failed control are rejected.
- The external pin and file manifest reject source/result mutation before accepting a frozen packet. A missing pin or unknown extra packet file is a failure.

## Stopping condition

This lane ends after replay and independent audit of the exact stated finite bounds. It makes no assertion about a counterexample's existence, impossibility at all orders, or the status of any larger search. It does not change a queue, repository, or publication state.
