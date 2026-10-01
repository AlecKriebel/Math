#!/usr/bin/env python3
"""Read-only publication-infrastructure audit; never stages or publishes."""

import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
from datetime import datetime, timezone

sys.dont_write_bytecode = True

ROOT = Path('/Users/alec/Documents/Math')
OUT = ROOT / 'draft_pr_publication_program_20260930/infrastructure'
SPREADSHEET = '1ZljUv5Q98jNXLoHK8WjwrkzSm3dhHC1-7LElcOU7y20'
TARGET_SHEET_ID = 1254632077
OUT.mkdir(parents=True, exist_ok=True)

def save(name, value):
    (OUT / name).write_text(json.dumps(value, indent=2, ensure_ascii=False) + '\n')

calls = []
def run(argv, name):
    result = subprocess.run(argv, cwd=ROOT, capture_output=True, text=True, timeout=60)
    calls.append({'argv': argv, 'returncode': result.returncode, 'output_file': name})
    if result.returncode:
        save(name, {'returncode': result.returncode, 'stderr': result.stderr, 'stdout': result.stdout})
        save('read-only-command-journal.json', calls)
        raise RuntimeError(f'{name} failed with status {result.returncode}; see saved non-secret API diagnostic')
    value = json.loads(result.stdout)
    save(name, value)
    return value

spec = importlib.util.spec_from_file_location('zenodo_audit', ROOT / 'zenodo_deposit_tool/zenodo.py')
zenodo = importlib.util.module_from_spec(spec)
spec.loader.exec_module(zenodo)
credentials = {}
for environment in ('production', 'sandbox'):
    try:
        credentials[f'{environment}_token_available'] = bool(zenodo.token_for(environment))
    except zenodo.DepositError:
        credentials[f'{environment}_token_available'] = False
credentials['private_credential_file_exists'] = zenodo.SECRETS.is_file()
credentials['private_credential_file_permissions_acceptable'] = (
    zenodo.SECRETS.is_file() and not bool(zenodo.SECRETS.stat().st_mode & 0o077)
)
credentials['production_environment_token_available'] = bool(os.environ.get('ZENODO_TOKEN', '').strip())
credentials['sandbox_environment_token_available'] = bool(os.environ.get('ZENODO_SANDBOX_TOKEN', '').strip())
credentials['zenodo_authentication_or_scopes_validated'] = False
save('credential-availability-booleans.json', credentials)

gws = shutil.which('gws')
if not gws:
    raise RuntimeError('gws is absent from PATH')
for schema in ('sheets.spreadsheets.get', 'sheets.spreadsheets.values.get', 'sheets.spreadsheets.values.append'):
    run([gws, 'schema', schema], schema.replace('.', '-') + '-schema.json')

metadata = run([gws, 'sheets', 'spreadsheets', 'get', '--params', json.dumps({
    'spreadsheetId': SPREADSHEET,
    'fields': 'spreadsheetId,spreadsheetUrl,properties(title,locale,timeZone),sheets(properties,protectedRanges,basicFilter,merges)',
    'includeGridData': False,
})], 'spreadsheet-metadata.json')
matches = [sheet for sheet in metadata.get('sheets', []) if sheet['properties']['sheetId'] == TARGET_SHEET_ID]
if len(matches) != 1:
    raise RuntimeError('Could not resolve the exact target sheet ID uniquely')
target = matches[0]
title = target['properties']['title']
quoted_title = "'" + title.replace("'", "''") + "'"
values = run([gws, 'sheets', 'spreadsheets', 'values', 'get', '--params', json.dumps({
    'spreadsheetId': SPREADSHEET,
    'range': quoted_title + '!A:D',
    'majorDimension': 'ROWS',
    'valueRenderOption': 'FORMATTED_VALUE',
})], 'target-tab-values.json')
formulas = run([gws, 'sheets', 'spreadsheets', 'values', 'get', '--params', json.dumps({
    'spreadsheetId': SPREADSHEET,
    'range': quoted_title + '!A:D',
    'majorDimension': 'ROWS',
    'valueRenderOption': 'FORMULA',
})], 'target-tab-formulas.json')
formatting = run([gws, 'sheets', 'spreadsheets', 'get', '--params', json.dumps({
    'spreadsheetId': SPREADSHEET,
    'ranges': [quoted_title + '!A1:D12'],
    'fields': 'spreadsheetId,sheets(properties(sheetId,title),data(startRow,startColumn,rowData(values(userEnteredValue,formattedValue,userEnteredFormat,effectiveFormat,hyperlink,textFormatRuns))),merges,basicFilter,protectedRanges)',
})], 'target-tab-first-rows-formatting.json')
save('read-only-command-journal.json', calls)
save('audit-summary.json', {
    'audit_utc': datetime.now(timezone.utc).isoformat(),
    'spreadsheetId': SPREADSHEET,
    'sheetId': TARGET_SHEET_ID,
    'exact_tab_title': title,
    'explicit_range': quoted_title + '!A:D',
    'headers': values.get('values', [])[0] if values.get('values') else [],
    'populated_rows_in_A_to_D_including_header': len(values.get('values', [])),
    'credentials': credentials,
    'google_sheet_authenticated_read_succeeded': True,
    'google_sheet_write_access_validated': False,
    'zenodo_api_calls_performed': False,
    'writes_to_google_sheets_performed': False,
})
print(json.dumps({'target_title': title, 'sheetId': TARGET_SHEET_ID, 'headers': values.get('values', [])[0],
                  'rows_including_header': len(values.get('values', [])), 'credentials': credentials}, indent=2))
