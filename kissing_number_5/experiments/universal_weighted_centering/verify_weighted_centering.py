#!/usr/bin/env python3
"""Exact audit of weighted-centering identities and D5 counterexamples."""

from __future__ import annotations

from fractions import Fraction as Q
import hashlib
import itertools
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
CERTIFICATE = HERE / "weighted_centering_counterexamples.json"
DELETION_DEPTH_CERTIFICATE = (
    HERE / "deletion_depth_weight_counterexample.json"
)
DEPTH_CERTIFICATE = (
    ROOT / "certificates" / "positive_circuit_pair_catalog.json"
)


def roots_d5() -> list[tuple[int, ...]]:
    roots = []
    for first, second in itertools.combinations(range(5), 2):
        for first_sign, second_sign in itertools.product(
            (-1, 1), repeat=2
        ):
            root = [0] * 5
            root[first] = first_sign
            root[second] = second_sign
            roots.append(tuple(root))
    return roots


def zero_matrix(rows: int, columns: int | None = None) -> list[list[Q]]:
    if columns is None:
        columns = rows
    return [[Q(0) for _ in range(columns)] for _ in range(rows)]


def matrix_vector(
    matrix: list[list[Q]], vector: list[Q]
) -> list[Q]:
    return [
        sum(entry * value for entry, value in zip(row, vector))
        for row in matrix
    ]


def matrix_rank(matrix: list[list[Q]]) -> int:
    work = [row[:] for row in matrix]
    if not work:
        return 0
    row_count = len(work)
    column_count = len(work[0])
    rank = 0
    for column in range(column_count):
        pivot = next(
            (
                row
                for row in range(rank, row_count)
                if work[row][column] != 0
            ),
            None,
        )
        if pivot is None:
            continue
        work[rank], work[pivot] = work[pivot], work[rank]
        pivot_value = work[rank][column]
        work[rank] = [
            value / pivot_value for value in work[rank]
        ]
        for row in range(row_count):
            if row == rank:
                continue
            multiplier = work[row][column]
            if multiplier:
                work[row] = [
                    value - multiplier * pivot_entry
                    for value, pivot_entry in zip(
                        work[row], work[rank]
                    )
                ]
        rank += 1
        if rank == row_count:
            break
    return rank


def gram(roots: list[tuple[int, ...]]) -> list[list[Q]]:
    return [
        [
            Q(sum(a * b for a, b in zip(first, second)), 2)
            for second in roots
        ]
        for first in roots
    ]


def covariance(
    roots: list[tuple[int, ...]], weights: list[Q]
) -> list[list[Q]]:
    answer = zero_matrix(5)
    for weight, root in zip(weights, roots):
        for i in range(5):
            for j in range(5):
                answer[i][j] += Q(weight * root[i] * root[j], 2)
    return answer


def verify_weight_family(
    roots: list[tuple[int, ...]],
    gram_matrix: list[list[Q]],
    weights: list[Q],
) -> dict[str, object]:
    count = len(roots)
    assert len(weights) == count
    assert all(weight >= 0 for weight in weights)
    assert sum(weights) == 1
    assert all(
        sum(weight * root[coordinate] for weight, root in zip(weights, roots))
        == 0
        for coordinate in range(5)
    )
    assert matrix_vector(gram_matrix, weights) == [Q(0)] * count

    lorentzian = zero_matrix(count)
    for i in range(count):
        for j in range(count):
            lorentzian[i][j] = (
                Q(i == j) + 1 - 2 * gram_matrix[i][j]
            )
    assert all(lorentzian[i][i] == 0 for i in range(count))
    assert all(
        0 <= lorentzian[i][j] <= 3
        for i in range(count)
        for j in range(count)
    )
    assert matrix_vector(lorentzian, weights) == [
        1 + weight for weight in weights
    ]

    frame = covariance(roots, weights)
    leverage = [
        sum(
            weights[j] * gram_matrix[i][j] ** 2
            for j in range(count)
        )
        for i in range(count)
    ]
    quadratic = zero_matrix(count)
    for i in range(count):
        for j in range(count):
            if i != j:
                entry = lorentzian[i][j]
                quadratic[i][j] = entry * (3 - entry)
    quadratic_times_weights = matrix_vector(quadratic, weights)
    assert quadratic_times_weights == [
        2 + 4 * weights[i] - 4 * leverage[i]
        for i in range(count)
    ]
    for weight, value in zip(weights, leverage):
        if weight == 1:
            continue
        assert value >= weight / (1 - weight)
        assert value <= weight + Q(1, 2)

    # The rational reversible Markov kernel associated with Bp=1+p.
    transition = [
        [
            lorentzian[i][j] * weights[j] / (1 + weights[i])
            for j in range(count)
        ]
        for i in range(count)
    ]
    assert matrix_vector(transition, [Q(1)] * count) == [Q(1)] * count
    stationary_unnormalized = [
        weight * (1 + weight) for weight in weights
    ]
    for i in range(count):
        for j in range(count):
            assert (
                stationary_unnormalized[i] * transition[i][j]
                == stationary_unnormalized[j] * transition[j][i]
            )

    a = [weight / (1 + weight) for weight in weights]
    trace_s_squared = sum(
        a[i] * a[j] * lorentzian[i][j] ** 2
        for i in range(count)
        for j in range(count)
    )
    second_weight_moment = sum(weight * weight for weight in weights)
    maximum_weight = max(weights)
    a_sum = sum(a)
    a_square_sum = sum(value * value for value in a)
    positive_eigenvalue_lower = 1 / (1 + second_weight_moment)
    lorentzian_lower = (
        positive_eigenvalue_lower**2
        + (positive_eigenvalue_lower + a_sum) ** 2 / 5
        - a_square_sum
    )
    lorentzian_upper = 3 * (
        1 - second_weight_moment / (1 + maximum_weight)
    )
    assert trace_s_squared >= lorentzian_lower
    assert trace_s_squared <= lorentzian_upper

    return {
        "positive_weights": sum(weight > 0 for weight in weights),
        "minimum_weight": str(min(weights)),
        "maximum_weight": str(max(weights)),
        "covariance_rank": matrix_rank(frame),
        "normalized_lorentzian_trace_square": str(trace_s_squared),
        "rank_inertia_lower_bound": str(lorentzian_lower),
        "entrywise_upper_bound": str(lorentzian_upper),
    }


def verify_deletion_depth_counterexample(
    certificate_path: Path,
) -> dict[str, object]:
    certificate = json.loads(certificate_path.read_text())
    assert certificate["schema"] == (
        "deletion-six-balanced-weight-counterexample-v1"
    )
    assert certificate["status"] == (
        "EXACT PARAMETRIC COUNTEREXAMPLE TO DEPTH-ONLY WEIGHT BALANCE"
    )
    assert certificate["ambient_dimension"] == 5
    assert certificate["cardinality"] == 41

    epsilon = Q(certificate["parameter_epsilon"])
    assert 0 < epsilon < 1
    denominator = certificate["moment_curve_parameters"]["denominator"]
    numerators = certificate["moment_curve_parameters"]["numerators"]
    parameters = [Q(numerator, denominator) for numerator in numerators]
    assert len(parameters) == 20
    assert len(set(parameters)) == 20
    assert all(-1 <= parameter <= 1 for parameter in parameters)

    # The five-by-five determinant for parameters t_1,...,t_5 is epsilon
    # times their Vandermonde determinant.  Thus every five of the twenty
    # projective lines span R^5.
    minimum_absolute_vandermonde = None
    for selection in itertools.combinations(parameters, 5):
        determinant = epsilon
        for i in range(5):
            for j in range(i + 1, 5):
                determinant *= selection[j] - selection[i]
        assert determinant
        absolute = abs(determinant)
        if (
            minimum_absolute_vandermonde is None
            or absolute < minimum_absolute_vandermonde
        ):
            minimum_absolute_vandermonde = absolute
    assert minimum_absolute_vandermonde is not None

    def raw(parameter: Q) -> tuple[Q, Q, Q, Q, Q]:
        return (
            Q(1),
            parameter,
            parameter**2,
            parameter**3,
            epsilon * parameter**4,
        )

    raw_vectors = [raw(parameter) for parameter in parameters]
    norm_squares = [
        sum(coordinate * coordinate for coordinate in vector)
        for vector in raw_vectors
    ]
    assert all(norm_square > 0 for norm_square in norm_squares)
    assert all(
        vector[4] ** 2 <= epsilon**2 * norm_square
        for vector, norm_square in zip(raw_vectors, norm_squares)
    )

    # A hyperplane contains at most four of the projective lines.  Every
    # other antipodal pair contributes one point to either open hemisphere.
    open_hemisphere_minimum = len(parameters) - 4
    assert open_hemisphere_minimum == certificate[
        "minimum_open_hemisphere_count_from_antipodal_pairs"
    ] == 16

    deletion_count = certificate["robust_deletion_count"]
    intact_pairs_after_deletion = len(parameters) - deletion_count
    assert deletion_count == 6
    assert intact_pairs_after_deletion == 14 >= 5

    # The forty antipodal points cancel, so the unweighted centroid of the
    # 41-point configuration is e_5.  Every point other than e_5 has fifth
    # coordinate at least -epsilon.  Hence the radial reach opposite the
    # centroid is at most epsilon, and the exact max-min formula gives
    # mu*=rho/(1+41 rho) <= epsilon.
    radial_reach_upper = epsilon
    max_min_weight_upper = epsilon
    assert certificate[
        "radial_reach_upper_bound_opposite_centroid"
    ] == "epsilon"
    assert certificate[
        "max_min_barycentric_weight_upper_bound"
    ] == "epsilon"

    # This depth construction is deliberately not a kissing code.  The
    # first two normalized moment-curve points already have inner product
    # strictly larger than 1/2; verify it without square roots.
    first = raw_vectors[0]
    second = raw_vectors[1]
    dot_product = sum(a * b for a, b in zip(first, second))
    assert dot_product > 0
    assert 4 * dot_product**2 > norm_squares[0] * norm_squares[1]

    return {
        "status": "PASS",
        "parameter_epsilon": str(epsilon),
        "projective_lines": len(parameters),
        "minimum_open_hemisphere_count": open_hemisphere_minimum,
        "intact_pairs_after_six_deletions": intact_pairs_after_deletion,
        "radial_reach_upper_bound": str(radial_reach_upper),
        "max_min_weight_upper_bound": str(max_min_weight_upper),
        "minimum_absolute_vandermonde": str(
            minimum_absolute_vandermonde
        ),
        "explicit_pair_is_not_kissing": True,
        "scope": certificate["scope_warning"],
    }


def verify(
    certificate_path: Path = CERTIFICATE,
    depth_certificate_path: Path = DEPTH_CERTIFICATE,
    deletion_depth_certificate_path: Path = DELETION_DEPTH_CERTIFICATE,
) -> dict[str, object]:
    certificate = json.loads(certificate_path.read_text())
    depth_bytes = depth_certificate_path.read_bytes()
    depth_certificate = json.loads(depth_bytes)
    assert certificate["schema"] == (
        "universal-weighted-centering-counterexamples-v1"
    )
    assert certificate["status"] == (
        "EXACT D5 WEIGHT-SELECTION COUNTEREXAMPLES"
    )
    assert certificate["ambient_dimension"] == 5
    assert certificate["code_cardinality"] == 40
    assert certificate["root_normalization_squared"] == "2"
    assert certificate["imported_depth_certificate"] == (
        depth_certificate_path.name
    )
    assert certificate["imported_depth_certificate_sha256"] == (
        hashlib.sha256(depth_bytes).hexdigest()
    )
    assert depth_certificate["d5_open_origin_hemisphere_minimum"] == 8
    assert certificate["imported_open_hemisphere_minimum"] == 8

    roots = roots_d5()
    assert len(roots) == 40
    distinguished = tuple(
        certificate["distinguished_unnormalized_root"]
    )
    assert roots[0] == distinguished
    antipode = tuple(-entry for entry in distinguished)
    antipode_index = roots.index(antipode)
    assert antipode_index != 0

    gram_matrix = gram(roots)
    assert all(gram_matrix[i][i] == 1 for i in range(40))
    assert max(
        gram_matrix[i][j]
        for i in range(40)
        for j in range(i)
    ) == Q(1, 2)
    assert matrix_rank(gram_matrix) == 5

    lorentzian = [
        [
            Q(i == j) + 1 - 2 * gram_matrix[i][j]
            for j in range(40)
        ]
        for i in range(40)
    ]
    assert matrix_rank(
        [
            [lorentzian[i][j] - Q(i == j) for j in range(40)]
            for i in range(40)
        ]
    ) <= 6
    quadratic = [
        [
            (
                lorentzian[i][j] * (3 - lorentzian[i][j])
                if i != j
                else Q(0)
            )
            for j in range(40)
        ]
        for i in range(40)
    ]
    harmonic_two = [
        [
            (5 * gram_matrix[i][j] ** 2 - 1) / 4
            for j in range(40)
        ]
        for i in range(40)
    ]
    quadratic_shift = [
        [quadratic[i][j] - 4 * Q(i == j) for j in range(40)]
        for i in range(40)
    ]
    expected_quadratic_shift = [
        [
            Q(6, 5)
            - 2 * gram_matrix[i][j]
            - Q(16, 5) * harmonic_two[i][j]
            for j in range(40)
        ]
        for i in range(40)
    ]
    assert quadratic_shift == expected_quadratic_shift
    assert matrix_rank(quadratic_shift) <= 20

    # D5 is a unit-norm tight frame: sum_x x x^T = 8 I.
    unweighted_frame = covariance(roots, [Q(1)] * 40)
    assert unweighted_frame == [
        [Q(8) if i == j else Q(0) for j in range(5)]
        for i in range(5)
    ]

    epsilon = Q(certificate["epsilon"])
    assert 0 < epsilon < 1
    distinguished_pair = {0, antipode_index}

    ill_conditioned = [
        (
            (1 - epsilon) / 2
            if index in distinguished_pair
            else epsilon / 38
        )
        for index in range(40)
    ]
    ill_report = verify_weight_family(
        roots, gram_matrix, ill_conditioned
    )
    ill_frame = covariance(roots, ill_conditioned)
    unit_line_projection = [
        [Q(distinguished[i] * distinguished[j], 2) for j in range(5)]
        for i in range(5)
    ]
    perpendicular_eigenvalue = 4 * epsilon / 19
    parallel_eigenvalue = 1 - 16 * epsilon / 19
    expected_frame = [
        [
            perpendicular_eigenvalue * Q(i == j)
            + (parallel_eigenvalue - perpendicular_eigenvalue)
            * unit_line_projection[i][j]
            for j in range(5)
        ]
        for i in range(5)
    ]
    assert ill_frame == expected_frame
    assert ill_report["covariance_rank"] == 5

    small_weight = [
        (
            epsilon / 2
            if index in distinguished_pair
            else (1 - epsilon) / 38
        )
        for index in range(40)
    ]
    small_report = verify_weight_family(
        roots, gram_matrix, small_weight
    )
    assert Q(small_report["minimum_weight"]) == epsilon / 2

    two_point = [
        Q(1, 2) if index in distinguished_pair else Q(0)
        for index in range(40)
    ]
    two_point_report = verify_weight_family(
        roots, gram_matrix, two_point
    )
    assert two_point_report["positive_weights"] == 2
    assert two_point_report["covariance_rank"] == 1
    deletion_depth_report = verify_deletion_depth_counterexample(
        deletion_depth_certificate_path
    )

    return {
        "status": "PASS",
        "scope": (
            "exact counterexamples to properties of an arbitrary "
            "centering-weight choice; not counterexamples to optimized "
            "weight-selection claims"
        ),
        "d5_open_hemisphere_depth": 8,
        "small_weight_family": small_report,
        "ill_conditioned_family": {
            **ill_report,
            "parallel_covariance_eigenvalue": str(
                parallel_eigenvalue
            ),
            "orthogonal_covariance_eigenvalue": str(
                perpendicular_eigenvalue
            ),
        },
        "two_point_family": two_point_report,
        "deletion_depth_only_counterexample": deletion_depth_report,
        "conclusion": (
            "depth alone neither makes every positive barycentric choice "
            "well-conditioned nor supplies a quantitative lower bound "
            "without using the kissing inequalities"
        ),
    }


def main() -> None:
    print(json.dumps(verify(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
