#!/usr/bin/env python3
"""Append one confirmed paper to the exact tracker tab; read back before retry.

Default is a read-only preview. Credentials and unrelated tracker rows are
never saved in public receipts. A lost write response is reconciled by reading.
"""
import argparse
import datetime
import json
from pathlib import Path
import subprocess

SPREADSHEET = '1ZljUv5Q98jNXLoHK8WjwrkzSm3dhHC1-7LElcOU7y20'
TAB_ID = 1254632077
TITLE = 'Math Puzzles'
HEADERS = ['Original Problem', 'Solution Chat URL', 'DOI', 'Notes']


def command(service, action, params, body=None):
    args = ['gws', 'sheets', 'spreadsheets', *service, action,
            '--params', json.dumps(params)]
    if body is not None:
        args += ['--json', json.dumps(body)]
    result = subprocess.run(args, capture_output=True, text=True)
    if result.returncode:
        raise RuntimeError('Workspace CLI request failed: ' + result.stderr)
    return json.loads(result.stdout)


def rows():
    data = command(['values'], 'get', {'spreadsheetId': SPREADSHEET,
                   'range': "'Math Puzzles'!A:D"})
    values = data.get('values', [])
    if not values or values[0][:4] != HEADERS:
        raise RuntimeError('Tracker headers changed')
    return values


def padded(value):
    return (value + [''] * 4)[:4]


def matches(values, doi):
    suffix = doi.removeprefix('https://doi.org/')
    return [(i + 1, padded(v)) for i, v in enumerate(values)
            if len(v) >= 3 and str(v[2]).strip().removeprefix('https://doi.org/') == suffix]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('operation')
    parser.add_argument('--append', action='store_true')
    args = parser.parse_args()
    spec = json.loads(Path(args.operation).read_text())
    paper, row = spec['published_record'], spec['row']
    if (paper.get('environment') != 'production' or paper.get('state') != 'published'
            or len(row) != 4 or row[2] != paper.get('doi_url')
            or not row[2].startswith('https://doi.org/10.5281/zenodo.')):
        raise RuntimeError('Only a confirmed production DOI may be appended')
    if not 800 <= spec['pr'] <= 900:
        raise RuntimeError('PR outside assigned shard')
    metadata = command([], 'get', {'spreadsheetId': SPREADSHEET,
                       'fields': 'spreadsheetId,sheets(properties(sheetId,title))'})
    selected = [s['properties'] for s in metadata['sheets']
                if s['properties']['sheetId'] == TAB_ID]
    if len(selected) != 1 or selected[0]['title'] != TITLE:
        raise RuntimeError('Exact tracker tab changed')
    before = rows()
    found = matches(before, row[2])
    if len(found) > 1 or (found and found[0][1] != row):
        raise RuntimeError('Existing DOI rows conflict with intended entry')
    receipt = {'timestamp_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
               'pr': spec['pr'], 'spreadsheet_id': SPREADSHEET, 'sheet_id': TAB_ID,
               'sheet_title': TITLE, 'intended_row': row, 'existing_doi_count': len(found),
               'append_requested': args.append, 'status': 'preview'}
    if args.append:
        if found:
            receipt.update(status='already_recorded', updated_range=f"'Math Puzzles'!A{found[0][0]}:D{found[0][0]}")
        else:
            try:
                response = command(['values'], 'append', {
                    'spreadsheetId': SPREADSHEET, 'range': "'Math Puzzles'!A:D",
                    'valueInputOption': 'RAW', 'insertDataOption': 'INSERT_ROWS',
                    'includeValuesInResponse': True}, {'values': [row]})
                receipt['append_response'] = response
            except Exception as error:
                # Never replay the mutation on an unknown outcome.
                receipt['append_response_error'] = str(error)
            after = rows()
            found = matches(after, row[2])
            if len(found) != 1 or found[0][1] != row:
                receipt['status'] = 'unconfirmed_do_not_retry_mutation'
                Path(spec['receipt_path']).write_text(json.dumps(receipt, indent=2) + '\n')
                raise RuntimeError('Append outcome not uniquely confirmed; inspect before any retry')
            receipt.update(status='recorded_and_read_back',
                           updated_range=f"'Math Puzzles'!A{found[0][0]}:D{found[0][0]}",
                           exact_read_back_row=found[0][1], final_doi_count=1)
        readback = command(['values'], 'get', {'spreadsheetId': SPREADSHEET,
                           'range': receipt['updated_range']})
        if [padded(v) for v in readback.get('values', [])] != [row]:
            raise RuntimeError('Exact appended-row readback failed')
        receipt['exact_range_read_back_confirmed'] = True
    Path(spec['receipt_path']).write_text(json.dumps(receipt, indent=2) + '\n')
    print(json.dumps(receipt))


if __name__ == '__main__':
    main()
