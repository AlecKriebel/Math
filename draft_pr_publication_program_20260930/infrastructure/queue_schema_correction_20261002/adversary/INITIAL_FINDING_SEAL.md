# Initial independent schema finding

UTC: 2026-10-02T02:31:28.089410+00:00. Audit completion estimate: 25%.

I inspected the literal queue header and all 21 completed primary PR rows (9–17, 19, 21–31), plus the shared PR22 duplicate, from immutable main commit `cab3546c2`, before reading root postmerge receipts, root reconstruction reports, mirror implementations or a proposed correction. The two initial JSON inspections contain all 22 full accepted records, read under names taken from the literal header.

The header has 12 columns. Its last six logical columns are Proposed, Status, Turns, Chat, Findings, DOI. With a leading empty pipe split, Chat is split index 10 and Findings is split index 11. With leading/trailing empties removed, Chat is logical index 9 and Findings index 10. These indexing conventions must not be mixed.

Confirmed defect: all eight accepted PR rows 24–31 currently place their accepted-result prose in Chat and leave Findings empty. IDs: 10000062, 2800102, 10400115, 30003713, 7000019, 30004186, 30003955, 10000043. Every inspected row is structurally 12 cells (14 raw split parts); a shape-only check does not detect this semantic error. The other 13 accepted primary rows and the PR22 duplicate have their acceptance prose in Findings and Chat empty. The DOI fields for PR9 and PR16 contain the expected distinct published DOI links. No conclusion about the unchanged science or mirror state has yet been drawn.

Bounded candidate repair hypothesis: for these eight rows only, move the complete existing Chat text unchanged to Findings, then restore the genuine preserved Chat field only if prior main/source records establish its contents. A blank presumed Chat is not enough without that comparison. Keep Status, Turns, DOI and every other field unchanged; keep all other rows byte-for-byte unchanged. An existing empty Findings field should be required as a precondition, rather than silently overwritten. Historical receipts claiming that split index 10 is Findings require an additive correction notice, not destructive edits.

This initial finding concerns queue metadata. It neither invalidates nor re-certifies any accepted mathematics, universal proof, publication, attempt ledger or preserved historical transcript.

Input hashes:
- `INITIAL_QUEUE_cab3546c2.md`: 376985 bytes, SHA256 `2a8afda44a3e9bc1c4d348fd40fd6c260d13d70950e1b5f17677372c628be980`.
- `INITIAL_ACCEPTED_ROWS.json`: 29223 bytes, SHA256 `51faca19fd0bc86e92f3f9744f2fbaab5727513a804bd0919f7cb1378f6793f0`.
