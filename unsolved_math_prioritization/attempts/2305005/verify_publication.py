#!/usr/bin/env python3
"""Authenticate frozen qualified partials; run only source-free finite controls."""
import sys
if not (sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode):
    raise SystemExit('REJECT: use python -I -S -B')
import hashlib
import io
import json
import math
import os
from pathlib import Path
import re
import stat
import subprocess
import tempfile
import zipfile

ACCEPTED = {'AUDIT_FREEZE_RECEIPT.json': {'bytes': 1555, 'sha256': '897f678e8ff54c88d4723354b9bef0c9f384c301e322fb54f931d3be3adb2f05'}, 'AUTHOR_FREEZE_RECEIPT.json': {'bytes': 3516, 'sha256': '7e17750906cdf0c3f2c2a6fef621c98cdf3ac756b307e6b7856cc89f8036a15b'}, 'SLOW_INRADIUS_2305005_AUDIT_PACKET.zip': {'bytes': 17223, 'sha256': 'f9e052e5520c6e17ad3f683f5b18ab84d1e79f55e9c1b747c8229cbecebdaf54'}, 'SLOW_INRADIUS_2305005_AUTHOR_PACKET.zip': {'bytes': 20951, 'sha256': '8c85e9a8e91e9a0124b62644a7663d7c69b487bb579678ef5772a57e0f1671a1'}, 'audit/ACCEPTANCE.json': {'bytes': 3796, 'sha256': '492d2aefe9b5642eeaf3dcfb744df219dc7133a63ca0775b86c5cade22777710'}, 'audit/AUDIT.md': {'bytes': 19581, 'sha256': '6fb815863e352b162acd42fe2f7fc82acf8cd8a9b7f165328dfebcc1953dcc66'}, 'audit/CHECK_RESULTS.json': {'bytes': 5073, 'sha256': 'e226660962087d4233aa813c6135349802517e4eb256a7889479bc2e0ae77bfc'}, 'audit/MANIFEST.json': {'bytes': 689, 'sha256': '3b291188c7b0e79961ae68a5e038487b5245bbf8a1c989ceb8575468a61df776'}, 'audit/audit_checks.py': {'bytes': 13729, 'sha256': '4b3eb31a1d366602d0473a3121aa53d5efae17722838571dc7e6bb2dcfd27418'}, 'author/CLAIMS.json': {'bytes': 1909, 'sha256': '08efa046f1aa1019d3559115c41287cd18281b60c1738131f146e8000dc6ec6b'}, 'author/FIXTURES.json': {'bytes': 28134, 'sha256': '55398de04d947048ec182de1a4f158a6ace184a5b25d8c473cb8643a7fa7c4c3'}, 'author/MANIFEST.json': {'bytes': 1082, 'sha256': '916ef2162da505bef37aab22de595ccc2c91497908a3b8f28f9c29a81588356a'}, 'author/README.md': {'bytes': 2724, 'sha256': '0da2e32b8c5cc7ea2461971a21bfc12f0c23868bc7b1909e4d70bff83e1e38e4'}, 'author/REPORT.md': {'bytes': 17949, 'sha256': '8dad8162b583d12b5dfd89bffa86a3f3fe2dbf58165a5b01b7e4bcb5dff6cf05'}, 'author/SOURCES.json': {'bytes': 2956, 'sha256': 'aae687e0c2dc69a5f8d834feb3f8b12cf865256bd6f9d60d65c0d0bb6244e769'}, 'author/controls.py': {'bytes': 7310, 'sha256': '15296427ecf733e0e896d409b9923a64b3ad433fd3b7dae964e894323eb403c0'}, 'author/verify.py': {'bytes': 10889, 'sha256': '487fcef8ed8739fc083835904b3093cd99920c388a3a07e6e48a712a5f7ed870'}}
AUTHOR = {n.split('/', 1)[1] for n in ACCEPTED if n.startswith('author/')}
AUDIT = {n.split('/', 1)[1] for n in ACCEPTED if n.startswith('audit/')}
PAYLOAD = set(ACCEPTED) | {'README.md', 'ACCEPTANCE.md', 'verify_publication.py', 'mutation_tests.py'}
FILES = PAYLOAD | {'PUBLICATION_MANIFEST.json', 'BOOTSTRAP.py'}
DIRS = {'author', 'audit'}
AUTHOR_PIN = '916ef2162da505bef37aab22de595ccc2c91497908a3b8f28f9c29a81588356a'


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
    exact_int(value['problem_id'], 2305005)
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


def archive(raw, snapshot, prefix, names):
    with zipfile.ZipFile(io.BytesIO(raw)) as z:
        entries = z.infolist()
        need(len(entries) == len(names) and {e.filename for e in entries} == names, 'archive exact inventory')
        need(z.comment == b'', 'unexpected archive comment')
        for entry in entries:
            need(not entry.is_dir() and stat.S_ISREG(entry.external_attr >> 16), 'archive member type')
            need(not (entry.flag_bits & 1) and entry.file_size == len(snapshot[prefix+entry.filename]), 'archive type/size')
            need(z.read(entry) == snapshot[prefix+entry.filename], 'archive member bytes')


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
    for prefix, names in [('author/', AUTHOR), ('audit/', AUDIT)]:
        manifest(parsed[prefix+'MANIFEST.json'], {n:snapshot[prefix+n] for n in names}, names-{'MANIFEST.json'},
                 'independent_audit' if prefix == 'audit/' else None)
    archive(snapshot['SLOW_INRADIUS_2305005_AUTHOR_PACKET.zip'], snapshot, 'author/', AUTHOR)
    archive(snapshot['SLOW_INRADIUS_2305005_AUDIT_PACKET.zip'], snapshot, 'audit/', AUDIT)
    accepted = parsed['audit/ACCEPTANCE.json']
    for key, expected in dict(recommended_queue_status='unsolved', recommended_turns='5/5', full_solution_accepted=False,
                              correction_required=False, original_fernandez_proof_independently_verified=False,
                              onto_counterexample_proved=False).items():
        need(same(accepted[key], expected), 'acceptance scope changed')
    inventory(root)
    return snapshot, parsed


def replay(snapshot, parsed):
    need(hasattr(os, 'geteuid') and os.getuid() == os.geteuid() != 0, 'real equal nonroot UID/EUID required')
    historical = parsed['audit/CHECK_RESULTS.json']
    with tempfile.TemporaryDirectory(prefix='slow-publication-') as temporary:
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
                                        cwd=work/'cwd', env=env, capture_output=True, timeout=180)
                need(result.returncode == 0 and result.stderr == b'', 'accepted verifier replay rejected')
                return parse(result.stdout)
            author_root = str(work/'author')
            direct = run('readonly-author/verify.py', ['--root', str(work/'readonly-author'), '--manifest-sha256', AUTHOR_PIN])
            expected_direct = dict(historical['author_source_replay'])
            expected_direct['source_inputs_rehashed'] = []
            need(same(direct, expected_direct), 'source-free author receipt changed')
            controls = run('readonly-author/controls.py', ['--root', author_root, '--manifest-sha256', AUTHOR_PIN])
            need(same(controls, historical['author_controls_replayed']), 'author control receipt changed')
            audit = run('audit/audit_checks.py', ['--author-root', author_root, '--archive', str(work/'SLOW_INRADIUS_2305005_AUTHOR_PACKET.zip'),
                                               '--receipt', str(work/'AUTHOR_FREEZE_RECEIPT.json')])
            expected_audit = dict(historical['independent_controls'])
            expected_audit['read_only_uid'] = os.geteuid()
            need(same(audit, expected_audit), 'independent control receipt changed')
            need(not list((work/'cwd').iterdir()), 'child wrote to read-only cwd')
            for name in ACCEPTED:
                need((work/name).read_bytes() == snapshot[name], 'replay mutated accepted evidence')
            for name in AUTHOR:
                need((work/'readonly-author'/name).read_bytes() == snapshot['author/'+name], 'readonly input changed')
            return dict(author_finite_checks=6806, author_negative_rejections=63,
                        independent_finite_checks=20510, independent_negative_rejections=111,
                        readonly_write_probes_denied=denied, historical_source_bindings='MATCHED_HISTORICALLY',
                        fresh_source_bindings='NOT_RUN', original_fernandez_proof_verification='NOT_RUN',
                        analytic_existence_proof_computation='NOT_RUN')
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
    result.update(schema=1, problem_id=2305005, status='PASS', publication_files=len(FILES),
                  optimization=sys.flags.optimize, uid=os.getuid(), euid=os.geteuid(),
                  queue_status='unsolved', substantive_turns='5/5',
                  manifest_sha256=manifest_pin, bootstrap_sha256=bootstrap_pin)
    print(json.dumps(result, sort_keys=True))


if __name__ == '__main__':
    try:
        main()
    except (ValueError, OSError, TypeError, KeyError, zipfile.BadZipFile, subprocess.TimeoutExpired):
        print('REJECT: publication integrity/replay validation failed', file=sys.stderr)
        sys.exit(1)
