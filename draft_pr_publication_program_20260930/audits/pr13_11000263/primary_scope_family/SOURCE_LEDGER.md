# Source/version ledger

Every source is a read-only public retrieval. Full source bytes are cached only under ignored `tmp/`. Persistent reports contain own analysis, short source locators and hashes, not third-party fulltexts. For the correction probe's sources, see its separate manifest and notes.

| ID | Primary artifact / version | Verified locator | Supported scope / limitation |
|---|---|---|---|
| S1 | [math/0505064v1](https://arxiv.org/abs/math/0505064v1), submitted 2005-05-04 00:23:54 UTC; no later version on current record | printed pp. 3, 4, 10, 12, 13, 14; arXiv source `.tex` | Generator ceiling, coefficient restrictions, whole-word inverse, exact recursion/relations, Question 6 and neighbors. Formula page visually checked; source TeX independently confirms inverse/index defect. |
| S2 | [author-hosted published scan 10.pdf](https://web.math.ucsb.edu/~bigelow/publications/10.pdf), Proc. Sympos. Pure Math. 74, 2006, pp. 285-299 | printed pp. 285, 287, 288, 294, 296, 297, 298 = one-based PDF pages 1, 3, 4, 10, 12, 13, 14 | Same target definitions visibly survive publication. Scan creation 2015 is digitization evidence, not article date. |
| S3 | [Farb edited-volume draft mcgbook.pdf](https://www.math.uchicago.edu/~farb/papers/mcgbook.pdf), PDF creation 2006-07-24 | generator PDF p. 311; coefficient p. 312; sum-unit p. 319; one-parameter p. 320; definitions printed p. 315 / PDF p. 322; questions printed p. 316 / PDF p. 323 | Actual imported source. PDF has 402 pages; printed page and PDF page distinguished. |
| B1 | [Crossref DOI record](https://api.crossref.org/works/10.1090/pspum/074/2264547) | registry fields title/author/year/page/publisher | Confirms title, Stephen Bigelow, year 2006, pp. 285-299, AMS. DOI redirect inaccessible through browser tool; Crossref returned directly. |
| A1 | [initial Argus commit b8f6054](https://github.com/Argus-AiTeam/argus-mathematics/commit/b8f60542f758750e263016cad1d45cc0650ed64d) | review-package blob 274c04c5..., initial 8-page report, CITATION.cff | Exact two-repair Burau construction already contained here; first twist and joint image extension in report. Metadata dates 2026-08-30; unsigned, not external publication timestamp. |
| A2 | [extension commit 5abed44](https://github.com/Argus-AiTeam/argus-mathematics/commit/5abed447441b42dbe9f735e8b2960ee0a0705235) | unchanged review blob; extension PDF pp. 1-5; README/completion boundary | Adds full twist and u=q^3/X4=0. Manuscript names Zimo and Qiugu; no universal finite-dimension proof. Metadata dates 2026-09-03; unsigned. |
| R1 | [BIRS 2004 report](https://www.birs.ca/workshops/2004/04w5526/report04w5526.pdf) | PDF p. 4, visually checked by correction probe | Two-parameter finite-dimensional zipper announcement; no complete presentation identifying it with the printed target. |
| R2 | [AMS Paper 48822 native API](https://meetings.ams.org/math/spring2025w/meetingapi.cgi/Paper/48822) | abstract record and separate slot API | Current Bigelow-Moos work, finite-dimensional quotient and normal-form algorithm announcement; no target relation identification. May 4, 2025 scheduled date; citation fields contain a May 3 inconsistency. |
| L1 | Local source dataset at revision 37e53eabe540fb458758e198be61634bd02ee008 | numeric ID/code joins once; definitions spill into 11000262 | Upstream snapshot open/OPEN-TRIAGE is metadata, not current openness certificate. |
| L2 | Local PR head 7a845f7e025a24affe1b712cf7ada648570f9c64 | catalog row 11000263; related-target groups | Queued/open, 0/5; separate neighbors; literal target not marked solved. Names-only bounded duplicate scan cannot exclude earlier worldwide work. |

## Bytes and identifiers

- S1 PDF SHA256 `5666062b7bcf6121f6411bfd4bff4ac338eae7901a44a39bcd64260c0025b31e` (246141 bytes).
- S1 gzipped source SHA256 `7530206e5237810b8f858885d7fe9186688a981189b3ad76b905e6092557c60c` (17275 bytes); decompressed TeX SHA256 `254ab65663a7af56375a07f03edf7c753470cf830fb519e40cc8e30865faef7a`.
- S2 SHA256 `31caf2929cfd10c44bee9b41fc85c27791d58c6769951fee7564f7abab55e909` (2162740 bytes).
- S3 SHA256 `f37c6a1dbc875105c2b294196de1a03a88595b75e8705e6077e9d48f066e402a` (2724624 bytes).
- B1 SHA256 `49e2ac189b2fcb9c49f85d11b5d7d92e85355aa45899b4d8094b78e115349216` (1733 bytes).
- A1 report SHA256 `2282e06444902f6079c84ee0e8368885dd1983c420d829b9934f07899dec5750` (255884 bytes), Git blob `6133919ac4a2704da55ffeef03801337a5ecab78`.
- A1/A2 review SHA256 `3f23574c4ae400301f7aba7835599650caf016b0f7662122002e7b88b95e44d2` (4893 bytes), Git blob `274c04c5f59fd5f56be95373191ae36d278b3618`.
- A2 extension SHA256 `1f4cd1b3c1ff08098a10cf5ea0dc0dfbb9b7f2a927f72c18cb791bccbc777d4c` (290211 bytes), Git blob `ac74ae3fc6cd10fd624a743ef6584d67df6084c8`.
- L1 problems SHA256 `04128381e42a5e312326d74adb0947ee02062ade70229e02d3060ac4ef9942cf`; research results `8da848d31c20eb4eecaa07702eced4724aa4a89f877c2a0774d9f3138389aa6b`.

Git blobs are SHA1 content-addressed identifiers and must not be mislabeled SHA256. Retrieval manifest HTTP/PDF dates are technical metadata and must not be promoted into original publication/editorial dates. All 21 cached source responses and 10 exact source/provenance assertions passed the final integrity replay.
