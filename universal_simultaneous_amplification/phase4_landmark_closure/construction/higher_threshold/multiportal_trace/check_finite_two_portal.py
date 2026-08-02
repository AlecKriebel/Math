#!/usr/bin/env python3
"""Exact-lumping numerical audit for finite homogeneous two-portal modules.

The lumped state is (k,z,u), where k is the number of mutant portals and
z,u are the numbers of all-resident and heterotypic blades.  The remaining
blades are all mutant.  Continuous-time rates are used; their absorption
probabilities equal those of the stated discrete Bd and dB chains.
"""

from __future__ import annotations

import argparse
from collections import defaultdict

import numpy as np
from scipy.sparse import csr_matrix
from scipy.sparse.linalg import spsolve

from search_two_portal import extinction_bd, extinction_db


State = tuple[int, int, int]


def states(s: int) -> list[State]:
    return [(k, z, u) for k in range(3) for z in range(s + 1) for u in range(s - z + 1)]


def add(out: dict[State, float], state: State, rate: float) -> None:
    if rate > 0.0:
        out[state] += rate


def transitions_bd(state: State, s: int, r: float, c: float, theta: float) -> dict[State, float]:
    k, z, u = state
    v = s - z - u
    a = c / s
    h = 2.0 * c * theta
    db = 1.0 + 2.0 * a
    do = 2.0 * c + h
    out: dict[State, float] = defaultdict(float)

    # Portal-to-portal and blade-to-portal replacements.
    if k < 2:
        cross_gain = (r * h / do) if k == 1 else 0.0
        blade_gain = r * (u + 2 * v) * (2 - k) * a / db
        add(out, (k + 1, z, u), cross_gain + blade_gain)
    if k > 0:
        cross_loss = (h / do) if k == 1 else 0.0
        blade_loss = (2 * z + u) * k * a / db
        add(out, (k - 1, z, u), cross_loss + blade_loss)

    # Portal-to-blade replacements.
    if k > 0:
        add(out, (k, z - 1, u + 1), r * k * (2 * z) * a / do if z else 0.0)
        add(out, (k, z, u - 1), r * k * u * a / do if u else 0.0)  # u -> v
    if k < 2:
        add(out, (k, z, u + 1), (2 - k) * (2 * v) * a / do if v else 0.0)
        add(out, (k, z + 1, u - 1), (2 - k) * u * a / do if u else 0.0)

    # Internal strong-pair replacements.
    if u:
        add(out, (k, z, u - 1), r * u / db)  # mutant fixes
        add(out, (k, z + 1, u - 1), u / db)  # resident fixes
    return out


def transitions_db(state: State, s: int, r: float, c: float, theta: float) -> dict[State, float]:
    k, z, u = state
    v = s - z - u
    a = c / s
    h = 2.0 * c * theta
    mcount = u + 2 * v
    rcount = 2 * z + u
    out: dict[State, float] = defaultdict(float)

    # Portal deaths.  For a portal of a specified type, the other portal has
    # type determined by k and the dead portal's type.
    if k < 2:
        other_mutant = 1 if k == 1 else 0
        mut = r * (mcount * a + other_mutant * h)
        res = rcount * a + (1 - other_mutant) * h
        add(out, (k + 1, z, u), (2 - k) * mut / (mut + res))
    if k > 0:
        other_mutant = 1 if k == 2 else 0
        mut = r * (mcount * a + other_mutant * h)
        res = rcount * a + (1 - other_mutant) * h
        add(out, (k - 1, z, u), k * res / (mut + res))

    # Deaths in resident blades.
    if z:
        mut = r * k * a
        res = 1.0 + (2 - k) * a
        add(out, (k, z - 1, u + 1), 2 * z * mut / (mut + res))

    # Deaths in mutant blades.
    if v:
        mut = r * (1.0 + k * a)
        res = (2 - k) * a
        add(out, (k, z, u + 1), 2 * v * res / (mut + res))

    # Heterotypic blade: resident death can fix mutant; mutant death can fix resident.
    if u:
        mut_when_resident_dies = r * (1.0 + k * a)
        res_when_resident_dies = (2 - k) * a
        add(
            out,
            (k, z, u - 1),
            u * mut_when_resident_dies / (mut_when_resident_dies + res_when_resident_dies),
        )
        mut_when_mutant_dies = r * k * a
        res_when_mutant_dies = 1.0 + (2 - k) * a
        add(
            out,
            (k, z + 1, u - 1),
            u * res_when_mutant_dies / (mut_when_mutant_dies + res_when_mutant_dies),
        )
    return out


def fixation(s: int, r: float, c: float, theta: float, rule: str) -> tuple[float, float, float]:
    all_states = states(s)
    extinct = (0, s, 0)
    fixed = (2, 0, 0)
    transient = [x for x in all_states if x not in (extinct, fixed)]
    index = {x: i for i, x in enumerate(transient)}
    rows: list[int] = []
    cols: list[int] = []
    data: list[float] = []
    rhs = np.zeros(len(transient))
    transition = transitions_bd if rule == "Bd" else transitions_db
    for state in transient:
        i = index[state]
        out = transition(state, s, r, c, theta)
        total = sum(out.values())
        rows.append(i)
        cols.append(i)
        data.append(total)
        for target, rate in out.items():
            if target == fixed:
                rhs[i] += rate
            elif target != extinct:
                rows.append(i)
                cols.append(index[target])
                data.append(-rate)
    matrix = csr_matrix((data, (rows, cols)), shape=(len(transient), len(transient)))
    sol = spsolve(matrix, rhs)
    blade = float(sol[index[(0, s - 1, 1)]])
    portal = float(sol[index[(1, s, 0)]])
    average = (2.0 * s * blade + 2.0 * portal) / (2.0 * s + 2.0)
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
    parser.add_argument("--r", type=float, default=8.0 / 5.0)
    parser.add_argument("--c", type=float, default=0.4)
    parser.add_argument("--gamma", type=float, default=0.3)
    parser.add_argument("--sizes", type=int, nargs="+", default=[8, 16, 32, 64])
    args = parser.parse_args()
    theta = args.gamma / (1.0 - args.gamma)
    qb = extinction_bd(args.r, args.c, theta)
    qd = extinction_db(args.r, args.c, theta)
    limit_bd = args.r / (args.r + 1.0) * (1.0 - qb)
    limit_db = 0.5 * (1.0 - qd)
    print(f"r={args.r} c={args.c} gamma={args.gamma} theta={theta}")
    print(f"predicted limits Bd={limit_bd:.12g} dB={limit_db:.12g}")
    for s in args.sizes:
        bd = fixation(s, args.r, args.c, theta, "Bd")
        db = fixation(s, args.r, args.c, theta, "dB")
        n = 2 * s + 2
        kb = complete_baseline(n, args.r, "Bd")
        kd = complete_baseline(n, args.r, "dB")
        print(f"s={s:4d} Bd={bd} K_Bd={kb:.12g} dB={db} K_dB={kd:.12g}")


if __name__ == "__main__":
    main()
