#!/usr/bin/env python3
"""Authenticate frozen double-cover partial results; replay source-free finite checks."""
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

ACCEPTED = {'author/APPROACH_LEDGER.json': {'bytes': 2605, 'sha256': 'ce2526362f7f77a299c066f3551085881fc77e78ca23d0110f6c4b1df6dd18a0'}, 'author/MANIFEST.json': {'bytes': 1146, 'sha256': '626c7b5eeea0440efe0f5cc4d05876c973f4561489231bdc292e057396dbebd2'}, 'author/README.md': {'bytes': 2135, 'sha256': '4cc49383295a6016082ab9b648b91874dd70b0c13a80f8d763e8c73276b5534a'}, 'author/REPLAY.json': {'bytes': 405, 'sha256': '1b813aaf6fa512b87524f8dc03cbb1baebec13a7dc7065cd1145ac9366073380'}, 'author/REPORT.md': {'bytes': 25111, 'sha256': 'deb6777556d7fed299d31b2759a5f21cd0a8135d115e5cd542f9d35af775ef94'}, 'author/SOURCE_MANIFEST.json': {'bytes': 9790, 'sha256': 'd6f52a52611efbfe343cc8a24f4a8ee81a53d068acede932a499f10f2e877a5b'}, 'author/verification.json': {'bytes': 2653, 'sha256': '56b9d05d4432070227ef5c53d4c16ba52271dce32d7e504495529d80fcb1176a'}, 'author/verify.py': {'bytes': 11652, 'sha256': '4c9f9a9bc5bae8d2d5ff703ffd003efb6f3085e0042b399da671008c1d428df9'}, 'audit/AUDIT.md': {'bytes': 13506, 'sha256': '99aeaf0a1c63ca6801d81b796d66c41afa23bdc2bf557f822af7b24f8a54980c'}, 'audit/FROZEN_INPUTS.json': {'bytes': 1765, 'sha256': '5ea3dd8587ccba4a86546c83c03dbb136842e632dd915f3bec2ae5a3641f4f83'}, 'audit/MANIFEST.json': {'bytes': 1036, 'sha256': '2349178b577059b8f3c76980046daee11b043a4143c6027903d916f0140bad30'}, 'audit/REPLAY_AUDIT.json': {'bytes': 5690, 'sha256': 'c318c8d6d5356c43ed75a67284efc96bfe27cc9801822972374e163f64b1c5e1'}, 'audit/independent_checks.py': {'bytes': 8453, 'sha256': '5274abe374c1697cadbe5ee95adb5868d48c9378dfa66104bfc857717f857bcb'}, 'audit/independent_results.json': {'bytes': 7555, 'sha256': 'cbee89034fde120b460a14f87dd1c9360af31ba3c9a40d5159cb5d5796d092c2'}, 'audit/replay_audit.py': {'bytes': 5483, 'sha256': '47fbfe951fc32f8ef630c39d08bbb1e0dcc4072b4f9f25e07d95f4f9715ab2f5'}}
AUTHOR = {n.split('/', 1)[1] for n in ACCEPTED if n.startswith('author/')}
AUDIT = {n.split('/', 1)[1] for n in ACCEPTED if n.startswith('audit/')}
PAYLOAD = set(ACCEPTED) | {'README.md', 'ACCEPTANCE.md', 'verify_publication.py', 'mutation_tests.py'}
FILES = PAYLOAD | {'PUBLICATION_MANIFEST.json', 'BOOTSTRAP.py'}
DIRS = {'author', 'audit'}
AUTHOR_PIN = '626c7b5eeea0440efe0f5cc4d05876c973f4561489231bdc292e057396dbebd2'
AUDIT_PIN = '2349178b577059b8f3c76980046daee11b043a4143c6027903d916f0140bad30'


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
    exact_int(value['problem_id'], 2681)
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
        keys(value, ['files', 'includes_third_party_source_documents', 'general_problem_solved'] if prefix == 'author/' else ['files', 'general_problem_solved', 'result', 'schema_version'])
        need(value['general_problem_solved'] is False, 'original unsolved scope')
        if prefix == 'author/':
            need(value['includes_third_party_source_documents'] is False, 'original source boundary')
        else:
            exact_int(value['schema_version'], 1)
            need(value['result'] == 'ACCEPTED_AS_PARTIAL_RESEARCH', 'audit disposition')
        rows = value['files']
        need(type(rows) is list and len(rows) == len(names)-1, 'original file count')
        seen = set()
        for row in rows:
            keys(row, ['path', 'bytes', 'sha256'])
            name = row['path']
            need(type(name) is str and name in names-{'MANIFEST.json'} and name not in seen, 'original member name')
            seen.add(name)
            exact_int(row['bytes']); digest(row['sha256'])
            need(same(row, dict(path=name, bytes=len(snapshot[prefix+name]), sha256=sha(snapshot[prefix+name]))), 'original manifest binding')
        need(seen == names-{'MANIFEST.json'}, 'original exact inventory')
    frozen = parsed['audit/FROZEN_INPUTS.json']
    need(frozen['status'] == 'ACCEPTED_AS_PARTIAL_RESEARCH' and frozen['general_problem_solved'] is False and frozen['correction_patch_required'] is False, 'frozen acceptance disposition')
    exact_int(frozen['mathematical_attempts'], 5)
    need(same(frozen['author_files'], [dict(path=name, **ACCEPTED['author/'+name]) for name in sorted(AUTHOR)]), 'independent author pins')
    inventory(root)
    return snapshot, parsed


def replay(snapshot, parsed):
    need(hasattr(os, 'geteuid') and os.getuid() == os.geteuid() == 1000, 'real UID/EUID 1000 required')
    with tempfile.TemporaryDirectory(prefix='double-cover-publication-') as temporary:
        work = Path(temporary)
        for name in DIRS | {'cwd'}:
            (work/name).mkdir()
        for name in ACCEPTED:
            (work/name).write_bytes(snapshot[name])
        readonly = [work/'author', work/'audit', work/'cwd']
        for directory in readonly:
            for path in directory.iterdir():
                path.chmod(0o444)
            directory.chmod(0o555)
        denied = []
        try:
            for path in [work/'author'/'NEW_FILE', work/'author'/'REPORT.md', work/'audit'/'NEW_FILE', work/'audit'/'AUDIT.md', work/'cwd'/'NEW_FILE']:
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
                return result.stdout, parse(result.stdout)
            author_raw, author = run('author/verify.py', [])
            need(author_raw == snapshot['author/verification.json'], 'author arithmetic bytes changed')
            exact_int(author['positive_controls'], 878)
            exact_int(author['negative_controls'], 3)
            independent_raw, independent = run('audit/independent_checks.py', [])
            need(independent_raw == snapshot['audit/independent_results.json'], 'independent arithmetic bytes changed')
            exact_int(independent['checks'], 1071)
            _, audit = run('audit/replay_audit.py', [str(work/'author')])
            historical = parsed['audit/REPLAY_AUDIT.json']
            # Python version is runtime provenance; every other field is compared
            # with exact types, keys, list order, values and actual UID/EUID.
            need(same({k:v for k,v in audit.items() if k != 'python_version'},
                      {k:v for k,v in historical.items() if k != 'python_version'}), 'native mutation receipt changed')
            need(audit['python_version'] == sys.version.split()[0], 'actual Python version')
            need(not list((work/'cwd').iterdir()), 'child wrote to read-only cwd')
            for name in ACCEPTED:
                need((work/name).read_bytes() == snapshot[name], 'replay mutated accepted evidence')
            return dict(author_positive_controls=878, author_internal_negative_controls=3,
                        author_output_sha256=sha(author_raw), independent_checks=1071,
                        independent_output_sha256=sha(independent_raw), native_mutation_rejections=24,
                        native_controls_own_modes=['normal','-O','-OO'],
                        readonly_write_probes_denied=denied, python_version=sys.version.split()[0],
                        historical_source_bindings='11_PUBLIC_PDF_AND_TEXT_PAIRS_MATCHED_HISTORICALLY',
                        fresh_source_bindings='NOT_RUN', imported_theorem_proofs='NOT_MACHINE_CERTIFIED',
                        knot_signatures='NOT_INDEPENDENTLY_RECOMPUTED', general_problem='UNSOLVED')
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
    result.update(schema=1, problem_id=2681, status='PASS', publication_files=len(FILES),
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
