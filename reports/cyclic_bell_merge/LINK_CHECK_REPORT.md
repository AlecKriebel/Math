# Cyclic Bell link-check report

Date: 8 August 2026

Canonical URL: <https://aleckriebel.github.io/Math/papers/cyclic-bell-exact-values-and-randomness/>

## Pre-deployment verdict

**PASS.** Static parsing, a local HTTP server, and an actual Chromium render
all agree. The post-push production check is recorded in the final section
after GitHub Pages deployment.

## Local link and metadata checks

- Canonical `index.html` parsed as HTML and its JSON-LD parsed as one
  `ScholarlyArticle` object.
- `citation_title`, `citation_author`, `citation_publication_date`,
  `citation_pdf_url`, version, canonical URL, and OpenGraph URL match.
- No `citation_doi`, DOI identifier, submission, acceptance, endorsement, or
  peer-review claim is present.
- MathJax loaded and rendered 31 expressions; no browser console warnings or
  errors were emitted.
- The embedded canonical PDF loaded from the local server with HTTP 200.
- The canonical PDF and two-page summary links resolve.
- All relative links from the homepage, canonical page, and three redirect
  pages resolve on disk.
- `docs/sitemap.xml` is well formed, lists the canonical route once, and lists
  none of the three redirects.
- The homepage has one merged card, no old cyclic-card links, and the updated
  count of sixteen provisional artifacts.

The only HTTP 404 observed during browser rendering was the site's optional
`favicon.ico`; no page, artifact, stylesheet, script, or required link failed.

## Redirect checks

Each route initially rendered its consolidation notice, historical-PDF link,
immutable-source link, and ordinary canonical link, then navigated after
three seconds to the exact canonical production URL:

| Route | Notice | Historical PDF link | Final URL | Result |
|---|---:|---:|---|---|
| `/Math/papers/cyclic-bell-tsirelson-bound/` | yes | `./paper.pdf` | canonical URL | PASS |
| `/Math/papers/cyclic-bell-randomness-counterexample/` | yes | `./paper.pdf` | canonical URL | PASS |
| `/Math/papers/permutation-blind-bell-randomness/` | yes | `./paper.pdf` | canonical URL | PASS |

Every stub contains `noindex,follow`, a canonical link, meta refresh,
`window.location.replace`, a scripts-disabled ordinary link, and no return
link that can create a redirect loop.

## Historical-PDF integrity

| PDF route | SHA-256 | Result |
|---|---|---|
| `cyclic-bell-tsirelson-bound/paper.pdf` | `c4e80e0956595c28cbf0323639dcf5b84f5ffbd0785362cc4233e2c19812b96f` | unchanged |
| `cyclic-bell-randomness-counterexample/paper.pdf` | `3bef4205ead0c1629cc78120dd701f2464ab3a38f855c8f01891412ce7b38975` | unchanged |
| `permutation-blind-bell-randomness/paper.pdf` | `2c9e4d864f5b617f0d99c1b199f8b3546e3d3aa27ac96356e399a860fd1263c3` | unchanged |

The old live routes and PDFs returned HTTP 200 before the merger and their
served PDF bytes matched these local hashes. Initial superseded PDF bytes
remain accessible through the commit-pinned links on the canonical page.

## Browser layout check

The existing site style renders the long title without clipping, keeps the
four primary actions visible, lays out the three main-result cards and
theorem boxes coherently, wraps long hashes within the historical table, and
embeds the manuscript at the end. The page was tested at the default 1280 by
720 viewport and has no horizontal overflow there.

## Post-push production check

Pending the first scoped implementation push. This section will record live
HTTP/content-type/hash/canonical results before the release-record commit.
