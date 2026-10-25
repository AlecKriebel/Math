# Live full window PDF presentation verification

The three live manuscripts pass the bounded desktop rendering, narrow viewport fitting and visible page-count checks. The checks completed on 25 October 2026 between 05:06 and 05:08 UTC. Completion estimate for this bounded PDF task: **100%**. The overall publication goal remains active; this report does not authorize a tracker status or assert completion of the full inventory.

## Results

| Zenodo record | Desktop first page and toolbar | Narrow first page after viewer fit | Visible properties count | Decision |
| --- | --- | --- | --- | --- |
| 23393596 braid | [2056 × 1146 capture](braid-desktop-initial.jpg), 1 / 4 | [390 × 844 capture](braid-narrow-fit-settled.jpg) | [4 pages](braid-narrow-properties.jpg) | Bounded PDF PASS |
| 23358014 wave | [2056 × 1146 capture](wave-desktop-initial.jpg), 1 / 6 | [390 × 844 capture](wave-narrow-fit.jpg) | [6 pages](wave-narrow-properties.jpg) | Bounded PDF PASS |
| 23356964 Cantor actions | [2056 × 1146 capture](cantor-desktop-initial.jpg), 1 / 5 | [390 × 844 capture](cantor-narrow-fit.jpg) | [5 pages](cantor-narrow-properties.jpg) | Bounded PDF PASS |

Each article's actual visible **Open PDF in a full window** link was followed in the same isolated browser tab. Article DOM observations, the resulting exact PDF URLs, action timestamps and screenshot records are preserved in `braid-article-dom.txt`, `wave-article-dom.txt`, `cantor-article-dom.txt`, `browser-actions.json` and `report.json`.

The targets were:

- Braid: https://aleckriebel.com/research/deep-derived-pure-braids-not-one-solvable/deep-derived-pure-braids-v1.0.pdf
- Wave: https://aleckriebel.com/research/critical-wave-sparse-control-quadratic-growth/critical_wave_growth.pdf
- Cantor actions: https://aleckriebel.com/research/generic-cantor-actions-wreath-product-hyperfinite/generic-wreath-hyperfiniteness-note.pdf

## Meaning of the narrow viewport result

The narrow captures come from Chrome's actual desktop PDF viewer with a 390 × 844 viewport, scale factor 1 and `mobile=false`. They establish that each live PDF renders at this width and fits after selecting the viewer's ordinary fit control in the desktop toolbar before resizing. They do not establish behavior on a physical phone or mobile OS, or that the fit control remains exposed at 390 pixels.

At its retained 100% zoom, the initial braid PDF is horizontally cropped; `braid-narrow-initial.jpg` preserves that finding. The fitted captures show the complete page width. Fixed-page body text is small at fit scale; these are rendering and fitting checks, not claims of reflow or comfortable detailed reading at that scale. The article mobile HTML and embedded-view checks remain in the earlier frozen evidence and were outside this bounded rerun.

In the narrow viewer the toolbar hides the total count. The visible three-dot menu and **Document properties** dialog establish 4, 6 and 5 pages directly. The Cantor dialog clips part of its long title at the right edge, but its count remains visible. No native desktop screenshot, source-PDF rendering or image manipulation substitutes for these frames.

## Capture custody and exclusions

All 22 JPEG files are untouched output bytes from the documented browser `Tab.screenshot({})` API. `screenshot-manifest.json` records their exact byte lengths, SHA-256 hashes and JPEG dimensions. The browser action record associates each frame with its actual URL and notes. All desktop captures are 2056 × 1146; all narrow captures are 390 × 844.

The following resize frames remain preserved but are excluded from the positive rendering adjudication because their PDF redraw had not settled:

- `braid-desktop-restored-before-fit.jpg`
- `braid-narrow-after-fit-initial.jpg`
- `cleanup-desktop-initial.jpg`

`braid-desktop-fit-tooltip.jpg` did not expose a visible tooltip and is not used as proof of an action label. Subsequent captures show the actual fit-control change and fitted page. The initial own-tab creation returned a transient detach notification; a fresh tab listing identified the newly created tab, and that same tab was bound and verified. No other tab was created to recover it.

## Preservation and cleanup

Before browser UI actions, `preservation-before.json` hashed 457 pre-existing evidence files, including the readiness manifest and the original browser and index evidence trees. `preservation-after-browser.json` verifies that all 457 remain byte-identical. The readiness manifest remains SHA-256 `78473ab6ccd0564084f753f716d2f0af095c5af31366f94f4acad5466a2cd0e4`.

All 51 actual paths referenced by the frozen readiness manifest were rehashed after UI and match the manifest's frozen byte lengths and SHA-256 hashes (`readiness-51-after-browser.json`). This session's before-UI baseline covered the manifest and evidence files, rather than a separate fresh read of all 51 referenced source paths. The final seal repeats the 51-path check. No stronger before-UI source-path claim is made.

The frozen 107-file and 109-file browser manifests, and the completed 103-file post-expiry index manifest, independently verify against every referenced file after this session (`frozen-manifests-after-browser.json`). Their manifest hashes remain respectively `58fa35ed8823b2eecc6e362a0b76b2f27d882c8ec79a304e33e1e618b1a747a5`, `f1ad3375442aa67332d9d7a9713483aad20ec1bff072bd907198060600d497f2` and `ef5998dfe59959a1219085ae4d823c1f3206bd025f9a779a71665e144162c17c`.

The sole created tab, **963520696**, was closed at 05:08:31 UTC after clearing the temporary viewport override and capturing the settled restored desktop viewport. The session then had zero owned tabs. All 11 original user tabs remained listed with their original IDs and URLs. The protected Google Sheet tab **963520539** was never claimed, navigated, edited or closed. `browser-cleanup.json` preserves the final inventory. UI ownership was released to the parent before offline report preparation.

Only this dedicated verification directory was written. This session made no Git, site, shared script, source manuscript, spreadsheet, deployment, redirect or download changes, and no external communication. No child agents were spawned. Existing ZIP-download receipts and post-expiry index checks were preserved and not rerun.

The retained `audit_evidence.py` can be run with `python3` in its default read-only mode to repeat the custody checks. Its explicit `--write-receipt` option regenerates the local receipt and should only be used when intentionally resealing this bundle.
