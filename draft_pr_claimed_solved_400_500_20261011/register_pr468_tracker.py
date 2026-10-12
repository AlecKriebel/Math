#!/usr/bin/env python3
"""Register a confirmed DOI exactly once through the Google Workspace CLI."""
import argparse
import datetime
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent / 'audits/pr468_30000689'
GWS = '/Users/alec/.nvm/versions/node/v22.16.0/bin/gws'
SHEET = '1ZljUv5Q98jNXLoHK8WjwrkzSm3dhHC1-7LElcOU7y20'
TAB = 'Math Puzzles'


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def cli(action, params, body=None):
    cmd = [GWS, 'sheets', 'spreadsheets', 'values', action, '--params', json.dumps(params)]
    if body is not None:
        cmd += ['--json', json.dumps(body)]
    run = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
    require(run.returncode == 0, 'Google Workspace operation failed; reconcile before retrying a write')
    return json.loads(run.stdout)


def get(range_name):
    return cli('get', {'spreadsheetId': SHEET, 'range': range_name})


def dump(name, obj):
    (ROOT / name).write_text(json.dumps(obj, indent=2) + '\n')


def matches(doi, row):
    token = doi.removeprefix('https://doi.org/')
    return [i + 1 for i, values in enumerate(row)
            if len(values) >= 3 and values[2].strip() in {doi, token}]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--apply', action='store_true')
    args = parser.parse_args()
    pub = json.loads((ROOT / 'ZENODO_PUBLISH_RECEIPT.json').read_text())
    require(pub['state'] == 'published' and pub['environment'] == 'production',
            'Confirmed production publication is required')
    doi = pub['doi_url']
    require(doi.startswith('https://doi.org/10.'), 'Confirmed DOI URL missing')
    canonical = json.loads((ROOT / 'package/metadata.json').read_text())
    require(pub['title'] == canonical['title'], 'Publication title does not match canonical metadata')
    header = get("'Math Puzzles'!A1:D1").get('values', [])
    require(header == [['Original Problem', 'Solution Chat URL', 'DOI', 'Notes']], 'Tracker header changed')
    values = [[
        '30000689 / OWR-1455-008 — Embedding Obstructions from Missing Simplicial Faces; '
        'original conjecture: https://ems.press/content/serial-article-files/46090 (p.238, Conjecture4)',
        '', doi,
        canonical['title'] + '; Alec Kriebel; version1.0, 12October2026; '
        'https://github.com/AlecKriebel/Math/pull/468. Full topological-source/topological-embedding result; '
        'credited synthesis and dimension-four extension. Extensive AI use; unrefereed; '
        'no independent human peer review or first-priority claim. Paper and verification archive at DOI.'
    ]]
    existing = get("'Math Puzzles'!A:D").get('values', [])
    rows = matches(doi, existing)
    require(len(rows) <= 1, 'More than one tracker row already has this DOI; reconcile')
    operation = {'prepared_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
                 'spreadsheet_id': SHEET, 'tab': TAB, 'doi': doi, 'values': values,
                 'matching_existing_rows': rows, 'state': 'read_only_preflight'}
    dump('TRACKER_APPEND_OPERATION.json', operation)
    if not args.apply:
        print(json.dumps({'state': 'read_only_preflight', 'existing_doi_rows': rows}, indent=2))
        return
    if rows:
        row = rows[0]
        updated_range = f"'Math Puzzles'!A{row}:D{row}"
        observed = get(updated_range).get('values', [])
        require(observed == values, 'Existing DOI row differs from intended registration; do not duplicate')
        state = 'existing_identical_registration'
        response = None
    else:
        operation['state'] = 'append_attempted_once'
        dump('TRACKER_APPEND_OPERATION.json', operation)
        try:
            response = cli('append', {'spreadsheetId': SHEET, 'range': "'Math Puzzles'!A:D",
                                     'valueInputOption': 'RAW', 'insertDataOption': 'INSERT_ROWS',
                                     'includeValuesInResponse': True},
                           {'majorDimension': 'ROWS', 'values': values})
        except (RuntimeError, subprocess.TimeoutExpired):
            # A lost response never authorizes another append. Read back only.
            latest = get("'Math Puzzles'!A:D").get('values', [])
            recovered = matches(doi, latest)
            require(len(recovered) == 1 and latest[recovered[0] - 1] == values[0],
                    'Append outcome unconfirmed; inspect saved operation before any further write')
            row = recovered[0]
            updated_range = f"'Math Puzzles'!A{row}:D{row}"
            response = None
            state = 'recovered_append_readback'
        else:
            updates = response['updates']
            require(updates['updatedRows'] == 1 and updates['updatedColumns'] == 4,
                    'Unexpected append size; inspect without repeating')
            updated_range = updates['updatedRange']
            state = 'appended_once'
        observed = get(updated_range).get('values', [])
        require(observed == values, 'Appended range does not match intended row')
    receipt = {'verified_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
               'verified': True, 'state': state, 'spreadsheet_id': SHEET, 'sheet_id': 1254632077,
               'tab': TAB, 'updated_range': updated_range, 'values': observed,
               'append_response': response, 'doi': doi, 'unrelated_rows_saved': False}
    dump('TRACKER_APPEND_RECEIPT.json', receipt)
    print(json.dumps({'state': state, 'verified': True, 'updated_range': updated_range, 'doi': doi}, indent=2))


if __name__ == '__main__':
    main()
