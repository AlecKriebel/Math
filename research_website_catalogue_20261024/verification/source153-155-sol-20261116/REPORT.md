# Source-only custody report: rows 153–155

All three exact queued records are acquired and sealed. Each is a native public publication/preprint with state `done`, its sole enumerated version and latest record. The native `is_published` field is absent in all three and remains explicitly absent. Creator: `Kriebel, Alec`; affiliation `Independent researcher`; ORCID `0009-0001-9320-500X`. All native license objects are exactly `{"id":"cc-by-4.0"}`. Source/code/README rights statements have not been read or inferred.

| Row / record | Native version | Original publication date | Native created | Native updated |
|---|---|---|---|---|
|153 / 23444050|`1.0.0`|2026-10-17|2026-10-18T00:29:32.173838+00:00|2026-10-18T00:29:32.631863+00:00|
|154 / 23334001|`1.0`|2026-10-13|2026-10-13T06:36:40.403085+00:00|2026-10-13T06:36:41.078509+00:00|
|155 / 23394004|`1.0`|2026-10-15|2026-10-15T11:39:15.137334+00:00|2026-10-15T11:39:15.430611+00:00|

Native titles were checked exactly against the queued work-specific titles. Complete native original Description strings are present and retained in `ACQUIRED.records[].description_whole_field` and raw API response bodies, without summarizing or normalizing them. Their UTF-8 byte counts are 2443, 1372 and 1917. Original dates, version/license presence and value, resource type, complete native file objects and order are retained. Printed manuscript dates/versions remain uninspected.

There were 21 complete ordinary Zenodo HTTPS responses: 18 HTTP 200 and three native HTTP 301 latest redirects. Record, latest, all versions, files and asset responses include durable original bodies plus actual method/status/ordered header receipts. No request failed, no bypass/retry campaign was used, and no cached asset replaced a fresh GET. No source program or scientific helper ran.

All six assets match native sizes and MD5s. Each actual queued PDF also matches the root-supplied whole SHA256. Native file order is PDF then ZIP for row 153, and ZIP then PDF for rows 154 and 155:

| Row | Ordered native filename | Bytes | Native MD5 |
|---|---|---:|---|
|153|mixed-kato-counterexample.pdf|71463|ebf0be4da8fa825886d3d536e252e750|
|153|mixed-kato-counterexample-source-and-verification.zip|372851|db4dc2dcdac594c6cb6244b015004d41|
|154|odd-origin-area-product-verification.zip|170660|be84f24ca1c162c04139f490210ddd97|
|154|odd_origin_area_product.pdf|70407|41d81f3a257963151df69268eccf99d4|
|155|k904a-source-verification.zip|396642|a963325d2840d33d6b6906e890ab7807|
|155|k904a-outer-focal-inverse-areas.pdf|76736|8b04ff0d06a26d835a8f14957c8dcf10|

All three ZIP containers were safely inventoried and extracted, including a recursive nested-container check. There are no nested containers in the actual assets. All 344 regular member occurrences (143, 50 and 151) have original member order/name, size, CRC, mode, timestamps/compression flags, extracted path and whole SHA256 recorded. No special/link/path-escape member was accepted. File/code/result/opinion bodies were not interpreted.

All actual PDFs and TeX candidates are enumerated. Each work has exactly one version-specific TeX candidate, associated structurally by matching basename or sole candidate, without claiming a build correspondence:

| Row | Native PDF in `sources/assets` | Pages from pdfinfo | Sole TeX candidate below `sources/published-source/container-001/tree` |
|---|---|---:|---|
|153|mixed-kato-counterexample.pdf|4|main.tex; 13263 bytes, 299 opaque byte-lines|
|154|odd_origin_area_product.pdf|5|odd-origin-area-product-verification/paper/odd_origin_area_product.tex; 16257 bytes, 367 opaque byte-lines|
|155|k904a-outer-focal-inverse-areas.pdf|6|k904a_outer_focal_inverse_product/manuscript.tex; 19125 bytes, 229 opaque byte-lines|

Row 153 also contains `output/pdf/mixed-kato-counterexample.pdf`, and row 155 contains `k904a_outer_focal_inverse_product/manuscript.pdf`, both byte-identical to the respective native PDF. Row 154 has no archived PDF. Five PDF occurrences received only `pdfinfo -isodates` metadata checks, all exit 0; no PDF text/pixels or TeX body was read. There are 15 native manuscript pages, or 25 pages counting the exact archived PDF copies.

The current 21742-byte fixed helper, SHA256 `9b6b2266825c4199d4bb03b028e529a5cc2e58271bbe08ef768209e0ae00e84b`, and the exact 3041-byte delta, SHA256 `eb2cfd2a13a861e210bf499116e7424bed2b2fe87de7564fc1adf1fb8ec12187`, were personally read in full before the first execution. The previous 21204-byte helper was a static reference only. The adaptation changes only the new namespace/mapping and the supplied PDF filename/SHA binding guard; no old collector was called. Three acquisitions, three exclusive seals and one combined genuinely read-only custody invocation exited 0 with empty stderr. The final read-only run (afde9f) checked every finite payload pin and every native asset MD5 without source writes.

Source extents are 168 files / 21 child directories for `papers/23444050/sources`, 73 / 15 for `papers/23334001/sources`, and 176 / 24 for `papers/23394004/sources`. Their finite manifests exclude only the exact terminal names `SOURCE_MANIFEST.json` and `SOURCE_FINAL.json`, with no future/subtree carveout. All source writes finished before early handoff. `SOURCE_HANDOFF.json` is 26958 bytes, SHA256 `50c1ebd84282b551af1e5c00545016ddfe4a9f0613248f86e8423ea50001e469`, and binds all reader paths, native metadata, associations and actual source seals.

Literal schemas: ACQUIRED `source-only-native-acquired-v1`; SOURCE_READY `source-only-ready-unread-science-v1`; SOURCE_FINAL `source-only-final-v1`; source manifest `finite-source-manifest-v1`. Reader fields are `actual_PDF_readers`, `all_TeX_candidates` and `source_associations`; full original objects are in `ACQUIRED.records`, `all_native_assets`, `containers`, `members` and `actual_HTTP_receipts`.

Source custody completion is 100%. Scientific bodies, code/results, README/review opinions and root scientific findings remain unread. Scientific verdict, follow-up, AA and canonical URL are null; no promotion, scientific/native execution, DOI/release, outside contact or prepared outreach occurred. All old packets, other papers, W/Git/Sheet/core and deployment remain unchanged. These sealed bytes are ready for independent source-first readers. This source lane waits for further assignment.
