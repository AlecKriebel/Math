# Checkable prior corollary for every advertised hardness restriction

Timestamp: 2026-10-06 04:22 UTC. Completion estimate: 70%. This is an explicit model translation for a priority audit, not a new attempt to prove the target.

## Primary premise

Chapoullié and Szigeti, *On packing time-respecting arborescences*, Discrete Optimization 45 (2022), 100702, DOI [10.1016/j.disopt.2022.100702](https://doi.org/10.1016/j.disopt.2022.100702), [arXiv 2203.01096](https://arxiv.org/abs/2203.01096). Full public [author PDF](https://pagesperso.g-scop.grenoble-inp.fr/~szigetiz/OCG/13.C-Szigeti.pdf). Theorem 13 and its entire proof are on printed/PDF pp.11–12; the spanning out-arborescence convention is in Section 2, p.2.

Theorem 13 proves NP-completeness of finding one spanning fixed-root arborescence whose root paths are monochromatic, even in an acyclic directed graph with two colors. Its reduction from exact cover in 3-regular 3-uniform hypergraphs uses two differently colored parallel root arcs into each hyperedge vertex u_i. Element vertices v_j receive black arcs from incident hyperedge vertices; each intersecting hyperedge pair has a vertex w_{i,j} receiving two gray arcs from that pair. The element vertices have indegree three, and pair vertices indegree two. This is a full primary proof, not an abstract-level analogy. The construction's mechanism is a binary parent choice at u_i that is shared by every descendant path.

The arXiv v1 was publicly submitted on **2 March 2022 at 13:32:07 UTC**, and its full text contains Theorem 13 and this reduction. The journal issue is August 2022. These are evidence-backed dates, not an assertion of earliest historical priority.

### Source notation defects and intended convention

The displayed definition of W omits the condition i<j. We use exactly one pair vertex for each **distinct unordered intersecting pair**:

    W={w_{i,j}: 1<=i<j<=h and H_i intersects H_j}.

The source's Fig. 2 visibly lists only such pairs, its bound |W|<=3h counts unordered pairs, and its final converse uses j<k. Literal inclusion of self-pairs would make its yes-construction false, so that omission cannot be silently inherited. Fig. 2 was rendered and visually inspected from the public PDF; its six-hyperedge example has fourteen pair vertices, including no self-pairs or ordered duplicates. The printed expression Z' intersect Z''=s also omits r from its displayed vertex sets; the intended two branches are disjoint outside their common root. Neither shorthand is needed in our proof: the explicit arborescence construction below avoids both. These are narrow notation repairs supported by the full proof and figure, not a new unsupported hardness premise.

The underlying RXC3 premise was also checked in the cited Gonzalez (1985) primary article: Section 3 defines 3-element subsets with every element occurring exactly three times, and Appendix A, Theorem A.1, establishes NP-completeness. [Public full text](https://www.cs.columbia.edu/~verma/classes/uml/ref/clustering_minimize_intercluster_distance_gonzalez.pdf), printed pp.297 and 305–306, DOI [10.1016/0304-3975(85)90224-5](https://doi.org/10.1016/0304-3975(85)90224-5).

## Our explicit translation

Fix a source instance produced by that prior reduction. Write U={u_1,...,u_h}, V={v_1,...,v_h}, and W for the pair vertices. These names are merely labels in the input to the transformation. Its two root-arc choices at u_i are denoted B_i and G_i. All arcs into an element destination belong to its B category; all arcs into a pair destination belong to its G category. Every vertex in V union W is a sink. These input facts are sufficient for the following transformation; no assertion about an arbitrary colored digraph is needed.

Create two new vertices b_i,g_i for every i. Replace B_i by r->b_i->u_i and G_i by r->g_i->u_i. Keep all arcs from U to V union W, and discard the colors after recording the categories. The resulting layers are

    L0={r}, L1={b_i,g_i}, L2=U, L3=V union W.

For each destination v_j in V, define c^{v_j}_{r->g_i}=1 for every i, and set every other entry in that destination's vector to zero. For each destination w in W, define c^{w}_{r->b_i}=1 for every i, and set every other entry to zero. For each destination b_i,g_i,u_i, use the identically zero vector. This is an arbitrary destination-by-arc table of exactly the kind allowed by OWR Problem 2. Threshold is zero; no capacities, minimax aggregation, or local transition prices have been introduced.

## Bijection and exact cost test

Every new b_i and g_i has its root arc forced, because that is its only incoming arc. Every u_i selects exactly one of b_i->u_i and g_i->u_i. Replace that selected two-arc route by B_i or G_i, respectively. Every sink selects one of its incoming U arcs. These choices give exactly one source arborescence. Conversely, every source arborescence gives exactly one new arborescence after inserting both forced root arcs and the selected parent into u_i. The unused b_i or g_i is simply a leaf. The graphs are acyclic and every nonroot vertex has exactly one selected incoming arc, so all vertices are connected to r and there are no hidden feasibility assumptions.

For any element destination v_j with selected parent u_i, its new root path is r->b_i->u_i->v_j or r->g_i->u_i->v_j. Its path price is respectively zero or one. Its corresponding original root path is monochromatic exactly in the zero case. For a pair destination w with selected parent u_i, its new path price is zero exactly when u_i uses g_i, which is exactly the original monochromatic condition for that sink. Original root paths ending at u_i have only one arc and are automatically monochromatic; the new b_i,g_i,u_i destinations have price zero regardless of their choice. Therefore, for every matched arborescence,

    C_new(T)=number of non-monochromatic original root-to-sink paths.

In particular C_new(T)=0 if and only if every source root path is monochromatic. Nonnegative prices ensure that summation cannot cancel violations. This proves a polynomial many-one reduction from the prior NP-complete problem to the exact target at threshold zero.

For completeness without the source's Z-set shorthand, start with an exact cover and select b_i->u_i exactly for its hyperedges, g_i->u_i for the rest. Every element destination has a covering parent with the b choice. Every intersecting distinct pair has at least one endpoint outside the cover, so its pair destination has a parent with the g choice. Choose those parents and all forced root arcs. This spans every vertex and every destination price is zero.

For soundness without the source's chosen-set notation, start with any new zero-cost tree and take **all** hyperedges whose u_i parent is b_i. Every element destination has some selected parent of this kind, so they cover the universe. If two selected hyperedges intersect, their pair destination must choose one of those two u parents and would pay one, contradicting zero total cost. Thus all selected hyperedges are pairwise disjoint and form an exact cover. This directly checks the prior reduction mechanism and the objective translation for every input size.

## Advertised restriction checks

| Feature | Translation check |
|---|---|
| One fixed root | The prior root becomes r. |
| Spanning, unique directed root paths | Exact parent-choice bijection above; both new literal vertices are spanned. |
| Sum of destination-specific path costs | Each sink alone charges its incompatible first root arc; non-sinks are free. |
| Simple digraph | The only parallel arcs were B_i,G_i; their distinct subdivisions remove them. Other arcs connect distinct pairs in the prior construction. |
| Root reachable | Each b_i,g_i is direct; each u_i has a two-arc route; each element is incident to three hyperedges and each pair to two. |
| Depth three/four layers | Every arc goes L_k to L_{k+1}, k=0,1,2. |
| Nonroot indegree at most three | L1 has one, U two, element sinks three, pair sinks two. |
| Binary costs | Every explicitly encoded entry is 0 or 1, with no exceptional entries. |
| Polynomial size | There are 1+3h+h+|W| vertices and 4h+3h+2|W| arcs; the dense table is polynomial too. |

Adding one to every destination-by-arc entry gives only 1 and 2. Every new tree has 2h paths of length one, h of length two, and h+|W| of length three. Thus all objectives rise by exactly

    K=4h+3(h+|W|).

Zero feasibility becomes feasibility at threshold K. Consequently the strictly positive-cost claim is also a direct prior corollary with the identical 4n+3m structure, where n=h and m=h+|W|. This offset does not rely on the prior graph's variable-length behavior, because our explicitly constructed new graph has fixed layers.

## What this proves about priority

The 2022 paper does not state OWR Problem 2 verbatim and should not be described as its explicit published solution. The exact broad and restricted binary hardness conclusions nevertheless follow by the elementary translation above. A discovery claim for the candidate's hardness theorem therefore needs correction. The candidate's exact minimum-unsatisfied-clause identity for **every cleaned general 3SAT formula** is a formally stronger reduction property than threshold-existence equivalence. The 2022 paper does not print that identity, and our translation alone does not prove its exact historical priority. The oriented PACE gadget admits analogous clause accounting for monotone formulas, and the translated 2022 gadget admits analogous accounting for its cover/exclusion formula. The candidate's mixed-sign formulation remains an explicit verified correspondence, with priority of that exact property unresolved. Independent clause-parent minimization explains why it is immediate once the gadget is fixed; no substantive discovery is thereby established on present evidence.

The 2013 PACE appendix supplies an earlier SAT label-consistency construction; it has notation and proof wording defects and is therefore supporting mechanism evidence rather than the decisive premise of this audit. The clean full primary 2022 theorem is sufficient to defeat novelty of all listed hardness restrictions.
