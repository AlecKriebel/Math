#!/usr/bin/env python3
"""Strict file inventory and exact replay verifier; standard library only."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--source-dir',type=Path)
    args=parser.parse_args()
    root=Path(__file__).resolve().parent
    manifest_path=root/'MANIFEST.json'
    require(not manifest_path.is_symlink(),'symlinked manifest')
    manifest=json.loads(manifest_path.read_text())
    require(set(manifest)=={'schema_version','problem_id','files'},'unexpected manifest fields')
    require(manifest['schema_version']==1 and manifest['problem_id']=='30003070','manifest identity')
    require(isinstance(manifest['files'],list),'invalid file list')
    names=[]
    for entry in manifest['files']:
        require(isinstance(entry,dict) and set(entry)=={'name','bytes','sha256'},'bad manifest entry')
        name=entry['name']
        require(isinstance(name,str) and re.fullmatch(r'[A-Za-z0-9_.-]+',name) is not None
                and name not in ('.','..','MANIFEST.json'),'unsafe manifest path')
        require(type(entry['bytes']) is int and entry['bytes']>=0,'invalid byte count')
        require(isinstance(entry['sha256'],str) and re.fullmatch('[0-9a-f]{64}',entry['sha256']) is not None,
                'invalid hash')
        names.append(name)
    require(len(names)==len(set(names)),'duplicate manifest path')
    children=list(root.iterdir())
    require(all(p.is_file() and not p.is_symlink() for p in children),'nonregular or symlinked member')
    require(set(p.name for p in children)==set(names)|{'MANIFEST.json'},'inventory mismatch')
    for entry in manifest['files']:
        b=(root/entry['name']).read_bytes()
        require(len(b)==entry['bytes'],'byte-count mismatch: '+entry['name'])
        require(hashlib.sha256(b).hexdigest()==entry['sha256'],'hash mismatch: '+entry['name'])
    status=json.loads((root/'STATUS.json').read_text())
    require(status['problem_id']=='30003070' and status['status']=='unsolved','status overclaim or mismatch')
    require(status['approaches_used']==status['approach_limit']==5,'wrong approach accounting')
    for flag in ('full_solution','full_counterexample','verified_full_prior_resolution','novelty_claim',
                 'global_current_openness_claim','remote_changes_performed'):
        require(status[flag] is False,'unsupported claim: '+flag)
    flags=['-B']+(['-O'] if sys.flags.optimize else [])
    result=subprocess.run([sys.executable,*flags,str(root/'verify_math.py')],capture_output=True,check=False)
    require(result.returncode==0,'math replay failed: '+result.stderr.decode(errors='replace'))
    require(result.stdout==(root/'expected_math.json').read_bytes(),'math output differs from frozen bytes')
    source_count=0
    if args.source_dir is not None:
        meta=json.loads((root/'SOURCE_VERIFICATION.json').read_text())
        for s in meta['sources']:
            name=s['filename_for_optional_private_verification']
            require(Path(name).name==name,'unsafe source filename')
            b=(args.source_dir/name).read_bytes()
            require(len(b)==s['bytes'] and hashlib.sha256(b).hexdigest()==s['sha256'],'source mismatch: '+name)
            source_count+=1
    print(json.dumps({'status':'PASS','manifest_members':len(names),'math_checks':json.loads(result.stdout)['checks'],
                      'source_pdfs_verified':source_count,'mathematical_disposition':'unsolved, 5/5',
                      'independent_audit':'not performed by this author verifier'},sort_keys=True))

if __name__=='__main__':
    try:
        main()
    except Exception as exc:
        print('FAIL: '+str(exc),file=sys.stderr)
        raise SystemExit(1)
