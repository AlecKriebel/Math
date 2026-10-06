#!/usr/bin/env python3
"""Adversarial payload checks in both ordinary and optimized Python."""
import sys
sys.dont_write_bytecode = True
import hashlib
import json
import shutil
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def require(ok, why):
    if not ok:
        raise RuntimeError(why)


def reseal(root):
    entries = {}
    for path in sorted(root.iterdir()):
        if path.name != 'MANIFEST.json' and path.is_file():
            raw = path.read_bytes()
            entries[path.name] = {'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}
    (root/'MANIFEST.json').write_text(json.dumps({'schema':'sha256-byte-inventory-v1','files':entries},sort_keys=True,indent=2)+'\n')


def change_json(root, filename, fn):
    path = root/filename
    data = json.loads(path.read_text())
    fn(data)
    path.write_text(json.dumps(data,sort_keys=True,indent=2)+'\n')
    reseal(root)


def mutate(root, kind):
    if kind == 'alter_proof_without_reseal':
        with (root/'PROOF.md').open('a') as f:
            f.write('\nTampered.\n')
    elif kind == 'missing_proof':
        (root/'PROOF.md').unlink()
    elif kind == 'extra_pdf':
        (root/'third_party.pdf').write_bytes(b'%PDF-1.4\n')
        reseal(root)
    elif kind == 'symlink_proof':
        (root/'PROOF.md').unlink()
        (root/'PROOF.md').symlink_to('README.md')
    elif kind == 'wrong_quantum_resealed':
        change_json(root,'claims.json',lambda d:d.update(energy_quantum_pi_squared_coefficient=32))
    elif kind == 'false_solution_resealed':
        change_json(root,'claims.json',lambda d:d.update(full_resolution=True))
    elif kind == 'wrong_boundary_resealed':
        change_json(root,'claims.json',lambda d:d.update(boundary=['u=0','normal_derivative_u=0']))
    elif kind == 'missing_positivity_resealed':
        def f(d): d['criterion_hypotheses'].remove('all_height_ratios_positive_and_finite')
        change_json(root,'claims.json',f)
    elif kind == 'energy_tightness_overclaim_resealed':
        change_json(root,'claims.json',lambda d:d.update(ordinary_energy_tightness_suffices=True))
    elif kind == 'wrong_review_hash_resealed':
        def f(d):d['review']['review_sha256']='0'*64
        change_json(root,'PUBLIC_METADATA.json',f)
    elif kind == 'null_absent_report_resealed':
        def f(d):d['review']['missing_report_representation']='null'
        change_json(root,'PUBLIC_METADATA.json',f)
    elif kind == 'wrong_dimension_resealed':
        change_json(root,'claims.json',lambda d:d.update(dimension=2))
    else:
        raise RuntimeError('unknown mutation')


def run(path, optimized):
    cmd=[sys.executable]+(['-O'] if optimized else [])+[str(path/'verify.py')]
    return subprocess.run(cmd,cwd=path.parent,text=True,capture_output=True,timeout=90)


def main():
    cases=['alter_proof_without_reseal','missing_proof','extra_pdf','symlink_proof',
           'wrong_quantum_resealed','false_solution_resealed','wrong_boundary_resealed',
           'missing_positivity_resealed','energy_tightness_overclaim_resealed',
           'wrong_review_hash_resealed','null_absent_report_resealed','wrong_dimension_resealed']
    results=[]
    with tempfile.TemporaryDirectory(prefix='navier_audit_') as tmp:
        tmp=Path(tmp)
        for opt in (False,True):
            baseline=run(ROOT,opt)
            require(baseline.returncode==0,'baseline failed: '+baseline.stderr)
            relocated=tmp/('relocated_optimized' if opt else 'relocated_normal')
            shutil.copytree(ROOT,relocated)
            result=run(relocated,opt)
            require(result.returncode==0,'relocated failed: '+result.stderr)
            results.append({'mode':'optimized' if opt else 'normal','baseline':'PASS','relocated':'PASS'})
            for i,case in enumerate(cases):
                dst=tmp/(('opt' if opt else 'normal')+'_'+str(i))
                shutil.copytree(ROOT,dst)
                mutate(dst,case)
                got=run(dst,opt)
                require(got.returncode!=0,'mutation unexpectedly accepted: '+case)
                require('"status": "FAIL"' in got.stderr,'mutation lacked explicit failure: '+case)
                results.append({'mode':'optimized' if opt else 'normal','mutation':case,'status':'REJECTED'})
    print(json.dumps({'status':'PASS','mutation_rejections':2*len(cases),'runs':results,'full_target_proved':False},indent=2))

if __name__=='__main__':
    try:
        main()
    except Exception as exc:
        print(json.dumps({'status':'FAIL','error':str(exc)}),file=sys.stderr)
        sys.exit(1)
