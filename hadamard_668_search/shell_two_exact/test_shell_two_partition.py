#!/usr/bin/env python3
"""Focused tests for the shell-two partition theorem and exact survivor."""

from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path
import sys
import unittest


HERE = Path(__file__).resolve().parent
SEARCH_ROOT = HERE.parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(SEARCH_ROOT))

from verify_shell_two_partition_theory import (  # noqa: E402
    CANDIDATE_A,
    CANDIDATE_B,
    candidate_certificate,
    compact_hash,
)
from verify_shell_two_exact_orbits import (  # noqa: E402
    CENSUS_FIELDS,
    EXPECTED_SEMANTIC_SHA256,
    PARTITION_CENSUS,
    build_certificate,
    compact_hash as orbit_compact_hash,
)
from verify_lp333_order3_phase_transfer import (  # noqa: E402
    audit_profile_transfer,
    catalog_phase_sum_intersection,
)


SEMANTIC_CERTIFICATE_SHA256 = (
    "4bb83d560f3b80fc765374f44480bf30d94c515a694a10f6867003cf1c9ada02"
)
CERTIFICATE_FILE_SHA256 = (
    "869ce920f49b9bae3126e823082fcc63ca5c68d939de9daacd04168dc03c95e7"
)
PHASE_COMPATIBLE_SHA256 = (
    "fb6ad9ac45b3fe4c59358dda5da3f6ba9a1655b68e7e55e76c0a2b962dd77481"
)
PHASE_SUM_CORPUS_SHA256 = (
    "d132ae6246ac96c030507e9efdd8a605d12f659f90e0f44ca4ba09ab60b72aac"
)
ORBIT_CERTIFICATE_FILE_SHA256 = (
    "8e7579d6361ffda0187c10e8e4fef654c8288e51e87e41432c178725cec40614"
)


class ShellTwoPartitionTest(unittest.TestCase):
    def test_detached_exact_profile_certificate(self) -> None:
        path = HERE / "shell_two_exact_profile_certificate.json"
        payload = path.read_bytes()
        stored = json.loads(payload)
        generated = json.loads(json.dumps(candidate_certificate()))
        self.assertEqual(stored, generated)
        self.assertEqual(compact_hash(stored), SEMANTIC_CERTIFICATE_SHA256)
        self.assertEqual(sha256(payload).hexdigest(), CERTIFICATE_FILE_SHA256)
        self.assertEqual(stored["physical_correlations"][0], [167, 0])
        self.assertEqual(
            stored["physical_correlations"][1:],
            [[0, 0]] * 36,
        )
        self.assertEqual(stored["full_profile_orbit_size"], 24)
        self.assertEqual(stored["stabilizer_size"], 1)

    def test_phase_lift_size_and_root_character_join(self) -> None:
        transfer = audit_profile_transfer(CANDIDATE_A, CANDIDATE_B)
        catalog = catalog_phase_sum_intersection(CANDIDATE_A, CANDIDATE_B)
        self.assertEqual(transfer["active_variables"], 54)
        self.assertEqual(
            transfer["total_assignments"],
            58_149_737_003_040_059_690_390_169,
        )
        self.assertEqual(transfer["channel_a_states"], 1_713)
        self.assertEqual(transfer["channel_b_states"], 1_961)
        self.assertEqual(transfer["compatible_signature_count"], 64)
        self.assertEqual(transfer["compatible_phase_sum_count"], 72)
        self.assertEqual(catalog["compatible_catalog_rows"], 72)
        self.assertEqual(
            transfer["accepted_assignments"],
            272_797_926_089_102_312_850,
        )
        self.assertEqual(
            transfer["accepted_assignments"],
            catalog["accepted_assignments"],
        )
        self.assertEqual(
            transfer["phase_sum_corpus"],
            catalog["phase_sum_corpus"],
        )
        self.assertEqual(
            transfer["compatible_sha256"],
            PHASE_COMPATIBLE_SHA256,
        )
        self.assertEqual(
            transfer["phase_sum_corpus_sha256"],
            PHASE_SUM_CORPUS_SHA256,
        )

    def test_all_five_exact_orbits_and_partition_census(self) -> None:
        path = HERE / "shell_two_exact_orbits_certificate.json"
        payload = path.read_bytes()
        stored = json.loads(payload)
        generated = build_certificate()
        self.assertEqual(
            orbit_compact_hash(generated),
            EXPECTED_SEMANTIC_SHA256,
        )
        self.assertEqual(
            stored["full_semantic_sha256"],
            EXPECTED_SEMANTIC_SHA256,
        )
        self.assertEqual(
            sha256(payload).hexdigest(),
            ORBIT_CERTIFICATE_FILE_SHA256,
        )
        self.assertEqual(stored["exact_orbits"], 5)
        self.assertEqual(stored["raw_orbit_members"], 84)
        self.assertEqual(
            stored["partition_census"],
            {
                partition: list(values)
                for partition, values in PARTITION_CENSUS.items()
            },
        )
        self.assertEqual(stored["census_fields"], list(CENSUS_FIELDS))
        for stored_orbit, generated_orbit in zip(
            stored["orbits"], generated["orbits"]
        ):
            self.assertEqual(
                stored_orbit["label"], generated_orbit["label"]
            )
            self.assertEqual(
                stored_orbit["profile_ids_a"],
                list(generated_orbit["profile_ids_a"]),
            )
            self.assertEqual(
                stored_orbit["profile_ids_b"],
                list(generated_orbit["profile_ids_b"]),
            )
            self.assertEqual(
                stored_orbit["orbit_size"],
                generated_orbit["orbit_size"],
            )
            self.assertEqual(
                stored_orbit["stabilizer_size"],
                generated_orbit["stabilizer_size"],
            )
            self.assertEqual(
                stored_orbit["compatible_row_margin_catalog_rows"],
                generated_orbit["phase_lift"][
                    "compatible_row_margin_catalog_rows"
                ],
            )


if __name__ == "__main__":
    unittest.main()
