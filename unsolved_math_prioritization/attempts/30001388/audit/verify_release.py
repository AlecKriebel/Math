#!/usr/bin/env python3
"""Read-only portable release/replay verification. No downloads.
Usage: python3 verify_release.py PATH_TO_FROZEN_INPUT_PACKET
"""
import hashlib
import json
from pathlib import Path
import subprocess
import sys

EXPECTED_MANIFEST='5f04dcc149f26a7cab938e0fdf5c649e56230667eab8c0f75ebd5c34ea67f1ad'
EXPECTED_RESULT='5699d79746744620edc6a428d9a8b9afe060f42c7c1fabdb5b851d4e34036ebc'
def sha(data): return hashlib.sha256(data).hexdigest()
def verify_entries(root,manifest):
    for row in manifest['files']:
        data=(root/row['path']).read_bytes()
        assert len(data)==row['bytes'], f"Length mismatch: {row['path']}"
        assert sha(data)==row['sha256'], f"Hash mismatch: {row['path']}"
    return len(manifest['files'])
if len(sys.argv)!=2:
    raise SystemExit(__doc__)
root=Path(sys.argv[1]).resolve()
audit=Path(__file__).resolve().parent
raw=(root/'MANIFEST.json').read_bytes()
assert sha(raw)==EXPECTED_MANIFEST, 'Wrong frozen input release'
assert sha((root/'RESULT.md').read_bytes())==EXPECTED_RESULT, 'Wrong frozen input result'
input_count=verify_entries(root,json.loads(raw))
audit_count=verify_entries(audit,json.loads((audit/'MANIFEST.json').read_text()))
original=subprocess.run([sys.executable,str(root/'verification/check.py')],capture_output=True,check=True).stdout
assert original==(root/'verification/result.json').read_bytes()
assert original==(audit/'original-controls-replayed.json').read_bytes()
independent=subprocess.run([sys.executable,str(audit/'audit_controls.py')],capture_output=True,check=True).stdout
assert independent==(audit/'audit-controls.json').read_bytes()
compile((audit/'audit_controls.py').read_text(),'audit_controls.py','exec')
compile((audit/'verify_release.py').read_text(),'verify_release.py','exec')
print(json.dumps({'status':'passed','input_manifest_sha256':EXPECTED_MANIFEST,'input_result_sha256':EXPECTED_RESULT,'input_files_verified':input_count,'audit_files_verified':audit_count,'original_replay_byte_identical':True,'independent_replay_byte_identical':True,'python_syntax_checks_passed':True},indent=2,sort_keys=True))
