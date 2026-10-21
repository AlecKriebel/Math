#!/usr/bin/env python3
"""Record an existing external result, retaining authorship and one-row custody."""
import datetime as dt
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import subprocess
import sys
import urllib.request
import uuid

AUDIT = Path(__file__).resolve().parent
ROOT = AUDIT.parents[1]
sys.path.insert(0, str(ROOT))
from sweep_io import atomic_json


def public_get(url):
    request = urllib.request.Request(url, headers={'User-Agent': 'Independent-mathematical-publication-audit/1.0'})
    with urllib.request.urlopen(request, timeout=30) as response:
        return response.read(), {'status': response.status, 'final_url': response.url}


def cli(args):
    return json.loads(subprocess.run(args, capture_output=True, text=True, check=True).stdout)


def matching_rows(rows):
    pattern = re.compile(r'30002792|OWR.?13494.?011|pseudostar|Janssen|zenodo[./]23284413(?!\d)|/pull/293(?!\d)|\bPR\s*#?293(?!\d)', re.I)
    return [(n, row) for n, row in enumerate(rows, 1) if pattern.search(' '.join(map(str, row)))]


def main():
    acceptance = json.loads((AUDIT / 'ROOT_REVIEW_ACCEPTANCE.json').read_text())
    assert acceptance['ready_for_existing_publication_record'] is True
    assert acceptance['complete_line_proof_verified'] is True and not acceptance['material_objections']
    for item in acceptance['frozen_review_bindings']:
        assert hashlib.sha256((AUDIT / item['path']).read_bytes()).hexdigest() == item['sha256']
    plan = json.loads((AUDIT / 'LEDGER_RECONCILIATION_PLAN.json').read_text())
    assert plan['spreadsheet_id'] == '1ZljUv5Q98jNXLoHK8WjwrkzSm3dhHC1-7LElcOU7y20'
    assert plan['sheet_gid'] == 1254632077 and plan['range'] == "'Math Puzzles'!A:D"
    row = plan['proposed_row']
    assert len(row) == 4 and row[1] == '' and row[2] == 'https://doi.org/10.5281/zenodo.23284413'
    assert 'Alper Ferudun' in row[3] and 'not Alec Kriebel authorship' in row[3]
    operation = uuid.uuid4().hex
    raw = ROOT / 'raw/pr0293' / ('ledger_reconciliation_' + operation)
    raw.mkdir()
    spec = importlib.util.spec_from_file_location('owned_account_reader', ROOT / 'audits/pr0292_30001608/prepublication_check.py')
    reader = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(reader)
    reader.verify_destination()
    client = reader.zenodo.ZenodoClient('production', reader.zenodo.token_for('production'))
    account = reader.account_search(client, '')
    atomic_json(raw / 'account_complete.json', account)
    account_pattern = re.compile(r'30002792|OWR.?13494.?011|pseudostar|fattening|Janssen|initial.degree|Cohen.Macaulay', re.I)
    matches = []
    for item in account['records']:
        files = item.get('files', [])
        assert isinstance(files, list)
        if account_pattern.search(json.dumps(item.get('metadata', {}))) or any(account_pattern.search(str(f.get('key', f.get('filename', '')))) for f in files):
            matches.append(int(item['id']))
    assert set(matches) <= {23395703, 23444839}, 'New own-account result lead; reconcile before row insertion.'
    pr = cli(['gh', 'api', '--hostname', 'github.com', 'repos/AlecKriebel/Math/pulls/293'])
    assert pr['head']['sha'] == '6e717193f93c8a321cce1ce35a00eed1ecfb56e7'
    assert pr['base']['repo']['id'] == 1307717439 and pr['base']['ref'] == 'main'
    wire, _ = public_get('https://zenodo.org/api/records/23284413')
    record = json.loads(wire)
    baseline = json.loads((ROOT / 'raw/pr0293/external_record23284413.json').read_text())
    assert record['state'] == 'done' and record['submitted'] is True
    assert record['doi'] == '10.5281/zenodo.23284413'
    assert record['metadata']['title'] == baseline['metadata']['title']
    assert record['metadata']['creators'] == baseline['metadata']['creators'] == [{'name': 'Ferudun, Alper', 'affiliation': 'Mercury Software GmbH'}]
    files = lambda value: {f['key']: (f['size'], f['checksum']) for f in value['files']}
    assert files(record) == files(baseline)
    _, resolution = public_get(row[2])
    assert resolution['status'] == 200 and re.fullmatch(r'https://zenodo.org/records?/23284413/?', resolution['final_url'])
    atomic_json(raw / 'record.json', record)
    params = {'spreadsheetId': plan['spreadsheet_id'], 'range': "'Math Puzzles'!A:AQ", 'valueRenderOption': 'FORMATTED_VALUE'}

    def read(label):
        value = cli(['gws', 'sheets', 'spreadsheets', 'values', 'get', '--params', json.dumps(params)])
        atomic_json(raw / (label + '.json'), value)
        assert value['values'][0] == plan['schema']
        return value['values']

    before = read('ledger_before')
    found = matching_rows(before)
    intent = AUDIT / 'LEDGER_RECONCILIATION_INTENT.json'
    appended = False
    if found:
        assert len(found) == 1 and found[0][1] == row, 'Existing result/DOI row needs reconciliation; no append performed.'
    else:
        if intent.exists():
            raise RuntimeError('Prior append intent exists without a matching row; resolve outcome before any retry.')
        atomic_json(intent, {'timestamp': dt.datetime.now(dt.timezone.utc).isoformat(), 'pr': 293,
                             'operation': operation, 'row': row, 'before_rows': len(before),
                             'external_author': 'Alper Ferudun', 'no_new_publication': True,
                             'recovery_rule': 'On uncertain append read the live sheet by DOI/result; never blindly retry.'})
        append_params = {'spreadsheetId': plan['spreadsheet_id'], 'range': plan['range'],
                         'valueInputOption': 'RAW', 'insertDataOption': 'INSERT_ROWS', 'includeValuesInResponse': True}
        response = cli(['gws', 'sheets', 'spreadsheets', 'values', 'append', '--params', json.dumps(append_params),
                        '--json', json.dumps({'majorDimension': 'ROWS', 'values': [row]})])
        atomic_json(AUDIT / 'LEDGER_RECONCILIATION_RESPONSE.json', response)
        assert response['updates']['updatedRows'] == 1 and response['updates']['updatedColumns'] == 4
        assert response['updates']['updatedData']['values'] == [row]
        appended = True
    after = read('ledger_after')
    found = matching_rows(after)
    assert len(found) == 1 and found[0][1] == row
    assert sum(len(v) > 2 and v[2] == row[2] for v in after) == 1
    receipt = {'timestamp': dt.datetime.now(dt.timezone.utc).isoformat(), 'pr': 293,
               'status': 'verified', 'external_publication': True, 'external_author': 'Alper Ferudun',
               'new_publication': False, 'new_row': appended, 'read_back_exact': True,
               'unique_target_and_DOI': True, 'row_number': found[0][0], 'values': row,
               'doi': record['doi'], 'doi_resolution': resolution,
               'ledger_rows_before': len(before), 'ledger_rows_after': len(after),
               'complete_account_records': account['total'], 'reconciled_different_result_account_leads': matches,
               'live_pr': {'head': pr['head']['sha'], 'state': pr['state'], 'draft': pr['draft'], 'merged': pr['merged']},
               'raw_receipts': raw.relative_to(ROOT).as_posix()}
    atomic_json(AUDIT / 'LEDGER_PUBLICATION_VERIFICATION.json', receipt)
    print(json.dumps(receipt, indent=2))


if __name__ == '__main__':
    main()
