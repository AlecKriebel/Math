# Acquisition and scope — Zenodo 23444839

**Scope complete; no mathematical verdict issued.** This report authenticates the exact published edition, maps its statements and primary-source interfaces, and prepares conditional explanatory content. Independent analytic and adversarial reviewers retain responsibility for mathematical approval.

## Published identity and complete reader coverage

*A negative answer to Nevo's homology-sphere decomposition question*, Alec Kriebel, version 1.0.0, 17 October 2026. Version-specific DOI: [10.5281/zenodo.23444839](https://doi.org/10.5281/zenodo.23444839). Inventory row 60, work `Z-23444838`. Zenodo classifies it as a preprint. It has an explicitly published standalone manuscript and is eligible as a paper record.

| Public asset | Bytes | MD5 | SHA256 |
| --- | ---: | --- | --- |
| spherefree-doubly-cm.pdf | 83,093 | 9a53980cbbfef3ce7a69a16dd33ea3eb | 0f3bd7b0b576188794376e5a6428f7049bd19a1e778b68ad5c63b696a73c3a01 |
| spherefree-doubly-cm-source-and-verification.zip | 392,255 | 8de2a0c44ddb66e859eec9f4c70cd861 | 7919adebe0119f34df35e905ebe3665b1d66e79477fa36a06c30801bbe736a5b |

Both public files were freshly fetched and matched API sizes/MD5 and the frozen inventory. The five-page PDF also matches the inventory SHA256. The ZIP has 120 regular files; extraction checked paths, types and member CRCs and rejected unsafe members. The sole embedded PDF, `output/pdf/spherefree-doubly-cm.pdf`, is byte-identical to the standalone main manuscript. A scan for PDF and ZIP magic and archive suffixes found no second reader or nested archive. Thus reader coverage is **one distinct five-page document, two identical PDF occurrences**. All five pages were read by extraction and TeX, and every rendered page was visually inspected.

`sources/receipt.json` binds all public bytes and all extracted members. `reader_document_map.json` records reader identity. `final_integrity_check.json` rechecks all 120 extracted members and both assets, unchanged. `scope.json` binds the TeX, metadata, receipt, and every read mathematical support file. The complete 116-word abstract is retained in `abstract_original.txt`, together with its unabridged TeX environment and a hash/normalization receipt.

## Exact statement and boundaries

Theorem 1 on page 1 asserts existence of **one finite pure two-dimensional abstract simplicial complex K** that is doubly Cohen–Macaulay over every characteristic-zero coefficient field and has **no two-dimensional homology-sphere subcomplex over any field**. Doubly Cohen–Macaulay means Cohen–Macaulay both before and after each single vertex deletion, with the same dimension. Here Cohen–Macaulay is stated by the below-top reduced-homology vanishing condition at every face, including the empty face.

A homology sphere is defined using sphere homology for **every face link**, including the empty-face link, with `{∅}` the dimension −1 sphere. A complex having sphere homology only globally is not the target class. The excluded subcomplex need not be induced. The statement does not assert that arbitrary topologically embedded spheres, immersed spheres, or sphere subcomplexes appearing after subdivisions are absent. It makes no enlargement or subdivision of the ambient complex. Triangulated PL/topological two-spheres that are subcomplexes are among the excluded local-link homology spheres, but no classification of all embedded topological subsets is claimed.

The number 11 is the order of the geometric finite field. It is **not** the characteristic of a universally quantified homology field. The 2-CM assertion is limited to characteristic zero; no assertion of 2-CM over every positive characteristic is made. The example is not a surface: the manuscript gives twelve incident triangles at each edge. It is not a theorem for all dimensions or all building quotients.

The original question asks for a union of suitable sphere subcomplexes subject to overlap/reordering conditions. Because the claimed K contains no permitted piece at all, even an unordered cover would fail. This does not dispute the earlier decomposition into minimal cycle complexes.

## Manuscript mechanism and proof obligations

| Pages | Component | Exact interface that a mathematical review must validate |
| --- | --- | --- |
| 2 | Finite quotient | Start with the affine building of PGL₃(F₁₁((y))). Use the faithful 9×9 conjugation representation of the vertex-regular lattice Γ over F₁₁[t], t=1/y. Reduce matrices modulo t⁹. A path of at most four undirected edges yields polynomial degree at most eight; congruence to I modulo t⁹ then forces identity. Normality transports displacement to all vertices. |
| 2 | Quotient links | Faces are precisely images of building faces, not newly completed cliques. Displacement prevents identification in a closed star; incident quotient edges/triangles lift uniquely there. Every vertex link is the incidence graph G of PG(2,11). |
| 3 | Link estimates | G has 133 points and 133 lines, degree 12, Gram matrix 11I+J and no cycle shorter than six. After deleting any one link vertex, degrees are 11 or 12. The estimate uses unweighted mean-zero extension for the ordinary energy and actual degree-weighted variance for normalization. The stated lower bound is (11−√11)/12 > 7/12 > 1/2. |
| 3 | Lemma 2 | Finite pure dimension two, connected links, strict normalized gap >1/2. Triangle multiplicities weight an energy-minimizing cocycle; local Poincaré inequalities sum to E≥2λE. This is a finite linear-algebra proof, not an appeal to contractibility or Property (T). |
| 3–4 | Every deletion | A surviving edge retains at least eleven triangles; vertices retain at least 265 neighbors. Paths bypass the deleted vertex through its connected link. Surviving links are G or G−w. Real first-cohomology vanishing transfers through finite-dimensional duality and integer matrix ranks to every characteristic-zero field; empty, vertex, edge and facet faces are addressed separately. |
| 4 | Sphere exclusion | Edge links force exactly two triangles per edge; connected vertex links become simple cycles of length at least six. The incidence equations give Euler characteristic ≤0, incompatible with sphere homology's Euler characteristic 2 over any field. The proof does not assume orientability or invoke surface classification. |

This map records the submitted mechanism rather than substituting a generic building theorem or a different counterexample. No repair or alternative construction was attempted.

## Primary sources inspected

Fresh raw PDFs, text and URL/byte/SHA receipts are in `cache/primary-sources` and `primary-source-receipts.json`. `primary_interfaces.json` gives selective reading scopes and exact byte identities. The external bodies are retained in ignored review cache rather than added to the submitted source archive.

- **Original question.** Nevo's [OWR report](https://ems.press/content/serial-article-files/45990), printed 959–962, was read in its entirety; Definition 1, Theorem 7 and Problem 8 occur on 960–961. The [published 2008 article](https://link.springer.com/content/pdf/10.1007/s00454-007-9017-y.pdf), printed 414–417, independently authenticates Definition 3.1, Theorem 3.4 and Problem 3.7. Its fixed-field, d≥1 formulation includes the manuscript's proposed Q/dimension-two example. The additional question about Cohen–Macaulay intersections is separate.
- **Meaning of homology sphere.** [Swartz v1](https://arxiv.org/pdf/math/0512086v1), PDF 12–13, explicitly includes the local-link condition in Section 4. Its sufficient ear-decomposition construction is context, not a converse imported here.
- **Construction.** [LSV v2](https://arxiv.org/pdf/math/0406217v2), PDF 1–13, was read through the needed Sections 2–4. Equation (9), Corollary 4.6, Definition 4.7 and Proposition 4.8 supply the polynomial and simple-transitivity interfaces. The distinction between the cyclic algebra's base ring and the polynomial **matrix** representation is explicit. The global Ramanujan results in Section 6 are not imported.
- **Congruence antecedent.** [Lubotzky–Meshulam's ten-page author version](https://ma.huji.ac.il/~alexlub/PAPERS/a%20Moore%20Bound%20for%20simplicial%20complexes/a%20Moore%20Bound%20for%20simplicial%20complexes.pdf), PDF 5–8, uses a different irreducible-polynomial quotient in Proposition 3.3. The present t⁹ quotient is supported by the manuscript's own degree argument, not by ignoring that source hypothesis. The `www` host failed TLS validation; the no-`www` author host succeeded. An IAS alternate returned 403. Both failures are preserved.
- **Spectral antecedent.** [Ballmann–Świątkowski MPI96-127](https://archive.mpim-bonn.mpg.de/id/eprint/2255/1/preprint_1996_127.pdf), PDF 3–5, states the strict normalized-link-gap theorem, and explicitly permits the trivial group. The full 28-page proof was not revalidated; the current finite cocycle proof was read in full. Additional formula context on PDF 12 and 15 was inspected.
- **Curvature antecedent.** [Januszkiewicz–Świątkowski](https://www.numdam.org/article/PMIHES_2006__104__1_0.pdf), printed/PDF 8–12, supplies the cited Example 1.8(5). The surrounding full-subcomplex/k-large definitions were checked. The manuscript's direct Euler argument is what handles arbitrary non-induced sphere subcomplexes.
- **Recent adjacent result.** The full introduction of [Larson–Stapledon v2](https://arxiv.org/pdf/2504.20264v2), PDF 1–4, concerns algebraic/numerical complementary-vector consequences in characteristic two. This provides context; it is not substituted for the original sphere-piece question. Its entire 17-page proof and published-version introduction were not independently read in this scope.

The Nevo arXiv v2 alternate is also freshly retained. Reisner's criterion is explicitly stated by Nevo and used as the manuscript's definition; the original Reisner article was not separately acquired. No survey or search here certifies novelty, firstness, or present worldwide openness. The manuscript itself records unread literature, including full bodies of Chari 1997 and Baclawski 1982; this scope does not claim to close those gaps.

## Mathematical support and code coverage

Read in full: `main.tex`; the authored `inputs/PROOF.md`; current `verification/README.md`; the finite-incidence/torus/energy program; the optional matrix program; and `verify_all.py`. Full diffs authenticated that the historical root finite-incidence program and historical arithmetic diagnostic have the same mathematical cores as the current copies. The separate 73-line sphere-incidence diagnostic was also read. Hashes and exact paths are in `scope.json`.

The default diagnostic covers incidence arithmetic, all 266 single link-vertex deletions, the strict 1/2 boundary through a rational-homology torus, and energy double-counting. The runner advertises normal/optimized replay and three corrupted constructions in both modes. The optional program contains exact finite-field/polynomial local matrices plus floating spectral diagnostics. **No submitted program was executed by this scope reviewer.** Packaging helpers/build/self-tests were not audited as a software-validation assignment. None of the read mathematics programs enumerates the finite quotient or computes its complete boundary matrices; the universal theorem remains a written-proof obligation.

## Independence, content and remaining work

Historical dedicated verdicts, acceptance records, stored diagnostic results and sibling reports were not opened. Incidental opinion/status summaries were encountered in current record metadata, the manuscript's disclosure, the verification README, the author proof's closing status, and literal output templates in mathematical code. They were not adopted as fresh evidence. Hashing those archived bytes is not a review of their opinions.

`CONTENT_CANDIDATE.md` supplies conditional short copy and SEO fields for use only after the independent mathematical gate. It preserves the unrefereed status and substantial antecedents, avoids a firstness claim, and proposes no follow-up question. No follow-up has met the requested high bar in this scope.

**Strongest completed scope result:** the exact five-page edition and complete 120-file archive are authenticated; every current manuscript page and necessary mathematical support was read; the original question, source interfaces and all field/dimension/subcomplex boundaries are documented.

**Remaining gap:** independent mathematical review of the universal construction and proof, including fresh controls and appropriate published replay. This report is not that verdict. No publication, website, spreadsheet, Git, release or outreach action occurred.
