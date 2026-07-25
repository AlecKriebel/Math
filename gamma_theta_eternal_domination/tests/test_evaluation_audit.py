from __future__ import annotations

import csv
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path
import sys
import tempfile
import unittest


CAMPAIGN = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(CAMPAIGN / "src"))

from coverage_checker.graph import Graph  # noqa: E402
from evaluation_checker.audit import (  # noqa: E402
    CATEGORY_ALPHA,
    CATEGORY_ETERNAL,
    CATEGORY_GAMMA,
    CATEGORY_PRIVATE,
    EMPTY_SHA256,
    EvaluationAuditError,
    EvaluationPolicy,
    UNIQUE_HEADER,
    sha256_file,
    verify_certificate,
    write_certificate,
)
from evaluation_checker.math_core import find_private_obstruction  # noqa: E402


def cycle(order: int) -> Graph:
    return Graph.from_edges(
        order, ((vertex, (vertex + 1) % order) for vertex in range(order))
    )


def path(order: int) -> Graph:
    return Graph.from_edges(
        order, ((vertex, vertex + 1) for vertex in range(order - 1))
    )


def star(leaves: int) -> Graph:
    return Graph.from_edges(
        leaves + 1, ((0, vertex) for vertex in range(1, leaves + 1))
    )


def private_graph() -> Graph:
    return Graph.from_edges(
        7,
        (
            (1, 2),
            (1, 3),
            (0, 4),
            (3, 5),
            (4, 5),
            (0, 6),
            (3, 6),
        ),
    )


def base_row(graph: Graph, gamma: int, alpha: int, category: str) -> dict[str, str]:
    return {
        "canonical_graph6": graph.to_graph6(),
        "n": str(graph.order),
        "m": str(graph.size),
        "origin_count": "1",
        "first_host_id": "MMV-001",
        "first_neighborhood_mask": "1",
        "first_raw_graph6": graph.to_graph6(),
        "gamma": str(gamma),
        "alpha": str(alpha),
        "category": category,
        "private_obstruction_json": "",
        "eternal_a": "",
        "eternal_b": "",
        "family_a_size": "",
        "family_b_size": "",
        "family_a_sha256": "",
        "family_b_sha256": "",
    }


def fixture_rows() -> list[dict[str, str]]:
    gamma_row = base_row(star(3), 1, 3, CATEGORY_GAMMA)
    alpha_row = base_row(path(8), 3, 4, CATEGORY_ALPHA)
    eternal_row = base_row(cycle(7), 3, 3, CATEGORY_ETERNAL)
    private = private_graph()
    private_row = base_row(private, 3, 3, CATEGORY_PRIVATE)
    obstruction = find_private_obstruction(private, 3)
    if obstruction is None:
        raise AssertionError("test fixture lost private obstruction")
    state_mask, attacked, failed = obstruction
    private_row["private_obstruction_json"] = json.dumps(
        {
            "attack": attacked,
            "failed_guards": [
                {"guard": guard, "newly_undominated": witness}
                for guard, witness in failed
            ],
            "independent_set_mask": state_mask,
        },
        sort_keys=True,
        separators=(",", ":"),
    )
    for row in (eternal_row, private_row):
        row.update(
            {
                "eternal_a": "0",
                "eternal_b": "0",
                "family_a_size": "0",
                "family_b_size": "0",
                "family_a_sha256": EMPTY_SHA256,
                "family_b_sha256": EMPTY_SHA256,
            }
        )
    return sorted(
        (gamma_row, alpha_row, eternal_row, private_row),
        key=lambda row: row["canonical_graph6"],
    )


TEST_POLICY = EvaluationPolicy(
    expected_rows=4,
    expected_category_counts=(
        (CATEGORY_GAMMA, 1),
        (CATEGORY_ALPHA, 1),
        (CATEGORY_ETERNAL, 1),
        (CATEGORY_PRIVATE, 1),
    ),
)


class EvaluationCertificateTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        self.unique = self.root / "unique.csv"
        with self.unique.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=UNIQUE_HEADER)
            writer.writeheader()
            writer.writerows(fixture_rows())
        self.certificate = self.root / "certificate.ndjson"
        self.binding = {"unique_csv_sha256": sha256_file(self.unique)}
        self.summary = write_certificate(
            self.unique,
            self.certificate,
            binding=self.binding,
            source_manifest=(),
            policy=TEST_POLICY,
        )

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def test_round_trip_all_four_mathematical_categories(self) -> None:
        replay = verify_certificate(
            self.unique,
            self.certificate,
            binding=self.binding,
            source_manifest=(),
            policy=TEST_POLICY,
        )
        self.assertEqual(replay, self.summary)
        self.assertEqual(replay.row_count, 4)
        self.assertEqual(dict(replay.category_counts), dict(TEST_POLICY.expected_category_counts))

    def test_truncated_certificate_fails_closed(self) -> None:
        payload = self.certificate.read_bytes()
        self.certificate.write_bytes(payload[:-1])
        with self.assertRaises(EvaluationAuditError):
            verify_certificate(
                self.unique,
                self.certificate,
                binding=self.binding,
                source_manifest=(),
                policy=TEST_POLICY,
            )

    def test_tampered_row_certificate_fails_closed(self) -> None:
        lines = self.certificate.read_text(encoding="ascii").splitlines()
        for index in range(1, len(lines) - 1):
            record = json.loads(lines[index])
            if record["category"] == CATEGORY_GAMMA:
                record["dominating_mask"] = 0
                lines[index] = json.dumps(
                    record, sort_keys=True, separators=(",", ":")
                )
                break
        self.certificate.write_text(
            "\n".join(lines) + "\n", encoding="ascii"
        )
        with self.assertRaises(EvaluationAuditError):
            verify_certificate(
                self.unique,
                self.certificate,
                binding=self.binding,
                source_manifest=(),
                policy=TEST_POLICY,
            )

    def test_tampered_fixed_point_trace_fails_closed(self) -> None:
        lines = self.certificate.read_text(encoding="ascii").splitlines()
        for index in range(1, len(lines) - 1):
            record = json.loads(lines[index])
            if record["category"] == CATEGORY_ETERNAL:
                record["deletion_trace_sha256"] = "0" * 64
                lines[index] = json.dumps(
                    record, sort_keys=True, separators=(",", ":")
                )
                break
        self.certificate.write_text(
            "\n".join(lines) + "\n", encoding="ascii"
        )
        with self.assertRaises(EvaluationAuditError):
            verify_certificate(
                self.unique,
                self.certificate,
                binding=self.binding,
                source_manifest=(),
                policy=TEST_POLICY,
            )

    def test_input_byte_tamper_breaks_hash_binding(self) -> None:
        with self.unique.open("ab") as handle:
            handle.write(b"\n")
        self.assertNotEqual(
            sha256(self.unique.read_bytes()).hexdigest(),
            self.binding["unique_csv_sha256"],
        )
        with self.assertRaises(EvaluationAuditError):
            verify_certificate(
                self.unique,
                self.certificate,
                binding=self.binding,
                source_manifest=(),
                policy=TEST_POLICY,
            )

    def test_certificate_extra_data_fails_closed(self) -> None:
        with self.certificate.open("ab") as handle:
            handle.write(b"{}\\n")
        with self.assertRaises(EvaluationAuditError):
            verify_certificate(
                self.unique,
                self.certificate,
                binding=self.binding,
                source_manifest=(),
                policy=TEST_POLICY,
            )

    def test_wrong_category_count_prevents_generation(self) -> None:
        wrong_policy = EvaluationPolicy(
            expected_rows=4,
            expected_category_counts=(
                (CATEGORY_GAMMA, 2),
                (CATEGORY_ALPHA, 1),
                (CATEGORY_ETERNAL, 1),
            ),
        )
        with self.assertRaises(EvaluationAuditError):
            write_certificate(
                self.unique,
                self.root / "wrong.ndjson",
                binding=self.binding,
                source_manifest=(),
                policy=wrong_policy,
            )


class IndependenceBoundaryTests(unittest.TestCase):
    def test_runtime_modules_do_not_import_search_or_existing_verifiers(self) -> None:
        for relative in (
            "src/evaluation_checker/math_core.py",
            "src/evaluation_checker/audit.py",
        ):
            text = (CAMPAIGN / relative).read_text(encoding="utf-8")
            self.assertNotIn("from search", text)
            self.assertNotIn("import search", text)
            self.assertNotIn("from verifier_a", text)
            self.assertNotIn("from verifier_b", text)


if __name__ == "__main__":
    unittest.main()
