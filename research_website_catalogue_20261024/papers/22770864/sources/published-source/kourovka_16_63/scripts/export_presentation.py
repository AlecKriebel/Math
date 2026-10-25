#!/usr/bin/env python3
"""Export an exact, portable finite Lie-ring / BCH group specification.
Requires NumPy and the independently regenerable Lie coefficient archive.
Integers in JSON must be read by an arbitrary-precision JSON implementation.
"""
from __future__ import annotations
import json
from pathlib import Path
import numpy as np
from lie31 import D, adapted_basis

def main() -> None:
    root = Path(__file__).resolve().parents[1]
    archive = np.load(root / 'data/lie31_tables.npz')
    ca, weights = archive['Ca'], archive['weights']
    _, _, expected_weights, basis = adapted_basis()
    if not np.array_equal(weights, expected_weights):
        raise ValueError('Unexpected lattice weights')
    p, depth, class_bound = 1009, 1689, 846
    terms = []
    for i in range(D):
        for j in range(i + 1, D):
            for k in np.flatnonzero(ca[i, j]):
                power = 2 + int(weights[i]) + int(weights[j]) - int(weights[k])
                if not 0 <= power <= 6:
                    raise ValueError('Nonintegral or unexpected scaled bracket')
                terms.append([i, j, int(k), int(ca[i, j, k]) * p**power])
    result = {
        'format': 'exact-finite-lie-ring-bch-group-v1',
        'problem': 'Kourovka Notebook 16.63 (D. MacHale)',
        'prime': p,
        'coefficient_ring': {'type': 'integers_mod_prime_power', 'prime': p, 'exponent': depth},
        'rank': D,
        'ambient_basis_b': basis,
        'weights_w': [int(x) for x in weights],
        'lie_basis_definition': 'ell[j] = p^(2+w[j]) * b[j]',
        'coordinate_convention': 'Elements are 31-tuples in the ordered ell basis; indices start at zero.',
        'bracket_convention': '[ell[i],ell[j]] = sum_k coefficient(i,j,k)*ell[k]; omitted terms vanish; reverse inputs negate; diagonal brackets vanish.',
        'bracket_terms_i_lt_j': terms,
        'integer_encoding_warning': 'Coefficients are exact JSON integers, some larger than 2^53; use an arbitrary-precision parser, not floating point.',
        'group_multiplication': {
            'operation': 'Baker-Campbell-Hausdorff',
            'maximum_bracket_length': class_bound,
            'exact_definition': 'Take degrees 1 through 846 of log(exp(X)exp(Y)) in the free associative algebra over Q. Apply the right-normed Dynkin operator divided by homogeneous degree to express each term as a Lie polynomial. Evaluate with the displayed bracket modulo p^1689.',
            'denominators': 'Only prime factors at most 846 occur; invert them in Z/(1009^1689).',
            'identity': [0] * D,
            'inverse': 'Coordinate-wise additive negation modulo p^1689'
        },
        'proved_nilpotency_class_upper_bound': class_bound,
        'group_order': {'base': p, 'exponent': D * depth},
        'full_automorphism_order': {'base': p, 'exponent': 30 * depth + 1689},
        'derivation_matrix': {
            'shape': [D * D * (D - 1) // 2, D * D],
            'rank': 931,
            'nullity': 30,
            'smith_valuation_multiplicities_at_prime': {'0': 87, '1': 55, '2': 758, '3': 6, '4': 25},
            'sum_of_nonzero_smith_valuations': 1689
        },
        'proof': 'report/kourovka_16_63.pdf and report/kourovka_16_63.tex',
        'verification_command': 'python3 scripts/resume.py',
        'verification_boundary': 'The group is specified by a finite canonical BCH polynomial; that polynomial and a Cayley table have not been explicitly expanded. The full automorphism count follows from the proof and exact matrix certificates, not group enumeration.'
    }
    target = root / 'data/group_lie_presentation.json'
    target.write_text(json.dumps(result, indent=2) + '\n')
    plan = json.loads((root / 'data/smith_pivot_plan.json').read_text())
    text = str(len(plan)) + '\n' + ''.join(f"{r['row']} {r['col']} {r['valuation']}\n" for r in plan)
    (root / 'data/smith_pivot_plan.txt').write_text(text)
    print(json.dumps({'file': str(target.relative_to(root)), 'bracket_terms': len(terms),
                      'pivot_plan_records': len(plan), 'group_order_exponent': D * depth,
                      'full_automorphism_order_exponent': 30 * depth + 1689}, indent=2))

if __name__ == '__main__':
    main()
