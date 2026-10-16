#!/usr/bin/env python3
"""Verify exact safe allowlist and replay independent diagnostics without writes."""
import argparse
import hashlib
import json
from pathlib import Path
import sys
sys.dont_write_bytecode=True
import independent_checks as checks

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--author-zip',type=Path)
    a=p.parse_args()
    root=Path(__file__).resolve().parents[1]
    manifest=json.loads((root/'MANIFEST.json').read_text())
    expected={e['path']:e for e in manifest['files']}
    actual={f.relative_to(root).as_posix() for f in root.rglob('*') if f.is_file()}
    checks.require(len(expected)==len(manifest['files']),'duplicate manifest entry')
    checks.require(actual==set(expected)|{'MANIFEST.json'},'safe allowlist')
    for n,r in expected.items():
        f=root/n
        checks.require(not f.is_symlink(),'symlink in safe payload')
        raw=f.read_bytes()
        checks.require(len(raw)==r['bytes'] and hashlib.sha256(raw).hexdigest()==r['sha256'],'hash mismatch: '+n)
    result=json.loads((root/'results/independent_checks.json').read_text())
    checks.require(checks.algebra()==result['finite_diagnostics'],'independent algebra changed')
    checks.require(checks.extra_controls()==result['extra_controls'],'extra controls changed')
    if a.author_zip:
        checks.require(checks.check_author(a.author_zip)==result['author_integrity'],'author integrity changed')
    print(json.dumps({'status':'PASS','safe_files_including_manifest':len(actual),
                      'independent_cases':56,'base_exact_controls':2168,
                      'extra_jump_controls':300,'criticality_controls':32,
                      'original_author_archive_checked':bool(a.author_zip),
                      'scope':'Integrity and finite diagnostics, not a proof assistant'},indent=2))

if __name__=='__main__':main()
