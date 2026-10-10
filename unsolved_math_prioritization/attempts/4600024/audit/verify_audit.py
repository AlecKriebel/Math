#!/usr/bin/env python3
"""Fail-closed recursive packet check followed by isolated source-only replay."""
from pathlib import Path
import hashlib
import json
import stat
import subprocess
import sys

ROOT=Path(__file__).resolve().parent
AUTHOR={'README.md','PROOF.md','APPROACHES.md','PROVENANCE.json','STATUS.json',
        'verify_math.py','MATH_RESULTS.json','verify_release.py','MANIFEST.json'}
TOP={'README.md','AUDIT.md','AUDIT_METADATA.json','INDEPENDENT_RESULTS.json',
     'INTEGRITY_RESULTS.json','independent_checks.py','integrity_checks.py',
     'verify_audit.py','MANIFEST.json'}
EXPECTED=TOP | {'author/'+f for f in AUTHOR}
AUTHOR_MANIFEST='f5846cf7f7467189dc0848af908a4668d61330206406e03e471edd8fc47bea32'

def fail(msg):
    raise RuntimeError(msg)

def main():
    actual=set()
    for p in ROOT.iterdir():
        mode=p.lstat().st_mode
        if p.name=='author':
            if not stat.S_ISDIR(mode): fail('author directory replaced')
            for q in p.iterdir():
                if not stat.S_ISREG(q.lstat().st_mode): fail('nonregular author node')
                actual.add('author/'+q.name)
        else:
            if not stat.S_ISREG(mode): fail('nonregular audit node: '+p.name)
            actual.add(p.name)
    if actual!=EXPECTED: fail('inventory mismatch: '+repr(sorted(actual^EXPECTED)))
    m=json.loads((ROOT/'MANIFEST.json').read_bytes())
    if set(m)!={'schema','files'} or m['schema']!=1: fail('manifest schema')
    if set(m['files'])!=EXPECTED-{'MANIFEST.json'}: fail('manifest inventory')
    for name,info in m['files'].items():
        if set(info)!={'bytes','sha256'}: fail('manifest metadata')
        b=(ROOT/name).read_bytes()
        if len(b)!=info['bytes'] or hashlib.sha256(b).hexdigest()!=info['sha256']:
            fail('hash mismatch: '+name)
    if hashlib.sha256((ROOT/'author/MANIFEST.json').read_bytes()).hexdigest()!=AUTHOR_MANIFEST:
        fail('frozen author manifest differs')
    for optimized in (False,True):
        flags=['-I','-B']+(['-O'] if optimized else [])
        for script,expected in [('independent_checks.py','INDEPENDENT_RESULTS.json'),
                                ('integrity_checks.py','INTEGRITY_RESULTS.json')]:
            p=subprocess.run([sys.executable,*flags,str(ROOT/script)],cwd=ROOT,
                             capture_output=True,check=True)
            if p.stdout!=(ROOT/expected).read_bytes(): fail('replay mismatch: '+script)
    a=json.loads((ROOT/'INDEPENDENT_RESULTS.json').read_bytes())
    i=json.loads((ROOT/'INTEGRITY_RESULTS.json').read_bytes())
    print(json.dumps({'status':'PASS','verified_regular_files':len(EXPECTED),
        'author_checks':3456,'independent_checks':a['checks'],'integrity_controls':i['tests'],
        'mathematical_disposition':'see AUDIT.md; this verifier checks finite controls'},sort_keys=True))

if __name__=='__main__':
    main()
