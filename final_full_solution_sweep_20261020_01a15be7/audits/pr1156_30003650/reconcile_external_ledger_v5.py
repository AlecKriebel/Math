#!/usr/bin/env python3
"""Reconcile one reviewed, already-published external result; never publish."""
import argparse
import datetime as dt
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import types
import uuid
from urllib.parse import unquote

AUDIT = Path(__file__).resolve().parent
ROOT = AUDIT.parents[1]
# No project code is imported before externally anchored root dependency checks.
SHEET = '1ZljUv5Q98jNXLoHK8WjwrkzSm3dhHC1-7LElcOU7y20'
DEPENDENCIES = ['publication_check.py','sweep_io.py','checkpoint.py',
                'audits/pr0399_30001179/ops_binding.py',
                'audits/pr0399_30001179/prepublication_check.py',
                '../zenodo_deposit_tool/zenodo.py']

PATTERN = re.compile(
    r'30003650|OWR.?15957.?003|CP[ _^+–-]*plus|cp\^?\+|positive[ -]?factor[ -]?rank|2335036[34]|Dickinson.{0,60}rank|'
    r'/pull/1156(?!\d)|\bPR\s*#?1156(?!\d)', re.I)



def require(value, reason):
    if not value:
        raise RuntimeError(reason)


def cli(args):
    return json.loads(subprocess.run(args, capture_output=True, text=True,
                                     check=True).stdout)


def matches(rows):
    return [(n, row) for n, row in enumerate(rows, 1)
            if PATTERN.search(' '.join(map(str, row))) or target_in_row(row, 23350364, [23350363])]


def main():
    plan_path = AUDIT / 'LEDGER_RECONCILIATION_PLAN.json'
    plan_bytes = plan_path.read_bytes()
    plan = json.loads(plan_bytes)
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--acceptance-sha256',required=True)
    args = parser.parse_args()
    require(re.fullmatch('[a-f0-9]{64}',args.acceptance_sha256) is not None, 'External root acceptance SHA required.')
    acceptance_bytes = (AUDIT / 'ROOT_LEDGER_REVIEW05_ACCEPTANCE.json').read_bytes()
    require(hashlib.sha256(acceptance_bytes).hexdigest() == args.acceptance_sha256, 'Root acceptance changed.')
    adopted = json.loads(acceptance_bytes)
    require(set(adopted['dependency_pins']) == set(DEPENDENCIES), 'Incomplete reviewed import inventory.')
    source_bytes = {}
    for rel, expected in adopted['dependency_pins'].items():
        path = ROOT / rel
        require(not path.is_symlink() and path.resolve().is_relative_to(ROOT.parent.resolve()), 'Unsafe dependency path.')
        data = path.read_bytes()
        require(hashlib.sha256(data).hexdigest() == expected, 'Reviewed dependency changed before import.')
        source_bytes[rel] = data
    # Execute the already hash-checked exact source bytes; never consult source
    # search paths or existing .pyc files for a project module.
    module_order = [('sweep_io','sweep_io.py'),('checkpoint','checkpoint.py'),
        ('zenodo','../zenodo_deposit_tool/zenodo.py'),
        ('ops_binding','audits/pr0399_30001179/ops_binding.py'),
        ('publication_check','publication_check.py'),
        ('pr1156_account_reader_final','audits/pr0399_30001179/prepublication_check.py')]
    loaded = {}
    for name, rel in module_order:
        module = types.ModuleType(name)
        module.__file__ = str((ROOT/rel).resolve())
        sys.modules[name] = module
        exec(compile(source_bytes[rel],module.__file__,'exec'),module.__dict__)
        loaded[name] = module
    get = loaded['publication_check'].get
    atomic_json = loaded['sweep_io'].atomic_json
    binding = loaded['ops_binding']
    schema_rows, record_identity_ids = binding.schema_rows,binding.record_identity_ids
    def row_identity_names(cells):
        # Conservative unresolved-resolver leads include bare domains and URI
        # references, regardless of scheme, case, or nested percent encoding.
        # This does not certify that any alias resolves or is URI-equivalent.
        require(isinstance(cells,(list,tuple)), 'Identity row must be text cells.')
        for text in cells:
            require(isinstance(text,str) and len(text)<=1_000_000,'Invalid identity cell.')
            decoded=text
            for _ in range(8):
                nxt=unquote(decoded)
                if nxt==decoded:break
                decoded=nxt
            else:require(unquote(decoded)==decoded,'Deep unresolved resolver encoding requires root review.')
            hosts=re.finditer(r'(?<![A-Za-z0-9_.-])(?P<host>(?:www\.)?(?:shortdoi\.org|(?:dx\.)?doi\.org))(?=$|[/:?#@\\])(?P<tail>[^\s<>"\[\]{}]*)',decoded,re.I)
            for match in hosts:
                host=match.group('host').lower()
                tail=match.group('tail').rstrip('.,;:!?)]}\'')
                if tail in {'','/'}:continue
                require('shortdoi.org' not in host and re.match(r'(?::[0-9]+)?/10\.[0-9]{4,9}/[^/\s].*',tail) is not None,
                        'Unresolved bare/protocol-relative DOI resolver alias requires root review.')
        return binding.row_identity_names(cells)
    def checked_target(cells,identifier,family_ids=()):
        row_identity_names(cells)
        return binding.target_in_row(cells,identifier,family_ids)
    global target_in_row
    target_in_row = checked_target
    started = dt.datetime.now(dt.timezone.utc)
    def fresh():
        age=(dt.datetime.now(dt.timezone.utc)-started).total_seconds()
        require(0<=age<=180,'Final account/provider/ledger observations expired; no append.')

    require(adopted['ready_for_existing_publication_record'] is True,
            'Independent review has not been adopted.')
    require(adopted['helper_sha256'] == hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'Reviewed mutation helper changed.')
    require(adopted['plan_sha256'] == hashlib.sha256(plan_bytes).hexdigest(),
            'Reviewed plan changed.')
    for pin in adopted['review_pins']:
        require(hashlib.sha256((AUDIT / pin['path']).read_bytes()).hexdigest()
                == pin['sha256'], 'Adopted review changed.')
    require(plan['spreadsheet_id'] == SHEET and plan['sheet_gid'] == 1254632077
            and plan['range'] == "'Math Puzzles'!A:D", 'Wrong destination.')
    row = plan['proposed_row']
    require(len(row) == 4 and row[1] == ''
            and row[2] == 'https://doi.org/10.5281/zenodo.23350364'
            and 'Alper Ferudun' in row[3]
            and 'not Alec Kriebel authorship' in row[3], 'Wrong authorship/DOI row.')
    raw = AUDIT / 'private' / ('ledger_' + uuid.uuid4().hex)
    raw.mkdir(parents=True, mode=0o700)

    # Read the complete owned account, including existing/draft records.
    reader = loaded['pr1156_account_reader_final']
    reader.verify_destination()
    client = reader.zenodo.ZenodoClient('production', reader.zenodo.token_for('production'))
    account = reader.account_search(client, '')
    require(23408971 in {item['id'] for item in account['records']}, 'Owned-account known-record positive control missing.')
    atomic_json(raw / 'account.json', account)
    expected_md5 = {f['checksum'].removeprefix('md5:') for f in plan['existing_publication']['files']}
    account_leads = [item['id'] for item in account['records']
                     if PATTERN.search(json.dumps(item,ensure_ascii=False))
                     or target_in_row([json.dumps(item,ensure_ascii=False)],23350364,[23350363])
                     or any(str(f.get('checksum','')).lower().removeprefix('md5:') in expected_md5
                            for f in item.get('files', []))]
    require(not account_leads, 'New own-account result/draft lead requires reconciliation.')

    live = cli(['gh', 'api', 'repos/AlecKriebel/Math/pulls/1156'])
    baseline_pr = next(p for p in json.loads((ROOT / 'rest_inventory.json').read_text())
                       ['pull_requests'] if p['number'] == 1156)
    require(plan['pr'] == 1156 and plan['problem_ids'] == ['30003650']
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
    baseline_bytes = (ROOT / 'raw/pr1156/zenodo_23350364.json').read_bytes()
    require(hashlib.sha256(baseline_bytes).hexdigest() == plan['baseline_provider_sha256'], 'Reviewed provider baseline changed.')
    baseline = json.loads(baseline_bytes)
    body, _ = get('https://zenodo.org/api/records/23350364')
    record = json.loads(body)
    require(record['state'] == 'done' and record['submitted'] is True
            and record['doi'] == '10.5281/zenodo.23350364', 'Record not published.')
    require(record_identity_ids(record,23350364) == [23350363,23350364], 'Record family changed.')
    require(record['metadata'] == baseline['metadata'], 'Publication metadata changed.')
    file_map = lambda x: {f['key']: (f['size'], f['checksum']) for f in x['files']}
    require(len(file_map(record))==len(record['files'])==3, 'Duplicate or unexpected public file inventory.')
    require(file_map(record) == file_map(baseline) == {f['name']: (f['size'], f['checksum']) for f in plan['existing_publication']['files']}, 'Published files changed.')
    for f in plan['existing_publication']['files']:
        payload, _ = get(next(x['links']['self'] for x in record['files'] if x['key'] == f['name']))
        require(len(payload) == f['size'] and hashlib.sha256(payload).hexdigest() == f['sha256']
                and 'md5:' + hashlib.md5(payload).hexdigest() == f['checksum'], 'Fresh provider payload changed.')
    _, resolution = get(row[2])
    require(resolution['status'] == 200 and re.fullmatch(
        r'https://zenodo.org/records?/23350364/?', resolution['final_url']),
        'DOI destination mismatch.')
    atomic_json(raw / 'record.json', record)
    params = {'spreadsheetId': SHEET, 'range': "'Math Puzzles'!A:AQ",
              'valueRenderOption': 'FORMATTED_VALUE'}

    def read(label):
        result = cli(['gws', 'sheets', 'spreadsheets', 'values', 'get',
                      '--params', json.dumps(params)])
        atomic_json(raw / (label + '.json'), result)
        require(result['values'][0] == plan['schema_columns'], 'Sheet schema changed.')
        rows = schema_rows(result)
        for cells in rows: row_identity_names(cells)
        require(result.get('majorDimension')=='ROWS' and re.fullmatch(r"'Math Puzzles'!A1:AQ[1-9][0-9]*",result.get('range','')) is not None, 'Full ledger read range changed.')
        return rows

    sheet_info = cli(['gws','sheets','spreadsheets','get','--params',json.dumps({
        'spreadsheetId':SHEET,'fields':'spreadsheetId,sheets(properties(sheetId,title))'})])
    atomic_json(raw/'sheet_identity.json',sheet_info)
    require(sheet_info.get('spreadsheetId')==SHEET and
            [e['properties']['title'] for e in sheet_info['sheets'] if e['properties']['sheetId']==1254632077]==['Math Puzzles'],
            'Sheet title/gid binding changed.')
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
        directory_fd = os.open(intent.parent,os.O_RDONLY)
        try: os.fsync(directory_fd)
        finally: os.close(directory_fd)
        immediate = read('immediate_before_append')
        require(immediate == before and not matches(immediate), 'Concurrent ledger change; stop without append.')
        current_pr = cli(['gh', 'api', 'repos/AlecKriebel/Math/pulls/1156'])
        require(current_pr['head']['sha'] == plan['head'] and current_pr['base']['sha'] == plan['base'] and current_pr['body'] == live['body'] and current_pr['state']==live['state'] and current_pr['merged'] is live['merged'] and current_pr['draft'] is live['draft'], 'PR advanced before append.')
        fresh()
        append_params = {'spreadsheetId': SHEET, 'range': plan['range'],
                         'valueInputOption': 'RAW', 'insertDataOption': 'INSERT_ROWS',
                         'includeValuesInResponse': True}
        response = cli(['gws', 'sheets', 'spreadsheets', 'values', 'append',
                        '--params', json.dumps(append_params), '--json',
                        json.dumps({'majorDimension': 'ROWS', 'values': [row]})])
        atomic_json(AUDIT / 'LEDGER_RECONCILIATION_RESPONSE.json', response)
        require(response.get('spreadsheetId')==SHEET
                and response['updates'].get('spreadsheetId')==SHEET
                and response['updates']['updatedData'].get('majorDimension')=='ROWS'
                and response['updates']['updatedData'].get('range')==response['updates']['updatedRange']
                and response['updates']['updatedCells']==4
                and re.fullmatch(r"(?:'Math Puzzles'|Math Puzzles)!A[1-9][0-9]*:D[1-9][0-9]*",response['updates']['updatedRange']) is not None
                and response['updates']['updatedRows'] == 1
                and response['updates']['updatedColumns'] == 4
                and response['updates']['updatedData']['values'] == [row],
                'Unexpected append response; inspect live sheet before recovery.')
        appended = True
    after = read('after')
    require(after[:len(before)] == before, 'Preexisting ledger rows changed; reconcile, never retry blindly.')
    found = matches(after)
    require(len(found) == 1 and found[0][1] == row,
            'Final row/uniqueness differs; reconcile without blind retry.')
    require(sum(target_in_row(r,23350364,[23350363]) for r in after)==1, 'Duplicate record/concept identity.')
    if appended:
        require(len(after)==len(before)+1 and after[-1]==row, 'Unexpected postappend row inventory.')
        expected_range = r"(?:'Math Puzzles'|Math Puzzles)!A"+str(found[0][0])+':D'+str(found[0][0])
        require(re.fullmatch(expected_range,response['updates']['updatedRange']) is not None,'Append response range does not bind exact final row.')
    receipt = {'at': dt.datetime.now(dt.timezone.utc).isoformat(), 'pr': 1156,
               'status': 'verified', 'external_publication': True,
               'external_author': 'Alper Ferudun', 'new_publication': False,
               'new_row': appended, 'read_back_exact': True,
               'unique_target_and_DOI': True, 'row_number': found[0][0], 'values': row,
               'doi': record['doi'], 'doi_resolution': resolution,
               'ledger_rows_before': len(before), 'ledger_rows_after': len(after),
               'complete_account_records': account['total'], 'own_account_leads': [],
               'checksum_and_semantic_account_scan':True,'record_and_concept_ids':[23350363,23350364],
               'all_preexisting_rows_preserved':True,'exact_four_updated_cells_and_range':True,
               'known_owned_positive_control':23408971,'project_dependencies_executed_from_verified_source_bytes':True,'all_four_column_schema_and_gid_verified':True,
               'remote_main': remote_main['object']['sha'], 'local_branch': local_branch,
               'live_pr_head': live['head']['sha'], 'live_pr_state': live['state'],
               'live_pr_merged': live['merged'], 'live_pr_draft': live['draft'],
               'raw_receipts': str(raw.relative_to(ROOT)),
               'scope': 'One existing external publication recorded; no Zenodo/PR/Git mutation.'}
    atomic_json(AUDIT / 'LEDGER_PUBLICATION_VERIFICATION.json', receipt)
    print(json.dumps(receipt, indent=2))


if __name__ == '__main__':
    main()
