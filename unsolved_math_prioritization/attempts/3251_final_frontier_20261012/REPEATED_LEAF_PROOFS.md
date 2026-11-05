Editorial note: This is the complete authored text. Only references to undistributed operational files, their identities, locations and replay directions have been replaced. All mathematical arguments, exact finite counts, corrections and limitations are retained. The public manifest identifies the actual distributed files.

# An odd-hole-free repeated-leaf obstruction with only one monochromatic boundary clique

## Exact scope

This is a separately frozen supplement within the fifth and final substantive pass for problem 3251 / ordered row 1753. It introduces no additional research pass. For every k>=4 it constructs an odd-hole-free, divisible graph with exact original high-incidence core X and a nonextendible coloring of X having exactly one monochromatic (k-1)-clique. Its unique effective signed-tree component is a five-node path with identical leaf boundaries. At k=4 the core has nine vertices; this does not resolve or exclude the eight-core boundary. No counterexample to the target conjecture, novelty, or minimality claim is made.

A division avoids monochromatic maximum-cardinality cliques. High incidence means membership in at least three original maximum cliques, not maximal cliques or cliques recomputed after deletion. The already frozen fifth-pass component-compression proof and the accepted fourth-pass propagation/tree proof are identified dependencies in the dependency identity record.

## Construction

Take four distinct low vertices z1,z2,z3,z4 inducing the diamond K4 minus z1z4. Take disjoint sets A,B1,B2,B3 of respective sizes k-1,k-2,k-2,k-2. Make each a clique. Join every vertex of A to z1,z4, and every vertex of Bi to zi,z(i+1), for i=1,2,3. No other edges occur between these blocks.

For each x in A attach one support k-clique containing x and k-1 new private vertices. For each x in B1 union B2 union B3 attach two such support k-cliques. All private vertices are fresh and have neighbors only within their support bag. The base graph before these supports has 4k-3 vertices; the full graph has 7k^2-16k+10 vertices. It is connected.

## Exact maximum cliques and core

The five base maximum cliques, in path order, are

    Q0=A+z1,
    Q1=B1+{z1,z2},
    Q2=B2+{z2,z3},
    Q3=B3+{z3,z4},
    Q4=A+z4.

Together with all support bags, these are exactly the maximum cliques and each has size k. Indeed, a clique using a support-private vertex lies in that support bag. A remaining clique using any Bi lies in Qi, since the two outside neighbors of Bi are adjacent. A clique using A lies in Q0 or Q4, because z1,z4 are nonadjacent. A clique using only low vertices has size at most three, strictly less than k. This also proves that no larger clique exists. The strict inequality is why k=3 is excluded: diamond triangles would then be additional maximum cliques.

Each A vertex lies in Q0,Q4 and its one support bag. Each Bi vertex lies in Qi and its two support bags. Thus every such vertex has incidence exactly three. Each zi lies in its two consecutive base bags and no support bag, so has incidence two. All private vertices have incidence one. Consequently

    X=A union B1 union B2 union B3,  |X|=4k-7.

The induced core is K_(k-1) disjoint from three copies of K_(k-2). It has exactly one clique of size k-1, namely A.

In the outside-X dual multigraph, the five base cliques form the path Q0-Q1-Q2-Q3-Q4. Every support bag is isolated and marked by its private vertices. The only unmarked component is therefore this path. Its two signed boundary unions are

    S=A union B2,  T=B1 union B3,

which are disjoint. A is repeated at both leaves on the same bipartition side. The two extra diamond edges z1z3 and z2z4 are actual graph edges but belong to no maximum clique; they must not be lost by a clique-shadow assumption.

## No induced odd hole

A support-private vertex is simplicial: its neighbors form its support clique minus itself. Such a vertex cannot lie on an induced cycle of length at least four. Delete all of them for the purpose of inspecting possible holes. Every Bi vertex is now simplicial, since its neighbors are the rest of Bi together with its adjacent low pair. Hence an induced cycle of length at least four can use no Bi vertex either.

The remaining graph is the diamond plus A, whose vertices are pairwise adjacent true twins with outside neighbors z1,z4. An induced cycle of length at least four can contain at most one A vertex: if it contained two, their equal external neighborhoods and adjacency would give a chord. It cannot contain no A vertex, because the diamond is chordal. With one A vertex a, its cycle neighbors must be z1,z4, and the rest of the cycle is an induced low-vertex path from z1 to z4. In the diamond every such induced path has two edges, through z2 or through z3. Both potential three-edge paths have a diamond chord. Thus every hole has length exactly four. In particular, the full graph is odd-hole-free. This proof concerns the actual graph, including both extra diamond edges, rather than its maximum-clique shadow.

## Nonextendible prescription and exact scope of the obstruction

Give A and B2 color 0, and B1 and B3 color 1. There is exactly one monochromatic (k-1)-clique in the core, namely A, and none of the opposite color. Nevertheless Q0 and Q4 force z1=z4=1; Q1 and Q3 then force z2=z3=0; Q2 is monochromatic. Thus the prescription cannot extend.

It follows that the following proposed sufficient conditions are false, even for odd-hole-free graphs:

- A prescribed exact-core coloring having only one monochromatic (k-1)-clique must extend.
- A graph-realizable matching tree cannot have two leaves with identical (k-1)-clique boundaries on the same side.

The original sufficient condition with NO monochromatic (k-1)-clique is unaffected. Nor is this a counterexample to a core-division extension heuristic at the core's own clique number: the prescription makes its maximum clique A monochromatic, and therefore is not a division of the induced core.

More precisely, the frozen component-compression theorem gives that exactly two assignments on X fail: S all 0,T all 1 and its complement. All other 2^(4k-7)-2 assignments extend. This exact count is an all-size consequence of the pinned theorem, not a count inferred from the finite checks below.

The whole graph has a direct division: give both colors to each of A,B1,B2,B3, possible because k>=4, and color the four low vertices arbitrarily. Every base maximum clique then contains a mixed block. In each support bag choose one private vertex opposite its core attachment's color. Every support bag is mixed as well.

For k=4, the full graph has 58 vertices, 20 maximum cliques, and nine core vertices. The nine-core example does not settle whether the eight-core k=4 frontier is possible, nor whether every odd-hole-free graph is divisible.

## Verification, scope and integrity

The bounded checker uses k=4,5,6,7. It builds adjacency independently of the maximum-clique oracle, reconstructs the complete maximum-clique family by Bron-Kerbosch, checks the exact high-incidence core, checks the successive simplicial removals used in the all-size hole proof, verifies the unique core maximum clique, and tries all sixteen assignments to the four low vertices under the obstructed prescription. For k=4 and k=5 it also exhausts every odd vertex subset of the base graph of size at least five, respectively 3,797 and 64,839 subsets, finding no induced odd holes. At k=6,7 no exhaustive odd-subset search is claimed; the all-size argument and verified simplicial reduction apply. These are four specific family members, not all graphs of their orders.

Mandatory external-pin, manifest, complete-inventory, nonsymlink-path, exact-byte/hash, fixed-scope and duplicate-key gates are in the original checker. No acceptance gate uses assert. The final normal/-O/-OO runs and disposable-copy rejection controls are recorded externally. This certifies the declared static snapshot and tested failure modes, not concurrent hostile-race protection or replacement of every trust anchor. No frozen prior file, queue, repository, or remote is changed.
