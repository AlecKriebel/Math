# Research index delivery diagnosis

**Outcome:** No current HTTP delivery or Firebase route/header fault was reproduced. The browser's recorded 44 → 47 → 44 sequence remains an unresolved user-visible failure; passing fresh HTTP checks does not close it. No website, deployment, browser setting, Git, spreadsheet, or source change was made.

## Bound evidence

The site checkout stayed on `main` at `0d7d9ffa0eef70309fb8e6425a42ebf21841548a`, matching the preserved successful deployment receipt for Firebase version `fa6309f827fd05fd`. Its research index has 47 entries, 39,069 bytes, SHA-256 `2f18693557c91c0d36af93a87dbc784ac57b07212ae9e5861b60d8a7132f0ed3`.

At 04:23:15–04:23:17 UTC on 25 October 2026, six ordinary starting GETs and six otherwise-identical `Cache-Control: no-cache` starting GETs tested these routes:

| Route | Both modes |
| --- | --- |
| `/research/` | 200; exact current 47-entry index |
| `/research/index.html` | 301 to `/research/`; exact current index |
| `/research` | 301 to `/research/`; exact current index |
| Braid article: canonical slash, explicit `index.html`, extensionless | Canonical 200; both aliases 301 to canonical; exact local article bytes |

Every redirect and final HTML response has `Cache-Control: public, max-age=0, must-revalidate`. Index final responses have ETag `"fbbb92389da596bb0c803131284e6c267895e51cc0f641cc4b8e662e87212502"` and Last-Modified `Sun, 25 Oct 2026 04:19:59 GMT`. Ordinary and no-cache bodies match; the response headers include `Vary: x-fh-requested-host, accept-encoding`. The observed edge identifiers are PAO. These are fresh Python HTTP requests with no local HTTP cache, rather than ordinary browser navigation.

Nine follow-up starting GETs at 04:23:57 UTC address the observed validators and encoding variation:

- Current ETag → 304, empty body, correct revalidation policy.
- Historical 44-entry ETag → 200 with the current 47-entry body, both ordinary and no-cache.
- Historical Last-Modified, and historical ETag plus Last-Modified → current 200.
- Gzip ordinary and no-cache → byte-identical current HTML after decompression.
- Article-referrer/document-navigation header variant → byte-identical current gzip HTML.
- Firebase default hostname `/research/` → byte-identical current HTML.

This is 21 starting requests and 29 wire GET hops. `http-probe.json` and `variant-probe.json` preserve request headers, every response/redirect header, timestamps, bodies and hashes. `checks.json` validates the receipts and unchanged site inputs. No repeated requests were needed for validation.

## What the saved browser evidence establishes

The browser owner's records show canonical `/research/` at 04:20:52.944 UTC with 44 entries, a normal reload at 04:20:58.691 with 47, and the braid article's actual Research-link return at 04:21:24.510 with 44 again. The ordered 140 captured anchor href/text pairs in both 44 states exactly match the historical `4b19ea12` index. The reload's 149 pairs exactly match current HEAD. This is stronger than an entry-count comparison, but it is not a raw browser response-body hash or network trace. Original browser artifacts were only read and remain unchanged.

The archived HTTP response at 03:57:22 GMT independently documents that the same 44-entry index was served with `max-age=3600` before the header repair. Its body hash is `c6d8da8fbd377990cd07f5f957f03c22d1df7373f65f01025e3f01723990b005`; its ETag is `"b727a72ae4a32064af5c3f465815cec24469f023fbb36553c936530080e24f9f"`. The current source has only non-executable JSON-LD on the index, and a current-public-source scan finds no service-worker/cache code. That scan does not inspect browser-internal state.

## Interpretation and recommendation

An old browser-stored response acquired under the one-hour policy is compatible with a 44-entry navigation during this time window. [Firebase documents](https://firebase.google.com/docs/hosting/manage-cache) that cache reuse depends on hostname, path, query and `Vary`, and that deployments clear its CDN's static-content cache. Neither this documentation nor these fresh requests proves which stored response Chrome selected. In particular, old caching alone does not establish why the successful reload was followed by an older navigation.

**Recommendation: retain the deployed revalidation rule; no additional source/configuration patch or redeploy is justified by these receipts.** The rule covers the canonical and alias routes and live responses apply it correctly. A proposed `no-store` change would not retrospectively revoke an already-stored old response, so it would not constitute a demonstrated repair of this recurrence.

The remaining acceptance check belongs to the browser owner: preserve ordinary article → Research navigation after the old one-hour freshness window has elapsed; if it recurs, capture the actual navigation's request/response/cache-source information alongside the DOM. Until that evidence exists, keep browser freshness acceptance open and do not describe the exact cause or the UI fix as verified. No browser network headers were captured or inferred here.

Bounded diagnosis completion: **100%**. Exact browser mechanism identified: **30%**. Findings and receipts are sealed by `SHA256SUMS`.
