# Local Zenodo deposit tool

This tool prepares a Zenodo draft, uploads files, verifies the remote file list and MD5 checksums, and publishes only through a separate explicit command. It uses Python 3.10+ and no third-party packages.

## Set up the key

Create a Zenodo personal access token with `deposit:write`. Add `deposit:actions` if you want to publish through the tool. Sandbox testing needs a separate sandbox account and token.

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

Metadata fields must match exactly, with one narrow representation exception: for a plain-text description without HTML markup or existing character references, Zenodo may encode `&`, `<`, and `>` as HTML entities. The verifier accepts that exact encoding because the description is displayed as HTML. It does not ignore substantive text changes, strip tags, double-encode existing entities, or normalize other fields. The local manifest and supplied metadata remain unchanged.

If the publication response is lost, the tool attempts one read-back, never an automatic second publication request. If it confirms publication, it returns the verified receipt. Otherwise it reports the outcome as unconfirmed and directs you to `inspect`. Repeating `publish` with the same confirmation ID returns an already-published record without another POST, provided its metadata and files still match. If local receipt writing fails, output still reports confirmed publication with `receipt_saved: false` and a recovery warning; retain that output and use `inspect` after fixing local storage.

Add `--sandbox` to **every** command in a sandbox run. Sandbox and production draft state and tokens are separate. Use the sandbox to test API behavior, though its deposits and test DOIs can be wiped. The tool currently handles new deposits, not creating a new version of an existing published record. If a draft already has conflicting or extra files, it stops rather than silently replacing them. If the local state file is lost after draft creation, find and reconcile that draft in the Zenodo account before rerunning `stage` to avoid duplicates.

Zenodo API references: [developer guide](https://developers.zenodo.org/) and [sandbox](https://sandbox.zenodo.org/).

## Diagnosing errors

- An HTML 403 mentioning unusual traffic is identified as a traffic-filter response. The tool always sends its truthful client identity; it does not retry around the filter.
- JSON 401/403 errors retain redacted server details and point to token environment, scopes, or record ownership. HTML bodies are never printed, and tokens are redacted from JSON errors.
- Rate limits, non-JSON successes, malformed or oversized responses, and unconfirmed publication outcomes produce explicit errors. Mutating requests are never automatically retried.
- A creation failure with no saved ID may be ambiguous. Reconcile the account before restaging if the request could have reached Zenodo; the tool cannot recover an unknown draft ID automatically.

Run the offline regression suite with `python3 -m unittest discover -s zenodo_deposit_tool -v`. The tests simulate publication; they do not create real deposits.

## First production workflow

The Brandes preprint was successfully published as [record 22982894](https://zenodo.org/records/22982894) on 26 September 2026, with exact metadata and two verified files. Live testing found that requests without a User-Agent received an HTML 403 traffic-filter response. The client now sends its truthful `Math-Zenodo-Deposit-Tool/1.0` identity.

Verify DOI resolution separately from the published state: the first resolver checks for this record returned 404 even though the public record and downloads were available. The later read-only tool check confirmed HTTP 200 resolution to the published record. Do not create a duplicate deposit or repeat publication to address this. Detailed [workflow feedback and receipts](../owr_17293_016_brandes_normalization/publication/README.md) include the explicit Google Workspace CLI command used to target the tracker tab.
