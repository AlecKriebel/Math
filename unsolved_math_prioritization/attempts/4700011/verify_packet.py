#!/usr/bin/env python3
"""Source-free integrity and isolated exact replay of this partial-results packet."""
from pathlib import Path
import argparse
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile

ROOT=Path(__file__).resolve().parent
AUDITS=('periodic_recurrence_independent_audit','odd_recurrence_audit','fifth_recurrence_audit')

def require(condition,message):
    if not condition:
        raise ValueError(message)

def pin(path):
    data=path.read_bytes()
    return {'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()}

def check_manifest(base,manifest):
    obj=json.loads((base/manifest).read_text())
    entries=obj['files'] if isinstance(obj,dict) else obj
    for row in entries:
        relative=Path(row['file'])
        require(not relative.is_absolute() and '..' not in relative.parts,'Unsafe manifest path')
        require(pin(base/relative)=={k:row[k] for k in ('bytes','sha256')},'Pin mismatch: '+str(base/relative))
    return entries

def verify_integrity():
    entries=check_manifest(ROOT,'PACKET_MANIFEST.json')
    paths={r['file'] for r in entries}
    require(len(paths)==len(entries),'Duplicate inventory entry')
    actual={str(p.relative_to(ROOT)) for p in ROOT.rglob('*') if p.is_file()}
    require(actual==paths|{'PACKET_MANIFEST.json'},'Unlisted or missing package files: '+str(sorted(actual^(paths|{'PACKET_MANIFEST.json'}))))
    for row in json.loads((ROOT/'INPUT_PINS.json').read_text())['manifests']:
        require(pin(ROOT/row['manifest'])=={k:row[k] for k in ('bytes','sha256')},'Input manifest pin mismatch')
        p=ROOT/row['manifest']
        require(len(check_manifest(p.parent,p.name))==row['listed_files'],'Input file-count mismatch')
    for turn in range(1,6):
        audit=AUDITS[0 if turn<=2 else 1 if turn<=4 else 2]
        for file in (ROOT/'authored').glob(f'*turn0{turn}*'):
            require(file.read_bytes()==(ROOT/audit/'frozen'/file.name).read_bytes(),'Author/frozen mismatch: '+file.name)
    return entries

def replay(entries):
    import sympy
    results=[]
    with tempfile.TemporaryDirectory(prefix='recurrence-4700011-') as temporary:
        work=Path(temporary)
        for row in entries:
            destination=work/row['file']
            destination.parent.mkdir(parents=True,exist_ok=True)
            shutil.copyfile(ROOT/row['file'],destination)
        jobs=[(f'authored/verify_turn0{i}.py',f'authored/turn0{i}_verification.json') for i in range(1,6)]
        jobs += [(a+'/checks/independent_checks.py',a+'/checks/independent_results.json') for a in AUDITS]
        for script,output in jobs:
            print('Replaying '+script,file=sys.stderr,flush=True)
            process=subprocess.run([sys.executable,str(work/script)],cwd=work,text=True,capture_output=True)
            require(process.returncode==0,'Replay failed: '+script+'\n'+process.stdout+'\n'+process.stderr)
            require((work/output).read_bytes()==(ROOT/output).read_bytes(),'Recorded result differs: '+output)
            value=json.loads((work/output).read_text())
            results.append({'script':script,'output':output,'exit_code':process.returncode,'byte_identical':True,**pin(work/output)})
        # No source fetches, manuscript proof checking, or all-order search occurs here.
    return {'all_passed':True,'python':sys.version.split()[0],'sympy':sympy.__version__,'scripts_executed':len(results),'results':results}

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--integrity-only',action='store_true')
    args=parser.parse_args()
    entries=verify_integrity()
    result={'integrity_passed':True,'inventoried_files':len(entries),'full_problem_solved':False,'novelty_established':False}
    if not args.integrity_only:
        result.update(replay(entries))
        verify_integrity()
    print(json.dumps(result,indent=2))

if __name__=='__main__':
    main()
