from __future__ import annotations

import json
import sys
import tempfile
import unittest
from collections import Counter
from pathlib import Path
from unittest.mock import patch


CAMPAIGN = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(CAMPAIGN / "src"))

from synthesis_k3.cegar import parse_dimacs_bytes  # noqa: E402
from synthesis_k3.encoding import build_k3_encoding  # noqa: E402
from synthesis_k3.hole5_signature_breaker import (  # noqa: E402
    ADJACENT_FREE_PAIRS,
    BREAKER_NAME,
    COMPARATOR_CLAUSES_PER_PAIR,
    COMPARATOR_LITERAL_COUNT_PER_PAIR,
    CORE_VERTICES,
    EXPECTED_BREAKER_CLAUSE_COUNT,
    EXPECTED_BREAKER_LITERAL_COUNT,
    EXPECTED_BREAKER_SHA256,
    EXPECTED_DERIVED_CLAUSE_COUNT,
    EXPECTED_DERIVED_CNF_SHA256,
    EXPECTED_DERIVED_LITERAL_COUNT,
    EXPECTED_DERIVED_VARIABLE_COUNT,
    EXPECTED_SOURCE_CLAUSE_COUNT,
    FREE_VERTICES,
    _derive_cnf_bytes,
    audit_derived_package,
    breaker_clause_stream_bytes,
    covariance_audit,
    exhaustive_comparator_audit,
    generate_derived_package,
    lexicographic_leq_clauses,
    relabel_clause,
    signature_breaker_clauses,
    signature_variables,
    variable_relabeling,
)
from synthesis_k3.template_color_bank import (  # noqa: E402
    CNF_NAME,
    MANIFEST_NAME,
    sha256_bytes,
)


SOURCE_PACKAGE = (
    CAMPAIGN / "results/synthesis_k3_template_bank_packages/hole5"
)


def fake_git_binding(
    sources: object,
    *,
    head: str | None = None,
) -> dict[str, object]:
    del sources
    return {
        "head_commit": "a" * 40 if head is None else head,
        "repository_relative_campaign_path": "gamma_theta_eternal_domination",
        "runtime_sources_match_head": True,
        "runtime_source_mismatches": [],
        "global_worktree_cleanliness_required": False,
    }


class ComparatorTests(unittest.TestCase):
    def test_exact_counts_variables_and_exhaustive_truth_tables(self) -> None:
        encoding = build_k3_encoding("hole5")
        clauses = signature_breaker_clauses(encoding)
        self.assertEqual(len(clauses), EXPECTED_BREAKER_CLAUSE_COUNT)
        self.assertEqual(
            sum(map(len, clauses)), EXPECTED_BREAKER_LITERAL_COUNT
        )
        self.assertEqual(len(set(clauses)), len(clauses))
        edge_variables = set(encoding.edge_variables.values())
        self.assertTrue(
            all(
                abs(literal) in edge_variables
                for clause in clauses
                for literal in clause
            )
        )
        report = exhaustive_comparator_audit(encoding)
        self.assertEqual(report["adjacent_comparators_checked"], 5)
        self.assertEqual(report["assignments_per_comparator"], 4096)
        self.assertEqual(report["total_assignments_checked"], 20_480)

    def test_each_adjacent_comparator_has_the_proved_shape(self) -> None:
        encoding = build_k3_encoding("hole5")
        for left, right in ADJACENT_FREE_PAIRS:
            with self.subTest(left=left, right=right):
                clauses = lexicographic_leq_clauses(
                    signature_variables(encoding, left),
                    signature_variables(encoding, right),
                )
                self.assertEqual(
                    len(clauses), COMPARATOR_CLAUSES_PER_PAIR
                )
                self.assertEqual(
                    sum(map(len, clauses)),
                    COMPARATOR_LITERAL_COUNT_PER_PAIR,
                )
                self.assertEqual(len(clauses[0]), 2)
                self.assertEqual(len(clauses[-1]), 12)

    def test_signature_scope_is_exact(self) -> None:
        encoding = build_k3_encoding("hole5")
        self.assertEqual(CORE_VERTICES, tuple(range(6)))
        self.assertEqual(FREE_VERTICES, tuple(range(6, 12)))
        for vertex in FREE_VERTICES:
            self.assertEqual(
                signature_variables(encoding, vertex),
                tuple(encoding.edge(core, vertex) for core in CORE_VERTICES),
            )
        for malformed in (-1, 5, 12, True):
            with self.subTest(vertex=malformed):
                with self.assertRaises(ValueError):
                    signature_variables(encoding, malformed)


@unittest.skipUnless(
    (SOURCE_PACKAGE / CNF_NAME).is_file(), "retained hole5 package absent"
)
class CovarianceAndPackageTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.source_payload = (SOURCE_PACKAGE / CNF_NAME).read_bytes()
        cls.source_cnf = parse_dimacs_bytes(cls.source_payload)

    def test_full_bank_cnf_is_covariant_under_s6_generators(self) -> None:
        report = covariance_audit(self.source_cnf)
        self.assertEqual(report["generator_count"], 5)
        self.assertEqual(
            report["generator_transpositions_checked"],
            [list(pair) for pair in ADJACENT_FREE_PAIRS],
        )
        self.assertEqual(
            report["source_clause_count"], EXPECTED_SOURCE_CLAUSE_COUNT
        )

    def test_induced_variable_maps_are_bijections_and_preserve_formula(self) -> None:
        encoding = build_k3_encoding("hole5")
        original = Counter(tuple(sorted(clause)) for clause in self.source_cnf.clauses)
        for left, right in ADJACENT_FREE_PAIRS:
            permutation = list(range(12))
            permutation[left], permutation[right] = (
                permutation[right],
                permutation[left],
            )
            variable_map = variable_relabeling(encoding, permutation)
            self.assertEqual(
                set(variable_map),
                set(range(1, EXPECTED_DERIVED_VARIABLE_COUNT + 1)),
            )
            self.assertEqual(set(variable_map), set(variable_map.values()))
            transformed = Counter(
                tuple(sorted(relabel_clause(clause, variable_map)))
                for clause in self.source_cnf.clauses
            )
            self.assertEqual(transformed, original)

    def test_derived_cnf_retains_source_body_and_appends_only_breaker(self) -> None:
        clauses = signature_breaker_clauses()
        derived_payload = _derive_cnf_bytes(self.source_payload, clauses)
        source_header, source_body = self.source_payload.split(b"\n", 1)
        derived_header, derived_body = derived_payload.split(b"\n", 1)
        self.assertEqual(
            source_header,
            b"p cnf 6886 23653",
        )
        self.assertEqual(
            derived_header,
            b"p cnf 6886 23968",
        )
        self.assertTrue(derived_body.startswith(source_body))
        self.assertEqual(
            derived_body[len(source_body) :],
            breaker_clause_stream_bytes(clauses),
        )
        parsed = parse_dimacs_bytes(derived_payload)
        self.assertEqual(
            sha256_bytes(derived_payload), EXPECTED_DERIVED_CNF_SHA256
        )
        self.assertEqual(
            parsed.variable_count, EXPECTED_DERIVED_VARIABLE_COUNT
        )
        self.assertEqual(len(parsed.clauses), EXPECTED_DERIVED_CLAUSE_COUNT)
        self.assertEqual(
            sum(map(len, parsed.clauses)), EXPECTED_DERIVED_LITERAL_COUNT
        )
        self.assertEqual(
            parsed.clauses[:EXPECTED_SOURCE_CLAUSE_COUNT],
            self.source_cnf.clauses,
        )
        self.assertEqual(
            parsed.clauses[EXPECTED_SOURCE_CLAUSE_COUNT:], clauses
        )

    def test_generator_is_deterministic_audited_and_no_overwrite(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            first = root / "first"
            second = root / "second"
            with patch(
                "synthesis_k3.hole5_signature_breaker.git_source_binding",
                side_effect=fake_git_binding,
            ):
                first_report = generate_derived_package(
                    source_package=SOURCE_PACKAGE,
                    output_directory=first,
                    validation_gate=True,
                )
                second_report = generate_derived_package(
                    source_package=SOURCE_PACKAGE,
                    output_directory=second,
                    validation_gate=True,
                )
                audit_report = audit_derived_package(
                    first,
                    source_package=SOURCE_PACKAGE,
                    exhaustive_covariance=True,
                )
            for name in (CNF_NAME, BREAKER_NAME, MANIFEST_NAME):
                self.assertEqual(
                    (first / name).read_bytes(),
                    (second / name).read_bytes(),
                )
            self.assertEqual(
                sha256_bytes((first / BREAKER_NAME).read_bytes()),
                EXPECTED_BREAKER_SHA256,
            )
            self.assertEqual(
                first_report["status"], "AUDITED_DERIVED_FORMULA_NONCLAIM"
            )
            self.assertEqual(
                first_report["claim_status"], "NO_MATHEMATICAL_CLAIM"
            )
            self.assertEqual(first_report["cnf_sha256"], second_report["cnf_sha256"])
            self.assertEqual(audit_report["covariance_generators_checked"], 5)
            manifest = json.loads(
                (first / MANIFEST_NAME).read_text(encoding="utf-8")
            )
            self.assertFalse(manifest["production_solve_gate"]["enabled"])
            self.assertEqual(
                manifest["formula_counts"]["appended"],
                {"variables": 0, "clauses": 315, "literals": 3210},
            )
            with patch(
                "synthesis_k3.hole5_signature_breaker.git_source_binding",
                side_effect=fake_git_binding,
            ):
                with self.assertRaises(FileExistsError):
                    generate_derived_package(
                        source_package=SOURCE_PACKAGE,
                        output_directory=first,
                        validation_gate=True,
                    )

    def test_validation_gate_refuses_before_writing(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary).resolve() / "derived"
            with self.assertRaises(PermissionError):
                generate_derived_package(
                    source_package=SOURCE_PACKAGE,
                    output_directory=output,
                    validation_gate=False,
                )
            self.assertFalse(output.exists())


if __name__ == "__main__":
    unittest.main()
