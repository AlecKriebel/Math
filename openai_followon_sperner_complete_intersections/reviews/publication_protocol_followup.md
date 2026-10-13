# Candidate-v3 operational binding follow-up

Timestamp: 2026-10-07 06:02:22 UTC. Narrow follow-up completion: 100%.
The mathematical full-package review remains separate and pending; its verdicts
were not read. No publication, tracker, credential, or external-communication
operation was performed. The only authored artifact is this report.

Inspected latest helper SHA-256:
`4fdfd5890690df76c14cf714ccb8b76a41d85e003c09aaef93ffe48a1362b0a1`.
Replacing only its `candidate_v3.json` string with `candidate_v2.json` reproduces
the previously audited helper hash
`90ccde6a04afcec7cba038072e21098ea80a43b7d4ddbbb1893098a6ec9f819e`.
Thus the helper's sole change since that audit is its frozen receipt binding.

The helper reads `receipts/candidate_v3.json`, whose SHA-256 is
`0be25f186e34656bb486b5b8e80c9c8befb5fa832c6358884a593ac889da439f`.
The actual manifest SHA-256 and receipt's `manifest_sha256` both equal
`803ec40cf0aa3e25b567c3a6bdd343104344372f6fe6f9f21c5e17aad88185ac`.
The actual manifest title is exactly **The Sperner property of standard graded
Artinian complete intersections in characteristic zero**. The helper derives the
tracker title from that manifest and explicitly requires the published-inspect
receipt title to match it.

All three actual manifest payload files agree exactly with candidate-v3 receipt
names, byte counts and SHA-256 values:

| Name | Bytes | SHA-256 |
| --- | ---: | --- |
| paper.pdf | 73479 | ae0526dfe7442b63e9c3f4754c324970b0d4e8ccd15d85b6f9585ed3ee45a119 |
| source.zip | 9840 | 6a1ce33589e9811d253e2b2b094d00236cd5dca9925383d8694fbae26c629272 |
| verification.zip | 65205 | 367e1a3e0b3a214cf8dcec3d13c64ae0db8031c00b7183904cde8e3fd3cbd6ae |

AST inspection confirms zero assertion statements. Publication state,
production environment, DOI/record ID, title, manifest hash, receipt payload,
local files, numeric tab uniqueness, headers, duplicate reconciliation, append
dimensions and exact readback retain explicit `require` exception gates.

In-memory execution with Python optimization enabled accepted a fabricated valid
v3 publication through the local gates, intercepting its first API call before
any network action. Fabricated draft, sandbox, old-title and wrong-payload
receipts were each rejected before that point. There were no real API calls or
receipt writes. Candidate files were only read.

No concrete repair is required for this helper revision. After the separate
final review gate, save a fresh repository Zenodo check for candidate v3 before
staging. The unchanged sequential-workflow and ambiguous-result reconciliation
limits from `publication_protocol_check.md` still apply. This follow-up does not
certify mathematical correctness or claim that publication/tracking occurred.
