# Publication tracker utility

`append_publication.py` defaults to a local append dry run after authenticated live reads. **Only `--execute` sends an append.** Run it after the publication/review workflow has established the final problem identity, DOI, and notes. The script does not itself validate the mathematics or authenticate publication on Zenodo. Root must serialize calls.

It resolves sheet ID **1254632077** live within spreadsheet **1ZljUv5Q98jNXLoHK8WjwrkzSm3dhHC1-7LElcOU7y20**, then requires the four exact A:D headers. It uses RAW values, blank B, four string cells, explicit tab selection, and at most one append. Never use the CLI append shortcut for this tracker.

Use argument arrays; Notes come from a UTF-8 file and its final newline(s) are removed. Example for PR9 after the actual publication DOI is known:

```python
from pathlib import Path
import subprocess

repo = Path('/Users/alec/Documents/Math')
argv = [
    'python3', '-B',
    str(repo / 'draft_pr_publication_program_20260930/infrastructure/append_publication.py'),
    '--problem-url', 'https://www.unsolvedmath.com/problems/OWR-12697711-006',
    '--problem-alias', 'https://www.unsolvedmath.com/problems/30005473',
    '--doi', published_doi,
    '--notes-file', str(notes_file),
    '--receipt-dir', str(publication_receipt_dir),
]
dry_run = subprocess.run(argv, cwd=repo, capture_output=True, text=True)
assert dry_run.returncode == 0

# Only the authorized publisher executes this after examining the saved dry run.
executed = subprocess.run(argv + ['--execute'], cwd=repo, capture_output=True, text=True)
assert executed.returncode == 0
```

The PR9 example follows the tab's observed coded-identifier convention: Original Problem contains `OWR-12697711-006`, while the numeric `30005473` route is supplied only as an explicitly source-verified alias. Root confirmed this mapping in the source record. Include the primary OWR DOI and page in the Notes when the website route itself cannot be checked. This script does not infer that mapping or test website accessibility.

Add `['--problem-alias', verified_alternate_url_or_id]` before execution when independent source evidence establishes an alternate problem identifier. Repeat for multiple aliases. No numeric-to-OWR mapping is inferred automatically. Numeric UnsolvedMath IDs and coded OWR/AMR identifiers are supported, preserving leading zeros. Recognized DOI URL, bare DOI, and `doi:` forms normalize to the same key. Generic original-problem URLs preserve path case, query, and fragment identity.

Possible successful states:

- `dry_run_ready`: local append validation succeeded; no append occurred.
- `verified_existing`: exactly one row already has the same DOI and original-problem key or explicitly supplied alias; its four actual cells were independently read back. `requested_row_matches` states whether the existing text also equals the supplied row. Existing notes are not replaced.
- `appended_verified`: one append succeeded, the returned range/counts/values were checked, and an independent readback exactly matched the four requested cells.

Any problem/alias key paired with a different DOI, DOI paired with an unverified different problem key, multiple matching rows, malformed nonempty keys, formula-backed keys, wrong headers, unexpected range/counts/values, or readback mismatch fails without an automatic retry. An unrelated malformed populated DOI also requires reconciliation before append; the utility fails closed.

Each invocation creates a unique `tracker-attempt-<UTC>-<suffix>/` folder inside `--receipt-dir`. It saves metadata, full live values/formulas, the exact request including a Notes hash and source path, command argument arrays, raw outputs, the local dry run, actual response/readback when applicable, and the terminal result or failure. Same-key existing rows return before a dry run; those attempts therefore contain the request and existing-row readback, with no append/dry-run response.

Before dispatch, an `append-attempted.json` marker is created and file/directory contents are synced. A timeout or lost/malformed response retains that marker and diagnostic evidence. **Read and reconcile the live tracker before any retry.** The same supplied receipt directory must be reused: prior append markers under that directory block another append for either key when no matching live row is visible. This local marker does not cover a different receipt root, another machine, or other writers. Google Sheets provides no atomic duplicate-check-and-append transaction, so serialization and retained receipts remain necessary.

Offline verification (mocked GWS only, no Google writes):

```python
subprocess.run([
    'python3', '-B', '-m', 'unittest', 'discover',
    '-s', 'draft_pr_publication_program_20260930/infrastructure',
    '-p', 'test_append_publication.py', '-v',
], cwd=repo, check=True)
```

The twelve tests cover numeric and coded IDs/verified aliases, DOI normalization, crossed/multiple matches, literal formula-looking Notes, default dry run, exact one-shot execution, ambiguous-response retry blocking, malformed responses, wrong row/tab/dimension readback, and receipt persistence. No real `--execute` call was performed while building this utility.
