#!/usr/bin/env python3
"""Authenticate the source-free negative-resolution packet; replay bounded checks."""
import sys
if not (sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode):
    raise SystemExit('REJECT: use python -I -S -B')
import copy
import hashlib
import io
import json
import math
import os
from pathlib import Path
import re
import stat
import subprocess
import tarfile
import tempfile

ACCEPTED = {'author/public/README.md': {'bytes': 1575, 'sha256': '98a106326df13cdab1b46094dab21565dd86519546246c34d943156a7f67f5a5'}, 'author/public/REPORT.md': {'bytes': 9338, 'sha256': 'ddde58f03f320c881b78e59b60a40f315e1811c7c88aaa25ce620c427afbb6ca'}, 'author/public/fixtures.json': {'bytes': 276, 'sha256': 'cc8769655ddc787fe8446f78f24afd3d27dac6c4e393932418b0846e2eba1581'}, 'author/public/provenance.json': {'bytes': 1065, 'sha256': 'd16faf5c48ca84bff4df008c8c9a7df40da8b8b43c025b6edc900ed1448392bb'}, 'author/public/sources.json': {'bytes': 2647, 'sha256': '3fd2c18b83be32c4579c63917c1907b2970508b805dace66e2eadfb818cc43d8'}, 'author/public/verify.py': {'bytes': 6773, 'sha256': 'b805650e49c5096f0fe368653122989c1087f59447871a5cb6fc32843d6983d1'}, 'author/external/AUDIT_INSTRUCTIONS.md': {'bytes': 2129, 'sha256': '49bf1d5d113f20220531bcb1efe34a9eddf2934b15f804c93c862b7563e6ec2c'}, 'author/external/MANIFEST.json': {'bytes': 919, 'sha256': '31bd2aed10d96d5ada5344531e2207dd4388c8cb1328e3c448ac89be5b78ec8c'}, 'author/external/PINS.json': {'bytes': 900, 'sha256': 'cbf61f7d4163f50d15eb264e779bb79c9fc8a0566b571f0d9d9a3bf3fd96634d'}, 'author/external/TEST_RESULTS.json': {'bytes': 3380, 'sha256': '379250873a4334150bd5d0127f6288d7c8258ebef09cb8b24bb1e6b86e509ffc'}, 'author/external/bootstrap.py': {'bytes': 3700, 'sha256': '054dbe643ad4f78f13ea0595e4cab5379d438a33ab2fd2f6aed9f5125d9dcb57'}, 'author/external/test_harness.py': {'bytes': 7784, 'sha256': '5c6d1056179a95c647db5cc11028059c64c5abcdcabd69790cef892948c9ca27'}, 'expansive_group_2616_frozen.tar.gz': {'bytes': 13488, 'sha256': '1e9e605ee96cdceaca6d9e5ea3b007f0849d0383c8db5f7e4b0c84c35a68de5b'}, 'audit_1/INDEPENDENT_MATHEMATICAL_AUDIT.md': {'bytes': 11198, 'sha256': '4342d824640fde88bfcd492841b365955456764d4c99eca61d788e3fa6e65f73'}, 'audit_2/INDEPENDENT_AUDIT.md': {'bytes': 14229, 'sha256': '9993b954dd21a2666eebef1a6653aa52a49b98ad14ac4007b1f7e9e62eb724e4'}, 'audit_2/independent_checks.py': {'bytes': 12076, 'sha256': '584a53a61519dbf67a4b97cbb06a56c4df239ae923a3e603645795e64e563523'}, 'audit_2/INDEPENDENT_RESULTS.json': {'bytes': 5165, 'sha256': 'a55904da47987715988fb43f448ee0e46fe2aa14102a37c67f4fda6dcf9f392b'}, 'audit_2/AUTHOR_HARNESS_RERUN.json': {'bytes': 3380, 'sha256': '379250873a4334150bd5d0127f6288d7c8258ebef09cb8b24bb1e6b86e509ffc'}, 'audit_2/AUTHOR_SNAPSHOT.json': {'bytes': 2236, 'sha256': '95c22d85bbce877de0ea004f89195473ffe628348de1eb2327a99f387ea21476'}, 'audit_2/AUDIT_MANIFEST.json': {'bytes': 1033, 'sha256': '56ebb21f388aa59805b2aa131fbb531841a3396d6b121d93d67de8db34784abf'}}
AUTHOR = {n.split('author/', 1)[1] for n in ACCEPTED if n.startswith('author/')}
PAYLOAD = set(ACCEPTED) | {'README.md', 'ACCEPTANCE.md', 'verify_publication.py', 'mutation_tests.py'}
FILES = PAYLOAD | {'PUBLICATION_MANIFEST.json', 'BOOTSTRAP.py'}
DIRS = {'author', 'author/public', 'author/external', 'audit_1', 'audit_2'}
AUTHOR_PIN = '31bd2aed10d96d5ada5344531e2207dd4388c8cb1328e3c448ac89be5b78ec8c'


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
    exact_int(value['problem_id'], 2616)
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


def records(value, names, snapshot, prefix):
    need(type(value) is list and len(value) == len(names), 'record inventory size')
    seen = set()
    for row in value:
        keys(row, ['name', 'bytes', 'sha256'])
        name = row['name']
        need(type(name) is str and name in names and name not in seen, 'record path')
        seen.add(name)
        exact_int(row['bytes']); digest(row['sha256'])
        raw = snapshot[prefix+name]
        need(same(row, dict(name=name, bytes=len(raw), sha256=sha(raw))), 'record bytes')
    need(seen == names, 'record exact names')


def archive(raw, snapshot, prefix, names):
    expected_dirs = {'public', 'external'}
    with tarfile.open(fileobj=io.BytesIO(raw), mode='r:gz') as package:
        entries = package.getmembers()
        need(len(entries) == len(names) + len(expected_dirs), 'archive count')
        need(len({e.name for e in entries}) == len(entries), 'duplicate archive path')
        need({e.name for e in entries} == names | expected_dirs, 'archive exact inventory')
        need(not package.pax_headers, 'archive global extensions')
        for entry in entries:
            need(not entry.pax_headers and not entry.linkname, 'archive metadata/link')
            if entry.name in expected_dirs:
                need(entry.isdir() and entry.size == 0, 'archive directory')
            else:
                need(entry.isreg() and entry.size == len(snapshot[prefix+entry.name]), 'archive regular size')
                stream = package.extractfile(entry)
                need(stream is not None and stream.read(1000001) == snapshot[prefix+entry.name], 'archive member bytes')


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
    author_manifest = parsed['author/external/MANIFEST.json']
    keys(author_manifest, ['schema_version', 'files']); exact_int(author_manifest['schema_version'], 1)
    public = {n.split('public/',1)[1] for n in AUTHOR if n.startswith('public/')}
    records(author_manifest['files'], public, snapshot, 'author/public/')
    pins = parsed['author/external/PINS.json']
    keys(pins, ['schema_version', 'public_manifest_sha256', 'external_files'])
    exact_int(pins['schema_version'], 1)
    need(same(pins['public_manifest_sha256'], AUTHOR_PIN), 'author manifest pin')
    external = {n.split('external/',1)[1] for n in AUTHOR if n.startswith('external/')} - {'PINS.json'}
    records(pins['external_files'], external, snapshot, 'author/external/')
    audit = parsed['audit_2/AUDIT_MANIFEST.json']
    keys(audit, ['schema_version', 'problem_id', 'files', 'author_freeze_modified', 'publication_performed', 'source_contents_included', 'verdict'])
    exact_int(audit['schema_version'], 1); exact_int(audit['problem_id'], 2616)
    for key in ['author_freeze_modified', 'publication_performed', 'source_contents_included']:
        need(same(audit[key], False), 'historical audit boundary')
    need(audit['verdict'] == 'ACCEPT_FULL_NEGATIVE_ZFC_PROOF_AND_BOUNDED_REPRODUCIBILITY', 'audit verdict')
    names = {n.split('/',1)[1] for n in ACCEPTED if n.startswith('audit_2/')} - {'AUDIT_MANIFEST.json'}
    records(audit['files'], names, snapshot, 'audit_2/')
    author_snapshot = parsed['audit_2/AUTHOR_SNAPSHOT.json']
    keys(author_snapshot, ['schema_version','problem_id','author_freeze_unchanged','archive','files'])
    exact_int(author_snapshot['schema_version'], 1); exact_int(author_snapshot['problem_id'], 2616)
    need(same(author_snapshot['author_freeze_unchanged'], True), 'author freeze status')
    records(author_snapshot['files'], AUTHOR, snapshot, 'author/')
    raw_archive = snapshot['expansive_group_2616_frozen.tar.gz']
    need(same(author_snapshot['archive'], dict(name='expansive_group_2616_frozen.tar.gz',bytes=len(raw_archive),sha256=sha(raw_archive),archived_bytes_match_frozen_files=True,exact_regular_file_allowlist_verified=True)), 'snapshot archive record')
    archive(raw_archive, snapshot, 'author/', AUTHOR)
    provenance = parsed['author/public/provenance.json']
    need(provenance['status'] == 'FULL_NEGATIVE_PROOF_CANDIDATE_PENDING_INDEPENDENT_AUDIT', 'preserve historical pending status')
    exact_int(provenance['mathematical_approaches'], 1)
    for key in ['source_contents_included','priority_claimed','formal_proof_mechanized','finite_tests_are_proof']:
        need(same(provenance[key], False), 'author scope')
    inventory(root)
    return snapshot, parsed


def replay(snapshot, parsed):
    need(hasattr(os, 'geteuid') and os.getuid() == os.geteuid() != 0, 'real equal nonroot UID/EUID required')
    with tempfile.TemporaryDirectory(prefix='expansive-publication-') as temporary:
        work = Path(temporary)
        for name in sorted(DIRS | {'cwd'}):
            (work/name).mkdir(parents=True, exist_ok=True)
        for name in ACCEPTED:
            (work/name).write_bytes(snapshot[name])
        readonly = [work/name for name in DIRS | {'cwd'}]
        for name in ACCEPTED:
            (work/name).chmod(0o444)
        for directory in readonly:
            directory.chmod(0o555)
        denied = []
        try:
            for path in [work/'author/public/NEW_FILE', work/'author/public/REPORT.md', work/'author/external/NEW_FILE', work/'audit_2/NEW_FILE', work/'cwd/NEW_FILE']:
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
            public, external = str(work/'author/public'), str(work/'author/external')
            author = run('author/external/test_harness.py', [public, external, AUTHOR_PIN])
            expected_author = copy.deepcopy(parsed['author/external/TEST_RESULTS.json'])
            expected_author.update(uid=os.getuid(), euid=os.geteuid(), python_version=sys.version.split()[0])
            need(same(author, expected_author), 'exact author harness receipt changed')
            need(same(parsed['author/external/TEST_RESULTS.json'], parsed['audit_2/AUTHOR_HARNESS_RERUN.json']), 'historical author rerun mismatch')
            independent = run('audit_2/independent_checks.py', [public, external])
            expected_independent = copy.deepcopy(parsed['audit_2/INDEPENDENT_RESULTS.json'])
            expected_independent['python_version'] = sys.version.split()[0]
            expected_independent['independent_execution_controls'].update(uid=os.getuid(), euid=os.geteuid())
            need(same(independent, expected_independent), 'exact independent receipt changed')
            need(not list((work/'cwd').iterdir()), 'child wrote to read-only cwd')
            for name in ACCEPTED:
                need((work/name).read_bytes() == snapshot[name], 'replay mutated accepted evidence')
            return dict(author_finite_checks_per_mode=43533, author_malformed_rejections_per_mode=18,
                        author_tamper_rejections_per_mode=10, independent_finite_checks=192528,
                        independent_malformed_rejections_per_mode=91, internal_modes=['normal','O','OO'],
                        readonly_write_probes_denied=denied, historical_source_bindings='RECORDED_IN_FROZEN_AUDITS',
                        fresh_source_bindings='NOT_RUN', fresh_corpus_bindings='NOT_RUN',
                        infinite_proof_mechanized=False, free_ultrafilter_simulated=False)
        finally:
            for directory in readonly:
                directory.chmod(0o755)
            for name in ACCEPTED:
                (work/name).chmod(0o644)


def main():
    need(len(sys.argv) == 4, 'expected manifest pin, bootstrap pin, packet directory')
    manifest_pin, bootstrap_pin, path = sys.argv[1:]
    root = Path(os.path.abspath(path))
    snapshot, parsed = integrity(root, manifest_pin, bootstrap_pin)
    result = replay(snapshot, parsed)
    after, after_parsed = integrity(root, manifest_pin, bootstrap_pin)
    need(after == snapshot and same(after_parsed, parsed), 'publication changed during replay')
    result.update(schema=1, problem_id=2616, status='PASS', publication_files=len(FILES),
                  optimization=sys.flags.optimize, uid=os.getuid(), euid=os.geteuid(),
                  queue_status='claimed_solved', substantive_turns='1/5',
                  manifest_sha256=manifest_pin, bootstrap_sha256=bootstrap_pin)
    print(json.dumps(result, sort_keys=True, allow_nan=False))


if __name__ == '__main__':
    try:
        main()
    except (ValueError, OSError, TypeError, KeyError, tarfile.TarError, subprocess.TimeoutExpired):
        print('REJECT: publication integrity/replay validation failed', file=sys.stderr)
        sys.exit(1)
