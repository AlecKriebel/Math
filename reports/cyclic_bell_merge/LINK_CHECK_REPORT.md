# Cyclic Bell link-check report

Date: 9 August 2026

Release version: 1.1.0

Deployed tip:
[a1cf257a5e935faa3c01292a4f5cd5d6accbbb1d](https://github.com/AlecKriebel/Math/commit/a1cf257a5e935faa3c01292a4f5cd5d6accbbb1d)

Scientific snapshot pinned by the manuscript:
[609f8c6ffc083b665804890dd82fc739d414ea9d](https://github.com/AlecKriebel/Math/commit/609f8c6ffc083b665804890dd82fc739d414ea9d)

GitHub Pages build completed: 2026-08-10T04:02:30Z

Canonical URL:
<https://aleckriebel.github.io/Math/papers/cyclic-bell-exact-values-and-randomness/>

## Deployment verdict

**PASS.** Repository parsing, local integrity checks, direct production HTTP
checks, and a production-browser replay agree for the final referee-explication
deployment of version 1.1.0. No required page or artifact is missing, no
compatibility route forms a redirect loop, and the deployed PDF bytes match
the repository artifacts exactly.

## Canonical production page

The canonical page loaded with the version 1.1.0 content and metadata. Its
title, author, publication date, canonical URL, citation PDF URL, OpenGraph
fields, JSON-LD ScholarlyArticle object, unrefereed status, and AI-assistance
disclosure agree with the repository source. No DOI metadata is present.

The browser replay found 43 rendered MathJax containers. The embedded
manuscript displayed successfully, the scientific source commit
`609f8c6ffc083b665804890dd82fc739d414ea9d` was visible, the canonical target
was correct, and the page had no horizontal overflow. MathJax and the page
scripts produced no warnings or errors; the only console item was the
repository-wide missing `/favicon.ico` request, which returned 404 and is
outside this scoped paper-page revision.

## Canonical PDF artifacts

| Artifact | Production URL | HTTP result | Served SHA-256 |
|---|---|---|---|
| Main manuscript, 28 pages | <https://aleckriebel.github.io/Math/papers/cyclic-bell-exact-values-and-randomness/paper.pdf> | 200, application/pdf | 9d0d23837aed20346f6e97234095ee146f7e7b852c7a4a4b5d646e5fa595c0f6 |
| Two-page summary | <https://aleckriebel.github.io/Math/papers/cyclic-bell-exact-values-and-randomness/two-page-summary.pdf> | 200, application/pdf | 0f3dfa78424a8934defdf9952593bf9a7269f7fec58dc6dd5c4824fa9db562d2 |

Both hashes match the files committed under the canonical website route.

## Compatibility-route checks

Each historical landing route remains a valid HTML document. Static
inspection confirmed the consolidation notice and all required fallback
mechanisms before the timed navigation to the canonical page.

| Historical route | Robots | Canonical | Meta refresh | JavaScript | Ordinary link | Historical PDF | Immutable source |
|---|---:|---:|---:|---:|---:|---:|---:|
| <https://aleckriebel.github.io/Math/papers/cyclic-bell-tsirelson-bound/> | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| <https://aleckriebel.github.io/Math/papers/cyclic-bell-randomness-counterexample/> | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| <https://aleckriebel.github.io/Math/papers/permutation-blind-bell-randomness/> | PASS | PASS | PASS | PASS | PASS | PASS | PASS |

For every stub:

- the robots value is noindex,follow;
- the absolute canonical target is the new canonical page;
- the meta-refresh delay is three seconds;
- the JavaScript fallback uses window.location.replace with the same target;
- an ordinary clickable link supports scripts-disabled clients;
- the original PDF has a direct, nonredirecting link; and
- the immutable source snapshot, release-hash record, archived landing page,
  and publication-history links remain present.

No stub links back to another stub, so no redirect loop is possible within
this compatibility layer.

## Historical-PDF production integrity

| Historical PDF URL | HTTP result | Served SHA-256 | Result |
|---|---|---|---|
| <https://aleckriebel.github.io/Math/papers/cyclic-bell-tsirelson-bound/paper.pdf> | 200, application/pdf | c4e80e0956595c28cbf0323639dcf5b84f5ffbd0785362cc4233e2c19812b96f | unchanged |
| <https://aleckriebel.github.io/Math/papers/cyclic-bell-randomness-counterexample/paper.pdf> | 200, application/pdf | 3bef4205ead0c1629cc78120dd701f2464ab3a38f855c8f01891412ce7b38975 | unchanged |
| <https://aleckriebel.github.io/Math/papers/permutation-blind-bell-randomness/paper.pdf> | 200, application/pdf | 2c9e4d864f5b617f0d99c1b199f8b3546e3d3aa27ac96356e399a860fd1263c3 | unchanged |

The served bytes match the frozen local artifacts and their historical
manifests. The landing-page redirects do not intercept these PDF URLs.

## Homepage and sitemap

- <https://aleckriebel.github.io/Math/> uses the current selected-portfolio
  design and presents exactly one canonical cyclic Bell card. It has no
  retired provisional-artifact count assertion.
- <https://aleckriebel.github.io/Math/sitemap.xml> lists the canonical paper
  route exactly once.
- The sitemap lists none of the three compatibility landing routes.
- The homepage contains no surviving card link to a superseded landing page.

## Final result

The production deployment from tip
`a1cf257a5e935faa3c01292a4f5cd5d6accbbb1d`, carrying scientific snapshot
`609f8c6ffc083b665804890dd82fc739d414ea9d`, passes the canonical-page,
metadata, rendering, PDF, redirect, sitemap, homepage, content-type, and
historical-integrity checks for version 1.1.0. A forthcoming
deployment-record commit will add these reports only; it will not change the
scientific snapshot or the deployed artifacts described here.

## Earlier version 1.1 deployment record

Before the referee-explication pass, implementation commit
`0dd9d030cba128565744c1c7c83cf3956b32d744` was built by GitHub Pages at
2026-08-09T16:19:04Z. That production replay rendered 41 MathJax containers
and served manuscript and summary hashes
`5a7265057a07ef58883defb4c46993328ac418ccf937f3e416e96c61099b3a9b`
and `a52798ec6451b368ddc7e6777004a8b30a478e1104769587e94b466ceac2819c`,
respectively. Those values are retained here as deployment history and are
superseded by the current results above.
