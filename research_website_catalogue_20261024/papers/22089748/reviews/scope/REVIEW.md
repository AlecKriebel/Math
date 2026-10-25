# Scope review — Zenodo 22089748

**Disposition: PASS for source acquisition, document coverage and scoped candidate wording only.** This is not an analytic or adversarial mathematical verdict. No scientific certificate program, theorem replay or manuscript rebuild was executed in this scope assignment. No website, spreadsheet, Git, release or outreach action was performed.

The exact object is *Local Complete-Graph Optimality at Fitness Two and Strong-Selection Rigidity under Death–Birth Updating*, Zenodo DOI **10.5281/zenodo.22089748**, version **1.0.0**, publication date **2026-08-25**. The manuscript prints **August 2026**, without a numbered manuscript version. The referee package carries an August 23 format date. These are different metadata fields, not competing publication dates.

## Sources and all reader documents

Fresh public API metadata and all five selected assets were acquired. Each size and MD5 matched both the queued inventory and current record. The published PDF additionally matched the queued SHA-256. Both detached SHA-256 files match their respective archives. Gzip CRC/trailer verification and tar-header checks passed. Extraction rejected traversal, absolute paths, links, special nodes and duplicate names, with bounded member/total sizes; no archive code was executed.

| Selected asset | Bytes | SHA-256 |
|---|---:|---|
| complete_graph_extremality_db.pdf | 235224 | ec8c09fbc4ef5f382272351f69721b6544c69f5d48bee961447e1907de2c0180 |
| complete_graph_extremality_db_source_and_certificates.tar.gz | 394499 | 7220a09d7eb31fdd81c42b35cbeb680f8c1b257df3b3002d37146b00d81e588e |
| complete_graph_extremality_db_source_and_certificates.tar.gz.sha256 | 127 | 94becfbead8da90a7ae211b79122227dccf88ecadd889e23b8742554d803f6c9 |
| paper_i_complete_graph_extremality_referee_package_2026-08-23_r4.tar.gz | 1041551 | d8fc0193da78cd4907ca7a36950111c00c761966538d71a937320b1db23909fb |
| paper_i_complete_graph_extremality_referee_package_2026-08-23_r4.tar.gz.sha256 | 138 | 9c988b9d2604bb8ba98f3343572c5f8a0d1e28c40508a7cca867945e7680880e |

The source archive has 73 regular members, and the referee archive has 84. A fresh independent inventory verifies the source manifest's 72 entries, referee manifest's 83 entries, and copied source manifest's 72 entries, including exact regular-file-set equality. The referee package's nested source archive equals the separately published archive byte for byte; its 73-file extracted source tree also matches completely.

There is **one unique reader PDF, 30 pages**. Its four direct occurrences are the separately published file, the source archive's `output/pdf` copy, the referee package's top-level copy, and that package's extracted-source copy. Every occurrence has the same SHA-256 and 30 pages. The nested identical source archive adds no new reader material. **There is no separate supplement or referee-report PDF.** `reader-documents.json` records every path. No reader PDF was omitted.

The complete manuscript was read through all 12 corresponding TeX files: main/abstract/author summary, all seven numbered sections, Appendices A–C, and references. PDF text was extracted, its 30-page coverage checked, and the first page visually checked. This is not a claim of a page-by-page visual typography audit. Current package navigation, claim-to-code map, version, declarations, environment and provenance notes were also read; the internal replay's call inventory was inspected. Mathematical code validation belongs to the separate mathematical reviews.

Primary manuscript path: `sources/published-source/complete_graph_extremality_db_source_and_certificates/universal_simultaneous_amplification/phase5_exact_threshold/paper_db_extremality/main.tex`. Its component hashes and full-file read scopes are in `source-bindings.json`.

## Exact claim boundaries for the page

The model chooses the dead individual uniformly, then chooses a parent proportionally to fitness times the directed incoming edge weight. There are no self-loops, incoming totals are positive, mutant fitness is constant and resident fitness is one. Initialization is a **uniformly chosen single mutant**. Rows of the normalized kernel are dead targets, columns are parents. Scaling every incoming weight at one target by the same positive factor changes no dynamics.

1. **Theorem 1, pp. 5, 10–12; Appendix A, pp. 18–26:** for each fixed n ≥ 3, the complete normalized kernel is a strict nondegenerate local maximum at r = 2 in the entire loopless row-stochastic kernel space. Column imbalance and nonreversible circulation are included. The neighborhood can depend on n. No global optimality, global concavity, uniform radius or weak-selection theorem follows.
2. **Theorem 2 and Corollary 3, p. 6; proof pp. 12–15:** on complete positive directed support, the leading strong-selection deficit is an incoming-column sum of squares divided by n²(n−2)r, with a fixed-graph O(r⁻²) remainder. Its zero set is the class of raw weights whose normalized kernel equals Jₙ; raw edge weights need not all be globally equal. Equality then means the entire replacement dynamics coincide for every fitness. Combined with the prior noncomplete-support theorem and the paper's source-component bound, every fixed P ≠ Jₙ is strictly suppressing beyond a threshold depending on P. At n = 2 the normalized kernel is necessarily J₂.
3. **Theorem 5, p. 6 and pp. 15–16; Theorem 16, Appendix B pp. 27–28:** every positive undirected weighted triangle is dominated by the complete graph for every r > 1, strictly away from equal weights. The two K₄ families have S₁ × S₃ or S₂ × S₂ symmetry: a three-satellite family with parameter x, and two pairs with internal weights x,y and equal cross weights. Equality is x = 1 or x = y = 1 respectively. This is not an unrestricted weighted-K₄ classification.
4. **Proposition 4, p. 6 and pp. 14–15; Proposition 13, p. 16:** the connected-undirected support limit gives a necessary support-degree-divergence condition for an asymptotically universally amplifying sequence. It is not sufficient and cannot exclude completed supports with arbitrarily weak edges.
5. **Appendix C, pp. 28–29:** fixing P and then taking r large is different from choosing a growing sequence and then requiring amplification eventually in n for each fixed r. The page preserves this order and does not infer the open global fitness-two or all-r growing-family statement.

The proof's local axis uses the fair-geometric union dual, coverage committor, phase-sensitive marked/active collision identity, rank projection and a multiplicity-free three-sector decomposition. The finite computational portions are explicit: with N = n−1, the standard sector uses exact N = 2,…,9 and an analytic tail from 10; the symmetric sector uses exact solves at 3,…,39, exact phase margins at 40,…,287, and an analytic tail from 288. The antisymmetric all-order proof is analytic. These are manuscript scope statements, not fresh replay results. The public candidate gives a short explanation instead of replaying the full checklist.

## External interfaces and attribution

The critical external interface is Tkadlec–Pavlogiannis–Chatterjee–Nowak (2020). The original publisher model, Theorem 1 and supplementary proof on pp. 5–7 were inspected. They use the same uniformly initialized loopless dB process, assume strong connectivity, allow directed/weighted edges and require noncomplete support; the threshold can be 2N². The proof uses an average-support-degree bound. It leaves complete support outside that theorem. No mismatch was found in the manuscript's use of this result. Original publisher PDF, supplement and HTML are saved with SHA receipts in this scope folder. The supplement's early overview numbers the two theorems differently, but the operative proof section and main article identify transience as Theorem 1.

Svoboda–Joshi–Tkadlec–Chatterjee (2024), Theorem 3 and the original publisher discussion, provide bounded-interval growing-family context. They do not prove a theorem about a single fixed graph at all fitnesses, and are not imported to prove the present local or strong-selection results. The source's weaker pointwise-in-fitness paraphrase does not overstate that contextual result.

The manuscript credits Harris's graphical construction, ancestral-selection work of Krone–Neuhauser, Etheridge–Griffiths and Mano, and the spatial dB dual of Foo–Gunnarsson–Leder–Sivakoff. These are methodological precedents; the current finite union-dual and collision identities are derived in Section 3 rather than taken as unnamed external theorems. Primary abstract access confirms the ancestral-selection and lattice-dual context, but their full proofs were not audited here. Direct DOI access for Harris and some publisher pages was unavailable; no substitute secondary summary is treated as theorem validation. Candidate attribution remains explicit and modest. This bounded check makes **no exhaustive novelty or firstness certification**.

## Provenance and incidental assertions

Fresh metadata for DOI 10.5281/zenodo.21753405 identifies the August 2, 2026 software release `universal-db-obstruction-v1.0.0`. It is in a different Zenodo concept record from the selected preprint. The paper says it incorporates and revises the earlier strong-selection and low-order results while adding fitness-two theory. That is preserved as author-declared provenance. The predecessor's 455 MB repository archive was not downloaded, so this review does not independently certify what was absent from every historical artifact.

The selected metadata also has an `isDerivedFrom` software relation to 10.5281/zenodo.21852072. The source describes this as the separate simultaneous-amplification companion. Preserve the original metadata relation; do not convert it into a load-bearing mathematical dependency or use that DOI to cite this paper.

Incidental exposure: the current introduction claims “to our knowledge” local-theorem originality and lists which components were first included here; package notes describe previous hardening and intended certified replay; the provenance note still says the consolidated paper had no new DOI at its writing date. These are author statements, not independent evidence. The fresh August 25 record supersedes that old status for candidate wording. No dedicated historical verdict, research diary, actual referee opinion or sibling review was consulted. Package prompt/template files were inventoried but not read as instructions or evidence.

## Candidate content and remaining gate

`content.json` contains the **full 233-word source abstract**, with only normalized math/dash typography and one paragraph break before “Second”. It includes plain-language and exact statements, scope boundaries, primary credit, truthful AI/unrefereed status, a professional invitation for substantive collaboration, all five published assets and `follow_up: null`. The explicit open questions are worth preserving as limitations, but no new conjecture or concrete follow-up mechanism was established here.

The source archive uses a TAR.GZ label. The referee archive uses `kind: "tar.gz"`; the current renderer accepts only pdf/zip/text for additional assets, so a later authorized editor must add archive-kind support rather than label this file ZIP. No renderer change was made here.

All candidate wording remains conditional on the root's separate mathematical gate. This scope review neither repairs the manuscript nor authorizes publication. The source receipt, complete manuscript-source hashes, asset map, primary receipts and authored checks permit a later editor to bind the approved page to exactly this edition.
