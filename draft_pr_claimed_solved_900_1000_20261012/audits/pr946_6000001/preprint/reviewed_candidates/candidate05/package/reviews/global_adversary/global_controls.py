#!/usr/bin/env python3
"""Independent global adversarial controls for the frozen PR946 theorem.

Python standard library only. Exact rational arithmetic verifies the explicit
compact model and scalar coefficients of the noncompact model. The global
arguments and the precise limitations are in FULL_REPORT.md. No original
author/audit program is imported or run, and this script has no network access.
"""
from fractions import Fraction as F
from pathlib import Path
import datetime
import json
import platform


def require(condition, description):
    if not condition:
        raise RuntimeError(description)


def add(*polynomials):
    result = {}
    for polynomial in polynomials:
        for exponent, coefficient in polynomial.items():
            result[exponent] = result.get(exponent, F(0)) + coefficient
    return {e: c for e, c in result.items() if c}


def scale(polynomial, scalar):
    return {e: scalar * c for e, c in polynomial.items() if scalar * c}


def multiply(left, right):
    result = {}
    for e, c in left.items():
        for f, d in right.items():
            exponent = tuple(a + b for a, b in zip(e, f))
            result[exponent] = result.get(exponent, F(0)) + c * d
    return {e: c for e, c in result.items() if c}


def derivative(polynomial, axis):
    result = {}
    for e, c in polynomial.items():
        if e[axis]:
            target = list(e)
            target[axis] -= 1
            result[tuple(target)] = c * e[axis]
    return result


def evaluate(polynomial, point):
    total = F(0)
    for exponent, coefficient in polynomial.items():
        term = coefficient
        for x, degree in zip(point, exponent):
            term *= x ** degree
        total += term
    return total


def determinant(matrix):
    matrix = [[F(v) for v in row] for row in matrix]
    value = F(1)
    for column in range(len(matrix)):
        pivot = next((r for r in range(column, len(matrix)) if matrix[r][column]), None)
        if pivot is None:
            return F(0)
        if pivot != column:
            matrix[column], matrix[pivot] = matrix[pivot], matrix[column]
            value = -value
        diagonal = matrix[column][column]
        value *= diagonal
        for r in range(column + 1, len(matrix)):
            ratio = matrix[r][column] / diagonal
            for c in range(column + 1, len(matrix)):
                matrix[r][c] -= ratio * matrix[column][c]
            matrix[r][column] = F(0)
    return value


def pairing(left, matrix, right):
    return sum(left[i] * matrix[i][j] * right[j]
               for i in range(len(left)) for j in range(len(right)))


def strings(matrix):
    return [[str(entry) for entry in row] for row in matrix]


# Coordinates (x,y,u,v), complex z1=x+iy, z2=u+iv.
one = {(0, 0, 0, 0): F(1)}
coordinates = [{tuple(int(i == j) for i in range(4)): F(1)} for j in range(4)]
x, y, u, v = coordinates
x2, y2 = multiply(x, x), multiply(y, y)
q1 = add(x2, y2, scale(one, -1))
q2 = add(u, scale(x2, -1), y2)
q3 = add(v, scale(multiply(x, y), -2))
imaginary = add(multiply(v, add(x2, scale(y2, -1))),
                scale(multiply(multiply(u, x), y), -2))
psi = add(scale(q1, F(1, 2)), scale(imaginary, -1),
          scale(add(*(multiply(q, q) for q in (q1, q2, q3))), 100))
gradient = [derivative(psi, j) for j in range(4)]
hessian = [[derivative(gradient[i], j) for j in range(4)] for i in range(4)]
p = [F(1), F(0), F(1), F(0)]
q = [F(0), F(1), F(-1), F(0)]
hp = [[evaluate(entry, p) for entry in row] for row in hessian]
phi = [evaluate(entry, p) for entry in gradient]
minors = [determinant([row[:k] for row in hp[:k]]) for k in range(1, 5)]
require(all(m > 0 for m in minors), "Compact model Hessian is not positive at base point")
tangent = [0, 1, 0, 2]
acceleration = [-1, 0, -4, 0]
g = pairing(tangent, hp, tangent)
gamma = pairing(acceleration, hp, tangent)
require(g == 1 and gamma == -6, "Ordered circle metric/connection mismatch")
require(evaluate(psi, p) == evaluate(psi, q) == 0, "Circle potential mismatch")
chord = [b - a for a, b in zip(p, q)]
midpoint = [(a + b) / 2 for a, b in zip(p, q)]
hm = [[evaluate(entry, midpoint) for entry in row] for row in hessian]
support = sum(a * b for a, b in zip(phi, chord))
midpoint_second = pairing(chord, hm, chord)
require(support == 1, "Convex-support negative control lost")
require(midpoint_second == -798, "Nonconvexity negative control lost")

# Noncompact parabola model. Differentiation of exp(-x)*P(x,y) is exact
# polynomial differentiation with the twisted x derivative (partial_x-1).
a = {(1, 0): F(1)}
b = {(0, 1): F(1)}
unit2 = {(0, 0): F(1)}
qxy = add(multiply(a, a), scale(b, -1))
polynomial_part = add(scale(qxy, F(1, 2)), multiply(qxy, qxy))


def weighted_derivative(polynomial, axis):
    ordinary = derivative(polynomial, axis)
    return add(ordinary, scale(polynomial, -1)) if axis == 0 else ordinary


hn = [[weighted_derivative(weighted_derivative(polynomial_part, i), j)
       for j in range(2)] for i in range(2)]
det_xy = add(multiply(hn[0][0], hn[1][1]), scale(multiply(hn[0][1], hn[1][0]), -1))
expected_det_xy = add(scale(multiply(qxy, qxy), -2), scale(qxy, 7), scale(unit2, F(7, 4)))
require(det_xy == expected_det_xy, "Differentiated noncompact determinant mismatch")
require(hn[1][1] == scale(unit2, 2), "Noncompact normal positivity mismatch")


def on_parabola(polynomial):
    result = {}
    for exponent, coefficient in polynomial.items():
        degree = (exponent[0] + 2 * exponent[1],)
        result[degree] = result.get(degree, F(0)) + coefficient
    return {e: c for e, c in result.items() if c}


z = {(1,): F(1)}
constant = {(0,): F(1)}
hn_on_curve = [[on_parabola(entry) for entry in row] for row in hn]
velocity = [constant, scale(z, 2)]
metric_normalized = add(*(multiply(multiply(velocity[i], hn_on_curve[i][j]), velocity[j])
                          for i in range(2) for j in range(2)))
gamma_normalized = scale(add(*(multiply(hn_on_curve[1][j], velocity[j]) for j in range(2))), 2)
require(metric_normalized == constant, "Differentiated noncompact metric mismatch")
require(gamma_normalized == constant, "Differentiated noncompact connection mismatch")

# A second scalar reduction makes the positivity domain easy to check by hand.
Fq = add(scale(z, F(1, 2)), multiply(z, z))
Fprime = derivative(Fq, 0)
det_normalized = add(scale(Fq, 2), scale(Fprime, 4),
                     scale(multiply(Fprime, Fprime), -1))
require(det_normalized == {(2,): F(-2), (1,): F(7), (0,): F(7, 4)},
        "Noncompact determinant formula mismatch")
require(evaluate(det_normalized, [F(0)]) == F(7, 4), "Noncompact base positivity failed")

output = {
    'status': 'PASS',
    'utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'python': platform.python_version(),
    'arithmetic': 'exact rational; Python standard library only',
    'compact_circle': {
        'hessian_at_theta_zero': strings(hp),
        'leading_principal_minors': [str(m) for m in minors],
        'gradient_at_theta_zero': [str(e) for e in phi],
        'metric': str(g),
        'ordered_connection_coefficients': [str(gamma), str(-gamma)],
        'parallel_transport_around_positive_loop': ['exp(12*pi)', 'exp(-12*pi)'],
        'global_positivity_argument': 'Orthogonal U(1) action preserves Psi and acts transitively on circle; Hessians conjugate.',
        'convex_support_violation': str(support),
        'chord_midpoint_directional_hessian': str(midpoint_second),
    },
    'noncompact_parabola': {
        'determinant_divided_by_exp_minus_2x': '-2*q^2+7*q+7/4',
        'positive_domain': '(7-sqrt(63))/4 < x^2-y < (7+sqrt(63))/4',
        'metric': 'exp(-x)*dx^2',
        'ordered_connection_coefficients': ['1', '-2'],
        'positive_end_length_from_zero': '2',
        'normalized_cubic': '-3*exp(x/2)',
        'global_positivity_argument': 'H_yy=2*exp(-x)>0 and determinant positive on stated domain.',
    },
    'limitations': [
        'Explicit models falsify proposed obstruction mechanisms; they do not prove universal realization.',
        'Completeness and convexity controls constrain additional requirements or these fixed models, not all possible embeddings.',
        'The full theorem requires the independently reviewed arguments and standard topology dependencies in FULL_REPORT.md.',
    ],
}
destination = Path(__file__).with_name('GLOBAL_CONTROLS.json')
destination.write_text(json.dumps(output, indent=2) + '\n')
print(json.dumps(output, indent=2))
