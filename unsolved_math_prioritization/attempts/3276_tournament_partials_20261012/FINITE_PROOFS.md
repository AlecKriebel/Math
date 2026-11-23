Editorial note: The complete authored text is preserved below. Only references to undistributed operational artifacts, their identities, locations and replay directions have been replaced with descriptive prose. Mathematical arguments, evidence counts, corrections and limitations are retained. This prose edition identifies its distributed files and public scholarly sources. Historical conditions in the source record are distinguished from current dependency status in ACCEPTANCE_AND_DEPENDENCIES.md.

# Mathematical reduction and exact-search completeness

## 1. Convention and the credited reduction

Write `x ~> y` when some directed monochromatic path leads from x to y, with its color allowed to depend on y. For distinct x,y a direct arc x->y is already such a path. A cyclic rainbow triangle consists of x->y->z->x in three pairwise distinct colors. A transitive rainbow triple is not forbidden.

Assume a counterexample exists at some order at most N, and take an induced-subtournament-minimal counterexample D. Any smaller induced subtournament has no cyclic rainbow triangle, since D has none. For distinct vertices x,y, define an auxiliary digraph A on V(D) by y->x exactly when x does not monochromatically reach y in D. No self-pair is included in A. Each such edge is an actual edge of D: the opposite edge would itself give reachability. Thus A has neither loops nor opposite pairs. Every vertex x has an incoming A-edge because x is not a monochromatic universal source.

Following incoming edges in a finite digraph supplies a directed cycle C in A, of length at least three. In D[V(C)], each vertex still fails to reach its predecessor on C: removing vertices cannot create a directed path. Hence that induced subtournament has neither a cyclic rainbow triangle nor a monochromatic universal source. Minimality forces C to span D.

If x fails to reach a vertex y other than its predecessor, then y->x is an A-edge. The successor cannot be such y because x directly beats its successor. The path from x to y along C followed by y->x is therefore a shorter directed A-cycle. Its induced subtournament is again a counterexample, a contradiction. Thus each vertex fails to reach exactly its predecessor, and the obstruction cycle is uniquely determined by that predecessor relation up to rotation.

This is the Shen lemma credited and reproved by Georgakopoulos–Sprüssel, Lemma 2.1. We do not claim it as new. For this search only the necessary weaker statement is used: a minimal counterexample can be labeled 0,...,n-1 so that i->i+1 modulo n is an arc and i cannot monochromatically reach i-1 in any color. Reachability of all nonpredecessors is not a constraint in the code.

Orders 1 and 2 have an actual outgoing source, independently of colors. Therefore if all searched obstruction-cycle completions vanish at n=3,...,8, there can be no counterexample of order at most 8.

## 2. Why the symmetry quotient loses no candidate

Fix the labels along the obstruction cycle. Each of its n directed arcs receives one of the three named colors; this gives a word w of length n. The remaining unordered pairs, n(n-1)/2-n of them, are chords. Every chord has exactly six choices: two orientations and three colors.

Permuting the three colors globally does not change directed paths being monochromatic or triangles being rainbow. Rotating all vertex labels along the directed cycle also preserves both constraints and predecessor identities. These two group actions preserve existence of a completion. No reflection, arc reversal, source/sink interchange, or independent per-edge color permutation is used.

For any word, relabel its first encountered color 0, its next previously unseen color 1, and its third previously unseen color 2. This first-occurrence normalization is the lexicographically smallest image under global color permutation: at the first occurrence of each as-yet unnamed color, the smallest unused label is necessary for lexicographic minimality. It also works for words using fewer than three colors.

The generator lists each normalized word once by starting with 0 and allowing the next symbol to be at most one larger than the largest previously used symbol, never larger than 2. For each such word it rejects the word if any cyclic rotation, after first-occurrence normalization, is lexicographically smaller. Every orbit has a minimum and that minimum is generated. A lexicographic minimum is a unique literal word, even when several group elements fix it. Thus exactly one word per rotation/color-permutation orbit remains.

At each retained word every chord's full six-element domain is searched; there is no additional symmetry quotient for chords and no division of raw tournament counts by an orbit size. The independent Python checker explicitly constructs all 3^n words through n=9 and all 6n group images per word, and verifies the literal orbit minima against normalization. A separate no-symmetry cycle search enumerates all 3^n raw cycle-color words for n=3,4,5,6 and again returns no completion.

For the three-periodic subcase the fixed word i modulo 3 represents any repeated cycle of three pairwise distinct colors under a global permutation and a starting-point choice. Its cyclic consistency requires n divisible by 3. Only n=3,6,9 are searched. This excludes that pattern below 12, not arbitrary patterns at order 9 or the periodic pattern at unsearched lengths.

## 3. Safe partial-state pruning

A partial state assigns zero or one oriented colored arc to each unordered pair. Once a cyclic rainbow triangle appears, adding remaining arcs cannot remove it. Likewise, once a monochromatic path from i to its predecessor appears, adding remaining arcs cannot remove it. Both violations therefore justify rejecting any partial state.

When adding u->v in color c, every newly created triangle must use this edge and has form u->v->w->u. The triangle predicate tests all w and rejects exactly if the two existing arcs have different colors from one another and from c. It does not test transitive rainbow triples.

For the incremental closure method, let R be the old directed reachability relation in color c, with positive-length paths. Let A be u together with all vertices that reach u under R, and B be v together with all vertices reached from v under R. The new closure is exactly R union (A times B). Every new path uses the new arc; a simple path needs it at most once, so its initial part lies in A and final part in B. Conversely, concatenating an old path to u, the new edge, and an old path from v produces a walk, from which a path can be extracted for distinct endpoints. The same formula correctly captures positive-length cycles on the diagonal. Therefore the update rejects exactly when a newly created pair (i,i-1) occurs. Previous colors' closures are unchanged.

The second method does not use this incremental formula. It rebuilds the affected-color adjacency relation from the matrix plus the proposed arc and runs Warshall's recurrence, then checks every predecessor pair. Both methods retain exact old closures for unaffected colors. Their complete claimed-scope searches have identical state/dead-state counts, not merely identical zero answers.

The initial state has no edges and no positive-length paths. Its cycle edges are inserted by the same checked operation. A rejected cycle word already violates a necessary property without needing any chord, so it has no valid completion.

## 4. DFS exhaustiveness

For a surviving partial state, the algorithm examines currently unassigned chord pairs, testing all six possible values with the checked addition operation. If any tested pair has an empty domain, no completion is possible. Otherwise it selects a pair with the smallest tested domain; encountering a singleton may end the selection scan early. Either choice is legitimate because it selects an actual unassigned pair and never removes a feasible value.

It branches over every value retained for that pair and recurses with one fewer unassigned chord. A valid completion extends exactly the branch corresponding to its value on that selected pair. Induction on the number of unassigned chords shows that every valid completion is visited. Different branches assign different values to that pair, so their completion sets are disjoint. At zero remaining chords the completed tournament is counted without applying any unproved additional condition.

The number of pairs and color words is finite; no runtime or node cap is imposed in the claimed runs. All runs terminate normally. State counters use unsigned 64-bit integers; recorded maximum counts are under 15 million and cannot overflow. Vertex sets use 32-bit bitmasks and the CLI enforces 3<=n<=15, so all shifts are in range. The finite exclusion does not rely on numerical tolerances.

## 5. What the output proves, and what it does not

Zero completions for every canonical cycle word at each n=3,...,8 excludes even the larger class specified in Section 1. The minimal-counterexample reduction then implies the original assertion for every nonempty tournament with at most eight vertices. Zero completions at the three-periodic word of length 9 adds only a restricted order-9 conclusion. These are computer-assisted finite conclusions conditional on correct implementation/replay; the supplied controls and independent closure implementation support auditing but are not formal certificates in a proof assistant.

There is no induction step covering larger n, no verified counterexample, and no proof that three colors alternate impossibly at all lengths. Consequently the unrestricted target remains unresolved by this packet.
