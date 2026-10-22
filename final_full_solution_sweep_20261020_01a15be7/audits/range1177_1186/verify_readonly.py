#!/usr/bin/env python3
"""Read-only independent PR identity/ledger checks; never executes proposal code.
Default emits exact live/pinned source bindings. --read PR FILE emits one text.
--ledger emits aggregate identity leads without retaining private raw rows.
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
PRIMARY = {1177:'PROOF.md',1178:'PROOF.md',1179:'PROOF.md',1180:'AUDIT.md',
           1181:'PROOF.md',1182:'AUDIT.md',1183:'AUDIT.md',1184:'AUDIT.md',
           1185:'PROOF.md',1186:'AUDIT.md'}

def sha(data):
    return hashlib.sha256(data).hexdigest()

def gh(path):
    for attempt in range(4):
        p = subprocess.run(['gh','api',path],capture_output=True)
        if p.returncode == 0:
            return json.loads(p.stdout)
        if attempt == 3 or not any(c in p.stderr for c in [b'HTTP 502',b'HTTP 503',b'HTTP 504']):
            raise RuntimeError(p.stderr.decode(errors='replace')[:1500])
        time.sleep(2**attempt)

def evidence(n):
    return json.loads((ROOT/f'eligibility/pr{n:04d}.json').read_text())

def text_blob(n, name):
    e=evidence(n)
    f=next(f for f in e['files'] if Path(f['filename']).name==name)
    value=gh(f'repos/{REPO}/git/blobs/{f["sha"]}')
    raw=base64.b64decode(value['content'])
    identity=hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
    if identity != f['sha'] or value['sha'] != identity or value['size'] != len(raw):
        raise RuntimeError('Immutable source identity mismatch')
    return raw,{'path':f['filename'],'git_blob':identity,'bytes':len(raw),'sha256':sha(raw)}

def check(n):
    e=evidence(n)
    p=gh(f'repos/{REPO}/pulls/{n}')
    base=e['inventory_base_sha'];head=e['inventory_head_sha']
    if p['head']['sha']!=head or p['base']['sha']!=base:
        raise RuntimeError(f'PR{n} live endpoint drift')
    c=gh(f'repos/{REPO}/compare/{base}...{head}')
    files=c['files']
    if len(files)>=300 or c['base_commit']['sha']!=base or not c['commits'] or c['commits'][-1]['sha']!=head:
        raise RuntimeError(f'PR{n} incomplete/unbound comparison')
    expected={(f['filename'],f['sha'],f['status']) for f in e['files']}
    actual={(f['filename'],f['sha'],f['status']) for f in files}
    if actual!=expected or len(files)!=e['file_count']:
        raise RuntimeError(f'PR{n} complete path/blob/status mismatch')
    if any(Path(f['filename']).name=='QUEUE.md' for f in files):
        raise RuntimeError(f'PR{n} unexpected QUEUE change')
    dpath=ROOT/f'PR{n:04d}_DISPOSITION.json';d=json.loads(dpath.read_text())
    body=(p['body'] or '').encode()
    if sha(body)!=d['inventory_body_sha256'] or d['inventory_head_sha']!=head or d['inventory_base_sha']!=base:
        raise RuntimeError(f'PR{n} classified text drift')
    selected=[]
    for name in [PRIMARY[n],'README.md']:
        unused,pin=text_blob(n,name);selected.append(pin)
    return {'pr':n,'base':base,'head':head,'merge_base':c['merge_base_commit']['sha'],
      'last_comparison_commit':c['commits'][-1]['sha'],'comparison_commits':c['total_commits'],
      'live_state':p['state'],'live_draft':p['draft'],'live_merged':p['merged'],
      'body_sha256':sha(body),'body_matches_disposition':True,
      'complete_changed_paths':sorted([{'path':f['filename'],'blob':f['sha'],'status':f['status']} for f in files],key=lambda f:f['path']),
      'no_QUEUE_change':True,'selected_texts':selected,
      'disposition_sha256':sha(dpath.read_bytes()),'scientific_disposition_final':d.get('scientific_disposition_final',True)}

def ledger():
    params={'spreadsheetId':'1ZljUv5Q98jNXLoHK8WjwrkzSm3dhHC1-7LElcOU7y20',
      'range':"'Math Puzzles'!A:AQ",'valueRenderOption':'FORMATTED_VALUE'}
    p=subprocess.run(['gws','sheets','spreadsheets','values','get','--params',json.dumps(params)],capture_output=True,check=True)
    value=json.loads(p.stdout);rows=value['values']
    terms=['EP377','EP385','EP423','EP413','EP461','EP486','EP488','EP538','EP710','EP711',
      'carry-depth','composite overshoot','Hofstadter','smooth components','Shouqiao Wang',
      'Declan Gessel','STARFLEET','fixed-start','distinct multiples','18154085']
    ids=[evidence(n)['path_problem_ids'][0] for n in range(1177,1187)]
    matches={}
    for term in terms+ids+[f'/pull/{n}' for n in range(1177,1187)]:
        hits=[i for i,row in enumerate(rows,1) if term.lower() in ' '.join(map(str,row)).lower()]
        if hits: matches[term]=hits
    return {'checked_at':datetime.now(timezone.utc).isoformat(),'spreadsheet_id':params['spreadsheetId'],
      'range':params['range'],'rows':len(rows),'max_populated_columns':max(map(len,rows)),
      'stdout_bytes':len(p.stdout),'stdout_sha256':sha(p.stdout),'raw_retained':False,
      'read_only':True,'term_row_leads':matches,'limits':'Numeric substring leads require semantic identity adjudication.'}

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--read',nargs=2);parser.add_argument('--ledger',action='store_true')
    args=parser.parse_args()
    if args.read:
        raw,pin=text_blob(int(args.read[0]),args.read[1]);print(json.dumps(pin));print(raw.decode())
    elif args.ledger:
        print(json.dumps(ledger(),indent=2))
    else:
        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
            checks=list(pool.map(check,range(1177,1187)))
        s=json.loads((ROOT/'STATE.json').read_text())
        tracked=[x for x in s.get('reopened_candidates',[]) if x['pr']==1180]
        print(json.dumps({'checked_at':datetime.now(timezone.utc).isoformat(),'read_only':True,
          'checks':checks,'state_observation':{'next_pr':s['next_pr'],'candidate1180_tracking':tracked,
          'root_state_sha256':sha((ROOT/'STATE.json').read_bytes())}},indent=2))
