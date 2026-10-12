# Five arbitrary exceptional lists in degrees at least four

Authored 12 October 2026 UTC. This is a restricted near-constant-list theorem, with a self-contained elementary proof. It does not resolve the unrestricted conjecture and makes no novelty claim.

## Theorem and setting

Let G be a finite simple graph of maximum degree Δ≥4. Assume G is not Δ-edge-colorable and G−e is Δ-edge-colorable for every edge e. Let every list L(e) have exactly Δ colors. If L is nonconstant and differs from some Δ-element palette A on at most five edges, then G has a proper L-edge-coloring.

Write X={e:L(e)≠A}, O(e)=L(e)\A, and d(e)=|O(e)|. The accepted [four-exception theorem](../3200_critical_list_partials_20261012/FOUR_EXCEPTIONS.md) handles |X|≤4, so assume |X|=5. A five-edge star support is covered by the accepted [arbitrary-star theorem](../3200_critical_list_partials_20261012/NEAR_CONSTANT.md). All remaining work is supplied below.

The elementary exterior-completion rule is as follows. If a nonempty F⊆X is properly colored from O and the residual sum ∑(e∈X\F)d(e) is less than Δ, ordinarily Δ-color G−F by restricting a coloring of G−f for any f∈F. A uniformly random permutation of its labels into A violates each residual list with probability d(e)/Δ. The union bound is strictly less than one, so a successful permutation exists. Its A-colored edges combine properly with the exterior-colored F.

We prove a stronger, degree-independent partial-coloring lemma that always leaves residual sum at most four, with a useful incidence condition in the equality case.

## 1. Elementary small-graph facts

All graphs in this section are vertex graphs; subsequently they will be line graphs of exceptional edges.

1. A noncomplete graph on four vertices is 2-degenerate, and hence colorable from arbitrary lists of size at least three. A noncomplete graph on five vertices is 3-degenerate, and hence colorable from arbitrary lists of size at least four. Repeatedly remove a vertex whose degree is smaller than its list size, and restore vertices in reverse order.
2. Three lists of sizes at least 2,2,3 have distinct representatives: choose distinct representatives for the first two, then a different representative for the third. Therefore they properly color any three-vertex graph. A nontriangle on three vertices is a forest, and is colorable from lists of size at least two. A nontriangle with list lower bounds 1,2,2 is also colorable: color its singleton-list vertex first, root its tree component there, and color the other vertices outward; other components cause no problem.
3. A triangle-free graph on at most four vertices is a forest or a four-cycle, and is colorable from lists of size at least two. For the four-cycle, reduce to two-element lists. If all four lists coincide, alternate the two colors. Otherwise choose adjacent vertices v,w with a color in L(v)\L(w). Give v that color and greedily traverse the cycle in the direction that reaches w last. The initial color cannot forbid a color at w, so its final choice avoids at most one color.

**Four-vertex lemma.** A noncomplete graph on four vertices is colorable from lists of sizes at least 2,2,3,3, in any placement of the lower bounds.

Let x,y be the vertices with lower bound two, and p,q the other two. If x,y are adjacent, a missing graph edge has at least one endpoint among p,q. That endpoint has degree at most two and can be removed. The other three vertices have lower bounds 2,2,3, so they can be assigned distinct colors; restore the removed vertex from its list of size at least three.

If x,y are not adjacent, reduce their lists to two elements and those of p,q to three. There are at least three possible unordered pairs of distinct representatives of L(p),L(q). Indeed, fixing a∈L(p) gives at least two such pairs containing a; also choose a'∈L(p)\{a} and b'∈L(q)\{a,a'}, giving a pair not containing a. At most two of these unordered pairs equal one of the two lists L(x),L(y). Choose a pair that equals neither, and use its distinct representatives on p,q. Each of x,y still has an available color. They are nonadjacent, so their choices can coincide. This colors a supergraph of any required incidences and proves the lemma.

**Triangle-transversal lemma.** Every K4-free graph on at most five vertices has a vertex whose deletion leaves a triangle-free graph, provided it has at least one vertex.

If there are no triangles, any vertex works; if there is only one, choose one of its vertices. If two triangles share exactly one vertex v, they occupy all five vertices. Vertex v is adjacent to every other vertex. Any triangle avoiding v would therefore form a K4 together with v, which is impossible. Thus every triangle contains v.

Otherwise every two distinct triangles share an edge, because two disjoint triangles require six vertices. Write two of them as abc and abd. A triangle avoiding a must share two vertices with each of these triangles, so it must be bcd. The resulting edges form a K4 on a,b,c,d, a contradiction. Thus every triangle contains a. This proves the lemma.

## 2. The support structure

Let H be the line graph of the five-edge support X: its vertices are the five exceptional edges, adjacent precisely when the corresponding edges of G meet.

Four pairwise incident edges in a simple graph must share one endpoint. To see this, start with uv and uw. Any edge meeting both but avoiding u is vw; an additional edge meeting all three would have to be one of those three edges. Thus a pairwise-incident family of at least four edges is a star.

We have excluded the case where all five exceptional edges form a star. Therefore H≠K5. Moreover, if H contains a four-vertex clique C, the corresponding four edges share a center, and the fifth edge z avoids that center. It can meet at most two of those four edges, one at each endpoint. Hence

    every K4 in H has its remaining vertex adjacent to at most two clique vertices.  (S)

In particular, H cannot contain K5 with only one edge removed.

## 3. Universal five-edge partial-coloring lemma

**Lemma.** Let X be five edges of a finite simple graph that do not all share an endpoint. Give each edge an arbitrary nonempty finite exterior list O(e), and let d(e)=|O(e)|. There is a nonempty F⊆X properly colorable from O such that either

- ∑(e∈X\F)d(e)≤3; or
- X\F consists of two incident edges, each having deficit two.

This is a combinatorial assertion about the five exceptional edges alone; criticality and the base palette are not used.

**Reduction to deficits at most four.** Replace each O(e) by an arbitrary subset of size a(e)=min(d(e),4). It suffices to prove the lemma for these reduced lists, with weights a. In either asserted outcome, every vertex with a(e)=4 is selected in F. Therefore every residual edge has d(e)=a(e), and the same certificate proves the original assertion. From now on write d for the reduced weights, all in {1,2,3,4}.

Call an edge large if d(e)≥2, and let h be the number of large edges.

### At most three large edges

- h=0: H≠K5 has two nonadjacent vertices. Color those two edges arbitrarily from their exterior lists. Three unit deficits remain.
- h=1: exterior-color the unique large edge and one unit-deficit edge. Color the latter first; the large edge can avoid that color if necessary. Three unit deficits remain.
- h=2: exterior-color the two large edges with distinct colors if needed. Three unit deficits remain.
- h=3 with some deficit at least three: the three large edges have lower bounds 2,2,3, so exterior-color all three. Two unit deficits remain.
- h=3 with all large deficits two: choose two large edges and one unit-deficit edge that do not form a triangle in H. Such a choice exists. Otherwise the three large vertices form a clique and each of the two unit-deficit vertices is adjacent to all three, contradicting (S). Their bounds 2,2,1 color this nontriangle. One deficit-two edge and one unit-deficit edge remain, of total three.

### Four large edges

- If both deficit two and a deficit at least three occur among the large edges, leave one deficit-two edge and exterior-color the other three large edges, using bounds 2,2,3. Together with the uncolored unit edge, the residual total is three.
- If all four large deficits are two and their induced graph is not K4, select a nonadjacent pair and any third large vertex. This nontriangle is exterior-colorable from two-element lists, leaving total deficit 2+1=3.
- If all four large deficits are two and induce K4, call the unit edge z. By (S), at least two clique edges are nonadjacent to z. Exterior-color z and two such clique edges, using distinct colors for the clique pair. The residual pair is incident and has deficits two and two. This is the lemma's second outcome.
- If all four large deficits are at least three and their induced graph is not K4, exterior-color all four by 2-degeneracy. The sole residual deficit is one.
- If these four vertices form K4 and some has deficit three, leave such a vertex. Color the unit edge z first. Of the three selected clique edges, at most two are adjacent to z, so their remaining exterior-list sizes are at least 2,2,3. Assign distinct colors to them. The residual deficit is three.
- Finally, if those four clique deficits are all four, color z first. The four remaining clique lists have lower bounds 3,3,4,4. In this increasing order, choose four distinct colors greedily. All five vertices are exterior-colored.

### Five large edges, with H K4-free

Every deficit is now at least two.

If all deficits are at most three, choose a triangle-transversal vertex v from Section 1. The graph H−v is triangle-free on four vertices and is exterior-colorable from the lists of size at least two. The residual deficit d(v) is at most three.

Otherwise let q be the number of deficit-four vertices.

- q=1: let u be the unique deficit-four vertex. The K4-free graph H−u on four vertices has a triangle-transversal vertex v. Color the three vertices of H−{u,v}, which form a forest, from their lists of size at least two. Restore u from its four-element list, avoiding at most three colors. Leave only v, whose deficit is at most three.
- 2≤q≤4: leave any vertex v of deficit at most three. Among the other four vertices, color the at most two vertices with deficits below four first, choosing different colors if they are adjacent. Then color the deficit-four vertices one at a time. Each avoids at most three already used neighbor colors. The residual deficit is at most three.
- q=5: H≠K5 is 3-degenerate, so exterior-color all five vertices from their four-element lists.

### Five large edges, with a four-vertex clique C

Let z be the fifth vertex and let s be the number of deficit-two vertices in C. Recall that z has at most two neighbors in C and d(z)≥2.

- s=0: all clique deficits are at least three. If one equals three, leave it, color z first, and color the other three clique vertices from remaining lists of sizes at least 2,2,3. If all four clique deficits are four, color z first and then use the lower bounds 3,3,4,4 for four distinct clique colors. The residual sum is respectively three or zero.
- s=1 or s=2: leave a deficit-two clique vertex. The remaining four-vertex graph is not complete, by (S), and its list lower bounds are at least 2,2,3,3. The four-vertex lemma exterior-colors it. The residual deficit is two.
- s=3: C has one vertex of deficit at least three. If z has a deficit-two neighbor in C, leave one such neighbor; otherwise leave any deficit-two clique vertex. Among the three remaining clique vertices, the lower bounds are 2,2,3, so assign distinct colors to them. By the choice of the omitted vertex and (S), z has at most one neighbor among those three. Its list has at least two colors, so restore z. The residual deficit is two.
- s=4: exterior-color z and two clique vertices nonadjacent to z, choosing distinct colors for the clique pair. The residual pair is incident and has deficits two and two.

These cases exhaust the reduced deficit assignments and prove the lemma. ∎

## 4. Completion of the theorem

Apply the partial-coloring lemma to the nonstar exceptional support.

If the residual total is at most three, it is strictly less than Δ≥4, and the exterior-completion rule gives an L-edge-coloring.

In the remaining case, precisely two residual exceptional edges e,f are incident, and d(e)=d(f)=2. If Δ≥5, the residual total four is already strictly below Δ.

Suppose Δ=4. In any ordinary four-edge-coloring of G−F, the incident edges e,f have distinct ordinary labels i,j. Their allowed sets A∩L(e), A∩L(f) each have two elements. Choose different representatives for these two sets, map i,j to those representatives, and extend this partial map to a permutation of all four labels onto A. Every other edge of G−F has the full list A. The permuted ordinary coloring respects every residual list and combines with the exterior coloring. Thus the assignment is colorable also at Δ=4. ∎

Together with the accepted four-exception and star theorems, this proves the stated at-most-five result in every degree at least four. The separate subcubic problem is outside this packet.

## 5. Exact checks and scope

The proof is symbolic; the checks are independent safeguards rather than unreported enumeration dependencies.

- An endpoint-partition generator exhausts simple five-edge supports, obtaining 24 line-graph types. Exactly one is K5, corresponding to five pairwise incident edges; the other 23 satisfy (S).
- For all 23×4^5=23,552 ordered reduced deficit profiles, a checker finds a certificate consisting of a greedy exterior-colorable subset, a two-list-colorable forest/four-cycle subset, or one of those subsets with an incident deficit-two residual pair.
- Before the forest/four-cycle and incident-pair refinements, the greedy strict-residual test alone leaves exactly 14 ordered profiles. Twelve occur on K4 plus a vertex with zero, one, or two clique neighbors, with all four clique deficits two and fifth deficit 1,2,3,4. The other two occur on W5=K1 joined to C4, with rim deficits two and hub deficit two or three. The first twelve admit the incident-pair certificate; the latter two admit the even-rim certificate.
- A separately implemented clique-partition support generator and explicit permutation-of-coloring-order verifier reproduce the support set and the full certificate outcome.
- All 432 cases of two distinct ordinary labels and two allowed two-subsets of a four-palette admit a palette permutation; exhaustive checking verifies the final Hall step.

No failed sufficient-method test is called an uncolorable list assignment. The unrestricted nonconstant-list conjecture and every historical-priority claim remain outside this theorem.

## Sources and inputs

The accepted near-constant-list packet supplies the four-exception and arbitrary-star theorems; the exterior-completion rule was reproved above. The original problem can be consulted at https://www.sfu.ca/~mohar/Problems/P7ListEdgeCriticalGraphs.html and its intended formulation at https://www.openproblemgarden.org/op/list_colorings_of_edge_critical_graphs. These links identify the problem, not external proofs of the present restricted theorem. All new mathematical arguments needed here are given in full.
