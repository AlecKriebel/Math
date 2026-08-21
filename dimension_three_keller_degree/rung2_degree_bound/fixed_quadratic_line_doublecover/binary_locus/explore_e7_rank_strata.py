#!/usr/bin/env python3
"""Generic exact ranks on the visible E7 determinant components."""

import sympy as sp

p, q = sp.symbols("p q")
a, b, c, d, eta = sp.symbols("a b c d eta")
R = a * p**3 + b * p**2 * q + c * p * q**2 + d * q**3


def jac(f, g):
    return sp.expand(sp.diff(f, p) * sp.diff(g, q)
                     - sp.diff(f, q) * sp.diff(g, p))


def matrices(h):
    P, Q = sp.expand(h * p**2), sp.expand(h * q**2)
    f, g, k = jac(Q, R), -jac(P, R), jac(P, Q)
    multiplier_blocks = (
        ((1,), (1,), ()),
        ((p, q), (p, q), (1,)),
        ((p**2, p * q, q**2), (p**2, p * q, q**2), (p, q)),
    )
    output = []
    for offset, blocks in enumerate(multiplier_blocks):
        columns = (
            tuple(f * item for item in blocks[0])
            + tuple(g * item for item in blocks[1])
            + tuple(k * item for item in blocks[2])
        )
        degree = 5 + offset
        output.append(
            sp.Matrix(
                [
                    [
                        sp.Poly(column, p, q).coeff_monomial(
                            p**i * q ** (degree - i)
                        )
                        for column in columns
                    ]
                    for i in range(degree, -1, -1)
                ]
            )
        )
    return tuple(output)


def show(label, mats, substitutions=None):
    values = mats if not substitutions else tuple(
        matrix.subs(substitutions) for matrix in mats
    )
    print(label, tuple(matrix.rank() for matrix in values))


branch_square = matrices(p**2)
show("p2 generic", branch_square)
show("p2 a=0", branch_square, {a: 0})
show("p2 d=0", branch_square, {d: 0})
show("p2 d=c=0", branch_square, {d: 0, c: 0})
show("p2 R=p3", branch_square, {b: 0, c: 0, d: 0})

two_branch = matrices(p * q)
show("pq generic", two_branch)
show("pq a=0", two_branch, {a: 0})
show("pq d=0", two_branch, {d: 0})
show("pq a=d=0", two_branch, {a: 0, d: 0})
show("pq a=b=0", two_branch, {a: 0, b: 0})
show("pq c=d=0", two_branch, {c: 0, d: 0})
show("pq R=p3", two_branch, {b: 0, c: 0, d: 0})

one_branch = matrices(p * (p + q))
show("one generic", one_branch)
show("one d=0", one_branch, {d: 0})
show("one split", one_branch, {b: 3 * a / 4})
show("one root", one_branch, {c: -a + b + d})
show("one d=split=0", one_branch, {d: 0, b: 3 * a / 4})
show("one split=root", one_branch, {b: 3 * a / 4, c: -a + b + d})

interior = matrices(p**2 + eta * p * q + q**2)
show("interior generic", interior)
show("interior left split", interior, {b: 3 * a * eta / 4})
show("interior right split", interior, {c: 3 * d * eta / 4})
show(
    "interior both split",
    interior,
    {b: 3 * a * eta / 4, c: 3 * d * eta / 4},
)
show("interior square eta=2", interior, {eta: 2})
