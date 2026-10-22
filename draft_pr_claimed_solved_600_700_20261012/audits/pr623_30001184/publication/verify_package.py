#!/usr/bin/env python3
"""Exact inventory checks and disposable replays; no input files are altered."""
import argparse
import hashlib
import json
import math
from pathlib import Path, PurePosixPath
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parent
MANIFEST = 'PACKAGE_MANIFEST.json'


def require(condition, message):
    if not condition:
        raise ValueError(message)


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, 'duplicate JSON key: ' + key)
        result[key] = value
    return result


def read_json(path):
    return json.loads(path.read_text(), object_pairs_hook=unique_object)


def integrity():
    doc = read_json(ROOT / MANIFEST)
    require(type(doc.get('schema')) is int and doc['schema'] == 1 and
            isinstance(doc.get('files'), list),
            'unsupported inventory schema')
    names, directories = set(), set()
    for entry in doc['files']:
        name = entry['path']
        require(isinstance(name, str), 'path must be a string')
        path = PurePosixPath(name)
        require(str(path) == name and not path.is_absolute() and
                '..' not in path.parts and '\\' not in name and
                name not in names and name != MANIFEST and name != '.',
                'invalid or duplicate path: ' + name)
        require(type(entry['bytes']) is int and entry['bytes'] >= 0,
                'invalid size: ' + name)
        require(isinstance(entry['sha256'], str) and
                len(entry['sha256']) == 64 and
                all(c in '0123456789abcdef' for c in entry['sha256']),
                'invalid hash: ' + name)
        names.add(name)
        directories.update(str(p) for p in path.parents if str(p) != '.')
        data = (ROOT / name).read_bytes()
        require(len(data) == entry['bytes'] and
                hashlib.sha256(data).hexdigest() == entry['sha256'],
                'size or hash mismatch: ' + name)
    actual, actual_directories = set(), set()
    for path in ROOT.rglob('*'):
        require(not path.is_symlink(), 'symlink prohibited')
        relative = path.relative_to(ROOT).as_posix()
        if path.is_file():
            actual.add(relative)
        elif path.is_dir():
            actual_directories.add(relative)
        else:
            raise ValueError('unexpected filesystem entry: ' + relative)
    require(actual == names | {MANIFEST}, 'file inventory mismatch')
    require(actual_directories == directories, 'directory inventory mismatch')
    require(type(doc.get('file_count')) is int and doc['file_count'] == len(names),
            'incorrect file count')
    return doc


def run(script, cwd):
    # -I omits environment optimization settings; no -O is passed to children.
    result = subprocess.run([sys.executable, '-I', str(script)], cwd=cwd,
                            capture_output=True, text=True, check=True)
    return json.loads(result.stdout)


def close_numeric(actual, expected):
    if isinstance(expected, bool) or expected is None:
        return type(actual) is type(expected) and actual == expected
    if isinstance(expected, (float, int)):
        return isinstance(actual, (float, int)) and not isinstance(actual, bool) and \
            math.isfinite(actual) and math.isclose(actual, expected,
                                                 rel_tol=1e-10, abs_tol=1e-11)
    if isinstance(expected, dict):
        return isinstance(actual, dict) and actual.keys() == expected.keys() and \
            all(close_numeric(actual[k], v) for k, v in expected.items())
    if isinstance(expected, list):
        return isinstance(actual, list) and len(actual) == len(expected) and \
            all(close_numeric(a, b) for a, b in zip(actual, expected))
    return type(actual) is type(expected) and actual == expected


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--integrity-only', action='store_true')
    args = parser.parse_args()
    doc = integrity()
    output = {'integrity': 'PASS', 'manifested_files': doc['file_count']}
    if not args.integrity_only:
        import sympy
        require(sympy.__version__ == '1.14.0', 'install pinned requirements.txt')
        with tempfile.TemporaryDirectory(prefix='gns-replay-') as temporary:
            root = Path(temporary) / 'packet'
            shutil.copytree(ROOT, root)
            candidate = root / 'candidate'
            result = run(candidate / 'verify_publication.py', candidate)
            require(result['integrity'] == 'PASS' and result['byte_identical_replays'],
                    'frozen candidate replay failed')
            require(result == read_json(root / 'chronology_and_reproduction/ROOT_ORIGINAL_REPLAY.json'),
                    'frozen candidate output differs')
            output['frozen_candidate'] = result
            controls = run(candidate / 'test_integrity.py', candidate)
            require(controls['result'] == 'PASS' and controls['negative_cases'] == 12,
                    'original negative integrity controls failed')
            output['negative_integrity_controls'] = 'PASS_NORMAL_AND_OPTIMIZED'
            operator = root / 'reviews/operator_01'
            result = run(operator / 'exact_operator_check.py', operator)
            require(result == read_json(operator / 'EXACT_RESULTS.json'),
                    'fresh operator output differs')
            output['operator_exact_assertions'] = result['exact_assertions']
            scope = root / 'reviews/scope_01'
            result = run(scope / 'check_scope.py', scope)
            require(result['status'] == 'all_assertions_passed' and
                    close_numeric(result, read_json(scope / 'CHECK_RESULTS.json')),
                    'scope numerical sanity checks differ beyond tolerance')
            output['scope_sanity_checks'] = 'PASS_WITH_DECLARED_NUMERICAL_TOLERANCE'
            priority = root / 'reviews/priority_01'
            expected = read_json(priority / 'PRIOR_IMPLICATION_CHECK.json')
            result = run(priority / 'verify_prior_implication.py', priority)
            require(result == expected and read_json(priority / 'PRIOR_IMPLICATION_CHECK.json') == expected,
                    'prior implication symbolic output differs')
            output['priority_symbolic_assertions'] = result['assertions']
            classical = root / 'reviews/classical_implication_01'
            expected = read_json(classical / 'EXACT_COMPRESSION_RESULTS.json')
            run(classical / 'exact_compression_check.py', classical)
            require(read_json(classical / 'EXACT_COMPRESSION_RESULTS.json') == expected,
                    'independent classical exact output differs')
            output['independent_classical_exact_controls'] = len(expected['checks'])
        integrity()
        output['original_packet_unmodified'] = 'PASS'
        output['meaning'] = 'Finite diagnostics supplement the written universal analytic proof.'
    print(json.dumps(output, indent=2))


if __name__ == '__main__':
    main()
