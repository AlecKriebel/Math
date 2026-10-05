#!/usr/bin/env python3
"""Corrupt fresh copies; every corruption must be rejected. No original writes."""
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile


def reseal(root,name):
    p=root/'MANIFEST.json';m=json.loads(p.read_text());b=(root/name).read_bytes()
    for entry in m['files']:
        if entry['name']==name:
            entry['bytes']=len(b);entry['sha256']=hashlib.sha256(b).hexdigest()
    p.write_text(json.dumps(m,indent=2)+'\n')


def mutate(root,case):
    if case=='changed-proof':
        p=root/'MATHEMATICS.md';p.write_bytes(p.read_bytes()+b'Changed.\n')
    elif case=='missing-proof':
        (root/'MATHEMATICS.md').unlink()
    elif case=='unexpected-file':
        (root/'unexpected.txt').write_text('unexpected')
    elif case=='unexpected-directory':
        (root/'unexpected').mkdir()
    elif case=='symlink-member':
        p=root/'MATHEMATICS.md';p.unlink();p.symlink_to('README.md')
    elif case=='wrong-expected-output':
        p=root/'expected_math.json';p.write_bytes(p.read_bytes()+b' ');reseal(root,p.name)
    elif case=='claimed-solved-status':
        p=root/'STATUS.json';s=json.loads(p.read_text());s['status']='solved';p.write_text(json.dumps(s));reseal(root,p.name)
    elif case=='full-solution-flag':
        p=root/'STATUS.json';s=json.loads(p.read_text());s['full_solution']=True;p.write_text(json.dumps(s));reseal(root,p.name)
    elif case=='wrong-approach-count':
        p=root/'STATUS.json';s=json.loads(p.read_text());s['approaches_used']=1;p.write_text(json.dumps(s));reseal(root,p.name)
    else:
        p=root/'MANIFEST.json';m=json.loads(p.read_text())
        if case=='duplicate-manifest-entry':m['files'].append(dict(m['files'][0]))
        elif case=='omitted-manifest-entry':m['files'].pop()
        elif case=='unsafe-manifest-path':m['files'][0]['name']='../escape'
        elif case=='wrong-manifest-target':m['problem_id']='30003071'
        else:raise RuntimeError('unknown control')
        p.write_text(json.dumps(m,indent=2)+'\n')


def main():
    root=Path(__file__).resolve().parent
    cases=['changed-proof','missing-proof','unexpected-file','unexpected-directory','symlink-member',
           'wrong-expected-output','claimed-solved-status','full-solution-flag','wrong-approach-count',
           'duplicate-manifest-entry','omitted-manifest-entry','unsafe-manifest-path','wrong-manifest-target']
    flags=['-B']+(['-O'] if sys.flags.optimize else [])
    rejected=[]
    with tempfile.TemporaryDirectory(prefix='plabic-negative-') as tmp:
        for index,case in enumerate(cases):
            copy=Path(tmp)/str(index);shutil.copytree(root,copy);mutate(copy,case)
            result=subprocess.run([sys.executable,*flags,str(copy/'verify_release.py')],cwd=tmp,
                                  capture_output=True,check=False)
            if result.returncode==0:
                raise RuntimeError('accepted negative control: '+case)
            rejected.append(case)
    print(json.dumps({'status':'PASS','negative_controls_rejected':len(rejected),'cases':rejected},sort_keys=True))

if __name__=='__main__':
    main()
