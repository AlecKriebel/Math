#!/usr/bin/env python3
"""Reproduce the submitted output and compare every computed matrix entry.

Run from any working directory after independent_verify.py has generated
independent_output.json beside this script. No submitted file is modified.
"""
from hashlib import sha256
from pathlib import Path
import json
import subprocess
import sys

root = Path(__file__).resolve().parent
def require(ok, label):
    if not ok:
        raise RuntimeError(label)

replay = subprocess.run([sys.executable, str(root.parent / 'public' / 'verify.py')],
                        check=True, capture_output=True).stdout
require(replay == (root.parent / 'public' / 'verification_output.json').read_bytes(),
        'Submitted verifier output differs from frozen expected output')
(root / 'package_replay.json').write_bytes(replay)
namespace = {'__name__': 'audit_import'}
source = root.parent / 'public' / 'verify.py'
exec(compile(source.read_bytes(), 'public/verify.py', 'exec'), namespace)
rows = namespace['integer_rows'](200)
digest = sha256(json.dumps(rows, separators=(',', ':')).encode()).hexdigest()
independent_namespace = {'__name__': 'audit_independent_import'}
exec(compile((root / 'independent_verify.py').read_bytes(),
             'audit/independent_verify.py', 'exec'), independent_namespace)
independent_rows, _ = independent_namespace['egf_power_rows'](200)
require(rows == independent_rows, 'Exact entrywise matrix comparison failed')
independent = json.loads((root / 'independent_output.json').read_text())
require(digest == independent['coefficient_matrix_sha256'],
        'Full coefficient matrices differ')
print(json.dumps({
    'coefficient_matrix_sha256': digest,
    'shape': [201, 201],
    'coefficient_pairs_including_initial_row': 40401,
    'full_matrix_identical': True,
    'exact_entrywise_comparison': True,
    'submitted_output_byte_identical': True,
}, indent=2, sort_keys=True))
