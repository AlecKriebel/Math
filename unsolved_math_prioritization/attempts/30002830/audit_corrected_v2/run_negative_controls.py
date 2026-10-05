#!/usr/bin/env python3
"""Executable mutation controls. Temporary copies only; frozen input untouched."""
import argparse
from concurrent.futures import ThreadPoolExecutor
import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile


def require(value,message):
    if not value:raise RuntimeError(message)


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--author-safe',required=True)
    parser.add_argument('--output')
    args=parser.parse_args()
    author=Path(args.author_safe).resolve()
    root=Path(__file__).resolve().parent
    independent=root/'independent_verifier.py'
    cases=[('net_inverse','net inverse recovers s'),('cubic_cover','cubic base change yields cube'),
           ('conic_sign','branch conic determinant'),('exceptional_branch','normalized branch class even'),
           ('newton_support','Newton width forcing pair 2')]

    def check_independent(case):
        mutation,label=case
        result=subprocess.run([sys.executable,'-O',str(independent),'--mutation',mutation],capture_output=True,text=True)
        require(result.returncode!=0 and 'CHECK FAILED: '+label in result.stderr,'independent mutation escaped: '+mutation)
        return dict(kind='independent_formula_mutation',name=mutation,mode='-O',rejected=True,check=label)

    original=(author/'verify_exact.py').read_text()
    changes=[('net_inverse_sign','sinv=(e-A*C)/(C*(C+1))','sinv=(e+A*C)/(C*(C+1))','inverse coefficients recover A'),
             ('cubic_exponent','s,u**3*(t-1)','s,u**2*(t-1)','cyclic base change makes pairing cube'),
             ('conic_determinant_sign','M.det()+4*U**2*s**4*(s-1)**4','M.det()-4*U**2*s**4*(s-1)**4','coefficient conic matrix determinant'),
             ('newton_support','expected_support={(2,1,3,0,0)','expected_support={(2,1,2,0,0)','Newton support exact')]

    with tempfile.TemporaryDirectory(prefix='ueno30002830-audit-') as temp:
        temp=Path(temp)
        jobs=[]
        for name,old,new,label in changes:
            require(original.count(old)==1,'author mutation pattern not unique: '+name)
            path=temp/(name+'.py');path.write_text(original.replace(old,new))
            jobs.append((name,path,label))

        def check_author(case):
            name,path,label=case
            result=subprocess.run([sys.executable,'-O',str(path)],capture_output=True,text=True)
            require(result.returncode!=0 and 'FAILED: '+label in result.stderr,'author mutation escaped: '+name)
            return dict(kind='author_formula_mutation',name=name,mode='-O',rejected=True,check=label)

        with ThreadPoolExecutor(max_workers=3) as pool:
            results=list(pool.map(check_independent,cases))+list(pool.map(check_author,jobs))
        spec=importlib.util.spec_from_file_location('audit_replay',root/'replay_audit.py')
        mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)

        # Do not silently create __pycache__ inside the safe tree.
        for name,change,pinned in [
            ('stale_payload',lambda p:(p/'README.md').write_text('corrupted'),True),
            ('extra_unlisted_file',lambda p:(p/'extra.txt').write_text('unlisted'),True),
            ('missing_file',lambda p:(p/'README.md').unlink(),True),
            ('payload_symlink',lambda p:((p/'README.md').unlink(),(p/'README.md').symlink_to(author/'README.md')),True),
            ('manifest_rebinding',lambda p:rebind_manifest(p),True)]:
            copy=temp/name;shutil.copytree(author,copy)
            change(copy)
            try:mod.verify_tree(copy,mod.AUTHOR_MANIFEST_SHA256 if pinned else None)
            except RuntimeError as exc:results.append(dict(kind='integrity_mutation',name=name,rejected=True,check=str(exc)))
            else:raise RuntimeError('integrity control escaped: '+name)
    output=dict(target_id='30002830',all_rejected=True,control_count=len(results),controls=results)
    data=json.dumps(output,indent=2)+'\n'
    if args.output:Path(args.output).write_text(data)
    else:print(data,end='')


def rebind_manifest(root):
    (root/'README.md').write_text('corrupted but locally rehashed')
    p=root/'MANIFEST.json';obj=json.loads(p.read_text())
    for item in obj['allowlisted_files']:
        if item['path']=='README.md':
            b=(root/item['path']).read_bytes();item.update(bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
    p.write_text(json.dumps(obj,indent=2)+'\n')
    (root/'MANIFEST.sha256').write_text(hashlib.sha256(p.read_bytes()).hexdigest()+'  MANIFEST.json\n')


if __name__=='__main__':
    sys.dont_write_bytecode=True
    main()
