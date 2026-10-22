#!/usr/bin/env python3
"""Independent, read-only GitHub/GWS audit. Never executes proposal code.

Default emits bindings as JSON. --read PR FILE prints the immutable text.
--ledger emits only hashes and matching lead row numbers; no raw private rows.
Uses installed authenticated gh/gws clients; writes no files or refs.
"""
import argparse
import base64
import concurrent.futures
import hashlib
import json
import pathlib
import re
import subprocess
from datetime import datetime, timezone

ROOT = pathlib.Path(__file__).resolve().parents[2]
REPO = 'AlecKriebel/Math'
SHEET = '1ZljUv5Q98jNXLoHK8WjwrkzSm3dhHC1-7LElcOU7y20'
RANGE = "'Math Puzzles'!A:AQ"
PRIMARY = {
 1161:'PROOF.md',1162:'PROOF.md',1163:'PROOF.md',1164:'COROLLARY.md',
 1165:'RESULT.md',1166:'PROOF.md',1167:'ENDPOINT_AND_PROOF_NOTES.md',
 1168:'AUDIT_REPORT.md',1169:'MATHEMATICAL_AUDIT.md',1170:'MATHEMATICAL_AUDIT.md',
 1171:'RESULT.md',1172:'PHASE_TAILS.md',1173:'PROOF.md',1174:'AUDIT.md',
 1175:'MATHEMATICAL_AUDIT.md'}

def sha(data):
    return hashlib.sha256(data).hexdigest()

def gh(path):
    p = subprocess.run(['gh','api',path],capture_output=True,check=True)
    return json.loads(p.stdout)

def source(n):
    return json.loads((ROOT/f'eligibility/pr{n:04}.json').read_text())

def blob(n, name):
    e=source(n)
    f=next(x for x in e['files'] if pathlib.PurePosixPath(x['filename']).name==name)
    b=gh(f'repos/{REPO}/git/blobs/{f["sha"]}')
    data=base64.b64decode(b['content'])
    calculated=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
    if calculated!=f['sha'] or b['sha']!=f['sha'] or b['size']!=len(data):
        raise RuntimeError('Blob content identity mismatch')
    return data,{'path':f['filename'],'git_blob':calculated,'bytes':len(data),'sha256':sha(data)}

def check(n):
    e=source(n)
    p=gh(f'repos/{REPO}/pulls/{n}')
    base=e['inventory_base_sha'];head=e['inventory_head_sha']
    if p['head']['sha']!=head or p['base']['sha']!=base:
        raise RuntimeError(f'PR{n}: changed live head/base')
    c=gh(f'repos/{REPO}/compare/{base}...{head}')
    files=c['files']
    if len(files)>=300 or c['base_commit']['sha']!=base or c['commits'][-1]['sha']!=head:
        raise RuntimeError(f'PR{n}: incomplete or unbound comparison')
    expected={(f['filename'],f['sha'],f['status']) for f in e['files']}
    actual={(f['filename'],f['sha'],f['status']) for f in files}
    if actual!=expected or len(files)!=e['file_count']:
        raise RuntimeError(f'PR{n}: cached complete paths/blobs differ')
    queues=[f['filename'] for f in files if pathlib.PurePosixPath(f['filename']).name=='QUEUE.md']
    if queues: raise RuntimeError(f'PR{n}: unexpected QUEUE change')
    docs=[]
    for name in [PRIMARY[n],'README.md']:
        data,pin=blob(n,name);docs.append(pin)
    d=json.loads((ROOT/f'PR{n}_DISPOSITION.json').read_text())
    if sha(p['body'].encode())!=d['inventory_body_sha256']:
        raise RuntimeError(f'PR{n}: live body changed from the classified claim')
    return {'pr':n,'url':p['html_url'],'base':base,'head':head,
      'merge_base':c['merge_base_commit']['sha'],'comparison_status':c['status'],
      'last_comparison_commit':c['commits'][-1]['sha'],'total_commits':c['total_commits'],
      'comparison_file_count':len(files),'files':sorted([{'path':f['filename'],'blob':f['sha'],
      'status':f['status']} for f in files],key=lambda x:x['path']),
      'cached_paths_blobs_statuses_equal':True,'queue_changed_paths':queues,
      'live_state':p['state'],'live_merged':p['merged'],'live_draft':p['draft'],
      'body_sha256':sha(p['body'].encode()),
      'body_matches_disposition':sha(p['body'].encode())==d['inventory_body_sha256'],
      'documents_content_verified':docs,'disposition_sha256':sha((ROOT/f'PR{n}_DISPOSITION.json').read_bytes())}

def ledger():
    params={'spreadsheetId':SHEET,'range':RANGE,'valueRenderOption':'FORMATTED_VALUE'}
    p=subprocess.run(['gws','sheets','spreadsheets','values','get','--params',json.dumps(params)],
                     capture_output=True,check=True)
    value=json.loads(p.stdout);rows=value['values']
    ids=[source(n)['path_problem_ids'][0] for n in range(1161,1176)]
    phrases=['relative ends','singleton','affine residue','factorial-minus-one',
      'Koukoulopoulos','maximal parking','3-permutable','Lavrentiev','tree torsor',
      'symmetry-respecting','Geneson','2609.25107','Tokengrinder','Erdos252',
      'logarithmic mass','running lcm','running-lcm','coprime','consecutive sums',
      'distinct block','reciprocal triples','Cambie','Khanukov','5/8']
    matches={}
    for term in ids+[f'/pull/{n}' for n in range(1161,1176)]+phrases:
        hits=[i for i,row in enumerate(rows,1) if term.lower() in ' '.join(map(str,row)).lower()]
        if hits:matches[term]=hits
    return {'checked_at':datetime.now(timezone.utc).isoformat(),'spreadsheet_id':SHEET,
      'range':RANGE,'value_render_option':'FORMATTED_VALUE','rows':len(rows),
      'max_columns':max(map(len,rows)),'stdout_bytes':len(p.stdout),'stdout_sha256':sha(p.stdout),
      'read_only':True,'raw_retained':False,'matching_terms_and_rows':matches,
      'note':'Matches are leads requiring human semantic adjudication; numeric years are not identities.'}

if __name__=='__main__':
    a=argparse.ArgumentParser();a.add_argument('--read',nargs=2);a.add_argument('--ledger',action='store_true')
    args=a.parse_args()
    if args.read:
        data,pin=blob(int(args.read[0]),args.read[1]);print(json.dumps(pin));print(data.decode())
    elif args.ledger: print(json.dumps(ledger(),indent=2))
    else:
        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
            results=list(pool.map(check,range(1161,1176)))
        print(json.dumps({'checked_at':datetime.now(timezone.utc).isoformat(),'repository':REPO,
          'read_only':True,'checks':results},indent=2))
