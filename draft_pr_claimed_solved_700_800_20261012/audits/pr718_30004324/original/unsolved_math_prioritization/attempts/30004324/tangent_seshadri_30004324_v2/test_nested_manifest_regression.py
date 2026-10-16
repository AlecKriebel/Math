#!/usr/bin/env python3
"""Demonstrate the historical defect and its strict replacement on isolated fixtures."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile

HERE=Path(__file__).resolve().parent
OLD=HERE/'historical'/'v1_verify_manifest.py'
NEW=HERE/'verify_manifest.py'

def accepted(verifier,root):
    return subprocess.run([sys.executable,str(verifier),str(root)],capture_output=True).returncode==0

with tempfile.TemporaryDirectory() as td:
    root=Path(td)/'fixture';root.mkdir()
    data=b'regression fixture\n'
    (root/'payload.txt').write_bytes(data)
    manifest={'schema':1,'files':[{'path':'payload.txt','bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()}]}
    (root/'MANIFEST.json').write_text(json.dumps(manifest))
    assert accepted(OLD,root)
    assert accepted(NEW,root)
    (root/'extra').mkdir()
    (root/'extra'/'MANIFEST.json').write_text('unlisted file\n')
    old_accepts=accepted(OLD,root)
    new_accepts=accepted(NEW,root)
    assert old_accepts is True, 'Historical behavior changed'
    assert new_accepts is False, 'Strict replacement still bypassed'
    print(json.dumps({'status':'PASS','historical_v1_verdict':'REVISE_REQUIRED',
          'original_actual_archive_had_extra_file':False,
          'clean_accepted_by_both':True,'v1_accepts_unlisted_nested_manifest':old_accepts,
          'v2_accepts_unlisted_nested_manifest':new_accepts,
          'authoritative_verifier':'root verify_manifest.py'},indent=2,sort_keys=True))
