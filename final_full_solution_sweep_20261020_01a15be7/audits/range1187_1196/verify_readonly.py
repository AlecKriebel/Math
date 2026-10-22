#!/usr/bin/env python3
"""Read-only GitHub and numeric-sheet identity audit. No candidate code runs.

Default checks all ten live PR endpoints, complete comparison paths and three
immutable source blobs each. --ledger emits aggregate leads only. --read PR
NAME prints one verified immutable authored text. This program writes no files.
"""
import argparse
import base64
import concurrent.futures
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import subprocess
import time

ROOT = Path(__file__).resolve().parents[2]
REPO = 'AlecKriebel/Math'
NUMBERS = tuple(range(1187, 1197))
PRIMARY = {n: ('AUDIT.md' if n == 1190 else 'PROOF.md') for n in NUMBERS}
BOOK = '1ZljUv5Q98jNXLoHK8WjwrkzSm3dhHC1-7LElcOU7y20'
GID = 1254632077


def require(value, message):
    if not value:
        raise RuntimeError(message)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def gh(endpoint):
    for attempt in range(4):
        result = subprocess.run(['gh', 'api', 'repos/'+REPO+'/'+endpoint], capture_output=True)
        if result.returncode == 0:
            return json.loads(result.stdout)
        transient = any(x in result.stderr for x in (b'HTTP 502', b'HTTP 503', b'HTTP 504'))
        if not transient or attempt == 3:
            raise RuntimeError(result.stderr.decode(errors='replace')[:1500])
        time.sleep(2**attempt)


def evidence(number):
    require(number in NUMBERS, 'PR outside bounded review')
    return json.loads((ROOT/f'eligibility/pr{number}.json').read_bytes())


def source(number, name):
    e = evidence(number)
    found = [x for x in e['files'] if Path(x['filename']).name == name]
    require(len(found) == 1, 'Text name not unique')
    expected = found[0]
    value = gh('git/blobs/'+expected['sha'])
    require(value['encoding'] == 'base64', 'Unexpected blob encoding')
    raw = base64.b64decode(value['content'])
    identity = hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
    require(identity == expected['sha'] == value['sha'] and value['size'] == len(raw), 'Blob mismatch')
    return raw, {'path': expected['filename'], 'git_blob': identity,
                 'bytes': len(raw), 'sha256': sha(raw)}


def check(number):
    e = evidence(number)
    live = gh('pulls/'+str(number))
    base, head = e['inventory_base_sha'], e['inventory_head_sha']
    require(live['head']['sha'] == head and live['base']['sha'] == base, 'Live endpoint drift')
    comparison = gh('compare/'+base+'...'+head)
    files = comparison['files']
    require(len(files) < 300 and comparison['base_commit']['sha'] == base
            and comparison['commits'] and comparison['commits'][-1]['sha'] == head,
            'Incomplete comparison or endpoint mismatch')
    key = lambda f: (f['filename'], f['sha'], f['status'])
    require(sorted(map(key, files)) == sorted(map(key, e['files']))
            and len(files) == e['file_count'], 'Complete path/blob/status mismatch')
    require(all(f['status'] == 'added' for f in files), 'Unexpected non-addition')
    require(not any(Path(f['filename']).name == 'QUEUE.md' for f in files), 'Unexpected QUEUE edit')
    disposition_bytes = (ROOT/f'PR{number}_DISPOSITION.json').read_bytes()
    d = json.loads(disposition_bytes)
    require(d['inventory_head_sha'] == head and d['inventory_base_sha'] == base
            and d['inventory_body_sha256'] == sha((live['body'] or '').encode()), 'Disposition text drift')
    acceptance = 'ACCEPTANCE.md' if number == 1189 else 'ACCEPTANCE.json'
    pins = [source(number, name)[1] for name in (PRIMARY[number], 'README.md', acceptance)]
    return {'pr': number, 'head': head, 'base': base,
            'merge_base': comparison['merge_base_commit']['sha'],
            'comparison_commits': comparison['total_commits'],
            'live_state': live['state'], 'live_draft': live['draft'], 'live_merged': live['merged'],
            'body_sha256': sha((live['body'] or '').encode()), 'body_matches_disposition': True,
            'complete_changed_paths': sorted([{'path': f['filename'], 'git_blob': f['sha'],
                                              'status': f['status']} for f in files], key=lambda f:f['path']),
            'no_QUEUE_change': True, 'immutable_texts': pins,
            'disposition_sha256': sha(disposition_bytes), 'classification': d['current_classification']}


def ledger():
    def cli(parts, params, body=None):
        cmd = ['gws', 'sheets', 'spreadsheets', *parts, '--params', json.dumps(params)]
        if body is not None:
            cmd += ['--json', json.dumps(body)]
        result = subprocess.run(cmd, capture_output=True, check=True)
        return json.loads(result.stdout), result.stdout
    metadata, unused = cli(['get'], {'spreadsheetId': BOOK, 'fields':'spreadsheetId,sheets(properties)'})
    require(metadata['spreadsheetId'] == BOOK, 'Metadata book mismatch')
    target = [x['properties'] for x in metadata['sheets'] if x['properties']['sheetId'] == GID]
    require(len(target) == 1 and target[0]['title'] == 'Math Puzzles'
            and target[0]['sheetType'] == 'GRID' and target[0]['gridProperties']['columnCount'] == 43,
            'Numeric sheet identity changed')
    result, raw = cli(['values', 'batchGetByDataFilter'], {'spreadsheetId': BOOK},
        {'dataFilters':[{'gridRange':{'sheetId':GID}}], 'majorDimension':'ROWS',
         'valueRenderOption':'UNFORMATTED_VALUE'})
    require(result['spreadsheetId'] == BOOK and len(result['valueRanges']) == 1, 'Read book/match mismatch')
    match = result['valueRanges'][0]
    require(match['dataFilters'] == [{'gridRange':{'sheetId':GID}}], 'Numeric filter mismatch')
    view = match['valueRange']
    require(view['majorDimension'] == 'ROWS' and view['range'] == "'Math Puzzles'!A1:AQ"+
            str(target[0]['gridProperties']['rowCount']), 'All-column sheet extent mismatch')
    rows = view['values']
    require(rows[0] == ['Original Problem','Solution Chat URL','DOI','Notes'], 'Header mismatch')
    terms = ['EP509','Hayman 4.7','EP677','EP839','EP730','EP757','EP885','EP1122','EP1016',
             'strong Sidon','equal prime','Blair','Freud','balanced permutation','Beniamini',
             '10.1007/s00493-024-00127-x','Eulerian multigraph','chip-firing']
    terms += [evidence(n)['path_problem_ids'][0] for n in NUMBERS]
    terms += ['/pull/'+str(n) for n in NUMBERS]
    leads = {t:[i for i,r in enumerate(rows,1) if t.casefold() in ' '.join(map(str,r)).casefold()] for t in terms}
    return {'at':datetime.now(timezone.utc).isoformat(),'spreadsheet_id':BOOK,'sheet_gid':GID,
            'sheet_title':target[0]['title'],'range':view['range'],'rows':len(rows),
            'max_populated_columns':max(map(len,rows)),'stdout_bytes':len(raw),'stdout_sha256':sha(raw),
            'leads':{t:h for t,h in leads.items() if h},'raw_retained':False,'read_only':True,
            'limits':'All term/number matches are leads requiring semantic source comparison; no absence theorem.'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--ledger', action='store_true')
    parser.add_argument('--read', nargs=2)
    args = parser.parse_args()
    if args.ledger:
        print(json.dumps(ledger(), indent=2))
    elif args.read:
        raw, pin = source(int(args.read[0]), args.read[1])
        print(json.dumps(pin)); print(raw.decode())
    else:
        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
            checks = list(pool.map(check, NUMBERS))
        state_bytes = (ROOT/'STATE.json').read_bytes(); state = json.loads(state_bytes)
        print(json.dumps({'at':datetime.now(timezone.utc).isoformat(),'read_only':True,
          'checks':checks,'tracking1194':[x for x in state.get('required_existing_publication_reconciliations',[])
                                       if x.get('pr') == 1194],
          'state_sha256':sha(state_bytes)}, indent=2))
