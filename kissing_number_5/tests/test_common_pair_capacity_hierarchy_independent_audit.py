"""Independent exact audit of the common-pair capacity hierarchy.

This test deliberately does not import the production verifier.  It rebuilds
the finite-support counts and rank-moment diagnostics directly from the JSON
certificates using only standard-library exact rational arithmetic.
"""

from fractions import Fraction as Q
from itertools import permutations
import json
from math import comb
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
CANDIDATE = (
    ROOT
    / "certificates"
    / "common_pair_capacity_degree4_pseudodistribution.json"
)
ALL_HARMONIC = (
    ROOT
    / "certificates"
    / "fixed41_bv_fullradial_k16_pseudodistribution.json"
)


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def capacity(p):
    if p > 1:
        return 0
    if p > Q(3, 4):
        return 1
    if p > Q(2, 3):
        return 2
    if p > Q(5, 8):
        return 3
    if p > Q(1, 2):
        return 4
    if p == Q(1, 2):
        return 6
    return None


def qualifying_edges(triple, nodes, a, b):
    """Count qualifying geometric base edges of a labeled triangle."""

    values = tuple(nodes[index] for index in triple)
    answer = 0
    for edge in range(3):
        other = tuple(index for index in range(3) if index != edge)
        answer += (
            values[edge] <= a
            and values[other[0]] >= b
            and values[other[1]] >= b
        )
    return answer


def fixed_coordinate_ordered_count(triple, nodes, a, b):
    """Enumerate all six vertex orders, retaining multiplicity.

    The edge values in ``triple`` are assigned to the labeled edges
    (01),(02),(12).  This enumeration continues to have six entries when
    two or all three edge colors agree.
    """

    edge_value = {
        frozenset((0, 1)): nodes[triple[0]],
        frozenset((0, 2)): nodes[triple[1]],
        frozenset((1, 2)): nodes[triple[2]],
    }
    answer = 0
    for x, y, z in permutations(range(3)):
        u = edge_value[frozenset((x, y))]
        v = edge_value[frozenset((x, z))]
        t = edge_value[frozenset((y, z))]
        answer += t <= a and u >= b and v >= b
    return answer


def hierarchy_rows(nodes, ordered_counts, triples):
    rows = []
    for a in (node for node in nodes if node <= 0):
        for b in (node for node in nodes if node > 0):
            if a == -1:
                p = None
                cap = 0
            else:
                p = 2 * b * b / (1 + a)
                cap = capacity(p)
            if cap is None:
                continue
            left = sum(
                Q(count) * qualifying_edges(triple, nodes, a, b)
                for triple, count in triples.items()
            )
            # ordered_counts/2 are the unordered edge multiplicities
            right = Q(cap, 2) * sum(
                count
                for node, count in zip(nodes, ordered_counts)
                if node <= a
            )
            rows.append((a, b, p, cap, left, right, right - left))
    return tuple(rows)


def triangle_determinant(values):
    u, v, t = values
    return 1 + 2 * u * v * t - u * u - v * v - t * t


def traces(nodes, ordered_counts, triples, kernel):
    diagonal = kernel(Q(1))
    values = tuple(kernel(node) for node in nodes)
    pair_square = sum(
        Q(count) * value * value
        for count, value in zip(ordered_counts, values)
    )
    trace_one = 41 * diagonal
    trace_two = 41 * diagonal * diagonal + pair_square
    trace_three = (
        41 * diagonal**3
        + 3 * diagonal * pair_square
        + 6
        * sum(
            Q(count) * values[i] * values[j] * values[k]
            for (i, j, k), count in triples.items()
        )
    )
    return trace_one, trace_two, trace_three


class CommonPairHierarchyIndependentAudit(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = load(CANDIDATE)
        cls.nodes = tuple(Q(value) for value in cls.data["nodes"])
        cls.ordered = tuple(cls.data["ordered_pair_counts"])
        cls.triples = {
            tuple(item["types"]): item["count"]
            for item in cls.data["triple_counts"]
        }

    def test_endpoint_capacity_table_and_sharp_models(self):
        expected = {
            Q(1): 1,
            Q(3, 4): 2,
            Q(2, 3): 3,
            Q(5, 8): 4,
            Q(1, 2): 6,
        }
        for p, bound in expected.items():
            self.assertEqual(capacity(p), bound)
            alpha = (Q(1, 2) - p) / (1 - p) if p != 1 else None
            if p == 1:
                continue
            self.assertEqual(
                alpha,
                {
                    Q(3, 4): -1,
                    Q(2, 3): Q(-1, 2),
                    Q(5, 8): Q(-1, 3),
                    Q(1, 2): 0,
                }[p],
            )
            # Equality-pattern residual Gram matrix:
            # antipodal pair, equilateral triangle, tetrahedron, orthoplex.
            if bound <= 4:
                residual_gram = [
                    [Q(1) if i == j else alpha for j in range(bound)]
                    for i in range(bound)
                ]
                eigenvalues = (
                    1 + (bound - 1) * alpha,
                    1 - alpha,
                )
                self.assertTrue(all(value >= 0 for value in eigenvalues))
                rank = (eigenvalues[0] != 0) + (bound - 1) * (
                    eigenvalues[1] != 0
                )
                self.assertLessEqual(rank, 3)
            else:
                # The six signed coordinate axes in R^3 have off-diagonal
                # inner products in {-1,0}.
                vectors = (
                    (1, 0, 0),
                    (-1, 0, 0),
                    (0, 1, 0),
                    (0, -1, 0),
                    (0, 0, 1),
                    (0, 0, -1),
                )
                self.assertTrue(
                    all(
                        sum(x * y for x, y in zip(vectors[i], vectors[j]))
                        <= 0
                        for i in range(6)
                        for j in range(i)
                    )
                )

        # With b=1/2, q=1/(2p)-1 realizes each equality endpoint in
        # the five-dimensional lift; q remains in the theorem's range.
        for p in (Q(1), Q(3, 4), Q(2, 3), Q(5, 8), Q(1, 2)):
            q = Q(1, 2) / p - 1
            self.assertTrue(-1 < q <= 0)
            self.assertEqual(2 * Q(1, 2) ** 2 / (1 + q), p)

        self.assertEqual(capacity(Q(3, 4) + Q(1, 10_000)), 1)
        self.assertEqual(capacity(Q(2, 3) + Q(1, 10_000)), 2)
        self.assertEqual(capacity(Q(5, 8) + Q(1, 10_000)), 3)
        self.assertEqual(capacity(Q(1, 2) + Q(1, 10_000)), 4)

    def test_candidate_mass_gram_and_orbit_normalization(self):
        self.assertEqual(sum(self.ordered), 41 * 40)
        self.assertTrue(all(count % 2 == 0 for count in self.ordered))
        self.assertEqual(sum(count // 2 for count in self.ordered), comb(41, 2))
        self.assertEqual(sum(self.triples.values()), comb(41, 3))

        incidences = tuple(
            sum(
                count * triple.count(color)
                for triple, count in self.triples.items()
            )
            for color in range(len(self.nodes))
        )
        self.assertEqual(
            incidences,
            tuple(39 * count // 2 for count in self.ordered),
        )
        self.assertEqual(incidences, (3315, 117, 5109, 12714, 10725))

        for triple in self.triples:
            values = tuple(self.nodes[index] for index in triple)
            self.assertTrue(all(-1 <= value <= 1 for value in values))
            self.assertGreaterEqual(triangle_determinant(values), 0)

        # Audit the factor two relating unordered base-edge incidences to
        # the fixed-coordinate ordered triple integral.  Explicit labeled
        # enumeration is important for repeated-color types 222, 333, 444,
        # 244, 344, and so on.
        for a in (node for node in self.nodes if node <= 0):
            for b in (node for node in self.nodes if node > 0):
                for triple in self.triples:
                    self.assertEqual(
                        fixed_coordinate_ordered_count(
                            triple, self.nodes, a, b
                        ),
                        2 * qualifying_edges(triple, self.nodes, a, b),
                    )

    def test_candidate_hierarchy_and_strongest_cut(self):
        """Reconstruct the cumulative threshold rows actually implemented."""

        rows = hierarchy_rows(self.nodes, self.ordered, self.triples)
        self.assertEqual(len(rows), 4)
        self.assertTrue(all(slack >= 0 for *_, slack in rows))
        strong = next(
            row
            for row in rows
            if row[0] == Q(-11, 25) and row[1] == Q(499, 1000)
        )
        self.assertEqual(
            strong,
            (
                Q(-11, 25),
                Q(499, 1000),
                Q(249001, 280000),
                1,
                Q(219),
                Q(219),
                Q(0),
            ),
        )
        all_negative = next(row for row in rows if row[0] == Q(-9, 100))
        self.assertEqual(
            all_negative,
            (
                Q(-9, 100),
                Q(499, 1000),
                Q(249001, 455000),
                4,
                Q(1643),
                Q(2180),
                Q(537),
            ),
        )
        # The saturated left side is exactly n_044+n_144+n_244.
        self.assertEqual(
            self.triples.get((0, 4, 4), 0)
            + self.triples.get((1, 4, 4), 0)
            + self.triples.get((2, 4, 4), 0),
            219,
        )

    def test_candidate_fails_stratified_universal_capacity_cuts(self):
        """Apply the pointwise theorem separately to each base color.

        A capacity bound for every base pair remains valid after summing over
        any selected subset of base pairs.  On a finite support, singleton
        colors are such subsets.  The candidate passes only the weaker
        cumulative rows because unused deeper edges subsidize shallower ones.
        """

        high = 4
        exact_color_rows = []
        for color, q in enumerate(self.nodes[:-1]):
            p = 2 * self.nodes[high] ** 2 / (1 + q)
            cap = capacity(p)
            self.assertIsNotNone(cap)
            left = sum(
                Q(count)
                * sum(
                    triple[position] == color
                    and all(
                        triple[other] == high
                        for other in range(3)
                        if other != position
                    )
                    for position in range(3)
                )
                for triple, count in self.triples.items()
            )
            right = Q(cap * self.ordered[color], 2)
            exact_color_rows.append(
                (color, q, p, cap, left, right, right - left)
            )

        self.assertEqual(
            exact_color_rows[2],
            (
                2,
                Q(-11, 25),
                Q(249001, 280000),
                1,
                Q(219),
                Q(131),
                Q(-88),
            ),
        )
        self.assertEqual(
            exact_color_rows[3],
            (
                3,
                Q(-9, 100),
                Q(249001, 455000),
                4,
                Q(1424),
                Q(1304),
                Q(-120),
            ),
        )

    def test_source_witnesses_and_seven_node_barrier(self):
        source = self.data["source_audits"]
        for stored in source["local_hybrid_witnesses"]:
            witness = load(ROOT / stored["file"])
            nodes = tuple(Q(value) for value in witness["nodes"])
            ordered = tuple(witness["ordered_pair_counts"])
            triples = {
                tuple(item["types"]): item["count"]
                for item in witness["triple_counts"]
            }
            rows = hierarchy_rows(nodes, ordered, triples)
            strong = next(
                row
                for row in rows
                if row[0] == Q(-11, 25)
                and row[1] == Q(499, 1000)
            )
            self.assertEqual(strong[4], Q(stored["strong_cut_left"]))
            self.assertEqual(strong[5], Q(stored["strong_cut_right"]))
            self.assertEqual(strong[6], Q(stored["slack"]))
            self.assertLess(strong[6], 0)

        harmonic = load(ALL_HARMONIC)
        nodes = tuple(Q(value) for value in harmonic["grid"])
        alpha = tuple(Q(value) for value in harmonic["alpha"])
        triples = tuple(tuple(item) for item in harmonic["triples"])
        weights = tuple(Q(value) for value in harmonic["nu"])
        self.assertEqual(sum(alpha), 40)
        self.assertEqual(sum(weights), 40 * 39)
        for triple in triples:
            values = tuple(nodes[index] for index in triple)
            self.assertGreaterEqual(triangle_determinant(values), 0)

        rows = []
        for a in (node for node in nodes if node <= 0):
            for b in (node for node in nodes if node > 0):
                if a == -1:
                    p, cap = None, 0
                else:
                    p = 2 * b * b / (1 + a)
                    cap = capacity(p)
                if cap is None:
                    continue
                # Each nu entry is the total normalized mass of its full
                # permutation orbit.  A fixed base-coordinate receives c/3.
                left = sum(
                    weight * qualifying_edges(triple, nodes, a, b) / 3
                    for triple, weight in zip(triples, weights)
                )
                right = cap * sum(
                    weight
                    for node, weight in zip(nodes, alpha)
                    if node <= a
                )
                rows.append((a, b, p, cap, left, right, right - left))
        positive = tuple(row[-1] for row in rows if row[-1] > 0)
        zero = tuple(row[-1] for row in rows if row[-1] == 0)
        self.assertEqual(len(rows), 7)
        self.assertEqual(len(positive), 4)
        self.assertEqual(len(zero), 3)
        self.assertEqual(
            min(positive), Q(155474701215499, 60000000000000)
        )

        # The corrected, pointwise-stratified hierarchy has the same number
        # of nontrivial rows here, but the exact q=-1/4, b=1/2 row fails.
        stratum_rows = []
        for base_color, a in enumerate(nodes):
            if a > 0:
                continue
            for b in (node for node in nodes if node > 0):
                if a == -1:
                    p, cap = None, 0
                else:
                    p = 2 * b * b / (1 + a)
                    cap = capacity(p)
                if cap is None:
                    continue
                left = sum(
                    weight
                    * sum(
                        triple[position] == base_color
                        and all(
                            nodes[triple[other]] >= b
                            for other in range(3)
                            if other != position
                        )
                        for position in range(3)
                    )
                    / 3
                    for triple, weight in zip(triples, weights)
                )
                right = cap * alpha[base_color]
                stratum_rows.append(
                    (base_color, a, b, p, cap, left, right, right - left)
                )
        self.assertEqual(len(stratum_rows), 7)
        failed = tuple(row for row in stratum_rows if row[-1] < 0)
        self.assertEqual(
            failed,
            (
                (
                    3,
                    Q(-1, 4),
                    Q(1, 2),
                    Q(2, 3),
                    3,
                    Q(722942322240113, 100000000000000),
                    Q(721699531533087, 100000000000000),
                    Q(-621395353513, 50000000000000),
                ),
            ),
        )

    def test_C047_and_centered_skew_scalings(self):
        pair_square = sum(
            Q(count, 41) * node * node
            for count, node in zip(self.ordered, self.nodes)
        )
        triple_cycle = sum(
            Q(6 * count, 41)
            * self.nodes[i]
            * self.nodes[j]
            * self.nodes[k]
            for (i, j, k), count in self.triples.items()
        )
        delta = pair_square - Q(36, 5)
        centered = (
            triple_cycle
            - Q(1116, 25)
            - Q(108, 5) * delta
        )
        normalized = 20 * centered**2 - 369 * delta**3
        spectral = 20 * (41 * centered) ** 2 - 9 * (41 * delta) ** 3
        stored = self.data["exact_diagnostics"]["rank_five_C047"]
        self.assertEqual(delta, Q(stored["delta"]))
        self.assertEqual(centered, Q(stored["centered_residual"]))
        self.assertEqual(
            normalized, Q(stored["normalized_polynomial_residual"])
        )
        self.assertEqual(
            spectral, Q(stored["spectral_polynomial_residual"])
        )
        self.assertEqual(spectral, 41**2 * normalized)
        self.assertLessEqual(normalized, 0)

        kernels = {
            "H0_over_6_plus_5H1_over_6": (
                6,
                lambda t: Q(1, 6) + Q(5, 6) * t,
            ),
            "H2": (14, lambda t: (5 * t * t - 1) / 4),
        }
        for name, (rank, kernel) in kernels.items():
            trace_one, trace_two, trace_three = traces(
                self.nodes, self.ordered, self.triples, kernel
            )
            variance = trace_two - trace_one**2 / rank
            centered_third = (
                trace_three
                - 3 * trace_one * trace_two / rank
                + 2 * trace_one**3 / rank**2
            )
            residual = (
                rank * (rank - 1) * centered_third**2
                - (rank - 2) ** 2 * variance**3
            )
            self.assertGreaterEqual(variance, 0)
            self.assertEqual(
                residual,
                Q(self.data["exact_diagnostics"]["centered_skew"][name]),
            )
            self.assertLessEqual(residual, 0)


if __name__ == "__main__":
    unittest.main()
