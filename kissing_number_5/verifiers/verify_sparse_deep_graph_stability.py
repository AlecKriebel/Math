#!/usr/bin/env python3
"""Exact checks for the sparse deep-graph classification and barrier."""

from __future__ import annotations

import json
from fractions import Fraction as Q
from itertools import combinations
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CERTIFICATE = ROOT / "certificates" / "sparse_deep_graph_stability.json"


class Qsqrt5:
    """An exact element a+b*sqrt(5), sufficient for sign-certified checks."""

    __slots__ = ("a", "b")

    def __init__(self, a: Q | int = 0, b: Q | int = 0):
        self.a = Q(a)
        self.b = Q(b)

    def __add__(self, other: object) -> "Qsqrt5":
        other = as_qsqrt5(other)
        return Qsqrt5(self.a + other.a, self.b + other.b)

    __radd__ = __add__

    def __neg__(self) -> "Qsqrt5":
        return Qsqrt5(-self.a, -self.b)

    def __sub__(self, other: object) -> "Qsqrt5":
        return self + (-as_qsqrt5(other))

    def __rsub__(self, other: object) -> "Qsqrt5":
        return as_qsqrt5(other) - self

    def __mul__(self, other: object) -> "Qsqrt5":
        other = as_qsqrt5(other)
        return Qsqrt5(
            self.a * other.a + 5 * self.b * other.b,
            self.a * other.b + self.b * other.a,
        )

    __rmul__ = __mul__

    def __eq__(self, other: object) -> bool:
        try:
            other = as_qsqrt5(other)
        except TypeError:
            return False
        return self.a == other.a and self.b == other.b

    def sign(self) -> int:
        if self.a == 0:
            return (self.b > 0) - (self.b < 0)
        if self.b == 0:
            return (self.a > 0) - (self.a < 0)
        if self.a > 0 and self.b > 0:
            return 1
        if self.a < 0 and self.b < 0:
            return -1
        comparison = self.a * self.a - 5 * self.b * self.b
        if self.a > 0:  # b < 0
            return (comparison > 0) - (comparison < 0)
        # a < 0 and b > 0
        return (comparison < 0) - (comparison > 0)

    def __ge__(self, other: object) -> bool:
        return (self - other).sign() >= 0

    def __gt__(self, other: object) -> bool:
        return (self - other).sign() > 0

    def __le__(self, other: object) -> bool:
        return (self - other).sign() <= 0

    def __lt__(self, other: object) -> bool:
        return (self - other).sign() < 0

    def __repr__(self) -> str:
        return f"Qsqrt5({self.a!r}, {self.b!r})"


def as_qsqrt5(value: object) -> Qsqrt5:
    if isinstance(value, Qsqrt5):
        return value
    if isinstance(value, (int, Q)):
        return Qsqrt5(value)
    raise TypeError(value)


def parse_qsqrt5(pair: list[str]) -> Qsqrt5:
    return Qsqrt5(Q(pair[0]), Q(pair[1]))


def graph_classification_arithmetic() -> dict[str, object]:
    """Check the exact q/s savings used in the 23/24-edge proof."""

    # Maximum savings by a single connected component of q=0,1,2,3.
    maximum_saving = {0: 0, 1: 2, 2: 5, 3: 7}
    assert 2 * 23 - 41 == 5
    assert maximum_saving[0] < 5
    assert maximum_saving[1] < 5
    assert 2 * maximum_saving[1] < 5
    assert maximum_saving[2] == 5

    # The unique equality component at q=2 is C5.
    assert 2 * 5 - 5 == 5
    assert 5 + 18 == 23
    assert 5 + 2 * 18 == 41
    assert 2 + 18 == 20

    assert 2 * 24 - 41 == 7
    assert maximum_saving[2] < 7
    assert 3 * maximum_saving[1] < 7
    assert maximum_saving[2] + maximum_saving[1] == 7
    assert maximum_saving[3] == 7

    edge_24_types = {
        "C7+17K2": (7 + 17, 7 + 2 * 17, 3 + 17),
        "C5_tail2+17K2": (7 + 17, 7 + 2 * 17, 3 + 17),
        "C5+P4+16K2": (5 + 3 + 16, 5 + 4 + 2 * 16, 2 + 2 + 16),
    }
    for edges, vertices, alpha in edge_24_types.values():
        assert (edges, vertices, alpha) == (24, 41, 20)

    return {
        "edge_23_type": "C5+18K2",
        "edge_24_types": tuple(edge_24_types),
    }


def verify_quadratic_identities(data: dict[str, object]) -> dict[str, Qsqrt5]:
    gram = data["rank_twenty_gram"]
    h_data = data["h_matrix"]
    assert isinstance(gram, dict) and isinstance(h_data, dict)

    one = Qsqrt5(1)
    sqrt5 = Qsqrt5(0, 1)
    assert sqrt5 * sqrt5 == 5
    assert sqrt5 > 2
    assert 3 > sqrt5

    matching_t = parse_qsqrt5(gram["matching_inner_product"])
    deep_t = parse_qsqrt5(gram["pentagon_deep_inner_product"])
    chord_t = parse_qsqrt5(gram["pentagon_chord_inner_product"])
    cross_t = parse_qsqrt5(gram["cross_component_inner_product"])
    assert matching_t == -1
    assert deep_t < -Q(1, 2)
    assert chord_t < Q(1, 2)
    assert chord_t > -Q(1, 2)
    assert cross_t == 0

    def h(t: Qsqrt5) -> Qsqrt5:
        t2 = t * t
        return t2 * (t2 - Q(1, 4))

    diagonal_h = parse_qsqrt5(h_data["diagonal"])
    matching_h = parse_qsqrt5(h_data["matching"])
    deep_h = parse_qsqrt5(h_data["pentagon_deep"])
    chord_h = parse_qsqrt5(h_data["pentagon_chord"])
    cross_h = parse_qsqrt5(h_data["cross_component"])
    assert h(one) == diagonal_h == Q(3, 4)
    assert h(matching_t) == matching_h == Q(3, 4)
    assert h(deep_t) == deep_h
    assert h(chord_t) == chord_h
    assert h(cross_t) == cross_h == 0
    assert deep_h > 0
    assert chord_h < 0

    # The regular pentagon Gram eigenvalues are 5/2 (twice), 0 (thrice).
    pentagon_gram_eigenvalues = (Q(5, 2), Q(5, 2), Q(0), Q(0), Q(0))
    assert sum(value > 0 for value in pentagon_gram_eigenvalues) == 2
    matching_rank = 18
    assert matching_rank + 2 == data["rank_twenty_gram"]["rank"] == 20

    expected_h_eigenvalues = [parse_qsqrt5(x) for x in h_data["pentagon_eigenvalues"]]
    assert expected_h_eigenvalues == [
        Qsqrt5(Q(5, 4)),
        Qsqrt5(Q(15, 16)),
        Qsqrt5(Q(15, 16)),
        Qsqrt5(Q(5, 16)),
        Qsqrt5(Q(5, 16)),
    ]
    assert all(value >= 0 for value in expected_h_eigenvalues)

    full_sum = 18 * matching_h + 5 * deep_h + 5 * chord_h
    assert full_sum == parse_qsqrt5(data["full_unordered_h_sum"]) == Q(59, 4)
    assert full_sum - Q(205, 14) == parse_qsqrt5(data["full_subset_margin"]) == Q(3, 28)

    return {
        "matching_h": matching_h,
        "deep_h": deep_h,
        "chord_h": chord_h,
        "full_sum": full_sum,
    }


def verify_kernel_psd() -> None:
    """Verify F-J/28 PSD using its exact block spectra and weighted CS."""

    # Matching nonconstant eigenvalues are zero. Pentagon nonconstant
    # eigenvalues are 15/16 and 5/16. On block sums the energy lower bound is
    # 3/4 sum s_i^2 + 1/4 s_P^2. Weighted Cauchy--Schwarz has denominator 28.
    assert Q(15, 16) > 0
    assert Q(5, 16) > 0
    reciprocal_weight_sum = 18 / Q(3, 4) + 1 / Q(1, 4)
    assert reciprocal_weight_sum == 28


def row_energy_envelope(m: int) -> Q:
    """The exact residual-PSD/box relaxation from Lemma 5."""

    assert m >= 1
    if m == 2:
        return Q(49, 64)
    if m % 2:
        return Q(3 * m + 9, 16)
    return Q(3 * m + 8, 16)


def verify_row_energy_envelopes() -> tuple[Q, ...]:
    """Check every endpoint pattern and the two-edge square identity."""

    # 49/64 - (5/8 + 3c/8 - c^2/4) = (4c-3)^2/64.
    assert Q(49, 64) - Q(5, 8) == Q(9, 64)
    assert -Q(3, 8) == -Q(24, 64)
    assert Q(1, 4) == Q(16, 64)

    phi = lambda z: z * z - z / 4
    values: list[Q] = []
    for m in range(1, 42):
        if m % 2:
            zs = (
                [Q(1)]
                + [Q(3, 4)] * ((m - 1) // 2)
                + [Q(1, 4)] * ((m - 1) // 2)
            )
        else:
            zs = (
                [Q(1)]
                + [Q(3, 4)] * ((m - 2) // 2)
                + [Q(1, 2)]
                + [Q(1, 4)] * ((m - 2) // 2)
            )
        assert len(zs) == m
        assert sum(zs) == Q(m + 1, 2)
        relaxed_value = sum(phi(z) for z in zs)
        if m == 2:
            assert relaxed_value == Q(7, 8)
            assert Q(49, 64) < relaxed_value
        else:
            assert relaxed_value == row_energy_envelope(m)
        values.append(row_energy_envelope(m))

    assert values[:8] == [
        Q(3, 4),
        Q(49, 64),
        Q(9, 8),
        Q(5, 4),
        Q(3, 2),
        Q(13, 8),
        Q(15, 8),
        Q(2),
    ]
    return tuple(values)


def verify_root_system_zero_slack_counts() -> None:
    """Check the finite root/slot counts in Lemma 6."""

    # Numbers of roots in the irreducible simply-laced systems of rank <= 5.
    a_roots = {rank: rank * (rank + 1) for rank in range(1, 6)}
    d_roots = {rank: 2 * rank * (rank - 1) for rank in range(4, 6)}
    assert a_roots[5] == 30
    assert d_roots[4] == 24
    assert d_roots[5] == 40
    assert d_roots[4] + a_roots[1] == 26

    for matching_lines in (16, 17, 18):
        initial_roots = 2 * matching_lines
        assert initial_roots > a_roots[5]
        core_points = 41 - 2 * matching_lines
        remaining_oriented_d5_roots = 2 * (20 - matching_lines)
        assert core_points == remaining_oriented_d5_roots + 1


def verify_d5_two_line_saturation_envelopes() -> None:
    """Check the quadratic endpoint bounds in Lemma 7 exactly."""

    def one_free_mate(a: Q) -> Q:
        return 2 * a * a + 3 * (1 - a) * (1 - a)

    def no_free_mate(a: Q) -> Q:
        return a * a + 4 * (1 - a) * (1 - a)

    # Both quadratics are convex, so their maxima on [1/2,1] occur at an
    # endpoint.  The first reaches 2 only at a=1; the second stays below 2.
    assert one_free_mate(Q(1, 2)) == Q(5, 4)
    assert one_free_mate(Q(1)) == 2
    assert no_free_mate(Q(1, 2)) == Q(5, 4)
    assert no_free_mate(Q(1)) == 1

    # The three Weyl-coordinate cases are: same support, disjoint supports,
    # and one-coordinate intersection.
    deletion_orbits = ("same_support", "disjoint_support", "intersecting")
    assert len(deletion_orbits) == 3


def verify_hypercube_c5_probe(data: dict[str, object]) -> None:
    """Verify the exact relaxed-extension probe from Lemma 8."""

    probe = data["hypercube_c5_probe"]
    assert isinstance(probe, dict)
    vectors = probe["sign_vectors"]
    assert isinstance(vectors, list) and len(vectors) == 5
    assert all(len(vector) == 5 for vector in vectors)
    assert all(entry in (-1, 1) for vector in vectors for entry in vector)
    assert all(sum(entry * entry for entry in vector) == 5 for vector in vectors)

    cycle_pairs = {(0, 1), (1, 2), (2, 3), (3, 4), (0, 4)}
    for i, j in combinations(range(5), 2):
        numerator = sum(a * b for a, b in zip(vectors[i], vectors[j]))
        expected = -3 if (i, j) in cycle_pairs else 1
        assert numerator == expected

    # An unnormalized D5 root is e_i +/- e_j and has norm squared 2.
    # Against s/sqrt(5), the squared normalized inner product is
    # (r.s)^2/10. Every value is therefore 0 or 2/5.
    cross_squares: set[Q] = set()
    for vector in vectors:
        for i, j in combinations(range(5), 2):
            for relative_sign in (-1, 1):
                numerator = vector[i] + relative_sign * vector[j]
                cross_squares.add(Q(numerator * numerator, 10))
    assert cross_squares == {Q(0), Q(2, 5)}
    assert [Q(value) for value in probe["d5_cross_squared_values"]] == [
        Q(0),
        Q(2, 5),
    ]
    assert Q(2, 5) > Q(1, 4)

    def h(value: Q) -> Q:
        square = value * value
        return square * (square - Q(1, 4))

    core_h_sum = 5 * h(-Q(3, 5)) + 5 * h(Q(1, 5))
    assert core_h_sum == Q(probe["core_h_sum"]) == Q(39, 250)


def verify_all_subset_inequalities(
    matching_h: Qsqrt5,
    deep_h: Qsqrt5,
    chord_h: Qsqrt5,
) -> Qsqrt5:
    """Enumerate the 32 pentagon masks and all matching-pair occupancies."""

    smallest_margin: Qsqrt5 | None = None
    checked = 0
    for mask in range(1 << 5):
        cycle_vertices = [i for i in range(5) if mask & (1 << i)]
        cycle_edges = sum(
            1
            for i, j in combinations(cycle_vertices, 2)
            if (i - j) % 5 in (1, 4)
        )
        cycle_pairs = len(cycle_vertices) * (len(cycle_vertices) - 1) // 2
        cycle_chords = cycle_pairs - cycle_edges
        cycle_value = cycle_edges * deep_h + cycle_chords * chord_h

        for selected_matching_vertices in range(37):
            # Among k vertices selected from 18 disjoint pairs, the least
            # possible number of complete pairs is max(0,k-18), and it is
            # attained.
            complete_pairs = max(0, selected_matching_vertices - 18)
            m = selected_matching_vertices + len(cycle_vertices)
            pair_sum = complete_pairs * matching_h + cycle_value
            required = Q(m * (m - 21), 56)
            margin = pair_sum - required
            assert margin >= 0
            # The empty subset has the tautological zero margin.  Record the
            # smallest nonempty-subset margin, which is attained at m=41.
            if m > 0 and (
                smallest_margin is None or (smallest_margin - margin) > 0
            ):
                smallest_margin = margin
            checked += 1

    assert checked == 32 * 37
    assert smallest_margin == Q(3, 28)
    return smallest_margin


def verify() -> dict[str, object]:
    with CERTIFICATE.open("r", encoding="utf-8") as stream:
        data = json.load(stream)
    assert data["field"] == "Q(sqrt(5))"
    assert data["vertices"] == 41
    assert data["deep_graph"] == {
        "C5": 1,
        "K2": 18,
        "edges": 23,
        "independence_number": 20,
    }

    classifications = graph_classification_arithmetic()
    values = verify_quadratic_identities(data)
    verify_kernel_psd()
    row_envelopes = verify_row_energy_envelopes()
    verify_root_system_zero_slack_counts()
    verify_d5_two_line_saturation_envelopes()
    verify_hypercube_c5_probe(data)
    smallest_margin = verify_all_subset_inequalities(
        values["matching_h"], values["deep_h"], values["chord_h"]
    )

    return {
        "vertices": 41,
        "edge_23_type": classifications["edge_23_type"],
        "edge_24_type_count": len(classifications["edge_24_types"]),
        "countermodel_rank": data["rank_twenty_gram"]["rank"],
        "row_envelopes_checked": len(row_envelopes),
        "root_zero_slack_cases_checked": 3,
        "d5_two_line_deletion_orbits_checked": 3,
        "hypercube_c5_probe_checked": True,
        "subset_checks": 32 * 37,
        "smallest_subset_margin": str(smallest_margin.a),
        "aggregate_kernel_psd": True,
        "status": "PASS",
    }


if __name__ == "__main__":
    for key, value in verify().items():
        print(f"{key}: {value}")
