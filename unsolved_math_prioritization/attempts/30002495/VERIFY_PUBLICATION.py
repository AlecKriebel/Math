#!/usr/bin/env python3
"""Fail-closed publication verifier. Pin this program externally before execution.

The expected outer-manifest hash must come from an independent trusted record.
This verifies bytes and finite computations, not the mathematical proof itself.
"""
import argparse
import ast
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import stat
import subprocess
import sys

FROZEN = {
    'original/MANIFEST.json': '6c41bb59af46e93ffdc169484847271bbec0a6fc178673d491cf8ec9e41244ea',
    'independent_audit/MANIFEST.json': '4d5639f148af610bfad3dac6a757fb3858a7c50196771fcf8eacb7a2ca90de6c',
    'corrected/MANIFEST.json': 'c78d12a95bb8b565d9266e959b272e9b9cb241046f26733f1892e0736df39ae7',
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
    need(manifest['schema'] == 'nyman-real-variable-publication-v1', 'Wrong publication schema')
    need(type(manifest['problem_id']) is int and manifest['problem_id'] == 30002495, 'Wrong problem')
    need(manifest['status'] == 'unsolved' and manifest['turns'] == '5/5', 'Wrong disposition')
    need(manifest['source_files_redistributed'] is False, 'Source redistribution not permitted')
    need(manifest['frozen_manifest_anchors'] == FROZEN, 'Frozen anchor mapping mismatch')
    count = validate_members(root, 'PUBLICATION_MANIFEST.json', manifest['files'])
    for relative, anchor in FROZEN.items():
        path = root / relative
        raw = read_regular(path)
        need(sha(raw) == anchor, 'Frozen manifest anchor mismatch: ' + relative)
        inner = json.loads(raw, object_pairs_hook=unique)
        need(type(inner['problem_id']) is int and inner['problem_id'] == 30002495, 'Wrong frozen problem')
        validate_members(path.parent, 'MANIFEST.json', inner['files'], flat=True)
        expected_schema = ('nyman-independent-audit-manifest-v1' if relative.startswith('independent_audit/')
                           else 'nyman-real-variable-frozen-packet-v1')
        need(inner['schema'] == expected_schema, 'Wrong frozen schema')
        if relative.startswith('independent_audit/'):
            need(inner['input_manifest_sha256'] == FROZEN['original/MANIFEST.json'], 'Audit author anchor mismatch')
        if relative.startswith('corrected/'):
            need(inner['derivation']['original_manifest_sha256'] == FROZEN['original/MANIFEST.json'], 'Correction provenance mismatch')
    exact_correction(root)
    return count


def apply_exact_patch(original, patch):
    """Strict single-file unified patch replay: exact positions and context, no fuzz."""
    old = original.decode('utf-8').splitlines(keepends=True)
    lines = patch.decode('utf-8').splitlines(keepends=True)
    need(lines[:2] == ['--- a/check_controls.py\n', '+++ b/check_controls.py\n'], 'Wrong patch target')
    output, cursor, i, hunks = [], 0, 2, 0
    while i < len(lines):
        match = re.fullmatch(r'@@ -(\d+),(\d+) \+(\d+),(\d+) @@\n', lines[i])
        need(match is not None, 'Malformed patch hunk')
        old_start, old_count, new_start, new_count = map(int, match.groups())
        need(old_start - 1 >= cursor, 'Overlapping patch hunk')
        output.extend(old[cursor:old_start - 1]); cursor = old_start - 1
        need(len(output) == new_start - 1, 'New hunk offset mismatch')
        used, made = 0, 0
        i += 1
        while i < len(lines) and not lines[i].startswith('@@ '):
            line = lines[i]
            need(line and line[0] in ' +-', 'Invalid patch line')
            if line[0] in ' -':
                need(cursor < len(old) and old[cursor] == line[1:], 'Exact patch context mismatch')
                cursor += 1; used += 1
            if line[0] in ' +':
                output.append(line[1:]); made += 1
            i += 1
        need(used == old_count and made == new_count, 'Patch hunk count mismatch')
        hunks += 1
    need(hunks > 0, 'Empty patch')
    output.extend(old[cursor:])
    return ''.join(output).encode('utf-8')


def exact_correction(root):
    original = read_regular(root / 'original/check_controls.py')
    corrected = read_regular(root / 'corrected/check_controls.py')
    patch = read_regular(root / 'independent_audit/OPTIMIZATION_SAFETY.patch')
    need(apply_exact_patch(original, patch) == corrected, 'Patch replay mismatch')
    need(corrected == read_regular(root / 'independent_audit/check_controls_hardened.py'), 'Audit corrected checker mismatch')
    need(sum(isinstance(n, ast.Assert) for n in ast.walk(ast.parse(original))) == 16, 'Wrong original assertion count')
    tree = ast.parse(corrected)
    need(not any(isinstance(n, ast.Assert) for n in ast.walk(tree)), 'Corrected asserts remain')
    need(sum(isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id == 'require'
             for n in ast.walk(tree)) == 16, 'Wrong corrected guard count')
    for path in (root / 'original').iterdir():
        if path.name not in ('MANIFEST.json', 'check_controls.py'):
            need(read_regular(path) == read_regular(root / 'corrected' / path.name), 'Unexpected derived change: ' + path.name)
    return True


def replay(root, selected):
    # Remove all PYTHON* variables for legacy nested subprocesses. -I pins the
    # immediate child against caller environment and import-path contamination.
    env = {k: v for k, v in os.environ.items() if not k.startswith('PYTHON')}
    env['PYTHONDONTWRITEBYTECODE'] = '1'
    specs = [
        ('corrected/check_controls.py', [], 'corrected/CONTROL_RESULTS.json', 'bytes'),
        ('independent_audit/independent_math_controls.py', [], 'independent_audit/INDEPENDENT_MATH_RESULTS.json', 'bytes'),
        ('independent_audit/audit_controls.py', ['--packet', str(root / 'original')], 'independent_audit/AUDIT_CONTROL_RESULTS.json', 'runtime_metadata'),
        ('original/verify_packet.py', ['--replay', '--selftest'], None, 'inventory'),
        ('corrected/verify_packet.py', ['--replay', '--selftest'], None, 'inventory'),
        ('independent_audit/verify_audit.py', ['--expected-manifest-sha256', FROZEN['independent_audit/MANIFEST.json'], '--selftest'], None, 'audit_inventory'),
    ]
    receipts = []
    for mode, flags in [('ordinary', []), ('optimized', ['-O']), ('double_optimized', ['-OO'])]:
        if selected != 'all' and selected != mode:
            continue
        for script, arguments, receipt, comparison in specs:
            result = subprocess.run([sys.executable, '-I', '-B', *flags, str(root / script), *arguments], cwd=root, env=env, capture_output=True, timeout=600)
            need(result.returncode == 0, 'Replay failed: ' + script + ': ' + result.stderr.decode(errors='replace'))
            parsed = json.loads(result.stdout, object_pairs_hook=unique)
            if comparison == 'inventory':
                need(parsed['inventory'] == 'PASS' and parsed['control_replay'] == 'BYTE_IDENTICAL' and parsed['assertion_groups'] == 23767, 'Original/corrected replay mismatch')
                need(len(parsed['rejected_integrity_mutations']) == 8, 'Missing inner inventory controls')
            elif comparison == 'audit_inventory':
                need(parsed['audit_inventory'] == 'PASS' and len(parsed['rejected_mutations']) == 7, 'Audit inventory selftest failure')
            else:
                need(parsed.get('status') == 'PASS', 'Replay did not report PASS: ' + script)
            if comparison == 'bytes':
                need(result.stdout == read_regular(root / receipt), 'Receipt byte mismatch: ' + script)
            if comparison == 'runtime_metadata':
                expected = json.loads(read_regular(root / receipt), object_pairs_hook=unique)
                parsed.pop('python', None); expected.pop('python', None)
                need(parsed == expected, 'Audit receipt mismatch beyond runtime-version metadata')
            receipts.append({'script': script, 'mode': mode, 'stdout_sha256': sha(result.stdout), 'comparison': comparison})
    return receipts


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--packet', type=Path, default=Path(__file__).absolute().parent)
    parser.add_argument('--expected-manifest', required=True)
    parser.add_argument('--check-only', action='store_true')
    parser.add_argument('--mode', choices=['all', 'ordinary', 'optimized', 'double_optimized'], default='all')
    args = parser.parse_args()
    root = args.packet.absolute()
    count = verify(root, args.expected_manifest)
    receipts = [] if args.check_only else replay(root, args.mode)
    verify(root, args.expected_manifest)
    print(json.dumps({'status': 'PASS', 'problem_id': 30002495, 'publication_manifest_sha256': args.expected_manifest,
                      'bound_files': count, 'check_only': args.check_only, 'replays': receipts,
                      'limits': 'Byte integrity and finite controls only; mathematical acceptance is in ROOT_ACCEPTANCE.md. No human peer review or novelty is certified.'}, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
