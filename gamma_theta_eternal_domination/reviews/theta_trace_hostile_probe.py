#!/usr/bin/env python3
"""Independent hostile probes for complement-coloring trace certificates.

This review-only program deliberately does not import verifier A, the search
stack, verifier B's invariant/coloring routines, or the checked-in trace
tests.  Truth is computed directly as a partition of V(G) into at most k
cliques using a Boolean adjacency matrix.  A second replay implementation
checks generated traces without calling the campaign checker.
"""

from __future__ import annotations

from hashlib import sha256
from itertools import combinations, product
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import time


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from verifier_b.coloring_trace_checker import (  # noqa: E402
    TraceVerificationError,
    check_uncolorability_trace,
    verify_uncolorability_trace,
)
from verifier_b.coloring_trace_generator import (  # noqa: E402
    ColorableGraphError,
    write_uncolorability_trace,
)
from verifier_b.graph import Graph  # noqa: E402


Matrix = tuple[tuple[bool, ...], ...]
FORMAT = "gamma-theta-complement-coloring-unsat-v1"


def matrix_from_edge_mask(order: int, edge_mask: int) -> Matrix:
    rows = [[False] * order for _ in range(order)]
    position = 0
    for first in range(order):
        for second in range(first + 1, order):
            if edge_mask & (1 << position):
                rows[first][second] = rows[second][first] = True
            position += 1
    return tuple(tuple(row) for row in rows)


def edges(matrix: Matrix) -> tuple[tuple[int, int], ...]:
    return tuple(
        (first, second)
        for first in range(len(matrix))
        for second in range(first + 1, len(matrix))
        if matrix[first][second]
    )


def clique_partition_colorable(matrix: Matrix, color_count: int) -> bool:
    """Definition-level theta <= k oracle, without constructing a complement."""

    order = len(matrix)
    assignment = [-1] * order

    def extend(vertex: int) -> bool:
        if vertex == order:
            return True
        for color in range(color_count):
            if all(
                assignment[earlier] != color or matrix[earlier][vertex]
                for earlier in range(vertex)
            ):
                assignment[vertex] = color
                if extend(vertex + 1):
                    return True
        assignment[vertex] = -1
        return False

    return extend(0)


def independent_graph6_matrix(record: str) -> Matrix:
    """Decode the campaign's small (n <= 62) graph6 records independently."""

    values = [ord(character) - 63 for character in record]
    if not values or values[0] < 0 or values[0] > 62:
        raise ValueError("probe accepts only the one-byte graph6 order format")
    order = values[0]
    expected = (order * (order - 1) // 2 + 5) // 6
    if len(values) != 1 + expected:
        raise ValueError("wrong graph6 length")
    bits = [
        (value >> shift) & 1
        for value in values[1:]
        for shift in range(5, -1, -1)
    ]
    rows = [[False] * order for _ in range(order)]
    position = 0
    for higher in range(1, order):
        for lower in range(higher):
            if bits[position]:
                rows[lower][higher] = rows[higher][lower] = True
            position += 1
    if any(bits[position:]):
        raise ValueError("nonzero graph6 padding")
    return tuple(tuple(row) for row in rows)


def canonical_line(value: object) -> bytes:
    return (
        json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
        + "\n"
    ).encode("ascii")


def graph_digest(graph6: str) -> str:
    return sha256(b"graph6\x00" + graph6.encode("ascii")).hexdigest()


def claim_digest(graph6: str, color_count: int) -> str:
    return sha256(
        b"gamma-theta-complement-coloring-unsat-v1\x00"
        + graph6.encode("ascii")
        + b"\x00"
        + str(color_count).encode("ascii")
    ).hexdigest()


def independent_replay(
    path: Path, expected_matrix: Matrix, expected_graph6: str, expected_k: int
) -> int:
    """Replay a generator output using only the direct clique condition."""

    raw_lines = path.read_bytes().splitlines(keepends=True)
    if not raw_lines or any(not line.endswith(b"\n") for line in raw_lines):
        raise AssertionError("malformed generated line endings")
    records = [json.loads(line) for line in raw_lines]
    header = records[0]
    assert header == {
        "claim_sha256": claim_digest(expected_graph6, expected_k),
        "format": FORMAT,
        "graph6": expected_graph6,
        "graph6_sha256": graph_digest(expected_graph6),
        "k": expected_k,
        "type": "header",
        "vertex_order": "least-uncolored",
    }

    assignment = [-1] * len(expected_matrix)
    cursor = 1
    node_lines: list[bytes] = []

    def replay(vertex: int) -> None:
        nonlocal cursor
        if vertex == len(expected_matrix):
            raise AssertionError("certificate reaches a complete clique partition")
        if cursor >= len(records):
            raise AssertionError("truncated generated tree")
        node = records[cursor]
        cursor += 1
        expected_legal = [
            color
            for color in range(expected_k)
            if all(
                assignment[earlier] != color
                or expected_matrix[earlier][vertex]
                for earlier in range(vertex)
            )
        ]
        assert node == {
            "legal_colors": expected_legal,
            "type": "node",
            "vertex": vertex,
        }
        node_lines.append(canonical_line(node))
        for color in expected_legal:
            assignment[vertex] = color
            replay(vertex + 1)
            assignment[vertex] = -1

    replay(0)
    if cursor != len(records) - 1:
        raise AssertionError("extra/missing records around generated footer")
    footer = records[cursor]
    trace_hash = sha256(b"".join(node_lines)).hexdigest()
    assert footer == {
        "node_count": len(node_lines),
        "trace_sha256": trace_hash,
        "type": "footer",
    }
    return len(node_lines)


def write_records(path: Path, records: list[object]) -> None:
    path.write_bytes(b"".join(canonical_line(record) for record in records))


def assert_rejected(path: Path, *, graph: Graph | None = None, k: int | None = None) -> None:
    if verify_uncolorability_trace(path, expected_graph=graph, expected_k=k):
        raise AssertionError(f"tampered proof accepted: {path.name}")


def mutation_probes(root: Path) -> int:
    matrix = matrix_from_edge_mask(
        5,
        sum(
            1 << position
            for position, edge in enumerate(combinations(range(5), 2))
            if edge in {(0, 1), (1, 2), (2, 3), (3, 4), (0, 4)}
        ),
    )
    graph = Graph.from_edges(5, edges(matrix))
    original = root / "c5.ndjson"
    write_uncolorability_trace(graph, 2, original)
    raw = original.read_bytes()
    records = [json.loads(line) for line in raw.splitlines()]
    rejected = 0

    # Every proper byte prefix is an incomplete proof.
    truncation = root / "truncated.ndjson"
    for cut in range(len(raw)):
        truncation.write_bytes(raw[:cut])
        assert_rejected(truncation, graph=graph, k=2)
        rejected += 1

    variants: list[list[object]] = []

    changed_k = [dict(record) for record in records]
    changed_k[0]["k"] = 3
    changed_k[0]["claim_sha256"] = claim_digest(graph.to_graph6(), 3)
    variants.append(changed_k)

    singleton = Graph.from_edges(1, ()).to_graph6()
    changed_graph = [dict(record) for record in records]
    changed_graph[0]["graph6"] = singleton
    changed_graph[0]["graph6_sha256"] = graph_digest(singleton)
    changed_graph[0]["claim_sha256"] = claim_digest(singleton, 2)
    variants.append(changed_graph)

    for root_colors in ([0], [1, 0], [0, 1, 2], [0, 0], [False, 1]):
        changed = [dict(record) for record in records]
        changed[1]["legal_colors"] = root_colors
        variants.append(changed)

    wrong_vertex = [dict(record) for record in records]
    wrong_vertex[1]["vertex"] = 1
    variants.append(wrong_vertex)

    missing_node = [dict(record) for record in records]
    del missing_node[len(missing_node) // 2]
    variants.append(missing_node)

    duplicate_node = [dict(record) for record in records]
    duplicate_node.insert(2, dict(duplicate_node[1]))
    variants.append(duplicate_node)

    early_footer = [dict(records[0]), dict(records[-1])] + [
        dict(record) for record in records[1:-1]
    ]
    variants.append(early_footer)

    bad_count = [dict(record) for record in records]
    bad_count[-1]["node_count"] = -1
    variants.append(bad_count)

    bad_hash = [dict(record) for record in records]
    bad_hash[-1]["trace_sha256"] = "0" * 64
    variants.append(bad_hash)

    extra_record = [dict(record) for record in records] + [{"type": "extra"}]
    variants.append(extra_record)

    extra_field = [dict(record) for record in records]
    extra_field[1]["shortcut"] = "unverified"
    variants.append(extra_field)

    for index, variant in enumerate(variants):
        path = root / f"mutation-{index}.ndjson"
        write_records(path, variant)
        assert_rejected(path, graph=graph, k=2)
        rejected += 1

    raw_variants = {
        "duplicate-key": (
            raw.splitlines(keepends=True)[0]
            + b'{"legal_colors":[0,1],"type":"node","vertex":0,"vertex":0}\n'
            + b"".join(raw.splitlines(keepends=True)[2:])
        ),
        "non-ascii": b"\xff\n",
        "non-json": b"not-json\n",
        "blank-prefix": b"\n" + raw,
        "blank-suffix": raw + b"\n",
        "nul-suffix": raw + b"\x00",
        "missing-final-lf": raw.rstrip(b"\n"),
    }
    for name, content in raw_variants.items():
        path = root / f"{name}.ndjson"
        path.write_bytes(content)
        assert_rejected(path, graph=graph, k=2)
        rejected += 1

    # Python's JSON decoder raises a plain ValueError for an over-limit integer.
    huge_integer = root / "huge-integer.ndjson"
    huge_integer.write_bytes(
        b'{"claim_sha256":"x","format":"'
        + FORMAT.encode("ascii")
        + b'","graph6":"@","graph6_sha256":"x","k":'
        + b"9" * 5000
        + b',"type":"header","vertex_order":"least-uncolored"}\n'
    )
    assert not verify_uncolorability_trace(huge_integer)
    try:
        check_uncolorability_trace(huge_integer)
    except TraceVerificationError as error:
        assert "invalid JSON" in str(error)
    else:
        raise AssertionError("digit-limit JSON was not normalized and rejected")

    parseable_huge = root / "parseable-huge-integer.ndjson"
    parseable_k = 10**3000
    write_records(
        parseable_huge,
        [
            {
                "claim_sha256": "x",
                "format": FORMAT,
                "graph6": "@",
                "graph6_sha256": "x",
                "k": parseable_k,
                "type": "header",
                "vertex_order": "least-uncolored",
            }
        ],
    )
    assert not verify_uncolorability_trace(parseable_huge)
    try:
        check_uncolorability_trace(parseable_huge)
    except TraceVerificationError as error:
        assert "claimed lower bound is false" in str(error)
    else:
        raise AssertionError("parseable huge k was not rejected before replay")

    return rejected


def cli_probes(root: Path) -> int:
    environment = {**os.environ, "PYTHONPATH": str(ROOT / "src")}
    base = [
        sys.executable,
        "-m",
        "verifier_b.coloring_trace_cli",
    ]
    checks = 0

    valid = root / "cli-c5.ndjson"
    process = subprocess.run(
        base + ["generate", "Dhc", "2", str(valid)],
        cwd=ROOT,
        env=environment,
        capture_output=True,
        text=True,
    )
    assert process.returncode == 0 and json.loads(process.stdout)["ok"]
    checks += 1

    for suffix, expected_code in (
        (["verify", str(valid), "--graph6", "Dhc", "--k", "2"], 0),
        (["verify", str(valid), "--graph6", "Dhc", "--k", "3"], 1),
        (["verify", str(valid), "--graph6", "@"], 1),
        (["verify", str(root / "missing.ndjson")], 1),
    ):
        process = subprocess.run(
            base + suffix,
            cwd=ROOT,
            env=environment,
            capture_output=True,
            text=True,
        )
        assert process.returncode == expected_code
        checks += 1

    false_path = root / "false-cli.ndjson"
    for graph6, color_count in (("Dhc", "3"), ("?", "0"), ("@", "1")):
        process = subprocess.run(
            base + ["generate", graph6, color_count, str(false_path)],
            cwd=ROOT,
            env=environment,
            capture_output=True,
            text=True,
        )
        assert process.returncode == 2 and not false_path.exists()
        checks += 1

    for graph6, color_count in (("Dhc", "-1"), ("??", "0")):
        process = subprocess.run(
            base + ["generate", graph6, color_count, str(false_path)],
            cwd=ROOT,
            env=environment,
            capture_output=True,
            text=True,
        )
        assert process.returncode == 2 and not false_path.exists()
        checks += 1

    process = subprocess.run(
        base + ["generate", "@", "9" * 3000, str(false_path)],
        cwd=ROOT,
        env=environment,
        capture_output=True,
        text=True,
    )
    assert process.returncode == 2 and not false_path.exists()
    checks += 1

    singleton_zero = root / "cli-singleton-k0.ndjson"
    process = subprocess.run(
        base + ["generate", "@", "0", str(singleton_zero)],
        cwd=ROOT,
        env=environment,
        capture_output=True,
        text=True,
    )
    assert process.returncode == 0
    checks += 1

    huge_integer = root / "cli-huge-integer.ndjson"
    huge_integer.write_bytes(
        b'{"claim_sha256":"x","format":"'
        + FORMAT.encode("ascii")
        + b'","graph6":"@","graph6_sha256":"x","k":'
        + b"9" * 5000
        + b',"type":"header","vertex_order":"least-uncolored"}\n'
    )
    process = subprocess.run(
        base + ["verify", str(huge_integer)],
        cwd=ROOT,
        env=environment,
        capture_output=True,
        text=True,
    )
    assert process.returncode == 1
    checks += 1
    return checks


def main() -> None:
    started = time.perf_counter()
    labeled_graphs = 0
    claims = 0
    true_certificates = 0
    false_claims_rejected = 0
    independently_replayed_nodes = 0

    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        for order in range(6):
            edge_count = order * (order - 1) // 2
            for edge_mask in range(1 << edge_count):
                matrix = matrix_from_edge_mask(order, edge_mask)
                graph = Graph.from_edges(order, edges(matrix))
                graph6 = graph.to_graph6()
                assert independent_graph6_matrix(graph6) == matrix
                labeled_graphs += 1
                for color_count in range(order + 1):
                    claims += 1
                    path = root / "claim.ndjson"
                    truth = clique_partition_colorable(matrix, color_count)
                    if truth:
                        try:
                            write_uncolorability_trace(graph, color_count, path)
                        except ColorableGraphError:
                            false_claims_rejected += 1
                        else:
                            raise AssertionError(
                                f"false proof generated for {(graph6, color_count)}"
                            )
                        assert not path.exists()
                    else:
                        summary = write_uncolorability_trace(
                            graph, color_count, path
                        )
                        checked = check_uncolorability_trace(
                            path, expected_graph=graph, expected_k=color_count
                        )
                        assert checked.node_count == summary.node_count
                        independently_replayed_nodes += independent_replay(
                            path, matrix, graph6, color_count
                        )
                        true_certificates += 1
                        path.unlink()

        # Empty graphs are colorable with every k, including k=0.
        empty = Graph.from_edges(0, ())
        for color_count in (0, 1, 3):
            path = root / f"empty-k{color_count}.ndjson"
            try:
                write_uncolorability_trace(empty, color_count, path)
            except ColorableGraphError:
                pass
            else:
                raise AssertionError("empty graph received a false proof")
            assert not path.exists()

        # A nonempty graph is not 0-colorable; no complement edge is needed.
        singleton = Graph.from_edges(1, ())
        zero_path = root / "singleton-k0.ndjson"
        zero_summary = write_uncolorability_trace(singleton, 0, zero_path)
        assert zero_summary.node_count == 1
        assert verify_uncolorability_trace(
            zero_path, expected_graph=singleton, expected_k=0
        )
        for invalid_k in (-1, True):
            invalid_path = root / f"invalid-k-{invalid_k}.ndjson"
            try:
                write_uncolorability_trace(singleton, invalid_k, invalid_path)
            except (TypeError, ValueError):
                pass
            else:
                raise AssertionError("invalid k was accepted")
        assert not verify_uncolorability_trace(None)  # type: ignore[arg-type]
        assert not verify_uncolorability_trace(zero_path, expected_k=True)
        assert not verify_uncolorability_trace(zero_path, expected_k=-1)

        enormous_color_count = 1 << 100_000
        enormous_path = root / "enormous-generator-k.ndjson"
        try:
            write_uncolorability_trace(
                singleton, enormous_color_count, enormous_path
            )
        except ColorableGraphError as error:
            assert error.coloring == (0,)
        else:
            raise AssertionError("generator did not reject enormous false claim")
        assert not enormous_path.exists()

        # Exercise the graph6 one-byte/18-bit order boundary at k=0.
        order_63 = Graph.from_edges(63, ())
        order_63_path = root / "order63-k0.ndjson"
        write_uncolorability_trace(order_63, 0, order_63_path)
        assert verify_uncolorability_trace(
            order_63_path, expected_graph=order_63, expected_k=0
        )

        # C5 and all 56 exact MMV records get an independent k=3 truth check.
        c5_matrix = independent_graph6_matrix("Dhc")
        assert not clique_partition_colorable(c5_matrix, 2)
        c5_path = root / "c5-target.ndjson"
        write_uncolorability_trace(Graph.from_graph6("Dhc"), 2, c5_path)
        independent_replay(c5_path, c5_matrix, "Dhc", 2)

        mmv_rows = (
            ROOT / "instances" / "mmv2022_table9.csv"
        ).read_text(encoding="ascii").splitlines()[1:]
        mmv_count = 0
        mmv_nodes = 0
        for row in mmv_rows:
            _, _, graph6, *_ = row.split(",")
            matrix = independent_graph6_matrix(graph6)
            assert not clique_partition_colorable(matrix, 3), graph6
            graph = Graph.from_graph6(graph6)
            assert edges(matrix) == tuple(graph.edges())
            path = root / "mmv.ndjson"
            summary = write_uncolorability_trace(
                graph, 3, path, overwrite=True
            )
            checked = check_uncolorability_trace(
                path, expected_graph=graph, expected_k=3
            )
            assert summary.node_count == checked.node_count
            assert independent_replay(path, matrix, graph6, 3) == summary.node_count
            mmv_nodes += summary.node_count
            mmv_count += 1

        rejected_mutations = mutation_probes(root)
        cli_checks = cli_probes(root)

    print(
        json.dumps(
            {
                "claims_checked_through_order_5": claims,
                "cli_checks": cli_checks,
                "false_claims_rejected": false_claims_rejected,
                "independent_oracle": "direct clique-partition recursion",
                "independent_replayed_nodes": independently_replayed_nodes,
                "labeled_graphs_through_order_5": labeled_graphs,
                "mmv_records": mmv_count,
                "mmv_trace_nodes": mmv_nodes,
                "mutated_or_truncated_proofs_rejected": rejected_mutations,
                "outcome": "all soundness comparisons agreed; hardening fixes verified",
                "true_certificates_checked": true_certificates,
                "wall_seconds": time.perf_counter() - started,
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
