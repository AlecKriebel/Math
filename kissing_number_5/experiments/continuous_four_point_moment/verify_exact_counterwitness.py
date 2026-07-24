#!/usr/bin/env python3
"""Exact verifier for the continuous four-point moment counter-witness.

The verifier uses only the Python standard library and rational
arithmetic.  It verifies:

* 74 positive rational rank-five K6 Gram atoms;
* the exact N=41 pair/triple/four-point scaling and projections;
* continuous Gram-support and permutation symmetries;
* all 27 sharp low-degree harmonic rank trace cuts;
* the selected closed semialgebraic depth/cap/product rows; and
* an exact SOS decomposition for the degree-two edge covariance block.

The atomic support is used only as a feasible measure for a relaxation
whose variables range over the full interval [-1,1/2].
"""

from __future__ import annotations

from collections import defaultdict
from fractions import Fraction as Q
import hashlib
import itertools
import json
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "certificates" / "centered_quarter_bv_pseudodistribution.json"
EXTENSION = (
    ROOT
    / "experiments"
    / "four_point_depth_projection"
    / "k6_product_audit"
    / "productpool_extension.json"
)
SOURCE_SHA256 = (
    "112be681b4fb98dcfb8af29d08be78bfecfde7088154429fba76774d4c57d550"
)
EXTENSION_SHA256 = (
    "def805e0c73fb5a5306f230ad21866a5b0fcab1a3708f6f7daaa3b175dc54991"
)

N = 41
PAIRS6 = tuple(itertools.combinations(range(6), 2))
PAIR6_INDEX = {edge: index for index, edge in enumerate(PAIRS6)}

BAND_LOWER = Q(-3, 10)
BAND_UPPER = Q(-6, 25)
HIGH_THRESHOLD = Q(49, 100)
DEPTH_DELTA = Q(1, 301)
CAPACITY = 3


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def determinant(matrix: list[list[int | Q]]) -> int | Q:
    """Fraction-preserving determinant."""

    if not matrix:
        return Q(1)
    work = [[Q(entry) for entry in row] for row in matrix]
    answer: int | Q = Q(1)
    for column in range(len(work)):
        pivot = next(
            (
                row
                for row in range(column, len(work))
                if work[row][column] != 0
            ),
            None,
        )
        if pivot is None:
            return 0
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


def rank(matrix: list[list[Q]]) -> int:
    work = [row[:] for row in matrix]
    row = 0
    for column in range(len(work[0])):
        pivot = next(
            (
                candidate
                for candidate in range(row, len(work))
                if work[candidate][column]
            ),
            None,
        )
        if pivot is None:
            continue
        work[row], work[pivot] = work[pivot], work[row]
        scale = work[row][column]
        work[row] = [entry / scale for entry in work[row]]
        for other in range(len(work)):
            if other == row:
                continue
            scale = work[other][column]
            if scale:
                work[other] = [
                    entry - scale * pivot_entry
                    for entry, pivot_entry in zip(work[other], work[row])
                ]
        row += 1
        if row == len(work):
            break
    return row


def gram6(edges: tuple[int, ...], scaled_nodes: tuple[int, ...]) -> list[list[int]]:
    matrix = [[4 if i == j else 0 for j in range(6)] for i in range(6)]
    for (i, j), color in zip(PAIRS6, edges):
        matrix[i][j] = scaled_nodes[color]
        matrix[j][i] = scaled_nodes[color]
    return matrix


def assert_rank_five_psd(
    edges: tuple[int, ...], scaled_nodes: tuple[int, ...]
) -> int:
    matrix = gram6(edges, scaled_nodes)
    positive_fifth = []
    for size in range(1, 7):
        for indices in itertools.combinations(range(6), size):
            minor = [[matrix[i][j] for j in indices] for i in indices]
            value = determinant(minor)
            assert value >= 0
            if size == 5 and value > 0:
                positive_fifth.append(int(value))
            if size == 6:
                assert value == 0
    assert positive_fifth
    return min(positive_fifth)


def edge_value(
    edges: tuple[int, ...],
    nodes: tuple[Q, ...],
    first: int,
    second: int,
) -> Q:
    return nodes[
        edges[PAIR6_INDEX[tuple(sorted((first, second)))]]
    ]


def triangle_delta(u: Q, v: Q, t: Q) -> Q:
    return 1 + 2 * u * v * t - u * u - v * v - t * t


def gram4(values: tuple[Q, Q, Q, Q, Q, Q]) -> list[list[Q]]:
    q, a, b, c, d, e = values
    return [
        [Q(1), q, a, c],
        [q, Q(1), b, d],
        [a, b, Q(1), e],
        [c, d, e, Q(1)],
    ]


def add_mass(table: dict[tuple[Q, ...], Q], key: tuple[Q, ...], mass: Q) -> None:
    table[key] = table.get(key, Q(0)) + mass


def induced_measures(
    atoms: list[tuple[tuple[int, ...], Q]],
    nodes: tuple[Q, ...],
) -> tuple[
    dict[tuple[Q, ...], Q],
    dict[tuple[Q, ...], Q],
    dict[tuple[Q, ...], Q],
]:
    """Build the globally normalized ordered alpha, nu, rho measures."""

    alpha6: dict[tuple[Q, ...], Q] = {}
    nu6: dict[tuple[Q, ...], Q] = {}
    rho6: dict[tuple[Q, ...], Q] = {}
    for edges, weight in atoms:
        for i, j in itertools.permutations(range(6), 2):
            add_mass(alpha6, (edge_value(edges, nodes, i, j),), weight)
        for i, j, k in itertools.permutations(range(6), 3):
            add_mass(
                nu6,
                (
                    edge_value(edges, nodes, i, j),
                    edge_value(edges, nodes, i, k),
                    edge_value(edges, nodes, j, k),
                ),
                weight,
            )
        for i, j, k, ell in itertools.permutations(range(6), 4):
            add_mass(
                rho6,
                (
                    edge_value(edges, nodes, i, j),
                    edge_value(edges, nodes, i, k),
                    edge_value(edges, nodes, j, k),
                    edge_value(edges, nodes, i, ell),
                    edge_value(edges, nodes, j, ell),
                    edge_value(edges, nodes, k, ell),
                ),
                weight,
            )
    alpha = {key: Q(4, 3) * mass for key, mass in alpha6.items()}
    nu = {key: Q(13) * mass for key, mass in nu6.items()}
    rho = {key: Q(494, 3) * mass for key, mass in rho6.items()}
    return alpha, nu, rho


def transform_triangle(
    values: tuple[Q, Q, Q], permutation: tuple[int, int, int]
) -> tuple[Q, Q, Q]:
    q, a, b = values
    edge = {(0, 1): q, (0, 2): a, (1, 2): b}

    def get(first: int, second: int) -> Q:
        return edge[tuple(sorted((first, second)))]

    i, j, k = permutation
    return get(i, j), get(i, k), get(j, k)


def transform_four(
    values: tuple[Q, Q, Q, Q, Q, Q],
    permutation: tuple[int, int, int, int],
) -> tuple[Q, Q, Q, Q, Q, Q]:
    q, a, b, c, d, e = values
    edge = {
        (0, 1): q,
        (0, 2): a,
        (1, 2): b,
        (0, 3): c,
        (1, 3): d,
        (2, 3): e,
    }

    def get(first: int, second: int) -> Q:
        return edge[tuple(sorted((first, second)))]

    i, j, k, ell = permutation
    return (
        get(i, j),
        get(i, k),
        get(j, k),
        get(i, ell),
        get(j, ell),
        get(k, ell),
    )


def monomial_exponents(variable_count: int, maximum_degree: int):
    return tuple(
        exponents
        for exponents in itertools.product(
            range(maximum_degree + 1), repeat=variable_count
        )
        if sum(exponents) <= maximum_degree
    )


def monomial_vector(
    values: tuple[Q, ...], exponents: tuple[tuple[int, ...], ...]
) -> tuple[Q, ...]:
    return tuple(
        math.prod(value**power for value, power in zip(values, powers))
        for powers in exponents
    )


def zero_matrix(size: int) -> list[list[Q]]:
    return [[Q(0) for _ in range(size)] for _ in range(size)]


def add_outer(
    matrix: list[list[Q]],
    first: tuple[Q, ...],
    second: tuple[Q, ...],
    coefficient: Q,
) -> None:
    for i, left in enumerate(first):
        for j, right in enumerate(second):
            matrix[i][j] += coefficient * left * right


def covariance_sos(
    atoms: list[tuple[tuple[int, ...], Q]],
    nodes: tuple[Q, ...],
) -> tuple[list[list[Q]], list[list[Q]]]:
    """Return the covariance matrix and its pair-difference SOS expansion."""

    exponents = monomial_exponents(3, 2)
    direct = zero_matrix(len(exponents))
    sos = zero_matrix(len(exponents))
    for edges, weight in atoms:
        coefficient = weight * Q(494, 3)
        for i, j in itertools.permutations(range(6), 2):
            q = edge_value(edges, nodes, i, j)
            residual = [vertex for vertex in range(6) if vertex not in (i, j)]
            vectors = [
                monomial_vector(
                    (
                        q,
                        edge_value(edges, nodes, i, vertex),
                        edge_value(edges, nodes, j, vertex),
                    ),
                    exponents,
                )
                for vertex in residual
            ]
            total = tuple(sum(vector[h] for vector in vectors) for h in range(len(exponents)))
            for vector in vectors:
                add_outer(direct, vector, vector, 4 * coefficient)
            add_outer(direct, total, total, -coefficient)
            for first, second in itertools.combinations(vectors, 2):
                difference = tuple(a - b for a, b in zip(first, second))
                add_outer(sos, difference, difference, coefficient)
    assert direct == sos
    return direct, sos


def gegenbauer_5_sequence(t: Q, maximum_degree: int) -> list[Q]:
    values = [Q(1)]
    if maximum_degree == 0:
        return values
    values.append(t)
    for degree in range(2, maximum_degree + 1):
        values.append(
            (
                (2 * degree + 1) * t * values[-1]
                - (degree - 1) * values[-2]
            )
            / (degree + 2)
        )
    return values


def harmonic_dimension(degree: int) -> int:
    return math.comb(degree + 4, 4) - (
        math.comb(degree + 2, 4) if degree >= 2 else 0
    )


def rank_kernel_specs():
    return (
        ("H1", ((1, Q(1)),)),
        ("H2", ((2, Q(1)),)),
        ("H3", ((3, Q(1)),)),
        ("H0+5H1", ((0, Q(1, 6)), (1, Q(5, 6)))),
        ("H0-5H1", ((0, Q(1, 6)), (1, Q(-5, 6)))),
        ("H0+14H2", ((0, Q(1, 15)), (2, Q(14, 15)))),
        ("H0-14H2", ((0, Q(1, 15)), (2, Q(-14, 15)))),
        ("5H1+14H2", ((1, Q(5, 19)), (2, Q(14, 19)))),
        ("5H1-14H2", ((1, Q(5, 19)), (2, Q(-14, 19)))),
        ("H0+H1", ((0, Q(1, 2)), (1, Q(1, 2)))),
        ("H0-H1", ((0, Q(1, 2)), (1, Q(-1, 2)))),
        ("H0+H2", ((0, Q(1, 2)), (2, Q(1, 2)))),
        ("H0-H2", ((0, Q(1, 2)), (2, Q(-1, 2)))),
        ("H1+H2", ((1, Q(1, 2)), (2, Q(1, 2)))),
        ("H1-H2", ((1, Q(1, 2)), (2, Q(-1, 2)))),
        (
            "H0+5H1+14H2",
            ((0, Q(1, 20)), (1, Q(1, 4)), (2, Q(7, 10))),
        ),
        (
            "H0+5H1-14H2",
            ((0, Q(1, 20)), (1, Q(1, 4)), (2, Q(-7, 10))),
        ),
        (
            "H0-5H1+14H2",
            ((0, Q(1, 20)), (1, Q(-1, 4)), (2, Q(7, 10))),
        ),
        (
            "H0-5H1-14H2",
            ((0, Q(1, 20)), (1, Q(-1, 4)), (2, Q(-7, 10))),
        ),
        ("H0+30H3", ((0, Q(1, 31)), (3, Q(30, 31)))),
        ("H0-30H3", ((0, Q(1, 31)), (3, Q(-30, 31)))),
        ("5H1+30H3", ((1, Q(1, 7)), (3, Q(6, 7)))),
        ("5H1-30H3", ((1, Q(1, 7)), (3, Q(-6, 7)))),
        (
            "H0+5H1+30H3",
            ((0, Q(1, 36)), (1, Q(5, 36)), (3, Q(5, 6))),
        ),
        (
            "H0+5H1-30H3",
            ((0, Q(1, 36)), (1, Q(5, 36)), (3, Q(-5, 6))),
        ),
        (
            "H0-5H1+30H3",
            ((0, Q(1, 36)), (1, Q(-5, 36)), (3, Q(5, 6))),
        ),
        (
            "H0-5H1-30H3",
            ((0, Q(1, 36)), (1, Q(-5, 36)), (3, Q(-5, 6))),
        ),
    )


def harmonic_rank_residuals(
    nodes: tuple[Q, ...],
    alpha_source: tuple[Q, ...],
    triples: tuple[tuple[int, int, int], ...],
    nu_source: tuple[Q, ...],
) -> list[tuple[Q, str]]:
    values = {node: gegenbauer_5_sequence(node, 3) for node in nodes}
    residuals = []
    for name, weights in rank_kernel_specs():
        kernel_rank = sum(
            harmonic_dimension(degree) for degree, _ in weights
        )
        diagonal = sum(coefficient for _, coefficient in weights)
        kernel_values = tuple(
            sum(
                coefficient * values[node][degree]
                for degree, coefficient in weights
            )
            for node in nodes
        )
        trace_one = Q(N) * diagonal
        pair_square = sum(
            mass * value * value
            for mass, value in zip(alpha_source, kernel_values)
        )
        trace_two = Q(N) * (diagonal * diagonal + pair_square)
        trace_three = (
            Q(N) * diagonal**3
            + Q(3 * N) * diagonal * pair_square
            + Q(N)
            * sum(
                mass
                * kernel_values[i]
                * kernel_values[j]
                * kernel_values[k]
                for mass, (i, j, k) in zip(nu_source, triples)
            )
        )
        variance = trace_two - trace_one**2 / kernel_rank
        centered_third = (
            trace_three
            - 3 * trace_one * trace_two / kernel_rank
            + 2 * trace_one**3 / kernel_rank**2
        )
        residual = (
            (kernel_rank - 2) ** 2 * variance**3
            - kernel_rank * (kernel_rank - 1) * centered_third**2
        )
        assert variance >= 0 and residual > 0
        residuals.append((residual, name))
    return residuals


def in_band(q: Q) -> bool:
    return BAND_LOWER <= q <= BAND_UPPER


def in_depth(q: Q, a: Q, b: Q) -> bool:
    total = a + b
    return (
        total <= 0
        and total * total >= DEPTH_DELTA**2 * (2 + 2 * q)
    )


def in_common(_q: Q, a: Q, b: Q) -> bool:
    return a >= HIGH_THRESHOLD and b >= HIGH_THRESHOLD


def product_masses(
    alpha: dict[tuple[Q, ...], Q],
    nu: dict[tuple[Q, ...], Q],
    rho: dict[tuple[Q, ...], Q],
) -> tuple[Q, Q, Q, Q]:
    alpha_band = sum(
        mass for (q,), mass in alpha.items() if in_band(q)
    )
    nu_depth = sum(
        mass
        for (q, a, b), mass in nu.items()
        if in_band(q) and in_depth(q, a, b)
    )
    nu_common = sum(
        mass
        for (q, a, b), mass in nu.items()
        if in_band(q) and in_common(q, a, b)
    )
    rho_product = sum(
        mass
        for (q, a, b, c, d, _e), mass in rho.items()
        if (
            in_band(q)
            and in_depth(q, a, b)
            and in_common(q, c, d)
        )
    )
    return alpha_band, nu_depth, nu_common, rho_product


def verify() -> dict[str, object]:
    assert sha256(SOURCE) == SOURCE_SHA256
    assert sha256(EXTENSION) == EXTENSION_SHA256
    source = json.loads(SOURCE.read_text())
    extension = json.loads(EXTENSION.read_text())
    assert source["schema"] == "kissing5.centered_quarter_bv_pseudodistribution.v1"
    assert extension["schema"] == "kissing5.rank5_k6_product_extension.v1"

    nodes = tuple(Q(value) for value in source["grid"])
    assert nodes == (
        Q(-1),
        Q(-3, 4),
        Q(-1, 2),
        Q(-1, 4),
        Q(0),
        Q(1, 4),
        Q(1, 2),
    )
    scaled_nodes = tuple(int(4 * value) for value in nodes)
    alpha_source = tuple(Q(value) for value in source["alpha"])
    triples = tuple(tuple(item) for item in source["triple_orbits"])
    nu_source = tuple(Q(value) for value in source["nu"])
    assert sum(alpha_source) == 40
    assert sum(nu_source) == 1560

    atoms = []
    minimum_fifth_minor = None
    for atom in extension["atoms"]:
        edges = tuple(
            atom[
                "edge_color_indices_"
                "01_02_03_04_05_12_13_14_15_23_24_25_34_35_45"
            ]
        )
        weight = Q(atom["weight"])
        assert weight > 0
        fifth = assert_rank_five_psd(edges, scaled_nodes)
        minimum_fifth_minor = (
            fifth
            if minimum_fifth_minor is None
            else min(minimum_fifth_minor, fifth)
        )
        atoms.append((edges, weight))
    assert len(atoms) == 74 and sum(weight for _, weight in atoms) == 1

    alpha, nu, rho = induced_measures(atoms, nodes)
    assert sum(alpha.values()) == 40
    assert sum(nu.values()) == 1560
    assert sum(rho.values()) == 59280

    # Match the stored pair and unordered-triangle orbit marginals.
    assert tuple(alpha.get((node,), Q(0)) for node in nodes) == alpha_source
    induced_orbits = defaultdict(Q)
    for values, mass in nu.items():
        induced_orbits[tuple(sorted(nodes.index(value) for value in values))] += mass
    assert tuple(induced_orbits[triple] for triple in triples) == nu_source

    # Projection identities.
    projected_nu = defaultdict(Q)
    for (q, _a, _b), mass in nu.items():
        projected_nu[(q,)] += mass
    assert projected_nu == {
        key: 39 * mass for key, mass in alpha.items()
    }
    projected_rho = defaultdict(Q)
    for (q, a, b, _c, _d, _e), mass in rho.items():
        projected_rho[(q, a, b)] += mass
    assert projected_rho == {
        key: 38 * mass for key, mass in nu.items()
    }

    # Full tuple symmetry.
    for values, mass in nu.items():
        for permutation in itertools.permutations(range(3)):
            assert nu[transform_triangle(values, permutation)] == mass
    for values, mass in rho.items():
        for permutation in itertools.permutations(range(4)):
            assert rho[transform_four(values, permutation)] == mass

    # Continuous support.  These checks include all boundary values.
    minimum_face_delta = None
    minimum_four_determinant = None
    for values in rho:
        assert all(Q(-1) <= value <= Q(1, 2) for value in values)
        q, a, b, c, d, e = values
        deltas = (
            triangle_delta(q, a, b),
            triangle_delta(q, c, d),
            triangle_delta(a, c, e),
            triangle_delta(b, d, e),
        )
        assert all(value >= 0 for value in deltas)
        four_det = determinant(gram4(values))
        assert four_det >= 0
        candidate_face = min(deltas)
        minimum_face_delta = (
            candidate_face
            if minimum_face_delta is None
            else min(minimum_face_delta, candidate_face)
        )
        minimum_four_determinant = (
            four_det
            if minimum_four_determinant is None
            else min(minimum_four_determinant, four_det)
        )

    # Every moment/localizing matrix is a positive sum of atomic outer
    # products.  Check the support multipliers used at order two.
    for (q,), mass in alpha.items():
        assert mass > 0 and q + 1 >= 0 and Q(1, 2) - q >= 0
    for (q, a, b), mass in nu.items():
        assert mass > 0
        assert all(value + 1 >= 0 for value in (q, a, b))
        assert all(Q(1, 2) - value >= 0 for value in (q, a, b))
        assert triangle_delta(q, a, b) >= 0
    for values, mass in rho.items():
        assert mass > 0
        assert all(value + 1 >= 0 for value in values)
        assert all(Q(1, 2) - value >= 0 for value in values)

    covariance, covariance_sos_matrix = covariance_sos(atoms, nodes)
    assert covariance == covariance_sos_matrix
    covariance_trace = sum(
        covariance[index][index] for index in range(len(covariance))
    )
    assert covariance_trace > 0
    covariance_rank = rank(covariance)

    residuals = harmonic_rank_residuals(
        nodes, alpha_source, triples, nu_source
    )
    minimum_rank_residual, minimum_rank_kernel = min(residuals)
    assert len(residuals) == 27

    # Exact capacity margin for every q in the selected band.
    projected_height_square = (
        2 * HIGH_THRESHOLD**2 / (1 + BAND_UPPER)
    )
    assert projected_height_square == Q(2401, 3800)
    assert projected_height_square - Q(5, 8) == Q(13, 1900)
    assert DEPTH_DELTA < Q(1, 300)

    alpha_band, nu_depth, nu_common, rho_product = product_masses(
        alpha, nu, rho
    )
    assert alpha_band == Q(125532493886399, 56250000000000)
    assert nu_depth == Q(974897098487491, 25000000000000)
    assert nu_common == Q(656862349021, 100000000000)
    assert rho_product == Q(8707691389928497, 75000000000000)
    depth_slack = nu_depth - 7 * alpha_band
    cap_slack = CAPACITY * alpha_band - nu_common
    product_slack = (
        CAPACITY * nu_depth
        + 7 * nu_common
        - 7 * CAPACITY * alpha_band
        - rho_product
    )
    assert depth_slack == Q(5259164057568247, 225000000000000) > 0
    assert cap_slack == Q(4741606889923, 37500000000000) > 0
    assert product_slack == 0

    return {
        "status": "PASS",
        "conclusion": (
            "exact feasible point for the continuous four-point moment, "
            "edge-covariance, product, and harmonic-rank relaxation"
        ),
        "source_sha256": SOURCE_SHA256,
        "extension_sha256": EXTENSION_SHA256,
        "positive_rank_five_k6_atoms": len(atoms),
        "minimum_positive_scaled_fifth_minor": minimum_fifth_minor,
        "measure_masses": {
            "alpha": str(sum(alpha.values())),
            "nu": str(sum(nu.values())),
            "rho": str(sum(rho.values())),
        },
        "projection_scaling": {
            "alpha_from_alpha6": "4/3",
            "nu_from_nu6": "13",
            "rho_from_rho6": "494/3",
        },
        "rho_support_atoms": len(rho),
        "minimum_triangle_face_determinant": str(minimum_face_delta),
        "minimum_k4_determinant": str(minimum_four_determinant),
        "edge_covariance_feature_degree": 2,
        "edge_covariance_matrix_size": len(covariance),
        "edge_covariance_exact_rank": covariance_rank,
        "edge_covariance_trace": str(covariance_trace),
        "edge_covariance_certificate": (
            "(494/3) sum weight*(v_i-v_j)(v_i-v_j)^T"
        ),
        "sharp_harmonic_rank_cuts": len(residuals),
        "minimum_rank_cut_kernel": minimum_rank_kernel,
        "minimum_rank_cut_residual": str(minimum_rank_residual),
        "band": [str(BAND_LOWER), str(BAND_UPPER)],
        "high_threshold": str(HIGH_THRESHOLD),
        "capacity": CAPACITY,
        "projected_height_square_lower": str(projected_height_square),
        "depth_slack": str(depth_slack),
        "cap_slack": str(cap_slack),
        "product_slack": str(product_slack),
        "scope": (
            "feasible relaxation witness, not a 41-point spherical code"
        ),
    }


if __name__ == "__main__":
    print(json.dumps(verify(), indent=2, sort_keys=True))
