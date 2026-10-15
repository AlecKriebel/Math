#!/usr/bin/env python3
"""Authenticate the closed PR908 archive and reproduce its finite controls.

An independently authenticated package-manifest SHA-256 anchors the current
archive. Historical bytes are separately pinned. Hashes are consistency
fingerprints, not signatures or mathematical/priority certificates.
"""
import argparse
import hashlib
import importlib.util
import json
import math
import os
from pathlib import Path, PurePosixPath
import re
import shutil
import stat
import subprocess
import sys
import tempfile

HEAD = 'a35667b1bb0bafed69916709997a4684223ecc93'
ORIGINAL_PIN = '828280cc131c38e1f651b48b655dff177f880ba3505bba54e049510d81827795'
PROOF_PIN = '2b7c22cfc54049a9e51fe5eb4eb283ba911e6f27e8b6e4dc9557927bc04d7350'


def require(condition, label):
    if not condition:
        raise RuntimeError(label)


def plain_directory(path):
    require(stat.S_ISDIR(path.lstat().st_mode), 'Nonregular directory: '+str(path))


def check_ancestors(path):
    require('..' not in path.parts, 'Parent traversal in supplied path')
    current = Path(path.anchor)
    for part in path.parts[1:]:
        current /= part
        plain_directory(current)


def read_regular(path):
    before = path.lstat()
    require(stat.S_ISREG(before.st_mode), 'Nonregular file: '+str(path))
    descriptor = os.open(path, os.O_RDONLY | getattr(os, 'O_NOFOLLOW', 0)
                         | getattr(os, 'O_NONBLOCK', 0))
    try:
        during = os.fstat(descriptor)
        require(stat.S_ISREG(during.st_mode) and
                (before.st_dev, before.st_ino) == (during.st_dev, during.st_ino),
                'Path changed while opening: '+str(path))
        with os.fdopen(descriptor, 'rb', closefd=False) as handle:
            data = handle.read()
        after = path.lstat()
        require((before.st_dev, before.st_ino, before.st_size, before.st_mtime_ns)
                == (after.st_dev, after.st_ino, after.st_size, after.st_mtime_ns),
                'Path changed while reading: '+str(path))
        return data
    finally:
        os.close(descriptor)


def strict_json(data):
    def pairs(items):
        result = {}
        for key, value in items:
            require(key not in result, 'Duplicate JSON key')
            result[key] = value
        return result
    def invalid(value):
        raise RuntimeError('Nonfinite JSON constant: '+value)
    return json.loads(data, object_pairs_hook=pairs, parse_constant=invalid)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def inventory(root, records):
    expected_directories = set()
    for name, record in records.items():
        require(type(name) is str and '\\' not in name and '\0' not in name,
                'Invalid payload name')
        q = PurePosixPath(name)
        require(name != '' and not q.is_absolute() and q.as_posix() == name and
                all(x not in ('', '.', '..') for x in q.parts), 'Unsafe payload path')
        require(name != 'PACKAGE_MANIFEST.json', 'Self-listed package manifest')
        require(type(record) is dict and set(record) == {'bytes', 'sha256'} and
                type(record['bytes']) is int and record['bytes'] >= 0 and
                type(record['sha256']) is str and
                re.fullmatch('[0-9a-f]{64}', record['sha256']), 'Invalid payload record')
        expected_directories.update(p.as_posix() for p in q.parents if p.as_posix() != '.')
    files, directories = set(), set()
    def visit(folder):
        plain_directory(folder)
        for child in folder.iterdir():
            name = child.relative_to(root).as_posix()
            mode = child.lstat().st_mode
            if stat.S_ISDIR(mode):
                require(name in expected_directories, 'Unlisted directory: '+name)
                directories.add(name)
                visit(child)
            else:
                require(stat.S_ISREG(mode), 'Symlink or special entry: '+name)
                files.add(name)
    visit(root)
    require(files == set(records) | {'PACKAGE_MANIFEST.json'}, 'Closed file inventory mismatch')
    require(directories == expected_directories, 'Closed directory inventory mismatch')


def validate(root, expected=None, pdf=None):
    check_ancestors(root)
    raw = read_regular(root/'PACKAGE_MANIFEST.json')
    pin = digest(raw)
    if expected is not None:
        require(type(expected) is str and re.fullmatch('[0-9a-f]{64}', expected)
                and pin == expected, 'External package anchor mismatch')
    m = strict_json(raw)
    require(type(m) is dict and set(m) == {'schema_version', 'pr', 'problem_id',
            'original_pr_head', 'original_packet_manifest_sha256', 'scope', 'files'},
            'Invalid package schema')
    require(type(m['schema_version']) is int and m['schema_version'] == 1 and
            type(m['pr']) is int and m['pr'] == 908 and
            type(m['problem_id']) is str and m['problem_id'] == '30006191',
            'Wrong target')
    require(m['original_pr_head'] == HEAD and
            m['original_packet_manifest_sha256'] == ORIGINAL_PIN, 'Wrong original provenance')
    require(type(m['scope']) is str and m['scope'] != '', 'Missing scope')
    records = m['files']
    require(type(records) is dict and records, 'Empty payload inventory')
    inventory(root, records)
    for name, record in records.items():
        data = read_regular(root/name)
        require(len(data) == record['bytes'] and digest(data) == record['sha256'],
                'Payload fingerprint mismatch: '+name)
    require(digest(read_regular(root/'original_packet/PACKAGE_MANIFEST.json')) == ORIGINAL_PIN,
            'Original external package pin mismatch')
    require(digest(read_regular(root/'original_packet/author/BOUNDED_REGION_PROOF.md')) == PROOF_PIN,
            'Original external proof pin mismatch')
    if pdf is not None:
        check_ancestors(pdf.absolute().parent)
        data = read_regular(pdf)
        require({'bytes': len(data), 'sha256': digest(data)} == records['note.pdf'],
                'Separate PDF mismatch')
    return m, pin


def equivalent(actual, expected, path='result'):
    """Separate exact statuses/counts from explicitly tolerated floating values."""
    if type(expected) is bool:
        require(type(actual) is bool and actual == expected, 'Boolean mismatch: '+path)
    elif type(expected) is float:
        require(type(actual) in (int, float) and math.isfinite(actual) and
                math.isclose(actual, expected, rel_tol=1e-9, abs_tol=1e-10),
                'Floating replay mismatch: '+path)
    elif type(expected) is dict:
        require(type(actual) is dict and actual.keys() == expected.keys(), 'Key mismatch: '+path)
        for key in expected:
            equivalent(actual[key], expected[key], path+'/'+key)
    elif type(expected) is list:
        require(type(actual) is list and len(actual) == len(expected), 'List mismatch: '+path)
        for i, item in enumerate(expected):
            equivalent(actual[i], item, path+'/'+str(i))
    else:
        require(type(actual) is type(expected) and actual == expected, 'Exact replay mismatch: '+path)


def clean_environment(work):
    env = dict(os.environ)
    for name in ('PYTHONOPTIMIZE', 'PYTHONPATH', 'PYTHONHOME'):
        env.pop(name, None)
    env.update(PYTHONDONTWRITEBYTECODE='1', TMPDIR=str(work), OPENBLAS_NUM_THREADS='1',
               OMP_NUM_THREADS='1', MKL_NUM_THREADS='1')
    return env


def worker(root, pin, work):
    require(sys.flags.optimize == 0 and sys.flags.isolated == 1,
            'Worker must be isolated and nonoptimized')
    validate(root, pin)
    observations = []
    with tempfile.TemporaryDirectory(dir=work, prefix='pr908_replay_') as td:
        temp = Path(td)
        copied = temp/'package'
        shutil.copytree(root, copied)
        env = clean_environment(temp)
        def run(name, *args):
            proc = subprocess.run([sys.executable, '-I', '-B', str(copied/'run_checked.py'),
                    str(copied/name), *map(str, args)], cwd=temp, env=env,
                    capture_output=True, text=True, timeout=600)
            require(proc.returncode == 0, 'Checker failed: '+name+'\n'+proc.stderr)
            guard = strict_json(proc.stderr.splitlines()[0])
            require(guard.get('execution_guard') == 'PASS' and
                    type(guard.get('child_optimization')) is int and
                    guard['child_optimization'] == 0 and guard.get('child_isolated') == 1,
                    'Child execution guard missing')
            observations.append({'script': name, 'optimization': 0, 'isolated': 1})
            return strict_json(proc.stdout)

        authenticated = run('reviews/computation_family/verify_frozen_packet.py',
                            '--root', copied/'original_packet')
        require(authenticated['status'] == 'PASS' and authenticated['file_count'] == 26,
                'Original packet integrity failed')

        author = run('original_packet/author/verify.py')
        saved = strict_json(read_regular(copied/'original_packet/author/CHECK_RESULTS.json'))
        require('source_bytes' not in author, 'Unexpected fresh source-byte claim')
        saved.pop('source_bytes')
        equivalent(author, saved, 'historical_author')

        a_saved_paths = ['original_packet/audit_a/INDEPENDENT_CHECK_RESULTS.json',
                         'original_packet/audit_a/INDEPENDENT_SUMMARY.json']
        a_bytes = {name: read_regular(copied/name) for name in a_saved_paths}
        audit_a = run('original_packet/audit_a/independent_checks.py', '--proof',
                      copied/'original_packet/author/BOUNDED_REGION_PROOF.md')
        equivalent(audit_a, strict_json(a_bytes[a_saved_paths[1]]), 'historical_audit_a')
        equivalent(strict_json(read_regular(copied/a_saved_paths[0])),
                   strict_json(a_bytes[a_saved_paths[0]]), 'historical_audit_a_details')
        for name, data in a_bytes.items():
            (copied/name).write_bytes(data)

        audit_b = run('original_packet/audit_b/independent_checks.py', '--author-dir',
                      copied/'original_packet/author')
        saved = strict_json(read_regular(copied/'original_packet/audit_b/INDEPENDENT_RESULTS.json'))
        require(audit_b['input_integrity']['source_bytes'] == 'not requested',
                'Unexpected fresh source-byte result')
        require(type(audit_b['python']) is str and audit_b['python'] == sys.version.split()[0],
                'Python version mismatch')
        saved['input_integrity']['source_bytes'] = 'not requested'
        saved['python'] = audit_b['python']
        equivalent(audit_b, saved, 'historical_audit_b')

        localization_path = 'reviews/localization_family/CONTROL_RESULTS.json'
        localization_saved = read_regular(copied/localization_path)
        localization = run('reviews/localization_family/check_controls.py')
        require(localization['all_pass'] is True, 'Localization controls failed')
        equivalent(strict_json(read_regular(copied/localization_path)),
                   strict_json(localization_saved), 'localization')
        (copied/localization_path).write_bytes(localization_saved)

        operator_path = 'reviews/operator_algebra_family/CHECK_RESULTS.json'
        operator_saved = read_regular(copied/operator_path)
        operator = run('reviews/operator_algebra_family/independent_checks.py')
        require(operator['all_pass'] is True and operator['checks_count'] == 148,
                'Operator controls failed')
        equivalent(strict_json(read_regular(copied/operator_path)),
                   strict_json(operator_saved), 'operator_algebra')
        (copied/operator_path).write_bytes(operator_saved)

        independent_output = temp/'math.json'
        mathematical = run('reviews/computation_family/independent_math_checks.py',
                           '--output', independent_output)
        require(mathematical['status'] == 'PASS' and mathematical['exact_predicates'] == 2668
                and mathematical['floating_diagnostics'] == 558, 'Computation counts mismatch')
        actual = strict_json(read_regular(independent_output))
        saved = strict_json(read_regular(copied/'reviews/computation_family/MATH_CHECK_RESULTS.json'))
        require(type(actual['environment']['python']) is str and
                actual['environment']['python'] == sys.version.split()[0], 'Python version mismatch')
        saved['environment']['python'] = actual['environment']['python']
        require(actual['environment'] == saved['environment'],
                'Use the pinned numerical dependency versions for the recorded replay scope')
        equivalent(actual, saved, 'independent_computation')
        validate(copied, pin)
        validate(root, pin)
    return {'status': 'PASS', 'problem_id': '30006191', 'pr': 908,
            'package_manifest_sha256': pin, 'original_files_unchanged': 26,
            'historical_controls': {'author_sector_cases': 4288, 'audit_a_check_calls': 5659,
                'audit_a_integer_predicates': 5000, 'audit_a_symbolic_predicates': 2,
                'audit_a_floating_or_mixed_predicates': 657, 'audit_b_sector_cases': 16768},
            'localization_controls': localization, 'operator_algebra_controls': operator,
            'fresh_exact_predicates': 2668, 'fresh_floating_diagnostics': 558,
            'replay_environment': actual['environment'],
            'child_execution_guards': observations, 'worker_optimization': 0,
            'bool_numeric_type_separation': True, 'source_bytes_retrieved_or_checked': False,
            'historical_float_tolerance': {'relative': 1e-9, 'absolute': 1e-10},
            'scope': 'Reproduced finite controls and byte integrity supplement the written universal proof; no formal-proof, priority, or empirical-physics certificate.'}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--expected-manifest')
    ap.add_argument('--pdf', type=Path)
    ap.add_argument('--integrity-only', action='store_true')
    ap.add_argument('--workdir', type=Path)
    ap.add_argument('--worker', action='store_true', help=argparse.SUPPRESS)
    args = ap.parse_args()
    root = Path(__file__).absolute().parent
    manifest, pin = validate(root, args.expected_manifest, args.pdf)
    if args.integrity_only:
        result = {'status': 'PASS_INTEGRITY', 'pr': 908, 'problem_id': '30006191',
                  'payload_files': len(manifest['files']), 'package_manifest_sha256': pin,
                  'external_anchor_checked': args.expected_manifest is not None}
    else:
        require(args.expected_manifest is not None, 'Full replay requires an external manifest anchor')
        work = (args.workdir or root.parent/('.'+root.name+'-replay-work')).absolute()
        require(work != root and root not in work.parents, 'Work directory lies inside the closed package')
        work.mkdir(parents=True, exist_ok=True)
        check_ancestors(work)
        if args.worker:
            result = worker(root, pin, work)
        else:
            proc = subprocess.run([sys.executable, '-I', '-B', str(root/'verify_package.py'),
                    '--worker', '--expected-manifest', pin, '--workdir', str(work)],
                    cwd=work, env=clean_environment(work), capture_output=True, text=True,
                    timeout=1800)
            require(proc.returncode == 0, 'Isolated replay failed:\n'+proc.stderr)
            result = strict_json(proc.stdout)
            validate(root, pin, args.pdf)
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
