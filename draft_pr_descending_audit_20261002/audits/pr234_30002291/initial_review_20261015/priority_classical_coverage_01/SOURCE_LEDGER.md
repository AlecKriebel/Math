# Primary-source retrieval and read ledger

This is authored metadata, not reproduced source text. Raw PDFs, text extractions, retrieval responses and search records remain under ignored `private_sources/`. Retrieval timestamps, byte counts and SHA256 hashes are in its JSON records and private_source_inventory.json. Full-source availability does not mean every unrelated second-order proof was read.

## Read order and isolation

1. Frozen PROOF.md read in full at intake, before SOURCE_SCOPE.md and KNOWN_RESULTS.md.
2. Source cache filenames inspected. No root acceptance file, sibling report, inherited independent-review verdict or upstream report was opened.
3. Local original primary texts used only after independently authenticating arXiv histories and model/theorem text. A parent exchange supplied the institution's publisher-PDF URL, with no substantive conclusion requested.

## Controlling originals

| ID | Primary URL | Local artifact relative to this folder | Controlling portions read |
|---|---|---|---|
| OWR13 | [MFO](https://publications.mfo.de/handle/mfo/3340) | Read-only `../private_reading/owr2013-09.pdf` and `.txt` | Podolskij contribution, printed 491–493, especially 492; independently authenticated official record |
| SUR14 | [v1](https://arxiv.org/pdf/1405.1531v1) | private_sources/survey2014_v1.pdf and .txt | Model and assumptions in section 4.2, Theorem 4.8 and surrounding remarks, PDF 29–32; source's survey/integration context |
| SUR14D | [institutional December report](https://data.math.au.dk/publications/thiele/2014/math-thiele-2014-03.pdf) | private_sources/lma_thiele2014.pdf and .txt | Cover, section 4.2, Theorem 4.7 and references; distinguished from May arXiv version |
| LMA15 | [v1](https://arxiv.org/pdf/1506.06679v1) | private_sources/lma_v1.pdf and .txt | Model, (A)/(A-log), Theorem 1.1(i), Remark 2.3, further extensions; full section 4.1 proof including Lemmas 4.1/4.2, PDF 15–25 |
| LSS16a | [v1](https://arxiv.org/pdf/1604.02307v1) | private_sources/lss_v1.pdf and .txt | Model and theorem assumptions; Theorem 1.2(i), topology statement and v1/v2 differences |
| LSS16 | [v2](https://arxiv.org/pdf/1604.02307v2) | private_sources/lss_v2.pdf and .txt | Model (1.2), (A)/(B1), Theorem 1.2(i), Remarks 1.3/1.4; section 3 estimates; complete section 4.1 including Lemmas 4.3–4.7 and Remark 4.8, PDF 13–21 |
| FUN18 | [preprint](https://arxiv.org/pdf/1806.10352) | private_sources/functionals2018.pdf and .txt | Model, (A), Theorem 2.1(i), Proposition 2.3(i), auxiliary smoothness class, PDF 1–7; relevant finite-jump and small-jump proof sections, PDF 12–20 |
| MULT18 | [preprint](https://arxiv.org/pdf/1803.01017), [journal](https://www.vmsta.org/journal/VMSTA/article/122/read) | private_sources/multiple2018.pdf and .txt | Model, prior theorem and new multiple-singularity theorem, PDF 1–7; scope search through full extracted text |
| FIELD20a | [v1](https://arxiv.org/pdf/2008.01412v1) | private_sources/fields_v1.pdf and .txt | Independently scattered model, (beta)/(theta)/(g), deterministic kernels, Theorems 3.1/3.2 and Remark 3.3, PDF 1–8 |
| FIELD20 | [v3](https://arxiv.org/pdf/2008.01412v3) | private_sources/fields_v3.pdf and .txt | Same model and restrictions rechecked in revised text, PDF 3–8; marked Poisson construction and Gaussian beta=2 remark |
| JAC06 | [preprint](https://arxiv.org/pdf/math/0604450) | private_sources/jacod2006.pdf and .txt | Observed statistic, hypotheses H/K/L-s, representation (2.11), main results, PDF 1–11; full Lemma 5.8 proof around Poisson jump times, PDF 30–32 |
| ID14 | [preprint](https://arxiv.org/pdf/1404.7598) | private_sources/id_semimart2014.pdf and .txt | Model, representability definitions, Theorems 1.6/3.1 and scope, PDF 1–9; recognition versus asymptotic distinction |
| FRONT24 | [v2](https://arxiv.org/pdf/2410.00566v2) | private_sources/frontiers2024_v2.pdf and .txt | Section 2.3 further-reading map, relevant references and infinite-dimensional context; used as a search map only |

## Authentication and retrieval limits

- arXiv abstract/history pages authenticated submission timestamps for 1506.06679, 1604.02307, 1405.1531, 1806.10352, 1803.01017, 2008.01412 and math/0604450. The reported May 2014 and June 2018 dates are history dates, not the PDF build date. Some arXiv PDFs have regenerated recent title-page dates; those were not used as priority timestamps.
- The AOP DOI, journal volume/pages and author bibliography were authenticated through primary publisher/author-institution records. The author-institution URL supplied only as a retrieval lead was `https://pure.au.dk/portal/files/120886195/euclid.aop.1513069265.pdf`.
- Publisher `.full`, `.pdf`, legacy Euclid and download endpoints returned an iframe/security page or unusable response. IMS official AOP/Bernoulli issue PDFs were indexed by search but returned bot pages to direct retrieval and 502 through web open. Institution alternatives returned 403. These attempts do **not** count as full publisher-PDF inspection.
- The root cache named lma2017.pdf has the same preprint identity as the fresh LMA15 retrieval. Its label must not be used as publisher provenance.
- No metadata-only hit was treated as proving theorem coverage. Non-primary aggregator hits were used only to identify primary leads. One unrelated arXiv ID (1806.10346) was accidentally opened during adjacent-ID lookup; it was immediately identified as molecular physics and not used.

## Search boundaries

Searches covered combinations of power/quadratic variation, general semimartingale and Volterra drivers, predictable compensators, random measures and marked Poisson fields, scalar/multivariate Lévy semistationary models, the exact classical titles/DOIs, and their multiple-singularity/general-functionals/field extensions. The private search ledger records query strings and the controlling primary hits. This is a bounded search, not a proof of absence. No conclusion in the report depends on zero search hits.
