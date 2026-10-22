# Two common colors in subcubic critical edge lists

Authored 12 October 2026 UTC. This bounded research round gives a symbolic theorem with no bound on the number of exceptional lists, and a precise six-edge boundary for a local recoloring criterion. The theorem requires two colors common to every list. It does not settle arbitrary nonconstant three-list assignments, and no historical novelty is claimed.

## 1 The common two-color theorem

**Theorem.** Let G be a finite simple graph of maximum degree three. Suppose G is not properly three-edge-colorable, but G−e is properly three-edge-colorable for every edge e. Give every edge a list L(e) of exactly three colors. If the lists are nonconstant and their intersection contains two colors, then G admits a proper L-edge-coloring.

There is no bound on the size of G, on the number of different lists, or on the number of edges differing from any one list.

### 1.1 A local matching recoloring lemma

Fix a three-color palette A. Suppose every exceptional list is

L(e)=(A\{a})∪{x_e},

where the omitted base color a is common to the exceptions and x_e∉A; all other lists are A. Let X be the exceptional edges. Choose e∈X and an ordinary three-coloring φ of G−e. If some ordinary label t is absent from the exceptional neighbors of e, then the lists can be colored.

Indeed, let F consist of e and all other exceptional edges with ordinary label t. The latter edges form a matching, and none meets e. Thus F is a matching. Color each f∈F with its own exterior color x_f. Permute the ordinary labels onto A, mapping t to a, and retain the resulting ordinary coloring on G−F. Every exceptional edge outside F avoids a and therefore receives a permitted base color. The nonexceptional edges allow all of A. Exterior colors lie outside A, and the exterior-colored edges form a matching, so the two parts combine properly.

In particular, the required label exists whenever e has at most two exceptional neighbors. It also exists if e has an exceptional nonneighbor f adjacent to every exceptional neighbor of e: use t=φ(f). The number of exceptional edges is unrestricted in this lemma.

### 1.2 There is a mixed vertex

There is exactly one connected component of G containing edges. To prove this, at least one component C is not three-edge-colorable, since G is not. If an edge e belonged to another component, then G−e would still contain C and would not be three-edge-colorable, a contradiction. All other components are isolated vertices.

Consequently, every partition of E(G) into two nonempty groups has a vertex incident with edges from both groups. Otherwise edges from different groups could not lie in the same connected component.

### 1.3 Collapse to two palettes

Choose a two-element set S contained in every L(e). Since each list has size three, write uniquely

L(e)=S∪{c(e)},  with c(e)∉S.

Nonconstancy means that c(e) takes at least two values. Choose one value c₀ and partition the edges into

P={e:c(e)=c₀},  Q=E(G)\P.

Both groups are nonempty. Choose a fresh marker color x not appearing in any original list. Form proxy lists

L*(e)=S∪{c₀} for e∈P,   L*(e)=S∪{x} for e∈Q.

At a mixed vertex v from Section 1.2, the degree bound forces one of P,Q to have exactly one incident edge: both groups are present and the total degree is at most three. Call that group W and its unique incident edge e. Relative to the other group's proxy palette, precisely W is exceptional. Its proxy lists replace one common base color by the other palette's third color.

Edge e has no other W-edge at v and at most two W-edges at its other endpoint. Hence it has at most two exceptional neighbors. The local lemma colors the proxy assignment, using any ordinary coloring of G−e.

### 1.4 Restore the individual colors

In the proxy coloring, every x-colored edge belongs to Q. Replace x on each such edge e by its original third color c(e), leaving all other colors unchanged.

This preserves membership in every original list. It also preserves properness. All x-colored edges formed a matching before restoration. Each restored color lies outside S and differs from c₀, since the edge lies in Q. Every edge not restored still has a color in S∪{c₀}. Thus a restored edge cannot conflict with an unrestored edge, and two restored edges are nonincident even if their restored colors coincide. This proves the theorem. ∎

The construction uses one ordinary deletion coloring, one global permutation, a recoloring of a matching, and marker restoration. It requires no Kempe-chain assumption and no arbitrary-boundary extension assertion.

## 2 Consequences and scope

**Common-omission corollary.** Fix A with |A|=3. Start with constant A-lists and make any nonempty collection of one-color substitutions, always omitting the same a∈A but allowing the introduced colors to differ. If the resulting assignment is nonconstant, it is colorable. Every list contains A\{a}, so the theorem applies. The number of substitutions is unrestricted, including six and larger supports.

The explicit nonconstant qualification matters if all edges have been changed to one identical new palette. Such a constant assignment is uncolorable by the hypothesis on G. Conversely, for the family of three-list assignments having two common colors, the theorem and ordinary non-three-colorability give the exact statement: a list assignment is uncolorable if and only if it is constant.

For assignments with no two colors common to all lists, this theorem gives no answer. In particular, six arbitrary exceptional lists with varying omitted base colors are not settled here.

## 3 The six-edge local-method frontier

The following identifies the six-edge supports on which the simple “at most two exceptional neighbors” sufficient condition cannot apply directly. It does not identify bad list assignments.

**Support lemma.** Let X be six edges of a finite simple subcubic graph, and suppose every edge of X meets at least three other edges of X. After deleting isolated vertices, the support G[X] is K₄ or K₂,₃.

Write d_X(v) for degree in the support. For e=uv∈X, its number of exceptional neighbors is d_X(u)+d_X(v)−2. Thus the hypothesis excludes degree-one support vertices and excludes edges joining two degree-two support vertices. Every nonisolated support vertex has degree two or three, and the degree-two vertices form an independent set.

Let n₂,n₃ count these vertices. Since |X|=6,

2n₂+3n₃=12.

The possibilities are (n₂,n₃)=(6,0),(3,2),(0,4). The first is impossible because degree-two vertices are independent and there are edges. In the last case a simple three-regular graph on four vertices is K₄. In the middle case each of the three degree-two vertices must have both of the degree-three vertices as neighbors, giving K₂,₃. This also rules out hidden disconnected alternatives. ∎

K₄ cannot occur as an exceptional support in the critical graph of the theorem. Its four vertices are already saturated, so it is an entire component of G. By Section 1.2 it would be the sole edge-containing component, but K₄ is three-edge-colorable by its three perfect matchings.

For K₂,₃, every support edge has three exceptional neighbors. No exceptional nonneighbor dominates those neighbors either. Label the bipartition {u,v} and {a,b,c}. The neighbors of ua are ub,uc,va. Its nonneighbors vb and vc miss uc and ub, respectively. Thus both purely support-based local sufficient conditions from Section 1.1 fail on this support. The common two-color theorem still works by choosing the reference proxy palette from the other edge group when necessary.

## 4 A critical example separating the methods

Consider the following ordered edges on nine vertices:

    e0=14, e1=12, e2=13, e3=23,
    e4=57, e5=58, e6=59,
    e7=67, e8=68, e9=69,
    e10=74, e11=82, e12=93.

The maximum degree is three. There are thirteen edges, while any matching on nine vertices has at most four edges. Three colors can therefore cover at most twelve edges, so the graph is not three-edge-colorable.

Every edge deletion is three-edge-colorable. The automorphisms (5 6) and (2 3)(8 9) reduce the deletions to the following seven representatives. Each displayed triple is a partition of the remaining edge indices into matchings:

- Delete 0: {1,5,7,12}, {2,4,9,11}, {3,6,8,10}.
- Delete 1: {0,4,8,12}, {2,6,7,11}, {3,5,9,10}.
- Delete 3: {0,4,8,12}, {1,5,9,10}, {2,6,7,11}.
- Delete 4: {0,3,5,9}, {1,8,10,12}, {2,6,7,11}.
- Delete 5: {0,3,6,7}, {1,4,8,12}, {2,9,10,11}.
- Delete 10: {0,3,5,9}, {1,4,8,12}, {2,6,7,11}.
- Delete 11: {0,3,6,7}, {1,4,8,12}, {2,5,9,10}.

The stated automorphisms give the edge orbits {0}, {1,2}, {3}, {4,7}, {5,6,8,9}, {10}, {11,12}, covering all thirteen deletions. Thus the graph meets the theorem's criticality hypotheses without relying on an unproved fixture assertion.

Take A={0,1,2}, and let X={e4,e5,e6,e7,e8,e9}, the K₂,₃ support. Give X the list {0,1,3} and every other edge A.

Delete e5. The following ordinary coloring of the remaining edges is proper, listed in edge order with a dash for the deletion:

    (0,2,1,0,0,–,1,1,2,0,2,1,2).

The exceptional neighbors of e5 are e4,e6,e8, with ordinary colors 0,1,2. Therefore this particular deletion coloring has no label absent from the exceptional neighborhood, so the matching-recoloring construction of Section 1.1 cannot begin with this e and this φ.

This is only a fixed-choice method obstruction. A full valid list coloring is

    (0,2,1,0,3,0,1,1,3,0,2,1,2).

One way to obtain it is to use the other palette as the base. Regard Y=E(G)\X as exceptional relative to {0,1,3}. At vertex 7, its only Y-edge is e10. Take the displayed representative coloring of G−e10, using the matching order as ordinary labels 0,1,2. Ordinary label 1 is absent from e10's exceptional neighbors. Recolor the matching {e1,e10,e12} with the exterior color 2, and map ordinary labels (0,1,2) to (0,3,1). The resulting full vector is the one above.

Both the rejected fixed choice and the successful reversed-palette construction satisfy the same original lists. No failure of list-colorability, or of all choices in the local method, is asserted.

## 5 Verification and primary context

The proof is symbolic. Independent finite checks exercise the collapse/restoration construction, every choice of a third-color class, both possible minority groups, all eligible boundary deletions, the six-edge support classification, and the explicit critical example. They are corroborative rather than logical premises.

The underlying unrestricted question is recorded in [Open Problem Garden](https://www.openproblemgarden.org/op/list_colorings_of_edge_critical_graphs), [Mohar's July 2001 page](https://www.sfu.ca/~mohar/Problems/P7ListEdgeCriticalGraphs.html), and [Kaul–Mudrock, Conjecture 6 in arXiv version 2](https://arxiv.org/pdf/1805.02147v2). Mohar's reversed printed equivalence is the known wording issue, not a substantive refutation. The present theorem handles the common-two-color family and makes no claim for all nonconstant assignments. Bounded primary-source research has not established historical novelty.
