#!/usr/bin/env python3
"""Independent exact verifier for FIRST_Q_EXCURSION_BUDGET.md.

The implementation uses only Python integers and Fraction.  It constructs
the labelled complete active chain directly from the update rule before
checking the three-channel quotient.  No discovery implementation is
imported.
"""

from __future__ import annotations

from fractions import Fraction as F
from math import comb


State = tuple[str, int]


def zeros(rows: int, cols: int) -> list[list[F]]:
    return [[F(0) for _ in range(cols)] for _ in range(rows)]


def row_times(row: list[F], matrix: list[list[F]]) -> list[F]:
    return [
        sum((row[i] * matrix[i][j] for i in range(len(row))), F(0))
        for j in range(len(matrix[0]))
    ]


def matmul(left: list[list[F]], right: list[list[F]]) -> list[list[F]]:
    return [row_times(row, right) for row in left]


def subtract(left: list[list[F]], right: list[list[F]]) -> list[list[F]]:
    return [
        [left[i][j] - right[i][j] for j in range(len(left[0]))]
        for i in range(len(left))
    ]


def inverse(matrix: list[list[F]]) -> list[list[F]]:
    n = len(matrix)
    augmented = [
        matrix[i][:] + [F(int(i == j)) for j in range(n)] for i in range(n)
    ]
    for col in range(n):
        pivot = next(row for row in range(col, n) if augmented[row][col])
        augmented[col], augmented[pivot] = augmented[pivot], augmented[col]
        scale = augmented[col][col]
        augmented[col] = [value / scale for value in augmented[col]]
        for row in range(n):
            if row == col or not augmented[row][col]:
                continue
            scale = augmented[row][col]
            augmented[row] = [
                x - scale * y for x, y in zip(augmented[row], augmented[col])
            ]
    return [row[n:] for row in augmented]


def quotient(N: int):
    states = (
        [("P", k) for k in range(1, N)]
        + [("Q", k) for k in range(1, N + 1)]
        + [("R", k) for k in range(1, N)]
    )
    index = {state: i for i, state in enumerate(states)}
    H = zeros(len(states), len(states))

    def add(source: State, target: State, mass: F) -> None:
        if mass and target in index:
            H[index[source]][index[target]] += mass

    for k in range(1, N):
        add(("P", k), ("P", k), F(k, 2 * N))
        add(("P", k), ("P", k + 1), F(N - k - 1, 2 * N))
        add(("P", k), ("Q", k + 1), F(1, 2 * N))

    for k in range(1, N + 1):
        add(("Q", k), ("Q", k), F(k * k - 1, 2 * k * N))
        add(("Q", k), ("Q", k + 1), F(N - k, 2 * N))
        add(("Q", k), ("P", k - 1), -F(k - 1, 2 * k * N))
        add(("Q", k), ("P", k), -F(N - k, 2 * k * N))
        add(("Q", k), ("R", k - 1), -F((k - 1) ** 2, 2 * k * N))
        add(("Q", k), ("R", k), -F((k - 1) * (N - k), 2 * k * N))

    for k in range(1, N):
        add(
            ("R", k),
            ("R", k),
            F(k, 2 * N) + F((k - 1) * (N - k), 2 * k * N),
        )
        add(("R", k), ("R", k + 1), F(N - k - 1, 2 * N))
        add(("R", k), ("R", k - 1), F((k - 1) ** 2, 2 * k * N))
        add(("R", k), ("Q", k), F(1, 2 * k * N))
        add(("R", k), ("P", k - 1), F(k - 1, 2 * k * N))
        add(("R", k), ("P", k), F(N - k, 2 * k * N))

    source = [F(0) for _ in states]
    for k in range(1, N):
        source[index[("R", k)]] = F(comb(N - 2, k - 1), 2 ** (N - 2))
    return states, H, source


def blocks(N: int):
    states, H, source = quotient(N)
    index = {state: i for i, state in enumerate(states)}
    good = [("P", k) for k in range(1, N)] + [
        ("R", k) for k in range(1, N)
    ]
    bad = [("Q", k) for k in range(1, N + 1)]
    S = [[H[index[a]][index[b]] for b in good] for a in good]
    C = [[H[index[a]][index[b]] for b in bad] for a in good]
    D = [[-H[index[a]][index[b]] for b in good] for a in bad]
    Q = [[H[index[a]][index[b]] for b in bad] for a in bad]
    s = [source[index[a]] for a in good]
    identity_minus_Q = [
        [F(int(i == j)) - Q[i][j] for j in range(N)] for i in range(N)
    ]
    fundamental = inverse(identity_minus_Q)
    E = matmul(matmul(C, fundamental), D)
    return good, bad, S, C, D, Q, E, s


def labelled_active_chain(N: int):
    """Complete active chain, constructed directly from its two branches."""

    n = N + 1
    states = [
        (B, v)
        for B in range(1, 1 << n)
        for v in range(n)
        if not (B >> v) & 1
    ]
    index = {state: i for i, state in enumerate(states)}
    chain = zeros(len(states), len(states))
    for row, (B, v) in enumerate(states):
        k = B.bit_count()
        # Retain v and sample a uniformly chosen label different from v.
        for i in range(n):
            if i != v:
                chain[row][index[(B | (1 << i), v)]] += F(1, 2 * N)
        # Choose a uniform cached target w, then sample i != w.
        for w in range(n):
            if not (B >> w) & 1:
                continue
            for i in range(n):
                if i != w:
                    new_B = (B & ~(1 << w)) | (1 << i)
                    chain[row][index[(new_B, w)]] += F(1, 2 * k * N)
        assert sum(chain[row], F(0)) == 1
    return states, chain


def labelled_quotient_audit(max_N: int = 5) -> None:
    def orbit(B: int, v: int):
        target = "X" if v == 0 else "Y" if v == 1 else "O"
        return B.bit_count(), (B >> 0) & 1, (B >> 1) & 1, target

    def swap(category):
        k, x_in, y_in, target = category
        return k, y_in, x_in, {"X": "Y", "Y": "X", "O": "O"}[target]

    def channel(category):
        k, x_in, y_in, target = category
        if target == "X":
            return ("Q" if y_in else "P", k)
        if target == "O" and x_in and not y_in:
            return "R", k
        return None

    for N in range(2, max_N + 1):
        labelled_states, chain = labelled_active_chain(N)
        categories = sorted({orbit(*state) for state in labelled_states}, key=repr)
        cat_index = {state: i for i, state in enumerate(categories)}
        representatives = {state: [] for state in categories}
        for i, state in enumerate(labelled_states):
            representatives[orbit(*state)].append(i)
        aggregate = []
        for category in categories:
            rows = []
            for source in representatives[category]:
                row = [F(0)] * len(categories)
                for target, mass in enumerate(chain[source]):
                    if mass:
                        row[cat_index[orbit(*labelled_states[target])]] += mass
                rows.append(row)
            assert all(row == rows[0] for row in rows)
            aggregate.append(rows[0])

        signed_states, signed, _ = quotient(N)
        signed_index = {state: i for i, state in enumerate(signed_states)}
        for category in categories:
            source_channel = channel(category)
            if source_channel is None:
                continue
            for target_channel in signed_states:
                positive = next(c for c in categories if channel(c) == target_channel)
                expected = aggregate[cat_index[category]][cat_index[positive]]
                expected -= aggregate[cat_index[category]][cat_index[swap(positive)]]
                actual = signed[signed_index[source_channel]][
                    signed_index[target_channel]
                ]
                assert actual == expected
    print(f"PASS (EXACT): labelled quotient N=2..{max_N}")


def one_excursion_audit(max_N: int = 30) -> None:
    for N in range(2, max_N + 1):
        good, bad, S, C, D, Q, E, s = blocks(N)
        good_index = {state: i for i, state in enumerate(good)}
        e = row_times(s, C)
        fundamental = inverse(
            [[F(int(i == j)) - Q[i][j] for j in range(N)] for i in range(N)]
        )
        v = row_times(e, fundamental)
        c = [F(comb(N - 2, k - 1), 2 ** (N - 2)) for k in range(1, N)]
        w = [F(c[k - 1], 2 * k * (N - k)) for k in range(1, N)]

        for k in range(1, N):
            lhs = w[k - 1] * (1 - Q[k - 1][k - 1])
            if k >= 2:
                lhs -= w[k - 2] * Q[k - 2][k - 1]
            residual = lhs - e[k - 1]
            expected = (
                F(c[0], 2 * N * (N - 1))
                if k == 1
                else F(c[k - 1], 4 * N * k * k * (N - k))
            )
            assert residual == expected > 0
            assert 0 <= v[k - 1] <= w[k - 1] <= c[k - 1]
        assert v[N - 1] == F(N, N * N + 1) * v[N - 2]

        completed = row_times(s, E)
        direct = row_times(s, S)
        assert all(0 <= x <= y for x, y in zip(completed, direct))

        for j in range(1, N):
            positive = N * c[j - 1]
            if j + 1 < N:
                positive += F(j * (N + 1), j + 1) * c[j]
            negative = (N - j) * v[j - 1]
            negative += F(j * (N + 1), j + 1) * v[j]
            assert 0 <= negative <= positive
    print(f"PASS (EXACT): first-excursion budget N=2..{max_N}")


def renewal_obstruction_audit() -> None:
    N = 3
    good, _bad, S, _C, _D, _Q, E, s = blocks(N)
    assert good == [("P", 1), ("P", 2), ("R", 1), ("R", 2)]
    expected_S = [
        [F(1, 6), F(1, 6), 0, 0],
        [0, F(1, 3), 0, 0],
        [F(1, 3), 0, F(1, 6), F(1, 6)],
        [F(1, 12), F(1, 12), F(1, 12), F(5, 12)],
    ]
    assert S == expected_S
    assert s == [0, 0, F(1, 2), F(1, 2)]
    sE = row_times(s, E)
    assert sE == [F(23, 648), F(7, 648), F(5, 648), F(9, 648)]
    y = [-1, 1, 1, 1]
    Sy = row_times(y, list(map(list, zip(*S))))
    assert Sy == [0, F(1, 3), 0, F(1, 2)]
    assert sum(x * z for x, z in zip(s, y)) == 1
    assert sum(x * z for x, z in zip(sE, y)) == -F(1, 324)

    M = subtract(S, E)
    row = s
    for exponent in range(1, 12):
        row = row_times(row, M)
        if exponent <= 10:
            assert all(value >= 0 for value in row)
    expected_negative = -F(
        2711557269637646196135713,
        1094189891315123592090000000000,
    )
    assert row[3] == expected_negative < 0
    print("PASS (EXACT): N=3 infinite-prefix separator and collapsed-power failure")


def finite_prefix_screen(max_N: int = 9, max_prefix: int = 40) -> None:
    """Finite evidence only: s S^g (S-E) is nonnegative on this corpus."""

    for N in range(3, max_N + 1):
        _good, _bad, S, _C, _D, _Q, E, s = blocks(N)
        difference = subtract(S, E)
        row = s
        for _g in range(max_prefix + 1):
            assert all(value >= 0 for value in row_times(row, difference))
            row = row_times(row, S)
    print(
        "PASS (EXACT FINITE SCREEN ONLY): "
        f"s S^g(S-E)>=0, N=3..{max_N}, g=0..{max_prefix}"
    )


if __name__ == "__main__":
    labelled_quotient_audit()
    one_excursion_audit()
    renewal_obstruction_audit()
    finite_prefix_screen()
