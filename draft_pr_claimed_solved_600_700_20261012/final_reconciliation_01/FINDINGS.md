# Completed-seven read-only reconciliation

Initially completed 2026-10-15T06:12:11.986760+00:00. Preliminary subtask completion: 100%. The active PR #681 and the persistent program goal are outside this reconciliation.

All 81 checks pass, including three publication-scope checks. No mismatches, mandatory findings, optional findings or access failures were found. The collection made 41 successful external readbacks, using authenticated GitHub and Google Workspace read commands and anonymous production Zenodo/DOI GET requests. No cloud writes, Git commits, pushes, shared-checkout/index changes, mathematical reaudit or skipped-PR processing occurred.

PRs #615, #628, #630 and #672 remain closed without merge at their original immutable heads. Their closure timestamps, comment URLs and exact saved posted bodies match fresh GitHub readbacks byte for byte. PR #615 uses CLOSURE_COMMENT_SENT.md, the saved actual posted body, rather than the earlier candidate CLOSURE_COMMENT.md.

PRs #618, #623 and #662 remain merged at their saved accepted heads and exact merge commits. GitHub still resolves every original and accepted commit. Each actual merge has the accepted commit as a parent. Local immutable Git-object readbacks verify exact accepted/merged scoped inventories: 23 files for #618, 36 for #623, and 45 for #662 (24 original files plus 21 sibling publication files). The selected QUEUE.md row also matches accepted versus actual merge bytes in every case. PR #618's whole merge tree differs from its accepted tree because the merge includes concurrent main changes; its own scoped inventory and selected row are identical. The entire accepted and merge trees coincide for #623 and #662.

Each production Zenodo record is public, published, and has its exact saved DOI. All eleven user-supplied metadata fields match the accepted local deposit metadata after explicit legacy-to-native schema mapping: title, resource type, subtype, date, version, description, creator/ORCID/affiliation, access, license, keywords and related identifiers. Every accepted local publication pin checked remains valid. Each exact two-file public inventory agrees with its saved publication receipt. Six freshly downloaded PDF/ZIP files match both the local accepted bytes and receipt SHA-256, with sizes and Zenodo MD5 checksums verified. All three DOI URLs resolve to the exact saved production record with HTTP 200.

The tracker spreadsheet ID, gid 1254632077, Math Puzzles tab title and four-column header match. Read-only exact-range and full-column readbacks establish exact A:D row equality and normalized DOI uniqueness:

| PR | DOI | Exact row |
| --- | --- | --- |
| #618 | 10.5281/zenodo.23331709 | 'Math Puzzles'!A73:D73 |
| #623 | 10.5281/zenodo.23356540 | 'Math Puzzles'!A88:D88 |
| #662 | 10.5281/zenodo.23384924 | 'Math Puzzles'!A94:D94 |

RECONCILIATION_RESULT.json contains every check and its evidence summary. EXPECTED_COMPLETED_SEVEN.json binds the exact saved decisions and expected metadata. INPUT_BINDINGS.json records the local receipt/file hashes, all rechecked unchanged at analysis time. Individual response JSON files preserve fresh readbacks of our own records; IMMUTABLE_MERGE_SCOPE_CHECK files and paired scoped inventories preserve the Git-object checks. The full-column spreadsheet scan and all-tab metadata are retained byte for byte only under ignored tmp/tracker_all_A_D.json and tmp/tracker_metadata.json. Their publishable counterparts allowlist our exact three matching rows, DOI match counts/row numbers, the selected tab identity and private-cache hashes; no unrelated row contents or tab properties are retained publicly. INPUT_BINDINGS.json binds both private raw responses by hash. Downloaded public PDF/ZIP bytes and DOI HTML responses are also confined to ignored tmp/. collect_readbacks.py applies this separation automatically. analyze_readbacks.py rederives the scoped evidence from the private cache and evaluates the saved responses without new network operations. PRIVACY_OUTPUT_SCAN.json records the check that no unrelated full row or other-tab properties remain in public JSON artifacts.

These readbacks establish external-state consistency at their recorded UTC times. They do not reassess mathematics, strengthen earlier priority conclusions, certify human peer review, or complete the still-active overall program.

Publication-scope repair completed 2026-10-15T06:17:00.417699+00:00: both raw wide-sheet responses were moved into the ignored cache without deletion or byte changes. The offline rerun passes 81 checks with 0 mandatory and 0 optional findings. No new cloud calls were made during this repair. The earlier 78-check result is superseded by this privacy-scoped 81-check record.
