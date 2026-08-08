#!/usr/bin/env python3
"""Exact refutation of the proposed Bd--dB rare-branching sum bound.

For m>=1, G_m is the unweighted graph obtained from a clique on 3m+1
vertices by attaching m pendant leaves to one distinguished clique vertex.
The three automorphism classes are hub, leaves, and ordinary clique
vertices.  This verifier derives their rare-mutant branching maps directly
from the update rules.

At m=25 it checks exact positive rational subsolutions for both branching
maps.  Monotone iteration from a subsolution lies below the maximal fixed
point, i.e. the survival vector.  Their uniform weighted mean already
exceeds the conjectured complete-graph sum by 4207/303000.

It also checks the algebraic limit of the full family.  The limiting excess
is (sqrt(85)-8)/36>0.  No floating-point number is used for a sign claim.
"""

from __future__ import annotations

from fractions import Fraction

import sympy as sp


Q = Fraction
R = Q(3, 2)
P = Q(1, 3)


def h(value: Q) -> Q:
    """The r=3/2 rare-dB birth rate h(z)=rz/(1+(r-1)z)."""
    return R * value / (1 + (R - 1) * value)


def graph_data(m: int):
    """Build the full unweighted graph and verify the three-class quotient."""
    n = 4 * m + 1
    hub = 0
    leaves = tuple(range(1, m + 1))
    core = tuple(range(m + 1, n))
    adjacency = [[0 for _ in range(n)] for _ in range(n)]

    # Clique on {hub} union core.
    clique = (hub,) + core
    for left_index, left in enumerate(clique):
        for right in clique[left_index + 1 :]:
            adjacency[left][right] = adjacency[right][left] = 1
    # Pendant leaves at the distinguished hub.
    for leaf in leaves:
        adjacency[hub][leaf] = adjacency[leaf][hub] = 1

    degree = tuple(sum(row) for row in adjacency)
    assert degree[hub] == 4 * m
    assert all(degree[leaf] == 1 for leaf in leaves)
    assert all(degree[vertex] == 3 * m for vertex in core)

    reached = {hub}
    frontier = [hub]
    while frontier:
        vertex = frontier.pop()
        for neighbor, edge in enumerate(adjacency[vertex]):
            if edge and neighbor not in reached:
                reached.add(neighbor)
                frontier.append(neighbor)
    assert len(reached) == n

    transition = [
        [Q(adjacency[i][j], degree[i]) for j in range(n)] for i in range(n)
    ]
    assert all(sum(row, Q(0)) == 1 for row in transition)
    # Reversibility with degree measure, checked on every ordered pair.
    for i in range(n):
        for j in range(n):
            assert degree[i] * transition[i][j] == degree[j] * transition[j][i]

    temperature = tuple(
        sum((transition[parent][target] for parent in range(n)), Q(0))
        for target in range(n)
    )
    expected_temperature = (
        Q(m + 1),
        Q(1, 4 * m),
        Q(1, 4 * m) + Q(3 * m - 1, 3 * m),
    )
    assert temperature[hub] == expected_temperature[0]
    assert all(temperature[leaf] == expected_temperature[1] for leaf in leaves)
    assert all(temperature[vertex] == expected_temperature[2] for vertex in core)

    # Total P-mass from a representative parent class to each child class.
    p_class = (
        (Q(0), Q(1, 4), Q(3, 4)),
        (Q(1), Q(0), Q(0)),
        (Q(1, 3 * m), Q(0), Q(3 * m - 1, 3 * m)),
    )
    representatives = (hub, leaves[0], core[0])
    classes = ((hub,), leaves, core)
    for row, representative in enumerate(representatives):
        for column, vertices in enumerate(classes):
            assert (
                sum((transition[representative][v] for v in vertices), Q(0))
                == p_class[row][column]
            )

    expected_db_birth = (
        (Q(0), Q(m), Q(3 * m) * h(Q(1, 3 * m))),
        (h(Q(1, 4 * m)), Q(0), Q(0)),
        (
            h(Q(1, 4 * m)),
            Q(0),
            Q(3 * m - 1) * h(Q(1, 3 * m)),
        ),
    )
    for row, representative in enumerate(representatives):
        for column, targets in enumerate(classes):
            direct_rate = sum(
                (h(transition[target][representative]) for target in targets),
                Q(0),
            )
            assert direct_rate == expected_db_birth[row][column]

    return n, expected_temperature, p_class


def branching_maps(m: int):
    """Return the exact three-type Bd and dB survival maps."""
    _n, temperature, p_class = graph_data(m)

    # Bd: each particle of type i dies at its temperature t_i and gives
    # birth into class j at total rate r P(i,class j).
    bd_birth = tuple(
        tuple(R * entry for entry in row) for row in p_class
    )

    # dB: a mutant parent i produces into target v at rare rate h(P_vi).
    # Counts of equivalent targets yield the following three-type matrix.
    h_hub_to_target = h(Q(1, 4 * m))
    h_core_to_hub = h(Q(1, 3 * m))
    db_birth = (
        (Q(0), Q(m), Q(3 * m) * h_core_to_hub),
        (h_hub_to_target, Q(0), Q(0)),
        (
            h_hub_to_target,
            Q(0),
            Q(3 * m - 1) * h_core_to_hub,
        ),
    )
    return bd_birth, temperature, db_birth, (Q(1), Q(1), Q(1))


def survival_map(vector, birth, death):
    """One step z -> Bz/(death+Bz) of the binary branching fixed map."""
    answer = []
    for row in range(3):
        birth_mass = sum(
            (birth[row][column] * vector[column] for column in range(3)),
            Q(0),
        )
        answer.append(birth_mass / (death[row] + birth_mass))
    return tuple(answer)


def verify_finite_counterexample():
    m = 25
    n = 4 * m + 1
    bd_birth, bd_death, db_birth, db_death = branching_maps(m)

    # All coordinates are deliberately rounded down from discovery values,
    # then checked as subsolutions using exact rational arithmetic.
    lower_bd = (Q(3, 125), Q(39, 50), Q(8, 25))
    lower_db = (Q(3, 8), Q(1, 200), Q(13, 40))
    image_bd = survival_map(lower_bd, bd_birth, bd_death)
    image_db = survival_map(lower_db, db_birth, db_death)
    residual_bd = tuple(image_bd[i] - lower_bd[i] for i in range(3))
    residual_db = tuple(image_db[i] - lower_db[i] for i in range(3))

    expected_bd = (
        Q(642, 1_332_625),
        Q(3, 1_150),
        Q(3_226, 1_378_825),
    )
    expected_db = (
        Q(7, 1_944),
        Q(61, 107_800),
        Q(21_089, 24_012_280),
    )
    assert residual_bd == expected_bd
    assert residual_db == expected_db
    assert all(value > 0 for value in residual_bd + residual_db)

    lower_mean = (
        lower_bd[0]
        + m * lower_bd[1]
        + 3 * m * lower_bd[2]
        + lower_db[0]
        + m * lower_db[1]
        + 3 * m * lower_db[2]
    ) / n
    conjectured_bound = P + P * Q(n - 2, n - 1)
    exact_excess = lower_mean - conjectured_bound
    assert lower_mean == Q(68_399, 101_000)
    assert conjectured_bound == Q(199, 300)
    assert exact_excess == Q(4_207, 303_000) > 0

    print(f"PASS G_25 has n={n}, is connected, unweighted, and reversible")
    print(f"PASS Bd strict rational subsolution residuals: {residual_bd}")
    print(f"PASS dB strict rational subsolution residuals: {residual_db}")
    print(
        "PASS exact survival-sum lower excess over conjectured bound: "
        f"{exact_excess}"
    )


def verify_asymptotic_counterexample():
    # The limiting pendant-leaf Bd survival is the positive root of
    #     ell/(1-ell) = (9/4)(ell+1),
    # equivalently 9 ell^2+4 ell-9=0.
    ell = (sp.sqrt(85) - 2) / 9
    assert sp.simplify(9 * ell**2 + 4 * ell - 9) == 0
    assert 0 < ell < 1

    limiting_sum = sp.simplify(ell / 4 + sp.Rational(1, 2))
    limiting_bound = sp.Rational(2, 3)
    limiting_excess = sp.simplify(limiting_sum - limiting_bound)
    assert limiting_sum == (sp.sqrt(85) + 16) / 36
    assert limiting_excess == (sp.sqrt(85) - 8) / 36
    # Exact positivity certificate: 85>8^2.
    assert 85 > 8**2

    print(f"PASS limiting branching sum: {limiting_sum}")
    print(f"PASS persistent exact limiting excess: {limiting_excess} > 0")

    # General pendant proportion alpha.  The sign on 0<alpha<3/5 follows
    # without numerical root evaluation by squaring two positive sides.
    alpha = sp.symbols("alpha", positive=True)
    discriminant = 9 + 60 * alpha - 44 * alpha**2
    ell_alpha = (
        8 * alpha - 3 + sp.sqrt(discriminant)
    ) / (18 * alpha)
    assert sp.simplify(
        9 * alpha * ell_alpha**2
        + (3 - 8 * alpha) * ell_alpha
        - 3 * (1 - alpha)
    ) == 0
    general_excess = sp.simplify(alpha * (ell_alpha - sp.Rational(2, 3)))
    assert general_excess == (
        sp.sqrt(discriminant) - 3 - 4 * alpha
    ) / 18
    assert sp.simplify(
        discriminant
        - (3 + 4 * alpha) ** 2
        - 12 * alpha * (3 - 5 * alpha)
    ) == 0
    print("PASS general limiting violation for every 0<alpha<3/5")


def main():
    verify_finite_counterexample()
    verify_asymptotic_counterexample()
    print("PASS: proposed reversible rare-branching sum inequality is false")


if __name__ == "__main__":
    main()
