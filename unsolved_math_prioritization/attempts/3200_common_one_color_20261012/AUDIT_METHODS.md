# Independent audit of the common-color matching reduction

## Decision and limits

**ACCEPT.** The exact fixed-matching criterion, critical-cycle construction, local-overlap argument, full-family connectivity statement, and both explicitly scoped negative examples are correct. Their certificates and numerical censuses have been independently reconstructed and checked. No mathematical correction is required.

The audited statement is the following. Let (G) be a finite simple graph of maximum degree at most three, not properly three-edge-colorable, such that deleting any edge makes it properly three-edge-colorable. Let every edge receive an exact three-element list, with a color common to all lists. Then the graph has a proper list edge coloring exactly when the assignment is nonconstant. The supplementary claims audited here specify how to select the matching and why an arbitrary matching may be inadequate.

This acceptance does not settle assignments with empty total intersection, claim historical novelty, or turn a failure of one fixed-matching strategy into a list-uncolorability conclusion. The theorem has a symbolic proof; the finite computations corroborate that proof and validate the explicit examples.

The complete reviewed argument is preserved in [METHODS.md](METHODS.md), with the implication-label clarification below and distribution-only editorial changes. All twelve original packet files and its exact inventory were checked against the frozen input pin. MANIFEST.json identifies only the actual distributed edition files; excluded-input identities are not published.

The reviewed manuscript called the nonconstant-to-colorable implication “forward,” and the colorable-to-nonconstant implication “reverse,” although its displayed equivalence was written in the opposite order. The implications were both proved correctly. In the distributed METHODS.md, “sufficiency of nonconstancy” and “necessity of nonconstancy” replace those labels and remove the directional ambiguity.

## 1. Exact scope of the fixed-matching criterion

Choose a globally common color (c), and write (B(e)=L(e)\setminus\{c\}). These are exact two-element lists. Let (M\subseteq E(G)) be a matching.

The matching covers all vertices of degree three if and only if (G-M) has maximum degree at most two. A matching deletes at most one incident edge at every vertex; thus coverage is necessary at a cubic vertex and sufficient everywhere in a subcubic graph.

For such a matching, the strategy that gives color (c) to **exactly** the edges of (M) succeeds if and only if no odd-cycle component of (G-M) has constant reduced lists.

Here is the complete component argument. A path with two-element edge lists is greedily colorable. An even cycle with constant two-element lists is alternately colorable; an odd cycle with such lists is not. For a cycle with nonconstant lists, some consecutive pair has unequal lists. Start the cyclic ordering immediately after that transition, so its first and last lists differ. Their equal cardinalities provide a color in the first list absent from the last. Give that color to the first edge and greedily color the remaining edges, always avoiding the predecessor. The last edge automatically avoids the first color because that color is absent from its list. This works for either parity. Isolated vertices impose no conditions. Different residual components are independent, and no residual color is (c), so there is no conflict with the matching.

Necessity follows because a constant-two-list odd cycle cannot be properly colored. Thus the criterion is an equivalence, and it tests **every** odd-cycle component. Its statement needs subcubicity, matching coverage, and exact two-element residual lists; it does not require criticality. Criticality is used to produce an appropriate matching below. No assertion is made that every full list coloring has a common-color class covering all cubic vertices.

## 2. The specially selected critical cycle

Fix any edge (e) and any proper three-edge-coloring of (G-e), with labels from a fixed three-element set. A cubic endpoint of (e) sees two distinct labels, forbidding just one possible label for a covering color class. At most two endpoints impose this restriction, so at least one permissible label exists. Every cubic vertex not incident with (e) sees all three labels. Consequently **every** permissible label has a color class (M) covering all original cubic vertices.

The graph (G-M) has maximum degree at most two. After removing (e), its edges are colored with the other two labels. Any odd-cycle component of (G-M) must therefore contain (e). Distinct components cannot both contain that edge, so there is at most one odd cycle. If there were none, two colors would color the entire residual graph, and the third color would color (M), contradicting the non-three-colorability of (G). There is exactly one odd cycle, and it contains (e).

The quantifiers are important: this holds for every deletion coloring and every covering-admissible label. It does not hold for every arbitrary degree-three-covering matching.

## 3. Overlap, connectivity, and the common-color conclusion

All edges of a deletion-critical graph lie in one connected component: an uncolorable component would remain after deleting an edge in any other edge-containing component. Extra isolated vertices are harmless. Its line graph is therefore connected, and a nonconstant assignment has incident edges (e,f) with different reduced lists.

Choose critical cycles through (e) and (f) as above. At their shared endpoint, each cycle uses two of at most three incident edges. The two cycles must share an incident edge. If both cycles had constant reduced lists, their constants would agree on this common edge, forcing (B(e)=B(f)), a contradiction. One of the cycles is nonconstant. Its selected matching has only that one odd-cycle component; the fixed-matching criterion colors the whole graph. This proves sufficiency of nonconstancy. Conversely, a constant exact-three-list assignment would be an ordinary three-edge-coloring, which is impossible.

The stronger global statement made in the manuscript is also correct. Consider all unique odd-cycle components arising from covering matchings whose complements have exactly one odd cycle. Select one critical cycle through every edge using the deletion construction. Whenever edges are incident, their selected cycles share an edge, so connectedness of the line graph implies connectedness of this selected cycle family under edge intersection. Every other member of the full family contains an edge and intersects its selected cycle. Hence the full family's edge-intersection graph is connected. This neither asserts nor requires pairwise intersection of all family members.

The proof uses deletion colorings for at most two incident edges. It does not claim an efficient algorithm for obtaining those ordinary deletion colorings from an arbitrary input graph. All arguments remain valid with isolated vertices present and when an endpoint of the chosen edge has degree below three.

## 4. A critical graph with a three-odd-cycle residual matching

The following explicit authored construction is valid. Begin with vertices (0,\ldots,8) and edges

\[
02,13,14,23,24,34,06,57,58,67,68,78,15.
\]

Retain vertex 0. Replace each other vertex (v) by a triangle, with one port (p(v,w)) for each neighbor (w). Replace each base edge by the edge joining its corresponding ports, using (p(0,w)=0). This gives 25 vertices and 37 edges: eight triangles supply 24 internal edges, and the base graph supplies 13 external edges. Vertex 0 has degree two; the other 24 vertices have degree three.

Use the base path (2,3,1,5,7,6). Take all external edges between triangle blocks except the five edges of this path. Also take, in each path block, the internal edge joining its predecessor and successor ports, using the port towards 0 at each endpoint. These are six external and six internal matching edges. Each of the six path blocks has its two path ports covered internally and its third port covered externally; all ports of blocks 4 and 8 are covered externally. Thus all 24 cubic vertices are covered.

After removing the matching, blocks 4 and 8 remain intact triangles. Each path block contributes a two-edge internal path. Those six two-edge paths, the five external path edges, and the two external edges to vertex 0 form a cycle of length (12+5+2=19). Therefore the residual graph is exactly (C_3+C_3+C_{19}).

Non-three-colorability is immediate: every color class on 25 vertices is a matching of size at most 12, whereas the graph has 37 edges. All 37 single-edge deletions have independently checked proper ordinary three-coloring certificates. Thus the graph is genuinely deletion-critical.

The independent enumeration also checks every covering matching of this graph. There are 16: 12 leave one odd cycle and four leave three odd cycles. The special deletion-color-class construction produces eight distinct critical cycles, four triangles and four Hamilton cycles. The triangles are edge-disjoint; the entire critical-cycle family is nevertheless connected. These bounded findings reinforce the intended distinction between special and arbitrary matchings.

## 5. Exactly one common color and a bad matching choice

Take ordered edges

\[
e_0=01,\ e_1=02,\ e_2=13,\ e_3=14,\ e_4=23,\ e_5=24,\ e_6=34.
\]

Give all edges list \(\{0,1,2\}\), except \(L(e_2)=\{0,1,3\}\) and \(L(e_5)=\{0,2,3\}\). The total list intersection is exactly \(\{0\}\).

The only matchings covering its four cubic vertices are \(M_{bad}=\{e_2,e_5\}\) and \(M_{good}=\{e_3,e_4\}\). Removing the former leaves a five-cycle whose reduced lists are all \(\{1,2\}\). The fixed-(M_{bad}) strategy fails. The complete edge-color tuple

\[
(2,1,1,0,0,3,2)
\]

is proper and list-respecting, and its zero-color class is exactly (M_{good}). Thus the assignment itself is colorable. The graph is non-three-colorable by its seven edges on five vertices, and all seven deletions were checked to be three-edge-colorable.

Exhausting all three triple-list types containing 0 in a four-color palette gives (3^7=2,187) assignments. Exactly three have no successful covering matching, and these are the constant assignments; 48 have one successful matching; 2,136 have two. For all 4,374 assignment/matching pairs, independent direct search agrees with the component criterion.

## 6. Independent verification and bounded coverage

The independent verifier imports none of the author's implementations. It uses endpoint color sets for exhaustive coloring search, vertex-walk component decomposition, a separate recursion enumerating covering matchings, and independently reconstructed port expansion. It has no search cutoff, random sampling, or timeout-to-impossibility inference.

All labeled proper deletion colorings were re-enumerated and individually validated. Every admissible color class was checked, and every stored critical-cycle witness was independently verified. Per-deletion counts, cycle-length histograms, graph totals, full cycle sets, and final aggregates all agree:

| Vertices | Edges | Deletion colorings | Admissible classes | Distinct critical cycles |
|---:|---:|---:|---:|---:|
| 5 | 7 | 48 | 60 | 2 |
| 7 | 10 | 96 | 120 | 3 |
| 7 | 10 | 108 | 120 | 3 |
| 7 | 10 | 72 | 84 | 2 |
| 7 | 10 | 144 | 168 | 4 |
| 9 | 12 | 360 | 468 | 8 |
| 25 | 37 | 864 | 888 | 8 |
| **Total** | | **1,692** | **1,908** | **30** |

All 96 stored first-deletion witnesses and the 37 separately stored deletion witnesses for the expanded graph were checked, as were the 30 full cycle/deletion-coloring/class witnesses. Six graphs are non-three-colorable by the overfull matching bound. The remaining graph, Petersen minus one vertex, was independently found to have no ordinary three-edge-coloring. Its separately supplied negative decision tree was also checked in full: 232 nodes, 36 dead ends, and exactly all legal color branches at every node.

The independent covering-matching enumeration checks all 38 covering matchings across the seven graphs and recovers the same single-odd-cycle families as the deletion-coloring census. Cycle coverage and family connectedness hold; all 1,274 stored-cycle pairs relevant to incident edges satisfy the local shared-edge conclusion at the common endpoint.

Additional bounded checks cover 3,267 two-list assignments on paths and 3,267 on cycles of lengths three through seven. On the actual three-odd-cycle example, making zero, one, or two residual odd components nonconstant still fails the fixed-matching strategy; making all three nonconstant succeeds. This directly exercises the criterion's universal quantifier over odd components.

## 7. Optimization, replay, corruption, and final boundary

The independent verifier passes under ordinary Python, `-O`, and `-OO`, producing identical result bytes. All four author programs were independently replayed in each of those modes, for 12 successful executions. Every replay exactly reproduces the frozen packet bytes, including all generated result files.

Twenty-seven fail-closed corruption controls were exercised in each mode, for 81 rejected corruptions. They cover false counts; conflicting or missing deletion colorings; altered, omitted, or mismatched cycle witnesses; malformed graph data; invalid or noncovering matchings; incomplete and illegal negative-tree branches; missing odd components; corrupted positive colorings and list assignments; modified input bytes; missing and extra files; changed manifest bytes; and a self-consistent attempted resealing against the immutable external pin. Semantic controls bypass the digest layer deliberately, so their rejection demonstrates mathematical validation rather than only checksum detection. No check relies on a Python `assert` that optimization could remove.

These computations do not exhaust all critical graphs or all list assignments. The symbolic proof establishes the restricted theorem without a size or palette bound. The two explicit examples establish limitations of arbitrary matching selection, not counterexamples to that theorem. For a fixed four-color palette, assignments using two or three distinct triple types retain a common color and are covered; using all four types has empty total intersection and remains outside this argument.

## 8. Prose-edition reproduction boundary

The complete substantive audit, symbolic reasoning, explicit authored examples, bounded coverage, all reported counts and every verification limitation are preserved. Programs, raw graph/fixture/certificate/coloring collections and run outputs are not distributed. The computational suites cannot be rerun or the omitted records reconstructed from this prose alone; fresh implementation and fresh input generation are required. All replay and corruption outcomes above describe the independent mathematical audit, not a new rerun during edition preparation. Actual distributed file identities are in MANIFEST.json.
