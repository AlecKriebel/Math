#!/usr/bin/env python3
"""Reproduce immutable old replays, supplementary controls and intentional failure.

Originals are copied under ignored tmp/reproduction; only copies execute.
No Git, network, package installation, canonical writes or ledger charges.
"""
from pathlib import Path
import subprocess
import shutil
import json
import hashlib
import sys

HERE = Path(__file__).resolve().parent
INPUT = HERE.parent / 'source_snapshot'
SCRATCH = HERE / 'tmp' / 'reproduction'
SCRATCH.mkdir(parents=True, exist_ok=True)
PYTHON = '/usr/bin/python3'
report = []
for folder, script, frozen_folder, files, result_name, expected_assertions in [
    ('original', 'check_monodromy.py', INPUT,
     ['check_monodromy.py', 'PARTIAL.md', 'check_results.json'], 'check_results.json', 31),
    ('old_suite', 'independent_checks.py', INPUT/'review',
     ['independent_checks.py', 'reviewed_partial.md', 'independent_results.json'], 'independent_results.json', 53830),
]:
    directory = SCRATCH / folder
    directory.mkdir(parents=True, exist_ok=True)
    for file in files:
        shutil.copy2(frozen_folder/file, directory/file)
    before = hashlib.sha256((directory/script).read_bytes()).hexdigest()
    proc = subprocess.run([PYTHON, script], cwd=directory, capture_output=True, text=True)
    (directory/'stdout.txt').write_text(proc.stdout)
    (directory/'stderr.txt').write_text(proc.stderr)
    assert proc.returncode == 0, proc.stderr
    assert before == hashlib.sha256((directory/script).read_bytes()).hexdigest()
    assert (directory/result_name).read_bytes() == (frozen_folder/result_name).read_bytes()
    result = json.loads((directory/result_name).read_text())
    assert result['assertions'] == expected_assertions
    report.append({'run': folder, 'exit_code': proc.returncode,
                   'output_byte_matches_frozen': True, 'assertions': result['assertions']})
proc = subprocess.run([PYTHON, str(HERE/'geometric_controls.py')], cwd=HERE, capture_output=True, text=True)
(SCRATCH/'new_controls_stdout.txt').write_text(proc.stdout)
(SCRATCH/'new_controls_stderr.txt').write_text(proc.stderr)
assert proc.returncode == 0, proc.stderr
controls = json.loads((HERE/'geometric_control_results.json').read_text())
assert controls['assertions'] == 159563
assert controls['prefix_repair_tuples'] == 50068
assert controls['original_same_tree_quotient_step'].startswith('REQUIRES_REPAIR')
assert controls['code_sha256'] == hashlib.sha256((HERE/'geometric_controls.py').read_bytes()).hexdigest()
report.append({'run': 'new_geometric_controls', 'exit_code': 0,
               'assertions': controls['assertions'], 'verdict_scope': controls['status']})
proc = subprocess.run([PYTHON, str(HERE/'failure_harness.py')], cwd=HERE, capture_output=True, text=True)
(SCRATCH/'intentional_failure_stdout.txt').write_text(proc.stdout)
(SCRATCH/'intentional_failure_stderr.txt').write_text(proc.stderr)
assert proc.returncode != 0 and 'INTENTIONAL_MUTANT' in proc.stderr
report.append({'run': 'intentional_failure_harness', 'exit_code': proc.returncode,
               'status': 'EXPECTED_FAILURE_RECORDED_NOT_PASS'})
print(json.dumps({'python': PYTHON, 'python_version': sys.version,
                  'runs': report, 'original_verdict': 'HOLD_FOR_GEOMETRIC_PROOF_REPAIR',
                  'no_general_source_solution': True}, indent=2))
