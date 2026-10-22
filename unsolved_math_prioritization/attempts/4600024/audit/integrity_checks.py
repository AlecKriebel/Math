#!/usr/bin/env python3
"""Auditor-created tamper and relocation checks; never changes frozen inputs."""
from pathlib import Path
import json
import os
import shutil
import subprocess
import sys
import tempfile

ROOT=Path(__file__).resolve().parent

def main():
    results=[]
    with tempfile.TemporaryDirectory(prefix='block-code-audit-') as tmp:
        base=Path(tmp)
        # Relocated paths contain spaces. Neither invocation depends on cwd.
        clean=base/'relocated author with spaces'
        shutil.copytree(ROOT/'author',clean)
        for optimized in (False,True):
            flags=['-I','-B']+(['-O'] if optimized else [])
            p=subprocess.run([sys.executable,*flags,str(clean/'verify_release.py')],cwd=base,capture_output=True)
            if p.returncode or json.loads(p.stdout)['mathematical_checks']!=3456:
                raise RuntimeError('clean relocated author failed')
            results.append({'case':'clean_relocated_author','optimized':optimized,'passed':True})
            p=subprocess.run([sys.executable,*flags,str(clean/'verify_math.py')],cwd=base,capture_output=True)
            if p.returncode or p.stdout!=(clean/'MATH_RESULTS.json').read_bytes():
                raise RuntimeError('direct source replay failed')
            results.append({'case':'direct_author_math','optimized':optimized,'passed':True})
            p=subprocess.run([sys.executable,*flags,str(ROOT/'independent_checks.py')],cwd=base,capture_output=True)
            if p.returncode or p.stdout!=(ROOT/'INDEPENDENT_RESULTS.json').read_bytes():
                raise RuntimeError('independent source replay failed')
            results.append({'case':'independent_math','optimized':optimized,'passed':True})
        cases=['changed_proof','changed_results','changed_math','missing_readme','extra_file',
               'extra_directory','empty_pycache','populated_pycache','raw_pyc','symlink','fifo',
               'manifest_schema','manifest_inventory']
        for case in cases:
            for optimized in (False,True):
                where=base/(case+('-O' if optimized else ''))
                shutil.copytree(clean,where)
                if case=='changed_proof':
                    with (where/'PROOF.md').open('ab') as f: f.write(b'\nMutation.\n')
                elif case=='changed_results':
                    (where/'MATH_RESULTS.json').write_text('{}\n')
                elif case=='changed_math':
                    (where/'verify_math.py').write_text('print("MUTATED_SOURCE_EXECUTED")\n')
                elif case=='missing_readme': (where/'README.md').unlink()
                elif case=='extra_file': (where/'extra.txt').write_text('extra')
                elif case=='extra_directory': (where/'extra').mkdir()
                elif case=='empty_pycache': (where/'__pycache__').mkdir()
                elif case=='populated_pycache':
                    (where/'__pycache__').mkdir()
                    (where/'__pycache__'/'verify_math.cpython-311.pyc').write_bytes(b'not trusted bytecode')
                elif case=='raw_pyc': (where/'verify_math.pyc').write_bytes(b'not trusted bytecode')
                elif case=='symlink': (where/'link').symlink_to(where/'PROOF.md')
                elif case=='fifo': os.mkfifo(where/'pipe')
                else:
                    p=where/'MANIFEST.json'; m=json.loads(p.read_text())
                    if case=='manifest_schema': m['schema']=0
                    else: del m['files']['PROOF.md']
                    p.write_text(json.dumps(m))
                flags=['-I','-B']+(['-O'] if optimized else [])
                p=subprocess.run([sys.executable,*flags,str(where/'verify_release.py')],cwd=base,capture_output=True)
                if not p.returncode or b'MUTATED_SOURCE_EXECUTED' in p.stdout:
                    raise RuntimeError('mutation was not rejected before execution: '+case)
                results.append({'case':case,'optimized':optimized,'rejected':True})
    print(json.dumps({'status':'PASS','tests':len(results),'results':results,
        'scope':'Fail-closed inventory and source replay; external hash pins remain required.'},sort_keys=True,indent=2))

if __name__=='__main__':
    main()
