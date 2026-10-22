# Primary-source priority audit: PR582 / problem 30004404

Audit performed 15 October 2026 UTC. Family: Ito–Motegi–Teragaito persistence literature and version history. This is a bounded priority and scope audit, not an additional proof-search turn or a publication authorization. The frozen candidate is identified by original head `e4b27ac757babc1aea75149ea986ed2beea438f9`; the read-file hashes are in `ORIGINAL_READ_RECEIPT.json`.

## Finding

**No explicit earlier negative resolution of the full literal OWR target was found in the primary text actually inspected. Historical priority remains unestablished.** The important unresolved access gap is the full 2024 cyclic-persistence article. Its abstract, references and metadata are public, but its body was not read. Neither negative searches nor the 2026 authors' statement that no hyperbolic positive examples are known closes that gap.

The candidate should continue to be described as a short deduction from established filling topology and elementary group theory. A useful additional attribution is available: **Ito–Motegi–Teragaito's 2023 v1 realization preprint, printed/PDF p.37, already explicitly discusses the figure-eight zero filling as a torus bundle and derives that its commutator subgroup is the torus fiber group.** That is a close antecedent for the ingredient. The inspected passage does not state that a persistent rank-two free subgroup is impossible, and does not answer the OWR question. [Primary v1 PDF](https://arxiv.org/pdf/2303.15738v1)

The present review found no new mathematical issue undermining the target alignment. It does not independently redo the complete figure-eight exceptional-surgery classification. The separate topology and algebra verification belongs to the main audit. This review does not certify novelty, human peer review, formal verification, or priority clearance.

## Independence and evidence boundary

The exact priority-collision criterion was recorded and SHA-256 sealed in `SOURCE_FIRST_CHECKPOINT.md` before reading the original candidate or previous priority verdict. The filesystem timestamp is 2026-10-15T05:30:00.340356+00:00. The manually typed timestamp in that checkpoint was ahead of machine time; `TIMESTAMP_CORRECTION.json` preserves and explains the error without rewriting the independent checkpoint or its seal.

The source-first work read Motegi's entire OWR contribution and the pertinent 2026 definitions and question. The rest of the 18-page 2026 paper was subsequently read, including every reference. Only after the checkpoint were the frozen `PROOF.md`, `SOURCES.md`, `STATEMENT_AND_SCOPE.md`, and prior `AUDIT.md` (including its complete priority section) read. No sibling-reviewer outputs were read. A later parent message supplied a bibliographic correction, which was independently checked against the publisher. All writes are confined to this review directory. No Git index, branch or remote changes, external outreach, or publication actions were performed.

`SOURCE_LEDGER.json` supplies exact requested and resolved URLs, versions, source hashes, extracted-text hashes, and candid per-file read scopes. `TEXT_SCAN_RECEIPT.json` records every match from the whole-text scans; a scan is not represented as a complete reading or proof of absence. Raw PDFs, HTML, extracted texts and renders are in ignored `.cache/`. `SEARCH_QUERY_LEDGER.json` records the queries and outcomes, including unhelpful and inaccessible results.

## Exact question and priority test

Motegi's contribution with Ito and Teragaito occupies printed pp.491–493 of OWR 8/2020, DOI [10.4171/OWR/2020/8](https://doi.org/10.4171/OWR/2020/8). The contribution fixes standard meridian–longitude coordinates and identifies the filling kernel with the slope's normal closure. Its final question has an arbitrary hyperbolic knot without finite surgery and asks for a subgroup isomorphic to the rank-two free group satisfying

\[
H\cap\bigcup_{r\in\mathbb Q}N_r=\{1\},\qquad N_r=\ker(G(K)\longrightarrow\pi_1(K(r))).
\]

The rational indexing includes zero and excludes the meridian infinity. The displayed symbol is a union; the question has no allowance to omit exceptional slopes. These facts were checked in the text and in a render of PDF p.29. [Primary report](https://ems.press/content/serial-article-files/46844)

My priority criterion required an earlier primary source explicitly to resolve this literal universal assertion negatively, identify the eligible figure-eight knot as lacking persistent F2, or explicitly state an appropriate no-free-subgroup filling obstruction and supply an eligible instance. Merely supplying the old topology, or the elementary algebra from which a new reader can deduce the answer, was not counted as an explicit earlier resolution. This criterion was fixed before the old verdict was read.

The elementary comparison used throughout this audit is:

\[
H\cap\bigcup_r N_r=\{1\}
\iff \forall r\;H\cap N_r=\{1\}
\iff \forall r\;(q_r|_H\text{ is injective}).
\]

Consequently one filling with metabelian fundamental group defeats every proposed F2, since a nonabelian free group has a nontrivial second-derived subgroup and a metabelian group does not. This is a deduction, not an attribution to any paper unless that paper actually makes the deduction. It distinguishes the candidate from all results in the comparison below.

## Source lineage and theorem comparisons

### 2026 persistence paper: complete read

The current [arXiv record](https://arxiv.org/abs/2604.01697) lists only v1, submitted 2 April 2026, 18 pages, titled *Dehn filling and the knot group II: Ubiquity of persistent elements*. The primary PDF was read in full, and pp.3,16,17 rendered and inspected.

Definition 1.5, p.3, uses “torsion-free hyperbolic” for knots with no torsion surgeries, equivalently no finite or reducing surgeries. Section 7.1, p.16, defines persistence for every nonidentity subgroup element, gives the cyclic criterion via [18], discusses satellite examples, and describes the absence of known hyperbolic positive examples. Question 7.1, p.17, uses an arbitrary hyperbolic K and does not print the no-finite-surgery qualification. Example 6.2, p.16, concerns an individual persistent figure-eight element and a finite quotient by that element's normal closure. Reference [18], p.18, uses a title variant for the 2024 article. [Primary PDF](https://arxiv.org/pdf/2604.01697v1)

The logical distinctions are decisive:

| Passage | What it can establish | Why it is not the full target |
| --- | --- | --- |
| Theorem 1.6 (minimizer) and Theorem 1.7, pp.3–4,14 | Under their stated knot hypothesis, suitable H contains some persistent h | This is an existential quantifier inside H. Persistence of H is a universal quantifier over H minus the identity. |
| Corollary 1.8, p.4 | H either totally vanishes under a filling or contains a persistent element | H may have both persistent elements and other nonidentity elements killed by zero filling. |
| Corollary 1.12, p.4 | A subgroup contained in the union of kernels is contained in one kernel | The target asks for a subgroup disjoint from that union, except at the identity. These are different conditions. |
| Example 6.2, p.16 | An element may persist without being a pseudo-meridian | The order-336 quotient is by the displayed element, not a specified surgery slope. It is not a finite surgery or a no-F2 claim. |
| Section 7.1 and Q7.1 | The target subgroup definition and the question remain explicit | Repetition of a question is not proof that no negative example is known, especially when the accompanying discussion seeks a positive example. |

The word “torsion-free” does not mean “all fillings contain a nonabelian free subgroup.” Infinite metabelian torus-bundle groups are compatible with torsion-freeness. Adding no reducing surgery therefore does not remove this obstruction. The printed universal question and the contextual search for at least one hyperbolic positive example must remain distinct. A counterexample to the former leaves the latter unresolved.

### The 2024 cyclic-persistence article: metadata verified, body unread

The primary publisher record establishes the exact published title **Dehn filling and the knot group III: cyclic persistent subgroups**, by Tetsuya Ito, Kimihiko Motegi and Masakazu Teragaito, *Boletín de la Sociedad Matemática Mexicana* **30**, article **99** (2024), DOI [10.1007/s40590-024-00674-9](https://doi.org/10.1007/s40590-024-00674-9). Received 27 March 2024; accepted 18 September 2024; published and version of record 9 October 2024. Thus the frozen candidate's title is correct. The “Dehn filling trivialization on a knot group III” wording in 2026 v1 [18] is a reference-title difference, not a correction to impose on the candidate. [Publisher page](https://link.springer.com/article/10.1007/s40590-024-00674-9)

The accessible abstract states an equivalence between absence of finite surgery and infinitely many mutually nonconjugate cyclic subgroups all of whose nonidentity elements persist. This does not establish the rank-two result: an infinite cyclic group may embed in a metabelian group. The abstract makes no explicit rank-two negative claim. The public bibliography cites paper I v3 and paper II in preparation, which helped trace the version lineage.

The page explicitly presents subscription content. This reviewer did not attempt a publisher PDF after that restriction. Ordinary title, DOI, author-site and institutional-repository searches did not locate a legitimate full preprint. Motegi's public list has a journal entry, Ito's commented list has a journal link, and Teragaito's old preprint list is stale. None supplied this article's full text. Search results offering “request full text” were not used to contact anyone. **It remains possible that the body contains a rank-two obstruction or discussion absent from the abstract.** That is the principal live priority gap.

### Realization paper I: four arXiv versions and published metadata

The current [arXiv record](https://arxiv.org/abs/2303.15738) verifies v4, 30 June 2025, *Dehn filling and the knot group I: Realization Property*, 40 pages, final accepted version. The published record is *International Mathematics Research Notices* **2025**(13), article **rnaf203**, published 8 July 2025, DOI [10.1093/imrn/rnaf203](https://doi.org/10.1093/imrn/rnaf203). The accepted preprint's 40-page layout differs from the journal's cited 31-page layout. The publisher metadata was accessible through the web reader; a subsequent ordinary cache fetch returned 403 and was not retried. [Publisher metadata](https://academic.oup.com/imrn/article/2025/13/rnaf203/8191426)

| Version | Title and change evidence | Read scope and priority relevance |
| --- | --- | --- |
| [v1, 28 March 2023](https://arxiv.org/abs/2303.15738v1), 59 pages | *Dehn filling trivialization on a knot group: separation and realization* | Full-text scan and targeted reading. In Claim 6.3's proof, printed p.37 explicitly identifies the figure-eight zero torus bundle and its commutator subgroup with the fiber group. This is the closest inspected antecedent for the ingredient. |
| [v2, 4 July 2023](https://arxiv.org/abs/2303.15738v2), 59 pages | Same title; metadata acknowledges a gap in v1 Claim 6.3 and says Lemma 6.6 repairs it | Full-text scan and relevant passages read, including Lemma 6.6 statement, printed p.40. The gap warning prevents treating the entire old proof as validated. No rank-two persistence obstruction was identified. |
| [v3, 15 March 2024](https://arxiv.org/abs/2303.15738v3), 41 pages | Title becomes *Dehn filling and the knot group I: Realization Property*; scope focused on hyperbolic knots | Full-text scan; Example 5.1 read. Element-wise persistence is explicit, but no all-elements free subgroup is asserted. |
| [v4, 30 June 2025](https://arxiv.org/pdf/2303.15738v4), 40 pages | Final accepted preprint | Main statements, definitions, §5 beginning and references read; whole text scanned. Theorem 1.5 realizes prescribed finite trivializing sets under its hypotheses. Theorem 1.13 yields many individual elements surviving specified classes of fillings. Neither quantifies over every word in a fixed F2. |

In all versions, figure-eight Example 5.1 produces a particular persistent commutator from two meridians. That example is compatible with the candidate: one commutator can survive while suitable commutators of commutators necessarily die in a metabelian filling. V4 Remark 9.5, p.38, supplies noncommuting elements in a constructed family. Even two noncommuting persistent elements, or two that freely generate, do not by themselves show that every nonidentity word in their generators persists.

The p.37 historical passage is **not an exact collision under the source-first criterion**. It does not mention a persistent F2 or a negative answer to the question. It does show that the core ingredient is explicitly present in this authors' research line by 2023. It would be misleading to present the torus-bundle or metabelian observation as a newly discovered topological fact. The v1 passage is recorded for attribution and history; the candidate's independent classical sources remain the appropriate mathematical dependencies.

### January 2026 companion survey and earlier precursors

The complete 22-page [arXiv:2601.03756v1](https://arxiv.org/pdf/2601.03756v1), 7 January 2026, *Group theoretic perspective on Dehn fillings: Property P conjecture and beyond*, was read. This is the direct [17] lead in the April paper. Its §§5–8 concern individual trivializing sets, realization/separation, and examples where those properties fail. Its figure-eight Example 6.7 is a construction preserving individual trivializing sets; §8 obstructions concern finite-family separation and finite surgeries. No explicit negative answer to the present rank-two target was identified. Its reference [23] still described paper II as in preparation. [Metadata](https://arxiv.org/abs/2601.03756)

The earlier Ito–Motegi–Teragaito paper is [arXiv:1705.04470v2](https://arxiv.org/pdf/1705.04470), 23 March 2019, first submitted 12 May 2017. The preprint title uses “which are”; the published title is *Nontrivial Elements in a Knot Group That are Trivialized by Dehn Fillings*, *IMRN* **2021**(11), 8297–8321, DOI [10.1093/imrn/rnz069](https://doi.org/10.1093/imrn/rnz069), online 8 April 2019. Main results concern normal-closure equality, finite generation, and intersections/inclusions. Theorem 1.6 and Corollary 1.8, p.3, are about infinitely many kernels having trivial intersection or an individual element dying only finitely often. They do not imply disjointness from their union. Printed p.6 explicitly recalls that the figure-eight has no nontrivial finite surgery. Only the stated targeted portions and references were read; the whole extracted text was scanned.

Ichihara–Motegi–Teragaito, *Vanishing nontrivial elements in a knot group by Dehn fillings*, *Topology and its Applications* **264** (1 September 2019), 223–232, DOI [10.1016/j.topol.2019.06.023](https://doi.org/10.1016/j.topol.2019.06.023), is a direct OWR reference. Its publisher abstract concerns finite trivialization for an individual nonidentity element and existence of elements surviving all nontrivial fillings. The publisher full text was not accessed; direct open returned 403 and was not retried. Its body remains a lesser priority gap. [Publisher abstract](https://www.sciencedirect.com/science/article/pii/S0166864119301890)

### The residual-perfect paper: a later version was checked

April 2026 [19] cites [arXiv:2504.16345v1](https://arxiv.org/pdf/2504.16345v1). The live record now has [v2, 4 August 2026](https://arxiv.org/abs/2504.16345), 23 pages, an accepted version. Both complete texts were scanned; their introductions were read. V2 Corollaries 1.6 and 1.8 explicitly give injectivity into the product of filling groups and intersection of all slope kernels equal to the identity. These concern

\[
\forall g\ne1\;\exists r\quad q_r(g)\ne1,
\]

while a persistent F2 requires one subgroup with

\[
\exists H\cong F_2\;\forall h\in H\setminus\{1\}\;\forall r\quad q_r(h)\ne1.
\]

There is no implication from the former to the latter. Likewise, the introductory fact that a knot group is not residually free concerns maps from G(K) **to** free groups; it is not an obstruction about maps of its free subgroups into surgery groups. No exact collision was identified in this lead, and the remainder of its proofs was not read in full.

## Adversarial priority checks and remaining gaps

1. **Could the universal assertion silently exclude zero?** No. The primary slope definition and rational index include zero. A modified problem would need an explicit change.
2. **Could “torsion-free hyperbolic” exclude the example?** That convention removes torsion surgeries; it does not remove infinite solvable zero fillings. No such exclusion appears in Definition 1.5.
3. **Could the 2026 repeated question certify the candidate's originality?** No. Its positive-example context and “to the best of our knowledge” status do not certify absence of a negative example, an unpublished observation, or a remark in inaccessible literature.
4. **Could v1 p.37 count as a prior resolution?** It establishes a central ingredient explicitly, but the inspected text makes no no-F2 or negative-target assertion. Calling it an exact earlier resolution would cross the criterion fixed independently at the start.
5. **Could keywords miss a statement?** Yes. Notation, language, indexing and source versions vary. Full reading of the 18-page current paper and 22-page direct survey reduces this risk locally; it does not make scans of longer precursor papers exhaustive.
6. **Could the 2024 article settle priority?** Yes. This is the strongest live gap. A legitimate complete body could contain a no-free-subgroup remark not captured by its abstract or subsequent citations. No negative result is attributed to an unread article.
7. **Could classical derivability make an explicit prior answer unnecessary to priority assessment?** It makes strong novelty claims inappropriate already. It does not allow a reviewer to invent a historical statement or name a first author of the application.

Remaining work for stronger historical clearance is specific: inspect the full 2024 article through an ordinary legitimate copy if one becomes available; inspect the 2019 article's full body; complete readings of longer precursor versions if a remark-level priority claim is contemplated; and trace additional nonindexed talks/notes only if concrete primary leads emerge. None of these limitations is represented as a mathematical counterexample to the candidate. They are reasons for qualified priority language. Outside input could improve historical assessment, but this project prohibits communication with individuals; no outreach was prepared or initiated.

## Publication framing assessment

A carefully attributed short clarification or note is a reasonable form to evaluate. Its value would be to make the one-filling obstruction and the universal-versus-existential distinction explicit and checkable. This review does not establish that a journal will regard it as new or publishable. It should not be promoted as a substantial new surgery theorem, a first solution, or a resolution of whether **some** hyperbolic knot has a persistent F2.

The defensible claim is that the figure-eight knot rules out the literal universal assertion using classical facts. The currently unresolved positive-example problem should be stated immediately beside that claim. Bibliography should use the actual 2024 title and may note the 2023 p.37 antecedent with its version warning. Retain the candid unread-full-text qualification when reporting the bounded priority search.

**Disposition: qualified priority clearance only; no explicit collision found in inspected primary text, no firstness finding, and no automatic acceptance or publication action.** The assigned bounded audit is complete, with its exact gaps recorded.
