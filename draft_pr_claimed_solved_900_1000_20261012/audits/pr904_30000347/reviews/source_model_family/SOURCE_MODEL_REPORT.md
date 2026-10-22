# PR #904 / 30000347: independent source-model audit

Checkpoint: 2026-10-13T03:17:17.098105+00:00 (UTC); 2026-10-12T20:17:17.098105-07:00 (America/Los_Angeles).

Completion estimate: **100% of this source-model audit**, not of publication approval. Verdict: **PASS for matching the historical target.** No source/scope repair is required. This is conditional on the reduction being mathematically valid; it is not a current-priority clearance or a merge recommendation.

## Exact claim tested

The frozen proof claims that the following decision problem is NP-complete: input a finite simple undirected graph with unit traversal lengths, three distinct terminals r,s,t that are initially pairwise connected, and a nonnegative integer B; ask whether at most B edges can be deleted so that every one of the three terminal distances increases by at least one. Disconnection after deletion is allowed. Hardness is claimed even when all three initial distances are exactly 3 and all deletion costs are 1. Its extension permits positive rational deletion costs encoded in binary. The optimization versions are claimed NP-hard.

Frozen PROOF.md SHA-256: `f31b19b8e4286e0104ed1e272f5cbc4a39e20aea78aa30334466f5b44e5830f7`.

Success criterion for this family: the cited historical question must ask for this triangle demand pattern and this deletion objective, with no omitted restriction that invalidates the reduction's target instances. A mismatch in direction, metric, terminal pattern, disconnection rule, or required graph class would fail the audit.

## Independently retrieved primary evidence

Krause's workshop contribution defines distances by edge count and distinguishes deletion cost from traversal length. Its first explicit open question concerns the simultaneous pairwise distances among three vertices of an undirected graph, with or without edge costs, using an increase of at least one. The preceding discussion identifies the three pairs as the triangle case; it does not require a planar, bounded-degree, or bipartite graph. [Oberwolfach Report 50/2005, printed pp. 2856-2858](https://ems.press/content/serial-article-files/46024?nt=1).

The dissertation restricts its graph vocabulary to finite simple graphs (p. 5), defines unavailable distances as infinity (p. 7), and defines BSP by hitting original geodesics (p. 2). Its initial-connectivity and positive-cost conventions remove trivial cases; it expressly accepts multicut solutions as feasible BSP solutions. Section 4.3 leaves the undirected triangle case unclassified. Theorem 9.3 instead addresses directed instances. Section 9.2 separates the exact-one variant. [Krause, Increasing Distances in Graphs, pp. 2, 5, 7, 34-36, 83-84](https://webdoc.sub.gwdg.de/ebook/dissts/Braunschweig/Krause2006.pdf).

Both PDFs were retrieved afresh, independently of prior audits, and all 11 listed pages were inspected as extracted text and rendered page images. Full sources and page images remain in the ignored `private_sources/` directory. Public retrieval receipts, page locations, and hashes are in SOURCE_MODEL_MANIFEST.json. No previous audit report was read and no subsequent-priority search was undertaken.

## Adversarial comparison and boundary cases

| Potential substitution or hidden assumption | Finding against the frozen proof |
| --- | --- |
| Directed rather than undirected input | All construction edges are unordered. The directed theorem is not used to prove the result. |
| Three arbitrary pairs rather than exactly three terminal pairs | The demand set is exactly {r,s}, {r,t}, {s,t}. No disjoint-pair surrogate appears. |
| Weighted shortest paths rather than weighted deletion | Length is always the number of edges. The positive rational extension weights only the chosen deletion set. |
| Disconnecting terminals forbidden | Post-deletion finite distance is not required by the target. The proof's infinity convention matches blocking all original geodesics. |
| Initially disconnected pairs create an invalid infinity comparison | The main theorem requires initial pairwise connectivity, and the construction supplies finite distances 3. Removing already-vacuous demands in broader inputs cannot weaken hardness of this subclass. |
| Repeated terminals, adjacency, or distance-zero degeneracy | The three terminals are newly created and distinct. They are nonadjacent and have disjoint neighborhoods, placing them within the nontrivial target class. |
| Multigraph, loops, protected edges, or nonpositive costs | The construction is finite and simple and gives every edge deletion cost 1. It does not depend on broader graph or cost conventions. |
| An implicit planar or degree restriction | No such restriction belongs to the historical triangle question. The theorem claims no hardness for these smaller graph classes. Its terminal degrees may grow with input size. |
| Only selected geodesics blocked | Lemma 2 states a complete characterization of the original length-three geodesics. All three demand pairs are subject to that characterization. Full validity of this lemma belongs to the mathematical audit. |
| Exactly-one or arbitrary-length-threshold question substituted | The main theorem uses at-least-one and original geodesics. The exact 3-to-4 result is clearly optional and does not carry the historical classification. |

## Why the stronger restriction answers the complete intended target

A subclass hardness result is sufficient here. If the claimed polynomial reduction is valid, a polynomial algorithm for the historical unweighted triangle problem would solve every constructed instance with initial distances 3, contradicting NP-hardness unless P=NP. The unit-cost class is also contained in the positive-cost class, so the same reduction classifies the costed problem. Ordinary binary-encoded rational costs give a precise computational input model; arbitrary unencoded real numbers are not a meaningful NP input convention.

The proof's requirement of three finite initial distances is not an easier replacement of the open target. Restricting the hardness proof to initially connected, distinct, nonadjacent terminals strengthens the result. In fact, every construction vertex has a terminal spoke and all three terminals are mutually connected, so the constructed original graph is connected as well.

Nor does the use of distance 3 accidentally import a different threshold question: the required post-deletion condition is still relative to the original distance. Its value happens to be 4 on these instances. A classification on that restricted family determines hardness of the full original-distance problem without asserting a classification of every fixed-threshold or planar variation.

The optional four-edge backup paths address a different, stricter convention. Their presence is not necessary to justify the main source match. The proof expressly limits that strengthening to terminal connectivity and does not claim that all remaining vertices stay connected.

## Strongest verified result and exact remaining gap

Verified: the frozen statement and construction target the undirected triangle BSP complexity question recorded in 2005 and left unresolved in Section 4.3 of the 2006 dissertation. There is no identified historical model mismatch, and the quoted directed theorem is correctly kept separate.

Not established by this report: correctness of every reduction step and computed count; whether later literature already classified this model or supplied an equivalent restriction; novelty of the reduction; publication readiness. Those are independent required gates. Historical open status alone cannot support a present-day priority claim.
