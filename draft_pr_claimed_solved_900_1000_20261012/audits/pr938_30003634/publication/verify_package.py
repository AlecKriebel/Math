#!/usr/bin/env python3
"""Authenticate the closed PR938 archive and reproduce its finite controls.

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

HEAD = '2b3ea2de7a9a9ea4fa8cba9a34cbdb01063bda3b'
ORIGINAL_PIN = '149e6144f0ad90ee12945c29155318100b65c6faee8ba2661d2c09db58b9ae30'
PROOF_PIN = '0492e0e0de785be263174e86d69855120b2f5c24b105c6479739cd72d64abe3b'


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
            type(m['pr']) is int and m['pr'] == 938 and
            type(m['problem_id']) is str and m['problem_id'] == '30003634',
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
    require(digest(read_regular(root/'original_packet/PUBLICATION_MANIFEST.json')) == ORIGINAL_PIN,
            'Original external package pin mismatch')
    require(digest(read_regular(root/'original_packet/original/PROOF.md')) == PROOF_PIN,
            'Original external proof pin mismatch')
    if pdf is not None:
        check_ancestors(pdf.absolute().parent)
        data = read_regular(pdf)
        require({'bytes': len(data), 'sha256': digest(data)} == records['note.pdf'],
                'Separate PDF mismatch')
    return m, pin


def equivalent(actual, expected, path='result'):
    """Compare replay JSON including exact scalar types; no numeric tolerance."""
    require(type(actual) is type(expected), 'Type mismatch: '+path)
    if type(expected) is dict:
        require(actual.keys() == expected.keys(), 'Key mismatch: '+path)
        for key in expected:
            equivalent(actual[key], expected[key], path+'/'+key)
    elif type(expected) is list:
        require(len(actual) == len(expected), 'List length mismatch: '+path)
        for i, item in enumerate(expected):
            equivalent(actual[i], item, path+'/'+str(i))
    else:
        require(actual == expected, 'Value mismatch: '+path)


def clean_environment(work):
    env = dict(os.environ)
    for name in list(env):
        if name.startswith('PYTHON'):
            env.pop(name, None)
    env.update(PYTHONDONTWRITEBYTECODE='1', TMPDIR=str(work), OPENBLAS_NUM_THREADS='1',
               OMP_NUM_THREADS='1', MKL_NUM_THREADS='1')
    return env


def worker(root, pin, work):
    require(sys.flags.optimize == 0 and sys.flags.isolated == 1,
            'Worker must be isolated and nonoptimized')
    validate(root, pin)
    observations = []
    with tempfile.TemporaryDirectory(dir=work, prefix='pr938_replay_') as td:
        temp = Path(td)
        copied = temp/'package'
        shutil.copytree(root, copied)
        # Authenticate the actual disposable bytes before executing any of them.
        # Source validation alone does not establish the identity of a copy.
        validate(copied, pin)
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

        author = run('original_packet/original/verify.py')
        author_expected = {'status': 'PASS_EXACT_CERTIFICATE', 'problem_id': 30003634,
                'n': 1, 'm': 3, 'derived_level': 3, 'word_length': 104,
                'goeritz_dimension': 48, 'goeritz_inertia': [23,25,0],
                'signature': -2, 'additional_controls': 286,
                'scope': 'Finite certificate replay; topology theorem and source hypotheses require mathematical review.'}
        equivalent(author, author_expected, 'original_author')
        controls = {}
        for family,script in [('goeritz_family','independent_goeritz.py'),
                              ('meyer_algebra_family','reproduce.py')]:
            name = 'reviews/'+family+'/'+script
            actual = run(name)
            saved = strict_json(read_regular(copied/'reviews'/family/'INDEPENDENT_RESULTS.json'))
            actual.pop('utc',None); saved.pop('utc',None)
            if family == 'goeritz_family':
                actual.pop('python_optimization',None); saved.pop('python_optimization',None)
                require(actual['link_signature'] == -2 and actual['inertia'] == [23,25,0],
                        'Planar signature reconstruction failed')
            else:
                require(actual['signature'] == -2 and actual['term_count'] == 104,
                        'Meyer signature reconstruction failed')
            equivalent(actual, saved, name)
            controls[family] = {'status':'PASS_EXACT_JSON','script':script,
                               'omitted_descriptive_keys':['utc'] + (['python_optimization'] if family == 'goeritz_family' else [])}
        validate(copied, pin)
        validate(root, pin)
    return {'status': 'PASS', 'problem_id': '30003634', 'pr': 938,
            'package_manifest_sha256': pin, 'original_files_unchanged': 44,
            'original_certificate': author, 'independent_controls': controls,
            'child_execution_guards': observations, 'worker_optimization': 0,
            'exact_json_type_comparison': True, 'floating_tolerance_used': False,
            'source_bytes_retrieved_or_checked': False,
            'scope': 'Finite exact original certificate and independent full planar/Meyer reconstructions; all-depth topology/group proof and priority are not certified by these computations. Historical SymPy-based recovery and full transport suites are preserved with their recorded root replays, not rerun by this standard-library release entry point.'}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--expected-manifest')
    ap.add_argument('--pdf', type=Path)
    ap.add_argument('--integrity-only', action='store_true')
    ap.add_argument('--workdir', type=Path)
    ap.add_argument('--worker', action='store_true', help=argparse.SUPPRESS)
    args = ap.parse_args()
    require(os.name == 'posix' and hasattr(os, 'O_NOFOLLOW'), 'POSIX O_NOFOLLOW required')
    raw_script = __file__
    require(os.path.isabs(raw_script) and all(x not in ('', '.', '..')
            for x in raw_script.split('/')[1:]) and raw_script == os.path.realpath(raw_script),
            'Verifier path must be canonical and absolute')
    root = Path(raw_script).parent
    manifest, pin = validate(root, args.expected_manifest, args.pdf)
    if args.integrity_only:
        result = {'status': 'PASS_INTEGRITY', 'pr': 938, 'problem_id': '30003634',
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
