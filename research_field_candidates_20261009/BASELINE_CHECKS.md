# Elementary checks supporting candidate selection

Status: independently checked deductions; **novelty is not claimed**. These establish that the proposed models have concrete, accessible starting points. They do not validate the entire research programs.

## A. Two final changes can require many temporary helpers

Let P_n have vertices 0,...,n−1 and x(j)=j modulo 3. Choose 1≤i≤n−3. Let y interchange x(i) and x(i+1), leaving every other vertex fixed. This is a proper coloring: the exterior neighbors i−1 and i+2 share the third color.

Under proper single-vertex recoloring using exactly three colors, the minimum number of vertices outside {i,i+1} ever recolored is

    h(x,y) = min(i, n−i−2).

For the lower bound, let S be the set of ever-recolored vertices. A connected component of P_n[S] not containing either endpoint cannot have a first recoloring: the vertex selected for that first recoloring still sees its two differently colored initial neighbors, leaving no alternate color. Thus the component containing i,i+1 must extend to an endpoint, forcing at least the stated number of helpers.

For the upper bound, restrict changes to the interval from the nearer endpoint through i,i+1. The opposite external boundary vertex is fixed. Proper three-colorings of this interval are connected under single-vertex recoloring. To see this inductively, remove the free leaf; realize a recoloring path on the remaining interval; whenever its neighbor needs the leaf's color, first give the leaf the third color, different from the neighbor's old and new colors. Finally set the leaf to its target color. The one-vertex case is immediate. This reaches y using only the stated helpers.

With a fourth color the two target vertices alone suffice: move the first to the spare color, the second to its target, then the first to its target. Thus this example's helper requirement is sensitive to spare freedom.

Two independent conceptual agents and an adversarial reviewer checked the argument. The reviewer also reported exhaustive support/reachability checks of 21 interior adjacent swaps for n=4,...,9. No execution transcript from that separate check is included in this package; the written proof is the retained verification artifact.

The helper count is not a distance metric. Minimum total touched support equals minimum-label path on the implicit state graph, so broad abstract originality is ruled out.

## B. Exact environment size for an autonomous reversible reset

Let X be a nonempty finite set of size n, c∈X, and f(x)=c for all x. Let T≥0 be an integer. Minimize |E| over finite E, e0∈E, and permutations U:X×E→X×E with

    first_coordinate(U^t(x,e0)) = c

for all x and 1≤t≤T. Then

    M_f(T) = (n−1)T+1.

If n=1 or T=0, the identity with |E|=1 suffices. For the remaining cases set a_x=(x,e0) and C={c}×E.

The set B={U^t(a_x):x≠c,1≤t≤T} has (n−1)T distinct elements. At equal times, equality implies the initial states agree. If s<t and U^s(a_x)=U^t(a_y), cancellation gives a_x=U^(t−s)(a_y), contradicting the first coordinates x≠c and c. All elements of B lie in C.

There is an additional element of C outside B. If a_c is outside B, it suffices. Otherwise a_c=U^s(a_x) for some 1≤s≤T. Then w=U^(T+1)(a_x)=U^(T+1−s)(a_c) lies in C. If w=U^t(a_y) for y≠c and 1≤t≤T, cancellation gives U^(T+1−t)(a_x)=a_y, again contradicting visible coordinates. Thus |C|=|E|≥(n−1)T+1. This explicitly handles shifted overlaps with the orbit starting at c.

For the upper bound, choose |E|=(n−1)T+1 and fix (c,e0). For each x≠c allocate T distinct other states of C and make a cycle starting at a_x, passing through those T states, and returning to a_x. These cycles are disjoint. Fix every remaining product state. The resulting single permutation has the required visible trajectory through time T.

A systems agent derived this proof and a separate adversarial agent independently verified it. The result measures environment states, not physical energy or entropy production. It does not establish novelty relative to finite dilation or reversible-simulation theory.

## C. Ordinary diagnosis plus eventual restoration is insufficiently new

Suppose a known deterministic machine has n states and is strongly connected under its allowed actions. If a policy identifies its unknown initial state within D actions in the worst case, its current state is also known from that initial state and the action history. A shortest path back to the initial state has at most n−1 edges.

Therefore identification followed by restoration needs at most D+n−1 actions. From every intermediate transcript, one can finish the distinguishing policy and then return. Consequently unbounded prefix recoverability does not add a constraint in this setting. A fixed recovery budget, restricted undo, disturbance cost, or memory limit is essential to the proposed research question.

The pair-state formulation is finite: a belief retains (initial,current) pairs. Let G_0 consist of beliefs contained in the diagonal. Recursively a belief belongs to G_(r+1) if it is in G_r or some action sends every nonempty output branch into G_r. This exactly characterizes adaptive recovery within r+1 actions. Restrict identification policies to G_r to enforce the recovery budget at every prefix.

## D. Stable rectangle descriptions have useful easy bounds

For one-dimensional bit strings, maximal black runs give the unique minimum disjoint interval description. Flipping one bit can create/delete one run, resize one run, split one into two, or join two into one. At most three interval records are added or removed. The transition 101→111 attains three.

In a two-dimensional picture, adding a black pixel to a partition is possible by adding its singleton rectangle. Deleting one black pixel removes its containing rectangle and replaces the remainder by at most four disjoint rectangles. Consequently adding a pixel increases the optimal count by at most one, while deleting it increases the count by at most three. Applying the reverse operation shows the absolute change is at most three.

Starting from an optimal partition, deletion changes at most five rectangle records and produces at most opt(old)+3 rectangles. Since opt(old)≤opt(new)+1 in this direction, the constructed partition is within additive four of the new optimum. Addition changes one record and produces opt(old)+1 rectangles; the reverse deletion bound gives opt(old)≤opt(new)+3, again yielding additive four. These are one-step bounds from an optimal starting partition, not perpetual online guarantees.

The unresolved proposed question concerns the change required between every possible pair of exact old/new optima, or tighter/coherent/persistent guarantees. No family separating every such pair has been established in this scouting effort.

An adversarial reviewer independently checked these bounds and identified a quantifier boundary. If all available rectangles have at most two pixels, partitions are matchings plus singleton vertices. Adjacent pictures always admit some optimal pair with at most two records changed: preserve an old maximum matching if its size remains optimal; otherwise remove the edge incident to the new pixel from a new maximum matching to obtain a compatible old optimum.

But an odd-length zigzag path of pixels has an optimal partition consisting of dominoes and one singleton. After committing to such a partition, adding a pixel at the endpoint farther from the singleton forces the unique perfect matching on the new even path, changing a linear number of records. This is an elementary matching-based online obstruction, not a claimed novel result. It cannot prove that every pair of old/new optima is far apart.

## E. Two endpoints of finite arithmetic's accuracy/law tradeoff

Fix integer m≥1, S={−m,...,m}, and a closed operation ⊕ agreeing with x+y whenever that integer is in S. Define C(t)=max(−m,min(m,t)) and E=max|x⊕y−C(x+y)|/(2m). Define D as the fraction of triples violating associativity.

If D=0, interior exactness supplies identity 0 and two-sided inverse −x for every x. Associativity therefore makes S a group. Repeated exact additions of 1 generate every positive displayed integer, and inverses give every negative integer. Thus this is the cyclic group of order 2m+1, with the prescribed signed integer labeling. Commutativity follows automatically. At (m,1), the result is −m while clipping gives m, so E=1.

If E=0, the table is exactly saturation/clipping. It is nonassociative for every m≥1: the triple (m,m,−m) gives 0 under left grouping and m under right grouping.

If the operation is required to be coordinatewise nondecreasing, it must also be saturation. For x+y>m, compare x with m−y, which is in S. Monotonicity gives x⊕y≥(m−y)⊕y=m, forcing equality. The lower overflow case is analogous, and interior values are already prescribed. Exact monotonicity and exact associativity are therefore incompatible under these assumptions.

An arithmetic agent and a separate adversarial reviewer verified these claims, including m=1. The excluded m=0 would make normalized E undefined. No assertion is made about the optimal intermediate E/D frontier or its originality.
