#!/usr/bin/env python3
"""Standalone R1 witness. Does not modify input sources or import project code.

Default succeeds only if both tested readers falsely accept malformed terms.
Use --expect-rejection against a repaired source to require rejection instead.
Requires the tested project's Python dependencies in the current interpreter.
"""
import argparse
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--source', type=Path, default=Path(__file__).resolve().parent / 'source_snapshot')
parser.add_argument('--expect-rejection', action='store_true')
args = parser.parse_args()
source = args.source.resolve()
original = json.loads((source / 'independent_verifier/pareto_all_m_certificate.json').read_text())
original['modulus']['homogeneous']['terms'].append(
    {'powers': [99, 99], 'coefficient_in_U_ascending': ['-1']})
original['modulus']['spatial']['terms'].append(
    {'powers': [99, 99, 99], 'coefficient_in_A_ascending': ['-1']})
results = []
with tempfile.TemporaryDirectory(prefix='turing-referee-r1-') as temporary:
    root = Path(temporary)
    minimal = root / 'minimal'
    shutil.copytree(source / 'external_audit/minimal_verifier', minimal)
    mutation = minimal / 'pareto_all_m_certificate.json'
    mutation.write_text(json.dumps(original) + '\n')
    commands = [
        ('direct_reader', [sys.executable, '-B', str(minimal / 'frontier_verify_mode_certificates.py'), str(mutation)], 'VERIFY_MODE_CERTIFICATES_PASS'),
        ('minimal_aggregate', [sys.executable, '-B', str(minimal / 'verify_symbolic_certificates.py')], 'ALL_SYMBOLIC_CERTIFICATES_PASS'),
    ]
    for name, command, marker in commands:
        run = subprocess.run(command, cwd=minimal, capture_output=True, text=True, timeout=180)
        passed = run.returncode == 0 and marker in run.stdout
        results.append({'reader': name, 'exit_code': run.returncode,
                        'pass_marker': marker in run.stdout,
                        'accepted_malformed_terms': passed})
        if args.expect_rejection:
            if run.returncode == 0 or marker in run.stdout:
                raise RuntimeError(f'{name} still accepts malformed terms')
        elif not passed:
            raise RuntimeError(f'{name} did not reproduce the expected defect: {run.stderr[-1000:]}')
print(json.dumps({'mode': 'require_rejection' if args.expect_rejection else 'reproduce_known_defect',
                  'results': results}, indent=2))
