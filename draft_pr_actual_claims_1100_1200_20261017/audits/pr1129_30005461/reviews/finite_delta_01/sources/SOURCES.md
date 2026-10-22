# Fresh primary-source versions and inspection boundaries

All source bodies below are stored only in ignored sources/private/. Renders and text-extraction intermediates are ignored too. Public receipts contain URLs, times, sizes, and digests only. No complete source is republished.

| ID | Requested primary URL | Bytes | SHA-256 |
| --- | --- | ---: | --- |
| stubborn_v1_pdf | https://arxiv.org/pdf/2602.01191v1 | 648190 | `c91b217bbe413cb934822be9c5f364c75739b38b7bdf178bbf2b764af6ecd0b9` |
| stubborn_current_record | https://arxiv.org/abs/2602.01191 | 42408 | `a4465d107cea8d095ec6714705515b623d5a59a9770f3370e1d8deb9efb57755` |
| stubborn_v1_record | https://arxiv.org/abs/2602.01191v1 | 42420 | `c7c122e592ffd78a4acf0ac7d20eed623e3296e6d925d62a4ca6797ef7c143c3` |
| owr_2023_14 | https://ems.press/content/serial-article-files/47007 | 734622 | `5a9bdc9f9daa12ef35185ceae208c0f2f75e191875827f78b7b6ad0f5cdbf240` |
| bkr_publisher | https://www.cambridge.org/core/journals/forum-of-mathematics-sigma/article/on-odd-powers-of-nonnegative-polynomials-that-are-not-sums-of-squares/7C4BAF1C7EBA17DE741C36DB40691412 | 3328553 | `bb0b854ccff48a656d7c1b2bd03e6395c959c361be634c74189f02e5910e9053` |
| bkr_pdf | https://www.cambridge.org/core/services/aop-cambridge-core/content/view/7C4BAF1C7EBA17DE741C36DB40691412/S2050509426102217a.pdf/on-odd-powers-of-nonnegative-polynomials-that-are-not-sums-of-squares.pdf | 666704 | `f4058ac7b54e498c5b639eb21bf54973b421a9fc7b5ed301b1053e0e594078bb` |
| stubborn_author_current_status | https://sites.google.com/site/grrigg/ | 323076 | `2099226a1e91fed3c070163ad1cfae441e995af284f92e839ca05ce2d8b764df` |

## Actual inspection

- OWR 14/2023: 72-page PDF, physical p.40 / printed p.780 read completely in text and visually. Exact affine target, threshold convention, and neighboring distinct positive-definite perturbation inspected. Remaining pages not substantively audited.
- Stubborn Polynomials v1: 24-page PDF, arXiv margin v1 / 1 February 2026, manuscript date 3 February 2026. Complete pages 2 and 20 visually inspected; page 20 Definition 6.3 and Theorem 6.4, page 2 Theorem 1.2. Full Theorem 6.4 proof inspected through page 21 text. Page 19/example context and definition of stubbornness also inspected in available primary HTML/text. The rest of the paper and foundational Del Pezzo references are not independently validated.
- Current unversioned arXiv abstract record and v1 abstract record inspected for submission history, version, and journal-reference fields. Both show only v1, submitted 1 February 2026, no journal reference. This does not prove absence of an unindexed journal publication.
- Fresh author publication page: entry for Stubborn Polynomials inspected; it says submitted for publication. Other entries not audited.
- BKR publisher HTML: publication metadata, exact Theorem 6.3 family/statement/proof, its c_0=0 paragraph, and limit-question discussion inspected. Publisher PDF pages 23-24 read and visually inspected, including reference [2] to Stubborn Polynomials. The rest of BKR is outside this family audit. Publisher PDF is 25 pages and is the current published article, not the 2024 arXiv version.
- Supplied PROOF.md, REAL_DELTA_APPENDIX.md, MATHEMATICAL_AUDIT.md were each read completely and separately SHA-256 pinned. No omitted historical check program or historical count was used as authority.

Fresh retrieval times and final response URLs are in FETCH_RECEIPTS.json. The browser DOI redirect failed once, but the canonical publisher HTML and PDF were retrieved directly and inspected successfully. Source bytes retain their own digests; the public RECEIPT.json fingerprints this metadata and all authored public files.
