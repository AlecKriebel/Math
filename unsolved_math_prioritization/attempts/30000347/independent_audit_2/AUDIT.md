# Independent full-proof audit: three-terminal shortest-path blocking

Audit date: 7 October 2026.
Problem identifier: 30000347 (OWR-1111-001).

## Verdict

**ACCEPT. No mathematical correction is required.**

The frozen manuscript proves that the decision form of undirected, unit-length, three-terminal Blocking Shortest Paths is NP-complete, even when every deletion cost is 1 and every original terminal distance is 3. It therefore answers the full complexity classification asked by the cited historical source, as a mathematical implication. It also correctly establishes the positive rational-cost decision classification and the optional finite-terminal-connectivity strengthening.

This verdict is about the proof and its match to the stated problem. It does not establish novelty, priority, publication status, or absence of an earlier classification. In particular, it is not a claim that the historical problem remained unresolved until this manuscript.

The reviewed PROOF.md has SHA-256 f31b19b8e4286e0104ed1e272f5cbc4a39e20aea78aa30334466f5b44e5830f7. Its frozen manifest has SHA-256 b13c9cee3e806a263ba0e24b2838599692727ea48d26977d4fca714e1e30d273. All six payload sizes and hashes in that manifest were independently verified. The original files were left unchanged.

## Review independence and method

I read the entire frozen proof and source/model assessment, checked the cited primary sources, and reconstructed both reductions directly. I did not read another audit. Fresh computational controls were written and successfully run before examining the author's check implementation. Only afterward did I inspect and rerun a copy of the author's checker, to verify the manuscript's historical computation counts. The fresh program neither imports nor executes that checker.

The universal correctness verdict rests on the arguments below, not on the finite tests.

## 1. Source and target-model assessment

The [Oberwolfach report](https://ems.press/content/serial-article-files/46024?nt=1), printed pp. 2856-2858, defines edge deletion that blocks all original shortest paths, with traversal length measured by number of edges. Its first listed open problem asks for all three unordered pairs among three specified vertices, with or without deletion costs. It separately states directed-triangle hardness. Thus the manuscript selects the correct undirected question; it does not mistake a demand triangle for three adjacent graph vertices.

The [dissertation](https://webdoc.sub.gwdg.de/ebook/dissts/Braunschweig/Krause2006.pdf), printed p. 2, permits assuming positive deletion costs and originally connected, nonadjacent demand pairs. It explicitly allows multicut solutions, resolving the disconnection convention. Printed p. 5 supplies the finite-simple-graph convention. Section 4.3, pp. 34-36, leaves the undirected triangle case unresolved; Theorem 9.3, pp. 83-84, addresses directed instances. These statements are consistent with the manuscript's model.

The [Karp scan](https://cgi.di.uoa.gr/~sgk/teaching/grad/handouts/karp.pdf), printed p. 94, visually confirms the Main Theorem and Node Cover entry. This is the standard Vertex Cover decision problem used in the reduction. Nothing else is imported as an unproved complexity theorem.

Independent public-web openings succeeded for the report and dissertation. The web screenshot service failed, so I inspected rendered local copies instead; the direct Karp web opening also failed, and its supplied university-hosted scan was inspected locally. The supplied report, thesis, and Karp PDF hashes and sizes agree with the source manifest. These are local-byte verifications, not claims of independent fresh byte retrieval at the author's recorded times.

The old and newer report PDFs differ in bytes, as disclosed. Independently extracting printed pp. 2856-2858, isolating Krause's complete contribution, and collapsing whitespace gives identical 4,565-character text and SHA-256 80037c2f79bde157b603e243898db7bc03af548072cdf5df985fed306bdc73f0 for both files. This reproduces the manifest's normalized-content comparison.

I do not independently certify completeness of the bounded literature search. The manuscript's explicit refusal to infer priority from search absence is appropriate.

## 2. Twice-subdivision identity

For each source edge uv, the graph H uses fresh vertices b and c and the path u-b-c-v. Every original vertex is in A, each b in B, and each c in C. The parts are independent even when Q is not bipartite and regardless of endpoint orientation. No parallel edges or loops are introduced.

The upper bound tau(H) <= m + tau(Q) is valid in all three relevant endpoint cases. If only u is covered, select c; if only v is covered, select b; if both are covered, either new vertex covers the middle edge. Exactly one new vertex per gadget suffices.

For the reverse bound, let X cover H, and set S = X intersect V(Q). Every gadget needs at least one new vertex. If neither original endpoint is in S, its two outer edges force both new vertices. If q original edges are uncovered by S, therefore |X| >= |S| + m + q. Adding an endpoint of each such edge covers Q with at most |S| + q vertices. Endpoint repetitions only improve the inequality; no injectivity is assumed. Hence tau(Q) <= |X| - m, proving equality.

This argument applies to nonoptimal covers, isolated vertices, disconnected Q, arbitrary gadget orientations, and all nonnegative source budgets. It does not assume an optimum with a special normal form.

## 3. Terminal-spoke identity

Every H vertex has exactly one terminal neighbor, determined by its part. Distinct terminals are nonadjacent and have disjoint neighborhoods, excluding paths of length 1 and 2. A nonempty edge type between each pair of parts supplies a path of length 3 for the corresponding terminal pair.

Conversely, a three-edge terminal path has exactly two internal vertices. Its first and last edges must be the two appropriate spokes; its middle edge must join the corresponding H vertices. Therefore the entire family of original terminal geodesics is exactly the family indexed by H edges. Routes through the third terminal cannot produce an overlooked three-edge path.

A vertex cover X of H gives a blocker by deleting its spokes: each original geodesic is hit at an endpoint. For an arbitrary blocker F, map deleted spokes to their incident H vertices and deleted H edges to one endpoint each. For every H edge uv, its particular three-edge geodesic must contain a deleted edge. Whichever of the three edges was deleted contributes an endpoint of uv to the extracted set. This proves that the extracted set covers H and has at most |F| vertices.

Crucially, the reverse direction does not restrict deletions to spokes, assume protected middle edges, or assume inclusion-minimality of F. Shared endpoints and repeated selections decrease set size rather than causing a loss. The two inequalities prove opt(G_H) = tau(H).

The conversion is cardinality-preserving in the needed inequality because all deletion costs are 1. The proof does not incorrectly assert the same identity for arbitrary assigned costs; it uses the unit-cost subclass to establish hardness of the rational-cost superproblem.

## 4. Complete reduction and encoding

For m >= 1, every source-edge gadget contains all three cross-part edge types. Thus Lemma 2's hypothesis is automatic, not an extra restriction on Vertex Cover. With B = m + k, the two identities give the required if-and-only-if decision equivalence.

The graph has n + 2m + 3 vertices and n + 5m edges: 3m gadget edges and n + 2m spokes. All vertices are connected initially, including isolated source vertices, because each has its spoke and the three terminals are interconnected. The output is finite, simple, undirected, and unit-length, and all edges remain eligible for deletion.

There is no hidden bounded-degree claim: terminal degrees may grow with the input. No planarity, bipartiteness of G_H, unique-geodesic property, or global residual connectivity is used.

The edgeless source cases are yes-instances because k is nonnegative. A fully explicit fixed output is the construction for Q = K2 with target budget 2; it has all original terminal distances 3 and optimum 2. This supplies the manuscript's optional total-reduction branch. For nonempty Q with k = 0, the target budget m is correctly infeasible. Large k changes only the encoded budget, not the graph; the addition m + k has polynomial bit complexity. The adjacency-list size claim is valid with its stated representation-cost qualification.

The reduction from an NP-complete source establishes restricted NP-hardness and therefore hardness of the full target problem, rather than merely hardness of a different path-length-threshold problem.

## 5. Membership in NP and optimization consequence

An edge subset is a polynomial-size certificate. Validate its membership in E, eliminate or reject duplicate entries, count deletions, and perform BFS before and after deletion. Three pairs require only constantly many searches. A disconnected pair is treated as infinite distance, as the source model allows.

For unit traversal lengths, destroying every original geodesic is equivalent to increasing distance by at least one: deletion never shortens paths, and finite distances are integers. The proof does not conflate deletion cost with traversal length.

For positive binary-encoded rational deletion costs and a rational budget, exact summation has polynomial bit complexity. A common denominator formed from the product of input denominators has bit length at most their total bit length; intermediate numerators remain polynomially bounded in bit length. Consequently the stated rational-cost decision problem is also in NP. An exact optimization algorithm would decide the budget problem, proving the claimed optimization hardness.

## 6. Optional finite-distance extension

Three fresh four-edge terminal-to-terminal paths introduce exactly nine internal vertices and twelve edges. Internal vertices have degree two and no other incidences. Any simple path between original vertices that uses these new internal vertices must traverse an entire added path between terminals. Hence none creates a path of length at most three, and the original geodesic family is unchanged.

Every blocker in the enlarged graph must still hit those original geodesics. Ignoring deletions on the added paths and applying the old-edge extraction gives an H cover of no greater size, establishing the same lower bound. Conversely, deleting the spokes of an H cover leaves all added routes intact, blocks every original length-three path, and makes all three distances exactly four. This proves equality of the optima under the ordinary, finite-distance, and exactly-one-increase requirements for this construction.

The finite-distance requirement itself need not be monotone under further deletions; the proof does not require such monotonicity. It supplies an explicit feasible optimal witness instead. All variants are in NP by BFS. The manuscript correctly avoids claiming that every remaining graph vertex stays connected.

## 7. Fresh adversarial controls

The separate standard-library program fresh_controls.py passed the following checks:

- Every deletion subset for all 274 valid tripartite graphs with part sizes (1,1,3) and (1,1,4): 862,464 subsets in total. Three actual BFS distances were compared with the predicted geodesic hitting condition for each subset; exact blocker optima were compared with independently brute-forced vertex-cover optima.
- All 451,946 feasible blockers were converted to covers twice, selecting the first endpoint of every deleted H edge in one pass and the second endpoint in another: 903,892 successful no-larger-cover extractions.
- All 759 source edge-presence/orientation assignments on two through four labelled vertices. These include 756 nonempty full compositions. Shortest paths were independently enumerated by simple-path DFS at BFS-determined depth, and their exact minimum hitting sets were computed independently of the subdivision formula. All 5,262 budget comparisons passed, including k = 0, oversized k, and k = 2^2048.
- Another 460 subdivision cases, including seeded random graphs, dense graphs, cycles through ten vertices, two disjoint triangles, and source isolates. Exact endpoint-branching vertex cover on H agreed with brute-force vertex cover on Q plus m.
- Four optional-extension instances: every one of the 32,298 deletion subsets smaller than the proposed optimum failed by direct BFS, including subsets deleting fallback-route edges. All 134 cover-derived witnesses had all three terminal distances exactly four.
- Four deliberately invalid modifications were detected: omitting a demand pair, omitting a cross-part edge type, using three-edge fallback routes, and subdividing a source edge only once. A separate convention control confirmed that terminal disconnection is accepted in the ordinary model.
- The fixed yes-instance for the edgeless branch was checked explicitly, and all six frozen payload hashes and byte counts were verified.

After these independent controls, a separately copied author checker also passed and reproduced every numerical count reported in PROOF.md: 145 graphs, 165,952 deletion subsets, 89,975 feasible blockers, 3,375 size-(2,2,2) graphs, 1,094 nonempty base graphs, 6,484 budget comparisons, and 66 finite-distance cover checks. Runtime metadata naturally differs between runs.

Finite checks do not prove the universal statements. They specifically exercise arbitrary middle-edge deletions, graph orientation choices, budget extremes, missing hypotheses, alternative endpoints, and fallback-path deletions where a superficially similar incorrect reduction could fail.

## 8. Required changes and disposition

There are no required mathematical corrections and no fatal or unresolved proof gaps. No original manuscript or frozen payload was changed. No correction patch is supplied because none is needed.

Accept the frozen proof for its stated NP-completeness and NP-hardness claims, retaining its no-priority disclaimer. Any separate publication or novelty claim would require a different assessment.
