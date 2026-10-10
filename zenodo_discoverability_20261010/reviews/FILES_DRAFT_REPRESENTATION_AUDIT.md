# Independent live audit: public/draft file representation

Checkpoint: 2026-10-10 14:21 PDT. Estimated completion of this assigned representation audit: **100%**. Only two authenticated GET calls were made using the effort's `PacedClient`; no remote mutations.

**Result:** the staged draft preserves every file field except generated entry links, which are absent. The full current public file object also remains exactly equal to the original public baseline in `receipts/23271172/before.json`.

## Exact differences

The raw native public/draft file objects and recursive differences are saved in `FILES_DRAFT_REPRESENTATION_COMPARISON.json`, with retrieval time and GET-only methods.

- `files.entries.k108_counterexample.pdf.links` exists publicly and is absent in the draft: `self`, `content`, `iiif_canvas`, `iiif_base`, `iiif_info`, `iiif_api`.
- `files.entries.k108_counterexample_support.zip.links` exists publicly and is absent in the draft: `self`, `content`, `container`.

There are **no other differences**. Both retain `enabled=true`, `order=[]`, `count=2`, `total_bytes=187711`, exactly the same entry names/key fields, file UUIDs, MD5 checksums, sizes, extensions, MIME types, storage class, per-file metadata and access flags. The PDF's width/height remain 612/792; both file `hidden` flags remain false.

## Why link-only normalization is appropriate

Official Invenio defines file content/identity fields separately from dynamically generated endpoint links. The file schema includes UUID/checksum/size/type/storage/key/metadata/access data and no stored links field; `WithFileLinks` builds self/content/IIIF/container endpoint links from service routing and record/draft context. This supports treating links as representation data rather than uploaded bytes or editable file metadata. [File schema](https://raw.githubusercontent.com/inveniosoftware/invenio-rdm-records/fc3cd3fc88175f1845b40176763c551f984e0232/invenio_rdm_records/services/schemas/files.py), [Dynamic file-link configuration](https://raw.githubusercontent.com/inveniosoftware/invenio-rdm-records/fc3cd3fc88175f1845b40176763c551f984e0232/invenio_rdm_records/services/config.py). Pinned source snapshots and hashes are in `files_source_snapshots/manifest.json`. These official sources are not a claim to identify the exact deployed build; the live observation supplies the actual difference here.

## Narrow safe staged invariant

For the staged pre-publication comparison, deep-copy both full file objects and remove **only** each `files.entries[filename].links` field. Require exact equality of the resulting objects. This requires the exact file set, identities, checksums/sizes, counts/total bytes, order/default-preview/enabled state, file metadata and access to stay unchanged. Reject any other difference. Do not merely compare counts or omit all file metadata.

Keep the original full public file baseline untouched. Immediately before publication require the live public full file object still equals that baseline; after metadata publication require **exact full public file equality**, including every original generated link. Continue the separate legacy checksum/size/file-name and record/DOI/version invariants. The normalization applies only when comparing staged draft versus public representation, never to the final public equality test.

No code, draft, record, DOI, version or deposited file was changed by this reviewer.
