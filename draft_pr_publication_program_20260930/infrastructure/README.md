# Read-only publication infrastructure audit

Audit completed on 2026-09-30. Infrastructure audit completion: **100%**. This is a narrow readiness result, not an estimate of mathematical validation or overall publication-program completion. No real Zenodo API operation, Google Sheets write, Git edit/commit/push, or external researcher communication occurred.

The reusable `append_publication.py` CLI and its [usage guide](append_publication_usage.md) implement the explicit-tab procedure with default dry run, explicit execution, source-verified aliases, conflict guards, durable attempt evidence, and independent readback. Its twelve mocked safety tests and an independent adversarial review pass. No real execution occurred while building it.

## Verified readiness and exact limits

- Installed CLI: `gws 0.22.5`; Sheets metadata and explicit-tab reads succeeded with existing authentication.
- Production Zenodo token available: **true**. Sandbox token available: **false**. Private credential file present and permissions acceptable: **true**. These are availability checks only; Zenodo authentication/scopes were not tested, and Sheets write access was not tested.
- The repository Zenodo tool's offline regression suite passes **27 tests**. Invocation: `['python3', '-B', '-m', 'unittest', 'discover', '-s', 'zenodo_deposit_tool', '-v']` from `/Users/alec/Documents/Math`. No live deposits are created by this suite.
- The Sheets append helper has **no tab/range flag** in the installed CLI. Do not use `gws sheets +append` for this tracker. Use the direct `sheets spreadsheets values append` method with an explicit tab range.
- No target-tab protected ranges, merges, or basic filter appeared in the requested metadata response. Absence here is an observation, not proof of write permission.

## Tracker destination and observed conventions

Spreadsheet ID: `1ZljUv5Q98jNXLoHK8WjwrkzSm3dhHC1-7LElcOU7y20`.

The spreadsheet title is `Papers`. The user-specified sheet ID **1254632077** resolves exactly to tab **Math Puzzles**. Its explicit A1 range is **`'Math Puzzles'!A:D`**. The default first tab is `Papers`, which is a different destination.

| Column | Exact header | Existing convention |
|---|---|---|
| A | Original Problem | Original-problem URL, except one older Kourovka problem label |
| B | Solution Chat URL | All existing body cells blank; preserve blank unless an authorized usable URL is supplied |
| C | DOI | Full `https://doi.org/10.5281/zenodo.<id>` URL |
| D | Notes | Title, Alec Kriebel, version/dates, precise claim and caveats, validation summary, public record/materials links |

At audit time there are **10 populated rows including the header**, covering body rows 2–10. No exact normalized duplicate problem or DOI keys were found. Rows 2–10 use ordinary string values; formula-rendered values equal the formatted read. Row 1 is bold Arial 10 with wrapping and is frozen. Body rows generally use Arial 10 and `OVERFLOW_CELL`; URLs in A/C have hyperlink formatting. A preexisting empty C11 has a different monospace 11 format. A values append does not promise formatting inheritance; do not add formatting mutations merely to change that existing convention.

Older notes contain historical outreach descriptions. They confer no authorization for outreach and must not be copied into new publication notes.

Existing problem/DOI keys are indexed in `target-tab-derived-summary.json`, and full observed values are in `target-tab-values.json`. Read the live tab again immediately before an eventual append; this audit snapshot must not serve as the final duplicate check.

## Zenodo procedure for the authorized publisher

Keep each manifest at a stable absolute resolved path. The tool hashes that path to locate the environment-specific ignored state file in `/Users/alec/Documents/Math/.zenodo-state/`; moving the manifest can make the same deposit appear unstaged. Preserve the ignored state file through interruptions.

Build the manifest with exactly `metadata` and `files`. File paths are resolved relative to the manifest location; remote filenames must be unique. Stage the intended paper and source/verification archive separately, rather than an outer upload kit. Preserve supplied metadata exactly, including dates, version, author/ORCID, claim limits, AI assistance, review status, and attribution. Confirm all local files before the live mutation.

Use subprocess argument lists, without a shell:

```python
import json
import subprocess
from pathlib import Path

root = Path('/Users/alec/Documents/Math')
manifest = str(Path('/absolute/stable/path/zenodo-deposit.json').resolve())
tool = str(root / 'zenodo_deposit_tool/zenodo.py')

def zenodo(command, *options):
    result = subprocess.run(
        ['python3', '-B', tool, command, manifest, *options],
        cwd=root, capture_output=True, text=True, timeout=900,
    )
    if result.returncode:
        raise RuntimeError(result.stderr)
    return json.loads(result.stdout)

# The actual publisher executes these only for the validated publication candidate.
checked = zenodo('check')             # local only
staged = zenodo('stage')              # creates/resumes draft, uploads, verifies
inspected = zenodo('inspect')         # independent remote metadata/file verification
assert staged['id'] == inspected['id']
assert inspected['state'] == 'ready_to_publish'
published = zenodo('publish', '--confirm-id', str(staged['id']))
assert published['state'] == 'published'
verified = zenodo('inspect', '--check-doi')
assert verified['state'] == 'published'
```

Save every result into the candidate's receipt folder promptly. A publish error can be ambiguous: inspect the saved draft rather than issuing an automatic second POST or creating a replacement. The tool itself reads back after a publication response and checks ID, submitted state, metadata, checksums, and sizes. An already-published retry with the same ID is read-only if the manifest still matches. DOI resolver failure is separate from publication success and must not trigger restaging or republication. Verify public downloadable files independently against local hashes, as in the Brandes example. `inspect` of a published record may update its ignored local receipt; it does not mutate Zenodo.

The tool sends a truthful `Math-Zenodo-Deposit-Tool/1.0` User-Agent. An HTML traffic-filter 403, JSON authorization error, and 429 have distinct diagnostics. It does not automatically retry mutating operations. A creation failure before a saved ID needs account reconciliation before restaging.

## Explicit-tab append and independent readback procedure

Use the installed schemas persisted here. Do not invoke `gws generate-skills`, including `--help`, which previously generated files. The relocated shared skill was read as instructed. Its general request for confirmation is satisfied by the user's existing explicit publication/tracker authorization; do not request that same authorization again.

For each confirmed published candidate:

1. Re-fetch spreadsheet metadata and assert sheet ID 1254632077 still maps to `Math Puzzles`.
2. Read the full explicit range `'Math Puzzles'!A:D`, assert the four exact headers, and search body rows for the original-problem key **or** DOI key. Normalize DOI URL/bare-DOI/`doi:` spellings to lowercase bare DOI; normalize UnsolvedMath links to their printed problem ID, ignoring host scheme and trailing slash/query/fragment. An exact existing publication is already recorded. A problem collision with a different DOI is a reconciliation case, not permission to append a second solution blindly.
3. Build exactly four string cells: `[problem_url, '', doi_url, precise_notes]`. Prepare/save params and body before executing. Use `RAW` to avoid formula interpretation and `INSERT_ROWS` to append a row.
4. Dry-run the same direct method locally. If valid and publication verification has passed, execute **one** append, save its response, and validate `updatedRows == 1`, `updatedColumns == 4`, `updatedCells == 4` and a single-row `updatedRange` under the exact target tab and A:D.
5. Independently read back `updates.updatedRange`; pad omitted trailing empty cells to four strings and require exact equality to the requested row. Save the request, response, and readback. If the append response is lost, re-read/search before any retry; appends are not idempotent.

Reproducible command construction (the write calls below were **not executed in this audit**):

```python
import json
import subprocess

spreadsheet_id = '1ZljUv5Q98jNXLoHK8WjwrkzSm3dhHC1-7LElcOU7y20'
target_range = "'Math Puzzles'!A:D"
params = {
    'spreadsheetId': spreadsheet_id,
    'range': target_range,
    'valueInputOption': 'RAW',
    'insertDataOption': 'INSERT_ROWS',
    'includeValuesInResponse': True,
    'responseValueRenderOption': 'UNFORMATTED_VALUE',
}
row = [problem_url, '', doi_url, precise_notes]
body = {'majorDimension': 'ROWS', 'values': [row]}
argv = [
    'gws', 'sheets', 'spreadsheets', 'values', 'append',
    '--params', json.dumps(params), '--json', json.dumps(body),
]
# Validate first; then the authorized publisher executes argv exactly once.
dry_run = subprocess.run(argv + ['--dry-run'], capture_output=True, text=True)
assert dry_run.returncode == 0
result = subprocess.run(argv, capture_output=True, text=True)
assert result.returncode == 0
receipt = json.loads(result.stdout)
updated_range = receipt['updates']['updatedRange']
readback_argv = [
    'gws', 'sheets', 'spreadsheets', 'values', 'get',
    '--params', json.dumps({
        'spreadsheetId': spreadsheet_id,
        'range': updated_range,
        'majorDimension': 'ROWS',
        'valueRenderOption': 'UNFORMATTED_VALUE',
    }),
]
readback = subprocess.run(readback_argv, capture_output=True, text=True)
assert readback.returncode == 0
observed = json.loads(readback.stdout)['values']
assert len(observed) == 1 and (observed[0] + ['', '', '', ''])[:4] == row
```

Only one process should append to this target during the program. The read/append sequence is not a transaction; the publisher should serialize it and retain receipts to prevent duplicate writes after interruptions.

## Reproduction and saved artifacts

Run `['python3', '-B', 'draft_pr_publication_program_20260930/infrastructure/audit_readonly.py']` from the repository root to repeat the read-only availability/schema/metadata/value/format audit. It performs no staging, publishing, or sheet append. `read-only-command-journal.json` records exact subprocess argument arrays for the successful API reads and schema queries. All audit artifacts are in this dedicated infrastructure folder.
