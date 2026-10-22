# Final independent partial-result audit

## Verdict

**PASS for the explicitly bounded computational claims and concrete counterexamples reviewed here.** No unrestricted characterization, four-point obstruction theorem, product-closure theorem, or novelty claim is supported by these experiments. No external publication was performed in this audit.

## Independent verification rather than a rerun

Added `computation/independent_audit.py` and retained its output in `computation/independent_audit_results.txt`. It does not import any of the existing apex, realization, or product test functions.

The independent implementation uses:

- Floyd–Warshall distances, rather than NetworkX shortest-path routines;
- interval bitsets and a greatest-element test for the common basepoint interval, rather than enumeration of maximal elements;
- closure constraints from unordered three-element sets and the three possible roots;
- canonical adjacency recovered directly from restricted intervals;
- exact comparison of all restricted intervals with the candidate graph's intervals, rather than comparison with a newly computed ternary table.

The last test is mathematically sufficient: the original apex belongs to the closed subset and is greatest in each original common interval. Equality of all restricted intervals makes it greatest in the candidate common interval too, so the candidate is apiculate with the required operation. Disconnected candidates are explicitly rejected. Repeated-input ternary values are always inputs, so omitting them from closure constraints is valid.

The independent check still uses the same standard NetworkX atlas enumeration, so it is algorithmically independent but not an independent catalog of unlabeled graphs.

## Results

All connected atlas graphs of orders 1 through 7 were checked, and there were **zero classification disagreements** with the original results.

- Order 1: connected 1, apiculate 1, graphical 1.
- Order 2: connected 1, apiculate 1, graphical 1.
- Order 3: connected 2, apiculate 2, graphical 2.
- Order 4: connected 6, apiculate 6, graphical 6.
- Order 5: connected 21, apiculate 17, graphical 16, nongraphical 1.
- Order 6: connected 112, apiculate 68, graphical 61, nongraphical 7.
- Order 7: connected 853, apiculate 298, graphical 233, nongraphical 65.

Independent exhaustive product checks agree:

- House × P3: 15 vertices, all 32767 nonempty subsets considered, 2075 closed subsets, zero failures.
- House × K2: 317 closed subsets, zero failures.
- C5 × K2: 323 closed subsets, 65 failures.
- House alone: 27 closed subsets, zero failures.

## A9 and A11

The implementation's parenthesization was compared directly with the displayed equations in Part II. It matches A9 and A11. The independent apex tables reproduce exactly **29 graphical graphs violating their conjunction**, with the two smallest witnesses at order six:

- Atlas 147: 51 closed subsets, all realized. A9 fails at (u,v,w,x)=(3,4,1,0), with left side 2 and right side 1.
- Atlas 148: 46 closed subsets, all realized. A11 fails at (5,2,3,4), with left side 4 and right side 3.

Thus the conjunction A9+A11 is not necessary for graphicality. The original results further report that no graph satisfying the conjunction fails graphicality through order seven; this is only a bounded sufficiency observation, not a theorem for arbitrary graphs. In particular, finding 29 counterexamples to necessity does not provide a replacement characterization.

## Prior art

Part II, Section 4, Lemma 4 explicitly classifies four-element subalgebras of apiculate imprint algebras into six graph-realizable types and three exceptional types R1, R2, R3. The C5 restriction is explicitly R2. The source's proof distinguishes the six graphical types from the three others. Therefore the observed three bad four-point types and the C5 example are verification of existing results, not discoveries.

The source passage was inspected in full. The original isomorphism-classification code correctly minimizes the entire labeled ternary table over all 24 permutations, including the appropriate output relabeling. Its assertion that all 73 nongraphical atlas entries have four-point witnesses is a finite-data assertion only. No extrapolation to larger graphs is justified by the enumeration.

## Weakly median interpretation

Part I defines the excluded configuration using an **unconnected triplet of common neighbors**. In `weakly_median_definition.py`, the test is `not nx.is_connected(G.subgraph(t))`: a disconnected induced triplet, not an arbitrary nonclique. These are materially different. In particular, an induced three-vertex path is connected and is not excluded by this test. Replacing the test with 'not a clique' would be incorrect.

The separate literal TQ! transcription experiment is already marked invalid in the README because of its K2,3 discrepancy; its results must not be used as recognition evidence. The house's explicit triangle-condition failure and the primary theorem using A8/A11 remain the preferred bases for the non-weakly-median conclusion. The earlier clique interpretation should not be propagated.

## Remaining boundaries

- I independently recomputed every atlas graphicality classification, the A9/A11 counterexample count and minimum witnesses, and all listed product counts.
- I inspected but did not independently reimplement the generalized-median enumeration or the four-point isomorphism grouping. Their methods appear structurally correct; they should not be described as independently recomputed in this audit.
- The README's explicit finite-scope warnings and invalid-TQ! warning are appropriate and should be retained.
- These calculations do not solve either unrestricted question in Problem 14.

## Supplemental review: exact edge-rank criterion

**PASS.** Independently reviewed `GENERAL_ATTEMPT.md`, including its infinite-graph scope. The proposition correctly characterizes realization of the restricted interval system by its forced unweighted graph. It remains a realization criterion, not the requested structural characterization.

No finiteness of the graph, local finiteness, or finiteness of an interval is needed. For fixed u,v, every strict basepoint chain has at most d_G(u,v) steps, because integer distance from u strictly increases at each step. The possible chain lengths are a nonempty bounded set of nonnegative integers, so their maximum is attained even when infinitely many vertices or chains exist. This justifies the maximum rank and a maximum-length chain without any compactness assumption.

Each consecutive pair x<y of such a chain is a canonical edge. If z belongs to J(x,y) other than its endpoints, then metric additivity places z between x and y in the same basepoint chain; insertion contradicts maximal length. Thus the forced graph is connected. This part actually holds for any nonempty subset S; closure is needed later for the apex statement.

For necessity, when J=I_H, all basepoint chains have at most d_H(u,v) steps and an H-geodesic attains that number. Hence r_u(v)=d_H(u,v). For adjacent endpoints whose distances differ by one, a geodesic to the nearer endpoint followed by their edge is a geodesic to the farther endpoint. This proves comparability in the direction claimed. Conversely comparable adjacent endpoints have distances differing by exactly one. Incomparable adjacent endpoints must therefore have equal ranks.

For sufficiency, the stated rules make r_u 1-Lipschitz on every canonical edge, and the maximum chain supplies the matching path upper bound. Hence d_H(u,v)=r_u(v). If z is in J(u,v), chains from u to z and from z to v concatenate monotonically in the u-basepoint order by metric additivity; all their edges increase r_u by exactly one. The path through z is consequently geodesic. Conversely an H-geodesic whose total rank increase equals its length must increase rank by one on every edge. The incomparable-edge rule excludes incomparable endpoints, and the reverse-comparability rule excludes a descending edge. The whole geodesic is therefore an increasing basepoint chain, giving the reverse interval inclusion. This verifies the potentially delicate converse-comparability step.

Finally, apex closure retains the ambient meet for each pair in every basepoint order. Once the intervals agree, that meet is also the meet in H, so H is apiculate and the operations agree. No hidden finite-poset argument is required here.

The report correctly identifies the unresolved step: absence of the known closed four-point obstructions has not been shown to imply either the comparable-edge rank rule or the incomparable-edge equal-rank rule. A chosen quartet need not be closed, and invoking an apiculate-graph theorem for H before proving realization would be circular. The randomized search remains secondary bounded evidence only.

Accordingly, a final status of **unsolved after five substantive attempts** is mathematically accurate: canonical obstruction, geodetic subclass, atlas/identity counterexamples, product/four-point approach, and rank reduction with its explicit general gap. Nothing in this supplemental review supports claiming the unrestricted problem solved.
