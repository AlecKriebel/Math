#!/usr/bin/env python3
"""Closed portable evidence checks; arithmetic and integrity do not prove analysis."""
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import shutil
import stat
import subprocess
import sys
import tempfile


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def unique(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, 'duplicate JSON key')
        result[key] = value
    return result


def load(path):
    return json.loads(path.read_bytes(), object_pairs_hook=unique)


def bind(root, pin):
    require(stat.S_ISDIR(root.lstat().st_mode), 'regular root directory')
    manifest = root / 'package_index.json'
    require(stat.S_ISREG(manifest.lstat().st_mode), 'regular index')
    require(hashlib.sha256(manifest.read_bytes()).hexdigest() == pin, 'external index pin')
    data = load(manifest)
    require(data['schema'] == 'higher-koszul-characteristic-preprint-v1' and data['problem_id'] == 30003060,
            'package identity')
    names = [row['path'] for row in data['files']]
    require(len(names) == len(set(names)), 'unique inventory')
    require(all(type(n) is str and n == str(PurePosixPath(n)) and n not in ('', '.', 'package_index.json')
                and not n.startswith('/') and '..' not in PurePosixPath(n).parts and '\\' not in n
                for n in names), 'safe paths')
    expected_dirs = {str(p) for n in names for p in PurePosixPath(n).parents if str(p) != '.'}
    files, dirs = set(), set()
    for path in root.rglob('*'):
        mode = path.lstat().st_mode
        name = path.relative_to(root).as_posix()
        if stat.S_ISREG(mode):
            files.add(name)
        elif stat.S_ISDIR(mode):
            dirs.add(name)
        else:
            raise RuntimeError('nonregular member: ' + name)
    require(files == set(names) | {'package_index.json'} and dirs == expected_dirs, 'closed inventory')
    for row in data['files']:
        raw = (root / row['path']).read_bytes()
        require(type(row['bytes']) is int and len(raw) == row['bytes'], 'byte count: ' + row['path'])
        require(hashlib.sha256(raw).hexdigest() == row['sha256'], 'digest: ' + row['path'])
    return len(files)


def full(root):
    flags = ['-I', '-S', '-B'] + (['-O'] if sys.flags.optimize else [])
    with tempfile.TemporaryDirectory(prefix='higher Koszul full replay with spaces ') as td:
        scratch = Path(td).resolve()
        # Historical controls reject macOS /var symlink ancestors. All nested
        # temporary paths inherit one canonical directory outside the package.
        import os
        env = dict(os.environ, TMPDIR=str(scratch), TMP=str(scratch), TEMP=str(scratch))
        def run(script, *args, reject=None):
            result = subprocess.run([sys.executable, *flags, str(script), *map(str,args)],
                                    cwd='/', env=env, capture_output=True, text=True, timeout=900)
            if reject:
                require(result.returncode != 0 and reject in result.stderr,
                        'expected rejection did not occur: ' + str(script))
                return {'expected_rejection': True, 'returncode': result.returncode}
            require(result.returncode == 0 and not result.stderr, str(script) + ': ' + result.stderr)
            return json.loads(result.stdout, object_pairs_hook=unique)
        source = scratch / 'source'
        shutil.copytree(root / 'source', source)
        historical = run(source / 'verify_publication.py', source)
        require(historical['status'] == 'PASS' and historical['archives_verified'] == 4
                and historical['members_verified'] == 55 and len(historical['runs']) == 14,
                'historical archive and replay coverage')
        source_manifest = load(root / 'root_evidence/SOURCE_MANIFEST.json')
        require(source_manifest['frozen_head'] == '286cc67c0727b4decfd4f261a0591cd8823ebce9'
                and len(source_manifest['files']) == 65, 'original identity')
        for row in source_manifest['files']:
            raw = (source / row['path']).read_bytes()
            require(len(raw) == row['bytes'] and hashlib.sha256(raw).hexdigest() == row['sha256'],
                    'source replay changed input')
        algebra = scratch / 'algebra'; algebra.mkdir()
        checker = algebra / 'exact_chain_check.py'
        shutil.copyfile(root / 'algebra_audit_01/exact_chain_check.py', checker)
        output = algebra / 'replayed.json'
        fresh = run(checker, '--output', output)
        actual, expected = load(output), load(root / 'algebra_audit_01/RESULTS.json')
        strip = lambda data: {k:v for k,v in data.items() if k not in {'timestamp_utc','checker_sha256'}}
        require(strip(actual) == strip(expected) and actual['verification_checks_performed'] == 2110
                and actual['matrix_period_comparisons'] == 234 and actual['witness_primes'] == 14
                and actual['negative_controls'] == 10 and actual['all_passed'] is True,
                'fresh exact algebraic controls')
        require(actual['checker_sha256'] == hashlib.sha256(checker.read_bytes()).hexdigest(),
                'fresh checker self-receipt')
        bad_output = algebra / 'bad.json'
        bad = run(checker, '--output', bad_output, '--inject-wrong-expectation', reject='matrix=1, expected=2')
        require(not bad_output.exists(), 'bad expectation wrote acceptance')
        classical = scratch / 'classical'; classical.mkdir()
        operator = classical / 'check_operator_blocks.py'
        shutil.copyfile(root / 'priority_audit_01/classical_lane/check_operator_blocks.py', operator)
        operators = run(operator)
        require((classical / 'OPERATOR_CHECK.json').read_bytes() ==
                (root / 'priority_audit_01/classical_lane/OPERATOR_CHECK.json').read_bytes(),
                'classical operator output changed')
        require(operators['case_count'] == 21 and operators['orbit_blocks_checked'] == 604,
                'classical operator coverage')
        (classical / 'OPERATOR_CHECK.json').unlink()
        text = operator.read_text()
        require(text.count('need(euler_scalar == d,') == 1, 'operator mutation point')
        operator.write_text(text.replace('need(euler_scalar == d,', 'need(euler_scalar == d + 1,', 1))
        bad_operator = run(operator, reject='Euler scalar differs from orbit cardinality')
        require(not (classical / 'OPERATOR_CHECK.json').exists(), 'wrong operator wrote acceptance')
    return {'historical': historical, 'fresh_algebra': fresh,
            'bad_expectation': bad, 'classical_operators': operators,
            'bad_operator': bad_operator, 'unlimited_proof_certified_by_program': False,
            'priority_certified_by_program': False}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('trusted_index_sha256')
    parser.add_argument('--full', action='store_true')
    args = parser.parse_args()
    require(sys.flags.isolated and sys.flags.no_site and sys.flags.dont_write_bytecode, 'run with python -I -S -B')
    root = Path(__file__).absolute().parent
    result = {'status': 'PASS', 'regular_files': bind(root, args.trusted_index_sha256),
              'unlimited_proof_certified_by_program': False, 'priority_verified_by_program': False}
    if args.full:
        result['full'] = full(root)
        bind(root, args.trusted_index_sha256)
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
