# CPT institutional access follow-up: precise limit

2026-10-04 UTC. Zero central proof attempts. **No full Nencka body acquired. Historical ordinary-closure priority remains UNRESOLVED.**

New primary entry points were followed directly:

| Route | Actual outcome | Limit |
|---|---|---|
| [CPT historical FindPreprint page](https://www.cpt.univ-mrs.fr/~vittot/FindPreprint.htm) | HTTP200, 14,862 bytes; authenticated its ordinary library/publication link. | Page itself is a locator, not the requested manuscript. Credential-bearing historical links and authenticated forms were not used. |
| Linked Alexandrie library endpoint, `/documentation/biblio.html` | HTTP404 under both HTTP and HTTPS. | No public catalog body or search interface was returned. No guessed replacement endpoint or authentication bypass was used. |
| [Current CPT publications](https://www.cpt.univ-mrs.fr/fr/research/publications/) | HTTP200, 17,938 bytes, normal public bibliography with HAL/DOI/arXiv links and338 pages. | This is a current selected institutional bibliography; its coverage of historical CPT reports is not certified. |
| Relevant-period publication pages322–330 | All nine actual pages returned HTTP200 and were fully parsed as displayed text. Page322 spans2000/1999; pages323–324 include1999,325 includes1999/1998,326–327 include1998/1997,328–329 include1997/1996,330 includes1996/1995. | No Nencka/Cantorian/3381/braid/Artin whole-word target match appeared in these displayed records. This is bounded retrieval evidence, not proof of bibliographic absence or manuscript invalidity. Year-token ranges can contain journal-name ranges and bibliographic numbers; they are navigation aids, not exact catalog date guarantees. |
| [Current CPT visible site search](https://www.cpt.univ-mrs.fr/fr/search/) | Unauthenticated Chrome/CUA search for author produced5 fuzzy matches; title-word search produced14. Expanded both result batches until all14 were visible. | Displayed results matched `ne`, `NeV`, `can` and unrelated names, yielding no usable target record. These fuzzy results do not identify a full historical preprint or establish absence. |

Page323 initially failed to save because of a transient local no-space error; its empty artifact was not treated as a successful source read. A single18,169-byte retry succeeded at01:56:13 UTC, and the full saved page was inspected. The initial folder creation had also failed with no space; only this auditor's earlier unnecessary44,853,132-byte AMS Notices download was removed, leaving its prior access URL/hash record intact. No other agents' files or research findings were deleted.

Actual HTTP response captures and SHA256/timestamp records are confined to ignored `private/`, with the source request helper and `private/commands/source_access_*.json`. `private/catalog_scan_summary.json` records the final nine-page inspection, and `private/cpt_search_observed.txt` records the visible browser searches. Private ignore status was directly checked.

The new CPT route therefore did not supply the missing definition/model/proof from CPT96/P.3381, the1998 MFAT article, or the1999 AMS chapter. The earlier authenticated source identities and priority hold remain exactly as before. No exhausted exact-title HAL/INSPIRE searches were repeated. The separately assigned mp_arc route was left to the parent.

No external person was contacted. No credentials used, authenticated form submitted, access barrier bypassed, or Git/index/ref/remote/PR/queue/Zenodo/Sheets state changed. The current v3 theorem/package was neither read for revision nor edited by this follow-up.
