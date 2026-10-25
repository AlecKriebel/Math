# First-six display evidence coverage audit

**Disposition: historical evidence substantially covers the original desktop/mobile article and desktop embedded-PDF checks; it does not establish all of the later, more granular browser gates.** No new page failure was found or inferred. No UI, network, mathematical review, source repair, website edit, publication/status change, or external communication was performed by this audit.

The six current HTML files and the shared research stylesheet are byte-identical to their historical live-deployment receipts. All six PDFs and six source ZIPs still match both the authenticated source-download receipts and the historical live HTTP byte checks. This preserves the relevance of the earlier checks. It does not establish current server behavior without a new live check.

The absence of these six IDs from the later `browser-root-disposition.json` is an incremental-registry coverage omission, not evidence that earlier checks failed. That registry explicitly says `PASS_FOR_LISTED_PAPERS`. Its detailed phone iframe/full-window checks cannot be retroactively attributed to papers it does not list.

## Gate coverage

“Written” below means an explicit contemporaneous browser-inspection attestation, read in full. “Image” means the saved pixels were actually inspected in this audit. A content-check boolean or HTML iframe element alone is never classified as visual evidence.

| Record | Desktop article | 390px article | Desktop embedded PDF | Mobile embedded PDF | Full-window PDF action/render | Browser download completion |
| --- | --- | --- | --- | --- | --- | --- |
| 23575190, pilot | Written + original article image | Written | Written + revised 7-page viewer image | Unproven | Unproven specifically | Unproven |
| 23539283, tensor core | Written, full HTML page | Written, 390×844 | Written, correct title/pages/edition | Unproven | Unproven | Unproven |
| 23577484, Bray | Written, full HTML page | Written, 390×844 | Written, correct title/pages/edition | Unproven | Unproven | Unproven |
| 23310484, sphere skeleta | Written, full page | Written, local 390px | Written, local 8-page iframe | Unproven | Unproven | Unproven |
| 23331395, Seshadri | Written, full page | Written + live 390×844 top image | Written, live 5-page iframe | Unproven | Unproven | Unproven |
| 22770864, odd-order group | Written, full page | Written, 390×844, no overflow | Written, 13-page title/version | Unproven | Unproven | Unproven |

For **every record**, historical HTTP 200 responses with PDF/ZIP bytes and SHA-256 matching sources are proven by saved receipts and the fresh local comparison. This establishes delivery/integrity at the recorded time; it is distinct from an actual completed browser click/download. Likewise, visible or statically correct full-window/Zenodo fallback links do not establish that the clicked destination rendered or a browser download completed. Phone checks were desktop-browser viewport emulation, not tests on a physical mobile device. A native first-page render does not mean every PDF page was visually checked in-browser.

## Exact historical evidence

Paths below are relative to `/Users/alec/Documents/Math/research_website_catalogue_20261024` unless explicitly prefixed. The machine-readable `evidence-identities.json` supplies absolute paths, full SHA-256 and sizes for all 66 input identities, including receipts and images. `source-live-bindings.json` records exact per-record source/current/live bindings; `ui-parameters.json` is the complete canonical URL, main-PDF filename/page count/hash, source-download target/hash and fallback handoff.

### Human-approved pilot: 23575190

The pilot is a separate programme at `/Users/alec/Documents/Math/research_website_pilot_20261024`; it is not missing merely because it has no equivalent catalogue paper folder. Root's assignment identifies this as the human-approved pilot, consistent with the supplied user acceptance of the revised page and request to extend the workflow. Human acceptance is distinct from technical evidence for every browser/device gate. The initial `verification/COMPLETION.json` truthfully records `user_review_pending: true` before the later revision and acceptance; this audit does not rewrite that history or invent a machine-readable approval receipt.

The pilot `verification/browser-qa.json` is dated 2026-10-24T22:58:06Z and records 856px desktop and 390px phone layouts, no horizontal overflow, both index/article checks, visible abstract, paper-link and anchor navigation. Its screenshot `site_preview/paper-desktop.jpg` visibly shows the original article top/abstract/comparison; its Review notes link predates the requested simplification and iframe revision.

The later `verification/revision-completion.json` at 23:12:34Z explicitly records desktop Chrome PDF rendering, no phone overflow, and a **blank native PDF surface in the Codex in-app browser**, with direct-open fallback retained. `site_preview/revision-live.jpg` actually shows the revised research question, the two visible fallback links, and the embedded Chrome viewer on page 1/7 with the correct title, author, 22 October 2026 date and v1.0.0. It is desktop evidence, not phone or full-window evidence. `site_preview/research-live.jpg` shows the one-paper index only. None of these images includes URL chrome; the named receipts and adjacent production receipt provide the historical context, not a cryptographic screen-to-HTML binding.

Pilot source identity comes from `sources/download-receipt.json` in that separate programme. The initial production receipt at 22:59:17Z corresponds to pre-revision HTML hash `254f1caf98c8326f226f1eff1b2ffb53f0d16eda2fc50e61a4f3c0c5e5b5ed7a`. The relevant revised `verification/revision-production-check.json` at 23:11:17Z binds current HTML `0c34921ab54ee95dab43c67e6379b4af5a4fba15cc7131654c8c6eb62ae2c98f` and current CSS/PDF/ZIP, under hosting version `f9bed7463d888f5a`. Catalogue `verification/pilot-live-recheck.json` repeats those HTML/PDF/ZIP hashes but lacks a timestamp and URL, so it is corroborative rather than the principal provenance receipt. The original and revised receipts must not be merged as though their HTML/CSS were identical.

### Tensor core and Bray: 23539283 and 23577484

`verification/local-browser-qa.json`, 2026-10-24T23:48:30Z, says both full HTML pages were visually inspected, both native Chrome PDF iframes rendered the correct title/pages/edition, and both 390×844 article views wrapped without clipping. It explicitly describes the local-preview stage, with live verification pending. The subsequent `verification/live-23539283-23577484.json`, 23:51:40Z, supplies HTTP and exact byte/hash checks for the same HTML, PDF, ZIP, citation and shared CSS. This connects unchanged local inspected files to historical live delivery; it does not turn a local visual observation into a direct live-browser observation.

No named saved screenshots for these two papers were found in the bounded visual stores searched. That does not erase the explicit written attestation. `verification/final-content-check.json` and `final-content-check-revalidated.json` provide exact content/source/metadata hashes and searchable 10/11-page PDFs; their PASS/iframe booleans are not substituted for browser evidence.

### Sphere skeleta and Seshadri: 23310484 and 23331395

`verification/batch2-browser-qa.json`, 2026-10-25T00:10:16Z, records both full-page inspections; sphere's 8-page iframe and 390px article were inspected locally, while Seshadri's 5-page iframe and 390×844 article were inspected live. Seshadri's scrollWidth equals innerWidth, 390px. `screenshots/seshadri-mobile.png` visibly corroborates the article top/title, 12 October 2026/version 1.0/preprint status, PDF/ZIP/Zenodo links and abstract start. It does not show a PDF viewer.

`verification/live-23310484-23331395.json`, 00:06:46Z, binds HTML/PDF/ZIP/citation and shared CSS. `batch2-content-check.json` binds source metadata/searchable 8/5-page PDFs and static links; it is not an extra visual test. No named sphere screenshot was found in the bounded stores.

### Odd-order group: 22770864

`verification/group-browser-qa.json`, 2026-10-25T00:33:21Z, explicitly says the full article and 13-page Chrome native iframe were visually inspected with correct title/version. The 390×844 article had scrollWidth = innerWidth = 390 with wrapped title/links. It names `verification/live-22770864-22729537.json`, 00:17:37Z, which binds this page's HTML/PDF/ZIP/citation/CSS. The companion record in that live receipt is outside this audit. `batch3-group-content-check.json` supplies static/source bindings only. No named group screenshot was found in the bounded stores.

## Search boundary and recommendations

The audit enumerated the actual image files in the catalogue `screenshots/`, catalogue `verification/` tree, and pilot `site_preview/`, and searched the catalogue/pilot verification JSON/Markdown/text for six IDs/slugs and display terms. It examined the complete relevant early browser/source/live receipts, complete pilot completion/production/revision receipts and logs, the source-bound static checks, and the early programme publication-log entries. Later `browser-2026-10-25T00-47-24-393Z.json` covers nine other papers, not these six. First-six references in `browser-display-20261025/evidence.json` and `index-links-final.json` occur only in index-link lists, so they do not prove individual paper rendering. Sheet snapshots, test passes, index screenshots, mathematical reports and later unrelated page screenshots are not used to fill missing visual gates.

Root may preserve/backfill the explicit historical desktop/mobile article and desktop-PDF attestations with their exact limits. To apply the newer uniform display gate, a separate Chrome agent should acquire actual 390×844 embedded-PDF renders, activate and inspect each full-window PDF, and distinguish completed browser downloads from link presence or HTTP hash checks. Capturing fresh article/desktop images too would standardize evidence, but the earlier written observations should remain intact. Preserve the pilot's recorded in-app blank-viewer limitation and clear fallback. No failure is inferred merely because a screenshot or later registry row is absent.
