# Cube, DFC and BV production browser verification

Checkpoint: 2026-10-25T03:37:51.027148+00:00. Browser task completion:100%; root acceptance remains the publication-tracker gate.

Actual Chrome-extension UI checks are complete for the three production articles at2056×1146 and390×844. Each article was opened by its ordinary research-index title link; each canonical article-title link, natural Read on this page link and full-window PDF link was exercised. Dates/editions are12 October2026 / Zenodo1.0,20 October2026 / Zenodo1.0, and22 October2026 / version1.0.0. All six article metadata captures match canonical/date/link expectations, have equal client/scroll widths, and show no article-content overflow. The intentionally offscreen skip link is the only offscreen DOM element. Mobile PDF frames measure374px.

Each embedded PDF renders its manuscript on desktop and390px. Desktop embed and full-window counters visibly show1/6. The narrow toolbar omits that counter; the actual three-dot menu → Document properties visibly shows Page count6 for each correct filename. Cube/BV full-window390px captures retain100%-scale horizontal crop; DFC captured fit to width. The article embeds fit the narrow frame. The BV native properties dialog overflows for long metadata while the page count remains visible. The report does not claim universal automatic full-window fitting.

Four actual article-link ZIP clicks completed with CUA download events returning local paths. Files were hashed and copied unchanged into downloaded-files/:

- `aim_5_2_source.zip`: 11,430 bytes; SHA-256 `a244ddbbbb0f7ca6d9ca073d21589bef1e9c0a98a404daaca195ee9fc87f6935`; exact archived-source/website match.
- `aim_5_2_verification.zip`: 56,309 bytes; SHA-256 `8ff6e88f6d4a539680667b22931e080365dfd905dd64f795f408e23cc7bb8f01`; exact archived-source/website match.
- `dfc_stability_verification.zip`: 251,455 bytes; SHA-256 `38664f12e8d2e74fa46b3f11363a071ec100aad62ece713b578293a6593d9a0e`; exact archived-source/website match.
- `bv-generators-source-and-verification.zip`: 100,928 bytes; SHA-256 `a7ab72e55fd0952d363f78f92bc418b9f1331ccefb1f75eaea8dda32868601e6`; exact archived-source/website match.

Initial painting states are retained. DFC/BV desktop full-window blank panes settle to rendered manuscripts on subsequent observations without reload. BV mobile initially showed a dark blank viewer; returning to the visibly rendered article top and clicking Read on this page without reload produced a normal manuscript. Large-scroll white captures likewise settled. Cube End/wheel attempts did not browse later PDF pages and are not counted as such. Some immediate Back/navigation browser-helper calls detached or saw the prior page; fresh state was inspected and ordinary navigation continued.

The initial fresh index showed42 entries. One later cube→Research return showed39 and lacked all three new links; raw DOM/screenshot are retained. A single normal reload restored42. Later ordinary DFC→Research return and final fresh direct index navigation both showed42 and the three links. No cause is inferred; no site modification was made.

The57 prepared source/approval/site/checker/renderer bindings were rehashed after UI and remain exact. Root acceptance and16-file liveHTTP manifest are bound separately. Browser serialization is not treated as original HTTP bytes. All37 JPEG screenshots are raw unmodified CUA captures; dimensions and hashes are in screenshot-manifest.json.

Cleanup: only ephemeral963520647 was created and is closed. User Sheet963520539 was never claimed or operated and remains present. Requested2056×1146 viewport was restored explicitly; default reset had measured2056×1202. UI released to root. No Git, deploy, Sheet, redirect, release, outside contact, website/source/shared-code write or frozen-evidence rewrite performed.

Scope: Chrome viewport, not physical phone or cross-browser testing. First-page rendering and total counts, not every page. External DOI traversal and PDF-download-button testing are not claimed. Root should inspect screenshots and receipts before accepting tracker URLs.

Key screenshot evidence:

- `23328912`: desktop embed `23328912-desktop-embedded-initial.jpg`; desktop full-window `23328912-desktop-fullwindow-pdf.jpg`; mobile embed `23328912-mobile-embedded-initial.jpg`; mobile count `23328912-mobile-pdf-properties.jpg`.
- `23524971`: desktop embed `23524971-desktop-embedded-initial.jpg`; desktop full-window `23524971-desktop-fullwindow-settled.jpg`; mobile embed `23524971-mobile-embedded-initial.jpg`; mobile count `23524971-mobile-pdf-properties.jpg`.
- `23572690`: desktop embed `23572690-desktop-embedded-initial.jpg`; desktop full-window `23572690-desktop-fullwindow-settled.jpg`; mobile embed `23572690-mobile-embedded-normalflow-recheck.jpg`; mobile count `23572690-mobile-pdf-properties.jpg`.
