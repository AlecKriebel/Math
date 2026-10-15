Editorial note: The complete authored text is preserved below. Only references to undistributed operational artifacts, their identities, locations and replay directions have been replaced with descriptive prose. Mathematical arguments, evidence counts, corrections and limitations are retained. This prose edition identifies its distributed files and public scholarly sources. Historical conditions in the source record are distinguished from current dependency status in ACCEPTANCE_AND_DEPENDENCIES.md.

# Independent acceptance: finite tournament obstruction-cycle search

Date: 12 October 2026 UTC. Target: row 1754 / problem 3276.

## Decision

**ACCEPT the stated bounded computer-assisted conclusion. The unrestricted target is not resolved.**

Accepted candidate: `the original source packet`, final v2 manifest SHA-256 `[verified undistributed artifact identity]`, [verified original byte count omitted]. All nine manifested files were checked against that external pin before and after each final independent audit run. The executable source is SHA-256 `[verified undistributed artifact identity]`.

The finite assertion is valid for every nonempty tournament on at most eight vertices whose arcs receive colors from a palette of size at most three: either a directed cyclic triangle has three distinct colors, or some vertex reaches every other vertex by a monochromatic directed path, with the path color permitted to depend on the destination.

The additional accepted exclusion is only for obstruction Hamilton cycles colored by repetitions of three pairwise distinct colors at lengths 3, 6, and 9. A minimal counterexample with that particular periodic obstruction cycle must therefore have at least 12 vertices. General order 9, periodic lengths at least 12, and all-size resolution are not established. No priority or novelty claim is made.

## Exact searched universe

For each order n from 3 through 8, vertices are labeled cyclically so that every arc i→i+1 is present. The search fills every other unordered pair with one of six oriented-color choices, imposing only:

1. no directed cyclic rainbow triangle;
2. no monochromatic directed path from i to i−1, for every i.

Cycle-color words are reduced only by simultaneous cyclic vertex rotation and a single global permutation of the three colors. Chords receive their full six-valued domains. No reflection, arbitrary vertex permutation, independently recolored edge, all-three-colors incidence condition, interval reachability condition, or new structural theorem is imposed. In particular, the search does not require reachability of every nonpredecessor. It examines a superset of the minimal counterexamples supplied by the credited reduction.

## Mathematical review

**Reduction.** In an induced-subtournament-minimal counterexample, put y→x in an auxiliary graph exactly when x and y are distinct and x fails to reach y monochromatically. This edge is necessarily an actual tournament edge, so the auxiliary graph is loopless and has no opposite pair. Every vertex has an incoming auxiliary edge. Following such edges yields a directed cycle of length at least three. Every vertex on that cycle still fails to reach its predecessor in the induced subtournament, because deletion cannot create paths; the forbidden-triangle condition is also hereditary. Thus the cycle induces a counterexample and minimality makes it spanning. Any additional failed pair supplies a chord closing a strictly shorter auxiliary cycle: the successor cannot be a failed target because it is directly reached. This proves exactly the required obstruction-cycle reduction, and also the stronger unique-failed-predecessor conclusion. Uniqueness refers only to this obstruction cycle, not to arbitrary Hamilton cycles.

The first frozen proof did not explicitly exclude self-pairs from the auxiliary relation. The author accepted that precision correction and issued v2. The final definition is unambiguous even though the implementation stores positive-length reachability. Orders 1 and 2 have actual outgoing sources. An empty tournament is outside the stated universe. The n=3 case is covered both directly and by enumeration.

**Credit and source boundary.** This is Shen's known structural lemma, explicitly reproved as Lemma 2.1 in Agelos Georgakopoulos and Philipp Sprüssel, [On 3-coloured tournaments, arXiv:0904.1967v2](https://arxiv.org/pdf/0904.1967v2). The supplied primary-source text of that lemma and its surrounding conventions was inspected. The supplied source PDF hash agrees with the author's provenance: `37c70064ec08aba920ed480061d68328341e61a0ddb2738a7100fb0d75660279`. This audit neither relies on another unproved all-size lemma nor interprets the source's periodic-cycle question as solved. No third-party source text is redistributed here.

**Symmetry.** First-occurrence color normalization is the lexicographically minimum image under a global color permutation, including words using only one or two colors. Restricted-growth generation lists all such normalized words once. Retaining the lexicographically smallest normalized rotation gives one literal representative of every rotation/color orbit even when the word has stabilizers. Both actions preserve cycle direction, predecessor identities, monochromatic reachability, and cyclic rainbow exclusion. No division by a presumed orbit size occurs.

**Pruning and closure.** Both forbidden features are monotone under inserting arcs. A newly created directed triangle must use the inserted arc u→v and existing v→w→u. The color test checks exactly that cyclic configuration. The incremental color-closure update is R∪(A×B), where A consists of u and its old same-color ancestors and B consists of v and its old same-color descendants. This accounts for every newly possible path and positive-length diagonal cycle. The fresh engine rebuilds affected-color adjacency and computes Warshall closure. Unaffected colors remain unchanged. Independent BFS checks below cover positive-length diagonal entries as well as distinct endpoints.

**Completeness.** An empty domain for any unassigned pair certifies impossibility. Otherwise choosing an arbitrary unassigned pair, including an early singleton, and visiting every permissible value partitions all valid completions. Induction on unassigned pairs proves exhaustiveness and disjointness. Cycle insertion uses the same sound checks. Claimed runs have no time or node cap. For the accepted scopes the counters and 32-bit shifts cannot overflow.

## Independent computational checks

The auditor independently authored `the original checker`, `the original checker`, and `the original checker`; the raw enumerator uses adjacency matrices and direct per-color BFS, not either candidate closure routine.

- Exhaustive enumeration of all 46,879 labeled, oriented, three-colored tournaments of orders 1 through 4: zero target counterexamples. The rainbow-free counts by order are 1, 6, 204, and 37,152.
- Literal enumeration of all 1,892,511 fixed-cycle completions over orders 3, 4, and 5. Every orientation/color assignment is examined without partial-state pruning. Each completion is tested under all four combinations of the two constraints, both before and after restricting cycle words to literal full-group orbit minima.
- All 24 resulting nonzero/zero count scopes agree with the candidate search. In particular, at n=5 the raw counts are 1,889,568 with neither condition, 743,718 with only cyclic-rainbow exclusion, 53,190 with only predecessor nonreachability, and zero with both. Canonical-word counts in those four scopes are 69,984; 30,214; 1,773; and zero. These satisfiable controls prevent an always-zero enumerator from passing.
- A deterministic independent BFS harness checks 746,070 proposed insertions across 9,600 partial-state trials, orders 3 through 8, both candidate engines, and all four constraint combinations. It checks all reachability bits after each accepted insertion, including diagonal cycles, and checks that rejected insertions leave the state unchanged. There are 581,193 accepted and 164,877 rejected proposals.
- Literal color-permutation/rotation minimization checks all 29,511 raw words of lengths 3 through 9 against the candidate canonical predicate. Orbit counts are 3, 6, 9, 26, 53, 146, and 369. This length-9 word check is not an unrestricted n=9 tournament search.
- Seventy-eight transformed hostile fixtures check rotation/global-color invariance. Explicit fixtures distinguish transitive rainbow triples from cyclic ones, monochromatic multistep paths from single edges, and outgoing sources from incoming sinks. A rainbow cycle feeding a fourth sink has no outgoing universal source, while its complete arc reversal has source 3.
- The auditor independently ran the full candidate replay: both closure engines agree on all exact claimed counts through n=8 and periodic lengths 3, 6, 9. The general n=8 run has 146 canonical words, 14,944,184 DFS states, 5,728,965 dead states, and zero completions.

The independently authored raw tournament enumeration is exhaustive through n=4; the independently authored raw fixed-cycle enumeration is exhaustive through n=5. The higher-order result is supported by inspected completeness proofs, full replay of the two candidate closure engines, independent partial-state BFS tests, symmetry enumeration, and hostile mutation controls. This report does not claim a wholly independent unrestricted n=8 brute-force enumerator or a proof-assistant certificate.

## Hostile gates and optimization behavior

All final independent audits pass under normal Python, `-O`, and `-OO`; their substantive results agree after removing the optimization indicator. Every guard uses explicit exceptions, not removable assertions. In every mode, the following six mutated candidate programs are detected:

1. checking the successor instead of predecessor;
2. corrupting the cyclic-triangle distinct-color predicate;
3. omitting the incremental closure update;
4. omitting the new edge's target from descendants;
5. dropping the sixth chord branch;
6. suppressing every third color in canonical word generation.

Four corrupted result controls are rejected: lost satisfying leaves, wrong rainbow semantics, reversed predecessor direction, and a nonzero candidate falsely presented as exclusion. The candidate's additional eight result mutations and eight invalid CLI scopes passed during the independently run full replay. The six pin-integrity mutations passed under normal, `-O`, and `-OO` verification. The author additionally supplied full normal/`-O`/`-OO` replay receipts, all PASS with empty diagnostics; the auditor's independent full replay is the separately recorded normal run.

## Reproduction and final boundaries

Run the original normal-mode audit/replay operation, the original optimized-mode audit/replay operation, and the original optimized-mode audit/replay operation using the original audit environment. The script pins the final candidate manifest itself, recompiles programs into temporary directories, reruns the independent checks and mutations, and rechecks candidate bytes afterward. Run the candidate's `the original checker` to reproduce every claimed higher-order finite search. the original externally pinned audit integrity and hostile-control check verifies the final acceptance packet and its recorded scopes; it is an integrity/receipt check, not a fresh search replay.

No remote repository, queue, or publication state was changed by this audit. The accepted conclusion remains bounded and computer-assisted. The all-size conjecture is unresolved by this work.
