#!/usr/bin/env python3
"""Read-only recheck of the frozen packet and the audit's helper counterexample."""
import hashlib
import json
from fractions import Fraction
from pathlib import Path
import runpy
import subprocess
import sys

HERE = Path(__file__).resolve().parent
AUTHOR = HERE.parent / 'public'
EXPECTED = '22542408192501b6ff6f2c1cd3491cc529463fb0549283fa8164334dfb83012e'
manifest_path = AUTHOR / 'MANIFEST.json'
manifest = json.loads(manifest_path.read_text())
manifest_hash = hashlib.sha256(manifest_path.read_bytes()).hexdigest()
assert manifest_hash == EXPECTED
files = []
for entry in manifest['files']:
    p = AUTHOR / entry['path']
    raw = p.read_bytes()
    sha = hashlib.sha256(raw).hexdigest()
    passed = sha == entry['sha256'] and len(raw) == entry['bytes']
    assert passed, entry['path']
    files.append({'path': entry['path'], 'bytes': len(raw), 'sha256': sha, 'passed': passed})
expected_files = {'MANIFEST.json'} | {e['path'] for e in manifest['files']}
actual_files = {str(p.relative_to(AUTHOR)) for p in AUTHOR.rglob('*') if p.is_file()}
assert expected_files == actual_files, (expected_files, actual_files)
result = subprocess.run([sys.executable, '-B', str(AUTHOR / 'check_controls.py')], check=True, text=True, capture_output=True)
rerun = json.loads(result.stdout)
assert rerun == json.loads((AUTHOR / 'CONTROL_RESULTS.json').read_text())
assert rerun['checks_passed'] == 48
namespace = runpy.run_path(str(AUTHOR / 'check_controls.py'), run_name='audit_import')
n, arc_bound, norm_bound = namespace['approximation_parameters'](Fraction(100), Fraction(1))
assert n == 1 and arc_bound == Fraction(1, 2) and norm_bound == Fraction(88, 7)
print(json.dumps({
    'problem_id': '2305065',
    'manifest_sha256': manifest_hash,
    'frozen_file_checks': files,
    'author_directory_has_only_manifested_files_and_manifest': True,
    'controls_reproduced_exactly': True,
    'controls_passed': rerun['checks_passed'],
    'helper_counterexample': {
        'epsilon': '100', 'eta': '1', 'n': n,
        'arc_bound': str(arc_bound), 'norm_bound': str(norm_bound),
        'lemma_condition_n_at_least_2_satisfied': n >= 2,
        'severity': 'nonblocking generality defect outside all exercised inputs'
    },
    'limitations': ['These computations do not prove the analytic existence theorem.']
}, indent=2, sort_keys=True))
