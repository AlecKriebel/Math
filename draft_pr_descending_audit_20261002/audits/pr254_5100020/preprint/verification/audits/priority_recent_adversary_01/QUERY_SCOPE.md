# Query scope and depth — recent/public-artifact priority audit

Search run:2026-10-13, approximately05:17–05:30 UTC. Searches returned both relevant and irrelevant leads; only primary manuscripts, publisher/author pages, Zenodo records/files, and native repository objects support the report. Search snippets and third-party summaries were leads only. No sibling new priority report was read.

## Web query families actually used

- Exact labels: `"k403" billiards proof`, `"k403,a"`, `site:eulersolve.org "AMR-050-0020"`.
- Construction-aware: `"elliptic billiards" "antipedal" "origin" area`; `"Pedal" "Antipedal" "area" "odd" elliptic`; `"origin" "antipedal" "billiards" proof`; `"antipedal" "area ratio" "odd" ellipse`; `"origin antipedal"`; `"Origin-pedal" "antipedal" billiards area product`; `"center-pedal" "antipedal"`; `"center" "antipedal" "billiard"`.
- Primary-source restrictions: `site:arxiv.org elliptic billiards pedal antipedal area product`; `site:zenodo.org elliptic billiards origin antipedal`; `antipedal elliptic billiard invariant proof` restricted to arXiv; `"antipedal" "billiard" "proof"` and `"antipedal" "odd" "billiard"` restricted to EulerSolve.
- Recent lead screens: antipedal+billiards+2024/2025/2026; elliptic-billiard invariants/areas+2021–2026 restricted to arXiv and publisher sources; antipedal+elliptic+invariants+2022–2026 restricted to arXiv; antipedal+billiard with2020–2026 date restriction across arXiv/Zenodo/GitHub/EulerSolve. These did not amount to a complete year-by-year index census.
- Broader synonyms/covering routes: `"antipedal" "Poncelet" "area"`; `"antipedal" "invariant" "area" "odd N"`; `"antipedal" "odd" billiards areas invariant`; `"More about areas and centers of Poncelet polygons" antipedal`; `"Billiards in ellipses revisited" antipedal`; `"Exploring the Dynamics of the Circumcenter Map"`; `"bicentric" "hexagons" Reznik Garcia 2024`; `"A telescoping proof of the focal antipedal sum invariant"`. aiXiv was used as a catalogue lead, not as proof evidence.
- Selected negative screens excluded secondary hosts such as ResearchGate/Scribd/emergent summaries; any primary reference discovered there was followed to its original source.

## Direct primary-source and repository work

1. Entire frozen PR254 proof, source gate, existing source audit, metadata, and author log read. Strongest prior-credit combination identified before searching: PR204 plus a possible origin-antipedal/original-area ratio.
2. Current EulerSolve catalogue fetched. All21 AMR-050 metadata records and all21 source ZIPs downloaded, ZIP hashes compared with metadata, LaTeX manuscripts extracted safely. Exact statements and construction/pole references screened across the corpus. Detailed mathematical reading focused on the potential transfer lemmas in0021,0019,0026,0023,0014 and0069; this does **not** claim all21 manuscripts received a full independent mathematical audit.
3. Original deposited source archives authenticated for Zenodo IDs23079799,23085904,23087221,23088516,23077039,23071366,23092466,23089778,23090907. Provider MD5 matches all; original main-source hashes recorded. Current versions were not assumed to be original versions.
4. Expanded Zenodo antipedal query with optional sorting/size returned400. The plain `https://zenodo.org/api/records?q=antipedal` returned200 and nine indexed records. Additional old record21907170 was then authenticated through its original standalone TeX and evidence ZIP and read in full. Its explicit even/focal/N8 scope was checked rather than rejected by title alone.
5. Native GitHub PR204 and254 metadata and commit lists fetched. PR204 source recovered from its immutable tree/blob. Repository PR searches for `antipedal`, `5100020`, and `k403` returned13,1,2 hits respectively. These counts refer to those particular metadata/body searches, not complete code search.
6. Earlier immutable proof objects for background PR140,223,224,227,228 and110 fetched using commits before the candidate's reported author window. Initial PR110 path guesses failed because the correct ID is5100032; the native changed-file list recovered the actual source and matching author replay. PR140 and110 entire proofs read; other background objects screened for exact statements and relevant symmetry/area mechanisms.
7. Primary arXiv manuscripts2202.02551v3,2009.02581v3,1008.0110v1 fetched and relevant full sections inspected. The circumcenter manuscript's printed pages4–5 rendered and visually inspected after Poppler recovered an xref warning. The2021 bicentric and2024 bicentric-hexagon primary papers were read from the already downloaded primary-source cache; their checked statements concern other objects/periods.

## Access and inference boundaries

- Direct EulerSolve0020 page/metadata returned403; browser access likewise failed. Neither counts as absence or proof that no paper exists.
- The earliest source conjecture table's question mark cannot establish current openness. A lack of exact-ID hits cannot exclude a differently named corollary.
- Recorded Git dates, source logs, server PR creation, archive creation/modification and current HTTP access are distinct forms of chronology. No causality or first-discovery inference is made.
- Focal central-pairing and n-fold-circumcenter similarity transfers are explicitly blocked when they leave the required odd-origin area ratio unsupported.
- Source copies and raw responses remain under `sources/` and `receipts/`, excluded from public output. Public output contains only authored report/query log/logs/ledgers/pins/reproducible retrieval scripts/hash manifest.
