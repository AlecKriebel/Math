#!/usr/bin/env python3
"""Narrow derivative replay of PR397; frozen historical programs are unchanged."""
import argparse
import datetime as dt
import hashlib
import json
import math
import os
from pathlib import Path, PurePosixPath
import platform
import shutil
import subprocess
import sys
import tempfile
import uuid

BINDING_SHA256 = 'cb2f5bef79d21619ebf8c40d25951bdb22def993370e5692a3b587a6176c4a57'
POLICY_SHA256 = '2470d16dfdb0647301998052c7025ec701eb97953fb57836ae238a95be07b53f'
COMPONENTS = [
    ('turn1', 'turns/turn_01/check_model.py', 'turns/turn_01/CHECKS.json', 'turns/turn_01/CHECKS.json'),
    ('turn2', 'turns/turn_02/check_model.py', 'turns/turn_02/CHECKS.json', 'turns/turn_02/CHECKS.json'),
    ('portable', 'review/portable_independent_checks.py', 'review/INDEPENDENT_CHECKS.json', 'review/PORTABLE_INDEPENDENT_CHECKS.json'),
]

class AuditError(Exception):
    pass

def require(ok, message):
    if not ok:
        raise AuditError(message)

def sha(data):
    return hashlib.sha256(data).hexdigest()

def reject_constant(value):
    raise AuditError('Non-finite JSON number: ' + value)

def reject_duplicate_keys(pairs):
    obj = {}
    for key, value in pairs:
        require(key not in obj, 'Duplicate JSON object key: ' + key)
        obj[key] = value
    return obj

def finite_tree(value, path=''):
    if type(value) is float:
        require(math.isfinite(value), 'Non-finite number at ' + path)
    elif type(value) is dict:
        for key, item in value.items():
            finite_tree(item, path + '/' + key)
    elif type(value) is list:
        for i, item in enumerate(value):
            finite_tree(item, path + '/' + str(i))

def strict_json(data):
    try:
        result = json.loads(data, parse_constant=reject_constant, object_pairs_hook=reject_duplicate_keys)
    except (ValueError, UnicodeError) as error:
        raise AuditError('Invalid JSON: ' + str(error)) from error
    finite_tree(result)
    return result

def load_controls(home):
    binding_data = (home / 'candidate-binding.json').read_bytes()
    policy_data = (home / 'comparison-policy.json').read_bytes()
    require(sha(binding_data) == BINDING_SHA256, 'Candidate binding itself differs from reviewed bytes')
    require(sha(policy_data) == POLICY_SHA256, 'Comparison policy itself differs from reviewed bytes')
    return strict_json(binding_data), strict_json(policy_data)

def safe_relative(name):
    require(type(name) is str and name != '', 'Invalid manifest path')
    path = PurePosixPath(name)
    require(not path.is_absolute() and all(x not in ('', '.', '..') for x in path.parts), 'Unsafe manifest path')
    require(str(path) == name, 'Noncanonical manifest path')
    return path

def verify_candidate(candidate, binding):
    require(candidate.is_dir() and not candidate.is_symlink(), 'Candidate must be a real directory')
    entries = binding['files']
    require(type(entries) is list and len(entries) == 24, 'Expected exactly24 binding entries')
    names = [x['path'] for x in entries]
    require(len(set(names)) == 24, 'Duplicate binding path')
    allowed_dirs = set()
    for name in names:
        rel = safe_relative(name)
        allowed_dirs.update(str(p) for p in rel.parents if str(p) != '.')
    actual = set()
    for current, dirs, files in os.walk(candidate, followlinks=False):
        for name in dirs + files:
            file = Path(current) / name
            rel = file.relative_to(candidate).as_posix()
            require(not file.is_symlink(), 'Symlink in candidate: ' + rel)
            if file.is_dir():
                require(rel in allowed_dirs, 'Unexpected candidate directory: ' + rel)
            else:
                require(file.is_file(), 'Nonregular candidate file: ' + rel)
                actual.add(rel)
    require(actual == set(names), 'Candidate file set differs: missing=' + repr(sorted(set(names)-actual)) + ', extra=' + repr(sorted(actual-set(names))))
    for item in entries:
        name = item['path']
        data = (candidate / name).read_bytes()
        require(type(item['bytes']) is int and len(data) == item['bytes'], 'Candidate byte length mismatch: ' + name)
        require(sha(data) == item['sha256'], 'Candidate SHA256 mismatch: ' + name)
        blob = hashlib.sha1(('blob ' + str(len(data)) + '\0').encode() + data).hexdigest()
        require(blob == item['git_blob'], 'Candidate Git blob mismatch: ' + name)
    return {'files':24, 'all_lengths_sha256_and_Git_blobs_match':True, 'source_head':binding['source_head'], 'binding_sha256':BINDING_SHA256}

def runtime_versions():
    import numpy
    import scipy
    return {'python':platform.python_version(), 'numpy':numpy.__version__, 'scipy':scipy.__version__}

def compare_records(expected, actual, component, policy, runtime):
    """Exact typed comparison except immutable, explicitly enumerated rules."""
    changes = []
    tolerances = policy['float_tolerances'].get(component, {})
    special = policy['portable_metadata']
    finite_tree(expected)
    finite_tree(actual)
    def walk(before, after, path):
        require(type(before) is type(after), 'Type mismatch at ' + path)
        if type(before) is dict:
            require(set(before) == set(after), 'Object keys mismatch at ' + path)
            for key in sorted(before):
                walk(before[key], after[key], path + '/' + key)
        elif type(before) is list:
            require(len(before) == len(after), 'List length mismatch at ' + path)
            for i, (x, y) in enumerate(zip(before, after)):
                walk(x, y, path + '/' + str(i))
        elif component == 'portable' and path in ('/python', '/numpy', '/scipy'):
            key = path[1:]
            require(type(before) is str and before == special['historical_versions'][key], 'Unexpected historical version at ' + path)
            require(after == runtime[key], 'Reported version differs from imported runtime at ' + path)
            if before != after:
                changes.append({'path':path, 'rule':'explicit runtime metadata', 'before':before, 'after':after})
        elif component == 'portable' and path in ('/checks/0/name', '/checks/0/files'):
            key = path.rsplit('/', 1)[1]
            require(before == special['historical_projection'][key], 'Unexpected historical projection at ' + path)
            require(after == special['public_projection'][key], 'Incorrect public-input projection at ' + path)
            if before != after:
                changes.append({'path':path, 'rule':'explicit documented public-input projection', 'before':before, 'after':after})
        elif path in tolerances:
            rule = tolerances[path]
            require(type(before) is float and type(after) is float, 'Diagnostic must retain float type at ' + path)
            require(before == rule['historical_value'], 'Historical diagnostic drift at ' + path)
            require(rule['relative_tolerance'] == 0, 'Unexpected relative tolerance')
            error = abs(before-after)
            require(error <= rule['absolute_tolerance'], 'Diagnostic exceeds narrow tolerance at ' + path)
            if before != after:
                changes.append({'path':path, 'rule':'enumerated floating diagnostic', 'before':before, 'after':after, 'absolute_difference':error, 'absolute_tolerance':rule['absolute_tolerance']})
        else:
            require(before == after, 'Exact value mismatch at ' + path)
    walk(expected, actual, '')
    require(type(actual) is dict and actual.get('all_assertions_passed') is True, 'Required assertion flag is not true')
    return changes

def compare_component(expected_data, actual_data, component, policy, runtime):
    expected = strict_json(expected_data)
    actual = strict_json(actual_data)
    if component == 'turn2':
        require(expected_data == actual_data, 'Turn2 must reproduce the exact frozen output bytes')
    changes = compare_records(expected, actual, component, policy, runtime)
    return {'all_assertions_passed':True, 'expected_sha256':sha(expected_data), 'actual_sha256':sha(actual_data), 'exact_bytes_match':expected_data == actual_data, 'declared_differences':changes}

def write_receipt(output, receipt):
    data = json.dumps(receipt, indent=2, allow_nan=False) + '\n'
    temp = output / 'receipt.json.tmp'
    temp.write_text(data)
    temp.replace(output / 'receipt.json')

def run_component(candidate, binding, output, spec, policy, runtime, timeout):
    name, script, expected_name, produced_name = spec
    evidence = output / name
    evidence.mkdir()
    with tempfile.TemporaryDirectory(prefix='fresh-', dir=str(evidence)) as tmp:
        fresh = Path(tmp) / 'candidate'
        shutil.copytree(candidate, fresh)
        verify_candidate(fresh, binding)
        expected_data = (fresh/expected_name).read_bytes()
        env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', PYTHONHASHSEED='0')
        with (evidence/'stdout.txt').open('xb') as stdout, (evidence/'stderr.txt').open('xb') as stderr:
            result = subprocess.run([sys.executable, '-B', str(fresh/script)], cwd=fresh, env=env, stdout=stdout, stderr=stderr, timeout=timeout)
        require(result.returncode == 0, 'Component exited with code ' + str(result.returncode) + ': ' + name)
        actual_data = (fresh/produced_name).read_bytes()
        (evidence/'actual.json').write_bytes(actual_data)
        comparison = compare_component(expected_data, actual_data, name, policy, runtime)
        (evidence/'comparison.json').write_text(json.dumps(comparison, indent=2, allow_nan=False) + '\n')
    return {'component':name, 'exit_code':0, **comparison}

def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--candidate', type=Path, help='Frozen24-file candidate directory; default: candidate/ beside this wrapper')
    parser.add_argument('--output', type=Path, help='New evidence directory; must not exist and must be outside candidate/')
    parser.add_argument('--timeout', type=int, default=180, help='Maximum seconds per component; failure is recorded, never automatically retried')
    args = parser.parse_args(argv)
    home = Path(__file__).resolve().parent
    candidate = args.candidate.absolute() if args.candidate is not None else home/'candidate'
    tag = dt.datetime.now(dt.timezone.utc).strftime('%Y%m%dT%H%M%SZ') + '-' + uuid.uuid4().hex[:8]
    output = args.output.absolute() if args.output is not None else home/'replay-output'/tag
    try:
        require(args.timeout > 0, 'Timeout must be positive')
        require(not output.resolve().is_relative_to(candidate.resolve()), 'Output must be outside frozen candidate')
        output.mkdir(parents=True, exist_ok=False)
    except Exception as error:
        print(json.dumps({'status':'failed_before_output_creation', 'error':str(error)}), file=sys.stderr)
        return 2
    receipt = {'schema':1, 'status':'running', 'started_at':dt.datetime.now(dt.timezone.utc).isoformat(), 'wrapper_sha256':sha(Path(__file__).read_bytes()), 'policy_sha256':POLICY_SHA256, 'components':[], 'original_historical_wrapper_used':False, 'frozen_inputs_modified':False, 'no_automatic_retry':True}
    write_receipt(output, receipt)
    try:
        binding, policy = load_controls(home)
        receipt['input_verification'] = verify_candidate(candidate, binding)
        runtime = runtime_versions()
        receipt['runtime'] = runtime
        write_receipt(output, receipt)
        for spec in COMPONENTS:
            receipt['current_component'] = spec[0]
            write_receipt(output, receipt)
            receipt['components'].append(run_component(candidate, binding, output, spec, policy, runtime, args.timeout))
            write_receipt(output, receipt)
        verify_candidate(candidate, binding)
        receipt.pop('current_component', None)
        receipt.update(status='passed', completed_at=dt.datetime.now(dt.timezone.utc).isoformat(), all_original_components_passed=True, interpretation='New narrow derivative replay. Turn2 exact bytes; declared original floating diagnostics and explicit metadata/projection differences only. Not a proof or novelty certificate.')
        write_receipt(output, receipt)
        print(json.dumps({'status':'passed', 'original_files_verified':24, 'components':len(receipt['components']), 'turn2_exact_bytes':True, 'declared_differences':sum(len(x['declared_differences']) for x in receipt['components'])}))
        return 0
    except Exception as error:
        receipt.update(status='failed', completed_at=dt.datetime.now(dt.timezone.utc).isoformat(), error_type=type(error).__name__, error=str(error))
        try:
            verify_candidate(candidate, binding)
        except Exception:
            receipt['final_input_reverification_passed'] = False
        else:
            receipt['final_input_reverification_passed'] = True
        write_receipt(output, receipt)
        print(json.dumps({'status':'failed', 'error_type':type(error).__name__, 'error':str(error)}), file=sys.stderr)
        return 1

if __name__ == '__main__':
    raise SystemExit(main())
