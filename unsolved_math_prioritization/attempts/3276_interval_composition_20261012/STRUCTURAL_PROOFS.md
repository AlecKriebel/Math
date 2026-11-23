Editorial note: The complete authored text follows. Only references to undistributed operational artifacts, identities, byte counts, locations and replay commands are replaced by descriptive prose. Mathematical arguments, full audit findings, evidence counts and limits are retained. The original structural bound-eight application is historical and remains unchanged; the new bound-nine consequence is a separate deduction in BOUND_NINE_DEDUCTION.md. Historical candidate-review conditions are reconciled in ACCEPTANCE_AND_DEPENDENCIES.md.

# Row 1754 / problem 3276 / OPG-1808
## Interval-safe propagation and exact colored-module composition

Date: 12 October 2026 UTC.

## Status and exact target

The target concerns every **nonempty finite tournament** with arcs colored from a palette of at most three colors. It asks for either a **directed cyclic rainbow triangle**, or a vertex from which every other vertex is reachable by a monochromatic directed path. The path color may depend on the destination. A transitive rainbow triple does not satisfy the first alternative.

**The unrestricted target is not proved or disproved here.** This packet proves an all-order sound propagation rule, an exact composition theorem, and sufficient all-order subclasses that extend the earlier bounded-incidence-core criterion. It includes finite verification of its own algorithms and negative fixtures. It does not enumerate all tournament completions at any new order. Any separate finite-search result requires its own audit. There is no claim of novelty, priority, or certification of the entire primary source proof.

## 1. Credited starting point

The primary dependency is Agelos Georgakopoulos and Philipp Sprüssel, *On 3-coloured tournaments*, arXiv:0904.1967v2, 17 April 2009, https://arxiv.org/pdf/0904.1967v2. We read its full locally recovered text for this pass. Its Lemma 2.1 credits Shen Minggang for the following minimal-counterexample structure: an induced-minimal counterexample D has a distinguished directed Hamilton cycle C such that each vertex reaches every other vertex monochromatically except its predecessor on C. The distinguished obstruction cycle, rather than every Hamilton cycle, is unique up to rotation.

Lemma 2.5 states interval-local reachability: if y is not the predecessor of x, then x reaches y monochromatically inside the forward cyclic interval xCy. For distinct endpoints this interval has between two and n-1 vertices. Its short proof is useful: every vertex of the interval except x has its predecessor in the interval, so none of them can be a universal source there. Minimality supplies a universal source in the proper induced interval, and that source must be x. The color of an arbitrary global x-to-y path need not work inside the interval. A uniquely possible global color must work there.

The earlier accepted structural packet also uses the source's Proposition 2.4 and Theorem 3.1: every minimal counterexample has all three colors incident at every vertex and at least two colors in each direction. These are cited source dependencies, not newly certified proofs in this packet. They imply the incidence-core containment recalled in Section 5.

The source's Lemma 2.7 forces a forward two-step **actual chord** at a color switch and reverse reachability in the third color. The previously accepted closure generated only by cycle arcs and those reverse paths accepts every genuine three-color cyclic word, and even some words excluded by the stronger source Proposition 2.8. We do not repeat that closure as a proposed route to a complete proof. Source Problem 2.1, concerning strict three-color alternation on the obstruction cycle, is not settled here.

## 2. Safe interval propagation

This section gives a general finite constraint rule, then specializes it to a minimal counterexample. Let V be finite. For each unordered pair, retain a nonempty domain of possible orientation/color states. Each state specifies exactly one of the two directions and one of three colors. Fix:

- A set B of ordered pairs of distinct vertices that may not be connected by a monochromatic path of any color.
- Three relations R_c, containing the diagonal and closed under composition, known to be realizable as c-reachability in every completion still under consideration. Relations can contain actual arcs and previously sound path assertions.
- Mandatory path requirements (x,y,I), with x and y distinct members of I. Every completion under consideration must have an x-to-y monochromatic path lying entirely in I, in at least one color.

For each c, form the **possible actual-arc graph** P_c from all currently retained c-oriented states of all pair domains. A singleton domain supplies its actual arc. No virtual relation edge is inserted into P_c merely because it belongs to R_c.

For a requirement (x,y,I), retain color c only when both tests pass:

1. P_c[I] contains an x-to-y directed path.
2. Adding (x,y) to R_c and closing transitively produces no forbidden pair from B.

If no color remains, reject the partial state. If exactly one color remains, add the corresponding global reachability assertion to R_c and close transitively. With two or three colors, no single-color assertion follows from this rule.

Likewise remove an orientation/color state of a pair whenever adding its actual arc to R would force a forbidden pair. If a pair domain becomes empty, reject. If it becomes a singleton, adjoin the actual arc to R. Other independently sound local pruning, such as rejecting an actual cyclic rainbow triangle, may be interleaved.

### Theorem 1. Soundness and termination

These operations preserve every completion satisfying the initial domains, R, B, and mandatory requirements. Repeating them until no change terminates.

**Proof.** Fix such a completion T. Every actual c-arc of T remains in the possible graph if its state remains in its domain. Every R_c assertion represents a c-path in T; composition represents a c-walk, and deleting repeated-vertex segments gives a path between distinct endpoints. Thus adding a true actual arc or a true c-reachability assertion cannot produce a pair prohibited in T.

For any requirement, T supplies some monochromatic path in I. Its color passes the possible-graph test because every arc on that actual path is among the retained domain states. It also passes the closure test because the added reachability assertion is true in T. Therefore deleting all colors cannot occur while T remains possible; and if only one color survives, that color is forced in T. The same argument applies to deleting impossible actual-arc states and assigning a singleton domain. This proves the invariant inductively after every operation.

There are finitely many pair states to remove and finitely many color-reachability pairs to add. A changing iteration removes at least one state or adds at least one pair; no operation reverses a change. Hence the process terminates. A nonrejected fixed point is only a necessary relaxation, not a completion certificate. QED.

### Corollary 1. Minimal-counterexample specialization

Index an obstruction cycle by Z/nZ, n>=3. Set B={(x,x-1):x in V}. Require (x,y,xCy) for all distinct y other than x-1. Start with the cycle arcs and any separately proved reachability assertions, retaining all possible states of unknown chords. The rule retains every possible induced-minimal counterexample extending this data.

This is stronger information than the exhausted word-only closure: its possible-path test uses the actual chord domains inside each specified interval, and may force new path colors or reject a state when every interval path color fails. No claim that it always rejects is made.

### Why global relation edges cannot replace actual interval arcs

A known c-path from u to v may leave I even when u and v lie in I. Counting that virtual edge as an actual edge of P_c[I] would invent an interval witness. In the rule above, virtual edges participate in **global composition and forbidden-pair tests only**. Actual arc domains supply the interval possible-path graphs. The generic checker follows exactly this distinction.

The generic rule does not require rainbow-freeness. This permits nonvacuous soundness tests against known complete tournaments: choose only genuinely absent reachability pairs for B and only interval requirements with actual witnesses. Every such known model must survive. This is a test of the algorithm, not a search for counterexamples.

## 3. Exact composition through uniform colored modules

Let Q be a nonempty finite colored tournament on {1,...,k}. Replace each quotient vertex i by a nonempty finite colored tournament T_i. Between different factors, orient and color **every** arc according to its quotient arc: if i -> j has color c in Q, every vertex of T_i sends a c-arc to every vertex of T_j. Denote the resulting tournament by T=Q[T_1,...,T_k]. This is uniform colored substitution.

A partition satisfying this cross-block direction-and-color uniformity is a colored-module partition. Direction uniformity alone is insufficient. A proper nontrivial colored module M is a set with 1<|M|<|T| such that every vertex outside M has the same direction and color relationship with every member of M; it yields the partition consisting of M and outside singletons.

Write u R_c^H v for c-reachability in H, allowing the length-zero path when u=v. Let L_c(Q) consist of quotient vertices lying on a **positive-length** closed c-walk. In a finite digraph this is equivalent to lying on a directed c-cycle: use a shortest positive returning walk. It is not equivalent to the reflexive statement i R_c^Q i.

### Theorem 2. Exact reachability transfer

Let x belong to T_i and y belong to T_j.

1. If i!=j, then x R_c^T y if and only if i R_c^Q j.
2. If i=j and x!=y, then x R_c^T y if and only if either x R_c^{T_i} y or i belongs to L_c(Q).

**Proof.** A c-path in T projects to a sequence of quotient vertices. Suppress steps that remain inside a factor. Every remaining step is a c-arc of Q. For distinct endpoint factors this gives a c-walk from i to j, hence a c-path. If the path starts and ends in T_i and leaves T_i, its projection is a positive-length closed c-walk through i. If it never leaves, it is internal.

Conversely a quotient c-path between distinct factors lifts by choosing arbitrary vertices in its intermediate factors and retaining the prescribed endpoints. Uniform cross-block color and direction supply every required arc. A quotient c-cycle through i similarly lifts from any x in T_i, through its other distinct factors, back to any distinct y in T_i. An internal path already is a path in T. QED.

### Theorem 3. Exact universal-source formula

Let S(H) be the set of vertices reaching every other vertex monochromatically, with color allowed to depend on the target. The global sources lying in T_i are exactly:

- No vertices, if i is not in S(Q).
- All of T_i, if i is in S(Q) and lies in L_c(Q) for at least one c.
- Exactly S(T_i), if i is in S(Q) and lies in none of the L_c(Q).

**Proof.** By Theorem 2, reaching every outside factor is equivalent to i being a quotient source. If some monochromatic quotient return cycle passes through i, every vertex of T_i reaches all other vertices of T_i using that return route. With no such return cycle, global reachability between members of T_i is exactly internal reachability, color by color. QED.

This formula is exact for all colored tournaments; no absence of rainbow triangles, minimality, finite-search premise, or incidence condition is needed. With k=1 the quotient has no positive return cycle, and the formula correctly reduces to S(T)=S(T_1).

### Theorem 4. Exact cyclic-rainbow transfer

T has a directed cyclic rainbow triangle if and only if Q has one or some T_i has one.

**Proof.** A triangle inside one factor is unchanged. A triangle in three distinct factors has the same directions and colors as its quotient triangle, and any quotient triangle lifts. A triple in exactly two factors cannot be a directed cycle, because the outside vertex beats both vertices in the other factor or loses to both. QED.

## 4. Consequences for the target and minimal obstructions

### Corollary 2. Substitution closure

If Q and every T_i satisfy the target alternative, then their uniform colored substitution does too.

**Proof.** A cyclic rainbow triangle in any constituent lifts by Theorem 4. If none exists, Q and all factors have universal monochromatic sources. Choose a source i of Q and a source x of T_i. Theorem 3 makes x a source of the substitution. QED.

Requiring every factor to have an internal source is sufficient but not necessary for existence of a source in the expansion: the quotient-return-cycle clause can bypass even a factor with no internal source. This does not produce a rainbow-free counterexample to the original target; the explicit source-free factor used in testing is itself a cyclic rainbow triangle.

### Corollary 3. Colored-primeness of every minimal counterexample

Every induced-minimal counterexample to the target has no proper nontrivial colored module.

**Proof.** Suppose M is such a module in D. Contract M to one representative, giving quotient Q; Q is isomorphic to an induced subtournament obtained by keeping that representative and all outside vertices. Both Q and D[M] are nonempty proper induced subtournaments. They contain no cyclic rainbow triangle because D contains none, and minimality therefore supplies a universal source in each. All singleton factors trivially have sources. Corollary 2 gives a source in D, contradiction. QED.

This argument is independent of the Hamilton-cycle and incidence dependencies. It excludes uniform colored modules, not all ordinary tournament modules, and not arbitrary equal-size blocks. It gives an additional necessary composition restriction on a hypothetical minimal counterexample, without bounding the orders of colored-prime tournaments.

## 5. Recursive quotient-core sufficient classes

Recall the accepted incidence-deletion process. In a current induced tournament delete a vertex if it misses any of the three incident colors, or has fewer than two incoming colors, or fewer than two outgoing colors. Its terminal vertex set K(H) is independent of deletion order. The earlier accepted proof identifies it as the unique largest vertex set in which every vertex meets all three colors and at least two colors in each direction. The cited source incidence conditions ensure that every induced-minimal counterexample contained in H is contained in K(H).

Consequently, if the target is known at every nonempty order at most b, a nonempty cyclic-rainbow-free H with |K(H)|<=b has a universal monochromatic source. An empty K(H) needs no finite-search premise: any induced-minimal counterexample would have to be contained in the empty set.

A recursive colored-substitution certificate is a finite rooted tree. Its leaves are singleton tournaments. Every internal node carries a colored quotient with at least two vertices and has exactly one nonempty child for each quotient vertex. The node's tournament is the uniform colored substitution of its child tournaments into that quotient.

### Theorem 5. Recursive bounded quotient cores

Assume the target is known for every nonempty order at most b. If every internal quotient of such a certificate has no cyclic rainbow triangle and has incidence core of size at most b, its root tournament has a universal monochromatic source and no cyclic rainbow triangle.

**Proof.** The core criterion gives a source for each quotient. Leaves are singleton sources. Induct upward: every child tournament has a source and no cyclic rainbow triangle; Corollary 2 or Theorem 3 supplies a source for the parent, and Theorem 4 supplies rainbow-freeness. The tree is finite, so induction reaches the root. QED.

If every quotient core is empty, the result requires no computer-assisted finite bound. The b=8 specialization may use the separate independently accepted finite search through order eight. This packet does not audit or reproduce that finite search. A subsequently established b=9 or larger could be substituted only after its own verification; no such larger bound is claimed here.

The earlier whole-core criterion is a special case: represent any nonsingleton H by the one-level quotient H with singleton children. The recursive criterion also covers tournaments whose whole incidence core is arbitrarily large.

### Proposition 1. Unbounded strict separation from the whole-core bound

Let L_d, d>=1, be the depth-d uniform substitution tree whose quotient at level ell, counting the root as level zero, is a directed 3-cycle with all arcs in color ell modulo 3. Every leaf is a singleton. Then:

- |L_d|=3^d.
- L_d has no cyclic rainbow triangle.
- Every vertex of L_d is a universal monochromatic source.
- Every internal quotient has empty incidence core.
- For d>=3, K(L_d)=V(L_d).

**Proof.** The order follows by multiplication. All quotient triangles are monochromatic and leaves are singleton, so Theorem 4 proves rainbow-freeness by induction. Every vertex of the root quotient lies on a monochromatic directed cycle and is a quotient source. Theorem 3 therefore makes every vertex of the expansion a source, regardless of its internal factors. A monochromatic quotient has empty incidence core because each vertex misses two colors.

For any vertex x of L_d and each level ell<d, the sibling blocks at that level contain one nonempty incoming block and one nonempty outgoing block relative to x, both in color ell modulo 3. When d>=3 this gives all three colors in both directions at every vertex. Thus no vertex can be deleted even at the first core step, and the whole vertex set is the core. As 3^d is unbounded, no fixed whole-core bound covers this family, whereas the recursive empty-quotient-core criterion covers every member. QED.

This is a strict extension of that particular sufficient criterion, not a claim to extend the literature's strongest known classes.

## 6. Exact tests and failure gates

`the original checker` implements validated uniform substitution, the exact reach/source formulas, cyclic-rainbow detection, incidence deletion, colored partition checking, and recursive quotient-core certificate checking. A recursive certificate check verifies the stated structural conditions; for a positive bound it does **not** independently establish the target at every order up to that bound.

`the original checker` implements Theorem 1 for arbitrary forbidden pairs and mandatory vertex-set paths. It deliberately does not incorporate a tournament-completion DFS or the rainbow-triangle rule. The terminal relations remain necessary assertions, never sufficient existence witnesses.

`the original checker` independently computes Boolean-matrix reachability in expanded tournaments and checks:

- All 74,389 substitutions with quotient order one, two, or three and every factor independently a singleton or any of the six colored directed edges. The largest expanded order is six.
- All 2,592 substitutions with an arbitrary two-vertex quotient and one arbitrary three-vertex factor, in either factor position; the other factor is a singleton.
- Recursive examples at depths one through four, orders 3, 9, 27, and 81. Their quotient cores are empty; the latter two entire tournaments are their incidence cores.
- All 216 labeled three-vertex colored tournaments under each of the eight choices of initially fixed pairs, totaling 1,728 known-model fixtures for generic propagation. Forbidden pairs are actual nonreachabilities; mandatory paths have actual interval witnesses; optional global seeds are actual reachabilities. Propagation must never discard the known model or assert a false reachability.
- Empty-domain, singleton-color, impossible-required-path, conflicting-seed, malformed-matrix, malformed-partition, malformed-certificate, and oversized-undecomposed-core gates.
- False stronger claims: omit the quotient return-cycle clause, mistake the reflexive path for a positive cycle, merge colors, ignore the quotient-source condition, omit cross-block color uniformity, or count a transitive rainbow triple as cyclic.

The color-uniformity negative fixture has matrix rows

    [-1, 0, 0,-1]
    [-1,-1, 1,-1]
    [-1,-1,-1, 0]
    [ 0, 0,-1,-1]

and partition {0,1},{2},{3}. Cross-block directions are uniform but the colors from {0,1} to {2} differ. It is cyclic-rainbow-free and has sources {0,2,3}. The representative quotient is a monochromatic directed 3-cycle, whose invalid color-uniform lifting formula would incorrectly add vertex 1. The validator rejects the partition. This demonstrates why ordinary tournament modules cannot simply replace colored modules in the theorem.

All tests use explicit exceptions, not removable assertions. Receipts are produced under ordinary Python, -O, and -OO. Finite tests check the implementations and fixtures; the all-order statements rest on the proofs above. No proof assistant or exhaustive search beyond the precisely stated test families is claimed.

## 7. Frontier

This packet leaves the unrestricted conjecture unresolved. Colored-prime tournaments with large retained incidence cores remain outside the recursive criterion. The interval propagator may stop without a contradiction, and its soundness is not a proof that every obstruction-cycle word is impossible. The strict periodic three-color source problem, a general upper bound on minimal-counterexample order, and any larger finite tournament bound are not established here.

The deliverables are proofs and exact implementation tests of these partial results. No source text or source PDF is copied into the packet. No repository, queue, or publication state is changed by this work.
