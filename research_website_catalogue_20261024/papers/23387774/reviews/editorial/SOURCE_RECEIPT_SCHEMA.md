# Preserve the exact cylinder source-receipt shape

The authoritative file is `sources/receipt.json`, SHA256 `c18de70258995903a5118cb065c0ddcec13bd9fcab9d09a54c5796ca3fb53b0b`. The verbatim copy in this packet is `source-receipt.original.json`.

It is the complete original ready-shaped object. Its actual asset arrays are `exact_assets` and `selected_PDF`. Every asset retains its complete `file_object` with API `id`, `key`, `size`, `checksum` and original `links`; the separate original `path`, byte/hash/checksum-pass fields and provenance remain present. The record title, DOI, version, declared publication date, created/updated timestamps, candidate comparison, archive facts, TeX path and source-change/read-boundary fields also remain intact.

There is no `files` property. Do not add one to make this source fit a legacy consumer. Do not rename `file_object.key` to a stored `name`, rewrite its actual link as a stored `url`, or invent an HTTP `status`, MIME type or response header. The real transport receipt is the unchanged `sources/api-receipt.json`; it must be treated with its own original `requests` shape and actual recorded facts.

`publication.json` retains the complete object under `source_binding.source_receipt_original`; `promotion.json` retains it under `source_receipt_original`. They are semantic copies of the entire original object, with exact original-byte copies and hashes alongside. Neither stored object is a normalized asset view. The original source remains unchanged.

A later authorized consumer may validate the receipt and each original asset against its pinned hash and actual API file object, then derive a temporary view in memory for its own needs. That would be a consumer adapter, not a repaired or newly interpreted source receipt. This handoff implements no adapter and changes no shared core.

The selected reader is the complete separate seven-page `cylinder_areas.pdf`; the complete support is the original outer ZIP. No PDF is embedded in that ZIP. The selected-record DOI, declaration date and creation timestamp retain their separate meanings.
