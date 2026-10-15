#!/usr/bin/env python3
"""Independent exact-rational checks of the stochastic proof's finite algebra.

These checks do not certify the infinite-dimensional approximation argument.
Only Python's standard library is required.
"""
from fractions import Fraction as F
import json


def matrix(rows):
    return [[F(x) for x in row] for row in rows]


def transpose(a):
    return [list(row) for row in zip(*a)]


def add(a, b):
    return [[x + y for x, y in zip(ar, br)] for ar, br in zip(a, b)]


def scale(c, a):
    return [[c * x for x in row] for row in a]


def multiply(a, b):
    bt = transpose(b)
    return [[sum(x * y for x, y in zip(ar, bc)) for bc in bt] for ar in a]


def trace(a):
    return sum(a[i][i] for i in range(len(a)))


def identity(n):
    return matrix([[int(i == j) for j in range(n)] for i in range(n)])


def inverse(a):
    n = len(a)
    rows = [ar[:] + er[:] for ar, er in zip(a, identity(n))]
    for k in range(n):
        pivot = next(j for j in range(k, n) if rows[j][k])
        rows[k], rows[pivot] = rows[pivot], rows[k]
        rows[k] = [x / rows[k][k] for x in rows[k]]
        for j in range(n):
            if j != k:
                c = rows[j][k]
                rows[j] = [x - c * y for x, y in zip(rows[j], rows[k])]
    return [r[n:] for r in rows]


def determinant(a):
    n = len(a)
    if n == 1:
        return a[0][0]
    return sum((-1) ** j * a[0][j] * determinant(
        [row[:j] + row[j + 1:] for row in a[1:]]) for j in range(n))


def chain(*args):
    out = args[0]
    for a in args[1:]:
        out = multiply(out, a)
    return out


def zero(a):
    return all(x == 0 for row in a for x in row)


checks = {}

# A nonsymmetric generator derivative and noncommuting Q, B, D.
A = matrix([[1, -2, 0], [0, -1, 1], [1, 0, -3]])
B = matrix([[1, 0], [1, 2], [0, 1]])
K = matrix([[2, 1, 0], [1, 2, 1], [0, 1, 2]])
Q = multiply(K, K)
D = matrix([[4, 1], [1, 3]])
M = inverse(D)
Bt = transpose(B)
AB = multiply(A, B)
Dprime = scale(2, chain(Bt, Q, B))
Mprime = scale(-1, chain(M, Dprime, M))
psi = chain(B, M, Bt)
psi_prime = add(add(chain(AB, M, Bt), chain(B, Mprime, Bt)),
                chain(B, M, transpose(AB)))
riccati = add(add(multiply(A, psi), multiply(psi, transpose(A))),
               scale(-2, chain(psi, Q, psi)))
checks['riccati_with_nonsymmetric_A_noncommuting_Q'] = zero(
    add(psi_prime, scale(-1, riccati)))
checks['logdet_derivative_normalization'] = (
    trace(chain(M, Dprime)) / 2 == trace(multiply(Q, psi)))

# Real Hilbert--Schmidt coordinate noise. X=R^2 and Q=K^2 make exact roots.
R = matrix([[2, 0, 1], [0, 1, 0], [1, 0, 2]])
X = multiply(R, R)
v = multiply(B, Bt)
noise_coefficients = []
combined_equal = True
for i in range(3):
    for j in range(3):
        E = matrix([[int(r == i and c == j) for c in range(3)] for r in range(3)])
        coefficient = trace(chain(v, R, E, K)) + trace(chain(v, K, transpose(E), R))
        combined_equal &= coefficient == 2 * trace(chain(K, v, R, E))
        noise_coefficients.append(coefficient)
bracket = sum(c * c for c in noise_coefficients)
checks['two_noise_terms_combine'] = combined_equal
checks['factor_four_bracket'] = bracket == 4 * trace(chain(X, v, Q, v))

# Drift of exp(-phi - tr(psi X)) with backward Riccati test.
alpha = F(-7, 3)
alpha_term = alpha * trace(multiply(Q, psi))
trace_drift = alpha_term + trace(chain(X, add(
    add(multiply(A, psi), multiply(psi, transpose(A))), scale(-1, psi_prime))))
exponent_drift = alpha_term - trace_drift
half_bracket = 2 * trace(chain(X, psi, Q, psi))
checks['ito_drift_cancellation_even_negative_alpha'] = exponent_drift + half_bracket == 0

# Resolvent and determinant matching, both nonsingular and singular v.
C = matrix([[2, 1], [1, 3]])
for name, root in [('positive', matrix([[2, 1], [1, 2]])),
                   ('singular', matrix([[1, 0], [0, 0]]))]:
    V = multiply(root, root)
    sym_D = add(identity(2), scale(2, chain(root, C, root)))
    nonsym_D = add(identity(2), scale(2, multiply(C, V)))
    lhs = chain(root, inverse(sym_D), root)
    rhs = multiply(V, inverse(nonsym_D))
    checks[f'resolvent_identity_{name}_v'] = lhs == rhs
    checks[f'determinant_identity_{name}_v'] = determinant(sym_D) == determinant(nonsym_D)
    checks[f'resolvent_is_symmetric_{name}_v'] = rhs == transpose(rhs)

out = {
    'method': 'standard-library exact rational arithmetic; no floating point',
    'check_count': len(checks),
    'passed_count': sum(checks.values()),
    'all_passed': all(checks.values()),
    'checks': checks,
    'quadratic_variation_example_exact': str(bracket),
    'limitation': 'Finite algebra only. Infinite-dimensional stochastic analysis is derived separately in REPORT.md.'
}
print(json.dumps(out, indent=2, sort_keys=True))
if not all(checks.values()):
    raise SystemExit(1)
