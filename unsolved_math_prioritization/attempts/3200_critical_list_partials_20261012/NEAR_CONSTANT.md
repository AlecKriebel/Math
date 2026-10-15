# Near-constant lists on edge-critical graphs

Status: accepted restricted theorems, with the required statement corrections integrated, 12 October 2026 UTC. This is not a full resolution of Mohar's conjecture and no novelty claim is made.

## Exact setting

Let G be a finite simple graph with maximum degree Δ. Assume that G is not Δ-edge-colorable and that G−e is Δ-edge-colorable for every edge e. Every list L(e) has exactly Δ colors. The conjecture asks whether every nonconstant L is colorable. The constant assignments are necessarily bad.

Fix any Δ-element color set A, and put X={e: L(e)≠A}, O(e)=L(e)\A, and d(e)=|O(e)|=|A\L(e)|. Lists equal to A outside X are called the common lists. If X is nonempty, every exceptional edge has at least one outside color.

## 1. Exact palette-permutation criterion

Let F be a nonempty set of edges that has a proper coloring ψ with ψ(f)∈O(f) for every f∈F. Let φ:E(G−F)→{1,…,Δ} be any proper Δ-edge-coloring; such φ exists by restricting a coloring of G−f for any f∈F. Define

B_i = A ∩ ⋂_{e∈X\F: φ(e)=i} L(e),

where an empty intersection means B_i=A. If the family (B_1,…,B_Δ) has a system of distinct representatives a_i∈B_i, then G has a proper L-edge-coloring: use ψ on F and use a_{φ(e)} on E(G−F). The first part uses only colors outside A, the second only colors inside A, so there are no conflicts between the parts. Each part is proper. Every prescribed list is respected by construction.

The SDR condition is equivalent to |⋃_{i∈I}B_i|≥|I| for every I⊆{1,…,Δ}, by Hall's theorem. This criterion is sufficient, not asserted necessary for L-colorability. It is necessary and sufficient only for completing this chosen exterior coloring by a single global permutation of this chosen ordinary coloring φ.

## 2. Arbitrary exceptional lists on one star

**Theorem.** If the nonempty exceptional set X is contained in the edges incident with one vertex, then G is L-edge-colorable.

**Proof.** Greedily choose a maximal matching in the bipartite incidence graph whose left vertices are X, whose right vertices are the colors outside A, and where e is adjacent to c when c∈O(e). Let F⊆X be the matched edges, let r=|F|≥1, and assign each f∈F its distinct matched outside color. This is a proper coloring of F, even though its edges are incident. Maximality implies that for every e∈X\F every color of O(e) is among the r matched colors. Thus |A∩L(e)|=Δ−|O(e)|≥Δ−r.

Restrict a proper Δ-edge-coloring of G−f, for any f∈F, to G−F. The t=|X\F| remaining exceptional edges receive pairwise distinct ordinary colors, since they are incident with the same vertex. Also t≤Δ−r because |X|≤Δ. Their corresponding allowed sets A∩L(e) each have at least Δ−r≥t elements. These t sets have an SDR: greedily choose a different representative in each, or apply Hall. Assign these representatives to the t distinct ordinary labels that occur on X\F, and extend to a bijection from all Δ ordinary labels to A. This is exactly the criterion in Section 1 and completes the proof. ∎

The matching above need only be inclusion-maximal, not maximum.

**Clique extension.** The identical proof works when X is pairwise incident and |X|≤Δ. In a simple graph a pairwise-incident edge family is contained in a star or a triangle: take uv and uw; any edge not through u must be vw, and an additional edge meeting all three must belong to the triangle. Therefore the theorem also treats arbitrary exceptional lists supported on one triangle when Δ≥3. For Δ=2 the critical graph's unique edge-containing component is an odd cycle, proved in full in ADDITIONAL_CASES.md, Section 1.

Consequently every nonconstant assignment differing from a common Δ-set on at most two edges is colorable: disjoint exceptional edges have an exterior coloring immediately; incident ones satisfy the theorem. This strictly extends the earlier exceptional-matching argument, which by itself cannot color two adjacent exceptional edges whose only outside color is the same color.

## 3. A deficit bound with arbitrary exceptional support

**Theorem.** Let F be nonempty and properly colorable from its outside lists O(f). If

Σ_{e∈X\F} d(e) < Δ,

then G is L-edge-colorable.

**Proof.** Fix an ordinary Δ-edge-coloring φ of G−F and choose a uniformly random bijection π from its Δ labels to A. For each remaining exceptional edge e, the probability that π(φ(e))∉L(e) is d(e)/Δ. By the union bound, the probability of at least one violated list is at most Δ^{-1}Σ d(e)<1. Hence some permutation violates none. Combine it with the exterior coloring of F, whose palette is disjoint from A. ∎

The proof does not require independence of the bad events. It applies to arbitrary critical graphs and arbitrary positions of exceptional edges.

**Single-edge corollary.** It suffices that

Σ_{e∈X}d(e) − max_{e∈X}d(e) < Δ.

Choose an exceptional edge with largest deficit, and color it with any outside color. In particular, any assignment obtained from a constant Δ-list assignment by replacing one color in each of between one and Δ edge lists is colorable, with no restriction on where those edges lie.

**Obstruction forced by the theorem.** If L is a counterexample and A is any Δ-set occurring as one of its lists, then X cannot be a matching, cannot be supported on one star or triangle, and must satisfy Σd(e)−max d(e)≥Δ. These are necessary conditions only and do not establish existence of a counterexample.

## 4. Boundary

Sections 2 and 3 extend the exceptional matching case but remain restricted near-constant-list theorems. General Δ≥3 and arbitrary nonconstant assignments are unresolved in this work. The original homepage's reversed iff sign is a known wording error and is not used as a counterexample.

## Sources

- Bojan Mohar, original July 2001 problem: https://www.sfu.ca/~mohar/Problems/P7ListEdgeCriticalGraphs.html . Directly inspected.
- Open Problem Garden, posted 12 June 2007: https://www.openproblemgarden.org/op/list_colorings_of_edge_critical_graphs . Intended nonconstant-list problem directly inspected.
- Hemanshu Kaul and Jeffrey A. Mudrock, *Criticality, The List Color Function, and List Coloring the Cartesian Product of Graphs*, arXiv:1805.02147v2 (7 August 2018), Conjecture 6, printed page 11: https://arxiv.org/pdf/1805.02147v2 . The line-graph reformulation and exact definitions were directly inspected. Their (Δ+1)-edge-critical indexing refers to the chromatic index. Their compressed defining sentence does not separately repeat non-Δ-edge-colorability; the explicit non-Δ-edge-colorability hypothesis above is essential and is taken from the original problem.

All mathematical arguments in Sections 1–3 are provided in full here. Hall's finite marriage theorem is the only named general combinatorial input; the special use in Section 2 also has the indicated greedy proof. No claim of historical priority is made.
