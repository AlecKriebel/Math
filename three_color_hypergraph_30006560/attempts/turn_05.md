# Attempt 5: Complementary shadows and the first three dimensions

Verdict: the conjectured inequality is proved for hypergraphs whose active vertex set has at most r+2 vertices, as well as a complementary-dimension/count regime. The unrestricted problem remains unresolved after five substantive attempts. No claim of novelty is made for these elementary restricted cases.

## An exact dual description

Delete isolated vertices; no successful S uses one, since S is the union of any two differently colored faces. Let n be the number of remaining vertices. If n<r then T=0. Otherwise put d=n−r+1. Replace each hyperedge e by its complement V\e, a d-set, preserving its color. The resulting families F_R,F_G,F_B are pairwise disjoint and have sizes R,G,B.

For a family F of d-sets, let ∂F be its family of (d−1)-subsets. Complementation sends a successful r-set S to Q=V\S, with |Q|=d−1. The condition e⊆S is exactly Q⊆V\e. Hence

T = |∂F_R ∩ ∂F_G ∩ ∂F_B|.                                (12)

Each d-set has d faces, so T≤d min(R,G,B). For sorted positive color counts a≤b≤c, this gives

T²≤d²a²≤2abc whenever d²a≤2bc.                             (13)

In particular this proves the target whenever a≥d²/2, since bc≥a². This complements Attempt 1's small-a and highly unbalanced regimes.

For d=1 the common shadow has at most one member, the empty set, so T≤1. For d=2, (13) handles a≥2, and Attempt 1 handles a≤2. Thus n≤r+1 is settled. The remaining work is d=3, where the colored families consist of triples and their shadows are ordinary graph edges.

## Lemma: two disjoint three-triple families have at most seven common pairs

Let F and G each consist of three distinct triples, with F∩G empty. Suppose their pair shadows had at least eight common pairs. Choose a set P of eight such pairs.

Count pairs with multiplicity in each family. Each family has nine pair incidences, so its pair-incidence multigraph is P plus a single extra pair, say e_F or e_G. Each vertex has even degree in either pair-incidence multigraph, since each triangle contributes degree two at each of its vertices. It follows that the odd-degree vertices of the ordinary graph P are exactly the endpoints of e_F, and also exactly the endpoints of e_G. Therefore e_F=e_G, and F and G have identical pair-incidence multisets.

We now show that two disjoint three-triple families cannot have the same pair-incidence multiset. If a vertex appears in exactly one triple {v,x,y} of F, it has pair-incidence degree two, with neighbors x and y. Its occurrences in G must therefore also consist of that same triple, contradicting disjointness. Consequently every vertex in the union appears in at least two triples of F. Since F has nine vertex incidences, at most four vertices are used. But at most four distinct triples exist on four vertices, whereas F∪G has six distinct triples. This contradiction proves

|∂F ∩ ∂G|≤7.                                               (14)

This is a direct small-trade argument; it is not based on finite enumeration.

## Lemma: three disjoint four-triple families have at most eleven common pairs

Suppose F_R,F_G,F_B each have four triples and their common pair shadow has at least twelve members. Each family has exactly twelve pair incidences, so all three must cover exactly the same set P of twelve distinct pairs, without repetition. Thus P is a simple graph with a triangle decomposition into four triangles in each of the three colors.

Every nonisolated vertex of P has positive even degree. A vertex of degree two forces the triangle containing that vertex and its two neighbors in every decomposition, contrary to the disjointness of the three triple families. All nonisolated degrees are therefore at least four.

The degree sum is 24, so P has at most six nonisolated vertices. Twelve edges require at least six vertices, because five vertices support at most ten edges. Hence P has exactly six vertices, all of degree four. Its complement on those six vertices is a perfect matching, so P is the complete tripartite graph with parts of size two. Every triangle chooses one vertex from each part; there are exactly 2³=8 triangles. The three disjoint families would require twelve distinct triangles, a contradiction. Therefore

|∂F_R ∩ ∂F_G ∩ ∂F_B|≤11.                                 (15)

## Completion of d=3

Let a≤b≤c be the color counts. Counts a≤2 were already settled by Attempt 1. If bc≥9a/2, (13) applies. If neither condition holds, the only possibilities are

(a,b,c)=(3,3,3), (3,3,4), or (4,4,4).

Indeed a≥5 implies bc≥a²≥9a/2. For a=3, bc<13.5 forces b=3 and c∈{3,4}; for a=4, bc<18 forces b=c=4.

In the first two cases, apply (14) to the two three-triple families: T≤7, so T²≤49≤2abc. In the final case, (15) gives T≤11 and T²≤121<128=2abc. This exhausts every d=3 case.

Thus T²≤2RGB whenever n≤r+2. Since n is the active-vertex count, the result is unchanged by adjoining any number of isolated vertices.

## Final scope and what is still missing

Combining this result with the block decomposition in Attempt 2 proves the inequality whenever every intersection-connected hyperedge block, considered on its own active vertex set, has at most r+2 vertices. Common-core blocks are also covered independently by the known graph theorem, even when their vertex sets are larger.

For an unresolved block with n≥r+3, the complementary dimension is d≥4. The elementary bounds settle ab≤2c or d²a≤2bc. Outside these regimes, the common-(d−1)-shadow inequality

|∂F_R ∩ ∂F_G ∩ ∂F_B|² ≤ 2 |F_R||F_G||F_B|

is still unproved here. The d=3 proof depends on triangle-decomposition parity and the impossibility of very small disjoint trades; no argument extending those constraints to arbitrary d has been obtained. The five-turn outcome is partial progress, not a proof or counterexample for OWR Question 8 in full generality.
