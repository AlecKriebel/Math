#!/usr/bin/env python3
"""Verify authored review bytes, frozen input binding, and symbolic replay.

Run with Python's -B option. Private third-party source files are excluded.
"""
from pathlib import Path
import hashlib,json,subprocess,sys

root=Path(__file__).resolve().parent
manifest=json.loads((root/'REVIEW_MANIFEST.json').read_text())
expected={r['path']:r for r in manifest['files']}
actual={p.name for p in root.iterdir() if p.is_file()}
assert actual==set(expected)|{'REVIEW_MANIFEST.json'},'Authored review inventory differs'
for name,row in expected.items():
    p=root/name;assert not p.is_symlink(),name
    data=p.read_bytes()
    assert len(data)==row['bytes'] and hashlib.sha256(data).hexdigest()==row['sha256'],name
freeze=json.loads((root/'FROZEN_INPUTS.json').read_text());base=Path(freeze['root'])
for row in freeze['files']:
    p=base/row['path'];assert not p.is_symlink(),row['path']
    data=p.read_bytes()
    assert len(data)==row['bytes'] and hashlib.sha256(data).hexdigest()==row['sha256'],row['path']
run=subprocess.run([sys.executable,'-B',str(root/'check_geometry.py')],capture_output=True,text=True,check=True)
assert json.loads(run.stdout)==json.loads((root/'geometry_symbolic_RESULTS.json').read_text()),'Symbolic replay differs'
print(json.dumps({'result':'PASS','authored_review_files':len(expected),'frozen_files':len(freeze['files']),'symbolic_identity_replay':'PASS','private_sources_excluded':True},sort_keys=True))
