#!/usr/bin/env python3
"""Exact checks for the finite Haar fixed-support normality formulas.

Only rational arithmetic from the Python standard library is used.
The environment dimension is reduced from 9 to 2 because the local
projection algebra in equations (18) and (23) is dimension-independent.
"""

from __future__ import annotations

from fractions import Fraction as F


def zeros(n: int, m: int) -> list[list[F]]:
    return [[F(0) for _ in range(m)] for _ in range(n)]


def eye(n: int) -> list[list[F]]:
    out = zeros(n, n)
    for i in range(n):
        out[i][i] = F(1)
    return out


def add(*matrices: list[list[F]]) -> list[list[F]]:
    return [
        [sum(m[i][j] for m in matrices) for j in range(len(matrices[0][0]))]
        for i in range(len(matrices[0]))
    ]


def scale(a: F, x: list[list[F]]) -> list[list[F]]:
    return [[a * value for value in row] for row in x]


def matmul(a: list[list[F]], b: list[list[F]]) -> list[list[F]]:
    return [
        [
            sum(a[i][k] * b[k][j] for k in range(len(b)))
            for j in range(len(b[0]))
        ]
        for i in range(len(a))
    ]


def kron(a: list[list[F]], b: list[list[F]]) -> list[list[F]]:
    return [
        [
            a[i // len(b)][j // len(b[0])]
            * b[i % len(b)][j % len(b[0])]
            for j in range(len(a[0]) * len(b[0]))
        ]
        for i in range(len(a) * len(b))
    ]


def partial_trace_local(e: list[list[F]], env: int) -> list[list[F]]:
    out = zeros(env, env)
    for alpha in range(env):
        for beta in range(env):
            out[alpha][beta] = sum(
                e[a * env + alpha][a * env + beta] for a in range(3)
            )
    return out


def trace_after_left(
    r: list[list[F]], e: list[list[F]], env: int
) -> list[list[F]]:
    """Tr_local((R tensor I) E)."""
    out = zeros(env, env)
    for alpha in range(env):
        for beta in range(env):
            out[alpha][beta] = sum(
                r[a][b] * e[b * env + alpha][a * env + beta]
                for a in range(3)
                for b in range(3)
            )
    return out


def local_L(e: list[list[F]], env: int) -> list[list[F]]:
    return add(e, scale(F(-1, 2), kron(eye(3), partial_trace_local(e, env))))


def direct_n(
    p: list[list[F]], e: list[list[F]], env: int
) -> list[list[F]]:
    p_big = kron(p, eye(env))
    return matmul(p_big, local_L(matmul(p_big, e), env))


def polynomial_n(
    z: list[F], e: list[list[F]], env: int
) -> list[list[F]]:
    r = sum(value * value for value in z)
    rank_one = [[z[i] * z[j] for j in range(3)] for i in range(3)]
    r_big = kron(rank_one, eye(env))
    tr_e = partial_trace_local(e, env)
    tr_re = trace_after_left(rank_one, e, env)
    return add(
        scale(r * r, e),
        scale(-r, matmul(r_big, e)),
        scale(F(-1, 2) * r * r, kron(eye(3), tr_e)),
        scale(F(1, 2) * r, kron(eye(3), tr_re)),
        scale(F(1, 2) * r, kron(rank_one, tr_e)),
        scale(F(-1, 2), kron(rank_one, tr_re)),
    )


def deterministic_matrix(n: int) -> list[list[F]]:
    return [
        [F(((7 * i + 11 * j + 3 * i * j) % 19) - 9, 13) for j in range(n)]
        for i in range(n)
    ]


def main() -> None:
    env = 2
    e = deterministic_matrix(3 * env)
    z = [F(1), F(2), F(-1)]
    r = sum(value * value for value in z)
    rank_one = [[z[i] * z[j] for j in range(3)] for i in range(3)]
    p = add(eye(3), scale(F(-1, r), rank_one))

    # Equation (18): the cleared polynomial equals r^2 times the direct form.
    assert polynomial_n(z, e, env) == scale(r * r, direct_n(p, e, env))

    # Equation (23), using E R=(I/3) and
    # E[R tensor Tr(RE)]=(E+I tensor Tr(E))/12.
    tr_e = partial_trace_local(e, env)
    averaged = add(
        scale(F(2, 3), e),
        scale(F(-1, 3), kron(eye(3), tr_e)),
        scale(F(1, 6), kron(eye(3), tr_e)),
        scale(F(-1, 24), add(e, kron(eye(3), tr_e))),
    )
    q_local = add(e, scale(F(-1, 3), kron(eye(3), tr_e)))
    assert averaged == scale(F(5, 8), q_local)

    # The high-rank scalar solution has E=I/4 and N(P)=0 for every P.
    scalar_e = scale(F(1, 4), eye(3 * env))
    assert direct_n(p, scalar_e, env) == zeros(3 * env, 3 * env)

    # A bidegree-(2,2) form on C^3 has 6 times 6 coefficients.
    assert (3 * 4 // 2) ** 2 == 36

    print("verified: finite Haar fixed-support polynomial and Haar constant")


if __name__ == "__main__":
    main()
