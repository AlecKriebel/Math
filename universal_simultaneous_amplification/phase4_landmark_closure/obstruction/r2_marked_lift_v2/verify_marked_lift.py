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


def active_kernel(P):
    """Build the forward active chain K_P=R A_P over exact rationals."""
    n = len(P)
    active = [
        (B, v)
        for v in range(n)
        for B in range(1 << n)
        if B and not ((B >> v) & 1)
    ]
    index = {state: position for position, state in enumerate(active)}
    kernel = [[F(0) for _ in active] for _ in active]
    for source, (B, v) in enumerate(active):
        b = B.bit_count()
        # Continue: keep B and v, then take the next P_v sample.
        for i in range(n):
            if P[v][i]:
                kernel[source][index[B | (1 << i), v]] += P[v][i] / 2
        # Stop: retarget uniformly inside B, delete that target, then sample.
        for w in range(n):
            if not ((B >> w) & 1):
                continue
            C = B & ~(1 << w)
            for i in range(n):
                if P[w][i]:
                    kernel[source][index[C | (1 << i), w]] += P[w][i] / (2 * b)
        assert sum(kernel[source], F(0)) == 1
    return active, index, kernel


def apply_kernel(kernel, values):
    """Apply a row-stochastic kernel to a column observable."""
    return [
        sum((probability * values[target]
             for target, probability in enumerate(row)), F(0))
        for row in kernel
    ]


def propagate_law(law, kernel):
    """Propagate a row law through a row-stochastic kernel."""
    return [
        sum((law[source] * kernel[source][target]
             for source in range(len(kernel))), F(0))
        for target in range(len(kernel))
    ]


def two_step_gap(P, t):
    """Return U M_P^2 t^K - U t^K by direct exact enumeration."""
    marked, _, kernel = marked_kernel(P)
    values = [t ** C.bit_count() for C, _ in marked]
    twice = apply_kernel(kernel, apply_kernel(kernel, values))
    return (sum(twice, F(0)) - sum(values, F(0))) / len(marked)


def two_step_formula(P, t):
    """Closed sum-of-squares formula for the two-step radial gap."""
    n = len(P)
    assert n >= 3
    row_square = sum(
        (P[v][i] ** 2 for v in range(n) for i in range(n)), F(0)
    )
    columns = [sum((P[v][i] for v in range(n)), F(0)) for i in range(n)]
    column_square = sum((value ** 2 for value in columns), F(0))
    mutual = sum(
        (P[v][i] * P[i][v] for v in range(n) for i in range(n)), F(0)
    )

    row_defect = row_square - F(n, n - 1)
    assert row_defect >= 0
    transport_defect = (column_square - mutual) - (n - row_square)
    transport_sos = sum(((value - 1) ** 2 for value in columns), F(0))
    transport_sos += sum(
        ((P[v][i] - P[i][v]) ** 2
         for v in range(n) for i in range(n)), F(0)
    ) / 2
    assert transport_defect == transport_sos
    assert transport_defect >= 0

    if n == 3:
        return (1 - t ** 2) * row_defect / 24

    s = n - 2
    binomial_sum = sum(
        (F(comb(s - 2, j), j + 2) * t ** j for j in range(s - 1)), F(0)
    )
    beta = (1 - t ** 2) * binomial_sum / (4 * n * 2 ** s)
    alpha = (1 - t ** 2) * (
        (1 + t) ** (s - 1) / 2 - binomial_sum
    ) / (2 * n * 2 ** s)
    assert alpha >= 0
    assert beta >= 0
    return alpha * row_defect + beta * transport_defect


def two_step_psi_formula(P):
    """Closed exact value of U M_P^2 psi from the integrated SOS."""
    n = len(P)
    assert n >= 3
    N = n - 1
    complete_inverse_mean = F(2 ** N - 1, N * 2 ** (N - 1))
    row_square = sum(
        (P[v][i] ** 2 for v in range(n) for i in range(n)), F(0)
    )
    columns = [sum((P[v][i] for v in range(n)), F(0)) for i in range(n)]
    column_square = sum((value ** 2 for value in columns), F(0))
    mutual = sum(
        (P[v][i] * P[i][v] for v in range(n) for i in range(n)), F(0)
    )
    row_defect = row_square - F(n, n - 1)
    transport_defect = (column_square - mutual) - (n - row_square)
    assert row_defect >= 0
    assert transport_defect >= 0
    if n == 3:
        return complete_inverse_mean + row_defect / 24

    s = n - 2
    integrated_sum = sum(
        (F(comb(s - 2, j), (j + 1) * (j + 2) ** 2)
         for j in range(s - 1)),
        F(0),
    )
    integrated_half = F(2 ** s - 1, s) - F(2 ** (s + 1) - 1, 2 * (s + 1))
    alpha = (integrated_half - integrated_sum) / (n * 2 ** s)
    beta = integrated_sum / (2 * n * 2 ** s)
    assert alpha > 0
    assert beta > 0
    return complete_inverse_mean + alpha * row_defect + beta * transport_defect


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
    psi_vector = [psi[C.bit_count()] for C, _ in marked]
    twice = apply_kernel(kernel, apply_kernel(kernel, psi_vector))
    two_step_psi = sum(twice, F(0)) / len(marked)
    assert two_step_psi == two_step_psi_formula(P)

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
        "two_step_psi": two_step_psi,
        "handoff": handoff,
    }


def audit_two_step_sos():
    """Independently compare the closed formula with marked enumeration."""
    raw_kernels = [
        ((0, 1, 3), (2, 0, 1), (4, 1, 0)),
        ((0, 1, 2, 5), (3, 0, 7, 1), (4, 2, 0, 9), (1, 8, 3, 0)),
        (
            (0, 1, 2, 3, 5),
            (7, 0, 1, 4, 2),
            (3, 8, 0, 1, 6),
            (2, 5, 9, 0, 1),
            (4, 1, 3, 7, 0),
        ),
    ]
    for raw in raw_kernels:
        P = [
            [F(value, sum(row)) for value in row]
            for row in raw
        ]
        marked, _, kernel = marked_kernel(P)
        parity = [(-1) ** C.bit_count() for C, _ in marked]
        assert apply_kernel(kernel, parity) == [F(0) for _ in marked]
        for t in (F(0), F(1, 5), F(2, 3), F(1)):
            assert two_step_gap(P, t) == two_step_formula(P, t)
            assert two_step_formula(P, t) >= 0

    print("PASS: exact universal two-step sum-of-squares identity")


def audit_density_factorization():
    """Check the active Perron density equations independently on P3."""
    weights = [[0, 1, 0], [1, 0, 1], [0, 1, 0]]
    P, _, _, nu, _, lam, mean = posterior_midpoint(weights)
    n = len(P)
    N = n - 1
    marked = [
        (C, v)
        for v in range(n)
        for C in range(1 << n)
        if not ((C >> v) & 1)
    ]
    active = [
        (B, v)
        for v in range(n)
        for B in range(1 << n)
        if B and not ((B >> v) & 1)
    ]
    U = F(1, n * 2 ** N)

    def nu_complete(B):
        return F(B.bit_count(), n * N * 2 ** (N - 1))

    h = {(C, v): lam[v][C] / mean / U for C, v in marked}
    g = {
        (B, v): (nu[v][B] / mean) / nu_complete(B)
        for B, v in active
    }

    def reverse_density(values):
        output = {}
        for C, v in marked:
            k = C.bit_count()
            value = F(0)
            if k:
                value += F(k, N) * values[C, v]
            value += sum(
                (values[C | (1 << v), u] / N
                 for u in range(n)
                 if u != v and not ((C >> u) & 1)),
                F(0),
            )
            output[C, v] = value
        return output

    def sample_density(values):
        output = {}
        for B, v in active:
            b = B.bit_count()
            value = sum(
                (P[v][i] * values[B & ~(1 << i), v]
                 for i in range(n) if (B >> i) & 1),
                F(0),
            )
            value += sum(
                (P[v][i] for i in range(n) if (B >> i) & 1), F(0)
            ) * values[B, v]
            output[B, v] = F(N, 2 * b) * value
        return output

    assert reverse_density(g) == h
    assert sample_density(h) == g
    assert sum((B.bit_count() * value for (B, _), value in g.items()), F(0)) \
        == n * N * 2 ** (N - 1)
    assert sum(g.values(), F(0)) / (n * N * 2 ** (N - 1)) == 1 / mean

    ones = {state: F(1) for state in active}
    first = sample_density(reverse_density(ones))
    for B, v in active:
        row_mass = sum(
            (P[v][i] for i in range(n) if (B >> i) & 1), F(0)
        )
        assert first[B, v] == F(N, B.bit_count()) * row_mass
    second = sample_density(reverse_density(first))
    transient = sum(second.values(), F(0)) / (n * N * 2 ** (N - 1))
    assert transient == marked_data(weights)["two_step_psi"]
    assert sum(g.values(), F(0)) > sum(second.values(), F(0))

    # Independently build the forward active chain and verify the exact rank
    # flux, R psi=1/|B|, and the two-step/long-run formulations.
    active_forward, _, forward = active_kernel(P)
    assert active_forward == active
    stationary = [nu[v][B] / mean for B, v in active]
    assert propagate_law(stationary, forward) == stationary
    for row, (B, v) in zip(forward, active):
        b = B.bit_count()
        up = sum(
            (probability for probability, (D, _) in zip(row, active)
             if D.bit_count() == b + 1),
            F(0),
        )
        down = sum(
            (probability for probability, (D, _) in zip(row, active)
             if D.bit_count() == b - 1),
            F(0),
        )
        p_vB = sum((P[v][i] for i in range(n) if (B >> i) & 1), F(0))
        internal = sum(
            (P[w][i]
             for w in range(n) if (B >> w) & 1
             for i in range(n) if (B >> i) & 1),
            F(0),
        )
        assert up == (1 - p_vB) / 2
        assert down == internal / (2 * b)

    psi_rank = marked_data(weights)["psi"]
    for B, _ in active:
        b = B.bit_count()
        assert (psi_rank[b] + psi_rank[b - 1]) / 2 == F(1, b)
    H = [F(1, B.bit_count()) for B, _ in active]
    reference = [
        F(B.bit_count(), n * (n - 1) * 2 ** (n - 2))
        for B, _ in active
    ]
    assert sum(reference, F(0)) == 1
    law = propagate_law(propagate_law(reference, forward), forward)
    assert sum((mass * value for mass, value in zip(law, H)), F(0)) == transient
    assert sum((mass * value for mass, value in zip(stationary, H)), F(0)) == 1 / mean

    print("PASS: exact Perron/forward-active factorization and strict P3 promotion")


def audit_complete_and_path():
    path = [[0, 1, 0], [1, 0, 1], [0, 1, 0]]
    data = marked_data(path)
    assert data["mean"] == F(11, 9)
    assert data["q"][1:3] == [F(7, 11), F(4, 11)]
    assert data["eta"] == [F(7, 22), F(1, 2), F(2, 11)]
    assert 1 / data["mean"] > data["two_step_psi"]

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
        assert 1 / complete_data["mean"] == complete_data["two_step_psi"]

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
    assert 1 / data["mean"] > data["two_step_psi"]

    print(
        "PASS: exact n=6 event-rank tail counterexample; "
        f"tail excess ~{float(tail_excess):.12g}"
    )
    print(
        "PASS: same graph remains below baseline; "
        f"harmonic excess ~{float(harmonic_excess):.12g}"
    )


def audit_lower_envelope_obstructions():
    """Certify failures of stronger semigroup claims, not of promotion."""
    # This rational reversible K5 has a strict late decrease in U M^t psi.
    temporal = matrix_from_edges(
        5,
        (1, 20000, 1, 15000, 660, 164, 1280000, 1000000, 3150, 293),
    )
    P, _, _, _, _, lam, mean = posterior_midpoint(temporal)
    marked, _, kernel = marked_kernel(P)
    N = 4
    psi = [
        2 * sum(
            (F((-1) ** (ell - 1 - C.bit_count()), ell)
             for ell in range(C.bit_count() + 1, N + 1)),
            F(0),
        )
        for C, _ in marked
    ]
    values = psi
    sequence = [sum(values, F(0)) / len(marked)]
    for _ in range(37):
        values = apply_kernel(kernel, values)
        sequence.append(sum(values, F(0)) / len(marked))
    assert sequence[37] < sequence[36]
    stationary_psi = sum(
        (lam[v][C] * value / mean
         for (C, v), value in zip(marked, psi)),
        F(0),
    )
    assert stationary_psi > sequence[2]

    # A different rational reversible K5 shows that the stationary lower
    # envelope is special to psi: it is false for the radial PGF at t=0.
    pgf = matrix_from_edges(
        5,
        (12, 3150, 1850000, 812000, 1810000,
         4180, 295000, 4, 159000, 1),
    )
    P, _, _, _, _, lam, mean = posterior_midpoint(pgf)
    marked, _, kernel = marked_kernel(P)
    zero_rank = [F(C == 0) for C, _ in marked]
    twice = apply_kernel(kernel, apply_kernel(kernel, zero_rank))
    transient = sum(twice, F(0)) / len(marked)
    stationary = sum(
        (lam[v][C] * value / mean
         for (C, v), value in zip(marked, zero_rank)),
        F(0),
    )
    assert stationary < transient

    print("PASS: exact late-time decrease; psi lower envelope still survives")
    print("PASS: exact stationary PGF lower-envelope counterexample at t=0")


def main():
    audit_two_step_sos()
    audit_density_factorization()
    audit_complete_and_path()
    audit_tail_counterexample()
    audit_lower_envelope_obstructions()
    print("OPEN: universal marked collision inequality, equivalently dB r=2 maximality")


if __name__ == "__main__":
    main()
