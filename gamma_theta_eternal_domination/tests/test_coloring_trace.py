"""Adversarial tests for exhaustive theta lower-bound certificates."""

from __future__ import annotations

from itertools import combinations, product
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


CAMPAIGN_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(CAMPAIGN_ROOT / "src"))

from verifier_b.coloring_trace_checker import (  # noqa: E402
    TraceVerificationError,
    check_uncolorability_trace,
    verify_uncolorability_trace,
)
from verifier_b.coloring_trace_generator import (  # noqa: E402
    ColorableGraphError,
    write_uncolorability_trace,
)
from verifier_b.graph import Graph, complete_graph, cycle_graph, edgeless_graph  # noqa: E402


def all_labeled_graphs(order: int):
    possible_edges = tuple(combinations(range(order), 2))
    for choices in product((False, True), repeat=len(possible_edges)):
        yield Graph.from_edges(
            order,
            (
                edge
                for edge, chosen in zip(possible_edges, choices)
                if chosen
            ),
        )


def transparent_is_colorable(graph: Graph, color_count: int) -> bool:
    if graph.order == 0:
        return True
    return any(
        all(colors[first] != colors[second] for first, second in graph.edges())
        for colors in product(range(color_count), repeat=graph.order)
    )


def read_lines(path: Path) -> list[dict[str, object]]:
    return [json.loads(line) for line in path.read_text(encoding="ascii").splitlines()]


def write_lines(path: Path, records: list[dict[str, object]]) -> None:
    path.write_text(
        "".join(
            json.dumps(record, sort_keys=True, separators=(",", ":")) + "\n"
            for record in records
        ),
        encoding="ascii",
    )


class ColoringTraceTests(unittest.TestCase):
    def test_c5_theta_greater_than_two_round_trip(self):
        graph = cycle_graph(5)
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "c5-k2.ndjson"
            generated = write_uncolorability_trace(graph, 2, path)
            checked = check_uncolorability_trace(
                path, expected_graph=graph, expected_k=2
            )
            self.assertGreater(generated.node_count, 0)
            self.assertEqual(checked.node_count, generated.node_count)
            self.assertEqual(checked.trace_sha256, generated.trace_sha256)
            self.assertEqual(
                checked.certificate_sha256, generated.certificate_sha256
            )
            records = read_lines(path)
            self.assertEqual(records[1]["vertex"], 0)
            self.assertEqual(records[1]["legal_colors"], [0, 1])

    def test_published_near_miss_theta_greater_than_three(self):
        graph = Graph.from_graph6("IEhbtj{ro")
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "mmv001-k3.ndjson"
            generated = write_uncolorability_trace(graph, 3, path)
            self.assertTrue(
                verify_uncolorability_trace(
                    path, expected_graph=graph, expected_k=3
                )
            )
            self.assertGreater(generated.node_count, 1)

    def test_colorable_claim_is_rejected_without_output(self):
        cases = (
            (complete_graph(5), 1),
            (edgeless_graph(5), 5),
            (cycle_graph(5), 3),
            (edgeless_graph(0), 0),
        )
        with tempfile.TemporaryDirectory() as directory:
            for index, (graph, color_count) in enumerate(cases):
                path = Path(directory) / f"false-{index}.ndjson"
                with self.assertRaises(ColorableGraphError):
                    write_uncolorability_trace(graph, color_count, path)
                self.assertFalse(path.exists())

    def test_zero_colors_proves_every_nonempty_complement_uncolorable(self):
        graph = complete_graph(2)
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "k0.ndjson"
            summary = write_uncolorability_trace(graph, 0, path)
            self.assertEqual(summary.node_count, 1)
            self.assertTrue(verify_uncolorability_trace(path, expected_k=0))

    def test_huge_color_counts_and_json_integers_fail_closed(self):
        graph = complete_graph(2)
        enormous_color_count = 1 << 100_000
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            output = root / "false-claim.ndjson"
            with self.assertRaises(ColorableGraphError):
                write_uncolorability_trace(
                    graph, enormous_color_count, output
                )
            self.assertFalse(output.exists())

            parseable = root / "parseable-huge-k.ndjson"
            header = {
                "claim_sha256": "x",
                "format": "gamma-theta-complement-coloring-unsat-v1",
                "graph6": "@",
                "graph6_sha256": "x",
                "k": 10**3000,
                "type": "header",
                "vertex_order": "least-uncolored",
            }
            write_lines(parseable, [header])
            self.assertFalse(verify_uncolorability_trace(parseable))

            digit_limit = root / "digit-limit.ndjson"
            digit_limit.write_bytes(
                b'{"claim_sha256":"x","format":'
                b'"gamma-theta-complement-coloring-unsat-v1",'
                b'"graph6":"@","graph6_sha256":"x","k":'
                + b"9" * 5000
                + b',"type":"header","vertex_order":"least-uncolored"}\n'
            )
            self.assertFalse(verify_uncolorability_trace(digit_limit))

    def test_every_labeled_graph_through_order_five(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            case = 0
            for order in range(6):
                for graph in all_labeled_graphs(order):
                    complement = graph.complement()
                    for color_count in range(order + 1):
                        path = root / f"case-{case}.ndjson"
                        case += 1
                        is_colorable = transparent_is_colorable(
                            complement, color_count
                        )
                        if is_colorable:
                            with self.assertRaises(ColorableGraphError):
                                write_uncolorability_trace(
                                    graph, color_count, path
                                )
                            self.assertFalse(path.exists())
                        else:
                            write_uncolorability_trace(graph, color_count, path)
                            self.assertTrue(
                                verify_uncolorability_trace(
                                    path,
                                    expected_graph=graph,
                                    expected_k=color_count,
                                ),
                                (graph.to_graph6(), color_count),
                            )
                            path.unlink()

    def test_external_claim_binding(self):
        graph = cycle_graph(5)
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "proof.ndjson"
            write_uncolorability_trace(graph, 2, path)
            with self.assertRaises(TraceVerificationError):
                check_uncolorability_trace(path, expected_graph=cycle_graph(6))
            with self.assertRaises(TraceVerificationError):
                check_uncolorability_trace(path, expected_k=3)

    def test_tree_and_footer_tampering_is_rejected(self):
        graph = cycle_graph(5)
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            original = root / "original.ndjson"
            write_uncolorability_trace(graph, 2, original)
            records = read_lines(original)

            variants: list[list[dict[str, object]]] = []

            wrong_graph_hash = [dict(record) for record in records]
            wrong_graph_hash[0]["graph6_sha256"] = "0" * 64
            variants.append(wrong_graph_hash)

            wrong_claim_hash = [dict(record) for record in records]
            wrong_claim_hash[0]["k"] = 3
            variants.append(wrong_claim_hash)

            wrong_vertex = [dict(record) for record in records]
            wrong_vertex[1]["vertex"] = 1
            variants.append(wrong_vertex)

            omitted_color = [dict(record) for record in records]
            omitted_color[1]["legal_colors"] = [0]
            variants.append(omitted_color)

            reordered_colors = [dict(record) for record in records]
            reordered_colors[1]["legal_colors"] = [1, 0]
            variants.append(reordered_colors)

            boolean_colors = [dict(record) for record in records]
            boolean_colors[1]["legal_colors"] = [False, True]
            variants.append(boolean_colors)

            floating_colors = [dict(record) for record in records]
            floating_colors[1]["legal_colors"] = [0.0, 1.0]
            variants.append(floating_colors)

            extra_field = [dict(record) for record in records]
            extra_field[1]["pruned_by"] = "wishful thinking"
            variants.append(extra_field)

            bad_count = [dict(record) for record in records]
            bad_count[-1]["node_count"] = int(bad_count[-1]["node_count"]) + 1
            variants.append(bad_count)

            bad_trace_hash = [dict(record) for record in records]
            bad_trace_hash[-1]["trace_sha256"] = "f" * 64
            variants.append(bad_trace_hash)

            truncated = [dict(record) for record in records[:-2]] + [
                dict(records[-1])
            ]
            variants.append(truncated)

            extra_after_footer = [dict(record) for record in records] + [
                {"legal_colors": [], "type": "node", "vertex": 0}
            ]
            variants.append(extra_after_footer)

            for index, variant in enumerate(variants):
                path = root / f"tampered-{index}.ndjson"
                write_lines(path, variant)
                self.assertFalse(
                    verify_uncolorability_trace(
                        path, expected_graph=graph, expected_k=2
                    ),
                    index,
                )

    def test_malformed_stream_records_are_rejected(self):
        graph = cycle_graph(5)
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            original = root / "original.ndjson"
            write_uncolorability_trace(graph, 2, original)
            raw_lines = original.read_bytes().splitlines(keepends=True)

            duplicate_key = root / "duplicate.ndjson"
            duplicate_key.write_bytes(
                raw_lines[0]
                + b'{"legal_colors":[0,1],"type":"node","vertex":0,"vertex":0}\n'
                + b"".join(raw_lines[2:])
            )
            self.assertFalse(verify_uncolorability_trace(duplicate_key))

            missing_newline = root / "missing-newline.ndjson"
            missing_newline.write_bytes(b"".join(raw_lines).rstrip(b"\n"))
            self.assertFalse(verify_uncolorability_trace(missing_newline))

            non_json = root / "non-json.ndjson"
            non_json.write_bytes(raw_lines[0] + b"not-json\n")
            self.assertFalse(verify_uncolorability_trace(non_json))

            blank_after_footer = root / "blank-after-footer.ndjson"
            blank_after_footer.write_bytes(b"".join(raw_lines) + b"\n")
            self.assertFalse(verify_uncolorability_trace(blank_after_footer))

    def test_existing_output_is_preserved_without_overwrite(self):
        graph = cycle_graph(5)
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "proof.ndjson"
            path.write_bytes(b"keep me")
            with self.assertRaises(FileExistsError):
                write_uncolorability_trace(graph, 2, path)
            self.assertEqual(path.read_bytes(), b"keep me")

    def test_cli_generate_and_verify(self):
        graph6 = cycle_graph(5).to_graph6()
        environment = {
            **dict(os.environ),
            "PYTHONPATH": str(CAMPAIGN_ROOT / "src"),
        }
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "c5.ndjson"
            generated = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "verifier_b.coloring_trace_cli",
                    "generate",
                    graph6,
                    "2",
                    str(path),
                ],
                cwd=CAMPAIGN_ROOT,
                env=environment,
                check=True,
                capture_output=True,
                text=True,
            )
            self.assertTrue(json.loads(generated.stdout)["ok"])
            verified = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "verifier_b.coloring_trace_cli",
                    "verify",
                    str(path),
                    "--graph6",
                    graph6,
                    "--k",
                    "2",
                ],
                cwd=CAMPAIGN_ROOT,
                env=environment,
                check=True,
                capture_output=True,
                text=True,
            )
            self.assertTrue(json.loads(verified.stdout)["ok"])


if __name__ == "__main__":
    unittest.main()
