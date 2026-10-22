"""Externally pinned audit inventory and independent finite-control replay."""
import argparse
import ast
import hashlib
import json
from pathlib import Path
import re
import runpy
import stat

class AuditError(Exception):pass

def demand(x,s):
    if not x:raise AuditError(s)

def unique(pairs):
    x={}
    for k,v in pairs:
        demand(k not in x,'duplicate JSON key');x[k]=v
    return x

def run(root,pin):
    demand(re.fullmatch('[0-9a-f]{64}',pin) is not None,'invalid external audit pin')
    p=root/'MANIFEST.json';demand(p.is_file() and not p.is_symlink(),'invalid audit manifest')
    raw=p.read_bytes();demand(hashlib.sha256(raw).hexdigest()==pin,'audit manifest pin mismatch')
    m=json.loads(raw,object_pairs_hook=unique)
    demand(isinstance(m,dict) and m.get('format')=='rational-orbit-independent-audit-v1','wrong audit format')
    f=m['files'];demand(isinstance(f,dict) and bool(f),'wrong audit inventory')
    actual=set()
    for p in root.iterdir():
        demand(p.is_file() and not p.is_symlink(),'nonregular audit path');actual.add(p.name)
    demand(actual==set(f)|{'MANIFEST.json'},'audit inventory mismatch')
    for name,entry in f.items():
        demand(isinstance(name,str) and re.fullmatch('[A-Za-z0-9_.-]+',name) is not None and name not in ('.','..','MANIFEST.json'),'unsafe inventory path')
        p=root/name;raw=p.read_bytes()
        demand(len(raw)==entry['bytes'] and hashlib.sha256(raw).hexdigest()==entry['sha256'],'audit file drift: '+name)
        demand(stat.S_IMODE(p.stat().st_mode)==int(entry['mode'],8),'audit mode drift: '+name)
        if p.suffix=='.py':demand(not any(isinstance(n,ast.Assert) for n in ast.walk(ast.parse(raw))),'assert prohibited')
    a=json.loads((root/'ACCEPTANCE.json').read_text(),object_pairs_hook=unique)
    demand(a['problem_id']==30003116 and a['rank']==993,'wrong target')
    demand(a['verdict']=='ACCEPT_RESTRICTED_PROGRESS' and a['asymptotic_disposition']=='unresolved_5_of_5','wrong verdict')
    demand(a['original_manifest_sha256']=='f0e11096444ac0a676a9e4a8cd267e51bb4600512574eebf961ce5789a03c115','wrong original pin')
    observed=runpy.run_path(str(root/'independent_math_controls.py'))['run']()
    recorded=json.loads((root/'independent_math_results.json').read_text(),object_pairs_hook=unique)
    demand(observed==recorded,'independent replay mismatch')
    return {'status':'PASS','audit_manifest_sha256':pin,'files':len(f),'independent_checks':observed['checks'],'verdict':a['verdict']}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--expected-manifest',required=True);args=p.parse_args()
    try:print(json.dumps(run(Path(__file__).resolve().parent,args.expected_manifest),sort_keys=True))
    except (AuditError,KeyError,TypeError,ValueError,OSError,SyntaxError) as exc:
        print('REJECTED: '+str(exc));raise SystemExit(2)
