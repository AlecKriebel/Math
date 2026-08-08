#!/usr/bin/env python3
"""Exact verifier for the one-dimensional common-pin reduction.

Fix a vertex ``x``.  The pin replacement kernel ``Q_x`` is uniform in row
``x`` and points deterministically to ``x`` in every other row.  If ``A`` is
the corresponding active operator and ``B`` is the average of the other pin
operators, then

    K(p) = p A + (1-p) B

equals the complete active operator at ``p=1/n``.  The degree-``t``
Bernstein control ``psi[t,c]`` of ``nu K(p)^t H`` is the reward conditional
on seeing exactly ``c`` copies of the distinguished pin among the ``t``
uniformly located pin times.  Consequently

    Phi_t''(p)/(t(t-1))
      = E[Delta^2 psi[t,C]],  C ~ Binomial(t-2,p).

At ``p=1/n`` this is, up to the exact positive scale checked below, the
standard-sector fixed-count-two coefficient.  The script also records the
first discovered failure of the stronger pointwise convexity conjecture.
All arithmetic is over ``fractions.Fraction``.
"""

from __future__ import annotations

from fractions import Fraction as Q
from math import comb


State = tuple[int, int]
Operator = list[dict[int, Q]]


def replacement_complete(n: int) -> list[list[Q]]:
    return [
        [Q(0) if i == j else Q(1, n - 1) for j in range(n)]
        for i in range(n)
    ]


def replacement_pin(n: int, pin: int) -> list[list[Q]]:
    rows = [[Q(0) for _ in range(n)] for _ in range(n)]
    for source in range(n):
        if source == pin:
            for target in range(n):
                if target != source:
                    rows[source][target] = Q(1, n - 1)
        else:
            rows[source][pin] = Q(1)
    return rows


def standard_embedding(n: int, pin: int) -> list[list[Q]]:
    """Return E(s), with s_pin=n-1 and all other coordinates -1."""

    N = n - 1
    s = [Q(N) if i == pin else Q(-1) for i in range(n)]
    return [
        [
            Q(0) if i == j else (s[i] + N * s[j]) / (n * (n - 2))
            for j in range(n)
        ]
        for i in range(n)
    ]


def active_operator(rows: list[list[Q]]) -> tuple[list[State], Operator]:
    n = len(rows)
    states = [
        (B, v)
        for v in range(n)
        for B in range(1, 1 << n)
        if not ((B >> v) & 1)
    ]
    index = {state: position for position, state in enumerate(states)}
    operator: Operator = []
    for B, v in states:
        k = B.bit_count()
        row: dict[int, Q] = {}

        def add(target: State, mass: Q) -> None:
            j = index[target]
            row[j] = row.get(j, Q(0)) + mass

        for i, mass in enumerate(rows[v]):
            if mass:
                add((B | (1 << i), v), mass / 2)
        for w in range(n):
            if (B >> w) & 1:
                C = B & ~(1 << w)
                for i, mass in enumerate(rows[w]):
                    if mass:
                        add((C | (1 << i), w), mass / (2 * k))
        assert sum(row.values(), Q(0)) == 1
        operator.append(row)
    return states, operator


def operator_average(operators: list[Operator]) -> Operator:
    count = len(operators)
    answer: Operator = []
    for row_index in range(len(operators[0])):
        row: dict[int, Q] = {}
        for operator in operators:
            for target, mass in operator[row_index].items():
                row[target] = row.get(target, Q(0)) + mass / count
        answer.append({target: mass for target, mass in row.items() if mass})
    return answer


def operator_mix(left: Operator, right: Operator, weight: Q) -> Operator:
    """Return ``weight*left + (1-weight)*right``."""

    answer: Operator = []
    for left_row, right_row in zip(left, right):
        row: dict[int, Q] = {}
        for target, mass in left_row.items():
            row[target] = row.get(target, Q(0)) + weight * mass
        for target, mass in right_row.items():
            row[target] = row.get(target, Q(0)) + (1 - weight) * mass
        answer.append({target: mass for target, mass in row.items() if mass})
    return answer


def apply(operator: Operator, vector: list[Q]) -> list[Q]:
    return [
        sum((mass * vector[target] for target, mass in row.items()), Q(0))
        for row in operator
    ]


def add_scaled(
    left: list[Q] | None,
    left_scale: Q,
    right: list[Q] | None,
    right_scale: Q,
) -> list[Q]:
    if left is None:
        assert right is not None
        return [right_scale * value for value in right]
    if right is None:
        return [left_scale * value for value in left]
    return [
        left_scale * left_value + right_scale * right_value
        for left_value, right_value in zip(left, right)
    ]


def dot(left: list[Q], right: list[Q]) -> Q:
    return sum((x * y for x, y in zip(left, right)), Q(0))


def conditional_controls(
    A: Operator,
    B: Operator,
    H: list[Q],
    final_time: int,
) -> list[list[Q]]:
    """Return controls conditional on the count of ``A``-coloured times."""

    controls = [H]
    for time in range(1, final_time + 1):
        previous = controls
        controls = []
        for count in range(time + 1):
            B_part = apply(B, previous[count]) if count < time else None
            A_part = apply(A, previous[count - 1]) if count else None
            controls.append(
                add_scaled(
                    B_part,
                    Q(time - count, time),
                    A_part,
                    Q(count, time),
                )
            )
    return controls


def direct_two_colour_control(
    K0: Operator,
    A: Operator,
    H: list[Q],
    final_time: int,
) -> list[Q]:
    """Return the degree-``t`` Bernstein control with two ``A`` updates."""

    controls: list[list[Q] | None] = [H, None, None]
    for time in range(1, final_time + 1):
        previous = controls
        controls = [None, None, None]
        for count in range(min(2, time) + 1):
            K_part = (
                apply(K0, previous[count])
                if count < time and previous[count] is not None
                else None
            )
            A_part = (
                apply(A, previous[count - 1])
                if count and previous[count - 1] is not None
                else None
            )
            controls[count] = add_scaled(
                K_part,
                Q(time - count, time),
                A_part,
                Q(count, time),
            )
    assert controls[2] is not None
    return controls[2]


def count_sign_changes(values: list[Q]) -> int:
    signs = [1 if value > 0 else -1 if value < 0 else 0 for value in values]
    signs = [sign for sign in signs if sign]
    return sum(left != right for left, right in zip(signs, signs[1:]))


def main() -> None:
    n = 5
    N = n - 1
    pin = 0
    final_time = 21
    p0 = Q(1, n)

    P0 = replacement_complete(n)
    Qx = replacement_pin(n, pin)
    embedding = standard_embedding(n, pin)
    embedding_scale = Q(N - 1, N)
    for i in range(n):
        for j in range(n):
            assert Qx[i][j] - P0[i][j] == embedding_scale * embedding[i][j]

    states, K0_direct = active_operator(P0)
    pin_operators = [active_operator(replacement_pin(n, x))[1] for x in range(n)]
    A = pin_operators[pin]
    B = operator_average([pin_operators[x] for x in range(n) if x != pin])
    K0_from_pins = operator_mix(A, B, p0)
    assert K0_from_pins == K0_direct

    # Q_x-P_0=(1-p_0)(Q_x-Q_bar), and active-kernel linearity preserves it.
    line_scale = 1 - p0
    for row_A, row_B, row_0 in zip(A, B, K0_direct):
        targets = set(row_A) | set(row_B) | set(row_0)
        for target in targets:
            delta = row_A.get(target, Q(0)) - row_0.get(target, Q(0))
            pin_line = row_A.get(target, Q(0)) - row_B.get(target, Q(0))
            assert delta == line_scale * pin_line

    nu = [
        Q(Bset.bit_count(), n * N * 2 ** (N - 1))
        for Bset, _v in states
    ]
    H = [Q(1, Bset.bit_count()) for Bset, _v in states]
    baseline = dot(nu, H)

    controls = conditional_controls(A, B, H, final_time)
    psi = [dot(nu, vector) for vector in controls]
    curvature = [
        psi[count + 2] - 2 * psi[count + 1] + psi[count]
        for count in range(final_time - 1)
    ]
    expected_negative = Q(
        -6721646494761620342351,
        10038636664090908488047263744,
    )
    assert curvature[19] == expected_negative
    assert [count for count, value in enumerate(curvature) if value < 0] == [19]

    weighted_curvature = sum(
        Q(comb(final_time - 2, count))
        * p0**count
        * (1 - p0) ** (final_time - 2 - count)
        * value
        for count, value in enumerate(curvature)
    )
    assert weighted_curvature > 0

    direct_control = direct_two_colour_control(K0_direct, A, H, final_time)
    direct_b = dot(nu, direct_control) - baseline
    assert direct_b == line_scale**2 * weighted_curvature
    assert direct_b > 0

    # Finite exact one-crossing audit.  This is evidence for a possible
    # sign-regularity theorem, not a proof beyond the checked range.
    controls = [H]
    for time in range(1, 31):
        previous = controls
        controls = []
        for count in range(time + 1):
            B_part = apply(B, previous[count]) if count < time else None
            A_part = apply(A, previous[count - 1]) if count else None
            controls.append(
                add_scaled(
                    B_part,
                    Q(time - count, time),
                    A_part,
                    Q(count, time),
                )
            )
        if time >= 2:
            values = [dot(nu, vector) for vector in controls]
            second = [
                values[count + 2] - 2 * values[count + 1] + values[count]
                for count in range(time - 1)
            ]
            assert count_sign_changes(second) <= 1
            if any(value < 0 for value in second):
                first_negative = next(i for i, value in enumerate(second) if value < 0)
                assert all(value < 0 for value in second[first_negative:])

    print("PASS: exact pin-mixture and standard-embedding scales")
    print("PASS: binomial second-difference identity matches independent b_(21,2)")
    print(f"EXACT NEGATIVE CURVATURE: {expected_negative}")
    print(f"EXACT POSITIVE BINOMIAL MEAN: {weighted_curvature}")
    print("EXACT FINITE SCREEN: one curvature sign change for n=5, 2<=t<=30")
    print("OPEN: prove the weighted curvature sign and one-crossing property for all n,t")


if __name__ == "__main__":
    main()
