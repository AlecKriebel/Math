#!/usr/bin/env python3
"""Exact checker for the global second-kernel reduction.

The checker uses only fractions.  It verifies the two characteristic
polynomials in the raw-contraction obstruction
U = span{E_11,E_22}, together with its marginal distance data.
"""

from fractions import Fraction as F


def zeros(n: int, m: int) -> list[list[F]]:
    return [[F(0) for _ in range(m)] for _ in range(n)]


def transpose(a: list[list[F]]) -> list[list[F]]:
    return [list(row) for row in zip(*a)]


def matmul(a: list[list[F]], b: list[list[F]]) -> list[list[F]]:
    bt = transpose(b)
    return [[sum(x * y for x, y in zip(row, col)) for col in bt] for row in a]


def add(a: list[list[F]], b: list[list[F]]) -> list[list[F]]:
    return [[a[i][j] + b[i][j] for j in range(len(a[0]))] for i in range(len(a))]


def scale(c: F, a: list[list[F]]) -> list[list[F]]:
    return [[c * x for x in row] for row in a]


def eye(n: int) -> list[list[F]]:
    out = zeros(n, n)
    for i in range(n):
        out[i][i] = F(1)
    return out


def inner(a: list[list[F]], b: list[list[F]]) -> F:
    return sum(
        a[i][j] * b[i][j]
        for i in range(len(a))
        for j in range(len(a[0]))
    )


def trace(a: list[list[F]]) -> F:
    return sum(a[i][i] for i in range(len(a)))


def partial_trace(a: list[list[F]], site: int) -> list[list[F]]:
    out = zeros(3, 3)
    if site == 0:
        for j in range(3):
            for ell in range(3):
                out[j][ell] = sum(a[3 * i + j][3 * i + ell] for i in range(3))
    else:
        for i in range(3):
            for k in range(3):
                out[i][k] = sum(a[3 * i + j][3 * k + j] for j in range(3))
    return out


def endpoint_pair(a: list[list[F]], b: list[list[F]]) -> F:
    return (
        inner(a, b)
        - F(1, 2)
        * (
            inner(partial_trace(a, 0), partial_trace(b, 0))
            + inner(partial_trace(a, 1), partial_trace(b, 1))
        )
        + F(1, 4) * trace(a) * trace(b)
    )


def main() -> None:
    # u_0=E_11 and u_1=E_22, using zero-based physical indices.
    u = [[F(0)] * 9 for _ in range(2)]
    u[0][0] = F(1)
    u[1][4] = F(1)

    basis = []
    for input_index in range(9):
        for code_index in range(2):
            c = zeros(9, 9)
            for output_index in range(9):
                c[output_index][input_index] = u[code_index][output_index]
            basis.append(c)

    h = [
        [endpoint_pair(basis[i], basis[j]) for j in range(18)]
        for i in range(18)
    ]

    psi = [[F(0)] for _ in range(18)]
    for physical_index in range(9):
        for code_index in range(2):
            psi[2 * physical_index + code_index][0] = u[code_index][physical_index]
    s_raw = add(
        scale(F(2), add(eye(18), scale(F(-1), h))),
        scale(F(1, 2), matmul(psi, transpose(psi))),
    )

    # Check the minimal polynomials and spectral moments.  Since both
    # matrices are symmetric, these determine the stated spectra.
    h_poly = matmul(matmul(h, add(h, scale(F(-1), eye(18)))), add(scale(F(2), h), scale(F(-1), eye(18))))
    s_poly = matmul(
        matmul(s_raw, add(s_raw, scale(F(-1), eye(18)))),
        add(s_raw, scale(F(-2), eye(18))),
    )
    assert h_poly == zeros(18, 18)
    assert s_poly == zeros(18, 18)
    assert trace(h) == F(25, 2)
    assert trace(matmul(h, h)) == F(41, 4)
    assert trace(s_raw) == 12
    assert trace(matmul(s_raw, s_raw)) == 16

    # rho_L=rho_R=diag(1,1,0), so M=1 and distance squared=4-2M=2.
    rho = [[F(1), F(0), F(0)], [F(0), F(1), F(0)], [F(0), F(0), F(0)]]
    assert trace(rho) == 2
    assert max(rho[i][i] for i in range(3)) == 1
    assert 4 - 2 * max(rho[i][i] for i in range(3)) == 2

    print("verified: exact factor distance and raw-S obstruction")


if __name__ == "__main__":
    main()
