# The universal at-most-five-exception theorem

Row 1751, problem 3200, OPG 388. Authored synthesis, 12 October 2026 UTC. The theorem below combines independently accepted restricted results. It does not resolve the unrestricted conjecture or establish historical novelty.

## Exact standalone statement

Let G be a finite simple graph, and let Δ be its actual maximum degree. Suppose that G has no proper edge coloring with Δ colors, while G−e has a proper edge coloring with Δ colors for every edge e of G. Let L assign to every edge e a set L(e) of exactly Δ colors. Assume L is nonconstant: at least two edges have different lists.

If there is a Δ-element color set A such that

|{e∈E(G):L(e)≠A}|≤5,

then G has a proper edge coloring c satisfying c(e)∈L(e) for every edge e.

The palette A is arbitrary and need not have been designated as any particular edge's list. All exceptional lists may have arbitrary overlaps, including being disjoint from A. No connectedness, regularity, bounded graph order, exterior-palette-size bound, or prescribed boundary-coloring hypothesis is added. Isolated vertices are immaterial. The colors themselves are arbitrary names.

Nonconstancy is essential. If every list is the same Δ-element set, a list coloring would be a proper Δ-edge-coloring, contrary to the hypothesis. In particular, merely requiring a nonempty exceptional set relative to a palette A is not a substitute for nonconstancy in the uniform statement: a constant assignment with common list B≠A may have a nonempty exceptional set.

## Notation and completion mechanism

Fix A and write X={e:L(e)≠A}, O(e)=L(e)\A and d(e)=|O(e)|. Because every list and A have exactly Δ elements,

d(e)=|O(e)|=|A\L(e)|.

Thus every exceptional edge has a nonempty exterior list. Nonconstancy ensures X is nonempty. For every nonempty F⊆X, a proper ordinary Δ-edge-coloring of G−F exists: restrict a coloring of G−f for any f∈F. If F can be properly colored using its exterior lists, it suffices to permute the ordinary labels onto A so that every residual exceptional edge respects its list. The two palettes are disjoint.

The strict residual-deficit condition ∑_{e∈X\F}d(e)<Δ ensures such a permutation. Under a uniformly random bijection of the Δ ordinary labels onto A, a residual edge violates its list with probability d(e)/Δ. The union bound is less than one, so a successful permutation exists. This argument uses no independence of the bad events. A failure of this sufficient test or of one fixed ordinary coloring is not a bad-list counterexample.

## Proof by degree and exceptional-set size

### Maximum degree at most one

A finite simple graph with maximum degree zero has no edges and admits its empty proper coloring. With maximum degree one it is a matching, possibly with isolated vertices, and admits a one-edge-coloring. Neither case satisfies the assumed non-Δ-edge-colorability. This part of the theorem is vacuous.

### Maximum degree two

Every nonisolated connected component is a path or a cycle. Paths and even cycles are two-edge-colorable, so G must contain an odd cycle. Criticality forbids any edge outside that odd cycle: deleting such an edge would leave the odd cycle and fail to make the graph two-edge-colorable. Hence, apart from isolated vertices, G is one odd cycle.

List its edges cyclically as e₁,…,e_m, with m odd. Nonconstancy supplies an adjacent unequal pair of two-element lists; rotate the order so L(e₁)≠L(e_m). Choose c∈L(e₁)\L(e_m), color e₁ with c, and color e₂,…,e_m successively, each time avoiding the preceding color. Each two-element list gives a choice. The last edge cannot receive c, so its adjacency to e₁ is proper too. This proves the degree-two assertion for every nonconstant assignment, even without a bound on the number of exceptions.

This is the accepted [first-round odd-cycle proof](../3200_critical_list_partials_20261012/ADDITIONAL_CASES.md), restated here in full.

### One through four exceptions in degree at least three

Apply the accepted [four-exception theorem](../3200_critical_list_partials_20261012/FOUR_EXCEPTIONS.md), with its explicit setting and nonconstancy requirements. Its elementary at-most-three branch is in [ADDITIONAL_CASES.md](../3200_critical_list_partials_20261012/ADDITIONAL_CASES.md), and its strict deficit and star inputs are in [NEAR_CONSTANT.md](../3200_critical_list_partials_20261012/NEAR_CONSTANT.md). The complete [first-round structural audit](../3200_critical_list_partials_20261012/AUDIT_NEAR_CONSTANT.md) and [integrated statement clarifications](../3200_critical_list_partials_20261012/STATEMENT_CLARIFICATIONS.md) establish the exact accepted form. These are explicit mathematical dependencies, not newly rerun audits in this synthesis.

### Exactly five exceptions in degree three

Apply the complete symbolic proof in [SUBCUBIC.md](SUBCUBIC.md), accepted in [AUDIT_SUBCUBIC.md](AUDIT_SUBCUBIC.md). Its direct lemmas and exhaustive symbolic cases handle the number h=0,1,2,3,4,5 of exceptional edges having deficit at least two. The proof uses the strict deficit condition, two exact equality criteria and deliberately selected deletion colorings. It neither assumes extension of an arbitrary boundary coloring nor depends on a computational list of supports or on the earlier large exterior-certificate classification.

### Exactly five exceptions in degree at least four

If all five exceptional edges share one endpoint, use the accepted arbitrary-star theorem. Its complete proof is restated in the next section. A five-edge star cannot occur at actual maximum degree four.

Otherwise apply the symbolic nonstar five-edge partial-coloring lemma proved in [HIGHER_DEGREE.md](HIGHER_DEGREE.md) and accepted in [AUDIT_HIGHER_DEGREE.md](AUDIT_HIGHER_DEGREE.md). It selects a nonempty exterior-colorable F such that either the residual total deficit is at most three, or exactly two residual edges remain, they are incident, and both have deficit two.

The first outcome is strict for every Δ≥4. The second outcome is strict for Δ≥5. At Δ=4, the incident residual edges have distinct ordinary labels, and their allowed subsets of A each have size two. Choose different representatives for those two sets and extend the resulting map to a permutation of the four ordinary labels onto A. No other residual list differs from A. The exterior and ordinary pieces combine to give a proper L-edge-coloring.

This covers every possible actual maximum degree and every permitted exceptional-set size, proving the theorem. ∎

## The inherited arbitrary-star dependency, with full proof

Suppose the nonempty exceptional set X lies in one star. In the bipartite graph of exceptional edges and exterior colors, join e to every color in O(e). Take any inclusion-maximal matching, and let F be the matched exceptional edges, r=|F|≥1. Color F with its r distinct matched exterior colors.

For every remaining exceptional edge e, every color of O(e) is already among those r matched colors; otherwise an unmatched edge and unmatched exterior color could be added to the matching. Therefore its permitted palette set A∩L(e) has size at least Δ−r. In an ordinary coloring of G−F the t=|X\F| remaining star edges have distinct labels. Also t≤Δ−r because the whole star contains at most Δ edges. Their allowed palette sets thus each have at least t colors. Greedily choose distinct representatives for the t sets, assign these to the corresponding distinct ordinary labels and extend to a bijection of all Δ labels onto A. Combine with the exterior colors on F. This gives a proper L-edge-coloring.

Maximality, rather than maximum matching size, is sufficient. The proof permits arbitrary exceptional-list overlaps. The original complete accepted argument appears in [NEAR_CONSTANT.md](../3200_critical_list_partials_20261012/NEAR_CONSTANT.md), Section 2; its independent recheck is also retained in AUDIT_HIGHER_DEGREE.md.

## Consequence and acceptance boundary

A hypothetical bad nonconstant exact-Δ-list assignment on a graph satisfying the criticality hypotheses must differ from every Δ-element palette on at least six edges. In particular, it differs from every Δ-set occurring as a list on at least six edges. This necessary condition asserts no existence of a counterexample. Degree two is fully settled by the odd-cycle proof; the unresolved part concerns more general assignments in higher degrees.

The exactly-five symbolic arguments are the basis of acceptance. The reported author and independent computational checks corroborate them and have their own bounded domains; they are not premises of the universal theorem. No omitted large classification, raw certificate list, copied external proof or finite experiment is being substituted for an authored proof.

The unrestricted critical-edge-list conjecture remains unresolved by this work. Literature inspection is bounded and does not certify present-day openness or historical priority.
