#!/usr/bin/env python3
"""Relocation, optimized-mode and adversarial corruption controls. No external dependencies."""
from pathlib import Path
import copy
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile

ROOT=Path(__file__).resolve().parent

def run(root, optimized=False):
    args=[sys.executable]+(['-O'] if optimized else [])+[str(root/'verify.py')]
    return subprocess.run(args,cwd=root.parent,text=True,capture_output=True)

def manifest(root):
    files={str(p.relative_to(root)):{'bytes':len(p.read_bytes()),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
           for p in sorted(root.rglob('*')) if p.is_file() and p.name!='MANIFEST.json'}
    (root/'MANIFEST.json').write_text(json.dumps({'files':files},sort_keys=True,indent=2)+'\n')

def main():
    base=run(ROOT)
    if base.returncode:raise RuntimeError(base.stderr)
    fast=run(ROOT,True)
    if fast.returncode or fast.stdout!=base.stdout:raise RuntimeError('Optimized replay differs')
    integrity_cases=['proof edit','verifier edit','certificate edit','missing manifest','missing proof',
                     'extra file','nested extra','empty directory','symlink','manifest byte count']
    semantic_cases=['first coordinate','second solution','midpoint area','Jacobian sign',
                    'harmonic coordinate','weighted polynomial','weighted area','scope claim']
    rejected_integrity=0;rejected_semantic=0
    with tempfile.TemporaryDirectory(prefix='equal_area_checks_') as tmp:
        tmp=Path(tmp)
        relocated=tmp/'relocated';shutil.copytree(ROOT,relocated)
        for opt in (False,True):
            p=run(relocated,opt)
            if p.returncode or p.stdout!=base.stdout:raise RuntimeError('Relocated replay differs')
        for name in integrity_cases:
            folder=tmp/('case'+str(rejected_integrity));shutil.copytree(ROOT,folder)
            if name in ('proof edit','verifier edit','certificate edit'):
                f={'proof edit':'PROOFS.md','verifier edit':'verify.py','certificate edit':'CERTIFICATES.json'}[name]
                with (folder/f).open('a') as out:out.write('\n')
            elif name=='missing manifest':(folder/'MANIFEST.json').unlink()
            elif name=='missing proof':(folder/'PROOFS.md').unlink()
            elif name=='extra file':(folder/'extra.txt').write_text('unlisted')
            elif name=='nested extra':
                (folder/'nested').mkdir();(folder/'nested'/'extra.txt').write_text('unlisted')
            elif name=='empty directory':(folder/'empty').mkdir()
            elif name=='symlink':(folder/'link').symlink_to('PROOFS.md')
            else:
                p=folder/'MANIFEST.json';d=json.loads(p.read_text());d['files']['PROOFS.md']['bytes']+=1;p.write_text(json.dumps(d))
            for opt in (False,True):
                p=run(folder,opt)
                if not p.returncode:raise RuntimeError('Integrity mutation accepted: '+name)
                rejected_integrity+=1
        for name in semantic_cases:
            folder=tmp/('semantic'+str(rejected_semantic));shutil.copytree(ROOT,folder)
            p=folder/'CERTIFICATES.json';d=json.loads(p.read_text())
            key={'first coordinate':'octahedron_plus','second solution':'octahedron_minus',
                 'midpoint area':'midpoint_areas','Jacobian sign':'endpoint_jacobian_determinants',
                 'harmonic coordinate':'harmonic_coordinates','weighted polynomial':'weighted_obstruction_polynomial',
                 'weighted area':'weighted_area_assignment'}.get(name)
            if name=='scope claim':d['status']='claimed_solved'
            elif name=='weighted polynomial':d[key][0]+=1
            else:d[key][0]='0'
            p.write_text(json.dumps(d,sort_keys=True,indent=2)+'\n')
            manifest(folder)  # Bypass only integrity to exercise actual semantic checks.
            for opt in (False,True):
                result=run(folder,opt)
                if not result.returncode:raise RuntimeError('Semantic mutation accepted: '+name)
                rejected_semantic+=1
    print(json.dumps({'status':'PASS','baseline':json.loads(base.stdout),
                      'normal_optimized_byte_identical':True,'relocated_normal_optimized_byte_identical':True,
                      'integrity_mutation_runs_rejected':rejected_integrity,
                      'semantic_mutation_runs_rejected':rejected_semantic,
                      'integrity_mutations':integrity_cases,'semantic_mutations':semantic_cases},sort_keys=True,indent=2))

if __name__=='__main__':main()
