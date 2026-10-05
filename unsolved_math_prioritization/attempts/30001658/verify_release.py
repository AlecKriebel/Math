#!/usr/bin/env python3
"""Strictly bind this publication payload and replay its preserved audit."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

AUTHOR_PIN = '68a1fa6b5900a7cc03cd2d991e1a135afb2366a169b680ad5ac9db335203ed68'
AUDIT_PIN = '319db7556fc80438f22288fd6a6b4261c192fb5d883a76691827d81bc642acf5'
AUDIT_TEXT_PIN = '3e9c162a5dc9140872e60e0f4584f8ce44f0ae28cb04887fb7f16baea38546bf'
MANIFEST = 'PUBLICATION_MANIFEST.json'

def require(ok, message):
    if not ok:
        raise ValueError(message)

def sha(data):
    return hashlib.sha256(data).hexdigest()

def unique(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, 'duplicate JSON key')
        result[key] = value
    return result

def verify(root, pin):
    entries = list(root.rglob('*'))
    require(all(not p.is_symlink() for p in entries), 'symlink forbidden')
    require({p.relative_to(root).as_posix() for p in entries if p.is_dir()} ==
            {'release', 'audit_release'}, 'directory inventory mismatch')
    require(all(p.is_file() or p.is_dir() for p in entries), 'nonregular entry')
    raw = (root / MANIFEST).read_bytes()
    require(sha(raw) == pin, 'publication manifest pin mismatch')
    data = json.loads(raw, object_pairs_hook=unique)
    require(set(data) == {'format', 'problem_id', 'files'}, 'manifest schema')
    require(data['format'] == 1 and data['problem_id'] == '30001658', 'manifest identity')
    require(type(data['files']) is list and len(data['files']) == 22, 'manifest count')
    names = []
    for entry in data['files']:
        require(set(entry) == {'path', 'bytes', 'sha256'}, 'entry schema')
        name = entry['path']
        require(type(name) is str and name not in names, 'duplicate or invalid path')
        parts = name.split('/')
        require(all(part not in {'', '.', '..'} for part in parts) and '\\' not in name,
                'unsafe path')
        require(name != MANIFEST, 'self manifest entry')
        names.append(name)
        require(type(entry['bytes']) is int and entry['bytes'] >= 0, 'byte count type')
        payload = (root / name).read_bytes()
        require(len(payload) == entry['bytes'] and sha(payload) == entry['sha256'],
                'payload binding: ' + name)
    files = {p.relative_to(root).as_posix() for p in entries if p.is_file()}
    require(files == set(names) | {MANIFEST}, 'file inventory mismatch')
    require(sha((root/'release/MANIFEST.json').read_bytes()) == AUTHOR_PIN, 'author pin')
    require(sha((root/'audit_release/MANIFEST.json').read_bytes()) == AUDIT_PIN, 'audit pin')
    require(sha((root/'audit_release/AUDIT.md').read_bytes()) == AUDIT_TEXT_PIN, 'audit text pin')
    return {'files': len(files), 'bytes': sum((root/p).stat().st_size for p in files)}

def controls(root, pin):
    cases = ('author_mutation', 'audit_mutation', 'missing_file', 'extra_file',
             'extra_directory', 'replacement_symlink', 'wrong_pin')
    for mode in (False, True):
        for case in cases:
            with tempfile.TemporaryDirectory(prefix='boolean-publication-') as td:
                copy = Path(td)/'packet'
                shutil.copytree(root, copy)
                test_pin = pin
                if case == 'author_mutation':
                    with (copy/'release/PROOF.md').open('ab') as stream:
                        stream.write(b'\nCORRUPTION\n')
                elif case == 'audit_mutation':
                    with (copy/'audit_release/AUDIT.md').open('ab') as stream:
                        stream.write(b'\nCORRUPTION\n')
                elif case == 'missing_file':
                    (copy/'release/PROOF.md').unlink()
                elif case == 'extra_file':
                    (copy/'unexpected.txt').write_text('unexpected', encoding='utf-8')
                elif case == 'extra_directory':
                    (copy/'unexpected').mkdir()
                elif case == 'replacement_symlink':
                    (copy/'release/PROOF.md').unlink()
                    (copy/'release/PROOF.md').symlink_to(root/'release/PROOF.md')
                else:
                    test_pin = '0'*64
                command = [sys.executable, '-B'] + (['-O'] if mode else [])
                command += [str(copy/'verify_release.py'), '--expected-manifest-sha256',
                            test_pin, '--integrity-only']
                result = subprocess.run(command, capture_output=True, check=False)
                require(result.returncode != 0 and b'FAIL:' in result.stderr,
                        'corruption accepted or unrelated failure: ' + case)
    return list(cases)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--expected-manifest-sha256', required=True)
    parser.add_argument('--integrity-only', action='store_true')
    args = parser.parse_args()
    root = Path(__file__).resolve().parent
    before = verify(root, args.expected_manifest_sha256)
    if args.integrity_only:
        print(json.dumps({'status': 'PASS_INTEGRITY_ONLY', **before}, sort_keys=True))
        return
    rejected = controls(root, args.expected_manifest_sha256)
    command = [sys.executable, '-B'] + (['-O'] if sys.flags.optimize else [])
    command += [str(root/'audit_release/verify_audit.py'), '--source-dir',
                str(root/'release'), '--expected-audit-manifest-sha256', AUDIT_PIN]
    result = subprocess.run(command, capture_output=True, check=False)
    require(result.returncode == 0 and not result.stderr, 'audit replay failed')
    audit = json.loads(result.stdout, object_pairs_hook=unique)
    require(audit['status'] == 'PASS_PINNED_INDEPENDENT_AUDIT', 'audit replay status')
    require(before == verify(root, args.expected_manifest_sha256), 'payload changed')
    print(json.dumps({'status': 'PASS_PINNED_PUBLICATION', **before,
                      'manifest_sha256': args.expected_manifest_sha256,
                      'actual_corruption_controls_each_mode': rejected,
                      'audit': audit, 'full_resolution': False}, sort_keys=True, indent=2))

if __name__ == '__main__':
    try:
        main()
    except (ValueError, OSError) as error:
        print('FAIL: ' + str(error), file=sys.stderr)
        raise SystemExit(1)
