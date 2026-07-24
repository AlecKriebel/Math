#!/usr/bin/env python3
"""Focused tests for the independent two-forced-edge audit."""

from __future__ import annotations

import copy
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "verify"))

import e2_double_forced_search_independent_check as audit  # noqa: E402


def one_clique() -> tuple[int, ...]:
    adjacency = [0] * audit.ORDER
    for left in range(5):
        for right in range(left + 1, 5):
            adjacency[left] |= 1 << right
            adjacency[right] |= 1 << left
    return tuple(adjacency)


class DoubleForcedIndependentAuditTests(unittest.TestCase):
    def test_graph6_round_trip_and_complement(self) -> None:
        for adjacency in (
            tuple([0] * audit.ORDER),
            one_clique(),
            audit.complement(one_clique()),
        ):
            code = audit.encode_graph6(adjacency)
            self.assertEqual(audit.decode_graph6(code), adjacency)
            self.assertEqual(
                audit.complement(audit.complement(adjacency)), adjacency
            )

    def test_strict_json_rejects_duplicate_keys(self) -> None:
        with tempfile.TemporaryDirectory() as directory_name:
            path = Path(directory_name) / "duplicate.json"
            path.write_text('{"same": 1, "same": 2}\n', encoding="utf-8")
            with self.assertRaises(audit.AuditFailure):
                audit.strict_json_load(path)

    def test_source_semantics_detects_E1_stop_and_export(self) -> None:
        source = (
            ROOT / "src/search43_e2_barrier_escape.cpp"
        ).read_text(encoding="utf-8")
        record = audit.inspect_e1_semantics(source)
        self.assertTrue(all(
            value
            for key, value in record.items()
            if key not in {
                "near_return_site_count",
                "E1_counter_increment_site_count",
            }
        ))
        self.assertEqual(record["near_return_site_count"], 2)
        with self.assertRaises(audit.AuditFailure):
            audit.inspect_e1_semantics(
                source.replace("return 11;", "return 12;")
            )

    def test_published_endpoint_representatives_recount(self) -> None:
        path = (
            ROOT
            / "results/constructive/e2_low_closure_v2/"
            "double_forced_E2_representatives_v2.g6"
        )
        record = audit.recount_e2_stream(audit.graph6_stream(path))
        self.assertEqual(record["record_count"], 2)
        self.assertEqual(record["unique_record_count"], 2)
        self.assertEqual(
            record["geometry_counts"],
            {"same_colour_pair;overlap=4": 2},
        )

    def test_aggregate_identities_accept_published_result(self) -> None:
        plan = audit.strict_json_load(
            ROOT
            / "results/benchmark_plans/e2_low_closure_double_forced_v1.json"
        )
        result = audit.strict_json_load(
            ROOT
            / "results/constructive/e2_low_closure_v2/"
            "double_forced.result.json"
        )
        with tempfile.TemporaryDirectory() as directory_name:
            record = audit.validate_search_aggregates(
                plan=plan,
                result=result,
                endpoint_count=1_878,
                near_path=Path(directory_name) / "absent_E1.g6",
            )
        self.assertTrue(all(record.values()))

        corrupted = copy.deepcopy(result)
        corrupted["second_candidate_count"] = 39_511_630
        with tempfile.TemporaryDirectory() as directory_name:
            with self.assertRaises(audit.AuditFailure):
                audit.validate_search_aggregates(
                    plan=plan,
                    result=corrupted,
                    endpoint_count=1_878,
                    near_path=Path(directory_name) / "absent_E1.g6",
                )

    def test_shortg_verbose_parser(self) -> None:
        text = """
  1 : 1 3 5
      7 9
  2 : 2 4
      6 8 10
"""
        self.assertEqual(
            audit.parse_shortg_verbose(text),
            ((1, 3, 5, 7, 9), (2, 4, 6, 8, 10)),
        )

    def test_schedule_comparison_is_fail_closed(self) -> None:
        production = {
            key: value
            for key, value in audit.EXPECTED_SEARCH_FIELDS.items()
        }
        production.update(
            {
                "first_by_height": {"4": 47_675},
                "second_by_height": {"4": 47_675},
            }
        )
        schedule = {
            "low_seed_count": 53,
            "low_seed_objective_distribution": {"3": 9, "4": 44},
            "known_E2_state_count": 1_892,
            "first_barrier_count": 47_675,
            "first_barrier_exact_replays": 47_675,
            "first_nonconflict_barrier_count": 46_225,
            "first_high_conflict_barrier_count": 1_450,
            "first_by_source_objective": {"3": 8_100, "4": 39_575},
            "first_by_height": {"4": 47_675},
            "second_candidate_count": 39_511_631,
            "second_barrier_count": 47_675,
            "second_barrier_exact_replays": 47_675,
            "first_without_second_candidate_count": 0,
            "second_by_height": {"4": 47_675},
            "second_delta_distribution": {"0": 15_615, "1": 32_060},
            "objective_ceiling": 80,
            "neutral_cycle_length_histogram": {"86": 22},
        }
        audit.compare_schedule(schedule, production)
        schedule["second_candidate_count"] = 1
        with self.assertRaises(audit.AuditFailure):
            audit.compare_schedule(schedule, production)


if __name__ == "__main__":
    unittest.main()
