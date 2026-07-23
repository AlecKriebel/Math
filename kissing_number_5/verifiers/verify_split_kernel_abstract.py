#!/usr/bin/env python3
"""Exact verifier for proofs/split_kernel_abstract_barrier.md."""

from __future__ import annotations

from fractions import Fraction
from itertools import combinations, product
import json
from pathlib import Path


Q = Fraction
ROOT = Path(__file__).resolve().parents[1]


class Quad:
    """The exact number a+b*sqrt(2)."""

    __slots__ = ("a", "b")

    def __init__(self, a: Q = Q(0), b: Q = Q(0)) -> None:
        self.a = Q(a)
        self.b = Q(b)

    def __eq__(self, other: object) -> bool:
        return (
            isinstance(other, Quad)
            and self.a == other.a
            and self.b == other.b
        )

    def __hash__(self) -> int:
        return hash((self.a, self.b))

    def __add__(self, other: "Quad") -> "Quad":
        return Quad(self.a + other.a, self.b + other.b)

    def __sub__(self, other: "Quad") -> "Quad":
        return Quad(self.a - other.a, self.b - other.b)

    def __neg__(self) -> "Quad":
        return Quad(-self.a, -self.b)

    def __mul__(self, other: "Quad") -> "Quad":
        return Quad(
            self.a * other.a + 2 * self.b * other.b,
            self.a * other.b + self.b * other.a,
        )

    def inverse(self) -> "Quad":
        denominator = self.a**2 - 2 * self.b**2
        assert denominator != 0
        return Quad(self.a / denominator, -self.b / denominator)

    def __truediv__(self, other: "Quad") -> "Quad":
        return self * other.inverse()

    def sign(self) -> int:
        if self.b == 0:
            return (self.a > 0) - (self.a < 0)
        if self.a == 0:
            return (self.b > 0) - (self.b < 0)
        if self.a > 0 and self.b > 0:
            return 1
        if self.a < 0 and self.b < 0:
            return -1
        comparison = self.a**2 - 2 * self.b**2
        if comparison == 0:
            return 0
        if self.a > 0:
            return 1 if comparison > 0 else -1
        return -1 if comparison > 0 else 1


ZERO = Quad()
ONE = Quad(Q(1))


def exact_rank(matrix: list[list[Quad]]) -> int:
    work = [row[:] for row in matrix]
    rows = len(work)
    columns = len(work[0]) if rows else 0
    rank = 0
    for column in range(columns):
        pivot = next(
            (
                row
                for row in range(rank, rows)
                if work[row][column] != ZERO
            ),
            None,
        )
        if pivot is None:
            continue
        work[rank], work[pivot] = work[pivot], work[rank]
        pivot_value = work[rank][column]
        work[rank] = [value / pivot_value for value in work[rank]]
        for row in range(rows):
            if row == rank or work[row][column] == ZERO:
                continue
            multiplier = work[row][column]
            work[row] = [
                value - multiplier * pivot_entry
                for value, pivot_entry in zip(work[row], work[rank])
            ]
        rank += 1
        if rank == rows:
            break
    return rank


def d5_integer_roots() -> list[tuple[int, ...]]:
    roots: list[tuple[int, ...]] = []
    for i, j in combinations(range(5), 2):
        for sign_i, sign_j in product((-1, 1), repeat=2):
            root = [0] * 5
            root[i] = sign_i
            root[j] = sign_j
            roots.append(tuple(root))
    return roots


def verify(certificate_path: Path = None) -> dict[str, object]:
    if certificate_path is None:
        certificate_path = (
            ROOT / "certificates" / "split_kernel_abstract_counterexample.json"
        )
    data = json.loads(certificate_path.read_text())
    assert data["schema"] == "split-kernel-abstract-counterexample-v1"
    assert data["order"] == 41

    roots = d5_integer_roots()
    assert len(roots) == 40
    size = 41
    half = Q(1, 2)
    fifth = Q(1, 5)

    # The old normalized inner product is dot(r,s)/2.  Against e1 it is
    # r[0]/sqrt(2) = (r[0]/2)*sqrt(2).
    old_gram = [
        [
            Q(sum(x * y for x, y in zip(first, second)), 2)
            for second in roots
        ]
        for first in roots
    ]
    a = [[ZERO for _ in range(size)] for _ in range(size)]
    b = [[ZERO for _ in range(size)] for _ in range(size)]
    for i in range(40):
        for j in range(40):
            inner = old_gram[i][j]
            a[i][j] = Quad(half * inner)
            b[i][j] = Quad(inner**2 - fifth)
        t = Quad(Q(0), Q(roots[i][0], 2))
        a[i][40] = a[40][i] = Quad(half) * t
        t_squared = (t * t).a
        assert (t * t).b == 0
        b[i][40] = b[40][i] = Quad(fifth - t_squared)
    a[40][40] = Quad(half)
    b[40][40] = Quad(Q(4, 5))

    r_matrix = [
        [a[i][j] + b[i][j] for j in range(size)]
        for i in range(size)
    ]
    k_matrix = [
        [r_matrix[i][j] - Quad(Q(3, 10)) for j in range(size)]
        for i in range(size)
    ]

    assert exact_rank(a) == data["linear_rank_bound"] == 5
    assert exact_rank(b) == data["quadratic_rank_bound"] == 14
    combined_rank = exact_rank(r_matrix)
    assert combined_rank <= data["combined_rank_bound"] == 19
    assert exact_rank(k_matrix) <= 20
    assert sum(a[i][i].a for i in range(size)) == Q(data["linear_trace"])
    assert sum(b[i][i].a for i in range(size)) == Q(data["quadratic_trace"])
    assert all(a[i][i] == Quad(Q(1, 2)) for i in range(size))
    assert all(b[i][i] == Quad(Q(4, 5)) for i in range(size))
    assert all(r_matrix[i][i] == Quad(Q(13, 10)) for i in range(size))
    assert all(k_matrix[i][i] == ONE for i in range(size))

    for i in range(size):
        for j in range(size):
            if i == j:
                continue
            assert (k_matrix[i][j]).sign() <= 0
            assert (r_matrix[i][j] - Quad(Q(3, 10))).sign() <= 0

    cross_r = sorted(
        set(r_matrix[i][40] for i in range(40)),
        key=lambda value: (value.a, value.b),
    )
    expected_cross = {
        Quad(Q(1, 5)),
        Quad(-Q(3, 10), Q(1, 4)),
        Quad(-Q(3, 10), -Q(1, 4)),
    }
    assert set(cross_r) == expected_cross
    lower_endpoint = Quad(-Q(21, 80))
    minimum_cross = Quad(-Q(3, 10), -Q(1, 4))
    assert (minimum_cross - lower_endpoint).sign() < 0

    # Exact covering-width obstruction for any D5-based extension.
    assert Q(data["d5_covering_lower_bound_squared"]) == Q(2, 5)
    assert Q(data["interval_width_squared"]) == Q(81, 256)
    assert Q(2, 5) > Q(81, 256)

    return {
        "status": "PASS",
        "order": size,
        "rank_A": exact_rank(a),
        "rank_B": exact_rank(b),
        "rank_R": combined_rank,
        "rank_K": exact_rank(k_matrix),
        "trace_A": str(Q(41, 2)),
        "trace_B": str(Q(164, 5)),
        "all_K_offdiagonal_nonpositive": True,
        "full_entry_range_violated": True,
        "d5_extension_with_full_range_impossible": True,
        "conclusion": (
            "split PSD ranks, Ky Fan traces, and K off-diagonal signs "
            "admit an exact order-41 abstract counterexample"
        ),
    }


def main() -> None:
    print(json.dumps(verify(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
