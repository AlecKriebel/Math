# Five exceptional lists: a cycle theorem and sharp method boundaries

Research round two, 12 October 2026 UTC. This packet is separate from the accepted first-round packet. It proves restricted five-exception results, not the unrestricted five-exception assertion and not Mohar's full conjecture. No novelty claim is made.

## Setting and accepted input

G is a finite simple graph with maximum degree Δ, is not Δ-edge-colorable, and G−e is Δ-edge-colorable for every edge e. Every list L(e) has exactly Δ colors. Fix a Δ-set A, let X={e:L(e)≠A}, and put O(e)=L(e)\A and d(e)=|O(e)|=|A\L(e)|. Only nonconstant assignments are under consideration.

The accepted first-round strict-deficit theorem will be used: if a nonempty F⊆X has a proper edge coloring from O(f), and Σ_{e∈X\F}d(e)<Δ, then L is colorable. For completeness, take an ordinary Δ-coloring of G−F, randomly permute its labels onto A, and apply the union bound: the chance of any remaining list violation is at most Δ^{-1}Σd(e)<1. Combine a successful permutation with the exterior coloring of F. Existence of the ordinary coloring follows by restricting a Δ-coloring of G−f for any f∈F.

The first round also proves all nonconstant assignments with at most four exceptional edges and the full Δ=2 case. Those results have been independently audited, with explicit nonconstant qualifications. Here the new universal cycle theorem is for Δ=3 and exactly five exceptional edges forming a 5-cycle.

## 1. Equality in the three-unit-deficit permutation test

**Lemma.** Let A have three colors. Suppose exactly three remaining exceptional edges each omit one color a_j∈A, and have ordinary labels i_j∈{1,2,3}. A permutation π of the ordinary labels onto A avoiding π(i_j)=a_j for all j exists unless one of the following holds:

- All three labels i_j are equal, and the three omitted colors a_j are pairwise distinct.
- The three labels i_j are pairwise distinct, and all three omitted colors a_j are equal.

Each displayed configuration really blocks every permutation.

**Proof.** Each constraint removes one cell (i_j,a_j) from the 3-by-3 bipartite graph of possible label-to-color assignments. Repeated constraints remove only one cell, so there are at most three removed cells. If no perfect matching remains, Hall gives a set I of labels whose allowed colors number fewer than |I|.

If |I|=1, its only row is completely removed. This needs all three distinct removed cells in the same row, giving the first configuration. If |I|=2, each of its two rows allows at most the same single color, requiring at least four distinct removed cells, impossible. If |I|=3, at least one column is completely removed, giving the second configuration. Conversely a removed row or column prevents a perfect matching. ∎

This classification concerns a chosen ordinary coloring; it is not a classification of bad list assignments.

## 2. Five one-color substitutions with different omitted colors

**Theorem.** Suppose Δ=3, |X|=5, and every exceptional list is obtained from A by one replacement. If the omitted colors a_e∈A are not all equal, then G is L-edge-colorable. The exterior colors may coincide or differ arbitrarily.

**Proof.** If the exceptional support has a matching of size three, exterior-color those three edges and apply the strict-deficit theorem, leaving two unit deficits. Otherwise its matching number is two. Indeed five edges in a simple subcubic graph cannot all be pairwise incident, so a two-edge matching exists.

For every e∈X, the four edges X\{e} contain a disjoint pair: a pairwise-incident four-edge family in a simple graph would form a four-edge star, which is impossible at maximum degree three. Therefore the complements in X of two-edge matchings cover X. Every two such complements are three-element subsets of a five-element set, so they intersect.

If each complement triple had a constant omitted color, the intersection property would force the same color on every triple, and the covering property would then force every a_e to be equal. This contradicts the hypothesis. Thus some two-edge matching F has a complement R=X\F whose omitted colors are not all equal.

Exterior-color F arbitrarily, which is proper because F is a matching. Fix any ordinary 3-coloring of G−F. The three edges of R cannot all receive the same ordinary label: that would make them a three-edge matching in X. Their omitted colors are also not all equal. Neither obstruction in Section 1 can occur, so a palette permutation respects their lists. All other edges outside F have list A; the exterior palette on F is disjoint from A. The resulting full coloring is proper and respects L. ∎

This result applies to arbitrary five-edge supports. For Δ≥4, five one-color substitutions were already covered by the accepted Δ+1-substitution theorem. The new content here is the additional subcubic equality case with nonconstant omitted colors.

## 3. A five-boundary-color lemma

Let q_0,…,q_4 be any cyclic word of length five on a set of three labels. Indices below are modulo five.

**Lemma.** There is a position u, with a=q_u, such that:

1. If q_{u−1} and q_{u+1} are both different from a, then they are different from each other.
2. If q_{u+2} and q_{u+3} are both different from a, then they are equal to each other.

**Proof.** Classify the multiplicities of the labels, omitting zero counts.

- Multiplicities 5 or 4+1: choose a most frequent label a and any position u carrying it. At most one position has another label, so both conditions are immediate.
- Multiplicities 3+2: let a be the label occurring three times. Choose an a-position whose two neighbors are not both the other label. Such a position exists: otherwise the three a-positions would require six incidences to the two other positions, which have only four incidences in the cycle. Condition 1 follows by this choice. Condition 2 holds because all non-a labels are the same.
- Multiplicities 3+1+1: choose a as the label occurring three times, and call the others b,c. Condition 1 is automatic, since two non-a neighbors must be the distinct singleton labels. Condition 2 can fail only if the edge between positions u+2 and u+3 is the edge joining b to c. There is at most one such u: the map from u to this opposite edge is a bijection between the five positions and the five cycle edges. Choose one of the three a-positions other than this possible forbidden position.
- Multiplicities 2+2+1: let v be the position carrying the singleton label c, choose a neighbor u of v, and put a=q_u. The other label occurring twice is b. Of the two neighbors of u, one is c; if the other is not a, it is b, so condition 1 holds. The opposite edge at positions u+2,u+3 does not contain v. Its labels are therefore only a and b. If neither is a, both are b, proving condition 2.

These are all partitions of five into at most three positive parts. ∎

## 4. Uniform one-color replacement on a 5-cycle

**Proposition.** Suppose Δ=3, the five exceptional edges form a cycle C=v_0v_1v_2v_3v_4v_0, and all five have the same list B=(A\{a_0})∪{x}, where a_0∈A and x∉A. Then G has a proper L-edge-coloring.

**Proof.** Properly 3-edge-color G−E(C) with ordinary labels 1,2,3. Such a coloring exists by criticality and restriction. Since G is subcubic, at each cycle vertex v_i there is at most one incident edge outside C. Let q_i be its ordinary label when that edge exists. When no such edge exists, assign q_i any of the three labels; treating it as a forbidden boundary label only adds a restriction and will not invalidate a coloring that avoids it.

Choose u and a=q_u from Section 3. Globally relabel the ordinary coloring so that label a becomes a_0, and the other two labels become the two colors b_0,c_0 of A\{a_0}. Rotate the cycle indexing so u=0. The two boundary conditions are preserved under this bijection.

Color cycle edges v_1v_2 and v_3v_4 with x. They are disjoint, so this creates no conflict. No edge outside C uses x.

The remaining edges v_4v_0 and v_0v_1 form a two-edge path. Assign b_0 and c_0 to them in opposite orders so as to avoid the boundary colors at v_4 and v_1 whenever those colors belong to {b_0,c_0}. Such an order exists: if both endpoints impose restrictions, condition 1 says their boundary colors are different; if just one imposes a restriction, choose the order accordingly; if neither does, either order works. At v_0 the boundary color is a_0, which differs from both path colors.

Finally color v_2v_3 with a color in {b_0,c_0} avoiding the boundary colors at its endpoints. Condition 2 guarantees that at most one distinct member of {b_0,c_0} is forbidden there. Thus a choice exists.

All five cycle colors lie in B, and every adjacent pair is different: x separates the two retained-color components, and the two path edges have opposite colors. Boundary conflicts were explicitly avoided, and all edges off C retain a proper coloring from A. This is a full proper L-edge-coloring. ∎

Only ordinary colorability of G−E(C), subcubic degree, and the two-palette hypothesis were needed in this proposition. The proof does not assume that an arbitrary preselected coloring of G−F can be repaired by a global permutation.

## 5. Arbitrary exceptional lists on a 5-cycle

**Theorem.** Suppose Δ=3 and X is the edge set of a 5-cycle. Then G has a proper L-edge-coloring for every choice of the five exceptional three-element lists.

**Proof.** Call an exceptional edge large when d(e)≥2, and let h be the number of large edges. The adjacency graph of the five cycle edges is itself C5. Every proper induced subgraph is a forest with maximum degree at most two.

If h>0, we always construct a proper exterior-colored set with residual deficit less than three:

- h=1: choose the large edge, one of its neighbors in the exceptional line cycle, and the position at distance two from that neighbor that is nonadjacent to both selected positions. In cyclic indices with the large edge at position 0, use positions {0,1,3}. The latter two small edges are nonadjacent. Color them arbitrarily, and color the large edge avoiding the color at position 1; it has at least two choices and is nonadjacent to position 3. The two remaining edges have unit deficits.
- h=2: choose the two large edges and any one small edge. Their adjacency graph is a forest on three vertices. Color the small edge first, then root its component there and greedily color the large edges; any other component also colors greedily. Each large edge has at least two outside colors and at most one already colored neighbor in this ordering. The residual deficits are 1+1.
- h=3: exterior-color the three large edges from their lists of size at least two, using their induced forest. Two unit deficits remain.
- h=4: exterior-color the four large edges, which induce a path, from their lists of size at least two. One unit deficit remains.
- h=5: if some deficit equals two, leave that edge uncolored and exterior-color the remaining four-edge path from lists of size at least two; residual deficit is two. If every deficit is three, exterior-color the entire cycle greedily from its lists of size three; every edge has at most two neighbors. Residual deficit is zero.

The strict-deficit theorem completes all these cases.

Now suppose h=0, so each outside list is a singleton {x_e}. If the exterior colors x_e are nonconstant around C, form a conflict graph on the five edges by retaining a cycle adjacency only when its endpoints have the same exterior color. This is a proper subgraph of C5, hence a forest and bipartite. One bipartition class has at least three vertices. The corresponding exceptional edges can all be exterior-colored simultaneously: any adjacent pair with different exterior colors is harmless, and a same-color adjacency would have been an edge of the conflict graph. Choose three of them. Only two unit deficits remain, so the strict-deficit theorem applies.

It remains that all outside colors equal one color x. If the omitted colors in A are nonconstant, Section 2 applies. If they are constant, all five lists are the same B=(A\{a_0})∪{x}, and Section 4 applies. This exhausts every list assignment on the five exceptional cycle edges. ∎

Assignments with fewer exceptional edges contained in a 5-cycle are already covered by the first-round four-exception theorem. Thus the natural at-most-five cycle-supported formulation also holds.

## 6. Sharp limitations of the strict-deficit and fixed-coloring methods

The five-cycle uniform case shows why the first-round strict-deficit construction cannot alone establish the new theorem.

Let Δ=3, let X=E(C5), and give every exceptional edge the list B=(A\{a_0})∪{x}. An exterior-colored set F⊆X must be a matching, because every exterior list is the same singleton {x}. Hence |F|≤2. Its residual deficit is

Σ_{e∈X\F}d(e)=5−|F|≥3=Δ.

Therefore **no choice of F has a strict-deficit certificate**, even though Section 4 proves the full assignment colorable. This sharp threshold occurs at five exceptions: the independently accepted four-exception theorem supplied a strict-deficit certificate for every subcubic four-exception case, with no star fallback needed at Δ=3.

Here is a concrete additional fixed-coloring failure inside an actual critical graph. Let

E(G)=[04,41,02,03,12,13,23],

indexed 0,…,6 in this order. This is K4 with edge 01 subdivided once. It has five vertices and seven edges. Each color class is a matching of size at most two, so it is not 3-edge-colorable. Its criticality can be checked explicitly. Swapping vertices 0 and 1 and swapping vertices 2 and 3 partition the edges into three deletion types. The following partitions into three matchings give ordinary three-edge-colorings for representatives:

- Delete 04: {41,23}, {03,12}, {02,13}.
- Delete 02: {04,13}, {41,23}, {03,12}.
- Delete 23: {04,13}, {41,02}, {03,12}.

These automorphisms cover all seven edge deletions.

Take A={0,1,2}, put B={0,1,3} on X={e0,e1,e3,e4,e6}, the 5-cycle 0,4,1,2,3,0, and put A on e2,e5. Choose the maximum exterior matching F={e3,e4}, with both edges colored 3. One proper ordinary coloring of G−F is

φ(e0)=0, φ(e1)=1, φ(e2)=1, φ(e5)=0, φ(e6)=2.

The remaining exceptional edges e0,e1,e6 have all three ordinary labels, but each forbids the base color 2. Every global label permutation maps one of those labels to 2, so none repairs this chosen ordinary coloring.

The same assignment is colorable, for example by the full color sequence

(e0,e1,e2,e3,e4,e5,e6)=(0,1,1,3,3,2,0).

Thus the example is neither a counterexample to the conjecture nor a failure of every ordinary coloring for that exterior set. It shows that an arbitrary deletion coloring may need to be replaced or structurally chosen.

## 7. Why unrestricted exterior-plus-permutation failure would be stronger

**Observation.** For any fixed A in the target setting, existence of an exterior-plus-permutation completion when both F and the ordinary coloring are unrestricted is equivalent to L-edge-colorability.

One direction is the construction itself. Conversely, from any full proper L-edge-coloring, let F be exactly the edges colored outside A. This set is nonempty, because otherwise G would be properly colored using only the Δ colors of A. The restriction to F is a proper exterior coloring. The restriction to G−F is a proper coloring from A; label those A colors by 1,…,Δ and take the corresponding permutation back to A. This realizes the full coloring as an exterior-plus-permutation completion.

Consequently the sharp obstructions in Section 6 are carefully scoped to the strict-deficit certificate or a specified ordinary coloring. Claiming failure for all F and all ordinary colorings would be a genuine bad-list counterexample, which this packet does not provide.

## Residual question

The assertion for five arbitrary exceptional edges of an arbitrary support is not proved here. The new theorem fully handles a 5-cycle support at Δ=3, and the omitted-color theorem handles an additional family of arbitrary supports. Other five-edge supports with arbitrary deficits remain outside these arguments. The global conjecture remains unresolved in this work.

## Sources and credit

- Mohar's original problem: https://www.sfu.ca/~mohar/Problems/P7ListEdgeCriticalGraphs.html
- Intended OPG formulation: https://www.openproblemgarden.org/op/list_colorings_of_edge_critical_graphs
- Kaul–Mudrock, *Criticality, The List Color Function, and List Coloring the Cartesian Product of Graphs*, arXiv:1805.02147v2, Conjecture 6, printed p.11: https://arxiv.org/pdf/1805.02147v2

These primary sources specify the problem and its line-graph formulation; they are not cited as proofs of the new restricted statements. The July 2001 reversed equivalence and the later compressed criticality definition are handled using the explicit operational hypotheses above. The accepted first-round mathematical packet supplies the stated strict-deficit and four-exception inputs: see [NEAR_CONSTANT.md](../3200_critical_list_partials_20261012/NEAR_CONSTANT.md) and [FOUR_EXCEPTIONS.md](../3200_critical_list_partials_20261012/FOUR_EXCEPTIONS.md). Every new argument in this round is given in full, with no claim of historical priority.
