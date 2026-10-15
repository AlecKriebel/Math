# Fixed cut-complement extension: bounded evidence and a local-cut obstruction

## Status and scope

This packet does **not** prove or disprove the Weak pentagon conjecture (OPG434), which asks whether every finite simple triangle-free cubic graph maps to the Clebsch graph. It does not settle whether **every global maximum-cut complement** extends as a prescribed canonical Clebsch color class.

It proves a narrower negative result: **a single-vertex-local-maximum cut is insufficient** for that extension, even in a connected simple triangle-free cubic graph on 14 vertices. The counterexample has an ordinary Clebsch homomorphism, and both of its global maximum cuts have the requested extension.

It also records positive, independently checked certificates for every normalized maximum cut in the supplied House of Graphs connected triangle-free cubic catalogs at orders 6,8,...,20. This exhausts the supplied records. Transfer to all isomorphism classes depends on the catalog's externally asserted completeness and nonisomorphism; neither its graph-generation algorithm nor that assertion is re-proved here. No novelty claim is made.

## Definition of the stronger extension

Let U={1,2,4,8} and J=15, using four-bit integers with bitwise xor as addition in F_2^4. The Clebsch graph C has vertices 0,...,15 and connection set U∪{J}.

For a cut δ(S) in G, put M=E(G)\δ(S). A **fixed-M extension** is a map f:V(G)→F_2^4 for which

- f(u) xor f(v)=J on every uv in M;
- f(u) xor f(v)∈U on every uv outside M.

Thus M is exactly the preimage of the canonical J-class. This is stronger than merely finding a homomorphism G→C. Equivalently, G−M maps to the ordinary 4-cube with the endpoints of every M-edge forced antipodal.

A cut in a cubic graph is a single-vertex-local maximum exactly when M is a matching: flipping a vertex with k uncut incident edges changes the cut size by 2k−3. In particular every global maximum cut has this property. Every 5-cycle meets any matching cut complement in exactly one edge: cut parity makes its number of M-edges odd, and a matching on five vertices has size at most two. Consequently its other four edges must receive all four distinct unit differences under a fixed-M extension. This necessary condition holds in the counterexample; the obstruction is the incompatibility among several paths.

## Authored 14-vertex obstruction

The vertex set is {0,...,13}; the edge set is

01, 04, 0-11, 12, 18, 26, 2-12, 35, 3-10, 3-12, 47, 4-13, 59, 5-13, 67, 6-10, 79, 89, 8-10, 11-12, 11-13.

Here a hyphen separates labels whenever needed to avoid ambiguity. An unambiguous equivalent edge list is

(0,1), (0,4), (0,11), (1,2), (1,8), (2,6), (2,12), (3,5), (3,10), (3,12), (4,7), (4,13), (5,9), (5,13), (6,7), (6,10), (7,9), (8,9), (8,10), (11,12), (11,13).

The graph was constructed by an authored seeded random configuration-model search, not copied from a catalog. The specific historical discovery implementation is not retained. Its displayed mathematical definition is complete: direct independent checks establish connectivity, simplicity, cubicity and triangle-freeness.

Take S={1,3,6,7,8,11,13}, equivalently the bitmask 10698. Its complement M consists of

04, 18, 2-12, 59, 67, 11-13.

These six edges form a matching. The cut has size 15 and is a strict local maximum with respect to a single vertex flip: every such flip decreases its size by one or three. It is not a global maximum.

### Hand proof that this M cannot extend

Suppose f were a fixed-M extension. The 5-cycle 0-1-2-12-11-0 contains only the M-edge 2-12. Its four unit differences are therefore distinct: four unit vectors xor to J only when each occurs once. Translating all values and permuting the four coordinates lets us normalize

f(0)=0, f(1)=1, f(2)=3, f(11)=4, f(12)=12.

The M-edges then give f(4)=15, f(8)=14 and f(13)=11.

Write N(x)={x xor 1,x xor 2,x xor 4,x xor 8} for the ordinary cube neighbors. The edge 2-6 gives f(6)∈N(3). Since f(7)=f(6) xor 15 and 4-7 is a unit edge, also f(6)∈N(0). Thus f(6)∈{1,2}. The unit path 6-10-8 rules out f(6)=1: 1 and14 are antipodal and cannot be joined by a two-step cube walk. Hence f(6)=2.

Similarly, 5-13 and 8-9, together with f(9)=f(5) xor15, give

f(5)∈N(11)∩N(1)={3,9}.

The unit edge 7-9 requires f(6) xor f(5) to be a unit vector. Since f(6)=2, this rules out f(5)=9 and forces f(5)=3. But the unit path 5-3-12 would join antipodal values3 and12 in two steps, a contradiction. ∎

This proof uses only the displayed graph and elementary cube distances. The independent solver also returns no extension, after 522 search calls; the hand proof, rather than an unverified UNSAT solver status, is the negative certificate.

### Hand certificate of the actual maximum cut

The following seven pentagons are in G:

- 0-1-2-12-11-0
- 1-2-6-10-8-1
- 2-6-10-3-12-2
- 3-5-9-8-10-3
- 3-5-13-11-12-3
- 4-7-9-5-13-4
- 6-7-9-8-10-6

Each graph edge lies in at most three of them. Every cut omits an edge of every odd cycle. Therefore two omitted edges could hit at most six of these seven cycles, so every cut omits at least three edges and has size at most18.

The cut S₀={1,3,4,6,9,11}, with bitmask2650, has size18, proving MAXCUT(G)=18. Exhaustively checking all 2^13 normalized cuts shows that the only two maximum-cut bitmasks are2650 and7794.

Fixed-complement witnesses f(0),...,f(13), in that order, are:

- cut2650: (0,1,3,8,2,9,2,0,5,1,10,4,12,6)
- cut7794: (0,1,3,15,1,11,2,0,5,4,13,8,7,9)

An unrestricted Clebsch witness is

(0,1,3,9,1,8,2,3,5,7,13,4,11,0).

All three witnesses were checked edge by edge by the original normal-mode example suite and the independent assertion-free audit. The graph is consequently not a counterexample to the original conjecture or to fixed-global-maximum extension.

## Complete checks of the supplied catalogs

Every supplied record was checked for the declared even order, simplicity, degree three at every vertex, connectivity and absence of triangles. Exact duplicate graph6 records were rejected. Isomorphism rejection is inherited from the catalog provider; it was not independently rerun.

Order | Supplied graphs | Normalized maximum-cut pairs | Result
--- | ---: | ---: | ---
6 | 1 | 1 | positive
8 | 2 | 5 | positive
10 | 6 | 17 | positive
12 | 22 | 51 | positive
14 | 110 | 287 | positive
16 | 792 | 2,014 | positive
18 | 7,805 | 21,391 | positive
20 | 97,546 | 307,120 | positive
Total | 106,284 | 330,886 | positive

A normalized cut fixes vertex0 outside S, removing the duplication between S and its complement. Each pair has an explicit 4-bit witness in the private certificate stream. No equivalence of nonmaximum cuts is used to reduce the search.

For the supplied catalogs at orders6,8,10,12 we additionally checked **every** cut whose complement is a matching. The graph counts are1,2,6,22 and the corresponding normalized cut counts are1,9,28,175, totaling31 graphs and213 pairs. All extend. Subject to the provider's completeness assertion, the14-vertex local-cut obstruction is minimum order among connected simple triangle-free cubic graphs. Cubic graphs have even order; orders below6 contain no such graph. Disconnected graphs cannot give a smaller example because the extension problem separates componentwise.

## Why the positive certificate checking is exact

The original builder scans all 2^(n−1) normalized cuts using a Gray-code score update. Its constraint solver uses all16 possible values per vertex, fixes f(0)=0 by translation symmetry, repeatedly removes values with no edge-compatible support, and exhaustively branches on any remaining domain. It accepts only full singleton assignments. The solver is only a way of producing positive witnesses; no negative catalog conclusion relies on it.

The standalone original C++ verifier does not import the builder or call its constraint solver. It reads the exact original catalog in order, checks graph validity and record equality, then independently computes every normalized cut score by the recurrence

c(T)=c(T\{v})+3−2|N(v)∩(T\{v})|,

where T is a vertex subset excluding0 and v is its least element. It compares the true maximum with the claimed one, checks every listed cut is maximum, rejects duplicates, directly checks every edge difference, and finally requires every maximum cut to appear. Thus an omitted hard cut cannot silently pass. The corresponding local-cut C++ verifier replaces the maximum-cut coverage predicate by the matching-complement predicate for the through-12 local-cut screen.

The construction lane also included a separate Python implementation using direct cut-score summation and a separate forward-checking vertex-assignment search. Its normal-mode checks establish the exact numerical facts about the 14-vertex example and verify every algebraic set equality used in the hand proof. Its assertions disappear under -O and -OO; those optimized original runs are not verification. A separately authored assertion-free reconstruction passed in all three modes; see [Fixed cut audit](FIXED_CUT_AUDIT.md).

Five solver controls cover a forbidden triangle, positive unrestricted and prescribed pentagons, an impossible one-J square and an impossible three-J pentagon. Mutation tests reject a wrong maximum, wrong witness, omitted maximum cut, duplicated cut, missing record and extra record; the unaltered positive control passes. These original checks are implementation-independent replay within the construction lane. The later [independent mathematical audit](FIXED_CUT_AUDIT.md) additionally replayed all accepted catalog coverage with a different exhaustive algorithm. It found no mathematical correction, but established that the original bare C++ verifier needs full input binding: empty paired inputs and jointly truncated valid prefixes can otherwise pass, and unused graph6 padding bits are ignored. The accepted audit binds exact input bytes, inventory, order, count and canonical padding.

## Proven elementary boundary: at most one prescribed edge

If a triangle-free graph has a cut complement M with |M|≤1, then that M extends, without a degree restriction. For M empty, map the bipartition to the endpoints of one cube edge. For M={uv}, put B=G−M. B is bipartite, and u,v have equal parity in the original cut. If they are in the same B-component, their distance d_B(u,v) is even and at least4: distance2 would produce a triangle. Map a vertex at distance d from u to the d-th vertex of the cube path 0,1,3,7,15 for d≤4; for d>4 use15 at even d and7 at odd d. Adjacent B-vertices have distances differing by exactly1, so this is a cube homomorphism; u and v map to0 and15. Map other components to a single cube edge. If u,v lie in separate components, map their respective bipartitions to cube edges chosen to give u value0 and v value15. This proves the claim. It makes no assertion about two or more prescribed edges.

## Sources, provenance and residual

- House of Graphs, Connected cubic graphs: https://houseofgraphs.org/Cubic. This is the source of the finite input lists and their stated completeness/nonisomorphism. Its public page says the minimum-girth3,4,5 counts were independently confirmed by genreg, minibaum and snarkhunter through30 vertices. Our verification confirms the supplied records and witnesses, not those generation implementations.
- Exact public catalog URLs, byte lengths, record counts and SHA-256 hashes are in CATALOG_METADATA.json. The official site exposed the published download endpoints; unsuccessful guessed endpoints returned HTML and were not used as inputs.
- Matt DeVos and Robert Šámal, High-girth cubic graphs are homomorphic to the Clebsch graph, author-hosted manuscript: https://iuuk.mff.cuni.cz/~samal/papers/clebsch/clebsch.pdf. Proposition1.1 gives the cut-complement/projective-cube equivalences; Theorem1.3 handles maximum degree3 and girth≥17; Conjecture1.4 states the full triangle-free cubic target. These are background and scope checks, not evidence for the new fixed-cut finite computation.

This edition distributes the full authored mathematical graph, proofs, audits, public URLs and permitted verification metadata. It excludes programs, imported catalogs, certificate streams, raw search collections, source copies and private coordination material. The original shell reproduction workflow compares generated certificates with undistributed reference certificates and therefore cannot run unchanged from this edition. The prose and explicit examples are self-contained; the catalog evidence is an audited bounded computation rather than a bundled, publicly rerunnable experiment. See [Reproduction scope](REPRODUCTION.md).

The next mathematical question is whether global maximality supplies the additional compatibility missing from the local example, or whether an explicit globally maximum obstruction exists. The completed finite screen does not answer that question and does not resolve the original conjecture.
