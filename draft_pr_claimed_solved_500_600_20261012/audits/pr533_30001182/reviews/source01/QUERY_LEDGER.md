# Source and priority query ledger

All queries were read-only on 2026-10-13 UTC, during approximately 04:46–05:02. Search results are discovery aids. Only identified primary papers, publisher records, version histories, deposit metadata, and independently checked proofs support REPORT.md. Ignored `tmp/` holds raw responses and source bytes. Third-party full text and the raw catalogue are excluded from the authored manifest.

## Web search families

| Batch | Exact query strings | Material outcome |
|---|---|---|
| W00 | `"Liebscher" "extremal" "independence"`; `"quantum independence" "ambient"`; `"Quantum symmetric states" "independence" Liebscher`; `"On Quantum Independence" Liebscher` | Original OWR and DKW; many unrelated quantum-gravity/copula results. No prior complete witness identified. Initial discovery return not retained as a separate raw file. |
| W01 | `"Liebscher" "extremal exchangeable"`; `"Liebscher" "symmetric states"`; `"Quantum symmetric states on free product" "Liebscher"`; `"extremal exchangeable" "independence"` | Original OWR; Accardi singleton paper as a background lead; unrelated finite exchangeability. Raw `web_search1.json`. |
| W02 | `"ambient dependence" "exchangeable"`; `"extremal-exchangeable" independence`; `"Liebscher" "independence" "Dykema"`; `"quantum independence" "Kriebel"` | Original OWR and unrelated work; no target preprint found. Raw `web_search2.json`. |
| W03 | `"quantum symmetric states" "restriction"`; `"quantum symmetric states" "maximal amalgamation"`; `"Liebscher" "ambient algebra"`; `"Liebscher" "extreme" "states" independence` | DKW talks and OWR2015/2016 summaries; known extremality framework. Raw `web_search3.json`. |
| W04 | `"30001182"`; `"Ambient dependence of extremal"`; `"Kriebel" "exchangeable"`; `"Liebscher" "independence" "extremal" -copulas -copula -Eckhard` | Mostly irrelevant product IDs/patents/copula literature. No search-engine target disclosure found. Raw `web_search4.json`. |
| W05 | `"symmetric states" "pure" "commutative" "free product"`; `"Liebscher" "On Quantum Independence" -copula` | Original OWR, DKW and Crismale–Fidaleo lead. Raw `web_later1.json`. |
| W06 | `"Exchangeable stochastic processes and symmetric states in quantum probability"`; `"symmetric states" "restriction" "pure states" independence`; `"Liebscher" "exchangeable" "independence" -copula -copulas` | arXiv1310.1566 primary identified and downloaded; no target resolution found. Raw `web_later2.json`. |
| W07 | `"Liebscher" "independence" "Zenodo"`; `"ambient" "exchangeable" "Ferudun"`; `"extremal" "independence" "Ferudun"`; `"quantum independence" "counterexample"` | No exact contemporary target paper found; unrelated graph-theoretic quantum-independence number results. Name query was a deposit-discovery check, not a presumption of overlap. Raw `web_current1.json`. |
| W08 | `"free product" "symmetric states" "inclusion"`; `"free product" "exchangeable" "restriction" "extreme"`; `"quantum independence" Liebscher -chromatic -number -graph -gravity -cosmology -copula`; `"exchangeability" "ambient algebra"` | DKW and OWR2016 repeat framework; no all-witness target obstruction. Raw `web_scope_more.json`. |
| W09 | `"Liebscher" "extremal" "free product"`; `"extremal exchangeable independence"`; `"extreme exchangeable" "ambient"`; `"independence" "Liebscher" "state extension"` | Original OWR and unrelated results; no additional exact target source. Raw `web_lasttarget.json`. |

Search engine returns combine batches and can fail exact matching. The negative observations above mean no relevant paper was identified in those returned results; they are not evidence of exhaustive absence.

## Primary-source and index operations

| Endpoint or operation | Result and evidential role |
|---|---|
| Official MFO OWR2009/09 PDF; EMS article3392 | Fresh bytes match recorded hash; complete printed Liebscher pp540–541 visually read. EMS states publication2009-12-23. |
| `https://arxiv.org/abs/1305.7293v3`, explicitly versioned v1 and v3 PDFs | arXiv publicly records v1 2013-05-31, v3 2014-09-22. Folding is Prop8.8 in v1 and Prop8.7 in v3. Both complete relevant statements visually read; current v3 used for mathematical classification. |
| `https://api.crossref.org/works/10.1090/tran6661` | Publisher metadata: online2016-03-21, volume369, issue1, pages645–679. Created2015-02-11 is DOI metadata chronology, not first publication. Raw `query_raw_0.json`. |
| DOI/journal page and journal PDF | Web DOI open unavailable; AMS returned403. No journal-proof inspection claimed. |
| `https://api.openalex.org/works/https://doi.org/10.1090/tran6661` | Discovery only; bibliographic date2015-02-11 matches metadata deposit, so not used as first-publication evidence. Raw `query_raw_1.json`. |
| `https://api.openalex.org/works?filter=cites:W2164772287&per-page=100` | Five indexed citing records: Thompson monoid paper, KMS paper, tracial-simplex preprint, semi-cosimplicial paper, Indian operator-algebra survey. Citation indexing is incomplete. The Thompson full text was screened only; KMS/tracial relevant material read. Raw `openalex_citing.json`. |
| Crossref `query.bibliographic=Liebscher On Quantum Independence&rows=6` and `ambient dependence extremal exchangeable independence&rows=10` | No exact target resolution found; mostly irrelevant title matches. Bounded metadata discovery only. |
| arXiv1401.4692,1609.01225,2009.14811,1310.1566,2607.20342 PDFs | Download hashes in SOURCE_HASHES.json. Read coverage is explicit there. No whole-paper correctness validation inferred from selective reading. |
| arXiv2509.02270v2 abstract/version history | Current 2026 version and DOI10.1016/j.aim.2026.111119 identified; abstract scope differs. Full proof remains unread lead. |
| Oxford ORA thesis10.5287/ora-ermd4qrd8 | DataCite deposit abstract read; Oxford full record returned403. Metadata dates are Created2026-06-12/Copyrighted2025 and DOI-record creation2026-08-17. They do not certify an earlier public release. Full thesis is unresolved. |
| A mistaken arXiv1401.5810 open | Unrelated chain-fountain physics paper; excluded from conclusions and source packet. |
| HuggingFace immutable revision372682f27c1b0d3d39e75fa63ad7932c7a2e1bde | Fresh 69,291,427 bytes/SHA37067f… agree; target identity and broad normalized statement read. Catalogue mathematical labels ignored as proof/priority evidence. |

## Deposit and current-disclosure metadata searches

DataCite used `https://api.datacite.org/dois`, query below and `page[size]=100`; raw result pages are ignored.

| Query | Coverage/result |
|---|---|
| `creators.name:"Kriebel, Alec"` | 183 records, both pages read; no target-like title. This does not search every possible author-name spelling. |
| `Liebscher` | 690 results; first100 inspected. Mostly unrelated names. Explicitly not exhaustive. |
| `exchangeable AND (quantum OR symmetric)` | 253 results, all3 metadata pages screened; relevant sample-state/categorical papers identified. Metadata query semantics and indexing are limits. |
| `"ambient dependence"` | 12 metadata matches; none an operator-algebra target. |
| `30001182` | Zero metadata matches. |
| `"OWR-3392-009"` | Zero metadata matches. |
| `Liebscher AND quantum AND independence` | Zero metadata matches. |
| `"extremal exchangeable"` | One unrelated finite-statistics paper. |
| `titles.title:"ambient" AND titles.title:"exchangeable"` | Zero metadata matches. |

Zenodo used `/api/records` with q=`"quantum independence"` (five unrelated deposited results) and q=`"ambient dependence"` (zero). q=`Liebscher`, q=`exchangeable AND Kriebel`, and q=`"Kriebel"` returned400. Failed calls supply no absence evidence. No authentication, deposit, upload, or other mutation occurred.

Unauthenticated GitHub GETs independently read `/repos/AlecKriebel/Math/pulls/533`, `/commits/135911efff1ad14314f0506b0d5f158ba986426f`, `/repos/AlecKriebel/Math`, and `/releases?per_page=100`. PR creation is server-recorded2026-10-04T07:21:22Z; head unchanged at audit read. Repository is currently public. All28 returned releases screened; no target release. A broad word match in one unrelated mass-action release was excluded. Commit timestamps are author-controlled; no independent historical visibility archive was obtained.

## Initial unresolved leads at the first checkpoint (updated below)

1. Initially: Oxford thesis full text and its precise public-release history. **Full institutional text subsequently obtained and relevant proof/reference scope checked; specific lead closed in the05:09 addendum.** Its deposited abstract suggests categorical process limits, but does not rule out an incidental target observation.
2. Initially: complete arXiv2509.02270v2 text and references. **Complete43-page proof/reference material subsequently read; specific lead closed in the05:09 addendum.** Its abstract concerns twisted tensor products, not this target, but abstract-only inspection cannot exclude an incidental observation.
3. Older specialist literature using other terminology; complete citation searches on Scholar/zbMATH/MathSciNet were not available and are not represented as performed.
4. Journal-version comparison for DKW; access403 prevented it. The versioned author preprint supports the relevant theorem independently.
5. Historical archive of PR533's original public visibility and any target-specific release outside the services queried.

None of these leads is a positive prior-target overlap. No outside researcher was contacted and no outreach draft was prepared.

## 2026-10-13 05:05–05:09 UTC primary-source closure addendum

- Exact web queries: `"Exchangeability theorems as categorical limits of probabilistic and quantum processes"`; `"Ned Louis Summers" exchangeability thesis pdf`; `"4f027742-4931-4cc2-9736-cdf99741e338"`; `"ora-ermd4qrd8"`. The institutional record and an acknowledgement-only author PDF surfaced; only the institutional full thesis supports the proof comparison.
- Direct explicitly versioned arXiv2509.02270v2 PDF:200,530082bytes; complete proof/reference reading documented in the addendum and hashes.
- Ordinary unauthenticated HTTP GET of official ORA record with browser User-Agent:200,72019bytes. HTML exposes the official PDF full-text link and citation_pdf_url. The web-reader remains403, illustrating an access-method difference. No authentication or person-contact was used.
- Direct GET of official `/files/dj96021565`:200,1452750bytes; full191-page thesis obtained and inspected at explicit read coverage. DataCite DOI-record GET also succeeded. No API/OAI fallback remained necessary.
- Both formerly unresolved specific leads are now closed for reasonable priority review with no positive target overlap. Their earlier403/abstract-only observations above are historical checkpoints, not current limitations.
