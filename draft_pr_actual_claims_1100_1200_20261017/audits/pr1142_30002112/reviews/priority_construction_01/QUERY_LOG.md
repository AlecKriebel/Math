# Query and retrieval metadata

Date of execution: 17 October 2026 UTC. These are actual executed queries. Discovery snippets were treated as leads, not as proof of target scope. All primary-body classifications are stated separately in REPORT.md and the reading receipt. No prior or concurrent audit was consulted.

## Search batches

1. Initial construction search (web transcript `turn845search*`; retained raw return privately):
   - `"isoperimetric control" "hypersurface" "Nash"`
   - `"Colbois" "Dryden" "El Soufi" "Nash" "boundary"`
   - `"eigenvalues" "hypersurface" "small ball" "Colbois"`
   - `"isoperimetric" "boundary" "additive" "Colbois"`
   - Outcome: Nash–Kuiper/Steklov applications and nearby surveys. No full Euclidean target classification from this batch alone. Steklov and later 2026 hits were not counted as target resolutions.

2. CDE citation/consequence and isoperimetric search (web transcript `turn846search*`, `turn846academia*`):
   - `"Bounding the eigenvalues of the Laplace-Beltrami operator on compact submanifolds" citations`
   - `"hypersurface" "eigenvalues" "Nash-Kuiper"`
   - `"isoperimetric" "hypersurface" "additive" eigenvalues`
   - `"Colbois" "Hassannezhad" "isoperimetric" spectrum`
   - Outcome: official CDE publication metadata and institutional Pétiard thesis. The thesis PDF body, rather than the search description, supplied the first decisive full-target finding.

3. Pétiard provenance search (web transcript `turn852search*`, `turn852academia*`):
   - `"Pétiard" "Kröger"`
   - `"Counter-example to a Kröger type spectral inequality"`
   - `"Isoperimetric inequalities for Laplace and Steklov problems" 2019`
   - `"Petiard" "hypersurface" "eigenvalues"`
   - Outcome: arXiv:1706.09189 and institutional thesis. Downloaded and read the entire six-page v1 article; checked history rather than search-engine age labels.

4. Localization and flexible-embedding search (web transcript `turn861search*`):
   - `"hypersurface" "eigenvalues" "arbitrarily small" Nash`
   - `"hypersurface" "prescribed" "area" "first eigenvalue" Colbois`
   - `"Nash" "Kuiper" "isoperimetric ratio" eigenvalues`
   - Outcome: related Steklov small-eigenvalue constructions and Colbois survey leads. No independently recorded exact prescribed-small-ball, prescribed-area, large-gap lemma was identified from these search leads.

5. Citation-neighbor and metric-control search (web transcript `turn862search*`):
   - `"Colbois" "Dryden" "El Soufi" "Pétiard"`
   - `"Metric upper bounds for Steklov and Laplace eigenvalues" arxiv`
   - `"hypersurface" "large eigenvalues" "ball"`
   - Outcome: arXiv:2108.03101 and concentration papers. Read selected primary introductory statements and remarks of exact v2; did not classify abstracts as the additive target.

6. Hassannezhad and later citation search (web transcript `turn866search*`, retained raw return privately):
   - `"Conformal upper bounds for the eigenvalues of the Laplacian and Steklov problem" arxiv`
   - `"Nash-Kuiper" "eigenvalues" "boundary" -site:researchgate.net -site:scribd.com`
   - `"isoperimetric ratio" "Petiard" -site:researchgate.net`
   - Outcome: official Hassannezhad journal abstract/bibliography; another thesis cites Pétiard's Chapter 2. The latter was a lead only and was not needed or body-read as the positive priority proof.

7. Final source/venue search (web transcript `turn871search*`, `turn871academia*`; retained raw return privately):
   - `Asma Hassannezhad "Conformal upper bounds" filetype:pdf`
   - `"John Nash’s nonlinear iteration" De Lellis Székelyhidi 2012`
   - `"Pétiard" "Counter-example" published`
   - Outcome: author/institutional records and the precise Nash–Kuiper author PDF. No independently verified later journal venue for Pétiard's preprint was found. This is not a claim that none exists.

## Direct primary reads and histories

- OWR full report supplied privately; relevant talk on printed pages 2034–2036 read. DOI: `10.4171/owr/2012/33`; primary URL `https://ems.press/content/serial-article-files/46403`.
- CDE arXiv abstract/history fetched from `https://arxiv.org/abs/0909.5346`; exact v1 PDF fetched from `https://arxiv.org/pdf/0909.5346v1`. History: one version, 2009-09-29 13:56:51 UTC.
- CEG arXiv abstract/history fetched from `https://arxiv.org/abs/1007.0826`; exact v2 PDF fetched from `https://arxiv.org/pdf/1007.0826v2`. Histories: v1 2010-07-06 07:56:53 UTC; v2 2011-10-02 16:46:02 UTC.
- Pétiard abstract/history fetched from `https://arxiv.org/abs/1706.09189`; exact v1 PDF fetched from `https://arxiv.org/pdf/1706.09189v1`. History: one version, 2017-06-28 09:53:24 UTC.
- Thesis institutional bitstream, its bundle relation, and owning item JSON fetched in sequence. Item UUID `335eca35-b0d2-483b-b843-9a8cee1e04c8`; handle `20.500.14713/31635`; issue year 2019; accession/availability `2025-09-12T13:30:40Z`. Empty item-version endpoint; no version-history payload available. DOI registration API lookup returned 404, so no registration-date conclusion was drawn.
- Colbois–Girouard history at `https://arxiv.org/abs/2108.03101`; exact v2 body downloaded. History: v1 2021-08-06 13:07:25 UTC; v2 2023-08-20 09:48:37 UTC.
- An incorrectly recalled arXiv identifier, `1103.4384`, was opened during source discovery. Its title immediately identified an unrelated astrophysics paper; it was excluded and no PDF was downloaded. The transient returned metadata is retained in the private metadata-tool snapshot. This error has no bearing on any classification.

## Access limits

- `https://londmathsoc.onlinelibrary.wiley.com/doi/full/10.1112/blms/bdp100`: unavailable via web tool; official abstract/date landing page was available earlier. Full CDE author-preprint proof used.
- `https://www.degruyterbrill.com/document/doi/10.1515/crelle-2012-0008/html`: HTTP 405. Full CEG arXiv v2 used.
- `https://www.sciencedirect.com/science/article/pii/S0022123611002928`: HTTP 403 for direct body retrieval. Search returned official abstract and bibliographic metadata only. No primary-body theorem classification attributed to that unavailable journal body.

There were 24 explicit search queries in seven batches, plus the direct primary reads and history/API retrievals above. Early transient web returns not saved as files remain identified by their conversation transcript references; primary files supporting the decision have complete SHA-256/byte records in READ_RECEIPT.json.
