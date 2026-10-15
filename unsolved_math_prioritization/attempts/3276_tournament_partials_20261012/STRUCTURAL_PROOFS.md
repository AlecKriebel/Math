Editorial note: The complete authored text is preserved below. Only references to undistributed operational artifacts, their identities, locations and replay directions have been replaced with descriptive prose. Mathematical arguments, evidence counts, corrections and limitations are retained. This prose edition identifies its distributed files and public scholarly sources. Historical conditions in the source record are distinguished from current dependency status in ACCEPTANCE_AND_DEPENDENCIES.md.

# Queue row 1754 / problem 3276 / OPG-1808
## Exact switch-reachability relaxation and incidence reduction

### Recovery and status

This is a newly authored recovery edition of the same second-pass mathematical content. The previous local artifacts were unavailable after a workspace rollback. This edition does not claim to preserve their exact text or bytes. Its tests, manifest, and independent review must refer to these newly produced files.

The exact target concerns every **nonempty finite tournament** whose arcs use at most three colors. It asks for either a **directed cyclic** rainbow triangle or a vertex from which every other vertex is reachable by a monochromatic directed path. The path color may depend on the target. A transitive rainbow triple does not meet the first alternative.

The target remains unresolved by this packet. The results below concern a necessary relaxation and a source-dependent reduction. There is no claim of priority or novelty, and no proposed counterexample.

### 1. Credited starting facts and reconstructed reduction

Our primary dependency is Georgakopoulos and Sprüssel, *On 3-coloured tournaments*, arXiv:0904.1967v2 (17 April 2009), https://arxiv.org/pdf/0904.1967v2. Its Lemma 2.1 credits Shen for the minimal-counterexample structure. Its Lemma 2.7 supplies the switch rule; Proposition 2.8 excludes strict even two-color alternation. Proposition 2.4 and Theorem 3.1 supply the incidence conditions in Section 6. Source statements were re-inspected on 12 October 2026. The later generated date on the PDF title page does not replace its arXiv version date.

Here is a reconstruction of the minimal-counterexample argument. Let D be an induced-minimal counterexample, and form an auxiliary graph with an arc y -> x, **for distinct vertices x and y**, precisely when x cannot reach y monochromatically in D. Each auxiliary arc is an actual tournament arc: otherwise x -> y is a one-arc monochromatic path. Every vertex has positive auxiliary indegree, so an auxiliary directed cycle C exists. The auxiliary graph is a subgraph of a tournament, and has no loops or directed two-cycles.

Every vertex of C fails to reach its predecessor even in D, hence also in D[V(C)]. That induced tournament inherits the absence of a cyclic rainbow triangle and has no universal monochromatic source. Minimality therefore forces C to span D. If x failed to reach a second vertex y besides its predecessor, then y -> x would be an auxiliary chord. The successor cannot be such y because x has an actual arc to it. The segment xCy followed by y -> x would thus give a shorter auxiliary cycle and a smaller induced counterexample, a contradiction.

Each vertex consequently fails to reach exactly its predecessor. This determines the obstruction Hamilton cycle uniquely up to rotation. It does not assert that the tournament has no other Hamilton cycles.

Label C by Z/nZ, n>=3, with actual arcs i -> i+1 of colors w_i in {0,1,2}. All subscripts below are modulo n. Suppose w_i=a and w_{i+1}=b are distinct. The vertex i+2 reaches i, since i is not its predecessor. This reachability cannot use a: append i -> i+1 and i+2 reaches its predecessor. It cannot use b: prepend i+1 -> i+2 and i+1 reaches its predecessor. Hence i+2 reaches i exclusively in the third color c. If the actual chord were i+2 -> i, it would be c-colored and form a cyclic rainbow triangle. Thus the actual chord is i -> i+2. This reconstructs the credited switch rule.

### 2. The necessary relaxation

For an arbitrary cyclic word w of length n>=3, define a directed graph F_c(w) for each c in {0,1,2}. Add these generators:

- A forward generator i -> i+1 if w_i=c.
- A backward generator i+2 -> i if w_i and w_{i+1} are distinct and both different from c.

A backward generator represents a monochromatic path in a hypothetical minimal counterexample, not necessarily an actual tournament arc. At a switch, the actual chord has the opposite orientation. This relaxation omits unknown chord colors, the forced chord orientations, interval-local domination, and all other conditions.

Every generator represents c-reachability. Concatenating represented paths gives a c-walk; deleting loops yields a path between distinct endpoints. Therefore a necessary condition for a minimal counterexample's cycle word is that no F_c(w) reaches x-1 from x.

### Theorem 1. Exact characterization of rejection

Some F_c(w) reaches a predecessor if and only if at least one of the following occurs for some c and x:

(A) The n-1 entries w_x,w_{x+1},...,w_{x+n-2} are all c.

(B) n is odd, m=(n+1)/2, and for every j=1,...,m the pair

    (w_{x-2j}, w_{x-2j+1})

consists of the two distinct colors other than c.

Case (B) forces c to be absent from the whole word.

**Proof.** A walk cannot change generator type. A forward step i -> i+1 followed by a backward step i+1 -> i-1 would require w_i both equal and unequal to c. A backward step i+2 -> i followed by a forward step i -> i+1 has the same contradiction. Thus a nonempty walk uses exclusively +1 steps or exclusively -2 steps. At n=3 the two step destinations coincide, and a single arc can have both generator labels; the argument still prohibits any mixed adjacent pair, so it does not rely on disjointness of the generator types.

A forward walk from x to x-1 has length congruent to n-1 modulo n. Its initial n-1 steps already reach x-1; their existence is exactly (A). A backward walk of length k reaches x-2k. Thus it reaches x-1 precisely when 2k=1 modulo n. This is impossible at even n. At odd n the least positive solution is m=(n+1)/2, and all solutions are congruent to m modulo n. Any such walk has a prefix of length m with the required endpoint. The conditions for those m generators are exactly (B).

The indices covered by the paired entries in (B) are n+1 consecutive integers, from x-(n+1) through x-1. They cover every cyclic position, all required to differ from c. Conversely each condition explicitly provides the necessary walk. QED.

### Corollary 1. All genuine three-color words survive

Every word using all three colors passes this relaxation. Condition (A) leaves only one position for colors other than c and therefore cannot accommodate all three. Condition (B) explicitly forbids c everywhere.

This is an all-order limitation of the chosen relaxation, not evidence that a word can be completed to a counterexample. It even accepts 012 at n=3, which is itself cyclic rainbow. It accepts every repeated 012 pattern. In particular, closure under only these generators cannot settle the three-color-periodic obstruction-cycle pattern asked about in the primary source's Problem 2.1.

### 3. Exact classification for two used colors

Assume w uses exactly two colors. Let

    N={t in Z/nZ : w_{t-1}=w_t}

be the nonswitch positions.

### Theorem 2. Binary words

At even n, the word passes if and only if each used color occurs at least twice.

At odd n, put m=(n+1)/2. The word passes if and only if each used color occurs at least twice and every set

    {x-1,x-3,...,x-(2m-1)}

meets N. Equivalently, in the cyclic order that successively steps by -2, the distance between consecutive nonswitches is at most m. Distance counts steps, not intervening vertices.

**Proof.** For a word using exactly two colors, (A) is equivalent to one color occurring once and the other n-1 times. The long monochromatic interval is the complement of the singleton position. Case (B) cannot occur at even order. At odd order its color must be the missing third color. Its pair condition says exactly that each middle vertex x-(2j-1) is a switch. Since n is odd, repeated -2 steps visit every vertex. A gap of d steps between nonswitches has d-1 intervening switches; absence of m consecutive switches is exactly d<=m. QED.

### Corollary 2. Odd binary obstruction cycles have at least three nonswitches

Any odd-order minimal counterexample whose obstruction cycle uses two colors must satisfy the spacing condition and have at least three nonswitches. The number of switches in a binary cyclic word is even, because a full circuit toggles colors an even number of times. Therefore |N| is odd at odd n. If |N|=1, its unique gap is n>(n+1)/2, contradicting the condition. In particular a binary odd cycle alternating everywhere except at one repeated adjacent color cannot be an obstruction cycle.

This is an authored consequence of a credited switch lemma, without a claim that the consequence is new in the literature.

### 4. Sharpness and limits

- Monochromatic words and binary words with a singleton used color are rejected by (A).
- Every even strictly alternating binary word of length at least four passes this relaxation, although the source's stronger Proposition 2.8 excludes it. The relaxation is strictly weaker than the full source structure.
- The lower bound of three nonswitches is sharp for this relaxation: 00011 passes at n=5. At n=2k+1>=7, the word 000(10)^(k-1) has N={0,1,2}, at least two entries of each color, and step -2 nonswitch gaps k,k,1. Each gap is at most m=k+1. These words are not claimed to come from counterexamples.
- Unknown tournament chords and rainbow-triangle constraints, the forced forward chords, and interval-local domination from source Lemma 2.5 remain relevant. No unrestricted conclusion follows from the word tests.

### 5. Bounded replay

`the original checker` builds the generator graphs and computes reachability by queue search. It separately computes Theorem 1's formula and Theorem 2's nonswitch-gap criterion. It compares all 88,560 labeled ternary words of lengths three through ten, without symmetry reduction, and tests the sharpness family through odd order 101. Explicit exceptions remain enabled under ordinary Python, -O, and -OO. Malformed inputs and intentionally false stronger claims have negative controls.

This finite replay validates the implementation and examples. The all-order statements depend on the proofs above. It is not a search through all tournament completions and does not establish the original target even at those word lengths.

### 6. Canonical incidence deletion

In any finite colored tournament T, repeatedly delete a vertex having, in the current induced tournament, any of these deficiencies:

- Some one of the three colors is absent from all incident arcs.
- Fewer than two distinct colors occur on incoming arcs.
- Fewer than two distinct colors occur on outgoing arcs.

Let the terminal induced vertex set be K(T), allowing the empty set.

### Theorem 3. Order independence and containment

The terminal set is independent of deletion order. Every induced-minimal counterexample contained in T is contained in K(T).

**Proof.** A set S is stable if every vertex meets all three colors inside S and at least two colors in each direction inside S. Enlarging the ambient set preserves these witnesses for each old vertex. This is a vertexwise statement: an arbitrary superset need not be stable, because newly added vertices can be deficient.

No stable set loses a vertex during deletion. At the first purported deletion of one of its vertices, all that vertex's witnesses in the stable set remain. The terminal set is stable and contains every stable set. It is therefore the unique largest stable set, independent of order. The empty set causes no exception.

By the source's Theorem 3.1 every vertex of a minimal counterexample meets all three colors. By Proposition 2.4, together with its Hamilton cycle ensuring nonzero in- and out-degree, it meets at least two colors in each direction. Hence such a counterexample is a stable set and survives. These incidence statements are cited dependencies, not independently re-proved here. QED.

### Corollary 3. All-order sufficient subclasses

Let b be an integer for which the exact target has been established at every order at most b. If T is **nonempty**, has no cyclic rainbow triangle, and |K(T)|<=b, then T has a universal monochromatic source.

Otherwise an induced-minimal counterexample D inside T survives in K(T), and has order at most b, contradicting the assumed finite result. An empty K(T) suffices without any finite computation.

The b=8 specialization is computation-dependent: it may be invoked with an independently accepted exact finite-search certificate through eight. This recovery packet does not contain or audit that separate certificate. Historical acceptance of another packet is not claimed to recover its missing bytes.

The containment is one-way. We do not claim that a universal source of K(T) necessarily extends, or that merely checking goodness of K(T) suffices. The finite hypothesis must cover every possible induced-minimal counterexample of the bounded order.

`the original checker` checks order independence on finite fixtures by enumerating every deletion schedule and every stable subset. This checks the algorithm, not the cited incidence theorems or source existence in those fixtures.
