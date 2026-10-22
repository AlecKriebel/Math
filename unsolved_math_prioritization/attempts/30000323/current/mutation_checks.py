#!/usr/bin/env python3
"""Meaningful source-mutation checks against the finite-algebra verifier only."""
import ast
import hashlib
import json
from pathlib import Path
import sys

source_path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parents[2] / 'topological_euler_30000323/tests/verify_detectors.py'
source = source_path.read_text()
mutations = (
    ('nonzero_phase_mistaken_for_kernel', 'return numerator % denominator == 0', 'return numerator % denominator != 0'),
    ('group_ring_plus_for_minus', 'out.get(shifted, 0) - coefficient', 'out.get(shifted, 0) + coefficient'),
    ('wrong_ordinary_modulus', '(out.get(shifted, 0) + coefficient * a) % p', '(out.get(shifted, 0) + coefficient * a) % (p * p)'),
    ('primitive_alpha_in_W', 'step = 1 if elementary else p', 'step = 1'),
    ('drop_projective_character', '[(a * step, 1) for a in range(p)]', '[(a * step, 1) for a in range(p - 1)]'),
    ('replace_transfer_by_index', 'induced = {(a * p, 0): 1 for a in range(p)}', 'induced = {(0, 0): p}'),
    ('accept_composite_parameter', 'if any(p % d == 0 for d in range(3, int(p ** 0.5) + 1, 2)):', 'if False:'),
)
results = []
for name, old, new in mutations:
    if source.count(old) != 1:
        raise RuntimeError('Mutation target not unique: ' + name)
    changed = source.replace(old, new)
    env = {'__name__': 'mutation_subject'}
    exec(compile(changed, '<' + name + '>', 'exec'), env)
    try:
        env['run']()
    except RuntimeError as error:
        results.append({'mutation': name, 'rejected': True, 'reason': str(error)})
    else:
        raise RuntimeError('Mutation escaped: ' + name)
if any(isinstance(node, ast.Assert) for node in ast.walk(ast.parse(source))):
    raise RuntimeError('Original verifier contains optimization-sensitive assert')
print(json.dumps({'status': 'passed', 'python_optimize': sys.flags.optimize,
                  'original_verifier_sha256': hashlib.sha256(source.encode()).hexdigest(),
                  'mutations_rejected': results,
                  'scope': 'Tests detect listed finite-algebra errors; they cannot validate MSTOP.'}, indent=2))
