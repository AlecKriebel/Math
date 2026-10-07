#!/usr/bin/env python3
"""Verify audit files against an independently authenticated manifest digest."""
import argparse, hashlib, json
from pathlib import Path

def need(value, message):
    if not value:
        raise ValueError(message)

def digest(data):
    return hashlib.sha256(data).hexdigest()

def unique(items):
    result = {}
    for key, value in items:
        need(key not in result, 'duplicate JSON key')
        result[key] = value
    return result

def main():
    p = argparse.ArgumentParser()
    p.add_argument('--root', type=Path, required=True)
    p.add_argument('--manifest-sha256', required=True)
    a = p.parse_args()
    need(not a.root.is_symlink(), 'symlink root forbidden')
    raw = (a.root/'AUDIT_MANIFEST.json').read_bytes()
    need(digest(raw) == a.manifest_sha256, 'audit manifest differs from external anchor')
    m = json.loads(raw, object_pairs_hook=unique)
    expected = set(m['files']) | {'AUDIT_MANIFEST.json'}
    actual = set()
    for path in a.root.rglob('*'):
        need(not path.is_symlink(), 'symlink forbidden')
        if path.is_file():
            actual.add(path.relative_to(a.root).as_posix())
    need(actual == expected, 'unexpected or missing audit member')
    for name, pin in m['files'].items():
        path = Path(name)
        need(not path.is_absolute() and '..' not in path.parts, 'unsafe audit member path')
        data = (a.root/path).read_bytes()
        need(len(data) == pin['bytes'] and digest(data) == pin['sha256'], 'audit member mismatch: '+name)
    acceptance = json.loads((a.root/'EXACT_ACCEPTANCE.json').read_bytes(), object_pairs_hook=unique)
    need(acceptance['problem_id'] == 3800003 and acceptance['author_original_unchanged'] is True, 'acceptance identity mismatch')
    need(acceptance['full_extremal_problem_solved'] is False and acceptance['new_mathematical_discovery_claimed'] is False, 'audit scope escalation')
    print(json.dumps({'result':'PASS','audit_members_verified':len(expected),'external_anchor_verified':True,'scope':'Artifact integrity only; not theorem certification.'},sort_keys=True))

if __name__ == '__main__':
    main()
