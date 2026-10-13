# Independent acceptance audit: second documented surface-obstruction pass

Target: row 1756 / problem 3327 / OPG-172. This audit concerns the second newly documented investigation. The lifetime investigation count remains unknown. The unrestricted problem remains unresolved.

## Accepted conclusions

The corrected structural argument and the co-Heawood computation establish the following bounded results.

1. For a connected simple quartic triangle-free K_(2,3)-free graph with two or three squares through each edge, Euler genus two is equivalent to an exact square decomposition of the subgraph of three-square edges.
2. Every edge of an h=2 target lies on at least two distinct 5-cycles. If it lies on exactly two squares, it lies on at least four distinct 5-cycles. Therefore no bipartite h=2 target exists. The same pentagon conclusions hold for ordinary Euler hoppers of Euler genus four, excluding bipartite graphs in that class as well.
3. For the Fano point-line nonincidence graph G and e=(0,10), E(G)=nu(G)=4, E(G-e)=2 and nu(G-e)=3, while 3<=E(G/e)<=nu(G/e)<=4. Thus this graph fails both the required Klein-bottle deletion condition and the Euler-hopper contraction condition.

No implication from a genus lower bound alone to minor-minimality is accepted. No general existence or nonexistence conclusion, exact contraction genus, historical global-status certificate, or novelty claim is made.

## 1. Structural proof audit

### Square selection

The omitted-square exact-cover criterion has both directions. Density forces an Euler-genus-two embedding to be quadrangular. A length-four facial walk is a simple square here, and the same square cannot bound two faces at vertices of degree greater than two. Thus every two-square edge retains both squares and every three-square edge omits exactly one.

Conversely, an exact cover of the three-square edges leaves exactly two retained square incidences at every edge. K_(2,3)-freeness ensures that each vertex link is simple: two distinct squares with the same corner would give three common neighbors. The link is consequently a simple 2-regular graph on four vertices, necessarily C4. Attaching the retained square disks therefore gives a genuine closed connected surface, rather than a pseudomanifold with singular vertices. Its Euler characteristic is zero. No global compatible-square choice is inferred from the local links alone.

### Corrected block reversal

The accepted lemma is an Euler-genus bound. Separate a consecutive proper block of incident ends into a second vertex disk joined to the first by an auxiliary untwisted ribbon. Twisting this ribbon changes only the pairing of its four boundary ends, and hence changes the number of boundary components by at most one. Contracting the auxiliary ribbon yields exactly the block reversal and the incident-sign changes. This proves an Euler-genus increase of at most one.

The review specifically rejects an unnecessary stronger formulation in which the cellular Euler genus always rises by exactly one or the capped result is automatically nonorientable. Both fail in finite controls. An arbitrary-genus nonorientable bound is not inferred from the Euler bound.

A cyclic three-plus-three partition has two, four, or six runs. Two runs permit a direct split. In the four-run case A1 B1 A2 B2, reversing B1 A2 makes the A and B ends contiguous and permits the split. Triangle-freeness ensures the contraction had not merged any edges, so the reconstructed graph is exactly the original graph. Hence an Euler hopper cannot have either of these nonalternating contraction rotations at an embedding within two of its Euler genus. This argument applies directly to h=2 targets, whose Euler genus is four.

### Face budget and repeated walks

A contraction of an h=2 target has n-1 vertices, 2n-1 edges, degree six at the contracted vertex, minimum degree four, and two or three graph triangles. In a cellular embedding of Euler genus k<=2,

f3 - sum over j>=5 of (j-4)fj = 10-4k.

A triangle cannot bound two faces in this minimum-degree range. Thus f3<=3, forcing k=2 and precisely two possibilities: two triangles with all other faces quadrangular, or three triangles with one pentagonal face and all others quadrangular.

The repeated-walk issue is resolved without assuming polyhedral embeddings. A nonsimple closed walk of length at most five in a simple graph splits at a repeated vertex into two nonempty closed subwalks, one of length at most two. That forces a loop or an immediate reversal. An immediate facial reversal requires degree one. Consequently every face in these two profiles is a simple cycle, and each uses the contracted vertex at most once.

Strict alternation of its six corners leaves at least four quadrangular corners in the two-triangle case, and at least two in the three-triangle/one-pentagon case. Each quadrangle lifts across the inverse contraction to a simple 5-cycle containing the original edge. Distinct quadrangular faces give distinct cycles, since a square cannot bound two faces in this degree range. The stated pentagon counts follow.

The extension to ordinary Euler-genus-four hoppers correctly rederives connectedness, the density alternatives, quarticity, the corner restriction and the two/three-square condition using Euler-minor hypotheses. It does not assume their minors embed in the Klein bottle. The accepted first-pass triangle augmentation and block-genus facts remain source dependencies; this audit does not independently re-prove the cited literature classifications.

## 2. Independently reconstructed co-Heawood computation

The graph was reconstructed from the seven nonzero vectors of F2^3 and the seven XOR-zero triples, without importing the author's graph-generation or search code. Squares were recovered by independently inspecting induced four-vertex subgraphs.

The reconstruction gives 14 vertices, 28 edges and 21 squares, with exactly three squares through every edge. For the original quartic graph a selected corner-link graph is extendable precisely when it has maximum degree at most two and contains no triangle; disconnected partial paths are allowed. This produces 84 distinct forbidden triples of squares. Some triples have more than one local witness, so 112 local star/triangle witnesses must not be mistaken for 112 distinct triples.

Independent exhaustive counts agree:

- 293,930 twelve-square subsets: zero compatible.
- 352,716 eleven-square subsets: zero compatible.
- 352,716 ten-square subsets: 252 compatible.
- After deleting (0,10), 18,564 twelve-square subsets of eighteen squares: exactly one compatible.

Any cellular embedding of G has at most ten square faces. All its other facial walks have even length at least six. Thus 56>=6F-20, so F<=12 and E(G)>=4. The explicit nonorientable genus-four certificate independently replays to twelve faces: ten squares, one hexagon and one decagon. Its complete graph identity, rotations and signs were checked before evaluating the face permutation. The orientability test detects inconsistent sign potentials. Therefore E(G)=nu(G)=4.

### Compact orbit certificate

A second independent exact check constructs the 168 invertible linear transformations of F2^3, acts on the graph's squares, and closes compatible square selections under every one-square extension. The numbers of orbit representatives at sizes zero through eleven are:

1, 1, 4, 14, 39, 83, 128, 119, 67, 17, 2, 0.

The corresponding total numbers of compatible subsets are:

1, 21, 210, 1246, 4725, 11655, 18438, 17874, 9765, 2604, 252, 0.

The author independently generated the same orbit counts. A list of all representatives, the 84 forbidden triples, the complete square list and the 168 basis images supplies a small inductive certificate: every allowed extension of a listed representative maps to the next list, and the list at size eleven is empty. This certificate proves the same finite bound without publishing a large search log or accepting a failed heuristic search.

### Deletion completion and orientability

The unique compatible twelve-square subset of G-e forces exactly one unoriented local cyclic order at each vertex. Normalizing the local directions leaves every edge signature forced by the facial-square equations. Independent reconstruction finds no unused sign variable and obtains balanced signatures, twelve square faces and one hexagonal face. Its Euler characteristic is zero and its surface is orientable.

This proves absence of a Klein-bottle embedding, not merely existence of a torus embedding. Density forces Euler genus at least two. If an N2 embedding existed, capping its regular neighborhood could not lower Euler genus; equality forces every complementary component to be a disk, retaining N2 rather than producing a torus. Its unique normalized Euler-genus-two completion would therefore have to be nonorientable, contrary to the exact sign calculation. Adding a crosscap to the exhibited torus supplies the upper bound nu(G-e)<=3. Hence E(G-e)=2 and nu(G-e)=3.

### Contraction rejection

The contraction graph was separately reconstructed and its cycles generated by a different procedure. It has thirteen vertices, twenty-seven edges, three triangles and eighteen squares. Density and the triangle count show that any Euler-genus-at-most-two embedding would have Euler genus exactly two, with either two triangles and twelve squares, or three triangles, ten squares and one pentagonal face.

Instead of enumerating cyclic orders, the independent check tests whether each partial link is a disjoint union of paths or a complete cycle on all incident-edge symbols. A proper subcycle and degree greater than two are forbidden. This is equivalent to containment in a cyclic order and retains disconnected paths, including at the degree-six vertex. The permitted link-mask counts are 37 at degree four and 1,556 at degree six.

Independent replay finds zero compatible selections among 55,692 cases for the first profile and 43,758 for the second. The unspecified pentagonal face is not constrained more strongly than needed. This proves E(G/e)>=3. Minor monotonicity supplies nu(G/e)<=4. No failed search for an N3 embedding is used to improve either bound.

## 3. Hostile controls and finite scope

The independent block-reversal test covers all 120 cyclic orders at the second hub of K_(2,6), all 32 signature classes after fixing a positive spanning tree, and every four-run three-plus-three partition at the first hub: 46,080 cases. Observed Euler-genus changes are -1 in 15,384 cases, zero in 15,312 and +1 in 15,384. All 46,080 ensuing contiguous splits preserve the capped surface and orientability. The 2,052 cases starting at Euler genus at most two satisfy the required N3 bound. These finite tests corroborate, but do not replace, the ribbon proof.

Positive partial-link controls include the empty graph, disconnected paths, a three-edge path and a complete C4. Negative controls include a three-star and a proper triangle. Certificate mutations with duplicate edges, zero signs and false face counts are rejected. The author additionally supplies vertex-switch controls, wrong-geometry and wrong-orientability controls and a separate flag-involution replay.

All four independent replay programs were executed in normal Python, -O and -OO with byte-identical outputs. No essential check relies on Python assertions. Exact accepted author bytes and the acceptance-report digest are recorded in the accompanying acceptance record. The checks remain finite certificate verification and local-surgery regressions; they do not enumerate all target graphs or all genera.

## 4. Boundary of acceptance

The second pass narrows the first-genus frontier and definitively rejects one natural candidate. The outstanding existence alternatives are still a positive orientably simple Euler-critical ordinary graph or an ordinary Euler hopper, with the qualified doubling construction from the first report. Nonbipartite genus-four hoppers, higher-genus hoppers and the orientably simple route remain open within this investigation.

The public material consists only of authored mathematical arguments, exact mathematical certificates and verification metadata. Discovery scripts, raw source files and coordination material are not part of the publication payload.
