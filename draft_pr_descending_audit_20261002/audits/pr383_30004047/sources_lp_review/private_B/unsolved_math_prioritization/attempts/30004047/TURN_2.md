# Author turn 2: the rank-two first-incidence theorem

## 1. Statement and exact scope

Consider a finite mono-constrained weighted graph, with positive vertex weights alpha on A, beta on B, gamma on C, each summing to one. Thus every a sees beta-weight at least x, and every b sees gamma-weight at least y. Assume, additionally, that **each b is adjacent to at most two A-vertices**. The count concerns positive-weight A-types, not the total weight of the neighborhood. Zero-weight types can first be deleted.

**Theorem.** If every c reaches A-weight strictly less than 1/2, then

    x<=2/5, and, if x>1/3, necessarily y<=1/4.                    (1)

Consequently a c reaches at least half the A-weight whenever either

- x>2/5 and y>0; or
- x>1/3 and y>1/4.

In particular the source's one-third diagonal assertion holds in this rank-two class. This is a restricted-incidence theorem; general middle vertices can have three or more positive-weight A-neighbors. The theorem does not prove the unrestricted integer-k assertion.

## 2. Immediate consequences of a putative counterexample

Write S_b=N_A(b). Every b has a positive-weight C-neighbor because y>0. Hence

    alpha(S_b)<1/2.                                             (2)

Every a lies in some S_b because x>0, and consequently alpha(a)<1/2. In particular n=|A|>=3. Counting A--B incidence using beta, without alpha, gives

    nx <= sum_b beta(b)|S_b| <=2.                                (3)

Thus x>1/3 implies n<=5, and x>2/5 implies n<=4.

Let L be the simple graph on A whose edges are the two-element sets S_b that occur. Singletons are also allowed as middle neighborhoods. If I is independent in L, each middle neighborhood contains at most one vertex of I, so

    |I|x <= sum_b beta(b)|S_b intersect I| <=1.                  (4)

Finally, call two occurring middle-neighborhood types incompatible if the alpha-weight of their union is at least 1/2. Representatives of incompatible types have disjoint C-neighborhoods: a shared C-neighbor would reach their whole union. Therefore a collection of t pairwise incompatible occurring types gives

    ty<=1.                                                      (5)

These arguments use only the two required degree conditions and the rank-two assumption.

## 3. Three or four A-types

If n=3, every two-element subset has alpha-weight greater than 1/2, because its complementary singleton has weight less than 1/2. By (2) only singleton or empty middle types can occur. Summing the three degree bounds gives 3x<=1.

Suppose n=4. Two disjoint edges of L cannot occur: their weights would both be less than 1/2 by (2), although their union has weight one. A graph with no two disjoint edges is either a star (possibly with missing edges and isolated vertices), or a triangle with isolated vertices. To verify this classification, if two edges ab,ac exist, any edge not incident with a must be bc, or it is disjoint from one of them. If bc exists, an edge involving a fourth vertex is disjoint from one of the triangle edges.

In the star case the three noncentral vertices are independent, so x<=1/3 by (4). In the triangle case let v be the fourth vertex. Since v has positive A--B degree, the singleton {v} is an occurring middle type. The three triangle edges and {v} are pairwise incompatible:

- the union of two triangle edges is A minus {v}, of weight greater than 1/2;
- the union of a triangle edge with {v} is A minus a triangle vertex, also of weight greater than 1/2.

Thus 4y<=1. Moreover x<=2/5: give each triangle vertex charge 1/2 and v charge 1. Every possible singleton or edge type has charge at most one. Summing the four degree bounds with these charges gives (5/2)x<=1.

This already proves both conclusions of (1) when n<=4.

## 4. A five-vertex fractional-cover lemma

We need the following elementary finite fact.

**Lemma.** Let L be a graph on five vertices. If nonnegative weights on its edges and on singleton vertices cover every vertex to weight at least one, with total weight strictly less than three, then L contains either a five-cycle or a triangle together with an edge disjoint from it.

**Proof.** Minimize the total edge/singleton covering weight. The dual maximizes sum_i u_i subject to

    0<=u_i<=1, and u_i+u_j<=1 for each edge ij.                   (6)

Every extreme point of this dual has coordinates in {0,1/2,1}. Indeed, on vertices with coordinates strictly between zero and one, consider the graph of tight equations u_i+u_j=1. If a component is bipartite, alternately increasing and decreasing its coordinates by a small epsilon preserves all tight equations and all other inequalities, contradicting extremality. A tight edge to an integral-coordinate vertex cannot meet a fractional vertex. Thus each fractional component has an odd cycle, which forces all its coordinates to be 1/2. This proves half-integrality.

The dual has a maximizing extreme point since its polytope is compact. Its optimum is therefore a half-integer. The feasible vector u_i=1/2 gives value 5/2, while the assumed cover and duality give an optimum strictly below 3. The optimum is exactly 5/2. By finite linear-program duality there is a cover of total weight 5/2. Its total covered vertex weight is at least five; each edge supplies twice its weight and each singleton only once. Equality therefore forces no singleton weight and exactly unit incident edge weight at every vertex.

Choose an extreme point of this fractional perfect-matching polytope. In its positive support, a leaf forces its incident edge to have weight one, so its component is a single edge. Every other component has minimum degree at least two. Its incidence columns must be linearly independent, since otherwise a small signed perturbation would preserve all vertex equations. Thus each component has at most as many edges as vertices. It must be a cycle, and it cannot be even because alternating perturbation would again contradict extremality. Hence each remaining component is an odd cycle with all edge weights 1/2. On five vertices the only possibilities are a five-cycle or a triangle plus a single edge. This proves the lemma.

## 5. Five A-types and the disjoint C-neighborhood certificate

Suppose n=5 and x>1/3. Aggregate beta-weights by singleton and edge types and divide them by x. They cover each A-vertex to at least one and have total weight at most 1/x<3; empty types can be omitted. The lemma applies to L.

If L contains a triangle and a disjoint edge, choose middle representatives of these four edge types. The two triangle-edge union is the complement of the disjoint edge, hence has weight greater than 1/2 by (2). A triangle edge together with the disjoint edge is the complement of a singleton, hence also has weight greater than 1/2. Thus all four types are pairwise incompatible, and 4y<=1 by (5).

If L contains a five-cycle, choose representatives of its five edges. The union of two nonadjacent cycle edges is the complement of a singleton, of weight greater than 1/2. The union of two adjacent cycle edges is the complement of another edge of that same five-cycle. That complementary edge has weight less than 1/2 by (2), so the union again has weight greater than 1/2. All five types are pairwise incompatible, giving the stronger 5y<=1.

Finally (3) gives x<=2/5 whenever n=5. Combining this with Section 3 proves (1), including all strict and weak endpoints claimed there.

## 6. Sharpness controls and a small-ordinary-graph corollary

The numerical barriers in (1) cannot be replaced by strict inequalities in both directions without further assumptions.

First, three disjoint three-vertex paths, one vertex in each part, are (1/3,1/3)-constrained with largest reach 1/3. All middle neighborhoods have size one. This shows why x>1/3 cannot simply be replaced by x>=1/3 in the second sufficient condition.

Second, take A={1,2,3,4,5}, B={b12,b23,b31,b45,b45'}, and C={c12,c23,c31,c45}. A middle vertex is adjacent to the two A-vertices in its label. Join b12 only to c12, b23 only to c23, b31 only to c31, and both b45 copies only to c45. Then every A-vertex has two of the five B-neighbors, every B has one of four C-neighbors, and each C reaches exactly two of five A-vertices. This ordinary 14-vertex graph is (2/5,1/4)-constrained and has largest reach 2/5. It is not a counterexample to the source implication: x+2y=9/10 fails its first strict hypothesis.

**Corollary.** If x,y>1/3 and an ordinary finite admissible graph has |A|<=6, some c reaches at least |A|/2 vertices. Otherwise every b's A-neighborhood is contained in the fewer-than-|A|/2 vertices reached by any one of its C-neighbors; it has size at most two. The rank-two theorem then contradicts y>1/3>1/4.

Thus an ordinary diagonal counterexample would need at least seven first-part vertices and at least one middle vertex with three or more first-part neighbors. This is a lower bound on a possible counterexample, not a bounded verification of the unrestricted statement.

## 7. Status after turn 2

Two genuine substantive turns are used. The original bundled target remains unresolved. The new theorem handles rank-two incidence with arbitrary positive weights; it does not constrain higher-rank middle neighborhoods. The next mechanism must handle such higher-rank overlap rather than repackage the disproved integral-cover shortcut or treat a finite support bound as a universal theorem. Standard finite LP duality is used explicitly; no historical novelty claim is made.
