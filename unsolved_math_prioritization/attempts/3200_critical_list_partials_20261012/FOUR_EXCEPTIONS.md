# Four arbitrary exceptional lists

Authored 12 October 2026 UTC. This is a restricted theorem in the setting and notation of NEAR_CONSTANT.md. No novelty or full-target claim is made.

## Theorem

Every nonconstant Δ-list assignment on a finite simple Δ-edge-critical graph that differs from some common Δ-set A on at most four edges admits a proper list-edge-coloring. The lists on those four edges can be arbitrary Δ-sets.

Equivalently, any counterexample to the unrestricted conjecture must differ from every Δ-set occurring as one of its lists on at least five edges.

## Elementary ingredients

We use the following fully elementary facts.

1. Any three pairwise distinct objects with lists of sizes at least 2,2,3 can be assigned three distinct colors: choose distinct colors for the two objects with smaller lists, then choose a third color for the object with at least three options. Therefore three edges with outside-list sizes at least 2,2,3 can always be properly exterior-colored, regardless of their incidence.
2. A graph on three vertices that is not a triangle is a forest. Any lists of size at least two admit a proper vertex coloring, by repeatedly removing and then restoring a leaf. Thus three edges that are not pairwise incident can be properly colored from arbitrary outside lists of size at least two.
3. A graph on four vertices other than K_4 is 2-degenerate: it has a vertex of degree at most two, and after removing it every remaining graph has at most three vertices and hence minimum degree at most two. Consequently arbitrary lists of size at least three color it greedily in reverse removal order.
4. Four pairwise incident edges in a simple graph lie in one star, by the star-or-triangle classification proved in NEAR_CONSTANT.md. In particular, a simple subcubic graph cannot contain four pairwise incident edges.
5. The deficit theorem in NEAR_CONSTANT.md says that it suffices to exterior-color a nonempty F⊆X while leaving total deficit Σ_{e∈X\F}d(e)<Δ. Exterior colors always lie outside A. All uses below explicitly check this strict inequality.

For ingredient 1, if all three lists have size≥3, arbitrarily designate one as the third object. For ingredient 2, fewer adjacencies only help. These facts concern the line graph on the selected edges, not a vertex coloring of the original graph.

## Proof for Δ=3

The case of at most three exceptions has already been proved in ADDITIONAL_CASES.md, and Δ≤2 is fully handled there. Assume Δ=3 and |X|=4. Each deficit d(e) lies in {1,2,3}. Call an exceptional edge large when d(e)≥2, and let h be the number of large edges. The line graph H on the four exceptional edges is not K_4 by ingredient 4.

- h=0. Since H is not K_4, two exceptional edges are disjoint. Exterior-color those two edges arbitrarily. The two remaining deficits sum to 2<3.
- h=1. Exterior-color the unique large edge and any one other edge. Color the latter first; the large edge has at least two outside colors and can avoid that color if the two edges are incident. Two deficit-1 edges remain, with sum 2<3.
- h=2. Exterior-color the two large edges. Two lists each of size at least two permit distinct colors if necessary. Again the residual deficit is 2<3.
- h=3. Let a denote the sole deficit-1 edge. If one of the three large edges has deficit 3, exterior-color all three large edges using ingredient 1; the residual deficit is 1<3. If all three have deficit 2 and they are not pairwise incident, use ingredient 2, with the same residual deficit. It remains that the three large edges are pairwise incident and all have deficit 2. Since H is not K_4, a is disjoint from at least one large edge b. Choose any other large edge c. Exterior-color a with its sole outside color, then color c avoiding the color of a if necessary, then color b avoiding the color of c. Edge b is disjoint from a, and has two outside colors, so this succeeds. The fourth edge is large with deficit 2, which is <3.
- h=4. If all deficits are 2, choose two disjoint exceptional edges and any third edge. They are not pairwise incident, so ingredient 2 exterior-colors these three edges, leaving residual deficit 2<3. If both values 2 and 3 occur, leave one deficit-2 edge uncolored. The other three have lists of size at least 2,2,3, so ingredient 1 exterior-colors them, again leaving deficit 2<3. Finally, if all deficits are 3, ingredient 3 colors all four exceptional edges from their outside lists because H≠K_4. The residual deficit is 0<3.

In every case ingredient 5 completes an L-edge-coloring of G.

## Proof for Δ≥4

Again assume |X|=4, since fewer exceptions are covered by ADDITIONAL_CASES.md. Define large edges by d(e)≥2.

- h=0 or h=1. Exterior-color an exceptional edge of maximum deficit. Every remaining edge has deficit 1, so the residual sum is 3<Δ.
- h=2. Exterior-color the two large edges, which have outside lists of size at least two. The residual sum is 2<Δ.
- h=3. If some large edge has deficit at least 3, exterior-color all three large edges by ingredient 1 and leave residual sum 1<Δ. Otherwise all three large deficits are 2. Exterior-color any two of them, leaving deficits 2 and 1, with sum 3<Δ.
- h=4. First suppose all four deficits are 2. If the four exceptional edges are pairwise incident, they are supported on one star and the star theorem in NEAR_CONSTANT.md applies directly. Otherwise choose a disjoint pair and a third edge; ingredient 2 exterior-colors the selected triple, leaving residual deficit 2<Δ. Next suppose some deficit is at least 3, and the minimum deficit is less than Δ. Leave a minimum-deficit edge uncolored. At least one of the three remaining edges has deficit at least 3, while all have deficit at least 2. Ingredient 1 exterior-colors them, and the remaining deficit is <Δ. Finally, if the minimum deficit equals Δ, all four outside lists have size Δ≥4. Assign distinct outside colors greedily to all four exceptional edges. The residual deficit is 0.

The deficit theorem completes every case not already handled by the star theorem. This proves the four-exception assertion. ∎

## Additional direct corollary: Δ+1 one-color substitutions

For a nonconstant assignment, if Δ≥3 and every exceptional list differs from A by exactly one replacement, then |X|≤Δ+1 suffices. The case |X|≤Δ is already in NEAR_CONSTANT.md. If |X|=Δ+1, the exceptional edges cannot all be pairwise incident: a star has at most Δ edges and a triangle only three. Choose a disjoint pair as F, exterior-color it arbitrarily, and note that the remaining total deficit is (Δ+1)−2=Δ−1<Δ. The case Δ=2 follows from the full odd-cycle proof.

This last corollary and the four-arbitrary-exception theorem are incomparable when Δ≥4: one controls list changes by deficit and the other by exceptional support size.
