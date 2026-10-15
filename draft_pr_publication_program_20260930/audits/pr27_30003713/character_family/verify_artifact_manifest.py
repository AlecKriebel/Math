#!/usr/bin/env python3
"""Verify the self-excluding first-party family artifact inventory."""
from pathlib import Path
import hashlib,json

ROOT=Path(__file__).resolve().parent
EXCLUDED={'artifact_manifest.json'}
IGNORED={'tmp_sources','tmp_replay','__pycache__'}


def inventory():
    out={}
    for p in ROOT.rglob('*'):
        rel=p.relative_to(ROOT)
        if not p.is_file() or rel.as_posix() in EXCLUDED or any(x in IGNORED for x in rel.parts):continue
        b=p.read_bytes()
        out[rel.as_posix()]={'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
    return out


if __name__=='__main__':
    m=json.loads((ROOT/'artifact_manifest.json').read_text())
    assert m['self_excluded']=='artifact_manifest.json'
    assert m['artifacts']==inventory(),'artifact inventory or byte hash mismatch'
    print('PASS: self-excluding first-party manifest matches every included file')
