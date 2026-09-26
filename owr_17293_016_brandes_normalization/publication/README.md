# Published record and workflow feedback

Completed upload and tracker entry on 26 September 2026. Requested upload/tracker actions: **100% complete**. DOI resolver activation is separately checked in `doi-resolution.json`.

- Paper: **A coefficient normalization for positive definite forms**, Alec Kriebel, version 1.0.
- Assigned DOI: **10.5281/zenodo.22982894**.
- Working public record: [Zenodo 22982894](https://zenodo.org/records/22982894).
- Preprint publication date in the original metadata: **2026-09-23** (retained exactly). Zenodo publication action: **2026-09-26**.
- Tracker: [Math Puzzles, row 5](https://docs.google.com/spreadsheets/d/1ZljUv5Q98jNXLoHK8WjwrkzSm3dhHC1-7LElcOU7y20/edit?gid=1254632077#gid=1254632077&range=A5:D5).

The repository's `zenodo_deposit_tool` performed stage, inspect, publish, and post-publication inspect. Every supplied metadata value equals the original kit metadata. The two files named in the kit were uploaded separately: `paper.pdf` and `source-and-verification.zip`. The outer upload kit was not deposited. Both published files were downloaded without authentication and compared byte-for-byte with the local kit.

The Google Workspace CLI appended exactly one row after checking for an existing problem URL or DOI, then independently read it back. It contains the original-problem link, DOI and paper details. The Solution Chat URL cell is blank, following the existing rows: no portable shared conversation URL was supplied, and no conversation-sharing link was created.

## Issues encountered and lessons for repeat use

1. **Zenodo requests without a User-Agent received HTTP 403.** The response was an HTML traffic-filter page, not a JSON credential error. A controlled authenticated read with the same credentials succeeded when it included the truthful `Math-Zenodo-Deposit-Tool/1.0` identity. That header was added to the reusable tool and covered by a regression assertion; all five offline tests pass. The first rejected request saved no draft. Staging, publication, and verification then succeeded. No token or metadata changes were needed. Zenodo's [15 September 2026 service update](https://blog.zenodo.org/2026/09/15/2026-09-15-stability-and-performance-updates/) also requests a clear client identity for automated applications.
2. **The installed Google Workspace append shortcut lacks its documented tab selector.** Its skill lists `--range`, but `gws 0.22.5 sheets +append --help` does not. Using `gws sheets spreadsheets values append` with the explicit range `'Math Puzzles'!A:D`, `RAW`, and `INSERT_ROWS` targeted the correct tab. The CLI's schema and a dry run were checked first.
3. **CLI skill setup has a side effect.** The local Sheets skill's shared prerequisite was missing. Calling `gws generate-skills --help` generated files instead of displaying help. Those generated files were moved out of repository publication paths into the effort's ignored temporary directory. For future setup, run skill generation in a temporary directory and consult the installed command help/schema before writes.
4. **Publication and DOI resolution need separate checks.** Zenodo reported the record as published and exposed its public record, files, and assigned DOI. The first DOI resolver and DataCite lookups nevertheless returned 404. Registration delay is a possible explanation, not a verified diagnosis or promised activation time. The final observed status is in `doi-resolution.json`; use the direct public record link if the DOI has not activated. Do not repeat publication or create another deposit in response to resolver lag.

For future deposits, retain a stable manifest path and the ignored local draft-state file; inspect after staging; publish only once with the returned draft ID; save the publication receipt immediately; confirm the public files and DOI resolution separately; then append to the explicitly selected tracker tab after a duplicate check. An HTML 403 should be distinguished from a JSON authorization error. The current tool's generic error message obscured that distinction; richer safe error diagnostics would be a useful future improvement.

## Receipt files

- `../zenodo-deposit.json`: exact kit metadata plus the two upload paths.
- `stage-receipt.json` and `inspect-draft-receipt.json`: staged draft and independent pre-publication check.
- `publish-receipt.json` and `inspect-published-receipt.json`: successful publication and post-publication inspection.
- `public-record-verification.json`: public metadata, file hashes, and download URLs.
- `doi-resolution.json`: observed DOI and public-record availability.
- `tracker-row-request.json`, `tracker-append-response.json`, and `tracker-readback.json`: exact row and verified destination.

The original paper, kit metadata, archives, and frozen source manifest were not rebuilt or changed. This publication receipt supersedes the historical “no DOI created” status in the pre-deposit kit. These new receipt files remain outside that immutable upload snapshot. No GitHub release, journal submission, or communication with another individual was performed.
