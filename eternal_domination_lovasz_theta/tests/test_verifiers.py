from __future__ import annotations

import copy
import json
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from verify_eternal import (  # noqa: E402
    DEFAULT_CERTIFICATE as ETERNAL_CERTIFICATE,
)
from verify_eternal import decode_graph6 as decode_eternal_graph6  # noqa: E402
from verify_eternal import verify_certificate as verify_eternal  # noqa: E402
from verify_theta_certificate import (  # noqa: E402
    DEFAULT_CERTIFICATE as THETA_CERTIFICATE,
)
from verify_theta_certificate import decode_graph6 as decode_theta_graph6  # noqa: E402
from verify_theta_certificate import verify_certificate as verify_theta  # noqa: E402


def load(path: Path) -> dict[str, object]:
    with path.open(encoding="utf-8") as stream:
        value = json.load(stream)
    if not isinstance(value, dict):
        raise TypeError("fixture root must be an object")
    return value


class ThetaCertificateTests(unittest.TestCase):
    def setUp(self) -> None:
        self.data = load(THETA_CERTIFICATE)

    def test_exact_certificate(self) -> None:
        result = verify_theta(self.data)
        self.assertEqual(result["objective"], "7593/2500")
        self.assertEqual(result["edge_zero_count"], 26)
        self.assertTrue(result["positive_definite"])

    def test_edge_mutation_is_rejected(self) -> None:
        broken = copy.deepcopy(self.data)
        broken["matrix"][0][3] = broken["matrix"][3][0] = 1
        with self.assertRaisesRegex(ValueError, "edge 0-3"):
            verify_theta(broken)

    def test_diagonal_mutation_is_rejected(self) -> None:
        broken = copy.deepcopy(self.data)
        broken["matrix"][0][0] -= 1
        with self.assertRaisesRegex(ValueError, "trace one"):
            verify_theta(broken)

    def test_two_decoders_agree(self) -> None:
        order, bitsets = decode_theta_graph6("IEhbtj{ro")
        sets = decode_eternal_graph6("IEhbtj{ro")
        self.assertEqual(order, len(sets))
        self.assertEqual(
            [
                {vertex for vertex in range(order) if mask & (1 << vertex)}
                for mask in bitsets
            ],
            [set(neighbors) for neighbors in sets],
        )

    def test_graph6_matches_frozen_edge_list(self) -> None:
        expected_edges = {
            (0, 3), (0, 4), (0, 7), (0, 8), (0, 9),
            (1, 3), (1, 5), (1, 6), (1, 8), (1, 9),
            (2, 4), (2, 5), (2, 6), (2, 7), (2, 8),
            (3, 6), (3, 7), (3, 8),
            (4, 6), (4, 8), (4, 9),
            (5, 7), (5, 8), (5, 9),
            (6, 9), (7, 9),
        }
        neighborhoods = decode_eternal_graph6("IEhbtj{ro")
        decoded_edges = {
            (first, second)
            for first, neighbors in enumerate(neighborhoods)
            for second in neighbors
            if first < second
        }
        self.assertEqual(decoded_edges, expected_edges)


class EternalCertificateTests(unittest.TestCase):
    def setUp(self) -> None:
        self.data = load(ETERNAL_CERTIFICATE)

    def test_exact_family(self) -> None:
        result = verify_eternal(self.data)
        self.assertEqual(result["gamma_infinity_one_guard"], 3)
        self.assertEqual(result["greatest_closed_family_size"], 86)
        self.assertEqual(result["verified_attack_pairs"], 602)
        self.assertEqual(result["fixed_point_sizes"], {1: 0, 2: 0, 3: 86})

    def test_removed_configuration_is_rejected(self) -> None:
        broken = copy.deepcopy(self.data)
        broken["family"].pop()
        with self.assertRaises(ValueError):
            verify_eternal(broken)

    def test_repeated_vertex_is_rejected(self) -> None:
        broken = copy.deepcopy(self.data)
        broken["family"][0] = [0, 0, 2]
        with self.assertRaisesRegex(ValueError, "repeats"):
            verify_eternal(broken)

    def test_graph_mutation_is_rejected(self) -> None:
        broken = copy.deepcopy(self.data)
        broken["graph6"] = "IEhbtn{ro"
        with self.assertRaises(ValueError):
            verify_eternal(broken)


if __name__ == "__main__":
    unittest.main()
