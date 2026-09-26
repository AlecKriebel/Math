# Zenodo publication and tracker receipt

26 September 2026. Publication and tracking actions: **100% complete**.

- Published preprint: **Radial orthogonality does not imply dual 1-conformal flatness**, Alec Kriebel, v1.0.1.
- DOI: [10.5281/zenodo.22983519](https://doi.org/10.5281/zenodo.22983519).
- Public record: [Zenodo 22983519](https://zenodo.org/records/22983519).
- Original metadata publication date and actual deposit publication date: **2026-09-26**.
- Spreadsheet: [Math Puzzles, row 9](https://docs.google.com/spreadsheets/d/1ZljUv5Q98jNXLoHK8WjwrkzSm3dhHC1-7LElcOU7y20/edit?gid=1254632077#gid=1254632077&range=A9:D9).
- Queue: problem **6000011 / AMR-059-0011**, status **preprint_published**, DOI recorded. Historical priority remains unresolved.

The repository's `zenodo_deposit_tool` staged, inspected, published, and then
re-inspected the deposit. Every supplied metadata value is identical to the
original v1.0.1 kit. All three specified files were uploaded separately:
`paper.pdf`, `source-and-verification.zip`, and `SHA256SUMS.txt`. The outer kit
was not deposited. All three public, unauthenticated downloads were compared
byte-for-byte with their originals. The DOI resolved with HTTP 200 to the
published record at the publication check and subsequent inspection.

The Google Workspace CLI targeted the tab with sheet ID 1254632077 after
checking its name and headers. A full used-range duplicate check found no row
for this problem or DOI. Exactly one row was appended, and an independent
read-back matched all four cells. The Solution Chat URL field is blank, as in
the existing rows; no conversation sharing link was created.

The user explicitly requested `preprint_published` and a DOI in QUEUE.md. Its
current table has manually maintained Chat/Findings/DOI columns absent from
the legacy generator, whose allowed states also omit `preprint_published`.
Accordingly only the requested row was changed, preserving its original
findings, chat link, and 1/5 proof-turn count. No new proof attempt was recorded,
no queue was reranked, and no historical review was overwritten.

## Exact snapshot and later publication records

The deposited PDF, source archive, checksum payload, original kit metadata,
and outer kit remain unchanged. Historical statements in that prepared kit
about having no assigned DOI refer to the pre-deposit snapshot. This publication
receipt supplies the later DOI and supersedes those historical status statements.
Current repository citation and website notices may include the DOI without
changing the immutable deposit. Their working-tree manifest is separate from
the archived source's internal manifest. Reproduce the deposited package from
the deposited source archive; do not rebuild it from later edited working-tree
materials expecting the same bytes.

The two notification drafts were prepared only because the user explicitly
requested them; neither was sent or posted. Recipient identification uses the
original problem attribution and the supplied 2024 paper's professional contact
information. See [notification-drafts.md](notification-drafts.md).

No GitHub release or journal submission was created. All original priority and
AI-provenance disclosures are retained. The DOI provides a persistent identifier,
not a priority certificate, external human peer-review endorsement, or formal
proof verification.

## Receipts

- `../zenodo-deposit.json`: exact kit metadata and three upload paths.
- `local-check.json`, `stage-receipt.json`, `inspect-draft-receipt.json`: file identities and pre-publication checks.
- `publish-receipt.json`, `inspect-published-receipt.json`: confirmed publication and DOI resolution.
- `public-record-verification.json`: unauthenticated public file comparison.
- `tracker-row-request.json`, `tracker-duplicate-check.json`, `tracker-append-response.json`, `tracker-readback.json`: exact row and destination.
- `queue-update.json`: before/after row, status and DOI, with update rationale.
