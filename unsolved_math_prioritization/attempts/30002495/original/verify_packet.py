#!/usr/bin/env python3
"""Strict frozen inventory, optional deterministic replay, and integrity controls."""
import argparse
import copy
import hashlib
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

SCHEMA = 'nyman-real-variable-frozen-packet-v1'
MANIFEST = 'MANIFEST.json'


def verify(root):
    root = Path(root).resolve()
    mp = root/MANIFEST
    if mp.is_symlink() or not mp.is_file():
        raise ValueError('Manifest missing or symlinked')
    m = json.loads(mp.read_text())
    if m.get('schema') != SCHEMA or not isinstance(m.get('files'), list):
        raise ValueError('Wrong manifest schema')
    entries = {}
    for e in m['files']:
        if set(e) != {'path', 'bytes', 'sha256'}:
            raise ValueError('Wrong entry fields')
        name = e['path']
        if not isinstance(name, str) or not re.fullmatch(r'[A-Za-z0-9_.-]+', name) or name in {'.', '..', MANIFEST}:
            raise ValueError('Unsafe or reserved path')
        if name in entries:
            raise ValueError('Duplicate path')
        if type(e['bytes']) is not int or e['bytes'] < 0 or not re.fullmatch(r'[0-9a-f]{64}', e['sha256']):
            raise ValueError('Invalid byte count or digest')
        entries[name] = e
    actual = set()
    for p in root.iterdir():
        if p.is_symlink() or not p.is_file():
            raise ValueError('Unexpected non-regular entry: '+p.name)
        actual.add(p.name)
    if actual != set(entries)|{MANIFEST}:
        raise ValueError('Complete inventory mismatch')
    for name, e in entries.items():
        data = (root/name).read_bytes()
        if len(data) != e['bytes'] or hashlib.sha256(data).hexdigest() != e['sha256']:
            raise ValueError('Length/hash mismatch: '+name)
    return len(entries)


def mutations(root):
    names = ['altered_bytes', 'missing_file', 'extra_file', 'wrong_byte_count',
             'wrong_hash', 'traversal_path', 'duplicate_entry', 'symlinked_file']
    passed = []
    with tempfile.TemporaryDirectory(prefix='nyman_integrity_') as tmp:
        tmp = Path(tmp)
        for name in names:
            p = tmp/name
            shutil.copytree(root, p)
            m = json.loads((p/MANIFEST).read_text())
            if name == 'altered_bytes':
                with (p/'PROOFS.md').open('ab') as f:
                    f.write(b'\nMUTATION\n')
            elif name == 'missing_file':
                (p/'RESULT.json').unlink()
            elif name == 'extra_file':
                (p/'EXTRA.txt').write_text('unexpected')
            elif name == 'wrong_byte_count':
                m['files'][0]['bytes'] += 1
            elif name == 'wrong_hash':
                m['files'][0]['sha256'] = '0'*64
            elif name == 'traversal_path':
                m['files'][0]['path'] = '../escape'
            elif name == 'duplicate_entry':
                m['files'].append(copy.deepcopy(m['files'][0]))
            elif name == 'symlinked_file':
                (p/'RESULT.json').unlink()
                (p/'RESULT.json').symlink_to(Path(root)/'RESULT.json')
            (p/MANIFEST).write_text(json.dumps(m, indent=2)+'\n')
            try:
                verify(p)
            except (ValueError, OSError, TypeError, KeyError):
                passed.append(name)
            else:
                raise AssertionError('Mutation not rejected: '+name)
    return passed


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--root', type=Path, default=Path(__file__).resolve().parent)
    ap.add_argument('--replay', action='store_true')
    ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args()
    n = verify(a.root)
    report = {'inventory': 'PASS', 'hashed_files': n,
              'manifest_sha256': hashlib.sha256((a.root/MANIFEST).read_bytes()).hexdigest()}
    if a.replay:
        p = subprocess.run([sys.executable, str((a.root/'check_controls.py').resolve())],
                           capture_output=True, check=True)
        expected = (a.root/'CONTROL_RESULTS.json').read_bytes()
        if p.stdout != expected:
            raise ValueError('Control replay differs from recorded bytes')
        report['control_replay'] = 'BYTE_IDENTICAL'
        report['assertion_groups'] = json.loads(expected)['total_assertion_groups']
    if a.selftest:
        report['rejected_integrity_mutations'] = mutations(a.root.resolve())
    report['limits'] = 'Integrity and finite-control replay, not a mathematical proof certificate.'
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
