Editorial note: This preserves the complete authored text, with only operational artifact references, undistributed identities and byte counts, locations, and executable command descriptions edited for this prose edition. Mathematical proofs, full audit findings, counts, and limitations remain complete. The final structural theorem is independent of a finite computer bound. Earlier through-nine and through-ten results retain their historical scope in unchanged companion editions. Historical candidate conditions are reconciled in ACCEPTANCE_AND_DEPENDENCIES.md. Executable programs and raw enumeration outputs are not distributed.

# Exact full-orbit computation for twisted rotational symmetry

12 October 2026 UTC. Row 1754 / problem 3276 / OPG-1808. Fifth and final substantive pass, coordinated with the separate structural lane. This is one computational lane of that pass, not an additional pass.

## Target and strict limits

The target asks whether every nonempty finite tournament with at most three arc colors has either a directed cyclic rainbow triangle or an outgoing universal monochromatic source. A source reaches each other vertex by a directed monochromatic path; its color may depend on the destination. Transitive rainbow triples are allowed. Incoming sinks do not meet the stated conclusion.

This packet is an exact search of a much smaller **whole-tournament symmetry class**. It does not search arbitrary tournaments of its displayed orders, and it does not search arbitrary tournaments with a three-periodic Hamilton-cycle word. It establishes no new general tournament bound. The previously accepted general bound remains ten. The unrestricted conjecture, arbitrary periodic length twelve and arbitrary all-size three-periodic cycles remain unresolved by this computation. No novelty, current-literature-status, proof-assistant, or formal unsatisfiability-certificate claim is made.

The completed search scopes have a fixed actual arc 0 to 1 of color 0; all rotations act on the entire tournament while cyclically permuting all three colors. They forbid cyclic rainbow triangles and every monochromatic path from a vertex to its cyclic predecessor. We do not impose reachability to the other vertices, interval conditions, incidence requirements, colored primeness, or minimality. The searched class is therefore a relaxation of the fully color-permuting-transitive induced-minimal-counterexample class. Excluding this relaxation at a specified order excludes that minimal class at that order. It does not exclude every symmetric tournament, and it gives no conclusion about a minimal induced subtournament that has lost the symmetry of a larger tournament.

## 1. Source premise and reduction to the stated class

The credited external source is Agelos Georgakopoulos and Philipp Sprüssel, *On 3-coloured tournaments*, arXiv:0904.1967v2, https://arxiv.org/pdf/0904.1967v2 . Lemma 2.1, which credits Shen, says an induced-minimal counterexample to the general Conjecture 1.2 has a unique distinguished directed Hamilton cycle such that each vertex reaches every other vertex except its predecessor. Uniqueness concerns the cycle with that reachability property, not all Hamilton cycles. The statement and surrounding general-minimal-counterexample hypotheses were re-read from the recovered text and freshly extracted PDF pages. The source bytes and public URLs are recorded without redistributing the source.

For completeness, the symmetry reduction used by the previous accepted structural packet is short. A direction-preserving automorphism applying one global permutation of the used colors preserves monochromatic reachability. It therefore commutes with the unique failed-predecessor permutation. The centralizer of a full cycle consists of its rotations: the image of one vertex determines all the other images. A transitive subgroup of these rotations is the full rotation group. Thus the single-step shift belongs to the group.

No direction-preserving automorphism of a tournament can be a nonidentity involution: a swapped pair would have its arc reversed. An even-order rotation has an involutive power, so the order n of the distinguished cycle is odd. The induced color permutation of the single-step shift has order dividing n and acts on at most three used colors. It is the identity or a three-cycle. The identity would make the distinguished cycle monochromatic, yielding a path from every vertex to its predecessor, which is forbidden. Thus all three colors occur and the color permutation is a three-cycle. Relabel the vertices along the distinguished cycle and name its successive colors 0,1,2. The shift then sends i to i+1 and color c to c+1, and the actual arc 0 to 1 has color 0. In particular 3 divides n.

The earlier accepted additional argument gives 9 dividing n: write n=3m and inspect the orbit of the order-three rotation by m. It is an actual cyclic triangle. If 3 does not divide m, its three arc colors are cyclically permuted and distinct. When 9 divides n this triangle is monochromatic, so that argument stops. The finite controls at orders 3,15,21 intentionally test the immediately obstructed orders as well as the residual orders 9,27,45,81. Nothing in our finite implementation assumes a further divisibility property.

This reduction is used only for the conditional minimal-counterexample implication. The exact enumeration below independently establishes its literal stated matrix class, without importing the separate fifth-pass all-order structural theorem.

## 2. Bijective arc-orbit encoding

Fix odd n divisible by three, and let h=(n-1)/2. Vertices are the residues modulo n, and colors are residues modulo three. A complete state is a vector q=(q_1,...,q_h) with each q_d in {0,1,2,3,4,5}.

For each d and each vertex x, put y=x+d modulo n. If q_d<3, put the actual arc x to y in color x+q_d modulo three. If q_d>=3, put the actual arc y to x in color x+(q_d-3) modulo three. There is no reverse arc and no loop. Color is determined from the orbit base x, even in the negative orientation; substituting the tail y in that case would be a different, incorrect encoding.

### Proposition 1. The encoding is a bijection

These vectors are in bijection with all colored tournaments on the fixed labeled vertex set for which the single-step vertex shift preserves orientation and increases each arc color by one modulo three.

**Proof.** Every unordered pair has a unique representation {x,x+d} with 1<=d<=h. Given the pair {u,v}, exactly one of the two nonzero opposite differences lies in that interval. Uniqueness also follows directly: if two representations have the same orientation around the pair, their base vertices and differences agree; if they exchange endpoints, their differences are d and n-d, which cannot both be at most h. Thus every pair receives one actual arc. Shifting x by one preserves the chosen orientation and increases its color by one. At the wraparound x=n-1 to x=0, color consistency holds because 3 divides n.

Conversely, for a tournament with the stipulated shift, inspect the actual arc between 0 and d, for each 1<=d<=h. Its orientation and color determine exactly one q_d. Repeated shifts determine every arc in that orbit by the displayed formula. The unique pair representation covers all arcs, so this reconstruction gives the original tournament and determines q uniquely. QED.

A partial vector permits q_d=-1. That value removes all n arcs of that distance orbit; it is never an actual color. The same proof shows the remaining partial graph is invariant under the twisted shift. It has neither a reverse pair nor a loop. Assigning a variable adds a whole actual orbit. No virtual reachability relation is ever inserted as an arc.

Fixing q_1=0 means that all actual cycle arcs i to i+1 have colors i modulo three. This fixing is justified for the distinguished-cycle labeling from Section 1. We do **not** divide raw counts by six or claim that an arbitrary predecessor-constrained model can be normalized to this fixing by reflection. The independent raw and fixed counts differ in ways that would detect that unjustified normalization.

## 3. Sound tests on partial states

### Lemma 1. Triangles anchored at zero suffice

A partial encoded graph has a cyclic rainbow triangle if and only if one such triangle contains vertex zero.

**Proof.** The reverse direction is immediate. Given any cyclic rainbow triangle, rotate one of its vertices to zero. Whole-orbit symmetry preserves all its actual directed arcs and applies one common permutation to their colors, so the translated triangle is still cyclic and rainbow. QED.

The candidate checks every ordered pair v,w other than zero for actual arcs 0 to v, v to w and w to 0, and then checks that their three colors are distinct. Allowing both orders of v,w covers both directed orientations. The independent oracle instead inspects every unordered triple and both cyclic orders, without using the anchoring lemma. It does not reject a transitive rainbow triple.

### Lemma 2. Predecessor paths from zero suffice

A partial encoded graph has a monochromatic path from some vertex i to i-1 modulo n if and only if it has one from zero to n-1.

**Proof.** Translate the first path by -i. The translated arcs are actual arcs, preserve direction, and all have their old common color decreased by i modulo three. Their endpoints become zero and n-1. The converse takes i=0. QED.

For each of the three colors the candidate does a breadth-first graph search starting at zero and rejects if n-1 is discovered. These are distinct endpoints, so the path has positive length. Marking the start reached is only the ordinary search convention; it cannot create a spurious predecessor path. A monochromatic walk with repeated vertices can be shortened to a path by deleting closed segments. The independent oracle uses reflexive Boolean Warshall closure separately in each color and checks every vertex against its own predecessor. It never mixes colors along one path.

### Lemma 3. Both tests preserve every valid completion

Adding actual arcs cannot destroy an existing cyclic rainbow triangle or an existing monochromatic path. Therefore rejection by either test proves that no extension of that partial state can satisfy both prohibitions. The same argument proves soundness when either test is deliberately disabled to obtain a relaxed positive-control scope.

No incidence assumptions, interval constraints, source-transfer assumption, hidden minimality test, virtual arc, orientation quotient, or unproved color-class relation is used for pruning.

## 4. Exact recursive enumeration

The search first validates its initial partial state, including the fully specified initial state at n=3 with q_1=0. Failing to test that initial state would falsely count the rainbow three-cycle; an explicit source mutation tests this gate.

At each recursive node, the search tests all six values of every unassigned orbit variable against the two partial-state predicates. The retained values form a necessary domain. An empty domain rejects the node. Otherwise it selects a variable of minimum domain size, breaking ties by increasing distance, and recurses on every retained value. The assigned variable is restored after those branches. Rejected proposals do not leave their tested value assigned.

### Theorem 1. Completeness of the finite orbit search

For its fixed order, initial assignments, and enabled predicates, the algorithm counts exactly all satisfying complete orbit vectors.

**Proof.** Any satisfying complete vector extending a reached node assigns a value to each unassigned variable that passes the tests, by Lemma 3. It therefore cannot be lost to an empty domain, and its value is included in the selected variable's branch domain. Inductively a branch reaches it. At every recursive step the number of unassigned variables decreases by one, so the recursion terminates. A complete state is reached through only the unique sequence of its selected values, so it is counted once. Its initial or final value assignment has already passed the enabled tests. Thus every counted vector satisfies them and every satisfying vector is counted exactly once. QED.

The minimum-domain heuristic affects runtime only. It is not an additional mathematical exclusion. The implementation bounds supported n to odd multiples of three between 3 and 99, validates flag and state values, and raises an explicit exception instead of silently overflowing any candidate counter. Those input bounds are implementation limits, not completed enumeration claims at every supported order.

## 5. Completed finite scopes

With q_1=0 and both prohibitions enabled, the candidate completes orders 3,9,15,21,27,45,81, with zero complete vectors at each. Its exact deterministic node counts are respectively 0,5,1,1,11,19,33. At n=3 the initial rainbow triangle is rejected before entering DFS, which explains the zero node count. The independent implementation separately completes orders 15,21,27,45 using its own pair-based matrix encoder, all-triples triangle inspection, all-vertices Warshall predicate, and DFS. It independently obtains zero. Orders 3 and9 also have a stronger independent literal check: all 6^h complete raw vectors, with no partial pruning.

For n=3 the raw complete counts under neither condition, triangle-only, predecessor-only, and both are 6,0,3,0. With q_1=0 they are 1,0,1,0. For n=9 the raw counts are 1296,432,54,0; with q_1=0 they are 216,72,18,0. These counts are exact for the displayed labeled rotational models, not isomorphism counts and not counts of all labeled tournaments of those orders.

Thus the completed finite computations exclude fully color-permuting-transitive induced-minimal counterexamples at those listed orders. The residual first order from the previous pass, 27, is included, with 11 candidate DFS nodes and 589 partial-state tests. The computation alone is not an all-order exclusion. The separate structural lane may prove a stronger statement, but its proof is not an assumption here.

## 6. Positive and hostile controls

Across n=3 and9 the independent harness enumerates 1302 full vectors. For each, it erases every subset of distance orbits, compares the separately constructed matrices, checks the whole twisted action, and compares all four enabled/disabled predicate combinations. This gives 82992 partial-rule comparisons. Whenever the full vector satisfies a selected combination, every erased-orbit partial graph must survive; there are 28530 such positive preservation checks. Repeated partial graphs arising from different full models are intentionally counted as separate model-preservation cases, not advertised as distinct partial graphs. The harness performs 22050 complete-or-partial action checks. The independent literal complete counts are compared against both candidate DFS modes and the independently implemented DFS.

The 432 rainbow-free raw order-nine models all have every vertex as an outgoing universal monochromatic source, checked by the independent closure oracle. The explicit order-nine vector (0,2,2,2) is rainbow-free, has all nine sources, and has no spanning strongly connected monochromatic color. It guards against claiming that the entire twisted-symmetric class is empty or borrowing the stronger conclusion for color-preserving transitivity. The explicit vector (0,1,0,0) has no monochromatic predecessor path and no universal source, but has 18 cyclic rainbow triangles. It guards against an always-zero predecessor-only computation or dropping the rainbow hypothesis. Their complete matrices and computed properties are in EXAMPLES.md and are freshly verified in Python. The rainbow three-cycle is retained as a boundary fixture.

Nine hostile source mutations are compiled and run through the independent harness. They disable either prohibition; test the successor instead of the predecessor; allow color changes along a path; omit rotated copies; use the negative arc's tail instead of the orbit base to assign color; skip initial-state rejection; test a transitive triple instead of a cyclic one; or omit the final distance orbit. Every mutation must terminate with the explicit rejection exit code and a concrete mismatch reason. Compilation errors, timeouts, missing output, and incidental crashes do not count as detection. Fourteen malformed CLI cases and twelve malformed internal inputs are also explicitly rejected.

Normal Python, -O and -OO runs repeat the fresh compilation and all substantive checks. Their results must agree after removing only the Python optimization flag. C++ uses -O2 in each mode. Python optimization does not remove any assertion gate because validations use explicit exceptions rather than assert statements.

## 7. Evidentiary and reconstruction boundary

A pinned manifest records the exact full authored proof, implementation, independent harness, verification scripts, fixtures, and execution results. The externally stored archive contains every packet byte, not a hash-only record; actual extraction into a fresh directory is verified against the same external pin. Mutations run only on temporary copies. No prior packet or primary-source file is changed. Exact original-input identities remain preserved in the original undistributed provenance record; SOURCE_CREDIT.md provides the permitted public scholarly source credit.

The integrity and rollback checks show that the inspected bytes can be recovered. They are not substitutes for the mathematical proof or fresh execution. No external repository or queue write was performed. No copied source text, PDF, dataset contents, or private coordination material is included in this packet.
