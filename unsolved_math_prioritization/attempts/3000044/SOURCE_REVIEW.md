# Source review and exact structural boundary

## Originating question and credited results

A. Frank, S. Fujishige, N. Kamiyama and N. Katoh, *Independent arborescences
in directed graphs*, Discrete Mathematics 313 (2013), 453–459,
[DOI](https://doi.org/10.1016/j.disc.2012.11.006),
[author PDF](https://andrasfrank.web.elte.hu/cikkek/FrankJ63.pdf), is the
originating primary source. Question 2 asks the prescribed-convex-set
independent-arborescence question; the present target imposes acyclicity.
The simultaneous paths at each terminal must have disjoint arcs and only
the permitted common vertices. A merely arc-disjoint spanning-to-roots
paraphrase would be a different problem.

Theorem 4 supplies common-root DAG existence. Theorem 5 supplies its O(km)
algorithm for weakly connected digraphs with non-singleton prescribed sets.
Theorems 6 and 7 give arbitrary-root results when every vertex belongs to at
most two prescribed sets; Theorem 7 gives the corresponding O(km) algorithm.
These are credited prior results. Counterexamples in cyclic digraphs do not
settle the acyclic target.

## Accepted result and dependency

The self-contained base theorem assumes that each pairwise overlap, after
deleting the common root when applicable and collapsing parallel arcs, has
at most one directed vertex-sequence path between each ordered pair.
Under that condition, terminalwise simultaneous independent paths, local
resource matchings, and coherent independent prescribed-set trees are
equivalent; arbitrary local matching choices suffice.

The stronger root-group theorem imposes uniqueness only between indices
with different roots. Same-root overlaps are unrestricted. Its proof first
constructs root-group arc pools and proves their required path property by
a separator argument. It then invokes Theorem 4 inside each pool, and proves
cross-root independence from disjoint predecessor-tail pools. This stronger
theorem is explicitly source-dependent. Before invoking Theorem 5, singleton
sets are removed and later restored; all remaining pools are weakly connected
because every pool vertex is reachable from its root. Membership/singleton
preprocessing is charged separately.

The depth-at-most-two corollary, unbounded-depth shared-chain family, and
nine-vertex greedy-prefix obstruction are included with their full analytic
arguments. The obstruction has a valid global family and is not a conjecture
counterexample. Arbitrary different-root overlaps with alternative directed
paths remain unresolved. No novelty or current-worldwide-open certification
is made. Problem 3000044 is distinct from the rainbow-arborescence problem 30004008.

## Recorded inspection and supplementary evidence

The accompanying audit records reading the complete seven-page paper as
extracted text, successfully reopening the public author PDF, and visually
inspecting locally rendered PDF pages 1, 4 and 7. A failed web screenshot
attempt was not counted. The recorded PDF is 232,496 bytes, SHA-256
`d40a08b63338bc6137855424683eb3b6b43325880946e876eac6dcd0a5d5b04a`.

The proof-review record reports a bounded search with no checked general
resolution, and an access failure at the exact old Egres problem URL; it
records the [Trees and branchings index](https://lemon.cs.elte.hu/egres/open/Trees_and_branchings).
These are historical observations, not a literature-completeness claim.
[SOURCE_METADATA.json](SOURCE_METADATA.json) preserves their scope.

Finite census, stress and sampled-search counts are retained only as recorded
supplementary verification metadata. They are not the general proof and are
not required for analytic acceptance. Programs, raw outputs and datasets are
omitted. Edition preparation did not rerun those computations or retrieve,
rehash, inspect or search scholarly sources anew. The edition is AI-assisted
and unrefereed; no external human peer review or formal certification is claimed.
