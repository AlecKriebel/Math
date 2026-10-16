# Search coverage and reproducibility

All checks occurred on 2026-10-15 UTC. Successful full source payloads and web-tool response objects are in ignored `private/`, outside the safe authored manifest. Raw outputs may contain index snippets that are search hypotheses rather than evidence of theorem contents. Author, institution, repository and publisher sources support the historical claims. Citation indexes were discovery aids.

## Query families executed

1. Joint names with DDA, nonzero frequency, stability, 2024, 2025 and 2026; exact static paper title and citations.
2. Exact dynamic title and shorter title variants. These led to the Padova 2023 and IMU 2022 announcements, then the Hilbert 2023 reference. No actual manuscript was located.
3. Separate author homepages and publication lists: Costabel current recent/all/CV; Dauge current documentation/CV/publications; Nedaiasl IASBS attempt, ORCID and author results. Checked primary sources extending to August 2026.
4. Current arXiv searches by each full author name, newest first, 200 results maximum on one page. Inspected returned titles and dates, with counts 24, 32 and 8. The static and Hilbert version-history pages were checked directly.
5. HAL API full static record; all Nedaiasl records matching the name; Costabel/Dauge submissions in 2023-2026; exact dynamic title and fulltext queries. All returned metadata were read. Author queries are not claimed exhaustive under every possible alias.
6. Publisher Crossref static/Hilbert records and 100 ranked Nedaiasl author-query records since 2023. The sparse separate ORCID record was not treated as complete.
7. Semantic Scholar and OpenAlex citation lists; followed the three-item union: Hilbert 2023 relevant full proofs, Axioms 2026 partial publisher text, and Goepfert 2024 primary abstract/metadata with the PDF inaccessible.
8. Full PDF downloads for the 2021 slides through the current author link, static/Hilbert relevant proofs, and the source OWR contribution. Images on the 2021 slides were inspected by rendering.

## Material limitations

The dynamic work is known by name but its actual manuscript was not found. Current author lists and repository searches do not prove absence of unpublished or retitled work. HAL web pages and the thesis PDF were challenged or denied; ordinary public API metadata worked. The IASBS author homepage was inaccessible. The publisher static PDF request returned HTML, so the journal full text was not read; arXiv v3 was. Edition differences beyond the checked versions remain possible. Citation-index counts differ and cannot certify complete coverage. No outreach was prepared or initiated.

## Private payload inventory

`search1.json`, `search2.json`, `queries3.json`, `queries_arxiv_hal.json` and `final_title_search.json` preserve search results. `homepages.json`, `costabel_bib.json`, `author_queries.json`, `author_open3.json` and `dauge_bib.json` preserve primary web opens and discovery responses. `citation_followup.json`, `thesis_metadata.json`, `thesis_search.json` and `thesis_pdf_web.json` preserve forward-citation followups. Direct author HTML, arXiv HTML, HAL/Crossref/ORCID/index JSON, PDFs and rendered PNGs are also private. The source read map gives exact artifact digests and read depth. No sibling priority verdicts were consulted.
