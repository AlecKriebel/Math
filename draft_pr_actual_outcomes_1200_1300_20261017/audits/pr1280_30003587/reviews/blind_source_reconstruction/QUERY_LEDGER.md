# Literal-query ledger

All entries are authored status records. No source excerpts or search-result snippets are reproduced here. Persisted source bodies, extracted text, renderings, and raw provider responses are confined to `_local/`. Retrieval times and headers for direct downloads are in `_local/*_fetch.json` and `_local/source_fetch.json`.

Provider: `web.run` for the requests below; direct HTTPS reads were also used to preserve primary bytes. Queries were made during this reconstruction on 2026-10-18 UTC. The original primary URL was supplied in the assignment. These searches did not target any candidate, repository, pull request, or review.

| Entry | Literal request | URL or primary lead | Authored status |
| --- | --- | --- | --- |
| D1 | `open https://ems.press/journals/owr/articles/15585` | <https://ems.press/journals/owr/articles/15585> | Publisher metadata authenticated; primary HTML preserved |
| D2 | `open https://ems.press/content/serial-article-files/46706` | <https://ems.press/content/serial-article-files/46706> | Primary PDF body downloaded, extracted, printed page 2621 rendered and visually inspected |
| D3 | `open https://arxiv.org/abs/1708.08258` | <https://arxiv.org/abs/1708.08258> | Primary abstract/version history authenticated; v3 PDF and HTML preserved |
| Q1 | `"1708.08258" strongly approximately inner` | <https://arxiv.org/abs/1708.08258> | Primary preprint identified; secondary metadata snippets also displayed but not used as theorem evidence |
| Q2 | `"diagonal quasi-free" "periodic"` | <https://ems.press/content/serial-article-files/46706> | Returned original question and restricted theorem; no general periodic theorem imported |
| Q3 | `"Cuntz-Krieger algebras of directed graphs" Kumjian Pask Raeburn 1998 pdf` | <https://documents.uow.edu.au/~dpask/index_files/papers/ckaodg.pdf> | Primary author-hosted paper fetched; graph conventions and structural background checked |
| Q4 | `"graph" "diagonal" "maximal abelian" "Condition (L)" C*-algebras` | <https://www.maths.tcd.ie/pub/ims/bull61/S6101.pdf> | Primary Renault paper fetched; section 6.3 checked for diagonal MASA under exits |
| D4 | `open https://arxiv.org/abs/1708.08258v1` | <https://arxiv.org/abs/1708.08258v1> | Initial preprint version fetched separately; date and restricted graph theorem checked |
| D5 | `open https://www.mscand.dk/article/view/114823` | <https://journals.msp.org/mscand/article/view/221> | Publisher redirect observed; no new theorem imported from this landing page |
| Q5 | `Izumi "Finite group actions" "Definition 3.6" strongly approximately inner pdf` | <https://projecteuclid.org/journalArticle/Download?urlid=10.1215/S0012-7094-04-12221-3> | Original Duke dependency identified; body not fetched, so no claim of direct Definition 3.6 inspection |
| Q6 | `"Finite group actions on C*-algebras with the Rohlin property, I" pdf` | <https://doi.org/10.1215/S0012-7094-04-12221-3> | Bibliographic corroboration only; actual definition authenticated in workshop body and primary preprint Definition 2.5 |
| R1 | Replay of D1-D3 and Q1-Q2 | Same URLs and literal queries | Provider output archived in `_local/authentication_queries_replay_raw.txt`; the first display was not archived verbatim |

Direct download URL membership:

- <https://ems.press/content/serial-article-files/46706>
- <https://ems.press/journals/owr/articles/15585>
- <https://arxiv.org/pdf/1708.08258>
- <https://arxiv.org/abs/1708.08258>
- <https://arxiv.org/pdf/1708.08258v1>
- <https://arxiv.org/abs/1708.08258v1>
- <https://documents.uow.edu.au/~dpask/index_files/papers/ckaodg.pdf>
- <https://www.maths.tcd.ie/pub/ims/bull61/S6101.pdf>

Raw provider response membership:

- `_local/web_sources_search_raw.txt`: Q3-Q4 and D4-D5.
- `_local/izumi_search_raw.txt`: Q5-Q6.
- `_local/authentication_queries_replay_raw.txt`: R1.

Nonprimary search results included bibliographic aggregators, research-sharing mirrors, theses, and unrelated results. They were visible as search outputs, not mathematical authorities. No candidate-specific material was exposed by any result noticed in this run. A complete novelty or current-status search was not attempted.
