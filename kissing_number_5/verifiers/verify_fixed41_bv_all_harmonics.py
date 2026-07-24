#!/usr/bin/env python3
"""Verify the all-harmonic fixed-41 BV pseudo-distribution certificate.

The program uses only Python's standard library.  All finite calculations are
performed with fractions.Fraction; floating-point arithmetic is not used.
"""

from __future__ import annotations

import argparse
from fractions import Fraction
import hashlib
import itertools
import json
import math
from pathlib import Path


Q = Fraction


class VerificationError(ValueError):
    """Raised when an exact certificate condition fails."""


def check(condition: bool, message: str) -> None:
    """Proof-critical assertion that remains active under ``python -O``."""

    if not condition:
        raise VerificationError(message)


def parse_q(value: str) -> Q:
    return Q(value)


def zero_matrix(size: int) -> list[list[Q]]:
    return [[Q(0) for _ in range(size)] for _ in range(size)]


def symmetric(matrix: list[list[Q]]) -> bool:
    return all(
        matrix[i][j] == matrix[j][i]
        for i in range(len(matrix))
        for j in range(len(matrix))
    )


def ldl_pivots(matrix: list[list[Q]]) -> list[Q]:
    """Exact diagonal pivots in an unpivoted LDL^T decomposition."""
    size = len(matrix)
    lower = zero_matrix(size)
    pivots: list[Q] = []
    for i in range(size):
        lower[i][i] = Q(1)
        for j in range(i):
            check(pivots[j] != 0, f"zero LDL pivot at index {j}")
            lower[i][j] = (
                matrix[i][j]
                - sum(
                    lower[i][h] * lower[j][h] * pivots[h]
                    for h in range(j)
                )
            ) / pivots[j]
        pivots.append(
            matrix[i][i]
            - sum(lower[i][h] ** 2 * pivots[h] for h in range(i))
        )
    return pivots


def inverse(matrix: list[list[Q]]) -> list[list[Q]]:
    """Exact Gauss--Jordan inverse."""
    size = len(matrix)
    work = [
        row[:] + [Q(i == j) for j in range(size)]
        for i, row in enumerate(matrix)
    ]
    for column in range(size):
        pivot = next(
            row
            for row in range(column, size)
            if work[row][column] != 0
        )
        work[column], work[pivot] = work[pivot], work[column]
        pivot_value = work[column][column]
        work[column] = [value / pivot_value for value in work[column]]
        for row in range(size):
            if row == column:
                continue
            multiplier = work[row][column]
            if multiplier:
                work[row] = [
                    value - multiplier * pivot_entry
                    for value, pivot_entry in zip(work[row], work[column])
                ]
    return [row[size:] for row in work]


def ceil_sqrt_fraction(value: Q) -> int:
    """Least integer n with n^2 >= value, computed without floats."""
    check(value > 0, "square-root argument must be positive")
    result = math.isqrt(value.numerator // value.denominator)
    while result * result * value.denominator < value.numerator:
        result += 1
    while (
        result > 0
        and (result - 1) ** 2 * value.denominator >= value.numerator
    ):
        result -= 1
    return result


def gegenbauer_5_sequence(t: Q, maximum_degree: int) -> list[Q]:
    """Normalized P_k^(5)(t), k=0,...,maximum_degree."""
    values = [Q(1)]
    if maximum_degree == 0:
        return values
    values.append(t)
    for k in range(2, maximum_degree + 1):
        values.append(
            ((2 * k + 1) * t * values[-1] - (k - 1) * values[-2])
            / (k + 2)
        )
    return values


def normalized_transverse_sequences(
    area: Q, displacement: Q, maximum_index: int
) -> tuple[list[Q], list[Q]]:
    """Even and odd normalized transverse kernels on one support triple.

    Entry m of the even sequence is P_(2m)^(4)(z).  Entry m of the odd
    sequence is sqrt(area) P_(2m+1)^(4)(z).  Both are rational because
    z=displacement/sqrt(area).
    """
    check(area > 0, "transverse area must be positive")
    x = 4 * displacement * displacement / area - 2
    even = [Q(1), (4 * displacement * displacement / area - 1) / 3]
    odd = [
        displacement,
        2 * displacement**3 / area - displacement,
    ]
    while len(even) <= maximum_index:
        degree = 2 * (len(even) - 1)
        even.append(
            (
                x * (degree + 1) * even[-1]
                - (degree - 1) * even[-2]
            )
            / (degree + 3)
        )
    while len(odd) <= maximum_index:
        degree = 2 * (len(odd) - 1) + 1
        odd.append(
            (
                x * (degree + 1) * odd[-1]
                - (degree - 1) * odd[-2]
            )
            / (degree + 3)
        )
    return even, odd


def verify(
    source_path: Path,
    all_harmonics_certificate_path: Path,
) -> dict[str, object]:
    source_bytes = source_path.read_bytes()
    source_sha256 = hashlib.sha256(source_bytes).hexdigest()
    source = json.loads(source_bytes)
    certificate = json.loads(all_harmonics_certificate_path.read_text())

    check(
        certificate["schema"] == "fixed41-bv-all-harmonics-v1",
        "unexpected all-harmonics certificate schema",
    )
    check(
        certificate["source_certificate"] == source_path.name,
        "source certificate filename mismatch",
    )
    check(
        certificate["source_sha256"] == source_sha256,
        "source certificate SHA-256 mismatch",
    )
    check(
        source["schema"]
        == "fixed41-bv-fullradial-k16-pseudodistribution-v1",
        "unexpected source schema",
    )
    check(source["dimension"] == 5, "source dimension is not five")
    check(source["cardinality"] == 41, "source cardinality is not 41")
    check(
        parse_q(source["maximum_inner_product"]) == Q(1, 2),
        "source maximum inner product is not 1/2",
    )

    grid = [parse_q(value) for value in source["grid"]]
    alpha = [parse_q(value) for value in source["alpha"]]
    triples = [tuple(triple) for triple in source["triples"]]
    nu = [parse_q(value) for value in source["nu"]]
    check(
        grid
        == [
            Q(-1),
            Q(-3, 4),
            Q(-1, 2),
            Q(-1, 4),
            Q(0),
            Q(1, 4),
            Q(1, 2),
        ],
        "unexpected source grid",
    )
    check(len(alpha) == len(grid), "pair vector length mismatch")
    check(len(triples) == len(nu), "triple vector length mismatch")
    check(all(weight > 0 for weight in alpha + nu), "nonpositive source mass")
    check(sum(alpha) == 40, "pair mass is not 40")
    check(sum(nu) == 40 * 39, "triple mass is not 1560")

    for triple_index, triple in enumerate(triples):
        check(
            tuple(sorted(triple)) == triple,
            f"triple {triple_index} is not sorted",
        )
        u, v, t = (grid[index] for index in triple)
        check(
            1 + 2 * u * v * t - u * u - v * v - t * t >= 0,
            f"triple {triple_index} violates the Gram determinant",
        )
    for index in range(len(grid)):
        marginal = sum(
            weight * triple.count(index) / 3
            for triple, weight in zip(triples, nu)
        )
        check(
            marginal == 39 * alpha[index],
            f"fixed-cardinality marginal mismatch at grid index {index}",
        )

    # Check W_0 itself: it has the fixed-cardinality kernel, and the
    # complementary 7-by-7 principal submatrix is positive definite.
    extended_grid = grid + [Q(1)]
    w_zero = zero_matrix(len(extended_grid))
    w_zero[-1][-1] = Q(1)
    for index, weight in enumerate(alpha):
        w_zero[-1][index] += weight
        w_zero[index][-1] += weight
        w_zero[index][index] += weight
    for triple, weight in zip(triples, nu):
        values = tuple(grid[index] for index in triple)
        orbit = sorted(set(itertools.permutations(values)))
        for u, v, _t in orbit:
            w_zero[extended_grid.index(u)][extended_grid.index(v)] += (
                weight / len(orbit)
            )
    check(symmetric(w_zero), "W_0 is not symmetric")
    kernel = [Q(-1, 40)] * len(grid) + [Q(1)]
    check(
        all(
            sum(w_zero[i][j] * kernel[j] for j in range(len(w_zero)))
            == 0
            for i in range(len(w_zero))
        ),
        "W_0 fixed-cardinality kernel identity fails",
    )
    zero_reduced = [row[:-1] for row in w_zero[:-1]]
    zero_pivots = ldl_pivots(zero_reduced)
    check(
        all(pivot > 0 for pivot in zero_pivots),
        "W_0 reduced block is not positive definite",
    )

    # For k>0, the endpoint rows u=-1 and u=1 vanish.  Work on the six
    # interior support points and aggregate equal (area, displacement)
    # transverse kernels.
    active_grid = grid[1:]
    active_index = {value: index for index, value in enumerate(active_grid)}
    coefficient_matrices: dict[tuple[Q, Q], list[list[Q]]] = {}
    ordered_terms: list[tuple[int, int, Q, Q, Q, Q]] = []
    for triple, weight in zip(triples, nu):
        values = tuple(grid[index] for index in triple)
        orbit = sorted(set(itertools.permutations(values)))
        coefficient = weight / len(orbit)
        for u, v, t in orbit:
            if u not in active_index or v not in active_index:
                continue
            i, j = active_index[u], active_index[v]
            area = (1 - u * u) * (1 - v * v)
            displacement = t - u * v
            delta = area - displacement * displacement
            check(
                area > 0 and delta >= 0,
                "active transverse support violates its closed Gram domain",
            )
            key = (area, displacement)
            matrix = coefficient_matrices.setdefault(key, zero_matrix(6))
            matrix[i][j] += coefficient
            ordered_terms.append(
                (i, j, coefficient, area, displacement, delta)
            )
    check(
        all(symmetric(matrix) for matrix in coefficient_matrices.values()),
        "transverse coefficient matrix is not symmetric",
    )

    # Exact even/odd boundary limits and entrywise interior-tail bounds.
    limits = [zero_matrix(6), zero_matrix(6)]
    tail_bounds = [zero_matrix(6), zero_matrix(6)]
    for i, q in enumerate(active_grid):
        radial_factor = 1 - q * q
        limits[0][i][i] += alpha[i + 1]
        limits[1][i][i] += alpha[i + 1] * radial_factor
    for i, j, coefficient, area, displacement, delta in ordered_terms:
        if delta == 0:
            limits[0][i][j] += coefficient
            limits[1][i][j] += coefficient * displacement
        else:
            tail_bounds[0][i][j] += coefficient * ceil_sqrt_fraction(
                area / delta
            )
            tail_bounds[1][i][j] += coefficient * ceil_sqrt_fraction(
                area * area / delta
            )

    expected_limit_pivots = certificate["limit_ldl_pivots"]
    expected_inverse_norms = certificate["limit_inverse_infinity_norm"]
    expected_eigenvalue_bounds = certificate[
        "limit_eigenvalue_lower_bound"
    ]
    expected_tail_rows = certificate["interior_tail_row_sums"]
    expected_tail_constants = certificate["tail_constants"]

    tail_constants: list[Q] = []
    eigenvalue_lower_bounds: list[Q] = []
    for parity, name in enumerate(("even", "odd")):
        check(symmetric(limits[parity]), f"{name} limit matrix is not symmetric")
        check(
            symmetric(tail_bounds[parity]),
            f"{name} tail-bound matrix is not symmetric",
        )
        pivots = ldl_pivots(limits[parity])
        check(
            all(pivot > 0 for pivot in pivots),
            f"{name} limit matrix is not positive definite",
        )
        check(
            [str(value) for value in pivots] == expected_limit_pivots[name],
            f"{name} stored limit LDL pivots mismatch",
        )

        limit_inverse = inverse(limits[parity])
        inverse_infinity_norm = max(
            sum(abs(value) for value in row) for row in limit_inverse
        )
        check(
            str(inverse_infinity_norm) == expected_inverse_norms[name],
            f"{name} stored inverse infinity norm mismatch",
        )
        eigenvalue_lower_bound = 1 / inverse_infinity_norm
        eigenvalue_lower_bounds.append(eigenvalue_lower_bound)
        check(
            str(eigenvalue_lower_bound) == expected_eigenvalue_bounds[name],
            f"{name} stored eigenvalue lower bound mismatch",
        )

        tail_row_sums = [sum(row) for row in tail_bounds[parity]]
        check(
            [str(value) for value in tail_row_sums]
            == expected_tail_rows[name],
            f"{name} stored interior-tail row sums mismatch",
        )
        tail_constant = max(
            sum(
                abs(limit_inverse[i][h]) * tail_row_sums[h]
                for h in range(6)
            )
            for i in range(6)
        )
        tail_constants.append(tail_constant)
        check(
            str(tail_constant) == expected_tail_constants[name],
            f"{name} stored tail constant mismatch",
        )

    finite_check_through = certificate["finite_check_through"]
    analytic_tail_from = certificate["analytic_tail_from"]
    check(finite_check_through >= 1, "finite harmonic range is empty")
    check(
        analytic_tail_from == finite_check_through + 1,
        "finite and analytic harmonic ranges are not consecutive",
    )
    check(
        tail_constants[0] < analytic_tail_from,
        "even analytic tail threshold is insufficient",
    )
    check(
        tail_constants[1] < analytic_tail_from,
        "odd analytic tail threshold is insufficient",
    )

    # Exact finite verification.  Scaling row i by
    # (1-q_i^2)^floor(k/2) turns W_k into the following rational matrix.
    maximum_index = finite_check_through // 2
    sequences = {
        key: normalized_transverse_sequences(*key, maximum_index)
        for key in coefficient_matrices
    }
    minimum_pivot: tuple[Q, int, int] | None = None
    for k in range(1, finite_check_through + 1):
        parity = k % 2
        sequence_index = k // 2
        matrix = zero_matrix(6)
        for i, q in enumerate(active_grid):
            matrix[i][i] = alpha[i + 1]
            if parity:
                matrix[i][i] *= 1 - q * q
        for key, coefficient_matrix in coefficient_matrices.items():
            kernel_value = sequences[key][parity][sequence_index]
            for i in range(6):
                for j in range(6):
                    matrix[i][j] += (
                        coefficient_matrix[i][j] * kernel_value
                    )
        check(symmetric(matrix), f"degree-{k} matrix is not symmetric")
        pivots = ldl_pivots(matrix)
        check(
            all(pivot > 0 for pivot in pivots),
            f"degree-{k} matrix is not positive definite",
        )
        for pivot_index, pivot in enumerate(pivots):
            candidate = (pivot, k, pivot_index)
            if minimum_pivot is None or pivot < minimum_pivot[0]:
                minimum_pivot = candidate
    check(minimum_pivot is not None, "finite harmonic range produced no pivot")
    # The preceding check narrows the type for human readers and static tools.
    if minimum_pivot is None:
        raise VerificationError("unreachable missing finite harmonic pivot")
    expected_minimum = certificate["minimum_finite_ldl_pivot"]
    check(
        minimum_pivot[1] == expected_minimum["harmonic_degree"],
        "stored minimum harmonic-pivot degree mismatch",
    )
    check(
        minimum_pivot[2] == expected_minimum["pivot_index"],
        "stored minimum harmonic-pivot index mismatch",
    )
    check(
        str(minimum_pivot[0]) == expected_minimum["value"],
        "stored minimum harmonic-pivot value mismatch",
    )

    # Ordinary two-point moments at every degree.  The atom at -1 is
    # separated exactly; the remaining six atoms obey the analytic
    # dimension-five Gegenbauer tail estimate documented in the proof.
    pair_finite_through = certificate["pair_moment_finite_check_through"]
    pair_tail_from = certificate["pair_analytic_tail_from"]
    check(pair_finite_through >= 1, "finite pair-moment range is empty")
    check(
        pair_tail_from == pair_finite_through + 1,
        "finite and analytic pair-moment ranges are not consecutive",
    )
    sequences_5 = [
        gegenbauer_5_sequence(q, pair_finite_through) for q in grid
    ]
    minimum_pair_moment: tuple[Q, int] | None = None
    for k in range(1, pair_finite_through + 1):
        moment = 1 + sum(
            alpha[i] * sequences_5[i][k] for i in range(len(grid))
        )
        check(moment > 0, f"pair moment is nonpositive at degree {k}")
        candidate = (moment, k)
        if minimum_pair_moment is None or moment < minimum_pair_moment[0]:
            minimum_pair_moment = candidate
    check(
        minimum_pair_moment is not None,
        "finite pair-moment range produced no moment",
    )
    if minimum_pair_moment is None:
        raise VerificationError("unreachable missing finite pair moment")
    expected_pair_minimum = certificate["minimum_finite_pair_moment"]
    check(
        minimum_pair_moment[1] == expected_pair_minimum["degree"],
        "stored minimum pair-moment degree mismatch",
    )
    check(
        str(minimum_pair_moment[0]) == expected_pair_minimum["value"],
        "stored minimum pair-moment value mismatch",
    )

    inverse_three_halves_bounds = [
        parse_q(value)
        for value in certificate[
            "pair_interior_inverse_three_halves_bounds"
        ]
    ]
    check(
        len(inverse_three_halves_bounds) == len(active_grid),
        "wrong number of inverse-three-halves bounds",
    )
    for index, (t, upper) in enumerate(
        zip(active_grid, inverse_three_halves_bounds, strict=True)
    ):
        q = 1 - t * t
        check(
            upper > 0 and upper**2 * q**3 >= 1,
            f"inverse-three-halves bound fails at active index {index}",
        )
    weighted_pair_bound = sum(
        alpha[i + 1] * inverse_three_halves_bounds[i]
        for i in range(len(active_grid))
    )
    check(
        str(weighted_pair_bound) == certificate["pair_weighted_tail_bound"],
        "stored weighted pair-tail bound mismatch",
    )
    endpoint_margin = 1 - alpha[0]
    check(
        str(endpoint_margin) == certificate["pair_endpoint_margin"],
        "stored pair endpoint margin mismatch",
    )

    # pi<22/7 and sqrt(2*pi)<251/100 imply the analytic constant is <31/5.
    check(
        Q(44, 7) < Q(251, 100) ** 2,
        "rational sqrt(2*pi) comparison fails",
    )
    analytic_constant_upper = Q(22, 7) ** 2 * Q(251, 100) / 4
    check(
        analytic_constant_upper < Q(31, 5),
        "rational analytic Gegenbauer constant is too large",
    )
    normalized_pair_tail = (
        Q(31, 5) * weighted_pair_bound / endpoint_margin
    )
    check(
        str(normalized_pair_tail)
        == certificate["normalized_pair_tail_constant"],
        "stored normalized pair-tail constant mismatch",
    )
    check(
        normalized_pair_tail**2 < pair_tail_from**3,
        "analytic pair-tail threshold is insufficient",
    )

    return {
        "status": "PASS",
        "source_sha256": source_sha256,
        "w0_rank": 7,
        "finite_harmonic_check": f"1..{finite_check_through}",
        "analytic_harmonic_tail": f"k>={analytic_tail_from}",
        "minimum_finite_ldl_pivot": str(minimum_pivot[0]),
        "minimum_finite_ldl_pivot_degree": minimum_pivot[1],
        "even_limit_eigenvalue_lower_bound": str(
            eigenvalue_lower_bounds[0]
        ),
        "odd_limit_eigenvalue_lower_bound": str(
            eigenvalue_lower_bounds[1]
        ),
        "pair_moment_finite_check": f"1..{pair_finite_through}",
        "pair_moment_analytic_tail": f"k>={pair_tail_from}",
        "minimum_finite_pair_moment": str(minimum_pair_moment[0]),
        "minimum_finite_pair_moment_degree": minimum_pair_moment[1],
        "conclusion": "W_k is PSD for every k>=0",
    }


def main() -> None:
    project_root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "source",
        nargs="?",
        type=Path,
        default=(
            project_root
            / "certificates"
            / "fixed41_bv_fullradial_k16_pseudodistribution.json"
        ),
    )
    parser.add_argument(
        "--all-harmonics-certificate",
        type=Path,
        default=(
            project_root
            / "certificates"
            / "fixed41_bv_all_harmonics_certificate.json"
        ),
    )
    args = parser.parse_args()
    print(
        json.dumps(
            verify(args.source, args.all_harmonics_certificate),
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
