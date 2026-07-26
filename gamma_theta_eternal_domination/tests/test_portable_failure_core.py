from __future__ import annotations

from copy import deepcopy
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path
import sys
import tempfile
import unittest


CAMPAIGN = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(CAMPAIGN / "src"))

from search.portable_failure_core import (  # noqa: E402
    EMBEDDING_SPECS,
    EXPECTED_CORE_DATA,
    EXPECTED_DEEP_EXTENSION_KEYS,
    EXPECTED_EXTENSION_PARAMETER_COUNTS,
    EXPECTED_EXTENSION_RANK_COUNTS,
    J_GRAPH6,
    Q_GRAPH6,
    PortableCoreError,
    _audit_extension_rows,
    _core_certificate,
    _embedding_record,
    _extension_rows,
    _find_J_embeddings,
    _occurrence_summary,
    _verify_core,
    _verify_ranked_dag,
    audit_artifacts,
    extension_csv_bytes,
    generate_artifacts,
    read_extension_csv,
    strict_json_load,
    verify_certificate,
)
from search.three_step_kernel import (  # noqa: E402
    KernelGraph,
    is_independent,
    kernel_profile,
)


LABELG = CAMPAIGN / "tools/nauty2_9_3/labelg"


def graph_from_code(order: int, code: int) -> KernelGraph:
    edges = tuple(combinations(range(order), 2))
    return KernelGraph.from_edges(
        order,
        (
            edge
            for position, edge in enumerate(edges)
            if code & (1 << position)
        ),
    )


class PortableFailureCoreTests(unittest.TestCase):
    def test_every_independent_k_state_is_in_each_stable_k_family_small(self) -> None:
        for order in range(1, 5):
            edge_count = order * (order - 1) // 2
            for code in range(1 << edge_count):
                graph = graph_from_code(order, code)
                for guard_count in range(1, order + 1):
                    profile = kernel_profile(graph, guard_count)
                    if not profile.stable_family:
                        continue
                    independent_states = tuple(
                        state
                        for state in range(1 << order)
                        if state.bit_count() == guard_count
                        and is_independent(graph, state)
                    )
                    self.assertTrue(
                        set(independent_states)
                        <= set(profile.stable_family),
                        (graph.to_graph6(), guard_count),
                    )

    def test_fixed_core_profiles_and_ranked_DAGs(self) -> None:
        for record in (J_GRAPH6, Q_GRAPH6):
            with self.subTest(graph6=record):
                core = _core_certificate(record)
                _verify_core(core, record)
                expected = EXPECTED_CORE_DATA[record]
                self.assertEqual(
                    core["kernel_sizes"]["3"],
                    list(expected["kernel_3"]),
                )
                self.assertEqual(
                    core["statistics"]["dag_nodes"],
                    expected["dag_nodes"],
                )
                self.assertEqual(
                    core["statistics"]["unrolled_tree_nodes"],
                    expected["tree_nodes"],
                )

    def test_ranked_DAG_rejects_decisive_mutations(self) -> None:
        core = _core_certificate(J_GRAPH6)
        graph = __import__(
            "coverage_checker.graph", fromlist=["Graph"]
        ).Graph.from_graph6(J_GRAPH6)

        missing_response = deepcopy(core)
        missing_response["ranked_attack_dag"][0]["responses"].pop()
        with self.assertRaisesRegex(
            PortableCoreError, "response count"
        ):
            _verify_ranked_dag(graph, missing_response)

        occupied_attack = deepcopy(core)
        occupied_attack["ranked_attack_dag"][0]["attack"] = (
            occupied_attack["ranked_attack_dag"][0]["configuration"][0]
        )
        with self.assertRaises(PortableCoreError):
            _verify_ranked_dag(graph, occupied_attack)

        wrong_witness = deepcopy(core)
        changed = False
        for row in wrong_witness["ranked_attack_dag"]:
            for response in row["responses"]:
                if "undominated" in response:
                    response["undominated"] = response["successor"][0]
                    changed = True
                    break
            if changed:
                break
        self.assertTrue(changed)
        with self.assertRaisesRegex(PortableCoreError, "witness"):
            _verify_ranked_dag(graph, wrong_witness)

        nondecreasing = deepcopy(core)
        changed = False
        for row in nondecreasing["ranked_attack_dag"]:
            for response in row["responses"]:
                if "successor_rank" in response:
                    response["successor_rank"] = row["rank"]
                    changed = True
                    break
            if changed:
                break
        self.assertTrue(changed)
        with self.assertRaisesRegex(PortableCoreError, "rank"):
            _verify_ranked_dag(graph, nondecreasing)

        wrong_root_rank = deepcopy(core)
        wrong_root_rank["root_rank"] += 1
        with self.assertRaisesRegex(PortableCoreError, "root rank"):
            _verify_ranked_dag(graph, wrong_root_rank)

    def test_all_six_explicit_induced_embeddings(self) -> None:
        for spec in EMBEDDING_SPECS:
            with self.subTest(host=spec.host_graph6):
                row = _embedding_record(spec)
                embeddings = _find_J_embeddings(spec.host_graph6)
                self.assertTrue(embeddings)
                self.assertIn(
                    spec.deleted_vertex,
                    {
                        embedding["deleted_vertex"]
                        for embedding in embeddings
                    },
                )
                self.assertEqual(
                    row["extension_kind"], spec.extension_kind
                )
        self.assertEqual(_find_J_embeddings(Q_GRAPH6), ())

    def test_fixed_526_population_has_exactly_37_J_occurrences(self) -> None:
        summary = _occurrence_summary(CAMPAIGN)
        self.assertEqual(summary["population_size"], 526)
        self.assertEqual(summary["induced_J_occurrence_count"], 37)
        self.assertEqual(
            summary["occurrence_earliest_rank_histogram"],
            {"3": 30, "5": 7},
        )
        self.assertEqual(len(summary["deep_tail"]), 8)
        self.assertEqual(
            sum(
                row["portable_core"] == "J"
                for row in summary["deep_tail"]
            ),
            7,
        )
        self.assertEqual(
            sum(
                row["portable_core"] == "Q"
                for row in summary["deep_tail"]
            ),
            1,
        )

    @unittest.skipUnless(LABELG.is_file(), "pinned labelg is not built")
    def test_complete_J_extension_observation(self) -> None:
        rows, summary = _extension_rows(LABELG)
        self.assertEqual(len(rows), 623)
        self.assertEqual(
            sum(int(row["origin_count"]) for row in rows),
            2047,
        )
        self.assertEqual(
            {
                tuple(entry["values"]): entry["count"]
                for entry in summary["parameter_histogram"]
            },
            EXPECTED_EXTENSION_PARAMETER_COUNTS,
        )
        self.assertEqual(
            {
                int(key): value
                for key, value in (
                    summary["earliest_forced_rank_histogram"].items()
                )
            },
            EXPECTED_EXTENSION_RANK_COUNTS,
        )
        self.assertEqual(
            tuple(summary["deep_extension_graph6"]),
            EXPECTED_DEEP_EXTENSION_KEYS,
        )

    @unittest.skipUnless(LABELG.is_file(), "pinned labelg is not built")
    def test_extension_CSV_round_trip_and_independent_audit(self) -> None:
        rows, expected_summary = _extension_rows(LABELG)
        temporary_root = CAMPAIGN / "results/tmp"
        temporary_root.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(dir=temporary_root) as temporary:
            path = Path(temporary) / "extensions.csv"
            canonical = extension_csv_bytes(rows)
            path.write_bytes(canonical)
            decoded = read_extension_csv(path)
            self.assertEqual(decoded, rows)
            actual_summary = _audit_extension_rows(
                decoded, labelg_path=LABELG
            )
            self.assertEqual(actual_summary, expected_summary)

            header, first_row, remainder = canonical.split(b"\n", 2)
            path.write_bytes(
                header
                + b"\n"
                + first_row
                + b",IGNORED_PAYLOAD\n"
                + remainder
            )
            with self.assertRaisesRegex(
                PortableCoreError, "missing or surplus fields"
            ):
                read_extension_csv(path)

    @unittest.skipUnless(LABELG.is_file(), "pinned labelg is not built")
    def test_artifact_generation_is_deterministic_and_auditable(self) -> None:
        temporary_root = CAMPAIGN / "results/tmp"
        temporary_root.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(dir=temporary_root) as temporary:
            directory = Path(temporary)
            certificate = directory / "certificate.json"
            result = directory / "result.json"
            extensions = directory / "extensions.csv"
            kwargs = {
                "campaign_root": CAMPAIGN,
                "certificate_path": certificate,
                "result_path": result,
                "extension_path": extensions,
                "labelg_path": LABELG,
            }
            first = generate_artifacts(**kwargs)
            second = generate_artifacts(**kwargs)
            self.assertEqual(first, second)
            self.assertEqual(audit_artifacts(**kwargs), first)
            verify_certificate(
                strict_json_load(certificate), campaign_root=CAMPAIGN
            )

            extensions.write_bytes(extensions.read_bytes() + b"\n")
            noncanonical = strict_json_load(result)
            noncanonical["bindings"]["extension_table_sha256"] = sha256(
                extensions.read_bytes()
            ).hexdigest()
            result.write_text(
                json.dumps(noncanonical, sort_keys=True),
                encoding="ascii",
            )
            with self.assertRaisesRegex(
                PortableCoreError, "bytes are not canonical"
            ):
                audit_artifacts(**kwargs)

            self.assertEqual(generate_artifacts(**kwargs), first)
            tampered = strict_json_load(result)
            tampered["limitations"] = ["FALSE: this resolves all graphs"]
            result.write_text(
                json.dumps(tampered, sort_keys=True),
                encoding="ascii",
            )
            with self.assertRaisesRegex(
                PortableCoreError, "payload differs from exact replay"
            ):
                audit_artifacts(**kwargs)

            self.assertEqual(generate_artifacts(**kwargs), first)
            tampered = json.loads(result.read_text(encoding="ascii"))
            tampered["fixed_population"]["population_size"] = 525
            result.write_text(
                json.dumps(tampered, sort_keys=True),
                encoding="ascii",
            )
            with self.assertRaisesRegex(
                PortableCoreError, "occurrence summary"
            ):
                audit_artifacts(**kwargs)


if __name__ == "__main__":
    unittest.main()
