# Zenodo publication and tracker record

Published on 26 September 2026: **A note on Γ-supercyclicity of dissipative composition operators**, Alec Kriebel, version 1.0.1.

- DOI: [10.5281/zenodo.22983147](https://doi.org/10.5281/zenodo.22983147)
- Public record: [Zenodo 22983147](https://zenodo.org/records/22983147)
- Website: [research-note page](https://aleckriebel.github.io/Math/papers/gamma-supercyclicity/)
- Tracker: [Math Puzzles, A8:D8](https://docs.google.com/spreadsheets/d/1ZljUv5Q98jNXLoHK8WjwrkzSm3dhHC1-7LElcOU7y20/edit?gid=1254632077#gid=1254632077&range=A8:D8)
- [DOI citation](CITATION.bib) and [user-requested notification drafts](notification-drafts.md).

The supplied metadata exactly matches `../zenodo/metadata.json` and both metadata representations in the existing upload kit. The metadata publication date remains **23 September 2026**, as requested. The Zenodo API stores the description’s less-than signs as HTML entities; their rendered meaning is unchanged. No title, author, attribution, version, date, license, keyword, related identifier, or note was altered. The original PDF, source archive, and upload kit were not rebuilt. Historical upload instructions inside that frozen kit describe its pre-deposition state; do not use them to create a duplicate record.

## Verification

[Publication receipt](publish-receipt.json) confirms the submitted record after one publication request. [Read-only inspection](inspect-published-receipt.json) separately records the latest DOI resolver status; the resolver initially returned HTTP 404 even though the public record and downloads were available. The subsequent read-only check confirmed HTTP 200 resolution to the public record. Resolver propagation required no additional publication request.

[Anonymous public verification](public-record-verification.json) confirms both files match the reviewed kit byte for byte:

| File | Bytes | SHA-256 |
| --- | ---: | --- |
| paper.pdf | 80260 | `671cf6be89c45cbda49c207c2a656064958494fce60f05619d63a3061ee123c7` |
| note-source.zip | 8464 | `7ef22e4bdf8a34289384f25d2fb481d76059910b9caf21b6d1d8ff92c4d47385` |

The original upload-kit ZIP remains SHA-256 `838ed43c0f91a402e608a72421b7564288ed9a2b1d1bb15881c61af9b8001e22`.

## Tool feedback and recovery

The first stage saved draft 22983147 and uploaded its two files, but verification stopped at the HTML-encoded description. [The initial diagnostic](draft-inspection.json) records the only metadata difference. The shared Zenodo tool now accepts only exact entity encoding of plain text without existing HTML tags or character references. It still rejects substantive changes and preserves exact equality for unchanged HTML. No draft was recreated; [inspection](inspect-draft-receipt.json) recovered the existing draft before publication.

An independent adversarial artifact review confirmed metadata/file/tracker consistency and identified a generic double-encoding edge case in the initial tool adjustment. The correction adds a pre-existing-entity guard and named/numeric entity regression cases. All 25 offline tests pass, and a fresh second adversarial reviewer found no actionable issues in the final change; see [review evidence](adversarial-review.md). These checks concern deposit integrity and the uploader; the manuscript remains the previously reviewed version 1.0.1.

## Sheet entry and authorization

The user explicitly authorized Zenodo publication and a Google Workspace CLI append. The CLI checked the requested tab’s headers and found no matching problem/DOI row, previewed the exact request, appended once to `'Math Puzzles'!A8:D8`, and independently read back all four values. [Request](tracker-row-request.json), [append response](tracker-append-response.json), and [read-back](tracker-readback.json) are retained. The solution-chat cell is blank because no share URL was provided. No other tracker rows are included in these receipts.

No email or public comment was sent. The notification texts are drafts for the human user. No GitHub release was created, avoiding a second automatic Zenodo deposit. Credentials and private resumable tool state remain outside these publication materials.
