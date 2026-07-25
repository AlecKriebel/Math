from __future__ import annotations

from collections import Counter, defaultdict
import importlib.util
import itertools
import json
from pathlib import Path
import tempfile
import unittest
from unittest import mock


HERE = Path(__file__).resolve().parent
PATH = HERE / "verify_fixed_support_obstruction.py"
SPEC = importlib.util.spec_from_file_location("verify_k9_fixed", PATH)
assert SPEC is not None and SPEC.loader is not None
VERIFY = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(VERIFY)


class FixedK8SupportK9Tests(unittest.TestCase):
    def test_core_against_independent_python_bruteforce(self) -> None:
        pairs8 = tuple(itertools.combinations(range(8), 2))
        pairs9 = tuple(itertools.combinations(range(9), 2))
        pair_index9 = {pair: index for index, pair in enumerate(pairs9)}
        k7_indices = tuple(
            index for index, (_i, j) in enumerate(pairs8) if j < 7
        )
        face_indices = tuple(
            tuple(
                pair_index9[tuple(sorted((vertices[i], vertices[j])))]
                for i, j in pairs8
            )
            for deleted in range(9)
            for vertices in [
                tuple(vertex for vertex in range(9) if vertex != deleted)
            ]
        )

        def orbit(representative: tuple[int, ...]) -> set[tuple[int, ...]]:
            by_pair = dict(zip(pairs8, representative, strict=True))
            return {
                tuple(
                    by_pair[tuple(sorted((permutation[i], permutation[j])))]
                    for i, j in pairs8
                )
                for permutation in itertools.permutations(range(8))
            }

        zero = (0,) * 28
        one_marked_edge = (1,) + (0,) * 27
        orbits = [orbit(zero), orbit(one_marked_edge)]
        support = set().union(*orbits)
        self.assertEqual(sum(map(len, orbits)), len(support))
        by_k7: dict[tuple[int, ...], list[tuple[int, ...]]] = defaultdict(list)
        for edges in support:
            key = tuple(edges[index] for index in k7_indices)
            by_k7[key].append(edges)
        compatible = 0
        for group in by_k7.values():
            for first in group:
                for second in group:
                    base = [-1] * 36
                    for position, color in zip(
                        face_indices[8], first, strict=True
                    ):
                        base[position] = color
                    for position, color in zip(
                        face_indices[7], second, strict=True
                    ):
                        if base[position] != -1:
                            self.assertEqual(base[position], color)
                        base[position] = color
                    self.assertEqual(base.count(-1), 1)
                    self.assertEqual(base[35], -1)
                    for color in range(7):
                        base[35] = color
                        candidate = tuple(base)
                        if all(
                            tuple(
                                candidate[index]
                                for index in face_indices[deleted]
                            )
                            in support
                            for deleted in range(9)
                        ):
                            compatible += 1
        group_sizes = Counter(map(len, by_k7.values()))
        ordered_pairs = sum(size * size for size in group_sizes.elements())
        expected = {
            "k8_orbits": 2,
            "labeled_k8_support": len(support),
            "orbit_size_distribution": dict(Counter(map(len, orbits))),
            "k7_overlap_keys": len(by_k7),
            "overlap_group_size_distribution": dict(group_sizes),
            "compatible_ordered_k8_face_pairs": ordered_pairs,
            "pre_support_k9_color_trials": 7 * ordered_pairs,
            "support_compatible_labeled_k9": compatible,
        }
        self.assertEqual(
            VERIFY.run_core([zero, one_marked_edge]),
            expected,
        )

    def test_core_on_constant_support(self) -> None:
        result = VERIFY.run_core([(0,) * 28])
        self.assertEqual(
            result,
            {
                "k8_orbits": 1,
                "labeled_k8_support": 1,
                "orbit_size_distribution": {1: 1},
                "k7_overlap_keys": 1,
                "overlap_group_size_distribution": {1: 1},
                "compatible_ordered_k8_face_pairs": 1,
                "pre_support_k9_color_trials": 7,
                "support_compatible_labeled_k9": 1,
            },
        )

    def test_exact_obstruction(self) -> None:
        result = VERIFY.verify()
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["support_compatible_labeled_k9"], 0)

    def test_tampered_source_hash_is_rejected(self) -> None:
        data = json.loads(VERIFY.CERTIFICATE_PATH.read_text())
        data["source_k8_sha256"] = "0" * 64
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "tampered.json"
            path.write_text(json.dumps(data))
            with mock.patch.object(VERIFY, "CERTIFICATE_PATH", path):
                with self.assertRaises(AssertionError):
                    VERIFY.verify()


if __name__ == "__main__":
    unittest.main()
