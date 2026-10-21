# Public read-only search ledger

Entries record actual queries and outcomes. Search no-hit is not proof of absence. Retrieved full texts and excerpts have separate read scopes in the final manifest.

All searches were public and read-only, executed 2026-10-05 approximately 20:48–21:00 UTC. Exact source retrieval times are recorded separately in HTTP receipts. Search-result JSON files contain the actual returned tool text. Earlier literal query strings were not separately saved before context compaction; entries 01–18 below preserve their known themes and result receipts, not invented literal queries or exact timestamps. Entries 19–21 give literal arguments still present in the live call history. This is an explicit search-replay limitation.

| Receipt | Query or operation theme, for result-only older calls | Outcome and limit |
| --- | --- | --- |
| web_search_01.json | Original GP, fundamental group; Ohtsuki update sources | Original arXiv, problem-list sources located. |
| web_open_02.json | Open GP arXiv, printed EMIS, candidate Ohtsuki page, 2003 draft | GP and draft accessible; EMIS attempt and wrong Ohtsuki path failed. |
| web_search_03.json | Named GP counterexamples, Conjecture 7.5, official Ohtsuki workshop | Official workshop page located; no authenticated resolution at this stage. |
| web_open_04.json | Workshop page, publisher metadata and printed arXiv | Official solutions link and printed source obtained. |
| web_search_05.json | Named conjecture and counterexamples; follow solutions, publisher PDF, INSPIRE | Solutions page and citation index inspected; direct publisher PDF unavailable. |
| web_search_06.json | Exact Kuriya title, PDF, solved quantum conjecture | Institutional author record and preprint citation lead. |
| web_search_07.json | Kuriya GP PDF, excluding ResearchGate, exact title, publication | Later LMO work found; no exact preprint bytes. |
| web_search_08.json | GP false/counterexamples, lens spaces, Kuriya 2003, quantum PSU(n) | Relevant scope leads; no authenticated finite full SU(5) answer. |
| web_search_09.json | GP 1998 counterexamples, exact 3475 magnitude, Conjecture 7.5 solution | ArXiv 2008 and 2010 papers; publisher date lead. |
| web_search_10.json | Japanese Kuriya/LMO, name, lens-space title outside ResearchGate | Kyushu and symposium records; exact preprint still inaccessible. |
| web_open_11.json | Large Kyushu and symposium PDFs | Web tool rejected PDFs above its 10 MiB limit; ordinary public HTTP downloads succeeded and were authenticated separately. |
| web_search_12.json | GP with SU(5), SU(4), refutation and disproof terms | No authenticated earlier target answer from these returned results. |
| web_search_13.json | Named GP outside ResearchGate, absolute magnitude/fundamental group counterexample | Hikami and publisher date confirmed; no current-status proof. |
| web_search_14.json | GP solution variants, magnitude SU(5), Kuriya/fundamental group | Returned sources did not authenticate the target's earlier resolution. |
| web_search_15.json | Yamada exact title, GP SU(N), status, erratum/correction | Earlier SU(2) bibliography lead; no correction authenticated. |
| web_search_16.json | Exact Kuriya title/PDF, marron author path, repositories, Japanese PhD | Institutional and ResearchGate author records; no exact preprint bytes. |
| web_find_17.json | Find Kuriya/GP in public author pages | ResearchGate exact publication link; current Osaka Sandai faculty page lists Kuriya without a homepage link. |
| web_open_18.json | Open exact-title ResearchGate publication | Unclaimed aggregator abstract only; explicitly no full text. No request-for-full-text action taken. |

Exact recent queries:

- Receipt 19: `"The LMO invariant and the Guadagnini-Pilo conjecture" filetype:pdf`; `"Kuriya" "Guadagnini" preprint archive`; `"The absolute value of the Chern-Simons-Witten invariants" Yamada`; `"Guadagnini-Pilo" site:cir.nii.ac.jp`. Results repeated known institutional/bibliographic sources and Yamada citations; no exact Kuriya PDF.
- Receipt 20: `"Kuriya" "LMO" site:ir.library.osaka-u.ac.jp`; `"Kuriya" "Guadagnini" -site:researchgate.net -site:math.kyushu-u.ac.jp -site:scirate.com`; `"Kuriya" "marron" mathematics`; `"Kuriya" "Guadagnini-Pilo" "pdf" "2003"`. Results included Watanabe's 2007 paper citing *On the LMO conjecture* as a 2003 preprint, not the exact GP text. Unrelated name matches were disregarded. No new exact-title bytes.
- Receipt 21, which also preserves structured arguments: `"The Absolute Value" "Lens Spaces" "Yamada" site:worldscientific.com`; `"Guadagnini-Pilo" "counterexample"`; `"Conjecture 7.5" "Ohtsuki" "solved"`; `"Guadagnini-Pilo" "correction"`. No authenticated target correction or finite full SU(5) resolution in returned results. Aggregator current-status labels were not accepted as evidence.

Additional direct public operations:

- INSPIRE `refersto:recid:427075`, size 100: four returned citing records. All returned records examined for discovery; readable mathematical papers fetched as appropriate. No exhaustive coverage claimed.
- Semantic Scholar GP DOI citations, limit 100: five returned records, no next page in returned JSON. Index used only for discovery; not evidence of literature completeness.
- Semantic Scholar exact-title search: HTTP 429; receipt retained, no result body saved. Not a no-hit.
- Wayback CDX search `www.math.kyushu-u.ac.jp/~marron/*`, status 200, collapse URL key: `[]`. The path was inferred from a public institutional account name, not verified as an author homepage. No conclusion about other hostnames or paths.
- Old CiNII `search?q=Guadagnini-Pilo&format=atom`: redirected to generic `https://cir.nii.ac.jp/`, returned HTML rather than Atom search results. Uninformative, not a no-hit.
- Large scanned PDF receipt verification: Poppler rendered all 99 Kyushu pages as thumbnails; English OCR of 600-pixel pages failed to locate the title. Re-rendering physical pages 1–41 at 1800 pixels and OCR located physical page 32. That page was visually read. Earlier OCR failure was a resolution limit, not absence.
- Ohtsuki target copy comparison: physical pages 99–102 (printed 471–474) extracted from both PDFs, identical after whitespace removal. Actual receipt and excerpt hashes retained. No new mathematical evaluation performed.

Bounded stop rule: close after official problem-list/update sources, two citation-index neighborhoods, exact-title institutional/proceedings/author-page/archive checks and the accessible successor primary texts. The unresolved exact Kuriya preprint scope is carried into the verdict, rather than converted into a positive novelty assertion.
