# Source-bound comparison with a published restricted hardness construction

Root checkpoint, 2026-10-06 UTC. Priority assessment approximately 65%; PR workflow approximately 50%. No new central proof-search turn is claimed. This is verification of a published construction against the source question and candidate restrictions, not a new proposed solution.

## Full primary material inspected

Romain Chapoullié and Zoltán Szigeti, *On packing time-respecting arborescences*, Discrete Optimization 45 (2022), 100702, DOI 10.1016/j.disopt.2022.100702. The author-hosted journal PDF was retrieved independently by root, extracted, and its printed page 11 was visually inspected including Figure 2. The entire Theorem 13 statement, construction, forward and converse arguments on printed pages 11–12 were read. The private PDF's exact retrieval and hash are in PRIMARY_RETRIEVAL.json. It is not selected for redistribution.

Theorem 13 establishes NP-completeness of finding a spanning rooted arborescence whose directed paths are monochromatic, with an acyclic graph and two colors. Crucially, its proof gives a particular two-level parallel-arc construction from exact cover in 3-regular 3-uniform hypergraphs (RXC3). The following implication uses this proof-level construction; the theorem statement alone would not certify the additional depth and degree bounds.

## Exact published family and notation corrections

Let the RXC3 instance have h vertices and h hyperedges H_i, each hyperedge of size three and each vertex in three hyperedges. The published graph has root s; vertices u_i; element vertices v_j; and overlap vertices w_{ij} for unordered DISTINCT pairs i<j with H_i intersecting H_j. There are two parallel arcs s→u_i, colored black and gray. Each membership arc u_i→v_j is black; both arcs u_i→w_{ij}, u_j→w_{ij} are gray.

The display defining W omits i<j. This convention is unambiguous from Figure 2 (only distinct ordered-with-i<j indices), the |W|≤3h bound, and the converse's explicit j<k. Including self-pairs would break the construction and is not the interpretation used here. The forward proof also writes Z′∩Z″=s while its displayed Z′ and Z″ omit s; these are disjoint nonroot sets, and adding the common root makes that sentence correct. Neither notation defect is imported into our reconstructed argument.

## Polynomial transformation into the literal destination-cost model

For each i, replace the black root arc by s→t_i→u_i and the gray root arc by s→f_i→u_i. Both t_i and f_i are vertices and their sole incoming root arcs are forced in every spanning arborescence. All membership and overlap arcs stay unchanged. The graph is simple, root-reachable, and has consecutive layers {s}, {t_i,f_i}, {u_i}, {v_j,w_{ij}}. Every nonroot indegree is at most three: one for the new selector vertices, two for u_i and overlap vertices, and three for each element vertex.

Give all destination-specific coefficients value zero except:

- For destination v_j, set its coefficient on EVERY s→f_i arc to one.
- For destination w_{ij}, set its coefficient on EVERY s→t_k arc to one.

The cost of an element's root path is one exactly when its chosen membership parent u_i uses the gray selector. The cost of an overlap vertex's path is one exactly when its chosen parent uses the black selector. Therefore a spanning tree has total cost zero iff every element picks a black-selector parent and every overlap picks a gray-selector parent. Compressing the chosen two-arc selector path to its matching original root arc produces precisely a monochromatic spanning arborescence. Conversely any such original arborescence extends by including both forced root-selector arcs and choosing the matching parent of each u_i. The unused selector remains a harmless root leaf. This is a bijection of the parent choices, including positive-cost trees; the selector destinations themselves have zero vector.

For completeness, a zero-cost tree gives an exact cover without relying on notation in the published converse: take ALL black-selected H_i. Every element has a black parent, so these cover every element. If two selected hyperedges intersect, their overlap vertex has only black-selected parents, and hence costs one. Thus selected hyperedges are pairwise disjoint and form an exact cover. Conversely an exact cover selects those u_i black and all others gray; every element has a black parent and every intersecting pair has at least one gray parent. This proves both implications on the published instance family.

Let m=h+|W|. There are 1+3h+m vertices and 4h+3h+2|W| arcs. The dense table is polynomial. All coefficients are binary and the threshold is zero. NP membership is the ordinary finite integer-input certificate check. Because all numerical magnitudes are bounded, the optimization hardness is strong. This recovers the complete restricted theorem claimed in PR107: a simple root-reachable four-layer depth-three DAG, nonroot indegree at most three, binary destination costs, and zero threshold.

For the positive-cost variant, add one to EVERY coefficient, including previously zero vectors. The sum of root-path lengths is constant across every feasible tree: 2h selector paths of length one, h u-paths of length two, and m terminal paths of length three. It equals 4h+3m. Thus costs in {1,2} at threshold 4h+3m give the same equivalence. This is exactly the candidate's universal-offset argument, with h replacing n.

## What this does and does not establish

The restricted candidate result is an elementary corollary of the full published 2022 construction. The paper does not literally print Kaibel's destination-by-arc cost-table formulation; the transformation above is explicitly our audit inference. A direct 3SAT proof and reproducible checker can be useful exposition, but neither establishes a new hardness theorem or a novel resolution of the original question. No substantive new mathematical contribution in PR107 has been established by the current audit.

This is not an assertion of earliest priority, plagiarism, or that every possible refinement of the candidate is already published. Separate priority families are checking older general-objective literature and formulation history. Mathematical soundness of PR107 is independently cleared after the recorded minor repairs. A fresh disposition adversary must still examine this comparison and the proposed no-publication closure before promotion of the classification.
