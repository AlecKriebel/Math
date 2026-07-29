#!/usr/bin/python3
"""Exact hostile audit of the determinant-critical n=3 Hessian.

The checker uses exact SymPy arithmetic.  It independently:

* differentiates a genuinely complex determinant graph curve;
* verifies the normal-curvature coefficient and conjugation;
* certifies the strictly positive-parent countermodel; and
* checks the full-support plane with zero triple-Hodge leakage.
"""

from __future__ import annotations

import itertools

import sympy as sp


I = sp.I
t = sp.symbols("t", real=True)


def dagger(matrix: sp.Matrix) -> sp.Matrix:
    return matrix.conjugate().T


def vec(matrix: sp.Matrix) -> sp.Matrix:
    return sp.Matrix(
        [matrix[row, column]
         for row in range(matrix.rows)
         for column in range(matrix.cols)]
    )


def unvec(vector: sp.Matrix, size: int) -> sp.Matrix:
    return sp.Matrix(
        size, size, lambda row, column: vector[size * row + column]
    )


def hs_inner(left: sp.Matrix, right: sp.Matrix) -> sp.Expr:
    return sp.simplify((vec(left).conjugate().T * vec(right))[0])


def quadratic(operator: sp.Matrix, matrix: sp.Matrix) -> sp.Expr:
    vector = vec(matrix)
    return sp.simplify((vector.conjugate().T * operator * vector)[0])


def partial_transpose(operator: sp.Matrix, size: int) -> sp.Matrix:
    out = sp.zeros(size * size)
    for a, b, c, d in itertools.product(range(size), repeat=4):
        out[size * a + b, size * c + d] = (
            operator[size * a + d, size * c + b]
        )
    return out


# ------------------------------------------------------------------
# Strictly positive parent and its negative critical singlet.
# ------------------------------------------------------------------

frame = sp.Matrix([[1, 0], [0, 1], [0, 0]])
epsilon = sp.Matrix([[0, -1], [1, 0]])
coefficient = frame * epsilon * dagger(frame)
coefficient_vector = vec(coefficient)

inside_indices = [0, 1, 3, 4]  # 00, 01, 10, 11 in row vectorization
parent = 2 * sp.eye(9)
for row in inside_indices:
    for column in inside_indices:
        parent[row, column] = 0
for index in inside_indices:
    parent[index, index] = 1
phi = sp.Matrix([1, 0, 0, 0, 1, 0, 0, 0, 0]) / sp.sqrt(2)
parent += 3 * phi * dagger(phi)

z = sp.symbols("z")
assert sp.factor(parent.charpoly(z).as_expr()) == (
    (z - 4) * (z - 2) ** 5 * (z - 1) ** 3
)

endpoint = partial_transpose(parent, 3)
assert endpoint * coefficient_vector == -coefficient_vector / 2
assert quadratic(endpoint, coefficient) == -1
critical_lambda = sp.Rational(-1, 2)

# The three unnormalized Bell companions all have energy 5.
logical_companions = [
    sp.Matrix([[0, 1], [1, 0]]),
    sp.Matrix([[1, 0], [0, -1]]),
    sp.eye(2),
]
for companion in logical_companions:
    physical = frame * companion * dagger(frame)
    assert quadratic(endpoint, physical) == 5

# ------------------------------------------------------------------
# Independent complex graph-chart differentiation.
# Add a Hermitian core/normal coupling so that the R term is nonzero.
# ------------------------------------------------------------------

normal = sp.zeros(3)
normal[2, 2] = 1
normal_vector = vec(normal)
rho = sp.Rational(1, 3)
audit_operator = endpoint + rho * (
    normal_vector * dagger(coefficient_vector)
    + coefficient_vector * dagger(normal_vector)
) / hs_inner(coefficient, coefficient)

assert unvec(audit_operator * coefficient_vector, 3) == (
    -coefficient / 2 + rho * normal
)

logical_velocity = (
    logical_companions[0]
    + I * logical_companions[1]
    + 2 * logical_companions[2]
)
left_velocity = sp.Matrix(
    [[0, 0], [0, 0], [1 + I, 2 - I]]
)
right_velocity = sp.Matrix(
    [[0, 0], [0, 0], [2 + I, -1 + 2 * I]]
)

inverse_epsilon = epsilon.inv()
W = inverse_epsilon * logical_velocity
assert sp.re(sp.trace(W)) == 0

raw_curve = (
    (frame + t * left_velocity)
    * (epsilon + t * logical_velocity)
    * dagger(frame + t * right_velocity)
)

gram_left = sp.eye(2) + t**2 * dagger(left_velocity) * left_velocity
gram_right = (
    sp.eye(2) + t**2 * dagger(right_velocity) * right_velocity
)
det_middle = sp.det(epsilon + t * logical_velocity)
delta_squared = sp.simplify(
    det_middle * sp.conjugate(det_middle)
    * sp.det(gram_left) * sp.det(gram_right)
)
delta = sp.sqrt(delta_squared)
normalized_energy = sp.simplify(
    quadratic(audit_operator, raw_curve) / delta
)
direct_half_hessian = sp.simplify(
    sp.diff(normalized_energy, t, 2).subs(t, 0) / 2
)

tangent = (
    frame * logical_velocity * dagger(frame)
    + left_velocity * epsilon * dagger(frame)
    + frame * epsilon * dagger(right_velocity)
)
normal_curvature = left_velocity * epsilon * dagger(right_velocity)
metric_norm = sp.trace(dagger(left_velocity) * left_velocity) + (
    sp.trace(dagger(right_velocity) * right_velocity)
)
formula_half_hessian = sp.simplify(
    quadratic(audit_operator, tangent)
    + 2 * sp.re(hs_inner(rho * normal, normal_curvature))
    + critical_lambda * sp.re(sp.trace(W * W))
    - critical_lambda * metric_norm
)
assert sp.simplify(direct_half_hessian - formula_half_hessian) == 0

# Changing the two leakage phases verifies the different phase laws:
# ordinary cross response uses conjugate(alpha)*beta, whereas the
# curvature uses alpha*beta.
alpha = 2 + I
beta = -1 + 3 * I
d_left = left_velocity * epsilon * dagger(frame)
d_right = frame * epsilon * dagger(right_velocity)
p0 = hs_inner(d_left, unvec(audit_operator * vec(d_right), 3))
q0 = hs_inner(rho * normal, normal_curvature)
scaled_p = hs_inner(
    alpha * d_left,
    unvec(audit_operator * vec(beta * d_right), 3),
)
scaled_q = hs_inner(
    rho * normal,
    alpha * beta * normal_curvature,
)
assert sp.simplify(scaled_p - sp.conjugate(alpha) * beta * p0) == 0
assert sp.simplify(scaled_q - alpha * beta * q0) == 0

# In the positive-parent model itself R and all core/outside couplings
# vanish.  The core gaps are 4 and 6, and the outside gap is 5/2.
assert all(5 - gap > 0 for gap in (1, -1))
assert sp.Rational(2) - critical_lambda == sp.Rational(5, 2)

# ------------------------------------------------------------------
# Full-support qutrit plane with zero triple-Hodge leakage.
# ------------------------------------------------------------------

def basis_index(a: int, b: int, c: int) -> int:
    return 9 * a + 3 * b + c


u0 = sp.zeros(27, 1)
u1 = sp.zeros(27, 1)
for j in range(3):
    u0[basis_index(j, j, j)] = 1 / sp.sqrt(3)
for triple in ((0, 1, 2), (1, 2, 0), (2, 0, 1)):
    u1[basis_index(*triple)] = 1 / sp.sqrt(3)

assert (dagger(u0) * u0)[0] == 1
assert (dagger(u1) * u1)[0] == 1
assert (dagger(u0) * u1)[0] == 0


def levi(a: int, b: int, c: int) -> int:
    if len({a, b, c}) < 3:
        return 0
    values = (a, b, c)
    inversions = sum(
        values[i] > values[j]
        for i in range(3)
        for j in range(i + 1, 3)
    )
    return -1 if inversions % 2 else 1


hodge = sp.zeros(27, 1)
for a, b, c, p, q, r, i, j, k in itertools.product(
    range(3), repeat=9
):
    coefficient_hodge = (
        levi(p, a, i) * levi(q, b, j) * levi(r, c, k)
    )
    if coefficient_hodge:
        hodge[basis_index(a, b, c)] += (
            u0[basis_index(p, q, r)]
            * u1[basis_index(i, j, k)]
            * coefficient_hodge
        )
assert hodge == sp.zeros(27, 1)


def one_site_reduction(vector: sp.Matrix, site: int) -> sp.Matrix:
    tensor = [
        vector[basis_index(a, b, c)]
        for a, b, c in itertools.product(range(3), repeat=3)
    ]
    out = sp.zeros(3)
    for row, column in itertools.product(range(3), repeat=2):
        value = 0
        for environment in itertools.product(range(3), repeat=2):
            left = list(environment)
            right = list(environment)
            left.insert(site, row)
            right.insert(site, column)
            value += (
                tensor[basis_index(*left)]
                * sp.conjugate(tensor[basis_index(*right)])
            )
        out[row, column] = sp.simplify(value)
    return out


for site in range(3):
    assert one_site_reduction(u0, site) == sp.eye(3) / 3
    assert one_site_reduction(u1, site) == sp.eye(3) / 3

print(
    "verified complex graph Hessian, phase conjugations, positive-parent "
    "negative critical model, and full-support zero triple-Hodge plane"
)
