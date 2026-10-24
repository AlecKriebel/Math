# Acquisition validation checkpoint

Timestamp: 2026-10-24 10:31 America/Los_Angeles. Estimated completion of complete source acquisition: 85%; the direct-record corpus is complete, and a supplemental archive audit is in progress.

## Strongest verified result

The authenticated, read-only owned-account listing was paginated with `all_versions=true` through three pages of 100, 100, and 26 records. All 226 IDs are distinct. The public scholarly fields, public file inventories, and page response hashes are preserved in `sources/corpus_account_public.json`. No ownership details, credentials, or bucket write links were persisted.

The direct-manuscript filter yields 202 published manuscript version records, 201 Zenodo concepts, and 211 standalone PDF files. Every PDF was matched to an exact local copy by its advertised Zenodo MD5, then independently hashed with SHA256 and fully extracted page by page. There are no acquisition errors. Each PDF is bound to its precise local file, original public filename, page count, text count, file hashes, and extraction hash in `sources/corpus_records.json`.

This count is **not yet the final count of all authored papers on Zenodo**. Some excluded software records are whole-repository releases and contain additional manuscripts. That gap is being addressed in `sources/archive_papers.json`; the original direct-record corpus has not been silently changed.

## Authorship and manuscript checks

All 202 direct manuscript records list exactly one creator, `Kriebel, Alec`, with ORCID `0009-0001-9320-500X`. There are no coauthor or other-author exceptions among these records. All 211 PDF first pages contain Alec Kriebel's name. The smallest complete extracted PDF text contains 5,758 characters; there are no blank or image-only PDFs in this set. The nine additional PDF files are companion/supplement manuscripts, rather than extra independently scored main works.

The direct-record corpus does not contain any record represented solely by a supporting archive, integrity manifest, or code package. The source-only Bell deposit 21699181 is separately classified, and the 21753316 continuum draft is unpublished and empty. Their status must not erase published manuscripts inside other records.

## Version and duplication checks

* 21971507 and 22013710 share concept 21971506; 22013710 is the current direct-manuscript edition.
* 21699069 and 21699161 are distinct Zenodo concepts bearing the identical title *Minimum Bell-Setting Complexity for Qubit POVM–PVM Separation*. They are presentation variants (review/line-numbered and standard PDFs) of the same scientific work; keep both deposits in the inventory and avoid counting their scientific contribution twice.
* Exhaustive title-similarity comparison among all 202 records found no other identical or near-identical title pair suggesting a hidden edition beyond the above. Other close title pairs distinguish different billiard constructions (focal versus center pedal, inner versus outer, original-side versus outer-area) or different phylogenetic models. This is a duplication screen, not a proof that no theorem overlap exists.

## Existing spreadsheet DOI reconciliation

The saved pre-edit spreadsheet snapshot supplies 13 primary DOI references in `Papers` and 207 in `Math Puzzles` (220 rows total). `Papers` has 12 direct manuscript DOIs plus the owned Yang–Baxter concept DOI 21971506, which maps to 21971507/22013710. `Math Puzzles` has 186 owned manuscript DOIs and 21 primary DOI references outside the owned account.

Every one of those 21 outside-account references was independently read through the public Zenodo record API. Their published creator metadata lists 18 records by Alper Ferudun, one by Wouter van Doorn, and two by Anonymous. None lists Alec Kriebel or his ORCID. The sheet's explanatory notes credit these as external/public existing results rather than Kriebel-authored papers. They must not be attributed to Alec in the inventory. The evidence and exact row mappings are in `sources/corpus_sheet_validation.json`.

Searching all text in the sheet yields more external record and concept DOI citations than searching the primary DOI cells. Those citations are bibliographic context, not missing owned deposits. The primary DOI reconciliation above uses the actual DOI columns, rather than treating every DOI in a research note as an authored paper.

## Exact remaining gap

All 24 provisional exclusions are being audited semantically. Published archive 21753405 contains *No universal death–birth amplifier*, a distinct paper missing from the direct-record filter. Published 21753527/21753997 are two editions of *A reversible three-species mass-action continuum without a common factor*, also absent from the direct-record filter. Whole-repository archives also carry earlier research PDFs, duplicate presentation files, external literature, and intermediate versions. A complete inventory must distinguish these instead of assuming that `upload_type=software` excludes all scientific manuscripts.

The archive method uses public HTTPS byte ranges to inspect ZIP central directories and acquire selected exact PDF members. Each extracted member is checked against its ZIP CRC32 and size and given MD5 and SHA256 hashes. The whole archive MD5 is recorded as advertised by Zenodo; it is not represented as locally recomputed unless the full archive is downloaded. This distinction is recorded explicitly in the supplemental JSON.


## Final source-validation checkpoint

Timestamp: 24 October 2026, 10:42 America/Los_Angeles. Completion of source acquisition and coverage validation: **100%**. The earlier provisional gap is closed. All 226 owned records, all 211 direct manuscript PDFs, all 276 distinct PDF payloads within the 20 excluded ZIPs, and both source tarballs have explicit source/coverage dispositions. The canonical supplement has 42 document candidates, of which 40 have verified Zenodo archive payloads and two remain repository-only; no unidentified manuscript family remains. The independent follow-up details are in `reviews/archive_coverage_independent.md` and its per-payload JSON. Public author/ORCID discovery exactly recovers all 225 published owned records, with no additional unowned authored/coauthored record. Scientific validity and editorial assessment remain separate from this completed acquisition task.
