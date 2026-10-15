# Additive evidence-custody clarification

Recorded 2026-10-13T05:33:06.293438+00:00. This addendum changes no previously sealed file, source identity, source-access claim or scientific-priority assessment. It corrects the private-file count and clarifies the drafting/freeze timestamps.

## Correct private count: 43 files

A recursive enumeration of private_sources found **43 files with 43 distinct SHA256 hashes**. PRIVATE_SOURCE_HASHES.json contains **42 member records**, all present. The only actual file omitted from those member records is PRIVATE_SOURCE_HASHES.json itself. It was deliberately omitted from its own inventory to avoid a recursive self-hash.

Accordingly, the earlier final message's “42 excluded private files” was an inaccurate description of the total directory count. The correct description is **42 inventoried private payload files plus one private integrity inventory = 43 excluded private files**. All 43 are excluded from the public own-file allowlist. The additional counted file is our integrity inventory; it is not a newly recovered primary source or an additional third-party body.

PRIVATE_SOURCE_HASHES.json: 8,365 bytes; SHA256 `2119f79cbc4e1f7dc0614ba9888c095de6bac6d05c88d0169db25de2d52f4bc9`. Filesystem creation time is 2026-10-13T05:26:00.184431+00:00 and modification time is 2026-10-13T05:26:00.184674+00:00. It therefore existed **before** the final freeze at 05:27:04.647888 UTC, rather than being a post-freeze source artifact. The first final inventory's count of 42 member payloads and the later full directory count of 43 have this precise counting explanation.

## Distinct timestamps

The report header and SOURCE_READ_LEDGER.json retain drafting/checkpoint timestamp **2026-10-13T05:20:53.395842+00:00**. This is not the time when their final bytes became immutable. FINAL_HASH_INVENTORY.json and FINAL_SEAL.json record the final freezing event at **2026-10-13T05:27:04.647888+00:00**, following the final documentary-materiality clarification. The earlier header is preserved as historical data; this addendum identifies its meaning without rewriting it.

## New post-freeze own artifacts

This addendum, PUBLIC_OWN_FILE_ALLOWLIST_ADDENDUM_20261013.txt and CUSTODY_ADDENDUM_SEAL_20261013.json are newly created after the prior final freeze, solely to record this custody correction. They contain our analysis, safe file names and hashes. They add no primary-body download, extract, render or service payload. The updated safe allowlist is additive: it contains the previous eleven self-authored public artifacts plus these three own artifacts. The older allowlist and all earlier seals remain unchanged.

Before and after this addition, every pre-existing public file was checked byte-for-byte against its prior SHA256, and the first/final sealed payload hashes still match. Rootcase progress, campaign counts and the historical/contribution conclusions are unchanged. No external contact, remote write, Git action or delegation occurred.
