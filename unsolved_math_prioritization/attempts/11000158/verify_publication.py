#!/usr/bin/env python3
"""Replay exact frozen public artifacts without changing historical scripts."""
from pathlib import Path
import contextlib
import hashlib
import io
import json
import runpy
import subprocess
import sys

ROOT = Path(__file__).resolve().parent

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    manifest=json.loads((ROOT/'PUBLICATION_MANIFEST.json').read_text())
    for name, expected in manifest['files'].items():
        assert sha(ROOT/name)==expected, name
    original=json.loads(subprocess.check_output([sys.executable,str(ROOT/'verify.py')]))
    assert original==json.loads((ROOT/'verification.json').read_text())
    module=runpy.run_path(str(ROOT/'independent_review'/'independent_controls.py'),run_name='frozen_independent_controls')
    module['main'].__globals__['PACKET']=ROOT
    output=io.StringIO()
    with contextlib.redirect_stdout(output):
        module['main']()
    independent=json.loads(output.getvalue())
    assert independent==json.loads((ROOT/'independent_review'/'independent_controls.json').read_text())
    for name,want in json.loads((ROOT/'CURRENT_MANIFEST.json').read_text())['frozen_files'].items():
        assert sha(ROOT/name)==want
    for name,want in json.loads((ROOT/'CURRENT_MANIFEST.json').read_text())['additive_files'].items():
        assert sha(ROOT/name)==want
    narrow=json.loads((ROOT/'independent_review'/'CLARIFICATION_PASS_9ac653e44e50.json').read_text())
    assert narrow['result']=='PASS' and not narrow['corrections_required']
    assert narrow['stronger_ambient_isotopy_target_resolved'] is False
    print(json.dumps({'status':'PASS','public_files_hash_verified':len(manifest['files']),
        'original_receipt_matched':True,'independent_receipt_matched':True,
        'original_ten_files_unchanged':True,'reviewed_additive_files_unchanged':True,
        'clarification_pass':True,'topology_certified_by_computation':False},indent=2,sort_keys=True))

if __name__=='__main__':
    main()
