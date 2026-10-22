#!/usr/bin/env python3
"""Portable, offline audit verification; no downloaded sources are required."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

AUTHOR_HASH = 'c9a24f4c45b730d60d2ee9668372c729515be65be0425042d5f227e29b613feb'
AUTHOR_BYTES = 2037


def digest(path):
    data = path.read_bytes()
    return len(data), hashlib.sha256(data).hexdigest()


def verify_files(root, pinned=None):
    assert root.is_dir(), str(root)
    assert not any(p.is_symlink() or p.is_dir() for p in root.iterdir()), 'nonregular entry'
    manifest = root / 'SHA256SUMS.json'
    if pinned is not None:
        assert digest(manifest) == pinned, 'pinned manifest changed'
    m = json.loads(manifest.read_text())
    rows = m['files']
    names = [r['path'] for r in rows]
    assert len(names) == len(set(names)), 'duplicate path'
    assert all(Path(n).name == n and n != 'SHA256SUMS.json' for n in names), 'unsafe path'
    actual = {p.name for p in root.iterdir() if p.is_file() and p.name != 'SHA256SUMS.json'}
    assert actual == set(names), 'exact file set differs'
    for row in rows:
        assert digest(root / row['path']) == (row['bytes'], row['sha256']), row['path']
    return m


def replay(script):
    return json.loads(subprocess.check_output([sys.executable, str(script)], text=True))


def mutation_controls(author):
    rejected = []
    with tempfile.TemporaryDirectory(prefix='rank646-audit-') as tmp:
        for name in ('byte_mutation', 'extra_file', 'missing_file', 'changed_manifest'):
            target = Path(tmp) / name
            shutil.copytree(author, target)
            if name == 'byte_mutation':
                p = target / 'README.md'
                p.write_bytes(p.read_bytes() + b'\n')
            elif name == 'extra_file':
                (target / 'unmanifested.txt').write_text('extra')
            elif name == 'missing_file':
                (target / 'README.md').unlink()
            else:
                p = target / 'SHA256SUMS.json'
                p.write_bytes(p.read_bytes() + b'\n')
            try:
                verify_files(target, (AUTHOR_BYTES, AUTHOR_HASH))
            except AssertionError:
                rejected.append(name)
            else:
                raise AssertionError('mutation incorrectly accepted: ' + name)
    return rejected


def main():
    root = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser()
    parser.add_argument('--author', type=Path, default=root.parent / 'submission')
    args = parser.parse_args()
    audit = verify_files(root)
    binding = audit['author_packet']
    assert (binding['manifest_bytes'], binding['manifest_sha256']) == (AUTHOR_BYTES, AUTHOR_HASH)
    author = verify_files(args.author, (AUTHOR_BYTES, AUTHOR_HASH))
    assert len(author['files']) == binding['payload_count'] == 13
    assert replay(args.author / 'verify.py') == json.loads((args.author / 'CONTROL_RESULTS.json').read_text())
    assert replay(root / 'audit_checks.py') == json.loads((root / 'AUDIT_RESULTS.json').read_text())
    result = {'result': 'pass', 'author_payloads': len(author['files']),
              'audit_payloads': len(audit['files']), 'author_control_replay': 'exact',
              'independent_control_replay': 'exact', 'mutation_controls_rejected': mutation_controls(args.author)}
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
