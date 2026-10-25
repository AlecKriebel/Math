# Three live PDFs and six actual browser downloads

The bounded PDF-rendering and download gates **PASS for all three approved publications**. The raw first pages render at desktop width, the desktop viewer exposes total counts of **6, 7 and 21**, and each fixed page fits the complete width of a **390 × 844** desktop PDF viewer after its ordinary fit control is selected. All six files actually saved by the browser match the approved production bytes and a matching acquired primary source. Browser work ran on 25 October 2026, 05:44–05:47 UTC.

Completion is **100% for the PDF and download checks**, and **95% for the entire assigned finish including inherited-tab cleanup**. All six tabs created here were closed and temporary viewport overrides were cleared. Two inherited research tabs remain assigned to their earlier browser sessions; their owners need to close them. UI ownership was released to root at 05:47:35 UTC. No full native-URL gate PASS is asserted.

## Checkable results

| Record and paper | Desktop first page / total | 390-pixel fitted page | Visible narrow properties | Actual PDF and support download |
| --- | --- | --- | --- | --- |
| 23306332 — Nonunique nearest stable complex quadratics | [2056 × 1146, 1 / 6](quadratic-desktop-settled.jpg) | [390 × 844](quadratic-narrow-fit.jpg) | [6 pages](quadratic-narrow-properties.jpg) | Both byte-identical PASS |
| 23203100 — Pure-loss bosonic dynamic capacities | [2056 × 1146, 1 / 7](bosonic-desktop-settled.jpg) | [390 × 844](bosonic-narrow-fit.jpg) | [7 pages](bosonic-narrow-properties.jpg) | Both byte-identical PASS |
| 22089807 — Simultaneous amplifiers beyond relative fitness 3/2 | [2056 × 1146, 1 / 21](amplifier-desktop-settled.jpg) | [390 × 844](amplifier-narrow-fit.jpg) | [21 pages](amplifier-narrow-properties.jpg) | Both byte-identical PASS |

The article's actual **Open PDF in a full window** link was followed for every viewer check. The exact raw PDF URLs, tab IDs and timestamps are recorded in `browser-events.json` and `capture-events.json`; fresh article DOM snapshots establish the visible links. This work does not repeat or replace the earlier article-body, embedded-PDF, scope, collaboration, citation, and index-50 checks in `../browser-approved-three-sol-20261025/` and `../root-three-browser-finish-20261025/`.

The production bindings are site commit `16b7b547c7cf7f54e586f2a753fc861763807f33` and hosting release `f3d003e1e8f50e45`. This session did not deploy, alter, commit or push production files.

## Download identity

Each download used the documented locator `downloadMedia` action on a fresh own article tab, with exactly one file downloaded per tab. It did not use a command-line network transfer. The browser saved the files in Downloads; no downloaded code or archive was executed or extracted. `actual-download-verification.json` records actual saved paths, byte counts, SHA-256 values, the matching site path, and matching acquired primary-source paths.

| Record | File | Bytes | SHA-256 |
| --- | --- | ---: | --- |
| 23306332 | nonunique_nearest_stable_complex_quadratics.pdf | 76,336 | `6439bda84f32d9a5ac1680e184975df159f51f8c7e44e609fa873dfa8ae78e1f` |
| 23306332 | nonunique_nearest_stable_complex_quadratics_verification.zip | 37,068 | `2fc6b62d67ab6681c36f7d3806db549073a3f0b2e0d039817f997fab9eb96dee` |
| 23203100 | paper.pdf | 88,566 | `490c6d4d78eb4c2ae829d06f31df1ed1ace955174acec87279f5d5eb8dee8581` |
| 23203100 | zenodo-upload-kit.zip | 114,329 | `e9f9adb0dca6f7776b215672ab97b7f8922aae415d2d9f73afd631259ca40fab` |
| 22089807 | simultaneous_amplification_beyond_three_halves.pdf | 214,040 | `1d6d1d31a782776b07b9240467f02d624b47dcde5c83f4740a192136c2dfb8e3` |
| 22089807 | simultaneous_amplifier_beyond_three_halves_source_and_certificates.tar.gz | 6,952,578 | `e5b61e79d065a9abec0908e28db7e79366b5fccedeb6efbf22eadd7af3cc57ae` |

The bosonic PDF's actual saved filename is `paper (5).pdf`; this browser duplicate suffix is recorded without renaming it. Its contents match `paper.pdf` exactly.

## Scope of narrow rendering evidence

The three positive narrow captures are untouched screenshots from Chrome's real desktop PDF viewer with CDP viewport configuration `{width:390,height:844,deviceScaleFactor:1,mobile:false}`. Saved `*-narrow-metrics.json` files assert CSS visual width 390 before the final captures. The fit control was clicked in the ordinary desktop toolbar before resizing. At 390 pixels the toolbar hides the count, so the ordinary three-dot menu and Document properties dialog establish the total independently on screen.

These checks establish rendering and full-page-width fitting in the desktop viewer at the stated dimensions. They do not establish physical-phone, mobile-OS or PDF reflow behavior. The fixed-page body text is small at this scale. Long title and filename fields in the narrow properties dialogs clip at the right edge; the page counts remain clearly visible.

Every screenshot is raw `Tab.screenshot({})` output, with no cropping, compositing, resampling, annotation, or substitute local PDF rendering. `screenshot-manifest.json` records all 20 captures, dimensions, byte lengths and SHA-256 values. All dimensions are either 2056 × 1146 or 390 × 844. Four captured redraw frames are retained and explicitly excluded from positive rendering adjudication:

- `quadratic-desktop-first-page.jpg` — blank viewer before PDF redraw settled; its initial action-note wording is superseded by this exclusion.
- `bosonic-desktop-initial.jpg` — toolbar rendered, page and thumbnails still blank.
- `amplifier-desktop-initial.jpg` — toolbar rendered, page and thumbnails still blank.
- `amplifier-narrow-fit-initial.jpg` — blank page area immediately after resizing.

The settled captures listed in the results table supply the positive evidence. PDF DOM snapshots are empty, so visible browser screenshots and viewer properties are the relevant evidence. No native desktop screenshot was substituted.

## Preservation and cleanup

The lean preservation baseline was captured at 05:45:24 UTC, after the first PDF viewer check and before the six download transfers. It contains **591 exact file bindings**: all **444 actual public site files**, `render_page.py`, `bosonic_source.py`, `final-content-check.py`, three site configuration files, three publication configuration files, and the acquired primary-source files for these records. This is deliberately narrower than the whole programme and excludes review runtimes and caches. `preservation-after.json` rehashes every path and confirms **591 / 591 byte-identical**, with 444 public files still present. No stronger before-first-UI baseline claim is made.

The session created and closed tabs **963520728, 963520731, 963520734, 963520737, 963520740, 963520743**. The final cleanup capture and metrics establish the restored 2056 × 1146 desktop viewport. All ten protected original tabs retain their original IDs and URLs at release. The Google Sheet **963520539** and protected research index **963520551** were never claimed or operated. Private user tab titles and URLs were inspected only in the transient inventory and are not retained in this evidence bundle.

Inherited tabs **963520718** and **963520725** were explicitly authorized for closure, but remain. The supported claim operation for 718 reports that it belongs to previous browser session `01a17173-ba96-7c41-9434-d189739ed321`; documented `tabs.get` cannot access it from this session. No native workaround, browser restart, security change, unlock request, or repeated busy loop was used. Root was notified to have the owning sessions complete cleanup. `browser-cleanup.json` preserves the exact scope and pending condition.

Only this dedicated verification directory was written, apart from the six authorized inbound browser downloads. No site, manuscript, research result, shared source/configuration, Sheet, review evidence, Git, hosting, or external communication was changed. No child agents were spawned. This report verifies publication presentation and file delivery, not the underlying mathematical proofs.

`audit_evidence.py` repeats the file, download and screenshot custody checks in read-only mode. `evidence-manifest.json` and `SEAL.json` bind the complete local verification bundle; they deliberately preserve the pending inherited-owner cleanup condition.
