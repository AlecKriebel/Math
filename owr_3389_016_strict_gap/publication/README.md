# Zenodo publication and tracker record

Completed public deposition and tracker update on 26 September 2026. Requested publication/tracking/drafting work: **100% complete**, with repository checkpoint below.

- Paper: **Nonattainment in the Harrell–Stubbe Dirichlet gap inequality**, Alec Kriebel, version **1.0.1**.
- DOI: [10.5281/zenodo.22983513](https://doi.org/10.5281/zenodo.22983513). Resolver verified HTTP 200.
- Public record: [Zenodo 22983513](https://zenodo.org/records/22983513).
- Preprint date in the supplied metadata: **2026-09-23**, retained exactly. Zenodo publication action: **2026-09-26**.
- [Tracker row 10](https://docs.google.com/spreadsheets/d/1ZljUv5Q98jNXLoHK8WjwrkzSm3dhHC1-7LElcOU7y20/edit?gid=1254632077#gid=1254632077&range=A10:D10): original problem link, DOI, and paper details; a separate readback matches the appended row exactly.
- Queue target `30001163 / OWR-3389-016`: `preprint_published`, with DOI `10.5281/zenodo.22983513`. Prior findings and turn count are preserved.

## Exact submitted inputs and remote normalization

The stable [deposit manifest](../zenodo-deposit.json) copies every metadata field from the version 1.0.1 upload kit unchanged. The three uploaded files are precisely the kit's `paper.pdf`, `source-and-verification.zip`, and optional `SHA256SUMS.txt`. They were uploaded separately rather than hiding the paper inside the outer kit. Public unauthenticated downloads of all three files match the kit byte-for-byte.

Zenodo itself changes exactly two U+2019 curly apostrophes to ASCII apostrophes in the description: “Yang’s” and “report’s”. No other submitted metadata field differs. This distinction is explicit: the submitted metadata is exactly the original kit metadata; the remote description is semantically identical but not byte-identical because of server punctuation normalization. Full local/remote values are preserved in `stage-metadata-normalization.json`.

The first stage call stopped at this mismatch after saving draft ID 22983513 and uploading the files. No second draft was created. The repository tool was repaired to accept only that exact apostrophe transformation for descriptions consisting of plain paragraph-only HTML, and to report any accepted normalization. Regression tests reject changed text/numbers, HTML tag or attribute changes, other punctuation, partial apostrophe normalization, and changes in other metadata fields. All **27 offline tests** pass. Read-only inspection then cleared the existing draft; one publication command succeeded. Post-publication inspection confirmed the record, metadata, files, and DOI resolution.

## Frozen publication payload

The original manuscript, PDF, metadata, archives, website snapshot, and source manifest were not rebuilt or changed. Their pre-deposit “no DOI” language is a historical status of that prepared kit, superseded by this publication receipt. These new administrative records remain outside the immutable deposited source package. No new GitHub release or subsequent Zenodo version was created.

## Unsent notification drafts

- Website comment: drafted for the user to post to the problem page; supplied in the task, not posted.
- Email: drafted for **Evans M. Harrell II**, one of the named proposers with Joachim Stubbe in the original report. His [official Georgia Tech profile](https://math.gatech.edu/people/evans-harrell) lists `harrell@math.gatech.edu`; verified September 26, 2026. The email is a notification framed as “if you’re interested,” with no request for review or response.

The user's explicit current request authorizes preparation of these drafts. Neither was sent or posted; no person was contacted. Draft text is kept in ignored local scratch storage and delivered to the user, rather than published as part of these administrative receipts. The Solution Chat URL spreadsheet cell remains blank in line with the surrounding rows; no public conversation link was created.

## Checkable receipts

- `stage-metadata-normalization.json`: saved draft identity and exact local/remote metadata comparison.
- `inspect-draft-receipt.json`, `publish-receipt.json`, `inspect-published-receipt.json`: validated draft, publication, and post-publication inspection.
- `public-record-verification.json`: public metadata, download URLs, sizes, and matching SHA-256 hashes.
- `tracker-row-request.json`, `tracker-dry-run.json`, `tracker-append-response.json`, `tracker-readback.json`: exact row content, inspected request, append result, and independent readback.
- `tool-regression-tests.txt`: 27 passing offline tool tests.
- `RESEARCH_LOG.md`: timestamped checkpoints and completion estimates.

Record checked at 2026-09-26T22:11:43Z.
