# Final publication and tracker receipt audit

**PASS — no concrete discrepancy found in this bounded audit.** Independently checked on 2026-10-07 UTC. The exact completion timestamp, HTTP receipts, comparison results and input hashes are retained in [AUDIT_RESULT.json](final_receipt_audit/AUDIT_RESULT.json).

Audit completion estimate: 100%. Publication/tracker receipt-verification estimate: 100%. Mathematical resolution was not re-estimated: the previously recorded 100% status remains outside this receipt audit's scope. These estimates are workflow status, not proof probabilities.

## Scope

Read `/Users/alec/Documents/Math/AGENTS.md` and the complete original `research/USER_REQUEST.txt`. This is a bounded receipt/custody audit, not a fresh mathematical, dependency, literature or reproduction review. No credential file or environment value was read or displayed. The only outside operations were public Zenodo/DOI GETs and read-only Google Workspace calls restricted to the own-row range. No other tracker rows were read, no sheet write occurred, no individual was contacted, and no Git, upstream, frozen candidate or publication state was changed. All audit writes are in `reviews/final_receipt_audit/` and this report.

An internal subagent independently crosschecked the saved local metadata and publication/tracker receipts. Its scoped PASS and evidentiary caution are retained in [LOCAL_SECOND_PASS.md](final_receipt_audit/LOCAL_SECOND_PASS.md).

## Frozen v5 identity and custody

Current bytes of all five entries in reviewer05's `V5_CUSTODY_SEAL.json` match its SHA-256 and size. The seal itself hashes to `c3e718fbedd414f4ff6af2b8efd045cfe459d22d3a8a13f610d80c05fcb07855`, matching reviewer delivery and root release approval. The complete reviewer05 report hashes to `3abfa0a8f438eb34512a27816ac8ed90ec4d016bda689f217b6df65484dd17b7`, matching delivery and approval. Candidate identity hashes to `348fe001e2d79d3734e07eb9a9ed1904e3eea5304713a4776f8d14b80ef8b388`.

Manifest SHA-256 remains `2fe834bdf2e5de74a92f7b9463fdc6917717c7e37ccf7ca58c9670065f3efa7d` (2,971 bytes). All 28 current authored payload hashes match the candidate identity. ZIP CRC passes, its 29-member set has no repeated names and exactly matches the sealed set, and every member hash/size matches the seal. ZIP copies of the 28 authored files match current authored bytes. No compilation or finite mathematical test was rerun here.

## Live public publication, files and metadata

Fresh unauthenticated GET of [the public record API](https://zenodo.org/api/records/23205294) returned HTTP **200**, record ID **23205294**, DOI **10.5281/zenodo.23205294**, and exactly the intended three files. Each file was freshly downloaded from its public API content link. The downloaded bytes exactly equal the current upload files, reviewed v5 hashes and saved public-download receipt; public API MD5 and lengths also agree.

| File | Bytes | SHA-256 |
|---|---:|---|
| README.md | 6,238 | `a272e4bc9b525d60a9adfe3ba3a113e8c46c53f246ccd01f16b77eb8958cc1cd` |
| paper.pdf | 75,751 | `8c93b0f14bc4fd935dbc3a489c5ecca63a8262ba4560a09822b7f65e1036bee7` |
| source-and-verification.zip | 183,748 | `e79ba53de7b0d937189271d5941ee77eb8e1f10212fef33aa3bb4c4311c666fa` |

Every manifest-supplied metadata field matches both saved deposition snapshots and the live public record: title; publication/preprint resource type; Alec Kriebel and ORCID; complete description; date `2026-10-06`; open access; `cc-by-4.0`; version `1.0.0`; ordered keywords; and related identifiers. The public API represents license by an object `id` and publication/preprint by resource type/subtype. The only creator normalization is the documented addition of omitted `affiliation: null`. No fabricated affiliation or extra creator appears.

Fresh GET of [the DOI](https://doi.org/10.5281/zenodo.23205294) returned HTTP **200** and resolved to [the same public record](https://zenodo.org/records/23205294). This independently confirms both saved tool DOI-resolution receipts, which also report 200. Raw public record JSON, audit download copies and status/URL/hash receipts are retained in the audit folder. The web preview could not open these exact endpoints; direct public GETs succeeded without credentials.

## Observable publication gates

The saved `check → stage → inspect draft → publish → inspect published` receipts use production and identical reviewed title and upload hash/size records. Stage and draft inspection identify **23205294** in `ready_to_publish` state. The draft snapshot states `submitted: false` and reserves the same DOI; the published snapshot states `submitted: true` and assigns it.

Root release approval at `06:41:48.906129 UTC` links the exact complete review report and seal and records no substantive concern. Remote draft verification at `06:42:26.803230 UTC` precedes prepublish clearance at `06:42:48.569243 UTC`. That clearance identifies `--confirm-id 23205294`, unchanged reviewed bytes and matching remote metadata/files. Publication verification follows at `06:42:51.161286 UTC`, then inspection at `06:43:02.862249 UTC`. These records are consistent with the explicitly authorized gates and same-ID publication.

Current repository help requires `--confirm-id`; the saved read-only source excerpt shows a mismatched confirmation ID is rejected, metadata/files are verified before the POST, publication is read back on the same ID, and the tool does not automatically repeat a publication POST. No contradictory ID, sandbox deposit or extra upload appears in the scoped receipts. Current interface captures and tool hash are in [CURRENT_INTERFACE_CHECKS.json](final_receipt_audit/CURRENT_INTERFACE_CHECKS.json).

**Historical evidence limit:** several command receipts omit argv and timestamps. They establish internal consistency and compatible annotated chronology, not an independently immutable transcript of exact invocation or result inspection after each separate command. The current guard supports the confirmation mechanism but cannot independently authenticate the tool version/argv executed earlier. Mathematical, priority and review clearance is checked here through unchanged sealed records, not re-proved.

## Exact tracker entry

The installed Google Sheets read instructions and current `values.get` schema were read before the live own-row GET. The current `values.append` schema also confirms `RAW` and `INSERT_ROWS` are valid. Current CLI version is `gws 0.22.5`. The shared prerequisite skill is absent locally; it was not generated because the original user request expressly forbids skill-generation commands in the research checkout.

Saved numeric-ID resolution maps spreadsheet `1ZljUv5Q98jNXLoHK8WjwrkzSm3dhHC1-7LElcOU7y20`, tab **1254632077**, to **Math Puzzles**. The recorded schema is `Original Problem`, `Solution Chat URL`, `DOI`, `Notes`. Request, dry-run body/flags, append response, stored readback and verification agree exactly. Saved execution records **one append attempt**; response records **one row/four cells** at **`'Math Puzzles'!A53:D53`**, with **RAW** and **INSERT_ROWS**. Column C contains the published DOI URL and column B is intentionally blank.

Independent live GET was restricted to **`'Math Puzzles'!A53:D53`**, using `UNFORMATTED_VALUE`. The entire response, including the four complete cell values, exactly equals the stored readback, requested row, append response values and final verification. The exact live response is retained in [tracker_exact_row_live.json](final_receipt_audit/tracker_exact_row_live.json). Recorded tracker timestamps follow confirmed publication. [Open the tracker row](https://docs.google.com/spreadsheets/d/1ZljUv5Q98jNXLoHK8WjwrkzSm3dhHC1-7LElcOU7y20/edit?gid=1254632077#range=A53:D53).

**Duplicate/history evidence limit:** the saved preappend scan reports no DOI/deposit-ID/title duplicate and final verification reports DOI occurrence only at row 53. Execution and verification both record one append. This auditor did not read other tracker rows or repeat a full duplicate scan; current global duplicate absence and preservation of unrelated rows rely on those retained receipts. Own-row correctness is independently live-verified.

No repair is required by this bounded audit.
