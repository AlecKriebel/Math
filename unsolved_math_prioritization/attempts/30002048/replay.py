#!/usr/bin/env python3
"""Reproduce the three mathematical certificates in this exact published layout."""
import hashlib,os,subprocess,sys
from pathlib import Path

root=Path(__file__).resolve().parent
subprocess.run([sys.executable,str(root/'verify_manifest.py')],check=True)
env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1')
for rel,cmd,expected in [
 ('release/author',['verify.py'],'results.json'),
 ('release/author',['crosscheck_sympy.py'],'CROSSCHECK.txt'),
 ('release/independent_review',['independent_verify.py','--author-json','../author/results.json'],'independent_results.json')]:
    cwd=root/rel
    p=subprocess.run([sys.executable,*cmd],cwd=cwd,env=env,capture_output=True,check=True)
    if p.stdout!=(cwd/expected).read_bytes():raise SystemExit('FAIL: replay mismatch '+expected)
    print('PASS:',rel+'/'+expected,hashlib.sha256(p.stdout).hexdigest())
subprocess.run([sys.executable,str(root/'verify_manifest.py')],check=True)
print('All three exact replays passed. The all-degree conjecture remains unsolved.')
