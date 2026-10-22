# Common two-color lists on subcubic critical graphs

Row 1751, problem 3200, OPG 388. Authored mathematics and independent audit dated 12 October 2026 UTC. This is the fourth accepted substantive research round in the present continuation. It proves a restricted theorem with no bound on the number of exceptional lists and includes a separately accepted bounded six-unit method classification. The unrestricted conjecture is unresolved by this work, and no historical novelty is claimed.

## Exact result

Let G be a finite simple graph of maximum degree at most three. Suppose G is not properly three-edge-colorable, but G−e is properly three-edge-colorable for every edge e. Give every edge a list of exactly three colors. If the assignment is nonconstant and at least two colors belong to every list, then G has a proper list-edge-coloring.

There is no bound on the number of vertices or edges, distinct lists, introduced colors, or exceptions relative to a chosen palette. Within this global-common-two-color family, an assignment is uncolorable if and only if it is constant. In particular, nonconstant common-omission substitutions are colorable on arbitrarily large supports, including when every edge is changed and the resulting lists are not all identical.

The proof is fully symbolic. It derives the one-edge-containing-component property from criticality, collapses the third colors to two proxy palettes, selects a minority edge at a mixed vertex, recolors a matching and restores the individual third colors. The local lemma is proved in full. Neither the preceding five-exception theorem nor a finite enumeration is a logical dependency.

## Complete authored contents

- [THEOREM.md](THEOREM.md): the complete accepted theorem and proof, common-omission corollary, exact constant-list boundary, six-edge support classification, explicit critical graph and method separation
- [AUDIT.md](AUDIT.md): the complete substantive independent audit, every proof step, support review, criticality certificates, finite coverage, controls, reproduction modes and acceptance limits
- [ACCEPTANCE.json](ACCEPTANCE.json): scoped acceptance with identities of the actual distributed proof and audit
- [CHECKS.md](CHECKS.md) and [AGGREGATE_CHECKS.json](AGGREGATE_CHECKS.json): author and independent corroborative counts, exact tested domains and reproduction limits
- [SOURCES.md](SOURCES.md): primary sources, inspected versions, corrected bibliographic title, bounded search and explicit retrieval limitations
- [METHODS.md](METHODS.md), [AUDIT_METHODS.md](AUDIT_METHODS.md) and [METHOD_ACCEPTANCE.md](METHOD_ACCEPTANCE.md): the complete complementary six-unit method analysis, substantive independent audit and scoped acceptance
- [SCOPE_CORRECTION.md](SCOPE_CORRECTION.md): the explicit retraction of a false extension implication, with its complete small counterexample in METHODS.md
- [METHOD_CHECKS.md](METHOD_CHECKS.md) and [METHOD_AGGREGATES.json](METHOD_AGGREGATES.json): exact finite normalization, pointwise three-program agreement, all aggregate counts, controls and the computational reproduction boundary
- MANIFEST.json: identities of the actual distributed files, excluding the manifest itself

## Six-edge frontier and explicit example

If six support edges in a finite simple subcubic graph each meet at least three other support edges, their nonisolated support is K₄ or K₂,₃. The complete proof does not assume connected support. K₄ is incompatible with the ambient graph's edge-criticality, while K₂,₃ defeats both purely support-based sufficient conditions considered in the local lemma. This is a boundary of those sufficient conditions, not an obstruction to list colorability.

The complete nine-vertex, thirteen-edge critical example is preserved, including its edge order, matching-capacity proof of non-three-colorability, seven representative deletion-coloring triples, two automorphisms and the seven edge orbits covering all thirteen deletions. For its six-edge K₂,₃ support, a particular deletion coloring uses all three ordinary labels on the selected edge's exceptional neighbors. That fixed choice blocks the local construction. The exact reversed-palette construction gives a proper full list coloring for the same lists. No claim that all deletion choices fail is made for this example.

## Complementary six-unit method classification

Exactly six one-color substitutions with varying omitted base colors form a separate, bounded method analysis. It classifies 47 support line-graph types and every exterior singleton equality pattern, totaling 1,154,461 normalized cases. Three independently written programs agree point for point. The ordered phase totals are 1,095,050 strict-deficit cases, 56,674 additional universal three-residual cases, 2,725 additional deletion-adaptive cases and 12 method-obstruction records.

Four records lie on the impossible K4 support. The other eight patterns have examples in three actual critical graphs. Six examples block every ordinary-deletion-derived repair for the selected edge; two verified Kempe switches repair selected failures. All eight nevertheless have proper full list colorings with the selected edge exterior. The explicit seven-edge example proves why: its ordinary coloring on G−F cannot extend to G−e. The false inference from failure of every deletion-derived repair to full selected-edge-exterior impossibility is expressly retracted.

The local support failure has quantifiers “for every deleted edge, some ordinary local coloring blocks every permutation.” It does not mean that every ordinary coloring fails or that local witnesses simultaneously occur in one graph. The six exhaustive actual failures have the stronger negative quantifier only for their selected edge and only for the deletion-derived scheme.

The complete symbolic method-sufficiency, uniform-omission K2,3 boundary, quantifier and nonextension arguments are preserved. The finite phase classification relies on completed exhaustive computations; its raw orbit, witness and ordinary-coloring collections are excluded. This finite classification is not a premise of the common-two-color theorem. The complement does not settle all six-unit patterns or all six arbitrary exceptional lists.

## Distribution and reproduction boundary

All symbolic proofs, substantive mathematical audit arguments and explicit authored small examples are included. The common-two-color theorem is complete without the computational suites. The separate method classification uses exhaustive finite verification, with the distinct evidence and reproduction limits explained above. Author checks cover 2,127,942 nonconstant assignments and several overlapping construction domains; the independent audit covers 11,396 nonconstant assignments and 1,838,448 complete constructions. CHECKS.md distinguishes their fixture sizes, witnesses and choice quantifiers. These counts must not be added as disjoint coverage, and they do not count distinct final colorings.

Executable programs, compiled binaries, raw support/fixture/certificate/coloring collections, raw run outputs, copied third-party source documents, dataset contents, private original-input identities, hashes and byte counts, and coordination records are excluded. The raw machine records cannot be reconstructed or the computational suites rerun from this prose alone. Computational reproduction requires a fresh implementation and fresh input generation. The public manifest identifies only files actually distributed in this edition.

## Relation to preceding results and remaining question

The preceding third-round theorem covers at most five exceptions to a palette in every degree. This fourth round instead allows arbitrarily many exceptions in degree three when two colors are globally common. It does not prove colorability for arbitrary varying-omission lists with no globally common pair, for arbitrary six-exception assignments, or in higher degree. The preceding editions remain separate historical records; no earlier proof or finding is replaced here.

Four accepted substantive rounds are confirmed in this continuation. The common-two-color theorem and complementary six-unit method analysis belong to the same fourth round; parallel directions within a round are not counted separately. An earlier screen exists, so total lifetime attempts remain unknown. The row remains unsolved. The bounded source review does not establish novelty or certify comprehensive current literature status.
