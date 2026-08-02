#!/usr/bin/env python3
"""Exact verifier for the additive Bd and geometric-OR dB duals.

The script derives both forward generators and both nonempty-set dual
generators directly from the update maps.  It then solves the fixation and
stationary equations over the rationals and checks (57)--(63), together with
the weighted-adjoint and local-resolvent identities (67)--(68).  At r=3/2 it
also subjects the open product conjecture (65) to a deterministic exact
small-graph screen.  Passing that screen is evidence only, not a proof of
(65).
"""

from __future__ import annotations

from itertools import combinations

import sympy as sp


def subsets(mask: int):
    sub = mask
    while True:
        yield sub
        if sub == 0:
            return
        sub = (sub - 1) & mask


def add_rate(generator: sp.MutableDenseMatrix, row: int, column: int, rate):
    if row != column and rate:
        generator[row, column] += rate


def finish_generator(generator: sp.MutableDenseMatrix) -> sp.Matrix:
    for row in range(generator.rows):
        generator[row, row] = -sum(
            generator[row, column]
            for column in range(generator.cols)
            if column != row
        )
    return sp.Matrix(generator)


def forward_generator(weights, fitness, rule: str) -> sp.Matrix:
    order = len(weights)
    state_count = 1 << order
    degree = [sum(map(sp.sympify, row), sp.Integer(0)) for row in weights]
    transition = [
        [sp.sympify(weights[i][j]) / degree[i] for j in range(order)]
        for i in range(order)
    ]
    generator = sp.zeros(state_count, state_count)
    for state in range(state_count):
        mutant = [(state >> i) & 1 for i in range(order)]
        if rule == "Bd":
            # Common-fitness normalization is deleted: this is the exact
            # continuous-time copying-arrow representation.
            for parent in range(order):
                for target in range(order):
                    if not transition[parent][target]:
                        continue
                    rate = transition[parent][target] * (
                        fitness if mutant[parent] else 1
                    )
                    new_state = (
                        state | (1 << target)
                        if mutant[parent]
                        else state & ~(1 << target)
                    )
                    add_rate(generator, state, new_state, rate)
        elif rule == "dB":
            for target in range(order):
                x = sum(
                    transition[target][parent] * mutant[parent]
                    for parent in range(order)
                )
                new_mutant_probability = fitness * x / (
                    1 + (fitness - 1) * x
                )
                if mutant[target]:
                    add_rate(
                        generator,
                        state,
                        state & ~(1 << target),
                        1 - new_mutant_probability,
                    )
                else:
                    add_rate(
                        generator,
                        state,
                        state | (1 << target),
                        new_mutant_probability,
                    )
        else:
            raise ValueError(rule)
    return finish_generator(generator)


def geometric_union_probabilities(row, fitness):
    """Return exact probabilities for the nonempty union of K row samples."""
    support_mask = sum((1 << i) for i, value in enumerate(row) if value)
    pgf = lambda z: z / (fitness - (fitness - 1) * z)
    probabilities = {}
    for target_set in subsets(support_mask):
        if not target_set:
            continue
        probability = 0
        for included in subsets(target_set):
            mass = sum(
                row[i] for i in range(len(row)) if (included >> i) & 1
            )
            sign = (-1) ** (target_set.bit_count() - included.bit_count())
            probability += sign * pgf(mass)
        probabilities[target_set] = sp.cancel(probability)
    assert sp.cancel(sum(probabilities.values()) - 1) == 0
    assert all(probability > 0 for probability in probabilities.values())
    return probabilities


def dual_generator(weights, fitness, rule: str) -> sp.Matrix:
    order = len(weights)
    full = (1 << order) - 1
    states = list(range(1, full + 1))
    index = {state: position for position, state in enumerate(states)}
    degree = [sum(map(sp.sympify, row), sp.Integer(0)) for row in weights]
    transition = [
        [sp.sympify(weights[i][j]) / degree[i] for j in range(order)]
        for i in range(order)
    ]
    generator = sp.zeros(len(states), len(states))
    union_laws = (
        [geometric_union_probabilities(row, fitness) for row in transition]
        if rule == "dB"
        else None
    )
    for state in states:
        row_index = index[state]
        for target in range(order):
            if not ((state >> target) & 1):
                continue
            if rule == "Bd":
                for parent in range(order):
                    # A forward parent->target arrow has rate P_parent,target.
                    rate = transition[parent][target]
                    neutral = (state & ~(1 << target)) | (1 << parent)
                    selective = state | (1 << parent)
                    add_rate(generator, row_index, index[neutral], rate)
                    add_rate(
                        generator,
                        row_index,
                        index[selective],
                        (fitness - 1) * rate,
                    )
            elif rule == "dB":
                without_target = state & ~(1 << target)
                assert union_laws is not None
                for parent_set, probability in union_laws[target].items():
                    new_state = without_target | parent_set
                    add_rate(
                        generator,
                        row_index,
                        index[new_state],
                        probability,
                    )
            else:
                raise ValueError(rule)
    return finish_generator(generator)


def reversed_arrow_generator(weights, fitness) -> sp.Matrix:
    """Bd set generator after reversing every underlying graphical arrow."""
    order = len(weights)
    full = (1 << order) - 1
    degree = [sum(map(sp.sympify, row), sp.Integer(0)) for row in weights]
    transition = [
        [sp.sympify(weights[i][j]) / degree[i] for j in range(order)]
        for i in range(order)
    ]
    generator = sp.zeros(full, full)
    for state in range(1, full + 1):
        for target in range(order):
            if not ((state >> target) & 1):
                continue
            for source in range(order):
                # Reversing original source target -> target source leaves
                # the rate P_target,source and makes the source distribution
                # the row P_target,*.
                rate = transition[target][source]
                neutral = (state & ~(1 << target)) | (1 << source)
                selective = state | (1 << source)
                add_rate(generator, state - 1, neutral - 1, rate)
                add_rate(
                    generator,
                    state - 1,
                    selective - 1,
                    (fitness - 1) * rate,
                )
    return finish_generator(generator)


def local_sample_kernels(weights, fitness, target: int):
    """Return S_v, N_v, and the geometric burst B_v as row kernels."""
    order = len(weights)
    full = (1 << order) - 1
    degree = [sum(map(sp.sympify, row), sp.Integer(0)) for row in weights]
    transition = [
        [sp.sympify(weights[i][j]) / degree[i] for j in range(order)]
        for i in range(order)
    ]
    selective = sp.zeros(full, full)
    neutral = sp.zeros(full, full)
    burst = sp.zeros(full, full)
    union_law = geometric_union_probabilities(transition[target], fitness)
    for state in range(1, full + 1):
        row = state - 1
        if not ((state >> target) & 1):
            selective[row, row] = 1
            neutral[row, row] = 1
            burst[row, row] = 1
            continue
        for source in range(order):
            probability = transition[target][source]
            selective_state = state | (1 << source)
            neutral_state = (state & ~(1 << target)) | (1 << source)
            selective[row, selective_state - 1] += probability
            neutral[row, neutral_state - 1] += probability
        without_target = state & ~(1 << target)
        for source_set, probability in union_law.items():
            burst[row, (without_target | source_set) - 1] += probability
    assert all(sum(selective.row(i)) == 1 for i in range(full))
    assert all(sum(neutral.row(i)) == 1 for i in range(full))
    assert all(sum(burst.row(i)) == 1 for i in range(full))
    return sp.Matrix(selective), sp.Matrix(neutral), sp.Matrix(burst)


def fixation_values(generator: sp.Matrix) -> list[sp.Expr]:
    state_count = generator.rows
    full = state_count - 1
    transient = list(range(1, full))
    matrix = generator.extract(transient, transient)
    rhs = -generator.extract(transient, [full])
    solution = list(matrix.inv() * rhs)
    values = [sp.Integer(0)] + solution + [sp.Integer(1)]
    return [sp.cancel(value) for value in values]


def stationary(generator: sp.Matrix) -> list[sp.Expr]:
    matrix = generator.T.copy()
    rhs = sp.zeros(generator.rows, 1)
    for column in range(generator.cols):
        matrix[-1, column] = 1
    rhs[-1] = 1
    solution = list(matrix.inv() * rhs)
    assert all(value >= 0 for value in solution), solution
    assert any(value > 0 for value in solution)
    return [sp.cancel(value) for value in solution]


def check_graph(weights, fitness):
    order = len(weights)
    full = (1 << order) - 1
    degree = [sum(map(sp.sympify, row), sp.Integer(0)) for row in weights]
    transition = [
        [sp.sympify(weights[i][j]) / degree[i] for j in range(order)]
        for i in range(order)
    ]

    # Weighted adjoint bridge.  Reversing every base arrow gives C, and the
    # off-diagonal transitions of L_Bd and C are paired by the reference
    # weight mu(A)=(r-1)^|A|.  Their exit-rate discrepancy is exactly the
    # cut-imbalance potential r(Acut-Bcut).
    bd_dual = dual_generator(weights, fitness, "Bd")
    reversed_arrows = reversed_arrow_generator(weights, fitness)
    reference = sp.diag(
        *[(fitness - 1) ** state.bit_count() for state in range(1, full + 1)]
    )
    weighted_adjoint = reference.inv() * bd_dual.T * reference
    potential = []
    for state in range(1, full + 1):
        row_cut = sum(
            transition[i][j]
            for i in range(order)
            for j in range(order)
            if (state >> i) & 1 and not ((state >> j) & 1)
        )
        column_cut = sum(
            transition[j][i]
            for i in range(order)
            for j in range(order)
            if (state >> i) & 1 and not ((state >> j) & 1)
        )
        potential.append(fitness * (row_cut - column_cut))
    assert weighted_adjoint == reversed_arrows + sp.diag(*potential)

    # A geometric dB burst at one occupied target is the exact resolvent of
    # the corresponding reversed-arrow local generator.  Matrix rows act on
    # test functions, so selective samples occur before the final neutral
    # sample in S^m N.
    identity = sp.eye(full)
    for target in range(order):
        selective, neutral, burst = local_sample_kernels(
            weights, fitness, target
        )
        local_reversed = (
            neutral - identity + (fitness - 1) * (selective - identity)
        )
        resolvent_identity = (
            identity - (fitness - 1) / fitness * selective
        ) * (burst - identity) - local_reversed / fitness
        assert resolvent_identity == sp.zeros(full, full)

    results = {}
    for rule in ("Bd", "dB"):
        forward = forward_generator(weights, fitness, rule)
        fixation = fixation_values(forward)
        dual = dual_generator(weights, fitness, rule)
        invariant = stationary(dual)

        # Full set duality, not merely the singleton-density consequence.
        for mutant_set in range(1 << order):
            intersection_probability = sum(
                invariant[dual_set - 1]
                for dual_set in range(1, full + 1)
                if dual_set & mutant_set
            )
            difference = sp.cancel(fixation[mutant_set] - intersection_probability)
            assert difference == 0, (rule, mutant_set, difference)

        average_fixation = sum(fixation[1 << i] for i in range(order)) / order
        mean_dual_size = sum(
            invariant[state - 1] * state.bit_count()
            for state in range(1, full + 1)
        )
        assert sp.cancel(average_fixation - mean_dual_size / order) == 0

        # The type-complement argument gives the reverse-fitness singleton
        # identity for both update rules, not only for dB.
        reverse = fixation_values(forward_generator(weights, 1 / fitness, rule))
        for vertex in range(order):
            assert sp.cancel(
                reverse[1 << vertex] - invariant[(1 << vertex) - 1]
            ) == 0

        singleton = [invariant[(1 << i) - 1] for i in range(order)]
        doubleton = {
            (i, j): invariant[((1 << i) | (1 << j)) - 1]
            for i in range(order)
            for j in range(i + 1, order)
        }

        def pair_mass(i, j):
            if i == j:
                return sp.Integer(0)
            return doubleton[min(i, j), max(i, j)]

        if rule == "dB":
            ell = lambda x: x / (fitness - (fitness - 1) * x)
            for i in range(order):
                level_one_balance = singleton[i] - sum(
                    ell(transition[j][i])
                    * (singleton[j] + pair_mass(i, j))
                    for j in range(order)
                )
                assert sp.cancel(level_one_balance) == 0

            h = lambda x: fitness * x / (1 + (fitness - 1) * x)
            stationary_drift = 0
            for state in range(1, full + 1):
                outward = sum(
                    h(transition[v][u])
                    for v in range(order)
                    for u in range(order)
                    if (state >> v) & 1 and not ((state >> u) & 1)
                )
                stationary_drift += invariant[state - 1] * (
                    outward - state.bit_count()
                )
            assert sp.cancel(stationary_drift) == 0

            # Expanding h_r(x)=r x-r(r-1)x^2/(1+(r-1)x) in
            # the size balance gives a useful exact collision identity.
            collision_drift = 0
            p = 1 - 1 / fitness
            for state in range(1, full + 1):
                internal = sum(
                    transition[v][u]
                    for v in range(order)
                    for u in range(order)
                    if (state >> v) & 1 and (state >> u) & 1
                )
                remainder = sum(
                    transition[v][u] ** 2
                    / (1 + (fitness - 1) * transition[v][u])
                    for v in range(order)
                    for u in range(order)
                    if (state >> v) & 1 and not ((state >> u) & 1)
                )
                collision_drift += invariant[state - 1] * (
                    internal + (fitness - 1) * remainder
                    - p * state.bit_count()
                )
            assert sp.cancel(collision_drift) == 0
        else:
            incoming = [
                sum(transition[j][i] for j in range(order))
                for i in range(order)
            ]
            for i in range(order):
                level_one_balance = fitness * incoming[i] * singleton[i] - sum(
                    transition[i][j]
                    * (singleton[j] + pair_mass(i, j))
                    for j in range(order)
                )
                assert sp.cancel(level_one_balance) == 0

            aggregate_balance = (fitness - 1) * sum(
                incoming[i] * singleton[i] for i in range(order)
            ) - sum(
                (transition[i][j] + transition[j][i]) * doubleton[i, j]
                for i in range(order)
                for j in range(i + 1, order)
            )
            assert sp.cancel(aggregate_balance) == 0

            stationary_drift = 0
            for state in range(1, full + 1):
                flow_b = sum(
                    transition[u][v]
                    for v in range(order)
                    for u in range(order)
                    if (state >> v) & 1 and not ((state >> u) & 1)
                )
                internal = sum(
                    transition[u][v]
                    for u in range(order)
                    for v in range(order)
                    if (state >> u) & 1 and (state >> v) & 1
                )
                stationary_drift += invariant[state - 1] * (
                    (fitness - 1) * flow_b - internal
                )
            assert sp.cancel(stationary_drift) == 0


        results[rule] = {
            "rho": sp.cancel(average_fixation),
            "invariant": invariant,
            "singleton_mass": sp.cancel(sum(singleton)),
        }

    # Exact finite screening of the OPEN stationary product inequality (65).
    # This assertion must not be interpreted as a proof beyond the listed
    # graphs.  Returning the exact slack lets the caller record the minimum.
    p = 1 - 1 / fitness
    excess_bd = max(results["Bd"]["rho"] - p, sp.Integer(0))
    excess_db = max(results["dB"]["rho"] - p, sp.Integer(0))
    harmonic_sum = sum(1 / value for value in degree)
    weighted_db_singletons = sum(
        results["dB"]["invariant"][(1 << i) - 1]
        / (harmonic_sum * degree[i])
        for i in range(order)
    )
    product_slack = sp.cancel(
        results["Bd"]["singleton_mass"] * weighted_db_singletons
        - fitness**3 * order * excess_bd * excess_db
    )
    return product_slack


def main() -> None:
    graphs = [
        (
            (0, 1, 2),
            (1, 0, 3),
            (2, 3, 0),
        ),
        (
            (0, 1, 2, 4),
            (1, 0, 3, 5),
            (2, 3, 0, 7),
            (4, 5, 7, 0),
        ),
        (
            (0, sp.Rational(1, 3), 5, 2),
            (sp.Rational(1, 3), 0, 4, sp.Rational(2, 5)),
            (5, 4, 0, 1),
            (2, sp.Rational(2, 5), 1, 0),
        ),
    ]
    checks = 0
    product_checks = 0
    minimum_product_slack = None
    for weights in graphs:
        for fitness in (sp.Rational(3, 2), sp.Rational(7, 3)):
            product_slack = check_graph(weights, fitness)
            checks += 1
            if fitness == sp.Rational(3, 2):
                assert product_slack >= 0, (weights, product_slack)
                product_checks += 1
                if minimum_product_slack is None or product_slack < minimum_product_slack:
                    minimum_product_slack = product_slack

    # A deterministic library of additional connected complete-support
    # rational graphs.  Integer edge weights are generated explicitly, so
    # every solve and every product comparison remains exact.
    for order in (3, 4):
        for seed in range(1, 9):
            weights = [[sp.Integer(0) for _ in range(order)] for _ in range(order)]
            for i in range(order):
                for j in range(i + 1, order):
                    value = sp.Integer(1 + ((i + 2) * (j + 3) * (seed + 1) + seed**2) % 11)
                    weights[i][j] = value
                    weights[j][i] = value
            product_slack = check_graph(tuple(map(tuple, weights)), sp.Rational(3, 2))
            assert product_slack >= 0, (order, seed, weights, product_slack)
            checks += 1
            product_checks += 1
            if minimum_product_slack is None or product_slack < minimum_product_slack:
                minimum_product_slack = product_slack

    # Exhaust every labelled connected support through four vertices under
    # three exact edge-weight patterns.  This deliberately includes paths,
    # stars, and graphs with highly unequal weights; zero entries are absent
    # edges, while every present edge has a positive integer weight.
    for order in (3, 4):
        edges = list(combinations(range(order), 2))
        for support_mask in range(1, 1 << len(edges)):
            adjacency = [set() for _ in range(order)]
            for edge_index, (i, j) in enumerate(edges):
                if (support_mask >> edge_index) & 1:
                    adjacency[i].add(j)
                    adjacency[j].add(i)
            reached = {0}
            frontier = [0]
            while frontier:
                vertex = frontier.pop()
                for neighbor in adjacency[vertex] - reached:
                    reached.add(neighbor)
                    frontier.append(neighbor)
            if len(reached) != order:
                continue

            for pattern in range(3):
                weights = [
                    [sp.Integer(0) for _ in range(order)]
                    for _ in range(order)
                ]
                for edge_index, (i, j) in enumerate(edges):
                    if not ((support_mask >> edge_index) & 1):
                        continue
                    if pattern == 0:
                        value = sp.Integer(1)
                    elif pattern == 1:
                        value = sp.Integer(
                            1 + ((edge_index + 2) * (support_mask + 3)) % 13
                        )
                    else:
                        value = sp.Integer(5**edge_index)
                    weights[i][j] = value
                    weights[j][i] = value
                product_slack = check_graph(
                    tuple(map(tuple, weights)), sp.Rational(3, 2)
                )
                assert product_slack >= 0, (
                    order, support_mask, pattern, weights, product_slack
                )
                checks += 1
                product_checks += 1
                if (
                    minimum_product_slack is None
                    or product_slack < minimum_product_slack
                ):
                    minimum_product_slack = product_slack

    print(f"PASS: {checks} exact forward/dual stationary-chain checks")
    print(
        "PASS: open product inequality survived "
        f"{product_checks} exact rational small-graph tests at r=3/2 "
        f"(minimum slack {minimum_product_slack})"
    )


if __name__ == "__main__":
    main()
