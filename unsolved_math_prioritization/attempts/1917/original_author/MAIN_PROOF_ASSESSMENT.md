# First-pass assessment of the main proof chain

Source: [Okechukwu, arXiv:2609.20871v1](https://arxiv.org/html/2609.20871v1). The entire manuscript was text-inspected; the main chain in Sections 1–5 was mathematically checked in the following bounded sense. PDF pages 2, 19 and 20 were also visually inspected. No fatal defect was identified. This document is an authored audit of calculations and logical interfaces, not a replacement exposition or final independent acceptance.

## 1. Elimination and extremal arithmetic (pages 3–6)

The rooted-to-ordered equivalence survives deletion, including an empty root. The reverse implication needs the condition in every induced subgraph, not merely one ordering. The forbidden configuration argument counts missing endpoints in a clique and then uses an independent common-neighbour set. For defect zero this specializes to the induced four-cycle obstruction.

The edge-colouring palette Δ+d is safe: on restoring an edge at the removed vertex, fewer than Δ+d colours are forbidden. Balancing two colour classes by interchanging an alternating path decreases the sum of squares; cycles and even paths cannot account for a size discrepancy of at least two.

The quadratic optimization and modular edge-colouring construction were recomputed. The latter spends each core edge once and each spoke at most once. A finite verification program tests these counts and rejects overlapping or incomplete candidate partitions. These checks corroborate examples; they do not bound all chordal graphs.

## 2. Signed fractional step (pages 6–11)

The edge-equality primal requires unrestricted signed dual variables. Replacing it by a nonnegative covering dual would not justify the argument. The chosen positive clique-star is compatible with an elimination order ending in its clique. Each exterior edge is counted at its first endpoint. Adding only exterior negative mass converts that part of the sum to a positive sum, while preserving the signed core contribution.

I checked the two-case bound: in the large-core range, the triangle and four-clique inequalities produce affine bounds meeting at α=5c/12, and the resulting quadratic is at most 25n²/192. In the other range, completing the square gives the required positive deficiencies. No positivity assumption was silently imposed on core weights.

The random cover in Lemma 3.2 is not an edge partition. The displayed correction for repeated negative weights is essential and has the correct sign. A pair lies in the same random block with probability at most (L−2)/(|U|−1). This remains valid when the final block is smaller. The subsequent localization estimates account for missing spokes and low-weight spokes separately; adjacent good rows force a negative row-edge weight. The parameter choices occur in a consistent order.

The rounding lemma packages multiple clique sizes into one fixed disconnected template. At a fixed vertex, clique-packing mass is at most (n−1)/2, since each component has order at least three. Excluding the bounded vertex set already used by a bundle therefore loses O(n) mass. Taking a threshold over finitely many templates makes the error uniform. This avoids treating independently rounded sizes as edge-disjoint. The template and cutoff are fixed before the limit n→∞. The packing approximation's applicability, including disconnected templates and non-induced copies, was checked against Yuster's introductory conventions and Theorems 1.1–1.2. Its deep proof was not re-proved.

## 3. Integral construction (pages 11–14)

For the split palette, the bipartite lists have at least the maximum degree, while internal lists exceed the number of conflicting edges. Actual core edges are a subset of the abstract pairs being coloured. Proper edge colours therefore forbid reuse of a spoke. The first exterior-edge triangles and the later core-edge triangles are built in a common residual graph; the latter's increased deficiency includes the cross edges already spent. No assertion that edge deletion preserves chordality is needed.

For the exceptional vertices, a jointly maximum family of edge-disjoint matchings is individually maximum after removing the others. The unmatched rectangle contains at most tL available original edges already spent elsewhere. This yields L²−tL≤D and L≤sqrt(D)+t. In the final count, −D+2t sqrt(D)≤t² and the remaining O(t²) costs fit the stated error. The bound needs t bounded later; treating it as o(n) would not suffice for the same finite argument.

## 4. Bounded exceptional set and rigidity (pages 14–19)

This is the most consequential interface for a fresh reviewer. The nonedge-matching pigeonhole argument produces a fixed number of missing pairs and a linear common-neighbour set. Its independence conclusion uses chromatic number at most clique number plus the fixed defect. Sparse exterior edges imply clique number o(n), so this step is available. Promoted near-universal rows are made into a clique by placing both endpoints of a bounded complement matching into the exceptional set. They are not returned to the exterior. The normal form preserves the required column deficiency and a strict maximum-degree saving.

The incidence estimate counts edges at their earlier endpoint in an order ending in the clique. The strict missing-core-neighbour inequality makes every largest forward clique at a row avoid the exceptional vertices; it bounds both possible edge directions. The limiting finite optimization was checked case by case. Compactness is applied only after the exceptional-set size has been made uniformly bounded. Rows with large core deficiency are discarded in number o(n), so restoring their incidences with boundedly many exceptional vertices costs only o(n).

The argument then constructs a fresh cut of the original graph. Preliminary matchings used to obtain a numerical inequality are not retained. This avoids double-counting consumed edges in the final exact construction. Both palette inequalities have strictly positive normalized slack for λ=1/[100(s+1)] and ρ=λ/100. The coefficient of the remaining exterior-edge count is strictly positive. Equality in the resulting finite inequality therefore forces zero missing cross edges, zero exterior edges and exactly the prescribed core edges. The arithmetic maximum has the asserted nearest-integer choices. These observations are compatible with the claimed classification; no exhaustive graph or formal verification was performed.

## 5. Removal of minimum-degree hypothesis (pages 19–20)

For a fixed integer allowance K, a smallest-order counterexample has every one-vertex deletion below that allowance. Adding incident edges as singleton parts is valid regardless of which clique partition was used in the deletion. Integrality therefore gives minimum degree at least Q_s(n)−Q_s(n−1)+1. The exact difference is floor((n+s+1)/3), so the resulting sequence meets the rigidity proposition's minimum-degree requirement. An unbounded excess forces the orders to tend to infinity. This proves bounded excess if the rigidity proposition is correct; the argument is not assuming the desired constant first. Only after this constant is established is it used to derive eventual exactness. This order avoids circularity.

## Imported results and uncompleted checks

- Dirac's simplicial-pair characterization is used for the chordal bridge. Its original 1961 article was not retrieved or re-proved.
- Linear programming strong duality is standard finite-dimensional input; no formal LP development was reproduced.
- Galvin's bipartite list edge-colouring theorem is applied to a finite simple bipartite graph with every list at least its maximum degree. This is the standard theorem, but the original 1995 full text and exact theorem numbering were not verified here.
- Yuster's primary preprint, math/0305350v4, pages 1–3, confirms the approximation statement, graph conventions and uniform quantifier needed for the fixed template. The proof of this deep result and its regularity/matching dependencies was not independently re-proved. Haxell–Rödl's original article was not inspected.
- The 1993 problem paper was verified only at primary publisher-abstract level. The 1994 split-graph paper and June 2026 comments were background only and are not inputs to the new claim.
- Sections 6–7 were read for scope and the unresolved finite-order distinction. Their auxiliary signed theorem, maximum-cut corollary, all-order conjecture and complete equality classification are not independently certified in this packet.
- No peer review, formal verification, exhaustive computation, explicit universal threshold or comprehensive novelty search is claimed. The finite verifier checks specified arithmetic/examples and metadata, never the asymptotic theorem.

## Assessment

The statement bridge is exact. The main proof chain is substantive and appears internally coherent in this pass. The strongest warranted disposition remains PRIOR_CLAIM_PENDING_INDEPENDENT_AUDIT. An independent reviewer should concentrate on the bounded-exception and exact-rigidity steps, the uniformity in fractional rounding, and the external list-colouring/packing interfaces before accepting a prior resolution.
