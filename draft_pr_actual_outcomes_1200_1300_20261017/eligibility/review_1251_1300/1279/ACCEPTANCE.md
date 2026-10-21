# Cycle continuous antichains literature acceptance

## Decision

**Accept as a known positive resolution of problem 3223 / OPG-323.** There is a sequence of finite cubic bridgeless graphs such that, for every pair of distinct indices, no cycle-continuous edge map exists in either direction. This is the exact requested infinite antichain, with stronger graph restrictions than the question requires. The result is due to Robert Šámal; no novelty is claimed here.

The source is Robert Šámal, *Cycle-Continuous Mappings—Order Structure*, Journal of Graph Theory **85**(1), 56–73 (May 2017), [DOI 10.1002/jgt.22047](https://doi.org/10.1002/jgt.22047). The publisher records first online publication on 12 June 2016. The inspected full text is [arXiv:1212.6909v1](https://arxiv.org/abs/1212.6909v1), submitted 31 December 2012. The relevant locators in **that 12-page version**, not asserted journal-page locators, are Theorem 1.3 on PDF page 2 and Corollary 3.5 on PDF page 9.

## Exact problem and definition match

The question asks for infinitely many pairwise incomparable graphs under edge maps whose inverse images preserve binary cycle spaces. The [original Open Problem Garden page](https://www.openproblemgarden.org/op/antichains_in_the_cycle_continuous_order) gives this same question and describes the ambient graphs as finite with at least one edge. Its retained open wording is superseded by the published result.

Write Z(G) for the kernel, over the two-element field, of the vertex-edge incidence matrix of G. Equivalently, Z(G) consists of edge sets having even degree at each vertex; it includes the empty set and disconnected unions of circuits. An edge function f from G to H is cycle-continuous precisely when f inverse-image maps Z(H) into Z(G). This is the convention on page 1 of the arXiv paper. It is not a requirement that the inverse image of a simple circuit be a single connected circuit.

The source permits loops and parallel edges in its ambient category. The antichain construction uses finite simple cubic graphs, so it also answers the question if “graph” is interpreted as simple. Connectedness and bridgelessness do not weaken the conclusion. The original page reverses the symbol used for the order; incomparability is unaffected.

The countable-poset extension is separately stated as Theorem 1.4 and Corollary 3.6, with construction on PDF pages 9–11: for any countable poset P, graphs can be assigned to its elements so that p is below q exactly when the corresponding cycle-continuous map exists. The construction there uses finite cubic bridgeless graphs. This stronger statement is not needed for the present acceptance, and its directed-path universality dependency was not independently reproved here.

## What was checked

The definition, theorem statements, construction, proof dependencies, and concluding restrictions were read. Pages 2, 6, 7, 8, 9, and 11 were also rendered and visually inspected. The publisher abstract and bibliographic record were independently read. The publisher full text was not acquired; it returned access errors. No claim is made that the arXiv file and final journal file are byte-identical.

The following independent checks supplement the literature inference:

- The two displayed 18-vertex Blanuša graphs were manually transcribed and checked with newly written standard-library code. Each has 27 edges, girth 5, no nontrivial edge cut of size at most 3, and no 3-edge-coloring.
- All 27 single-edge deletions of each graph have saved, individually verified nowhere-zero flows over the four-element group. Thus all 54 criticality instances needed here were checked directly.
- Exhaustive perfect-matching enumeration independently confirmed non-3-edge-colorability. The two graphs have respectively 20 and 19 perfect matchings; none has an all-even complementary 2-factor.
- The graphs have respectively 8 and 10 five-cycles, proving nonisomorphism. In the second graph the distinguished attachment vertices are independent and lie in different automorphism orbits: the numbers of five-cycles through their incident edges are respectively {1,1,2} and {0,2,2}.
- A complete path-specific localization and no-folding argument is given in `PATH_PROOF.md`. It supplies the antichain conclusion without requiring an independent reconstruction of the paper's more general tree-localization lemma.

The finite checks cover the two transcribed graphs. They do **not** replay a classification of all graphs on 16 or 18 vertices, test all cycle-continuous functions on arbitrary graphs, verify every theorem in the article, or constitute formal proof-assistant verification. No source-author program was run. The local graph transcriptions and flow witnesses are verification inputs; source documents and dataset contents are not part of the public report.

## Dependency audit

The paper's Lemma 3.1 uses equal-sized cyclically 4-edge-connected critical snarks to force any cycle-continuous map to be induced by an isomorphism. Section 2 of `PATH_PROOF.md` proves that implication directly from cut-cycle orthogonality and criticality. Equal edge counts and the cyclic-connectivity assumption are essential to that argument.

For Lemma 3.2, the paper invokes the absence of triangle-free snarks on 16 vertices to infer criticality of the two Blanuša graphs. That external finite classification was not reproduced. The direct 54 flow certificates independently check the specific criticality facts actually needed. The paper's unproved broader dot-product assertion is explicitly avoided by its construction and is not used in this acceptance.

Lemmas 3.3–3.4 organize maps between trees of snarks; Corollary 3.5 then uses a path with two copies of the first Blanuša graph at its ends and copies of the second graph between them. The short printed argument is expanded here only for these paths. In particular, endpoint colors alone do not prove that the two endpoints have different images. The no-collapse and no-folding argument establishes that fact before deducing equal path lengths.

The general Lemma 3.3 proof is not being certified line by line here. Criticality alone should not be read as saying that every edge-deleted subgraph is flow-colorable; that would be false for a subgraph containing a bridge. The explicit path-specific flow-gluing proof avoids using such an unstated blanket implication. This is a limit on the scope of this audit, not a claim that the published theorem is false.

## Limits of the conclusion

The question is completely answered in the affirmative. No new result is claimed. This acceptance does not resolve Jaeger's Petersen-coloring conjecture, universality of every interval, or the antichain questions restricted to cyclically 4- or 5-edge-connected graphs. The constructed large graphs have nontrivial 3-edge cuts, so the stronger cyclic-connectivity restriction would be a different problem.

The recorded inspections and computations describe this audit only.

## Authorship and review disclosure

This is an AI-assisted explanatory proof and mathematical audit of a published result. It has received no external human review and no formal certification or proof-assistant verification. The word "independent" describes the explanatory derivation and distinct finite-check algorithms; it does not imply external human review.
