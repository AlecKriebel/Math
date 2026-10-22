#!/usr/bin/env python3
"""Independent exact certificates; standard library, stdout only, no writes.

This script imports none of the frozen author's code and does not read any
candidate file. Universal deductions are given in REPORT.md; finite recurrence
checks below corroborate the algebra and deliberately test scope failures.
"""
from fractions import Fraction as Q
from math import comb, factorial
import json


def require(condition, message):
    if not condition:
        raise ValueError(message)


def trim(poly):
    result = list(map(Q, poly))
    while result and result[-1] == 0:
        result.pop()
    return tuple(result)


def derivative(poly):
    return trim(i * poly[i] for i in range(1, len(poly)))


def theta(poly):
    return trim(i * poly[i] for i in range(len(poly)))


def value(poly, x):
    result = Q(0)
    for coefficient in reversed(poly):
        result = result * x + coefficient
    return result


def multiply_scale(poly, scale):
    return trim(scale * x for x in poly)


def main():
    # Formal normalization by arbitrary nonzero target b. The source has
    # g/B=z^2/4; B=2b gives g/b=z^2/2, identically, not just numerically.
    source_normalized = (Q(0), Q(0), Q(1, 4))
    g_over_b = multiply_scale(source_normalized, 2)
    gp_over_b = derivative(g_over_b)
    gpp_over_b = derivative(gp_over_b)
    require(g_over_b == (0, 0, Q(1, 2)), 'source specialization')
    require(gp_over_b == (0, 1), 'first derivative')
    require(gpp_over_b == (1,), 'second derivative')
    require(value(gp_over_b, 1) == value(gpp_over_b, 1) == 1,
            'nonvacuous target b-fiber at z=1')
    require(value(gp_over_b, 2) == value(g_over_b, 2) == 2,
            'separate source B-fiber at z=2')
    require(g_over_b != gp_over_b, 'failure of target k=2 identity')
    # Without the parameter conversion B=2b, the neighboring source condition
    # still holds but the target derivative condition fails. This guards the
    # central distinction between the two predicates.
    require(value(derivative(source_normalized), 2) == 1,
            'unscaled target antecedent is attained')
    require(value(derivative(derivative(source_normalized)), 2) != 1,
            'wrong source-parameter transfer must fail')

    # Polynomial family checked with fully expanded nonzero translations.
    polynomial_cases = 0
    for k in range(2, 33):
        for b in (Q(1), Q(-3, 7)):
            for z0 in (Q(0), Q(5, 3)):
                poly = trim(b * Q(comb(k, j), factorial(k)) * (-z0)**(k-j)
                            for j in range(k + 1))
                fp = derivative(poly)
                fk = poly
                for _ in range(k):
                    fk = derivative(fk)
                require(fk == (b,), 'constant kth derivative')
                require(value(poly, z0) == value(fp, z0) == 0,
                        'common root of translated family')
                require(len(poly) == k + 1 and len(fp) == k,
                        'degree and multiplicity difference')
                polynomial_cases += 1

    # Derivative operator on t=exp(lambda*z). The actual lambda factor is
    # external: D_z^k f=lambda^k theta^k((t-1)^2).
    base = (Q(1), Q(-2), Q(1))
    old_A_minus_two = (Q(1), Q(-2), Q(1))
    require(base == old_A_minus_two, '2009 squared-exponential template')
    first = theta(base)
    require(first == (0, -2, 2), 'first theta derivative')
    at_half = Q(1, 2)
    order_records = []
    for k in range(3, 65):
        current = base
        for _ in range(k):
            current = theta(current)
        require(current == (0, -2, 2**k), 'kth theta derivative')
        r = Q(-1, 2**(k-1)-2)  # lambda^(k-1)
        normalized = multiply_scale(current, r)
        require(value(normalized, at_half) == Q(-1, 2),
                'resonant higher-derivative value')
        require(value(derivative(normalized), at_half) != 0,
                'higher-derivative b-fiber has a simple zero')
        require(value(current, at_half) != Q(-1, 2),
                'lambda=1 must fail')
        # Arbitrary b after A=-2b/lambda: f^(k)/b=-2*r*theta^k(base).
        require(value(multiply_scale(current, -2*r), at_half) == 1,
                'arbitrary prescribed nonzero b scaling')
        order_records.append({'k': k, 'lambda_power': str(r),
                              'normalized_value': '-1/2'})

    second = theta(theta(base))
    require(value(second, at_half) == 0, 'k=2 ansatz boundary')
    require(value(second, at_half) != Q(-1, 2),
            'k=2 cannot satisfy this critical-fiber calibration')
    # The b-fiber polynomial normalized by lambda is 2(t-1/2)^2.
    first_minus_b = (Q(1, 2), Q(-2), Q(2))
    require(value(first_minus_b, at_half) == 0 and
            value(derivative(first_minus_b), at_half) == 0 and
            derivative(derivative(first_minus_b)) == (4,),
            'double b-fiber, stronger multiplicity condition excluded')
    print(json.dumps({
        'status': 'PASS',
        'arithmetic': 'fractions.Fraction; no floating point',
        'independent_of_frozen_code': True,
        'file_or_network_writes': False,
        'formal_source_specialization': 'B=2b gives g/b=z^2/2',
        'target_antecedent': 'g_prime=b exactly at z=1',
        'separate_source_antecedent': 'g_prime=B exactly at z=2',
        'wrong_parameter_transfer_rejected': True,
        'expanded_translated_polynomial_cases': polynomial_cases,
        'resonance_orders_checked': len(order_records),
        'resonance_order_range': [3, 64],
        'orders': order_records,
        'negative_controls': ['B=b without rescaling', 'lambda=1',
                              'k=2 squared-exponential calibration',
                              'multiplicity-dominating b-condition'],
        'scope': 'Algebra certificates only; written proof supplies universal claims.'
    }, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
