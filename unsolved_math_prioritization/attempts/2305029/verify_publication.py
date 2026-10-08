#!/usr/bin/env python3
"""Fixed accepted bytes and source-free replay. Enter through trusted BOOTSTRAP.py."""
import sys
if not (sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode):
    raise SystemExit('REJECT: use python -I -S -B')
import hashlib
import json
import math
import os
from pathlib import Path
import re
import stat
import subprocess
import tempfile

ACCEPTED = {'author/ACCEPTANCE_REPORT.md': {'bytes': 6530, 'sha256': 'ddca6860d6b51a422d90e282eacf93021c8c62df7331e1136cede15296ccd1a5'}, 'author/MANIFEST.json': {'bytes': 961, 'sha256': 'cf5f178a46b580701522ce59ff4707c4179963ec5d2f8848a759261b1d974206'}, 'author/REPRODUCIBILITY.md': {'bytes': 2453, 'sha256': '4d64f4b98761519b366b20f4e9f45ff9ceaad23b5b2e915e1e788a4d4d880e82'}, 'author/RESULT.json': {'bytes': 1084, 'sha256': 'e4c95918e40475ccd21b86cd6b09346c50514e8649452df08ba902df4504666b'}, 'author/SOURCES.json': {'bytes': 3061, 'sha256': '1925dd3c63bd56fff5a77d271bc639ba3135a2ab783b268e857cee31b309b69f'}, 'author/VALIDATION.json': {'bytes': 772, 'sha256': '8fbc46e3f24c142fab1930d1b6959a3738e938c3febf40664c90b57e8340ec92'}, 'author/verify_packet.py': {'bytes': 2848, 'sha256': 'd6e4afbaf3a7ff9766124220e5ebc9c258b150b6336ea61d4485816dab2a229e'}, 'audit/AUDIT_REPORT.md': {'bytes': 14160, 'sha256': '0abb75eb7347c740ae1031b3be56a954f2a850a5f1a4b8223719f4e16cd9526e'}, 'audit/AUDIT_TEST_RESULTS.json': {'bytes': 106153, 'sha256': '95aaf456faf98563f7b3363369effc3d3b2b52ce8902aa6ed0a1f674086eea63'}, 'audit/INPUT_INVENTORY.json': {'bytes': 1206, 'sha256': '6a9446debefd2d850882a4010e5f0b250f5091af710653f6057b1c232791fa30'}, 'audit/MANIFEST.json': {'bytes': 1223, 'sha256': '5d6f157b0a9ca81a43f14e40ad6e69a767393baf25c84a5a3142b306e95a86af'}, 'audit/REPRODUCIBILITY.md': {'bytes': 3458, 'sha256': '5ca77b4af45b75bc885c897ad39c98eee19533e210813718ef1bd569b913570d'}, 'audit/SOURCE_AUDIT.json': {'bytes': 2767, 'sha256': '23ab64166632e0d17045f3c99db85879829b08daed471fecd457228e7317322d'}, 'audit/run_audit_tests.py': {'bytes': 18152, 'sha256': 'ec648dd9a0d3c8c56a7c4613e03d6d71463d1995935123dfe0d7cba6ef485cdd'}, 'audit/verify_independent.py': {'bytes': 8083, 'sha256': '38a492fafcb770fb2eaf3ffb282db8db4bee7d034fc04fa33d61847ab6463b48'}}

AUTHOR = {'ACCEPTANCE_REPORT.md', 'MANIFEST.json', 'REPRODUCIBILITY.md', 'RESULT.json', 'SOURCES.json', 'VALIDATION.json', 'verify_packet.py'}
AUDIT = {'AUDIT_REPORT.md', 'AUDIT_TEST_RESULTS.json', 'INPUT_INVENTORY.json', 'REPRODUCIBILITY.md', 'SOURCE_AUDIT.json', 'run_audit_tests.py', 'verify_independent.py', 'MANIFEST.json'}
PAYLOAD = {'author/'+n for n in AUTHOR} | {'audit/'+n for n in AUDIT} | {'ACCEPTANCE.md', 'README.md', 'FRESH_REPLAY.json', 'verify_publication.py', 'mutation_tests.py'}
FILES = PAYLOAD | {'PUBLICATION_MANIFEST.json', 'BOOTSTRAP.py'}
DIRS = {'author', 'audit'}
SOURCE_LABELS = {'three_source_byte_identities', 'symlink_source_root', 'source_same_size_mutation', 'source_truncation', 'source_missing', 'source_symlink'}


def need(value, message):
    if not value:
        raise ValueError(message)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def same(a, b):
    if type(a) is not type(b):
        return False
    if type(b) is dict:
        return set(a) == set(b) and all(same(a[k], v) for k, v in b.items())
    if type(b) is list:
        return len(a) == len(b) and all(same(x, y) for x, y in zip(a, b))
    return a == b


def unique(pairs):
    value = {}
    for k, v in pairs:
        need(k not in value, 'duplicate JSON key')
        value[k] = v
    return value


def bad_float(value):
    raise ValueError('nonfinite JSON number')


def finite(value):
    result = float(value)
    need(math.isfinite(result), 'overflowed JSON number')
    return result


def parse(raw):
    return json.loads(raw, object_pairs_hook=unique, parse_constant=bad_float, parse_float=finite)


def keys(obj, names):
    need(type(obj) is dict and set(obj) == set(names), 'exact object fields')


def int_value(value, expected=None):
    need(type(value) is int and value >= 0 and (expected is None or value == expected), 'exact nonnegative integer')


def digest(value):
    need(type(value) is str and re.fullmatch('[0-9a-f]{64}', value) is not None, 'lowercase SHA-256 required')


def inventory(root):
    for p in (root, *root.parents):
        need(stat.S_ISDIR(p.lstat().st_mode), 'root or ancestor is linked/non-directory')
    files, dirs = set(), set()
    def visit(directory):
        for item in os.scandir(directory):
            path = Path(item.path)
            name = path.relative_to(root).as_posix()
            mode = item.stat(follow_symlinks=False).st_mode
            if stat.S_ISDIR(mode):
                need(name in DIRS, 'unexpected directory')
                dirs.add(name)
                visit(path)
            else:
                need(stat.S_ISREG(mode), 'symlink or special member')
                files.add(name)
    visit(root)
    need(files == FILES and dirs == DIRS, 'exact recursive inventory required')


def read_regular(path):
    before = path.lstat()
    need(stat.S_ISREG(before.st_mode) and before.st_size <= 1000000, 'regular bounded member required')
    with os.fdopen(os.open(path, os.O_RDONLY | getattr(os, 'O_NOFOLLOW', 0)), 'rb') as stream:
        opened = os.fstat(stream.fileno())
        need((before.st_dev, before.st_ino) == (opened.st_dev, opened.st_ino), 'member changed at open')
        data = stream.read(1000001)
    need(len(data) == before.st_size, 'member changed size')
    return data


def validate_manifest(value, snapshot):
    keys(value, ['schema', 'problem_id', 'files'])
    int_value(value['schema'], 1)
    int_value(value['problem_id'], 2305029)
    rows = value['files']
    need(type(rows) is list and len(rows) == len(PAYLOAD), 'manifest list size/type')
    seen = set()
    for row in rows:
        keys(row, ['path', 'bytes', 'sha256'])
        n = row['path']
        need(type(n) is str and n in PAYLOAD and n not in seen, 'unknown/duplicate manifest path')
        seen.add(n)
        int_value(row['bytes'])
        digest(row['sha256'])
        need(same(row, dict(path=n, bytes=len(snapshot[n]), sha256=sha(snapshot[n]))), 'manifest identity mismatch')
    need(seen == PAYLOAD, 'manifest inventory mismatch')


def validate_receipt(value, expected_rows, source_run):
    keys(value, ['schema', 'problem_id', 'verdict', 'python_version', 'nonroot', 'readonly_write_probes_blocked', 'original_packet_unchanged', 'source_inputs_unchanged', 'source_tests_run', 'tests', 'test_count', 'scope'])
    fixed = dict(schema=1, problem_id=2305029, verdict='PASS', nonroot=True,
                 readonly_write_probes_blocked=2, original_packet_unchanged=True,
                 source_inputs_unchanged=source_run, source_tests_run=source_run,
                 tests=expected_rows, test_count=len(expected_rows),
                 scope='Finite byte/inventory/parser controls only; no analytic theorem computation')
    for k, v in fixed.items():
        need(same(value[k], v), 'exact receipt field mismatch: '+k)
    need(type(value['python_version']) is str and re.fullmatch(r'[0-9]+\.[0-9]+\.[0-9]+', value['python_version']) is not None, 'Python version type/format')


def integrity(root, manifest_pin, bootstrap_pin):
    digest(manifest_pin); digest(bootstrap_pin)
    inventory(root)
    snapshot = {name: read_regular(root/name) for name in FILES}
    need(sha(snapshot['PUBLICATION_MANIFEST.json']) == manifest_pin, 'external manifest pin mismatch')
    need(sha(snapshot['BOOTSTRAP.py']) == bootstrap_pin, 'external bootstrap identity mismatch')
    parsed = {name: parse(raw) for name, raw in snapshot.items() if name.endswith('.json')}
    validate_manifest(parsed['PUBLICATION_MANIFEST.json'], snapshot)
    for name, row in ACCEPTED.items():
        need(same(row, dict(bytes=len(snapshot[name]), sha256=sha(snapshot[name]))), 'accepted evidence changed')
    historical = parsed['audit/AUDIT_TEST_RESULTS.json']
    need(type(historical['tests']) is list and len(historical['tests']) == 337, 'historical receipt count')
    validate_receipt(historical, historical['tests'], True)
    for row in historical['tests']:
        need(type(row['passed']) is bool and row['passed'] is True, 'historical outcome type')
        int_value(row['expected_exit']); int_value(row['actual_exit'])
        need(row['expected_exit'] == row['actual_exit'], 'historical exit mismatch')
    expected_rows = [row for row in historical['tests'] if row['test'] not in SOURCE_LABELS]
    need(len(expected_rows) == 301, 'source-free subset count')
    validate_receipt(parsed['FRESH_REPLAY.json'], expected_rows, False)
    inventory(root)
    return snapshot, expected_rows


def replay(snapshot, expected_rows):
    need(hasattr(os, 'geteuid') and os.getuid() == os.geteuid() != 0, 'real equal nonroot UID/EUID required')
    with tempfile.TemporaryDirectory(prefix='boundary-publication-') as temporary:
        work = Path(temporary)
        author, audit, cwd = (work/name for name in ['author', 'audit', 'cwd'])
        for p in [author, audit, cwd]:
            p.mkdir()
        for name in ACCEPTED:
            (work/name).write_bytes(snapshot[name])
        for p in audit.iterdir():
            p.chmod(0o444)
        audit.chmod(0o555); cwd.chmod(0o555)
        try:
            env = dict(PATH=os.defpath, HOME=str(work), TMPDIR=str(work), LC_ALL='C',
                       PYTHONNOUSERSITE='1', PYTHONSAFEPATH='1', PYTHONDONTWRITEBYTECODE='1')
            flags = [] if sys.flags.optimize == 0 else ['-'+('O'*sys.flags.optimize)]
            cmd = [sys.executable, '-I', '-S', '-B', *flags, str(audit/'run_audit_tests.py'), '--packet-dir', str(author)]
            result = subprocess.run(cmd, env=env, cwd=cwd, capture_output=True, timeout=180)
            need(result.returncode == 0 and result.stderr == b'', 'source-free audit replay failed')
            fresh = parse(result.stdout)
            validate_receipt(fresh, expected_rows, False)
            need(not list(cwd.iterdir()), 'child wrote to read-only cwd')
            for name in ACCEPTED:
                need((work/name).read_bytes() == snapshot[name], 'replay changed accepted bytes')
            return dict(source_free_expected_outcomes=301, readonly_write_probes_denied=2,
                        historical_full_receipt_outcomes=337, omitted_source_outcomes=36,
                        source_identity_checks='NOT_RUN', source_retrieval='NOT_RUN',
                        source_interpretation='NOT_RUN', mathematical_proof_check='NOT_RUN')
        finally:
            audit.chmod(0o755); cwd.chmod(0o755)


def main():
    need(len(sys.argv) == 4, 'expected manifest pin, bootstrap pin, packet directory')
    manifest_pin, bootstrap_pin, path = sys.argv[1:]
    root = Path(os.path.abspath(path))
    snapshot, rows = integrity(root, manifest_pin, bootstrap_pin)
    result = replay(snapshot, rows)
    after, after_rows = integrity(root, manifest_pin, bootstrap_pin)
    need(after == snapshot and same(after_rows, rows), 'publication input changed')
    result.update(schema=1, problem_id=2305029, status='PASS', publication_files=len(FILES),
                  optimization=sys.flags.optimize, uid=os.getuid(), euid=os.geteuid(),
                  queue_status='already_solved', substantive_turns=0,
                  manifest_sha256=manifest_pin, bootstrap_sha256=bootstrap_pin)
    print(json.dumps(result, sort_keys=True))


if __name__ == '__main__':
    try:
        main()
    except (ValueError, OSError, TypeError, KeyError, subprocess.TimeoutExpired):
        print('REJECT: publication integrity/replay validation failed', file=sys.stderr)
        sys.exit(1)
