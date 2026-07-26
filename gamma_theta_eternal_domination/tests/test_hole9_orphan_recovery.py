from __future__ import annotations

import hashlib
from pathlib import Path
import tempfile
import unittest

from verifier_b.hole9_orphan_recovery import (
    EXPECTED_ADDITION_ONLY_PROOF,
    EXPECTED_ORPHAN_ARTIFACTS,
    VerificationError,
    canonical_coloring,
    checker_command,
    parse_exact_unsat_result,
    reconstruct_hole9_formula,
    sha256_bytes,
    strict_json_bytes,
    strip_deletion_lines,
    validate_checker_transcript,
    validate_expected_stripped_proof,
    validate_source_evidence,
)


ROOT = Path(__file__).resolve().parents[1]
ORPHAN = (
    ROOT
    / "results/synthesis_k3_runs/hole9/attempts/000170.akmx9xl0"
)


class Hole9OrphanRecoveryTests(unittest.TestCase):
    def test_independent_base_dimensions(self) -> None:
        formula = reconstruct_hole9_formula(())
        self.assertEqual(formula.variable_count, 6886)
        self.assertEqual(len(formula.clauses), 20030)
        self.assertEqual(formula.literal_count, 114619)
        self.assertEqual(
            hashlib.sha256(formula.dimacs()).hexdigest(),
            "cf555f359dc887c89f84e35a40ee649e77ef805b2690ec34e72cc4ef75e5d5c7",
        )

    def test_full_reconstruction_matches_preserved_cnf(self) -> None:
        checkpoint = strict_json_bytes(
            (ROOT / "results/synthesis_k3_runs/hole9/checkpoint.json").read_bytes()
        )
        colorings = [record["coloring"] for record in checkpoint["cuts"]]
        formula = reconstruct_hole9_formula(colorings)
        self.assertEqual(len(formula.clauses), 20200)
        self.assertEqual(formula.literal_count, 117841)
        self.assertEqual(
            formula.dimacs(),
            (ORPHAN / "instance.cnf").read_bytes(),
        )
        self.assertEqual(
            sha256_bytes(formula.dimacs()),
            EXPECTED_ORPHAN_ARTIFACTS["instance.cnf"][1],
        )

    def test_exact_proof_transformation(self) -> None:
        stripped, stats = strip_deletion_lines(
            (ORPHAN / "proof.drat").read_bytes()
        )
        validate_expected_stripped_proof(stripped, stats)
        self.assertEqual(stats.deletion_count, 11683)
        self.assertEqual(stats.addition_count, 4705)
        self.assertEqual(
            sha256_bytes(stripped),
            EXPECTED_ADDITION_ONLY_PROOF["sha256"],
        )
        self.assertNotIn(b"\nd ", b"\n" + stripped)

    def test_proof_parser_rejects_malformed_deletions(self) -> None:
        bad = (
            b"1 0\n"
            b"d 2\n"       # missing terminator
            b"0\n"
        )
        with self.assertRaises(VerificationError):
            strip_deletion_lines(bad)
        with self.assertRaises(VerificationError):
            strip_deletion_lines(b"1 0\nd 2 2 0\n0\n")
        with self.assertRaises(VerificationError):
            strip_deletion_lines(b"1 0\nd 0\n0\n")
        with self.assertRaises(VerificationError):
            strip_deletion_lines(b"1 0\nd 2 0 0\n0\n")

    def test_proof_parser_rejects_other_mutations(self) -> None:
        for payload in (
            b"1 0\n0\njunk\n",
            b"1  0\n0\n",
            b"+1 0\n0\n",
            b"1 -1 0\n0\n",
            b"1 0\n0\n2 0\n",
            b"1 0\r\n0\r\n",
            b"1 0\n\xff 0\n",
        ):
            with self.subTest(payload=payload):
                with self.assertRaises(VerificationError):
                    strip_deletion_lines(payload)

    def test_stripped_hash_is_a_required_binding(self) -> None:
        stripped, stats = strip_deletion_lines(
            (ORPHAN / "proof.drat").read_bytes()
        )
        mutated = stripped.replace(b"-67 0\n", b"-66 0\n", 1)
        with self.assertRaises(VerificationError):
            validate_expected_stripped_proof(mutated, stats)

    def test_solver_result_parser_is_exact(self) -> None:
        parse_exact_unsat_result(b"s UNSATISFIABLE\n", "test")
        for payload in (
            b"s SATISFIABLE\n",
            b"s UNSATISFIABLE",
            b"c comment\ns UNSATISFIABLE\n",
            b"s UNSATISFIABLE\ns UNSATISFIABLE\n",
            b"s UNSATISFIABLE\r\n",
        ):
            with self.subTest(payload=payload):
                with self.assertRaises(VerificationError):
                    parse_exact_unsat_result(payload, "test")

    def test_checker_transcript_mutation_traps(self) -> None:
        validate_checker_transcript(b"c checked\ns VERIFIED\n", b"")
        validate_checker_transcript(
            b"\rc progress\n\rs VERIFIED\n\rc done\n", b""
        )
        for stdout, stderr in (
            (b"c checked\n", b""),
            (b"s VERIFIED\ns VERIFIED\n", b""),
            (b"s VERIFIED\nc WARNING: ignored\n", b""),
            (b"s VERIFIED\nc failed later\n", b""),
            (b"s VERIFIED\n", b"diagnostic\n"),
        ):
            with self.subTest(stdout=stdout, stderr=stderr):
                with self.assertRaises(VerificationError):
                    validate_checker_transcript(stdout, stderr)

    def test_checker_commands_have_sound_exact_modes(self) -> None:
        checker = Path("/checker")
        cnf = Path("/formula.cnf")
        proof = Path("/proof.drat")
        primary = checker_command(
            checker, cnf, proof, wall_seconds=60, plain=False
        )
        redundant = checker_command(
            checker, cnf, proof, wall_seconds=60, plain=True
        )
        self.assertEqual(
            primary[-6:], ("-I", "-f", "-W", "-U", "-t", "60")
        )
        self.assertNotIn("-p", primary)
        self.assertEqual(
            redundant[-7:],
            ("-I", "-f", "-p", "-W", "-U", "-t", "60"),
        )

    def test_canonical_coloring_rejects_relabeling_and_bool(self) -> None:
        self.assertEqual(
            canonical_coloring((0, 1, 2, 0, 1, 2, 0, 1, 2, 0, 1, 2)),
            (0, 1, 2, 0, 1, 2, 0, 1, 2, 0, 1, 2),
        )
        with self.assertRaises(VerificationError):
            canonical_coloring((1, 0, 2, 1, 0, 2, 1, 0, 2, 1, 0, 2))
        with self.assertRaises(VerificationError):
            canonical_coloring((False,) + (0,) * 11)

    def test_strict_json_rejects_duplicate_and_nonfinite(self) -> None:
        with self.assertRaises(VerificationError):
            strict_json_bytes(b'{"x":1,"x":2}\n')
        with self.assertRaises(VerificationError):
            strict_json_bytes(b'{"x":NaN}\n')

    def test_complete_source_evidence_is_read_only_and_valid(self) -> None:
        checkpoint = ROOT / "results/synthesis_k3_runs/hole9/checkpoint.json"
        before = sha256_bytes(checkpoint.read_bytes())
        evidence = validate_source_evidence(ROOT)
        after = sha256_bytes(checkpoint.read_bytes())
        self.assertEqual(before, after)
        self.assertEqual(
            evidence["proof_stats"].stripped_sha256,
            EXPECTED_ADDITION_ONLY_PROOF["sha256"],
        )
        self.assertGreaterEqual(evidence["present_artifact_hash_checks"], 170)


if __name__ == "__main__":
    unittest.main()
