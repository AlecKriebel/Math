#!/usr/bin/env python3
"""Authenticate frozen SU(2) partial results; replay source-free finite checks."""
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

ACCEPTED = {'author/MANIFEST.json': {'bytes': 1079, 'sha256': '7d5d62eaa2d96d5f67383b8f0f7d9ec1888c337f7ff8982d55c0a9fc9f0b97ca'}, 'author/README.md': {'bytes': 1897, 'sha256': '2b0a6a5ec9afbff0a61061f0b5a880d4eb557afac3228df65a3c8c37a4f65b86'}, 'author/REPORT.md': {'bytes': 17013, 'sha256': '31e6d260356d651b18604abf6aa73570726c837f03b59e63c4494ee7312ff4a0'}, 'author/SOURCE_PINS.json': {'bytes': 5708, 'sha256': '45099440c9fa607524486079f2288b6faed18183a88f6bafd0a5bb39c815e1fa'}, 'author/VALIDATION.json': {'bytes': 1373, 'sha256': 'fbda8ae0cc6b378c86a73d55060ca4545e8c2e0e9459f9e927cc738ebcdfa393'}, 'author/audit.py': {'bytes': 8530, 'sha256': '08aa99efb85804497cd09d6ef2aa52a972ec33381a3f44a05eaa9290787c8913'}, 'author/controls.py': {'bytes': 4317, 'sha256': '1ef02eb25f79f057f6fceb5f612d657edf98948a29894c254a72216d1b048e31'}, 'author/verify.py': {'bytes': 3119, 'sha256': '3367e41ffb5e711c436dae352b9786d93295687c053e0090e24c1f4ac1efb41e'}, 'audit/AUDIT.md': {'bytes': 14946, 'sha256': 'a5f8ebdf9e52298d2c986b4d1e56713eef3fbb8b444aefaa85c75740a72a55dc'}, 'audit/MANIFEST.json': {'bytes': 1259, 'sha256': '3212febefd0554e915e7cc352c8be9404dcf406e6c6fc0cd3dc254210b9640b8'}, 'audit/ORIGINAL_FREEZE.json': {'bytes': 1447, 'sha256': '9f2302c8ad549547fea08acd40b7d6873ccc8d96bd017163517108521bf48e86'}, 'audit/README.md': {'bytes': 1943, 'sha256': '4000b65894b6d1c9740006a400eef0e320d910c548da4648639c74e8107ea86e'}, 'audit/SOURCE_REVIEW.json': {'bytes': 5426, 'sha256': '8ce4edb6a32dbb494eb59e0ba1541701b8c7439fecd026568b2b060de0c4d521'}, 'audit/VALIDATION.json': {'bytes': 2435, 'sha256': '051d44bbf0ed0c789007f215226ed3bbf4f7eded48114c466fdf9246dc651a4e'}, 'audit/independent_audit.py': {'bytes': 7661, 'sha256': 'd644bc290c9eed0fc14f4f45dd7e2bf10e70804cd327a01f730b4743fdb06531'}, 'audit/independent_controls.py': {'bytes': 9592, 'sha256': '796f62278feb1378fda323891d0f758e52d32fc40fb54a6f8f3bf9e9ac80da87'}, 'audit/verify.py': {'bytes': 3119, 'sha256': '3367e41ffb5e711c436dae352b9786d93295687c053e0090e24c1f4ac1efb41e'}}
AUTHOR = {n.split('/', 1)[1] for n in ACCEPTED if n.startswith('author/')}
AUDIT = {n.split('/', 1)[1] for n in ACCEPTED if n.startswith('audit/')}
PAYLOAD = set(ACCEPTED) | {'README.md', 'ACCEPTANCE.md', 'verify_publication.py', 'mutation_tests.py'}
FILES = PAYLOAD | {'PUBLICATION_MANIFEST.json', 'BOOTSTRAP.py'}
DIRS = {'author', 'audit'}
AUTHOR_PIN = '7d5d62eaa2d96d5f67383b8f0f7d9ec1888c337f7ff8982d55c0a9fc9f0b97ca'
AUDIT_PIN = '3212febefd0554e915e7cc352c8be9404dcf406e6c6fc0cd3dc254210b9640b8'
ORIGINAL_VERIFIER_PIN = '3367e41ffb5e711c436dae352b9786d93295687c053e0090e24c1f4ac1efb41e'


def need(ok, message):
    if not ok:
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
    result = {}
    for key, value in pairs:
        need(key not in result, 'duplicate JSON key')
        result[key] = value
    return result


def nonfinite(value):
    raise ValueError('nonfinite JSON number')


def finite(value):
    result = float(value)
    need(math.isfinite(result), 'overflowed JSON number')
    return result


def parse(raw):
    return json.loads(raw, object_pairs_hook=unique, parse_constant=nonfinite, parse_float=finite)


def keys(obj, names):
    need(type(obj) is dict and set(obj) == set(names), 'exact object schema')


def exact_int(value, expected=None):
    need(type(value) is int and value >= 0 and (expected is None or value == expected), 'exact nonnegative integer')


def digest(value):
    need(type(value) is str and re.fullmatch('[0-9a-f]{64}', value) is not None, 'lowercase SHA-256')


def inventory(root):
    for path in (root, *root.parents):
        need(stat.S_ISDIR(path.lstat().st_mode), 'linked/non-directory root or ancestor')
    files, dirs = set(), set()
    def visit(directory):
        for entry in os.scandir(directory):
            path = Path(entry.path)
            name = path.relative_to(root).as_posix()
            mode = entry.stat(follow_symlinks=False).st_mode
            if stat.S_ISDIR(mode):
                need(name in DIRS, 'extra directory')
                dirs.add(name)
                visit(path)
            else:
                need(stat.S_ISREG(mode), 'symlink or special member')
                files.add(name)
    visit(root)
    need(files == FILES and dirs == DIRS, 'exact recursive inventory')


def ordinary(path):
    before = path.lstat()
    need(stat.S_ISREG(before.st_mode) and before.st_size <= 1000000, 'regular bounded member')
    with os.fdopen(os.open(path, os.O_RDONLY | getattr(os, 'O_NOFOLLOW', 0)), 'rb') as stream:
        opened = os.fstat(stream.fileno())
        need((before.st_dev, before.st_ino) == (opened.st_dev, opened.st_ino), 'member replaced at open')
        raw = stream.read(1000001)
    need(len(raw) == before.st_size, 'member size changed')
    return raw


def manifest(value, snapshot, payload, role=None):
    keys(value, ['schema', 'problem_id', 'files'] + (['role'] if role is not None else []))
    if role is not None:
        need(same(value['role'], role), 'manifest role')
    exact_int(value['schema'], 1)
    exact_int(value['problem_id'], 2673)
    rows = value['files']
    need(type(rows) is list and len(rows) == len(payload), 'manifest list length/type')
    seen = set()
    for row in rows:
        keys(row, ['path', 'bytes', 'sha256'])
        name = row['path']
        need(type(name) is str and name in payload and name not in seen, 'unknown/duplicate manifest path')
        seen.add(name)
        exact_int(row['bytes']); digest(row['sha256'])
        need(same(row, dict(path=name, bytes=len(snapshot[name]), sha256=sha(snapshot[name]))), 'manifest byte binding')
    need(seen == payload, 'manifest inventory')


def integrity(root, manifest_pin, bootstrap_pin):
    digest(manifest_pin); digest(bootstrap_pin)
    inventory(root)
    snapshot = {name: ordinary(root/name) for name in FILES}
    need(sha(snapshot['PUBLICATION_MANIFEST.json']) == manifest_pin, 'external manifest pin')
    need(sha(snapshot['BOOTSTRAP.py']) == bootstrap_pin, 'external bootstrap pin')
    parsed = {name: parse(raw) for name, raw in snapshot.items() if name.endswith('.json')}
    manifest(parsed['PUBLICATION_MANIFEST.json'], snapshot, PAYLOAD)
    for name, row in ACCEPTED.items():
        need(same(row, dict(bytes=len(snapshot[name]), sha256=sha(snapshot[name]))), 'accepted evidence bytes changed')
    for prefix, names, pin in [('author/', AUTHOR, AUTHOR_PIN), ('audit/', AUDIT, AUDIT_PIN)]:
        need(sha(snapshot[prefix+'MANIFEST.json']) == pin, 'original manifest pin')
        value = parsed[prefix+'MANIFEST.json']
        keys(value, ['format', 'files'])
        need(value['format'] == 'su2-surgery-audit-v1', 'original format')
        rows = value['files']
        need(type(rows) is list and len(rows) == len(names)-1, 'original file count')
        seen = set()
        for row in rows:
            keys(row, ['name', 'bytes', 'sha256'])
            name = row['name']
            need(type(name) is str and name in names-{'MANIFEST.json'} and name not in seen, 'original member name')
            seen.add(name)
            exact_int(row['bytes']); digest(row['sha256'])
            need(same(row, dict(name=name, bytes=len(snapshot[prefix+name]), sha256=sha(snapshot[prefix+name]))), 'original manifest binding')
        need(seen == names-{'MANIFEST.json'}, 'original exact inventory')
    need(parsed['author/VALIDATION.json']['status'] == parsed['audit/VALIDATION.json']['status'] == 'passed', 'historical disposition')
    inventory(root)
    return snapshot, parsed


def replay(snapshot, parsed):
    need(hasattr(os, 'geteuid') and os.getuid() == os.geteuid() == 1000, 'real UID/EUID 1000 required')
    with tempfile.TemporaryDirectory(prefix='su2-publication-') as temporary:
        work = Path(temporary)
        for name in DIRS | {'cwd', 'readonly-author'}:
            (work/name).mkdir()
        for name in ACCEPTED:
            (work/name).write_bytes(snapshot[name])
        for name in AUTHOR:
            (work/'readonly-author'/name).write_bytes(snapshot['author/'+name])
        readonly = [work/'readonly-author', work/'audit', work/'cwd']
        for directory in readonly:
            for path in directory.iterdir():
                path.chmod(0o444)
            directory.chmod(0o555)
        denied = []
        try:
            for path in [work/'readonly-author'/'NEW_FILE', work/'readonly-author'/'REPORT.md', work/'audit'/'NEW_FILE', work/'cwd'/'NEW_FILE']:
                try:
                    with path.open('ab') as stream:
                        stream.write(b'forbidden')
                except PermissionError:
                    denied.append(path.relative_to(work).as_posix())
                else:
                    raise ValueError('read-only write succeeded')
            env = dict(PATH=os.defpath, HOME=str(work), TMPDIR=str(work), LC_ALL='C',
                       PYTHONNOUSERSITE='1', PYTHONDONTWRITEBYTECODE='1', PYTHONSAFEPATH='1')
            flags = [] if sys.flags.optimize == 0 else ['-'+('O'*sys.flags.optimize)]
            def run(script, arguments):
                result = subprocess.run([sys.executable, '-I', '-S', '-B', *flags, str(work/script), *arguments],
                                        cwd=work/'cwd', env=env, capture_output=True, timeout=240)
                need(result.returncode == 0 and result.stderr == b'', 'accepted verifier replay rejected')
                return parse(result.stdout)
            author_root = str(work/'author')
            ro_root = str(work/'readonly-author')
            direct = run('readonly-author/audit.py', [])
            need(same(direct, parsed['author/VALIDATION.json']['math_result']), 'author arithmetic receipt changed')
            for prefix, root, pin in [('readonly-author', ro_root, AUTHOR_PIN), ('audit', str(work/'audit'), AUDIT_PIN)]:
                verified = run(prefix+'/verify.py', [root, '--manifest-sha256', pin])
                need(same(verified, dict(status='passed',file_count=7 if prefix=='readonly-author' else 8,manifest_sha256=pin)), 'native verifier receipt')
            extra = ['--manifest-sha256', AUTHOR_PIN, '--verifier-sha256', ORIGINAL_VERIFIER_PIN]
            independent = run('audit/independent_audit.py', [ro_root, *extra])
            need(same(independent, parsed['audit/VALIDATION.json']['independent_math']), 'independent arithmetic receipt changed')
            # Native mutation harnesses copy mode bits. Their authenticated temporary
            # source copy stays writable; actual arithmetic and verifier inputs above
            # and each harness's dedicated read-only fixture are read-only.
            controls = run('author/controls.py', [author_root, '--manifest-sha256', AUTHOR_PIN])
            need(same(controls, parsed['author/VALIDATION.json']), 'author control receipt changed')
            audit = run('audit/independent_controls.py', [author_root, *extra])
            need(same(audit, parsed['audit/VALIDATION.json']), 'independent control receipt changed')
            need(not list((work/'cwd').iterdir()), 'child wrote to read-only cwd')
            for name in ACCEPTED:
                need((work/name).read_bytes() == snapshot[name], 'replay mutated accepted evidence')
            for name in AUTHOR:
                need((work/'readonly-author'/name).read_bytes() == snapshot['author/'+name], 'readonly input changed')
            return dict(author_math=direct, independent_math=independent,
                        author_control_rejections=50, independent_control_rejections=276,
                        native_controls_own_modes=dict(author=['normal','-O'],independent=['normal','-O','-OO']),
                        readonly_write_probes_denied=denied,
                        historical_source_bindings='11_PUBLIC_PDF_PINS_MATCHED_HISTORICALLY',
                        fresh_source_bindings='NOT_RUN', imported_theorem_proofs='NOT_MACHINE_CERTIFIED',
                        full_classification='UNSOLVED', conditional_extension='PREPRINT_DEPENDENT')
        finally:
            for directory in readonly:
                directory.chmod(0o755)
                for path in directory.iterdir():
                    path.chmod(0o644)


def main():
    need(len(sys.argv) == 4, 'expected manifest pin, bootstrap pin, packet directory')
    manifest_pin, bootstrap_pin, path = sys.argv[1:]
    root = Path(os.path.abspath(path))
    snapshot, parsed = integrity(root, manifest_pin, bootstrap_pin)
    result = replay(snapshot, parsed)
    after, after_parsed = integrity(root, manifest_pin, bootstrap_pin)
    need(after == snapshot and same(after_parsed, parsed), 'publication changed during replay')
    result.update(schema=1, problem_id=2673, status='PASS', publication_files=len(FILES),
                  optimization=sys.flags.optimize, uid=os.getuid(), euid=os.geteuid(),
                  queue_status='unsolved', substantive_turns='5/5',
                  manifest_sha256=manifest_pin, bootstrap_sha256=bootstrap_pin)
    print(json.dumps(result, sort_keys=True))


if __name__ == '__main__':
    try:
        main()
    except (ValueError, OSError, TypeError, KeyError, subprocess.TimeoutExpired):
        print('REJECT: publication integrity/replay validation failed', file=sys.stderr)
        sys.exit(1)
