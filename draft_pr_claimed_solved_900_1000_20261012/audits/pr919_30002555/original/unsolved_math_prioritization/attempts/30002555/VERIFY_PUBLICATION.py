#!/usr/bin/env python3
"""Fail-closed publication verifier. Pin this program externally before execution.

The expected outer-manifest hash must come from an independent trusted record.
This verifies bytes and finite computations, not the mathematical proof itself.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import stat
import subprocess
import sys

FROZEN = {
    'public/MANIFEST.json': 'f7b959531c352611c5c9b9d0c2cb57bcb865de9399d65dbd66c4fabef3a88e59',
    'audit_rotational_independent/public/MANIFEST.json': 'f8253e86c12c287519a511681d28ec8bcd1206836a3c88b5468c3590db4ea172',
    'reviewer_b/public/MANIFEST.json': 'd28152e3fe482c20d9c5e089bfce21f6582ccbd616223ed010ae6ce51b07025f',
}
HEX = re.compile(r'[0-9a-f]{64}')


def need(value, message):
    if not value:
        raise RuntimeError(message)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def unique(pairs):
    result = {}
    for key, value in pairs:
        need(key not in result, 'Duplicate JSON key: ' + key)
        result[key] = value
    return result


def read_regular(path):
    need(stat.S_ISREG(path.lstat().st_mode), 'Missing or nonregular file: ' + str(path))
    return path.read_bytes()


def validate_members(root, manifest_name, entries, flat=False):
    need(type(entries) is list and bool(entries), 'Empty or invalid inventory')
    names = {manifest_name}
    directories = set()
    for item in entries:
        need(type(item) is dict and set(item) == {'path', 'bytes', 'sha256'}, 'Invalid member schema')
        name = item['path']
        need(type(name) is str and name and '\\' not in name, 'Unsafe path')
        parts = name.split('/')
        need(all(re.fullmatch(r'[A-Za-z0-9_.-]+', p) and p not in ('.', '..') for p in parts), 'Unsafe path')
        need(not flat or len(parts) == 1, 'Nonflat frozen inventory')
        need(name not in names, 'Duplicate inventory path')
        names.add(name)
        for parent in PurePosixPath(name).parents:
            if str(parent) != '.':
                directories.add(str(parent))
        need(type(item['bytes']) is int and item['bytes'] >= 0, 'Invalid byte count')
        need(type(item['sha256']) is str and HEX.fullmatch(item['sha256']) is not None, 'Invalid digest')
    actual_files, actual_dirs = set(), set()
    for directory, subdirs, files in os.walk(root, followlinks=False):
        for name in subdirs + files:
            path = Path(directory) / name
            mode = path.lstat().st_mode
            relative = path.relative_to(root).as_posix()
            need(not stat.S_ISLNK(mode), 'Symlink forbidden: ' + relative)
            if stat.S_ISDIR(mode):
                actual_dirs.add(relative)
            else:
                need(stat.S_ISREG(mode), 'Special file forbidden: ' + relative)
                actual_files.add(relative)
    need(actual_files == names and actual_dirs == directories, 'Exact inventory mismatch')
    for item in entries:
        data = read_regular(root / item['path'])
        need(len(data) == item['bytes'], 'Size mismatch: ' + item['path'])
        need(sha(data) == item['sha256'], 'Digest mismatch: ' + item['path'])
    return len(entries)


def verify(root, expected):
    need(type(expected) is str and HEX.fullmatch(expected) is not None, 'Invalid external anchor')
    need(stat.S_ISDIR(root.lstat().st_mode), 'Packet root must be a real directory')
    raw = read_regular(root / 'PUBLICATION_MANIFEST.json')
    need(sha(raw) == expected, 'Publication manifest anchor mismatch')
    manifest = json.loads(raw, object_pairs_hook=unique)
    need(set(manifest) == {'schema', 'problem_id', 'status', 'turns', 'source_files_redistributed', 'frozen_manifest_anchors', 'files'}, 'Invalid publication schema')
    need(manifest['schema'] == 'veech-ends-publication-v1', 'Wrong publication schema')
    need(type(manifest['problem_id']) is int and manifest['problem_id'] == 30002555, 'Wrong problem')
    need(manifest['status'] == 'claimed_solved' and manifest['turns'] == '1/5', 'Wrong disposition')
    need(manifest['source_files_redistributed'] is False, 'Source redistribution not permitted')
    need(manifest['frozen_manifest_anchors'] == FROZEN, 'Frozen anchor mapping mismatch')
    count = validate_members(root, 'PUBLICATION_MANIFEST.json', manifest['files'])
    for relative, anchor in FROZEN.items():
        path = root / relative
        raw = read_regular(path)
        need(sha(raw) == anchor, 'Frozen manifest anchor mismatch: ' + relative)
        inner = json.loads(raw, object_pairs_hook=unique)
        need(type(inner['problem_id']) is int and inner['problem_id'] == 30002555, 'Wrong frozen problem')
        validate_members(path.parent, 'MANIFEST.json', inner['files'], flat=True)
        if relative != 'public/MANIFEST.json':
            need(inner['author_manifest_sha256'] == FROZEN['public/MANIFEST.json'], 'Audit author anchor mismatch')
    return count


def replay(root):
    # Isolated top-level children ignore all PYTHON* variables. Also remove these
    # variables explicitly so legacy nested ordinary subprocesses stay ordinary.
    env = {k: v for k, v in os.environ.items() if not k.startswith('PYTHON')}
    env['PYTHONDONTWRITEBYTECODE'] = '1'
    specs = [
        ('public/CHECKS.py', [], 'public/CHECK_RESULTS.json'),
        ('audit_rotational_independent/public/INDEPENDENT_CHECKS.py', [str(root / 'public')], 'audit_rotational_independent/public/INDEPENDENT_RESULTS.json'),
        ('reviewer_b/public/INDEPENDENT_CHECKS.py', [], 'reviewer_b/public/INDEPENDENT_RESULTS.json'),
        ('public/VERIFY.py', [FROZEN['public/MANIFEST.json']], None),
        ('audit_rotational_independent/public/VERIFY_AUDIT.py', [FROZEN['audit_rotational_independent/public/MANIFEST.json'], str(root / 'public')], None),
    ]
    receipts = []
    for mode, flags in [('ordinary', []), ('optimized', ['-O']), ('double_optimized', ['-OO'])]:
        for script, arguments, receipt in specs:
            result = subprocess.run([sys.executable, '-I', '-B', *flags, str(root / script), *arguments], cwd=root, env=env, capture_output=True, timeout=180)
            need(result.returncode == 0, 'Replay failed: ' + script + ': ' + result.stderr.decode(errors='replace'))
            parsed = json.loads(result.stdout, object_pairs_hook=unique)
            need(parsed.get('status') == 'PASS', 'Replay did not report PASS: ' + script)
            if receipt:
                need(result.stdout == read_regular(root / receipt), 'Receipt mismatch: ' + script)
            receipts.append({'script': script, 'mode': mode, 'stdout_sha256': sha(result.stdout), 'receipt_byte_match': receipt is not None})
    return receipts


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--packet', type=Path, default=Path(__file__).absolute().parent)
    parser.add_argument('--expected-manifest', required=True)
    parser.add_argument('--check-only', action='store_true')
    args = parser.parse_args()
    root = args.packet.absolute()
    count = verify(root, args.expected_manifest)
    receipts = [] if args.check_only else replay(root)
    verify(root, args.expected_manifest)
    print(json.dumps({'status': 'PASS', 'problem_id': 30002555, 'publication_manifest_sha256': args.expected_manifest,
                      'bound_files': count, 'check_only': args.check_only, 'replays': receipts,
                      'limits': 'Byte integrity and finite controls only; mathematical acceptance is in ROOT_ACCEPTANCE.md. No human peer review or novelty is certified.'}, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
