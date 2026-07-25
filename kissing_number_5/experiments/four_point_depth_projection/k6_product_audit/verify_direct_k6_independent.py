#!/usr/bin/env python3
"""Independent exact audit of the direct rank-five K6 certificate.

This verifier intentionally does not import the discovery code or the original
verifier.  It uses an exact rational LDL decomposition rather than the
original all-principal-minors/Leibniz-determinant path.  It also makes the
implicit orbit symmetrization explicit and computes the induced K5 and K4
orbit distributions.

Only the Python standard library is required.  The file is compatible with
Python 3.9 and later.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from fractions import Fraction as Q
import hashlib
import itertools
import json
import math
from pathlib import Path
from typing import Dict, Iterable, List, Sequence, Tuple


ROOT = Path(__file__).resolve().parents[3]
SOURCE_PATH = (
    ROOT / "certificates" / "centered_quarter_bv_pseudodistribution.json"
)
K6_PATH = (
    ROOT
    / "experiments"
    / "centered_quarter_k6_rank"
    / "direct_k6_triangle_extension.json"
)

EXPECTED_SOURCE_SHA256 = (
    "112be681b4fb98dcfb8af29d08be78bfecfde7088154429fba76774d4c57d550"
)
EXPECTED_K6_SHA256 = (
    "32e629ab5df91cf6e616aa1f7a61af22f853b78ccff50947738b5cab1394d0ba"
)
EDGE_KEY6 = (
    "edge_color_indices_01_02_03_04_05_12_13_14_15_23_24_25_34_35_45"
)

EdgeVector = Tuple[int, ...]
Matrix = Tuple[Tuple[int, ...], ...]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def pairs(size: int) -> Tuple[Tuple[int, int], ...]:
    return tuple(
        (i, j) for i in range(size) for j in range(i + 1, size)
    )


def gram(
    edges: EdgeVector, scaled_values: Sequence[int], size: int
) -> Matrix:
    ps = pairs(size)
    assert len(edges) == len(ps)
    answer = [[4 if i == j else 0 for j in range(size)] for i in range(size)]
    for pair, color in zip(ps, edges):
        i, j = pair
        answer[i][j] = scaled_values[color]
        answer[j][i] = scaled_values[color]
    return tuple(tuple(row) for row in answer)


def rational_rank(matrix: Sequence[Sequence[int]]) -> int:
    """Exact row rank by rational Gaussian elimination."""
    work = [[Q(value) for value in row] for row in matrix]
    rows = len(work)
    columns = len(work[0]) if rows else 0
    pivot_row = 0
    for column in range(columns):
        pivot = next(
            (
                row
                for row in range(pivot_row, rows)
                if work[row][column] != 0
            ),
            None,
        )
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        scale = work[pivot_row][column]
        work[pivot_row] = [value / scale for value in work[pivot_row]]
        for row in range(rows):
            if row == pivot_row or work[row][column] == 0:
                continue
            scale = work[row][column]
            work[row] = [
                value - scale * pivot_value
                for value, pivot_value in zip(
                    work[row], work[pivot_row]
                )
            ]
        pivot_row += 1
        if pivot_row == rows:
            break
    return pivot_row


def ldl_pivots(matrix: Matrix, order: Sequence[int]) -> Tuple[Q, ...]:
    """Return exact no-pivot LDL pivots in the supplied vertex order.

    A zero pivot is permitted only in the final position.  The caller uses an
    order for which the first five vertices form a positive-definite block.
    """
    size = len(order)
    lower = [[Q(0) for _ in range(size)] for _ in range(size)]
    diagonal = [Q(0) for _ in range(size)]
    for i in range(size):
        lower[i][i] = Q(1)
        for j in range(i):
            if diagonal[j] == 0:
                raise ZeroDivisionError("zero nonfinal LDL pivot")
            residual = Q(matrix[order[i]][order[j]]) - sum(
                lower[i][h] * lower[j][h] * diagonal[h]
                for h in range(j)
            )
            lower[i][j] = residual / diagonal[j]
        diagonal[i] = Q(matrix[order[i]][order[i]]) - sum(
            lower[i][h] * lower[i][h] * diagonal[h] for h in range(i)
        )
    return tuple(diagonal)


def rank_five_psd_factor(matrix: Matrix) -> Tuple[Tuple[int, ...], Tuple[Q, ...]]:
    """Certify PSD and rank exactly five via an exact block LDL factorization."""
    assert len(matrix) == 6
    assert all(len(row) == 6 for row in matrix)
    assert all(
        matrix[i][j] == matrix[j][i] for i in range(6) for j in range(6)
    )
    for final_vertex in range(6):
        order = tuple(
            vertex for vertex in range(6) if vertex != final_vertex
        ) + (final_vertex,)
        try:
            pivots = ldl_pivots(matrix, order)
        except ZeroDivisionError:
            continue
        if all(pivot > 0 for pivot in pivots[:5]) and pivots[5] == 0:
            return order, pivots
    raise AssertionError("no exact rank-five PSD LDL factorization found")


def determinant3(matrix: Matrix) -> int:
    assert len(matrix) == 3
    a, b, c = matrix
    return (
        a[0] * (b[1] * c[2] - b[2] * c[1])
        - a[1] * (b[0] * c[2] - b[2] * c[0])
        + a[2] * (b[0] * c[1] - b[1] * c[0])
    )


def feasible_triangle_types(scaled_values: Sequence[int]) -> Tuple[EdgeVector, ...]:
    """Enumerate all sorted color triples whose 3-point Gram matrix is PSD."""
    result = []
    for colors in itertools.combinations_with_replacement(
        range(len(scaled_values)), 3
    ):
        matrix = gram(colors, scaled_values, 3)
        two_by_two = [
            16 - matrix[i][j] * matrix[i][j]
            for i in range(3)
            for j in range(i + 1, 3)
        ]
        if min(two_by_two) >= 0 and determinant3(matrix) >= 0:
            result.append(colors)
    return tuple(result)


def edge_lookup(edges: EdgeVector, size: int) -> Dict[Tuple[int, int], int]:
    return dict(zip(pairs(size), edges))


def relabel(
    edges: EdgeVector, size: int, permutation: Sequence[int]
) -> EdgeVector:
    lookup = edge_lookup(edges, size)
    return tuple(
        lookup[tuple(sorted((permutation[i], permutation[j])))]
        for i, j in pairs(size)
    )


_CANONICAL_CACHE: Dict[Tuple[int, EdgeVector], EdgeVector] = {}


def canonical(edges: EdgeVector, size: int) -> EdgeVector:
    key = (size, edges)
    cached = _CANONICAL_CACHE.get(key)
    if cached is not None:
        return cached
    answer = min(
        relabel(edges, size, permutation)
        for permutation in itertools.permutations(range(size))
    )
    _CANONICAL_CACHE[key] = answer
    return answer


def orbit(edges: EdgeVector, size: int) -> frozenset:
    return frozenset(
        relabel(edges, size, permutation)
        for permutation in itertools.permutations(range(size))
    )


def face(
    edges: EdgeVector, ambient_size: int, vertices: Sequence[int]
) -> EdgeVector:
    lookup = edge_lookup(edges, ambient_size)
    return tuple(
        lookup[tuple(sorted((vertices[i], vertices[j])))]
        for i, j in pairs(len(vertices))
    )


def triangle_feature(
    edges: EdgeVector,
    size: int,
    triple_index: Dict[EdgeVector, int],
) -> Tuple[int, ...]:
    lookup = edge_lookup(edges, size)
    answer = []
    for vertices in itertools.combinations(range(size), 3):
        colors = tuple(
            sorted(
                lookup[tuple(sorted(pair))]
                for pair in itertools.combinations(vertices, 2)
            )
        )
        answer.append(triple_index[colors])
    return tuple(sorted(answer))


def induced_orbit_distribution(
    atoms: Sequence[Tuple[EdgeVector, Q]], face_size: int
) -> Dict[EdgeVector, Q]:
    """Induce the uniform face marginal and aggregate it by S_face_size orbit."""
    denominator = Q(math.comb(6, face_size))
    masses = defaultdict(Q)
    for edges, weight in atoms:
        for vertices in itertools.combinations(range(6), face_size):
            induced = face(edges, 6, vertices)
            masses[canonical(induced, face_size)] += weight / denominator
    assert sum(masses.values(), Q(0)) == 1
    assert all(weight > 0 for weight in masses.values())
    return dict(masses)


def induce_k4_from_k5(
    k5_masses: Dict[EdgeVector, Q]
) -> Dict[EdgeVector, Q]:
    masses = defaultdict(Q)
    for edges, weight in k5_masses.items():
        for vertices in itertools.combinations(range(5), 4):
            induced = face(edges, 5, vertices)
            masses[canonical(induced, 4)] += weight / 5
    assert sum(masses.values(), Q(0)) == 1
    return dict(masses)


def expected_counts(
    orbit_masses: Dict[EdgeVector, Q],
    size: int,
    triple_index: Dict[EdgeVector, int],
) -> Tuple[List[Q], List[Q]]:
    edge_counts = [Q(0) for _ in range(7)]
    triangle_counts = [Q(0) for _ in range(len(triple_index))]
    for edges, weight in orbit_masses.items():
        for color in edges:
            edge_counts[color] += weight
        for index in triangle_feature(edges, size, triple_index):
            triangle_counts[index] += weight
    return edge_counts, triangle_counts


def assert_vector_equal(left: Iterable[Q], right: Iterable[Q]) -> None:
    left_tuple = tuple(left)
    right_tuple = tuple(right)
    assert left_tuple == right_tuple, (left_tuple, right_tuple)


def rank_summary(
    orbit_masses: Dict[EdgeVector, Q],
    size: int,
    scaled_values: Sequence[int],
) -> Tuple[Dict[int, int], Dict[int, str]]:
    orbit_counts = Counter()
    mass = defaultdict(Q)
    for edges, weight in orbit_masses.items():
        rank = rational_rank(gram(edges, scaled_values, size))
        orbit_counts[rank] += 1
        mass[rank] += weight
    return (
        dict(sorted(orbit_counts.items())),
        {rank: str(value) for rank, value in sorted(mass.items())},
    )


def verify(
    source_path: Path = SOURCE_PATH,
    certificate_path: Path = K6_PATH,
    pin_certificate_hash: bool = True,
) -> dict:
    assert sha256(source_path) == EXPECTED_SOURCE_SHA256
    if pin_certificate_hash:
        assert sha256(certificate_path) == EXPECTED_K6_SHA256
    source = json.loads(source_path.read_text())
    certificate = json.loads(certificate_path.read_text())

    assert source["schema"] == (
        "kissing5.centered_quarter_bv_pseudodistribution.v1"
    )
    assert source["dimension"] == 5
    assert source["cardinality"] == 41
    assert certificate["schema"] == (
        "kissing5.centered_quarter_direct_k6_triangle_extension.v1"
    )
    assert certificate["source_sha256"] == EXPECTED_SOURCE_SHA256

    grid = tuple(Q(value) for value in source["grid"])
    assert grid == (
        Q(-1),
        Q(-3, 4),
        Q(-1, 2),
        Q(-1, 4),
        Q(0),
        Q(1, 4),
        Q(1, 2),
    )
    scaled_values = tuple(int(4 * value) for value in grid)
    assert tuple(Q(value, 4) for value in scaled_values) == grid

    triples = tuple(tuple(item) for item in source["triple_orbits"])
    assert triples == feasible_triangle_types(scaled_values)
    triple_index = {triple: index for index, triple in enumerate(triples)}
    assert len(triples) == len(triple_index) == 51

    alpha = tuple(Q(value) for value in source["alpha"])
    nu = tuple(Q(value) for value in source["nu"])
    assert all(value > 0 for value in alpha + nu)
    assert sum(alpha, Q(0)) == 40
    assert sum(nu, Q(0)) == 1560
    assert 1 + sum(
        weight * node for weight, node in zip(alpha, grid)
    ) == 0
    for color in range(7):
        marginal = sum(
            weight * triple.count(color) / 3
            for triple, weight in zip(triples, nu)
        )
        assert marginal == 39 * alpha[color]

    raw_atoms = certificate["atoms"]
    assert len(raw_atoms) == certificate["positive_atom_count"] == 51
    weights = tuple(Q(atom["weight"]) for atom in raw_atoms)
    assert all(weight > 0 for weight in weights)
    assert sum(weights, Q(0)) == 1
    atoms = []
    k6_canonical = set()
    orbit_sizes = []
    minimum_positive_ldl_pivot = None
    for atom, weight in zip(raw_atoms, weights):
        edges = tuple(atom[EDGE_KEY6])
        assert len(edges) == 15
        assert all(0 <= color < 7 for color in edges)
        matrix = gram(edges, scaled_values, 6)
        assert all(matrix[i][i] == 4 for i in range(6))
        assert all(
            matrix[i][j] <= 2
            for i in range(6)
            for j in range(i + 1, 6)
        )
        order, pivots = rank_five_psd_factor(matrix)
        del order
        assert rational_rank(matrix) == 5
        local_minimum = min(pivots[:5])
        minimum_positive_ldl_pivot = (
            local_minimum
            if minimum_positive_ldl_pivot is None
            else min(minimum_positive_ldl_pivot, local_minimum)
        )

        feature = triangle_feature(edges, 6, triple_index)
        assert feature == tuple(atom["triangle_orbit_indices"])
        canon = canonical(edges, 6)
        assert canon not in k6_canonical
        k6_canonical.add(canon)
        orbit_sizes.append(len(orbit(edges, 6)))
        atoms.append((edges, weight))

    assert len(k6_canonical) == 51
    assert Counter(orbit_sizes) == Counter({180: 9, 360: 14, 720: 28})
    assert sum(orbit_sizes) == 26820

    k6_masses = {canonical(edges, 6): weight for edges, weight in atoms}
    k6_edge, k6_triangle = expected_counts(k6_masses, 6, triple_index)
    assert_vector_equal(k6_edge, (3 * value / 8 for value in alpha))
    assert_vector_equal(k6_triangle, (value / 78 for value in nu))
    # Divide the count expectations by C(6,2)=15 and C(6,3)=20.
    assert_vector_equal(
        (value / 15 for value in k6_edge),
        (value / 40 for value in alpha),
    )
    assert_vector_equal(
        (value / 20 for value in k6_triangle),
        (value / 1560 for value in nu),
    )

    k5_masses = induced_orbit_distribution(atoms, 5)
    k4_masses_direct = induced_orbit_distribution(atoms, 4)
    k4_masses_via_k5 = induce_k4_from_k5(k5_masses)
    assert k4_masses_direct == k4_masses_via_k5

    k5_edge, k5_triangle = expected_counts(k5_masses, 5, triple_index)
    assert_vector_equal(k5_edge, (value / 4 for value in alpha))
    assert_vector_equal(k5_triangle, (value / 156 for value in nu))
    assert_vector_equal(
        (value / 10 for value in k5_edge),
        (value / 40 for value in alpha),
    )
    assert_vector_equal(
        (value / 10 for value in k5_triangle),
        (value / 1560 for value in nu),
    )

    k4_edge, k4_triangle = expected_counts(
        k4_masses_direct, 4, triple_index
    )
    assert_vector_equal(k4_edge, (3 * value / 20 for value in alpha))
    assert_vector_equal(k4_triangle, (value / 390 for value in nu))
    assert_vector_equal(
        (value / 6 for value in k4_edge),
        (value / 40 for value in alpha),
    )
    assert_vector_equal(
        (value / 4 for value in k4_triangle),
        (value / 1560 for value in nu),
    )

    k5_rank_counts, k5_rank_mass = rank_summary(
        k5_masses, 5, scaled_values
    )
    k4_rank_counts, k4_rank_mass = rank_summary(
        k4_masses_direct, 4, scaled_values
    )
    assert max(k5_rank_counts) <= 5
    assert max(k4_rank_counts) <= 4

    return {
        "status": "PASS",
        "scope": (
            "exact symmetrized local K6 pair/triangle extension only; "
            "not a global code or a Lasserre consistency certificate"
        ),
        "source_sha256": sha256(source_path),
        "k6_sha256": sha256(certificate_path),
        "positive_orbit_masses": len(atoms),
        "weight_sum": "1",
        "minimum_weight": str(min(weights)),
        "maximum_weight": str(max(weights)),
        "k6_distinct_orbits": len(k6_canonical),
        "k6_orbit_size_distribution": dict(sorted(Counter(orbit_sizes).items())),
        "k6_labeled_support_union": sum(orbit_sizes),
        "k6_rank": 5,
        "minimum_positive_exact_ldl_pivot": str(minimum_positive_ldl_pivot),
        "uniform_edge_marginal": "alpha/40",
        "uniform_triangle_marginal": "nu/1560",
        "induced_k5": {
            "positive_orbits": len(k5_masses),
            "expected_edge_counts": "alpha/4",
            "expected_triangle_counts": "nu/156",
            "rank_orbit_counts": k5_rank_counts,
            "rank_mass": k5_rank_mass,
        },
        "induced_k4": {
            "positive_orbits": len(k4_masses_direct),
            "expected_edge_counts": "3*alpha/20",
            "expected_triangle_counts": "nu/390",
            "rank_orbit_counts": k4_rank_counts,
            "rank_mass": k4_rank_mass,
            "direct_equals_via_k5": True,
        },
    }


if __name__ == "__main__":
    print(json.dumps(verify(), indent=2, sort_keys=True))
