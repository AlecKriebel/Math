#!/usr/bin/env python3
"""One result, one server-side append; read back before any uncertain retry."""
import datetime as dt
import hashlib
import json
import pathlib
import re
import subprocess
import sys

AUDIT = pathlib.Path(__file__).resolve().parent
ROOT = AUDIT.parents[1]
sys.path.insert(0, str(ROOT))
from sweep_io import atomic_json

SHEET = '1ZljUv5Q98jNXLoHK8WjwrkzSm3dhHC1-7LElcOU7y20'
RANGE = "'Math Puzzles'!A:D"
DOI = 'https://doi.org/10.5281/zenodo.23524971'
ROW = [
    'OWR-4530-006 (30001608): All-load stability of the deterministic-first-chunk chain',
    '',
    DOI,
    'All-load stability of a deterministic-first-chunk file-sharing chain — Alec Kriebel, v1.0 (2026-10-20). '
    'Six-page research note: nonexplosion, irreducibility and positive recurrence in physical continuous time for every fixed real arrival rate lambda>0 in the exact six-rate four-population model with a permanent seed, invisible empty waiting rooms and immediate completed-peer departure. '
    'The contribution is the all-load extension; the classical elementary workload argument already handles lambda<1/2. '
    'Bounded priority review compares the historical OWR conjecture, January 5, 2011 author proof and actual Allerton 2012 protocol; final 2011/2015 publisher bodies and some later bodies were not inspected. '
    'No worldwide-firstness/current-openness certificate, stationary moment or other-protocol conclusion is asserted. '
    'Two fresh sequential complete-package adversarial AI reviews passed. Extensive AI involvement in research, proofs, computations, writing and auditing; unrefereed, without formal independent human peer review. '
    'Published PDF and portable source/verification ZIP: https://zenodo.org/records/23524971; original PR https://github.com/AlecKriebel/Math/pull/292.'
]


def gws(action, params, body=None):
    args = ['gws', 'sheets', 'spreadsheets', 'values', action, '--params', json.dumps(params)]
    if body is not None:
        args += ['--json', json.dumps(body)]
    result = subprocess.run(args, capture_output=True, text=True)
    if result.returncode:
        raise RuntimeError('GWS operation failed; inspect saved intent and live sheet before retry: ' + result.stderr[:700])
    return json.loads(result.stdout)


def read(label):
    response = gws('get', {'spreadsheetId': SHEET, 'range': "'Math Puzzles'!A:AQ", 'valueRenderOption': 'FORMATTED_VALUE'})
    atomic_json(ROOT / 'raw/pr0292' / (label + '.json'), response)
    values = response['values']
    assert values[0] == ['Original Problem', 'Solution Chat URL', 'DOI', 'Notes']
    return values


def matches(values):
    found = []
    for n, row in enumerate(values[1:], 2):
        text = ' '.join(map(str, row))
        compact = re.sub(r'[^a-z0-9]', '', text.casefold())
        if (re.search(r'(?<!\d)30001608(?!\d)', text)
                or 'owr4530006' in compact
                or 'zenodo23524971' in compact
                or re.search(r'github\.com/AlecKriebel/Math/pull/292(?!\d)', text, re.I)
                or 'deterministicfirstchunk' in compact
                or ('chunk' in compact and 'norros' in compact and 'stability' in compact)):
            found.append((n, row))
    return found


def main():
    pub = json.loads((AUDIT / 'ZENODO_PUBLISH.json').read_text())
    inspection = json.loads((AUDIT / 'ZENODO_PUBLISHED_INSPECTION.json').read_text())
    assert pub['id'] == inspection['id'] == 23524971
    assert pub['state'] == inspection['state'] == 'published'
    assert inspection['doi_url'] == DOI and inspection['doi_resolution']['http_status'] == 200
    gate = subprocess.run([sys.executable, str(AUDIT / 'prepublication_check.py'), '--phase', 'before_ledger',
                           '--expected-pr-head', 'acc269a3ecf5b009e164b49ecfd3b89d4f4e956e',
                           '--expected-deposit-id', '23524971'], capture_output=True, text=True, check=True)
    gate_data = json.loads(gate.stdout)
    assert not gate_data['unexpected_account_matches']
    before = read('ledger_before_new_publication')
    found = matches(before)
    intent_path = AUDIT / 'LEDGER_APPEND_INTENT.json'
    appended = False
    if found:
        assert len(found) == 1 and found[0][1] == ROW, 'Existing target lead requires reconciliation, no new row was inserted.'
        row_number = found[0][0]
    else:
        if intent_path.exists():
            raise RuntimeError('An earlier append intent exists without a matching row. Resolve its outcome before any retry.')
        atomic_json(intent_path, {'timestamp': dt.datetime.now(dt.timezone.utc).isoformat(),
                                 'pr': 292, 'spreadsheet_id': SHEET, 'range': RANGE, 'row': ROW,
                                 'before_rows': len(before), 'gate_receipt': gate_data['receipt'],
                                 'before_sha256': hashlib.sha256(json.dumps(before, sort_keys=True).encode()).hexdigest(),
                                 'uncertain_outcome_rule': 'Read live sheet for exact DOI/result before any retry; never blindly repeat append.'})
        reply = gws('append', {'spreadsheetId': SHEET, 'range': RANGE, 'valueInputOption': 'RAW',
                               'insertDataOption': 'INSERT_ROWS', 'includeValuesInResponse': True},
                    {'majorDimension': 'ROWS', 'values': [ROW]})
        atomic_json(AUDIT / 'LEDGER_APPEND_RESPONSE.json', reply)
        assert reply['updates']['updatedRows'] == 1 and reply['updates']['updatedColumns'] == 4
        assert reply['updates']['updatedData']['values'] == [ROW]
        appended = True
        row_number = None
    after = read('ledger_after_new_publication')
    found = matches(after)
    assert len(found) == 1 and found[0][1] == ROW, 'Read-back target row or uniqueness mismatch; reconcile without further append.'
    if row_number is not None:
        assert row_number == found[0][0]
    row_number = found[0][0]
    assert sum(len(r) > 2 and r[2] == DOI for r in after) == 1
    receipt = {'timestamp': dt.datetime.now(dt.timezone.utc).isoformat(), 'pr': 292,
               'status': 'verified', 'spreadsheet_id': SHEET, 'sheet_gid': 1254632077,
               'row_number': row_number, 'range': f"'Math Puzzles'!A{row_number}:D{row_number}",
               'values': ROW, 'doi': pub['doi'], 'new_row': appended, 'unique_target_and_DOI': True,
               'read_back_exact': True, 'ledger_rows_before': len(before), 'ledger_rows_after': len(after),
               'gate_receipt': str(pathlib.Path(gate_data['receipt']).relative_to(ROOT))}
    atomic_json(AUDIT / 'LEDGER_PUBLICATION_VERIFICATION.json', receipt)
    print(json.dumps(receipt, indent=2))


if __name__ == '__main__':
    main()
