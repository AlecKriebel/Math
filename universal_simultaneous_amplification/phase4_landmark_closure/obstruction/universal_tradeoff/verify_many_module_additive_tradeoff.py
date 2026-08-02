#!/usr/bin/env python3
"""Exact checks for MANY_MODULE_ADDITIVE_TRADEOFF.md."""

from __future__ import annotations

from fractions import Fraction as F


def budget_b(size: int, fitness: F) -> F:
    return F(size, 1) / (1 - fitness ** (-size))


def budget_d(size: int, fitness: F) -> F:
    return F(size - 1, 1) / (1 - fitness ** (1 - size))


def complete_value(size: int, fitness: F, rule: str) -> F:
    asymptotic = 1 - 1 / fitness
    budget = budget_b if rule == "Bd" else budget_d
    return asymptotic * budget(size, fitness) / size


def general_identity(
    sizes: list[int], fitness: F, probabilities: list[F], rule: str
) -> None:
    total = sum(sizes)
    asymptotic = 1 - 1 / fitness
    budget = budget_b if rule == "Bd" else budget_d
    fixation = asymptotic / total * sum(
        budget(size, fitness) * probability
        for size, probability in zip(sizes, probabilities)
    )
    local_excess = sum(budget(size, fitness) for size in sizes) - budget(
        total, fitness
    )
    loss = sum(
        budget(size, fitness) * (1 - probability)
        for size, probability in zip(sizes, probabilities)
    )
    direct = total / asymptotic * (
        fixation - complete_value(total, fitness, rule)
    )
    assert direct == local_excess - loss


def scalar_values(size: int, fitness: F, scale: F) -> tuple[F, F, F]:
    t_value = fitness**size
    c_value = F(size, size - 1) * fitness * (
        fitness ** (size - 1) - 1
    )
    s_value = fitness * (
        size - fitness ** (size - 1)
    ) / (size - 1)
    b_value = F(size, 1) * (scale - 1) / (
        1 + scale * (t_value - 1)
    )
    d_value = F(size, 1) * (s_value - scale) / (scale + c_value)
    delta = (
        F(size, 1)
        * (1 - s_value)
        * (t_value - 2)
        / ((t_value - 1) * c_value - 1)
    )
    return b_value, d_value, delta


def fixation_clique(size: int, fitness: F, rule: str) -> F:
    """Uniform-singleton fixation obtained from the clique count chain."""
    asymptotic = 1 - 1 / fitness
    if rule == "Bd":
        return asymptotic / (1 - fitness ** (-size))
    return asymptotic * F(size - 1, size) / (
        1 - fitness ** (1 - size)
    )


def exact_gate_odds(
    core: int, satellite: int, fitness: F, scale: F, rule: str
) -> F:
    """Successful favorable/adverse odds from their raw-rate definition."""
    raw_ratio = fitness * scale if rule == "Bd" else fitness**2 / scale
    return raw_ratio * fixation_clique(core, fitness, rule) / fixation_clique(
        satellite, 1 / fitness, rule
    )


def closed_gate_odds(
    core: int, satellite: int, fitness: F, scale: F, rule: str
) -> F:
    if rule == "Bd":
        return (
            scale
            * fitness**core
            * (fitness**satellite - 1)
            / (fitness**core - 1)
        )
    return (
        F(1, 1)
        / scale
        * F(satellite * (core - 1), core * (satellite - 1))
        * fitness**core
        * (fitness ** (satellite - 1) - 1)
        / (fitness ** (core - 1) - 1)
    )


def satellite_correction_identity(
    size: int, fitness: F, scale: F, rule: str
) -> None:
    """Check equations (14)--(15) before any asymptotic approximation."""
    if rule == "Bd":
        odds = scale * (fitness**size - 1)
        correction = budget_b(size, fitness) * odds / (1 + odds) - size
        b_value, _, _ = scalar_values(size, fitness, scale)
        assert correction == b_value
    else:
        c_value = F(size, size - 1) * fitness * (
            fitness ** (size - 1) - 1
        )
        odds = c_value / scale
        correction = budget_d(size, fitness) * odds / (1 + odds) - size
        _, d_value, _ = scalar_values(size, fitness, scale)
        assert correction == d_value


def solve_linear(matrix: list[list[F]], rhs: list[F]) -> list[F]:
    """Exact Gauss--Jordan solver, used only on the independent macrochain."""
    size = len(rhs)
    augmented = [row[:] + [value] for row, value in zip(matrix, rhs)]
    for column in range(size):
        pivot = next(row for row in range(column, size) if augmented[row][column])
        augmented[column], augmented[pivot] = augmented[pivot], augmented[column]
        pivot_value = augmented[column][column]
        augmented[column] = [value / pivot_value for value in augmented[column]]
        for row in range(size):
            if row == column:
                continue
            multiplier = augmented[row][column]
            if multiplier:
                augmented[row] = [
                    left - multiplier * right
                    for left, right in zip(augmented[row], augmented[column])
                ]
    return [augmented[row][-1] for row in range(size)]


def exact_macro_fixation(
    sizes: list[int],
    internal_degrees: list[F],
    conductances: dict[tuple[int, int], F],
    fitness: F,
    rule: str,
) -> dict[int, F]:
    """Build and solve the homogeneous-module macrochain from update rates."""
    module_count = len(sizes)
    full_state = (1 << module_count) - 1
    transient = list(range(1, full_state))
    position = {state: index for index, state in enumerate(transient)}
    matrix = [[F(0) for _ in transient] for _ in transient]
    rhs = [F(0) for _ in transient]

    for state in transient:
        row = position[state]
        successful_rates: dict[int, F] = {}
        for (left, right), conductance in conductances.items():
            left_mutant = bool(state & (1 << left))
            right_mutant = bool(state & (1 << right))
            if left_mutant == right_mutant:
                continue
            for source, destination in ((left, right), (right, left)):
                source_mutant = bool(state & (1 << source))
                destination_mutant = bool(state & (1 << destination))
                source_fitness = fitness if source_mutant else F(1)
                destination_fitness = fitness if destination_mutant else F(1)
                relative_fitness = source_fitness / destination_fitness
                if rule == "Bd":
                    raw_rate = (
                        source_fitness
                        * conductance
                        / internal_degrees[source]
                    )
                else:
                    raw_rate = (
                        relative_fitness
                        * conductance
                        / internal_degrees[destination]
                    )
                rate = raw_rate * fixation_clique(
                    sizes[destination], relative_fitness, rule
                )
                if source_mutant:
                    next_state = state | (1 << destination)
                else:
                    next_state = state & ~(1 << destination)
                successful_rates[next_state] = (
                    successful_rates.get(next_state, F(0)) + rate
                )

        total_rate = sum(successful_rates.values(), F(0))
        assert total_rate > 0
        matrix[row][row] = total_rate
        for next_state, rate in successful_rates.items():
            if next_state == full_state:
                rhs[row] += rate
            elif next_state:
                matrix[row][position[next_state]] -= rate

    solution = solve_linear(matrix, rhs)
    return {state: solution[position[state]] for state in transient}


def macrochain_star_checks(fitness: F) -> int:
    """Independent exact transition, solve, identity, and gate checks."""
    sizes = [13, 2, 5]
    internal_degrees = [F(17, 5), F(7, 3), F(11, 4)]
    conductances = {(0, 1): F(2, 7), (0, 2): F(5, 13)}
    total = sum(sizes)
    checks = 0
    for rule in ("Bd", "dB"):
        fixation = exact_macro_fixation(
            sizes, internal_degrees, conductances, fitness, rule
        )
        single_module_probabilities = [fixation[1 << module] for module in range(3)]
        general_identity(sizes, fitness, single_module_probabilities, rule)
        checks += 1

        budget = budget_b if rule == "Bd" else budget_d
        normalized_actual = (
            sum(
                budget(size, fitness) * probability
                for size, probability in zip(sizes, single_module_probabilities)
            )
            - budget(total, fitness)
        )
        normalized_gate_bound = budget(sizes[0], fitness) - budget(
            total, fitness
        )
        for satellite in (1, 2):
            scale = internal_degrees[0] / internal_degrees[satellite]
            odds = closed_gate_odds(
                sizes[0], sizes[satellite], fitness, scale, rule
            )
            gate_probability = odds / (1 + odds)
            assert single_module_probabilities[satellite] <= gate_probability
            normalized_gate_bound += (
                budget(sizes[satellite], fitness) * gate_probability
            )
            checks += 1
        assert single_module_probabilities[0] <= 1
        assert normalized_actual <= normalized_gate_bound
        checks += 2
    return checks


def main() -> None:
    fitness = F(31, 20)

    identity_checks = 0
    examples = [
        ([2, 3, 11], [F(1, 4), F(2, 3), F(7, 8)]),
        ([4, 7, 9, 20], [F(3, 5), F(1, 7), F(5, 6), F(9, 10)]),
        ([8, 13, 21], [F(2, 9), F(4, 9), F(8, 9)]),
    ]
    for sizes, probabilities in examples:
        for rule in ("Bd", "dB"):
            general_identity(sizes, fitness, probabilities, rule)
            identity_checks += 1

    scalar_checks = 0
    correction_checks = 0
    smallest_delta = None
    for size in range(2, 41):
        t_value = fitness**size
        c_value = F(size, size - 1) * fitness * (
            fitness ** (size - 1) - 1
        )
        sigma_zero = (c_value - 1) / (t_value - 2)
        b_value, d_value, delta = scalar_values(
            size, fitness, sigma_zero
        )
        assert b_value + d_value == -delta
        assert delta > 0
        if smallest_delta is None or delta < smallest_delta:
            smallest_delta = delta

        # Exact off-maximum checks on both sides.
        for scale in (sigma_zero / 3, sigma_zero * 5):
            b_value, d_value, _ = scalar_values(size, fitness, scale)
            assert b_value + d_value < -delta
            for rule in ("Bd", "dB"):
                satellite_correction_identity(size, fitness, scale, rule)
                correction_checks += 1
        scalar_checks += 3

    # Audit the sharpened range at a rational fitness just above sqrt(2).
    near_threshold_fitness = F(10, 7)
    assert near_threshold_fitness**2 > 2
    threshold_checks = 0
    for size in range(2, 41):
        t_value = near_threshold_fitness**size
        c_value = F(size, size - 1) * near_threshold_fitness * (
            near_threshold_fitness ** (size - 1) - 1
        )
        assert t_value > 2 and c_value > 1
        sigma_zero = (c_value - 1) / (t_value - 2)
        b_value, d_value, delta = scalar_values(
            size, near_threshold_fitness, sigma_zero
        )
        assert b_value + d_value == -delta < 0
        if smallest_delta is None or delta < smallest_delta:
            smallest_delta = delta
        threshold_checks += 1

    below_threshold_fitness = F(7, 5)
    assert below_threshold_fitness**2 < 2
    limiting_sum = (
        2
        * (2 - below_threshold_fitness**2)
        / (below_threshold_fitness**2 - 1)
    )
    assert limiting_sum > 0
    threshold_checks += 1

    gate_checks = 0
    for core, satellite, scale in (
        (13, 2, F(1, 7)),
        (29, 7, F(11, 5)),
        (61, 19, F(43, 17)),
    ):
        for rule in ("Bd", "dB"):
            assert exact_gate_odds(
                core, satellite, fitness, scale, rule
            ) == closed_gate_odds(core, satellite, fitness, scale, rule)
            gate_checks += 1

    macrochain_checks = macrochain_star_checks(fitness)

    # Exact all-mesoscopic dB budgets are negative before macro charges.
    mesoscopic_checks = 0
    for sizes in ([10, 12], [15, 20, 25], [30, 40, 50, 60]):
        total = sum(sizes)
        excess = sum(budget_d(size, fitness) for size in sizes) - budget_d(
            total, fitness
        )
        assert excess < 0
        mesoscopic_checks += 1

    print(f"PASS: {identity_checks} exact general budget/charge identities")
    print(f"PASS: {gate_checks} exact update-rule gate identities")
    print(f"PASS: {macrochain_checks} exact multi-satellite macrochain checks")
    print(f"PASS: {correction_checks} exact satellite correction identities")
    print(f"PASS: {scalar_checks} exact additive scalar checks")
    print(f"PASS: {threshold_checks} exact sqrt(2)-threshold checks")
    print(f"PASS: {mesoscopic_checks} exact mesoscopic budget checks")
    print(f"smallest audited delta ~= {float(smallest_delta):.6f}")
    print("PROVED CLASS OBSTRUCTION ONLY: no new universal R_sim bound")


if __name__ == "__main__":
    main()
