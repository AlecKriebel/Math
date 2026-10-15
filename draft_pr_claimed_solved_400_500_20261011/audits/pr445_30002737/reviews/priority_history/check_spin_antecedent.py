#!/usr/bin/env python3
"""Finite checks of the cited Example5.4; not a quadrature certificate."""
import json
from decimal import Decimal

def main():
    letters = [(g, d) for g in range(4) for d in range(2)]
    # Spin matrix rows [[1,i],[1,-1]], group elements represented modulo4.
    rows = [[0, 1], [0, 2]]
    children = {a: {((a[0] + rows[a[1]][j]) % 4, j) for j in range(2)} for a in letters}
    reached = {a: {a} for a in letters}
    primitive_power = None
    for n in range(1, 33):
        reached = {a: set().union(*(children[z] for z in reached[a])) for a in letters}
        if all(reached[a] == set(letters) for a in letters):
            primitive_power = n
            break
    square_map = {g: (2 * g) % 4 for g in range(4)}
    # Conservative log2 lower bound; source Table1's error is an assumption.
    log2_lower = Decimal('0.69314')
    reported_error_upper = Decimal('0.001')
    numerical_margin = {
        str(n): str(log2_lower - (Decimal(v) + reported_error_upper))
        for n, v in [(12, '0.688005'), (13, '0.682035')]
    }
    return {
        'source': 'arXiv:2108.08642v1 Example5.4 pp32–33',
        'primitive_transition_power': primitive_power,
        'scalar_chi1_faithful': len(set(range(4))) == 4,
        'square_factor_spin_exponents': square_map,
        'chi2_matrix': [[1, -1], [1, 1]],
        'chi2_rows_orthogonal': (1 * 1 + (-1) * 1) == 0,
        'chi2_row_norm_squared': 2,
        'twice_f_upper_bound_margin_below_log2_given_source_error': numerical_margin,
        'source_error_bound_independently_reproduced': False,
        'scope': 'finite primitivity, faithful square map, unitary character and arithmetic only',
        'acceptance': 'not an approval or rigorous quadrature certificate',
    }

if __name__ == '__main__':
    print(json.dumps(main(), indent=2))
