# Turn 3: split graphs and a composition-closed class

Third substantive author turn. The exact general Melnikov bound remains unresolved.
This route uses actual graph structure rather than formal degree assignments.

## 1. A stronger core property

For a graph G, remove all isolated vertices to obtain its core H. Define property P as follows: it holds vacuously when H is empty, and otherwise

    |V(H)| <= (2 chi(H)-1)(|V(H)|-w(H)).                 (1)

Property P implies the source inequality for every G of order at least two. If G is edgeless this is immediate. Otherwise write N=|V(H)|, D=N-w(H), k=chi(G)=chi(H), and r for the number of removed isolates. If r=0, (1) is stronger than the source form n-1<=(2k-1)d. If r>=1, then d=D+r-1, so

    n-1=N+r-1 <= (2k-1)D+r-1 <= (2k-1)d.

Turn1 proves P for every bipartite graph: its nonempty core has chromatic number2 and satisfies N<=3D.

## 2. Every split graph has property P

A split graph here means one whose vertex set partitions into a clique and an independent set. Removing isolates preserves that property. Consider an isolate-free split graph H, and put k=chi(H).

There is a split partition K,I with K a maximum clique. Indeed, from any split partition Q,R, either Q is maximum, or one vertex of the independent set R joins all of Q and can be added to it. A clique contains at most one vertex of R. The remaining vertices are still independent. If |K|=k0, each vertex of I misses at least one vertex of K, so it can be assigned a missing clique color; since I is independent, this proves chi(H)=k0. Thus |K|=k.

Every vertex of I has degree between1 and k-1. The k clique vertices contribute at most k further degree values. Consequently

    W=w(H)<=2k-1.                                      (2)

Let N=|V(H)| and D=N-W. Because H has an edge, k>=2 and D>=1. If D>=2, then

    N=W+D<=2k-1+D<=(2k-1)D,

where the final inequality follows from (2k-2)D>=2k-1. It remains to handle D=1.

In that case (2) gives N<=2k. Suppose N=2k. Then W=2k-1, and equality in the degree-value count forces I to realize every degree1,...,k-1 while the k clique degrees are all distinct and disjoint from those values. Hence every clique degree is at least k. Since |I|=k, its degree sum is at most

    1+2+...+(k-1)+(k-1) = (k-1)(k+2)/2.

The clique degree sum is at least k+(k+1)+...+(2k-1). Subtracting its internal degree contribution k(k-1), the number of edges between K and I is therefore at least

    k(3k-1)/2-k(k-1)=k(k+1)/2.

These are two counts of the same cut, but the proposed upper bound is exactly one smaller than the lower bound. This contradiction excludes N=2k. Thus N<=2k-1=(2k-1)D, proving P for every split graph.

The proof covers complete graphs as well: the exceptional equality configuration would require |I|=k, so an empty independent part cannot produce it. No infinite family of graphs has been inferred from a finite scan.

## 3. Closure under disjoint union

Suppose G_1,G_2 have P. Their isolate-free cores H_1,H_2 may be empty. Discard empty cores; if none remain the union is edgeless. Otherwise let their orders, varieties, deficits and chromatic numbers be N_i,W_i,D_i,k_i.

For the disjoint union H of the nonempty cores,

    N=sum N_i, chi(H)=max k_i,
    w(H)<=sum W_i, hence D=N-w(H)>=sum D_i.

Writing k=max k_i and using P for each core gives

    N<=sum (2k_i-1)D_i<=(2k-1)sum D_i<=(2k-1)D.

Thus the union again has P. Degree-set overlaps only increase its deficit and cannot invalidate the argument.

## 4. Closure under complete join

The complete join G=G_1 vee G_2 of two nonempty graphs adds every edge between the parts. It has no isolates and satisfies chi(G)=k_1+k_2. If the orders are n_i and the degree varieties w_i, the two degree sets are translated by the other part's order. Hence

    w(G)<=w_1+w_2,
    d(G)>=d_1+d_2, where d_i=n_i-w_i.

P for each input implies the polynomial source inequality

    n_i-1 <= (2k_i-1)d_i.

This remains valid for a one-vertex input: both sides are zero. If d_1+d_2>=1, then

    n_1+n_2 <= (2k_1-1)d_1+(2k_2-1)d_2+2
               <= [2(k_1+k_2)-1](d_1+d_2).

For the second inequality, subtract the previous expression from the right-hand side; the difference is 2k_2 d_1+2k_1 d_2-2, nonnegative because k_i>=1 and d_1+d_2>=1. Using d(G)>=d_1+d_2 proves P for the join.

The remaining case d_1=d_2=0 forces both inputs to be singletons, since every simple graph of order at least two has positive deficit. Their join is K_2, with order2, chromatic number2 and deficit1; it satisfies P. This resolves the otherwise dangerous zero-deficit boundary.

## 5. Consequence and exact gap

Every graph obtained from bipartite and split graphs by finitely many disjoint unions and complete joins satisfies P and therefore the exact source inequality. In particular, graphs constructed recursively from singletons by those two operations are covered. The result concerns the explicit generated class; arbitrary graphs are not asserted to admit such a construction.

This proves a second broad structural collection beyond the bipartite subcase and isolates a robust composition mechanism. It does not establish P or the source inequality for a general graph, and it does not classify all graphs satisfying them. No novelty or priority claim is made. The original target remains unresolved after3/5 author turns.
