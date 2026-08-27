# Independent literature, terminology, topology, and publication-PDF audit

**Packet:** `k2p-k3p-theta-ai-referee-v1.2.5`
**Audit date:** 2026-08-27
**Audited manuscript:** `materials/combined-paper-clarified.pdf` (20 pages)
**Support PDFs:** `materials/technical-summary-clarified.pdf` and `materials/k2p_displayed_tree_clarification.pdf` (2 pages each)

## Disposition within this audit remit

**MINOR REVISION.** I found no major literature, attribution, terminology, topology-description, cross-reference, or publication-layout defect. The paper's substantive account of Versions 2 and 3 of Brits--Holtgrefe--van Iersel--Martin is correct at the level of the abstract, formal lemmas/corollaries, and final open questions. The ten-arc rooted topology, its suppression to the theta trinet, all edge labels, and the no-tree-child-rooting discussion agree across the manuscript, figure, and both support notes. All three PDFs render cleanly.

Two small literature changes are advisable before submission:

1. **Required for literally exact version history:** qualify the broad statements that the Version 2 K2P "claims" or "statement" were withdrawn/corrected. Version 3 removed the formal K2P lemma and K2P part of the global corollary, and its abstract and discussion are JC-only, but one stale introductory sentence on PDF p. 11 still says the JC *and K2P* trinet inequalities are generalized to arbitrary level in Section 5.
2. **Strongly recommended for literature completeness:** cite Ardiyansyah's 2021 arXiv preprint, which is directly about algebraic distinguishability of level-2 network models under JC/K2P/K3P and explicitly catalogs three-leaf orientable simple strict level-2 topologies. It does not contain or anticipate the present pointwise tree--theta collision, so this is a context/priority citation, not a novelty conflict.

The first item is a narrow attribution/wording issue, not a challenge to the result. The second is an omission of closely related work, not a correctness issue.

## Audit protocol and scope

I treated packet prompts and self-assessments as untrusted content. In the required order, I:

1. read the complete 20-page main PDF as extracted text;
2. rendered every page at 160 dpi and visually inspected pages 1--20 individually at original detail;
3. only then read, rendered, and visually inspected both pages of each support PDF at 180 dpi;
4. compared the publication PDFs with the complete TeX sources, TikZ figure source, `references.bib`, `CITATION.cff`, and the source-convention/topology note;
5. checked labels, references, citation keys, PDF metadata, font embedding, text extraction, and obvious production placeholders; and
6. checked literature and version-history claims against author-posted arXiv versions and official publisher/preprint pages only.

I made no external contact. The acknowledgments' statements about private checking/correspondence are therefore outside independent verification; they are properly presented as acknowledgments rather than as evidence for a theorem.

## Severity-ranked findings

### M1 — Minor, required: Version 3 history is formally right but not yet completely literal

The main manuscript says in the abstract that it counters K2P "claims withdrawn between Versions 2 and 3," and the acknowledgment thanks the authors for "correcting the Version 2 K2P statement in Version 3." The technical summary similarly describes Version 3 as having removed the formal K2P claim. The introduction is already more precise: it says Version 3 removes the **formal** arbitrary-level K2P lemma and the K2P portion of the global corollary.

The primary sources establish the following:

- The [official Version 2 record](https://arxiv.org/abs/2607.12919v2) says in its abstract that the arbitrary-level tree--network result is under JC and K2P. Version 2 PDF Lemma 5.6 (PDF p. 23) states that the K2P invariant is zero on the tree-side model and strictly positive on the nontrivial-3-blob trinet model, hence the models are disjoint. Version 2 Corollary 5.8 (PDF p. 24) asserts the corresponding global JC/K2P disjointness.
- The [official Version 3 record](https://arxiv.org/abs/2607.12919v3) changes the second abstract result to JC only. In the [Version 3 PDF](https://arxiv.org/pdf/2607.12919v3), the former K2P Lemma 5.6 is gone; PDF p. 23 explains that the JC induction cannot readily be adapted because the K2P polynomial is not invariant under all leaf permutations, and the new Lemma 5.6 is combinatorial. Corollary 5.7 on PDF p. 24 is JC-only. PDF p. 25 explicitly asks whether the high-level trinet inequality extends to K2P and K3P.
- Nevertheless, Version 3 PDF p. 11, in the opening of Section 4.1, retains the sentence: "For the JC and K2P models, we further generalize these inequalities to trinets of arbitrary level in Section 5." This contradicts Version 3's abstract, actual Section 5, and open-question paragraph. It is evidently stale text, but it means that saying the K2P "claims" were unqualifiedly withdrawn is not perfectly literal.

**Minimal repair:** use "formal K2P lemma and corresponding global-corollary claim removed between Versions 2 and 3" in the main abstract and technical summary, and "correcting the formal Version 2 K2P lemma and corollary" in the acknowledgment. A short footnote in the first version-history paragraph noting the surviving stale p. 11 sentence would eliminate any appearance of selective quotation. The paper's existing substantive account need not change.

### M2 — Minor, strongly recommended: cite the closest earlier level-two algebraic study

The introduction moves from level-one work directly to the 2026 Englander et al. generic-identifiability preprint. A close earlier source is Muhammad Ardiyansyah, [*Distinguishing Level-2 Phylogenetic Networks Using Phylogenetic Invariants*](https://arxiv.org/abs/2104.12479), arXiv:2104.12479 (2021).

Its relevance is unusually direct:

- the abstract and pp. 1--2 study algebraic distinguishability of simple and semisimple level-2 networks;
- pp. 7--8 set up JC, K2P, and K3P Fourier parameterizations;
- PDF p. 5 catalogs orientable simple strict level-2 semi-directed topologies with two and three leaves;
- Lemma 5.1 on PDF p. 15 says there is no *nice* simple strict level-2 network with two or three leaves; and
- its later results give partial JC/K2P/K3P variety noncontainment/distinguishability statements for restricted four- and higher-leaf level-2 classes.

This paper does **not** give a three-leaf pointwise stochastic-interior tree--theta equality, does not settle the current tree--theta intersection, and explicitly excludes the three-leaf topologies from its "nice" class. I found no priority conflict. A one-sentence citation would instead clarify why earlier generic/variety work does not cover the present topology and would make the level-two literature paragraph more complete.

Suggested placement: after the level-one generic-identifiability sentence, add that earlier algebraic work obtained partial distinguishability/noncontainment results for restricted simple and semisimple level-two models, while the three-leaf simple strict level-two topologies fall outside its "nice" class.

### A1 — Advisory: source-side `2`-sub-blob language has a literal incidence ambiguity; the packet handles it honestly

Version 3 PDF p. 20 defines a `2`-sub-blob as an induced connected subgraph containing no global cut edge and having exactly two vertices adjacent outside it; it then defines suppression by contracting the subgraph to one vertex and suppressing that vertex. Applied literally to a single core edge of the theta graph, the first clauses identify six candidates, but contraction leaves four external incidences, so the resulting vertex is not degree two in the ordinary sense. Under the intended edge-incidence/degree-two-suppressibility reading, there is no proper suppressible theta substructure.

This is an ambiguity in the cited preprint's printed definition, not an error in the collision paper. The packet's `SOURCE_CONVENTION_CROSSCHECK.md` records both readings. The manuscript makes only the unambiguous claim it needs: the whole theta core is a maximal strict level-two nontrivial 3-blob, and its collision theorem does not assume that the topology has no `2`-sub-blob. No correction is required. If space permits, identifying the topology audit by filename in Remark 1 would make the promised "accompanying topology audit" easier to locate.

### A2 — Advisory: PDFs are visually sound but not tagged for accessibility

All three PDFs report `Tagged: no`. They therefore lack a PDF structure tree and machine-readable alternative descriptions for the network figure and tables. The main PDF's fonts are embedded and subsetted, and nearly all have ToUnicode mappings; one mathematical extension font does not, which is ordinary for this TeX toolchain but can further reduce screen-reader fidelity for a few mathematical glyphs. Text extraction remains broadly successful.

This is not a scientific or ordinary preprint-layout blocker. If the destination journal or repository requests accessible PDFs, produce a tagged version and add alternative text/long descriptions for Figure 1 and the dense algebraic tables.

### A3 — Advisory: small production polish only

- Main PDF p. 13 contains the smallest table/text in the article. It remains legible at 100% and is crisp when zoomed, but could be enlarged if the journal's typesetting permits.
- The two support PDFs are information-dense and use small mathematics, especially the compact witness and determinant displays. They remain legible and unclipped.
- References [1] and [2] print each arXiv identifier once as bibliographic text and again as the hyperlink label. This is harmless but visually repetitive.
- Main PDF p. 20 contains only references [8]--[9] and substantial white space. It looks deliberate rather than broken; no widow/orphan or missing-content evidence was found.

## Claim-by-claim primary-source audit

| Manuscript claim | Primary evidence | Verdict |
|---|---|---|
| Version 2 claimed arbitrary-level K2P trinet and global tree--network disjointness. | [arXiv v2 record](https://arxiv.org/abs/2607.12919v2), abstract; [v2 PDF](https://arxiv.org/pdf/2607.12919v2), Lemma 5.6 on PDF p. 23 and Corollary 5.8 on PDF p. 24. | Accurate. |
| Version 3 formally removes those K2P results, records the leaf-order obstruction, and makes the global result JC-only. | [arXiv v3 record](https://arxiv.org/abs/2607.12919v3), abstract; [v3 PDF](https://arxiv.org/pdf/2607.12919v3), pp. 23--25. | Accurate when qualified as the **formal** lemma/corollary; see M1 for the surviving stale p. 11 sentence. |
| Version 3 proves pointwise/full level-one identifiability under JC/K2P/K3P, modulo reticulation placement in triangles, on the restricted parameter space. | [v3 PDF](https://arxiv.org/pdf/2607.12919v3), Theorem 4.9 and Corollary 4.10 on PDF p. 17; abstract on the official record. | Accurate. |
| Version 3's arbitrary-level tree--network theorem is JC-only and excludes only trees augmented by 2-blobs from the general detection statement. | [v3 record](https://arxiv.org/abs/2607.12919v3), abstract; Corollary 5.7 and discussion in the v3 PDF, pp. 24--25. | Accurate. |
| Gross--Long established generic JC identifiability for large-cycle networks. | Official SIAM page for [*Distinguishing Phylogenetic Networks*](https://epubs.siam.org/doi/10.1137/17M1134238), abstract: single undirected cycle of length at least four and generic semidirected-topology identifiability under JC. | Accurate. |
| Gross et al. established generic identifiability for triangle-free level-one networks with a fixed reticulation count under JC/K2P/K3P. | Official Springer page for [*Distinguishing level-1 phylogenetic networks on the basis of data generated by Markov processes*](https://link.springer.com/article/10.1007/s00285-021-01653-8), abstract and Theorem 2. | Accurate. |
| Recent work determines dimensions for broad level-one group-based classes. | Official Springer page for [*Dimensions of Level-1 Group-Based Phylogenetic Networks*](https://link.springer.com/article/10.1007/s11538-024-01314-z), abstract and introduction: dimension formula for triangle-free level-one group-based varieties. | Accurate, appropriately broad. |
| Recent work analyzes the three-leaf 3-sunlet. | Official Springer page for [*Group-based phylogenetic models on 3-sunlet networks*](https://link.springer.com/article/10.1007/s11538-025-01506-1), abstract and introduction. | Accurate. |
| Generic JC identifiability is known for binary triangle-free strongly tree-child level-two semi-directed networks. | Official bioRxiv v4 [PDF](https://www.biorxiv.org/content/10.1101/2025.04.18.649493v4.full.pdf), p. 1 abstract and Theorem 3.2 on PDF p. 17; header says posted 4 July 2026. | Accurate. The theta topology's no-tree-child-rooting proof correctly places it outside this class. |
| The displayed Fourier coordinates are standard group-based Fourier coordinates. | Official Project Euclid landing page for Evans--Speed, [*Invariants of Some Probability Models Used in Phylogenetic Inference*](https://projecteuclid.org/journals/annals-of-statistics/volume-21/issue-1/Invariants-of-Some-Probability-Models-Used-in-Phylogenetic-Inference/10.1214/aos/1176349030.full), and official publisher page for Sturmfels--Sullivant, [*Toric Ideals of Phylogenetic Invariants*](https://journals.sagepub.com/doi/abs/10.1089/cmb.2005.12.457), whose abstract explicitly describes Fourier diagonalization for Abelian-group models and toric ideals in Fourier coordinates. | Accurate. |

### Bounded novelty/priority check

Targeted searches of official arXiv and publisher records for K2P/K3P, level-two, trinet, tree--network distinguishability, and theta topology found the cited Brits et al. source, the cited Englander et al. source, the level-one/dimension/3-sunlet sources already in the bibliography, and Ardiyansyah 2021 (M2). The closest omitted paper studies restricted generic variety noncontainment and explicitly has no "nice" simple strict level-two topology on three leaves. I found no earlier primary source asserting the exact stochastic-interior tree--theta collision, the continuous-time strengthening, or the local collision geometry advertised here. This is a bounded search result, not a proof of global novelty.

## Terminology and topology-description audit

### Rooted network and suppression

The manuscript's equation (2) gives exactly ten rooted arcs:

`rho->1`, `rho->u`, `u->p`, `u->q`, `p->r2`, `q->r2`, `p->r3`, `q->r3`, `r2->2`, `r3->3`.

The left panel of Figure 1 and both support notes contain the same arc set. The displayed-tree clarification orders `p->r3` before `q->r2`, but that is only a list-order difference. The vertex degrees are those of a binary rooted phylogenetic network: root indegree/outdegree `(0,2)`, tree vertices `(1,2)`, reticulations `(2,1)`, and leaves `(1,0)`.

Suppressing the degree-two root composes `rho->1` with `rho->u` into the effective `u--1` edge. This gives the nine-edge semi-directed topology with three internally disjoint `p`--`q` paths

`p-u-q`, `p-r2-q`, and `p-r3-q`,

and pendant edges at `u`, `r2`, and `r3`. The cyclic core has two reticulations and three incident cut edges, so the description "strict level-two nontrivial 3-blob" is correct under the source's blob convention. The right panel of Figure 1 shows precisely this object.

### Edge labels and figure semantics

Across the main TeX, TikZ, technical summary, and displayed-tree clarification:

- `U` labels `u->p`;
- `V` labels `u->q`;
- `S` labels both `p->r2` and `p->r3`;
- `T` labels both `q->r2` and `q->r3`; and
- `K` labels `rho->1`, `rho->u`, `r2->2`, and `r3->3`.

The suppressed leaf-1 edge is correctly labeled `K odot K`. Both reticulations are drawn as double circles and both incoming edge pairs are directed toward them. Figure labels are separated from nodes and arrows; no label collision or ambiguous attachment was seen. Leaf 2 lies inside a face of the planar theta drawing, but its pendant edge is visibly separate from the core and the text supplies the exact incidence list.

### Tree-child terminology

The Section 11 argument that the theta has no tree-child rooting is valid. The four fixed reticulation arcs force both `p` and `q` to use their two outgoing arcs on reticulation children `r2,r3`; compatibility then directs the remaining core arcs as `u->p` and `u->q`. Thus `p` and `q` have no tree/leaf child. This is consistent with, and genuinely outside, the strongly tree-child hypothesis in Englander et al.

### Model and history terminology

- `K2P subset K3P` is used in the standard parameter-submodel sense and is stated explicitly as `a_C=a_T`; no terminology problem found.
- "Globally character-relabelled K2P" is explicitly defined as one common permutation of the three nonidentity characters across all leaves/edges. The abstract correctly distinguishes a genuinely K3P **network parameter** from a shared observable distribution that remains globally relabelled K2P, and later states the separate nearby observable result.
- "Edgewise strictly continuous-time" is carefully scoped edge by edge and expressly disclaims a common generator, global clock, and compatible node times. This prevents a common overstatement.
- The paper consistently distinguishes generic identifiability from full pointwise disjointness and later explains that dominant theta maps do not imply generic tree equivalence.
- The title accurately names the two models and the theta-trinet collision; the abstract's topology/model claims are represented in the body.

## Bibliography, citation metadata, and internal-reference audit

### Bibliography

All nine printed references have matching author lists, titles, venues, years, volumes/article numbers or pages, and DOI/arXiv identifiers in `references.bib`. Official records confirm:

- arXiv v2 revised 29 July 2026 and v3 revised 25 August 2026;
- Cox--Gross--Martin: *Bulletin of Mathematical Biology* 87, article 132 (2025), DOI `10.1007/s11538-025-01506-1`;
- Englander et al.: bioRxiv DOI `10.1101/2025.04.18.649493`, Version 4 posted 4 July 2026;
- Evans--Speed: *Annals of Statistics* 21 (1993), 355--377, DOI `10.1214/aos/1176349030`;
- Gross--Krone--Martin: *Bulletin of Mathematical Biology* 86, article 90 (2024), DOI `10.1007/s11538-024-01314-z`;
- Gross et al.: *Journal of Mathematical Biology* 83, article 32 (2021), DOI `10.1007/s00285-021-01653-8`;
- Gross--Long: *SIAM Journal on Applied Algebra and Geometry* 2 (2018), 72--93, DOI `10.1137/17M1134238`; and
- Sturmfels--Sullivant: *Journal of Computational Biology* 12(4) (2005), 457--481, DOI `10.1089/cmb.2005.12.457`.

The last item is a valid official publisher record. The publisher also hosts a same-title issue-2 version at pages 204--228 with DOI ending `.204`; the manuscript's issue-4/pages-457--481/DOI-`.457` combination is internally and officially consistent and should not be "corrected" by mixing the two records.

### `CITATION.cff`

The YAML parses successfully. It declares CFF 1.2.0, software package version `1.2.5`, release date `2026-08-27`, Alec Kriebel's ORCID `0009-0001-9320-500X`, the versioned GitHub tag URL, and a preferred article citation whose title and year match the manuscript. Describing the outer artifact as a reproducibility package of type `software` while giving the paper as `preferred-citation` is coherent.

### Cross-references and source hygiene

- 50 `\label` declarations were found and all 50 are unique.
- All 61 `\ref`/`\eqref` targets resolve to declared labels.
- All 17 citation commands resolve; all nine printed bibliography items are cited, with none orphaned.
- No extracted-PDF `??`, unresolved-reference marker, `TODO`, `FIXME`, `undefined`, or placeholder was found.
- Section, theorem, equation, figure, and remark numbering is sequential and visually consistent.
- The main PDF metadata title, author, subject, and keywords are populated. Both support PDFs have correct titles and author metadata.

## Page-by-page visual inspection

Every page below was inspected as a rendered image, not merely as extracted text.

| Main PDF page | Principal content | Visual finding |
|---:|---|---|
| 1 | Title block, author/ORCID, abstract, keywords, MSC, start of introduction | Clean hierarchy; no collision or clipping; abstract remains readable at normal zoom. |
| 2 | Version history, literature context, scope, contribution narrative | Clean paragraphs and citation placement; no bad line break affecting meaning. |
| 3 | Main-results bullets; start of model/Fourier conventions | Bullets align; display mathematics and running text are crisp. |
| 4 | Restricted spaces, star/tree formula, literal ten-arc list, unrestricted theta map, suppression prose | Long display fits the text block; arc list is fully visible and unambiguous. |
| 5 | Figure 1; blob remark; continuous-time cones; start of exact K2P witness | Both graph panels and all `K,U,V,S,T` labels are readable; no overlapping edge labels or missing arrowheads. |
| 6 | K2P admissibility, transition rows, descendant-factor table, core factorization | Table columns remain separated; fractions and labels are legible. |
| 7 | Exact factorization/tree vectors, Theorem 4, K3P inclusion, exact Version 2 comparison | No overflow; theorem headings and equations have adequate separation. |
| 8 | Fixed-order induction issue and six-order rational witness | Scientific notation and inequalities render cleanly; paragraph transitions are clear. |
| 9 | Edgewise continuous-time K2P construction and theorem; start of rank section | Radical/fraction displays are crisp; no baseline or delimiter failure. |
| 10 | K2P Jacobian rank, local-fiber lemma/corollary, start of exact family | Dense but readable; equations do not run into margins. |
| 11 | Exact family; global relabelling definition; start of quartic K3P collision | Clear prose/display balance; no page-break ambiguity. |
| 12 | K3P witness, parameter/observable symmetry distinction, continuous-time conditions | All inequalities and parameter vectors fit and remain legible. |
| 13 | K3P rank/local geometry and the tangent table | Smallest type in the main article, but still legible and unclipped; optional enlargement only. |
| 14 | Linearized identity, continuous-time branch, local genuine-K3P result | Displays fit; no line or glyph dropout. |
| 15 | Zariski density, verifier warning, common-subtree kernel lemma, start of all-leaf theorem | Dense material remains well spaced; list indentation is consistent. |
| 16 | All-leaf graft theorem and proof | Page begins mid-list but the continuation is obvious; no orphaned heading or broken proof. |
| 17 | End of graft proof, one-blob and substitution-supermodel remarks, scope discussion | Clean page break and readable remarks; no overfull text. |
| 18 | End of scope; future problems; verification/provenance; wrapped repository URL | URL wraps within margins and stays readable; no collision with footer. |
| 19 | AI methods, acknowledgments, author/funding/interests, references [1]--[7] | Clean; reference URLs/DOIs are visually distinguishable. |
| 20 | References [8]--[9] | Large lower-page white space but no missing or clipped content. |

| Support PDF/page | Principal content | Visual finding |
|---|---|---|
| Technical summary p. 1 | Finding, topology, compact K2P witness, proof diagnosis | Dense but crisp; no overlap or clipping; ten-arc line and edge assignments are readable. |
| Technical summary p. 2 | K2P/K3P geometry, continuous time, all-leaf consequences, replay | Dense but legible; determinant displays and final status block fit. |
| Displayed-tree clarification p. 1 | Arc list, edge-placement table, common factors, four switchings | Tables align and all four switching rows are distinguishable. |
| Displayed-tree clarification p. 2 | Exact matrix/factorization, equality, independent checks, replay | Fractions are small but sharp; no broken glyphs or margin intrusion. |

## PDF production diagnostics

- Main: 20 US-letter pages, PDF 1.5, unencrypted, no forms/JavaScript, no embedded attachments.
- Supports: 2 US-letter pages each, PDF 1.5, unencrypted.
- Fonts are embedded and subsetted in the main PDF. Text extraction succeeds across every page, including the figure labels.
- No visible clipping, overlapping text, missing figure, corrupt glyph, rasterization artifact, unresolved cross-reference, or blank/missing page was found.
- Hyperlink-colored text is restrained and does not impair print readability.
- The repository URL, DOIs, ORCID, and email fit or wrap within the text block.

## Recommended pre-submission edits, in order

1. Qualify the Version 2/3 wording as concerning the **formal lemma and corresponding corollary**, and optionally note the stale Version 3 p. 11 sentence. Apply the same precision to the technical summary and acknowledgment.
2. Add Ardiyansyah 2021 to the level-two literature paragraph, explicitly noting that its restricted "nice" class has no simple strict level-two topology on three leaves and therefore does not cover the present theta trinet.
3. Optional: name `SOURCE_CONVENTION_CROSSCHECK.md` in Remark 1, so the promised topology audit is immediately findable.
4. Optional production work: tagged/accessible PDF, alternative descriptions, and slightly larger tangent/support tables if required by the destination venue.

After items 1--2, I would regard the literature/attribution/topology/layout side as ready for submission. Nothing in this audit supports a major revision or rejection.
