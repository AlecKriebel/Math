Editorial note: This preserves the complete authored text, with only operational artifact references, undistributed identities and byte counts, locations, and executable command descriptions edited for this prose edition. Mathematical proofs, full audit findings, counts, and limitations remain complete. The structural proof retains its original through-nine premise; the separately accepted through-ten application appears in BOUND_TEN_DEDUCTION.md. Historical candidate conditions are reconciled in ACCEPTANCE_AND_DEPENDENCIES.md. Executable programs and raw enumeration outputs are not distributed.

# Row 1754 / problem 3276 / OPG-1808
## Monochromatic circulation, transitive symmetry, and the prime frontier

12 October 2026 UTC. Fourth confirmed substantive pass in the current program. Lifetime pass total is not asserted.

## Status and target

The target concerns every nonempty finite tournament whose arcs have at most three colors: either there is a directed cyclic rainbow triangle, or a vertex has a monochromatic directed path to every other vertex, with the color allowed to depend on the destination.

**The unrestricted target remains unresolved.** This packet proves an all-order symmetry theorem, gives prime full-core examples outside the prior bounded quotient-core criterion, and sharply distinguishes color-preserving symmetry from symmetry that permutes colors. It gives a necessary divisibility condition for a hypothetical fully symmetric minimal counterexample. It proves no new general finite tournament bound and no unrestricted three-periodic exclusion. There is no novelty or priority claim.

Paths with distinct endpoints can always be taken simple: a directed walk can have repeated segments removed. Strong connectivity includes the length-zero path at a vertex. A return witnessing reversibility of an actual arc has positive length. A singleton is handled separately wherever a prime divisor or positive cycle is used.

## 1. Circulation and reversal of actual arcs

For each color c, let H_c be the directed graph consisting of all vertices and the actual c-colored arcs. Call a coloring balanced if every vertex has equal c-indegree and c-outdegree, separately for every c. This is stronger than the underlying uncolored tournament being regular.

### Lemma 1. Balance implies cycle coverage

In a finite directed graph with equal indegree and outdegree at every vertex, every actual arc u -> v lies on a directed cycle.

**Proof.** Let R be the set of vertices reachable from v, including v. There is no arc from R to its complement. If u were outside R, the given arc would enter R, so summing outdegree minus indegree over R would be strictly negative. The sum is zero by balance, a contradiction. Hence v reaches u. Choose a simple v-to-u path; together with u -> v it is a directed cycle. In a tournament the returning path has length at least two. QED.

The converse is not used and is false: a union of overlapping directed cycles need not have equal indegree and outdegree if arcs are counted only once.

### Corollary 1. Balanced colorings have every vertex as a source

A finite tournament with a balanced coloring, using any finite palette, has monochromatic reachability in both directions between every pair of vertices. In particular every vertex is an outgoing universal monochromatic source.

**Proof.** One of u -> v or v -> u is an actual arc. Its color graph contains a return path by Lemma 1, so that color connects the pair in both directions. QED.

More generally the same conclusion holds whenever every actual arc is on a monochromatic directed cycle, without balance. Neither conclusion needs the absence of a rainbow triangle.

## 2. A spanning monochromatic color under transitive symmetry

A color-preserving automorphism is a permutation of the vertices preserving the direction and the exact color of every actual arc. A group acts transitively when some member takes any specified vertex to any other. No free or regular action is assumed.

### Theorem 1. Transitive small-palette theorem

Let T be a nonempty finite tournament with a transitive group of color-preserving automorphisms.

1. Every vertex is an outgoing universal monochromatic source, for any finite palette.
2. If T has at most three colors, some single color makes the whole vertex set strongly connected. Thus the same color works for every ordered pair of distinct vertices.
3. More generally, if n=|T|>1 and p is the least prime divisor of n, conclusion 2 holds for any palette of size at most p.

**Proof.** For each c, transitivity makes c-outdegree constant and c-indegree constant. Both degree sums count the same total number of c-arcs, so these constants are equal. Lemma 1 applies separately to every color and proves conclusion 1.

For n>1, transitivity also makes the uncolored outdegree constant, equal to (n-1)/2. Thus n is odd and at least three; its least prime divisor p is at least three.

Let E_c(x) be the strongly connected component of x in H_c. Automorphisms preserve c-paths in both directions, so they send c-components onto c-components. Transitivity on vertices implies that all c-components have the same size. In particular, their number divides n. If c is not spanning-strong, that number is a divisor of n larger than one, hence at least p. Therefore |E_c(x)| <= n/p for every x.

Fix x. For any y, the tournament arc between x and y is reversible in its color by Lemma 1. Consequently y belongs to E_c(x) for at least one c. Thus the at most k sets E_c(x) cover V(T), and every one of them contains x. If no color were spanning-strong, then

    n <= sum_c |E_c(x)| - (k-1) <= k n/p - (k-1).

For 2 <= k <= p the last quantity is at most n-(k-1), less than n. For k=1 it is at most n/p, also less than n. This contradiction proves conclusion 3, and conclusion 2 follows because p>=3. Unused colors can be omitted from the palette; they contribute only singleton components if retained.

If n=1, every color graph is strongly connected under the reflexive convention and there is no distinct-endpoint reachability obligation. Any one color from the allowed nonempty palette supplies the conclusion. QED.

The proof uses equal component sizes obtained from transitivity, not a claim that arbitrary balanced colorings have equal component sizes. It also does not identify a color before inspecting the tournament. The conclusion is a spanning strongly connected monochromatic subgraph, not a monochromatic Hamilton cycle.

### Classical group-cover connection, without a novelty claim

The three-color conclusion also relates to Scorza's classical subgroup-cover theorem, stated in Mira Bhargava, *Finiteness criteria for coverings of groups by finitely many subgroups or cosets*, International Electronic Journal of Algebra 2 (2007), 83–89, Theorem 1(ii), https://dergipark.org.tr/en/download/article-file/232921 . That theorem characterizes a cover by three proper subgroups through a Klein-four quotient.

Here the setwise stabilizers of the three components E_c(x) cover the acting group: a group element belongs to that stabilizer exactly when it sends x into E_c(x). A tournament automorphism group has odd order, since an involution would swap a pair and reverse its arc. Thus it cannot have the stated quotient. The elementary equal-component-size proof above needs neither this group theorem nor an assumption of a regular action. This connection is contextual attribution, not a novelty assertion.

### Proposition 1. The palette threshold is sharp in general

For every odd prime p there is a color-preserving vertex-transitive tournament on p^2 vertices with p+1 colors and no spanning strongly connected monochromatic color.

**Construction and proof.** Take the additive group F_p^2. Its p+1 one-dimensional linear subspaces are the colors. For each line choose a nonzero vector v. For each scalar t in {1,...,(p-1)/2}, include the arc x -> x+t v in that line's color, for all x. Every nonzero difference belongs to exactly one line, and exactly one of t and -t is in the displayed scalar set. Thus there is exactly one oriented arc per unordered pair. Translations preserve colors and act transitively.

For a fixed color, the components are exactly the p affine lines parallel to its chosen line. Each is strongly connected because it contains the directed p-cycle given by repeatedly adding v. No c-arc leaves such an affine line. Hence no color is spanning-strong. Every vertex still reaches every other vertex monochromatically, as conclusion 1 predicts. The p=3 instance has nine vertices and four colors, and disproves a false four-color extension of conclusion 2. QED.

### Why balance alone is insufficient for a spanning color

An explicit nine-vertex three-color balanced example has no spanning monochromatic color. Partition its vertices into A={0,1,2}, B={3,4}, C={5,6}, D={7,8}. Assign colors to all cross pairs as follows:

- color 0: A-B and C-D
- color 1: A-C and B-D
- color 2: A-D and B-C

Give the three edges inside A color 0, the edge inside B color 0, the edge inside C color 1, and the edge inside D color 2. Each undirected color graph has only even degrees. Orient an Euler tour in each of its connected components. This gives a tournament balanced in every color. Each color has two components of orders five and four; the tour orientations make both strongly connected. Thus no color spans. All vertices are sources by Corollary 1. `the original checker` fixes a deterministic orientation and `EXAMPLES.md` records its full matrix. This fixture is not asserted to be rainbow-free. It prevents replacing color-preserving transitivity by balance in Theorem 1(2).

## 3. Arbitrarily large colored-prime full-core examples

A colored module M requires that every vertex outside M has exactly the same direction-and-color relationship with every member of M. It is proper nontrivial if 1<|M|<|T|. A colored-prime tournament has no such module.

### Lemma 2. A color consisting of exactly one Hamilton cycle certifies colored primeness

If, for some color c, the actual c-arcs are exactly a directed Hamilton cycle on at least three vertices, then the tournament is colored-prime.

**Proof.** Suppose M is a proper nontrivial colored module. If x belongs to M and its c-successor y does not, then the module condition makes every member of M send a c-arc to y. But the c-indegree of y is exactly one, a contradiction. Hence M is closed under taking c-successors. A nonempty subset closed under the successor of one spanning directed cycle is the whole vertex set, another contradiction. QED.

Containing a monochromatic Hamilton cycle is not enough for this particular primeness statement: extra c-arcs invalidate its indegree-one argument. A fully monochromatic substitution of three nonempty tournaments into a directed three-cycle supplies nontrivial colored modules and contains a monochromatic Hamilton cycle. No such stronger primeness claim is made.

### Theorem 2. Prime full-core family

For every odd n>=7, let T_n have vertex set Z/nZ and actual arcs

    x -> x+d,    1 <= d <= (n-1)/2.

Give distance 1 color 0, distance 2 color 1, and all distances at least 3 color 2. Then:

- T_n is colored-prime and color-preserving vertex-transitive.
- It has no directed cyclic rainbow triangle.
- Every vertex sees all three colors in each direction, so its entire incidence core survives.
- Every vertex reaches every other vertex in color 0 alone.

**Proof.** The distance convention gives exactly one orientation per unordered pair. Translation by one preserves the complete colored tournament and is transitive. Color 0 consists exactly of the directed n-cycle, so Lemma 2 proves colored primeness and that cycle proves spanning color-0 reachability.

Every directed cyclic triangle has three positive forward step lengths in {1,...,(n-1)/2}, whose sum is a positive multiple of n. A rainbow one would have steps 1, 2, and d for 3<=d<=(n-1)/2. Their sum is at most (n+5)/2, which is strictly less than n for n>=7. This is impossible. No transitive rainbow triple is forbidden by this argument or by the target.

At each vertex, steps 1 and 2 give an incoming and outgoing edge in colors 0 and 1, and step 3 gives both directions in color 2. Thus every vertex already has all three colors in both directions, and no incidence deletion can start. QED.

### Exact separation from the previous criterion

Fix any finite bound b. Choose odd n>max(b,6). The tournament T_n has whole incidence core of size n>b and has no proper nontrivial colored module. In a uniform colored-substitution representation, every factor is a colored module. Any nontrivial recursive representation must therefore have only singleton factors at its root, and its root quotient is T_n itself. That quotient has core n>b and fails the prior bounded-quotient-core test. A one-child internal node is not allowed in the prior certificate definition.

Therefore these are arbitrarily large, cyclic-rainbow-free, colored-prime full-core tournaments outside that particular bounded recursive criterion, while Theorem 1 and the direct cycle certificate settle them. This is not a claim to extend the strongest known literature classes. It does not turn colored primeness or a large core alone into a sufficient condition.

## 4. Symmetries of a hypothetical minimal counterexample

The only external structural premise needed here is Shen's obstruction-cycle lemma, reproved as Lemma 2.1 of Georgakopoulos and Sprüssel, *On 3-coloured tournaments*, arXiv:0904.1967v2. An induced-minimal counterexample D has a distinguished directed Hamilton cycle C such that each vertex reaches every vertex except its predecessor on C. The cycle with this property is unique up to rotation. This does not mean D has only one Hamilton cycle.

Allow now an automorphism to preserve directions while applying one fixed global permutation of the three colors to all arcs. Such a permutation preserves whether a path is monochromatic, and so preserves the unique failed predecessor of every vertex.

### Lemma 3. All these symmetries are rotations of the distinguished cycle

Every such vertex permutation commutes with the predecessor permutation of C, and therefore is a rotation of C. In particular the vertex permutation group embeds in the cyclic rotation group. A nonidentity rotation of even order cannot be a tournament automorphism.

**Proof.** If f is an automorphism with a global color permutation, u cannot reach v monochromatically exactly when f(u) cannot reach f(v) monochromatically. The unique failed predecessor is therefore equivariant: f(pred(u))=pred(f(u)). A permutation commuting with a full n-cycle is determined by the image of one vertex, and sends every successive cycle vertex to the corresponding successive image; thus it is a rotation.

If a rotation has even order r, its r/2 power has order two and swaps some pair u,v. Applying it to the arc between that pair would reverse its direction, impossible for an automorphism. QED.

For an induced-minimal counterexample every one of the three colors occurs, by the credited source incidence theorem. Alternatively in the transitive situation of Theorem 3 below all three are forced by the color action. Thus the global permutation on used colors is determined; no ambiguity on unused colors affects the argument.

### Theorem 3. Fully color-permuting-transitive counterexamples have order divisible by nine

Suppose a hypothetical induced-minimal counterexample D admits a vertex-transitive group of the just-defined color-permuting automorphisms. Then:

1. n=|D| is odd and divisible by 9.
2. The obstruction-cycle colors repeat the three colors in a strict period of three, up to their global renaming.
3. Using the separately accepted target theorem through order nine, n>=27.

**Proof.** By Lemma 3 the group acts by rotations. A subgroup of rotations transitive on the n vertices is the full rotation group. In particular the shift g by one vertex of C is an automorphism with some global color permutation sigma. Every cycle arc color is obtained by applying successive powers of sigma to the first arc color.

The rotation g has order n, and Lemma 3 implies n is odd. Its induced permutation on the colors that occur has odd order, dividing n. A permutation of at most three colors with odd order is the identity or a three-cycle. The identity would make C monochromatic; following C from any vertex to its predecessor would then contradict the obstruction property. Thus sigma is a three-cycle, and 3 divides n. This proves the strict three-periodic word statement.

Let m=n/3. The power h=g^m has order three. If 3 does not divide m, its induced color permutation sigma^m is also a three-cycle. For any x, the three distinct vertices x,h(x),h^2(x) form a directed cyclic triangle: the order-three automorphism preserves its orientation, so if the first arc points one way, the other two are its successive cyclic images; the reverse orientation gives the reverse directed cycle. Their three colors are successive images under sigma^m, and hence all distinct. This is a cyclic rainbow triangle, a contradiction. Therefore 3 divides m and 9 divides n.

Since n is both odd and divisible by nine, the possible orders begin 9,27,45,... . The accepted separate finite theorem excludes n=9, giving n>=27. QED.

This does not assume that a three-periodic obstruction cycle forces a symmetry of the whole colored tournament. That converse is unjustified and is a central failure gate. At n divisible by nine the special orbit triangle in the proof is monochromatic, so the same argument gives no further factor of three. The packet does not exclude the fully symmetric class at order 27 or above, and does not exclude arbitrary three-periodic cycles at length 12 or above.

A three-vertex cyclic rainbow triangle has a vertex-transitive action rotating both vertices and colors, but has no universal monochromatic source. This shows why color-permuting transitivity cannot silently replace color-preserving transitivity in Theorem 1. It also shows that rainbow exclusion is essential in Theorem 3.

## 5. Tests, independent-checkable examples, and failure gates

`the original checker` verifies supplied generators by checking every actual arc, and computes their orbit without enumerating the group. `transitive_certificate` checks color-preserving generators only. It rejects directions-only symmetries and color permutations presented as color-preserving. It checks a supplied action; it does not discover all automorphisms.

`the original checker` uses a separate Floyd-Warshall implementation for exact monochromatic reachability. Its finite tests include all labeled tournaments through order four, every circulant six-state color/orientation choice through order eleven, all cyclic-shift-invariant labeled odd-order-five and odd-order-seven cases as part of that circulant scope, the affine sharpness examples, the prime full-core family, a nonregular transitive group action, explicit source/sink and transitive/cyclic-rainbow distinctions, and malformed inputs. Exact counts and receipts are in `STRUCTURAL_VERIFICATION.md` and the three optimization-mode result files.

The nonregular action fixture uses an affine nine-vertex construction with colors determined by the first nonzero coordinate: translations together with a nonidentity shear preserve the coloring and generate a transitive action with nontrivial point stabilizer. This directly tests that regularity is unnecessary.

The proof, rather than these finite tests, establishes the all-order results. No proof assistant, unrestricted exhaustive search, or new finite conjecture bound is claimed. All failures use explicit exceptions, not removable Python assertions. `the original checker` checks the externally pinned manifest, exact file set, byte sizes and hashes, and expected semantic scopes; it is an integrity check rather than a substitute for proof review or fresh computation.

## 6. Residual obstruction

A hypothetical minimal counterexample is still required to be colored-prime and have a full incidence core by the previous accepted results. It cannot have transitive color-preserving symmetry, and a fully transitive color-permuting symmetry would force the restricted situation in Theorem 3. General asymmetric colored-prime tournaments with large cores remain outside these results. The symmetric periodic class surviving the divisibility argument is also unresolved. No actual counterexample is supplied.

There were no remote repository changes, queue changes, publication actions, or further substantive passes inside this task. The exact final packet is frozen for a separate independent audit.
