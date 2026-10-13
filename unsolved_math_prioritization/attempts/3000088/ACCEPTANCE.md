# Acceptance of the restricted weighted-coloring results

## Decision

Accept the restricted proofs and method obstructions without a substantive proof correction. The unrestricted bipartite-multigraph question is not solved.

This AI-assisted manuscript is unrefereed. Acceptance means an independent internal AI audit. No external human peer review, journal acceptance, or formal proof-assistant certification is claimed.

## Exact mathematical scope

Let the graph be finite and loopless, with arbitrary real edge weights in [0,1]. A weighted color is feasible if its total incident weight at every vertex is at most one. Let b be the maximum optimal incident unit-bin count. Algorithms receive an integer B>=1 and feasible local partitions into at most B bins. Taking B=b gives existential bounds; no efficient procedure to compute optimal bin packings is asserted.

1. Simple forests admit B colors, and have exact index b when b>=1. The proof uses the unique parent edge to permute local bin labels.
2. Multigraphs with forest support admit 2B-1 colors for unbounded finite parallel multiplicity. Each incoming bundle uses at most B colors. Only q=r=B needs a merge, and the two minimum loads sum to at most one by averaging. Support cycles invalidate that incoming-color invariant and are not covered.
3. For each b>=2, the retained bipartite parallel family has index exactly b+1. It makes the 2b-1 bound sharp only at b=2; all-b sharpness for forest support is not asserted.
4. A simple cactus has a cycle-breaking matching, and therefore admits B+1 colors. The matching argument includes non-bipartite cacti. If b=1, one color suffices. The retained bipartite unicyclic family proves the exact worst-case value b+1 for every b>=2.
5. The retained eleven-edge b=3 graph has exact index four. Its specified frozen optimal root packing needs five colors to extend. The proof fully specifies the incoming loads, outgoing weights, local packings, forced three-color saturation, and successful recoloring. It is a method obstruction, not a counterexample to the conjectured five-color bound.

Empty graphs have index zero. A nonempty all-zero graph has local optimum and index one when every edge must be assigned. Nonempty zero-load bins and used zero-load color names count normally. Disconnected components reuse one palette, and isolated vertices impose no constraint. Supplied packings need not be optimal.

## Attribution and evidence

Sannyasi's Theorems 10 and 11 were directly inspected for the stated simple edge-disjoint-cycle and multigraph-tree bounds. The matching-deletion proof here is self-contained. Huc's indexed abstract lacks the mathematical formula, and primary publisher access returned HTTP 403. Its exact theorem and proof remain unverified and are not imported as dependencies. Known-subclass attribution prevents any novelty claim. No cited paper is fully proof-audited here.

The independent historical audit verified the written proofs, all seven central graph instances, all 224 stored rejection assignments, 10,976 support-path colorings, 2,187 cactus-grid colorings, 59,377 rooted structural cactus checks, and cross-checks and semantic controls under normal Python, -O and -OO. The original merge-event count depends on packing tie-breaking and was not reproduced; no mathematical claim relies on it. Independent graph/root counts, feasibility and certificate conclusions agreed.

The complete analytical proofs, parameterized construction formulas, and the full frozen b=3 construction are retained. This is not a computational reproduction package: raw assignment tables, certificate packages, detailed instance records, generated grid realizations, checker programs, copied source documents and images are omitted. The seven central graph instances are mathematically specified by the retained all-b families and frozen construction, but the stored certificate realizations and the other finite grid/control inputs cannot all be reconstructed from this edition alone. Historical finite checks support the proofs; no universal theorem depends on those computations.

The public edition introduces no substantive theorem change. It adds review-status, empty-case and reproduction clarifications, records historical verification accurately, supplies the verified historical Feige–Singh PDF URL, and excludes non-public material. ACCEPTANCE.json binds the accepted originals separately from the edited public documents. Preparation included no new mathematical runs or scholarly-source inspection.

## Remaining question

The unrestricted Chung–Ross target remains unresolved by this work. No novelty, priority, or comprehensive current-openness claim is made.
