#!/usr/bin/env python3
"""Exact verifier for the fixed-N=41 degree-5 BV pseudo-distribution.

Only Python's standard library is used. All arithmetic is rational.
"""

from __future__ import annotations

import argparse
from fractions import Fraction
import itertools
import json
from pathlib import Path
from typing import Iterable


def parse_fraction(value: str) -> Fraction:
    return Fraction(value)


def gegenbauer_5(k: int, t: Fraction) -> Fraction:
    """Normalized spherical Gegenbauer P_k^(5), with P_k^(5)(1)=1."""
    if k == 0:
        return Fraction(1)
    if k == 1:
        return t
    p0, p1 = Fraction(1), t
    for j in range(2, k + 1):
        p0, p1 = (
            p1,
            ((2 * j + 1) * t * p1 - (j - 1) * p0) / (j + 2),
        )
    return p1


def transverse_q(
    k: int, u: Fraction, v: Fraction, t: Fraction
) -> Fraction:
    """Polynomialized normalized P_k^(4) transverse kernel."""
    if k == 0:
        return Fraction(1)
    w = t - u * v
    if k == 1:
        return w
    a = (1 - u * u) * (1 - v * v)
    q0, q1 = Fraction(1), w
    for j in range(1, k):
        q0, q1 = (
            q1,
            (2 * (j + 1) * w * q1 - j * a * q0) / (j + 2),
        )
    return q1


def z_matrix(
    k: int,
    radial_degree: int,
    u: Fraction,
    v: Fraction,
    t: Fraction,
) -> list[list[Fraction]]:
    q = transverse_q(k, u, v, t)
    return [
        [q * u**i * v**j for j in range(radial_degree + 1)]
        for i in range(radial_degree + 1)
    ]


def zero_matrix(size: int) -> list[list[Fraction]]:
    return [[Fraction(0) for _ in range(size)] for _ in range(size)]


def add_scaled(
    target: list[list[Fraction]],
    source: list[list[Fraction]],
    scale: Fraction = Fraction(1),
) -> None:
    for i in range(len(target)):
        for j in range(len(target)):
            target[i][j] += scale * source[i][j]


def determinant(matrix: list[list[Fraction]]) -> Fraction:
    """Exact Gaussian-elimination determinant."""
    a = [row[:] for row in matrix]
    n = len(a)
    value = Fraction(1)
    sign = 1
    for column in range(n):
        pivot = next(
            (row for row in range(column, n) if a[row][column]),
            None,
        )
        if pivot is None:
            return Fraction(0)
        if pivot != column:
            a[column], a[pivot] = a[pivot], a[column]
            sign = -sign
        pivot_value = a[column][column]
        value *= pivot_value
        for row in range(column + 1, n):
            ratio = a[row][column] / pivot_value
            for col in range(column + 1, n):
                a[row][col] -= ratio * a[column][col]
    return sign * value


def leading_principal_minors(
    matrix: list[list[Fraction]],
) -> list[Fraction]:
    return [
        determinant([row[:size] for row in matrix[:size]])
        for size in range(1, len(matrix) + 1)
    ]


def unique_permutations(
    triple: tuple[Fraction, Fraction, Fraction],
) -> list[tuple[Fraction, Fraction, Fraction]]:
    return sorted(set(itertools.permutations(triple)))


def verify(certificate_path: Path) -> dict[str, object]:
    data = json.loads(certificate_path.read_text())
    assert data["schema"] in {
        "fixed41-bv-degree5-pseudodistribution-v1",
        "fixed41-bv-degree6-pseudodistribution-v1",
        "fixed41-bv-fullradial-k8-pseudodistribution-v1",
        "fixed41-bv-fullradial-k16-pseudodistribution-v1",
    }
    assert data["dimension"] == 5
    assert data["cardinality"] == 41
    assert parse_fraction(data["maximum_inner_product"]) == Fraction(1, 2)
    full_radial_degree = data.get("bv_full_radial_harmonic_degree")
    total_degree = data.get("bv_total_degree")
    two_point_degree = data["two_point_degree"]
    assert (total_degree, full_radial_degree, two_point_degree) in {
        (5, None, 20),
        (6, None, 30),
        (None, 8, 50),
        (None, 16, 100),
    }

    grid = [parse_fraction(value) for value in data["grid"]]
    triples = [tuple(map(int, triple)) for triple in data["triples"]]
    alpha = [parse_fraction(value) for value in data["alpha"]]
    nu = [parse_fraction(value) for value in data["nu"]]

    assert grid == sorted(grid)
    assert len(set(grid)) == len(grid)
    assert all(Fraction(-1) <= q <= Fraction(1, 2) for q in grid)
    assert len(alpha) == len(grid)
    assert len(nu) == len(triples)
    assert all(weight > 0 for weight in alpha)
    assert all(weight > 0 for weight in nu)
    assert sum(alpha) == 40
    assert sum(nu) == 40 * 39

    assert triples == sorted(triples)
    assert len(set(triples)) == len(triples)
    for triple in triples:
        assert tuple(sorted(triple)) == triple
        assert all(0 <= index < len(grid) for index in triple)
        u, v, t = (grid[index] for index in triple)
        gram_determinant = 1 + 2 * u * v * t - u * u - v * v - t * t
        assert gram_determinant >= 0

    # Here nu[h] is the total mass of the full permutation orbit of
    # triples[h]. Thus its contribution to one coordinate marginal at q is
    # multiplicity(q) * nu[h] / 3.
    for index in range(len(grid)):
        marginal = sum(
            weight * triple.count(index) / 3
            for triple, weight in zip(triples, nu, strict=True)
        )
        assert marginal == 39 * alpha[index]

    pair_moments = [
        1
        + sum(
            weight * gegenbauer_5(k, q)
            for q, weight in zip(grid, alpha, strict=True)
        )
        for k in range(1, two_point_degree + 1)
    ]
    assert all(moment > 0 for moment in pair_moments)

    def harmonic_matrix(
        total_degree: int, k: int
    ) -> list[list[Fraction]]:
        radial_degree = total_degree - k
        matrix = zero_matrix(radial_degree + 1)
        add_scaled(
            matrix,
            z_matrix(k, radial_degree, Fraction(1), Fraction(1), Fraction(1)),
        )
        for q, weight in zip(grid, alpha, strict=True):
            add_scaled(
                matrix,
                z_matrix(k, radial_degree, Fraction(1), q, q),
                weight,
            )
            add_scaled(
                matrix,
                z_matrix(k, radial_degree, q, Fraction(1), q),
                weight,
            )
            add_scaled(
                matrix,
                z_matrix(k, radial_degree, q, q, Fraction(1)),
                weight,
            )
        for triple, weight in zip(triples, nu, strict=True):
            values = tuple(grid[index] for index in triple)
            orbit = unique_permutations(values)
            for u, v, t in orbit:
                add_scaled(
                    matrix,
                    z_matrix(k, radial_degree, u, v, t),
                    weight / len(orbit),
                )
        assert all(
            matrix[i][j] == matrix[j][i]
            for i in range(len(matrix))
            for j in range(len(matrix))
        )
        return matrix

    harmonic_minors: list[list[Fraction]] = []
    if full_radial_degree is None:
        assert total_degree is not None
        for k in range(total_degree + 1):
            matrix = harmonic_matrix(total_degree, k)
            minors = leading_principal_minors(matrix)
            # Sylvester's criterion proves positive definiteness.
            assert all(minor > 0 for minor in minors)
            harmonic_minors.append(minors)
    else:
        # On a finite radial grid, positivity for arbitrary radial
        # polynomials is equivalent to PSD of the kernel-weight matrices W_k.
        extended_grid = grid + [Fraction(1)]

        def full_radial_matrix(k: int) -> list[list[Fraction]]:
            matrix = zero_matrix(len(extended_grid))
            matrix[-1][-1] = transverse_q(
                k, Fraction(1), Fraction(1), Fraction(1)
            )
            for index, (q, weight) in enumerate(
                zip(grid, alpha, strict=True)
            ):
                matrix[-1][index] += weight * transverse_q(
                    k, Fraction(1), q, q
                )
                matrix[index][-1] += weight * transverse_q(
                    k, q, Fraction(1), q
                )
                matrix[index][index] += weight * transverse_q(
                    k, q, q, Fraction(1)
                )
            for triple, weight in zip(triples, nu, strict=True):
                values = tuple(grid[index] for index in triple)
                orbit = unique_permutations(values)
                for u, v, t in orbit:
                    i = extended_grid.index(u)
                    j = extended_grid.index(v)
                    matrix[i][j] += (
                        weight * transverse_q(k, u, v, t) / len(orbit)
                    )
            assert all(
                matrix[i][j] == matrix[j][i]
                for i in range(len(matrix))
                for j in range(len(matrix))
            )
            return matrix

        assert grid == [
            Fraction(-1),
            Fraction(-3, 4),
            Fraction(-1, 2),
            Fraction(-1, 4),
            Fraction(0),
            Fraction(1, 4),
            Fraction(1, 2),
        ]
        for k in range(full_radial_degree + 1):
            matrix = full_radial_matrix(k)
            if k == 0:
                # Fixed-N marginals force this exact one-dimensional kernel.
                kernel = [Fraction(-1, 40)] * len(grid) + [Fraction(1)]
                assert all(
                    sum(
                        matrix[i][j] * kernel[j]
                        for j in range(len(matrix))
                    )
                    == 0
                    for i in range(len(matrix))
                )
                reduced = [row[:-1] for row in matrix[:-1]]
            else:
                # At u=-1 and u=1 the polynomialized transverse kernel is
                # zero. The six interior grid values form the active block.
                endpoint_indices = (0, len(matrix) - 1)
                assert all(
                    matrix[i][j] == 0
                    for i in endpoint_indices
                    for j in range(len(matrix))
                )
                reduced = [
                    [matrix[i][j] for j in range(1, len(grid))]
                    for i in range(1, len(grid))
                ]
            minors = leading_principal_minors(reduced)
            assert all(minor > 0 for minor in minors)
            harmonic_minors.append(minors)

    result = {
        "status": "PASS",
        "two_point_degree": two_point_degree,
        "grid_point_count": len(grid),
        "triple_orbit_count": len(triples),
        "alpha_mass": str(sum(alpha)),
        "nu_mass": str(sum(nu)),
        "minimum_two_point_moment": str(min(pair_moments)),
        "harmonic_block_sizes": [
            len(minors) for minors in harmonic_minors
        ],
        "minimum_alpha_weight": str(min(alpha)),
        "minimum_nu_weight": str(min(nu)),
    }
    if total_degree is not None:
        result["bv_total_degree"] = total_degree
        result["harmonic_mode"] = "total_degree"
    else:
        result["bv_full_radial_harmonic_degree"] = full_radial_degree
        result["harmonic_mode"] = "full_radial"
    if total_degree == 5:
        # This particular set of weights does not extend one more total degree.
        # For d=6, k=0, the principal submatrix indexed by radial monomials
        # 1,u^3,u^5,u^6 has a strictly negative exact determinant.
        degree_6_matrix = harmonic_matrix(6, 0)
        obstruction_indices = (0, 3, 5, 6)
        degree_6_obstruction = determinant(
            [
                [degree_6_matrix[i][j] for j in obstruction_indices]
                for i in obstruction_indices
            ]
        )
        assert degree_6_obstruction < 0
        result["degree_6_obstruction_determinant"] = str(
            degree_6_obstruction
        )
    return result


def main() -> None:
    default_certificate = (
        Path(__file__).resolve().parents[1]
        / "certificates"
        / "fixed41_bv_degree5_pseudodistribution.json"
    )
    parser = argparse.ArgumentParser()
    parser.add_argument("certificate", nargs="?", type=Path, default=default_certificate)
    args = parser.parse_args()
    print(json.dumps(verify(args.certificate), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
