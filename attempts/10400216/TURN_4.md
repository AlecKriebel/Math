# Turn 4: exact exterior-preserving compression and a coercive-gleam obstruction

**Scoped partial result; original Problem 12.11 remains unresolved after four substantive author turns.** This route tests whether a condition involving large absolute gleams or many true vertices can supply a direct lower bound while including the alternating examples. A concrete family shows why raw, presentation-dependent quantities cannot do this. The argument also follows an actual exterior-preserving shadow collapse, rather than drilling to another manifold.

All volume inputs and the shadow-collapse construction are credited prior results. The elementary family calculation is not presented as a historical discovery or a counterexample to the original existence question.

## 1. An explicit family of alternating knot diagrams

For an integer k>=2, let G_k be the plane graph with vertices A,B,C, with k parallel edges p_1,...,p_k between A and B, and two further edges a=AC and b=BC. Its planar cyclic orders are

    A:(a,p_1,...,p_k),   B:(b,p_k,...,p_1),   C:(a,b).

Give every edge the same Tait sign and take the signed medial diagram D_k. Moffatt's Tait construction identifies this plane data with an actual link diagram. It is alternating by the local preceding/following-corner argument in turn 3. It has n=k+2 crossings.

The diagram is a knot diagram for every k. Here is an all-size combinatorial certificate, avoiding reliance on a name or a picture of a twist knot. Straight-through medial traversal from the following corner of a at A has crossing-visit word

    k even:  a p_1 ... p_k a b p_k ... p_1 b,
    k odd:   a p_1 ... p_k b a p_k ... p_1 b.              (1)

These words follow directly from the specified rotations: within the parallel bundle the next crossing index increases, switching endpoint at each crossing; the parity at the far end determines whether a or b is encountered first; the return traverses the bundle in reverse. Each crossing occurs twice and the two occurrences have opposite over/under parity. Consequently both branches at every crossing lie on this one component. The opposite directed traversal is its reversal; there are no further components. The checker constructs this permutation directly, including parallel-edge labels and degree-two corners.

The diagram is prime. To see the needed planar fact, a simple closed curve meeting a projection in exactly two edge points consists of an arc in one black face and one in one white face. If both sides contain crossings, the corresponding black Tait vertex separates the Tait graph, unless one side consists only of loops at that vertex. Our graph has no loops, and deleting any one of A,B,C leaves a connected graph. Therefore no such decomposition is possible. It also has no bridges, so there is no nugatory crossing in the reduced alternating medial diagram.

For k>=2 this is not the standard two-strand torus-link diagram: its Tait graph is neither a bond with two vertices nor a simple cycle, the two checkerboard possibilities for that standard diagram. The Menasco hyperbolicity statement quoted in Lackenby's introduction therefore applies. D_k represents a hyperbolic knot K_k.

## 2. The twist count and the bounded volume

The k-1 bigon faces between the parallel edges in G_k become k-1 white bigon regions in D_k, forming one twist chain on p_1,...,p_k. The degree-two black face C is the bigon joining a and b, forming the other twist chain. The other two white faces are triangles, and the other two black faces have valence k+1. Thus

    t(D_k)=2.                                           (2)

Lackenby's Theorem 1 now gives the uniform upper bound

    vol(S^3 minus K_k) < 16 v_3.                         (3)

The stronger appendix bound could replace 16 by 10, but no sharper constant is needed here. The lower estimate from twist number is not used to prove anything about this family's volume growth.

In contrast, the raw crossing/true-vertex count of the uncollapsed canonical shadow is k+2, tending to infinity. With black signs chosen positive, the black gleams are

    ((k+1)/2, (k+1)/2, 1),

and the white gleams consist of k-1 entries -1 and two entries -3/2. Consequently

    sum_black |g| = k+2,
    sum_all_spherical_faces |g| = 2(k+2),
    max_face |g| >= (k+1)/2.                             (4)

Every one of these diagrams satisfies the exact saturation criterion from turn 3. Even if the outside face's gleam is omitted, the absolute sum over the remaining planar faces is at least (3k+7)/2, so it still diverges.

It follows rigorously that no universal lower bound on this whole class can have the form vol>=f(n), vol>=f(sum|g|), or vol>=f(max|g|), with f(x) tending to infinity as x tends to infinity. Given any such function, (3) and (4) contradict its proposed inequality for sufficiently large k. This is not a statement against bounds using twist count, a normalized shadow, several interacting quantities, or a bounded coefficient.

## 3. A real move to an efficient shadow of the same exterior

Choose the face corresponding to A as the outside face of D_k. Use Costantino–Thurston's canonical construction in Section 3.2: its outer disk boundary has color f (false), and the free boundary of the link annulus has color e when representing the exterior. Collapse the region meeting that false boundary, as in the construction immediately preceding Example 3.15. This preserves the reconstructed exterior; it is not an extra Dehn filling or drilling of a core.

The face A meets precisely the k+1 distinct crossings a,p_1,...,p_k, once each, and misses b. Every one of these k+1 vertices disappears in that collapse. Locally, the link of a true vertex is the tetrahedral graph K_4. Removing the unique sector belonging to the outside region removes one edge from that link. Suppressing the two resulting valence-two points gives the theta-graph link of a nonvertex triple-line point. Along the intervening edges, deleting the outside sheet merely removes singularity; it creates no true vertex. The neighborhood of b is untouched. Thus the resulting relative shadow has exactly one true vertex.

The global justification is the source's exterior-preserving collapse, with the boundary colors retained. The local link calculation checks its vertex count in this particular family. Merely erasing a face from an arbitrary decorated shadow would not be a justified manifold-preserving operation.

For comparison, Costantino–Thurston Example 3.15 performs this same collapse on the figure-eight diagram, reducing four vertices to one. Here the distinct-incidence count makes the reduction explicit for every k. We do not assume that the original numerical face data or planar checkerboard structure can be read unchanged after this collapse.

In particular the ordinary shadow complexity of each exterior is exactly one. The constructed shadow proves sc<=1. Hyperbolicity makes its Gromov norm positive, and Costantino–Thurston Theorem 3.37 forces sc>0. Since sc is integral, sc=1. The same theorem gives the further uniform upper bound

    vol(S^3 minus K_k) <= 2 v_oct.                        (5)

No lower volume bound has been inferred by reversing this inequality.

## 4. Consequences for the attempted general condition

The family distinguishes two failures which a proposed condition must avoid.

- Retaining every alternating canonical shadow while demanding a coercive lower bound in its raw vertex count or absolute gleam size is impossible, by (3)–(4).
- Normalizing by actual shadow moves changes the relevant data dramatically: this family compresses from k+2 vertices to one while preserving the exterior. A direct canonical saturation argument does not automatically become an invariant condition on the resulting one-vertex polyhedron.

The compression is constructive, so this is more than the warning that one might have chosen a nonminimal presentation. On this family the minimum is known exactly. It still does not give a general algorithmic reduction or a geometric lower bound for efficient shadows of arbitrary alternating knots.

The remaining route should extract an essential-surface, guts, or other complexity which survives or correctly tracks these collapses. The examples do not preclude a general shadow condition with such additional structure, nor do they show that the original source question is impossible. The original target remains unresolved, with one substantive author turn remaining.

## Checks and sources

The exact program independently constructs the plane face permutations and medial straight-through permutations for the specified multigraphs. It checks the parity-dependent word, one-component count, face and gleam incidence formulas, the removed-vertex count, and the K_4-edge deletion/suppression. Finite instances are controls on the written all-k proof, not hyperbolicity tests.

Primary inputs are the already-pinned Moffatt Section 3.1, Thurston's canonical corner rule, Lackenby Theorem 1 and its introductory Menasco statement, and Costantino–Thurston Section 3.2/Example 3.15 and Theorem 3.37. No uninspected parameter convention for another twist-knot diagram is needed.
