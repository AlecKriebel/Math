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
import shutil
import tempfile

FROZEN = {
    'public/FROZEN_MANIFEST.json': '58932d752e971ec0789b637ceab3ae3f0246927befb6bece2dcb1188ae034100',
    'independent_audit/AUDIT_MANIFEST.json': 'ab605b4f37e0f42b629beb4ca01adc6e0709ab18aabaffaccec8f07cdf09a6a6',
}
CORRECTED = 'a79471afeeed8236e333a7a40bfede32359613eb1e2c9af2b6488984a12fc660'
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


def load_json(raw):
    def bad_constant(value):
        raise ValueError('Nonfinite JSON constant: ' + value)
    return json.loads(raw, object_pairs_hook=unique, parse_constant=bad_constant)


def verify(root, expected):
    need(type(expected) is str and HEX.fullmatch(expected) is not None, 'Invalid external anchor')
    need(stat.S_ISDIR(root.lstat().st_mode), 'Packet root must be a real directory')
    raw = read_regular(root / 'PUBLICATION_MANIFEST.json')
    need(sha(raw) == expected, 'Publication manifest anchor mismatch')
    manifest = load_json(raw)
    need(set(manifest) == {'schema', 'problem_id', 'status', 'turns', 'source_files_redistributed', 'frozen_manifest_anchors', 'files'}, 'Invalid publication schema')
    need(manifest['schema'] == 'kmedian-publication-v1', 'Wrong publication schema')
    need(type(manifest['problem_id']) is int and manifest['problem_id'] == 2800903, 'Wrong problem')
    need(manifest['status'] == 'unsolved' and manifest['turns'] == '5/5', 'Wrong disposition')
    need(manifest['source_files_redistributed'] is False, 'Source redistribution not permitted')
    need(manifest['frozen_manifest_anchors'] == FROZEN, 'Frozen anchor mapping mismatch')
    count = validate_members(root, 'PUBLICATION_MANIFEST.json', manifest['files'])
    for relative, anchor in FROZEN.items():
        path = root / relative
        raw = read_regular(path)
        need(sha(raw) == anchor, 'Frozen manifest anchor mismatch: ' + relative)
        inner = load_json(raw)
        need(type(inner['problem_id']) is int and inner['problem_id'] == 2800903, 'Wrong frozen problem')
        validate_members(path.parent, path.name, inner['files'], flat=True)
        if relative.startswith('independent_audit/'):
            need(inner['frozen_input_manifest_sha256'] == FROZEN['public/FROZEN_MANIFEST.json'], 'Audit author anchor mismatch')
    path = root / 'corrected/CORRECTED_MANIFEST.json'
    raw = read_regular(path)
    need(sha(raw) == CORRECTED, 'Corrected manifest anchor mismatch')
    corrected = load_json(raw)
    validate_members(path.parent, path.name, corrected['files'], flat=True)
    need(read_regular(root / 'corrected/verify.py') == read_regular(root / 'independent_audit/verify_hardened.py'), 'Hardened copy mismatch')
    need(read_regular(root / 'corrected/SOURCE_NOTES.md') == read_regular(root / 'independent_audit/SOURCE_NOTES_corrected.md'), 'Source notes copy mismatch')
    # Parse all included JSON after their bytes are authenticated.
    for item in manifest['files']:
        if item['path'].endswith('.json'):
            load_json(read_regular(root / item['path']))
    return count


def replay_patches(root):
    pairs = [('verify.py', 'VERIFY_HARDENING.patch'), ('SOURCE_NOTES.md', 'SOURCE_SCOPE.patch')]
    receipts = []
    with tempfile.TemporaryDirectory(prefix='kmedian-patch-') as temporary:
        target = Path(temporary)
        for name, patch in pairs:
            (target / name).write_bytes(read_regular(root / 'public' / name))
            result = subprocess.run(['patch', '--batch', '--fuzz=0', '-p1', '-i', str(root / 'independent_audit' / patch)],
                                    cwd=target, capture_output=True, timeout=30)
            need(result.returncode == 0, 'Patch replay failed: ' + patch)
            need(b'offset' not in result.stdout.lower() and b'fuzz' not in result.stdout.lower(), 'Inexact patch application')
            data = read_regular(target / name)
            need(data == read_regular(root / 'corrected' / name), 'Patch output mismatch: ' + name)
            receipts.append({'patch': patch, 'output_sha256': sha(data), 'exact_match': True})
        need({p.name for p in target.iterdir()} == {p[0] for p in pairs}, 'Unexpected patch output')
    return receipts


def replay(root):
    # Preserve frozen bytes and remove all inherited Python settings. -I explicitly
    # disables environmental optimization for the assertion-dependent original.
    env = {k: v for k, v in os.environ.items() if not k.startswith('PYTHON')}
    env['PYTHONDONTWRITEBYTECODE'] = '1'
    receipts = []
    with tempfile.TemporaryDirectory(prefix='kmedian-replay-') as temporary:
        target = Path(temporary)
        for name in ('public', 'independent_audit', 'corrected'):
            shutil.copytree(root / name, target / name)
        specs = [('public/verify.py', [], 'public/verification.json', 'ordinary_original')]
        for mode, flags in [('ordinary', []), ('optimized', ['-O']), ('double_optimized', ['-OO'])]:
            specs.append(('corrected/verify.py', flags, 'corrected/verification.json', mode))
            specs.append(('independent_audit/replay_audit.py', flags, 'independent_audit/AUDIT_CHECKS.json', mode))
        for script, flags, receipt, mode in specs:
            output = target / receipt
            if output.exists(): output.unlink()
            result = subprocess.run([sys.executable, '-I', '-B', *flags, str(target / script)], cwd=target,
                                    env=env, capture_output=True, timeout=240)
            need(result.returncode == 0, 'Replay failed: ' + script + ': ' + result.stderr.decode(errors='replace'))
            payload = read_regular(output)
            expected = 'public/verification.json' if script.endswith('verify.py') else receipt
            need(payload == read_regular(root / expected), 'Receipt mismatch: ' + script)
            parsed = load_json(payload)
            key, value = ('exact_assertions', 118649) if script.endswith('verify.py') else ('exact_independent_checks', 30090)
            need(parsed[key] == value, 'Wrong check count')
            receipts.append({'script': script, 'mode': mode, 'receipt_sha256': sha(payload), 'receipt_byte_match': True})
    return receipts


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--packet', type=Path, default=Path(__file__).absolute().parent)
    parser.add_argument('--expected-manifest', required=True)
    parser.add_argument('--check-only', action='store_true')
    args = parser.parse_args()
    root = args.packet.absolute()
    count = verify(root, args.expected_manifest)
    patches = [] if args.check_only else replay_patches(root)
    receipts = [] if args.check_only else replay(root)
    verify(root, args.expected_manifest)
    print(json.dumps({'status': 'PASS', 'problem_id': 2800903, 'publication_manifest_sha256': args.expected_manifest,
                      'bound_files': count, 'check_only': args.check_only, 'patch_replay': patches, 'replays': receipts,
                      'limits': 'Byte integrity and finite controls only; mathematical acceptance is in ROOT_ACCEPTANCE.md. No human peer review or novelty is certified.'}, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
