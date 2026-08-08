#!/usr/bin/env python3
"""Exact verifier for the stationary marked one-sample lift at r=2.

The finite screens certify the displayed identities and the explicit
counterexample to event-rank stochastic domination.  They do not prove the
remaining universal harmonic collision inequality.
"""

from __future__ import annotations

import sys
from fractions import Fraction as F
from math import comb
from pathlib import Path


HERE = Path(__file__).resolve().parent
OBSTRUCTION = HERE.parent
CHI = OBSTRUCTION / "r2_entropy_certificate" / "chi_square_channel"
COLLISION = OBSTRUCTION / "r2_collision_closure"
sys.path.insert(0, str(CHI))
sys.path.insert(0, str(COLLISION))

from verify_resolvent_identities import solve  # noqa: E402
from verify_direct_flow_screen import matrix_from_edges  # noqa: E402


def posterior_midpoint(weights):
    P, states, _, kernels, pi = solve(weights)
    n = len(P)
    full = 1 << n
    pi_all = [F(0) for _ in range(full)]
    for state, mass in zip(states, pi):
        pi_all[state] = mass

    sigma = [[F(0) for _ in range(full)] for _ in range(n)]
    nu = [[F(0) for _ in range(full)] for _ in range(n)]
    for v in range(n):
        incoming = [
            sum(
                (pi[source] * kernels[v][source][target]
                 for source in range(len(states))),
                F(0),
            )
            for target in range(len(states))
        ]
        for state, mass in zip(states, incoming):
            if not ((state >> v) & 1):
                nu[v][state] = mass - pi_all[state]
                assert nu[v][state] >= 0
        for C in range(full):
            if not ((C >> v) & 1):
                sigma[v][C] = pi_all[C | (1 << v)]

    lam = [
        [(sigma[v][C] + nu[v][C]) / 2 for C in range(full)]
        for v in range(n)
    ]

    def add_sample(v, measure):
        image = [F(0) for _ in range(full)]
        for C, mass in enumerate(measure):
            if not mass:
                continue
            for i in range(n):
                image[C | (1 << i)] += mass * P[v][i]
        return image

    for v in range(n):
        assert add_sample(v, lam[v]) == nu[v]
    for B in states:
        assert sum(
            (nu[v][B] for v in range(n) if not ((B >> v) & 1)), F(0)
        ) == B.bit_count() * pi_all[B]

    mean = sum(
        (pi_all[state] * state.bit_count() for state in states), F(0)
    )
    assert sum((sum(row, F(0)) for row in lam), F(0)) == mean
    return P, states, pi_all, nu, sigma, lam, mean


def marked_kernel(P):
    n = len(P)
    marked = [
        (C, v)
        for v in range(n)
        for C in range(1 << n)
        if not ((C >> v) & 1)
    ]
    index = {state: position for position, state in enumerate(marked)}
    kernel = [[F(0) for _ in marked] for _ in marked]
    for source, (C, v) in enumerate(marked):
        for i in range(n):
            if not P[v][i]:
                continue
            B = C | (1 << i)
            kernel[source][index[B, v]] += P[v][i] / 2
            size = B.bit_count()
            assert size >= 1
            for w in range(n):
                if (B >> w) & 1:
                    kernel[source][index[B & ~(1 << w), w]] += (
                        P[v][i] / (2 * size)
                    )
        assert sum(kernel[source], F(0)) == 1
    return marked, index, kernel


def marked_data(weights):
    P, states, pi, nu, sigma, lam, mean = posterior_midpoint(weights)
    n = len(P)
    N = n - 1
    marked, index, kernel = marked_kernel(P)
    lam_vector = [lam[v][C] for C, v in marked]

    for target in range(len(marked)):
        assert sum(
            (lam_vector[source] * kernel[source][target]
             for source in range(len(marked))),
            F(0),
        ) == lam_vector[target]

    pi_level = [F(0) for _ in range(n + 1)]
    for state in states:
        pi_level[state.bit_count()] += pi[state]
    Lambda = [F(0) for _ in range(n)]
    cut_mass = [F(0) for _ in range(n)]
    for mass, (C, v) in zip(lam_vector, marked):
        k = C.bit_count()
        Lambda[k] += mass
        cut_mass[k] += mass * sum(
            (P[v][i] for i in range(n) if (C >> i) & 1), F(0)
        )
    for k in range(n):
        assert 2 * Lambda[k] == (k + 1) * pi_level[k + 1] + k * pi_level[k]

    q = [F(0) for _ in range(n + 1)]
    eta = [value / mean for value in Lambda]
    for k in range(1, n):
        q[k] = k * pi_level[k] / mean
    assert sum(q, F(0)) == 1
    for k in range(n):
        assert eta[k] == (q[k] + q[k + 1]) / 2

    # Aggregated nearest-neighbour flux and stationary rank drift.
    assert sum(cut_mass, F(0)) == mean / 2
    for k in range(1, n):
        assert cut_mass[k] == k * pi_level[k] / 2

    psi = [
        2 * sum(
            ((-1) ** (ell - 1 - j) * F(1, ell)
             for ell in range(j + 1, N + 1)),
            F(0),
        )
        for j in range(N + 1)
    ]
    assert sum((eta[k] * psi[k] for k in range(n)), F(0)) == 1 / mean
    assert sum((q[k] / k for k in range(1, n)), F(0)) == 1 / mean

    # The unconditional stopping-and-handoff flow has mass exactly 1/2 in
    # the unnormalised stationary measure, hence probability 1/(2m).
    handoff = F(0)
    for mass, (C, v) in zip(lam_vector, marked):
        for i in range(n):
            if P[v][i]:
                handoff += mass * P[v][i] / (2 * (C | (1 << i)).bit_count())
    assert handoff == F(1, 2)

    return {
        "n": n,
        "mean": mean,
        "q": q,
        "eta": eta,
        "psi": psi,
        "handoff": handoff,
    }


def audit_complete_and_path():
    path = [[0, 1, 0], [1, 0, 1], [0, 1, 0]]
    data = marked_data(path)
    assert data["mean"] == F(11, 9)
    assert data["q"][1:3] == [F(7, 11), F(4, 11)]
    assert data["eta"] == [F(7, 22), F(1, 2), F(2, 11)]

    for n in range(3, 7):
        complete = [[0 if i == j else 1 for j in range(n)] for i in range(n)]
        complete_data = marked_data(complete)
        expected_eta = [F(comb(n - 1, k), 2 ** (n - 1)) for k in range(n)]
        expected_q = [F(0)] + [
            F(comb(n - 2, k - 1), 2 ** (n - 2)) for k in range(1, n)
        ] + [F(0)]
        assert complete_data["eta"] == expected_eta
        assert complete_data["q"] == expected_q
        complete_mean = F((n - 1) * 2 ** (n - 2), 2 ** (n - 1) - 1)
        assert complete_data["mean"] == complete_mean

    print("PASS: exact marked stationarity, path values, and complete binomial law")


def audit_tail_counterexample():
    weights = matrix_from_edges(
        6,
        (1, 3, 3, 1000, 30, 1000, 300, 3, 1, 10, 1, 30, 1, 300, 30),
    )
    data = marked_data(weights)
    q = data["q"]
    complete_tail = F(15, 16)
    tail_excess = sum(q[2:], F(0)) - complete_tail
    assert tail_excess > 0

    complete_inverse_mean = F(31, 80)
    harmonic_excess = sum((q[k] / k for k in range(1, 6)), F(0)) - complete_inverse_mean
    assert harmonic_excess > 0
    assert data["mean"] < F(80, 31)

    print(
        "PASS: exact n=6 event-rank tail counterexample; "
        f"tail excess ~{float(tail_excess):.12g}"
    )
    print(
        "PASS: same graph remains below baseline; "
        f"harmonic excess ~{float(harmonic_excess):.12g}"
    )


def main():
    audit_complete_and_path()
    audit_tail_counterexample()
    print("OPEN: universal marked collision inequality, equivalently dB r=2 maximality")


if __name__ == "__main__":
    main()

