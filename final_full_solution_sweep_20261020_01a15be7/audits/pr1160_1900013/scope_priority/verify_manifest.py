#!/usr/bin/env python3
"""Read-only hash/membership verifier. Never executes reviewed code or downloads data."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys

HEAD = '6124be0d9baffbfb83d80d7273a2389146b3cf1d'
PREFIX = 'unsolved_math_prioritization/attempts/1900013/'
PR_NAMES = frozenset(['ACCEPTANCE.md','AUDIT.md','CORRECTIONS.md','MANIFEST.json','PROOF.md','README.md','RESULT.md','SOURCE_METADATA.json','SOURCE_VERIFICATION.md','VERIFICATION_SUMMARY.json'])

def require(ok, message):
    if not ok:
        raise ValueError(message)

def digest(data):
    return hashlib.sha256(data).hexdigest()

def verify(root, check_git=False, check_sources=False):
    require(not root.is_symlink(), 'Root must not be a symlink')
    manifest_path = root / 'MANIFEST.json'
    require(manifest_path.is_file() and not manifest_path.is_symlink(), 'Bad manifest')
    manifest = json.loads(manifest_path.read_text())
    require(manifest.get('schema') == 'pr1160-scope-priority-closed-v1', 'Bad schema')
    entries = manifest.get('entries')
    require(type(entries) is list and entries, 'Missing entries')
    seen = set()
    for entry in entries:
        require(type(entry) is dict and set(entry) == {'file','bytes','sha256'}, 'Bad entry keys')
        name = entry['file']
        require(type(name) is str and name not in {'', '.', '..', 'MANIFEST.json'} and Path(name).name == name and '/' not in name and '\\' not in name, 'Unsafe member')
        require(name not in seen, 'Duplicate member')
        seen.add(name)
        require(type(entry['bytes']) is int and entry['bytes'] >= 0, 'Bad byte count')
        require(type(entry['sha256']) is str and len(entry['sha256']) == 64 and all(c in '0123456789abcdef' for c in entry['sha256']), 'Bad digest')
        path = root / name
        require(path.is_file() and not path.is_symlink(), 'Missing or unsafe member: '+name)
        data = path.read_bytes()
        require(len(data) == entry['bytes'] and digest(data) == entry['sha256'], 'Content mismatch: '+name)
    require(manifest.get('members') == sorted(seen | {'MANIFEST.json'}), 'Member list mismatch')
    actual = set()
    for path in root.iterdir():
        require(not path.is_symlink(), 'Symlink in root')
        if path.is_dir():
            require(path.name in {'private_sources','.checks_tmp','__pycache__'}, 'Unlisted directory: '+path.name)
        else:
            actual.add(path.name)
    require(actual == seen | {'MANIFEST.json'}, 'Closed membership mismatch')
    git_count = 0
    if check_git:
        for name in sorted(PR_NAMES):
            actual_blob = subprocess.check_output(['git','show',HEAD+':'+PREFIX+name], cwd=root)
            require(actual_blob == (root/('PR_'+name)).read_bytes(), 'Immutable Git mismatch: '+name)
            git_count += 1
    source_count = 0
    if check_sources:
        pins = json.loads((root/'SOURCE_PINS.json').read_text())
        expected_sources = set()
        for source in pins['sources']:
            for kind in ['pdf','text']:
                item = source[kind]
                name = item['file']
                require(type(name) is str and Path(name).name == name and name not in {'.','..'}, 'Unsafe source path')
                expected_sources.add(name)
                path = root/'private_sources'/name
                require(path.is_file() and not path.is_symlink(), 'Unsafe or missing source')
                data = path.read_bytes()
                require(len(data)==item['bytes'] and digest(data)==item['sha256'], 'Source mismatch: '+name)
                source_count += 1
        require({p.name for p in (root/'private_sources').iterdir()} == expected_sources, 'Private source membership mismatch')
    return {'status':'PASS','authored_members':len(seen)+1,'immutable_git_members_checked':git_count,'private_source_files_checked':source_count}

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--root', type=Path, default=Path(__file__).absolute().parent)
    parser.add_argument('--check-git', action='store_true')
    parser.add_argument('--check-private-sources', action='store_true')
    args = parser.parse_args()
    try:
        print(json.dumps(verify(args.root, args.check_git, args.check_private_sources), sort_keys=True))
    except (ValueError, OSError, KeyError, TypeError, json.JSONDecodeError, subprocess.SubprocessError) as exc:
        print(json.dumps({'status':'FAIL','error':str(exc)}, sort_keys=True))
        sys.exit(1)
