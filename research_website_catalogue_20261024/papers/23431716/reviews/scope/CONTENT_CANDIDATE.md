# Conditional content candidate — Zenodo 23431716

This copy is grounded in the published scope. It is not approved for publication until the independent mathematical review is complete.

## Title and search description

Title: Chip-firing halting is NP-complete on simple directed graphs

Suggested slug: `chip-firing-halting-simple-digraphs`

Description: An attributed proof of NP-completeness for conservative chip-firing halting on simple directed graphs, including graphs without antiparallel arcs.

Published title: *A modular-storage proof of NP-completeness for chip-firing halting on simple digraphs*.

Author: Alec Kriebel. Version 1.0, 16 October 2026. [Zenodo record](https://zenodo.org/records/23431716), DOI [10.5281/zenodo.23431716](https://doi.org/10.5281/zenodo.23431716).

Status: Unrefereed preprint. The paper discloses extensive AI assistance and has not received external human peer review. Its exact full-result and realization priority remain unknown. Any new internal-review status must come from the completed mathematical reviews, not this scope assignment.

## Plain-language explanation

Place a pile of chips at each vertex of a directed graph. A vertex can fire when it has enough chips to send one along every outgoing arrow. Firing moves chips around without creating or removing any. The question is whether the process can eventually reach a position where no vertex can fire.

The paper gives an attributed proof that deciding this is NP-complete even when the graph has no loops or repeated arrows and every vertex can reach every other vertex. A separate construction also rules out pairs of arrows pointing in opposite directions. The difficulty persists with polynomially many initial chips and a graph that becomes exceptionally shallow after removing one specified vertex.

The construction encodes a Boolean formula using counters that cycle through residues modulo small primes. Their combined chip storage reaches a chosen maximum exactly when the residues describe a satisfying assignment. An ordinary root vertex then becomes unable to fire precisely at those successful checkpoints. The proof accounts for each legal firing and the return of every emitted chip, and uses least action to connect this chosen order to arbitrary legal play.

The counter mechanism and prime-residue encoding have classical antecedents, which the paper credits explicitly. Its subject is their conservative graph realization and the complete halting reduction. NP-completeness does not mean that every input takes a long time, and the short verification certificate does not give a polynomial-time simulation of the game.

## Exact result

The claimed theorem concerns finite loopless simple strongly connected digraphs with at least two vertices, nonnegative integer chip configurations encoded in binary, and the ordinary outdegree firing rule. HALTING asks whether a finite legal sequence reaches a stable configuration. There is no dissipative sink.

The reduction is deterministic and polynomial in the explicit 3-CNF input length. Its output has a specified root whose removal leaves an acyclic graph with no path of two directed arcs. The numerical total number of initial chips is polynomial, so the hardness also applies when chip counts are written in unary. The oriented construction forbids antiparallel arcs. It does not claim bounded degree, an Eulerian graph, or polynomial simulation time.

NP membership is credited to Farrell–Levine and reproved with an explicit firing-count certificate. The modular counter priming is credited to Holroyd–Levine–Winkler. The prime/Boolean/clause encoding is credited to Stockmeyer–Meyer and to Gregor Gramlich's reconstruction. The publication does not claim first discovery or establish that the historical question remained open immediately before this work.

## Abstract and assets

Use the **complete original abstract** from `ORIGINAL_ABSTRACT.md` or `abstract_original.txt`; it includes the attribution and review-status qualifications and must not be shortened into a novelty claim.

The real top-level [published PDF](https://zenodo.org/records/23431716/files/paper.pdf?download=1) has seven pages and SHA256 `52d4355533f5095be83c8799bd148e9927e5c4bef8c2f6a00d534303f0b7ee5c`. The [published support archive](https://zenodo.org/records/23431716/files/pr1098_support_v1_0.zip?download=1) has SHA256 `a9606c07600ca9ac60f36f5165c8c09ff3e0c0b42e83e50d006df6f1ee2723fe` and contains the complete TeX source, current diagnostics and preserved authored history. It contains no additional manuscript PDF and no third-party primary-source PDF.

The historical reports inside the support archive are not separate papers or new independent reviews. Old preparation fields stating that publication was held are dated workflow history; the current public record is a released preprint.

## Follow-up recommendation

None proposed. A question about further graph restrictions needs a separate novelty and feasibility assessment before it is worth presenting as a paper-worthy research direction.
