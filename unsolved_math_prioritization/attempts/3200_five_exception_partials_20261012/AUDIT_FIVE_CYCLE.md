# Independent audit of the second five-exception coloring packet

Date: 12 October 2026 UTC. Target: row 1751, problem 3200.

## Verdict and exact scope

Accepted as restricted mathematical results, with no correction required to the two audited mathematical texts, distributed in this prose edition as FIVE_CYCLE.md and KEMPE_REPAIR.md. Original input identities are omitted; MANIFEST.json identifies the actual distributed files.

The candidate proves that every nonconstant three-list assignment whose five exceptional edges form a 5-cycle is colorable in the stated edge-critical setting. It also proves colorability for five one-color substitutions on arbitrary subcubic support when their omitted base colors are not all equal. Its equality-case Hall classification, five-boundary-color lemma, explicit method obstructions and completion-equivalence observation are correct. The supplement verifies one explicit Kempe repair; it makes no general one-switch assertion.

This is a separate acceptance from the first-round audit. It neither changes the first-round packet nor certifies any separate normalized-family enumeration or obstruction-classification packet. The unrestricted assertion for five arbitrary lists on arbitrary support remains unproved here. Neither historical novelty nor resolution of Mohar's full conjecture is claimed.

## Hypotheses and accepted first-round input

G is finite and simple, Δ is its actual maximum degree, G is not Δ-edge-colorable, and G−e is Δ-edge-colorable for every edge e. Every list has exactly Δ colors. A is a Δ-element palette, X consists of edges whose lists differ from A, and each exterior deficit d(e)=|L(e)\A| equals |A\L(e)|. The assignment under discussion is nonconstant.

The equality of the two deficit expressions uses the exact list-size assumption. In the new results Δ=3, so every exceptional deficit is 1, 2 or 3. Exterior lists are nonempty. A nonempty exterior-colored set F permits an ordinary Δ-coloring of G−F by restriction from G−f for any f∈F; no stronger criticality assertion is used.

The candidate restates the accepted strict residual-deficit argument accurately. A uniform permutation sends each ordinary label uniformly into A; the union bound needs no independence between violated-list events. Residual deficit strictly below Δ gives a successful permutation, and the disjoint palettes prevent conflicts between exterior-colored and base-colored edges. The first-round four-exception result is used only with its explicit nonconstant qualification. Degree two is already completely settled there, and degree zero or one is impossible under the criticality hypotheses.

## Equality classification for three unit deficits

For a chosen ordinary coloring, a remaining unit-deficit edge forbids one label-to-base-color cell of a 3-by-3 bipartite matching problem. Three edges remove at most three distinct cells; repeated constraints must not be counted as additional removals.

Hall's obstruction on one row requires all three cells of that row to be removed. Thus all three ordinary labels coincide and the omitted colors are all different. An obstruction on two rows would require their combined neighborhood to have at most one color, requiring at least four distinct removed cells. This is impossible. An obstruction on all three rows requires an entirely removed column, giving three distinct labels and one common omitted color. These exhaust Hall's possibilities, and an empty row or column indeed blocks every permutation.

This is an exact classification for those three constraints on a specified ordinary coloring. It does not classify uncolorable list assignments. In particular, repeated cells, repeated labels without three distinct omissions, or repeated omissions without three distinct labels need not obstruct completion.

## Five unit substitutions on arbitrary support

If the exceptional support has a matching of size at least three, exterior-color any three matching edges. The remaining total deficit is two, so the strict theorem applies.

Otherwise the matching number is exactly two. It cannot be one: five pairwise-incident edges in a simple subcubic graph are impossible. Moreover, after removing any one of the five edges, the four remaining edges contain a disjoint pair, since a pairwise-incident four-edge family would be a four-edge star. Consequently the complements of two-edge matchings cover all five edges. Every two such complements intersect because they are three-element subsets of a five-element set.

If every complement triple had a constant omitted color, their intersections would force one common color for all triples, and their covering property would make every omission the same. Therefore nonconstant omissions give a matching F whose complement R has nonconstant omissions.

Exterior choices on F are automatically proper. In any ordinary coloring of G−F, the three edges of R cannot have one common label, because a proper ordinary color class is a matching and that would produce a matching of size three in X. The omissions on R are not constant either. The two equality obstructions are therefore both excluded, and a palette permutation works. This reasoning is independent of the actual exterior colors and of edges outside X.

The hypothesis on omitted colors is sufficient, not necessary. Equal omissions on a 5-cycle are subsequently handled by another argument, and their equality is not evidence of a bad assignment.

## Five-boundary-color lemma

The multiplicity split in the proof is exhaustive: 5, 4+1, 3+2, 3+1+1 and 2+2+1 are exactly the partitions of five into at most three positive parts.

For 5 and 4+1, choosing the frequent label leaves at most one nonmatching entry, so both conditional requirements are immediate. For 3+2, at least one frequent-label position lacks two minority-label neighbors; otherwise the three positions demand six incidences from two cycle vertices with only four available incidences. All nonmatching labels are identical, which gives the second condition.

For 3+1+1, two nonmatching neighbors are automatically the distinct singleton labels. The second condition can fail only when the opposite edge joins those two singletons. The map from a position to its opposite cycle edge is bijective, so at most one position is forbidden and another of the three frequent-label positions can be chosen.

For 2+2+1, choose a neighbor of the singleton position. One neighbor is the singleton; another nonmatching neighbor, if present, has the other repeated label. The opposite edge cannot contain the singleton, so two entries there that differ from the chosen repeated label must both equal the other repeated label.

The selected position matters. The lemma does not say that every position works, and direct controls below demonstrate both ways an arbitrary position can fail.

## Uniform-list cycle extension and its boundary cases

An ordinary coloring of G−E(C) exists by criticality and restriction. At a cycle vertex, subcubic degree allows at most one edge outside C. The proof correctly records its ordinary label. At a vertex with no such edge, an arbitrary fictitious boundary label imposes an additional restriction; avoiding it cannot introduce a real conflict.

A chord belongs to G−E(C), not to the exceptional cycle. Its same ordinary color appears at both endpoint positions. The boundary lemma holds for every cyclic word, including words with these equalities. Thus chords do not require the cycle to be induced and do not break the argument. Global relabeling preserves properness of the entire graph outside C, including components and edges not incident with the cycle.

After rotating the chosen position to zero and mapping its boundary label to the omitted base color, two disjoint cycle edges receive the exterior color x. The remaining edges consist of a two-edge path through vertex zero and an isolated edge, separated along the cycle by the x-edges.

For the two-edge path, the endpoint restrictions can be met by opposite retained base colors exactly as claimed: if both restrictions are effective, the first boundary condition makes them different. If just one restriction is effective, it determines an order; if neither is effective, either order works. The boundary label at the middle vertex is the omitted color, so it conflicts with neither path edge.

For the isolated edge, the second condition says that effective forbidden retained colors at its endpoints, if both present, are equal. At most one of the two retained colors is therefore forbidden. Its color exists. No off-cycle edge uses x, and every on-cycle adjacency was handled by the path colors or separated by an x-edge.

Only ordinary colorability of G−E(C), the subcubic boundary-degree bound and the specified two palettes enter this construction. It need not preserve an arbitrary prior coloring of G−F for a smaller exterior set.

## Arbitrary exceptional lists on the 5-cycle

The exceptional-edge adjacency graph is C5, and every proper induced subgraph is a forest of maximum degree two.

For h=1 large deficit, positions 0,1,3 may be selected after rotating the large edge to zero. The two small edges are nonadjacent; the large edge meets only position 1 among the selected edges and has at least two exterior choices. The residual deficit is two.

For h=2, select the large edges and a small edge. Their induced forest can be rooted at the small edge in its component. Color that singleton exterior list first; each subsequently colored large edge avoids at most one previously colored neighbor. Other components also admit greedy coloring. Again the residual deficit is two.

For h=3 or h=4, the large edges induce a forest or a path, respectively, and their exterior lists have size at least two. The residual deficits are two and one. For h=5 with a deficit-two edge, leave that edge and color the other four-edge path; the residual is two. If all five deficits are three, arbitrary three-element lists color a cycle greedily because at most two neighbors have been colored when a vertex is processed. The residual is zero. Every exterior set used here is nonempty.

When h=0, nonconstant singleton exterior colors give a proper subgraph of the adjacency cycle after retaining only equal-color adjacencies. This conflict graph is a forest, hence bipartite; one side has at least three vertices. Three selected edges can share vertices in G without conflict if their exterior colors differ, and no selected same-color adjacency exists. The residual is two.

If all exterior colors are equal, nonconstant omissions invoke the arbitrary-support theorem. If the omissions are also constant, the uniform-list boundary construction applies. These alternatives exhaust all assignments, including lists completely disjoint from A. Fewer than five exceptional edges supported on the same cycle are covered by the corrected first-round theorem.

## Critical example and precise method limitations

The example has ordered edges [04,41,02,03,12,13,23]. Its maximum degree is three. Seven edges on five vertices cannot be colored with three colors, because each color class has at most two edges.

Criticality can also be checked without relying on an opaque computational assertion. Swapping vertices 0 and 1 and swapping 2 and 3 partition its edges into three deletion types. For representatives of these types, the following partitions of the remaining edges are partitions into three matchings:

- Delete 04: {41,23}, {03,12}, {02,13}.
- Delete 02: {04,13}, {41,23}, {03,12}.
- Delete 23: {04,13}, {41,02}, {03,12}.

The automorphisms cover all seven edge deletions. The auditor also independently generated and checked all seven deletion colorings.

For uniform exterior singleton lists on the five-cycle, a properly exterior-colored F must be a matching and has size at most two. Hence its residual deficit is at least three. This proves failure of every strict-deficit certificate for this assignment, not uncolorability.

For the specified F={03,12}, the given ordinary coloring of the complement is proper. The three remaining exceptional edges receive all three ordinary labels and all omit base color 2, so the equality lemma blocks every global permutation. The displayed full coloring (0,1,1,3,3,2,0) was checked edge by edge against both adjacency and lists. It even keeps the same F and exterior color, but uses a different ordinary coloring of the complement. Thus the example does not obstruct all ordinary colorings for that F.

The Kempe supplement is equally narrow and correct. In the two-color subgraph on ordinary colors 0 and 2, the component containing edge 04 is that edge alone: its two neighbors in G−F have color 1. Swapping 0 and 2 on this component preserves ordinary properness. The stated permutation then produces (1,0,0,3,3,2,1), another proper full list coloring with unchanged F. No claim that one such switch always suffices follows.

Finally, allowing F, its exterior coloring and the ordinary coloring all to vary makes existence of an exterior-plus-permutation completion equivalent to existence of a full list coloring. From a full coloring, take precisely its exterior-colored edges as F. F is nonempty because G cannot be colored solely from A. The remaining coloring already uses A and becomes an ordinary coloring by renaming labels. This proves the converse construction. Therefore a purported obstruction to every such unrestricted completion would be a genuine bad-list example, unlike either demonstrated method limitation.

## Independent finite checks and controls

The auditor implemented the second-round constructions independently. The only reused code was the auditor's previously validated exact solver and coloring verifier from the first-round audit. No author test implementation or separate support-enumeration result was imported. Every completed full coloring was separately checked for list membership and properness.

The completed checks were:

- All 729 label/omission triples in the equality lemma: exactly 36 obstructed triples and 693 feasible triples, matching the stated classification.
- All 243 boundary words, every valid selected position, all three omitted base colors and both bijections of the other labels: 4,410 constructed cycle colorings. There were 480 invalid choices among all arbitrary word/position pairs, confirming the need to select the position.
- All 82 local layouts formed from a matching of cycle chords and independent choices of a pendant or absent off-cycle edge at every remaining vertex. Across every consistent boundary labeling this gave 11,286 full local extensions, including 3,510 with chords and 10,503 with an absent boundary edge. These local layouts test the extension mechanism; they are not claimed individually critical.
- Every five-edge simple subcubic support on six labeled vertices: 2,697 supports, of which 945 have a matching of size three and 1,752 have matching number two. The latter covered 420,480 nonconstant omission assignments and 5,636,160 proper ordinary-label restrictions.
- Independently, every K4-free graph on five labeled vertices was used as an abstract exceptional-edge adjacency graph. Of 958 graphs, 636 have an independent triple; the other 322 covered 77,280 nonconstant omission assignments and 1,071,720 proper-label restrictions. This abstract family contains the relevant subcubic line-graph patterns, including patterns not represented by supports on six vertices.
- On the stated critical subdivided-K4 graph, every three-element list from a six-color universe other than A was allowed independently on each of the five cycle edges. All 19^5=2,476,099 assignments were completed. The exact branch counts were 328,050, 729,000, 810,000, 450,000 and 100,000 for h=1 through 5; 58,320 unit-deficit cases with varying exterior colors; 720 with uniform exterior colors but varying omissions; and nine uniform-list cases requiring the boundary construction. The first 2,476,090 cases also passed direct Hall-versus-permutation comparison.

All branches passed. The smaller complete suite covering equality, boundaries, abstract supports, critical deletion checks, controls and Kempe repair was repeated under normal Python, -O and -OO and agreed after excluding elapsed time. Checks use explicit failures, not removable assertions. The 2,476,099-case full assignment enumeration was run in normal mode; it is not being reported as repeated under optimization.

Explicit controls distinguish the hypotheses and the methods:

1. On boundary word (0,1,0,0,1), choosing position zero fails the first condition and forces equal colors on the two retained path edges.
2. On word (0,0,1,2,0), choosing position zero fails the second condition and forbids both retained colors on the isolated edge.
3. The uniform cycle example has ten nonempty properly exterior-colorable subsets, none with residual deficit below three.
4. The specified ordinary coloring admits zero repairing permutations, while the displayed full coloring and the Kempe-repaired coloring both succeed with the same exterior set.
5. Changing one exterior color, changing one omitted color, or increasing one deficit exercises three distinct successful neighboring branches.
6. Constant A-lists on the critical fixture fail, as required.
7. A disjoint union of the same constant-list critical fixture and a five-cycle carrying the exceptional lists remains uncolorable. This graph lacks the required criticality and ordinary colorability off the cycle; it is not a counterexample to the theorem.

Finite enumeration is corroboration. The general proofs and their quantifiers are assessed separately above.

## Sources and publication scope

The target problem is the nonconstant-list formulation in the [Open Problem Garden entry](https://www.openproblemgarden.org/op/list_colorings_of_edge_critical_graphs). [Mohar's original page](https://www.sfu.ca/~mohar/Problems/P7ListEdgeCriticalGraphs.html) has the reversed equivalence already identified in the first-round audit. [Kaul and Mudrock, version 2, Conjecture 6](https://arxiv.org/pdf/1805.02147v2), gives line-graph context; its compressed criticality wording does not remove the explicit non-Δ-colorability hypothesis. These sources were directly inspected during the first-round audit and are not invoked as proofs of the new results.

The acceptance is limited to the two authored mathematical texts and the stated first-round dependencies. The full independent report and concise acceptance metadata are suitable mathematical audit artifacts. Test source, raw machine certificates, private extracts and coordination material are excluded. The first-round acceptance remains unchanged, and no remote state was modified by this audit.

## Reproduction boundary of this prose edition

The symbolic proofs, explicit criticality matchings, fixed-coloring obstruction and Kempe repair are fully displayed. All aggregate finite counts, branch contracts, controls and run-mode limitations are retained as audited reports. Executable programs and raw machine-certificate collections are not distributed; the full finite suites cannot be rerun or their raw outputs reconstructed from this prose alone. The separately audited method classification is in METHOD_CLASSIFICATION.md and AUDIT_METHOD_CLASSIFICATION.md.
