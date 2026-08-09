# Cyclic Bell link-check report

Date: 9 August 2026

Release version: 1.1.0

Implementation commit:
[0dd9d030cba128565744c1c7c83cf3956b32d744](https://github.com/AlecKriebel/Math/commit/0dd9d030cba128565744c1c7c83cf3956b32d744)

GitHub Pages build completed: 2026-08-09T16:19:04Z

Canonical URL:
<https://aleckriebel.github.io/Math/papers/cyclic-bell-exact-values-and-randomness/>

## Deployment verdict

**PASS.** Repository parsing, local integrity checks, and a production-browser
replay agree for deployed version 1.1.0. No required page or artifact is
missing, no compatibility route forms a redirect loop, and the deployed PDF
bytes match the repository artifacts.

## Canonical production page

The canonical page loaded with the version 1.1.0 content and metadata. Its
title, author, publication date, canonical URL, citation PDF URL, OpenGraph
fields, JSON-LD ScholarlyArticle object, unrefereed status, and AI-assistance
disclosure agree with the repository source. No DOI metadata is present.

The browser replay found 41 rendered MathJax containers. The embedded
manuscript displayed successfully, the browser console contained no warnings
or errors, and the page had no horizontal overflow.

## Canonical PDF artifacts

| Artifact | Production URL | HTTP result | Served SHA-256 |
|---|---|---|---|
| Main manuscript | <https://aleckriebel.github.io/Math/papers/cyclic-bell-exact-values-and-randomness/paper.pdf> | 200, application/pdf | 5a7265057a07ef58883defb4c46993328ac418ccf937f3e416e96c61099b3a9b |
| Two-page summary | <https://aleckriebel.github.io/Math/papers/cyclic-bell-exact-values-and-randomness/two-page-summary.pdf> | 200, application/pdf | a52798ec6451b368ddc7e6777004a8b30a478e1104769587e94b466ceac2819c |

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

- <https://aleckriebel.github.io/Math/> presents exactly one canonical cyclic
  Bell card and displays the total count of sixteen provisional artifacts.
- <https://aleckriebel.github.io/Math/sitemap.xml> lists the canonical paper
  route exactly once.
- The sitemap lists none of the three compatibility landing routes.
- The homepage contains no surviving card link to a superseded landing page.

## Final result

The production deployment from implementation commit
0dd9d030cba128565744c1c7c83cf3956b32d744 passes the canonical-page,
metadata, rendering, PDF, redirect, sitemap, homepage, content-type, and
historical-integrity checks for version 1.1.0.
