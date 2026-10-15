# PR623 native transport author report

Assigned offline adapter work is complete. **Author checks pass: 25 tests, zero failures. No live mutation was made.** Independent adversarial review and the live file lifecycle remain outside this author's validation.

`native_transport.py` subclasses the repository `ZenodoClient` and passes it to `zenodo.run`. The repository kit still loads the original manifest, checks exact metadata, checks the complete file set and MD5/size, performs final publication readback, checks DOI resolution, and writes the normal publication receipt. The adapter adds downloaded SHA-256 verification of every completed native file. The receipt therefore retains the required environment/title/id/state/DOI/record URL/DOI-resolution/receipt-saved fields and each file's name, size, and SHA-256. Tests exercise that actual kit code; they do not manufacture receipt schemas.

## Exact permitted scope

- Production, own recovered initial draft **23356540**, and version DOI **10.5281/zenodo.23356540**.
- The original manifest and reviewed PDF/ZIP bytes only. The CLI hashes the kit and all inputs before dispatch. No sandbox/generic record/manifest arguments exist.
- Authenticated GETs use the kit token loader and client transport. Native record reads explicitly request `application/vnd.inveniordm.v1+json`; full native metadata is checked against the recovered snapshot hash before its reversible projection is exposed to the kit. The exact original metadata is already present, so `update()` re-reads and verifies; it makes no PUT.
- File initialization POST, reviewed-file content PUT, file commit POST, and publish POST are the only mutating routes. They are pinned to known HTTPS host, ID, filenames, and paths. Direct `request()` mutations cannot bypass durable operation intent. Creation, deletion, editing, new versions, metadata PUTs, other records, and account search are unavailable.
- The CLI requires existing kit state for this recovered ID and an explicit execution switch with the exact confirmation ID for stage/publish. Those switches are an execution guard for the parent; this author never enabled or ran them.

## Evidence

The read-only preflight completed at **2026-10-14T04:18:32.814076Z** with exact native metadata, `submitted=false`, no completed files, and no pending files. That is a transport preflight, **not** a ready-to-publish or publication receipt. Earlier authenticated reads produced the filtered `native_shape.json` and `native_files.json` fixtures. They exclude account-owner/grant data and tokens.

The 25 offline tests cover ordinary initialization/content/commit, exact metadata projection and rich/drifting native metadata rejection, only-known-ID/host/path guards, disabled writes, missing-state/no-create behavior, duplicate/foreign file guards, unexpected status, MD5/size/SHA-256 drift, bounded binary read/no redirects, lost initialization/content/commit/publication responses, partial uploads, restart without repeated PUT, HTTP-200 transfer errors, durable journal failure before a mutation, publication readback, repeated publication as read-only, wrong version DOI, and publication receipt persistence failure.

## Ambiguous outcomes

Each mutation has an atomically saved `attempted` marker before the request. The same operation is never issued twice automatically, even after restart. A lost initialization can advance only if its registered key is read back. A lost commit can advance only if the completed native file is read back with exact size/MD5 and downloaded SHA-256. A lost publication is resolved by the kit's independent native record readback; a still-unpublished record does not trigger another POST. A later published read can recover the usual kit receipt.

A validated acknowledged content PUT permits the reversible commit, followed by exact committed-file verification before publication. A lost PUT requires an independent SHA-256 read of pending staged content. **If Zenodo cannot expose pending content, or exposes partial/different bytes, the runner stops with its durable `attempted` marker and does not repeat PUT or commit.** No automatic delete/reupload/reconciliation escape hatch exists. Manual reconciliation would require separately reviewed evidence and work.

## Remaining limits

1. This author has not performed a native initialize, content PUT, commit, or publish against production. The documented file endpoint sequence and current empty-file/metadata read shape are verified; deployed write response shape, pending-download availability, and postpublication representation remain live boundaries.
2. The runner deliberately fails closed on unexpected file/metadata/access/DOI representations, including vocabulary-annotation drift, foreign pending keys, additional file metadata, or record-versus-file collection discrepancies. A safe stop needs review of filtered read evidence; changing the manifest, simplifying metadata, replacing the deposit, or suppressing checks is not supported.
3. The local lock protects only this runner on this filesystem. It cannot prevent browser/other-machine edits between a read and an action. Every transport mutation rechecks the record where relevant, and final publication still requires exact file/metadata readback, but there is no claimed server-atomic transaction.
4. A DOI resolver failure remains separate from confirmed publication, using the kit's existing semantics. The dependent integration should require its already-reviewed successful DOI-resolution and durable-receipt fields.

The parent's newly independent adversary must review this source and failure evidence before live execution. Full downloaded primary sources are in ignored `tmp/`; `SOURCE_RECEIPT.json` records their URLs/hashes. Source endpoints are documented in the official [InvenioRDM reference](https://github.com/inveniosoftware/docs-invenio-rdm/blob/master/docs/reference/rest_api_drafts_records.md).

## Parent commands after independent acceptance

Run the unchanged reviewed source in this folder (or an approved identical copy):

```text
python3 native_transport.py check
python3 native_transport.py preflight
python3 native_transport.py stage --execute-own-draft --confirm-id 23356540
python3 native_transport.py inspect
python3 native_transport.py publish --execute-own-draft --confirm-id 23356540
python3 native_transport.py inspect --check-doi
```

Do not remove the native journal after an interrupted/unknown write. `check`, `preflight`, and `inspect` make no API mutations; kit inspect may save a confirmed publication receipt locally.
