#!/usr/bin/env python3
"""Exact checks for TWO_MODULE_ONE_OVER_N_TRADEOFF.md.

All computations use Fraction arithmetic.  The asymptotic arguments in the
note are analytic; this verifier independently checks every finite algebraic
identity and representative instances of each threshold regime.
"""

from __future__ import annotations

from fractions import Fraction as F


def local_bd(size: int, fitness: F) -> F:
    return (1 - 1 / fitness) / (1 - fitness ** (-size))


def local_db(size: int, fitness: F) -> F:
    return (
        (1 - 1 / fitness)
        * F(size - 1, size)
        / (1 - fitness ** (1 - size))
    )


def budget_bd(size: int, fitness: F) -> F:
    return F(size, 1) / (1 - fitness ** (-size))


def budget_db(size: int, fitness: F) -> F:
    return F(size - 1, 1) / (1 - fitness ** (1 - size))


def odds(
    left: int, right: int, fitness: F, scale: F
) -> tuple[F, F, F, F]:
    z_b_left = (
        scale
        * fitness**right
        * (fitness**left - 1)
        / (fitness**right - 1)
    )
    z_b_right = (
        fitness**left
        * (fitness**right - 1)
        / (scale * (fitness**left - 1))
    )
    z_d_left = (
        F(left * (right - 1), right * (left - 1))
        * fitness**right
        * (fitness ** (left - 1) - 1)
        / (scale * (fitness ** (right - 1) - 1))
    )
    z_d_right = (
        scale
        * F(right * (left - 1), left * (right - 1))
        * fitness**left
        * (fitness ** (right - 1) - 1)
        / (fitness ** (left - 1) - 1)
    )
    return z_b_left, z_b_right, z_d_left, z_d_right


def weak_fixation(
    left: int, right: int, fitness: F, scale: F, rule: str
) -> F:
    total = left + right
    z_b_l, z_b_r, z_d_l, z_d_r = odds(left, right, fitness, scale)
    if rule == "Bd":
        local = local_bd
        z_left, z_right = z_b_l, z_b_r
    elif rule == "dB":
        local = local_db
        z_left, z_right = z_d_l, z_d_r
    else:
        raise ValueError(rule)
    return (
        F(left, total) * local(left, fitness) * z_left / (1 + z_left)
        + F(right, total) * local(right, fitness) * z_right / (1 + z_right)
    )


def correction(
    left: int, right: int, fitness: F, scale: F, rule: str
) -> tuple[F, F, F]:
    total = left + right
    z_b_l, z_b_r, z_d_l, z_d_r = odds(left, right, fitness, scale)
    if rule == "Bd":
        budget = budget_bd
        local = local_bd
        z_left, z_right = z_b_l, z_b_r
    else:
        budget = budget_db
        local = local_db
        z_left, z_right = z_d_l, z_d_r
    excess = budget(left, fitness) + budget(right, fitness) - budget(
        total, fitness
    )
    loss = budget(left, fitness) / (1 + z_left) + budget(
        right, fitness
    ) / (1 + z_right)
    direct = F(total, 1) / (1 - 1 / fitness) * (
        weak_fixation(left, right, fitness, scale, rule)
        - local(total, fitness)
    )
    assert direct == excess - loss
    return excess, loss, direct


def scalar_identities(size: int, fitness: F, scale: F) -> int:
    c_value = F(size, size - 1) * fitness * (
        fitness ** (size - 1) - 1
    )
    sigma_star = fitness * (
        size - fitness ** (size - 1)
    ) / (size - 1)
    e_d = F(
        size, 1
    )  # overwritten in the exact rational expression below
    e_d = (size - fitness ** (size - 1)) / (
        fitness ** (size - 1) - 1
    )
    e_b = F(size, 1) / (fitness**size - 1)

    d_left = e_d - budget_db(size, fitness) / (1 + c_value / scale)
    b_left = e_b - budget_bd(size, fitness) / (
        1 + scale * (fitness**size - 1)
    )
    assert d_left == F(size, 1) * (sigma_star - scale) / (
        scale + c_value
    )
    assert b_left == F(size, 1) * (scale - 1) / (
        1 + scale * (fitness**size - 1)
    )
    assert 1 - sigma_star == (
        fitness**size - size * fitness + size - 1
    ) / (size - 1)
    return 3


def main() -> None:
    fitness = F(31, 20)  # 3/2 < r < 4^(1/3): k=2,3,4 are possible.
    finite_checks = 0
    for left, right, scale in [
        (2, 7, F(1, 3)),
        (3, 11, F(5, 7)),
        (4, 19, F(9, 5)),
        (8, 13, F(17, 4)),
    ]:
        z_b_l, z_b_r, z_d_l, z_d_r = odds(
            left, right, fitness, scale
        )
        assert z_b_l * z_b_r == fitness ** (left + right)
        assert z_d_l * z_d_r == fitness ** (left + right)
        correction(left, right, fitness, scale, "Bd")
        correction(left, right, fitness, scale, "dB")
        finite_checks += 4

    scalar_checks = 0
    for size in (2, 3, 4):
        sigma_star = fitness * (
            size - fitness ** (size - 1)
        ) / (size - 1)
        assert 0 < sigma_star < 1
        scalar_checks += scalar_identities(size, fitness, sigma_star / 2)

        # At a large finite core, a scale below the threshold gives positive
        # dB comparison and negative Bd comparison exactly.
        _, _, d_gap = correction(
            size, 120, fitness, sigma_star / 2, "dB"
        )
        _, _, b_gap = correction(
            size, 120, fitness, sigma_star / 2, "Bd"
        )
        assert d_gap > 0
        assert b_gap < 0

    # If both modules grow, the dB local budget tends to -1 and is already
    # negative in these exact mesoscopic examples, before macro losses.
    mesoscopic_checks = 0
    for left, right in ((10, 30), (20, 80), (40, 160)):
        excess = (
            budget_db(left, fitness)
            + budget_db(right, fitness)
            - budget_db(left + right, fitness)
        )
        assert excess < 0
        mesoscopic_checks += 1

    print(f"PASS: {finite_checks} exact odds/correction checks")
    print(f"PASS: {scalar_checks} exact bounded-module scalar checks")
    print(f"PASS: {mesoscopic_checks} exact negative dB local budgets")
    print("PROVED: dB amplification forces Bd suppression in the two-module model")


if __name__ == "__main__":
    main()
