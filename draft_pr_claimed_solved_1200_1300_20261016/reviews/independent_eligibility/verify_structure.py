#!/usr/bin/env python3
"""Second parser checks every target has exactly the table's twelve columns."""
import base64
import collections
import datetime as dt
import hashlib
import json
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parent
data = json.loads((ROOT / 'independent_eligibility.json').read_text())
targets = {pid for p in data['pull_requests'] for pid in p['problem_ids']}
representatives = {r['queue_blob_sha']:r for r in data['head_queue_receipts']}
representatives[data['main_queue_receipt']['queue_blob_sha']] = data['main_queue_receipt']

def split_markdown(line):
    fields, current = [], ''
    escapes = 0
    for ch in line.strip():
        if ch == '|' and escapes % 2 == 0:
            fields.append(current.strip())
            current = ''
        else:
            current += ch
        escapes = escapes + 1 if ch == '\\' else 0
    fields.append(current.strip())
    assert fields[0] == fields[-1] == ''
    return fields[1:-1]

checks = []
for blob, receipt in sorted(representatives.items()):
    response = json.loads(subprocess.check_output(['gh','api',receipt['endpoint']]))
    payload = base64.b64decode(response['content'])
    assert response['sha'] == blob
    assert hashlib.sha1(b'blob ' + str(len(payload)).encode() + b'\0' + payload).hexdigest() == blob
    matches, header = {}, None
    for lineno,line in enumerate(payload.decode().splitlines(),1):
        if not line.startswith('|'):
            continue
        values = split_markdown(line)
        if 'Status' in values:
            header = values
            assert header == ['Rank','ID / code','Problem','EV','Impact (/10)','Difficulty','Proposed','Status','Turns','Chat','Findings','DOI']
        if not header:
            continue
        match = re.match(r'^`?(\d+)(?=[` /]|$)',values[1])
        if match and match.group(1) in targets:
            pid = match.group(1)
            assert len(values) == len(header) == 12, (blob,pid,len(values))
            assert values[7] == 'queued', (blob,pid,values[7])
            assert pid not in matches
            matches[pid] = {'line':lineno,'id_cell':values[1],'status':values[7],'columns':len(values)}
    assert set(matches) == targets
    checks.append({'blob_sha':blob,'representative_commit':receipt['commit_sha'],
                   'header':header,'all_103_targets_have_12_columns':True,
                   'all_103_exact_statuses':'queued','rows':matches})

excluded = collections.Counter()
for p in data['pull_requests']:
    excluded.update((set(p['title_numeric_tokens'])|set(p['branch_numeric_tokens']))-set(p['problem_ids']))
assert set(excluded) == {'20261011','1110'}
assert [p['number'] for p in data['pull_requests'] if not set(p['title_numeric_tokens']) & set(p['problem_ids'])] == [1297]
assert next(p for p in data['pull_requests'] if p['number']==1210)['problem_ids']==['5000002','5000003']
assert next(p for p in data['pull_requests'] if p['number']==1214)['problem_ids']==['30006433','30006435']
assert next(p for p in data['pull_requests'] if p['number']==1297)['problem_ids']==['30002198']
result = {'completed_utc':dt.datetime.now(dt.timezone.utc).isoformat(),
          'second_parser':'escape-parity Markdown pipe scanner, header-defined 12 fields, target rows only',
          'excluded_numeric_tokens':dict(excluded),
          'excluded_token_reasons':{'20261011':'branch timestamp','1110':'EP1110 secondary label in PR1278; primary target is 2497'},
          'checks':checks,'unresolved_concerns':[]}
(ROOT/'structure_verification.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'verified_queue_blobs':len(checks),'target_rows_per_blob':len(targets),'unresolved_concerns':[]}))
