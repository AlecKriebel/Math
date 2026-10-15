Editorial note: The complete authored text is preserved below. Only references to undistributed operational artifacts, their identities, locations and replay directions have been replaced with descriptive prose. Mathematical arguments, evidence counts, corrections and limitations are retained. This prose edition identifies its distributed files and public scholarly sources. Historical conditions in the source record are distinguished from current dependency status in ACCEPTANCE_AND_DEPENDENCIES.md.

# Recovery acceptance: finite tournament obstruction-cycle search

Date: 12 October 2026 UTC. Row 1754 / problem 3276.

## Current decision

**RECOVERY ACCEPT, bounded only.** The exact original final v2 candidate was restored, freshly reviewed, and freshly replayed. This acceptance relies on the new recovery checks, not merely the historical acceptance summary or restored hashes. The unrestricted conjecture is not resolved.

Accepted candidate manifest: SHA-256 `[verified undistributed artifact identity]`, [verified original byte count omitted], nine exact-hash files. Search source: SHA-256 `[verified undistributed artifact identity]`, [verified original byte count omitted]. The independent recovery audit pins and verifies the complete candidate before and after each run.

Every nonempty tournament of order at most 8, with arcs colored from at most three colors, has either a directed cyclic rainbow triangle or a vertex reaching every other vertex by a monochromatic directed path. Path color may depend on destination. Transitive rainbow triples are allowed; the universal vertex is an outgoing source in the monochromatic reachability relation.

In addition, the single three-periodic cycle-color pattern 012012... is excluded at lengths 3, 6, and 9. Therefore a minimal counterexample with that periodic obstruction cycle has order at least 12. General order 9, periodic lengths 12 and above, and all-size resolution remain unproved. No novelty or current-literature-status claim is made.

## Fresh proof and code review

The recovered complete `FINITE_PROOFS.md`, `the original checker`, and `the original checker` were reread. The source convention and Shen reduction were freshly checked in the restored primary text of Georgakopoulos and Sprüssel, [On 3-coloured tournaments, arXiv:0904.1967v2](https://arxiv.org/pdf/0904.1967v2), Conjecture 1.2 and Lemma 2.1. The PDF and extracted-text hashes match the original source metadata. The finite proof is explicit below and does not depend on another new or unproved structural lemma.

For a minimal counterexample, define auxiliary edges y→x only for distinct vertices such that x fails to reach y monochromatically. Each is an actual tournament edge. Every vertex has an incoming auxiliary edge, so the finite loopless graph, which has no opposite edge pair, contains a directed cycle of length at least three. In the cycle-induced subtournament every vertex still fails to reach its predecessor, and cyclic-rainbow exclusion is inherited. Hence it is also a counterexample, forcing the cycle to be spanning by minimality. An extra failed pair other than a predecessor closes a strictly shorter auxiliary cycle; the successor is directly reachable and cannot be a failed target. Thus the obstruction cycle supplies all vertices and the required predecessor failures. This is the credited Shen lemma. The explicit self-pair exclusion in the accepted v2 proof was verified. Orders 1 and 2 have actual outgoing sources; the empty tournament is excluded.

The exact finite search requires only the fixed cycle i→i+1, exclusion of cyclic rainbow triangles, and failure of every vertex i to reach i−1 monochromatically. All other unordered pairs have all six oriented-color possibilities. No stronger interval, incidence, or minimality condition is imposed, and no nonpredecessor reachability is assumed. It therefore searches a superset of the reduced minimal counterexamples.

First-occurrence color normalization gives the lexicographic minimum under a global color permutation, including one- and two-color words. Restricted-growth generation lists all normalized words; taking the minimum normalized rotation gives precisely one word in each color/rotation orbit. These symmetries preserve direction, predecessor identities, and both forbidden conditions. No reflection, arbitrary vertex relabeling, or division by orbit size is used.

A forbidden monochromatic predecessor path or cyclic rainbow triangle cannot disappear after adding edges, so partial-state pruning is sound. For a newly inserted arc u→v of color c, every new cyclic triangle uses existing v→w→u. In color c, if A is u plus its old ancestors and B is v plus its old descendants, exact positive-length reachability updates by R∪(A×B), including newly created diagonal cycles. The second engine instead rebuilds adjacency and runs Warshall closure. Its affected-color predecessor test and the incremental test use the same outgoing convention.

Every selected unassigned chord branches over all values that survive these sound tests. An empty domain certifies impossibility; early selection of a singleton only changes search order. Induction on unassigned pairs establishes completeness and disjointness. Cycle insertion uses the same predicates. No search cap is used in accepted runs; accepted counters and bit shifts remain in range. These checks are computer-assisted evidence, not a proof-assistant or formal unsatisfiability certificate.

## Fresh independent computation

All receipts in this recovery packet were generated after recovery. `the original checker` uses literal adjacency matrices and direct per-color BFS, independent of the candidate closure implementation. `the original checker` compares that oracle to both candidate engines and includes satisfiable hostile fixtures. `the original checker` recompiles everything into temporary directories, runs the checks, mutates actual candidate source, and rejects invalid scopes using explicit exception gates.

1. Raw enumeration covers all 46,879 labeled, oriented, three-colored tournaments of orders 1 through 4. Rainbow-free counts are 1, 6, 204, and 37,152; there are no target counterexamples.
2. Literal raw fixed-cycle enumeration covers 1,892,511 completions over orders 3 through 5, without partial-state pruning. The candidate matches all 24 raw/canonical and relaxed-constraint scopes. At order 5, raw counts for neither constraint, only cyclic-rainbow exclusion, only predecessor nonreachability, and both are respectively 1,889,568; 743,718; 53,190; and zero. The nonzero controls detect an always-zero or overpruned enumerator.
3. A deterministic direct-BFS harness checks 746,070 proposed arc insertions across 9,600 partial-state trials, orders 3 through 8, both engines, and all four constraint combinations. It verifies all closure bits, including positive-length diagonal cycles, after 581,193 accepted proposals and confirms state immutability after 164,877 rejections.
4. Literal group minimization checks all 29,511 color words of lengths 3 through 9 against the candidate canonical predicate. Orbit counts are 3, 6, 9, 26, 53, 146, and 369. Seventy-eight transformed fixtures test global-color and rotation invariance. Fixtures distinguish cyclic from transitive rainbow triples, multistep monochromatic reachability from single edges, and outgoing source from incoming sink.
5. The auditor freshly ran the complete candidate replay. Both closure engines reproduce every accepted general order 3 through 8 and periodic length 3, 6, 9. The general order-8 run has 146 words, 14,944,184 DFS states, 5,728,965 dead states, and zero completions. The replay also repeats all raw color-word cycles through order 6 and its own raw tournament/orbit reference checks.

The independent raw tournament enumeration is exhaustive through order 4, and its raw fixed-cycle enumeration through order 5. Higher-order acceptance combines the inspected completeness proof, full candidate dual-engine replay, independent BFS/state tests, word-orbit checks, and actual code mutations. This report does not claim a wholly independent unrestricted order-8 brute-force enumeration.

## Fresh optimization and hostile gates

Independent recovery audits pass in normal Python, `-O`, and `-OO`, with identical substantive results. In each mode six actual code mutations are detected: successor substituted for predecessor; corrupted triangle distinct-color test; omitted closure update; omitted new target from descendants; dropped sixth chord branch; and suppressed third colors. Four altered result controls and eight invalid candidate CLI scopes are rejected. Five out-of-scope independent-enumerator requests also fail explicitly.

The candidate's complete normal replay reproduces its eight result-mutation controls and eight CLI failure gates. Candidate byte verification and its six actual integrity mutations pass in normal, `-O`, and `-OO`. The recovery acceptance verifier separately checks seven semantic corruptions, including substitution of a historical receipt, and six integrity corruptions. Post-freeze verification is recorded outside the frozen packet so it cannot alter its own manifest.

## Recovery provenance and reproduction

`FINITE_RECOVERY_SCOPE.md` separates historically recovered content from freshly reissued checks. `FINITE_HISTORICAL_AUDIT.md` exactly recovers the original authored report at [verified original byte count omitted] and SHA-256 `[verified undistributed artifact identity]`. Its old manifest and receipt links remain historical. This recovery packet has a new manifest, external pin, and terminal receipt. It does not claim that the entire old audit tree or missing receipt files survived.

Run the original normal-mode audit/replay operation, the original optimized-mode audit/replay operation, and the original optimized-mode audit/replay operation for the independent tests. Run the recovered candidate's `the original checker` for every claimed higher-order finite search. Run the original externally pinned audit integrity and hostile-control check to verify the sealed packet and recorded semantic scopes; that command does not itself replay searches.

No new research pass, enlarged search scope, remote write, queue change, or publication action occurred in this audit. The final mathematical status remains bounded progress, with the unrestricted target unresolved by this work.
