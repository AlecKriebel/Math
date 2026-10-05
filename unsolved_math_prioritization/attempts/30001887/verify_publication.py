#!/usr/bin/env python3
"""Portable integrity and finite-control replays; no universal-solution claim."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parent
PINNED = {
    'original_author': (1778, 'ff6abddb8c4dc94bd3ef7da776d88e42bfe41501e5f6de8bf9a5206b72f8fa64'),
    'independent_audit': (1811, '7d2a8d49b6d425bd0ebee4075047916c98ba97466eca080487539d76899fd52a'),
}

def require(ok, message):
    if not ok:
        raise ValueError(message)

def digest(data):
    return hashlib.sha256(data).hexdigest()

def check_file(path, entry):
    require(path.is_file() and not path.is_symlink(), f'missing or nonregular file: {path.name}')
    data = path.read_bytes()
    require(len(data) == entry['bytes'], f'byte-count mismatch: {path.name}')
    require(digest(data) == entry['sha256'], f'SHA-256 mismatch: {path.name}')
    if 'git_blob_sha1' in entry:
        blob = b'blob ' + str(len(data)).encode() + b'\0' + data
        require(hashlib.sha1(blob).hexdigest() == entry['git_blob_sha1'], f'Git blob mismatch: {path.name}')

def integrity():
    count = 0
    for directory, (size, sha) in PINNED.items():
        root = ROOT / directory
        manifest_path = root / 'MANIFEST.json'
        check_file(manifest_path, {'bytes': size, 'sha256': sha})
        manifest = json.loads(manifest_path.read_bytes())
        entries = manifest['files']
        expected = {'MANIFEST.json'} | {e['path'] for e in entries}
        actual = {str(p.relative_to(root)) for p in root.rglob('*') if p.is_file()}
        require(actual == expected, f'frozen inventory mismatch: {directory}')
        for entry in entries:
            require(Path(entry['path']).name == entry['path'], 'non-flat frozen manifest path')
            check_file(root / entry['path'], entry)
        count += len(expected)
    manifest_path = ROOT / 'PUBLICATION_MANIFEST.json'
    entries = json.loads(manifest_path.read_bytes())['files']
    expected = {'PUBLICATION_MANIFEST.json'} | {e['path'] for e in entries}
    actual = {str(p.relative_to(ROOT)) for p in ROOT.rglob('*') if p.is_file()}
    require(actual == expected, 'publication inventory mismatch')
    require(len(entries) == len({e['path'] for e in entries}), 'duplicate publication entry')
    for entry in entries:
        path = Path(entry['path'])
        require(not path.is_absolute() and '..' not in path.parts, 'unsafe publication path')
        check_file(ROOT / path, entry)
    return {'immutable_files_checked': count, 'publication_files_checked': len(expected)}

def replay(script, expected):
    with tempfile.TemporaryDirectory(prefix='cover-replay-') as working:
        proc = subprocess.run([sys.executable, str(ROOT / script)], cwd=working,
                              capture_output=True, timeout=240)
    require(proc.returncode == 0, f'replay failed: {script}')
    require(proc.stderr == b'', f'replay stderr not empty: {script}')
    require(proc.stdout == (ROOT / expected).read_bytes(), f'replay bytes differ: {script}')
    return {'script': script, 'return_code': proc.returncode, 'stderr_empty': True,
            'relocated_stdout_byte_identical': True, 'stdout_bytes': len(proc.stdout),
            'stdout_sha256': digest(proc.stdout)}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check-only', action='store_true')
    args = parser.parse_args()
    result = {'problem_id': '30001887', 'integrity': integrity(),
              'scope': 'Integrity and finite controls; not a universal geometric proof.'}
    if not args.check_only:
        result['replays'] = [
            replay('original_author/verify.py', 'original_author/verification_results.json'),
            replay('independent_audit/independent_controls.py', 'independent_audit/independent_results.json'),
        ]
    result['all_requested_checks_passed'] = True
    print(json.dumps(result, indent=2, sort_keys=True))

if __name__ == '__main__':
    main()
