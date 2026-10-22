#!/usr/bin/env python3
"""Relocation and integrity/semantic tamper tests, normal and optimized Python."""
from hashlib import sha256
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

ROOT=Path(__file__).resolve().parent

def reseal(path):
    manifest=json.loads((path/'MANIFEST.json').read_text())
    for row in manifest['files']:
        raw=(path/row['name']).read_bytes()
        row.update(bytes=len(raw),sha256=sha256(raw).hexdigest())
    (path/'MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n')

def change_certificate(path,mode):
    p=path/'certificate.json'; obj=json.loads(p.read_text())
    if mode=='false_interior_resealed':
        obj['monochromatic_triangles'][0]['inside']=[1]
    elif mode=='duplicate_geometry_resealed':
        obj['points'][0]=obj['points'][1]
    p.write_text(json.dumps(obj,indent=2)+'\n');reseal(path)

def main():
    results=[]
    modes=['relocation','altered_member','missing_member','unexpected_member','false_interior_resealed','duplicate_geometry_resealed']
    with tempfile.TemporaryDirectory(prefix='triangles-3081-') as td:
        base=Path(td)
        for optimized in (False,True):
            for mode in modes:
                target=base/(mode+('-optimized' if optimized else '-normal'))
                shutil.copytree(ROOT,target)
                if mode=='altered_member':
                    with (target/'REPORT.md').open('a') as f:f.write('\nTampered.\n')
                elif mode=='missing_member':
                    (target/'REPORT.md').unlink()
                elif mode=='unexpected_member':
                    (target/'UNEXPECTED').write_text('extra')
                elif mode.endswith('_resealed'):
                    change_certificate(target,mode)
                cmd=[sys.executable,'-B']+(['-O'] if optimized else [])+[str(target/'checker.py')]
                run=subprocess.run(cmd,cwd=base,capture_output=True,text=True,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'})
                wanted=(mode=='relocation')
                if (run.returncode==0)!=wanted:
                    raise RuntimeError('Unexpected result '+mode+': '+run.stdout+run.stderr)
                results.append({'mode':mode,'optimized':optimized,'returncode':run.returncode,'expected_pass':wanted,'diagnostic':run.stderr.strip() if not wanted else 'PASS'})
    print(json.dumps({'status':'PASS','cases':results},indent=2))

if __name__=='__main__':
    main()
