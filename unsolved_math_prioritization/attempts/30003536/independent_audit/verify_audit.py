#!/usr/bin/env python3
"""Verify an externally pinned independent audit and replay its local controls."""
import argparse
import difflib
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import subprocess
import sys

AUTHOR_PIN='bd0c3dbdf92de2f92f3d31ed64033dfe16e188d1ea28ed66b069af2fad8919d6'
class Failure(Exception):pass

def need(ok,message):
    if not ok:raise Failure(message)

def digest(data):return hashlib.sha256(data).hexdigest()

def strict_json(raw):
    def pairs(items):
        result={}
        for key,value in items:
            need(key not in result,'duplicate JSON key');result[key]=value
        return result
    def nonfinite(value):raise Failure('nonfinite JSON number')
    return json.loads(raw,object_pairs_hook=pairs,parse_constant=nonfinite)

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--audit-root',type=Path,default=Path(__file__).resolve().parent)
    ap.add_argument('--packet',type=Path,required=True)
    ap.add_argument('--expected-audit-manifest-sha256',required=True)
    args=ap.parse_args();root=args.audit_root.resolve();packet=args.packet.resolve()
    pin=args.expected_audit_manifest_sha256
    need(re.fullmatch('[0-9a-f]{64}',pin) is not None,'invalid audit pin')
    manifest=root/'AUDIT_MANIFEST.json'
    need(manifest.is_file() and not manifest.is_symlink(),'manifest missing or symlink')
    raw=manifest.read_bytes();need(digest(raw)==pin,'audit manifest pin mismatch')
    data=strict_json(raw)
    need(type(data) is dict and set(data)=={'format','author_manifest_sha256','files'},'manifest shape')
    need(data['format']=='riesz-independent-audit-v1' and data['author_manifest_sha256']==AUTHOR_PIN,'manifest identity')
    need(type(data['files']) is list and data['files'],'file inventory')
    names=set()
    for row in data['files']:
        need(type(row) is dict and set(row)=={'path','bytes','sha256'},'inventory row')
        name=row['path'];need(type(name) is str and name and '\\' not in name,'path type')
        rel=PurePosixPath(name)
        need(not rel.is_absolute() and len(rel.parts)==1 and rel.parts[0] not in ('.','..'),'path safety')
        need(name not in names and name!='AUDIT_MANIFEST.json','duplicate or self path');names.add(name)
        need(type(row['bytes']) is int and row['bytes']>=0,'byte count type')
        need(type(row['sha256']) is str and re.fullmatch('[0-9a-f]{64}',row['sha256']) is not None,'digest format')
        path=root/name;need(path.is_file() and not path.is_symlink(),'missing or symlink payload')
        raw=path.read_bytes();need(len(raw)==row['bytes'] and digest(raw)==row['sha256'],'payload identity: '+name)
    need({p.name for p in root.iterdir()}==names|{'AUDIT_MANIFEST.json'},'complete audit inventory')
    need({'AUDIT_REPORT.md','ACCEPTANCE.json','REPORT.corrected.md','REGULARIZATION.patch',
          'INDEPENDENT_CONTROLS.json','independent_controls.py','verify_audit.py'}.issubset(names),'required audit payload')
    flags=['-I','-B']+(['-O'] if sys.flags.optimize==1 else ['-OO'] if sys.flags.optimize>=2 else [])
    proc=subprocess.run([sys.executable,*flags,str(packet/'verify_packet.py'),'--expected-manifest-sha256',AUTHOR_PIN],capture_output=True)
    need(proc.returncode==0 and not proc.stderr and strict_json(proc.stdout)['result']=='PASS','author packet replay')
    original=(packet/'REPORT.md').read_text();corrected=(root/'REPORT.corrected.md').read_text()
    patch=''.join(difflib.unified_diff(original.splitlines(keepends=True),corrected.splitlines(keepends=True),fromfile='a/REPORT.md',tofile='b/REPORT.md'))
    need(patch==(root/'REGULARIZATION.patch').read_text(),'patch does not reproduce corrected full report')
    acceptance=strict_json((root/'ACCEPTANCE.json').read_bytes())
    need(acceptance['author_manifest_sha256']==AUTHOR_PIN and acceptance['status']=='unsolved' and
         acceptance['author_turns']==5 and acceptance['original_inequality_proved'] is False and
         acceptance['original_inequality_disproved'] is False,'acceptance scope')
    proc=subprocess.run([sys.executable,*flags,str(root/'independent_controls.py'),'--packet',str(packet)],capture_output=True)
    need(proc.returncode==0 and not proc.stderr and proc.stdout==(root/'INDEPENDENT_CONTROLS.json').read_bytes(),
         'independent controls are not byte-identical')
    return {'result':'PASS','audit_manifest_sha256':pin,'author_manifest_sha256':AUTHOR_PIN,
            'audit_files_verified':len(names),'corrected_report_matches_patch':True,
            'independent_controls':'byte-identical','packet_writes':False}

if __name__=='__main__':
    try:print(json.dumps(main(),indent=2,sort_keys=True))
    except (Failure,OSError,ValueError,TypeError,KeyError) as exc:
        print(json.dumps({'result':'FAIL','error':str(exc)},sort_keys=True));sys.exit(2)
