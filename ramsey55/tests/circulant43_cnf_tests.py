#!/usr/bin/env python3
"""Tests for the exact circulant-order-43 encoding."""

from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load_module(name: str, path: Path):
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


generator = load_module("circulant43_generator", ROOT / "src" / "circulant43_cnf.py")
checker = load_module(
    "circulant43_checker", ROOT / "verify" / "circulant43_cnf_check.py"
)


class Circulant43EncodingTests(unittest.TestCase):
    def test_distance_is_symmetric_and_translation_invariant(self) -> None:
        for left in range(43):
            for right in range(43):
                observed = generator.circular_distance(left, right)
                self.assertEqual(observed, generator.circular_distance(right, left))
                self.assertEqual(
                    observed,
                    generator.circular_distance((left + 17) % 43, (right + 17) % 43),
                )

    def test_generator_and_independent_reconstruction_agree(self) -> None:
        signatures = generator.distance_signatures()
        independent = checker.independently_expected_clauses()
        reconstructed = []
        for signature in signatures:
            reconstructed.append(signature)
            reconstructed.append(tuple(-value for value in signature))
        self.assertEqual(tuple(reconstructed), independent)
        self.assertEqual(len(signatures), 10_437)

    def test_materialized_formula_passes_checker(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            temporary = Path(directory)
            cnf = temporary / "circulant43.cnf"
            metadata = temporary / "circulant43.metadata.json"
            generator.write_cnf(cnf, generator.distance_signatures())
            source = Path(generator.__file__).resolve()
            histogram = {}
            for signature in generator.distance_signatures():
                histogram[str(len(signature))] = histogram.get(str(len(signature)), 0) + 1
            metadata.write_text(
                __import__("json").dumps(
                    {
                        "order": 43,
                        "clique_size": 5,
                        "variable_count": 21,
                        "five_set_count": 962_598,
                        "unreduced_ramsey_clause_count": 1_925_196,
                        "unique_distance_signature_count": 10_437,
                        "clause_count": 20_874,
                        "signature_size_histogram": histogram,
                        "cnf_sha256": generator.sha256_file(cnf),
                        "cnf_bytes": cnf.stat().st_size,
                        "generator_path": str(source),
                    },
                    sort_keys=True,
                )
                + "\n",
                encoding="utf-8",
            )
            result = checker.check(cnf, metadata)
            self.assertTrue(result["valid"], result)


if __name__ == "__main__":
    unittest.main()
