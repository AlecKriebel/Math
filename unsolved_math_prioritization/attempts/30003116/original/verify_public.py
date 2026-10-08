"""Externally pinned integrity and exact-control replay; no assert-based checks."""
import argparse
import ast
import hashlib
import json
from pathlib import Path
import re
import runpy
import stat

class VerificationError(Exception):
    pass

def demand(condition,message):
    if not condition:raise VerificationError(message)

def unique_object(pairs):
    out={}
    for k,v in pairs:
        demand(k not in out,'duplicate JSON key: '+k);out[k]=v
    return out

def digest(b):return hashlib.sha256(b).hexdigest()

def verify(root,pin,integrity_only=False):
    demand(re.fullmatch('[0-9a-f]{64}',pin) is not None,'invalid external manifest pin')
    manifest=root/'MANIFEST.json'
    demand(manifest.is_file() and not manifest.is_symlink(),'manifest missing or symlink')
    raw=manifest.read_bytes();demand(digest(raw)==pin,'external manifest pin mismatch')
    m=json.loads(raw,object_pairs_hook=unique_object)
    demand(m.get('format')=='rational-orbit-entropy-v1','wrong manifest format')
    demand(m.get('exceptions')==['MANIFEST.json'],'wrong manifest exceptions')
    entries=m.get('files');demand(isinstance(entries,dict) and bool(entries),'empty or invalid inventory')
    for n in entries:
        demand(isinstance(n,str) and re.fullmatch('[A-Za-z0-9_.-]+',n) is not None and n not in ('.','..','MANIFEST.json'),'unsafe manifest path')
    actual=set()
    for p in root.iterdir():
        demand(not p.is_symlink(),'symlink forbidden: '+p.name)
        demand(p.is_file(),'extra directory or special path: '+p.name)
        actual.add(p.name)
    demand(actual==set(entries)|{'MANIFEST.json'},'exact inventory mismatch')
    for n,e in entries.items():
        p=root/n;b=p.read_bytes()
        demand(len(b)==e['bytes'],'byte count mismatch: '+n)
        demand(digest(b)==e['sha256'],'hash mismatch: '+n)
        demand(stat.S_IMODE(p.stat().st_mode)==int(e['mode'],8),'file mode mismatch: '+n)
        if n.endswith('.py'):
            tree=ast.parse(b,filename=n)
            demand(not any(isinstance(node,ast.Assert) for node in ast.walk(tree)),'assert statement forbidden: '+n)
    if integrity_only:
        return {'status':'PASS_INTEGRITY_ONLY','manifest_sha256':pin,'files':len(entries)}
    scope=json.loads((root/'source_scope.json').read_text(),object_pairs_hook=unique_object)
    demand(scope['problem_id']==30003116 and scope['rank']==993,'wrong target scope')
    demand(scope['disposition']=='asymptotic_unresolved_5_of_5','wrong disposition')
    module=runpy.run_path(str(root/'check_math.py'))
    observed=module['run']()
    expected=json.loads((root/'checks.json').read_text(),object_pairs_hook=unique_object)
    demand(observed==expected,'exact mathematical replay mismatch')
    return {'status':'PASS','manifest_sha256':pin,'files':len(entries),'checks':observed['checks']}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--expected-manifest',required=True);p.add_argument('--integrity-only',action='store_true');a=p.parse_args()
    try:print(json.dumps(verify(Path(__file__).resolve().parent,a.expected_manifest,a.integrity_only),sort_keys=True))
    except (VerificationError,KeyError,ValueError,TypeError,OSError) as exc:
        print('REJECTED: '+str(exc));raise SystemExit(2)
