#!/usr/bin/env python3
"""Closed portable evidence checks; arithmetic and integrity do not prove analysis."""
import argparse
from fractions import Fraction
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
    require(data['schema'] == 'weighted-yamabe-preprint-v1' and data['problem_id'] == 30001168,
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
    flags = ['-I', '-B'] + (['-O'] if sys.flags.optimize else [])
    def run(script, *args):
        result = subprocess.run([sys.executable, *flags, str(script), *args],
                                cwd='/', capture_output=True, text=True, timeout=900)
        require(result.returncode == 0 and not result.stderr, str(script) + ': ' + result.stderr)
        return json.loads(result.stdout, object_pairs_hook=unique)
    historical = run(root / 'source/verify_publication.py')
    require(historical['verified'] is True and historical['files'] == 42 and
            sum(x['members'] for x in historical['archives'].values()) == 32,
            'historical identity and archive count')
    controls = run(root / 'source/package_controls.py')
    require(controls['total'] == 20 and controls['accepted_baselines'] == 2 and
            controls['expected_rejections'] == 18, 'historical outer controls')
    trace = run(root / 'trace_audit_01/check_trace_bounds.py')
    require(trace == load(root / 'trace_audit_01/EXACT_RESULTS.json'), 'fresh trace replay')
    require(trace['round_stronger_uniform_threshold'] == '321/500' and
            Fraction(trace['cylinder_lower_exact']) == Fraction(1106714561, 1700054750),
            'current paper thresholds')
    rounded = [629002, 631338, 636143, 639464, 641172, 641202, 639541]
    exact = [trace['small_time_bound_exact']] + [r['bound_exact'] for r in trace['middle_intervals']]
    require(all(Fraction(x) < Fraction(y, 10**6) for x, y in zip(exact, rounded)) and
            max(rounded) < 642000, 'seven displayed rational enclosures')
    # These dated checkers write their receipts. Replay only disposable copies.
    with tempfile.TemporaryDirectory(prefix='yamabe independent evidence with spaces ') as td:
        scratch = Path(td)
        geometry = scratch / 'geometry_audit_01'
        geometry.mkdir()
        checker = root / 'geometry_audit_01/check_geometry_arithmetic.py'
        shutil.copyfile(checker, geometry / checker.name)
        geometry_summary = run(geometry / checker.name)
        require(load(geometry / 'GEOMETRY_ARITHMETIC_RESULTS.json') ==
                load(root / 'geometry_audit_01/GEOMETRY_ARITHMETIC_RESULTS.json'), 'fresh geometry replay')
        shutil.copytree(root / 'source', scratch / 'source')
        shutil.copytree(root / 'trace_audit_01', scratch / 'trace_audit_01')
        trace_controls = run(scratch / 'trace_audit_01/replay_and_controls.py')
        require(trace_controls['independent_negative_cases'] == 16 and
                trace_controls['scope_demonstrations'] == 2,
                'independent semantic controls and analytic scope boundary')
        require(load(scratch / 'trace_audit_01/REPLAY_CONTROLS.json') ==
                load(root / 'trace_audit_01/REPLAY_CONTROLS.json'), 'fresh semantic control receipt')
    return {'historical': historical, 'historical_outer_controls': controls,
            'fresh_trace': trace, 'fresh_geometry': geometry_summary,
            'fresh_trace_controls': trace_controls,
            'analytic_proof_verified_by_program': False, 'priority_verified_by_program': False}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('trusted_index_sha256')
    parser.add_argument('--full', action='store_true')
    args = parser.parse_args()
    root = Path(__file__).absolute().parent
    result = {'status': 'PASS', 'regular_files': bind(root, args.trusted_index_sha256),
              'analytic_proof_verified_by_program': False, 'priority_verified_by_program': False}
    if args.full:
        result['full'] = full(root)
        bind(root, args.trusted_index_sha256)
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
