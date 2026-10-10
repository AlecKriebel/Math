# Independent audit of the greedy spanning tree partial results

## Verdict

**Accepted as a partial-results report. No mathematical correction is required.** The exact coefficient formula, the theorem for dilations 1 through 4 of every 0–1 integer-decomposition polytope, the theorem for connected multigraphs with at most four vertices, the K5 theorem and its parallel extensions, and the two failed-selection-rule examples withstand this audit.

**The general spanning-tree question remains unresolved by this work.** These results do not resolve aggregate 30001932 or justify a solved status for problem 30001934. The audit adds zero research approaches. The existing five-approach stopping point remains unchanged. No novelty or current-openness certification is made.

The reviewed mathematical report is 11,848 bytes, SHA-256 `581bcaaef2bc3b3ee5554cdefb23cbfa0de05ad1ed44a821bc0be0139c00bb46`. The reviewed author manifest is 5,512 bytes, SHA-256 `64512846264e72ac8b25781f9502a5553ac9865ea6e1e980906ff5162ca29c15`. Its 33 allowlisted files matched their recorded sizes and hashes. Those hashes identify the precise accepted version.

## Original scope and conventions

I independently inspected Question 3 and its preceding definition on printed page 3027 of [OWR 53/2011](https://ems.press/content/serial-article-files/46369), including the rendered PDF page. The source is Dion Gijswijt's contribution with Guus Regts. It quantifies over positive integral k and integral w in kP, asks for an integral x in P, and asks whether the largest feasible coefficient is an integer. It explicitly permits lambda equal to zero and does not explicitly require a positive maximum. Questions 1 and 2 on that page have different targets.

The report openly adds lambda at most k and the convention 0P={0}. This is a necessary nonnegative-residual-mass convention, rather than a consequence of the printed lower bound alone. If negative scalar dilations are used literally, even a singleton polytope and w=kx allow arbitrarily large lambda. In fact the same issue occurs for w=kx in any polytope containing x. The report's singleton example already establishes the defect; no correction is needed.

Accordingly, all acceptance statements here use the report's disclosed interval [0,k]. They preserve the printed permission for an integer maximum of zero. The report correctly distinguishes that weak statement from a positive greedy step. Its stronger positivity claim for k at most 4 is separately proved. Relative-interior inputs have positive feasible coefficients for every vertex, as follows by extending the segment slightly from the vertex through the relative-interior point.

The one-vertex empty-tree case has maximum k. Loops have zero coordinates. Parallel edges remain distinct coordinates. Disconnected graphs have no positive-dilation input in the spanning-tree polytope; replacing that object by a forest polytope would change the question and is not done.

The cited [Gijswijt–Regts paper](https://www.math.ucdavis.edu/~deloera/TEACHING/READINGSEMINAR/PAPERS/gijswijt%2Bregts.pdf) supplies the integer decomposition and integer Caratheodory background for matroid base polytopes. These statements do not by themselves constrain the maximum coefficient. No uninspected result from Chaourar is needed for any accepted proof.

## Exact coefficient formula

The formula is valid. For a proper nonempty vertex set S, substituting z=w-lambda 1_T and residual mass q=k-lambda into the induced-subgraph inequality gives

lambda (|S|-1-|T intersect E(S)|) <= k(|S|-1)-w(E(S)).

The denominator is nonnegative because T[S] is a forest. If it vanishes, the already nonnegative input slack makes the condition automatic. A selected edge contributes lambda<=w_e; an unselected edge's coordinate remains nonnegative. Total mass holds identically because a spanning tree has n-1 edges. The mass bound lambda<=k handles q=0 and the empty-tree case. Together these conditions give exactly the minimum displayed in the report, with attainment.

The cited polytope description includes all the necessary conditions. The reduction from arbitrary edge-subset rank inequalities follows by partitioning an edge subset into its vertex components and bounding each part by all induced edges on that component. When the edge subset connects all vertices, the total equality supplies the full-vertex bound. Conversely, rank inequalities imply the displayed induced-subgraph bounds. The greedy support-function argument for the forest polytope and its total-rank face is valid; negative objective coordinates may be discarded because the independence polytope is downward closed.

To avoid checking the formula solely against a second copy of itself, the independent executable computes connectivity by graph traversal and uses every **edge-subset rank inequality**, rather than the author's induced vertex-subset implementation. It verifies input membership, all recorded tree lists, each claimed endpoint, feasibility at that endpoint, and infeasibility after adding 1/1009. It also checks that every recorded limiting constraint is actually binding.

## Low dilation theorem

The proof for a nonempty 0–1 polytope with the integer decomposition property is sound and is not specific to graphs.

- An integral point of the polytope is a 0–1 vertex: a convex representation cannot vary in a coordinate whose average is 0 or 1.
- If w has a coordinate 1, a summand using it has feasible coefficient 1 and cannot exceed 1 by nonnegativity.
- If w has a coordinate k-1, a summand not using it has feasible coefficient 1 and cannot exceed 1 because every residual coordinate is at most the residual mass.
- For k at most 3, absence of those coordinates leaves only 0 and k, so every summand agrees and coefficient k is feasible.
- For k=4, after removing coordinates 1 and 3, w/2 is an integral point of 2P. An integer decomposition w/2=x+y makes coefficient 2 feasible for x. If x differs from y, one differing coordinate bounds that coefficient by 2, in either orientation. If they agree, coefficient 4 is feasible.

This covers singleton polytopes, the zero vertex, and k=1. No assumption about full dimension or positive coordinates is hidden in the argument. The related slack-one certificate is also valid whenever the required integer decomposition is available: the integral nonnegative summand deficits add to 1, so one equals 1.

## Graphs with at most four vertices

For at most three vertices every proper nonempty induced-tree deficit is at most 1. On four vertices a Hamiltonian path has no independent three-vertex set, so it has the same bound. If a connected simple four-vertex graph has no Hamiltonian path, any spanning tree must be a star. An additional leaf-to-leaf edge would give a Hamiltonian path; hence the graph is that star and its polytope is a singleton. This exhausts the cases.

The independent structural check enumerates the 44 connected labeled simple graphs on one through four vertices. Exactly four are the non-Hamiltonian four-vertex stars. The chosen paths have the required denominator bound. This finite check is a corroboration of the preceding argument, not its replacement.

For a multigraph, summing coordinates within each parallel class maps its tree polytope onto that of the simple underlying graph. A lifted tree and its projection have identical induced-subgraph counts and input sums. Its endpoint is therefore the minimum of the projected endpoint and the individual weights of the chosen representatives. The class-sum edge bounds are redundant once those individual bounds are imposed. All those additional bounds are integral, even when some are zero. Loops remain fixed zero. This establishes the full multigraph extension without a bound on multiplicity.

As an extra implementation check, all 24 spanning trees of a K4 with one edge doubled and one loop added satisfy that exact projection/minimum identity. This supplements the one-vertex, unique-tree, and two-parallel-edge endpoint fixtures.

## Complete graph K5

The averaging and path arguments are correct for every positive k and every integral w in kP(K5).

There are ten three-vertex sets. Every edge belongs internally to three of them and crosses six of their cuts. Each cut has six edges. Consequently the sum of internal weights is 12k, and the sum of minimum crossing weights is at most 4k. The average of internal weight plus twice the minimum crossing weight is at most 2k. Thus a suitable set S exists, including when weights vanish.

Every selected crossing edge can be placed in an alternating path through the three vertices of S and two complementary vertices. In this five-vertex path, S is the unique independent triple. Every four-vertex induced subgraph has at least two edges. It follows that S is the only proper subset with deficit greater than 1, and its deficit is exactly 2. Its possible fractional endpoint is at least the weight of the selected crossing edge. That integral edge bound is already present, so the fractional bound cannot lower the minimum of the other, integral bounds.

The independent test checks all 60 combinations of a triple and a crossing edge, along with the edge-counting multiplicities. No case has an additional higher-denominator subset. The proof extends to nonempty parallel classes and loops by the preceding projection argument.

Completeness is genuinely used to build the alternating path. Assigning zero weights to missing edges does not transfer the chosen tree back to an arbitrary five-vertex graph. The report explicitly states this limitation. The proof is also not an induction to higher-order complete graphs.

## Selection rule counterexamples

All three recorded examples pass independent exact edge-rank verification across every spanning tree, 157 trees in total.

1. Uniform weights 3 on K4 at k=6 have 16 spanning trees. The star endpoint is 3/2 and a path endpoint is 3. Twelve trees have integral endpoints. This rejects the inference from one fractional tree to a counterexample to the question.
2. The stated K5 vector at k=10 has 125 spanning trees. The largest endpoint is 9/2; 105 trees have integral endpoints. Hence maximizing the endpoint globally need not yield an integral value. The smallest endpoint is 5/3. This does not refute the original existence statement.
3. The stated K4 vector at k=20 has a unique maximum-total-weight spanning tree, the star of weight 35. Its endpoint is exactly 15/2, from leaf-triangle slack 15 divided by 2. Fourteen of the 16 trees have integral endpoints. The largest endpoint among all trees is 9, but that is not the asserted objective of the failed maximum-weight rule.

All recorded per-tree witnesses bind. The independent tree lists match the recorded lists exactly, so omission of unexamined integer-endpoint trees cannot turn these records into false universal counterexamples.

## Reproduction and failure controls

Verification ran with real UID 1000 and effective UID 1000. The author allowlist was copied into a separate snapshot with files mode 0444 and directories mode 0555. Actual attempts both to append to an existing sentinel and to create a new file failed with PermissionError, errno 13. The snapshot and original author's packet had identical byte inventories before and after the nine main verification runs.

Under each of normal Python, -O, and -OO:

- The original core suite passed with 2,680 points: 1,680 feasible K4 inputs at k=1 through 4 and 1,000 seeded K5 inputs.
- The original saved-adversarial-point checker reproduced the saved exact summaries: 54 of 125 integral endpoints for K5, 623 of 1,296 for K6, and 6,909 of 16,807 for K7.
- The independent suite passed the 157 recorded endpoints, 44 small-graph structural cases, 60 K5 path cases, 24 parallel-extension tree cases, and degenerate/boundary fixtures.
- Nine deliberately false endpoint or selection claims were rejected, including omission of subset bounds, integer rounding, accepting one fractional tree as a target counterexample, global-maximum integrality, maximum-weight integrality, exclusion of zero, loss of the rank-zero mass bound, collapsing parallel-coordinate bounds, and negative residual mass.
- Five actual in-memory mutations of the author's source were rejected by the independent endpoint oracle: omitted subset facets, rounded-down endpoints, omitted selected-coordinate bounds, omitted mass bound, and replacement of zero by a positive endpoint. The mass-bound mutation fails closed on the rank-zero fixture; the other four disagree with the independent endpoint. Mutated code was compiled under the corresponding optimization mode and never written into the author packet.

These verification and mutation runs are not new discovery attempts. All enforce existing statements or fixed fixtures. Runtime guards use explicit exceptions and do not depend on assertions. The source-mutant results are separately recorded for the three modes. `certify_examples.py` is an output generator, so it was not invoked to overwrite an immutable source record; the audit instead verified its entire existing certificate output independently.

For reproduction, set `GREEDY_PACKET` to the reviewed author packet and run `python -B independent_exact_audit.py` and `python -B test_source_mutants.py` from this audit's `tests` directory. Repeat with `-O` and `-OO`. The separate `run_readonly_audit.py` creates a fresh permission-restricted snapshot and refuses to replace a pre-existing one; the individual verifiers can safely be rerun against the existing snapshot. The verifiers write only standard output.

## Finite search limits

I inspected the discovery code and saved summaries. The bounded-box counts add to 90,976 feasible points. The sparse-graph record contains 64 graph runs and 160,000 sampled points. These saved historical search totals were not re-executed by this audit, and no claim of independent replay of those searches is made.

The reported common-unit-interval infeasibilities are floating-point solver statuses, not exact certificates. Its K7 run reached a time limit without a candidate. The adversarial K7 record is explicitly an interrupted run, and its `checked` field is a proposal count when the best point was found. The independent work does not convert those outcomes into exhaustive nonexistence results.

The universal partial theorems rest on their mathematical proofs. The finite checks validate implementations and certificates. Neither establishes the remaining all-graph assertion.

## Corrections and accepted scope

Required corrections: none. The report already makes the necessary distinction between the printed coefficient domain and its nonnegative-mass repair, between zero and positive coefficients, between K5 and arbitrary five-vertex graphs, and between failed selection rules and the original existence question.

The acceptance is limited to the reviewed hashes and the partial mathematical statements above. It does not authorize a solved classification, an additional research approach, publication of copied sources, or a change to unrelated work. No repository publication or queue change was performed by this audit.
