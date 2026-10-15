# Search ledger

Search horizon: material publicly available through 2026-10-15, with queries aimed across 2000–2026. No date filter was treated as a completeness guarantee. Exact queries, archive timestamps and response hashes are in `SEARCH_LEDGER.json`; whole provider payloads are ignored/private. Call 001 is a replay because its initial response was not persisted. The ledger records negative and irrelevant branches without converting them into novelty evidence.

| Call | Search family / primary leads | Query count |
|---|---|---:|
| 001 | A,B; ordinary-semimartingale and Volterra leads | 3 |
| 002 | Liu2011; continuous-martingale literature | 4 |
| 003 | Hu/Russo; Liu2011 | 4 |
| 004 | A,B; Russo original | 3 |
| 005 | A,B; martingale-convolution branch | 4 |
| 006 | Russo; ordinary variation / modern Volterra | 4 |
| 007 | Critical2017; Errami1998 | 4 |
| 008 | OWR2013; ambit bibliography | 4 |
| 009 | BenthVeraart2024; Ljungdahl2018 | 4 |
| 010 | Hu2009; WeakVolterra2021 | 4 |
| 011 | Ljungdahl thesis; shot-noise branch | 4 |
| 012 | A,B; WeakVolterra2021 | 0 |
| 013 | A,B; primary bibliography | 4 |
| 014 | C | 4 |
| 015 | C; accessible-original checks | 0 |
| 016 | C; bibliography; VMSTA full text | 0 |
| 017 | C; ordinary-semimartingale checks | 4 |
| 018 | FractionalFields2021 | 0 |
| 019 | C metadata; Heinrich thesis | 4 |
| 020 | A,B,C metadata | 4 |
| 021 | Liu2017; Corcuera original | 4 |
| 022 | General semimartingale/Volterra branch | 4 |
| 023 | Jacod; Liu-related originals | 4 |
| 024 | Liu-related; general covariation branch | 4 |
| 025 | E; modern Volterra originals | 4 |
| 026 | Harmonizable2024 | 0 |
| 027 | E; Liu full-text search | 4 |
| 028 | D | 4 |
| 029 | Liu2017 publisher dates; general-kernel branch | 4 |
| 030 | Liu2017 access failure; university metadata | 0 |
| 031 | Liu2011 correct PII; Liu2014 preview | 0 |
| 032 | ApproxVolterra2019; Liu source search | 4 |

Total web search queries: 98. Additional opens/clicks and normal HTTP retrievals are recorded in the private response archive and source index.

Primary source acquisition used arXiv, publisher, university, and author-hosted originals. Aggregators were discovery aids only; no theorem-level coverage conclusion relies on their abstracts or summaries. Failed normal publisher retrievals are access gaps. Some initially guessed Elsevier PII URLs were unsuccessful; the correct Liu2011 PII was subsequently verified from primary metadata and used.

Search stop rule: multiple distinct theorem families had been inspected at the model/assumption/conclusion level; later citation chains returned the same main lines; major general-kernel alternatives were checked; remaining inaccessible originals are explicitly unresolved. This is a bounded adversarial audit, not an exhaustive bibliography or proof of novelty.
