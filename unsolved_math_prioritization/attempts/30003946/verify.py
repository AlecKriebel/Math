#!/usr/bin/env python3
"""Exact finite algebra checks only; does not certify the conjecture or PDE arguments.

Standard library only. No writes, network, third-party imports or optimization-
sensitive assertions. A deliberate failing check is available for guard testing.
"""
from fractions import Fraction as Q
from itertools import product
import argparse
import json
import sys


def require(condition, message):
    if not condition:
        raise ValueError(message)


class Polynomial:
    def __init__(self, n, terms=None):
        self.n = n
        self.terms = {}
        for powers, coefficient in (terms or {}).items():
            require(len(powers) == n, 'wrong monomial dimension')
            require(all(type(v) is int and v >= 0 for v in powers), 'invalid powers')
            coefficient = Q(coefficient)
            if coefficient:
                self.terms[tuple(powers)] = coefficient

    @classmethod
    def constant(cls, n, c):
        return cls(n, {(0,) * n: Q(c)})

    @classmethod
    def variable(cls, n, i):
        powers = [0] * n
        powers[i] = 1
        return cls(n, {tuple(powers): 1})

    def cast(self, other):
        if isinstance(other, Polynomial):
            require(self.n == other.n, 'polynomial dimension mismatch')
            return other
        return Polynomial.constant(self.n, other)

    def __add__(self, other):
        other = self.cast(other)
        terms = self.terms.copy()
        for powers, coefficient in other.terms.items():
            terms[powers] = terms.get(powers, Q(0)) + coefficient
        return Polynomial(self.n, terms)

    __radd__ = __add__

    def __neg__(self):
        return Polynomial(self.n, {p: -c for p, c in self.terms.items()})

    def __sub__(self, other):
        return self + (-self.cast(other))

    def __rsub__(self, other):
        return self.cast(other) - self

    def __mul__(self, other):
        other = self.cast(other)
        terms = {}
        for p, a in self.terms.items():
            for q, b in other.terms.items():
                r = tuple(i + j for i, j in zip(p, q))
                terms[r] = terms.get(r, Q(0)) + a * b
        return Polynomial(self.n, terms)

    __rmul__ = __mul__

    def __pow__(self, power):
        require(type(power) is int and power >= 0, 'invalid polynomial power')
        result = Polynomial.constant(self.n, 1)
        for _ in range(power):
            result = result * self
        return result

    def derivative(self, i):
        require(type(i) is int and 0 <= i < self.n, 'invalid derivative index')
        terms = {}
        for powers, coefficient in self.terms.items():
            if powers[i]:
                new = list(powers)
                new[i] -= 1
                terms[tuple(new)] = coefficient * powers[i]
        return Polynomial(self.n, terms)

    def evaluate(self, values):
        require(len(values) == self.n, 'wrong evaluation dimension')
        total = Q(0)
        for powers, coefficient in self.terms.items():
            term = coefficient
            for value, power in zip(values, powers):
                term *= Q(value) ** power
            total += term
        return total

    def __eq__(self, other):
        other = self.cast(other)
        return self.terms == other.terms


def verify(negative_control=False):
    checks = []

    def check(name, condition):
        require(condition, name)
        checks.append(name)

    x, t = [Polynomial.variable(2, i) for i in range(2)]
    normal = x
    tangential = t ** 3 - t - 3 * t * x ** 2
    lap = lambda p: p.derivative(0).derivative(0) + p.derivative(1).derivative(1)
    check('flat_normal_harmonic', lap(normal) == 0)
    check('flat_tangential_harmonic', lap(tangential) == 0)
    check('flat_normal_inward_derivative', normal.derivative(0) == 1)
    check('flat_tangential_normal_derivative', tangential.derivative(0) == -6 * t * x)
    edge_flux = tangential.derivative(0)
    check('flat_edge_flux_identically_zero', all(p[0] > 0 for p in edge_flux.terms))
    jac = (normal.derivative(0) * tangential.derivative(1)
           - normal.derivative(1) * tangential.derivative(0))
    check('flat_jacobian_identity', jac == 3 * t ** 2 - 1 - 3 * x ** 2)
    check('flat_negative_interior_jacobian', jac.evaluate([Q(1, 4), 0]) == Q(-19, 16))
    check('flat_positive_interior_jacobian', jac.evaluate([Q(1, 4), 1]) == Q(29, 16))
    check('chosen_points_inside_radius_two', Q(1, 16) + 1 < 4)

    a, b, c, d = [Polynomial.variable(4, i) for i in range(4)]
    energy = a ** 2 + b ** 2 + c ** 2 + d ** 2
    determinant = a * d - b * c
    defect = (a - d) ** 2 + (b + c) ** 2
    check('energy_area_polynomial_identity', energy - 2 * determinant == defect)
    # Independent rational-value check of the coefficient identity.
    count = 0
    for values in product([Q(-2), Q(-1, 3), Q(0), Q(1, 2), Q(3)], repeat=4):
        aa, bb, cc, dd = values
        direct = aa * aa + bb * bb + cc * cc + dd * dd - 2 * (aa * dd - bb * cc)
        require(direct == (aa - dd) ** 2 + (bb + cc) ** 2, 'direct identity regression')
        count += 1
    check('625_rational_matrix_regressions', count == 625)

    # Formal trig differentiation: D(s)=c, D(c)=-s.
    s, c = [Polynomial.variable(2, i) for i in range(2)]
    derivative = lambda p: p.derivative(0) * c - p.derivative(1) * s
    bump = 2 * s ** 2
    check('cusp_bump_first_derivative', derivative(bump) == 4 * s * c)
    check('cusp_bump_second_derivative', derivative(derivative(bump)) == 4 * (c ** 2 - s ** 2))
    check('cusp_trig_bound_identity', (s ** 2 + c ** 2) ** 2 - 4 * s ** 2 * c ** 2 == (s ** 2 - c ** 2) ** 2)
    check('cusp_derivative_extremes', (1 + 2 * Q(-1), 1 + 2 * Q(1)) == (-1, 3))
    check('cusp_energy_bound_constant', 1 + max(Q(-1) ** 2, Q(3) ** 2) == 10)
    check('cusp_nonharmonic_residual_numerator', 1 - Q(3) ** 2 == -8)
    check('identity_energy_density', Q(1) ** 2 + Q(1) ** 2 == 2)

    if negative_control:
        # This must fail under normal Python, -O and -OO alike.
        check('deliberately_false_jacobian_identity', jac == 3 * t ** 2 + 1 - 3 * x ** 2)
    return {'status': 'pass', 'checks': len(checks), 'check_names': checks,
            'rational_matrix_cases': count, 'optimization_level': sys.flags.optimize,
            'scope': 'finite algebra checks; not a proof of the conjecture'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--negative-control', action='store_true')
    args = parser.parse_args()
    try:
        result = verify(args.negative_control)
    except (ValueError, TypeError, ArithmeticError) as error:
        print(json.dumps({'status': 'fail', 'error': str(error),
                          'optimization_level': sys.flags.optimize}, sort_keys=True))
        return 1
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
