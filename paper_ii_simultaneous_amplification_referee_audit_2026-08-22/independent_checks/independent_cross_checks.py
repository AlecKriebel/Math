#!/usr/bin/env python3
"""Independent standard-library checks for representative manuscript claims.

This program deliberately does not import the delivered certificate programs,
SymPy, or any expected-output file.
"""

from __future__ import annotations

from decimal import Decimal, getcontext
from fractions import Fraction as F
from itertools import combinations


Polynomial = list[F]  # coefficients in increasing degree order


def trim(poly: Polynomial) -> Polynomial:
    result = list(poly)
    while result and result[-1] == 0:
        result.pop()
    return result or [F(0)]


def derivative(poly: Polynomial) -> Polynomial:
    return trim([F(index) * coefficient for index, coefficient in enumerate(poly)][1:])


def divide(dividend: Polynomial, divisor: Polynomial) -> tuple[Polynomial, Polynomial]:
    remainder = trim(dividend)
    divisor = trim(divisor)
    if divisor == [0]:
        raise ZeroDivisionError
    quotient = [F(0)] * max(1, len(remainder) - len(divisor) + 1)
    while remainder != [0] and len(remainder) >= len(divisor):
        shift = len(remainder) - len(divisor)
        coefficient = remainder[-1] / divisor[-1]
        quotient[shift] += coefficient
        for index, value in enumerate(divisor):
            remainder[index + shift] -= coefficient * value
        remainder = trim(remainder)
    return trim(quotient), remainder


def evaluate(poly: Polynomial, point: F) -> F:
    value = F(0)
    for coefficient in reversed(poly):
        value = value * point + coefficient
    return value


def sturm_sequence(poly: Polynomial) -> list[Polynomial]:
    sequence = [trim(poly), derivative(poly)]
    while sequence[-1] != [0]:
        _, remainder = divide(sequence[-2], sequence[-1])
        if remainder == [0]:
            break
        sequence.append([-coefficient for coefficient in remainder])
    return sequence


def variations(sequence: list[Polynomial], point: F) -> int:
    signs = []
    for poly in sequence:
        value = evaluate(poly, point)
        if value:
            signs.append(1 if value > 0 else -1)
    return sum(left != right for left, right in zip(signs, signs[1:]))


def roots_between(sequence: list[Polynomial], left: F, right: F) -> int:
    if evaluate(sequence[0], left) == 0 or evaluate(sequence[0], right) == 0:
        raise ValueError("endpoints must not be roots")
    return variations(sequence, left) - variations(sequence, right)


def birth_death_fixation(up: list[F], down: list[F]) -> F:
    if len(up) != len(down):
        raise ValueError("up and down arrays must have the same length")
    product = F(1)
    denominator = F(1)
    for up_rate, down_rate in zip(up, down):
        product *= down_rate / up_rate
        denominator += product
    return F(1) / denominator


def check_complete_graph_baselines() -> None:
    r = F(3, 2)
    for n in range(2, 10):
        bd_up = []
        bd_down = []
        db_up = []
        db_down = []
        for mutants in range(1, n):
            residents = n - mutants
            bd_up.append(r * mutants / (n + (r - 1) * mutants) * F(residents, n - 1))
            bd_down.append(F(residents, n + (r - 1) * mutants) * F(mutants, n - 1))
            db_up.append(F(residents, n) * r * mutants / (r * mutants + residents - 1))
            db_down.append(F(mutants, n) * residents / (r * (mutants - 1) + residents))

        exact_bd = birth_death_fixation(bd_up, bd_down)
        exact_db = birth_death_fixation(db_up, db_down)
        claimed_bd = (1 - 1 / r) / (1 - r ** (-n))
        claimed_db = F(n - 1, n) * (1 - 1 / r) / (1 - r ** (-(n - 1)))
        assert exact_bd == claimed_bd
        assert exact_db == claimed_db
    print("complete_graph_baselines=exact_for_n_2_through_9_at_r_3_over_2")


def orbit_label(mask: int, core: int, pairs: int, pendants: int) -> tuple[int, int, int, int, int]:
    hub = mask & 1
    ordinary = sum((mask >> vertex) & 1 for vertex in range(1, core))
    mixed = full = 0
    pair_offset = core
    for pair in range(pairs):
        count = sum((mask >> (pair_offset + 2 * pair + side)) & 1 for side in (0, 1))
        mixed += count == 1
        full += count == 2
    leaf_offset = core + 2 * pairs
    leaves = sum((mask >> (leaf_offset + leaf)) & 1 for leaf in range(pendants))
    return int(bool(hub)), ordinary, mixed, full, leaves


def representative_graph() -> list[list[F]]:
    core, pairs, pendants = 4, 1, 1
    sigma, epsilon = F(2, 5), F(1, 17)
    pair_weight = F(core) / sigma
    order = core + 2 * pairs + pendants
    weights = [[F(0) for _ in range(order)] for _ in range(order)]
    for left, right in combinations(range(core), 2):
        weights[left][right] = weights[right][left] = F(1)
    for vertex in (core, core + 1):
        partner = core + 1 if vertex == core else core
        weights[vertex][partner] = pair_weight
        for center in range(core):
            weights[vertex][center] = weights[center][vertex] = epsilon
    leaf = core + 2 * pairs
    weights[0][leaf] = weights[leaf][0] = F(1)
    return weights


def aggregate_changing_row(mask: int, rule: str) -> dict[tuple[int, int, int, int, int], F]:
    core, pairs, pendants = 4, 1, 1
    weights = representative_graph()
    order = len(weights)
    r = F(7, 4)
    mutant = [bool(mask & (1 << vertex)) for vertex in range(order)]
    fitness = [r if state else F(1) for state in mutant]
    row: dict[tuple[int, int, int, int, int], F] = {}
    if rule == "Bd":
        total_fitness = sum(fitness, F(0))
        degrees = [sum(neighbors, F(0)) for neighbors in weights]
        for parent in range(order):
            for target in range(order):
                if weights[parent][target] and mutant[parent] != mutant[target]:
                    probability = (
                        fitness[parent]
                        / total_fitness
                        * weights[parent][target]
                        / degrees[parent]
                    )
                    target_label = orbit_label(mask ^ (1 << target), core, pairs, pendants)
                    row[target_label] = row.get(target_label, F(0)) + probability
    elif rule == "dB":
        for target in range(order):
            denominator = sum(
                (fitness[parent] * weights[parent][target] for parent in range(order)),
                F(0),
            )
            for parent in range(order):
                if weights[parent][target] and mutant[parent] != mutant[target]:
                    probability = (
                        F(1, order)
                        * fitness[parent]
                        * weights[parent][target]
                        / denominator
                    )
                    target_label = orbit_label(mask ^ (1 << target), core, pairs, pendants)
                    row[target_label] = row.get(target_label, F(0)) + probability
    else:
        raise ValueError(rule)
    return row


def check_representative_orbit_sums() -> None:
    # Two configurations related by an ordinary-core swap and pair-end swap.
    first = (1 << 1) | (1 << 2) | (1 << 4) | (1 << 6)
    second = (1 << 1) | (1 << 3) | (1 << 5) | (1 << 6)
    assert orbit_label(first, 4, 1, 1) == (0, 2, 1, 0, 1)
    assert orbit_label(second, 4, 1, 1) == (0, 2, 1, 0, 1)
    for rule in ("Bd", "dB"):
        first_row = aggregate_changing_row(first, rule)
        second_row = aggregate_changing_row(second, rule)
        assert first_row == second_row
        assert F(0) < sum(first_row.values(), F(0)) < F(1)
        encoded = ";".join(
            f"{label}:{value}" for label, value in sorted(first_row.items())
        )
        print(f"representative_{rule}_orbit_row={encoded}")
    print("representative_orbit_sums=exact_at_distinct_parameters")


def check_response_and_sextic() -> None:
    phase: Polynomial = [F(1), F(-6), F(21), F(-30), F(22), F(-8), F(1)]
    sequence = sturm_sequence(phase)
    assert roots_between(sequence, F(1), F(3, 2)) == 0
    assert roots_between(sequence, F(3, 2), F(151, 100)) == 1
    assert evaluate(phase, F(3, 2)) == F(1, 64)
    assert evaluate(phase, F(151, 100)) == F(-39866792399, 10**12)

    left, right = F(3, 2), F(151, 100)
    for _ in range(180):
        midpoint = (left + right) / 2
        if evaluate(phase, midpoint) > 0:
            left = midpoint
        else:
            right = midpoint
    getcontext().prec = 40
    root_decimal = Decimal(left.numerator) / Decimal(left.denominator)
    assert abs(root_decimal - Decimal("1.50285691279056963")) < Decimal("1e-17")

    r, sigma, lam = F(3, 2), F(19, 137), F(20, 27)
    z_bd = sigma * (r * r - 1)
    z_db = 2 * r * (r - 1) / sigma
    p = 1 - 1 / r
    pair_bd = 2 * ((r / (r + 1)) * z_bd / (1 + z_bd) / p - 1)
    pair_db = 2 * (F(1, 2) * z_db / (1 + z_db) / p - 1)
    response_bd = pair_bd + lam * (1 / p - 1)
    response_db = pair_db - lam
    assert response_bd == F(232, 17361)
    assert response_db == F(65, 12123)

    rational_discriminant = 10138**2 - 4 * 6439 * 703
    assert rational_discriminant == 576 * 147001
    print(f"sextic_root_isolation=0_then_1; root_approx={root_decimal}")
    print(f"rational_responses=Bd:{response_bd};dB:{response_db}")
    print(f"gate_odds=Bd:{z_bd};dB:{z_db}")


def main() -> None:
    check_complete_graph_baselines()
    check_representative_orbit_sums()
    check_response_and_sextic()
    print("PASS: independent standard-library cross-checks")


if __name__ == "__main__":
    main()
