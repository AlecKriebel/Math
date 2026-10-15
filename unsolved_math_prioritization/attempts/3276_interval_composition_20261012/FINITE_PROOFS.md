Editorial note: The complete authored text follows. Only references to undistributed operational artifacts, identities, byte counts, locations and replay commands are replaced by descriptive prose. Mathematical arguments, full audit findings, evidence counts and limits are retained. The original structural bound-eight application is historical and remains unchanged; the new bound-nine consequence is a separate deduction in BOUND_NINE_DEDUCTION.md. Historical candidate-review conditions are reconciled in ACCEPTANCE_AND_DEPENDENCIES.md.

# Proper-interval propagation and the bounded tournament search

Row 1754 / problem 3276. Third substantive pass, 12 October 2026 UTC.

## Target, dependencies, and scope

A nonempty finite tournament has its arcs colored from a set of at most three colors. The target is either a **directed cyclic** triangle with three different colors, or a vertex that reaches every other vertex by a directed monochromatic path. The color may depend on the destination. Transitive rainbow triples are allowed. Reachability is outgoing.

The all-order target is not resolved here. The new search is over necessary conditions for an induced-minimal counterexample, not over all colored tournaments or even all predecessor-obstructed completions. Its finite conclusion requires the reduction and propagation proof below, plus the actual complete bounded runs.

The source is Georgakopoulos and Sprüssel, *On 3-coloured tournaments*, arXiv:0904.1967v2 (17 April 2009), https://arxiv.org/pdf/0904.1967v2. Lemma 2.1 credits Shen for the obstruction-cycle reduction. Lemma 2.5 supplies the proper-interval domination property, whose short proof is reconstructed here. No priority or novelty claim is made. The source's later PDF title-page date is not its arXiv version date. The source text and PDF are not copied into this packet.

## 1. Minimal counterexamples have a spanning obstruction cycle

Suppose the target fails at some order at most N, and choose an induced-minimal counterexample D. For distinct vertices x,y, put an auxiliary arc y to x precisely when x cannot reach y monochromatically in D. Each auxiliary arc is an actual tournament arc: the opposite arc would itself be a monochromatic path. The auxiliary graph has no loops or opposite pairs. Every vertex has positive auxiliary indegree, because no vertex of D reaches all the others.

Following incoming auxiliary arcs produces a directed auxiliary cycle C of length at least three. Every vertex of D[V(C)] still fails to reach its predecessor on C. Removing vertices cannot create a path, and cannot create a cyclic rainbow triangle. Thus this subtournament is itself a counterexample, and minimality forces C to span D.

An additional auxiliary arc y to x with y different from x's predecessor closes the forward segment xCy into a shorter auxiliary cycle, except that y cannot be x's successor because that successor is directly reachable from x. The shorter cycle would induce a smaller counterexample, impossible. Therefore each vertex fails to reach exactly its predecessor. Label the vertices cyclically by Z/nZ, with actual arcs i to i+1 and the forbidden reachabilities i to i-1.

Orders 1 and 2 have a direct outgoing source. It is consequently enough to exclude all possible reduced minimal counterexamples at each order 3 through the claimed bound.

## 2. Proper-interval domination

For distinct x,y with y not the predecessor of x, let I=xCy be the forward cyclic interval including both endpoints. Its size lies between 2 and n-1, so D[I] is a proper induced subtournament. It is cyclic-rainbow-free, and by minimality has a vertex that reaches every vertex of I monochromatically within D[I]. Every vertex z of I other than x has its predecessor z-1 in I and cannot reach that predecessor even in D. It cannot be the universal source in D[I]. The source must therefore be x. In particular, x reaches y in some color within D[I]. This is the source's Lemma 2.5.

Only endpoint assertions are required in the code: every proper forward interval has a monochromatic path from its first to its last vertex. Taking shorter endpoint intervals also gives domination of every vertex from the first. No color of an arbitrary global path is presumed to remain available inside I.

## 3. Sound propagated information

A state contains a partial assignment A of actual tournament arcs and, for each color c, a transitively closed relation R_c. The invariant is:

For every minimal-counterexample completion D extending the current branch and all previous deductions, every pair (u,v) in R_c is realized by a c-colored directed walk in D. For distinct endpoints this gives a path; diagonal pairs record positive-length cycles.

Initially the relations are empty. Assigned actual arcs are inserted into them. A virtual assertion u reaches v in color c represents a path, **not** an actual arc. In particular it is never used as a tournament edge in a rainbow-triangle test or as an edge in an interval possibility graph.

### Closure and forbidden predecessor test

To adjoin a required c-reachability u to v, take the current ancestors of u together with u itself, and the current descendants of v together with v itself. Add their Cartesian product to R_c. This gives exactly the transitive closure after adjoining one relation edge. Equivalently, append that edge to the old closed relation and recompute Warshall closure. These are the two implemented engines.

If a new relation contains i to i-1 for any i, the assertion is impossible in a minimal counterexample. Otherwise the updated relation remains sound whenever the assertion was sound. Positive-length diagonal cycles are retained; no reflexive diagonal is added merely by convention.

To test an actual arc u to v in color c, additionally reject any cyclic rainbow triangle u to v to w to u using the two already assigned arcs. Rejected tests leave the state unchanged. This predicate does not reject transitive rainbow triples.

### Actual chord domains

For each unassigned unordered pair, test all six oriented-color values against the assigned arcs and the mandatory reach relations. The surviving values form its domain. Every genuine minimal-counterexample completion's value survives, because its actual arc cannot contradict a true required path or introduce a forbidden triangle. An empty domain rejects the state. A singleton domain forces its actual arc, after which all domains are rebuilt.

For each color c form a directed **possibility graph** P_c from already assigned actual c-arcs and every oriented c-arc surviving in every unassigned pair's domain. A pair may contribute both orientations or multiple colors. This is deliberately an overapproximation: paths in P_c may use mutually incompatible choices. Such false possibilities weaken pruning and cannot remove a genuine completion.

### Interval color filtering and singleton forcing

For each proper interval I=xCy and color c, retain c only if both conditions hold:

1. P_c restricted to I contains a path from x to y.
2. Adjoining the virtual c-reachability x to y to R_c does not produce any predecessor reachability.

If D is a compatible minimal counterexample, Section 2 gives an actual interval-local path of some color c. Each arc of that path belongs to the corresponding actual domain or is already assigned, so condition 1 holds. Its reachability is true in D, as are all current mandatory relations, so condition 2 also holds. Hence every compatible minimal counterexample supplies at least one retained color.

It is sound to reject an interval with no retained colors. With exactly one retained color c, every compatible minimal counterexample has that interval-local c-path; the global assertion x reaches y in color c can therefore be adjoined and transitively closed. This is a genuine deduction rather than a guessed color choice. With multiple retained colors, no one color is asserted.

The implementation builds P once per pass. Additional virtual deductions during that pass can make some old domains stale. This is harmless: the stale P is a **larger** possibility graph than a recomputation would produce. It can only retain extra colors. All domains are rebuilt after a pass that adds a new virtual relation. No virtual reachability is inserted directly into P; its witness may leave the interval.

### Termination and all-order preservation theorem

Each successful singleton chord step assigns an unassigned pair. Each successful virtual step strictly enlarges some R_c; transitive closure may add further pairs. There are finitely many pairs and at most 3n^2 relation entries. Every other pass terminates or rejects. Therefore propagation terminates.

By induction on each domain deletion, forced actual arc, and forced virtual assertion, every compatible induced-minimal counterexample survives unless the state has no such completion. This preservation theorem holds at every finite order and is independent of the bounded tests. It does not claim that every state surviving propagation has any completion.

## 4. Exact bounded DFS and symmetries

For a fixed cycle word, all cycle arcs are inserted using the checked actual-arc operation. Every non-cycle pair initially has six possible values. At each DFS node, apply the sound propagation above. If unassigned pairs remain, select one having the smallest surviving domain and branch over **every** surviving value. The domains used for branching are from the final stable pass. By induction, any reduced minimal counterexample extends one of the children. Children choose different values for the same pair, so their completion sets are disjoint. If all pairs are assigned, the state is counted after checking the interval requirements. No node or time cap is used by the search executable.

For the default general scope, generate all first-occurrence normalized color words: start with color 0, and let each next color be at most one greater than the maximum previously used, capped at 2. This gives one representative for each global color-renaming orbit. Keep a word only if no cyclic rotation, after normalization, is lexicographically smaller. This gives precisely one representative in every rotation/global-color orbit, including one- and two-color words. Both transformations preserve directed cycles, proper intervals, predecessor identities and path colors. No reflection or arbitrary vertex permutation is used. The independent oracle uses literal permutations and rotations, rather than this normalization routine.

The periodic option searches only the one word 012012... and is accepted only at lengths divisible by three. An explicit word option searches only that supplied word. Neither restricted mode is interpreted as general-order coverage. Unreduced control scopes enumerate all 3^n literal cycle words.

Unsigned counters throw before overflow. Bit sets are 32-bit and the command-line order gate is 3 through 15. The recorded complete searches use orders at most 9 and have fewer than 600,000 DFS states. Larger orders are supported as inputs but are not claimed to have been searched or excluded.

## 5. Finite conclusion and its limits

If complete general searches give zero at every order 3 through 9, the minimal-counterexample reduction implies the target for every nonempty tournament of order at most 9. Order 9 is general only because every canonical cycle word is searched, with all surviving six-valued chord branches and sound minimality deductions. It is not inferred from the periodic word or from mere cycle-word acceptance.

This is a computer-assisted finite conclusion relying on the inspected source and replay. It is not a proof-assistant theorem, SAT/DRAT certificate, or all-order resolution. Exhaustive independent raw fixed-cycle completion enumeration is only through order 5; larger-order confidence combines the completeness proof, both full closure-engine searches, independent partial-state and completion-preservation checks, and hostile mutations.
