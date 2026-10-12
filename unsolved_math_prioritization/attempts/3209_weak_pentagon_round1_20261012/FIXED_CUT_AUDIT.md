# Independent audit: prescribed maximum-cut complements and Clebsch extensions

## Verdict and exact boundary

**Accept the mathematical local-cut counterexample, the elementary one-edge theorem, and the exact positive result on the supplied finite catalogs.** Accept neither a proof of the Weak pentagon conjecture nor an all-order fixed-global-maximum-cut extension theorem. Both targets remain unanswered by this work. The source packet's mathematical claims require no correction; its reusable verification and publication descriptions require the qualifications below.

The independently checked source packet manifest contained 98 members. Its undistributed manifest identity is omitted from this edition. Every member's bytes and hash matched, and the inventory was exact, with the manifest itself as the only additional file. The source packet was left unchanged. The independent reviewer rebuilt the two supplied C++ certificate verifiers, replayed both complete claimed finite computations, replayed the supplied ordinary-mode Python checks and mutations, and implemented a different exhaustive cut algorithm and an assertion-free reconstruction of the explicit example.

This is an audit of pinned mathematical evidence. Public source attribution and source-provider generation claims are not independently reproved, and no current-literature or novelty conclusion is inferred.

## 1. Definitions and elementary necessities

Work in the additive group of four-bit vectors, represented by integers 0 through 15 with xor. Put U={1,2,4,8} and J=15. The graph with connection set U union {J} is the canonical Clebsch model used throughout. For a cut delta(S), let M be its edge complement. A prescribed extension is a vertex map f such that its edge differences are J exactly on M and members of U exactly on the cut. It is therefore a Clebsch homomorphism with a specified canonical color class; unrestricted Clebsch homomorphism does not imply this stronger condition for an arbitrary M.

At a cubic vertex with k uncut incident edges, flipping that vertex changes the cut size by 2k-3. Thus a cut is a single-vertex local maximum if and only if k is at most one at every vertex, equivalently M is a matching. Such a local maximum is strict, because a flip loses one or three edges. Every global maximum is necessarily among these cuts.

On any cycle, the number of crossing edges is even. A matching complement on a 5-cycle must consequently have an odd number of edges, and at most two; it has exactly one. In a prescribed extension the four remaining differences xor to J. Each of the four coordinate bits must occur an odd number of times among four unit vectors, so each occurs exactly once. This reasoning does not presume injectivity of the homomorphism.

Translation f(v) to f(v) xor a preserves every edge difference, and coordinate permutations preserve U and J. These are the only target symmetries needed below. Fixing vertex 0 outside S removes precisely the complementary-cut duplication: each unordered bipartition has exactly one such representative. No quotient by graph automorphisms or by nonmaximum cuts is used.

## 2. The 14-vertex obstruction: full reconstruction

The authored graph has vertex set {0,...,13} and edges

(0,1), (0,4), (0,11), (1,2), (1,8), (2,6), (2,12), (3,5), (3,10), (3,12), (4,7), (4,13), (5,9), (5,13), (6,7), (6,10), (7,9), (8,9), (8,10), (11,12), (11,13).

Direct checks establish 21 distinct loop-free edges, degree three at every vertex, connectivity and no triangle. For S={1,3,6,7,8,11,13}, whose bitmask is 10698, the uncut edges are

(0,4), (1,8), (2,12), (5,9), (6,7), (11,13).

Their 12 endpoints are distinct. The cut has size 15 and every single-vertex flip strictly reduces its size.

### Nonextension proof

Suppose a prescribed extension existed. The pentagon 0-1-2-12-11-0 has just the uncut edge (2,12). By the preceding four-unit observation, translation and coordinate permutation give

f(0)=0, f(1)=1, f(2)=3, f(11)=4, f(12)=12.

The other three relevant uncut edges force f(4)=15, f(8)=14 and f(13)=11. Let N(x)={x xor d : d in U}.

From the unit edges (2,6),(4,7) and the J-edge (6,7), one obtains

f(6) in N(3) intersect N(0)={1,2}.

The unit path 6-10-8 cannot join the antipodal values 1 and 14 in two steps: their cube distance is four. Hence f(6)=2.

Likewise the unit edges (5,13),(8,9) and J-edge (5,9) imply

f(5) in N(11) intersect N(1)={3,9}.

Since both (6,7) and (5,9) are J-edges, the unit edge (7,9) implies f(6) xor f(5) is a unit. With f(6)=2, only f(5)=3 remains. But the unit path 5-3-12 would then join antipodal values 3 and 12 in two steps, a contradiction.

All edge classifications and set identities in this argument were independently checked. Additionally, an independent complete reconstruction enumerated all 16 translations and all 24 coordinate permutations of the initial pentagon, hence 384 initial assignments. Across their 1,536 possible pairs of values at vertices 6 and 5, no completion was possible. This finite reconstruction is corroboration of the hand proof, not a substitute for it and not an inference from a solver timeout.

### Actual global maximum and positive witnesses

The following seven pentagons exist:

1. 0-1-2-12-11-0
2. 1-2-6-10-8-1
3. 2-6-10-3-12-2
4. 3-5-9-8-10-3
5. 3-5-13-11-12-3
6. 4-7-9-5-13-4
7. 6-7-9-8-10-6

No edge occurs in more than three of these cycles. A cut omits at least one edge of each odd cycle. Two omitted edges could cover at most six of the seven cycles, so every cut omits at least three of the graph's 21 edges: its size is at most 18. The cut of bitmask 2650 has size 18 and attains this bound.

Independent direct summation over all 8,192 normalized cuts finds exactly two maximum cuts, bitmasks 2650 and 7794. In vertex order 0,...,13, valid prescribed witnesses are respectively

(0,1,3,8,2,9,2,0,5,1,10,4,12,6),

(0,1,3,15,1,11,2,0,5,4,13,8,7,9).

A valid unrestricted Clebsch witness is

(0,1,3,9,1,8,2,3,5,7,13,4,11,0).

Every one of the 21 edge differences in each witness was checked independently. Consequently the graph refutes only prescribed extension for a single-vertex-local maximum. It refutes neither unrestricted Clebsch homomorphism nor prescribed extension for a global maximum.

## 3. Exact finite coverage and independent enumeration

The following numbers passed both the rebuilt supplied checker and the independently authored checker:

| Order | Supplied graph records | Normalized global-maximum-cut pairs |
|---:|---:|---:|
| 6 | 1 | 1 |
| 8 | 2 | 5 |
| 10 | 6 | 17 |
| 12 | 22 | 51 |
| 14 | 110 | 287 |
| 16 | 792 | 2,014 |
| 18 | 7,805 | 21,391 |
| 20 | 97,546 | 307,120 |
| **Total** | **106,284** | **330,886** |

All records were checked for declared order, canonical graph6 character range, exact length and zero padding, cubicity, simplicity, triangle-freeness and connectivity. Exact duplicate encodings were rejected. Declared file-level record counts and pinned input bytes were checked independently. Every certificate record had to match its catalog record exactly; every required cut appeared once; every map value lay in {0,...,15}; and every edge satisfied its exact prescribed difference condition.

The supplied checker recomputed every normalized cut score by its subset-removal recurrence and required the maximum and its entire set of maximizing cuts to agree. Across all orders this entails 52,192,116,000 normalized cut positions. The recurrence is correct because adding vertex v changes the score by degree(v) minus twice the number of its neighbors already on that side. The unsigned-byte score type is safe for the supported orders, since a cubic graph on at most 30 vertices has at most 45 edges.

### Different independent algorithm and its completeness proof

The new checker does not use the builder's Gray-code update or the supplied verifier's subset-score recurrence. It enumerates Boolean assignments x(v), fixes x(0)=0, and requires each vertex to have at least two oppositely assigned neighbors. It propagates only these implications:

- If a vertex's value is assigned and one neighbor already has that same value, every unassigned neighbor must receive the opposite value; two same-valued neighbors reject the branch.
- If a vertex is unassigned and at least two of its neighbors have one common value, the vertex must receive the opposite value.

Both rules are necessary consequences of the local-maximum constraint. On any remaining unassigned variable, both values are explored. Thus no feasible complete assignment is removed: following the values of any feasible assignment gives a surviving branch to that assignment. A terminating complete assignment is directly checked against every local constraint. Branching creates no duplicate assignments.

The checker exhaustively found 4,723,275 locally optimal normalized cuts across the 106,284 records and directly summed their crossing edges. Every true global maximum lies in this collection, by the cubic local criterion. Therefore the largest score among the collection is the true global maximum, and selecting all leaves of that score produces its complete set of normalized maximizing cuts. This set had to equal the set in the certificate, and all witness edge differences were then checked. For orders through 12, direct enumeration of all normalized cuts independently cross-checked the entire local-optimum set: 48,416 mask positions over 31 records.

The optimized independent checker was compiled with `-O3 -DNDEBUG`; its requirements remain active and do not depend on C/C++ assertions. It completed without a search cutoff, random sampling or timeout-based inference.

### Local screen and minimum-order qualifier

For the complete supplied catalogs at orders 6,8,10,12, both checkers verified every matching-complement cut. There are respectively 1,9,28,175 such normalized pairs, totaling 213 on 31 graphs. Thus, conditional on the provider's asserted completeness, no smaller connected triangle-free cubic graph has the local-cut obstruction. Simple cubic triangle-free graphs cannot have order below 6, and cubic orders are even. For disconnected graphs, any local cut restricts to a local cut on each component, and prescribed extensions can be combined componentwise. Hence the same conditional minimum-order conclusion applies without connectedness.

The catalogs' completeness and pairwise nonisomorphism remain external assumptions. The audit proves the result on these exact supplied records unconditionally, but does not generate or independently classify every graph isomorphism class. All-isomorphism-class language must retain this qualification.

## 4. At most one prescribed edge: valid elementary theorem

Let a finite simple triangle-free graph have cut complement M with at most one edge. If M is empty, its bipartition maps to the endpoints of a single cube edge.

Suppose M={uv} and put B=G-M. The original cut bipartitions B, and u,v have the same cut-side parity. If they lie in one B-component, their B-distance is even, nonzero and not two, since a two-edge B-path plus uv would be a triangle. Thus their distance is at least four. For a vertex w of this component, let d be its B-distance from u. Map distance levels 0,1,2,3,4 to 0,1,3,7,15 respectively; for d>4 map even levels to 15 and odd levels to 7. Adjacent vertices in a bipartite graph have distances from u of opposite parity and differing by at most one, hence exactly one. Consecutive displayed values differ by a unit, including the alternating tail. Therefore every B-edge maps to a cube edge, while u,v map to 0,15.

If u,v lie in different B-components, map the component of u to a single cube edge with u assigned 0 and the component of v to a single cube edge with v assigned 15. Map each remaining component to any cube edge, or an arbitrary vertex if isolated. The only M-edge receives difference J in either case. No degree restriction is used, and no assertion about two prescribed edges follows.

## 5. Controls, reproduction limits and required corrections

The ordinary-mode supplied Python example checks and the supplied seven-case certificate mutation suite replayed with byte-identical result files. A rebuilt optimized harness also tested the source C++ solver against five deterministic controls: forbidden unrestricted triangle; positive unrestricted pentagon; positive one-J pentagon; impossible one-J square; impossible three-J pentagon. All outcomes and returned positive witnesses were correct.

The audit's 30 adversarial checks covered wrong maxima, bad/range-invalid witnesses, omitted and duplicated cuts, wrong normalization, malformed integers, invalid counts, missing/extra records or fields, wrong order/count, empty and jointly truncated input, duplicate catalog records, and nonzero padding. These include intentionally successful demonstrations of weaknesses in the original bare checker, distinguished from rejection tests. The new example checker produced identical valid results in normal Python, `-O` and `-OO`, and rejected a corrupt witness in all three modes. The independently implemented closed-manifest checker passed 27 controls across those modes, rejecting incorrect external pins, changed bytes, missing/extra/duplicated members, unsafe paths and symlinks.

Required qualifications:

1. **Assertion elision.** The supplied Python validation and fetch checks use `assert`. Under `-O`, `-OO` or equivalent optimization configuration, these checks disappear. A deliberately corrupted unrestricted witness was rejected in normal mode but reported as passing under both optimized modes. The supplied ordinary-mode run is valid; optimized execution of those scripts must not be advertised as fail-closed. The new audit uses explicit exceptions instead.
2. **Whole-input binding.** The supplied bare C++ verifier correctly checks the records it is given but does not require a nonempty catalog, its advertised record count or a command-line declared order. Empty paired inputs and jointly truncated valid prefixes can therefore pass it. It also ignores unused graph6 padding bits. None of these issues affected the pinned genuine input. Binding exact byte hashes, full inventory, declared order/count and canonical padding closes those gaps; the new independent verifier enforces them.
3. **Reproduction destination.** The supplied shell reproduction script compares regenerated certificates with private reference certificates. A public edition that omits those references cannot run that script unchanged. A later reproduction workflow must either obtain the authorized private references or replace the byte-comparison step with pinned-input generation, pinned expected certificate hashes if required, and the independent exact semantic verification. This audit replayed the supplied certificate checking, not a fresh network download or full re-execution of historical discovery searches.
4. **Retained probes are not accepted coverage.** Auxiliary random-search logs, higher-order probes and the interrupted local order-14 stream are not a coverage proof. The interrupted stream contains 28 complete graph records and a partial 29th record with 13 of 16 promised maps. Its 379 complete positive witness blocks were checked, but the stream is not a passing whole-catalog certificate. A separate retained order-16 probe's unrestricted witness and stated maximum were checked as auxiliary facts only. Neither strengthens the accepted theorem or expands the coverage table. The specific historical local-search implementation that discovered the authored example is not retained; the explicit graph, proof and subsequent checks suffice to reproduce its mathematical content.
5. **Edition boundary.** This public edition contains the authored explicit graph as mathematical proof text, the full mathematical audit, acceptance scope and permitted public citations/hash metadata. Programs, imported graph6 inputs, certificate streams containing those inputs, raw search collections and private input/coordination identities are excluded. Historical packaging eligibility did not establish permission to distribute those materials. The edition manifest describes only the files actually distributed.

## 6. Sources and remaining questions

The public catalog source is [House of Graphs: Connected cubic graphs](https://houseofgraphs.org/Cubic). Dataset identity here is established by the pinned bytes and accompanying public URL/hash metadata; the source's completeness/nonisomorphism assertions are inherited.

The background citation is Matt DeVos and Robert Šámal, [High-girth cubic graphs are homomorphic to the Clebsch graph](https://iuuk.mff.cuni.cz/~samal/papers/clebsch/clebsch.pdf). It is not used as proof of the new fixed-cut computation or the explicit local obstruction. This audit does not authenticate a new manuscript status or establish novelty.

The finite positive evidence does not establish that every global maximum-cut complement extends in every triangle-free cubic graph. The local obstruction shows precisely why the weaker single-vertex condition alone cannot prove such a theorem. There is no counterexample to the original Weak pentagon target in this audited result, and no all-order proof of that target.
