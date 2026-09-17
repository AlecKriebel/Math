#!/usr/bin/env python3
"""Exact algebra and finite regression audits; not a finite-search proof.

No imports from verify_matrix.py. Uses only Python's standard library.
The universal result is the written proof. Finite probes are diagnostics.
"""
from fractions import Fraction as F
from itertools import product
import json
from math import prod
from pathlib import Path
import random
import sys

VERSION = "1.0.0"
SEED = 20260914
ROOT = Path(__file__).resolve().parents[1]
if hasattr(sys, 'set_int_max_str_digits'):
    sys.set_int_max_str_digits(0)


def require(condition, message):
    if not condition:
        raise AssertionError(message)


# Tiny integer-polynomial arithmetic, with exponent triples as keys.
def add(*polys):
    out = {}
    for poly in polys:
        for exponent, coefficient in poly.items():
            out[exponent] = out.get(exponent, 0) + coefficient
    return {e: c for e, c in out.items() if c}


def scale(poly, factor):
    return {e: c*factor for e, c in poly.items() if c*factor}


def mul(left, right):
    out = {}
    for a, ca in left.items():
        for b, cb in right.items():
            exponent = tuple(x+y for x, y in zip(a, b))
            out[exponent] = out.get(exponent, 0) + ca*cb
    return {e: c for e, c in out.items() if c}


def square(poly):
    return mul(poly, poly)


def symbolic_audit():
    x, y, z = ({(1,0,0): 1}, {(0,1,0): 1}, {(0,0,1): 1})
    x2, y2, z2 = map(square, (x,y,z))
    left = scale(add(mul(x2,y2), mul(x2,z2), mul(y2,z2),
                     scale(mul(mul(mul(x,y),z), add(x,y,z)), -1)), 2)
    right = add(mul(square(add(x,scale(y,-1))), z2),
                mul(square(add(x,scale(z,-1))), y2),
                mul(square(add(y,scale(z,-1))), x2))
    residual = add(left, scale(right,-1))
    require(not residual, 'The polynomial sum-of-squares identity failed')
    return {
        'identity': '2*(x^2*y^2+x^2*z^2+y^2*z^2-x*y*z*(x+y+z)) = (x-y)^2*z^2+(x-z)^2*y^2+(y-z)^2*x^2',
        'coefficient_domain': 'integers',
        'normal_form_residual': [],
        'left_and_right_common_terms': [
            {'exponents_xyz': list(e), 'coefficient': c}
            for e,c in sorted(left.items())],
        'verified': True,
        'scope': 'An exact polynomial identity, not a finite evaluation test.'
    }


def control_audit():
    A = json.loads((ROOT/'certificates/source_two_rows.json').read_text())['matrix']
    flat = [a for row in A for a in row]
    require(len(flat) == len(set(flat)) == 20, 'Source distinctness failure')
    require(all(type(a) is int and a>0 for a in flat), 'Source positivity failure')
    rows = [sum(row) for row in A]
    columns = [prod(A[i][j] for i in range(len(A))) for j in range(len(A[0]))]
    require(rows == [840,840] and columns == [840]*10, 'Source arithmetic failure')
    reciprocal_sum = sum((F(1,a) for a in flat), F(0))
    require(reciprocal_sum == 2, 'Two-row reciprocal identity failure')
    B = json.loads((ROOT/'certificates/repeated_three_rows.json').read_text())['matrix']
    repeated_total = sum((F(sum(c),prod(c)) for c in zip(*B)), F(0))
    repeated_square_sum = sum((F(1,a*a) for row in B for a in row), F(0))
    require(repeated_total == repeated_square_sum == 3,
            'Repeated-entry adversarial control failed')
    # The three-row inverse-square bound must NOT be used for two rows.
    a,b = A[0][0], A[1][0]
    require(F(a+b,a*b) > F(1,a*a)+F(1,b*b),
            'Expected a counterexample to the incorrect two-row bound')
    return {'source_row_sums': rows, 'source_column_products': columns,
            'source_distinct_count': len(set(flat)),
            'source_reciprocal_sum': str(reciprocal_sum),
            'repeated_3_by_4_total': str(repeated_total),
            'repeated_3_by_4_inverse_square_sum': str(repeated_square_sum),
            'incorrect_two_row_inverse_square_bound_rejected_on_column': [a,b],
            'independent_of_matrix_checker': True}


def finite_audit():
    triple_count = 0
    # All ORDERED triples from 1..40, including repeats and the entry 1.
    for x,y,z in product(range(1,41), repeat=3):
        gap_numerator = x*x*y*y+x*x*z*z+y*y*z*z-x*y*z*(x+y+z)
        squares = (x-y)**2*z*z+(x-z)**2*y*y+(y-z)**2*x*x
        require(2*gap_numerator == squares >= 0, 'Triple identity/inequality failed')
        triple_count += 1

    # Exact reciprocal-square bound on every nonempty subset of {1,...,12}.
    subset_sums = [F(0)] * (1<<12)
    for mask in range(1,1<<12):
        low = mask & -mask
        value = low.bit_length()
        subset_sums[mask] = subset_sums[mask ^ low] + F(1,value*value)
        k = mask.bit_count()
        require(subset_sums[mask] <= 2-F(1,k) < 2, 'Distinct-set bound failed')

    square_sum, telescoping = F(0), F(1)
    for M in range(1,513):
        square_sum += F(1,M*M)
        if M>=2:
            telescoping += F(1,M*(M-1))
        require(telescoping == 2-F(1,M), 'Telescoping identity failed')
        require(square_sum <= telescoping < 2, 'Reciprocal-square bound failed')

    rng = random.Random(SEED)
    arrays_tested, columns_tested = 0, 0
    largest_normalized_sum = F(0)
    for m in range(3,13):
        for n in range(1,13):
            for trial in range(3):
                if trial == 0:
                    values = list(range(1,m*n+1))
                elif trial == 1:
                    values = rng.sample(range(1,10001), m*n)
                else:
                    values = [1] + rng.sample(range(2,10001), m*n-1)
                rng.shuffle(values)
                A = [values[i*n:(i+1)*n] for i in range(m)]
                weighted_sum = F(0)
                square_sum = sum((F(1,a*a) for a in values), F(0))
                for c in zip(*A):
                    P = prod(c)
                    x,y,z = c[:3]
                    outside = prod(c[3:])
                    require(outside>=1 and P==x*y*z*outside,
                            'Higher-row reduction failed')
                    lhs = F(x+y+z, P)
                    pairs = F(1,x*y)+F(1,x*z)+F(1,y*z)
                    squares = F(1,x*x)+F(1,y*y)+F(1,z*z)
                    require(lhs <= pairs <= squares, 'Three-row inequality failed')
                    # Separate all-row argument using cyclic pairs.
                    normalized = F(sum(c),P)
                    cyclic = sum((F(1,c[(i+1)%m]*c[(i+2)%m])
                                  for i in range(m)),F(0))
                    column_squares = sum((F(1,a*a) for a in c),F(0))
                    require(normalized <= cyclic <= column_squares,
                            'All-row cyclic inequality failed')
                    weighted_sum += normalized
                    columns_tested += 1
                require(weighted_sum <= square_sum <= 2-F(1,m*n) < 2,
                        'Array-wide distinctness bound failed')
                largest_normalized_sum = max(largest_normalized_sum,weighted_sum)
                arrays_tested += 1

    # A separate exact probe with 100-digit entries.
    x,y,z = 10**100+3,10**100+7,10**100+11
    require(F(1,x*y)+F(1,x*z)+F(1,y*z) <= F(1,x*x)+F(1,y*y)+F(1,z*z),
            'Large-integer rational audit failed')
    return {'ordered_triples': {'entry_range': [1,40], 'cases': triple_count},
            'distinct_sets': {'universe': [1,12], 'nonempty_subsets': (1<<12)-1},
            'telescoping': {'M_range': [1,512], 'cases':512},
            'higher_row_array_audit': {'m_range':[3,12], 'n_range':[1,12],
                                      'trials_per_shape':3, 'arrays':arrays_tested,
                                      'columns':columns_tested, 'seed':SEED,
                                      'random_entry_range':[1,10000],
                                      'consecutive_entry_trials':True,
                                      'largest_normalized_sum':str(largest_normalized_sum)},
            'large_integer_probe_digits':101,
            'all_passed':True,
            'warning':'These finite checks are regression tests, not the proof of universal nonexistence.'}


def main():
    symbolic = symbolic_audit()
    stored = json.loads((ROOT/'certificates/sum_of_squares_identity.json').read_text())
    require(symbolic == stored, 'Stored symbolic certificate differs from recomputation')
    result = {'audit_version': VERSION, 'status':'passed',
              'symbolic_certificate': symbolic,
              'independent_controls': control_audit(),
              'finite_regressions': finite_audit()}
    print(json.dumps(result,indent=2))


if __name__=='__main__':
    main()
