"""Generate exhaustive certificates that ``theta(G) > k``.

The certificate is a full, unsymmetrized backtracking tree for coloring the
complement of ``G`` with colors ``0, ..., k - 1``.  This module deliberately
does not import verifier A, the search stack, or verifier B's coloring solver.
The checker is implemented separately in ``coloring_trace_checker.py``.
"""

from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
import json
import os
from pathlib import Path
import tempfile
from typing import BinaryIO

from .graph import Graph


FORMAT_NAME = "gamma-theta-complement-coloring-unsat-v1"
VERTEX_ORDER = "least-uncolored"


class ColorableGraphError(ValueError):
    """Raised when the requested non-colorability claim is false."""

    def __init__(self, graph6: str, color_count: int, coloring: tuple[int, ...]):
        super().__init__(
            f"complement of {graph6!r} is colorable with the requested "
            f"number of colors: {coloring}"
        )
        self.graph6 = graph6
        self.color_count = color_count
        self.coloring = coloring


@dataclass(frozen=True, slots=True)
class TraceGenerationSummary:
    graph6: str
    color_count: int
    node_count: int
    trace_sha256: str
    claim_sha256: str
    certificate_sha256: str
    output_path: Path


def graph6_sha256(graph6: str) -> str:
    """Hash one canonical graph6 record with a domain separator."""

    return sha256(b"graph6\x00" + graph6.encode("ascii")).hexdigest()


def claim_sha256(graph6: str, color_count: int) -> str:
    """Bind the graph6 record and requested color count into one digest."""

    material = (
        b"gamma-theta-complement-coloring-unsat-v1\x00"
        + graph6.encode("ascii")
        + b"\x00"
        + str(color_count).encode("ascii")
    )
    return sha256(material).hexdigest()


def write_uncolorability_trace(
    graph: Graph,
    color_count: int,
    output_path: str | os.PathLike[str],
    *,
    overwrite: bool = False,
) -> TraceGenerationSummary:
    """Write an atomic proof that ``complement(graph)`` is not k-colorable.

    A partial file is deleted if a coloring is found or generation otherwise
    fails.  Existing output is preserved unless ``overwrite=True``.
    """

    if not isinstance(graph, Graph):
        raise TypeError("graph must be a verifier_b.graph.Graph")
    if isinstance(color_count, bool) or not isinstance(color_count, int):
        raise TypeError("color_count must be an integer")
    if color_count < 0:
        raise ValueError("color_count must be nonnegative")

    graph6 = graph.to_graph6()
    if graph.order == 0:
        raise ColorableGraphError(graph6, color_count, ())
    if color_count >= graph.order:
        raise ColorableGraphError(
            graph6, color_count, tuple(range(graph.order))
        )

    target = Path(output_path)
    if target.exists() and not overwrite:
        raise FileExistsError(f"refusing to overwrite {target}")
    if not target.parent.is_dir():
        raise FileNotFoundError(f"output directory does not exist: {target.parent}")

    graph_digest = graph6_sha256(graph6)
    claim_digest = claim_sha256(graph6, color_count)
    header = {
        "claim_sha256": claim_digest,
        "format": FORMAT_NAME,
        "graph6": graph6,
        "graph6_sha256": graph_digest,
        "k": color_count,
        "type": "header",
        "vertex_order": VERTEX_ORDER,
    }

    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{target.name}.",
        suffix=".partial",
        dir=target.parent,
    )
    temporary_path = Path(temporary_name)
    node_hasher = sha256()
    file_hasher = sha256()
    node_count = 0
    complement = graph.complement()
    assignment = [-1] * graph.order

    try:
        with os.fdopen(descriptor, "wb") as output:
            _write_json_line(output, header, file_hasher)

            def visit(vertex: int) -> tuple[int, ...] | None:
                nonlocal node_count
                if vertex == graph.order:
                    return tuple(assignment)

                legal_colors: list[int] = []
                for color in range(color_count):
                    conflict = False
                    for neighbor in complement.adjacency[vertex]:
                        if neighbor < vertex and assignment[neighbor] == color:
                            conflict = True
                            break
                    if not conflict:
                        legal_colors.append(color)

                node = {
                    "legal_colors": legal_colors,
                    "type": "node",
                    "vertex": vertex,
                }
                encoded_node = _canonical_json_line(node)
                output.write(encoded_node)
                node_hasher.update(encoded_node)
                file_hasher.update(encoded_node)
                node_count += 1

                for color in legal_colors:
                    assignment[vertex] = color
                    coloring = visit(vertex + 1)
                    if coloring is not None:
                        return coloring
                assignment[vertex] = -1
                return None

            coloring = visit(0)
            if coloring is not None:
                raise ColorableGraphError(graph6, color_count, coloring)

            trace_digest = node_hasher.hexdigest()
            footer = {
                "node_count": node_count,
                "trace_sha256": trace_digest,
                "type": "footer",
            }
            _write_json_line(output, footer, file_hasher)
            output.flush()
            os.fsync(output.fileno())

        if target.exists() and not overwrite:
            raise FileExistsError(f"refusing to overwrite {target}")
        os.replace(temporary_path, target)
        return TraceGenerationSummary(
            graph6=graph6,
            color_count=color_count,
            node_count=node_count,
            trace_sha256=trace_digest,
            claim_sha256=claim_digest,
            certificate_sha256=file_hasher.hexdigest(),
            output_path=target,
        )
    except BaseException:
        try:
            temporary_path.unlink()
        except FileNotFoundError:
            pass
        raise


def _canonical_json_line(value: object) -> bytes:
    return (
        json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
        + "\n"
    ).encode("ascii")


def _write_json_line(
    output: BinaryIO, value: object, file_hasher: "sha256"
) -> None:
    encoded = _canonical_json_line(value)
    output.write(encoded)
    file_hasher.update(encoded)
