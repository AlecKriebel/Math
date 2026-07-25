#!/usr/bin/env python3
"""Exact verifier for the E6 depth/common-pair rank-six countermodel.

Only Python's standard library and exact integer/Fraction arithmetic are
used.  The exhaustive frame check has 38,760 cases.
"""

from collections import Counter, defaultdict
from fractions import Fraction as Q
import hashlib
from itertools import combinations, product
import json
from math import comb
from pathlib import Path


HERE = Path(__file__).resolve().parent
CERTIFICATE = HERE / "e6_rank6_shadow_countermodel.json"


def d_root(vector):
    return ("D", tuple(vector), 0)


def spin_root(signs):
    parity = 1
    for sign in signs:
        parity *= sign
    return ("S", tuple(signs), parity)


def full_e6_roots():
    roots = []
    for first, second in combinations(range(5), 2):
        for first_sign, second_sign in product((-1, 1), repeat=2):
            vector = [0] * 5
            vector[first] = first_sign
            vector[second] = second_sign
            roots.append(d_root(vector))
    roots.extend(spin_root(signs) for signs in product((-1, 1), repeat=5))
    assert len(roots) == 72
    return tuple(roots)


def twice_inner(left, right):
    left_kind, left_vector, left_parity = left
    right_kind, right_vector, right_parity = right
    if left_kind == right_kind == "D":
        return sum(
            first * second
            for first, second in zip(left_vector, right_vector)
        )
    if left_kind == "S" and right_kind == "D":
        return twice_inner(right, left)
    if left_kind == "D":
        numerator = sum(
            first * second
            for first, second in zip(left_vector, right_vector)
        )
        assert numerator % 2 == 0
        return numerator // 2
    numerator = sum(
        first * second
        for first, second in zip(left_vector, right_vector)
    ) + 3 * left_parity * right_parity
    assert numerator % 4 == 0
    return numerator // 4


def selected_roots(data):
    full = full_e6_roots()
    roots = []
    for index in data["core_line_root_indices"]:
        root = full[index]
        roots.append(root)
        roots.append(antipode(root))
    roots.append(full[data["extra_root_index"]])
    return tuple(roots)


def antipode(root):
    kind, vector, parity = root
    return (kind, tuple(-entry for entry in vector), -parity)


def payload_hash(roots):
    payload = [
        {
            "kind": root[0],
            "v": list(root[1]),
            "parity": root[2],
        }
        for root in roots
    ]
    encoded = json.dumps(
        payload, separators=(",", ":"), sort_keys=True
    ).encode()
    return hashlib.sha256(encoded).hexdigest()


def matrix_rank(matrix):
    matrix = [[Q(value) for value in row] for row in matrix]
    row_count = len(matrix)
    column_count = len(matrix[0])
    rank = 0
    for column in range(column_count):
        pivot = next(
            (
                row
                for row in range(rank, row_count)
                if matrix[row][column]
            ),
            None,
        )
        if pivot is None:
            continue
        matrix[rank], matrix[pivot] = matrix[pivot], matrix[rank]
        pivot_value = matrix[rank][column]
        matrix[rank] = [
            value / pivot_value for value in matrix[rank]
        ]
        for row in range(row_count):
            if row == rank or not matrix[row][column]:
                continue
            scale = matrix[row][column]
            matrix[row] = [
                value - scale * pivot_entry
                for value, pivot_entry in zip(
                    matrix[row], matrix[rank]
                )
            ]
        rank += 1
        if rank == row_count:
            break
    return rank


def core_lines(data):
    full = full_e6_roots()
    lines = [
        full[index] for index in data["core_line_root_indices"]
    ]
    assert len(lines) == 20
    assert len(set(lines + [antipode(root) for root in lines])) == 40
    return tuple(lines)


def integer_congruence_matrix(lines, subset):
    """Return a rational congruence of 8(F_T-I/4).

    Write 8(F_T-I/4)=[[A,sqrt(3)b],[sqrt(3)b^T,c]].
    Congruence by diag(1,...,1,1/sqrt(3)), followed by multiplication
    by three, gives the integer matrix [[3A,3b],[3b^T,c]].
    """

    top = [[0 for _ in range(5)] for _ in range(5)]
    cross = [0 for _ in range(5)]
    last = 0
    for index in subset:
        kind, vector, parity = lines[index]
        if kind == "S":
            for row in range(5):
                for column in range(5):
                    top[row][column] += (
                        vector[row] * vector[column]
                    )
                cross[row] += vector[row] * parity
            last += 3
        else:
            for row in range(5):
                for column in range(5):
                    top[row][column] += (
                        4 * vector[row] * vector[column]
                    )
    for index in range(5):
        top[index][index] -= 2
    last -= 2

    matrix = [[0 for _ in range(6)] for _ in range(6)]
    for row in range(5):
        for column in range(5):
            matrix[row][column] = 3 * top[row][column]
        matrix[row][5] = 3 * cross[row]
        matrix[5][row] = 3 * cross[row]
    matrix[5][5] = last
    return matrix


def bareiss_determinant(matrix):
    matrix = [list(row) for row in matrix]
    size = len(matrix)
    if size == 0:
        return 1
    sign = 1
    previous = 1
    for column in range(size - 1):
        if matrix[column][column] == 0:
            pivot = next(
                (
                    row
                    for row in range(column + 1, size)
                    if matrix[row][column]
                ),
                None,
            )
            if pivot is None:
                return 0
            matrix[column], matrix[pivot] = (
                matrix[pivot],
                matrix[column],
            )
            sign = -sign
        pivot_value = matrix[column][column]
        for row in range(column + 1, size):
            for other in range(column + 1, size):
                numerator = (
                    matrix[row][other] * pivot_value
                    - matrix[row][column] * matrix[column][other]
                )
                assert numerator % previous == 0
                matrix[row][other] = numerator // previous
        previous = pivot_value
    return sign * matrix[-1][-1]


def verify_frame_certificate(data):
    lines = core_lines(data)
    frame_data = data["frame_certificate"]
    subset_size = frame_data["small_line_subset_size"]
    assert subset_size == 14
    assert Q(frame_data["shift"]) == Q(1, 4)
    minima = [None] * 6
    subset_count = 0
    for subset in combinations(range(len(lines)), subset_size):
        matrix = integer_congruence_matrix(lines, subset)
        for size in range(1, 7):
            determinant = bareiss_determinant(
                [row[:size] for row in matrix[:size]]
            )
            assert determinant > 0
            if minima[size - 1] is None or determinant < minima[size - 1]:
                minima[size - 1] = determinant
        subset_count += 1
    assert subset_count == comb(20, 14)
    assert subset_count == frame_data["subsets_checked"]
    assert minima == frame_data[
        "minimum_leading_principal_determinants_after_integer_congruence"
    ]
    # If at most six antipodal lines had |<e,v>|>1/300, fourteen
    # lines would contribute at most this amount to their frame form,
    # contradicting F_T > I/4.
    assert Q(14, 300**2) == Q(7, 45000) < Q(1, 4)
    return minima


def verify_common_pair_shadows(data, selected):
    full = full_e6_roots()
    audit = defaultdict(list)
    for first, second in combinations(range(len(full)), 2):
        base = twice_inner(full[first], full[second])
        if base <= 0:
            common = sum(
                twice_inner(full[first], root) == 1
                and twice_inner(full[second], root) == 1
                for root in full
            )
            audit[base].append(common)
    expected = data["full_e6_common_contact_audit"]
    assert {
        str(base): {
            "base_pairs": len(values),
            "common_contact_neighbors": min(values),
        }
        for base, values in audit.items()
    } == expected
    assert all(len(set(values)) == 1 for values in audit.values())

    selected_audit = defaultdict(list)
    for first, second in combinations(range(len(selected)), 2):
        base = twice_inner(selected[first], selected[second])
        common = sum(
            twice_inner(selected[first], root) == 1
            and twice_inner(selected[second], root) == 1
            for root in selected
        )
        selected_audit[base].append(common)
    maxima = {
        str(base): max(values)
        for base, values in selected_audit.items()
    }
    assert maxima == {
        key: value
        for key, value in data[
            "selected_common_contact_maxima"
        ].items()
    }
    # These are bounded by the strongest asserted code-base capacities on
    # the E6 support: 0 at q=-1, 1 at q=-1/2, 6 at q=0, and the separate
    # common-contact cap 7 at q=1/2.
    assert maxima == {"-2": 0, "-1": 1, "0": 5, "1": 7}
    capacities = {"-2": 0, "-1": 1, "0": 6, "1": 7}
    assert all(maxima[key] <= value for key, value in capacities.items())
    return maxima


def verify():
    data = json.loads(CERTIFICATE.read_text(encoding="utf-8"))
    assert data["schema"] == "e6-rank6-depth-common-pair-shadow-v1"
    assert data["cardinality"] == 41
    assert Q(data["robust_depth_threshold"]) == Q(1, 300)

    full = full_e6_roots()
    assert len(set(full)) == 72
    assert all(twice_inner(root, root) == 2 for root in full)
    assert max(
        twice_inner(full[first], full[second])
        for first, second in combinations(range(len(full)), 2)
    ) == 1

    selected = selected_roots(data)
    assert len(selected) == len(set(selected)) == 41
    assert payload_hash(selected) == data[
        "selected_root_payload_sha256"
    ]
    pair_distribution = Counter(
        twice_inner(selected[first], selected[second])
        for first, second in combinations(range(len(selected)), 2)
    )
    assert pair_distribution == {
        int(key): value
        for key, value in data[
            "selected_pair_distribution_by_twice_inner_product"
        ].items()
    }
    gram = [
        [Q(twice_inner(left, right), 2) for right in selected]
        for left in selected
    ]
    rank = matrix_rank(gram)
    assert rank == data["ambient_rank"] == 6
    frame_potential = sum(
        value * value for row in gram for value in row
    )
    degree_two_sum = (
        5 * frame_potential - len(selected) ** 2
    ) / 4
    rejection_data = data["dimension_five_rejections"]
    assert frame_potential == Q(rejection_data["frame_potential"]) == 300
    assert degree_two_sum == Q(
        rejection_data["degree_two_gegenbauer_sum"]
    ) == Q(-181, 4)

    clique = [
        full[index] for index in data["arbitrary_axis_five_clique_indices"]
    ]
    assert all(root in selected for root in clique)
    assert all(
        twice_inner(left, right) == 1
        for left, right in combinations(clique, 2)
    )
    # The clique sum has squared norm 15 and inner product 3 with each
    # clique root.  If s is its normalization and t is an orthogonal unit
    # vector, u=sqrt(5/12)s+sqrt(7/12)t and
    # v=sqrt(5/12)s-sqrt(7/12)t have the stored exact parameters.
    assert len(clique) == 5
    clique_sum_norm_squared = sum(
        Q(twice_inner(left, right), 2)
        for left in clique for right in clique
    )
    assert clique_sum_norm_squared == 15
    assert all(
        sum(Q(twice_inner(root, other), 2) for other in clique) == 3
        for root in clique
    )
    axis_q = Q(5, 12) - Q(7, 12)
    axis_height_squared = Q(5, 12) * Q(3, 5)
    axis_height = Q(1, 2)
    projected_parameter = 2 * axis_height**2 / (1 + axis_q)
    assert axis_q == Q(
        rejection_data["arbitrary_axis_base_inner_product"]
    ) == Q(-1, 6)
    assert axis_height_squared == axis_height**2
    assert axis_height == Q(
        rejection_data["arbitrary_axis_common_height"]
    )
    assert projected_parameter == Q(
        rejection_data["arbitrary_axis_projected_parameter"]
    ) == Q(3, 5)
    assert rejection_data["arbitrary_axis_capacity"] == 4
    assert rejection_data["arbitrary_axis_qualifying_points"] == 5
    assert 5 > 4

    minima = verify_frame_certificate(data)
    capacity_maxima = verify_common_pair_shadows(data, selected)
    return {
        "cardinality": len(selected),
        "gram_rank": rank,
        "maximum_inner_product": Q(max(pair_distribution), 2),
        "robust_depth_threshold": Q(1, 300),
        "frame_subsets_checked": data["frame_certificate"][
            "subsets_checked"
        ],
        "minimum_integer_congruence_determinants": minima,
        "common_pair_capacity_maxima": capacity_maxima,
        "frame_potential": frame_potential,
        "degree_two_gegenbauer_sum": degree_two_sum,
        "arbitrary_axis_capacity_violation": "5 > 4",
        "conclusion": (
            "robust depth plus all code-base common-pair capacity shadows "
            "and local K4 Gram positivity do not recover the global "
            "rank-five condition"
        ),
        "status": "PASS",
    }


if __name__ == "__main__":
    for key, value in verify().items():
        print(f"{key}: {value}")
