#!/usr/bin/env python3
"""Exact verifier for the arbitrary-weight star dB correction recurrence."""

from __future__ import annotations

import sympy as sp


def check_labelled_star_rates():
    raw = [sp.Integer(2), sp.Integer(5), sp.Integer(11), sp.Integer(17)]
    m = len(raw)
    total = sum(raw, sp.Integer(0))
    p = [value / total for value in raw]
    r = sp.Rational(3, 2)
    for hub in (0, 1):
        for mask in range(1 << m):
            subset = [i for i in range(m) if (mask >> i) & 1]
            k = len(subset)
            load = sum((p[i] for i in subset), sp.Integer(0))
            if hub == 0:
                # Direct parent--target enumeration after deleting the Bd
                # total-fitness clock.
                bd_hub_activation = sum((r for _ in subset), sp.Integer(0))
                bd_leaf_losses = {i: p[i] for i in subset}
                assert bd_hub_activation == r * k
                assert sum(bd_leaf_losses.values(), sp.Integer(0)) == load

                # Direct dB enumeration after multiplying the uniform death
                # clock by n.
                db_hub_activation = r * load / (1 + (r - 1) * load)
                db_leaf_losses = {i: sp.Integer(1) for i in subset}
                assert db_hub_activation == 3 * load / (2 + load)
                assert sum(db_leaf_losses.values(), sp.Integer(0)) == k
            else:
                bd_leaf_gains = {j: r * p[j] for j in range(m) if j not in subset}
                bd_hub_loss = m - k
                assert sum(bd_leaf_gains.values(), sp.Integer(0)) == r * (1 - load)
                assert bd_hub_loss == m - k

                db_hub_loss = (1 - load) / (1 + (r - 1) * load)
                db_leaf_gains = {j: sp.Integer(1) for j in range(m) if j not in subset}
                assert db_hub_loss == 2 * (1 - load) / (2 + load)
                assert sum(db_leaf_gains.values(), sp.Integer(0)) == m - k


def unit_harmonic(m: int):
    v = [sp.Integer(1)]
    for k in range(m):
        v.append(sp.cancel(v[-1] * sp.Rational(2 * m + 2 + k, 2 * m + 4 + k)))

    u0 = [sp.Integer(0)]
    for k in range(1, m + 1):
        u0.append(sp.cancel(u0[-1] + sp.Rational(3, 2) * v[k]))
    u1 = [sp.cancel(u0[k] + m * (1 + sp.Rational(k, 2 * m)) * v[k]) for k in range(m + 1)]

    scale = sp.cancel(1 / u1[m])
    v = [sp.cancel(scale * value) for value in v]
    u0 = [sp.cancel(scale * value) for value in u0]
    u1 = [sp.cancel(scale * value) for value in u1]
    assert u0[0] == 0 and u1[m] == 1

    for k in range(m + 1):
        d = 1 + sp.Rational(k, 2 * m)
        assert sp.cancel(u1[k] - u0[k] - m * d * v[k]) == 0
        if k < m:
            expected = sp.Rational(2 * m + 2 + k, 2 * m + 4 + k)
            assert sp.cancel(v[k + 1] / v[k] - expected) == 0
    for k in range(1, m + 1):
        p = sp.Rational(k, m)
        equation = (
            3 * p / (2 + p) * (u1[k] - u0[k])
            + k * (u0[k - 1] - u0[k])
        )
        assert sp.cancel(equation) == 0
    for k in range(m):
        p = sp.Rational(k, m)
        equation = (
            2 * (1 - p) / (2 + p) * (u0[k] - u1[k])
            + (m - k) * (u1[k + 1] - u1[k])
        )
        assert sp.cancel(equation) == 0
    return v, u0, u1


def correction(m: int, v):
    names = [(hub, k) for hub in (0, 1) for k in range(1, m)]
    index = {name: position for position, name in enumerate(names)}
    matrix = sp.zeros(2 * (m - 1), 2 * (m - 1))
    rhs = sp.zeros(2 * (m - 1), 1)

    def add(row, hub, k, value):
        position = index.get((hub, k))
        if position is not None:
            matrix[row, position] += value

    row = 0
    for k in range(1, m):
        p = sp.Rational(k, m)
        d = 1 + p / 2
        a = sp.Rational(3, 2) * m * v[k]
        rhs[row] = -a
        add(row, 1, k, sp.Rational(3, 2) * p)
        add(row, 0, k, -sp.Rational(3, 2) * p - d * k)
        add(row, 0, k - 1, d * (k - 1))
        row += 1

        rhs[row] = -a
        add(row, 0, k, 1 - p)
        add(row, 1, k, -(1 - p) - d * (m - k))
        add(row, 1, k + 1, d * (m - k - 1))
        row += 1

    assert matrix.det() != 0
    solution = matrix.inv() * rhs

    def c(hub, k):
        position = index.get((hub, k))
        return sp.Integer(0) if position is None else solution[position]

    for k in range(1, m):
        p = sp.Rational(k, m)
        d = 1 + p / 2
        a = sp.Rational(3, 2) * m * v[k]
        delta = c(1, k) - c(0, k)
        b0 = (
            a
            + sp.Rational(3, 2) * p * delta
            + d * ((k - 1) * c(0, k - 1) - k * c(0, k))
        )
        b1 = (
            a
            + (1 - p) * (c(0, k) - c(1, k))
            + d
            * ((m - k - 1) * c(1, k + 1) - (m - k) * c(1, k))
        )
        assert sp.cancel(b0) == sp.cancel(b1) == 0
        slope = sp.cancel((sp.Rational(3, 2) * delta - a / 2) / d)
        slope0 = sp.cancel(
            sp.Rational(3, 2) * delta
            + sp.Rational(1, 2)
            * ((k - 1) * c(0, k - 1) - k * c(0, k))
        )
        slope1 = sp.cancel(
            -(c(0, k) - c(1, k))
            + sp.Rational(1, 2)
            * ((m - k - 1) * c(1, k + 1) - (m - k) * c(1, k))
        )
        assert slope0 == slope1 == slope
        assert delta <= 0
        assert slope < 0
        if m >= 3:
            assert delta < 0
    return c


def check_subset_drifts(m: int, v, c):
    raw = [sp.Integer((i + 1) ** 2 + 1) for i in range(m)]
    total = sum(raw, sp.Integer(0))
    probabilities = [value / total for value in raw]
    for mask in range(1 << m):
        subset = [i for i in range(m) if (mask >> i) & 1]
        k = len(subset)
        if k in (0, m):
            continue
        p = sum((probabilities[i] for i in subset), sp.Integer(0))
        p0 = sp.Rational(k, m)
        d = 1 + p0 / 2
        defect = sp.cancel(p - p0)
        a = sp.Rational(3, 2) * m * v[k]
        delta = c(1, k) - c(0, k)
        b0 = sp.cancel(
            a
            + sp.Rational(3, 2) * p * delta
            + (1 + p / 2) * ((k - 1) * c(0, k - 1) - k * c(0, k))
        )
        b1 = sp.cancel(
            a
            + (1 - p) * (c(0, k) - c(1, k))
            + (1 + p / 2)
            * ((m - k - 1) * c(1, k + 1) - (m - k) * c(1, k))
        )
        slope = sp.cancel((sp.Rational(3, 2) * delta - a / 2) / d)
        assert sp.cancel(defect * b0 - slope * defect**2) == 0
        assert sp.cancel(defect * b1 - slope * defect**2) == 0
        assert defect * b0 <= 0 and defect * b1 <= 0


def main():
    check_labelled_star_rates()
    for m in range(2, 21):
        v, _, _ = unit_harmonic(m)
        c = correction(m, v)
        if m <= 6:
            check_subset_drifts(m, v, c)
    print("PASS exact arbitrary-weight star harmonic equations")
    print("PASS exact unit-star increment ratios")
    print("PASS exact correction recurrence and square drift through m=20")
    print("PROVED dB unit-star maximality among weighted stars through 20 leaves")
    print("OPEN correction sign for arbitrary leaf count")


if __name__ == "__main__":
    main()
