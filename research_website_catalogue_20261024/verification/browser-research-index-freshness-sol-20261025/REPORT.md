# Separate research-index freshness verification

Completed 2026-10-25T04:09:41.107448+00:00. Index-only assignment: **100%**, pending root acceptance. UI released at 2026-10-25T04:07:38.735Z.

**PASS for the observed normal navigation sequence:** initial canonical `/research/` already contained 44 entries; every later index observation contained 44 and exactly one ordinary link to each new paper. No reload was needed or performed, and no 42-entry state recurred in this separate batch. This verifies the tested Chrome profile/session; it does not claim a universal cold-cache result or retroactively revoke previously cached one-hour responses.

The browser evidence comprises 31 actual navigation/state observations, 19 index observations, and six unmodified JPEG screenshots. Desktop viewport was2056 × 1146; mobile viewport was390 × 844. All six required ordinary article→Research returns passed: reachability, Satoh, and the previous cube article at both widths. Desktop and mobile Back/Forward index returns and direct canonical index navigation also passed. Each index observation had scroll width equal to client width.

Exact index and canonical URL: `https://aleckriebel.com/research/`. Every inspected article header Research link had raw href `/research/`, resolving to that same URL. The expected ordinary title links were:

- `https://aleckriebel.com/research/binary-directed-chip-firing-reachability/`
- `https://aleckriebel.com/research/satoh-sl2-representation-filtration-counterexamples/`

The previous article was `https://aleckriebel.com/research/aim-free-by-cyclic-two-cube-cubulation/`. Both new entries visibly retain 15 October 2026 publication dates.

## Deployment and unchanged content

Root deployed site commit `1ac93166e5ec6c5bdca063041a944d40b226ff86`, Firebase version `37049a29eef5fc3c`. Root's copied post-deploy HTTP receipt reports research HTML `Cache-Control: public, max-age=0, must-revalidate`; asset and blog policies remain unchanged. Its SHA-256 is `767fee2cf1371fe05138f5cfb12b9ca4d0a5dff95add104ed511f257dfad80a7`. The copied current live receipt passes all 11 byte-identity checks, SHA-256 `e10bbadb1cbbf96b80ed75adb7946769b54ddeb2c8d60a9cd6e95349b5d3e8ca`. These 11 local public files were independently rehashed against that receipt. The copied public index is 36784 bytes, SHA-256 `c6d8da8fbd377990cd07f5f957f03c22d1df7373f65f01025e3f01723990b005`. Header policy evidence and local file identity are separately identified; the browser did not capture response-body hashes.

Only root's hosting configuration changed. This worker made no website, source, shared-code, Git, Sheet, redirect, deploy, release, or outreach changes. The owned copies in `header-deployment-bindings/` preserve root's before/after header evidence and current index bytes without alteration.

## Preserved attempts and scope limits

The first mobile title-link attempts for reachability and Satoh left the index displayed. Those unchanged 44-entry states and screenshots remain recorded. They were not counted as successful article navigation; visible-coordinate clicks subsequently reached the actual article URLs before their Research returns were checked.

The new tab record named `mobile-fresh-direct-tab-index` actually measured 2056 × 1146, despite its intended action label. Its recorded dimensions control the assessment; it is a desktop observation. Mobile dimensions were then explicitly applied and verified. The distinct `mobile-fresh-direct-index-confirmed390` record verifies actual direct navigation from the reachability article at 390 × 844.

No cache clearing, storage manipulation, browser cache-policy setting changes, content fetch, or undocumented browser automation was used. No reload was used to conceal recurrence. The new session showed no 42-entry state, so no priming reload was necessary.

The earlier folder `verification/browser-reach-satoh-sol-20261025/` remains frozen with its original pending-freshness status and 42→44→42→44 history. All64 artifacts bound by its original manifest were rehashed unchanged. Original manifest SHA-256: `884a668b4e241f07987b5ada48b65fa47dd5f65673ad87e5b01088e015a93382`. This supplement addresses only the outstanding index freshness observation. It does not rewrite or claim to retest the original article/PDF/download evidence. In particular, no new PDF page-count or completed ZIP-download tests are claimed here.

## Cleanup and evidence

Both ephemeral tabs 963520661 and963520664 were closed. Protected Sheet tab 963520539 remains present and was never claimed. The earlier 390px override belonged to the first ephemeral tab, which was closed. The last remaining verification tab measured 2056 × 1146 before it too was closed; no user tab was claimed or resized.

Primary raw captures: `desktop-after-three-normal-returns.jpg` and `mobile-fresh-direct44-links.jpg`. Their originals and all four other captures are bound with exact dimensions, lengths and hashes in `screenshot-manifest.json`. Full raw DOM snapshots accompany each event and capture. `navigation-events.json`, `browser-assessment.json`, `source-and-deployment-bindings.json`, `original-frozen-batch-integrity.json`, and `cleanup.json` provide machine-readable evidence. The final `evidence-manifest.json` seals all owned files except itself.

## Full actual sequence

| UTC | Record | Actual viewport | Index count or article | Exact URL |
| --- | --- | --- | --- | --- |
| 2026-10-25T04:02:51.453Z | desktop-initial-normal-index | 2056 × 1146 | 44 | https://aleckriebel.com/research/ |
| 2026-10-25T04:03:00.156Z | desktop-reach-article-navigation | 2056 × 1146 | article | https://aleckriebel.com/research/binary-directed-chip-firing-reachability/ |
| 2026-10-25T04:03:04.177Z | desktop-research-return-from-reach | 2056 × 1146 | 44 | https://aleckriebel.com/research/ |
| 2026-10-25T04:03:11.468Z | desktop-satoh-article-navigation | 2056 × 1146 | article | https://aleckriebel.com/research/satoh-sl2-representation-filtration-counterexamples/ |
| 2026-10-25T04:03:14.569Z | desktop-research-return-from-satoh | 2056 × 1146 | 44 | https://aleckriebel.com/research/ |
| 2026-10-25T04:03:19.160Z | desktop-previous-cube-article-navigation | 2056 × 1146 | article | https://aleckriebel.com/research/aim-free-by-cyclic-two-cube-cubulation/ |
| 2026-10-25T04:03:22.849Z | desktop-research-return-from-previous-cube | 2056 × 1146 | 44 | https://aleckriebel.com/research/ |
| 2026-10-25T04:03:28.516Z | desktop-history-back-to-previous-cube | 2056 × 1146 | article | https://aleckriebel.com/research/aim-free-by-cyclic-two-cube-cubulation/ |
| 2026-10-25T04:03:43.866Z | desktop-history-forward-to-index | 2056 × 1146 | 44 | https://aleckriebel.com/research/ |
| 2026-10-25T04:04:04.705Z | desktop-history-reach-article | 2056 × 1146 | article | https://aleckriebel.com/research/binary-directed-chip-firing-reachability/ |
| 2026-10-25T04:04:07.627Z | desktop-history-back-to-index | 2056 × 1146 | 44 | https://aleckriebel.com/research/ |
| 2026-10-25T04:04:11.177Z | desktop-history-forward-to-reach | 2056 × 1146 | article | https://aleckriebel.com/research/binary-directed-chip-firing-reachability/ |
| 2026-10-25T04:04:14.732Z | desktop-fresh-direct-index-navigation | 2056 × 1146 | 44 | https://aleckriebel.com/research/ |
| 2026-10-25T04:04:20.096Z | mobile-index-at 390-before-normal-returns | 390 × 844 | 44 | https://aleckriebel.com/research/ |
| 2026-10-25T04:04:24.404Z | mobile-reach-article-navigation | 390 × 844 | 44 | https://aleckriebel.com/research/ |
| 2026-10-25T04:04:32.453Z | mobile-reach-click-settled-state | 390 × 844 | 44 | https://aleckriebel.com/research/ |
| 2026-10-25T04:04:44.399Z | mobile-reach-article-confirmed | 390 × 844 | article | https://aleckriebel.com/research/binary-directed-chip-firing-reachability/ |
| 2026-10-25T04:04:48.633Z | mobile-research-return-from-reach | 390 × 844 | 44 | https://aleckriebel.com/research/ |
| 2026-10-25T04:05:01.439Z | mobile-satoh-article-navigation | 390 × 844 | 44 | https://aleckriebel.com/research/ |
| 2026-10-25T04:05:08.368Z | mobile-satoh-article-confirmed | 390 × 844 | article | https://aleckriebel.com/research/satoh-sl2-representation-filtration-counterexamples/ |
| 2026-10-25T04:05:12.086Z | mobile-research-return-from-satoh | 390 × 844 | 44 | https://aleckriebel.com/research/ |
| 2026-10-25T04:05:25.054Z | mobile-previous-cube-article-navigation | 390 × 844 | article | https://aleckriebel.com/research/aim-free-by-cyclic-two-cube-cubulation/ |
| 2026-10-25T04:05:28.775Z | mobile-research-return-from-previous-cube | 390 × 844 | 44 | https://aleckriebel.com/research/ |
| 2026-10-25T04:05:52.762Z | mobile-history-back-to-previous-cube | 390 × 844 | article | https://aleckriebel.com/research/aim-free-by-cyclic-two-cube-cubulation/ |
| 2026-10-25T04:05:56.760Z | mobile-history-back-to-index | 390 × 844 | 44 | https://aleckriebel.com/research/ |
| 2026-10-25T04:05:59.438Z | mobile-history-forward-to-previous-cube | 390 × 844 | article | https://aleckriebel.com/research/aim-free-by-cyclic-two-cube-cubulation/ |
| 2026-10-25T04:06:02.193Z | mobile-history-forward-to-index | 390 × 844 | 44 | https://aleckriebel.com/research/ |
| 2026-10-25T04:06:11.721Z | mobile-fresh-direct-tab-index | 2056 × 1146 | 44 | https://aleckriebel.com/research/ |
| 2026-10-25T04:06:35.221Z | fresh-direct-tab-actual390-state | 390 × 844 | 44 | https://aleckriebel.com/research/ |
| 2026-10-25T04:06:35.732Z | mobile-direct-test-reach-origin | 390 × 844 | article | https://aleckriebel.com/research/binary-directed-chip-firing-reachability/ |
| 2026-10-25T04:06:41.268Z | mobile-fresh-direct-index-confirmed390 | 390 × 844 | 44 | https://aleckriebel.com/research/ |
