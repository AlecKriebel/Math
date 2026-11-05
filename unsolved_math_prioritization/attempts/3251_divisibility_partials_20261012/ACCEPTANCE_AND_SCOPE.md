# Mathematical acceptance and edition scope

## Decision

The two preserved independent audits accept the stated partial mathematics without requiring mathematical corrections to the accepted frozen proofs. The unrestricted odd-hole-free 2-divisibility conjecture remains unresolved. These are independent AI audits, not human peer review, formalized proofs, or a novelty certification.

The structural author's initial checker used optimization-sensitive Python assertions. This implementation defect was corrected before the accepted freeze. The accepted checker uses explicit failures and was independently replayed in normal Python, -O, and -OO. The correction is part of the recorded history, not concealed by the final passing results.

## Accepted structural content

Color grouping gives division whenever chi is at most 2omega−2. The clique-number-two case is elementary. The clique-number-three case uses the external Chudnovsky–Robertson–Seymour–Thomas theorem, whose statement and local context were checked but whose entire proof was not re-audited.

The minimal-obstruction proofs establish deletion invariance of the clique threshold; paired disjoint neighborhood cliques with a perfect matching of nonedges; order and degree bounds; connectedness and absence of a cut vertex in the maximum-clique edge core; connected complement; and module-freeness, including the stable-module case.

Clique-precolor extension and exact separator compatibility are proved. The component-orbit bound and every-side chromatic/order obstruction follow without assuming that a general clique-cutset gluing theorem exists. The finite universe through six vertices contains no minimally indivisible graph with a clique cutset. Therefore the critical-separator numerical claims have no nonvacuous small-order test instance and rest on their complete written proofs. The separator identity and precolor extension have many nonvacuous tests.

The induced-P5 restriction invokes Chudnovsky–Sivaraman's (P5,C5)-free theorem. The optional odd-antihole restriction invokes the Strong Perfect Graph Theorem. Neither full external proof is established by this edition. Hoàng's general clique-cutset exclusion is treated as a conjecture, not an accepted theorem.

## Accepted hypergraph content

The shadow criterion is an exact realizability equivalence, with nonempty hyperedge family and maximum-cardinality cliques essential. The Fano configuration fails realizability as maximum triangles despite being non-two-colorable. The all-size chordal construction proves the failure of odd-hole-freeness preservation under removal of edges outside maximum cliques, while every graph in that family remains divisible.

The incidence-two theorem covers arbitrary finite hypergraphs with all edges of size at least three, including nonuniform families, repeated labelled edges when incidence counts multiplicity, and isolated vertices. Its proof handles the odd-length Euler circuit whose start is a real dual vertex. Size-two edges are excluded. The Hall union condition is sufficient, not necessary. The combined incidence bound is a necessary obstruction condition, not a full characterization or a solution to the graph problem.

## Preservation and reproducibility boundaries

STRUCTURAL_PROOFS.md and HYPERGRAPH_PROOFS.md contain the complete authored arguments. STRUCTURAL_AUDIT.md and HYPERGRAPH_AUDIT.md retain the complete substantive mathematical reviews, exact scopes, control outcomes, implementation correction and limitations. SOURCES.md preserves the full bounded source-frontier review and its inspection levels. Short summaries in this file and README.md do not replace those texts.

Original identities and sizes of omitted proofs, packets, programs, raw coverage collections, controls and receipts are excluded. Public-source PDF metadata identifies publicly retrieved byte streams, not proof correctness or journal-version identity. PUBLIC_MANIFEST.json describes only actual distributed files. The manifest itself is accounted for by the separate external preparation freeze, avoiding self-hashing. The complete preparation has a private closed inventory and reversible editorial checks; those operational materials are not part of this public prose edition.

The original executable computations and raw coverage data are not distributed, so this edition reports their accepted audit outcomes without advertising a self-contained executable reproduction package. Small authored finite graphs and hypergraphs remain available in SMALL_WITNESSES.md and can be checked directly.

## Attempt accounting and unresolved work

This is the second confirmed substantive pass: the earlier screen established the elementary baseline and inspected known subclasses, while this continuation supplied the structural and hypergraph partials. The lifetime total is unknown. Independent audits, source verification, integrity checks and edition preparation do not add research rounds. No ongoing subsequent round is incorporated here.

The queue proposal is confined to row 1753's Status, Turns and Findings cells: unsolved; at least two confirmed passes with lifetime total unknown; and a concise linked description of these accepted partials and remaining gap. No queue or remote mutation has been made by this preparation.


## Prior-credit update

The separately checked Hu–Xu–Zhuang preprint arXiv:2603.01967v2 already states directly overlapping minimal-non-2-divisibility necessary conditions: the minimum-degree bound, full clique number on cutset pieces, incompatible boundary traces, and maximum-clique blocking at minimum-disagreement traces. The complete arguments retained here are independent derivations without a novelty claim. See the [complete prior-credit audit](PRIOR_CREDIT_AUDIT.md) and [source ledger supplement](SOURCES.md). That source does not prove unrestricted clique-cutset exclusion or the target conjecture. Its distinct MNPD questions are kept separate from the later, explicitly conditional [status caveat](RELATED_STATUS_CAVEAT.md).
