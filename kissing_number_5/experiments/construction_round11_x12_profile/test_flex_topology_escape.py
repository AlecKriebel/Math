"""Regression and tamper tests for the rigidity-mode escape artifacts."""

from __future__ import annotations

import hashlib
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


verifier = load_module(
    "flex_topology_escape_verifier_tests",
    HERE / "verify_flex_topology_escape.py",
)


class FlexTopologyEscapeTests(unittest.TestCase):
    def verify_modified(
        self, source_mutation=None, topology_mutation=None
    ):
        source = json.loads(verifier.SOURCE.read_bytes())
        topology = json.loads(verifier.TOPOLOGY.read_bytes())
        if source_mutation is not None:
            source_mutation(source)
        source_bytes = (json.dumps(source, indent=2) + "\n").encode()
        topology["source_sha256"] = hashlib.sha256(
            source_bytes
        ).hexdigest()
        if topology_mutation is not None:
            topology_mutation(topology)
        with tempfile.TemporaryDirectory() as directory:
            source_path = Path(directory) / "source.json"
            topology_path = Path(directory) / "topology.json"
            source_path.write_bytes(source_bytes)
            topology_path.write_text(
                json.dumps(topology, indent=2) + "\n"
            )
            return verifier.verify(
                source_path,
                topology_path,
                enforce_pinned_hashes=False,
            )

    def test_original_verifies(self) -> None:
        report = verifier.verify()
        self.assertEqual(report["strict_improvement_count"], 0)
        self.assertEqual(report["nonisomorphic_restart_count"], 9)

    def test_rigidity_rank_tamper_fails(self) -> None:
        def mutation(source):
            source["analyses"][1]["rigidity"][
                "reduced_rigidity_rank_at_1e-9"
            ] += 1

        with self.assertRaises(verifier.VerificationError):
            self.verify_modified(source_mutation=mutation)

    def test_coordinate_tamper_fails(self) -> None:
        def mutation(source):
            source["runs"][0]["retained"][
                "coordinates_float64"
            ][0][0] += 1.0e-4

        with self.assertRaises(
            (verifier.VerificationError, verifier.base.VerificationError)
        ):
            self.verify_modified(source_mutation=mutation)

    def test_kick_metadata_tamper_fails(self) -> None:
        def mutation(source):
            source["runs"][4]["kick"][
                "selected_maximum_inner_product"
            ] -= 1.0e-4

        with self.assertRaises(verifier.VerificationError):
            self.verify_modified(source_mutation=mutation)

    def test_topology_mapping_tamper_fails(self) -> None:
        def mutation(topology):
            report = next(
                item
                for item in topology["reports"]
                if item["cardinality"] == 44
                and item["restart"] == 0
            )
            mapping = report["source_to_retained_isomorphism"]
            mapping[0], mapping[1] = mapping[1], mapping[0]

        with self.assertRaises(
            (verifier.VerificationError, verifier.base.VerificationError)
        ):
            self.verify_modified(topology_mutation=mutation)

    def test_status_tamper_fails(self) -> None:
        def mutation(source):
            source["evidence_status"] = "EXACT CONSTRUCTION"

        with self.assertRaises(verifier.VerificationError):
            self.verify_modified(source_mutation=mutation)

    def test_solver_status_is_not_trusted(self) -> None:
        def mutation(source):
            source["runs"][0]["epigraph_solver"][
                "success"
            ] = False
            source["runs"][0]["epigraph_solver"][
                "message"
            ] = "deliberately ignored"

        report = self.verify_modified(source_mutation=mutation)
        self.assertEqual(report["strict_improvement_count"], 0)


if __name__ == "__main__":
    unittest.main()
