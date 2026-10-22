#!/usr/bin/env python3
"""Portable read-only byte authentication and exact finite-sign diagnostics."""
import json
import os
from pathlib import Path
import subprocess
import sys

# The module is shipped next to this script in both layouts.
sys.dont_write_bytecode = True
_script = Path(os.path.abspath(__file__))
_helper = _script.parent / 'package_common.py'
for _input in (_script, _helper):
    for _component in reversed([_input, *_input.parents]):
        if _component.is_symlink():
            raise ValueError('symlink ancestor/member: ' + str(_component))
sys.path.insert(0, str(_helper.parent))
from package_common import (HERE, audit_root, byte_pin, encoded, load, need,
                            pin, read, read_allowlist, verify_audit,
                            verify_manifest, verify_pdf_qa)


def main():
    need(len(sys.argv) == 1, 'verifier accepts no command-line arguments')
    allowed = read_allowlist()
    verify_audit(allowed)
    verify_manifest(allowed)
    verify_pdf_qa()
    plan = load(HERE / 'verification/CONTROL_PLAN.json')
    expected_plan_fields = {
        'diagnostic', 'diagnostic_source', 'expected_stdout', 'positive_modes',
        'mutations', 'expected_positive_runs', 'expected_actual_wrong_result_failures',
        'mathematical_scope', 'historical_family_programs', 'source_body_custody_checks',
    }
    need(isinstance(plan, dict) and set(plan) == expected_plan_fields, 'control-plan schema mismatch')
    need(plan['diagnostic'] == 'verify_finite_signs.py', 'diagnostic path contract mismatch')
    program = audit_root() / 'verify_finite_signs.py'
    need(pin(program) == plan['diagnostic_source'] == allowed['verify_finite_signs.py'],
         'finite-sign source pin mismatch')
    expected = read(HERE / 'verification/EXPECTED_FINITE_SIGNS.stdout.json')
    need(byte_pin(expected) == plan['expected_stdout'], 'complete positive baseline pin mismatch')
    need(plan['positive_modes'] == ['normal', 'optimized']
         and plan['expected_positive_runs'] == 2
         and plan['expected_actual_wrong_result_failures'] == 8,
         'positive/negative process contract mismatch')
    mutations = {
        'omit_deletion': 'ValueError: explicit inverse failure',
        'keep_minimum': 'ValueError: rotation collision',
        'append_plus': 'ValueError: rotation collision',
        'omit_scaling': 'ValueError: bottom source generator does not map to target unit',
    }
    need(plan['mutations'] == mutations, 'mutation control contract mismatch')
    need(json.loads(expected).get('status') == 'PASS', 'invalid complete positive baseline')
    runs = []
    failures = []
    env = os.environ.copy()
    env.update({'PYTHONHASHSEED': '0', 'PYTHONDONTWRITEBYTECODE': '1', 'PYTHONIOENCODING': 'utf-8'})
    for mode in plan['positive_modes']:
        command = [sys.executable, '-B'] + (['-O'] if mode == 'optimized' else []) + [str(program)]
        result = subprocess.run(command, capture_output=True, env=env, timeout=120)
        need(result.returncode == 0 and result.stderr == b'' and result.stdout == expected,
             'complete positive output mismatch: ' + mode)
        runs.append({'mode': mode, 'exit': result.returncode,
                     'complete_stdout': result.stdout.decode('utf-8'),
                     'stdout': byte_pin(result.stdout), 'stderr': byte_pin(result.stderr)})
        for mutation, reason in mutations.items():
            result = subprocess.run(command + ['--mutation', mutation], capture_output=True,
                                    env=env, timeout=120)
            stderr_lines = result.stderr.decode('utf-8').splitlines()
            need(result.returncode == 1 and result.stdout == b''
                 and bool(stderr_lines) and stderr_lines[-1] == reason,
                 'actual mathematical mutation did not fail as expected: ' + mode + '/' + mutation)
            failures.append({'mode': mode, 'mutation': mutation, 'exit': result.returncode,
                             'checked_mathematical_failure': reason,
                             'stdout': byte_pin(result.stdout)})
    need(len(runs) == 2 and len(failures) == 8, 'incomplete process verification')
    result = {
        'status': 'PASS', 'authored_audit_members': len(allowed),
        'diagnostic_source': plan['diagnostic_source'], 'runs': runs,
        'actual_wrong_result_failures': failures,
        'finite_diagnostics_only': True,
        'mathematical_scope': plan['mathematical_scope'],
        'historical_family_programs': plan['historical_family_programs'],
        'source_body_custody_checks': plan['source_body_custody_checks'],
    }
    sys.stdout.buffer.write(encoded(result))


if __name__ == '__main__':
    main()
