# Zenodo metadata discovery workflow audit

Checkpoint: 2026-10-10 21:01 UTC (14:01 America/Los_Angeles). Audit completion: 100%. This audit made no Zenodo mutations, created no deposits or versions, and contacted nobody.

## Conclusion and exact supported claim

The existing metadata-only workflow is appropriate for compatible published paper records. Its mutation route is `actions/edit` → PUT metadata to the **same deposition ID** → `actions/publish`. It never calls deposition creation, file upload/removal, or `actions/newversion`. Zenodo explicitly states that republishing an edited record's metadata does not affect its DOI. This matches the user's authorization to update metadata without a DOI or version bump. [Official published-record editing guidance](https://help.zenodo.org/docs/deposit/manage-records/#edit-published-records), [official API actions](https://developers.zenodo.org/), [metadata-versus-version FAQ](https://zenodo.org/help/versioning).

The strongest verified result here is static route inspection plus 58 passing offline tests, not a live mutation experiment. DOI preservation also rests on Zenodo's documented semantics. Read-only public/native before-and-after snapshots should provide per-record evidence during the real execution.

## Safety mechanisms verified

- Published-record identity and boolean submitted state are checked. Unpublished drafts and externally opened edit sessions cannot enter the confirmed workflow.
- The entire original editable metadata is copied, then supplied patch fields replace whole fields. Original DOI, files, filenames, sizes and MD5 checksums are saved before the first mutation; `doi`, `prereserve_doi` and `relations` cannot be patched.
- Native metadata, custom fields, access and PIDs are snapshotted. Rich native content that the legacy PUT could lose is refused before opening an edit: controlled subjects, structured/multiple affiliations, organization creators, unsupported creator identifiers or extra fields, multiple licenses/languages, nonempty custom fields and unsupported descriptions/titles.
- Unpatched metadata and all native custom fields/access/PIDs are checked after staging and before publication. The full staged native snapshot is checked after publication.
- Original/proposed metadata and operation phase are durably saved before each API mutation. A lost response prompts one authenticated read-back, never an automatic mutation retry. A retry of a completed action becomes read-only if the expected record still matches.
- Native or legacy metadata/file/DOI drift blocks publication. A different pending patch cannot silently overwrite a saved edit. Discard refuses unrelated external changes.
- The client restricts API calls to HTTPS on the selected environment's host, uses bearer headers, and redacts token details in errors. Per-record local locks prevent concurrent local mutators.

Inspected: `metadata_updates.py`, `zenodo.py` client/verification/dispatch, metadata workflow README and all metadata tests. Executed `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s zenodo_deposit_tool`: 58 tests passed in 0.133 seconds.

## Limits and execution pitfalls

1. Use a specific version's `/records/ID`, never its concept DOI or concept identifier. Edit previous published versions only with descriptions faithful to those versions' actual files. [Official version management](https://help.zenodo.org/docs/deposit/manage-versions/).
2. Local snapshot verification does **not explicitly retain native parent/version-list identifiers or version count**. No workflow call requests a new version, and native PIDs are protected, so a version bump is not expected. For an explicit check, save and compare native/public `parent`/`versions` or legacy `conceptrecid`, `conceptdoi` and `relations.version` before/after, wherever the API supplies them. Preserve the metadata `version` string by omitting it from patches.
3. The local lock does not block another browser, machine or remote client. Zenodo's legacy action API lacks a server-side atomic check-and-publish transaction. Avoid concurrent edits to these records until completion.
4. Structured controlled subjects and modern identifiers/affiliations are valuable but this legacy tool cannot add them. Do not simplify rich records to bypass the guard; use the native editor for those records. Adding free-form text that looks like a controlled classification does not create its structured identifier.
5. `keywords`, `creators`, `references` and `related_identifiers` replace the whole list. Merge meaningful existing entries before patching. Do not alter author order or remove coauthors/ORCIDs.
6. Accepted representation changes are narrowly specified: plain-text HTML escaping, simple-paragraph curly apostrophe normalization, omitted affiliation to null, omission of explicitly empty optional fields, and inferred DOI/URL schemes. Other changes require inspection. Simple paragraph HTML with ASCII apostrophes minimizes avoidable serializer discrepancies.
7. A metadata staging failure can leave an edit draft open, with the public original still intact. Read `metadata ID`, retain the state file and reconcile or discard the saved session; do not delete snapshots or repeat raw POST actions blindly. A post-publication verification failure cannot undo the completed public change and must be reported accurately.
8. The guard and tests are conservative; API-side errors or field canonicalization may prevent some legitimate records from being updated. This is a compatibility limit, not permission to create a new record/version.

## High-value metadata practices supported by official guidance

- Preserve the scholarly paper title unless the manuscript proves a correction is warranted. Titles appear in citation and repository display; keep searchable technical nouns consistent with the paper. [Title guidance](https://help.zenodo.org/docs/deposit/describe-records/titles/).
- Put a faithful abstract first: mathematical object/problem, precise result, hypotheses, scope and remaining limits. Follow with a short statement of paper/source/verification contents when useful. Use ordinary field terminology alongside symbols so experts can find it by words. Zenodo supports abstracts and basic formatting. [Description guidance](https://help.zenodo.org/docs/deposit/describe-records/descriptions/).
- Add relevant field, object/problem, named-method and common synonym/acronym keywords; exclude broad unrelated topics and unsupported superlatives. This selection is an editorial recommendation, not an empirically proven keyword count or ranking claim. Zenodo confirms custom keywords and controlled subjects aid discoverability and currently lists EuroSciVoc, MeSH and GEMET. [Keywords and subjects](https://help.zenodo.org/docs/deposit/describe-records/keywords-and-subjects/).
- Ensure Alec Kriebel's existing creator entry has ORCID `0009-0001-9320-500X`; preserve every other creator and identifier. Do not invent affiliations or roles. Creator identifiers and correctly separated given/family names support citation identity. [Creator guidance](https://help.zenodo.org/docs/deposit/describe-records/creators/).
- Add related identifiers only when evidenced by manuscript/files/public records. Use correct semantic relationships (`cites`, `isSupplementedBy`, `isSupplementTo`, etc.) and canonical DOI/arXiv/URL identifiers. Avoid asserting identity or version relationships merely because papers share a topic. [Official legacy metadata field definitions](https://developers.zenodo.org/).
- Keep resource type and publication status honest: a Zenodo-hosted unpublished manuscript is normally a preprint, not evidence of journal publication or peer review. Retain the original publication date, license, access and version. Add English language only if supported by the actual paper. [Official metadata field definitions](https://developers.zenodo.org/).
- Test discoverability using a few natural specialist queries and exact title/ORCID queries, then confirm public read-back. Metadata terms are searchable and query-dependent ranking is documented; no exact improvement in ranking, views or expert uptake can be promised. [Zenodo search guide](https://help.zenodo.org/guides/search/).

No community submission, curator contact or outreach should be performed: project policy reserves external communication to the human. Any useful community suggestion may be recorded in research notes only.

## Safe operation sequence

Commands below are templates; replace `ID` and patch path after authenticating and checking the exact paper/version. The user already authorized publication of metadata changes, so numeric confirmations are tool safeguards, not a request for new user approval.

```sh
python3 zenodo_deposit_tool/zenodo.py metadata ID
python3 zenodo_deposit_tool/zenodo.py update-metadata ID zenodo_discoverability_20261010/patches/ID.json --dry-run
python3 zenodo_deposit_tool/zenodo.py update-metadata ID zenodo_discoverability_20261010/patches/ID.json --confirm-id ID
python3 zenodo_deposit_tool/zenodo.py metadata ID
python3 zenodo_deposit_tool/zenodo.py publish-metadata ID --confirm-id ID
python3 zenodo_deposit_tool/zenodo.py metadata ID
```

Retain preview, stage and publication receipts plus public/native snapshots. Compare same ID/DOI, unchanged original files/checksums/sizes, access/license, publication date and version information. Do not invoke the separate `stage`, ordinary `publish`, creation, DOI reservation, new-version or file-management workflows for this task. Only if an edit must be abandoned and the saved session still verifies, use `discard-metadata ID --confirm-id ID`.
