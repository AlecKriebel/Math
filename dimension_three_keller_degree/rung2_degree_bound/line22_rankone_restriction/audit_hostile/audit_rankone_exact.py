#!/usr/bin/env python3
"""Hostile exact reconstruction of the rank-one-restriction open orbit."""

if not __debug__:
    raise RuntimeError("hostile audit refuses optimized Python")

from itertools import product

import sympy as sp

x, y, z, c = sp.symbols("x y z c")
xyz = (x, y, z)
p = x**2
q = y**2 + x*z


def mons(degree):
    return tuple(
        x**i*y**j*z**(degree-i-j)
        for i in range(degree, -1, -1)
        for j in range(degree-i, -1, -1)
    )


def form(prefix, degree):
    coefficients = sp.symbols(f"{prefix}0:{len(mons(degree))}")
    return (
        sum(coefficient*monomial
            for coefficient, monomial in zip(coefficients, mons(degree))),
        coefficients,
    )


def det3(first, second, third):
    return sp.expand(
        sp.Matrix([first, second, third]).jacobian(xyz).det()
    )


def homogeneous_coefficient(L, H2, H3, H4, degree):
    matrices = [
        vector.jacobian(xyz) for vector in (L, H2, H3, H4)
    ]
    answer = 0
    for choices in product(range(4), repeat=3):
        if sum(choices) == degree:
            answer += sp.Matrix.vstack(
                *(matrices[choices[row]][row, :] for row in range(3))
            ).det()
    return sp.expand(answer)


def e7_matrix(first, second, third, prefix):
    U, uc = form(prefix + "u", 3)
    V, vc = form(prefix + "v", 3)
    W, wc = form(prefix + "w", 2)
    expression = (
        det3(first, second, W)
        + det3(first, V, third)
        + det3(U, second, third)
    )
    polynomial = sp.Poly(expression, *xyz)
    equations = [
        polynomial.coeff_monomial(monomial) for monomial in mons(7)
    ]
    matrix, right = sp.linear_eq_to_matrix(equations, uc + vc + wc)
    assert right == sp.zeros(36, 1)
    return matrix, expression, uc + vc + wc


def vector_coefficients(first, second, third):
    entries = []
    for expression, degree in ((first, 3), (second, 3), (third, 2)):
        polynomial = sp.Poly(expression, *xyz)
        entries.extend(
            polynomial.coeff_monomial(monomial)
            for monomial in mons(degree)
        )
    return sp.Matrix(entries)


# Full stabilizer after uniqueness of the double line has forced x'=alpha*x.
alpha, beta, gamma, delta, epsilon, eta, theta = sp.symbols(
    "alpha beta gamma delta epsilon eta theta"
)
xp = alpha*x
yp = gamma*x + beta*y + epsilon*z
zp = delta*x + eta*y + theta*z
qp = sp.Poly(sp.expand(yp**2 + xp*zp), *xyz)
assert qp.coeff_monomial(z**2) == epsilon**2
assert qp.coeff_monomial(y*z) == 2*beta*epsilon
qp_reduced = qp.as_expr().subs(
    {
        epsilon: 0,
        eta: -2*beta*gamma/alpha,
        theta: beta**2/alpha,
    }
)
assert sp.expand(
    qp_reduced - beta**2*q - (gamma**2 + alpha*delta)*p
) == 0
stabilizer = sp.Matrix(
    [
        [alpha, 0, 0],
        [gamma, beta, 0],
        [delta, -2*beta*gamma/alpha, beta**2/alpha],
    ]
)
assert sp.factor(stabilizer.det()) == beta**3

# The Borel becomes the affine group after v=1/u.  Its unordered
# {1,-1} stabilizer is exactly identity and sign.
A0, B0 = sp.symbols("A0 B0")
swap_solution = sp.solve(
    (
        sp.Eq(A0/(1+B0), -1),
        sp.Eq(-A0/(1-B0), 1),
    ),
    (A0, B0),
    dict=True,
)
assert swap_solution == [{A0: -1, B0: 0}]
fix_solution = sp.solve(
    (
        sp.Eq(A0/(1+B0), 1),
        sp.Eq(-A0/(1-B0), -1),
    ),
    (A0, B0),
    dict=True,
)
assert fix_solution == [{A0: 1, B0: 0}]

# Raw E7 reconstructed without importing the supplied verifier.
first = (p-q)**2
second = (p+q)**2
third = x*(p-c*q)
M7, E7, raw_unknowns = e7_matrix(first, second, third, "audit")
partial = lambda expression: sp.expand(
    2*y*sp.diff(expression, z) - x*sp.diff(expression, y)
)
Uraw = sum(raw_unknowns[i]*mons(3)[i] for i in range(10))
Vraw = sum(raw_unknowns[10+i]*mons(3)[i] for i in range(10))
Wraw = sum(raw_unknowns[20+i]*mons(2)[i] for i in range(6))
displayed_e7 = 2*(
    8*x*(p-q)*(p+q)*partial(Wraw)
    + (p+q)*((-3-2*c)*p+c*q)*partial(Uraw)
    + (p-q)*((2*c-3)*p+c*q)*partial(Vraw)
)
assert sp.expand(E7-displayed_e7) == 0

# A different 18-minor from the supplied certificate has exactly the same
# exceptional support.
alternate_rows = (0, 1, 2, 3, 4, 16, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 17, 19)
alternate_columns = (
    1, 2, 4, 5, 6, 7, 8, 9, 11,
    12, 14, 15, 16, 17, 18, 19, 24, 25,
)
alternate_minor = sp.factor(
    M7.extract(alternate_rows, alternate_columns).det()
)
assert alternate_minor == (
    -256494072527585280*c**7*(c-3)**4*(c+3)**4
)

# Complete universal kernel and the allegedly omitted z-translation.
directions = (
    (x**3, 0, 0),
    (x*q, 0, 0),
    (0, x**3, 0),
    (0, x*q, 0),
    (0, 0, p),
    (0, 0, q),
    (sp.diff(first, x), sp.diff(second, x), sp.diff(third, x)),
    (sp.diff(first, y), sp.diff(second, y), sp.diff(third, y)),
)
kernel = sp.Matrix.hstack(
    *(vector_coefficients(*direction) for direction in directions)
)
assert M7*kernel == sp.zeros(36, 8)
assert kernel.extract((0, 1, 2, 3, 10, 12, 20, 22), range(8)).det() == -8
tau_z = vector_coefficients(
    sp.diff(first, z), sp.diff(second, z), sp.diff(third, z)
)
assert (
    tau_z
    + 2*kernel[:, 0] - 2*kernel[:, 1]
    - 2*kernel[:, 2] - 2*kernel[:, 3]
    + c*kernel[:, 4]
) == sp.zeros(26, 1)

assert M7.subs(c, 0).rank() == 16
assert M7.subs(c, 3).rank() == 14
assert M7.subs(c, -3).rank() == 14
Minfinity, _, _ = e7_matrix(first, second, x*q, "infinity")
assert Minfinity.rank() == 18
assert e7_matrix(p**2, q**2, x**3, "marked0")[0].rank() == 8
assert e7_matrix(p**2, q**2, x*q, "marked1")[0].rank() == 18
assert e7_matrix(p**2, q**2, x*(p-q), "marked2")[0].rank() == 18

# Every frontier row has a literal E8/E7 leading witness.
frontier = (
    (p**2, q**2, x**3),
    (p**2, q**2, x*q),
    (p**2, q**2, x*(p-q)),
    (first, second, x**3),
    (first, second, x*(p-3*q)),
    (first, second, x*(p+3*q)),
    (first, second, x*q),
)
for first_case, second_case, third_case in frontier:
    assert det3(first_case, second_case, third_case) == 0
    assert (
        det3(first_case, second_case, 0)
        + det3(first_case, 0, third_case)
        + det3(0, second_case, third_case)
    ) == 0

# Reconstruct E6 with a different full-rank minor.
AA, BB, w0, w1 = sp.symbols("AA BB w0 w1")
u0, uq, u1, u2, u3, u4 = sp.symbols("u0 uq u1 u2 u3 u4")
v0, vq, v1, v2, v3, v4 = sp.symbols("v0 vq v1 v2 v3 v4")
U2 = u0*p + uq*q + u1*x*y + u2*x*z + u3*y*z + u4*z**2
V2 = v0*p + vq*q + v1*x*y + v2*x*z + v3*y*z + v4*z**2
ell = sp.symbols("ell0:9")
L = sp.Matrix(3, 3, ell)*sp.Matrix([x, y, z])
H4 = sp.Matrix([first, second, 0])
H3 = sp.Matrix([AA*x*q, BB*x*q, third])
H2 = sp.Matrix([U2, V2, w0*p+w1*q])
E6 = homogeneous_coefficient(L, H2, H3, H4, 6)
constrained = (ell[7], ell[8], u1, u2, u3, u4, v1, v2, v3, v4)
equations6 = [
    sp.Poly(E6, *xyz).coeff_monomial(monomial) for monomial in mons(6)
]
M6, right6 = sp.linear_eq_to_matrix(equations6, constrained)
assert right6 == sp.zeros(28, 1)
alternate_rows6 = (0, 5, 4, 6, 8, 10, 16, 22, 1, 3)
alternate_minor6 = sp.factor(
    M6.extract(alternate_rows6, range(10)).det()
)
assert alternate_minor6 == (
    -3623878656*c**3*(c-3)**2*(c+3)**2
)
zero_constrained = {symbol: 0 for symbol in constrained}
assert sp.expand(E6.subs(zero_constrained)) == 0

# Reconstruct the E5 exit and certify its only division by 2x2 minors
# whose determinants are nonzero precisely when c != 0.
E5 = homogeneous_coefficient(
    L.subs(zero_constrained),
    H2.subs(zero_constrained),
    H3,
    H4,
    5,
)
P5 = sp.Poly(E5, *xyz)
f12a = P5.coeff_monomial(x**3*z**2)
f12b = P5.coeff_monomial(x**5)
f13a = P5.coeff_monomial(y**5)
f13b = P5.coeff_monomial(x**4*y)
assert sp.expand(f12a + 2*c*(ell[1]-ell[4])) == 0
assert sp.expand(
    f12b - 2*((2*c+3)*ell[1]+(3-2*c)*ell[4])
) == 0
assert sp.expand(f13a - 4*c*(ell[2]-ell[5])) == 0
assert sp.expand(
    f13b + 4*((2*c+3)*ell[2]+(3-2*c)*ell[5])
) == 0
pair12 = sp.linear_eq_to_matrix((f12a, f12b), (ell[1], ell[4]))[0]
pair13 = sp.linear_eq_to_matrix((f13a, f13b), (ell[2], ell[5]))[0]
assert sp.factor(pair12.det()) == -24*c
assert sp.factor(pair13.det()) == -96*c
assert sp.Matrix(3, 3, ell).det().subs(
    {
        ell[1]: 0, ell[2]: 0, ell[4]: 0, ell[5]: 0,
        ell[7]: 0, ell[8]: 0,
    }
) == 0

print("PASS: hostile exact rank-one-restriction reconstruction")
