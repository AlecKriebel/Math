#!/usr/bin/env python3
"""Verify the audit allowlist, frozen input binding, and independent controls."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys

def digest(p):
    b=p.read_bytes()
    return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}

def main():
    base=Path(__file__).resolve().parent
    ap=argparse.ArgumentParser()
    ap.add_argument('--release',type=Path,default=base.parents[1]/'release')
    args=ap.parse_args()
    manifest=json.loads((base/'MANIFEST.json').read_text())
    expected={r['path']:r for r in manifest['files']}
    assert {p.name for p in base.iterdir()}==set(expected)|{'MANIFEST.json'}
    for name,r in expected.items():
        p=base/name
        assert p.is_file() and not p.is_symlink(),name
        assert digest(p)=={k:r[k] for k in ('bytes','sha256')},name
    binding=json.loads((base/'FROZEN_BINDING.json').read_text())
    for r in binding['frozen_files']:
        p=args.release/r['path']
        assert p.is_file() and not p.is_symlink(),r['path']
        assert digest(p)=={k:r[k] for k in ('bytes','sha256')},r['path']
    assert {p.name for p in args.release.iterdir()}=={r['path'] for r in binding['frozen_files']}
    out=subprocess.run([sys.executable,'-B',str(base/'independent_controls.py')],check=True,capture_output=True,text=True)
    assert json.loads(out.stdout)==json.loads((base/'INDEPENDENT_CONTROLS.json').read_text())
    replay=subprocess.run([sys.executable,'-B',str(args.release/'verify_clasp_bridge.py')],check=True,capture_output=True,text=True)
    assert json.loads(replay.stdout)==json.loads((base/'AUTHOR_REPLAY.json').read_text())
    print(json.dumps({'status':'PASS','safe_files_verified':len(expected),'frozen_files_verified':len(binding['frozen_files']),
        'independent_replay_matches':True,'author_replay_matches':True,
        'audit_verdict':'REVISE_REQUIRED_FOR_FROZEN_DOSSIER','audit_manifest_self_excluded':True},indent=2))

if __name__=='__main__':
    main()
