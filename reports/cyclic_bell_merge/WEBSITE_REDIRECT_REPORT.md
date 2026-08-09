# Cyclic Bell website merger and redirect report

Date: 9 August 2026

Release version: 1.1.0

Canonical route:
<https://aleckriebel.github.io/Math/papers/cyclic-bell-exact-values-and-randomness/>

Implementation commit:
[0dd9d030cba128565744c1c7c83cf3956b32d744](https://github.com/AlecKriebel/Math/commit/0dd9d030cba128565744c1c7c83cf3956b32d744)

GitHub Pages build completed: 2026-08-09T16:19:04Z

## Outcome

**PASS.** The three standalone cyclic Bell landing pages are deployed as
static compatibility redirects to one canonical version 1.1.0 manuscript
page. Each redirect remains a complete HTML document and preserves direct
access to its original PDF, immutable source snapshot, release-hash manifest,
archived landing page, and publication history.

The historical PDFs were not edited, renamed, or redirected. Their production
bytes still match the frozen source-package manifests.

## Old-to-new URL map

| Historical landing route | Canonical destination | Historical PDF retained at |
|---|---|---|
| <https://aleckriebel.github.io/Math/papers/cyclic-bell-tsirelson-bound/> | <https://aleckriebel.github.io/Math/papers/cyclic-bell-exact-values-and-randomness/> | <https://aleckriebel.github.io/Math/papers/cyclic-bell-tsirelson-bound/paper.pdf> |
| <https://aleckriebel.github.io/Math/papers/cyclic-bell-randomness-counterexample/> | <https://aleckriebel.github.io/Math/papers/cyclic-bell-exact-values-and-randomness/> | <https://aleckriebel.github.io/Math/papers/cyclic-bell-randomness-counterexample/paper.pdf> |
| <https://aleckriebel.github.io/Math/papers/permutation-blind-bell-randomness/> | <https://aleckriebel.github.io/Math/papers/cyclic-bell-exact-values-and-randomness/> | <https://aleckriebel.github.io/Math/papers/permutation-blind-bell-randomness/paper.pdf> |

## Redirect contract

Every compatibility page contains:

- a robots directive with noindex,follow;
- an absolute canonical link to the merged page;
- a three-second meta refresh;
- a JavaScript window.location.replace fallback to the same URL;
- an ordinary clickable canonical-page link;
- a direct link to the original historical PDF;
- an immutable commit-pinned source link;
- a release-hash link and displayed PDF SHA-256; and
- links to the archived original landing page and publication history.

Production inspection confirmed all listed elements on all three pages. The
ordinary links provide a scripts-disabled route, and no redirect stub points
to another redirect stub.

## Historical artifacts and integrity

| Standalone paper | Production PDF result | SHA-256 | Immutable source snapshot | Hash manifest |
|---|---|---|---|---|
| The exact quantum value of a cyclic Bell operator | 200, application/pdf | c4e80e0956595c28cbf0323639dcf5b84f5ffbd0785362cc4233e2c19812b96f | [21126e38…/cyclic_bell_tsirelson_bound](https://github.com/AlecKriebel/Math/tree/21126e384677d8bb5ebb796c695ce48904fd5e72/cyclic_bell_tsirelson_bound) | [SHA256SUMS](https://github.com/AlecKriebel/Math/blob/21126e384677d8bb5ebb796c695ce48904fd5e72/cyclic_bell_tsirelson_bound/SHA256SUMS) |
| Maximal violation without maximal global randomness in a cyclic Bell family | 200, application/pdf | 3bef4205ead0c1629cc78120dd701f2464ab3a38f855c8f01891412ce7b38975 | [0055250a…/cyclic_randomness_counterexample](https://github.com/AlecKriebel/Math/tree/0055250a009b5f7f0a8283cba4e8813c98b700f8/cyclic_randomness_counterexample) | [MANIFEST.sha256](https://github.com/AlecKriebel/Math/blob/0055250a009b5f7f0a8283cba4e8813c98b700f8/cyclic_randomness_counterexample/MANIFEST.sha256) |
| Permutation-blind Bell scores and obstructions to maximal global randomness | 200, application/pdf | 2c9e4d864f5b617f0d99c1b199f8b3546e3d3aa27ac96356e399a860fd1263c3 | [e3ae7a1a…/minimum_bell_randomness](https://github.com/AlecKriebel/Math/tree/e3ae7a1ac175071b14f2f5c83ddc86149c366da5/minimum_bell_randomness) | [MANIFEST.sha256](https://github.com/AlecKriebel/Math/blob/e3ae7a1ac175071b14f2f5c83ddc86149c366da5/minimum_bell_randomness/MANIFEST.sha256) |

The publication ledger also preserves earlier release bytes. In particular,
the first exact-value PDF had SHA-256
947b601903de18ea6ffbd8e49ba2bfe261c32342c4d1a71dd96ed9f283ec6c94,
and the initial counterexample PDF had SHA-256
73c2e2ab39de79357d7b441a2a4c30f901a13e99e15bf086540783041f7d6051.
No Bell-specific Git tag or GitHub release exists, so commit-pinned trees are
the authoritative immutable source snapshots.

## Canonical version 1.1.0 page

The deployed page uses the existing site stylesheet and includes:

- the merged title, subtitle, sole author, independent affiliation, version,
  date, unrefereed status, and AI-assistance disclosure;
- citation metadata, canonical URL, OpenGraph fields, and JSON-LD
  ScholarlyArticle metadata;
- no DOI metadata and an explicit statement that no DOI exists;
- the audited abstract and exact main results;
- finite-dimensional support rigidity for the first augmented family;
- the Bell-value versus full-behavior scope statement;
- proof architecture and unified replay instructions;
- adversarial-review, priority-audit, claims-ledger, proof-map, manifest, and
  reviewer-packet links;
- a focused source-author review link;
- all three historical PDF, source, and hash records; and
- the manuscript PDF and two-page-summary links.

A production-browser replay rendered 41 MathJax containers and the embedded
PDF without warnings or horizontal overflow.

## Canonical PDF artifacts

| Artifact | Production URL | HTTP result | SHA-256 |
|---|---|---|---|
| Main manuscript | <https://aleckriebel.github.io/Math/papers/cyclic-bell-exact-values-and-randomness/paper.pdf> | 200, application/pdf | 5a7265057a07ef58883defb4c46993328ac418ccf937f3e416e96c61099b3a9b |
| Two-page summary | <https://aleckriebel.github.io/Math/papers/cyclic-bell-exact-values-and-randomness/two-page-summary.pdf> | 200, application/pdf | a52798ec6451b368ddc7e6777004a8b30a478e1104769587e94b466ceac2819c |

Both served hashes match the files in the implementation commit.

## Homepage and sitemap

The deployed homepage at <https://aleckriebel.github.io/Math/> has one merged
cyclic Bell card, no superseded cyclic Bell cards, and the displayed count of
sixteen provisional artifacts.

The deployed sitemap at <https://aleckriebel.github.io/Math/sitemap.xml>
contains the canonical route exactly once and contains none of the three
compatibility routes. The redirect pages remain live but are not represented
as canonical publications.

## Deployment validation

GitHub Pages built implementation commit
0dd9d030cba128565744c1c7c83cf3956b32d744 at 2026-08-09T16:19:04Z.
Production validation then confirmed:

- version 1.1.0 metadata and canonical targeting;
- successful MathJax and embedded-PDF rendering;
- no browser warnings and no horizontal overflow;
- HTTP 200 with application/pdf for both canonical PDFs;
- all required redirect-stub mechanisms and preservation links;
- HTTP 200 with application/pdf for all three historical PDFs;
- exact agreement of all five served PDF hashes with local files;
- one homepage card and the count of sixteen; and
- canonical-only sitemap membership.

No redirect loop, missing artifact, content-type mismatch, metadata mismatch,
or byte-integrity failure was found.

## Website files in the merger

The merger and its version 1.1 refinement cover:

- docs/papers/cyclic-bell-exact-values-and-randomness/index.html;
- docs/papers/cyclic-bell-exact-values-and-randomness/paper.pdf;
- docs/papers/cyclic-bell-exact-values-and-randomness/two-page-summary.pdf;
- docs/papers/cyclic-bell-tsirelson-bound/index.html;
- docs/papers/cyclic-bell-randomness-counterexample/index.html;
- docs/papers/permutation-blind-bell-randomness/index.html;
- docs/index.html;
- docs/sitemap.xml; and
- reports/cyclic_bell_merge/WEBSITE_REDIRECT_REPORT.md.

The version 1.1 implementation commit updated the canonical HTML and PDFs,
homepage, and sitemap. The already-deployed redirect stubs and historical PDFs
were left byte-for-byte unchanged and were reverified in production. No DOI,
release, source-history rewrite, or unrelated paper-page change was made.
