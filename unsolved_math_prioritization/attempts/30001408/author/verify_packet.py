#!/usr/bin/env python3
"""Verify the frozen authored packet and replay finite controls without sources."""
import hashlib,json,pathlib,subprocess,sys
root=pathlib.Path(__file__).resolve().parent
manifest=json.loads((root/'AUTHOR_MANIFEST.json').read_text())
assert manifest['problem_id']=='30001408'
assert manifest['status']=='unsolved'
assert manifest['approaches_used']==5
for row in manifest['files']:
    path=root/row['path']
    assert path.parent==root and path.is_file(),row['path']
    data=path.read_bytes()
    assert len(data)==row['bytes'],row['path']+' byte count'
    assert hashlib.sha256(data).hexdigest()==row['sha256'],row['path']+' SHA-256'
expected=(root/'CONTROL_RESULTS.json').read_bytes()
actual=subprocess.check_output([sys.executable,str(root/'check_controls.py')])
assert actual==expected,'CONTROL_RESULTS.json does not reproduce byte-for-byte'
assert not list(root.glob('*.pdf'))
assert not list(root.glob('*.png'))
assert not list(root.glob('*.txt'))
print(json.dumps({'status':'PASS','frozen_files_verified':len(manifest['files']),
 'control_output_byte_match':True,'exact_assertions':json.loads(actual)['total_assertions'],
 'limitation':'Integrity and finite controls only; no complete mathematical resolution is certified.'},sort_keys=True,indent=2))
