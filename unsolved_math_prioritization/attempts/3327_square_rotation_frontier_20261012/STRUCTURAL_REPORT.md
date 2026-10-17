# Second newly documented investigation: square selection and contraction rotations

Target: problem 3327 / OPG-172. Lifetime investigation count remains unknown. This report belongs to the second newly documented substantive pass; no history reset or claim of a global solution is made.

## Results

1. For the quartic, triangle-free, K_(2,3)-free two/three-square class, quadrangular Euler-genus-two embeddings are exactly square decompositions of the subgraph consisting of three-square edges. This is a global compatibility criterion, not a claim that the decomposition always exists.
2. In an h=2 target, every low-genus embedding of an edge contraction has a strictly alternating three-plus-three rotation at the contracted vertex.
3. Consequently every edge of an h=2 target belongs to at least two distinct 5-cycles. An edge belonging to exactly two squares must belong to at least four distinct 5-cycles. In particular, no bipartite h=2 target exists.
4. The same pentagon conclusions exclude bipartite ordinary Euler hoppers of Euler genus four, even when their proper minors need not embed in the Klein bottle.

The unrestricted question is still unresolved: arbitrary higher genus, nonbipartite genus-four hoppers, and positive orientably simple Euler-critical graphs remain. No candidate or universal nonexistence proof is supplied.

## Accepted inputs and conventions

The complete accepted [first structural report](../3327_surface_obstruction_reductions_20261012/STRUCTURAL_REPORT.md), [first mathematical audit](../3327_surface_obstruction_reductions_20261012/INDEPENDENT_AUDIT.md), and [first edition acceptance](../3327_surface_obstruction_reductions_20261012/INDEPENDENT_EDITION_ACCEPTANCE.md) remain available unchanged. Their public identities are bound by the first edition manifest and acceptance report.

Write E(G) for Euler genus, and nu(G) for minimum positive nonorientable genus. An h-target satisfies nu(G)=h+2 and all proper minors embed in N_h. An ordinary Euler hopper H has positive Euler genus r and all proper minors of Euler genus at most r-2. The first accepted report proves triangle-freeness, minimum degree four, the corner restriction, and, for h=2, connectedness, 4-regularity, K_(2,3)-freeness, two or three squares through every edge, and order at least twelve. Its 3-connectivity conclusion uses the credited low-connectivity classification; none of the new arguments below requires that classification.

The local augmentation used in those inputs is credited to Campbell's triangle argument: adding an edge between two vertices with a common neighbor costs at most one in positive nonorientable genus above the original Euler genus. See Campbell, *Finding obstructions within irreducible triangulations* (2017), Lemma 5.3, https://dspace.library.uvic.ca/items/cca9ac7d-a34e-4991-99ba-0b0d458e2e62 . No new source retrieval is needed for the deductions below, and no novelty claim is made.

## 1. Exact global square-selection criterion

Let G be a connected finite simple 4-regular, triangle-free, K_(2,3)-free graph. Suppose every edge belongs to exactly two or three graph 4-cycles, here called squares. Let S be the set of all squares and let E_3 be the set of edges contained in three squares. An eligible omitted square is one all of whose four edges belong to E_3.

**Theorem 1.** The following are equivalent:

(a) E(G) is at most two.
(b) G admits a quadrangular embedding on a closed connected surface of Euler characteristic zero.
(c) Some set of eligible omitted squares partitions E_3: each edge of E_3 belongs to exactly one omitted square.

Proof. G has n vertices and 2n edges. Triangle-freeness, simplicity, and minimum degree four give face length at least four in any minimum-Euler-genus cellular embedding. Thus E(G) is at least two. If E(G) is two, Euler's formula forces every facial boundary walk to have length four. Such a walk is a simple graph square: a repeated vertex in a loopless length-four walk forces an immediate reversal at a vertex, which a facial walk cannot have at degree at least two. The same graph square cannot bound two faces, because at each vertex both sides of its incident edge pair would then be corners; that requires degree two. Thus the faces form a set of distinct members of S and every graph edge occurs in two of them.

An edge in two squares therefore permits neither square to be omitted, while an edge in three squares requires exactly one omitted square. Every omitted square consequently uses only E_3 edges, giving (c).

Conversely, omit an exact cover as in (c) and attach a disk along each retained square. Every edge is incident with exactly two disks. At a graph vertex v form the link on its four incident edge ends, with an edge for every retained square corner. This link is simple: two different squares using the same pair va,vb would give a and b the three common neighbors v and their two distinct opposite square vertices, contradicting K_(2,3)-freeness. Each link vertex has degree two because its graph edge has two retained square incidences. A simple 2-regular graph on four vertices is C_4. Thus the disk complex is a closed surface, connected because its 1-skeleton is G. It has n vertices, 2n edges, and n faces, hence Euler characteristic zero. It is a torus or Klein bottle, proving (b) and (a). QED.

### Local interpretation without a false global inference

The full square link at any vertex is C_4, K_4 minus one edge, or K_4. Its link degrees count squares through corresponding incident graph edges. Consequently the spanning subgraph (V(G), E_3) has vertex degrees zero, two, or four.

- At a C_4 link, nothing may be omitted.
- At a diamond K_4-ab, the two E_3 ends are c,d. Their unique square corner cd must be omitted. If that square uses an E_2 edge elsewhere, no exact cover exists.
- At a K_4 link, the omitted corners must be one of its three perfect matchings.

These forced choices must agree around entire squares. The co-Heawood graph already demonstrates that they need not agree globally. In particular, even an all-K_4 local link pattern does not imply any Euler-genus-two embedding. This criterion is not a finite-order bound or classification of the graph class.

## 2. A one-unit Euler-genus bound for a nonalternating split

The following lemma deliberately concerns Euler genus. An automatic nonorientable bound of the same numerical value is not asserted in arbitrary genus.

**Lemma 2 (block reversal).** In a signed rotation embedding, reverse one consecutive proper nonempty block of edge ends at a loopless vertex and reverse the signatures of the incident edges in that block. The resulting signed rotation embeds the same graph with Euler genus at most one greater than before.

Proof. Work with the ribbon neighborhood of the original embedding, whose complementary boundaries are capped to produce its cellular surface. Split the vertex disk into two disks, separating the chosen block from its complementary block, and join the disks by one new untwisted auxiliary ribbon t. This is an expansion inside the original disk and does not change the capped surface. Change the attachment of t by one half-twist. Only the reconnection of the two boundary arcs along this ribbon changes. The number of boundary components changes by at most one, as is seen by removing the ribbon interior and comparing the two pairings of its four boundary ends. Vertex and edge counts are unchanged, so the capped Euler genus increases by at most one. Contract the auxiliary ribbon t. A ribbon joining distinct vertex disks can be contracted; choosing the orientation of the merged disk shows that its effect is exactly reversal of one block and its incident signatures. Contraction preserves the ribbon surface and its capped Euler genus. QED.

**Lemma 3 (quartic split).** Suppose uv is an edge of a simple triangle-free graph, both u and v have degree four, and H=G/uv. Let w be the contracted vertex. Its six distinct incident ends partition into A, the three formerly at u, and B, the three formerly at v. In any cellular embedding of H, if these two classes do not strictly alternate in the cyclic rotation at w, then E(G) is at most one greater than the Euler genus of that embedding.

Proof. A circular word with three A's and three B's has two, four, or six maximal constant runs. With two runs, split the vertex disk between the two blocks and insert uv; the surface is unchanged. With four runs write the circular order as A_1 B_1 A_2 B_2, with each block nonempty. Apply Lemma 2 to the consecutive block B_1 A_2. The new order is A_1 reverse(A_2) reverse(B_1) B_2, in which all A ends and all B ends are contiguous. Split the disk into u and v and insert uv with no further change to the surface. Triangle-freeness ensures that contraction did not merge any edges, so the resulting ordinary graph is exactly G. QED.

**Corollary 4.** In any ordinary Euler hopper with quartic endpoints uv, every minimum-Euler-genus embedding of G/uv strictly alternates the A and B ends. More generally this holds for every embedding of G/uv with Euler genus at most E(G)-2. In particular it holds for every Euler-genus-at-most-two embedding of a contraction of an h=2 target.

Indeed, a nonalternating rotation would give E(G) at most E(G/uv)+1, contradicting the required drop of at least two. For h=2 the accepted first-pass dichotomy gives E(G)=4. This conclusion uses contraction; deletion-only criticality does not suffice.

## 3. The contraction face budget forces pentagons

Let G be an h=2 target and let e=uv. It is quartic and has n vertices and 2n edges. The graph H=G/e has n-1 vertices, 2n-1 edges, minimum degree four, and degree six at w. It is connected, simple, and admits an Euler-genus-at-most-two embedding. Its triangles are exactly the squares of G containing e, so there are t_e=2 or 3 such graph triangles, all through w.

Take a cellular embedding of H of Euler genus k at most two. Each face has length at least three. A triangle cannot occur as the boundary of two faces, since minimum degree four prevents the two incident triangle edges from being corners on both sides at its vertices. Thus the number f_3 of triangular faces is at most t_e, hence at most three. Euler's formula gives

  f_3 - sum_{j>=5} (j-4) f_j = 10-4k.

For k at most one the right side is at least six, impossible. Therefore k=2 and the right side is two. Exactly two possibilities remain:

- f_3=2 and every other face is a quadrangle;
- f_3=3, one face is a pentagon, and every other face is a quadrangle.

All face boundary walks here are simple cycles. In a simple graph a nonsimple closed walk of length at most five either has a loop or contains an immediate reversal: split at a repeated vertex into two nonempty closed subwalks; at least one has length at most two. A facial walk cannot reverse immediately at a vertex of degree at least two. This argument also handles repeated occurrences of w and avoids assuming facial simplicity without justification.

By Corollary 4, the six corners at w alternate A and B. A quadrangular face through w has a simple boundary w-a-b-c-w with a in A and c in B (or conversely). Lifting this face under the inverse contraction gives the simple 5-cycle u-a-b-c-v-u in G, containing e. Different quadrangular faces through w yield different 5-cycles: if their graph 4-cycles were the same, that cycle would bound two faces, impossible at degree at least four.

If f_3=2, the two triangular faces use at most two of the six corners at w, leaving at least four quadrangular faces through w. (In fact every triangle contains w.) If f_3=3, the three triangular faces and the single pentagonal face use at most four corners at w, leaving at least two quadrangular faces there.

**Theorem 5.** Every edge of an h=2 target is in at least two distinct graph 5-cycles. If an edge is in exactly two squares, it is in at least four distinct graph 5-cycles.

**Corollary 6.** No bipartite graph is an h=2 target. More strongly, every such target has girth four and every edge lies on a 5-cycle, so it is not enough for a graph merely to have a few odd cycles away from a locally bipartite region.

The contraction embedding can be orientable or nonorientable; the proof works in either case. The conclusion does not rely on incorrectly equating Euler genus two with Klein-bottle embeddability.

## 4. Extension to ordinary Euler hoppers of Euler genus four

Theorem 5 also holds for any ordinary Euler hopper G with E(G)=4. Here is why the necessary first-pass hypotheses still follow without assuming every proper minor embeds in N_2.

Every proper minor has Euler genus at most two. The accepted triangle augmentation and cubic reconstruction exclude triangles and degree at most three just as in the first report, because they would yield nu(G) at most three and hence E(G) at most three. Euler genus is additive over components, and every positive-genus hopper block has Euler genus at least four by the first report's density exclusion. No isolated vertices or genus-zero redundant pieces are permitted by minor-minimality. Thus G is connected. The deletion face-length count gives 2n <= m <= 2n+1.

The first report's consecutive-corner restriction also remains valid: if, in a minimum-Euler-genus embedding of G-uv, one of the specified internal square corners were consecutive, insert the auxiliary diagonal and restore uv by triangle augmentation. This gives nu(G) at most E(G-uv)+1 <=3 and contradicts E(G)=4. Therefore the same high-degree-vertex argument excludes m=2n+1, and G is quartic. The corner restriction gives K_(2,3)-freeness and at most three squares per edge; contraction Euler genus at most two gives at least two. Lemma 3, the face budget, and the pentagon lifting now apply unchanged.

Consequently there is no bipartite ordinary Euler hopper of Euler genus four. This does not exclude positive orientably simple Euler-critical graphs of Euler genus four, whose proper minors may have Euler genus three, or hoppers of higher genus.

## 5. Verification scope and unresolved work

The accompanying dependency-free checks test the exact-cover criterion on all-two-square Cartesian grids, mixed two/three-square grids, the four-dimensional cube, and the previously accepted co-Heawood near-miss. They independently test the signed block reversal and contiguous split on finite rotation systems. The four named graphs also fail the new pentagon-incidence filter, as expected for these non-target controls. These computations are controls for the local combinatorics and algebra; the written surface arguments carry the unbounded claims.

Actual finite checks: 4,608 two-run and 9,216 four-run signed wheel embeddings were tested, with both rim-orientation patterns, all center rotations, and all 64 sign classes after normalizing the spoke spanning tree. Every contiguous split preserves the capped surface and every block reversal changes Euler genus by at most one. Observed Euler-genus changes were -1 (1,996), 0 (8,302), and +1 (3,526); orientability changed in 288 cases. The 24 alternating center orders are only a word-level negative control: no single interval reversal makes them contiguous. They are not a proof that all conceivable nonlocal surgeries fail. All exact-cover controls retain their actual selected-square or exhausted-search certificates; the failed co-Heawood exact-cover tree has eleven nodes.

The co-Heawood higher-genus/minor investigation is presented in the [separate computational report](COHEAWOOD_GENUS_REPORT.md). This report does not duplicate or assume its conclusions. It is already excluded as an h=2 target by Corollary 6, because it is bipartite; that does not determine which of its minor hypotheses fails or its actual genus.

The square-selection problem remains globally nontrivial. The new contraction obstruction removes every bipartite candidate in the first genus and imposes a pentagon-rich frontier on the nonbipartite class. It neither proves an exact cover must exist there nor constructs any simultaneous obstruction. The unrestricted existence obligation still requires an example in one of the two equivalent classes or proofs that both classes are empty in every genus.

