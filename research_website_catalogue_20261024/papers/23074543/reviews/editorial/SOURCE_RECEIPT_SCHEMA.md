# Discotope source receipt: retain actual_assets exactly

The authoritative file is `sources/receipt.json`, SHA256 `4df529a4809b294fc7e623ff45e66309537bd0f45b2c0110bc83a1d7e9e6122d`. `source-receipt.original.json` is a verbatim byte copy. Both configurations embed the complete object without changing any field shape or value.

Its asset property is **actual_assets**. Each entry retains its complete actual `file_object` with API `id`, `key`, `size`, `checksum` and original `links`, together with the original `path`, `bytes`, uppercase `MD5`, uppercase `SHA256`, recorded checksum flag and selected PDF page count where originally present. The record identity, dates/version, candidate comparison, member count, expanded bytes, both original TeX locators and source-change field remain intact.

There is no `files` property and no cylinder `exact_assets` or `selected_PDF` property. Do not add any of them to fit a legacy consumer. Do not rewrite file-object keys into stored `name` or `url` aliases or invent HTTP status, MIME type or header facts. The real transport evidence is the unchanged original `sources/api-receipt.json`, which has its own original list shape and actual recorded facts.

A later explicitly authorized consumer may authenticate the whole original object and each asset against its pinned actual API object/bytes, then derive a temporary in-memory view for its own needs. That would be a consumer adapter, not a repaired source. No adapter, asset projection or shared builder has been implemented here.

The selected reader is `paper.pdf`, the actual four-page current manuscript. The historical five-page `verification/source_snapshot/proof.pdf` remains a different authored document inside the unchanged complete archive. The selected-record DOI and exact edition/creation dates retain their separate meanings. All three complete custom verdict objects are likewise preserved, not normalized to a default PASS.
