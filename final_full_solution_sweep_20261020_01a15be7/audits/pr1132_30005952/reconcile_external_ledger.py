#!/usr/bin/env python3
"""Reconcile one reviewed, already-published external result; never publish."""
import datetime as dt
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import uuid

AUDIT = Path(__file__).resolve().parent
ROOT = AUDIT.parents[1]
sys.path.insert(0, str(ROOT))
from publication_check import get, SHEET
from sweep_io import atomic_json

PATTERN = re.compile(
    r'30005952|OWR.?14298580.?008|Alfieri|Binns|strong.geography|23063072|'
    r'/pull/1132(?!\d)|\bPR\s*#?1132(?!\d)', re.I)



def require(value, reason):
    if not value:
        raise RuntimeError(reason)


def cli(args):
    return json.loads(subprocess.run(args, capture_output=True, text=True,
                                     check=True).stdout)


def matches(rows):
    return [(n, row) for n, row in enumerate(rows, 1)
            if PATTERN.search(' '.join(map(str, row)))]


def main():
    plan_path = AUDIT / 'LEDGER_RECONCILIATION_PLAN.json'
    plan = json.loads(plan_path.read_text())
    adopted = json.loads((AUDIT / 'ROOT_LEDGER_REVIEW_ACCEPTANCE.json').read_text())
    require(adopted['ready_for_existing_publication_record'] is True,
            'Independent review has not been adopted.')
    require(adopted['helper_sha256'] == hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'Reviewed mutation helper changed.')
    require(adopted['plan_sha256'] == hashlib.sha256(plan_path.read_bytes()).hexdigest(),
            'Reviewed plan changed.')
    for pin in adopted['review_pins']:
        require(hashlib.sha256((AUDIT / pin['path']).read_bytes()).hexdigest()
                == pin['sha256'], 'Adopted review changed.')
    require(plan['spreadsheet_id'] == SHEET and plan['sheet_gid'] == 1254632077
            and plan['range'] == "'Math Puzzles'!A:D", 'Wrong destination.')
    row = plan['proposed_row']
    require(len(row) == 4 and row[1] == ''
            and row[2] == 'https://doi.org/10.5281/zenodo.23063072'
            and 'Alper Ferudun' in row[3]
            and 'not Alec Kriebel authorship' in row[3], 'Wrong authorship/DOI row.')
    raw = AUDIT / 'private' / ('ledger_' + uuid.uuid4().hex)
    raw.mkdir()

    # Read the complete owned account, including existing/draft records.
    base = ROOT / 'audits/pr0399_30001179'
    sys.path.insert(0, str(base))
    spec = importlib.util.spec_from_file_location('pr1132_account_reader_final',
                                                base / 'prepublication_check.py')
    reader = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(reader)
    reader.verify_destination()
    client = reader.zenodo.ZenodoClient('production', reader.zenodo.token_for('production'))
    account = reader.account_search(client, '')
    atomic_json(raw / 'account.json', account)
    account_leads = [item['id'] for item in account['records']
                     if PATTERN.search(json.dumps(item.get('metadata', {})))
                     or PATTERN.search(json.dumps(item.get('files', [])))]
    require(not account_leads, 'New own-account result/draft lead requires reconciliation.')

    live = cli(['gh', 'api', 'repos/AlecKriebel/Math/pulls/1132'])
    baseline_pr = next(p for p in json.loads((ROOT / 'rest_inventory.json').read_text())
                       ['pull_requests'] if p['number'] == 1132)
    require(plan['pr'] == 1132 and plan['problem_ids'] == ['30005952']
            and live['head']['sha'] == plan['head']
            and live['base']['sha'] == plan['base']
            and hashlib.sha256(live['body'].encode()).hexdigest() == plan['body_sha256'],
            'Live PR differs from directly reviewed immutable plan.')
    require(live['head']['sha'] == baseline_pr['headRefOid']
            and live['base']['sha'] == baseline_pr['baseRefOid']
            and live['body'] == baseline_pr['body'], 'Live PR changed; rereview required.')
    atomic_json(raw / 'pr.json', live)
    remote_main = cli(['gh', 'api', 'repos/AlecKriebel/Math/git/ref/heads/main'])
    atomic_json(raw / 'main.json', remote_main)
    local_branch = subprocess.check_output(['git', 'branch', '--show-current'],
                                           text=True).strip()
    baseline_bytes = (ROOT / 'raw/pr1132/zenodo_23063072.json').read_bytes()
    require(hashlib.sha256(baseline_bytes).hexdigest() == plan['baseline_provider_sha256'], 'Reviewed provider baseline changed.')
    baseline = json.loads(baseline_bytes)
    body, _ = get('https://zenodo.org/api/records/23063072')
    record = json.loads(body)
    require(record['state'] == 'done' and record['submitted'] is True
            and record['doi'] == '10.5281/zenodo.23063072', 'Record not published.')
    require(record['metadata'] == baseline['metadata'], 'Publication metadata changed.')
    file_map = lambda x: {f['key']: (f['size'], f['checksum']) for f in x['files']}
    require(file_map(record) == file_map(baseline) == {f['name']: (f['size'], f['checksum']) for f in plan['existing_publication']['files']}, 'Published files changed.')
    _, resolution = get(row[2])
    require(resolution['status'] == 200 and re.fullmatch(
        r'https://zenodo.org/records?/23063072/?', resolution['final_url']),
        'DOI destination mismatch.')
    atomic_json(raw / 'record.json', record)
    params = {'spreadsheetId': SHEET, 'range': "'Math Puzzles'!A:AQ",
              'valueRenderOption': 'FORMATTED_VALUE'}

    def read(label):
        result = cli(['gws', 'sheets', 'spreadsheets', 'values', 'get',
                      '--params', json.dumps(params)])
        atomic_json(raw / (label + '.json'), result)
        require(result['values'][0] == plan['schema_columns'], 'Sheet schema changed.')
        return result['values']

    before = read('before')
    found = matches(before)
    intent = AUDIT / 'LEDGER_RECONCILIATION_INTENT.json'
    appended = False
    if found:
        require(len(found) == 1 and found[0][1] == row,
                'Concurrent/preexisting row needs manual scope review; no append.')
    else:
        require(not intent.exists(), 'Prior append intent has unknown outcome; never retry blindly.')
        intent_value = {'at': dt.datetime.now(dt.timezone.utc).isoformat(),
                        'row': row, 'before_rows': len(before),
                        'raw_directory': str(raw.relative_to(ROOT)),
                        'no_new_publication': True,
                        'recovery': 'Read by DOI/result before any retry; no blind append.'}
        # Exclusive durable claim: concurrent invocations cannot replace one
        # another's known/unknown append intent. A partial write blocks retry.
        descriptor = os.open(intent, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        with os.fdopen(descriptor, 'w', encoding='utf-8') as stream:
            json.dump(intent_value, stream, indent=2)
            stream.write('\n')
            stream.flush()
            os.fsync(stream.fileno())
        append_params = {'spreadsheetId': SHEET, 'range': plan['range'],
                         'valueInputOption': 'RAW', 'insertDataOption': 'INSERT_ROWS',
                         'includeValuesInResponse': True}
        response = cli(['gws', 'sheets', 'spreadsheets', 'values', 'append',
                        '--params', json.dumps(append_params), '--json',
                        json.dumps({'majorDimension': 'ROWS', 'values': [row]})])
        atomic_json(AUDIT / 'LEDGER_RECONCILIATION_RESPONSE.json', response)
        require(response['updates']['updatedRows'] == 1
                and response['updates']['updatedColumns'] == 4
                and response['updates']['updatedData']['values'] == [row],
                'Unexpected append response; inspect live sheet before recovery.')
        appended = True
    after = read('after')
    found = matches(after)
    require(len(found) == 1 and found[0][1] == row,
            'Final row/uniqueness differs; reconcile without blind retry.')
    require(sum(len(r) > 2 and r[2] == row[2] for r in after) == 1, 'Duplicate DOI.')
    receipt = {'at': dt.datetime.now(dt.timezone.utc).isoformat(), 'pr': 1132,
               'status': 'verified', 'external_publication': True,
               'external_author': 'Alper Ferudun', 'new_publication': False,
               'new_row': appended, 'read_back_exact': True,
               'unique_target_and_DOI': True, 'row_number': found[0][0], 'values': row,
               'doi': record['doi'], 'doi_resolution': resolution,
               'ledger_rows_before': len(before), 'ledger_rows_after': len(after),
               'complete_account_records': account['total'], 'own_account_leads': [],
               'remote_main': remote_main['object']['sha'], 'local_branch': local_branch,
               'live_pr_head': live['head']['sha'], 'live_pr_state': live['state'],
               'live_pr_merged': live['merged'], 'live_pr_draft': live['draft'],
               'raw_receipts': str(raw.relative_to(ROOT)),
               'scope': 'One existing external publication recorded; no Zenodo/PR/Git mutation.'}
    atomic_json(AUDIT / 'LEDGER_PUBLICATION_VERIFICATION.json', receipt)
    print(json.dumps(receipt, indent=2))


if __name__ == '__main__':
    main()
