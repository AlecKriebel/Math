# Additional structural cases and exact-method boundary

Authored 12 October 2026 UTC. This supplies the complete additional structural proofs used with NEAR_CONSTANT.md. The symbols G, Δ, A, X, O(e), and d(e) have the same meanings.

## 1. Fresh proof of the Δ=2 case

Every connected component with edges in a finite simple graph of maximum degree 2 is a path or cycle. Paths and even cycles have proper edge colorings with two colors. Therefore a non-2-edge-colorable graph of maximum degree 2 contains an odd-cycle component. Edge-criticality then forbids every edge outside this odd cycle, since deleting such an edge would leave the odd cycle untouched. It also forbids a second odd-cycle component for the same reason. Thus, apart from isolated vertices, G is one odd cycle.

Let its cyclically ordered edges be e_1,…,e_m, with m odd. For a nonconstant assignment of two-element lists, some consecutive pair differs. Rotate the cyclic order so L(e_1)≠L(e_m). Equal list cardinalities give a color c∈L(e_1)\L(e_m). Give e_1 color c, and greedily color e_2,…,e_m, always avoiding the color of the preceding edge. There is an available color at each step. The final edge cannot receive c because c∉L(e_m), so the only remaining adjacency is also proper. Every color belongs to its prescribed list. Constant lists fail because the odd cycle is not 2-edge-colorable. This proves the complete Δ=2 assertion by the argument given here.

There is no graph of maximum degree at most 1 satisfying the edge-critical hypotheses.

## 2. A matching plus one exceptional edge

**Theorem.** Suppose Δ≥3 and there is f∈X such that M=X\{f} is a matching. Then G is L-edge-colorable.

**Proof.** If M is empty, color f with an outside color and color G−f using A, which is permitted by edge-criticality. Assume M≠∅. Give each edge m∈M any color from O(m); this is proper because M is a matching.

If L(f)∩A≠∅, choose a proper Δ-edge-coloring of G−M by restricting a coloring of G−m_0 for any m_0∈M. Permute its Δ color names onto A so that f receives a color in L(f)∩A. Every other edge of G−M has list A. Combine with the exterior coloring on M; the palettes are disjoint, so this is a proper list coloring of G.

If L(f)∩A=∅, all Δ colors of L(f) lie outside A. An edge has only two endpoints and meets at most two edges of a matching. Hence at most two colors used on M are forbidden on f. Since Δ≥3, give f another color from L(f). This properly colors all of X using only outside colors. Color G−X using A by restricting any Δ-coloring of G−f, and combine. ∎

This includes arbitrarily large exceptional matchings with one additional edge. The proof uses simplicity only indirectly via the target setting; the fact that one edge meets at most two matching edges also holds in loopless multigraphs.

## 3. Three arbitrary exceptions

**Corollary.** Under the target hypotheses, a nonconstant assignment that differs from a common Δ-set A on at most three edges is list-edge-colorable, with no restriction on the exceptional lists.

For Δ≤2 use Section 1. For Δ≥3, if three exceptional edges contain a disjoint pair, take that pair as M in Section 2. Otherwise they are pairwise incident and are supported on a star or triangle, so Section 2 of NEAR_CONSTANT.md applies. For fewer exceptional edges, the same matching/star arguments apply.

Thus any bad nonconstant assignment must differ from every Δ-set that occurs as a list on at least four edges. This is a necessary condition, not an assertion that four exceptions suffice for a counterexample.

## 4. Sharpness of the uniform deficit/permutation bound

The strict inequality Σd(e)<Δ in NEAR_CONSTANT.md is optimal for a guarantee about *every fixed ordinary coloring and exterior-colored set*. To see the distinction, suppose the remaining exceptional edges e_1,…,e_Δ all have the same ordinary color label i, and let A={a_1,…,a_Δ}. Give e_j the list (A\{a_j})∪{x}, where x∉A. Then Σd(e_j)=Δ, but the allowed set B_i is empty. There is no global permutation of that fixed ordinary coloring that respects all lists.

This is an obstruction only to the selected completion method. Since the e_j have the same ordinary color, they are a matching and can themselves all receive x. It is not a counterexample to Mohar's conjecture.
