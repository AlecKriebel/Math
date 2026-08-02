#!/usr/bin/env python3
"""Exact diagnostic: level-1 plus size balance do not imply inequality (62).

This constructs an exchangeable probability law on the nonempty subsets of
K_7 at r=3/2.  The law satisfies every stationary singleton equation and the
exact stationary first-moment balance, but its (62) margin is negative.  It
is deliberately *not* asserted to be stationary for the full set chain.
"""

from fractions import Fraction as F
from math import comb


def main() -> None:
    n = 7
    r = F(3, 2)
    baseline_limit = 1 - 1 / r
    level_mass = {1: F(12, 67), 2: F(15, 67), 3: F(40, 67)}

    assert sum(level_mass.values()) == 1
    assert all(value >= 0 for value in level_mass.values())

    edge_probability = F(1, n - 1)
    ell = edge_probability / (r - (r - 1) * edge_probability)
    assert ell == F(2, 17)

    singleton = level_mass[1] / n
    doubleton = level_mass[2] / comb(n, 2)
    singleton_rhs = (n - 1) * ell * (singleton + doubleton)
    assert singleton_rhs == singleton

    # On a k-set of K_n,
    # C=k(k-1)/(n-1), while at r=3/2
    # (r-1)R2=k(n-k)/((n-1)(2n-1)).
    size_integrand = {
        k: F(k * (k - 1), n - 1)
        + F(k * (n - k), (n - 1) * (2 * n - 1))
        for k in range(1, n)
    }
    assert [size_integrand[k] for k in (1, 2, 3)] == [
        F(1, 13),
        F(6, 13),
        F(15, 13),
    ]

    mean_size = sum(k * mass for k, mass in level_mass.items())
    mean_integrand = sum(
        size_integrand[k] * mass for k, mass in level_mass.items()
    )
    assert mean_size == F(162, 67)
    assert mean_integrand == F(54, 67)
    assert mean_integrand == baseline_limit * mean_size

    # Regularity makes (sum_i q_i/d_i)/H = p_1/n.
    normalized_margin = (
        level_mass[1] / (n * r**2)
        - (mean_size / n - baseline_limit)
    )
    assert normalized_margin == -F(1, 1407)

    # A second example also satisfies the exact second factorial-moment
    # balance.  On K_9 its mass is supported on levels 3 and 8.
    n2 = 9
    level_mass2 = {3: F(112, 115), 8: F(3, 115)}
    assert sum(level_mass2.values()) == 1

    def appearance(size: int, edge_probability: F) -> F:
        """Probability that all `size` named vertices appear in the burst."""
        return sum(
            F((-1) ** (sampled + 1) * comb(size, sampled))
            * (
                r * sampled * edge_probability
                / (1 + (r - 1) * sampled * edge_probability)
            )
            for sampled in range(1, size + 1)
        )

    def factorial_generators(order: int, size: int) -> tuple[F, F]:
        edge_probability = F(1, order - 1)
        outside = order - size
        mean_added = outside * appearance(1, edge_probability)
        pair_added = comb(outside, 2) * appearance(2, edge_probability)
        first = size * (mean_added - 1)
        second = size * (
            (size - 1) * (mean_added - 1) + pair_added
        )
        return first, second

    generators = {
        size: factorial_generators(n2, size) for size in level_mass2
    }
    assert generators == {
        3: (F(3, 17), F(21, 17)),
        8: (-F(112, 17), -F(784, 17)),
    }
    assert all(
        sum(
            mass * generators[size][moment]
            for size, mass in level_mass2.items()
        )
        == 0
        for moment in (0, 1)
    )
    mean_size2 = sum(size * mass for size, mass in level_mass2.items())
    assert mean_size2 == F(72, 23)
    normalized_margin2 = -(mean_size2 / n2 - baseline_limit)
    assert normalized_margin2 == -F(1, 69)

    print("PASS exact hierarchy obstruction")
    print("singleton equations: all 7 hold by exchangeability")
    print(f"mean size = {mean_size}")
    print(f"normalized (62) margin = {normalized_margin}")
    print("PASS exact second-moment hierarchy obstruction")
    print(f"second-example normalized (62) margin = {normalized_margin2}")
    print("NOTE: the putative law is not a full-chain stationary law")


if __name__ == "__main__":
    main()
