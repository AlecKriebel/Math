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
    'original/MANIFEST.json': 'a9b478491ffe9f3dd75d177bd863ec8dc2f28ac3ed69f04bce9e35955247e989',
    'corrected/MANIFEST.json': '937d23a943cda19e23850e7e84842b74c97dd936e280d8d3a1bdea07a58710e3',
    'independent_audit/MANIFEST.json': '686831a2a758fcd663fa5795ae0cbe229adcd636be512cc1999e26f93d89287a',
    'second_review/MANIFEST.json': '56e6978c21452d495b7e8dd534ca70eb7f0848cb10f895b56985534acf16db6d',
}
TOP_FILES = {'README.md', 'PUBLICATION_ACCEPTANCE.md', 'RESEARCH_LOG.md',
             'VERIFY_PUBLICATION.py', 'TEST_MUTATIONS.py', 'MUTATION_RESULTS.json',
             'PUBLICATION_MANIFEST.json'}

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
        need(PurePosixPath(name).suffix in {'.md', '.json', '.py', '.patch'}, 'Disallowed file type')
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
        raise RuntimeError('Nonfinite JSON constant: ' + value)
    return json.loads(raw, object_pairs_hook=unique, parse_constant=bad_constant)


def verify(root, expected):
    need(type(expected) is str and HEX.fullmatch(expected) is not None, 'Invalid external anchor')
    need(stat.S_ISDIR(root.lstat().st_mode), 'Packet root must be a real directory')
    raw = read_regular(root / 'PUBLICATION_MANIFEST.json')
    need(sha(raw) == expected, 'Publication manifest anchor mismatch')
    manifest = load_json(raw)
    need(type(manifest) is dict and set(manifest) == {'schema', 'problem_id', 'status', 'turns', 'source_files_redistributed', 'frozen_manifest_anchors', 'files'}, 'Invalid publication schema')
    need(manifest['schema'] == 'rational-voa-publication-v1', 'Wrong publication schema')
    need(type(manifest['problem_id']) is int and manifest['problem_id'] == 30002842, 'Wrong problem')
    need(manifest['status'] == 'unsolved' and manifest['turns'] == '5/5', 'Wrong disposition')
    need(manifest['source_files_redistributed'] is False, 'Source redistribution not permitted')
    need(manifest['frozen_manifest_anchors'] == FROZEN, 'Frozen anchor mapping mismatch')
    need({p.name for p in root.iterdir()} == TOP_FILES | {'original', 'corrected', 'independent_audit', 'second_review'}, 'Top-level inventory mismatch')
    count = validate_members(root, 'PUBLICATION_MANIFEST.json', manifest['files'])
    for relative, anchor in FROZEN.items():
        path = root / relative
        raw = read_regular(path)
        need(sha(raw) == anchor, 'Frozen manifest anchor mismatch: ' + relative)
        inner = load_json(raw)
        second = relative.startswith('second_review/')
        need(type(inner) is dict and set(inner) == ({'schema', 'files'} if second else {'schema', 'problem_id', 'files'}), 'Frozen schema fields')
        if not second:
            need(type(inner['problem_id']) is int and inner['problem_id'] == 30002842, 'Wrong frozen problem')
        expected_schema = ('independent-voa-moving-tail-audit-v1' if second else 'rational-voa-independent-audit-v1' if relative.startswith('independent_audit/') else 'rational-voa-frozen-manifest-v1')
        need(inner['schema'] == expected_schema, 'Wrong frozen schema')
        need(type(inner['files']) is list, 'Wrong frozen inventory type')
        converted = []
        for e in inner['files']:
            need(type(e) is dict and set(e) == {'name', 'bytes', 'sha256'}, 'Frozen member schema')
            converted.append({'path': e['name'], 'bytes': e['bytes'], 'sha256': e['sha256']})
        validate_members(path.parent, 'MANIFEST.json', converted, flat=True)
    # Decode all JSON with duplicate-key and nonfinite-value rejection.
    for path in root.rglob('*.json'):
        load_json(read_regular(path))
    exact_correction(root)
    return count


def apply_exact_patch(originals, patch):
    """Strict multi-file unified patch replay: exact positions and context, no fuzz."""
    lines = patch.decode('utf-8').splitlines(keepends=True)
    outputs = {}
    i = 0
    while i < len(lines):
        need(lines[i].startswith('--- a/') and lines[i+1].startswith('+++ b/'), 'Malformed patch headers')
        name = lines[i][6:].rstrip('\n')
        need(lines[i+1] == '+++ b/' + name + '\n', 'Patch target mismatch')
        need(name in originals and name not in outputs, 'Unexpected or duplicate patch target')
        old = originals[name].decode('utf-8').splitlines(keepends=True)
        output, cursor, hunks = [], 0, 0
        i += 2
        while i < len(lines) and not lines[i].startswith('--- a/'):
            match = re.fullmatch(r'@@ -(\d+),(\d+) \+(\d+),(\d+) @@\n', lines[i])
            need(match is not None, 'Malformed patch hunk')
            old_start, old_count, new_start, new_count = map(int, match.groups())
            need(old_start - 1 >= cursor, 'Overlapping patch hunk')
            output.extend(old[cursor:old_start - 1]); cursor = old_start - 1
            need(len(output) == new_start - 1, 'New hunk offset mismatch')
            used, made = 0, 0
            i += 1
            while i < len(lines) and not lines[i].startswith(('@@ ', '--- a/')):
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
        outputs[name] = ''.join(output).encode('utf-8')
    need(set(outputs) == set(originals), 'Missing patch target')
    return outputs


def exact_correction(root):
    names = {'test_negative_controls.py', 'MANIFEST.json'}
    originals = {n: read_regular(root / 'original' / n) for n in names}
    outputs = apply_exact_patch(originals, read_regular(root / 'independent_audit/READONLY_REPLAY_FIX.patch'))
    for name, data in outputs.items():
        need(data == read_regular(root / 'corrected' / name), 'Patch replay mismatch: ' + name)
    for path in (root / 'original').iterdir():
        if path.name not in names:
            need(read_regular(path) == read_regular(root / 'corrected' / path.name), 'Unexpected derived change: ' + path.name)
    for relative in ['VERIFY_PUBLICATION.py', 'TEST_MUTATIONS.py', 'corrected/verify_packet.py', 'corrected/verify_math.py', 'corrected/test_negative_controls.py', 'independent_audit/verify_audit.py', 'independent_audit/test_audit.py']:
        tree = ast.parse(read_regular(root / relative))
        need(not any(isinstance(n, ast.Assert) for n in ast.walk(tree)), 'Optimization-removable guard: ' + relative)
    return True


def replay(root, selected):
    env = {k: v for k, v in os.environ.items() if not k.startswith('PYTHON')}
    env['PYTHONDONTWRITEBYTECODE'] = '1'
    audit_args = ['--author-root', str(root / 'original'), '--expected-audit-manifest', FROZEN['independent_audit/MANIFEST.json']]
    specs = [
        ('original/verify_packet.py', [], 'author'),
        ('corrected/verify_packet.py', [], 'author'),
        ('corrected/test_negative_controls.py', [], 'author_mutations'),
        ('independent_audit/verify_audit.py', audit_args, 'audit'),
        ('independent_audit/test_audit.py', audit_args, 'audit_mutations'),
    ]
    modes = [('ordinary', []), ('optimized', ['-O']), ('double_optimized', ['-OO'])]
    receipts = []
    for mode, flags in modes:
        if selected != 'all' and selected != mode:
            continue
        for script, extra, kind in specs:
            result = subprocess.run([sys.executable, '-I', '-B', *flags, str(root / script), *extra], env=env, capture_output=True, timeout=120)
            need(result.returncode == 0, 'Replay failed: ' + script + ': ' + result.stderr.decode())
            value = load_json(result.stdout)
            need(value.get('ok') is True, 'Replay did not report ok: ' + script)
            if kind == 'author':
                need(value['result']['status'] == 'unsolved_partial' and value['result']['files_authenticated'] == 9, 'Author result mismatch')
            elif kind == 'author_mutations':
                need(value['positive_baselines'] == 3 and value['mathematical_rejections'] == 30 and value['integrity_rejections'] == 21 and len(value['details']) == 54, 'Author mutation coverage mismatch')
            elif kind == 'audit':
                need(value['result']['author_files'] == 9 and value['result']['audit_files'] == 9, 'Audit result mismatch')
            elif kind == 'audit_mutations':
                need(value == load_json(read_regular(root / 'independent_audit/TEST_RESULTS.json'))['independent_suite'], 'Audit receipt mismatch')
            receipts.append({'script': script, 'mode': mode, 'stdout_sha256': sha(result.stdout), 'check': kind})
        # The immutable narrow review contains assertions. Always use an isolated
        # ordinary child, even if this wrapper itself runs under -O or -OO.
        control = subprocess.run([sys.executable, '-I', '-B', '-c', 'import sys; print(sys.flags.optimize); assert False, "ASSERTION_RETENTION_CONTROL"'], env=env, capture_output=True)
        need(control.returncode != 0 and control.stdout == b'0\n' and b'AssertionError: ASSERTION_RETENTION_CONTROL' in control.stderr, 'Ordinary assertion guard not retained')
        script = 'second_review/verify_controls.py'
        result = subprocess.run([sys.executable, '-I', '-B', str(root / script)], env=env, capture_output=True, timeout=60)
        need(result.returncode == 0 and result.stdout == read_regular(root / 'second_review/CONTROL_RESULTS.json'), 'Narrow-review ordinary replay mismatch')
        receipts.append({'script': script, 'wrapper_replay_mode': mode, 'child_mode': 'ordinary_enforced', 'assertion_negative_control': 'rejected', 'positive_checks': 1150, 'negative_controls': 4, 'stdout_sha256': sha(result.stdout)})
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
    print(json.dumps({'status': 'PASS', 'problem_id': 30002842, 'publication_manifest_sha256': args.expected_manifest,
                      'bound_files': count, 'check_only': args.check_only, 'replays': receipts,
                      'limits': 'Byte integrity and finite controls only; mathematical acceptance is in PUBLICATION_ACCEPTANCE.md. The narrow review certifies only Sections 2.3-2.5 and 5. No human peer review or novelty is certified.'}, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
