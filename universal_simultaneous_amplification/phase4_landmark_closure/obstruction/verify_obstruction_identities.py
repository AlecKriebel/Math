#!/usr/bin/env python3
"""Independent exact checks for the Phase-4 obstruction identities.

The checks use only ``fractions.Fraction``.  They build singleton and general
mutant-set transitions directly from the two update definitions and compare
them with the closed forms in REPORT.md.  This is a finite identity verifier,
not evidence for any open asymptotic claim.
"""

from __future__ import annotations

from fractions import Fraction
import random


def random_weights(order: int, rng: random.Random) -> list[list[Fraction]]:
    weights = [[Fraction(0) for _ in range(order)] for _ in range(order)]
    for i in range(order):
        for j in range(i + 1, order):
            value = Fraction(rng.randint(1, 13), rng.randint(1, 11))
            weights[i][j] = weights[j][i] = value
    return weights


def check_graph(weights: list[list[Fraction]], fitness: Fraction) -> int:
    order = len(weights)
    degrees = [sum(row) for row in weights]
    influence = [
        [weights[i][j] / degrees[j] for j in range(order)]
        for i in range(order)
    ]
    temperature = [sum(row) for row in influence]
    assert sum(temperature) == order

    bd_reach_two = []
    db_reach_two = []
    lambdas = []
    for initial in range(order):
        # Bd, from the update definition: the singleton reproduces across an
        # edge with total mass r/F, and residents replace it with mass t_i/F.
        total_fitness = fitness + order - 1
        up_bd = sum(
            fitness / total_fitness * weights[initial][j] / degrees[initial]
            for j in range(order)
            if j != initial
        )
        down_bd = sum(
            Fraction(1, 1)
            / total_fitness
            * weights[j][initial]
            / degrees[j]
            for j in range(order)
            if j != initial
        )
        assert up_bd == fitness / total_fitness
        assert down_bd == temperature[initial] / total_fitness
        direct_bd = up_bd / (up_bd + down_bd)
        closed_bd = fitness / (fitness + temperature[initial])
        assert direct_bd == closed_bd
        bd_reach_two.append(closed_bd)

        # dB, in the rate-one-per-target Poissonization.  The initial mutant
        # dies at rate one.  Its successful births are summed over targets.
        birth_rate = Fraction(0)
        for target in range(order):
            if target == initial:
                continue
            mutant_mass = weights[initial][target]
            direct_term = fitness * mutant_mass / (
                degrees[target] + (fitness - 1) * mutant_mass
            )
            p = influence[initial][target]
            closed_term = fitness * p / (1 + (fitness - 1) * p)
            assert direct_term == closed_term
            birth_rate += direct_term
        direct_db = birth_rate / (1 + birth_rate)
        db_reach_two.append(direct_db)
        lambdas.append(birth_rate)

    bd_average = sum(bd_reach_two) / order
    db_average = sum(db_reach_two) / order
    benchmark = fitness / (fitness + 1)
    assert bd_average >= benchmark
    assert db_average <= benchmark

    concentration = sum(
        influence[i][j] ** 2 for i in range(order) for j in range(order)
    ) / order
    lambda_average = sum(lambdas) / order
    # The exact mean deficit and its convenient lower bound.
    exact_deficit = (
        fitness
        * (fitness - 1)
        / order
        * sum(
            influence[i][j] ** 2
            / (1 + (fitness - 1) * influence[i][j])
            for i in range(order)
            for j in range(order)
        )
    )
    assert fitness - lambda_average == exact_deficit
    assert exact_deficit >= (fitness - 1) * concentration

    # General-state check of (40)--(42).  Here transition is the row-
    # stochastic kernel P, in contrast with the transposed indexing used by
    # ``influence`` above.
    transition = [
        [weights[i][j] / degrees[i] for j in range(order)]
        for i in range(order)
    ]
    state_cases = 0
    for mask in range(1, (1 << order) - 1):
        mutant = [(mask >> i) & 1 for i in range(order)]
        mutant_count = sum(mutant)
        total_fitness = order + (fitness - 1) * mutant_count
        x = [
            sum(transition[i][j] * mutant[j] for j in range(order))
            for i in range(order)
        ]
        flow_out = sum(1 - x[i] for i in range(order) if mutant[i])
        flow_in = sum(x[i] for i in range(order) if not mutant[i])
        assert flow_out > 0 and flow_in > 0

        direct_bd_up = Fraction(0)
        direct_bd_down = Fraction(0)
        direct_bd_inverse_degree_drift = Fraction(0)
        for parent in range(order):
            for target in range(order):
                if not weights[parent][target]:
                    continue
                probability = (
                    (fitness if mutant[parent] else 1)
                    / total_fitness
                    * weights[parent][target]
                    / degrees[parent]
                )
                if mutant[parent] and not mutant[target]:
                    direct_bd_up += probability
                elif not mutant[parent] and mutant[target]:
                    direct_bd_down += probability
                direct_bd_inverse_degree_drift += (
                    probability
                    * (mutant[parent] - mutant[target])
                    / degrees[target]
                )
        assert direct_bd_up == fitness * flow_out / total_fitness
        assert direct_bd_down == flow_in / total_fitness
        ratio_bd = direct_bd_up / direct_bd_down
        assert ratio_bd == fitness * flow_out / flow_in
        inverse_cut = sum(
            weights[parent][target]
            / (degrees[parent] * degrees[target])
            for parent in range(order)
            for target in range(order)
            if mutant[parent] and not mutant[target]
        )
        assert direct_bd_inverse_degree_drift == (
            (fitness - 1) / total_fitness * inverse_cut
        )

        direct_db_up = Fraction(0)
        direct_db_down = Fraction(0)
        direct_db_degree_drift = Fraction(0)
        for target in range(order):
            denominator = sum(
                weights[parent][target]
                * (fitness if mutant[parent] else 1)
                for parent in range(order)
            )
            for parent in range(order):
                if not weights[parent][target]:
                    continue
                probability = (
                    Fraction(1, order)
                    * weights[parent][target]
                    * (fitness if mutant[parent] else 1)
                    / denominator
                )
                if mutant[parent] and not mutant[target]:
                    direct_db_up += probability
                elif not mutant[parent] and mutant[target]:
                    direct_db_down += probability
                direct_db_degree_drift += (
                    probability
                    * (mutant[parent] - mutant[target])
                    * degrees[target]
                )
        closed_db_up = (
            fitness
            / order
            * sum(
                x[i] / (1 + (fitness - 1) * x[i])
                for i in range(order)
                if not mutant[i]
            )
        )
        closed_db_down = (
            Fraction(1, order)
            * sum(
                (1 - x[i]) / (1 + (fitness - 1) * x[i])
                for i in range(order)
                if mutant[i]
            )
        )
        assert direct_db_up == closed_db_up
        assert direct_db_down == closed_db_down
        ratio_db = direct_db_up / direct_db_down
        assert ratio_bd * ratio_db <= fitness**3
        closed_db_degree_drift = (
            (fitness - 1)
            / order
            * sum(
                degrees[i]
                * x[i]
                * (1 - x[i])
                / (1 + (fitness - 1) * x[i])
                for i in range(order)
            )
        )
        assert direct_db_degree_drift == closed_db_degree_drift
        state_cases += 1
    return state_cases


def main() -> None:
    rng = random.Random(20260801)
    cases = 0
    state_cases = 0
    for order in range(3, 9):
        for fitness in (Fraction(11, 10), Fraction(6, 5), Fraction(2), Fraction(7)):
            for _ in range(20):
                state_cases += check_graph(random_weights(order, rng), fitness)
                cases += 1
    print(
        f"PASS: {cases} exact weighted-graph and "
        f"{state_cases} nonabsorbing-state checks"
    )


if __name__ == "__main__":
    main()
