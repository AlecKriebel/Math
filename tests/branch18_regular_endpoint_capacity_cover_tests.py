#!/usr/bin/env python3
"""Focused tests for the independent endpoint-capacity reconstruction."""

from __future__ import annotations

import ast
import sys
import tempfile
import unittest
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "verify"))

import branch18_regular_endpoint_capacity_cover_check as checker  # noqa: E402


class EndpointCapacityCoverTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        (
            cls.a_payload,
            cls.h_payload,
            cls.a_profiles,
            cls.h_profiles,
            cls.full_h_edge_histogram,
            cls.selected_h_digest,
        ) = checker.reconstruct_catalogs(ROOT)
        cls.classification = checker.reconstruct_classification(
            cls.a_profiles, cls.h_profiles
        )
        cls.exceptional = cls.a_profiles[checker.EXPECTED_EXCEPTIONAL_A]
        (
            cls.classification_payload,
            cls.classification_summary,
            cls.terminal_summary,
        ) = checker.reconstruct_classification_stream(
            cls.a_profiles,
            cls.h_profiles,
            (
                "certificates/"
                "branch18_regular_endpoint_capacity_cover_v1.pairs"
            ),
        )

    def test_checker_does_not_import_producer(self) -> None:
        source = (
            ROOT
            / "verify/branch18_regular_endpoint_capacity_cover_check.py"
        ).read_text(encoding="utf-8")
        tree = ast.parse(source)
        imported: set[str] = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imported.update(alias.name for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                imported.add(node.module)
        self.assertNotIn(
            "branch18_regular_endpoint_capacity_cover", imported
        )

    def test_catalog_bindings_and_endpoint_selection(self) -> None:
        self.assertEqual(len(self.a_payload), checker.A_BYTES)
        self.assertEqual(checker.sha256(self.a_payload), checker.A_SHA256)
        self.assertEqual(len(self.h_payload), checker.H_BYTES)
        self.assertEqual(checker.sha256(self.h_payload), checker.H_SHA256)
        self.assertEqual(len(self.a_profiles), 74)
        self.assertEqual(len(self.h_profiles), 843)
        self.assertEqual(
            self.selected_h_digest,
            "2fe5a0505c0b6b252caaeee1c35d866a538567c0731aa9616734a444a880db5d",
        )
        self.assertEqual(
            sum(self.full_h_edge_histogram.values()), 352_366
        )

    def test_cross_neighborhood_identity(self) -> None:
        for h_degree in range(8, 13):
            self.assertEqual(
                18 - (23 - h_degree),
                h_degree - 5,
            )

    def test_capacity_double_counting_semantics(self) -> None:
        # If Q is an independent triple of A, the H vertices whose
        # cross-neighborhoods miss Q must be independent in H: an H-edge
        # between two of them would combine with Q to form I5 in G.
        # Every selected H has no independent set of size five.
        for h_profile in self.h_profiles[:8]:
            self.assertFalse(
                checker.has_clique(
                    checker.complement(h_profile.adjacency), 5
                )
            )
        self.assertEqual(
            4 * len(self.exceptional.independent3),
            296,
        )

    def test_exceptional_a_capacity_profile(self) -> None:
        a = self.exceptional
        self.assertEqual(a.index, 50)
        self.assertEqual(len(a.independent3), 74)
        self.assertEqual(len(a.independent4), 23)
        expected = {
            3: (0, None, 0),
            4: (0, None, 0),
            5: (30, 17, 10),
            6: (569, 10, 1),
            7: (3640, 7, 63),
        }
        self.assertEqual(
            {
                size: (
                    a.minimum(size).candidate_count,
                    a.minimum(size).value,
                    len(a.minimum(size).minimizers),
                )
                for size in range(3, 8)
            },
            expected,
        )

    def test_exceptional_q5_minimizers_are_exact(self) -> None:
        actual = [
            checker.vertices(mask, checker.A_ORDER)
            for mask in self.exceptional.minimum(5).minimizers
        ]
        self.assertEqual(
            actual,
            [
                [2, 3, 4, 12, 14],
                [2, 3, 4, 12, 15],
                [2, 4, 6, 9, 11],
                [2, 4, 7, 9, 11],
                [3, 8, 9, 11, 12],
                [3, 9, 10, 11, 12],
                [5, 6, 8, 9, 11],
                [5, 6, 9, 10, 11],
                [5, 7, 8, 9, 11],
                [5, 7, 9, 10, 11],
            ],
        )

    def test_exceptional_q6_minimizer_is_unique_and_semantic(self) -> None:
        q6 = self.exceptional.minimum(6)
        self.assertEqual(q6.value, 10)
        self.assertEqual(len(q6.minimizers), 1)
        minimizer = q6.minimizers[0]
        self.assertEqual(
            checker.vertices(minimizer, checker.A_ORDER),
            [2, 3, 4, 9, 11, 12],
        )
        self.assertTrue(
            checker.hits_every(minimizer, self.exceptional.independent4)
        )
        missed = [
            triple
            for triple in self.exceptional.independent3
            if minimizer & triple == 0
        ]
        self.assertEqual(len(missed), 10)
        self.assertEqual(
            checker.minimizer_stream_sha256(
                self.exceptional.minimum(5)
            ),
            "99cf8c6d83a46b8b68e67df2b592a5d5ab5118bad84764fa6bdaafef3bc684cb",
        )
        self.assertEqual(
            checker.minimizer_stream_sha256(q6),
            "0fac5312b98a3fef21dc66e22e8daeb8833fef3a922abe286ee5bfcbb228a797",
        )

    def test_strict_capacity_count_and_equality_survivors(self) -> None:
        kinds = self.classification["kind_histogram"]
        self.assertEqual(
            kinds["STRICT_INFINITE"] + kinds["STRICT_FINITE"],
            61_939,
        )
        self.assertEqual(kinds["EQUALITY"], 443)
        self.assertEqual(kinds["SLACK"], 0)
        self.assertEqual(
            self.classification["strict_count"], 61_939
        )
        self.assertEqual(
            len(self.classification["equality_pairs"]), 443
        )

    def test_every_equality_survivor_is_exceptional_a_and_exact_shape(
        self,
    ) -> None:
        equality_pairs = self.classification["equality_pairs"]
        self.assertEqual({pair[0] for pair in equality_pairs}, {50})
        self.assertEqual(
            Counter(
                self.h_profiles[pair[1]].size_histogram
                for pair in equality_pairs
            ),
            Counter({(0, 0, 8, 16, 0): 443}),
        )
        for a_index, h_index, decision in equality_pairs:
            self.assertEqual(a_index, 50)
            self.assertEqual(decision.lower_bound, 296)
            self.assertEqual(decision.capacity, 296)
            self.assertEqual(
                self.h_profiles[h_index].size_count(5), 8
            )
            self.assertEqual(
                self.h_profiles[h_index].size_count(6), 16
            )

    def test_every_equality_survivor_has_terminal_contradiction(self) -> None:
        witnesses = self.classification["terminal_witnesses"]
        self.assertEqual(len(witnesses), 443)
        unique = self.exceptional.minimum(6).minimizers[0]
        for a_index, h_index, witness in witnesses:
            self.assertEqual(a_index, 50)
            h_profile = self.h_profiles[h_index]
            left, right = witness.high_edge
            self.assertTrue(
                h_profile.adjacency[left] & (1 << right)
            )
            self.assertEqual(h_profile.degrees[left] - 5, 6)
            self.assertEqual(h_profile.degrees[right] - 5, 6)
            self.assertEqual(witness.forced_minimizer, unique)
            self.assertIn(
                witness.missed_independent_triple,
                self.exceptional.independent3,
            )
            self.assertEqual(
                unique & witness.missed_independent_triple, 0
            )

    def test_classification_stream_is_complete_and_semantic(self) -> None:
        self.assertEqual(
            self.classification_summary["record_count"], 62_382
        )
        self.assertEqual(
            self.classification_summary["capacity_exclusion_count"],
            61_939,
        )
        self.assertEqual(
            self.classification_summary["terminal_exclusion_count"], 443
        )
        self.assertEqual(
            self.classification_summary["retained_pair_count"], 0
        )
        self.assertEqual(
            self.classification_summary["sha256"],
            "3c72e75506a43bed6ca44213c5bf540f0370c39b85597259738709fd2345c785",
        )
        self.assertEqual(
            self.classification_payload.count(b"\n"), 62_382
        )
        errors: list[str] = []
        checker.validate_classification_lines(
            errors,
            self.classification_payload,
            self.a_profiles,
            self.h_profiles,
        )
        self.assertEqual(errors, [])

    def test_classification_parser_rejects_tampering(self) -> None:
        tampered = self.classification_payload.replace(
            b"C=TERM", b"C=XXXX", 1
        )
        self.assertNotEqual(tampered, self.classification_payload)
        errors: list[str] = []
        checker.validate_classification_lines(
            errors,
            tampered,
            self.a_profiles,
            self.h_profiles,
        )
        self.assertTrue(errors)

    def test_profile_and_terminal_streams_are_bound(self) -> None:
        profile_payload = b"".join(
            checker.a_profile_line(profile)
            for profile in self.a_profiles
        )
        self.assertEqual(
            checker.sha256(profile_payload),
            "4248b1d945f8cad5d1520e3e0de44f252daf2f64bee19db2c6c8cb67a622c932",
        )
        self.assertEqual(
            self.terminal_summary["terminal_H_record_count"], 443
        )
        self.assertEqual(
            self.terminal_summary["terminal_line_stream_sha256"],
            "c1b1aec885366baefee5ec4e5c8deeb4c3339fc62ceb1ae415ed8c60796fa05d",
        )
        self.assertEqual(
            self.terminal_summary[
                "terminal_H_cover_index_stream_sha256"
            ],
            "7f4c0b51edfe036e544b300e2e3150b755dd91c0a0966678607bf5dab01cdc08",
        )
        self.assertEqual(
            sum(
                self.terminal_summary[
                    "minimum_degree_inside_degree_11_set_histogram"
                ].values()
            ),
            443,
        )

    def test_graph6_decoder_rejects_noncanonical_padding(self) -> None:
        record = self.exceptional.record
        bad = bytearray(record)
        bad[-1] = ((bad[-1] - 63) | 1) + 63
        with self.assertRaises(ValueError):
            checker.decode_graph6(bytes(bad), 18)
        with self.assertRaises(ValueError):
            checker.decode_graph6(record[:-1], 18)

    def test_confined_path_rejects_escape(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            self.assertEqual(
                checker.confined_path(root, "inside/file"),
                root / "inside/file",
            )
            with self.assertRaises(ValueError):
                checker.confined_path(root, "../outside")

    def test_full_artifact_passes_independent_audit(self) -> None:
        manifest = (
            ROOT
            / "results/benchmark_plans/"
            "branch18_regular_endpoint_capacity_cover_v1.json"
        )
        self.assertTrue(manifest.is_file())
        report = checker.audit(ROOT, manifest)
        self.assertTrue(report["valid"], report["errors"])
        reconstructed = report["capacity_reconstruction"]
        self.assertEqual(
            reconstructed["strict_capacity_exclusion_count"], 61_939
        )
        self.assertEqual(
            reconstructed["terminal_exclusion_count"], 443
        )
        self.assertEqual(reconstructed["retained_pair_count"], 0)

    def test_saved_check_report_is_valid_and_source_bound(self) -> None:
        check_path = (
            ROOT
            / "results/verification/"
            "branch18_regular_endpoint_capacity_cover_v1.check.json"
        )
        manifest_path = (
            ROOT
            / "results/benchmark_plans/"
            "branch18_regular_endpoint_capacity_cover_v1.json"
        )
        self.assertTrue(check_path.is_file())
        report = checker.load_canonical_json(check_path.read_bytes())
        self.assertIsInstance(report, dict)
        self.assertTrue(report["valid"], report["errors"])
        self.assertEqual(
            report["manifest_sha256"],
            checker.sha256(manifest_path.read_bytes()),
        )
        self.assertEqual(
            report["checker_source_sha256"],
            checker.sha256(
                (
                    ROOT
                    / "verify/"
                    "branch18_regular_endpoint_capacity_cover_check.py"
                ).read_bytes()
            ),
        )


if __name__ == "__main__":
    unittest.main()
