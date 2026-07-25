"""Independent replay checker for complement-coloring UNSAT traces.

The verifier reconstructs the coloring state from the certificate's preorder
records.  It does not call the generator or either exact coloring solver.
"""

from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
import json
import os
from pathlib import Path
from typing import Any, BinaryIO

from .graph import Graph


FORMAT_NAME = "gamma-theta-complement-coloring-unsat-v1"
VERTEX_ORDER = "least-uncolored"
_HEADER_KEYS = {
    "claim_sha256",
    "format",
    "graph6",
    "graph6_sha256",
    "k",
    "type",
    "vertex_order",
}
_NODE_KEYS = {"legal_colors", "type", "vertex"}
_FOOTER_KEYS = {"node_count", "trace_sha256", "type"}


class TraceVerificationError(ValueError):
    """A malformed trace or failed proof obligation."""


@dataclass(frozen=True, slots=True)
class TraceCheck:
    graph6: str
    color_count: int
    node_count: int
    trace_sha256: str
    claim_sha256: str
    certificate_sha256: str


def check_uncolorability_trace(
    certificate_path: str | os.PathLike[str],
    *,
    expected_graph: Graph | None = None,
    expected_k: int | None = None,
) -> TraceCheck:
    """Replay a complete proof or raise ``TraceVerificationError``.

    ``expected_graph`` and ``expected_k`` let a caller bind the certificate to
    an externally supplied claim rather than trusting only its header.
    """

    if expected_graph is not None and not isinstance(expected_graph, Graph):
        raise TypeError("expected_graph must be a verifier_b.graph.Graph")
    if expected_k is not None:
        if isinstance(expected_k, bool) or not isinstance(expected_k, int):
            raise TypeError("expected_k must be an integer")
        if expected_k < 0:
            raise ValueError("expected_k must be nonnegative")

    try:
        certificate = open(Path(certificate_path), "rb")
    except OSError as error:
        raise TraceVerificationError(str(error)) from error

    with certificate:
        reader = _LineReader(certificate)
        header = reader.read_object("header")
        _require_exact_keys(header, _HEADER_KEYS, "header")
        if header["type"] != "header":
            raise TraceVerificationError("first record is not a header")
        if header["format"] != FORMAT_NAME:
            raise TraceVerificationError("unsupported trace format")
        if header["vertex_order"] != VERTEX_ORDER:
            raise TraceVerificationError("unsupported vertex order")

        graph6 = header["graph6"]
        if not isinstance(graph6, str):
            raise TraceVerificationError("header graph6 must be a string")
        try:
            graph = Graph.from_graph6(graph6)
        except (TypeError, ValueError) as error:
            raise TraceVerificationError(f"invalid header graph6: {error}") from error
        if graph.to_graph6() != graph6:
            raise TraceVerificationError("header graph6 is not canonical")

        color_count = header["k"]
        if isinstance(color_count, bool) or not isinstance(color_count, int):
            raise TraceVerificationError("header k must be an integer")
        if color_count < 0:
            raise TraceVerificationError("header k must be nonnegative")
        if graph.order == 0 or color_count >= graph.order:
            raise TraceVerificationError(
                "the claimed lower bound is false: an order-n graph is "
                "n-colorable, and the empty graph is 0-colorable"
            )

        graph_digest = _graph6_sha256(graph6)
        claim_digest = _claim_sha256(graph6, color_count)
        if header["graph6_sha256"] != graph_digest:
            raise TraceVerificationError("graph6 hash mismatch")
        if header["claim_sha256"] != claim_digest:
            raise TraceVerificationError("graph6/k claim hash mismatch")
        if expected_graph is not None and graph != expected_graph:
            raise TraceVerificationError("certificate graph differs from expected graph")
        if expected_k is not None and color_count != expected_k:
            raise TraceVerificationError("certificate k differs from expected k")

        complement = graph.complement()
        assignment: list[int | None] = [None] * graph.order
        trace_hasher = sha256()
        node_count = 0

        def replay(vertex: int) -> None:
            nonlocal node_count
            if vertex == graph.order:
                raise TraceVerificationError(
                    "a trace branch reaches a complete proper coloring"
                )

            node = reader.read_object(f"node at depth {vertex}")
            _require_exact_keys(node, _NODE_KEYS, f"node at depth {vertex}")
            if node["type"] != "node":
                raise TraceVerificationError(
                    f"expected node at depth {vertex}, got {node['type']!r}"
                )
            recorded_vertex = node["vertex"]
            if (
                isinstance(recorded_vertex, bool)
                or not isinstance(recorded_vertex, int)
                or recorded_vertex != vertex
            ):
                raise TraceVerificationError(
                    f"wrong vertex at depth {vertex}: {recorded_vertex!r}"
                )

            expected_legal: list[int] = []
            for color in range(color_count):
                is_legal = True
                for neighbor in complement.adjacency[vertex]:
                    assigned_color = assignment[neighbor]
                    if assigned_color is not None and assigned_color == color:
                        is_legal = False
                        break
                if is_legal:
                    expected_legal.append(color)

            recorded_legal = node["legal_colors"]
            if not isinstance(recorded_legal, list) or any(
                isinstance(color, bool) or not isinstance(color, int)
                for color in recorded_legal
            ):
                raise TraceVerificationError(
                    f"legal_colors at depth {vertex} must be a list of integers"
                )
            if recorded_legal != expected_legal:
                raise TraceVerificationError(
                    f"legal colors at depth {vertex} are {expected_legal}, "
                    f"not {recorded_legal!r}"
                )

            encoded_node = _canonical_json_line(node)
            trace_hasher.update(encoded_node)
            node_count += 1

            for color in expected_legal:
                assignment[vertex] = color
                replay(vertex + 1)
                assignment[vertex] = None

        replay(0)

        footer = reader.read_object("footer")
        _require_exact_keys(footer, _FOOTER_KEYS, "footer")
        if footer["type"] != "footer":
            raise TraceVerificationError("expected footer after complete tree")
        recorded_count = footer["node_count"]
        if (
            isinstance(recorded_count, bool)
            or not isinstance(recorded_count, int)
            or recorded_count != node_count
        ):
            raise TraceVerificationError(
                f"footer node count is {recorded_count!r}, expected {node_count}"
            )
        trace_digest = trace_hasher.hexdigest()
        if footer["trace_sha256"] != trace_digest:
            raise TraceVerificationError("trace hash mismatch")
        if reader.read_optional_line() is not None:
            raise TraceVerificationError("extra data follows the footer")

        return TraceCheck(
            graph6=graph6,
            color_count=color_count,
            node_count=node_count,
            trace_sha256=trace_digest,
            claim_sha256=claim_digest,
            certificate_sha256=reader.file_hasher.hexdigest(),
        )


def verify_uncolorability_trace(
    certificate_path: str | os.PathLike[str],
    *,
    expected_graph: Graph | None = None,
    expected_k: int | None = None,
) -> bool:
    """Fail-closed Boolean wrapper around ``check_uncolorability_trace``."""

    try:
        check_uncolorability_trace(
            certificate_path,
            expected_graph=expected_graph,
            expected_k=expected_k,
        )
    except (
        TraceVerificationError,
        OSError,
        UnicodeError,
        RecursionError,
        TypeError,
        ValueError,
        OverflowError,
    ):
        return False
    return True


class _LineReader:
    def __init__(self, source: BinaryIO):
        self.source = source
        self.line_number = 0
        self.file_hasher = sha256()

    def read_optional_line(self) -> bytes | None:
        encoded = self.source.readline()
        if encoded == b"":
            return None
        self.line_number += 1
        self.file_hasher.update(encoded)
        return encoded

    def read_object(self, description: str) -> dict[str, Any]:
        encoded = self.read_optional_line()
        if encoded is None:
            raise TraceVerificationError(f"truncated trace: missing {description}")
        if not encoded.endswith(b"\n"):
            raise TraceVerificationError(
                f"line {self.line_number} is missing its terminating newline"
            )
        try:
            text = encoded.decode("ascii")
        except UnicodeDecodeError as error:
            raise TraceVerificationError(
                f"line {self.line_number} is not ASCII"
            ) from error
        try:
            value = json.loads(text, object_pairs_hook=_unique_object)
        except (ValueError, TraceVerificationError) as error:
            raise TraceVerificationError(
                f"invalid JSON on line {self.line_number}: {error}"
            ) from error
        if not isinstance(value, dict):
            raise TraceVerificationError(
                f"line {self.line_number} ({description}) is not an object"
            )
        return value


def _unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise TraceVerificationError(f"duplicate JSON key {key!r}")
        result[key] = value
    return result


def _require_exact_keys(
    value: dict[str, Any], expected: set[str], description: str
) -> None:
    actual = set(value)
    if actual != expected:
        missing = sorted(expected - actual)
        extra = sorted(actual - expected)
        raise TraceVerificationError(
            f"{description} schema mismatch: missing={missing}, extra={extra}"
        )


def _canonical_json_line(value: object) -> bytes:
    return (
        json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
        + "\n"
    ).encode("ascii")


def _graph6_sha256(graph6: str) -> str:
    return sha256(b"graph6\x00" + graph6.encode("ascii")).hexdigest()


def _claim_sha256(graph6: str, color_count: int) -> str:
    material = (
        b"gamma-theta-complement-coloring-unsat-v1\x00"
        + graph6.encode("ascii")
        + b"\x00"
        + str(color_count).encode("ascii")
    )
    return sha256(material).hexdigest()
