# Native metadata workflow adversarial audit

Checkpoint: 2026-10-10. Native translation and offline mutation-control audit complete; best estimate 95% toward a publication-ready preserving workflow, with baseline refresh and the final protected-state read-back still owned by the root. No live record was edited or published by this auditor. All client, token, lock and persistence paths in execution probes were replaced with local fakes; no credentials were loaded by the probe.

## Exact claims and evidence

The requested workflow must change only reviewed discovery metadata on an existing published paper. Its record DOI, concept DOI, complete version registry, publication date, version label, license, access, file contents and file settings, custom fields, existing author information and unpatched rich native metadata must survive. Creating a record/version or reserving any PID is prohibited.

Reviewed files: `native_metadata.py`, `baseline.py`, `reviews/native_api_reference.md`, `apply_reviewed.py`, the native-preservation functions in `zenodo_deposit_tool/metadata_updates.py`, and the underlying request/storage behavior in `zenodo_deposit_tool/zenodo.py`. The [official InvenioRDM draft/record API reference](https://raw.githubusercontent.com/inveniosoftware/docs-invenio-rdm/master/docs/reference/rest_api_drafts_records.md) distinguishes same-record draft editing at `POST /api/records/{id}/draft` from creating a record, creating a version, and reserving a DOI. The native implementation uses only the existing-record edit, metadata PUT, and existing-draft publish mutation routes. Its payload carries full reviewed target metadata and the original custom fields; it sends no new PID, file or access payload.

The tested source snapshot (`reviews/native_metadata_audited_initial.py`, SHA-256 `4c3d2db89d95478b349f0f6e95d547c4fd2baede0416f10032f11c9e16712bbd`) already includes the root's repair of the first preflight finding. The word “initial” denotes the preserved audit snapshot, not the pre-repair file.

## Actionable findings and disposition

1. **Preflight must bind protected native state to the saved baseline. Resolved in the tested snapshot.** The first inspected native implementation compared the current public native record with `before.json` only for metadata and PIDs, then captured a new protected state. It could thereby accept prior drift in files, custom fields, access, parent identity or version history. This was reported before any publication. The root added a complete version-registry identity comparison, exact metadata/PID/custom/access comparisons, and the full native-file baseline comparison. The 34-case offline probe confirms those drift cases now fail before any mutation. Baselines without `native_files` now correctly fail closed.

2. **Complete version-registry/public serialization check after native publication. Root committed to adding it.** The tested native publish branch checks record/concept PIDs, the local record's `versions` object, protected files/access/custom fields and exact reviewed metadata (apart from controlled-vocabulary display labels). It does not itself re-fetch the complete version registry or the legacy public serialization. The root will add full `snapshot()` identity/version-IDs/count plus legacy public metadata/files comparison before reporting success. The mutation routes themselves contain no version-creation or PID-reservation operation.

3. **Legacy wrapper did not compare native file settings. Reported before first live edit; repair pending at this writing.** `apply_reviewed.py` initially compared legacy filename/checksum/size snapshots and record/concept identity, but neither its native preflight nor final read-back compared file enablement, preview/order or per-file access. The underlying legacy native snapshot excludes files, so it cannot independently cover these settings. The root was told to add a stable native-file-state comparison before and after the operation and refresh missing saved baselines. This finding concerns file metadata/settings in addition to content hashes.

No other material mutation-route whitelist bypass was found in the inspected wrapper: non-GET requests are restricted to the selected record's three existing legacy edit/update/publish endpoints, and the underlying client independently rejects hosts outside the configured Zenodo environment. The frozen patch hash is checked before application, the legacy-compatible route is enforced, old record metadata is bound to its saved baseline, and failures do not trigger mutation retries. Draft staging precedes publication and must have the expected state.

## Offline validation

`reviews/native_workflow_probe.py` runs 34 adversarial cases with a rich synthetic native record and a completely fake API. Both `NATIVE_WORKFLOW_PROBE_INITIAL.json` and `NATIVE_WORKFLOW_PROBE_CURRENT.json` record **34 passed, 0 failed** against the tested snapshot. Cases cover:

- exact translation of subjects/language and ORCID addition;
- preserved existing non-ORCID identifiers, structured affiliations, dates, title, publication date, version, unpatched descriptions and structured related identifiers;
- rejection of prohibited patch fields, empty patches, replacing an existing language, erasing controlled subjects or removing existing references;
- rejection of DOI, access, custom-field, file, version and scientific-title drift after session capture;
- rejection of saved-baseline metadata, PID, file, access, custom, version and parent drift before any mutation;
- refusing a pre-existing pending draft;
- persistence failure before the first write;
- uncertain failures at edit, PUT and publish, with no retry or later mutation;
- successful staging leaves public metadata unchanged, and successful simulated publication preserves record/concept DOI and version/file/access/custom state.

The early execution of the probe used a fixture without the newly required `native_files` baseline, so nominal success cases failed before mutation. The fixture was corrected to model the repaired baseline contract; the saved result files contain the final 34/34 output. No production outcome is inferred from these fake-server tests.

## Four actual rich-record translations

`reviews/NATIVE_ACTUAL_TRANSLATION_AUDIT.json` records offline translation of the real saved native metadata and the reviewed patches for all four affected papers. Every unpatched native field is equal, and original dictionaries remain unmodified:

| Record | Reviewed native changes | Rich data checked unchanged |
| --- | --- | --- |
| 21699161 | subjects, languages, creators (ORCID only), related identifiers | creator `researcher` role; custom `code:codeRepository`; original name fields |
| 22013710 | subjects, description | native submitted date **2026-08-16**; existing language, ORCID, references and resource/license metadata |
| 22168797 | subjects, languages, description | creator `researcher` role; existing ORCID and references; version |
| 22136869 | subjects, languages | full `technical-info` description, including the universal-proof versus four-leaf regression limitation and edgewise continuous-time caveats |

These translations neither flatten rich creator roles nor route native dates or technical-info descriptions through the incompatible legacy serializer. The original custom fields are deep preserved for the PUT payload. All four actual baseline snapshots lacked `native_files` at the time of this translation check; root is refreshing them under an unchanged public-inventory check before use.

## Remaining validation boundary

The offline proof of route restriction and state guards does not establish behavior of a live Zenodo deployment. Successful live staging and independent native/public read-back remain mandatory, including exact preservation of both record and concept DOI, full version IDs/count and file settings. Any unexpected native normalization or uncertain mutation response must halt automatic work and be reconciled from saved state; the code does not automatically retry the mutation. Existing manuscript claims, mathematical proofs and scientific priority were not revalidated as part of this workflow audit.
