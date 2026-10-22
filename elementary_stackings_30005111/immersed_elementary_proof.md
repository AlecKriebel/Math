# Elementary finite splitting proof (immersed scope)

Let W:C_n→G be a nonempty combinatorial immersion of a circle in a finite graph, with oriented edges mapped homeomorphically, and suppose its cyclic edge word is not a proper repetition. Replace G by the image.

## Splitting step
For any connected current image H of rank r=|E|-|V|+1≥2, fix an orientation of each edge. There exists an integer edge cochain c with signed sum along W equal to zero which is not a vertex gradient. Indeed the zero-sum condition is at most one rational linear equation in |E| variables, whereas gradients have dimension |V|-1; |E|-1>|V|-1. Clear denominators.

Starting with s_0=0, let s_i be cumulative c-increment up to the ith domain vertex. Since the total is zero, s_n=s_0. Replace each image vertex occurrence v_i by (v_i,s_i) and each traversed edge e by its copy whose initial level is the appropriate s_i. This constructs a finite connected graph H′ mapping to H inside the elementary integer voltage cover. The walk lifts and remains immersed. At least one vertex fiber splits: otherwise each vertex v has one level s(v), and every used oriented edge has c(e)=s(head e)-s(tail e), contradicting non-gradientness. Therefore |V(H′)|>|V(H)|. Each image vertex is visited, so |V(H′)|≤n.

Repeat whenever rank≥2. This terminates in at most n-|V(G)| steps. Every image graph is connected and has minimum degree at least two, because the lifted walk is immersed and edge-surjective. Thus its rank is at least one. At termination rank is one, so the finite connected image is a circle. An immersed circle-to-circle map is a covering. Its absolute degree must be one, since otherwise projection back to G expresses W as a proper repetition. Consequently the final lift is embedded.

## Descending heights, without a topological tower theorem
At one step, extend the cumulative levels linearly over every domain edge; call this height a. In the fixed orientation of an old edge e, a point with coordinate t on the copy starting at integer level k has a-height k+t c(e), including when the domain traversal goes against that orientation. Distinct occurrences of a common oriented old edge have a constant integer height difference. Distinct domain vertices over the same old vertex have integer level differences. Suppose the lifted walk has a stacking with height b, bounded by M on its compact domain. Set h=a+εb, with 2εM<1 (any ε>0 if M=0).

If two domain points have the same old projection but different lifted projections, their a-heights differ by a nonzero integer, so their h-heights are distinct. If they have the same lifted projection, their a-heights agree, while their b-heights differ. Thus the continuous map (W,h) is injective; compactness of the domain circle and the Hausdorff property of the graph product make it an embedding. Hence h is a stacking over the old graph. Start with constant height zero at the embedded final lift and descend finitely many times. This proves the primitive immersed stacking theorem with only finite graph counting, elementary linear algebra, and linear interpolation.

## Necessity, valid without immersion
If W factors through a k-fold cyclic covering for k≥2, let τ be its deck rotation. Any stacking height h would make d(t)=h(τt)-h(t) continuous and nowhere zero. Since the domain circle is connected, d has a constant sign. But summing d(τ^j t) for j=0,…,k-1 telescopes to zero, a contradiction.

## Scope warning
This proves precisely the primitive immersed-loop theorem, not unrestricted sufficiency for arbitrary backtracking walks. The Oberwolfach problem report omits an immersion restriction; that omission alone is not a counterexample. One-edge out-and-back is nonimmersed yet stackable with curved heights, showing original-edge affine restrictions must not be imposed.
