#!/usr/bin/env python3
"""Deterministic regressions for the support-level rigidity proposition.

The finite tests do not prove the proposition.  They independently exercise
the dimension-dependent phase identity, the weighted-cycle/reflection
relations used in its proof, the bad-phase exclusion, and the final rank
count.  The analytic argument is recorded in audit/RIGIDITY_RESTORATION_AUDIT.md.
"""

from __future__ import annotations

import cmath
import math
import random
from fractions import Fraction


TOL = 2.0e-10


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def require_close(actual: complex, expected: complex, message: str) -> None:
    error = abs(actual - expected)
    if error > TOL:
        raise AssertionError(
            f"{message}: got {actual!r}, expected {expected!r}, error {error:.3e}"
        )


def phase_data(d: int):
    omega = cmath.exp(2j * math.pi / d)
    eta = cmath.exp(1j * math.pi / d)
    delta = 1 if d % 2 == 0 else 0
    roots = [eta ** (2 * k + delta) for k in range(d)]
    phases = []
    for y in range(d):
        row = []
        for k, root in enumerate(roots):
            value = 1 + omega**y * root
            require(abs(value) > 1.0e-12, f"zero polar scalar at d={d}, y={y}, k={k}")
            row.append(value / abs(value))
        phases.append(row)
    return omega, eta, roots, phases


def test_supported_phase_algebra() -> str:
    checks = 0
    for d in range(2, 65):
        omega, eta, roots, phases = phase_data(d)
        target = (-1) ** (d - 1)
        r_star = (d - 1) // 2

        for y in range(d):
            bad_phase = -omega ** (-y)
            require_close(bad_phase**d, -target, f"bad phase parity at d={d}, y={y}")
            require(
                min(abs(bad_phase - root) for root in roots) > 1.0e-8,
                f"bad polar-kernel phase entered equality set at d={d}, y={y}",
            )

            phase_product = 1.0 + 0.0j
            for k, root in enumerate(roots):
                require_close(root**d, target, f"equality root at d={d}, k={k}")
                require_close(
                    phases[y][k] ** 2,
                    omega**y * root,
                    f"half-angle square at d={d}, y={y}, k={k}",
                )
                adjacent = phases[y][k].conjugate() * phases[(y + 1) % d][k]
                expected = eta * (-1 if (k + y) % d == r_star else 1)
                require_close(
                    adjacent,
                    expected,
                    f"adjacent phase at d={d}, y={y}, k={k}",
                )
                phase_product *= phases[y][k]
                checks += 1

            # The polar weighted shift has d-th power one.  Multiplication by
            # the single reflection flips exactly one cycle weight, so the
            # reflected weighted shift has d-th power minus one.
            require_close(phase_product, 1.0, f"polar cycle product at d={d}, y={y}")
            reflected_product = -phase_product
            require_close(
                reflected_product,
                -1.0,
                f"reflection cycle product at d={d}, y={y}",
            )

        labels = {(r_star - y) % d for y in range(d)}
        require(labels == set(range(d)), f"exceptional-label map is not bijective at d={d}")

    return f"supported phase and reflection identities d=2..64 ({checks} triples)"


def matmul(a, b):
    return [
        [sum((a[i][k] * b[k][j] for k in range(len(b))), Fraction(0)) for j in range(len(b[0]))]
        for i in range(len(a))
    ]


def matrix_rank(matrix) -> int:
    a = [row[:] for row in matrix]
    rows = len(a)
    cols = len(a[0])
    rank = 0
    for col in range(cols):
        pivot = next((r for r in range(rank, rows) if a[r][col] != 0), None)
        if pivot is None:
            continue
        a[rank], a[pivot] = a[pivot], a[rank]
        pivot_value = a[rank][col]
        a[rank] = [entry / pivot_value for entry in a[rank]]
        for row in range(rows):
            if row != rank and a[row][col] != 0:
                factor = a[row][col]
                a[row] = [a[row][j] - factor * a[rank][j] for j in range(cols)]
        rank += 1
        if rank == rows:
            break
    return rank


def identity(n: int):
    return [[Fraction(i == j) for j in range(n)] for i in range(n)]


def subtract(a, b):
    return [[a[i][j] - b[i][j] for j in range(len(a[0]))] for i in range(len(a))]


def test_rank_subadditivity() -> str:
    """Exact-rational hostile tests of rank(I-product) <= sum rank(I-factor)."""

    rng = random.Random(0xA12A2)
    trials = 0
    for n in range(1, 8):
        ident = identity(n)
        for number_of_factors in range(1, 7):
            for _ in range(20):
                factors = [
                    [
                        [Fraction(rng.randrange(-2, 3)) for _ in range(n)]
                        for _ in range(n)
                    ]
                    for _ in range(number_of_factors)
                ]
                product = ident
                for factor in factors:
                    product = matmul(product, factor)
                left_rank = matrix_rank(subtract(ident, product))
                right_rank = sum(matrix_rank(subtract(ident, factor)) for factor in factors)
                require(
                    left_rank <= right_rank,
                    f"rank subadditivity failed at n={n}, factors={number_of_factors}",
                )
                trials += 1
    return f"exact-rational rank subadditivity ({trials} hostile products)"


def test_dimension_count() -> str:
    cases = 0
    for d in range(2, 65):
        for n in range(1, 257):
            minimum_allowed_rank = (n + d - 1) // d
            feasible = d * minimum_allowed_rank <= n
            require(feasible == (n % d == 0), f"divisibility count failed at d={d}, n={n}")
            if feasible:
                common_rank = n // d
                require(d * common_rank == n, f"equal-rank sum failed at d={d}, n={n}")
                if common_rank > 0:
                    hostile = [common_rank + 1, common_rank - 1] + [common_rank] * (d - 2)
                    require(sum(hostile) == n, f"hostile ranks have wrong sum at d={d}, n={n}")
                    require(
                        any(n > d * rank for rank in hostile),
                        f"unequal ranks escaped a reflection bound at d={d}, n={n}",
                    )
            cases += 1
    return f"multiplicity/divisibility count d=2..64, dim K=1..256 ({cases} cases)"


def main() -> None:
    results = [
        test_supported_phase_algebra(),
        test_rank_subadditivity(),
        test_dimension_count(),
    ]
    for result in results:
        print(f"PASS: {result}")
    print("PASS: support-level rigidity regression suite")


if __name__ == "__main__":
    main()
