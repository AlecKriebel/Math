"""Regression and tamper tests for the round-11 construction artifacts."""

from __future__ import annotations

import copy
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest


HERE = Path(__file__).resolve().parent


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


portfolio_verifier = load_module("round11_verify_tests", HERE / "verify.py")
polish_verifier = load_module(
    "round11_polish_verify_tests", HERE / "verify_polished.py"
)


class Round11VerifierTests(unittest.TestCase):
    def test_portfolio_verifies(self) -> None:
        result = portfolio_verifier.verify()
        self.assertFalse(result["exact_candidate_found"])
        self.assertEqual(result["verified_phase_representatives"], 56)

    def test_polish_verifies(self) -> None:
        result = polish_verifier.verify()
        self.assertFalse(result["exact_candidate_found"])
        self.assertLess(
            result["best_n44"]["retained_maximum"],
            0.5274711925359575,
        )

    def test_coordinate_tamper_fails(self) -> None:
        source = json.loads(portfolio_verifier.RESULTS.read_text())
        modified = copy.deepcopy(source)
        modified["runs"][0]["best"]["coordinates_float64"][0][0] += 1.0e-5
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "portfolio.json"
            path.write_text(json.dumps(modified))
            with self.assertRaises(portfolio_verifier.VerificationError):
                portfolio_verifier.verify(path)

    def test_maximum_tamper_fails(self) -> None:
        source = json.loads(polish_verifier.SOURCE.read_text())
        modified = copy.deepcopy(source)
        modified["records"][-1]["retained"][
            "maximum_inner_product"
        ] -= 1.0e-6
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "polished.json"
            path.write_text(json.dumps(modified))
            with self.assertRaises(
                polish_verifier.portfolio_verifier.VerificationError
            ):
                polish_verifier.verify(path)

    def test_evidence_status_tamper_fails(self) -> None:
        source = json.loads(portfolio_verifier.RESULTS.read_text())
        modified = copy.deepcopy(source)
        modified["evidence_status"] = "EXACT"
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "portfolio.json"
            path.write_text(json.dumps(modified))
            with self.assertRaises(portfolio_verifier.VerificationError):
                portfolio_verifier.verify(path)


if __name__ == "__main__":
    unittest.main()
