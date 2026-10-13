#!/usr/bin/env python3
"""Supported read-only finite verifier for PR445 / 30002737.

The trusted input is this reviewed verify.py and its literal pins. Untrusted
fixtures cannot acquire authority by resealing a manifest. Historical scripts
are checked as bytes/history and NEVER executed or imported. All controlling
checks use explicit exceptions under normal Python and inherited optimization.
"""
from pathlib import Path, PurePosixPath
from fractions import Fraction as F
from itertools import product
import argparse
import hashlib
import json
import os
import sys
import types

HERE = Path(__file__).resolve().parent
HEAD = '3242c84e06db7e99012c7fe581adde5c3f89fc89'
SOURCE_MANIFEST_SHA256 = 'e68e9b9338723c3c1c4a1ab8022d1bb6b04ea03a4d8f5d3dd9abbbd3b072a347'
CONTROL_PINS = {
    'controls_exact.py': '83db2ecfa12dc2f28109b1ec4008c91bfa88f28c4748e23f075ce7fc01ccf581',
    'controls_deterministic.py': '849cfc6ea241317dc5bec94bdcf4af3edbf00b3432fcd2f8f81a08a1ee22ef5e',
}


class VerificationFailure(ValueError):
    pass


def require(condition, message):
    if not condition:
        raise VerificationFailure(message)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def read_json(data, label):
    try:
        # Reject duplicate keys: a resealed JSON object may not hide identities.
        def unique_pairs(pairs):
            answer = {}
            for key, value in pairs:
                require(key not in answer, f'Duplicate JSON key in {label}: {key}')
                answer[key] = value
            return answer
        return json.loads(data, object_pairs_hook=unique_pairs)
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise VerificationFailure(f'Invalid JSON in {label}: {error}') from error


def safe_path(path):
    require(isinstance(path, str), 'Source path must be text')
    pure = PurePosixPath(path)
    require(not pure.is_absolute() and pure.as_posix() == path and
            all(c not in ('', '.', '..') for c in pure.parts), 'Unsafe source path: '+path)
    return pure


def integrity(inputs):
    require(not inputs.is_symlink(), 'Inputs root is a symlink')
    manifest_path = inputs/'SOURCE_MANIFEST.json'
    require(manifest_path.is_file() and not manifest_path.is_symlink(), 'Canonical source manifest missing/unsafe')
    raw = manifest_path.read_bytes()
    require(digest(raw) == SOURCE_MANIFEST_SHA256, 'Canonical source manifest literal hash mismatch')
    manifest = read_json(raw, 'SOURCE_MANIFEST.json')
    require(manifest['pr'] == 445 and manifest['problem_id'] == 30002737 and
            manifest['frozen_head'] == HEAD, 'Frozen source identity mismatch')
    require(manifest['historical_status'] == 'claimed_solved' and
            manifest['author_attempt_count'] == '1/5' and manifest['DOI_columns'] == 'blank',
            'Frozen scope identity mismatch')
    require(manifest['original_file_count'] == 12 and len(manifest['files']) == 12,
            'Frozen source count mismatch')
    root = inputs/'frozen_history'
    require(root.is_dir() and not root.is_symlink(), 'Frozen history root missing/unsafe')
    paths = []
    for item in manifest['files']:
        safe_path(item['path'])
        paths.append(item['path'])
    require(len(set(paths)) == 12, 'Repeated source path')
    actual = []
    for path in root.rglob('*'):
        require(not path.is_symlink(), 'Frozen history contains a symlink: '+str(path))
        if path.is_file():
            actual.append(path.relative_to(root).as_posix())
        else:
            require(path.is_dir(), 'Frozen history contains nonregular entry: '+str(path))
    require(set(actual) == set(paths), 'Frozen source exact file inventory mismatch')
    blobs, records = {}, []
    for item in manifest['files']:
        path = root/item['path']
        data = path.read_bytes()
        require(len(data) == item['bytes'], 'Frozen source byte length mismatch: '+item['path'])
        require(digest(data) == item['sha256'], 'Frozen source hash mismatch: '+item['path'])
        blobs[item['path']] = data
        records.append(dict(item))
    meta = {x['path']: x for x in manifest['files']}
    author = read_json(blobs['author/MANIFEST.json'], 'author/MANIFEST.json')
    require(set(author['files']) == {'attempts/turn_01.md', 'checks/verify_counterexample.py',
                                   'checks/verification_results.json'}, 'Historical author manifest paths differ')
    for name, row in author['files'].items():
        expected = meta['author/'+name]
        require(row == {'sha256': expected['sha256'], 'bytes': expected['bytes']},
                'Historical author manifest metadata differs: '+name)
    release = read_json(blobs['RELEASE_MANIFEST.json'], 'RELEASE_MANIFEST.json')
    require(release['problem_id'] == 30002737 and release['status'] == 'claimed_solved' and
            release['turns'] == '1/5', 'Historical release identity differs')
    release_paths = [r['path'] for r in release['files']]
    require(len(release_paths) == 11 and len(set(release_paths)) == 11 and
            set(release_paths) == set(paths)-{'RELEASE_MANIFEST.json'},
            'Historical release manifest inventory differs')
    for row in release['files']:
        require(row == meta[row['path']], 'Historical release manifest metadata differs: '+row['path'])
    return blobs, records, meta


def load_controls():
    modules = []
    for filename, expected in CONTROL_PINS.items():
        path = HERE/filename
        require(path.is_file() and not path.is_symlink(), 'Supported control missing/unsafe: '+filename)
        data = path.read_bytes()
        require(digest(data) == expected, 'Supported control literal hash mismatch: '+filename)
        module = types.ModuleType(filename.removesuffix('.py'))
        module.__file__ = str(path)
        # Compile the same checked bytes; no cached or PYTHONPATH module is loaded.
        exec(compile(data, str(path), 'exec', optimize=sys.flags.optimize), module.__dict__)
        modules.append(module)
    return modules


def author_finite_result(exact, deterministic, checker_hash):
    mean = [F(1), F(1), F(1, 2), F(1, 2)]
    pair_checks = weighted_checks = flow_checks = 0
    for m, n in product(range(-4, 5), repeat=2):
        for c, d in product(range(4), repeat=2):
            actual = exact.expectation(exact.mul(exact.occupancy(c, 0, 0), exact.occupancy(d, m, n)))
            target = mean[c]*mean[d] + F(1, 4)*int(c == d == 2 and m == 0) + F(1, 4)*int(c == d == 3 and n == 0)
            require(actual == target, 'Original-range motif moment check differs')
            pair_checks += 1
        actual = exact.expectation(exact.mul(exact.weighted(0, 0), exact.weighted(m, n)))
        require(actual == 16+int(m == 0)+4*int(n == 0), 'Original-range weighted moment check differs')
        weighted_checks += 1
    require({4+x+2*y for x, y in product((-1, 1), repeat=2)} == {1, 3, 5, 7},
            'Weighted sign encoding differs')
    for q in range(1, 18):
        for p in range(-3*q, 3*q+1):
            t = F(p, q)
            direct = deterministic.section_integral(t)
            overlap = max(F(0), min(F(1), 1-t)-max(F(0), -t))
            require(direct == overlap == max(F(0), 1-abs(t)), 'Original-range exact overlap differs')
            flow_checks += 1
    return {'status': 'pass', 'arithmetic': 'exact rational, Python standard library',
            'marker_pairs': [[0, 1]], 'motif_pair_checks': pair_checks,
            'weighted_correlation_checks': weighted_checks, 'suspension_overlap_checks': flow_checks,
            'density': '3', 'autocorrelation_mass_at_zero': '3', 'bragg_intensity_at_zero': '9',
            'scope': 'finite algebra and marker checks only; not an independent proof of the infinite-system theorem',
            'checker_sha256': checker_hash}


def saved_result_validation(blobs, meta, author_fresh, deterministic_result, mutant=None):
    saved_author = read_json(blobs['author/checks/verification_results.json'], 'historical author saved result')
    if mutant == 'saved_author_semantic':
        saved_author['density'] = '300'
    require(saved_author == author_fresh, 'Saved author result semantic mismatch')
    saved_independent = read_json(blobs['audit/independent_controls_results.json'], 'historical independent saved result')
    if mutant == 'saved_independent_semantic':
        saved_independent['physical_point_count_controls'][0]['point_count'] += 1
    expected = {'verdict': 'PASS',
                'frozen_hashes': {p.removeprefix('author/'): meta[p]['sha256'] for p in
                                 ['author/attempts/turn_01.md', 'author/checks/verify_counterexample.py',
                                  'author/checks/verification_results.json']},
                **{k: deterministic_result[k] for k in ['rho_primitive_depth', 'rho_vs_bit_formula_sites',
                     'bilateral_source_recursion_sites', 'rs_finite_samples', 'physical_point_count_controls',
                     'exhaustive_local_marker_cases', 'bad_marker_negative_control', 'exact_flow_section_checks']},
                'frozen_checker_isolated_replay': 'identical results; frozen sources unchanged',
                'limitations': 'Finite tests are diagnostics; the infinite conclusions are proved analytically in independent_audit.md.'}
    require(saved_independent == expected, 'Saved independent result semantic mismatch')
    return {'author_result': 'all fields agree with newly evaluated guarded finite controls and frozen checker hash',
            'independent_result': 'finite fields agree with fresh deterministic controls; complete historical JSON identity checked',
            'historical_replay_sentence': 'retained and checked as historical text only; original assertion scripts not executed',
            'saved_result_files_checked': 2}


def verify(inputs, mutant=None):
    require(sys.version_info >= (3, 10), 'Python 3.10 or later required')
    blobs, source_records, meta = integrity(inputs)
    exact, deterministic = load_controls()
    exact_mutant = {'correlation': 'moments'}.get(mutant, mutant)
    e = exact.run_checks(exact_mutant if exact_mutant in ['marker', 'moments', 'normalization', 'flow', 'cocycle'] else None)
    d = deterministic.run_checks(mutant if mutant in ['rs', 'physical_pairs', 'subdivision'] else None)
    author = author_finite_result(exact, deterministic, meta['author/checks/verify_counterexample.py']['sha256'])
    saved = saved_result_validation(blobs, meta, author, d, mutant)
    after, after_records, _ = integrity(inputs)
    require(blobs == after and source_records == after_records, 'Frozen history changed during verification')
    return {'status': 'PASS', 'pr': 445, 'problem_id': 30002737, 'frozen_head': HEAD,
            'verifier': '/root/pr445_verification_repair',
            'interface_scope': 'Supported fresh finite controls plus frozen history integrity; no historical assertion script replay',
            'original_scripts_safe_under_optimization': False,
            'fresh_exact_controls': e, 'fresh_deterministic_controls': d,
            'historical_author_finite_fields_recomputed': author, 'saved_results': saved,
            'source_files_verified': source_records,
            'literal_source_manifest_sha256': SOURCE_MANIFEST_SHA256,
            'literal_supported_control_sha256': CONTROL_PINS,
            'runtime': {'executable': sys.executable, 'version': sys.version,
                        'optimization': sys.flags.optimize, 'inherited_PYTHONOPTIMIZE': os.environ.get('PYTHONOPTIMIZE')},
            'scope_limits': 'Finite controls do not prove infinite RS correlations, hull ergodicity, novelty, priority or a one-dimensional result'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--inputs', type=Path, default=HERE,
                        help='Package containing SOURCE_MANIFEST.json and frozen_history; always checked against literal trusted pins')
    parser.add_argument('--diagnostic-fault', choices=['marker', 'correlation', 'normalization', 'flow', 'cocycle',
                        'rs', 'physical_pairs', 'subdivision', 'saved_author_semantic', 'saved_independent_semantic'],
                        help='Deliberately incorrect mathematical/result variant; must reject before PASS')
    args = parser.parse_args()
    try:
        result = verify(args.inputs, args.diagnostic_fault)
    except (VerificationFailure, ValueError, OSError, KeyError, TypeError) as error:
        print('VERIFICATION_FAILED: '+str(error), file=sys.stderr)
        return 1
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == '__main__':
    sys.exit(main())
