"""Regression tests for the bounded exact mod-9 profile sampler."""

from __future__ import annotations

import io
import json
import unittest

from ortools.sat.python import cp_model

from legendre_333_profile_catalog import (
    EXACT_COMBINED_PAF,
    ROW_SUM_PROFILES,
    canonical_profile,
    profile_orbit,
)
from search_legendre_333_profile_catalog import (
    CENTERED_NORM_SHARDS,
    DEFAULT_MAX_MEMORY_MB,
    PROFILE_SYMMETRY_MODES,
    CanonicalProfileCollector,
    JsonSampleWriter,
    add_catalog_hint,
    add_basic_profile_symmetry,
    build_profile_model,
    configure_solver,
    exclude_catalog_orbits,
    profile_centered_norm_shard,
    profile_payload,
    sample_to_stream,
    validate_canonical_profile,
    validate_centered_norm_shard,
)


def _dihedral_images(vector: tuple[int, ...]) -> set[tuple[int, ...]]:
    return {
        tuple(vector[(reflection * index + shift) % 9] for index in range(9))
        for reflection in (-1, 1)
        for shift in range(9)
    }


def _independent_profile_orbit(
    a: tuple[int, ...], b: tuple[int, ...]
) -> set[tuple[tuple[int, ...], tuple[int, ...]]]:
    def image(
        vector: tuple[int, ...], multiplier: int, reflection: int, shift: int
    ) -> tuple[int, ...]:
        return tuple(
            vector[(reflection * multiplier * index + shift) % 9]
            for index in range(9)
        )

    images = set()
    for swap in (False, True):
        left, right = (b, a) if swap else (a, b)
        for multiplier in (1, 2, 4):
            for left_reflection in (-1, 1):
                for right_reflection in (-1, 1):
                    for left_shift in range(9):
                        left_image = image(
                            left, multiplier, left_reflection, left_shift
                        )
                        for right_shift in range(9):
                            images.add(
                                (
                                    left_image,
                                    image(
                                        right,
                                        multiplier,
                                        right_reflection,
                                        right_shift,
                                    ),
                                )
                            )
    return images


class ExactProfileSamplerTests(unittest.TestCase):
    def test_centered_norm_shards_are_a_disjoint_exhaustive_partition(self) -> None:
        self.assertEqual(CENTERED_NORM_SHARDS, tuple(range(76, 149, 2)))
        self.assertEqual(len(CENTERED_NORM_SHARDS), 37)

        # Each centered norm is even because x^2 == x (mod 2), and a vector
        # summing to -4 has squared norm at least four.  With combined norm
        # 152, these are all arithmetically possible oriented norm pairs.
        oriented_pairs = tuple((left, 152 - left) for left in range(4, 149, 2))
        shard_members = {
            shard: {
                pair for pair in oriented_pairs if max(pair) == shard
            }
            for shard in CENTERED_NORM_SHARDS
        }
        self.assertEqual(
            set().union(*shard_members.values()), set(oriented_pairs)
        )
        self.assertTrue(
            all(
                not shard_members[left] & shard_members[right]
                for index, left in enumerate(CENTERED_NORM_SHARDS)
                for right in CENTERED_NORM_SHARDS[index + 1 :]
            )
        )
        for profile in ROW_SUM_PROFILES:
            self.assertIn(
                profile_centered_norm_shard(*profile), CENTERED_NORM_SHARDS
            )

    def test_bad_centered_norm_shards_are_rejected(self) -> None:
        for bad_value in (75, 77, 150, True, 76.0):
            with self.subTest(value=bad_value):
                with self.assertRaisesRegex(ValueError, "even integer"):
                    validate_centered_norm_shard(bad_value)  # type: ignore[arg-type]
                with self.assertRaisesRegex(ValueError, "even integer"):
                    build_profile_model(bad_value)  # type: ignore[arg-type]
        with self.assertRaisesRegex(ValueError, "profile symmetry"):
            build_profile_model(profile_symmetry="invalid")

    def test_basic_symmetry_keeps_a_canonical_orbit_representative(self) -> None:
        self.assertEqual(PROFILE_SYMMETRY_MODES, ("none", "basic"))
        canonical_a, canonical_b = canonical_profile(*ROW_SUM_PROFILES[0])
        shard = profile_centered_norm_shard(canonical_a, canonical_b)
        model, z, w = build_profile_model(
            centered_norm_shard=shard, profile_symmetry="basic"
        )
        for variable, row_sum in zip(z, canonical_a, strict=True):
            model.add(variable == (row_sum - 1) // 2)
        for variable, row_sum in zip(w, canonical_b, strict=True):
            model.add(variable == (row_sum - 1) // 2)
        self.assertFalse(model.validate())
        solver = configure_solver(
            time_limit=2.0,
            random_seed=668,
            max_memory_mb=DEFAULT_MAX_MEMORY_MB,
        )
        self.assertIn(solver.solve(model), (cp_model.FEASIBLE, cp_model.OPTIMAL))

    def test_basic_symmetry_has_a_constructive_representative_in_each_orbit(
        self,
    ) -> None:
        for profile_index, (a, b) in enumerate(ROW_SUM_PROFILES):
            with self.subTest(profile=profile_index):
                maximal_a = max(_dihedral_images(a))
                maximal_b = max(_dihedral_images(b))
                representative = max(
                    (maximal_a, maximal_b),
                    (maximal_b, maximal_a),
                )
                self.assertEqual(
                    representative[0], max(_dihedral_images(representative[0]))
                )
                self.assertEqual(
                    representative[1], max(_dihedral_images(representative[1]))
                )
                self.assertGreaterEqual(representative[0], representative[1])
                self.assertIn(representative, _independent_profile_orbit(a, b))

    def test_catalog_hints_respect_the_selected_shard(self) -> None:
        model, z, w = build_profile_model(centered_norm_shard=136)
        hinted_profile = add_catalog_hint(
            model, z, w, random_seed=668, centered_norm_shard=136
        )
        self.assertIsNotNone(hinted_profile)
        assert hinted_profile is not None
        self.assertEqual(
            profile_centered_norm_shard(*ROW_SUM_PROFILES[hinted_profile]),
            136,
        )
        self.assertEqual(len(model.proto.solution_hint.vars), 18)

        unhinted_model, unhinted_z, unhinted_w = build_profile_model(
            centered_norm_shard=76
        )
        self.assertIsNone(
            add_catalog_hint(
                unhinted_model,
                unhinted_z,
                unhinted_w,
                random_seed=668,
                centered_norm_shard=76,
            )
        )
        self.assertEqual(len(unhinted_model.proto.solution_hint.vars), 0)

    def test_catalog_orbit_exclusion_rejects_every_known_orientation(self) -> None:
        raw_a, raw_b = ROW_SUM_PROFILES[0]
        shard = profile_centered_norm_shard(raw_a, raw_b)
        model, z, w = build_profile_model(centered_norm_shard=shard)
        orbit_count, assignment_count = exclude_catalog_orbits(
            model, z, w, centered_norm_shard=shard
        )
        self.assertEqual(orbit_count, 1)
        self.assertEqual(assignment_count, len(profile_orbit(raw_a, raw_b)))
        self.assertGreater(assignment_count, 0)
        for variable, row_sum in zip(z, raw_a, strict=True):
            model.add(variable == (row_sum - 1) // 2)
        for variable, row_sum in zip(w, raw_b, strict=True):
            model.add(variable == (row_sum - 1) // 2)
        self.assertFalse(model.validate())

        solver = configure_solver(
            time_limit=2.0,
            random_seed=668,
            max_memory_mb=DEFAULT_MAX_MEMORY_MB,
        )
        self.assertEqual(solver.solve(model), cp_model.INFEASIBLE)

    def test_catalog_exclusion_table_is_exactly_the_selected_orbit_union(
        self,
    ) -> None:
        shard = 82
        selected_profiles = tuple(
            profile
            for profile in ROW_SUM_PROFILES
            if profile_centered_norm_shard(*profile) == shard
        )
        expected_assignments = {
            tuple((value - 1) // 2 for value in image_a + image_b)
            for profile in selected_profiles
            for image_a, image_b in _independent_profile_orbit(*profile)
        }
        model, z, w = build_profile_model(
            centered_norm_shard=shard, profile_symmetry="basic"
        )
        orbit_count, assignment_count = exclude_catalog_orbits(
            model, z, w, centered_norm_shard=shard
        )
        tables = [
            constraint.table
            for constraint in model.proto.constraints
            if constraint.name == "exclude_catalog_profile_orbits"
        ]
        self.assertEqual(len(tables), 1)
        table = tables[0]
        self.assertTrue(table.negated)
        self.assertEqual(len(table.exprs), 18)
        self.assertEqual(
            tuple(expression.vars[0] for expression in table.exprs),
            tuple(range(18)),
        )
        actual_assignments = {
            tuple(table.values[start : start + 18])
            for start in range(0, len(table.values), 18)
        }
        self.assertEqual(orbit_count, len(selected_profiles))
        self.assertEqual(assignment_count, len(expected_assignments))
        self.assertEqual(actual_assignments, expected_assignments)

    def test_profile_17_is_exact_canonical_and_orbit_distinct(self) -> None:
        profile = ROW_SUM_PROFILES[17]
        a, b = profile

        def paf(vector: tuple[int, ...], lag: int) -> int:
            return sum(
                vector[index] * vector[(index + lag) % 9]
                for index in range(9)
            )

        self.assertEqual(sum(a), 1)
        self.assertEqual(sum(b), 1)
        self.assertEqual(
            tuple(paf(a, lag) + paf(b, lag) for lag in range(9)),
            EXACT_COMBINED_PAF,
        )
        self.assertEqual(profile_centered_norm_shard(a, b), 82)
        self.assertEqual(canonical_profile(a, b), profile)
        self.assertNotIn(
            profile,
            {canonical_profile(*earlier) for earlier in ROW_SUM_PROFILES[:17]},
        )
        self.assertEqual(len(_independent_profile_orbit(a, b)), 1_944)

    def test_excluding_catalog_disables_the_conflicting_hint(self) -> None:
        stream = io.StringIO()
        result = sample_to_stream(
            stream,
            count=1,
            time_limit=0.1,
            random_seed=0,
            max_memory_mb=DEFAULT_MAX_MEMORY_MB,
            centered_norm_shard=136,
            exclude_catalog=True,
        )
        document = json.loads(stream.getvalue())
        self.assertIsNone(document["catalog_hint_profile"])
        self.assertEqual(document["catalog_orbits_excluded"], 1)
        self.assertGreater(document["catalog_oriented_assignments_excluded"], 0)
        self.assertEqual(document["profile_symmetry"], "basic")
        self.assertEqual(result["profile_count"], len(document["profiles"]))

    def test_count_one_shard_stops_nonexhaustively_with_metadata(self) -> None:
        stream = io.StringIO()
        result = sample_to_stream(
            stream,
            count=1,
            time_limit=0.5,
            random_seed=0,
            max_memory_mb=DEFAULT_MAX_MEMORY_MB,
            centered_norm_shard=136,
        )
        document = json.loads(stream.getvalue())
        self.assertEqual(document["centered_norm_shard"], 136)
        self.assertEqual(document["catalog_hint_profile"], 0)
        self.assertEqual(result["centered_norm_shard"], 136)
        self.assertEqual(result["profile_count"], 1)
        self.assertTrue(result["stopped_after_requested_count"])
        self.assertFalse(result["exhaustive"])
        self.assertFalse(result["shard_exhaustive"])

    def test_catalog_profile_payload_is_canonical_and_noncertifying(self) -> None:
        a, b = canonical_profile(*ROW_SUM_PROFILES[0])
        payload = profile_payload(0, a, b)
        self.assertEqual(payload["row_sums_a"], list(a))
        self.assertEqual(payload["row_sums_b"], list(b))
        self.assertEqual(
            payload["combined_cyclic_paf_0_through_8"],
            [594] + [-74] * 8,
        )
        self.assertTrue(payload["compressed_constraints_verified"])
        self.assertFalse(payload["full_legendre_pair_verified"])
        self.assertFalse(payload["hadamard_668_verified"])

    def test_noncanonical_and_tampered_profiles_are_rejected(self) -> None:
        raw_a, raw_b = ROW_SUM_PROFILES[0]
        canonical_a, canonical_b = canonical_profile(raw_a, raw_b)
        self.assertNotEqual((raw_a, raw_b), (canonical_a, canonical_b))
        with self.assertRaisesRegex(ValueError, "not the canonical"):
            validate_canonical_profile(raw_a, raw_b)

        tampered = list(canonical_a)
        tampered[0] += 2
        with self.assertRaises(ValueError):
            validate_canonical_profile(tampered, canonical_b)

    def test_pinned_model_streams_one_valid_canonical_profile(self) -> None:
        raw_a, raw_b = ROW_SUM_PROFILES[0]
        shard = profile_centered_norm_shard(raw_a, raw_b)
        model, z, w = build_profile_model(centered_norm_shard=shard)
        for variable, row_sum in zip(z, raw_a, strict=True):
            model.add(variable == (row_sum - 1) // 2)
        for variable, row_sum in zip(w, raw_b, strict=True):
            model.add(variable == (row_sum - 1) // 2)
        self.assertFalse(model.validate())

        stream = io.StringIO()
        writer = JsonSampleWriter(stream, {"schema": "test"})
        collector = CanonicalProfileCollector(z, w, writer, count_limit=1)
        solver = configure_solver(
            time_limit=2.0,
            random_seed=668,
            max_memory_mb=DEFAULT_MAX_MEMORY_MB,
        )
        status = solver.solve(model, collector)
        self.assertIn(status, (cp_model.FEASIBLE, cp_model.OPTIMAL))
        writer.finish({"solver_status": solver.status_name(status)})

        document = json.loads(stream.getvalue())
        self.assertEqual(len(document["profiles"]), 1)
        self.assertEqual(collector.profile_count, 1)
        expected_a, expected_b = canonical_profile(raw_a, raw_b)
        self.assertEqual(document["profiles"][0]["row_sums_a"], list(expected_a))
        self.assertEqual(document["profiles"][0]["row_sums_b"], list(expected_b))
        self.assertTrue(collector.stopped_after_count)
        self.assertFalse(status == cp_model.OPTIMAL and not collector.stopped_after_count)

    def test_solver_defaults_are_one_worker_and_128_mib(self) -> None:
        solver = configure_solver(
            time_limit=1.0,
            random_seed=668,
            max_memory_mb=DEFAULT_MAX_MEMORY_MB,
        )
        self.assertEqual(solver.parameters.num_search_workers, 1)
        self.assertEqual(solver.parameters.max_memory_in_mb, 128)
        self.assertTrue(solver.parameters.enumerate_all_solutions)


if __name__ == "__main__":
    unittest.main()
