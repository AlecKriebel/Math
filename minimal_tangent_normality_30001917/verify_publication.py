#!/usr/bin/env python3
"""Pinned, source-free integrity and arithmetic replay. Not formal proof verification."""
import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import stat
import subprocess
import sys
import tempfile
import zipfile

AUTHOR_PIN = 'ab219c442efbac0927009ed5c346fd02e3555e9573374a1961b2efb30188c295'
AUDIT_PIN = '55aa5100c2a0b195a20bda1471739619ece9ca5d0da9394d835829e21b4d238c'
ZIP_PIN = 'ae0ee4bf1381861080eba7b0a84cedb84c266dcac3834f7703226c1f14aef913'

def require(condition, message):
    if not condition:
        raise ValueError(message)

def digest(data):
    return hashlib.sha256(data).hexdigest()

def no_duplicates(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, 'Duplicate JSON key: ' + key)
        result[key] = value
    return result

def read_json(path):
    return json.loads(path.read_bytes(), object_pairs_hook=no_duplicates)

def safe_path(name):
    p = PurePosixPath(name)
    require(isinstance(name, str) and name and not p.is_absolute()
            and p.as_posix() == name and '..' not in p.parts
            and '.' not in p.parts and '\\' not in name,
            'Unsafe or noncanonical manifest path')
    return p

def inventory(root):
    files, dirs = set(), set()
    for parent, children, names in os.walk(root, followlinks=False):
        for name in children + names:
            p = Path(parent) / name
            mode = p.lstat().st_mode
            rel = p.relative_to(root).as_posix()
            if stat.S_ISDIR(mode):
                dirs.add(rel)
            elif stat.S_ISREG(mode):
                files.add(rel)
            else:
                raise ValueError('Symlink or special file rejected: ' + rel)
    return files, dirs

def check_inventory(root, manifest_name, expected_pin):
    manifest_path = root / manifest_name
    require(manifest_path.is_file() and not manifest_path.is_symlink(), 'Missing regular manifest')
    require(digest(manifest_path.read_bytes()) == expected_pin, 'External manifest pin mismatch')
    manifest = read_json(manifest_path)
    entries = manifest['files']
    require(isinstance(entries, dict) and entries, 'Invalid inventory')
    required_files, required_dirs = {manifest_name}, set()
    for name, entry in entries.items():
        p = safe_path(name)
        require(name != manifest_name, 'Self-inclusion is invalid')
        required_files.add(name)
        for ancestor in p.parents:
            if ancestor.as_posix() != '.':
                required_dirs.add(ancestor.as_posix())
        require(set(entry) == {'bytes', 'sha256'}
                and type(entry['bytes']) is int and entry['bytes'] >= 0
                and re.fullmatch('[0-9a-f]{64}', entry['sha256']), 'Invalid file record')
    actual_files, actual_dirs = inventory(root)
    require(actual_files == required_files, 'File inventory differs')
    require(actual_dirs == required_dirs, 'Directory inventory differs')
    for name, entry in entries.items():
        data = (root / name).read_bytes()
        require({'bytes': len(data), 'sha256': digest(data)} == entry, 'Content mismatch: ' + name)
    return len(required_files)

def verify(root, pin):
    require(re.fullmatch('[0-9a-f]{64}', pin) is not None, 'Expected SHA-256 must be an external hexadecimal digest')
    count = check_inventory(root, 'PUBLIC_MANIFEST.json', pin)
    require(check_inventory(root / 'original', 'FROZEN_MANIFEST.json', AUTHOR_PIN) == 10, 'Original count')
    require(check_inventory(root / 'independent_audit', 'AUDIT_MANIFEST.json', AUDIT_PIN) == 6, 'Audit count')
    archive = root / 'archives/original_frozen_v1.zip'
    raw = archive.read_bytes()
    require(len(raw) == 16237 and digest(raw) == ZIP_PIN, 'Frozen archive mismatch')
    with zipfile.ZipFile(archive) as z:
        expected = {'minimal_tangent_normality_30001917/' + p.name for p in (root / 'original').iterdir()}
        require(set(z.namelist()) == expected and len(z.namelist()) == len(expected), 'Archive inventory mismatch')
        for name in z.namelist():
            require(z.read(name) == (root / 'original' / PurePosixPath(name).name).read_bytes(), 'Archive bytes mismatch')
    acceptance = read_json(root / 'independent_audit/ACCEPTANCE.json')
    require(acceptance['audited_frozen_manifest_sha256'] == AUTHOR_PIN
            and acceptance['decision'] == 'accept'
            and acceptance['correction_patch_required'] is False
            and acceptance['turns_completed'] == 0, 'Acceptance mismatch')
    flags = ['-' + 'O' * sys.flags.optimize] if sys.flags.optimize else []
    with tempfile.TemporaryDirectory(prefix='vmrt-replay-') as cwd:
        cp = subprocess.run([sys.executable, '-I', '-B', *flags, str(root / 'original/verify_packet.py')],
                            cwd=cwd, capture_output=True, text=True, timeout=30)
    require(cp.returncode == 0, 'Frozen arithmetic replay failed: ' + cp.stderr)
    result = json.loads(cp.stdout)
    require(result['frozen_integrity']['manifest_sha256'] == AUTHOR_PIN, 'Reported original pin mismatch')
    require(result['arithmetic_and_metadata']['passed'] is True
            and result['arithmetic_and_metadata']['check_count'] == 28, 'Arithmetic replay mismatch')
    # The replay is read-only: recheck inventory and every byte afterward.
    check_inventory(root, 'PUBLIC_MANIFEST.json', pin)
    return {'passed': True, 'problem_id': 30001917, 'disposition': 'credited_prior_result',
            'answer': 'negative', 'research_turns': '0/5', 'package_files': count,
            'arithmetic_checks': 28, 'python_optimization': sys.flags.optimize,
            'publication_manifest_sha256': pin, 'author_manifest_sha256': AUTHOR_PIN,
            'audit_manifest_sha256': AUDIT_PIN, 'frozen_archive_verified': True,
            'limitations': 'Integrity and arithmetic replay only; published geometric theorems remain dependencies. No new counterexample or novelty claimed.'}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--expected-manifest-sha256', required=True,
                        help='Trusted digest obtained independently, for example from the draft PR receipt')
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parent)
    args = parser.parse_args()
    print(json.dumps(verify(args.root.resolve(), args.expected_manifest_sha256), indent=2))

if __name__ == '__main__':
    main()
