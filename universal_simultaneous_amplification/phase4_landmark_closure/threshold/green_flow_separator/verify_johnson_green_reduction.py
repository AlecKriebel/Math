#!/usr/bin/env python3
"""Exact Johnson--Green reduction of the balanced endpoint obstruction.

This verifier starts from the exact Green occupations and geometry in
``endpoint_hostile_exact/verify_balanced_poisson.py``.  At each rank it
checks that the two signed geometry fields have zero counting mean, solves
their Johnson-graph Poisson equations in closed form, and verifies that

    T + C = sum_k E_J(z_B, psi_B) + E_J(z_D, psi_D).

Consequently the balanced separator is equivalent to bounding this joint
within-rank Dirichlet pairing by the exact dB tangent dispersion E.  The
identity is algebraic and uses no sampled fitness values.
"""

from __future__ import annotations

import argparse
import itertools
import pathlib
import sys

import sympy as sp


HERE = pathlib.Path(__file__).resolve().parent
ENDPOINT = HERE.parent / "endpoint_hostile_exact"
sys.path.insert(0, str(ENDPOINT))

from verify_balanced_poisson import Q, analyze, green_occupation, state_geometry
from verify_endpoint_candidates import hostile_corpus


def johnson_neighbors(state: int, n: int):
    """Yield each same-rank neighbor obtained by one occupied/unoccupied swap."""
    inside = [i for i in range(n) if state & (1 << i)]
    outside = [j for j in range(n) if not state & (1 << j)]
    for i in inside:
        for j in outside:
            yield state ^ (1 << i) ^ (1 << j)


def temperature_geometry(weights, state: int):
    n = len(weights)
    degree = tuple(sum(row, sp.Integer(0)) for row in weights)
    temperature = tuple(
        sum(weights[i][j] / degree[i] for i in range(n)) for j in range(n)
    )
    centered_temperature = tuple(1 - value for value in temperature)
    cut_imbalance = sum(
        centered_temperature[i] for i in range(n) if state & (1 << i)
    )
    a_cut, b_cut, b_complete, c_r, c_m, dispersion, _ = state_geometry(
        weights, state
    )
    assert sp.cancel(cut_imbalance - (a_cut - b_cut)) == 0
    return (
        cut_imbalance,
        sp.cancel(b_cut - b_complete),
        c_r,
        c_m,
        dispersion,
    )


def johnson_laplacian(values, state: int, n: int):
    return sp.cancel(
        sum(values[state] - values[target] for target in johnson_neighbors(state, n))
    )


def rank_fields(weights, k: int):
    """Return centered fields and their closed-form Johnson potentials."""
    n = len(weights)
    states = tuple(
        state for state in range(1, (1 << n) - 1) if state.bit_count() == k
    )
    c = {}
    b = {}
    e = {}
    c_m = None
    c_r = None
    for state in states:
        c[state], b[state], c_r_state, c_m_state, e[state] = (
            temperature_geometry(weights, state)
        )
        if c_m is None:
            c_m, c_r = c_m_state, c_r_state
        assert c_m == c_m_state and c_r == c_r_state

    # Both fields are exactly centered under counting measure on a rank.
    assert sum(c.values(), sp.Integer(0)) == 0
    assert sum(b.values(), sp.Integer(0)) == 0

    # The Johnson Laplacian J=sum_{i in S,j notin S}(f(S)-f(S-i+j))
    # obeys J c=n c and
    # J b=2(n-1)b+(n-k-1)c.  Hence the displayed potential is J^{-1}b.
    potential_c = {state: sp.cancel(c[state] / n) for state in states}
    potential_b = {
        state: sp.cancel(
            b[state] / (2 * (n - 1))
            - sp.Rational(n - k - 1, 2 * n * (n - 1)) * c[state]
        )
        for state in states
    }
    for state in states:
        assert sp.cancel(johnson_laplacian(c, state, n) - n * c[state]) == 0
        assert sp.cancel(
            johnson_laplacian(b, state, n)
            - 2 * (n - 1) * b[state]
            - (n - k - 1) * c[state]
        ) == 0
        assert sp.cancel(johnson_laplacian(potential_c, state, n) - c[state]) == 0
        assert sp.cancel(johnson_laplacian(potential_b, state, n) - b[state]) == 0
    return states, c, b, e, c_r, c_m, potential_c, potential_b


def dirichlet_pairing(left, right, states, n: int):
    """Counting-measure Johnson pairing, with every edge counted once."""
    answer = sp.Integer(0)
    for state in states:
        for target in johnson_neighbors(state, n):
            if state < target:
                answer += (left[state] - left[target]) * (
                    right[state] - right[target]
                )
    return sp.cancel(answer)


def verify_graph(weights):
    n = len(weights)
    full = (1 << n) - 1
    z_b_tuple = green_occupation(weights, "Bd")
    z_d_tuple = green_occupation(weights, "dB")
    z_b = {state: z_b_tuple[state - 1] for state in range(1, full)}
    z_d = {state: z_d_tuple[state - 1] for state in range(1, full)}

    direct_t = sp.Integer(0)
    direct_c = sp.Integer(0)
    direct_e = sp.Integer(0)
    johnson_b = sp.Integer(0)
    johnson_d = sp.Integer(0)
    rank_records = {}

    for k in range(1, n):
        (
            states,
            c,
            b,
            e,
            _c_r,
            c_m,
            potential_c,
            potential_b,
        ) = rank_fields(weights, k)
        scale = Q ** (k - 1)
        delta = sp.cancel(c_m - _c_r)

        psi_b = {
            state: sp.cancel(scale * potential_c[state]) for state in states
        }
        # The dB signed field in T+C is
        # -q^(k-1)/(n-1) * {C_M c + (C_M-C_R)b}.
        psi_d = {
            state: sp.cancel(
                -scale
                / (n - 1)
                * (c_m * potential_c[state] + delta * potential_b[state])
            )
            for state in states
        }

        direct_t_rank = sum(
            scale
            * (z_b[state] - c_m * z_d[state] / (n - 1))
            * c[state]
            for state in states
        )
        direct_c_rank = sum(
            -scale * z_d[state] * delta * b[state] / (n - 1)
            for state in states
        )
        direct_e_rank = sum(
            scale * z_d[state] * e[state] / (n - 1) for state in states
        )
        pairing_b = dirichlet_pairing(z_b, psi_b, states, n)
        pairing_d = dirichlet_pairing(z_d, psi_d, states, n)
        assert sp.cancel(pairing_b + pairing_d - direct_t_rank - direct_c_rank) == 0

        direct_t += direct_t_rank
        direct_c += direct_c_rank
        direct_e += direct_e_rank
        johnson_b += pairing_b
        johnson_d += pairing_d
        rank_records[k] = (
            sp.cancel(pairing_b),
            sp.cancel(pairing_d),
            sp.cancel(direct_e_rank),
        )

    direct = analyze(weights)
    assert sp.cancel(direct_t - direct["mismatch"]) == 0
    assert sp.cancel(direct_c - direct["cut"]) == 0
    assert sp.cancel(direct_e + direct["dispersion"]) == 0
    assert sp.cancel(johnson_b + johnson_d - direct_t - direct_c) == 0
    assert sp.cancel(
        johnson_b + johnson_d - direct_e - direct["total"]
    ) == 0
    return {
        "pairing_bd": sp.cancel(johnson_b),
        "pairing_db": sp.cancel(johnson_d),
        "dispersion": sp.cancel(direct_e),
        "slack_signed": sp.cancel(direct["total"]),
        "ranks": rank_records,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--all", action="store_true")
    args = parser.parse_args()
    selected = tuple(hostile_corpus())
    if not args.all:
        wanted = {
            "weighted-star",
            "rationalized-nearest-five-edge",
            "exact-dB-amplifying-windmill",
        }
        selected = tuple(item for item in selected if item[0] in wanted)

    for label, weights in selected:
        result = verify_graph(weights)
        print(
            f"PASS {label}: J_B~{sp.N(result['pairing_bd'], 10)}, "
            f"J_D~{sp.N(result['pairing_db'], 10)}, "
            f"E~{sp.N(result['dispersion'], 10)}, "
            f"J_B+J_D-E~{sp.N(result['slack_signed'], 10)}",
            flush=True,
        )
    print(
        "PASS: exact centered Johnson--Green identity and closed-form "
        "rank Poisson potentials"
    )


if __name__ == "__main__":
    main()
