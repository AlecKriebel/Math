#!/usr/bin/env python3
"""Verify this source-free audit from an externally supplied manifest pin."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile


def require(condition, message):
    if not condition:
        raise ValueError(message)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def verify(root, expected_digest):
    require(re.fullmatch('[0-9a-f]{64}', expected_digest) is not None, 'Expected digest must be SHA-256')
    path = root/'MANIFEST.json'
    require(path.is_file() and not path.is_symlink(), 'Manifest missing or symlinked')
    raw = path.read_bytes()
    require(sha(raw) == expected_digest, 'External audit-manifest pin mismatch')
    m = json.loads(raw)
    require(m['schema'] == 'nyman-independent-audit-manifest-v1', 'Wrong audit schema')
    names = {'MANIFEST.json'}
    for e in m['files']:
        require(set(e) == {'path', 'bytes', 'sha256'}, 'Malformed inventory entry')
        name = e['path']
        require(isinstance(name, str) and re.fullmatch('[A-Za-z0-9_.-]+', name) is not None
                and name not in names and name not in {'.', '..'}, 'Unsafe or duplicate path')
        require(type(e['bytes']) is int and e['bytes'] >= 0, 'Invalid byte count')
        require(isinstance(e['sha256'], str) and re.fullmatch('[0-9a-f]{64}', e['sha256']) is not None,
                'Invalid digest')
        p = root/name
        require(p.is_file() and not p.is_symlink(), 'Nonregular audit member')
        data = p.read_bytes()
        require(len(data) == e['bytes'] and sha(data) == e['sha256'], 'Audit member mismatch: '+name)
        names.add(name)
    require({p.name for p in root.iterdir()} == names, 'Audit inventory mismatch')
    return len(names)-1


def selftest(root, pin):
    names = ['changed_file', 'missing_file', 'extra_file', 'symlinked_file',
             'symlinked_manifest', 'nested_directory', 'coordinated_rehash']
    rejected = []
    with tempfile.TemporaryDirectory(prefix='nyman_audit_selftest_') as tmp:
        for name in names:
            p = Path(tmp)/name
            shutil.copytree(root, p)
            target = p/'INDEPENDENT_AUDIT.md'
            if name in ('changed_file', 'coordinated_rehash'):
                target.write_bytes(target.read_bytes()+b'\nNEGATIVE CONTROL\n')
            if name == 'missing_file': target.unlink()
            elif name == 'extra_file': (p/'extra.txt').write_text('unexpected')
            elif name == 'symlinked_file':
                target.unlink()
                target.symlink_to(root/'INDEPENDENT_AUDIT.md')
            elif name == 'symlinked_manifest':
                (p/'MANIFEST.json').unlink()
                (p/'MANIFEST.json').symlink_to(root/'MANIFEST.json')
            elif name == 'nested_directory': (p/'unexpected').mkdir()
            elif name == 'coordinated_rehash':
                mp = p/'MANIFEST.json'
                m = json.loads(mp.read_bytes())
                for e in m['files']:
                    if e['path'] == target.name:
                        e['bytes'], e['sha256'] = target.stat().st_size, sha(target.read_bytes())
                mp.write_text(json.dumps(m, indent=2)+'\n')
            try:
                verify(p, pin)
            except (ValueError, OSError, TypeError, KeyError):
                rejected.append(name)
            else:
                raise ValueError('Audit mutation accepted: '+name)
    return rejected


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--root', type=Path, default=Path(__file__).resolve().parent)
    ap.add_argument('--expected-manifest-sha256', required=True)
    ap.add_argument('--selftest', action='store_true')
    ap.add_argument('--replay', action='store_true')
    ap.add_argument('--packet', type=Path)
    a = ap.parse_args()
    root = a.root.resolve()
    n = verify(root, a.expected_manifest_sha256)
    result = {'audit_inventory': 'PASS', 'hashed_files': n,
              'manifest_sha256': a.expected_manifest_sha256}
    if a.selftest:
        result['rejected_mutations'] = selftest(root, a.expected_manifest_sha256)
    if a.replay:
        require(a.packet is not None, '--replay requires --packet pointing to the original frozen packet')
        env = dict(os.environ)
        env['PYTHONDONTWRITEBYTECODE'] = '1'
        commands = [('audit_controls.py', ['--packet', str(a.packet.resolve())], 'AUDIT_CONTROL_RESULTS.json'),
                    ('independent_math_controls.py', [], 'INDEPENDENT_MATH_RESULTS.json')]
        for program, args, expected_file in commands:
            p = subprocess.run([sys.executable, str(root/program), *args], capture_output=True, env=env)
            require(p.returncode == 0, 'Replay failed: '+program+'\n'+p.stderr.decode(errors='replace'))
            actual = json.loads(p.stdout)
            expected = json.loads((root/expected_file).read_bytes())
            actual.pop('python', None)
            expected.pop('python', None)
            require(actual == expected, 'Replay mismatch: '+program)
        result['replay'] = 'PASS_RUNTIME_VERSION_METADATA_EXCLUDED'
    result['limits'] = 'Authored audit integrity and finite controls only; not formal proof verification.'
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
