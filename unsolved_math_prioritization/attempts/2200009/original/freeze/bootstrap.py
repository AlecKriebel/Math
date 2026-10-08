#!/usr/bin/env python3
"""Verify all payload bytes against a pinned manifest before executing payload code.
Authenticate this bootstrap itself using the separately supplied external SHA-256.
"""
from pathlib import Path
import hashlib,json,re,stat,subprocess,sys
EXPECTED_MANIFEST='40ab15f865b6965782024a310c3b1dd17fe9b53a2343b1f41980e376d61aa438'
class Rejected(Exception):pass
def need(ok,msg):
    if not ok:raise Rejected(msg)
def sha(b):return hashlib.sha256(b).hexdigest()
def pairs(items):
    out={}
    for k,v in items:need(k not in out,'duplicate JSON key');out[k]=v
    return out
def nonfinite(v):raise Rejected('nonfinite JSON')
def regular(p):
    need(not p.is_symlink() and stat.S_ISREG(p.lstat().st_mode),'not a regular non-symlink file: '+p.name)
def run():
    need(len(sys.argv) in (1,2),'usage: bootstrap.py [packet-directory]')
    here=Path(__file__).resolve().parent
    root=Path(sys.argv[1]) if len(sys.argv)==2 else here/'packet'
    need(not root.is_symlink() and root.is_dir(),'packet directory missing or symlink')
    root=root.resolve();mp=here/'AUTHOR_MANIFEST.json';regular(mp)
    raw=mp.read_bytes();need(sha(raw)==EXPECTED_MANIFEST,'external manifest pin mismatch')
    m=json.loads(raw,object_pairs_hook=pairs,parse_constant=nonfinite)
    need(type(m) is dict and set(m)=={'schema','problem_id','disposition','new_mathematical_approaches','files'},'manifest keys')
    need(type(m['schema']) is str and m['schema']=='mesh-preserver-author-manifest-v1','schema')
    need(type(m['problem_id']) is int and m['problem_id']==2200009,'problem identity')
    need(type(m['disposition']) is str and m['disposition']=='previously_solved','disposition')
    need(type(m['new_mathematical_approaches']) is int and m['new_mathematical_approaches']==0,'approaches')
    need(type(m['files']) is list and bool(m['files']),'inventory')
    names=[]
    for e in m['files']:
        need(type(e) is dict and set(e)=={'path','bytes','sha256'},'entry keys')
        name=e['path'];need(type(name) is str and bool(re.fullmatch(r'[A-Za-z0-9_.-]+',name)) and name not in ('.','..'),'unsafe path')
        need(name not in names,'duplicate path');names.append(name)
        need(type(e['bytes']) is int and e['bytes']>=0,'exact byte count')
        need(type(e['sha256']) is str and bool(re.fullmatch(r'[0-9a-f]{64}',e['sha256'])),'hash syntax')
        p=root/name;regular(p);b=p.read_bytes()
        need(len(b)==e['bytes'] and sha(b)==e['sha256'],'payload size or hash: '+name)
    need(set(p.name for p in root.iterdir())==set(names),'extra or missing payload')
    need({'verify_math.py','CLAIMS.json','EXPECTED.json','run_controls.py'}<=set(names),'required payload absent')
    flags=[] if sys.flags.optimize==0 else ['-O' if sys.flags.optimize==1 else '-OO']
    r=subprocess.run([sys.executable,'-I','-S','-B',*flags,str(root/'verify_math.py'),'--claims',str(root/'CLAIMS.json')],cwd=root,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=120)
    need(r.returncode==0,'diagnostics: '+r.stderr.decode('utf-8','replace'))
    expected=(root/'EXPECTED.json').read_bytes();need(r.stdout==expected,'exact diagnostic output mismatch')
    return {'schema':'mesh-preserver-bootstrap-v1','status':'PASS','manifest_sha256':EXPECTED_MANIFEST,'payload_files':len(names),'diagnostic_sha256':sha(expected),'independent_review':'pending'}
if __name__=='__main__':
    try:print(json.dumps(run(),sort_keys=True,separators=(',',':')))
    except (Rejected,OSError,ValueError,KeyError,TypeError,subprocess.SubprocessError) as e:
        print('REJECT: '+str(e),file=sys.stderr);sys.exit(1)
