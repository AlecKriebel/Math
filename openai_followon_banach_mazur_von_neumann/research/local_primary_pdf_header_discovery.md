# Bounded physical PDF-header discovery

Checkpoint: 2026-10-06 23:06 PDT (2026-10-07 06:06 UTC).
Researcher: internal independent access agent, with a separate internal agent checking the Desktop research root. No outside individual was contacted.

**Outcome:** No new target article or author manuscript candidate was identified. Assigned bounded header-discovery route: 100% complete. Mandatory complete-article retrieval/read: 0% complete. These are access-subtask estimates, not mathematical-resolution or publication-package percentages. The first-page evidence does not justify global absence: some files have empty or failed text extraction, titles may be on a later page, and files outside the exact permitted/excluded scope were not searched.

Target: Jean Roydor, *Banach–Mazur stability of von Neumann algebras*, *Journal of Topology and Analysis* 14(03) (2022), 767–792, DOI [10.1142/S1793525321500151](https://doi.org/10.1142/S1793525321500151). The journal page span is 26 pages, but no page-count condition was imposed because an author manuscript may differ.

## Inventory, bounds, and method

At 2026-10-07 06:02:34 UTC, `rg --files --hidden --no-ignore` counted PDF filenames case-insensitively, scoped only to `/Users/alec/Documents/Math` and `/Users/alec/Desktop/math`. Explicit exclusions covered Git internals, dependency/Python/cache/virtual-environment folders, `build`, `_build`, `.build`, `build-*`, `dist`, `target`, `tmp`, `temp`, credential/secret directories, communications/email/messages directories, and browser-profile directories. The same explicit exclusions, roots, and full local inventory are retained in ignored metadata. Ignored files remained eligible because third-party research PDFs can be retained there. Real paths were checked to stay within each research root before reading. No unrelated home path, credential store, communications content, private browser profile, or other-project write was used.

The inventory found **13,993 PDF filenames** in Documents and **733** in Desktop, **14,726** total. These are filename counts; 98 Documents entries lacked any PDF signature within their first 1,024 bytes, so they were not classified as actual PDFs or submitted for text extraction.

The Documents scan started at 06:03:49 UTC and finished at 06:04:07 UTC, taking 18.61 seconds within a 180-second cap. Its confirmed running execution handle was session 85737; the process subsequently completed successfully. The separate Desktop scan ran at 06:04:23–06:04:25 UTC, taking 2.857 seconds within its 115-second cap. Both used six parallel extraction workers; per-file timeouts were eight seconds (Documents) and four seconds (Desktop). No time or volume cap left an inventoried eligible file unattempted.

Exact SHA-256 byte hashes deduplicated copies **within each root**. Cross-root duplicates were not additionally deduplicated. Only the first physical PDF page was extracted through `pdftotext`, with unrelated text kept solely in memory and discarded. Matching used normalized Unicode/whitespace and the exact title with dash variation, the exact DOI, or Jean Roydor's name. All filenames were eligible, including generic names. Metadata/page count was checked only for matching candidates. No full unrelated PDF text extraction or OCR was performed.

## Exact scan accounting

| Measure | Documents research root | Desktop research root |
|---|---:|---:|
| Inventoried PDF filenames | 13,993 | 733 |
| Entries lacking PDF signature in first 1,024 bytes | 98 | 0 reported |
| Eligible PDF byte paths hashed | 13,895 | 733 |
| Distinct byte hashes within root | 1,668 | 733 |
| Exact duplicate paths within root | 12,227 | 0 |
| Unique readable first pages scanned | 1,619 | 733 |
| Unique empty-text first pages | 41 | 0 |
| Unique failed first-page extractions | 8 | 0 |
| Matching unique candidates | 2 | 0 |
| Files unattempted because of time/volume cap | 0 | 0 |

Among the Documents duplicates, 12,168 reproduce a byte-identical file whose first page was successfully scanned, and 59 reproduce one whose first page yielded no text. Thus readable first-page coverage extends to 13,787 Documents paths and all 733 Desktop paths: **14,520 paths total**. **100 Documents paths (41 distinct byte hashes)** yielded no first-page text; **eight further distinct files** failed text extraction. Their derived path/hash/status records identify the exact unresolved extraction scope. The 98 entries without a PDF signature are separately listed by path/size/status. No unrelated raw text or failed-parser output was saved.

An empty first-page extraction is not absence evidence for a title rendered as an image, a textless first page, or other extraction failure. A successful no-match first-page scan likewise does not exclude a manuscript whose identifying title begins later. These limits are retained rather than converted into a complete-article absence claim.

## Matching candidates and source identity

The only two matching unique PDFs are already known sources, at their original project-local paths:

| Original path | Match / identity | Bytes / pages | SHA-256 |
|---|---|---|---|
| `sources/roydor/roydor_slides.pdf` | Target talk title and Jean Roydor; CIRM October 2020 Beamer slides | 459,832 / 87 | `b9202a2b4b3b50efc84a3430c593823f8c15404e83a2987be80083dc9028c36a` |
| `sources/roydor/ricard_roydor_1108.1970v2.pdf` | Jean Roydor; older Ricard–Roydor *A noncommutative Amir–Cambern theorem for von Neumann algebras and nuclear C*-algebras*, arXiv:1108.1970v2, 24 June 2013 | 193,449 / 11 | `36eb3ae3204ff33c1e44f785358d743bbaf53b5671438e7e1a9a4fff66fb8a14` |

Their complete first-page title/author/version and page counts were already checked in the immediately preceding local discovery report; the present independent header detector reproduced their hashes and identities. They are excluded as the target manuscript because their actual titles/formats/versions identify slides and a different earlier paper, not because they fail a 26-page condition. No new candidate required copying or a complete-manuscript audit.

## Preserved evidence and exact remaining gap

Only derived metadata was written under the project's ignored `sources/archival/` folder: `local_pdf_header_inventory_20261007.json`, `local_pdf_header_paths_20261007.json`, `documents_pdf_header_scan_20261007.json`, `documents_pdf_header_signature_classification_20261007.json`, and `desktop_pdf_header_scan_20261007.json`. Existing `.gitignore` excludes all these local verification records. No complete target article bytes/version/hash were obtained, and no third-party source was added to a publication payload.

The source gate remains unchanged: obtain an authorized complete journal article or complete author manuscript, then read and audit its exact theorem/cochain/field conventions, general/nonseparable scope, canonical-predual argument, and type-I reduction. Neither an absent local title match nor the already obtained author slides closes that requirement. This route performed no external access, download, purchase, authentication, outreach, Git action, manuscript edit, frozen-review edit, prior-access-report change, or other-project mutation.
