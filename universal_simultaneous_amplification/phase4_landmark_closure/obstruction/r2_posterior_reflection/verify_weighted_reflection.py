#!/usr/bin/env python3
"""Exact audit of the rank-weighted posterior-reflection reduction.

The universal weighted stationary inequality isolated in the accompanying
note remains open.  This verifier checks every identity over ``Fraction``,
certifies the exact counterexamples to the tempting separated signs, and
replays the deterministic hostile corpus.
"""

from __future__ import annotations

import sys
from fractions import Fraction as F
from pathlib import Path


HERE = Path(__file__).resolve().parent
OBSTRUCTION = HERE.parent
CHI_DIR = OBSTRUCTION / "r2_entropy_certificate" / "chi_square_channel"
COLLISION_DIR = OBSTRUCTION / "r2_collision_closure"
sys.path.insert(0, str(CHI_DIR))
sys.path.insert(0, str(COLLISION_DIR))

from verify_resolvent_identities import solve  # noqa: E402
from verify_direct_flow_screen import (  # noqa: E402
    connected,
    deterministic_graphs,
    exhaustive_graphs,
    matrix_from_edges,
)


def sharp_coefficient(n: int, k: int) -> F:
    """Sharp constant c_{n,k} in J <= n*c*G."""

    holes = n - k
    if holes == 1:
        return F(0)
    if k <= holes - 2:
        return F(k + 1, holes)
    return F(n * n, 4 * holes * (holes - 1))


def posterior_data(weights):
    P, states, _, kernels, pi = solve(weights)
    n = len(P)
    full = 1 << n
    pi_all = [F(0) for _ in range(full)]
    for state, probability in zip(states, pi):
        pi_all[state] = probability

    mu = [[F(0) for _ in range(full)] for _ in range(n)]
    nu = [[F(0) for _ in range(full)] for _ in range(n)]
    sigma = [[F(0) for _ in range(full)] for _ in range(n)]
    for v in range(n):
        for target, state in enumerate(states):
            mu[v][state] = sum(
                (pi[source] * kernels[v][source][target]
                 for source in range(len(states))),
                F(0),
            )
            if not ((state >> v) & 1):
                nu[v][state] = mu[v][state] - pi_all[state]
                assert nu[v][state] >= 0
        for state in range(full):
            if not ((state >> v) & 1):
                sigma[v][state] = pi_all[state | (1 << v)]

    lam = [
        [(sigma[v][state] + nu[v][state]) / 2 for state in range(full)]
        for v in range(n)
    ]

    def add_sample(v, measure):
        image = [F(0) for _ in range(full)]
        for state, mass in enumerate(measure):
            if not mass:
                continue
            for i in range(n):
                image[state | (1 << i)] += mass * P[v][i]
        return image

    for v in range(n):
        assert add_sample(v, lam[v]) == nu[v]

    mean = F(0)
    collision = F(0)
    harmonic = F(0)
    weighted_harmonic = F(0)
    rank_collision = [F(0) for _ in range(n)]
    rank_harmonic = [F(0) for _ in range(n)]
    variational = F(0)
    for position, state in enumerate(states):
        probability = pi[position]
        k = state.bit_count()
        holes = n - k
        e = [
            nu[v][state] / probability
            for v in range(n)
            if not ((state >> v) & 1)
        ]
        assert len(e) == holes
        assert sum(e, F(0)) == k

        x = [1 + value for value in e]
        assert sum(x, F(0)) == n
        j_state = sum((value * value for value in e), F(0)) - F(k * k, holes)
        g_state = sum((1 / value for value in x), F(0)) - F(holes * holes, n)
        assert j_state >= 0 and g_state >= 0

        # Two exact arithmetic--harmonic forms for G.
        centered = [value - F(n, holes) for value in x]
        assert g_state == F(holes * holes, n * n) * sum(
            (value * value / x_i for value, x_i in zip(centered, x)),
            F(0),
        )
        pair_square = sum(
            ((x[i] - x[j]) ** 2 for i in range(holes) for j in range(i + 1, holes)),
            F(0),
        )
        pair_harmonic = sum(
            (
                (x[i] - x[j]) ** 2 / (x[i] * x[j])
                for i in range(holes)
                for j in range(i + 1, holes)
            ),
            F(0),
        )
        assert j_state == pair_square / holes
        assert n * g_state == pair_harmonic

        coefficient = sharp_coefficient(n, k)
        assert j_state <= n * coefficient * g_state

        # The optimizer in the Hilbert variational formula is a_v=e_v-k/h.
        a = [value - F(k, holes) for value in e]
        assert sum(a, F(0)) == 0
        linear = sum((nu[v][state] * a_i for v, a_i in zip(
            (v for v in range(n) if not ((state >> v) & 1)), a
        )), F(0))
        quadratic = probability * sum((value * value for value in a), F(0))
        variational += 2 * linear - quadratic

        mean += probability * k
        collision += probability * j_state
        harmonic += probability * g_state
        weighted_harmonic += probability * coefficient * g_state
        rank_collision[k] += probability * j_state
        rank_harmonic[k] += probability * g_state

    assert variational == collision
    complete_mean = F((n - 1) * 2 ** (n - 2), 2 ** (n - 1) - 1)
    return {
        "n": n,
        "states": states,
        "pi": pi_all,
        "nu": nu,
        "sigma": sigma,
        "lambda": lam,
        "mean": mean,
        "complete_mean": complete_mean,
        "collision": collision,
        "harmonic": harmonic,
        "weighted_harmonic": weighted_harmonic,
        "rank_collision": rank_collision,
        "rank_harmonic": rank_harmonic,
        "target_slack": n * (complete_mean - mean) - collision,
        "weighted_slack": complete_mean - mean - weighted_harmonic,
    }


def conditional_centered_collision(family) -> F:
    n = len(family)
    full = len(family[0])
    answer = F(0)
    for state in range(full):
        holes = [v for v in range(n) if not ((state >> v) & 1)]
        total = sum((family[v][state] for v in holes), F(0))
        if total:
            answer += len(holes) * sum(
                (family[v][state] ** 2 for v in holes), F(0)
            ) / total - total
    return answer


def fixed_pi_centered_collision(data, family):
    n = data["n"]
    finite = F(0)
    zero_reference_mass = F(0)
    for state in range(1 << n):
        holes = [v for v in range(n) if not ((state >> v) & 1)]
        total = sum((family[v][state] for v in holes), F(0))
        deviations = sum(
            ((family[v][state] - total / len(holes)) ** 2 for v in holes),
            F(0),
        )
        if data["pi"][state]:
            finite += deviations / data["pi"][state]
        else:
            zero_reference_mass += deviations
    return finite, zero_reference_mass


def active_variance_decomposition(data):
    """Return the two exact brackets in the transported Brier identity."""

    n = data["n"]
    source_overlap = F(0)
    output_overlap = F(0)
    input_gain = F(0)
    for state in data["states"]:
        probability = data["pi"][state]
        k = state.bit_count()
        holes = n - k
        coefficient = sharp_coefficient(n, k)
        input_gain += probability * coefficient * F(k * holes, n)
        for v in range(n):
            if (state >> v) & 1:
                continue
            r_mass = probability
            source = data["sigma"][v][state]
            output = data["nu"][v][state]
            if r_mass + source:
                source_overlap += coefficient * r_mass * source / (r_mass + source)
            if r_mass + output:
                output_overlap += coefficient * r_mass * output / (r_mass + output)
    static = data["complete_mean"] - data["mean"] - input_gain + source_overlap
    active = output_overlap - source_overlap
    assert static + active == data["weighted_slack"]
    return {
        "input_gain": input_gain,
        "source_overlap": source_overlap,
        "output_overlap": output_overlap,
        "static": static,
        "active": active,
    }


def audit_sharp_extremizers() -> None:
    # Low-density extremizer: x=(k+1,1,...,1).
    for n, k in ((5, 1), (7, 2), (10, 3)):
        holes = n - k
        x = [F(k + 1)] + [F(1)] * (holes - 1)
        j = sum((value * value for value in x), F(0)) - F(n * n, holes)
        g = sum((1 / value for value in x), F(0)) - F(holes * holes, n)
        assert j == n * sharp_coefficient(n, k) * g

    # High-density extremizer: one n/2 entry and h-1 equal entries.
    for n, k in ((5, 2), (8, 4), (10, 7)):
        holes = n - k
        x = [F(n, 2)] + [F(n, 2 * (holes - 1))] * (holes - 1)
        assert all(value >= 1 for value in x)
        j = sum((value * value for value in x), F(0)) - F(n * n, holes)
        g = sum((1 / value for value in x), F(0)) - F(holes * holes, n)
        assert j == n * sharp_coefficient(n, k) * g

    print("PASS: both exact sharp arithmetic--harmonic extremizer families")


def audit_contraction_and_split_counterexamples() -> None:
    path = [[0, 1, 0], [1, 0, 1], [0, 1, 0]]
    path_data = posterior_data(path)
    path_active = active_variance_decomposition(path_data)
    assert conditional_centered_collision(path_data["nu"]) == F(1, 3)
    assert conditional_centered_collision(path_data["lambda"]) == F(103, 756)
    raw_nu, raw_nu_zero = fixed_pi_centered_collision(path_data, path_data["nu"])
    raw_lam, raw_lam_zero = fixed_pi_centered_collision(path_data, path_data["lambda"])
    assert (raw_nu, raw_nu_zero) == (F(1, 6), F(0))
    assert (raw_lam, raw_lam_zero) == (F(1, 54), F(25, 1944))
    assert path_active["static"] == -F(169, 1440)
    assert path_active["active"] == F(239, 1440)
    assert path_data["weighted_slack"] == F(7, 144)

    regular_k4 = [
        [0, 1, 1, 2],
        [1, 0, 2, 1],
        [1, 2, 0, 1],
        [2, 1, 1, 0],
    ]
    k4_data = posterior_data(regular_k4)
    k4_active = active_variance_decomposition(k4_data)
    assert conditional_centered_collision(k4_data["nu"]) == F(64, 1435)
    assert conditional_centered_collision(k4_data["lambda"]) == F(8, 4387)
    assert fixed_pi_centered_collision(k4_data, k4_data["nu"]) == (F(64, 4305), F(0))
    assert fixed_pi_centered_collision(k4_data, k4_data["lambda"]) == (F(4, 4305), F(0))
    assert k4_active["static"] == -F(50249, 253708)
    assert k4_active["active"] == F(240463, 1196052)
    assert k4_data["weighted_slack"] == F(368, 123123)

    # J <= nG fails, while the complementary mean-minus-G sign is positive.
    triangle = [[0, 1, 1], [1, 0, 5], [1, 5, 0]]
    triangle_data = posterior_data(triangle)
    assert triangle_data["collision"] == F(3456, 20291)
    assert triangle_data["harmonic"] == F(105472, 1976501)
    assert 3 * triangle_data["harmonic"] - triangle_data["collision"] \
        == -F(2083200, 203579603)
    assert triangle_data["complete_mean"] - triangle_data["mean"] \
        - triangle_data["harmonic"] == F(325696, 5929503)
    assert triangle_data["target_slack"] == F(3136, 20291) > 0
    assert triangle_data["collision"] / (3 * triangle_data["harmonic"]) \
        == F(90297, 84872) > F(6, 7)

    # G <= m_K-m fails, while nG-J compensates exactly.
    k22 = [
        [0, 0, 1, 1],
        [0, 0, 1, 1],
        [1, 1, 0, 0],
        [1, 1, 0, 0],
    ]
    k22_data = posterior_data(k22)
    k22_active = active_variance_decomposition(k22_data)
    assert k22_data["complete_mean"] - k22_data["mean"] == F(4, 133)
    assert k22_data["collision"] == F(4, 57)
    assert k22_data["harmonic"] == F(2, 57)
    assert k22_data["complete_mean"] - k22_data["mean"] \
        - k22_data["harmonic"] == -F(2, 399)
    assert (k22_data["complete_mean"] - k22_data["mean"]) \
        / k22_data["harmonic"] == F(6, 7)
    assert 4 * k22_data["harmonic"] - k22_data["collision"] == F(4, 57)
    assert k22_data["target_slack"] == F(20, 399) > 0
    assert k22_active["static"] == -F(1180, 3591)
    assert k22_active["active"] == F(172, 513)
    assert k22_data["weighted_slack"] == F(8, 1197)

    print("PASS: centered Cayley contraction is exactly false on P3 and weighted K4")
    print("PASS: both separated law-of-total-variance signs are exactly false")


def screen(label, graphs) -> None:
    count = 0
    minimum_target = None
    minimum_weighted = None
    for weights in graphs:
        if not connected(weights):
            continue
        data = posterior_data(weights)
        active = active_variance_decomposition(data)
        assert data["target_slack"] >= 0
        assert data["weighted_slack"] >= 0
        assert active["active"] >= 0
        minimum_target = (
            data["target_slack"]
            if minimum_target is None
            else min(minimum_target, data["target_slack"])
        )
        minimum_weighted = (
            data["weighted_slack"]
            if minimum_weighted is None
            else min(minimum_weighted, data["weighted_slack"])
        )
        count += 1
    assert count and minimum_target is not None and minimum_weighted is not None
    print(
        f"PASS: {label}: {count} exact graphs; "
        f"min target slack {'=0' if minimum_target == 0 else '>0'}; "
        f"min weighted slack {'=0' if minimum_weighted == 0 else '>0'}"
    )


def main() -> None:
    audit_sharp_extremizers()
    audit_contraction_and_split_counterexamples()
    screen("n=3 weights in {0,1,2,5}", exhaustive_graphs(3, (0, 1, 2, 5)))
    screen("n=4 weights in {0,1,2}", exhaustive_graphs(4, (0, 1, 2)))
    screen("n=5 deterministic sparse/extreme", deterministic_graphs(5, 48, 26080805))

    split_witness = matrix_from_edges(
        6,
        (3, 300, 2, 5, 1, 3, 3, 1, 300, 1, 1, 1, 20, 1, 1),
    )
    split_data = posterior_data(split_witness)
    assert split_data["target_slack"] > 0 and split_data["weighted_slack"] > 0
    print("PASS: exact n=6 split witness has both positive slacks")
    print("OPEN: universal rank-weighted stationary harmonic reflection")


if __name__ == "__main__":
    main()
