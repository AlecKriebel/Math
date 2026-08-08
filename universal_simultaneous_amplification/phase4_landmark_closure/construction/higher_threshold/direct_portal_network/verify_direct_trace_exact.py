#!/usr/bin/env python3
"""Independent exact audit of the labelled direct-portal episode trace.

This uses a rational Q=3,T=2 instance with a complete unequal portal
network.  It constructs every nonempty labelled portal subset from the raw
atomic rates, solves the phase-type transform, and checks the normalized
load/fraction survival maps and parent lifetime laws.
"""

from __future__ import annotations

import itertools

import sympy as sp


def checked_zero(expression, label):
    value = sp.factor(sp.cancel(expression))
    if value != 0:
        raise AssertionError(f"{label}: {value}")
    print("PASS", label)


def solve_episode(rule, r, pi, lam, portal, z):
    q = len(lam)
    types = len(pi)
    loads = [2 * sum(pi[t] * lam[a][t] for t in range(types))
             for a in range(q)]
    degrees = [loads[a] + sum(portal[a][b] for b in range(q))
               for a in range(q)]
    masks = list(range(1, 1 << q))
    row = {mask: j for j, mask in enumerate(masks)}
    matrix = sp.zeros(len(masks))
    rhs = sp.zeros(len(masks), 1)

    for mask in masks:
        active = [a for a in range(q) if mask >> a & 1]
        inactive = [a for a in range(q) if not mask >> a & 1]
        transitions = []
        if rule == "Bd":
            for a in active:
                transitions.append((
                    mask ^ (1 << a),
                    loads[a] + sum(portal[a][b] / degrees[b]
                                   for b in inactive),
                ))
            for b in inactive:
                transitions.append((
                    mask | (1 << b),
                    r * sum(portal[a][b] / degrees[a] for a in active),
                ))
            child = [
                2 * pi[t] * r**2 / (r + 1)
                * sum(lam[a][t] / degrees[a] for a in active)
                for t in range(types)
            ]
        elif rule == "dB":
            for a in active:
                resident = loads[a] + sum(portal[a][b] for b in inactive)
                mutant = sum(portal[a][b] for b in active if b != a)
                transitions.append((
                    mask ^ (1 << a), resident / (resident + r * mutant)
                ))
            for b in inactive:
                mutant = sum(portal[a][b] for a in active)
                resident = loads[b] + sum(
                    portal[b][c] for c in inactive if c != b
                )
                transitions.append((
                    mask | (1 << b), r * mutant / (resident + r * mutant)
                ))
            child = [pi[t] * r * sum(lam[a][t] for a in active)
                     for t in range(types)]
        else:
            raise ValueError(rule)

        killing = sum(child[t] * (1 - z[t]) for t in range(types))
        j = row[mask]
        matrix[j, j] = sum(rate for _, rate in transitions) + killing
        for nxt, rate in transitions:
            if nxt:
                matrix[j, row[nxt]] -= rate
            else:
                rhs[j] += rate

        # The PGF first-step row has exact total mass after the absorbing
        # empty-set term and marked-child killing are restored.
        checked_zero(
            matrix[j, j]
            + sum(matrix[j, k] for k in range(len(masks)) if k != j)
            - rhs[j] - killing,
            f"{rule} row balance subset {mask}",
        )

    solution = matrix.inv() * rhs
    return solution, row, loads, degrees


def main():
    r = sp.Rational(31, 20)
    pi = (sp.Rational(3, 8), sp.Rational(5, 8))
    lam = (
        (sp.Rational(2, 5), sp.Rational(7, 9)),
        (sp.Rational(11, 8), sp.Rational(1, 6)),
        (sp.Rational(4, 7), sp.Rational(13, 10)),
    )
    portal = (
        (0, sp.Rational(2, 3), sp.Rational(5, 11)),
        (sp.Rational(2, 3), 0, sp.Rational(7, 13)),
        (sp.Rational(5, 11), sp.Rational(7, 13), 0),
    )
    z = (sp.Rational(3, 10), sp.Rational(8, 15))
    q, types = 3, 2

    solutions = {}
    for rule in ("Bd", "dB"):
        solution, row, loads, degrees = solve_episode(
            rule, r, pi, lam, portal, z
        )
        solutions[rule] = (solution, row)

        # At z=(1,1), the PGF is identically one on all transient states.
        normalized, normalized_row, _, _ = solve_episode(
            rule, r, pi, lam, portal, (sp.Integer(1), sp.Integer(1))
        )
        for mask in range(1, 1 << q):
            checked_zero(normalized[normalized_row[mask]] - 1,
                         f"{rule} PGF normalization subset {mask}")

        # Reconstruct every marked-child killing rate from B,f and row marks.
        frac = [[2 * pi[t] * lam[a][t] / loads[a] for t in range(types)]
                for a in range(q)]
        marks = [sum(frac[a][t] * (1 - z[t]) for t in range(types))
                 for a in range(q)]
        for mask in range(1, 1 << q):
            active = [a for a in range(q) if mask >> a & 1]
            if rule == "Bd":
                raw = sum(
                    2 * pi[t] * r**2 / (r + 1)
                    * sum(lam[a][t] / degrees[a] for a in active)
                    * (1 - z[t])
                    for t in range(types)
                )
                reduced = r**2 / (r + 1) * sum(
                    loads[a] * marks[a] / degrees[a] for a in active
                )
            else:
                raw = sum(
                    pi[t] * r * sum(lam[a][t] for a in active)
                    * (1 - z[t])
                    for t in range(types)
                )
                reduced = r / 2 * sum(loads[a] * marks[a] for a in active)
            checked_zero(raw - reduced,
                         f"{rule} normalized killing subset {mask}")

        # Compare the raw parent death/seeding law with (10)--(11).
        singleton_h = [1 - solution[row[1 << a]] for a in range(q)]
        for t in range(types):
            frac = [2 * pi[t] * lam[a][t] / loads[a] for a in range(q)]
            if rule == "Bd":
                death = 2 / (r + 1) * sum(
                    lam[a][t] / degrees[a] for a in range(q)
                )
                killed = 2 * r * sum(
                    lam[a][t] * singleton_h[a] for a in range(q)
                )
                odds = r * (r + 1) * sum(
                    loads[a] * frac[a] * singleton_h[a] for a in range(q)
                ) / sum(loads[a] * frac[a] / degrees[a] for a in range(q))
            else:
                death = sum(lam[a][t] for a in range(q)) / r
                killed = 2 * r * sum(
                    lam[a][t] * singleton_h[a] / degrees[a]
                    for a in range(q)
                )
                odds = 2 * r**2 * sum(
                    loads[a] * frac[a] * singleton_h[a] / degrees[a]
                    for a in range(q)
                ) / sum(loads[a] * frac[a] for a in range(q))
            checked_zero(killed / death - odds,
                         f"{rule} normalized parent odds type {t}")

    print("ALL DIRECT-PORTAL TRACE CHECKS PASS")


if __name__ == "__main__":
    main()
