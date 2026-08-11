import unittest
import importlib.util
from pathlib import Path
import tempfile
import zipfile

from bimolecular_pr.verification import (
    EXPECTED_SEEDED_RANDOM_TOP,
    EXPECTED_THREE_SPECIES_ATLAS,
    SOURCE_FILES,
    canonical,
    deterministic_top_atlas,
    exact_entropy_checks,
    seeded_random_top,
    source_hashes,
)


class VerificationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.root = Path(__file__).resolve().parents[1]

    def test_source_hashes_use_closed_allowlist(self):
        self.assertEqual(tuple(source_hashes(self.root)), SOURCE_FILES)

    def test_canonical_json_is_independent_of_mapping_insertion_order(self):
        self.assertEqual(canonical({"b": 2, "a": 1}), canonical({"a": 1, "b": 2}))

    def test_entropy_verifier_executes_substantive_cases(self):
        self.assertGreater(exact_entropy_checks(), 100)

    def test_exhaustive_three_species_atlas_matches_fixed_result(self):
        self.assertEqual(deterministic_top_atlas(), EXPECTED_THREE_SPECIES_ATLAS)

    def test_seeded_random_stress_matches_fixed_result(self):
        self.assertEqual(seeded_random_top(), EXPECTED_SEEDED_RANDOM_TOP)

    def test_built_wheel_carries_the_mit_license(self):
        backend_path = self.root / "build_backend.py"
        spec = importlib.util.spec_from_file_location("release_build_backend", backend_path)
        self.assertIsNotNone(spec)
        self.assertIsNotNone(spec.loader)
        backend = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(backend)
        with tempfile.TemporaryDirectory() as directory:
            wheel_name = backend.build_wheel(directory)
            with zipfile.ZipFile(Path(directory) / wheel_name) as archive:
                license_path = (
                    "bimolecular_pr-1.1.0.dist-info/licenses/LICENSE"
                )
                self.assertEqual(
                    archive.read(license_path),
                    (self.root / "LICENSE").read_bytes(),
                )
                metadata = archive.read(
                    "bimolecular_pr-1.1.0.dist-info/METADATA"
                ).decode()
                self.assertIn("License-Expression: MIT\n", metadata)
                self.assertIn("License-File: LICENSE\n", metadata)


if __name__ == "__main__":
    unittest.main()
