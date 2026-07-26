from __future__ import annotations

import sys
import tempfile
import unittest
from collections import Counter
from dataclasses import replace
from pathlib import Path


CAMPAIGN = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(CAMPAIGN / "src"))

from search.deep_survivor_radius2 import (  # noqa: E402
    BASE_GRAPH6,
    EXPECTED_CANONICAL_CLASS_COUNT,
    EXPECTED_FULL_HISTOGRAM,
    EXPECTED_PROJECTED_HISTOGRAM,
    PAIR_COUNT,
    RAW_ORIGIN_COUNT,
    RUNTIME_SOURCE_RELATIVE_PATHS,
    _validate_output_path,
    canonicalize_origins,
    evaluate_canonical_graph,
    generate_raw_origins,
    origin_toggle_index_sets,
    runtime_source_manifest,
    toggle_pairs,
    validate_current_manifest,
    validate_fixed_base,
    validate_origin_coverage,
)
from verifier_a.core import BitGraph  # noqa: E402


LABELG = CAMPAIGN / "tools" / "nauty2_9_3" / "labelg"


class DeepSurvivorRadiusTwoTests(unittest.TestCase):
    def test_exact_raw_coverage_arithmetic_and_order(self) -> None:
        selections = origin_toggle_index_sets()
        self.assertEqual(PAIR_COUNT, 66)
        self.assertEqual(RAW_ORIGIN_COUNT, 1 + 66 + 66 * 65 // 2)
        self.assertEqual(len(selections), 2_212)
        self.assertEqual(len(set(selections)), 2_212)
        self.assertEqual(selections[0], ())
        self.assertEqual(selections[1], (0,))
        self.assertEqual(selections[66], (65,))
        self.assertEqual(selections[67], (0, 1))
        self.assertEqual(selections[-1], (64, 65))
        self.assertEqual(toggle_pairs(), tuple(sorted(toggle_pairs())))

    def test_raw_generation_and_tamper_detection(self) -> None:
        origins = generate_raw_origins()
        self.assertEqual(len(origins), RAW_ORIGIN_COUNT)
        validate_origin_coverage(origins, require_canonical=False)
        tampered = list(origins)
        tampered[100] = replace(
            tampered[100],
            raw_graph6=BASE_GRAPH6,
        )
        with self.assertRaisesRegex(ValueError, "raw graph6 mismatch"):
            validate_origin_coverage(
                tuple(tampered), require_canonical=False
            )

    @unittest.skipUnless(LABELG.is_file(), "pinned labelg is not built")
    def test_exact_canonical_multiplicity_coverage(self) -> None:
        origins = canonicalize_origins(generate_raw_origins(), LABELG)
        multiplicities = Counter(
            origin.canonical_graph6 for origin in origins
        )
        self.assertEqual(
            len(multiplicities), EXPECTED_CANONICAL_CLASS_COUNT
        )
        self.assertEqual(sum(multiplicities.values()), RAW_ORIGIN_COUNT)
        validate_origin_coverage(origins, require_canonical=True)

    def test_both_stacks_agree_on_deep_base_parameters_and_game(self) -> None:
        record = evaluate_canonical_graph(BASE_GRAPH6)
        expected = {
            "gamma": 3,
            "i": 3,
            "alpha": 3,
            "gamma_infinity": 4,
            "theta": 4,
        }
        self.assertEqual(record["parameters"], expected)
        self.assertEqual(record["stack_a"], expected)
        self.assertEqual(record["stack_b"], expected)
        self.assertEqual(
            [
                (decision["k"], decision["stack_a"], decision["stack_b"])
                for decision in record["eternal_decisions"]
            ],
            [(3, False, False), (4, True, True)],
        )
        self.assertTrue(
            record["eternal_decisions"][-1]["greatest_family_equal"]
        )
        self.assertFalse(record["is_candidate"])

    def test_expected_histograms_are_complete_and_candidate_free(self) -> None:
        self.assertEqual(
            sum(EXPECTED_PROJECTED_HISTOGRAM.values()),
            EXPECTED_CANONICAL_CLASS_COUNT,
        )
        self.assertEqual(
            sum(EXPECTED_FULL_HISTOGRAM.values()),
            EXPECTED_CANONICAL_CLASS_COUNT,
        )
        self.assertTrue(
            all(gamma < eternal for gamma, _, eternal, _ in (
                EXPECTED_PROJECTED_HISTOGRAM
            ))
        )

    def test_malformed_or_wrong_base_is_rejected(self) -> None:
        with self.assertRaisesRegex(ValueError, "exact fixed labeled"):
            validate_fixed_base("!")
        other = BitGraph.cycle(12).to_graph6()
        with self.assertRaisesRegex(ValueError, "exact fixed labeled"):
            validate_fixed_base(other)
        with self.assertRaisesRegex(ValueError, "must be a string"):
            validate_fixed_base(b"Kun_w{vRrblV")

    def test_source_manifest_tamper_is_rejected(self) -> None:
        manifest = runtime_source_manifest(CAMPAIGN)
        validate_current_manifest(
            manifest,
            campaign_root=CAMPAIGN,
            expected_paths=RUNTIME_SOURCE_RELATIVE_PATHS,
        )
        tampered = list(manifest)
        tampered[0] = (tampered[0][0], "0" * 64)
        with self.assertRaisesRegex(ValueError, "source hash mismatch"):
            validate_current_manifest(
                tampered,
                campaign_root=CAMPAIGN,
                expected_paths=RUNTIME_SOURCE_RELATIVE_PATHS,
            )
        reordered = tuple(reversed(manifest))
        with self.assertRaisesRegex(ValueError, "path sequence"):
            validate_current_manifest(
                reordered,
                campaign_root=CAMPAIGN,
                expected_paths=RUNTIME_SOURCE_RELATIVE_PATHS,
            )

    def test_output_path_cannot_be_a_non_json_source_alias(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            bad = Path(temporary) / "measurement.txt"
            with self.assertRaisesRegex(ValueError, ".json suffix"):
                _validate_output_path(bad, CAMPAIGN)
        source_alias = CAMPAIGN / RUNTIME_SOURCE_RELATIVE_PATHS[0]
        with self.assertRaisesRegex(ValueError, ".json suffix|aliases"):
            _validate_output_path(source_alias, CAMPAIGN)


if __name__ == "__main__":
    unittest.main()
