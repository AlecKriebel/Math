#!/usr/bin/env python3
"""Exact complete-kernel Hessian in a transposition-odd four-cycle direction.

The direction has nonzero entries

    Delta_02=Delta_13=+1,  Delta_03=Delta_12=-1,

and is symmetric with zero row sums.  At the complete kernel, vertices
4,...,n-1 remain exchangeable, so the labelled chain lumps exactly by the
mutant mask on vertices 0,1,2,3 and the number of other mutants.  The script
differentiates the lumped absorbing equations twice over QQ.
"""

from __future__ import annotations

import argparse

import sympy as sp


def derivative_rates(x: sp.Rational, z: sp.Rational, mutant: bool):
    h0 = 2 * x / (1 + x)
    h1 = 2 * z / (1 + x) ** 2
    h2 = -4 * z**2 / (1 + x) ** 3
    if mutant:
        return 1 - h0, -h1, -h2
    return h0, h1, h2


def exact_hessian(n: int):
    if n < 4:
        raise ValueError(n)
    ordinary = n - 4
    empty = (0, 0)
    full = (15, ordinary)
    states = [
        (mask, count)
        for count in range(ordinary + 1)
        for mask in range(16)
        if (mask, count) not in (empty, full)
    ]
    index = {state: row for row, state in enumerate(states)}
    matrices = [sp.MutableSparseMatrix(len(states), len(states), {}) for _ in range(3)]
    rhs = [sp.zeros(len(states), 1) for _ in range(3)]

    delta = sp.zeros(4, 4)
    for u, v, value in ((0, 2, 1), (1, 3, 1), (0, 3, -1), (1, 2, -1)):
        delta[u, v] = delta[v, u] = value

    def add_move(row, target, rates, multiplicity=1):
        for order in range(3):
            rate = multiplicity * rates[order]
            matrices[order][row, row] += rate
            if target == full:
                rhs[order][row] += rate
            elif target != empty:
                matrices[order][row, index[target]] -= rate

    for row, (mask, count) in enumerate(states):
        # Four distinguished targets.
        for v in range(4):
            is_mutant = bool(mask >> v & 1)
            special_mass = sum(
                sp.Rational(1, n - 1)
                for u in range(4)
                if mask >> u & 1 and u != v
            )
            x = special_mass + sp.Rational(count, n - 1)
            z = sum(
                (delta[v, u] for u in range(4) if mask >> u & 1),
                sp.Integer(0),
            )
            next_mask = mask & ~(1 << v) if is_mutant else mask | (1 << v)
            add_move(row, (next_mask, count), derivative_rates(x, z, is_mutant))

        # Exchangeable ordinary targets.  Their perturbation mass is zero.
        if count:
            x = sp.Rational(mask.bit_count() + count - 1, n - 1)
            add_move(
                row,
                (mask, count - 1),
                derivative_rates(x, sp.Integer(0), True),
                count,
            )
        if count < ordinary:
            x = sp.Rational(mask.bit_count() + count, n - 1)
            add_move(
                row,
                (mask, count + 1),
                derivative_rates(x, sp.Integer(0), False),
                ordinary - count,
            )

    A0, A1, A2 = (sp.SparseMatrix(matrix) for matrix in matrices)
    h0 = sp.linsolve((A0, rhs[0]))
    h0 = sp.Matrix(next(iter(h0)))
    h1 = sp.Matrix(next(iter(sp.linsolve((A0, rhs[1] - A1 * h0)))))
    h2 = sp.Matrix(
        next(iter(sp.linsolve((A0, rhs[2] - A2 * h0 - 2 * A1 * h1))))
    )

    alpha = sp.zeros(1, len(states))
    for v in range(4):
        alpha[0, index[(1 << v, 0)]] += sp.Rational(1, n)
    if ordinary:
        alpha[0, index[(0, 1)]] += sp.Rational(ordinary, n)
    occupation = sp.Matrix(next(iter(sp.linsolve((A0.T, alpha.T)))))
    direct = sp.factor((occupation.T * (rhs[2] - A2 * h0))[0])
    response = sp.factor((-2 * occupation.T * A1 * h1)[0])
    value = sp.factor(direct + response)
    assert value == sp.factor((alpha * h2)[0])
    assert direct < 0 < response < -direct
    assert value < 0
    return value, direct, response, len(states)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--min-n", type=int, default=4)
    parser.add_argument("--max-n", type=int, default=10)
    args = parser.parse_args()
    for n in range(args.min_n, args.max_n + 1):
        value, direct, response, states = exact_hessian(n)
        print(
            n,
            states,
            value,
            float(value),
            "direct",
            direct,
            "response_ratio",
            sp.factor(response / -direct),
        )


if __name__ == "__main__":
    main()
