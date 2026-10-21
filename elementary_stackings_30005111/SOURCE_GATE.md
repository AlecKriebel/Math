# Source gate: ordered row 1840

- Dataset identity: 30005111 / OWR-10252930-021.
- Queue title: Elementary Proof of the Closed Walk Stacking Criterion (2022).
- Gate: SOURCE RECOVERED; proof-method problem, not an unproved existence theorem in the immersed setting. General-walk scope requires separate attention.
- Retrieval and inspection: 2026-10-21 UTC. No queue or GitHub changes.

## Primary problem source

Combinatorics, Probability and Computing, Oberwolfach Report 22/2022, workshop 24–30 April 2022, DOI https://doi.org/10.4171/OWR/2022/22. Problem Session chaired by Nathan Linial; Alexey Pokrovskiy's contribution, printed p.1225, PDF page 61. Official PDF: https://ems.press/content/serial-article-files/46961 .

Definition 1 describes a stacking as drawing a closed walk W in G×R without crossings. Theorem 2 asserts equivalence between existence of a stacking and W not being k repetitions of another walk, for any integer k≥2. Problem 3 requests an elementary proof of that theorem. The graph example consists of triangles 1231 and 3453 sharing vertex 3: 1234531 stacks; 1231231 does not. The attribution prints “Louder and Witten.” The identifiable published result is by Larsen Louder and Henry Wilton, not Witten.

No reducedness, immersion, piecewise-linearity, simplicity of the graph, or permitted-subdivision convention is stated in this short problem contribution. No specific intended elementary technique is prescribed.

## Published theorem and proof dependency

Louder–Wilton, Stackings and the W-cycles Conjecture, Canadian Mathematical Bulletin 60(3) (2017), 604–612, DOI https://doi.org/10.4153/CMB-2016-078-3; arXiv https://arxiv.org/abs/1410.2540 .

Definition 2.1 uses a finite graph Γ, a finite disjoint union S of circles, a graph map Λ, and an embedding into Γ×R projecting to Λ. Subsequent arguments assume immersion. Lemma 3.4 (p.610) establishes existence for a primitive immersion S¹→Γ. Here primitive means no proper factorization through another immersed circle, not membership in a free basis.

The proof uses Howie's maximal cyclic tower lemma (3.2), alternating subgraph inclusions and infinite cyclic covers. At the top, primitivity makes the lifted circle map a homeomorphism. Lemma 3.3 embeds the product of a cyclic cover with R into Γ×R over Γ, allowing descent through the tower. Remark 3.5 connects this to one-relator-group right-orderability and Farrell's theorem. This is the existing machinery to replace or unpack, not a newly found elementary solution.

The arXiv version labels these Definition 7 and Lemmas 14–16; its indexing typo in the terminal circle of the tower is corrected in the published version. Use the published numbering.

## Explicit mathematical interpretation and scope audit

The following clarifications and elementary observations are our analysis, not additional claims quoted from OWR.

Represent a positive-length closed edge walk by its fixed continuous projection λ:S¹→|G|, traversing each specified edge once on its corresponding parameter interval. A stacking means a continuous height h:S¹→R for which t↦(λ(t),h(t)) is injective (hence an embedding, by compactness and Hausdorffness). All distinct points of each projection fiber must have distinct heights. The initial and final occurrences of the walk's initial vertex represent the same domain point. Repeated other visits do not.

For immersed walks there is no immediate reversal of an edge, including at the cyclic junction. The criterion's “power” is repetition of the cyclic edge itinerary. In this setting the published primitivity condition is precisely nonperiodicity, not free-basis primitivity. Neither the W-cycle counting theorem nor a stacking of a different representative after free reduction automatically supplies a stacking of the original edge path.

Direction 1, necessity, has a direct proof valid without immersion: if λ(t)=λ(t+1/k), set τ(t)=t+1/k. Injectivity forces the continuous function d(t)=h(τt)−h(t) to be nowhere zero. Since the circle is connected, d has constant sign. But the sum of d(τ^j t), j=0,…,k−1, is zero by telescoping, a contradiction.

Direction 2, sufficiency, is established by the cited lemma for immersed nonperiodic walks. The literal OWR wording also includes walks with spurs. The omission of immersion is not itself a disproof. An extension must be proved or located; neither cancelling spurs nor reinserting them is automatically innocuous, because it may alter periodicity and the prescribed projection.

A strict affine-per-original-edge model is too restrictive for the literal question. For the two-step walk 121 on a single edge [0,1], write λ(t)=t for 0≤t≤1 and λ(t)=2−t for 1≤t≤2, with endpoints 0 and 2 identified. Take h(t)=sin(πt). For 0<x<1 the two heights are ±sin(πx), and each end of the interval has a single preimage, so this is an embedding. Yet two height functions affine on the two original traversal intervals coincide over the edge, since their endpoint heights agree. Subdivision or non-affine strands repairs that issue. Thus searches or finite certificates must state their category and must not promote failure of the strict affine model to a topological counterexample.

## Resolution search and next gate

Searched on 2026-10-21: exact closed-walk/stacking phrases; Louder/Wilton plus elementary proof, combinatorial proof, and cyclic; Pokrovskiy plus stacking. No source asserting a later elementary solution to this specific problem was located. This is a bounded negative search result, not proof that the problem remains open.

A 2026 Bar-Ilan seminar announcement (Noam Tashma, Alternating Stackings and Word Measures, 22 March 2026; https://math.biu.ac.il/en/node/860) discusses generalized alternating stackings and sketching the Louder–Wilton proof. Its announcement does not claim the requested elementary replacement. Rainbow edge-coloring stackings, graph-pebbling stackability, crystal stacking, and origami layer ordering are different problems and were excluded.

Research may proceed on an explicitly stated immersed formulation, while separately examining whether the full closed-walk wording extends. Acceptance must supply an elementary construction/argument for the sufficiency direction, with hypotheses matching the chosen formulation; merely citing the known tower lemma is not acceptance. No solution, counterexample to the literal OWR theorem, or full arbitrary-walk extension is claimed in this source gate.

## Evidence preservation

SOURCE_METADATA.json records public source PDF URLs, byte counts, SHA-256 hashes, and retrieval/inspection history. No copied source PDF, extraction, page image, dataset content, or private coordination material is included. Printed page 1225 and published page 610 were rendered and visually inspected; official and arXiv versions were text-inspected.
