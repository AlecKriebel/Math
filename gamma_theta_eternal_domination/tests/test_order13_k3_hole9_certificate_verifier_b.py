"""Focused fail-closed tests for the clean-room hole9 certificate verifier."""

from __future__ import annotations

import sys
from pathlib import Path
import unittest


CAMPAIGN_ROOT = Path(__file__).resolve().parents[1]
SOURCE_ROOT = CAMPAIGN_ROOT / "src"
if str(SOURCE_ROOT) not in sys.path:
    sys.path.insert(0, str(SOURCE_ROOT))

from verifier_b.order13_k3_hole9_certificate import (  # noqa: E402
    VerificationError,
    _encode_unsigned,
    parse_addition_only_bdrat,
    parse_dimacs,
    run_hostile_mutations,
    validate_drat_trim_result,
    validate_lrat_check_result,
    _GOOD_DRAT_STDOUT,
    _GOOD_LRAT_STDOUT,
)


class DimacsParserTests(unittest.TestCase):
    def test_valid_multiline_formula(self) -> None:
        self.assertEqual(
            parse_dimacs(b"p cnf 2 2\n1 -2\n0\n2 0\n"),
            {
                "clauses": 2,
                "comments": 0,
                "empty_clauses": 0,
                "literals": 3,
                "maximum_clause_size": 2,
                "maximum_variable_observed": 2,
                "variables": 2,
            },
        )

    def test_unterminated_and_out_of_range_reject(self) -> None:
        with self.assertRaises(VerificationError):
            parse_dimacs(b"p cnf 1 1\n1\n")
        with self.assertRaises(VerificationError):
            parse_dimacs(b"p cnf 1 1\n2 0\n")


class BinaryProofParserTests(unittest.TestCase):
    def test_valid_addition_and_final_empty(self) -> None:
        proof = b"a" + _encode_unsigned(3) + b"\x00a\x00"
        stats = parse_addition_only_bdrat(proof, max_variable=1)
        self.assertEqual(stats["addition_records"], 2)
        self.assertEqual(stats["empty_addition_record"], 2)
        self.assertEqual(stats["maximum_variable_observed"], 1)

    def test_deletion_post_empty_and_overlong_reject(self) -> None:
        for proof in (
            b"d\x00",
            b"a\x00a\x00",
            b"a\x82\x00\x00a\x00",
        ):
            with self.subTest(proof=proof):
                with self.assertRaises(VerificationError):
                    parse_addition_only_bdrat(proof)


class CheckerTranscriptTests(unittest.TestCase):
    def test_exact_controls_pass(self) -> None:
        self.assertEqual(
            validate_drat_trim_result(0, _GOOD_DRAT_STDOUT, b"")["marker"],
            "s VERIFIED",
        )
        self.assertEqual(
            validate_lrat_check_result(0, _GOOD_LRAT_STDOUT, b"")["marker"],
            "c VERIFIED",
        )

    def test_exit_marker_and_stderr_fail_closed(self) -> None:
        cases = (
            lambda: validate_drat_trim_result(1, _GOOD_DRAT_STDOUT, b""),
            lambda: validate_drat_trim_result(
                0, _GOOD_DRAT_STDOUT.replace(b"s VERIFIED\n", b""), b""
            ),
            lambda: validate_drat_trim_result(
                0, _GOOD_DRAT_STDOUT, b"warning\n"
            ),
            lambda: validate_lrat_check_result(1, _GOOD_LRAT_STDOUT, b""),
            lambda: validate_lrat_check_result(
                0, _GOOD_LRAT_STDOUT.replace(b"c VERIFIED\n", b""), b""
            ),
            lambda: validate_lrat_check_result(
                0, _GOOD_LRAT_STDOUT, b"warning\n"
            ),
        )
        for case in cases:
            with self.subTest(case=case):
                with self.assertRaises(VerificationError):
                    case()


class HostileMutationSuiteTests(unittest.TestCase):
    def test_all_representative_corruptions_reject(self) -> None:
        formula = b"p cnf 1 1\n1 0\n"
        proof = b"a" + _encode_unsigned(2) + b"\x00a\x00"
        results = run_hostile_mutations(formula, proof)
        self.assertEqual(len(results), 18)
        self.assertTrue(all(item["rejected"] is True for item in results))


if __name__ == "__main__":
    unittest.main()
