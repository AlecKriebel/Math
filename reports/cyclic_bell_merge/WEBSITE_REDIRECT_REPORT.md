# Cyclic Bell website merger and redirect report

Date: 8 August 2026

Canonical route: <https://aleckriebel.github.io/Math/papers/cyclic-bell-exact-values-and-randomness/>

## Outcome

The three standalone cyclic Bell landing pages have been replaced by static
compatibility redirects to one canonical manuscript page.  Each redirect is
a complete HTML document and preserves direct access to its original PDF,
immutable source snapshot, release-hash manifest, archived landing page, and
publication history.

The historical PDFs were not edited, renamed, or redirected.  Their bytes
still match the frozen source-package manifests.

## Old-to-new URL map

| Historical landing route | Canonical destination | Historical PDF retained at |
|---|---|---|
| `/Math/papers/cyclic-bell-tsirelson-bound/` | `/Math/papers/cyclic-bell-exact-values-and-randomness/` | `/Math/papers/cyclic-bell-tsirelson-bound/paper.pdf` |
| `/Math/papers/cyclic-bell-randomness-counterexample/` | `/Math/papers/cyclic-bell-exact-values-and-randomness/` | `/Math/papers/cyclic-bell-randomness-counterexample/paper.pdf` |
| `/Math/papers/permutation-blind-bell-randomness/` | `/Math/papers/cyclic-bell-exact-values-and-randomness/` | `/Math/papers/permutation-blind-bell-randomness/paper.pdf` |

Every redirect contains:

- `<meta name="robots" content="noindex,follow">`;
- an absolute canonical link to the merged page;
- a three-second meta refresh;
- a JavaScript `window.location.replace` fallback to the same URL;
- an ordinary clickable canonical-page link;
- a direct link to the original PDF;
- an immutable commit-pinned source link;
- a release-hash link and displayed PDF SHA-256;
- a link to the archived original landing page and publication history.

## Historical artifacts and integrity

| Standalone paper | Current historical PDF SHA-256 | Immutable source snapshot | Hash manifest |
|---|---|---|---|
| *The exact quantum value of a cyclic Bell operator* | `c4e80e0956595c28cbf0323639dcf5b84f5ffbd0785362cc4233e2c19812b96f` | [`21126e38…/cyclic_bell_tsirelson_bound`](https://github.com/AlecKriebel/Math/tree/21126e384677d8bb5ebb796c695ce48904fd5e72/cyclic_bell_tsirelson_bound) | [`SHA256SUMS`](https://github.com/AlecKriebel/Math/blob/21126e384677d8bb5ebb796c695ce48904fd5e72/cyclic_bell_tsirelson_bound/SHA256SUMS) |
| *Maximal violation without maximal global randomness in a cyclic Bell family* | `3bef4205ead0c1629cc78120dd701f2464ab3a38f855c8f01891412ce7b38975` | [`0055250a…/cyclic_randomness_counterexample`](https://github.com/AlecKriebel/Math/tree/0055250a009b5f7f0a8283cba4e8813c98b700f8/cyclic_randomness_counterexample) | [`MANIFEST.sha256`](https://github.com/AlecKriebel/Math/blob/0055250a009b5f7f0a8283cba4e8813c98b700f8/cyclic_randomness_counterexample/MANIFEST.sha256) |
| *Permutation-blind Bell scores and obstructions to maximal global randomness* | `2c9e4d864f5b617f0d99c1b199f8b3546e3d3aa27ac96356e399a860fd1263c3` | [`e3ae7a1a…/minimum_bell_randomness`](https://github.com/AlecKriebel/Math/tree/e3ae7a1ac175071b14f2f5c83ddc86149c366da5/minimum_bell_randomness) | [`MANIFEST.sha256`](https://github.com/AlecKriebel/Math/blob/e3ae7a1ac175071b14f2f5c83ddc86149c366da5/minimum_bell_randomness/MANIFEST.sha256) |

The publication ledger also preserves earlier release bytes.  In particular,
the first exact-value PDF had SHA-256
`947b601903de18ea6ffbd8e49ba2bfe261c32342c4d1a71dd96ed9f283ec6c94`,
and the initial counterexample PDF had SHA-256
`73c2e2ab39de79357d7b441a2a4c30f901a13e99e15bf086540783041f7d6051`.
No Bell-specific Git tag or GitHub release exists, so commit-pinned trees are
the authoritative immutable source snapshots.

## Canonical page

`docs/papers/cyclic-bell-exact-values-and-randomness/index.html` uses the
existing site stylesheet and paper-page components.  It includes:

- the merged title, subtitle, sole author, independent affiliation, version,
  date, and unrefereed status;
- citation metadata, canonical URL, OpenGraph fields, and JSON-LD
  `ScholarlyArticle` metadata;
- no DOI metadata and an explicit statement that no DOI exists;
- the audited abstract and exact main results;
- attribution and theorem-comparison table;
- a prominent Bell-value versus full-behavior scope statement;
- proof architecture and unified replay instructions;
- adversarial-review, priority-audit, claims-ledger, proof-map, manifest, and
  reviewer-packet links;
- a focused source-author review link;
- all three historical PDF/source/hash records;
- a detailed AI-assistance disclosure;
- manuscript PDF and two-page-summary links.

The canonical `paper.pdf` and `two-page-summary.pdf` are produced and copied
by the manuscript/reviewer build workflow.  The HTML intentionally points to
their final public locations.

## Homepage and sitemap

The three cyclic Bell cards in the quantum-physics section were replaced by
one canonical card.  The displayed paper count changed from eighteen to
sixteen; every unrelated card and section remains in place.

The canonical route was added to `docs/sitemap.xml`.  The three compatibility
redirects were removed from the sitemap but remain live on disk.

## Local validation

The following checks passed after the HTML/XML changes:

- sitemap XML is well formed;
- canonical citation metadata, OpenGraph URL, canonical link, version, and
  JSON-LD parse correctly;
- no `citation_doi` field is present;
- all three redirect pages contain the required robots, canonical,
  meta-refresh, JavaScript, ordinary-link, PDF, and immutable-source elements;
- all local links resolve, with the two manuscript-workflow PDF outputs
  explicitly excepted until copied;
- the homepage publication section contains exactly sixteen cards and only
  one cyclic Bell card;
- the sitemap contains the canonical route exactly once and none of the
  redirect routes;
- all three historical PDFs retain their recorded SHA-256 hashes.
- a local static server returned HTTP 200 for the canonical page, all three
  compatibility pages, and all three historical PDFs, with `text/html` and
  `application/pdf` content types as appropriate.

Final deployment validation must repeat the HTTP, content-type, redirect-loop,
PDF-hash, and canonical-tag checks after the completed commit is built by
GitHub Pages from `main:/docs`.

## Files changed by the website merger

- `docs/papers/cyclic-bell-exact-values-and-randomness/index.html`
- `docs/papers/cyclic-bell-tsirelson-bound/index.html`
- `docs/papers/cyclic-bell-randomness-counterexample/index.html`
- `docs/papers/permutation-blind-bell-randomness/index.html`
- `docs/index.html`
- `docs/sitemap.xml`
- `reports/cyclic_bell_merge/WEBSITE_REDIRECT_REPORT.md`

No historical PDF, source directory, hash manifest, DOI record, release, or
unrelated paper page was changed.
