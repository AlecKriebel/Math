# Zenodo publication and tracker receipt

Published on 26 September 2026 using this repository's `zenodo_deposit_tool`.

- Paper: **Equality in the Fradelizi–Paouris–Schütt second-moment inequality**, Alec Kriebel, version 1.0.0.
- Assigned DOI: **10.5281/zenodo.22983138**.
- Public record: [Zenodo 22983138](https://zenodo.org/records/22983138).
- Original preprint date **2026-09-23** retained exactly; publication action **2026-09-26**.
- Tracker: [Math Puzzles, row 6](https://docs.google.com/spreadsheets/d/1ZljUv5Q98jNXLoHK8WjwrkzSm3dhHC1-7LElcOU7y20/edit?gid=1254632077#gid=1254632077&range=A6:D6).

Every supplied metadata field equals the original kit metadata. The three
specified files were uploaded separately: `paper.pdf`,
`source-and-verification.zip`, and `SHA256SUMS`. The outer upload kit was not
deposited. Anonymous public downloads of all three files were compared byte
for byte with the local kit. The tool verified the remote metadata, file set,
sizes, and checksums before and after publication.

The Google Workspace CLI appended exactly one row to the explicitly selected
tab, after checking for the original-problem URL and DOI. An independent
read-back matches the requested row. The Solution Chat URL cell is blank:
no portable shared chat URL was supplied, and no sharing link was created.

The original manuscript, metadata, kit, archives, and frozen source manifest
remain unchanged. These receipts supersede the historical pre-deposit
statements inside that immutable snapshot. Publication evidence and the two
user-requested drafts are stored separately here. No GitHub release, journal
submission, UnsolvedMath comment, or email was sent or created externally.

## Evidence and reuse

- `../zenodo-deposit.json`: original metadata plus the three upload paths.
- `stage-receipt.json` and `inspect-draft-receipt.json`: staged record and independent pre-publication inspection.
- `publish-receipt.json` and `inspect-published-receipt.json`: confirmed publication and read-only follow-up, including DOI-resolution status.
- `public-record.json` and `public-record-verification.json`: anonymous record metadata and byte-for-byte file verification.
- `tracker-row-request.json`, `tracker-append-response.json`, and `tracker-readback.json`: exact tracker write and verified destination.
- `unsolvedmath-comment.md` and `notification-email.md`: unsent drafts requested by the user.

Publication and DOI resolution are distinct checks. Zenodo has confirmed the
published record and assigned the DOI. The latest observed resolver status is
in `inspect-published-receipt.json`; a 404 does not warrant another deposit or
publication request. The direct record URL works independently of DOI routing.

The installed Sheets append shortcut does not support its skill's advertised
tab selector, so the raw CLI method `sheets spreadsheets values append` was
used with range `'Math Puzzles'!A:D`, `RAW`, and `INSERT_ROWS`. The shared skill
prerequisite was generated locally because it was missing; those temporary
helper files were moved outside the repository and are not publication inputs.
