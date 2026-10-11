# A complete path construction audit

This is an independent explanatory proof of the path construction underlying Šámal's known antichain theorem. It uses the two standard Blanuša graphs from Figure 1 of [arXiv:1212.6909v1](https://arxiv.org/pdf/1212.6909v1). Their particular finite properties were checked directly as described in the acceptance report. It does not assert a new theorem or a new construction.

## 1 The finite ingredients and elementary flow facts

Let A and B be the two nonisomorphic Blanuša snarks, each simple, cubic, connected, cyclically 4-edge-connected, with 18 vertices and 27 edges. Neither has a nowhere-zero flow over F = (Z/2Z)^2, while deleting any one edge of either leaves a graph with such a flow. In B choose the independent vertices a,b displayed in the source. No automorphism of B sends a to b. The cores obtained by deleting a,b from B, and by deleting a chosen attachment vertex from A, are connected. These are exactly the finite inputs checked in this audit.

For a graph, an F-flow assigns an element of F to each edge so that the sum at each vertex is zero. Orientations are immaterial in characteristic two. A nowhere-zero flow on a cubic graph is the same as a proper 3-edge-coloring: at a cubic vertex, three nonzero values have zero sum exactly when they are the three distinct nonzero elements of F.

Each coordinate of an F-flow is the indicator of an even edge set. Consequently, composition with a cycle-continuous edge function pulls an F-flow back to an F-flow. It is nowhere zero on the source whenever the target flow is nonzero on the image of that function. Also, every permutation of the three nonzero elements of F is a linear automorphism of F, so it preserves flow conservation.

## 2 Equal size rigidity

Suppose K and L are A or B and f is a cycle-continuous map K to L. If an edge e of L is missed, a nowhere-zero flow on L minus e extends by zero on e to an F-flow on L, nonzero on the image of f. Its pullback would be a nowhere-zero flow on K, a contradiction. Thus f is onto. Since both graphs have 27 edges, f is a bijection.

For any vertex v of K, the three images of its incident edges form a cut in L. Indeed, their indicator is orthogonal to every binary cycle in L: its dot product with a target cycle equals the parity of that cycle's preimage at v. The orthogonal complement of the binary cycle space is the cut space, by the elementary row-space/kernel orthogonality of the incidence matrix.

Every cut of size 3 in L is a vertex star. Cyclic 4-edge connectivity means one side of such a cut is acyclic. If that induced forest has s vertices and c components, cubic degree counting gives 3 = s + 2c. Since it is nonempty, s=c=1.

It follows that f maps each vertex star of K onto a unique vertex star of L. Different source vertices have different stars, so bijectivity of f makes the induced vertex map injective. Both graphs have 18 vertices, hence the vertex map is bijective. The image of an edge belongs to the stars of the images of its two endpoints, so this vertex bijection is a graph isomorphism inducing f. In particular, there are no such maps between A and B, and every such map B to B is an automorphism. This establishes the instance of Lemma 3.1 needed below.

## 3 Constructing the graphs

For each integer n at least 2, take a path indexed 0,1,...,n. Put a copy of A at each endpoint and a copy of B at every internal index. At each internal B use a as its left attachment vertex and b as its right attachment vertex. Choose a vertex in each endpoint A for its single attachment.

For each neighboring pair of blocks, delete the two attachment vertices and connect their three exposed neighbors by a chosen matching. All matchings may be fixed arbitrarily. Because a and b are independent, no original edge is incident to both attachment vertices in one block. Denote the resulting graph by H_n. Each joining matching is a triple of edges separating the left and right portions of the path.

The graph H_n is finite, simple, cubic, and connected. It has 16n+18 vertices and 24n+27 edges: start with n+1 blocks and remove two vertices and three net edges for each of the n joins. The connected-core property of the finite ingredients shows that every portion lying strictly to one side of a block is connected.

For a block v, let E_v be its 27-edge copy inside H_n: retain all its original nonattachment edges and identify each original edge incident to an attachment vertex with the corresponding joining edge. Different block copies have disjoint edge sets unless they are adjacent, in which case the intersection is their joining triple. Let I_v be the private edges of that block, excluding joining edges. These sets are pairwise disjoint, and each has at least 27-6=21 edges.

Every binary cycle in a block extends to a binary cycle in H_n with exactly the same restriction to E_v. At each attachment it uses zero or two of the three edges. If it uses two, join their exterior endpoints by a path through the connected exterior branch. Distinct exterior branches are disjoint, so the resulting edge set is even at every vertex. In particular, each edge of H_n lies on a cycle, because each block is bridgeless. Therefore H_n is bridgeless.

The natural injection of a block's edge set into H_n is cycle-continuous in the other direction of the cycle test as well: intersect any cycle of H_n with E_v and restore the attachment vertices. At an attachment vertex the resulting degree is even, since any cycle crosses a cut an even number of times. At other vertices evenness is inherited. Thus the restored edge set is a binary cycle of the block.

## 4 Localization for a path

**Claim.** Every cycle-continuous map from K in {A,B} to H_n has image exactly E_v for a single block v, and is an isomorphism onto that restored block followed by its natural edge injection.

Let R be its image. There are only 27 source edges, so |R| is at most 27. If R contains some E_v, then both have 27 edges and R=E_v. The cycle-extension property of Section 3 implies that the induced map from K to the restored block is cycle-continuous: test it against a block cycle by extending that cycle to H_n. Section 2 then proves the claimed rigidity.

It remains to rule out the case in which every E_v has at least one missed edge. Since the disjoint private sets I_v each have at least 21 edges, at most one I_v can be wholly contained in R.

First suppose every block has a missed private edge. In each block choose one such edge z_v. By edge-criticality, put an F-flow on the block which is zero at z_v and nonzero at all other edges. At every attachment star its three values are nonzero and distinct. By applying a linear automorphism of F to the entire next block's flow, these three values can be made to match the preceding block's values in the prescribed joining order. Continue along the path. The flows glue to an F-flow on H_n, and their only zero edges were chosen outside R. Its pullback is a nowhere-zero flow on K, a contradiction.

Now suppose one block v has I_v contained in R. Since E_v is not contained in R, it has a missed joining edge z on an interface with a neighboring block w. In both v and w choose z as the single zero edge. In every other block choose a missed private edge, which exists by uniqueness of v. On the special interface, each of the two block flows has pattern (0,c,c), with c nonzero, and the zero lies on the same joining edge. A linear automorphism matches the two nonzero values. At every other interface both triples are nonzero and distinct, so the same matching procedure works there too. Independence of the attachment vertices ensures that the zero at the special interface affects no other attachment star. Again, gluing along a path produces an F-flow on H_n nonzero on R. Its pullback contradicts the fact that K is a snark.

This exhausts the cases and proves the claim. The argument is specific to paths with 27-edge blocks and their 21-edge private cores; it does not assert the general tree-localization result.

## 5 No collapse and no folding

Suppose g is cycle-continuous from H_m to H_n, where m,n are at least 2. Compose g with the natural injection of each source block. Section 4 yields a target block index f(i) and a local block isomorphism sigma_i. The endpoint blocks are A and all others are B, so f preserves these types.

Two adjacent source blocks share three joining edges. Their images must share those three images. Consequently their target indices are equal or adjacent.

Adjacent blocks cannot have equal target indices. If one is an endpoint A and the other is B, their types already exclude equality. If both are internal B blocks, their shared edge triple is the star of b in the left block and the star of a in the right block. Equal target indices would make sigma_i(b) and sigma_(i+1)(a) the same vertex of one restored B: the two stars would be identical. Composing one local automorphism with the inverse of the other would give an automorphism sending a to b, which is impossible.

Thus adjacent source indices map to adjacent target indices. At an internal source block, the left and right attachment triples are disjoint, and the local map is an edge bijection. They cannot both map onto the same target joining triple. Hence f(i-1) and f(i+1) are distinct. There is no folding.

A path map taking every step to an adjacent index and never reversing its next step is strictly monotone, with every step +1 or every step -1. Its two endpoints therefore have distinct images. Since endpoint types force both images to lie in {0,n}, they are exactly those two endpoints, and m=n.

It follows that for distinct m,n no cycle-continuous map H_m to H_n exists. Interchanging m and n gives the other direction. The infinite family {H_n : n at least 2} is the required antichain of finite simple cubic connected bridgeless graphs.

## 6 Verification scope

All infinite-family reasoning above is elementary once the finite inputs in Section 1 hold. The finite audit used a manual transcription of the source figure, direct flow witnesses for all 54 deletions, exhaustive cut enumeration for the two 18-vertex graphs, and two different noncolorability algorithms. These are finite computations for the two examples, not a new proof of the full classification of small snarks. The published theorem independently provides the literature resolution regardless of whether a reader reruns this supplementary audit.
