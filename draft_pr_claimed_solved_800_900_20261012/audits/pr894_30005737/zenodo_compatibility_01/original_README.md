# Local Zenodo deposit tool

This tool prepares Zenodo uploads and edits metadata on existing published records. It verifies metadata and file checksums, and publishes through a separate explicit command. It uses Python 3.10+ and no third-party packages.

## Set up the key

Create a Zenodo personal access token with `deposit:write`. Add `deposit:actions` to publish, unlock published metadata for editing, or discard edits. Sandbox testing needs a separate sandbox account and token.

Keep tokens in the shell environment (`ZENODO_TOKEN` or `ZENODO_SANDBOX_TOKEN`) or in the ignored repository file `.secrets/zenodo.env`:

```sh
mkdir -p .secrets
cp zenodo_deposit_tool/credentials.example .secrets/zenodo.env
chmod 600 .secrets/zenodo.env
```

Edit that private file locally. It is read as `NAME=value` lines, **not executed as shell code**. Environment variables take precedence. Do not paste a key into a deposit manifest, commit, chat, command argument, or log. `.secrets/` and `.zenodo-state/` are Git ignored.

## Deposit a paper

Copy `deposit.example.json` into the paper's own folder as `zenodo-deposit.json`. Edit its metadata and list every file to upload. File paths are relative to the manifest location. The example's placeholder paths need replacement. If an existing paper has a Zenodo API metadata JSON, copy its `metadata` object into the manifest and add `files`.

From the repository root:

```sh
python3 zenodo_deposit_tool/zenodo.py check path/to/zenodo-deposit.json
python3 zenodo_deposit_tool/zenodo.py stage path/to/zenodo-deposit.json
python3 zenodo_deposit_tool/zenodo.py inspect path/to/zenodo-deposit.json
python3 zenodo_deposit_tool/zenodo.py publish path/to/zenodo-deposit.json --confirm-id 12345678
python3 zenodo_deposit_tool/zenodo.py inspect path/to/zenodo-deposit.json --check-doi
```

`check` is entirely local and prints file sizes and SHA-256 checksums. `stage` creates or resumes a draft, uploads missing files, updates metadata, and verifies checksums. It stores the draft ID in the ignored `.zenodo-state/` directory, so rerunning it after an interrupted upload does not create another draft. `inspect` rechecks the remote draft or published record. `publish` requires the exact draft ID from `stage`, rechecks the local manifest against Zenodo, then publishes; publication cannot be undone by this tool.

After a publication request, the tool fetches the deposition again and checks its ID, submitted state, metadata and files before reporting success. It saves a publication receipt in the existing ignored state file before checking the DOI resolver. Output includes `doi`, `doi_url`, `record_url`, and a separate `doi_resolution.status`: `resolved`, `not_resolved` (HTTP 404), `unavailable` (other lookup failures), `not_assigned`, or `not_checked`. A DOI lookup failure does not undo or invalidate confirmed publication. `inspect --check-doi` is a read-only way to recheck it later; plain `inspect` skips the resolver.

Metadata fields must match exactly, with narrow representation exceptions. For plain text without HTML markup or existing character references, Zenodo may encode `&`, `<`, and `>` as HTML entities. For a description consisting solely of plain `<p>...</p>` paragraphs, Zenodo may change every U+2019 curly apostrophe to its ASCII counterpart. In the creators list, the deposition API may add `affiliation: null` when that optional field was omitted; only this exact addition is accepted, preserving all supplied author fields and list order. The verifier reports accepted transformations in `metadata_normalizations`. It rejects substantive text changes, changed author details, extra creator fields, empty-string affiliations, reordered authors, stripped tags, altered attributes, double-encoded entities and other punctuation or field changes. The local manifest and supplied metadata remain unchanged.

If the publication response is lost, the tool attempts one read-back, never an automatic second publication request. If it confirms publication, it returns the verified receipt. Otherwise it reports the outcome as unconfirmed and directs you to `inspect`. Repeating `publish` with the same confirmation ID returns an already-published record without another POST, provided its metadata and files still match. If local receipt writing fails, output still reports confirmed publication with `receipt_saved: false` and a recovery warning; retain that output and use `inspect` after fixing local storage.

Add `--sandbox` to **every** command in a sandbox run. Sandbox and production draft state and tokens are separate. Use the sandbox to test API behavior, though its deposits and test DOIs can be wiped. The tool currently handles new deposits, not creating a new version of an existing published record. If a draft already has conflicting or extra files, it stops rather than silently replacing them. If the local state file is lost after draft creation, find and reconcile that draft in the Zenodo account before rerunning `stage` to avoid duplicates.

Zenodo API references: [developer guide](https://developers.zenodo.org/) and [sandbox](https://sandbox.zenodo.org/).

## Edit an existing upload's metadata

Zenodo supports metadata edits after publication, and publishing those edits [preserves the existing DOI](https://help.zenodo.org/docs/deposit/manage-records/#edit-published-records). These commands work with a specific published record ID, including compatible records uploaded through the website or GitHub. They do not require the original local manifest or files. Use the numeric ID from that version's `/records/ID` page, rather than its concept DOI identifier.

Read the current API metadata:

```sh
python3 zenodo_deposit_tool/zenodo.py metadata 12345678
```

Copy [metadata.patch.example.json](metadata.patch.example.json) into the paper's folder and replace its placeholders. A patch contains exactly one `metadata` object with only the fields to change, for example:

```json
{
  "metadata": {
    "keywords": ["finite groups", "spectral graph theory", "Cayley graphs"],
    "description": "<p>The exact result, its assumptions, and why it matters.</p><p>The deposit includes the paper, source, and reproducible verification.</p>"
  }
}
```

Preview, stage, review, and publish:

```sh
python3 zenodo_deposit_tool/zenodo.py update-metadata 12345678 path/to/metadata-patch.json
python3 zenodo_deposit_tool/zenodo.py update-metadata 12345678 path/to/metadata-patch.json --confirm-id 12345678
python3 zenodo_deposit_tool/zenodo.py metadata 12345678
python3 zenodo_deposit_tool/zenodo.py publish-metadata 12345678 --confirm-id 12345678
```

Without `--confirm-id`, `update-metadata` is read-only and prints the field changes and full proposed metadata. `--dry-run` explicitly selects the same behavior. With confirmation, it unlocks the record using `actions/edit`, updates metadata, and verifies the saved proposal. The public record keeps its current metadata until the separate `publish-metadata` command. That command requires the saved proposal to match exactly before making the changes visible. No new record or DOI is created, and no files are uploaded, replaced, or deleted.

Supported patch fields are `title`, `description`, `keywords`, `creators`, `related_identifiers`, `references`, `notes`, `method`, `publication_date`, `version`, `language`, `upload_type`, `publication_type`, and `image_type`. Omitted fields are preserved from the authenticated deposition response and checked against the native representation. Each supplied field replaces that entire field: lists such as `keywords`, `creators`, and `related_identifiers` replace the whole list. Include existing entries you want to retain when extending a list. Use `[]` to clear an optional list or an empty string to clear an optional text field; `null` is rejected. API validation still applies. DOI changes and API-generated fields (`prereserve_doi`, `relations`) are excluded from patches. The generated fields are omitted from the PUT payload; the existing DOI is preserved.

Verification accepts only the existing description/creator representation exceptions plus two metadata-edit exceptions documented in [Zenodo's serializer](https://github.com/zenodo/zenodo-rdm/blob/master/site/zenodo_rdm/legacy/serializers/schemas/common.py): omission of an explicitly empty optional field (`keywords`, `references`, `locations`, `notes`, `method`, `language`, or `custom`), and addition of an inferred `doi` or `url` scheme to a related identifier with every other supplied value and its position unchanged. For other identifier types, provide the API `scheme` explicitly and use its canonical identifier. Substantive link changes, changed relationships, extra fields, and arbitrary loss of omitted metadata are rejected.

The older API projects some rich native metadata into a simpler representation. Before staging, the tool reads the native representation using `Accept: application/vnd.inveniordm.v1+json` and refuses records whose metadata cannot be preserved by this workflow: organizational authors, multiple or structured affiliations, controlled subjects, multiple languages or licenses, nonempty custom fields, and unsupported additional metadata. This guard also runs on previews. Unpatched native fields, access settings, and identifiers are checked after staging and before publication; the complete staged native snapshot is checked again after publication. For richer records, use Zenodo's native editor. This is a conservative compatibility limit, not a requirement to simplify the record's metadata.

To abandon an edit staged by this tool:

```sh
python3 zenodo_deposit_tool/zenodo.py discard-metadata 12345678 --confirm-id 12345678
```

Original metadata, proposed metadata, native snapshots, DOI, filenames, sizes, and MD5 checksums are saved before writes in the ignored `.zenodo-state/metadata-ID-ENVIRONMENT.json` file. Lost responses trigger one read-back and never an automatic second write. Rerunning the same staged patch resumes the saved edit; a different patch requires completing or discarding the pending one. Repeated publication/discard is read-only when the remote result already matches. A pending edit created elsewhere is rejected, and metadata/file/DOI drift stops further writes. Inspect an uncertain outcome with `metadata ID`, then reconcile the saved session before acting again. Preserve the session file until the workflow is complete; deleting it can lose the original snapshot. Add `--sandbox` to every sandbox command.

Metadata writes use a local per-record process lock on macOS/Linux. Do not edit the same record concurrently through the browser or another machine: the older action API does not provide an atomic check-and-publish transaction. A verified remote action remains confirmed if writing its local receipt fails; output reports `receipt_saved: false`. Live validation of this extension used authenticated reads and previews only; action/failure behavior is covered by offline tests.

These metadata commands edit published uploads. For an unpublished upload, use the existing manifest-based `stage` workflow. Metadata changes made here may make an old local deposit manifest differ from the live record; update that manifest separately if you want its `inspect` verification to pass.

## Improve discoverability

Zenodo [searches and ranks records using metadata terms](https://zenodo.org/help/search), including title and description. Use the metadata editor to make each paper easier to find and understand:

- Use a precise title with the result's natural subject terms. Keep it consistent with the paper.
- Open the description with the exact contribution and scope; explain significance, limitations, and what the downloadable verification provides.
- Add relevant keywords covering the field, specific problem, named objects, and methods. Include common terminology researchers actually search for.
- Keep author names consistent and include ORCID `0009-0001-9320-500X`. Replace a creators list only after preserving every coauthor and supplied identifier.
- Add accurate `related_identifiers` linking the paper to its source, verification code, related papers, and any subsequent journal or arXiv version, with the appropriate relationship.
- Keep the resource type and publication status accurate, and preserve the original publication date.

These are recommendations for improving findability, not a measured publicity increase or a guarantee of search placement. [Zenodo's field guidance](https://help.zenodo.org/docs/deposit/describe-records/) describes titles, descriptions, keywords, and authors. Any outreach or curator communication must be handled by the human user under this repository's independent research policy.

## Diagnosing errors

- An HTML 403 mentioning unusual traffic is identified as a traffic-filter response. The tool always sends its truthful client identity; it does not retry around the filter.
- JSON 401/403 errors retain redacted server details and point to token environment, scopes, or record ownership. HTML bodies are never printed, and tokens are redacted from JSON errors.
- Rate limits, non-JSON successes, malformed or oversized responses, and unconfirmed publication outcomes produce explicit errors. Mutating requests are never automatically retried.
- A creation failure with no saved ID may be ambiguous. Reconcile the account before restaging if the request could have reached Zenodo; the tool cannot recover an unknown draft ID automatically.

Run the offline regression suite with `python3 -m unittest discover -s zenodo_deposit_tool -v`. The tests simulate publication; they do not create real deposits.
Run the independent metadata serializer, native-preservation, and interrupted-staging probes with `python3 zenodo_deposit_tool/metadata_updates_20261010/adversarial_probes.py`.

## First production workflow

The Brandes preprint was successfully published as [record 22982894](https://zenodo.org/records/22982894) on 26 September 2026, with exact metadata and two verified files. Live testing found that requests without a User-Agent received an HTML 403 traffic-filter response. The client now sends its truthful `Math-Zenodo-Deposit-Tool/1.0` identity.

Verify DOI resolution separately from the published state: the first resolver checks for this record returned 404 even though the public record and downloads were available. The later read-only tool check confirmed HTTP 200 resolution to the published record. Do not create a duplicate deposit or repeat publication to address this. Detailed [workflow feedback and receipts](../owr_17293_016_brandes_normalization/publication/README.md) include the explicit Google Workspace CLI command used to target the tracker tab.
