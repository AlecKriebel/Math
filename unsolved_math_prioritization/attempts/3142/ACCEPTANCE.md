# Acceptance of the explicit subdivision-power coloring family

## Decision

**Accept the restricted theorem without mathematical correction.** PROOF.md retains the entire accepted proof and complete 96-entry table. AUDIT.md retains the full six-part independent logical audit and accurately identifies its finite evidence.

This AI-assisted manuscript is unrefereed. Acceptance records an independent internal AI audit, not external human peer review, journal acceptance, or formal proof-assistant certification.

The general 2 Delta + 1 conjecture remains unresolved by this work. No novelty, priority, exhaustive literature-survey, or current-openness claim is made.

## Accepted mathematical scope

Replace every edge uv by the three-edge path u,(u,v),(v,u),v and take its third power. The proof derives the exact terminal and arc constraints from actual subdivision distances. Distinct arcs (u,v) and (w,z) conflict precisely when u=w, v=w, or z=u. Adjacent terminals differ; terminals avoid all incident colors; outgoing colors are pairwise distinct and disjoint from incoming colors.

The base C is the graph on four-bit vectors with XOR differences in {1,2,4,8,15}. Its 16 vertices and 40 edges form a connected, simple, nonbipartite 5-regular graph. The ten unordered pairs of distinct generators represent each nonzero nongenerator once. Every nonadjacent pair has two common neighbors, so C has diameter two and C^2=K16; deleting vertex 0 leaves a square K15.

The unchanged complete table assigns all 16 terminal and 80 ordered internal-vertex colors from a palette of eight. The explicit incoming sets are included beside it. Readers can verify all four constraints from these data. If any d-regular graph admitted at most d+2 colors, its incoming vertices at each vertex would be forced to a singleton color that properly colors its square. With d=5 this excludes seven colors on the base, giving equality eight.

Under the imposed singleton-incoming restriction, the same square coloring forces at least 16 colors on C. The matching construction colors arc (u,v) by v and terminal v by v XOR 3. The weight-two vector 3 is neither zero nor a generator, so all terminal and arc constraints hold. Thus the base singleton value is exactly 16, while its unrestricted value is eight. The eight-color table already uses at most two incoming colors; only vertex 0 has a singleton.

The pullback lemma explicitly requires a graph homomorphism injective on each neighborhood. This retains distinct outgoing arcs and all four constraints. A star-to-edge collapse shows why arbitrary homomorphisms are insufficient.

For every positive integer t, take vertices (x,i) with i modulo t. Copy every base edge within each layer except {0,2}; replace that edge by (0,i)--(2,i+1). Each base edge provides a matching between distinct fibers. This proves simplicity, degree five, local bijectivity, and counts 16t and 40t, including t=1 and t=2. Removing 0--2 from the unit-vector cube preserves connectivity by the alternate path 0--1--3--2. Untwisted edges connect each layer and twisted edges join consecutive layers, proving global connectivity. The untwisted five-cycle 0,1,3,7,15,0 proves nonbipartiteness in every layer.

Projection pulls back the eight-color table. The fifteen nonzero base labels in a fixed layer induce C-0 and yield a K15 in H_t^2. The regular-graph lemma rules out seven colors, proving chi(H_t^(3/3))=8 for every t>=1. The same clique and the pulled-back singleton construction give 15<=chi_vi,1(H_t)<=16. For t>1 the exact singleton value remains undetermined.

These results do not prove the target for all 5-regular graphs or all finite simple graphs. The singleton obstruction does not refute the original conjecture or the two-incoming-color model. No general improvement of the recorded 3 Delta bound is asserted.

## Source dependence and historical finite evidence

Mozafari-Nia and Nejad Iradmusa (2023) supply the fractional-power convention, target, prior special classes and credited incoming-color/square-coloring background. Open Problem Garden records the target. The exact elementary statements needed here are reproved. The audit does not accept every theorem in the source article or certify current literature completeness.

The candidate base check used Floyd--Warshall on the explicit 96-vertex subdivision, checked all 4,560 unordered pairs and all 720 power edges, including 200 terminal-involving edges. The historical candidate cover checks cover exactly t=1,...,16.

The independent checker was separately written using three rounds of Boolean neighbor-union reachability on rebuilt subdivisions. Candidate search and verification programs were not read as source, imported, or executed. For t=1,...,17 and t=31, each historical independent mode checks 12,644,736 unordered subdivision pairs and 132,480 power edges for each of the eight-color and sixteen-color constructions. A separate distance-criterion cross-check covers all 1,099 labeled simple graphs of orders one through five and 115,851 subdivision pairs. Thirteen deliberately incorrect controls were rejected per mode. The retained normal, -O and -OO outputs are byte-identical.

These are finite corroborating checks, not a graph census establishing the unrestricted target. Failed or incomplete searches supply no lower bound. The all-t conclusions follow from the complete written proof.

The complete written proof and the complete 96-entry numerical coloring table are retained. The table, the XOR graph definition, and the four proved constraints make the positive eight-color certificate independently checkable by hand. This is not an executable computational reproduction package: code, raw exhaustive computation records and search outputs, copied source documents and images, and private coordination material are omitted. The historical exhaustive checks are reported as authenticated supporting metadata; their original executions are not rerun or supplied as an executable replay. The all-positive-t theorem and the lower bounds rest on the written arguments, not finite testing or failed searches.

The candidate and independent audit remain unchanged. ACCEPTANCE.json binds the exact original and public documents. This edition includes authored proof/audit/acceptance material and public verification/source metadata only. Preparation performs editorial and byte-integrity checks without rerunning historical mathematical programs or inspecting new scholarly sources.
