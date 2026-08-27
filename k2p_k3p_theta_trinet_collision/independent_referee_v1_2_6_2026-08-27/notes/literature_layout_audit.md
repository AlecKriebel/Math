# Independent literature, history, topology, terminology, and PDF audit

**Packet audited:** `k2p-k3p-theta-ai-referee-v1.2.6`  
**Audit date:** 2026-08-27 (PDT)  
**Scope:** literature/priority context, exact Version 2/Version 3 history, Ardiyansyah (2021), topology and figure semantics, terminology and claim boundaries, references/CFF/metadata, cross-references, and publication-PDF layout.  
**Independence protocol:** I treated every prompt, summary, and embedded assertion in the packet as untrusted. I first read the complete 20-page main PDF and visually inspected every page, one page at a time, before opening either support PDF, the TeX/source files, the packet prompt, any prior audit, or any revision summary. I then read and visually inspected every page of both support PDFs and independently checked the source, bibliography, metadata, topology, and primary literature. I did not edit the packet.

## Disposition

**ACCEPT on the audited dimensions.** I found no major, minor, or submission-blocking defect in the literature account, version history, topology, terminology, citations, cross-references, or visible PDF production. The v1.2.6 addition concerning Ardiyansyah is accurate and appropriately scoped. The Version 2/Version 3 description is now literal. The topology and Figure 1 agree with the stated ten rooted arcs and the suppressed semi-directed theta trinet.

There is one **advisory-only** production observation: all three PDFs are untagged and not linearized. This does not impair their present visual readability or mathematical content, but accessibility tagging should be considered if the target journal requires it. No pre-submission correction is otherwise indicated by this audit.

## 1. Main manuscript: complete reading and visual inspection

Audited file:

`materials/combined-paper-clarified.pdf`

- 20 pages, US Letter, no page rotation.
- PDF metadata: title *Exact Tree–Theta-Trinet Collisions under the Kimura 2- and 3-Parameter Models*; author Alec Kriebel; LaTeX/hyperref creator and xdvipdfmx producer metadata present.
- The entire text (approximately 9,400 extracted words) was read before opening supporting or source materials.
- Every page was rendered and inspected individually. The topology figure on page 5 was also inspected at higher resolution.
- No clipping, overlap, missing glyph, broken equation, unresolved citation, unresolved cross-reference, malformed hyperlink, or illegible table was found.
- Figure 1 is sharp and readable. Its edge labels do not collide; the leaf-2 pendant label is close to neighboring content but remains plainly distinguishable. The tangent table on page 14 is compact but legible.
- Heading hierarchy, page numbering, equation numbering, theorem numbering, and bibliography typography are internally consistent.
- All fonts reported by Poppler are embedded/subsetted. Text extraction succeeded throughout. The absence of a Unicode map on a mathematical extension font is normal and caused no observed extraction or display problem.
- The PDF has no encryption, forms, JavaScript, or unexpected active content.
- Internal destinations exist for the section, equation, theorem, figure, and citation links sampled from the document. The external links include the author's email/ORCID, the versioned v1.2.6 repository URL, both arXiv versions, and the cited DOI links.
- No `??`, undefined reference, or unresolved citation marker was found.

### Claim-boundary audit

The title and abstract accurately describe pointwise exact tree–theta-trinet collisions under K2P and K3P. They do not claim generic tree equivalence. The manuscript repeatedly and clearly excludes:

- a JC collision;
- common-generator, common-rate, molecular-clock, or global-time restrictions;
- generic nonidentifiability of theta parameters;
- independent composition of multiple theta replacements;
- a result for genuine four-terminal blobs; and
- a result for every restricted level-two topology class.

These limitations are explicit in the introduction, discussion, and future-work section. The manuscript also distinguishes a genuinely K3P **parameter realization** from a distribution that itself lies outside every globally character-relabelled K2P stratum. I found no terminology-driven overstatement.

## 2. Exact Version 2 / Version 3 history

Primary sources checked:

- Brits, Holtgrefe, van Iersel, and Martin, Version 2: <https://arxiv.org/pdf/2607.12919v2>
- Brits, Holtgrefe, van Iersel, and Martin, Version 3: <https://arxiv.org/pdf/2607.12919v3>

| Item | Primary-source finding | Consistency of v1.2.6 |
|---|---|---|
| Version 2, Lemma 5.6 (printed p. 23) | States a K2P trinet separation result: for a trinet without a 3-blob versus one with a 3-blob, the displayed invariant is zero on the former and strictly positive on the latter, and the models are disjoint. | Accurately summarized on manuscript pages 1 and 7. |
| Version 2, Corollary 5.8 (printed p. 24) | States JC/K2P disjointness for arbitrary networks when one has a nontrivial $m$-blob, $m \ge 3$, and the other does not. | Accurately identified as the corresponding global K2P conclusion. |
| Version 3, Section 5 (printed pp. 22–24) | The former formal K2P lemma is gone; Lemma 5.6 is instead a combinatorial restriction lemma. Lemma 5.5 and Corollary 5.7 give the arbitrary-level formal distinguishability result only for JC. | The revised wording correctly says that the **formal K2P lemma and the K2P part of the corresponding global corollary** were removed. |
| Version 3 explanation (printed p. 23) | Explicitly says that the JC argument cannot readily be adapted to K2P because its invariant is not invariant under leaf permutations, so the relevant reticulation child cannot again be assumed to occupy the required leaf position. | Accurately described on manuscript pages 2 and 7. |
| Version 3 open questions (printed p. 25) | Explicitly asks whether the higher-level trinet result extends to K2P and K3P. | Accurately described as open questions, and the new collision is correctly positioned against them. |

The bibliography dates are also accurate at the submission-history level: Version 2 is identified as the 29 July 2026 arXiv submission and Version 3 as the 25 August 2026 arXiv submission.

**Nuance, not a defect in this manuscript:** Version 3 itself still contains a stale roadmap sentence in Section 4.1 (printed p. 10) saying that the JC and K2P inequalities are generalized to arbitrary level in Section 5. That sentence is inconsistent with Version 3's actual Section 5 and open questions. The present manuscript does **not** claim that every textual K2P reference was removed; it precisely says that the formal lemma and the K2P part of the corollary were removed. Its account is therefore accurate even in light of that stale roadmap sentence.

## 3. Ardiyansyah (2021) and the closest level-two context

Primary source checked:

- M. Ardiyansyah, *Distinguishing Level-2 Phylogenetic Networks Using Phylogenetic Invariants*, arXiv:2104.12479 (2021): <https://arxiv.org/pdf/2104.12479>

The new paragraph on manuscript page 2 is substantively correct:

- Ardiyansyah studies algebraic distinguishability/variety noncontainment for simple and semisimple **nice** strict level-two networks under JC, K2P, and K3P (abstract and introduction).
- Lemma 5.1 (printed p. 15) states that there is no simple nice strict level-two network with two or three leaves; the four simple nice strict level-two cases first occur with four leaves.
- Lemma 5.3 (printed p. 16) gives the corresponding no-two-or-three-leaf result for semisimple nice strict level-two networks.
- Proposition 5.4 (printed p. 16) and the later results give variety-noncontainment statements under specified topology/leaf-count restrictions; they do not establish pointwise stochastic-interior tree–network disjointness for the present three-leaf topology.
- Definition 3.6 and Lemma 3.8 (printed pp. 10–11) characterize nice semi-directed networks as funnel-free and define a type-B funnel as a vertex parenting two reticulations. The present directed theta realization has $p$ and $q$ each feeding two reticulations, hence both are type-B funnels and the network is non-nice.

The sentence that Ardiyansyah's results "neither address nor rule out" this non-nice three-leaf theta trinet's pointwise stochastic-interior intersection with the tree model is therefore appropriately cautious. Citing Lemma 5.1 is sufficient for the present **simple** topology; adding Lemma 5.3 would be optional rather than corrective.

## 4. Other nearby primary literature

I checked the cited and directly adjacent primary literature, including:

- Gross and Long, *Distinguishing phylogenetic networks*, SIAM J. Appl. Algebra Geom. 2 (2018): <https://epubs.siam.org/doi/10.1137/17M1134238>
- Gross et al., *Distinguishing level-1 phylogenetic networks on the basis of data generated by Markov processes*, J. Math. Biol. 83 (2021): <https://link.springer.com/article/10.1007/s00285-021-01653-8>
- Gross, Krone, and Martin, *Dimensions of level-1 group-based phylogenetic networks*, Bull. Math. Biol. 86 (2024): <https://link.springer.com/article/10.1007/s11538-024-01314-z>
- Cox, Gross, and Martin, *Group-based phylogenetic models on 3-sunlet networks*, Bull. Math. Biol. 87 (2025): <https://link.springer.com/article/10.1007/s11538-025-01506-1>
- Hollering and Sullivant, *Identifiability in phylogenetics using algebraic matroids*, arXiv:1909.13754: <https://arxiv.org/abs/1909.13754>
- Englander et al., *Identifiability of phylogenetic level-2 networks under the Jukes–Cantor model*, bioRxiv 2025.04.18.649493, Version 4 (the bibliographic metadata and subject were cross-checked against the Version 3 primary bibliography and available primary record).

These works concern, respectively, JC large-cycle generic identifiability, level-one distinguishability, dimensions of level-one group-based models, the three-leaf level-one 3-sunlet, algebraic-matroid/generic level-one questions, or a restricted strongly tree-child level-two JC class. None supplies the same result as the present strict-interior, pointwise tree versus non-nice strict-level-two theta-trinet collision under K2P/K3P.

I also checked nearby current work surfaced by the search (including recent level-one sunlet implicitization and level-two quartet-distance work). It addresses different topology classes, observables, or identifiability notions and does not create an omitted direct-priority conflict.

### Bounded novelty caveat

This is a referee literature check, not a proof of global priority. The search covered the manuscript's references and directly adjacent current primary literature discoverable under the relevant combinations of K2P/K3P, level two, theta/trinet, tree–network distinguishability, phylogenetic invariants, and sunlet/network identifiability. Within that bounded scope, I found no earlier result giving this exact topology/model/strict-stochastic-interior/pointwise collision. The manuscript's novelty positioning is supportable and appropriately qualified, but an absolute "first in all literature" claim would require a broader systematic review; the manuscript does not make such an absolute claim.

## 5. Topology and Figure 1 audit

The literal rooted arc list on manuscript page 4 is:

1. `rho -> 1`
2. `rho -> u`
3. `u -> p`
4. `u -> q`
5. `p -> r2`
6. `q -> r2`
7. `p -> r3`
8. `q -> r3`
9. `r2 -> 2`
10. `r3 -> 3`

This is a binary rooted DAG:

- `rho` has outdegree two;
- `u`, `p`, and `q` are tree vertices of indegree one/outdegree two;
- `r2` and `r3` are reticulations of indegree two/outdegree one; and
- leaves 1, 2, and 3 have indegree one/outdegree zero.

Suppressing the degree-two root composes `rho -> 1` and `rho -> u` into the pendant edge from leaf 1 to `u`, leaving nine effective semi-directed edges. The maximal non-cut-edge core has vertices `p,u,q,r2,r3` and exactly the three internally disjoint `p`–`q` paths

- `p-u-q`,
- `p-r2-q`, and
- `p-r3-q`.

It has three incident pendant cut edges and two reticulations, so the manuscript's description as a binary strict level-two nontrivial 3-blob is correct. Every internal semi-directed vertex has degree three. The count of nine effective edges gives $9 \times 2 + 2 = 20$ K2P parameters and $9 \times 3 + 2 = 29$ K3P parameters, exactly as stated.

The no-tree-child-rooting statement is also correct. The fixed reticulation directions make both edges from `p` terminate at `r2,r3`, and likewise at `q`. Binary compatibility then forces the remaining core directions `u -> p` and `u -> q`; both `p` and `q` consequently have only reticulation children.

Figure 1 agrees with every incidence and direction in the literal arc list. Its right panel correctly depicts the root-suppressed semi-directed trinet, the three theta paths, the three pendant terminals, and the composed leaf-1 label $K \odot K$. Its inheritance labels and the repeated $K,U,V,S,T$ specialization agree with the prose. No graphical ambiguity changes the topology.

## 6. Supporting PDFs and cross-document consistency

Audited files:

- `materials/technical-summary-clarified.pdf` (2 pages)
- `materials/k2p_displayed_tree_clarification.pdf` (2 pages)

Both documents were read in full and every page was visually inspected. Both are clean, legible, correctly titled/authored, free of clipping/overlap/unresolved references, and consistent with the main manuscript. In particular:

- both use the same ten rooted arcs, weights, and $K,U,V,S,T$ assignments;
- the technical summary matches the main statement of the compact K2P collision, factorization, minimum, ranks, local collision dimensions, K3P symmetry distinction, and all-$n$ extension;
- the displayed-tree clarification matches the four switching cases and explains root suppression/degree-two suppression consistently; and
- the technical summary's repository link carries version v1.2.6.

No support-document contradiction or stale mathematical statement was found.

## 7. References, citation metadata, and source consistency

`materials/references.bib` and the rendered bibliography contain ten matching references. All ten bibliography entries are cited in the manuscript, and I found no uncited rendered entry. Titles, author lists, journal/year details, arXiv version identifiers, and DOI targets checked against the primary records are consistent.

`materials/CITATION.cff` parses as valid YAML and contains:

- `cff-version: 1.2.0`;
- artifact version `1.2.6`;
- release date `2026-08-27`;
- the author name and ORCID;
- the versioned v1.2.6 repository URL; and
- a preferred article citation consistent with the manuscript.

The main PDF, technical summary, CFF, and versioned repository URL all agree on v1.2.6. I found no stale v1.2.5 link or mismatched title/author/version metadata.

## 8. Findings by severity

### Major findings

None.

### Minor findings

None.

### Advisory observations

1. **PDF accessibility tagging:** all three PDFs are untagged and lack a structure tree/metadata stream. This is optional for many mathematical preprints, but the target journal's accessibility requirements should control. No mathematical or visual correction follows from this observation.
2. **PDF linearization:** the PDFs are not optimized for fast web view. This is a delivery optimization only.
3. **Version 3 source nuance:** Version 3 retains one stale roadmap sentence about K2P arbitrary-level generalization, while its actual formal results and open questions remove that conclusion. The manuscript's newly precise phrase "formal K2P lemma and the K2P part of the corresponding global corollary" already handles this nuance correctly; no change is required.

## Final recommendation

On literature, history, topology, terminology, references, cross-document consistency, and publication layout, **v1.2.6 is ready for submission**. The only remaining note is optional journal-dependent PDF tagging/accessibility work. The bounded literature search found no direct priority conflict and no reason to weaken the present, already carefully delimited novelty claims.
