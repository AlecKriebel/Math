# Source-only custody: rows149,151,152

The three exact queued Zenodo records are acquired, safely inventoried and sealed. Each is its sole native version and latest record, a public publication/preprint with native state `done`. The `is_published` field is absent in all three records and remains explicitly absent; no value has been inserted. Each creator is `Kriebel, Alec`, affiliation `Independent researcher`, ORCID `0009-0001-9320-500X`. Each native license object is exactly `{"id":"cc-by-4.0"}`. README/code grants have not been inspected or inferred.

| Row / record | Native version | Original publication date | Native created | Native updated |
|---|---|---|---|---|
|149 /23332261|`1.0.0`|2026-10-12|2026-10-13T05:12:09.360305+00:00|2026-10-13T05:12:10.139650+00:00|
|151 /23573603|`1.0.0`|2026-10-22|2026-10-22T17:57:59.433479+00:00|2026-10-22T17:57:59.799057+00:00|
|152 /23191247|`1.0`|2026-10-06|2026-10-06T14:46:33.214104+00:00|2026-10-10T21:28:59.670909+00:00|

Exact native titles were guarded against the queue: *A Martin kernel with isolated Harnack contact in an annulus*; *A supercritical nonuniqueness example on a graph roughly isometric to the square lattice*; and *A telescoping proof of the focal antipedal sum invariant*. Native record IDs/DOIs, creator/ORCID, concept-family association, latest and complete version enumeration were checked without normalizing original metadata. Whole Description values are present and preserved unchanged in `ACQUIRED.json records[].description_whole_field` and the raw API response bodies, with original presence/value wrappers for versions, license and native publication fields. Description UTF-8 byte counts are1645/3216/1533; these are not abstract substitutions or mathematical endorsements.

All six native assets were acquired by ordinary public Zenodo HTTPS GET. Per work, raw response bodies, actual status and ordered response/request headers are retained for the exact record, latest redirect chain, complete versions endpoint, files endpoint and ordered asset downloads. There were21 complete responses:18 HTTP200 and3 ordinary native HTTP301 redirects. No HTTP request failed, no bypass/retry campaign was used, and no cached asset replaced a fresh GET. Expected absence probes for the new workspaces returned absence before exclusive creation; no preexisting packet was changed.

The native asset order is PDF then ZIP for each work. Sizes and native MD5 checksums all match:

| Row | Native filename | Bytes | Native MD5 |
|---|---|---:|---|
|149|annular-martin-kernel-note.pdf|64878|58b8ab4db0eb4d306d87eb225358fd22|
|149|annular-martin-kernel-verification.zip|190305|b23e788ceafc75dda0f5b9a6fc2b811d|
|151|supercritical-nonuniqueness.pdf|67272|750c37c873e02ab039596be692b3aac8|
|151|supercritical-nonuniqueness-source-and-verification.zip|103935|7ca9141233a1c0b18fd116061729a0d7|
|152|focal_antipedal_sum.pdf|65142|2557525eabb46e57ddece9d49cd0b4b4|
|152|focal_antipedal_sum_support.zip|113446|49694a21bd623ce1337ca4dafda9cf8f|

ZIP member order/names, sizes, CRCs, compression flags, timestamps, modes, extracted paths and exact SHA256 pins are recorded without executing any source. Four row149 containers were inventoried: the native ZIP and three depth1 ZIPs named `FUNCTION_THEORY_2307042_AUTHOR_SAFE_FREEZE.zip`, `FUNCTION_THEORY_2307042_INDEPENDENT_AUDIT_SAFE.zip`, and `FUNCTION_THEORY_2307042_SECOND_ADVERSARIAL_REVIEW_SAFE.zip`. Their bodies/opinions remain unread. The total is six containers and142 regular member occurrences:91/18/33 per work. No special/link/path-escape member was accepted. All nested copies are in the finite manifest; nothing is silently excluded as an old review or presumed duplicate.

Actual manuscripts and sole TeX candidates, identified structurally rather than by scientific reading:

| Row | Actual native PDF | Pages from pdfinfo | Sole controlling-source candidate within published ZIP |
|---|---|---:|---|
|149|assets/annular-martin-kernel-note.pdf|5|published-source/container-001/tree/preprint/note.tex;12513B,171 opaque byte-lines|
|151|assets/supercritical-nonuniqueness.pdf|5|published-source/container-001/tree/supercritical_nonuniqueness_source/main.tex;16869B,323 opaque byte-lines|
|152|assets/focal_antipedal_sum.pdf|4|published-source/container-001/tree/focal_antipedal_sum.tex;12111B,255 opaque byte-lines|

Rows151/152 also contain an archived PDF with exactly the native PDF's bytes/SHA256. Row149 has no other actual PDF in any nested archive. These are filename/sole-version-candidate associations, not a build correspondence assertion. Five total PDF occurrences were inspected only with `pdfinfo -isodates`, all exit0; no extracted manuscript text or pixels were read. Printed dates/versions and source/README/code/result/opinion content remain uninspected.

The new21204B adapter `acquire_sources.py`, SHA2560157f60e864559765d443c904e19ee1f6dd7e8541a3c1bffe88b9a09e1e9b0f9, was completely read before its first invocation. The old20747B4027e8b8 helper was a static reference only. Three acquisitions and three exclusive seals exited0 with empty stderr. One combined genuinely read-only default verification exited0 with empty stderr (59cd2a), checking every finite source pin and all native MD5s. No old collector, native science program, builder, release mechanism or optimized route ran.

Source roots are `papers/23332261/sources`114files/20child directories, `papers/23573603/sources`43files/6directories, and `papers/23191247/sources`58files/6directories. Their finite manifests exclude exactly the two terminal names `SOURCE_MANIFEST.json` and `SOURCE_FINAL.json`; there is no future/subtree carveout and no postseal source write is authorized. Full early reader paths/pins/counts are in `SOURCE_HANDOFF.json`16182B SHA256c035e569956f18db977e7610a5930e0b425a09b549336545a0f47e18a1891ed4.

Literal schemas: ACQUIRED=`source-only-native-acquired-v1`; SOURCE_READY=`source-only-ready-unread-science-v1`; SOURCE_FINAL=`source-only-final-v1`; source manifest=`finite-source-manifest-v1`. Reader arrays are `SOURCE_READY.actual_PDF_readers`, `all_TeX_candidates`, and `source_associations`; full native objects are in `ACQUIRED.records`, `all_native_assets`, `containers`, `members`, and `actual_HTTP_receipts`. No alias such as `selected_actual_PDF` is invented.

Source custody is100% complete. Scientific verdict, follow-up and public canonical URL are null; no scientific clearance, promotion, DOI/release creation, outside communication or prepared outreach occurred. Previous146–148 packets and all W/Git/Sheet/deployment/core files remain unchanged. Scientific readers may now begin from the sealed bytes; this source lane remains mathematically unread.
