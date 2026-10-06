#!/usr/bin/env python3
"""Fail-closed integrity and deterministic replay; not a formal proof checker."""
import argparse
import hashlib
import json
from pathlib import Path
import stat
import subprocess
import sys

NAMES = {
    'RESULT.md', 'PROOFS.md', 'APPROACHES.json', 'SOURCES.json',
    'PUBLIC_METADATA.json', 'exact_controls.py', 'RESULTS.json',
    'AUTHOR_VALIDATION.json', 'verify_release.py',
}


def need(condition, message):
    if not condition:
        raise ValueError(message)


def verify(root, anchor):
    need(len(anchor) == 64 and all(c in '0123456789abcdef' for c in anchor), 'invalid manifest SHA-256')
    actual = set()
    for p in root.iterdir():
        need(not p.is_symlink(), 'symlink forbidden: '+p.name)
        need(stat.S_ISREG(p.lstat().st_mode), 'nonregular entry forbidden: '+p.name)
        actual.add(p.name)
    need(actual == NAMES | {'MANIFEST.json'}, 'unexpected or missing release entry')
    raw = (root/'MANIFEST.json').read_bytes()
    need(hashlib.sha256(raw).hexdigest() == anchor, 'manifest anchor mismatch')
    manifest = json.loads(raw)
    need(set(manifest) == {'schema','problem_id','files'}, 'manifest schema keys')
    need(manifest['schema'] == 1 and manifest['problem_id'] == 30000573, 'manifest identity')
    need(set(manifest['files']) == NAMES, 'manifest member set')
    for name in sorted(NAMES):
        entry = manifest['files'][name]
        need(set(entry) == {'bytes','sha256'}, 'member schema')
        data = (root/name).read_bytes()
        need(type(entry['bytes']) is int and len(data) == entry['bytes'], 'byte count: '+name)
        need(hashlib.sha256(data).hexdigest() == entry['sha256'], 'SHA-256: '+name)
    # Launch the child in the same optimization mode; explicit checks remain active.
    cmd = [sys.executable] + (['-O'] if sys.flags.optimize else []) + ['-B', str(root/'exact_controls.py')]
    child = subprocess.run(cmd, cwd=root, capture_output=True, text=True, timeout=120)
    need(child.returncode == 0, 'control replay failed: '+child.stderr)
    got = json.loads(child.stdout)
    expected = json.loads((root/'RESULTS.json').read_text())
    need(got == expected, 'control output mismatch')
    need(got['status'] == 'PASS_FINITE_DIAGNOSTIC_CONTROLS', 'control result not passing')
    return {'status':'PASS_INTEGRITY_AND_REPLAY','problem_id':30000573,
            'manifest_sha256':anchor,'files_verified':len(NAMES),
            'primary_control_cases':got['total_primary_cases'],
            'scope':'Integrity and finite diagnostic replay, not independent mathematical acceptance.'}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--manifest-sha256', required=True)
    args = parser.parse_args()
    invoked = Path(__file__).absolute()
    root = invoked.parent
    try:
        need(not invoked.is_symlink() and not root.is_symlink(), 'symlink entrypoint or root forbidden')
        print(json.dumps(verify(root, args.manifest_sha256), sort_keys=True, indent=2))
    except Exception as exc:
        print('REJECT: '+str(exc), file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
