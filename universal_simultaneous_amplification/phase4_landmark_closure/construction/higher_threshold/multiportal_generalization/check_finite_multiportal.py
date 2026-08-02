#!/usr/bin/env python3
"""Independent finite-chain audit for exchangeable multiportal modules.

The exact lumped state is (k,z,u): mutant portals, all-resident blades, and
heterotypic blades.  The remaining blades are all mutant.  Every rate below
is built directly from one atomic Bd or dB update, independently of the
limiting episode recurrence.
"""

from __future__ import annotations

import argparse
from collections import defaultdict

import numpy as np
from scipy.sparse import csr_matrix
from scipy.sparse.linalg import spsolve

from explore_multiportal import extinction


State = tuple[int, int, int]


def states(s: int, q: int) -> list[State]:
    return [
        (k, z, u)
        for k in range(q + 1)
        for z in range(s + 1)
        for u in range(s - z + 1)
    ]


def add(out: dict[State, float], state: State, rate: float) -> None:
    if rate > 0.0:
        out[state] += rate


def transitions_bd(
    state: State, s: int, q: int, r: float, c: float, theta: float
) -> dict[State, float]:
    k, z, u = state
    v = s - z - u
    mutant_blade_vertices = u + 2 * v
    resident_blade_vertices = 2 * z + u
    a = c / s
    h = 2.0 * c * theta / (q - 1)
    blade_degree = 1.0 + q * a
    portal_degree = 2.0 * c + (q - 1) * h
    out: dict[State, float] = defaultdict(float)

    if k < q:
        cross_gain = r * k * (q - k) * h / portal_degree
        blade_gain = (
            r
            * mutant_blade_vertices
            * (q - k)
            * a
            / blade_degree
        )
        add(out, (k + 1, z, u), cross_gain + blade_gain)
    if k > 0:
        cross_loss = k * (q - k) * h / portal_degree
        blade_loss = resident_blade_vertices * k * a / blade_degree
        add(out, (k - 1, z, u), cross_loss + blade_loss)

    if k > 0:
        add(
            out,
            (k, z - 1, u + 1),
            r * k * (2 * z) * a / portal_degree if z else 0.0,
        )
        add(
            out,
            (k, z, u - 1),
            r * k * u * a / portal_degree if u else 0.0,
        )
    if k < q:
        add(
            out,
            (k, z, u + 1),
            (q - k) * (2 * v) * a / portal_degree if v else 0.0,
        )
        add(
            out,
            (k, z + 1, u - 1),
            (q - k) * u * a / portal_degree if u else 0.0,
        )

    if u:
        add(out, (k, z, u - 1), r * u / blade_degree)
        add(out, (k, z + 1, u - 1), u / blade_degree)
    return out


def transitions_db(
    state: State, s: int, q: int, r: float, c: float, theta: float
) -> dict[State, float]:
    k, z, u = state
    v = s - z - u
    mutant_blade_vertices = u + 2 * v
    resident_blade_vertices = 2 * z + u
    a = c / s
    h = 2.0 * c * theta / (q - 1)
    out: dict[State, float] = defaultdict(float)

    if k < q:
        mutant_mass = r * (mutant_blade_vertices * a + k * h)
        resident_mass = resident_blade_vertices * a + (q - k - 1) * h
        add(
            out,
            (k + 1, z, u),
            (q - k) * mutant_mass / (mutant_mass + resident_mass),
        )
    if k > 0:
        mutant_mass = r * (mutant_blade_vertices * a + (k - 1) * h)
        resident_mass = resident_blade_vertices * a + (q - k) * h
        add(
            out,
            (k - 1, z, u),
            k * resident_mass / (mutant_mass + resident_mass),
        )

    if z:
        mutant_mass = r * k * a
        resident_mass = 1.0 + (q - k) * a
        add(
            out,
            (k, z - 1, u + 1),
            2 * z * mutant_mass / (mutant_mass + resident_mass),
        )
    if v:
        mutant_mass = r * (1.0 + k * a)
        resident_mass = (q - k) * a
        add(
            out,
            (k, z, u + 1),
            2 * v * resident_mass / (mutant_mass + resident_mass),
        )
    if u:
        mutant_mass = r * (1.0 + k * a)
        resident_mass = (q - k) * a
        add(
            out,
            (k, z, u - 1),
            u * mutant_mass / (mutant_mass + resident_mass),
        )

        mutant_mass = r * k * a
        resident_mass = 1.0 + (q - k) * a
        add(
            out,
            (k, z + 1, u - 1),
            u * resident_mass / (mutant_mass + resident_mass),
        )
    return out


def fixation(
    s: int, q: int, r: float, c: float, theta: float, rule: str
) -> tuple[float, float, float]:
    all_states = states(s, q)
    extinct = (0, s, 0)
    fixed = (q, 0, 0)
    transient = [state for state in all_states if state not in (extinct, fixed)]
    index = {state: i for i, state in enumerate(transient)}
    rows: list[int] = []
    cols: list[int] = []
    data: list[float] = []
    rhs = np.zeros(len(transient))
    transition = transitions_bd if rule == "Bd" else transitions_db
    for state in transient:
        i = index[state]
        outgoing = transition(state, s, q, r, c, theta)
        total = sum(outgoing.values())
        rows.append(i)
        cols.append(i)
        data.append(total)
        for target, rate in outgoing.items():
            if target == fixed:
                rhs[i] += rate
            elif target != extinct:
                rows.append(i)
                cols.append(index[target])
                data.append(-rate)
    matrix = csr_matrix((data, (rows, cols)), shape=(len(transient), len(transient)))
    solution = spsolve(matrix, rhs)
    blade = float(solution[index[(0, s - 1, 1)]])
    portal = float(solution[index[(1, s, 0)]])
    average = (2.0 * s * blade + q * portal) / (2.0 * s + q)
    return blade, portal, average


def complete_baseline(n: int, r: float, rule: str) -> float:
    if rule == "Bd":
        return (1.0 - 1.0 / r) / (1.0 - r ** (-n))
    product = 1.0
    total = 1.0
    for k in range(1, n):
        ratio = (r * k + n - k - 1.0) / (r * (r * (k - 1) + n - k))
        product *= ratio
        total += product
    return 1.0 / total


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--q", type=int, default=3)
    parser.add_argument("--r", type=float, default=8.0 / 5.0)
    parser.add_argument("--c", type=float, default=0.35)
    parser.add_argument("--g", type=float, default=0.4)
    parser.add_argument("--sizes", type=int, nargs="+", default=[8, 16, 32])
    args = parser.parse_args()
    theta = args.g / (1.0 - args.g)
    qb = extinction(args.q, args.r, args.c, args.g, "Bd")
    qd = extinction(args.q, args.r, args.c, args.g, "dB")
    limit_bd = args.r / (args.r + 1.0) * (1.0 - qb)
    limit_db = 0.5 * (1.0 - qd)
    print(
        f"Q={args.q} r={args.r} c={args.c} g={args.g} theta={theta}"
    )
    print(f"predicted limits Bd={limit_bd:.12g} dB={limit_db:.12g}")
    for s in args.sizes:
        bd = fixation(s, args.q, args.r, args.c, theta, "Bd")
        db = fixation(s, args.q, args.r, args.c, theta, "dB")
        n = 2 * s + args.q
        kb = complete_baseline(n, args.r, "Bd")
        kd = complete_baseline(n, args.r, "dB")
        print(
            f"s={s:4d} Bd={bd} K_Bd={kb:.12g} "
            f"dB={db} K_dB={kd:.12g}"
        )


if __name__ == "__main__":
    main()
