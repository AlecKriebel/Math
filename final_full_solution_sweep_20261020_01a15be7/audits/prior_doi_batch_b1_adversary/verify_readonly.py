"""Read-only evidence, PR identity, source-data arithmetic, and live ledger checks."""
from pathlib import Path, PurePosixPath
import argparse
import concurrent.futures
import datetime as dt
import hashlib
import json
import subprocess
import sys
import unicodedata

HERE=Path(__file__).resolve().parent
REPO='AlecKriebel/Math'
BOOK='1ZljUv5Q98jNXLoHK8WjwrkzSm3dhHC1-7LElcOU7y20'

def need(ok,message):
    if not ok:raise RuntimeError(message)

def sha(b):return hashlib.sha256(b).hexdigest()

def verify_pins(name,complete):
    m=json.loads((HERE/name).read_bytes());files=m['files'];known=set()
    for e in files:
        p=PurePosixPath(e['path']);need(not p.is_absolute() and '..' not in p.parts,'Unsafe manifest path')
        path=HERE/p;need(not any(HERE.joinpath(*p.parts[:i]).is_symlink() for i in range(1,len(p.parts)+1)),'Symlink')
        b=path.read_bytes();need(len(b)==e['bytes'] and sha(b)==e['sha256'],'Input drift '+e['path']);known.add(e['path'])
    if complete:
        actual={p.relative_to(HERE).as_posix() for p in HERE.rglob('*') if p.is_file() and p.relative_to(HERE).as_posix()!='MANIFEST.json'}
        need(actual==known,'Complete evidence closure differs')
    return len(files)

def gh(path):
    q=subprocess.run(['gh','api','repos/'+REPO+'/'+path],capture_output=True)
    need(q.returncode==0,q.stderr.decode(errors='replace')[:600]);return json.loads(q.stdout)

def binding(e):
    p=gh('pulls/'+str(e['pr']));head=p['head']['sha'];base=p['base']['sha']
    need(head==e['head'] and base==e['base'] and sha((p['body'] or '').encode())==e['body_sha256'],'Live PR drift')
    c=gh('compare/'+base+'...'+head)
    need(len(c['files'])<300 and c['base_commit']['sha']==base and c['commits'][-1]['sha']==head,'Compare not complete')
    actual=sorted((f['filename'],f['sha'],f['status']) for f in c['files'])
    need(actual==sorted(tuple(f) for f in e['complete_changed_paths']),'Path/blob/status drift')
    return {'pr':e['pr'],'complete_paths':len(actual),'head':head,'body_matches':True}

def ledger():
    request={'dataFilters':[{'gridRange':{'sheetId':1254632077}}],'majorDimension':'ROWS','valueRenderOption':'UNFORMATTED_VALUE'}
    q=subprocess.run(['gws','sheets','spreadsheets','values','batchGetByDataFilter','--params',json.dumps({'spreadsheetId':BOOK}),'--json',json.dumps(request)],capture_output=True)
    need(q.returncode==0,'Fresh GWS read failed');j=json.loads(q.stdout);need(j['spreadsheetId']==BOOK,'Workbook drift')
    matches=j['valueRanges'];need(len(matches)==1 and matches[0]['dataFilters']==request['dataFilters'],'Wrong numeric filter')
    v=matches[0]['valueRange'];need(v['majorDimension']=='ROWS' and v['range'].startswith("'Math Puzzles'!A1:AQ"),'Incomplete range')
    rows=v['values'];need(rows[0]==['Original Problem','Solution Chat URL','DOI','Notes'],'Header drift')
    proposals=json.loads((HERE/'PROPOSED_ROWS.json').read_text())['items'];hits=[]
    semantic=json.loads((HERE/'private_sources/INITIAL_LEDGER_MATCHES.json').read_text())
    for p,s in zip(proposals,semantic):
        need(p['pr']==s['pr'],'Proposal order drift')
        aliases=p['identity_aliases']+s['aliases']
        leads=[]
        for i,row in enumerate(rows,1):
            text=unicodedata.normalize('NFKC',' '.join(map(str,row))).casefold()
            terms=[a for a in aliases if unicodedata.normalize('NFKC',a).casefold() in text]
            if terms:leads.append({'row':i,'terms':list(dict.fromkeys(terms))})
        if leads:hits.append({'pr':p['pr'],'leads':leads})
    return {'at':dt.datetime.now(dt.timezone.utc).isoformat(),'rows':len(rows),'range':v['range'],
            'stdout_bytes':len(q.stdout),'stdout_sha256':sha(q.stdout),'result_identity_leads':hits,
            'raw_retained_by_this_verifier':False,'mutations':False}

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--inputs-only',action='store_true');args=parser.parse_args()
    count=verify_pins('INPUT_PINS.json' if args.inputs_only else 'MANIFEST.json',not args.inputs_only)
    bindings=json.loads((HERE/'PR_BINDINGS.json').read_text())
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as p:checks=list(p.map(binding,bindings))
    math_result=subprocess.run([sys.executable,'-I','-S','-B',str(HERE/'verify_math_bridges.py')],capture_output=True)
    need(math_result.returncode==0,'Exact source math replay failed');math_json=json.loads(math_result.stdout);need(math_json['status']=='PASS','Math did not pass')
    result=ledger()
    print(json.dumps({'at':dt.datetime.now(dt.timezone.utc).isoformat(),'status':'PASS_READONLY_IDENTITY_CHECKS',
       'pinned_files_checked':count,'bindings':checks,'complete_paths':sum(x['complete_paths'] for x in checks),
       'math_replay_stdout_sha256':sha(math_result.stdout),'math_replay_stderr_bytes':len(math_result.stderr),
       'ledger':result,'limits':'A matching live ledger lead requires semantic reconciliation before a write; this verifier never writes services or claims a global duplicate lock.'},indent=2))

if __name__=='__main__':main()
