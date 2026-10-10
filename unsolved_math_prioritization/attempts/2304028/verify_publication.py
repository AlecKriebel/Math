#!/usr/bin/env python3
"""Externally pinned, fixed-input integrity and finite replay; no universal proof."""
import sys
if not (sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode):
    raise SystemExit('REJECT: use python -I -S -B [ -O | -OO ]')
import hashlib
import json
import math
import os
from pathlib import Path
import re
import stat
import subprocess
import tempfile

AUTHOR = {'REPORT.md', 'SOURCE_METADATA.json', 'cases.json', 'verify.py'}
AUDIT = {'MATHEMATICAL_AUDIT.md', 'INDEPENDENT_VERIFICATION.json'}
FILES = {'author/'+x for x in AUTHOR} | {'audit/'+x for x in AUDIT} | {
    'FREEZE.json', 'EXTERNAL_HASHES.json', 'ORIGINAL_PUBLIC_ALLOWLIST.json',
    'README.md', 'ACCEPTANCE.md', 'verify_publication.py', 'mutation_tests.py'}
DIRS = {'author', 'audit'}
# Populated from independently accepted evidence, not from a supplied manifest.
ACCEPTED = {'FREEZE.json': {'bytes': 631, 'sha256': 'b76dfab10d985100f7dc23854491ee83dddd6364a1eb8dee2fb7dc5ceeb22000'}, 'ORIGINAL_PUBLIC_ALLOWLIST.json': {'bytes': 2093, 'sha256': '9a41bb29846f2e5d46f5ed58a605cd6cd45202e6b3e56b35cf516d750f578116'}, 'EXTERNAL_HASHES.json': {'bytes': 1398, 'sha256': '490b3d6795ea29d5abc3d076a96c75b7eaf9766a950fd2c806b15602a75b8b85'}, 'author/REPORT.md': {'bytes': 8230, 'sha256': '67b28d2bef4ade9f5badcf80551dd334c490d73d5054f70ff001a88dd35ea540'}, 'author/verify.py': {'bytes': 9420, 'sha256': 'c665a143651efce5532f41d55db02471f1c4b1e0e7146477a87ad36f2369a58c'}, 'author/SOURCE_METADATA.json': {'bytes': 3139, 'sha256': '33c55ad7772f852cdeb5e343c3717262ae2f9827e99a43b0b9357ed780e5c3e9'}, 'author/cases.json': {'bytes': 9131, 'sha256': '5b75514f7123069c78d1251ac23f6043bca1aa19165236fc3a833e44e93babb9'}, 'audit/MATHEMATICAL_AUDIT.md': {'bytes': 17205, 'sha256': '3304db8d5c80a30fcad63bf283b3c4d23cd6715e0ef97c179d2c5ce14826bdf8'}, 'audit/INDEPENDENT_VERIFICATION.json': {'bytes': 58554, 'sha256': '840ea897f30073370be7c0f35d80a157f11ddf50c16072ea11029edf71a9d441'}}


def need(ok, message):
    if not ok:
        raise ValueError(message)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def same(actual, expected):
    """Recursive exact-type equality: True is never equal to 1 or 1.0 here."""
    if type(actual) is not type(expected):
        return False
    if type(expected) is dict:
        return set(actual) == set(expected) and all(same(actual[k], v) for k, v in expected.items())
    if type(expected) is list:
        return len(actual) == len(expected) and all(same(a, b) for a, b in zip(actual, expected))
    return actual == expected


def pairs(items):
    result = {}
    for key, value in items:
        need(key not in result, 'duplicate JSON key')
        result[key] = value
    return result


def nonfinite(value):
    raise ValueError('nonfinite JSON number')


def finite_float(value):
    number = float(value)
    need(math.isfinite(number), 'overflowed JSON float')
    return number


def parse(raw):
    return json.loads(raw, object_pairs_hook=pairs, parse_constant=nonfinite,
                      parse_float=finite_float)


def keys(obj, names):
    need(type(obj) is dict and set(obj) == set(names), 'exact object schema')


def integer(value, low, high):
    need(type(value) is int and low <= value <= high, 'exact bounded integer')


def digest_string(value):
    need(type(value) is str and re.fullmatch('[0-9a-f]{64}', value) is not None,
         'exact SHA-256 string')


def ordinary_root(root):
    for p in (root, *root.parents):
        need(stat.S_ISDIR(p.lstat().st_mode), 'linked or nondirectory ancestor')


def inventory(root):
    ordinary_root(root)
    files, dirs = set(), set()
    def visit(directory):
        for item in os.scandir(directory):
            p = Path(item.path)
            name = p.relative_to(root).as_posix()
            mode = item.stat(follow_symlinks=False).st_mode
            if stat.S_ISDIR(mode):
                need(name in DIRS, 'unlisted directory')
                dirs.add(name)
                visit(p)
            else:
                need(stat.S_ISREG(mode), 'linked or special entry')
                files.add(name)
    visit(root)
    need(files == FILES | {'PUBLIC_MANIFEST.json'} and dirs == DIRS,
         'exact packet inventory')


def file_rows(rows, expected_names, snapshot, prefix=''):
    need(type(rows) is list and len(rows) == len(expected_names), 'file list size/type')
    seen = set()
    for row in rows:
        keys(row, ['path', 'bytes', 'sha256'])
        name = row['path']
        need(type(name) is str and name in expected_names and name not in seen,
             'unknown or duplicate file path')
        seen.add(name)
        integer(row['bytes'], 1, 1000000)
        digest_string(row['sha256'])
        raw = snapshot[prefix+name]
        need(len(raw) == row['bytes'] and sha(raw) == row['sha256'], 'file hash/size mismatch')
    need(seen == expected_names, 'file inventory mismatch')


def integrity(root, pin):
    digest_string(pin)
    inventory(root)
    raw = (root/'PUBLIC_MANIFEST.json').read_bytes()
    need(sha(raw) == pin, 'external manifest pin mismatch')
    manifest = parse(raw)
    keys(manifest, ['schema_version', 'problem_id', 'files'])
    integer(manifest['schema_version'], 1, 1)
    integer(manifest['problem_id'], 2304028, 2304028)
    snapshot = {name: (root/name).read_bytes() for name in FILES}
    file_rows(manifest['files'], FILES, snapshot)
    for name, entry in ACCEPTED.items():
        need(len(snapshot[name]) == entry['bytes'] and sha(snapshot[name]) == entry['sha256'],
             'accepted evidence changed: '+name)
    parsed = {name: parse(data) for name, data in snapshot.items() if name.endswith('.json')}
    freeze = parsed['FREEZE.json']
    keys(freeze, ['schema_version', 'files'])
    integer(freeze['schema_version'], 1, 1)
    file_rows(freeze['files'], AUTHOR, snapshot, 'author/')
    external = parsed['EXTERNAL_HASHES.json']
    keys(external, ['schema_version', 'problem_identifier', 'recorded_date_utc',
                   'candidate_external_manifest', 'candidate_public_files',
                   'independent_audit_public_files', 'source_artifact_bytes_redistributed', 'pin_origin'])
    integer(external['schema_version'], 1, 1)
    need(same(external['source_artifact_bytes_redistributed'], False), 'source publication flag')
    file_rows(external['candidate_public_files'], AUTHOR, snapshot, 'author/')
    file_rows(external['independent_audit_public_files'], AUDIT, snapshot, 'audit/')
    need(same(external['candidate_external_manifest'],
              dict(path='FREEZE.json', **ACCEPTED['FREEZE.json'])), 'nested external pin')
    allowed = parsed['ORIGINAL_PUBLIC_ALLOWLIST.json']
    need(same(allowed['candidate_public_files'], external['candidate_public_files']) and
         same(allowed['independent_audit_public_files'], external['independent_audit_public_files']),
         'original public allowlist mismatch')
    need(same(allowed['publication_performed'], False), 'historical allowlist flag')
    historic = parsed['audit/INDEPENDENT_VERIFICATION.json']
    for key, value in [('schema_version', 1), ('rank', 1033), ('new_proof_search_approaches', 0),
                       ('decision', 'ACCEPT / KNOWN-SOLVED'), ('required_correction_patch', None),
                       ('original_payload_bytes', 29920), ('publication_performed', False),
                       ('queue_changed', False), ('authors_contacted', False)]:
        need(same(historic[key], value), 'historical exact-type field: '+key)
    need(same(historic['original_payload'], freeze), 'historical payload record')
    r = historic['reviewer_replay']
    for key, value in [('original_positive_runs', 3), ('original_negative_runs', 72),
                       ('additional_positive_runs', 6), ('additional_negative_runs', 126),
                       ('all_expected_outcomes', True)]:
        need(same(r[key], value), 'historical replay field: '+key)
    return snapshot


def denied(path, mode):
    try:
        with path.open(mode):
            pass
    except PermissionError:
        return True
    return False


def replay(snapshot):
    need(os.getuid() == os.geteuid() != 0, 'actual equal nonroot UID/EUID required')
    with tempfile.TemporaryDirectory(prefix='polynomial-publication-') as td:
        work = Path(td)
        payload = work/'author'
        payload.mkdir()
        for name in AUTHOR:
            (payload/name).write_bytes(snapshot['author/'+name])
        manifest = work/'FREEZE.json'
        manifest.write_bytes(snapshot['FREEZE.json'])
        hostile = work/'hostile'
        hostile.mkdir()
        for name in ['json', 'fractions', 'hashlib', 'pathlib', 'argparse', 'sitecustomize', 'usercustomize']:
            (hostile/(name+'.py')).write_text("raise RuntimeError('HOSTILE IMPORT')\n")
        try:
            for p in [*payload.iterdir(), *hostile.iterdir(), manifest]:
                p.chmod(0o444)
            payload.chmod(0o555)
            hostile.chmod(0o555)
            probes = [denied(payload/'new', 'w'), denied(payload/'cases.json', 'a'),
                      denied(manifest, 'a'), denied(hostile/'new', 'w')]
            need(all(probes), 'read-only write probes not denied')
            env = dict(os.environ, PYTHONPATH=str(hostile), PYTHONHOME='/nonexistent-python-home',
                       PYTHONSTARTUP=str(hostile/'sitecustomize.py'), PYTHONINSPECT='1', PYTHONOPTIMIZE='2')
            cmd = [sys.executable, '-I', '-S', '-B', *(['-O']*sys.flags.optimize),
                   str(payload/'verify.py'), '--root', str(payload), '--manifest', str(manifest),
                   '--expected-sha256', ACCEPTED['FREEZE.json']['sha256']]
            result = subprocess.run(cmd, cwd=hostile, env=env, capture_output=True, timeout=45)
            need(result.returncode == 0, 'author replay failed')
            expected = dict(status='PASS', uid=os.geteuid(), finite_cases=24, negative_type_controls=25,
                            universal_proof_checked_by_code=False, literature_classification='KNOWN-SOLVED')
            need(same(parse(result.stdout), expected), 'complete typed replay receipt')
            need(result.stderr == b'', 'unexpected replay stderr')
            need({p.name for p in payload.iterdir()} == AUTHOR, 'replay generated files')
            for name in AUTHOR:
                need((payload/name).read_bytes() == snapshot['author/'+name], 'replay changed snapshot')
            return dict(validator_receipt=expected, readonly_write_probes_denied=4)
        finally:
            payload.chmod(0o755)
            hostile.chmod(0o755)


def main():
    need(len(sys.argv) == 3, 'expected external manifest pin and packet path')
    pin, path = sys.argv[1:]
    root = Path(os.path.abspath(path))
    snapshot = integrity(root, pin)
    result = replay(snapshot)
    need(integrity(root, pin) == snapshot, 'input changed during replay')
    result.update(schema_version=1, problem_id=2304028, status='PASS',
                  optimization=sys.flags.optimize, uid=os.getuid(), euid=os.geteuid(),
                  manifest_sha256=pin, verified_payload_files=len(FILES),
                  source_checks='NOT_RUN', corpus_checks='NOT_RUN',
                  historical_sympy_reconstruction='NOT_RUN', universal_proof_by_code=False)
    print(json.dumps(result, sort_keys=True))


if __name__ == '__main__':
    try:
        main()
    except (ValueError, OSError, KeyError, TypeError, subprocess.TimeoutExpired) as exc:
        print('REJECT: '+str(exc), file=sys.stderr)
        sys.exit(1)
