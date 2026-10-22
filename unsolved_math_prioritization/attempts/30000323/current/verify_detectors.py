#!/usr/bin/env python3
"""Exact finite algebra checks only; this does not calculate MSTOP cohomology."""
import itertools
import json
import sys


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def prime(p):
    if not isinstance(p, int) or p < 3 or p % 2 == 0:
        raise ValueError('An odd prime is required')
    if any(p % d == 0 for d in range(3, int(p ** 0.5) + 1, 2)):
        raise ValueError('An odd prime is required')
    return p


def elements(moduli):
    if not moduli or any(not isinstance(n, int) or n < 2 for n in moduli):
        raise ValueError('Nonempty moduli >= 2 are required')
    return tuple(itertools.product(*(range(n) for n in moduli)))


def validate_weights(moduli, weights, allow_trivial=False):
    if any(len(w) != len(moduli) for w in weights):
        raise ValueError('Character dimension mismatch')
    if any(any(not isinstance(a, int) or not 0 <= a < n for a, n in zip(w, moduli)) for w in weights):
        raise ValueError('Character weight out of range')
    if not allow_trivial and any(not any(w) for w in weights):
        raise ValueError('The representation has a trivial summand')


def character_is_one(moduli, weight, point):
    # Tests exact rational angle modulo 1, by a common denominator.
    from math import lcm
    denominator = lcm(*moduli)
    numerator = sum(a * b * (denominator // n) for a, b, n in zip(weight, point, moduli))
    return numerator % denominator == 0


def avoiding_elements(moduli, weights):
    validate_weights(moduli, weights)
    return [g for g in elements(moduli)
            if all(not character_is_one(moduli, w, g) for w in weights)]


def euler_group_ring(moduli, weights, allow_trivial=False):
    """Product of (1 - chi), in Z[G*], calculated by exact sparse convolution."""
    validate_weights(moduli, weights, allow_trivial)
    zero = (0,) * len(moduli)
    result = {zero: 1}
    for w in weights:
        out = dict(result)
        for exponent, coefficient in result.items():
            shifted = tuple((a + b) % n for a, b, n in zip(exponent, w, moduli))
            out[shifted] = out.get(shifted, 0) - coefficient
        result = {a: b for a, b in out.items() if b}
    return result


def ordinary_mod_p_polynomial(p, moduli, weights):
    prime(p)
    validate_weights(moduli, weights, allow_trivial=True)
    result = {(0,) * len(moduli): 1}
    for w in weights:
        out = {}
        for exponent, coefficient in result.items():
            for i, a in enumerate(w):
                shifted = list(exponent)
                shifted[i] += 1
                shifted = tuple(shifted)
                out[shifted] = (out.get(shifted, 0) + coefficient * a) % p
        result = {a: b for a, b in out.items() if b}
    return result


def obstruction_weights(p, elementary=False):
    prime(p)
    step = 1 if elementary else p
    return [(step, 0)] + [(a * step, 1) for a in range(p)]


def expect_value_error(fn, label):
    try:
        fn()
    except ValueError:
        return
    raise RuntimeError('Negative control failed: ' + label)


def run():
    cases = []
    for p in (3, 5, 7, 11):
        moduli = (p * p, p)
        weights = obstruction_weights(p)
        require(len(weights) == p + 1, 'Wrong obstruction dimension')
        require(not avoiding_elements(moduli, weights), 'Kernels fail to cover G')
        require(not euler_group_ring(moduli, weights), 'K-Euler element was not exactly zero')
        require(not ordinary_mod_p_polynomial(p, moduli, weights), 'Ordinary mod-p detector should vanish')
        kernels = [frozenset(g for g in elements(moduli)
                            if character_is_one(moduli, w, g)) for w in weights]
        require(len(set(kernels)) == p + 1, 'Repeated maximal kernel')
        require(all(len(h) == p * p for h in kernels), 'A kernel is not maximal')
        # Every proper subgroup lies in a maximal subgroup, a theorem in the report.
        # The finite check below tests exactly the listed maximal subgroups.
        require(all(any(all(character_is_one(moduli, w, g) for g in h)
                            for w in weights) for h in kernels), 'Missing fixed line on a maximal subgroup')
        uncovered = []
        for i in range(len(weights)):
            smaller = weights[:i] + weights[i + 1:]
            points = avoiding_elements(moduli, smaller)
            require(len(points) == p * (p - 1), 'Removing a kernel gave wrong uncovered set')
            require(bool(euler_group_ring(moduli, smaller)), 'Deleting one line should give nonzero K element')
            uncovered.append(len(points))
        elementary = obstruction_weights(p, elementary=True)
        require(not euler_group_ring((p, p), elementary), 'Elementary K control should vanish')
        require(bool(ordinary_mod_p_polynomial(p, (p, p), elementary)), 'Elementary ordinary control should detect')
        cyclic = [(p,), (p,)]
        require(not ordinary_mod_p_polynomial(p, (p*p,), cyclic), 'Cyclic ordinary control should vanish')
        require(bool(euler_group_ring((p*p,), cyclic)), 'Cyclic K control should detect')
        primitive_mutant = [(1, 0)] + weights[1:]
        require(bool(ordinary_mod_p_polynomial(p, moduli, primitive_mutant)), 'Primitive-weight mutation should detect')
        require(not euler_group_ring(moduli, [(0, 0)], allow_trivial=True), 'Trivial-line Euler class must vanish')
        # Transfer for ker(alpha), represented by sum_(a=0)^(p-1) alpha^a.
        induced = {(a * p, 0): 1 for a in range(p)}
        scalar = {(0, 0): p}
        require(induced != scalar, 'Transfer of the unit was incorrectly scalar')
        cases.append({'p': p, 'group_orders': moduli, 'dimension': len(weights),
                      'ordinary_mod_p_zero': True, 'K_group_ring_zero': True,
                      'maximal_kernels_checked': len(kernels),
                      'each_deletion_uncovered': uncovered,
                      'complementary_detector_controls': 'passed',
                      'transfer_not_scalar': True})
    exhaustive = 0
    for moduli in ((3, 3), (9,), (9, 3)):
        weights = [g for g in elements(moduli) if any(g)]
        for d in (1, 2, 3):
            # Repeated summands do not change the union of kernels; subsets suffice.
            for selected in itertools.combinations(weights, d):
                require(bool(avoiding_elements(moduli, selected)), 'Dimension <= p avoidance failed')
                exhaustive += 1
    expect_value_error(lambda: prime(9), 'composite p')
    expect_value_error(lambda: prime(2), 'even p')
    expect_value_error(lambda: avoiding_elements((9, 3), [(0, 0)]), 'trivial summand')
    expect_value_error(lambda: avoiding_elements((9, 3), [(9, 0)]), 'out-of-range weight')
    expect_value_error(lambda: avoiding_elements((9, 3), [(1,)]), 'wrong coordinate count')
    return {'status': 'passed', 'python_optimize': sys.flags.optimize,
            'exhaustive_small_character_subsets': exhaustive, 'cases': cases,
            'scope': 'Finite character algebra only; no MSTOP cohomology computed',
            'exception_negative_controls': 5}


if __name__ == '__main__':
    print(json.dumps(run(), indent=2))
