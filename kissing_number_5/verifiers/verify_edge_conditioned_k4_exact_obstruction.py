#!/usr/bin/env python3
"""Exact verifier for the edge-conditioned K4 obstruction.

Only standard-library rational arithmetic is used.  The program rebuilds
all feasible triangle types, all Gram-PSD colored K4 orbits, their face
incidences, and all 75 coordinate covariance rows.  It then checks the
one-row exact Farkas contradiction and the independent geometric lemma.
"""

from collections import Counter
from fractions import Fraction as Q
import hashlib
from itertools import combinations_with_replacement, permutations, product
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CERTIFICATE = (
    ROOT / "certificates" / "edge_conditioned_k4_exact_obstruction.json"
)
VERTICES = tuple(range(4))
EDGES = ((0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3))
EDGE_INDEX = {edge: index for index, edge in enumerate(EDGES)}
VERTEX_PERMUTATIONS = tuple(permutations(VERTICES))


def sha256_file(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def digest(payload):
    encoded = json.dumps(
        payload, separators=(",", ":"), sort_keys=False
    ).encode()
    return hashlib.sha256(encoded).hexdigest()


def determinant(matrix):
    work = [list(row) for row in matrix]
    answer = Q(1)
    for column in range(len(work)):
        pivot = next(
            (
                row
                for row in range(column, len(work))
                if work[row][column]
            ),
            None,
        )
        if pivot is None:
            return Q(0)
        if pivot != column:
            work[column], work[pivot] = work[pivot], work[column]
            answer = -answer
        pivot_value = work[column][column]
        answer *= pivot_value
        for row in range(column + 1, len(work)):
            scale = work[row][column] / pivot_value
            for other in range(column + 1, len(work)):
                work[row][other] -= scale * work[column][other]
    return answer


def transform(pattern, permutation):
    transformed = []
    for first, second in EDGES:
        image = tuple(sorted((permutation[first], permutation[second])))
        transformed.append(pattern[EDGE_INDEX[image]])
    return tuple(transformed)


def orbit(pattern):
    return tuple(sorted({
        transform(pattern, permutation)
        for permutation in VERTEX_PERMUTATIONS
    }))


def canonical(pattern):
    return orbit(pattern)[0]


def triangle_faces(pattern):
    answer = []
    for first, second, third in (
        (0, 1, 2),
        (0, 1, 3),
        (0, 2, 3),
        (1, 2, 3),
    ):
        answer.append(tuple(sorted((
            pattern[EDGE_INDEX[tuple(sorted((first, second)))]],
            pattern[EDGE_INDEX[tuple(sorted((first, third)))]],
            pattern[EDGE_INDEX[tuple(sorted((second, third)))]],
        ))))
    return tuple(answer)


def gram_matrix(pattern, nodes):
    matrix = [
        [Q(int(first == second)) for second in VERTICES]
        for first in VERTICES
    ]
    for color, (first, second) in zip(pattern, EDGES):
        matrix[first][second] = nodes[color]
        matrix[second][first] = nodes[color]
    return matrix


def feasible_triangle_types(nodes):
    answer = []
    for triple in combinations_with_replacement(range(len(nodes)), 3):
        u, v, t = (nodes[index] for index in triple)
        if 1 + 2 * u * v * t - u**2 - v**2 - t**2 >= 0:
            answer.append(triple)
    return tuple(answer)


def feasible_four_types(nodes, triangle_types):
    triangle_set = set(triangle_types)
    representatives = set()
    labeled_count = 0
    for pattern in product(range(len(nodes)), repeat=6):
        if any(
            face not in triangle_set for face in triangle_faces(pattern)
        ):
            continue
        if determinant(gram_matrix(pattern, nodes)) < 0:
            continue
        labeled_count += 1
        representatives.add(canonical(pattern))
    return tuple(sorted(representatives)), labeled_count


def profile_categories(color_count):
    return tuple(
        combinations_with_replacement(range(color_count), 2)
    )


def edge_profile_second_coefficients(pattern, color_count):
    """Distinct-third-vertex part of sum_e n(e)n(e)^T."""

    categories = profile_categories(color_count)
    category_index = {
        category: index for index, category in enumerate(categories)
    }
    blocks = [
        [[0 for _ in categories] for _ in categories]
        for _ in range(color_count)
    ]
    for edge_index, (first, second) in enumerate(EDGES):
        anchor_color = pattern[edge_index]
        remaining = [
            vertex
            for vertex in VERTICES
            if vertex not in {first, second}
        ]
        profile_indices = []
        for vertex in remaining:
            first_color = pattern[
                EDGE_INDEX[tuple(sorted((first, vertex)))]
            ]
            second_color = pattern[
                EDGE_INDEX[tuple(sorted((second, vertex)))]
            ]
            profile_indices.append(
                category_index[
                    tuple(sorted((first_color, second_color)))
                ]
            )
        alpha, beta = profile_indices
        if alpha == beta:
            blocks[anchor_color][alpha][alpha] += 2
        else:
            blocks[anchor_color][alpha][beta] += 1
            blocks[anchor_color][beta][alpha] += 1
    return blocks


def edge_profile_first_moments(triangle_counts, color_count, categories):
    category_index = {
        category: index for index, category in enumerate(categories)
    }
    moments = [[0 for _ in categories] for _ in range(color_count)]
    for triple, count in triangle_counts.items():
        for edge_position, anchor_color in enumerate(triple):
            profile = tuple(sorted(
                triple[position]
                for position in range(3)
                if position != edge_position
            ))
            moments[anchor_color][category_index[profile]] += count
    return moments


def load_source(path):
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    assert data["schema"] == (
        "local-hybrid-degree4-rank-color-clique-pseudodistribution-v1"
    )
    assert data["dimension"] == 5 and data["cardinality"] == 41
    nodes = tuple(Q(value) for value in data["nodes"])
    ordered_counts = tuple(data["ordered_pair_counts"])
    triangle_counts = {
        tuple(item["types"]): item["count"]
        for item in data["triple_counts"]
    }
    assert sum(ordered_counts) == 41 * 40
    assert sum(triangle_counts.values()) == 41 * 40 * 39 // 6
    return nodes, ordered_counts, triangle_counts


def verify():
    certificate = json.loads(CERTIFICATE.read_text(encoding="utf-8"))
    assert certificate["schema"] == (
        "edge-conditioned-k4-exact-obstruction-v1"
    )
    source = ROOT / certificate["source"]["path"]
    assert sha256_file(source) == certificate["source"]["sha256"]
    nodes, ordered_counts, triangle_counts = load_source(source)
    enumeration = certificate["enumeration"]

    triangle_types = feasible_triangle_types(nodes)
    assert len(triangle_types) == enumeration["feasible_triangle_types"]
    triangle_determinants = []
    for first, second, third in triangle_types:
        u, v, t = nodes[first], nodes[second], nodes[third]
        triangle_determinants.append(
            1 + 2 * u * v * t - u**2 - v**2 - t**2
        )
    assert all(value >= 0 for value in triangle_determinants)
    assert sum(value == 0 for value in triangle_determinants) == enumeration[
        "determinant_zero_triangle_types"
    ]
    assert digest(triangle_types) == enumeration[
        "triangle_type_digest_sha256"
    ]

    four_types, labeled_count = feasible_four_types(
        nodes, triangle_types
    )
    assert len(four_types) == enumeration["gram_psd_k4_orbits"]
    assert labeled_count == enumeration["feasible_labeled_k4_patterns"]
    four_determinants = tuple(
        determinant(gram_matrix(pattern, nodes)) for pattern in four_types
    )
    assert all(value >= 0 for value in four_determinants)
    assert sum(value == 0 for value in four_determinants) == enumeration[
        "determinant_zero_k4_orbits"
    ]
    orbit_sizes = Counter(len(orbit(pattern)) for pattern in four_types)
    assert orbit_sizes == Counter({
        int(size): count
        for size, count in enumeration["orbit_size_distribution"].items()
    })
    assert sum(
        size * count for size, count in orbit_sizes.items()
    ) == labeled_count
    assert digest(four_types) == enumeration[
        "k4_representative_digest_sha256"
    ]

    # An orbit variable counts unordered four-vertex sets of that orbit
    # type.  Its face coefficient is therefore the number (0,...,4) of
    # faces of each type.  No stabilizer or orbit-size factor appears.
    face_incidence = [
        [
            triangle_faces(pattern).count(triple)
            for pattern in four_types
        ]
        for triple in triangle_types
    ]
    face_targets = [
        38 * triangle_counts.get(triple, 0)
        for triple in triangle_types
    ]
    assert all(
        sum(face_incidence[row][column] for row in range(21)) == 4
        for column in range(len(four_types))
    )
    assert digest(face_incidence) == enumeration[
        "face_incidence_digest_sha256"
    ]
    assert digest(face_targets) == enumeration[
        "face_target_digest_sha256"
    ]

    categories = profile_categories(len(nodes))
    assert len(categories) == 15
    first_moments = edge_profile_first_moments(
        triangle_counts, len(nodes), categories
    )
    second_coefficients = [
        edge_profile_second_coefficients(pattern, len(nodes))
        for pattern in four_types
    ]
    # The edge-conditioned coefficient is invariant across every labeled
    # representative of an orbit, so no stabilizer averaging is missing.
    for representative, expected in zip(
        four_types, second_coefficients
    ):
        assert all(
            edge_profile_second_coefficients(image, len(nodes)) == expected
            for image in orbit(representative)
        )

    coordinate_constants = []
    coordinate_coefficients = []
    for color in range(len(nodes)):
        edge_count = ordered_counts[color] // 2
        assert edge_count > 0
        for category in range(len(categories)):
            first = first_moments[color][category]
            coordinate_constants.append(str(
                Q(first) - Q(first**2, edge_count)
            ))
            coordinate_coefficients.append([
                block[color][category][category]
                for block in second_coefficients
            ])
    assert len(coordinate_constants) == 75
    assert digest(coordinate_constants) == enumeration[
        "coordinate_covariance_constant_digest_sha256"
    ]
    assert digest(coordinate_coefficients) == enumeration[
        "coordinate_covariance_coefficient_digest_sha256"
    ]

    # Exact one-row Farkas contradiction.
    special = certificate["special_covariance_cut"]
    color = special["anchor_edge_color"]
    category = special["profile_category_index"]
    assert categories[category] == tuple(special["profile_category"])
    edge_count = ordered_counts[color] // 2
    first = first_moments[color][category]
    row_index = color * len(categories) + category
    constant = Q(coordinate_constants[row_index])
    coefficients = coordinate_coefficients[row_index]
    assert edge_count == special["anchor_edge_count"] == 131
    assert first == special["profile_first_moment"] == 243
    assert constant == Q(special["covariance_constant"]) == Q(-27216, 131)
    assert set(coefficients) == {0}
    assert Q(special["farkas_multiplier"]) == 1
    # PSD would require constant + sum_R coefficient_R*y_R >= 0 for
    # nonnegative orbit counts y_R.  This row is the false inequality
    # -27216/131 >= 0, independently of the face equalities.
    assert constant < 0

    # Independent exact geometry behind the zero K4 coefficients.
    lemma = certificate["analytic_lemma"]
    q = Q(lemma["base_inner_product_upper"])
    s = Q(lemma["common_neighbor_inner_product_lower"])
    projection_square = Q(2) * s**2 / (1 + q)
    two_neighbor_lower = 2 * projection_square - 1
    assert projection_square == Q(
        lemma["projection_square_lower"]
    ) == Q(249001, 280000)
    assert two_neighbor_lower == Q(
        lemma["two_neighbor_inner_product_lower"]
    ) == Q(109001, 140000)
    assert two_neighbor_lower - Q(1, 2) == Q(
        lemma["margin_above_one_half"]
    ) == Q(39001, 140000)

    deep_colors = {
        index for index, node in enumerate(nodes) if node <= q
    }
    high_colors = {
        index for index, node in enumerate(nodes) if node >= s
    }
    assert deep_colors == {0, 1, 2}
    assert high_colors == {4}
    deep_edges = sum(ordered_counts[index] // 2 for index in deep_colors)
    deep_high_high_triangles = sum(
        count
        for triple, count in triangle_counts.items()
        if sum(index in deep_colors for index in triple) == 1
        and sum(index in high_colors for index in triple) == 2
    )
    counting = certificate["continuous_counting_cut"]
    assert deep_edges == counting["deep_edge_count"] == 219
    assert deep_high_high_triangles == counting[
        "deep_base_high_high_triangle_count"
    ] == 243
    assert deep_high_high_triangles - deep_edges == counting[
        "violation"
    ] == 24

    return {
        "status": "PASS",
        "feasible_triangle_types": len(triangle_types),
        "gram_psd_k4_orbits": len(four_types),
        "feasible_labeled_k4_patterns": labeled_count,
        "special_covariance_constant": constant,
        "continuous_counting_violation": deep_high_high_triangles
        - deep_edges,
        "conclusion": "exact one-row Farkas contradiction",
    }


if __name__ == "__main__":
    for key, value in verify().items():
        print(f"{key}: {value}")
