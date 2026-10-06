#!/usr/bin/env python3
"""Replay independent and frozen author controls, and reproduce two hardening gaps.
Temporary mutations are never written to the frozen author subtree.
"""
import difflib
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

ROOT=Path(__file__).resolve().parent

def rewrite_manifest(root):
    files={str(p.relative_to(root)):{'bytes':len(p.read_bytes()),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
      for p in sorted(root.rglob('*')) if p.is_file() and not p.is_symlink() and p!=root/'MANIFEST.json'}
    (root/'MANIFEST.json').write_text(json.dumps({'files':files},sort_keys=True,indent=2)+'\n')

def run(root,script='independent_verify.py',optimized=False,quick=False):
    return subprocess.run([sys.executable]+(['-O'] if optimized else [])+[str(root/script)]+(['--quick'] if quick else []),
      cwd=root.parent,text=True,capture_output=True,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'})

def must(ok,msg):
    if not ok:raise RuntimeError(msg)

def harden(source):
    old="        if p.is_dir() and str(p.relative_to(ROOT)) not in expected_dirs:"
    new="        if not p.is_file() and not p.is_dir():\n            raise ValueError('Nonregular member rejected: ' + str(p.relative_to(ROOT)))\n"+old
    must(source.count(old)==1,'Integrity hardening anchor')
    source=source.replace(old,new)
    old="def geometry(points,faces,expected=None):\n"
    new=old+"    need(points.get('A')==(0,1) and points.get('V0')==(0,0) and points.get('V1')==(1,0),\n         'Fixed exterior coordinates changed')\n"
    must(source.count(old)==1,'Geometry hardening anchor')
    return source.replace(old,new)

def main():
    full=run(ROOT);must(full.returncode==0,full.stderr)
    opt=run(ROOT,optimized=True);must(opt.returncode==0 and opt.stdout==full.stdout,'Independent optimized mismatch')
    author=run(ROOT/'author',script='run_checks.py');must(author.returncode==0,author.stderr)
    source=(ROOT/'author'/'verify.py').read_text()
    patch=''.join(difflib.unified_diff(source.splitlines(True),harden(source).splitlines(True),fromfile='a/verify.py',tofile='b/verify.py'))
    must(patch==(ROOT/'AUTHOR_HARDENING.patch').read_text(),'Patch differs from tested hardening')
    integrity_cases=['missing root manifest','proof append','nested extra','empty directory','symlink','FIFO','byte count','missing author certificate']
    semantics=[
      ('apex numerator','F(2*s,t)','F(3*s,t)'),
      ('translated outer coordinates','    return p\n','    return {v:(x+F(1,1000),y-F(1,500)) for v,(x,y) in p.items()}\n'),
      ('universal target area','want=r*r*s*s*t','want=r*r*s*s*(t+1)'),
      ('octahedron solution','for x in (2,1,4,2,1,4)','for x in (3,1,4,2,1,4)'),
      ('positive square','q==2*(11*b-5)**2+1','q==2*(11*b-5)**2+2'),
      ('harmonic target','for x in (5,3,1,3,5,3,5)','for x in (5,3,2,3,5,3,5)'),
      ('reflection labels','{i:(1-i)%m for i in range(m)}','{i:(-i)%m for i in range(m)}'),
      ('candidate count','len(seen)==m-2','len(seen)==m-1')]
    reject_i=reject_s=0;gap_tests=[]
    with tempfile.TemporaryDirectory(prefix='equal_area_independent_') as td:
        td=Path(td);reloc=td/'relocated';shutil.copytree(ROOT,reloc)
        for opt in (False,True):
            result=run(reloc,optimized=opt)
            must(result.returncode==0 and result.stdout==full.stdout,'Independent relocation mismatch')
        for k,name in enumerate(integrity_cases):
            d=td/('integrity_'+str(k));shutil.copytree(ROOT,d)
            if name=='missing root manifest':(d/'MANIFEST.json').unlink()
            elif name=='proof append':
                with (d/'author'/'PROOFS.md').open('a') as f:f.write('\n')
            elif name=='nested extra':(d/'unexpected').mkdir();(d/'unexpected'/'extra.txt').write_text('extra')
            elif name=='empty directory':(d/'empty').mkdir()
            elif name=='symlink':(d/'link').symlink_to('independent_verify.py')
            elif name=='FIFO':os.mkfifo(d/'fifo')
            elif name=='byte count':
                p=d/'MANIFEST.json';j=json.loads(p.read_text());j['files']['author/PROOFS.md']['bytes']+=1;p.write_text(json.dumps(j))
            elif name=='missing author certificate':(d/'author'/'CERTIFICATES.json').unlink()
            for opt in (False,True):
                p=run(d,optimized=opt,quick=True);must(p.returncode!=0,'Integrity accepted: '+name);reject_i+=1
        for k,(name,old,new) in enumerate(semantics):
            d=td/('semantic_'+str(k));shutil.copytree(ROOT,d)
            p=d/'independent_verify.py';code=p.read_text();must(code.count(old)==1,'Semantic anchor: '+name)
            p.write_text(code.replace(old,new));rewrite_manifest(d)
            for opt in (False,True):
                p=run(d,optimized=opt,quick=True);must(p.returncode!=0,'Semantic accepted: '+name);reject_s+=1
        # Prove the two old blind spots; then verify the separate patch rejects them.
        for hard in (False,True):
            base=td/('hardened_author' if hard else 'frozen_author');shutil.copytree(ROOT/'author',base)
            if hard:(base/'verify.py').write_text(harden(source));rewrite_manifest(base)
            for opt in (False,True):
                result=run(base,script='verify.py',optimized=opt)
                must(result.returncode==0,'Author/hardened baseline failed')
            if hard:hardened_baseline=json.loads(result.stdout)
            for name in ('translated_family','unlisted_FIFO'):
                d=td/(('hard_' if hard else 'original_')+name);shutil.copytree(base,d)
                if name=='translated_family':
                    p=d/'verify.py';code=p.read_text();old='    return points,faces'
                    must(code.count(old)==1,'Translation anchor')
                    p.write_text(code.replace(old,'    points={v:(x+Q(1,1000),y-Q(1,500)) for v,(x,y) in points.items()}\n'+old));rewrite_manifest(d)
                else:os.mkfifo(d/'unlisted_FIFO')
                for opt in (False,True):
                    result=run(d,script='verify.py',optimized=opt)
                    must((result.returncode!=0)==hard,'Hardening expectation: '+name)
                    gap_tests.append({'case':name,'hardening_applied':hard,'optimized':opt,'accepted':result.returncode==0})
        p=run(td/'hardened_author',script='run_checks.py')
        must(p.returncode==0,'Hardened author original regression harness failed')
        hardened_harness=json.loads(p.stdout)
    print(json.dumps({'status':'PASS','independent_baseline':json.loads(full.stdout),
      'independent_normal_optimized_relocated_identical':True,'independent_integrity_mutation_runs_rejected':reject_i,
      'independent_semantic_mutation_runs_rejected':reject_s,'independent_integrity_cases':integrity_cases,
      'independent_semantic_cases':[x[0] for x in semantics],
      'frozen_author_harness':json.loads(author.stdout),'separate_hardened_author_baseline':hardened_baseline,
      'separate_hardened_author_original_harness':hardened_harness,'reproduced_original_gaps_and_hardened_rejections':gap_tests},sort_keys=True,indent=2))

if __name__=='__main__':main()
