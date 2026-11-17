# Direct-history priority search matrix

All searches and primary reads occurred on 2026-10-12 UTC, with cutoff2026-10-12. Web searches were discovery, and scientific conclusions rely on actual primary bodies as identified in PRIORITY_REPORT.md. No query's absence is a proof of novelty. Incidental nonprimary results were not used as evidence. Negative screening findings are bounded by the read/access scope.

| Family | Exact web queries | Result and next primary-body check |
|---|---|---|
| Exact source / general polynomial | `"Gram determinants of real binary tensors"`; `"Gram locus" "Conjecture" Seigal`; `"Gram determinants" "single polynomial"`; `"Gram determinants of real binary tensors" erratum` | Original arXiv/author VOR/OWR, plus Ferudun canonical preprint. Ferudun full nine-page body read and Zenodo PDF downloaded; source introduction and formulas checked. |
| Source-specific conjecture history | `"Seigal" "Conjecture 1.5" tensors`; `"Gram determinants of real binary tensors" -site:researchgate.net -site:eurekamag.com -site:pmc.ncbi.nlm.nih.gov -site:seigal.github.io -site:arxiv.org`; `"Gram locus" polynomial -site:eulersolve.org`; `"Gram" "Seigal" erratum correction` | Thesis, Krämer, classical-groups complexity, related UTS thesis. Relevant primary full-text sections read, not accepted as resolution from metadata. |
| Later resolution / citations | `"Seigal" "Gram" "conjecture" -site:eulersolve.org -site:researchgate.net`; `"Gram determinants of real binary tensors" "cites"`; `"On the complexity of isomorphism problems" "III" classical groups arxiv`; `"Seigal" "Gram" "polynomial" zenodo` | Same source history, plus arXiv2306.03135. Actual group-isomorphism motivation and theorem scopes inspected. |
| Broad exact title / ID | `"Gram determinants of real binary tensors" -site:eulersolve.org -site:seigal.github.io -site:pmc.ncbi.nlm.nih.gov -site:researchcollaborations.elsevier.com -site:macaulay2.com -site:eurekamag.com -site:sciencedirect.com -site:people.math.harvard.edu -site:oa.tib.eu -site:arxiv.org`; `"1612.04420" -"Gram determinants of real binary tensors"`; `"Gram locus" "nonnegativity"`; `"Gram locus" "single" "polynomial"` | ORA record, thesis and CP-binary citation candidate. CP primary full PDF retrieved; direct citation is binary-tensor terminology, main result uses symmetric moment/LMI coordinates. |
| Errata / display correction | `"10.1002/qua.27030" "Seigal"`; `"Gram determinants" "corrigendum"`; `"Gram determinants" "errata"`; `"Seigal" "Gram" "single polynomial" -site:eulersolve.org -site:people.math.harvard.edu -site:seigal.github.io` | No additional explicit corrigendum/resolution identified. Source VOR/accepted/thesis repeated display checked; author-page/Crossref absence qualified. COVID citation body remained incomplete. |
| Target/problem identifiers | `"binary tensors" "single polynomial"`; `"Gram locus" "counterexample"`; `"30003480" "Gram"`; `"OWR-15428-003" -site:eulersolve.org` | Ferudun current treatment, original source and numeric-ID noise. No extra earlier candidate identified. This is not an exhaustive identifier index. |
| Current primary repositories | `site:zenodo.org "Gram determinants" tensor`; `site:arxiv.org "Gram determinants" Seigal conjecture`; `site:eulersolve.org "Gram" "Seigal"`; `"Quantitative structure-properties" "Seigal"` | Ferudun canonical page/current catalog and original arXiv. Current broad catalog not a historical snapshot. |
| Ingredient version authentication | `"On the largest multilinear singular values" "Theorem 5"`; `"16M110770X" pdf`; `"qua.27030" pdf`; `"Tensor Isomorphism over Some Matrix Groups" thesis` | Retrieved actual published DSL PDF from coauthor site, confirming November28,2017 publication and Theorem1.5. UTS thesis primary PDF independently retrieved despite web429. |
| Final source-specific checks | `"Seigal" "Gram" correction theorem`; `"Conjecture 1.5" "Gram" -site:eulersolve.org`; `"Gram determinants" "Kriebel"`; `"Gram locus" "polynomial" -site:eulersolve.org -site:researchgate.net` | Repeated original VOR/thesis/current overlap; no additional source-specific historical resolution identified. No exclusive-priority inference. |

## Direct API discovery and version checks

| Endpoint/query | Retrieved result, coverage, and evidence role |
|---|---|
| `https://arxiv.org/abs/1612.04420` and `/pdf/1612.04420v1`, `/pdf/1612.04420` | Onlyv1 listed; two downloaded PDF hashes identical. Relevant body read. |
| `https://arxiv.org/abs/1612.03751`, v1/v2 PDFs; Stegeman's published DSL PDF | Both manuscript versions obtained; v1 necessary theorem and different equality-case Theorem5 contrasted to published realization Theorem1.5 / v2Theorem5. |
| `https://api.crossref.org/works/10.1016/j.laa.2018.01.019` | Source DOI/publication metadata, cited-by count3, no correction relation. Metadata absence is not an exhaustive correction search. |
| `https://api.openalex.org/works/https://doi.org/10.1016/j.laa.2018.01.019` | WorkW2587191609, cited-by count6. Discovery only. |
| `https://api.openalex.org/works?filter=cites:W2587191609&per-page=200` | Six records returned; duplicated CP preprint/journal versions combined. Full candidate list compared with SemanticScholar. |
| SemanticScholar paperDOI query, fields`title,year,citationCount,citations.title,citations.year,citations.url,citations.externalIds,citations.openAccessPdf` | Five citation records including a duplicated Krämer title variant and the complexity paper. Metadata only; union yields six distinct cited works with OpenAlex. |
| `https://zenodo.org/api/records/23111048` and file-content endpoint | Successful JSON and exact PDF bytes; recordcreatedOctober2, latestv1.0 relation, PDF declared hash matched. Primary repository chronology and primary mathematical body. |
| `https://zenodo.org/api/records?q=%22Gram%20determinants%22&size=100` | HTTP400; no negative inference. |
| `https://zenodo.org/api/records?q=Seigal&size=25` | Seven total records, all returned. Relevant Gram-locus preprint23111048. Other metadata hits include unrelated nonmathematical papers and a generalized-trisecants preprint; those bodies were not read. The latter is an explicit metadata-triage limit, not proof of absence. |
| `https://export.arxiv.org/api/query?search_query=all:%22Gram%20determinants%22&start=0&max_results=100` | 122 total, first100 metadata records screened; only original Seigal paper identified as a binary-Gram-locus candidate. Remaining22 and other terminology are not excluded. |

## Full-text retrieval/read limits and failures

Successful PDF bytes and extraction hashes are in SOURCE_IDENTITIES.json and the recursive inventory. Ferudun, HSS, OWR and Seigal primary relevant passages were read directly; citing PDFs were scoped to relevant sections/citations/theorem statements. Visual source checks: Seigal printed354, Ferudun pages3,7,8. Images and source bodies are private.

- Canonical Ferudun PDF/metadata URLs gave direct-download403; web provided full PDF text/metadata, and the Zenodo file content succeeded with a matching declared SHA256.
- Seigal thesis Oxford/GitHub old URLs404; eScholarship download202 with zero bytes, including query retry. Primary web PDF body successfully supplied relevant Chapter4 content; private web response retained. No byte-hashed thesis PDF is claimed.
- Harvard original mirror403 and ORA direct-open403; original successful author VOR controls the published formula comparison. ORA metadata was read through an earlier primary web result.
- UTS primary web PDF429; direct primary HTTP download succeeded and relevant body read.
- COVID primary PMC partial body read; saved direct HTML is a bot challenge. EuropePMC web inaccessible; fullTextXML500; PMC OAI400; a later multi-open web call failed500. Exact Seigal citation context and full body remain unverified.
- Zenodo public HTML could not be opened by the web tool; its successful API and PDF acquisition suffice for the specific record facts and primary body.

The final search is extensive within this approach family, not an exhaustive theorem-index audit. Metadata, abstracts, citation counts and search absence never establish novelty. Independently indexed universal historical exclusion and a third-party archive of September30 repository visibility remain open.
