# Research and source-validation log

Observation date: 2026-10-05 UTC. This is a bounded investigation, not an exhaustive bibliographic survey.

## Identity and model

The available descriptor index associates ID 30002167 and OWR-12012-009 with the report DOI 10.4171/OWR/2012/40. The exact aggregator URL https://www.unsolvedmath.com/problems/30002167 returned HTTP 403 through the direct request, while web retrieval was unavailable. Its actual page text was not inspected, and no source-text match to that page is claimed. The raw AI corpora were absent and uninspected.

The primary report's printed page 2488 (PDF page 60, zero-based index 59) was inspected as text and as a rendered image. It asks separately for a planar radius-one disk tour bound 8 and, for even sets, a full-matching bound 4, both for sums of squared Euclidean edge lengths. It also asks broadly about other convex figures. The report does not impose even cardinality on the tour question. The six-point certificate would refute that version too if even cardinality were added. Points are arbitrary members of the disk, not necessarily its boundary or vertices of a convex polygon.

## Prior-attempt checks

Read-only GitHub searches in AlecKriebel/Math returned no PRs for the exact ID or the exact OWR identifier, no exact-ID branch, and no exact-ID commit matches. Searches for Hamiltonian and convex names returned only unrelated problem branches/PRs. Both paginated branch searches were followed to exhaustion. The default-branch attempts directory contained 62 entries and no folder named 30002167. A direct request for that folder returned 404. Default-branch code search for the exact ID returned no results. These checks are stronger than treating a queued/zero descriptor as proof of no prior work, but do not exclude deleted branches, unindexed contents, or inaccessible history.

The available conversation-history search returned unrelated-topic summaries and no reliable target-specific prior proof or counterexample. Such results were not treated as evidence of an actual earlier attempt. A local filename search found no earlier target-specific work folder before this investigation. No assertion is made about unavailable history.

## Literature checks before the proof was retained

Searches included the exact problem title and OWR identifier, Musin with sum of squares, Hamiltonian with disk and squared lengths, and matching with unit disk and squared lengths. The primary report was recovered and its Bern-Eppstein reference followed. No relevant later primary resolution was established by these searches. Unrelated graph-theoretic Hamiltonicity, disk-intersection matching, and maximum-sum matching results were not used.

Marshall Bern and David Eppstein, *Worst-Case Bounds for Subadditive Geometric Graphs*, was downloaded from Eppstein's institutional publication page. Its introduction explicitly distinguishes the sum-of-edge-lengths optimization from subsequent power-weighted evaluation. Its logarithmic lower bound for power costs of length-minimizing tours cannot be used as an unboundedness claim for tours chosen to minimize squared lengths. Only this scope distinction and bibliographic facts were inspected and used; a full independent proof audit of that paper was not performed.

## Substantive approach 1: separated clusters

A three-vertex equilateral triangle already exceeds the tour constant. To remove small-cardinality, parity, boundary, and numerical concerns, an explicit six-point rational instance was constructed in the open disk. A cut-count argument gives an analytic lower bound exceeding 8 for every tour. Exhaustive exact enumeration of all 60 undirected tours gives its exact optimum. The same clustering argument proves any putative universal tour bound must be at least 9, without asserting sufficiency. Complete proofs are retained in PROOF.md.

The perfect-matching bound remains separate: the example has an optimal matching of cost 3/10000. No claim is made that five matching approaches were completed. This packet records one substantive counterexample approach and the precise unresolved remainder, rather than treating a partial negative answer as a complete resolution of all questions.
