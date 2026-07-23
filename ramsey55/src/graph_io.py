#!/usr/bin/env python3
"""Dependency-free graph6 I/O and deterministic graph artifact helpers."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


def decode_graph6(text: str) -> list[int]:
    """Return adjacency bitsets for a graph6 string with at most 62 vertices."""
    line = text.strip()
    if line.startswith(">>graph6<<"):
        line = line[len(">>graph6<<") :]
    if not line:
        raise ValueError("empty graph6 input")
    n = ord(line[0]) - 63
    if not 0 <= n <= 62:
        raise ValueError("only short graph6 (n <= 62) is supported")
    payload = [ord(ch) - 63 for ch in line[1:]]
    if any(not 0 <= value < 64 for value in payload):
        raise ValueError("invalid graph6 payload")
    needed = n * (n - 1) // 2
    if len(payload) * 6 < needed:
        raise ValueError("truncated graph6 payload")

    adjacency = [0] * n
    bit_index = 0
    for j in range(1, n):
        for i in range(j):
            value = payload[bit_index // 6]
            bit = (value >> (5 - bit_index % 6)) & 1
            bit_index += 1
            if bit:
                adjacency[i] |= 1 << j
                adjacency[j] |= 1 << i
    return adjacency


def encode_graph6(adjacency: list[int]) -> str:
    """Encode adjacency bitsets as short graph6."""
    n = len(adjacency)
    if not 0 <= n <= 62:
        raise ValueError("only short graph6 (n <= 62) is supported")
    bits: list[int] = []
    for j in range(1, n):
        for i in range(j):
            bits.append((adjacency[i] >> j) & 1)
    while len(bits) % 6:
        bits.append(0)
    payload = []
    for start in range(0, len(bits), 6):
        value = 0
        for bit in bits[start : start + 6]:
            value = (value << 1) | bit
        payload.append(chr(value + 63))
    return chr(n + 63) + "".join(payload)


def validate_simple(adjacency: list[int]) -> None:
    n = len(adjacency)
    allowed = (1 << n) - 1
    for vertex, neighbors in enumerate(adjacency):
        if neighbors & ~allowed:
            raise ValueError(f"vertex {vertex} has an out-of-range neighbor")
        if neighbors & (1 << vertex):
            raise ValueError(f"loop at vertex {vertex}")
        for other in range(n):
            if ((neighbors >> other) & 1) != ((adjacency[other] >> vertex) & 1):
                raise ValueError(f"asymmetric pair {vertex},{other}")


def complement(adjacency: list[int]) -> list[int]:
    validate_simple(adjacency)
    n = len(adjacency)
    mask = (1 << n) - 1
    return [mask & ~(neighbors | (1 << vertex)) for vertex, neighbors in enumerate(adjacency)]


def edge_list(adjacency: list[int]) -> list[list[int]]:
    validate_simple(adjacency)
    return [
        [i, j]
        for i in range(len(adjacency))
        for j in range(i + 1, len(adjacency))
        if (adjacency[i] >> j) & 1
    ]


def artifact_dict(adjacency: list[int], provenance: dict | None = None) -> dict:
    """Build the canonical, representation-rich graph dictionary."""
    validate_simple(adjacency)
    n = len(adjacency)
    edges = edge_list(adjacency)
    adjacency_list = [
        [other for other in range(n) if (adjacency[vertex] >> other) & 1]
        for vertex in range(n)
    ]
    degrees = [len(row) for row in adjacency_list]
    matrix = [
        "".join("1" if (adjacency[i] >> j) & 1 else "0" for j in range(n))
        for i in range(n)
    ]
    result = {
        "schema": "ramsey55.graph.v1",
        "n": n,
        "graph6": encode_graph6(adjacency),
        "edge_count": len(edges),
        "degree_sequence": sorted(degrees),
        "adjacency_list": adjacency_list,
        "edge_list": edges,
        "adjacency_matrix_rows": matrix,
    }
    if provenance is not None:
        result["provenance"] = provenance
    return result


def write_canonical_artifact(
    adjacency: list[int], output: Path, provenance: dict | None = None
) -> str:
    output.parent.mkdir(parents=True, exist_ok=True)
    payload = (
        json.dumps(
            artifact_dict(adjacency, provenance),
            sort_keys=True,
            indent=2,
            separators=(",", ": "),
        )
        + "\n"
    ).encode("utf-8")
    output.write_bytes(payload)
    return hashlib.sha256(payload).hexdigest()


def read_graph(path: Path, line_number: int = 1) -> list[int]:
    """Read graph6 or a canonical JSON artifact."""
    if path.suffix.lower() == ".json":
        data = json.loads(path.read_text(encoding="utf-8"))
        if "graph6" not in data:
            raise ValueError("JSON artifact has no graph6 field")
        return decode_graph6(data["graph6"])
    lines = [
        line.strip()
        for line in path.read_text(encoding="ascii").splitlines()
        if line.strip() and not line.startswith("#")
    ]
    if not 1 <= line_number <= len(lines):
        raise ValueError(f"line number {line_number} outside 1..{len(lines)}")
    return decode_graph6(lines[line_number - 1])
