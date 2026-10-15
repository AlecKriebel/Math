#!/usr/bin/env python3
"""Actual normal/optimized negative matrix for the supported PR445 verifier.

Use a new --records directory for each checkpoint; existing records are refused.
All children use the launching sys.executable. All disposable fixtures are under
this package's private/ tree and are removed afterward. No frozen source bytes
are changed. Explicit guards validate rejection reason and absence of PASS.
"""
from pathlib import Path
from datetime import datetime, timezone
import argparse
import ast
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time

HERE = Path(__file__).resolve().parent


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True)+'\n')


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def copy_inputs(dest):
    dest.mkdir()
    shutil.copyfile(HERE/'SOURCE_MANIFEST.json', dest/'SOURCE_MANIFEST.json')
    shutil.copytree(HERE/'frozen_history', dest/'frozen_history')


def reseal_history(root):
    # Deliberately self-consistent but wrong history, with BOTH historical
    # manifests and the new canonical manifest resealed. A literal trusted
    # source-manifest pin must defeat this attempted substitution of identity.
    hist = root/'frozen_history'
    author_path = hist/'author/MANIFEST.json'
    author = json.loads(author_path.read_text())
    for name, row in author['files'].items():
        path = hist/'author'/name
        row.update({'bytes': path.stat().st_size, 'sha256': sha(path)})
    write_json(author_path, author)
    release_path = hist/'RELEASE_MANIFEST.json'
    release = json.loads(release_path.read_text())
    for row in release['files']:
        path = hist/row['path']
        row.update({'bytes': path.stat().st_size, 'sha256': sha(path)})
    write_json(release_path, release)
    manifest_path = root/'SOURCE_MANIFEST.json'
    manifest = json.loads(manifest_path.read_text())
    for row in manifest['files']:
        path = hist/row['path']
        row.update({'bytes': path.stat().st_size, 'sha256': sha(path)})
    write_json(manifest_path, manifest)


def fixture(root, variant):
    copy_inputs(root)
    hist = root/'frozen_history'
    manifest_path = root/'SOURCE_MANIFEST.json'
    saved_author = hist/'author/checks/verification_results.json'
    if variant == 'source_byte_corruption':
        path = hist/'author/attempts/turn_01.md'
        data = path.read_bytes()
        path.write_bytes(b'X'+data[1:])  # Same length: exercises the SHA guard.
    elif variant == 'source_byte_length':
        path = hist/'README.md'
        path.write_bytes(path.read_bytes()+b'\n')
    elif variant == 'source_manifest_hash':
        manifest = json.loads(manifest_path.read_text())
        manifest['files'][0]['sha256'] = '0'*64
        write_json(manifest_path, manifest)
    elif variant == 'saved_author_bytes':
        saved = json.loads(saved_author.read_text())
        saved['density'] = '300'
        write_json(saved_author, saved)
    elif variant == 'saved_independent_bytes':
        path = hist/'audit/independent_controls_results.json'
        saved = json.loads(path.read_text())
        saved['physical_point_count_controls'][0]['point_count'] += 1
        write_json(path, saved)
    elif variant == 'resealed_saved_results':
        saved = json.loads(saved_author.read_text())
        saved['density'] = '300'
        write_json(saved_author, saved)
        reseal_history(root)
    elif variant == 'missing_source':
        saved_author.unlink()
    elif variant == 'extra_source':
        (hist/'EXTRA.txt').write_text('unlisted source\n')
    elif variant == 'manifest_path_traversal':
        manifest = json.loads(manifest_path.read_text())
        manifest['files'][0]['path'] = '../README.md'
        write_json(manifest_path, manifest)
    elif variant == 'source_symlink':
        path = hist/'README.md'
        path.unlink()
        path.symlink_to(hist/'CLARIFICATIONS.md')
    else:
        raise RuntimeError('Unknown fixture '+variant)


def execute(name, script, arguments, optimize, cwd, env_base, records_dir, expected_error=None):
    env = env_base.copy()
    env.pop('PYTHONOPTIMIZE', None)
    if optimize:
        env['PYTHONOPTIMIZE'] = '1'
    command = [sys.executable, str(script), *arguments]
    start = time.monotonic()
    try:
        completed = subprocess.run(command, env=env, cwd=cwd, text=True, capture_output=True, timeout=180)
        record = {'name': name, 'command': command, 'sys_executable_pinned': command[0] == sys.executable,
                  'cwd': str(cwd), 'inherited_PYTHONOPTIMIZE': env.get('PYTHONOPTIMIZE'),
                  'returncode': completed.returncode, 'stdout': completed.stdout, 'stderr': completed.stderr,
                  'elapsed_seconds': round(time.monotonic()-start, 6),
                  'expected_rejection': expected_error is not None, 'expected_error_substring': expected_error}
    except subprocess.TimeoutExpired as error:
        record = {'name': name, 'command': command, 'returncode': None,
                  'stdout': str(error.stdout), 'stderr': str(error.stderr), 'timeout': True,
                  'expected_rejection': expected_error is not None, 'expected_error_substring': expected_error}
    # Persist raw evidence before interpreting it, including failed suite attempts.
    write_json(records_dir/(name+'.json'), record)
    if expected_error is None:
        require(record['returncode'] == 0, 'Positive verifier failed: '+name)
        value = json.loads(record['stdout'])
        require(value['status'] == 'PASS', 'Positive success record missing: '+name)
        require(value['runtime']['optimization'] == int(optimize), 'Child optimization flag differs: '+name)
        require(value['runtime']['executable'] == sys.executable, 'Child interpreter differs: '+name)
    else:
        require(record['returncode'] not in (0, None), 'Negative verifier falsely accepted/timed out: '+name)
        require(not record['stdout'].strip(), 'Negative emitted output before failure: '+name)
        require('VERIFICATION_FAILED:' in record['stderr'] and expected_error in record['stderr'],
                'Negative rejection reason differs: '+name)
    record['expectation_met'] = True
    write_json(records_dir/(name+'.json'), record)
    print(name+': expected '+('rejection' if expected_error else 'PASS')+' observed', flush=True)
    return record


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--records', required=True, type=Path, help='New records directory under this package')
    args = parser.parse_args()
    target = args.records if args.records.is_absolute() else HERE/args.records
    target = target.resolve()
    require(target.is_relative_to(HERE) and target != HERE, 'Records must be in a new subdirectory of this package')
    require(not target.exists(), 'Refusing to overwrite earlier raw records: '+str(target))
    target.mkdir(parents=True)
    private = HERE/'private'
    private.mkdir(exist_ok=True)
    records = []
    controlled = ['verify.py', 'controls_exact.py', 'controls_deterministic.py', 'test_suite.py']
    assertion_counts = {name: sum(isinstance(n, ast.Assert) for n in ast.walk(ast.parse((HERE/name).read_text())))
                        for name in controlled}
    require(all(count == 0 for count in assertion_counts.values()), 'Essential supported code must contain no assert nodes')
    before = {str(p.relative_to(HERE)): sha(p) for p in (HERE/'frozen_history').rglob('*') if p.is_file()}
    require(len(before) == 12, 'Suite requires exact 12-file frozen source copy')
    with tempfile.TemporaryDirectory(prefix='matrix path with spaces ', dir=private) as temp:
        work = Path(temp)
        cwd = work/'arbitrary cwd with spaces'
        cwd.mkdir()
        trap = work/'PATH trap'
        trap.mkdir()
        trap_python = trap/'python3'
        trap_python.write_text('#!/bin/sh\nprintf "UNPINNED_CHILD_INTERPRETER\\n" >&2\nexit 93\n')
        trap_python.chmod(0o755)
        env_base = os.environ.copy()
        env_base['PATH'] = str(trap)+os.pathsep+env_base.get('PATH', '')
        relocated = work/'supported package with spaces'
        copy_inputs(relocated)
        for filename in controlled:
            shutil.copyfile(HERE/filename, relocated/filename)
        script = relocated/'verify.py'
        for optimize in [False, True]:
            mode = 'optimized' if optimize else 'normal'
            records.append(execute('baseline_'+mode, script, [], optimize, cwd, env_base, target))
        math_cases = {'marker': 'Marker is ambiguous', 'correlation': 'Occupancy coefficient differs',
                      'normalization': 'normalization fails', 'flow': 'Floor-bin triangle fails',
                      'cocycle': 'Suspension action cocycle fails', 'rs': 'RS one-sided substitution/bit coding differs',
                      'physical_pairs': 'Physical direct/factored pair count differs',
                      'subdivision': 'Subdivision/triangle section correlation differs',
                      'saved_author_semantic': 'Saved author result semantic mismatch',
                      'saved_independent_semantic': 'Saved independent result semantic mismatch'}
        for variant, reason in math_cases.items():
            for optimize in [False, True]:
                mode = 'optimized' if optimize else 'normal'
                records.append(execute('fault_'+variant+'_'+mode, script,
                                       ['--diagnostic-fault', variant], optimize, cwd, env_base, target, reason))
        integrity_cases = {'source_byte_corruption': 'Frozen source hash mismatch',
                           'source_byte_length': 'Frozen source byte length mismatch',
                           'source_manifest_hash': 'Canonical source manifest literal hash mismatch',
                           'saved_author_bytes': 'Frozen source byte length mismatch',
                           'saved_independent_bytes': 'Frozen source',
                           'resealed_saved_results': 'Canonical source manifest literal hash mismatch',
                           'missing_source': 'Frozen source exact file inventory mismatch',
                           'extra_source': 'Frozen source exact file inventory mismatch',
                           'manifest_path_traversal': 'Canonical source manifest literal hash mismatch',
                           'source_symlink': 'Frozen history contains a symlink'}
        for variant, reason in integrity_cases.items():
            root = work/('bad '+variant+' inputs')
            fixture(root, variant)
            for optimize in [False, True]:
                mode = 'optimized' if optimize else 'normal'
                records.append(execute('integrity_'+variant+'_'+mode, script,
                                       ['--inputs', str(root)], optimize, cwd, env_base, target, reason))
        bad_code = work/'supported code corruption'
        copy_inputs(bad_code)
        for filename in controlled:
            shutil.copyfile(HERE/filename, bad_code/filename)
        file = bad_code/'controls_exact.py'
        file.write_bytes(file.read_bytes()+b'\n')
        for optimize in [False, True]:
            mode = 'optimized' if optimize else 'normal'
            records.append(execute('integrity_supported_code_'+mode, bad_code/'verify.py', [],
                                   optimize, cwd, env_base, target, 'Supported control literal hash mismatch'))
    after = {str(p.relative_to(HERE)): sha(p) for p in (HERE/'frozen_history').rglob('*') if p.is_file()}
    require(before == after, 'Suite modified frozen historical copy')
    baselines = [r for r in records if not r['expected_rejection']]
    comparable = [json.loads(r['stdout']) for r in baselines]
    for value in comparable:
        del value['runtime']
    require(comparable[0] == comparable[1], 'Normal/optimized mathematical outputs differ')
    summary = {'schema_version': 1, 'pr': 445, 'problem_id': 30002737,
               'frozen_head': '3242c84e06db7e99012c7fe581adde5c3f89fc89',
               'reviewer': '/root/pr445_verification_repair',
               'captured_at_utc': datetime.now(timezone.utc).isoformat(),
               'suite_runtime': {'executable': sys.executable, 'version': sys.version,
                                 'optimization': sys.flags.optimize,
                                 'inherited_PYTHONOPTIMIZE': os.environ.get('PYTHONOPTIMIZE')},
               'baseline_runs': len(baselines), 'baseline_math_outputs_identical': True,
               'actual_negative_runs': len(records)-len(baselines),
               'actual_mathematical_fault_runs': 16, 'saved_result_semantic_fault_runs': 4,
               'integrity_fault_runs': 22,
               'normal_negatives_rejected': sum(r['expected_rejection'] and r['returncode'] != 0
                                               and r['inherited_PYTHONOPTIMIZE'] is None for r in records),
               'optimized_negatives_rejected': sum(r['expected_rejection'] and r['returncode'] != 0
                                                  and r['inherited_PYTHONOPTIMIZE'] == '1' for r in records),
               'all_children_sys_executable_pinned': all(r['sys_executable_pinned'] for r in records),
               'all_negatives_stdout_empty': all(not r['stdout'].strip() for r in records if r['expected_rejection']),
               'supported_assertion_nodes': assertion_counts,
               'all_12_frozen_copies_unchanged': True,
               'original_scripts_executed': False,
               'run_records': [r['name']+'.json' for r in records],
               'status': 'ALL_EXPECTATIONS_MET',
               'scope': 'Proposed supported repair self-tests; no independent acceptance or infinite theorem claim'}
    write_json(target/'SUMMARY.json', summary)
    write_json(target/'FINITE_RESULTS.json', json.loads(baselines[0]['stdout']))
    print(json.dumps({k: v for k, v in summary.items() if k != 'run_records'}, indent=2))
    return 0


if __name__ == '__main__':
    sys.exit(main())
