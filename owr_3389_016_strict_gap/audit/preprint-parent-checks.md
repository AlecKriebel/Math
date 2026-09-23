# Additional preprint-readiness checks

Opened 2026-09-23T13:35:45Z. Initial checkpoint: 45% of the new review-and-republication cycle.

## Baseline reproduction and visual inspection

The parent independently extracted the existing source archive to a new temporary location, checked all source-manifest hashes and ZIP paths/CRC, ran the verifier under Python optimization, compared deterministic results, and rebuilt both publication archives byte-for-byte. All 7,016 exact checks passed. The verifier and results match the published baseline.

All three PDF pages were freshly rendered at 110 dpi and inspected. Equations, references, page breaks, text, and numbering are legible, with no clipping or overlap.

## Actionable presentation findings

1. The standalone paper refers to an accompanying verification package but does not link it. Add a stable public package landing-page link in the provenance paragraph so readers can locate the audit and scripts from the PDF alone.
2. The PDF has no title or author metadata. Add these fields, plus a short subject and keywords, through the manuscript's hyperref settings.

These are discoverability and presentation repairs; neither changes the mathematical argument. The independent adversarial review is proceeding without relying on these parent findings. Final disposition and release checks will be appended after the independent rounds.

## 2026-09-23T13:40:37Z — Presentation repairs and PDF check — 60%

Both parent findings are repaired. The revised three-page PDF has populated title, author, subject, and keyword fields and a direct supporting-package hyperlink. All three freshly rendered pages were inspected with no layout defect. The mathematical argument is unchanged. Current manuscript hashes are recorded in PREPRINT_REVIEW.md.

## 2026-09-23T13:46:51Z — Revision consistency checks — 85%

The revised CITATION.cff passes the official versioned CFF 1.2.0 schema. Current README, website, citation metadata, and Zenodo upload fields consistently identify version 1.0.1. The verifier and deterministic results are unchanged. The inspected manuscript diff contains only PDF metadata, the version label, and the supporting-package hyperlink; there is no mathematical edit. Repository whitespace checks pass. Fresh round two reports no proof flaw after independent reconstruction and reproduction; its written report and final package/deployment checks remain pending.

## 2026-09-23T13:48:38Z — Final local release checks passed — 95%

The second fresh reviewer completed a clean review: preprint-ready, no actionable issues, and no requested revision. Both reviewed manuscript hashes remain unchanged. The parent incorporated both reports and the completed consolidated review, then checked the refreshed payload:

- Every source-manifest hash agrees with canonical and extracted files. ZIP CRC checks pass; paths are unique and relative.
- Extracted-package optimized verification reproduces all 7,016 checks and byte-identical results. Both source and Zenodo archives rebuild byte-for-byte.
- Kit PDF and nested source ZIP match the canonical payload; canonical, API-wrapped, and kit metadata agree.
- Current version identifiers and PDF title/author fields are correct. The official CFF schema check passed.
- Every local site link resolves; website checksums and dedicated deployment copies agree. Both new full reviews are in the source package.
- The theorem, proof, citations, and verifier are unchanged; the final PDF is still three pages and has the exact hashes reviewed by round two.

This paragraph and the consolidated status are incorporated by a final rebuild followed by the same release check. Final public deployment evidence will be appended to DEPLOYMENT.md, which remains outside the archival manifest to avoid altering the verified payload. Completion here tracks the whole review-and-publication cycle; manuscript/preprint readiness is 100%.
