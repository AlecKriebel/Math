#!/usr/bin/env python3
"""Tests for the independent E=3/E=4 closure partition checker."""

from __future__ import annotations

import hashlib
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "verify"))

import e2_low_closure_partition_independent_check as audit  # noqa: E402


def disjoint_cliques(sizes: tuple[int, ...]) -> tuple[int, ...]:
    adjacency = [0] * audit.ORDER
    first = 0
    for size in sizes:
        for left in range(first, first + size):
            for right in range(left + 1, first + size):
                adjacency[left] |= 1 << right
                adjacency[right] |= 1 << left
        first += size
    return tuple(adjacency)


class IndependentClosurePartitionTests(unittest.TestCase):
    def test_graph6_round_trip_and_complement_involution(self) -> None:
        for adjacency in (
            tuple([0] * audit.ORDER),
            disjoint_cliques((5,)),
            disjoint_cliques((6, 5, 4)),
        ):
            encoded = audit.encode_graph6(adjacency)
            self.assertEqual(audit.decode_graph6(encoded), adjacency)
            dual = audit.graph_complement(adjacency)
            self.assertEqual(audit.graph_complement(dual), adjacency)
            self.assertEqual(
                audit.decode_graph6(audit.encode_graph6(dual)), dual
            )

    def test_exact_conflict_enumerator(self) -> None:
        clique, independent = audit.conflicts(disjoint_cliques((5,)))
        self.assertEqual(len(clique), 1)
        self.assertGreater(len(independent), 0)
        clique, _independent = audit.conflicts(disjoint_cliques((6,)))
        self.assertEqual(len(clique), 6)
        clique, _independent = audit.conflicts(
            disjoint_cliques((5, 5, 4))
        )
        self.assertEqual(len(clique), 2)

    def test_post_flip_height_matches_direct_recount(self) -> None:
        adjacency = disjoint_cliques((6, 5, 4))
        clique, independent = audit.conflicts(adjacency)
        for left, right in ((0, 1), (0, 6), (20, 42)):
            predicted = audit.exact_post_flip_height(
                adjacency, clique, independent, left, right
            )
            changed = audit.toggled(adjacency, left, right)
            after_clique, after_independent = audit.conflicts(changed)
            self.assertEqual(
                predicted, len(after_clique) + len(after_independent)
            )

    def test_shortg_verbose_parser(self) -> None:
        text = """
>A shortg -gtv input output
  1 : 1 4 7
      9 10
  2 : 2 3
      5 6 8
>Z 2 graphs written
"""
        self.assertEqual(
            audit.parse_shortg_verbose(text),
            ((1, 4, 7, 9, 10), (2, 3, 5, 6, 8)),
        )

    def test_augmented_partition_binding(self) -> None:
        # raw 1..4, duals 5..8, reps 9..10, rep duals 11..12.
        # Four ordinary classes pair into two complement classes.
        groups = (
            (1, 6, 9),
            (2, 5, 11),
            (3, 8, 10),
            (4, 7, 12),
        )
        result = audit.analyze_augmented_partition(groups, 4, 2)
        self.assertTrue(result["valid"])
        self.assertEqual(result["augmented_ordinary_class_count"], 4)
        self.assertEqual(result["raw_complement_class_count"], 2)
        self.assertEqual(
            result["raw_complement_class_size_histogram"],
            {"2": 2},
        )

    def test_augmented_partition_rejects_misbound_representatives(self) -> None:
        # The representative complements are deliberately swapped between
        # the two complement-isomorphism classes.
        groups = (
            (1, 6, 9),
            (2, 5, 12),
            (3, 8, 10),
            (4, 7, 11),
        )
        result = audit.analyze_augmented_partition(groups, 4, 2)
        self.assertFalse(result["valid"])
        self.assertFalse(
            result[
                "each_class_has_one_published_representative_and_its_complement"
            ]
        )

    def test_recorded_output_path_normalization_is_strict(self) -> None:
        with tempfile.TemporaryDirectory() as directory_name:
            project_root = Path(directory_name) / "ramsey55"
            planned = "results/constructive/run/output.g6"
            artifact = project_root / planned
            artifact.parent.mkdir(parents=True)
            artifact.write_text("placeholder\n", encoding="ascii")
            accepted = (
                planned,
                f"ramsey55/{planned}",
                str(artifact.resolve()),
            )
            for observed in accepted:
                with self.subTest(observed=observed):
                    self.assertTrue(
                        audit.recorded_output_matches_artifact(
                            observed=observed,
                            planned=planned,
                            artifact=artifact,
                            project_root=project_root,
                        )
                    )
            for observed in (
                f"other-project/{planned}",
                "results/constructive/run/other.g6",
                None,
            ):
                with self.subTest(observed=observed):
                    self.assertFalse(
                        audit.recorded_output_matches_artifact(
                            observed=observed,
                            planned=planned,
                            artifact=artifact,
                            project_root=project_root,
                        )
                    )
            self.assertFalse(
                audit.recorded_output_matches_artifact(
                    observed=planned,
                    planned="results/constructive/run/other.g6",
                    artifact=artifact,
                    project_root=project_root,
                )
            )

    def test_frozen_git_blob_binds_named_commit(self) -> None:
        commit, blob = audit.frozen_git_blob(
            ROOT.parent,
            "5677276e8135daec5af9fb09e360ec9b8a8dfe79",
            Path("ramsey55/src/search43_e2_barrier_escape.cpp"),
        )
        self.assertEqual(
            commit, "5677276e8135daec5af9fb09e360ec9b8a8dfe79"
        )
        self.assertEqual(
            hashlib.sha256(blob).hexdigest(),
            "cdddaef4c35dfb9ccdbcc7478029c15eb909247714ffc2bef9e8fa636fb0099c",
        )

    def test_ordered_seed_corpus_hash_is_order_sensitive(self) -> None:
        with tempfile.TemporaryDirectory() as directory_name:
            directory = Path(directory_name)
            left = directory / "left.g6"
            right = directory / "right.g6"
            left.write_bytes(b"left\n")
            right.write_bytes(b"right\n")
            self.assertEqual(
                audit.ordered_seed_corpus_sha256([left, right]),
                hashlib.sha256(b"left\nright\n").hexdigest(),
            )
            self.assertNotEqual(
                audit.ordered_seed_corpus_sha256([left, right]),
                audit.ordered_seed_corpus_sha256([right, left]),
            )
            right.write_bytes(b"right\nextra\n")
            with self.assertRaises(ValueError):
                audit.ordered_seed_corpus_sha256([left, right])


if __name__ == "__main__":
    unittest.main()
