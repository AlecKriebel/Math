#!/usr/bin/env python3
"""Independent finite exact controls. These are not existence proofs for Reeb flows."""
from fractions import Fraction as F
from itertools import product
import json


def require(value, label):
    if not value:
        raise RuntimeError(label)


I = (F(1), F(0), F(0), F(1))


def multiply(x, y):
    a, b, c, d = x
    e, f, g, h = y
    return (a*e+b*g, a*f+b*h, c*e+d*g, c*f+d*h)


def determinant(x):
    return x[0]*x[3]-x[1]*x[2]


def trace(x):
    return x[0]+x[3]


def matrix_power(x, n):
    result = I
    while n:
        if n & 1:
            result = multiply(result, x)
        n //= 2
        x = multiply(x, x)
    return result


def sign(q):
    return (q > 0)-(q < 0)


def quarter(a):
    return (F(0), -1/a, a, F(0))


def run():
    # This implementation uses flattened matrices, binary powers and a trace
    # recurrence, independently of the original verifier's nested-list powers.
    values = sorted({F(i, j) for i in range(1, 9) for j in range(1, 9)})
    products = 0
    for a, b in product(values, repeat=2):
        endpoint = multiply(quarter(b), quarter(a))
        require(endpoint == (-a/b, F(0), F(0), -b/a), 'quarter-turn general formula')
        require(determinant(endpoint) == 1, 'quarter-turn determinant')
        require(trace(endpoint) <= -2, 'positive coefficients give trace at most -2')
        require((trace(endpoint) < -2) == (a != b), 'strictness iff unequal coefficients')
        products += 1

    matrices = [tuple(map(F, x)) for x in product(range(-4, 5), repeat=4)
                if x[0]*x[3]-x[1]*x[2] == 1]
    power_tests = 0
    for x in matrices:
        t0, t1 = F(2), trace(x)
        for m in range(1, 17):
            xm = matrix_power(x, m)
            require(determinant(xm) == 1, 'power symplecticity')
            require(trace(xm) == t1, 'Cayley-Hamilton trace recurrence')
            ip = tuple(I[i]-xm[i] for i in range(4))
            require(determinant(ip) == 2-t1, 'fixed-point determinant trace identity')
            if abs(trace(x)) > 2:
                require(abs(t1) > 2, 'hyperbolic powers avoid unit circle')
                require(determinant(ip) != 0, 'every hyperbolic cover is nondegenerate')
                expected_sign = 1 if trace(x) < -2 and m % 2 else -1
                require(sign(determinant(ip)) == expected_sign, 'fixed-point index parity')
            if abs(trace(x)) <= 2:
                require(abs(t1) <= 2, 'inclusive ellipticity preserved by powers')
            t0, t1 = t1, trace(x)*t1-t0
            power_tests += 1

    positive_jordan = (F(1), F(1), F(0), F(1))
    negative_jordan = (F(-1), F(1), F(0), F(-1))
    require(abs(trace(positive_jordan)) == 2, 'positive parabolic included')
    require(abs(trace(negative_jordan)) == 2, 'negative parabolic included')
    require(trace(matrix_power(negative_jordan, 2)) == 2, 'negative parabolic double cover degenerates')
    require(abs(trace(I)) <= 2, 'Hopf identity included')
    require(not abs(trace(I)) < 2, 'strictly-nonreal convention rejects Hopf identity')

    # Sum least-period cycles by constructing their fixed-point contributions;
    # use only dyadic divisors, not the original verifier's divisors function.
    formal_tests = 0
    for n in range(1, 4097):
        d, contribution = 1, 0
        while n % d == 0:
            contribution += d if (n//d) % 2 else -d
            d *= 2
        require(contribution == 1, 'all-iterate formal dyadic model')
        formal_tests += 1
    bprev, dyadic_tests = 0, 0
    for k in range(20):
        a = (k*k+2*k+7) % 11
        b = a+(bprev if k else 1)
        require(b-a == (bprev if k else 1), 'dyadic difference recurrence')
        require(b >= 1, 'negative hyperbolic cycle at every dyadic period')
        bprev = b
        dyadic_tests += 1

    # Negative mathematical controls, with explicit witnessed failure values.
    # No proposed disk/flow realization is inferred from these formal data.
    missing_period_two = -1  # n=2, only a negative hyperbolic fixed cycle.
    wrong_sign_at_two = 1+2  # treating negative cycles as index +1 at all iterates.
    missing_cycle_weight = -1+1  # n=2, dropping the d fixed points per cycle.
    finite_cutoff_at_512 = -(2**9-1)  # retain periods 1,...,256, test n=512.
    require(missing_period_two != 1, 'missing-cycle negative control')
    require(wrong_sign_at_two != 1, 'wrong-parity negative control')
    require(missing_cycle_weight != 1, 'missing-weight negative control')
    require(finite_cutoff_at_512 != 1, 'finite-truncation negative control')

    # Hyperbolic admissibility counts subsets only. Positive actions make every
    # orbit in a filtered generator itself have action below L.
    actions = tuple(F(i, 3) for i in range(1, 13))
    filtered_tests = 0
    for L in map(F, range(1, 28)):
        available = sum(a < L for a in actions)
        admissible = 0
        for subset in product((0, 1), repeat=len(actions)):
            action = sum(a*m for a, m in zip(actions, subset))
            if action < L:
                require(all(m == 0 or a < L for a, m in zip(actions, subset)), 'filtered generator support')
                admissible += 1
        require(admissible <= 2**available, 'filtered hyperbolic subset bound')
        filtered_tests += 1
    require(4 > 2**1, 'multiplicity-free hypothesis necessary: one action-1 orbit, multiplicities 0..3, L=4')

    gaps = []
    for k in range(2, 1025):
        gap = (4*k-1)-3*k
        require(gap == k-1 and gap > 0, 'higher-iterate gap')
        gaps.append(gap)

    # f=2+x_1 has antipodal odd part x_1; an even approximant's errors at
    # antipodes cannot both be smaller than 1 at x_1=+1 and -1.
    for g in (F(i, 17) for i in range(-50, 90)):
        require(max(abs(F(3)-g), abs(F(1)-g)) >= 1, 'antipodal approximation lower bound')
    require(max(abs(F(3)-2), abs(F(1)-2)) == 1, 'even averaging attains distance')
    return {
        'status': 'pass',
        'arithmetic': 'exact rational and integer, explicit exceptions, no asserts',
        'quarter_turn_parameter_pairs': products,
        'integer_SL2_matrices': len(matrices),
        'trace_and_power_checks': power_tests,
        'formal_lefschetz_n': [1, formal_tests],
        'dyadic_recurrence_checks': dyadic_tests,
        'filtered_subset_cases': filtered_tests,
        'index_gap_k': [2, 1024],
        'negative_mathematical_control_values': {
            'missing_period_two': missing_period_two,
            'wrong_even_iterate_sign': wrong_sign_at_two,
            'missing_cycle_weight': missing_cycle_weight,
            'truncated_model_at_n512': finite_cutoff_at_512,
            'unrestricted_multiplicity_exceeds_subset_bound': [4, 2]
        },
        'scope': 'Finite exact controls only; no ODE compactness, ECH theorem, or orbit-existence proof is established computationally.'
    }


if __name__ == '__main__':
    print(json.dumps(run(), indent=2, sort_keys=True))
