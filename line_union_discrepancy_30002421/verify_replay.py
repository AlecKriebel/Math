"""Replay the floating-point diagnostic in isolation; never certify its mathematics.

Uses the current Python interpreter and installed NumPy. Copies only the public
experiment script into a temporary directory, runs from a different working
directory, and compares the generated JSON with the included baseline. Records
mathematical/diagnostic fields only; timing is neither retained nor compared.
Writes REPLAY_VERIFICATION.json beside this script. Does not edit the baseline.
"""
from pathlib import Path
import hashlib
import json
import math
import platform
import shutil
import subprocess
import sys
import tempfile

import numpy as np

HERE = Path(__file__).resolve().parent
SCRIPT = HERE / 'test_direction_mixtures.py'
EXPECTED = HERE / 'DIRECTION_MIXTURE_EXPERIMENT.json'
REPORT = HERE / 'REPLAY_VERIFICATION.json'
TIMING_KEYS = {'timing', 'timings', 'elapsed_seconds', 'elapsed_time', 'runtime_seconds', 'duration_seconds'}
REL_TOL = 1e-11
ABS_TOL = 1e-12


def hash_file(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def without_timing(obj):
    if isinstance(obj, dict):
        return {k: without_timing(v) for k, v in obj.items() if k not in TIMING_KEYS}
    if isinstance(obj, list):
        return [without_timing(v) for v in obj]
    return obj


stats = {'compared_numeric_fields': 0, 'maximum_absolute_difference': 0.0,
         'maximum_relative_difference': 0.0}
differences = []


def compare(expected, actual, trail='$'):
    if isinstance(expected, dict) and isinstance(actual, dict):
        if expected.keys() != actual.keys():
            differences.append({'field': trail, 'reason': 'object keys differ'})
            return
        for key in expected:
            compare(expected[key], actual[key], trail + '.' + key)
    elif isinstance(expected, list) and isinstance(actual, list):
        if len(expected) != len(actual):
            differences.append({'field': trail, 'reason': 'array lengths differ'})
            return
        for i, (a, b) in enumerate(zip(expected, actual)):
            compare(a, b, f'{trail}[{i}]')
    elif isinstance(expected, (int, float)) and not isinstance(expected, bool) and isinstance(actual, (int, float)) and not isinstance(actual, bool):
        stats['compared_numeric_fields'] += 1
        if not (math.isfinite(expected) and math.isfinite(actual)):
            differences.append({'field': trail, 'reason': 'nonfinite numerical value'})
            return
        delta = abs(expected - actual)
        rel = delta / max(abs(expected), abs(actual)) if expected or actual else 0.0
        stats['maximum_absolute_difference'] = max(stats['maximum_absolute_difference'], delta)
        stats['maximum_relative_difference'] = max(stats['maximum_relative_difference'], rel)
        matches = expected == actual if isinstance(expected, int) and isinstance(actual, int) else math.isclose(expected, actual, rel_tol=REL_TOL, abs_tol=ABS_TOL)
        if not matches:
            differences.append({'field': trail, 'reason': 'numeric difference exceeds tolerance'})
    elif type(expected) is not type(actual) or expected != actual:
        differences.append({'field': trail, 'reason': 'nonnumeric value differs'})


baseline = without_timing(json.loads(EXPECTED.read_text()))
with tempfile.TemporaryDirectory(prefix='line-discrepancy-replay-') as temp:
    root = Path(temp)
    script_dir = root / 'artifact'
    working_dir = root / 'unrelated_working_directory'
    script_dir.mkdir()
    working_dir.mkdir()
    isolated_script = script_dir / SCRIPT.name
    shutil.copy2(SCRIPT, isolated_script)
    run = subprocess.run([sys.executable, str(isolated_script)], cwd=working_dir,
                         check=True, capture_output=True, text=True)
    generated_path = script_dir / EXPECTED.name
    generated = without_timing(json.loads(generated_path.read_text()))
    compare(baseline, generated)
    sibling_output = generated_path.is_file() and not (working_dir / EXPECTED.name).exists()
    report = {
        'schema_version': 1,
        'purpose': 'Isolated reproducibility check of floating-point diagnostic output, not a proof certificate.',
        'result': 'PASS' if not differences and sibling_output else 'FAIL',
        'experiment_script_sha256': hash_file(SCRIPT),
        'baseline_sha256': hash_file(EXPECTED),
        'isolated_output_sha256': hash_file(generated_path),
        'environment': {'python_version': platform.python_version(), 'python_implementation': platform.python_implementation(), 'numpy_version': np.__version__, 'operating_system': platform.system(), 'architecture': platform.machine()},
        'isolation': {'fresh_temporary_directory': True, 'run_working_directory_differs_from_script_directory': True, 'output_written_beside_script_only': sibling_output, 'baseline_preserved': True},
        'comparison': {'scope': 'All JSON fields after recursive removal of timing keys. Integers and metadata exact; floating values at declared tolerances.', 'excluded_timing_keys': sorted(TIMING_KEYS), 'relative_tolerance': REL_TOL, 'absolute_tolerance': ABS_TOL, 'parsed_output_exact_match_excluding_timing': baseline == generated, **stats, 'differences': differences},
        'stdout_lines': run.stdout.splitlines(),
        'stderr_empty': not run.stderr,
        'limitations': ['Floating-point computation only; no exact arithmetic or interval certificate.', 'No certification of cube containment, clipping, event ordering, or roundoff.', 'No certified supremum lower or upper bound and no numerical counterexample.'],
    }
REPORT.write_text(json.dumps(report, indent=2) + '\n')
print(report['result'])
print(f"Compared {stats['compared_numeric_fields']} numeric fields; exact parsed match: {baseline == generated}.")
if report['result'] != 'PASS':
    raise SystemExit(1)
