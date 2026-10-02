# Turn 4: local neighborhood coloring, triangle-free graphs, and deficit one

Fourth substantive author turn. The original general source inequality remains unresolved.
This turn localizes the degree-capacity argument and separately closes the entire deficit-one boundary with an explicitly credited classical structure.

## 1. A maximum-degree neighborhood bound

Let H have no isolated vertices, order N, W distinct degrees, deficit D=N-W, and maximum degree Delta. Since its W degree values are distinct positive integers, Delta>=W. Put T=N-Delta, so

    T<=D.                                              (1)

Choose a vertex v of degree Delta. Suppose its induced neighborhood H[N(v)] has a proper coloring with h nonempty independent classes, h>=1. List their sizes in nondecreasing order as a_1,...,a_h, with S_i=a_1+...+a_i and S_0=0. They cover Delta vertices. The other T vertices, including v itself, are not required to be an independent set.

A degree value greater than N-a_i cannot be represented by a vertex in neighborhood classes i,...,h. Such a value can only be represented in the T outside vertices or the first i-1 classes. Counting positive degree values therefore gives

    W<=N-a_i+T+S_(i-1),
    a_i<=D+T+S_(i-1).

Induction yields Delta=S_h<=(2^h-1)(D+T). Together with(1),

    N=Delta+T <= (2^h-1)D+2^h T
                <= (2^(h+1)-1)D.                      (2)

This is a theorem about an actual coloring of one maximum-degree neighborhood. It does not assume that all neighborhoods have the same chromatic number or that the outside vertices are independent.

If k=chi(H) satisfies k>=2^h, then2^(h+1)-1<=2k-1. Hence(2) proves the stronger core inequality

    N<=(2k-1)D.                                        (3)

As in Turn3, this implies the exact source inequality after arbitrary isolates are restored.

## 2. Entire triangle-free class

In a triangle-free graph, the neighborhood of every vertex is independent. For a nonempty isolate-free core, its maximum degree is positive, so h=1 in(2). Thus

    N<=3D

for every isolate-free triangle-free graph. Since a graph with an edge has chi>=2, this proves property P of Turn3, and therefore the source inequality for **every triangle-free graph**, without a bound on its chromatic number.

A direct check of the same mechanism is useful. If Delta is the maximum degree, all positive degree values lie in1,...,Delta, so W<=Delta. The independent neighborhood of size Delta restricts its vertices to degrees at most N-Delta; the remaining N-Delta vertices can account for at most that many additional degree values. Hence W<=2(N-Delta). Combining the two gives W<=2N/3, equivalent to N<=3D.

This proof is not a consequence of treating a triangle-free graph as bipartite. Odd cycles and higher-chromatic triangle-free graphs are included by the independent-neighborhood argument.

More generally, if a maximum-degree neighborhood is bipartite and the graph has chi>=4, then h<=2 and(3) again holds. The case chi=3 is not covered by that numerical condition: its exponent bound gives7D while the desired coefficient is5D. A general3-colored graph has2-colored neighborhoods, so the local theorem does not silently solve that remaining case.

## 3. The deficit-one case and classical antiregular structure

Graphs with w=n-1 are the classical antiregular graphs. Their two recursive forms and uniqueness are credited, for example, in Levit–Mandrescu, [arXiv:1007.0880](https://arxiv.org/abs/1007.0880), Theorems1.4–1.5, with the earlier Behzad–Chartrand and Merris references. The following elementary reconstruction is included to verify the source-bound consequence directly; it is not a new classification claim.

Let G have n>=3 and w=n-1. Its degree set misses exactly one of0,...,n-1. The values0 and n-1 cannot coexist, so the missing value must be one of those two endpoints.

- If0 occurs, the degree set is0,...,n-2. The isolated vertex is unique: two isolates would make degree n-2 impossible. Remove that vertex. The remaining graph has order n-1 and degree values1,...,n-2, and contains a universal vertex.
- If n-1 occurs, the degree set is1,...,n-1. The universal vertex is unique: two universals would make degree1 impossible when n>=3. Remove it, reducing all remaining degrees by one. The remaining graph has order n-1 and degree values0,...,n-3, and contains an isolated vertex.

Thus unique endpoint deletion alternates until order2, where the two possibilities are an edge and two isolated vertices. Equivalently, if U_n and I_n denote the universal and isolated forms,

    U_n=K_1 vee I_(n-1),
    I_n=K_1 disjoint-union U_(n-1),                      (4)

with U_2=K_2 and I_2=2K_1. These descriptions are up to isomorphism and follow inductively from the endpoint deletions. Both forms have n-1 degree values, which also follows directly from(4).

Adding a universal vertex increases chromatic number by one; adding an isolate to a nonempty graph leaves it unchanged. The recurrences and order-two bases give

    chi(U_n)=floor(n/2)+1,
    chi(I_n)=ceil(n/2).                                 (5)

Consequently every graph with d=n-w=1 has chi>=ceil(n/2), exactly the source inequality in that case. The isolate-free form U_n even has n<=2chi(U_n)-1 and therefore satisfies the stronger core inequality. This also resolves the isolate-related boundary that Turn2 deliberately left open.

## 4. Scope after four turns

All triangle-free graphs, all deficit-one graphs, and the classes and compositions from the first three turns satisfy the requested inequality. The local-neighborhood criterion supplies additional cases when the global chromatic number is large relative to a coloring of one maximum-degree neighborhood. None of this proves the claim for arbitrary graphs with triangles and deficit at least two.

The most concrete residual regime is a3-chromatic graph with triangles, near-maximal degree variety, and deficit at least two, outside the structural composition class already proved. The cut-moment inequalities constrain it but do not establish realizability or nonrealizability. One final genuine author turn remains; it will test that residual edge-compatibility question rather than re-count a proved special case.
