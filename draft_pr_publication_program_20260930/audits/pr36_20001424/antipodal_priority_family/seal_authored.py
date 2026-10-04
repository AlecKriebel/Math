#!/usr/bin/env python3
"""Build/verify self-excluding authored audit manifest; foreign sources stay ignored."""
from pathlib import Path
import argparse,hashlib,json,datetime,subprocess
ROOT=Path(__file__).resolve().parent
MANIFEST='AUTHORED_MANIFEST.json'
def eligible():
    return sorted(p for p in ROOT.rglob('*') if p.is_file() and p.relative_to(ROOT).as_posix()!=MANIFEST and 'tmp' not in p.relative_to(ROOT).parts and '__pycache__' not in p.relative_to(ROOT).parts)
def verify(data):
    actual={p.relative_to(ROOT).as_posix():p for p in eligible()}
    listed=data['files'];bad=[]
    if set(actual)!=set(listed):bad.append({'inventory_difference':sorted(set(actual)^set(listed))})
    for name,p in actual.items():
        b=p.read_bytes();rec={'sha256':hashlib.sha256(b).hexdigest(),'bytes':len(b)}
        if listed.get(name)!=rec:bad.append({'changed':name})
    return {'status':'PASS' if not bad else 'FAIL','files_checked':len(actual),'errors':bad}
if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--verify',action='store_true');args=parser.parse_args()
    if args.verify:
        result=verify(json.loads((ROOT/MANIFEST).read_text()));print(json.dumps(result,indent=2))
        if result['status']!='PASS':raise SystemExit(1)
    else:
        sources=sorted(p for p in ROOT.rglob('*.pdf') if p.is_file())
        for p in sources:
            if 'tmp' not in p.relative_to(ROOT).parts:raise RuntimeError('Foreign PDF outside ignored tmp: '+str(p))
            r=subprocess.run(['git','check-ignore',str(p)],capture_output=True,text=True)
            if r.returncode:raise RuntimeError('Foreign PDF not ignored: '+str(p))
        files={}
        for p in eligible():
            b=p.read_bytes();files[p.relative_to(ROOT).as_posix()]={'sha256':hashlib.sha256(b).hexdigest(),'bytes':len(b)}
        data={'schema':'strict-self-excluding-authored-audit-v1','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'verdict':'PRIOR_APPLICATION','new_candidate_turns':0,'exclusions':[MANIFEST,'any tmp/ subtree','any __pycache__/ subtree'],'foreign_pdf_count_all_checked_ignored':len(sources),'files':files}
        result=verify(data)
        if result['status']!='PASS':raise RuntimeError(str(result))
        (ROOT/MANIFEST).write_text(json.dumps(data,indent=2,sort_keys=True)+'\n');print(json.dumps(result,indent=2))
