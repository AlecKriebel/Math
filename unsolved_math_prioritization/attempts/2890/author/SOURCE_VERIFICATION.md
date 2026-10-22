# Source verification for KP 4.14

Checked 5 October 2026 UTC. This file contains authored bibliographic and inspection notes, not source reproductions. Public fingerprints are recorded separately in SOURCE_METADATA.json.

## Target and duplicate check

- Requested catalogue page: https://www.unsolvedmath.com/problems/2890 . The web reader could not access it, and a direct ordinary retrieval returned HTTP 403. No page contents were inferred from that response.
- The live repository catalogue associates ID 2890 with KP-4.14, rank 693. Its source URL field is empty. Its topic is independently matched to the universal-cork question using the 2026 K3 text.
- Catalogue bytes already available locally were hashed. Their Git blob hash matches the live pinned repository object bd5c23e4e6c7e1901717a7e596477a7f6dc72425 and their byte count is 21,735,099. This verifies the catalogue used without downloading the research corpus.
- Repository main was pinned at 2669042ac964d5710972af552df141f7934588af. QUEUE.md row 693, line 704, was queued 0/5; its file object was 5d33a968894980499cb3fbb6d84fe5cca5a47aa4. The pinned state.json contains no entry for 2890. The attempt directory returned 404. Exact PR searches for 2890, KP-4.14, and “universal cork” across all states returned no matches; a branch search for 2890 returned none. This is an observed duplicate check, not a claim about deleted or inaccessible history.
- The public dataset manifest was read at that pin. Its published hashes and byte counts are recorded as **reported metadata**, not independently recomputed full-corpus hashes. Neither problems.json nor research_results.json was downloaded for this task.

## Primary problem

R. İnanç Baykur, Robion C. Kirby and Daniel Ruberman, editors, K3: A New Problem List in Low-Dimensional Topology, AMS Mathematical Surveys and Monographs 295 (2026).

Public preliminary copy: https://math.berkeley.edu/sites/default/files/surv-295-ruberman-watermarked-author-pdf.pdf

Editor page: https://math.berkeley.edu/node/172

The newly retrieved copy has 436 PDF pages and is byte-identical to the initial local reading copy. Problem 4.14 and its remarks are at printed pages 201–202. Page 201 was rendered and visually inspected; the adjacent stabilization question at printed pages 196–197 and the section introduction at page 191 were inspected in extracted text. The official published volume is described as 430 pages; these are different editions, and page numbers here refer to the preliminary copy. The full book was downloaded for private reading but not read cover to cover, and it must not be republished.

The editor's current page https://sites.google.com/brandeis.edu/ruberman/home was checked for updates. No specific resolution of Problem 4.14 was listed there. The linked AMS product page returned 403. Absence of a displayed update is not proof of global current open status.

## Ladu on nonuniversality

Roberto Ladu, The Akbulut cork is not universal, Selecta Mathematica (N.S.) 31, article 74 (2025), DOI https://doi.org/10.1007/s00029-025-01061-6 .

Inspected full author manuscript: https://arxiv.org/pdf/2311.17028v3 , 18 pages, 8 February 2024. Version history: https://arxiv.org/abs/2311.17028 .

The conventions, difference-element argument, named-family obstruction, complexity definitions, transfer lemma, and boundary-universal argument in Sections 1–4 were inspected in the author manuscript. Page 2 was visually checked for the two orientation classes and quantifiers. The finite proofs in the present packet use the gluing mechanism; Floer foundations and the cited existence/geography theorems remain external inputs.

The publisher page confirms publication on 31 July 2025 and the headline results. Its full PDF was not obtained: the attempted PDF request returned an HTML access page. The publisher preview displays only the opening page. No equality between the complete 2024 author manuscript and the final 2025 article is asserted.

The manuscript explicitly defines corks as oriented involutions. K3 allows arbitrary boundary diffeomorphisms and contains a remark about allowing both orientations that is not reconciled with the stronger-looking manuscript Theorem 1.2 here. The package consequently does not assert a two-orientation classification, an arbitrary-order extension of the manuscript's theorem, or a resolution of the main target.

## Yasui on twists and varying embeddings

Kouichi Yasui, Nonexistence of twists and surgeries generating exotic 4-manifolds, Transactions of the AMS 372 (2019), 5375–5392; DOI https://doi.org/10.1090/tran/7696 .

Author manuscript: https://arxiv.org/pdf/1610.04033v3 , 18 pages, 3 September 2018. Version history: https://arxiv.org/abs/1610.04033 .

Inspected introduction, Theorems 1.3 and 1.11, Definitions 2.2, the b₁(∂W)=0 proof of Proposition 3.2, and Theorem 4.2 with its proof. Page 6 was rendered to verify the signed formula and rational-basis definition. The authored argument uses an extended infimum J to avoid assuming nonnegativity or finiteness for unrestricted smooth manifolds. No global lower bound on 2g(v)−v² is presumed. The varying-embedding hypothesis is inapplicable to a contractible cork. Gauge-theoretic ingredients behind the source's examples have not been independently rederived.

## Newer complexity result

Roberto Ladu, On h-cobordisms of complexity 2, https://arxiv.org/abs/2501.08750 ; inspected https://arxiv.org/pdf/2501.08750v2 , 23 pages, 19 June 2025.

The author's page https://sites.google.com/view/robertoladu/research says it is to appear in Algebraic & Geometric Topology. Inspected the introduction and Section 6, especially Theorems 1.2 and 6.3 and the proof involving the specific isometries R_m. The result is about selected cobordisms, not the minimum over all cobordisms between unmarked endpoints. The difference between excess-intersection complexity and handle-count stabilization complexity is explicit in Section 6.1. The Floer calculations in Sections 3–5 were not independently checked and are not used as a new proof here. Version 2 changes coefficients to F₂ and removes a dependence on an integral-coefficient exact sequence.

## Stabilization updates

Sungkyung Kang, One stabilization is not enough for contractible 4-manifolds: https://arxiv.org/abs/2210.07510 , inspected https://arxiv.org/pdf/2210.07510v3 , 22 pages, 17 September 2024. The introduction, Theorem 1.1, Corollary 1.2 and Questions 1–2 were inspected. The closed-ambient step is explicitly a question there. The full bordered-Floer proof was not independently audited.

Gary Guth and Sungkyung Kang, Invariant splitting principles for the Lipshitz–Ozsváth–Thurston correspondence: https://arxiv.org/abs/2404.06618 , inspected https://arxiv.org/pdf/2404.06618v2 , accepted version, 31 July 2026. The introduction and Theorem 1.8 on page 5 were checked. The publisher confirms publication on 31 August 2026 in Journal of Topology 19, e70097: https://doi.org/10.1112/topo.70097 . Its application remains a family of contractible four-manifolds with boundary surviving one stabilization; it does not supply an unbounded closed-pair distance. The full splitting proof was not independently checked.

## Finite cork constructions and strong corks

Paul Melvin and Hannah Schwartz, Higher order corks, Inventiones Mathematicae 224 (2021), 291–313; DOI https://doi.org/10.1007/s00222-020-01009-x . Inspected final author version https://arxiv.org/pdf/1902.02840v2 , 28 November 2020, and version history https://arxiv.org/abs/1902.02840 . Inspected the introduction, relative involutory theorem discussion/proof, and the finite theorem and proof in Section 3.1. Its cork depends on the finite family and uses powers of a boundary map. The arXiv version notice says infinite-order results were removed because of errors. No removed v1 conclusion is used. The complete consolidation proof and its prior handlebody inputs were not independently reconstructed.

Tateaki Mukohara, Strong corks derived from the Akbulut cork: https://arxiv.org/abs/2601.02230 , inspected https://arxiv.org/pdf/2601.02230v3 , 22 July 2026. The introduction and main statements on pages 1–3 were inspected. Strong nonextendability over fillings is a different assertion from universality across closed ambient pairs. This paper is a current-scope check, not an input to an asserted universal obstruction.

## Verification limits

The negative literature check was targeted, using exact universal-cork, stabilization, and h-cobordism-complexity searches and author/publisher version pages. It is not an exhaustive bibliographic or novelty certification. Older foundational results by Freedman, Wall, Gompf, Morgan–Szabó, Curtis–Freedman–Hsiang–Stong and Matveyev are attributed through the inspected primary papers; their original proofs were not all re-audited. Finite controls test only the authored algebra and quantifier models. The final conclusion is that this investigation does not solve the target, rather than a certified assertion that no one else has solved it.
