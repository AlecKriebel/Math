# Independent audit of draft/public OAI PID differences

Checkpoint: 2026-10-10 14:17 PDT. Completion estimate for this source/representation audit: **100%**. No remote requests that mutate state were made.

**Recommendation: allow only omission of the existing OAI map from the staged draft, in the comparison layer; preserve the original full public PID baseline and require exact full public PID equality after publication.** Do not remove OAI from the baseline or metadata-check it as an allowed published change.

## Evidence and correction to the initial hypothesis

The snapshot `.zenodo-state/metadata-23271172-production.json` has phase `update_requested`. Its original public PIDs are the unchanged DataCite DOI map plus `{"identifier":"oai:zenodo.org:23271172","provider":"oai"}`. Its staged native draft PIDs equal the original map with **only** the `oai` key absent. The DOI identifier, provider and client are exactly unchanged; access/custom fields also match. An independent JSON check is retained in `OAI_DRAFT_REPRESENTATION_CHECK.json`.

This is not best described as a universal “OAI serializes only on public records” rule. Official Invenio's edit hook copies existing public PIDs into a draft. The exact legacy-PUT mechanism instead explains the omission: Zenodo's `LegacySchema._pids` reconstructs a DOI-only native PID map from `metadata.doi`, and Invenio's draft-update hook takes supplied PID data as the new map. [Zenodo legacy deserializer, lines 190–205](https://github.com/zenodo/zenodo-rdm/blob/580d24fb9dbfc1cc97a2318ed97baa0ce3821d6e/site/zenodo_rdm/legacy/deserializers/schemas.py#L190), [Invenio PID component, edit/update hooks](https://github.com/inveniosoftware/invenio-rdm-records/blob/fc3cd3fc88175f1845b40176763c551f984e0232/invenio_rdm_records/services/components/pids.py#L117).

On publishing an edited record, Invenio computes missing required schemes against both the public and draft scheme sets. Its publish hook then restores removed required PID maps directly from the original public record before setting the resulting public PIDs. Thus an OAI PID already present publicly is retained rather than generated anew. The DOI is present explicitly and unchanged; the PID manager's supplied-identifier branch retrieves the existing PID and is idempotent. [Publish hook, lines 211–238](https://github.com/inveniosoftware/invenio-rdm-records/blob/fc3cd3fc88175f1845b40176763c551f984e0232/invenio_rdm_records/services/components/pids.py#L211), [PID manager, lines 134–159](https://github.com/inveniosoftware/invenio-rdm-records/blob/fc3cd3fc88175f1845b40176763c551f984e0232/invenio_rdm_records/services/pids/manager.py#L134).

OAI is a required scheme in official Invenio configuration. Zenodo copies that PID configuration and only changes the DOI provider list, and its application config selects the copied configuration. [Invenio configuration, lines 602–607](https://github.com/inveniosoftware/invenio-rdm-records/blob/fc3cd3fc88175f1845b40176763c551f984e0232/invenio_rdm_records/config.py#L602), [Zenodo providers, lines 191–197](https://github.com/zenodo/zenodo-rdm/blob/580d24fb9dbfc1cc97a2318ed97baa0ce3821d6e/site/zenodo_rdm/providers.py#L191), [Zenodo application configuration, lines 485–489](https://github.com/zenodo/zenodo-rdm/blob/580d24fb9dbfc1cc97a2318ed97baa0ce3821d6e/invenio.cfg#L485).

## Exact safe comparator

Let `P` be the original full public PID map and `D` the staged native draft map. Accept the PID comparison only if:

1. `D == P`; or
2. `oai` is present in `P` and **absent** in `D`, and `D == {k:v for k,v in P.items() if k != 'oai'}`.

The second condition accepts no changed DOI, provider/client, unknown extra scheme, changed OAI value, empty/null OAI entry, or missing other scheme. A temporary comparison copy may reinsert `P['oai']`; the saved original baseline must remain untouched. This is comparison normalization, not a remote PID update or an instruction to remove/recreate identifiers.

Before publishing, require the live public record still matches its original full PID map, record ID, parent/concept DOI and version, and retain all existing file/checksum and protected-metadata checks. After publication require **exact full public `pids == P`**, including the original OAI map, plus exact parent/concept PID and version identity and file checks. Any mismatch stops further records. Use the existing-record edit/publish action and never a create/new-version action or DOI reservation.

The inspected sources are pinned to official repository commits `580d24fb9dbfc1cc97a2318ed97baa0ce3821d6e` (Zenodo) and `fc3cd3fc88175f1845b40176763c551f984e0232` (Invenio). Local source snapshots and hashes are in `oai_source_snapshots/manifest.json`. These source commits are not claimed to identify the exact deployed Zenodo build; the observed stage matches their mechanism, and the strict per-record post-publication equality check remains essential. This recommendation resolves the representation gap without weakening the no-new-DOI/no-version-change invariant.
