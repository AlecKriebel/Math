#!/usr/bin/env python3
"""Replay and deliberately mutate copies; never changes the source freeze."""
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

ROOT=Path(__file__).resolve().parent

def require(ok,message):
    if not ok:
        raise RuntimeError(message)

def call(root, anchor, optimized=False, cwd=None):
    cmd=[sys.executable]+(['-O'] if optimized else [])+['-B',str(root/'verify_package.py'),'--expected-manifest',anchor]
    return subprocess.run(cmd,cwd=cwd,capture_output=True)

def main():
    anchor=hashlib.sha256((ROOT/'MANIFEST.json').read_bytes()).hexdigest()
    positives=[]; rejected=[]; mathematical=[]
    with tempfile.TemporaryDirectory(prefix='ricci-pde-audit-') as tmp:
        tmp=Path(tmp);rel=tmp/'relocated';shutil.copytree(ROOT,rel)
        for label,root,opt,cwd in [('normal',ROOT,False,ROOT),('optimized',ROOT,True,ROOT),('relocated',rel,False,tmp),('relocated_optimized',rel,True,tmp)]:
            result=call(root,anchor,opt,cwd)
            require(result.returncode==0,label+': '+result.stderr.decode())
            positives.append(label)
        mutations=['edit_proof','edit_result','missing_member','extra_member','symlink_member','wrong_manifest_anchor']
        for opt in [False,True]:
            for kind in mutations:
                dst=tmp/('mut-'+kind+str(opt));shutil.copytree(ROOT,dst)
                target=dst/'README.md'
                if kind=='edit_proof': target.write_text(target.read_text()+'\nchanged\n')
                if kind=='edit_result': (dst/'results.json').write_text('{}\n')
                if kind=='missing_member': target.unlink()
                if kind=='extra_member': (dst/'EXTRA.txt').write_text('unexpected')
                if kind=='symlink_member': target.unlink();target.symlink_to(ROOT/'README.md')
                badanchor='0'*64 if kind=='wrong_manifest_anchor' else anchor
                result=call(dst,badanchor,opt,tmp)
                require(result.returncode!=0,'mutation accepted: '+kind)
                rejected.append(kind+('_optimized' if opt else '_normal'))
        source=(ROOT/'math_check.py').read_text()
        for label,old,new in [('conversion_factor','c_of_d = 2 * n * (n - 1) / d**2','c_of_d = n * (n - 1) / d**2'),('conformal_coefficient','k = 2/(n-2)','k = 3/(n-2)'),('radial_sign','z=-M*J/w','z=M*J/w')]:
            require(source.count(old)==1,'mutation target mismatch')
            dst=tmp/(label+'.py');dst.write_text(source.replace(old,new))
            for opt in [False,True]:
                result=subprocess.run([sys.executable]+(['-O'] if opt else [])+['-B',str(dst)],capture_output=True,cwd=tmp)
                require(result.returncode!=0,'mathematical mutation accepted')
                mathematical.append(label+('_optimized' if opt else '_normal'))
    print(json.dumps({'status':'PASS','positive_replays':positives,'package_mutation_rejections':rejected,'mathematical_code_mutation_rejections':mathematical,'scope':'Fail-closed replay and selected mutations; verifier/interpreter trust and geometric proof audit remain separate.'},sort_keys=True,indent=2))

if __name__=='__main__':
    main()
