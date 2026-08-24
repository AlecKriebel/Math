# PDF build and visual-inspection report

Both submission documents were rebuilt from the final sources with Tectonic
0.16.9 on 22 August 2026.

| document | source SHA-256 | PDF SHA-256 | pages | bytes |
|---|---|---|---:|---:|
| main article | `1107e5395a0e2ad4da0333cda066ae587d9a9854e61aeba3d2aadcf62e23e45b` | `86b7ace41d025caddcecae2accb04c496a401501b2a6e65233ad60cfc80e3e2a` | 26 | 193,906 |
| reader supplement | `fcb9df1f2ac3d31354e7a67ccb94700f1b67c8ef13db985bef34e327c58d58de` | `177006b4d2a21d958f1811c3920bbbfca18fdff87cda8da99b97c9c950dd15cb` | 24 | 158,528 |

All 50 rendered pages were inspected, including the total-rank-drop argument,
the clarified replay/runtime boundary, and the dense formula, transport,
crosswalk, hash, and replay tables. No clipping or layout defect was found.
The logs contain no overfull boxes, undefined references, undefined citations,
fatal errors, or hyperref PDF-string warnings. `pdffonts` confirms that every
font is embedded. Clean five-file source builds passed. Clean-source builds
with either `compression_tables.tex` or `certificate_appendix.tex` omitted
failed at the corresponding unconditional input, as required. Tectonic can
tolerate a missing bibliography while emitting warnings, so the source
manifest and its omission mutation enforce `references.bib` independently.
The machine-readable record is `PDF_BUILD_REPORT.json`.
