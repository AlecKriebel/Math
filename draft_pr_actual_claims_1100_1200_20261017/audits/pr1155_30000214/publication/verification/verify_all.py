#!/usr/bin/env python3
"""Portable read-only authentication and exact finite-incidence diagnostics.

This is finite evidence. Universal claims remain the responsibility of the
written proof and its stated hypotheses. No quotient K is enumerated here.
"""
import json
import os
from pathlib import Path
import stat
import subprocess
import sys

sys.dont_write_bytecode = True
_script = Path(os.path.abspath(__file__))
_helper = _script.parent / 'package_common.py'
for _input in (_script, _helper):
    for _component in reversed([_input, *_input.parents]):
        if _component.is_symlink():
            raise ValueError('symlink ancestor/member: ' + str(_component))
    if not _input.exists() or not stat.S_ISREG(_input.lstat().st_mode):
        raise ValueError('missing/nonregular input: ' + str(_input))
sys.path.insert(0, str(_helper.parent))
from package_common import (HERE, byte_pin, encoded, load, need,
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
    need(plan['diagnostic'] == 'verification/finite_incidence_and_threshold.py',
         'diagnostic path contract mismatch')
    program = HERE / plan['diagnostic']
    need(pin(program) == plan['diagnostic_source'], 'finite-incidence source pin mismatch')
    expected = read(HERE / 'verification/EXPECTED_FINITE_INCIDENCE.stdout.json')
    need(byte_pin(expected) == plan['expected_stdout'], 'complete positive baseline pin mismatch')
    need(plan['positive_modes'] == ['normal', 'optimized']
         and type(plan['expected_positive_runs']) is int and plan['expected_positive_runs'] == 2
         and type(plan['expected_actual_wrong_result_failures']) is int
         and plan['expected_actual_wrong_result_failures'] == 6,
         'positive/negative process contract mismatch')
    mutations = {
        'nonzero_incidence': 'RuntimeError: point degree\n',
        'corrupt_torus_triangle': 'RuntimeError: torus edge links\n',
        'wrong_edge_weight': 'RuntimeError: weighted cocycle identities\n',
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
                     'complete_stderr': result.stderr.decode('utf-8'),
                     'stdout': byte_pin(result.stdout), 'stderr': byte_pin(result.stderr)})
        for mutation, reason in mutations.items():
            result = subprocess.run(command + ['--mutation', mutation], capture_output=True,
                                    env=env, timeout=120)
            need(result.returncode == 1 and result.stdout == b''
                 and result.stderr == reason.encode('utf-8'),
                 'actual mathematical mutation did not fail as expected: ' + mode + '/' + mutation)
            failures.append({'mode': mode, 'mutation': mutation, 'exit': result.returncode,
                             'checked_mathematical_failure': reason.rstrip('\n'),
                             'complete_stdout': result.stdout.decode('utf-8'),
                             'complete_stderr': result.stderr.decode('utf-8'),
                             'stdout': byte_pin(result.stdout), 'stderr': byte_pin(result.stderr)})
    need(len(runs) == 2 and len(failures) == 6, 'incomplete process verification')
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
