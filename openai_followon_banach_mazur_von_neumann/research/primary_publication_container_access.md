# Publisher-container and authorized-format access check

Checkpoint: 2026-10-06 22:47 PDT (2026-10-07 05:47 UTC).
Researcher: internal independent access agent. No outside individual was contacted.

**Outcome:** No complete journal article or author manuscript was obtained. The bounded, materially different publisher-container route is complete (100% of this assigned route exploration); retrieval and reading of the mandatory complete article remain 0% complete. These estimates are scoped to this access subtask, not mathematical resolution or publication-package completion. The published-text dependency gap is unchanged.

Target: Jean Roydor, *Banach–Mazur stability of von Neumann algebras*, *Journal of Topology and Analysis* 14(03) (2022), 767–792, DOI [10.1142/S1793525321500151](https://doi.org/10.1142/S1793525321500151). Complete article bytes: none. Article version/hash: unavailable. This report does not certify the journal theorem or proof.

## New evidence

The following publisher container candidates were requested once through ordinary HTTPS. They were not alternate article endpoints, credentials, proxies, or access-control workarounds. The issue URL follows the publisher's conventional table-of-contents structure; because retrieval failed, its actual contents were not independently checked.

| Requested URL | Request time UTC | Outcome | Response bytes / SHA-256 |
|---|---|---|---|
| [Issue 14/03 candidate](https://www.worldscientific.com/toc/jta/14/03) | 2026-10-07 05:45:36.933285 | HTTP 403, `text/html; charset=UTF-8` | 5,538 / `cc7f366366a6be1f26310980c4f2423049af8ccaffd807f3c9e7f0fe0909e032` |
| [Journal issue-list candidate](https://www.worldscientific.com/loi/jta) | 2026-10-07 05:45:37.023791 | HTTP 403, `text/html; charset=UTF-8` | 5,498 / `145022d590ab74ae4d07de51a97c291c679c96f1c504df0b49d4ee906e2f2565` |

The hashes in this table identify error-response bodies, **not article bytes**. The web-reading tool also returned an internal error for both URLs. No issue-level contents, full-issue download link, article text, or proof was recovered. No further publisher-container requests were made after the same genuine access barrier was observed.

For authorized machine-readable formats, the previously retained publisher-deposited [Crossref record](https://api.crossref.org/works/10.1142/S1793525321500151) was inspected locally, rather than downloaded again. Its exact saved bytes have SHA-256 `f95ac0c2b0de6b22bfa50e6e61f17756afb77a7b9d5646df3882565812929711`. The sole deposited content link is the existing World Scientific PDF, marked `content-version: vor`, `content-type: unspecified`, and `intended-application: similarity-checking`. There is no deposited `text-mining` content link, license field, alternate XML/full-text format, or relation pointing to a manuscript in this saved record. A similarity-checking link does not establish public text-mining authorization. Its article PDF was already blocked in the earlier audit, so that URL was not retried by this agent.

Public indexed discovery for publisher documentation used the following new queries: `site:worldscientific.com/toc/jta/14/03`; `site:worldscientific.com text and data mining API full text Crossref`; `"World Scientific" "text and data mining"`; `"Journal of Topology and Analysis" "14" "03" "2022" World Scientific`; `"World Scientific" "TDM" "API"`; `"World Scientific" "Crossref" "text mining"`; and `"worldscientific.com" "Full Issue" "jta"`. No returned result provided a publisher-documented public text-mining endpoint or complete issue/manuscript link for this target. This finite failed discovery is not proof that such a service or manuscript does not exist.

One primary result was the publisher's [institutional user license](https://misc.worldscientific.com/cgi-bin/userlicense/userlicence.cgi), whose indexed text permits subscribers and authorized users to download for private research. That result concerns licensed access; it supplies neither current credentials nor a public complete article route. No account, institutional entitlement, purchase, or request to another individual was assumed or initiated.

## Scope and exact remaining gap

The earlier individual-article browser/security check, EBSCO sign-in route, HAL, OpenAlex, ORCID, current/archived author profiles, CORE, Oskar, Semantic Scholar, and CIRM slide checks were not repeated. No speculative private storage URL, unlisted machine endpoint, CAPTCHA bypass, paywall bypass, or security workaround was attempted. No new author-associated institutional repository candidate emerged from this bounded publisher-container search; none was invented or searched merely to repeat prior absence evidence.

The next advance requires a materially new **authorized complete primary text** or an actual accessible complete manuscript link. Once obtained, the exact journal theorem, cochain and field conventions, general/nonseparable scope, canonical-predual argument, and handling of the intermediate type-I restriction must be read and independently checked. A complete abstract, bibliographic record, or the already obtained author slides does not meet that condition.

Derived request metadata is retained locally in ignored `sources/archival/publisher_container_access_20261007.json` and `sources/archival/publisher_container_crossref_link_audit_20261007.json`. Error bodies were hashed in memory and not saved. No third-party article content was retrieved or added to the publication payload. No Git action was taken, and no manuscript or frozen review was altered.
