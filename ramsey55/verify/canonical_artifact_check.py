#!/usr/bin/env python3
"""Independently validate every representation in a canonical graph artifact.

This module intentionally does not import ``graph_io`` or any search module.
The graph6 codec and all derived graph representations are implemented here so
that this checker does not share the artifact producer's implementation path.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any


VALIDATOR = "ramsey55.independent_canonical_artifact_validator.v1"
REQUIRED_FIELDS = {
    "schema",
    "n",
    "graph6",
    "edge_count",
    "degree_sequence",
    "adjacency_list",
    "edge_list",
    "adjacency_matrix_rows",
}
OPTIONAL_FIELDS = {"provenance"}


class DuplicateKeyError(ValueError):
    """Raised when a JSON object contains a repeated key."""


class Audit:
    """Collect named checks and useful failure messages without stopping early."""

    def __init__(self) -> None:
        self.checks: dict[str, bool] = {}
        self.errors: list[dict[str, str]] = []

    def check(self, name: str, condition: bool, message: str) -> bool:
        passed = bool(condition)
        self.checks[name] = passed
        if not passed:
            self.errors.append({"check": name, "message": message})
        return passed


def _reject_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise DuplicateKeyError(f"duplicate JSON object key: {key!r}")
        result[key] = value
    return result


def _reject_nonfinite_number(token: str) -> None:
    raise ValueError(f"non-finite JSON number is not permitted: {token}")


def canonical_json_bytes(document: Any) -> bytes:
    """Serialize exactly as the project's canonical artifact writer does."""
    return (
        json.dumps(
            document,
            sort_keys=True,
            indent=2,
            separators=(",", ": "),
            ensure_ascii=True,
            allow_nan=False,
        )
        + "\n"
    ).encode("utf-8")


def decode_short_graph6(text: str) -> tuple[int, list[int]]:
    """Decode canonical short graph6 (orders 0 through 62), independently."""
    if not isinstance(text, str):
        raise ValueError("graph6 must be a JSON string")
    if not text:
        raise ValueError("graph6 string is empty")
    if text.startswith(">>graph6<<"):
        raise ValueError("canonical graph6 must not contain a header")
    try:
        encoded = text.encode("ascii")
    except UnicodeEncodeError as exc:
        raise ValueError("graph6 contains a non-ASCII character") from exc

    order_code = encoded[0]
    if not 63 <= order_code <= 125:
        raise ValueError("only canonical short graph6 orders 0..62 are supported")
    n = order_code - 63
    bit_count = n * (n - 1) // 2
    payload_length = (bit_count + 5) // 6
    if len(encoded) != payload_length + 1:
        raise ValueError(
            f"graph6 length is {len(encoded)}, expected {payload_length + 1}"
        )
    payload = encoded[1:]
    if any(not 63 <= code <= 126 for code in payload):
        raise ValueError("graph6 payload character lies outside ASCII 63..126")

    unused_bits = payload_length * 6 - bit_count
    if unused_bits and payload:
        low_mask = (1 << unused_bits) - 1
        if (payload[-1] - 63) & low_mask:
            raise ValueError("graph6 has nonzero padding bits")

    adjacency = [0] * n
    bit_index = 0
    for right in range(1, n):
        for left in range(right):
            value = payload[bit_index // 6] - 63
            present = (value >> (5 - bit_index % 6)) & 1
            bit_index += 1
            if present:
                adjacency[left] |= 1 << right
                adjacency[right] |= 1 << left
    return n, adjacency


def encode_short_graph6(adjacency: list[int]) -> str:
    """Encode a simple adjacency-bitset graph as canonical short graph6."""
    n = len(adjacency)
    if not 0 <= n <= 62:
        raise ValueError("only canonical short graph6 orders 0..62 are supported")
    bits = [
        (adjacency[left] >> right) & 1
        for right in range(1, n)
        for left in range(right)
    ]
    bits.extend([0] * ((-len(bits)) % 6))
    payload: list[str] = []
    for offset in range(0, len(bits), 6):
        value = 0
        for bit in bits[offset : offset + 6]:
            value = (value << 1) | bit
        payload.append(chr(value + 63))
    return chr(n + 63) + "".join(payload)


def _is_plain_int(value: Any) -> bool:
    return type(value) is int


def _derived_representations(adjacency: list[int]) -> dict[str, Any]:
    n = len(adjacency)
    adjacency_list = [
        [other for other in range(n) if (adjacency[vertex] >> other) & 1]
        for vertex in range(n)
    ]
    edge_list = [
        [left, right]
        for left in range(n)
        for right in range(left + 1, n)
        if (adjacency[left] >> right) & 1
    ]
    matrix = [
        "".join(
            "1" if (adjacency[row] >> column) & 1 else "0"
            for column in range(n)
        )
        for row in range(n)
    ]
    return {
        "adjacency_list": adjacency_list,
        "edge_list": edge_list,
        "adjacency_matrix_rows": matrix,
        "edge_count": len(edge_list),
        "degree_sequence": sorted(len(row) for row in adjacency_list),
    }


def validate_bytes(raw: bytes, artifact_name: str = "<memory>") -> dict[str, Any]:
    """Return a machine-readable validation report for one artifact."""
    audit = Audit()
    artifact_sha256 = hashlib.sha256(raw).hexdigest()
    try:
        text = raw.decode("utf-8")
        audit.check("utf8", True, "")
    except UnicodeDecodeError as exc:
        audit.check("utf8", False, f"invalid UTF-8: {exc}")
        return _report(artifact_name, artifact_sha256, None, audit)

    try:
        document = json.loads(
            text,
            object_pairs_hook=_reject_duplicate_keys,
            parse_constant=_reject_nonfinite_number,
        )
        audit.check("json_parse_and_unique_keys", True, "")
    except (json.JSONDecodeError, DuplicateKeyError, ValueError) as exc:
        audit.check("json_parse_and_unique_keys", False, str(exc))
        return _report(artifact_name, artifact_sha256, None, audit)

    try:
        expected_serialization = canonical_json_bytes(document)
        serialization_matches = raw == expected_serialization
    except (TypeError, ValueError) as exc:
        serialization_matches = False
        serialization_message = f"document cannot be canonically serialized: {exc}"
    else:
        serialization_message = (
            "JSON bytes are not sorted-key, two-space-indented UTF-8 with one "
            "terminal newline"
        )
    audit.check(
        "canonical_json_serialization",
        serialization_matches,
        serialization_message,
    )

    if not audit.check(
        "root_object", isinstance(document, dict), "JSON root must be an object"
    ):
        return _report(artifact_name, artifact_sha256, None, audit)

    actual_fields = set(document)
    audit.check(
        "required_fields",
        REQUIRED_FIELDS <= actual_fields,
        f"missing required fields: {sorted(REQUIRED_FIELDS - actual_fields)}",
    )
    audit.check(
        "schema_fields",
        actual_fields <= REQUIRED_FIELDS | OPTIONAL_FIELDS,
        f"unknown fields: {sorted(actual_fields - REQUIRED_FIELDS - OPTIONAL_FIELDS)}",
    )
    audit.check(
        "schema_identifier",
        document.get("schema") == "ramsey55.graph.v1",
        "schema must equal 'ramsey55.graph.v1'",
    )
    if "provenance" in document:
        audit.check(
            "provenance_object",
            isinstance(document["provenance"], dict),
            "provenance, when present, must be an object",
        )

    declared_n = document.get("n")
    n_well_formed = _is_plain_int(declared_n) and 0 <= declared_n <= 62
    audit.check(
        "n_well_formed",
        n_well_formed,
        "n must be an integer in the short-graph6 range 0..62",
    )

    graph6_value = document.get("graph6")
    try:
        decoded_n, adjacency = decode_short_graph6(graph6_value)
        graph6_ok = True
        graph6_message = ""
    except (TypeError, ValueError) as exc:
        decoded_n, adjacency = None, None
        graph6_ok = False
        graph6_message = str(exc)
    audit.check("graph6_syntax", graph6_ok, graph6_message)

    if adjacency is None:
        return _report(artifact_name, artifact_sha256, document, audit)

    graph6_round_trip = encode_short_graph6(adjacency) == graph6_value
    audit.check(
        "graph6_canonical_round_trip",
        graph6_round_trip,
        "independent graph6 decode/encode did not reproduce the field",
    )
    audit.check(
        "n_matches_graph6",
        n_well_formed and declared_n == decoded_n,
        f"declared n={declared_n!r}, graph6 encodes n={decoded_n}",
    )

    n = decoded_n
    allowed_mask = (1 << n) - 1
    simple = all(
        (row & ~allowed_mask) == 0 and (row & (1 << vertex)) == 0
        for vertex, row in enumerate(adjacency)
    )
    symmetric = all(
        ((adjacency[left] >> right) & 1)
        == ((adjacency[right] >> left) & 1)
        for left in range(n)
        for right in range(n)
    )
    audit.check(
        "graph6_decodes_simple_loopless",
        simple,
        "decoded graph has a loop or out-of-range neighbor",
    )
    audit.check(
        "graph6_decodes_symmetric",
        symmetric,
        "decoded graph is not symmetric",
    )
    expected = _derived_representations(adjacency)

    _check_adjacency_list(audit, document.get("adjacency_list"), expected, n)
    _check_edge_list(audit, document.get("edge_list"), expected, n)
    _check_matrix(
        audit, document.get("adjacency_matrix_rows"), expected, n
    )

    edge_count = document.get("edge_count")
    audit.check(
        "edge_count_well_formed",
        _is_plain_int(edge_count) and edge_count >= 0,
        "edge_count must be a nonnegative integer",
    )
    audit.check(
        "edge_count_matches_graph6",
        edge_count == expected["edge_count"],
        (
            f"edge_count={edge_count!r}, independently derived "
            f"{expected['edge_count']}"
        ),
    )

    degree_sequence = document.get("degree_sequence")
    degree_well_formed = (
        isinstance(degree_sequence, list)
        and len(degree_sequence) == n
        and all(_is_plain_int(value) and 0 <= value < n for value in degree_sequence)
    )
    audit.check(
        "degree_sequence_well_formed",
        degree_well_formed,
        f"degree_sequence must contain exactly {n} integer degrees in 0..{n - 1}",
    )
    audit.check(
        "degree_sequence_sorted",
        degree_well_formed
        and all(
            degree_sequence[index] <= degree_sequence[index + 1]
            for index in range(n - 1)
        ),
        "degree_sequence is not nondecreasing",
    )
    audit.check(
        "degree_sequence_matches_graph6",
        degree_sequence == expected["degree_sequence"],
        "degree_sequence differs from independently derived sorted degrees",
    )

    return _report(artifact_name, artifact_sha256, document, audit)


def _check_adjacency_list(
    audit: Audit, value: Any, expected: dict[str, Any], n: int
) -> None:
    well_formed = isinstance(value, list) and len(value) == n
    if well_formed:
        for vertex, row in enumerate(value):
            if not isinstance(row, list):
                well_formed = False
                break
            if any(
                not _is_plain_int(other)
                or not 0 <= other < n
                or other == vertex
                for other in row
            ):
                well_formed = False
                break
            if any(row[index] >= row[index + 1] for index in range(len(row) - 1)):
                well_formed = False
                break
    audit.check(
        "adjacency_list_well_formed",
        well_formed,
        (
            "adjacency_list must have n rows of strictly increasing, unique, "
            "in-range integer neighbors with no loops"
        ),
    )
    symmetric = well_formed and all(
        vertex in value[other]
        for vertex, row in enumerate(value)
        for other in row
    )
    audit.check(
        "adjacency_list_symmetric",
        symmetric,
        "adjacency_list does not represent an undirected symmetric graph",
    )
    audit.check(
        "adjacency_list_matches_graph6",
        value == expected["adjacency_list"],
        "adjacency_list differs from the independently decoded graph6 graph",
    )


def _check_edge_list(
    audit: Audit, value: Any, expected: dict[str, Any], n: int
) -> None:
    well_formed = isinstance(value, list)
    if well_formed:
        previous: tuple[int, int] | None = None
        for edge in value:
            if (
                not isinstance(edge, list)
                or len(edge) != 2
                or not all(_is_plain_int(endpoint) for endpoint in edge)
                or not 0 <= edge[0] < edge[1] < n
            ):
                well_formed = False
                break
            current = (edge[0], edge[1])
            if previous is not None and previous >= current:
                well_formed = False
                break
            previous = current
    audit.check(
        "edge_list_well_formed",
        well_formed,
        (
            "edge_list must be a strictly lexicographically increasing list of "
            "[u,v] pairs satisfying 0 <= u < v < n"
        ),
    )
    audit.check(
        "edge_list_matches_graph6",
        value == expected["edge_list"],
        "edge_list differs from the independently decoded graph6 graph",
    )


def _check_matrix(
    audit: Audit, value: Any, expected: dict[str, Any], n: int
) -> None:
    well_formed = (
        isinstance(value, list)
        and len(value) == n
        and all(
            isinstance(row, str)
            and len(row) == n
            and set(row) <= {"0", "1"}
            for row in value
        )
    )
    audit.check(
        "adjacency_matrix_well_formed",
        well_formed,
        f"adjacency_matrix_rows must contain {n} binary strings of length {n}",
    )
    loopless = well_formed and all(value[index][index] == "0" for index in range(n))
    audit.check(
        "adjacency_matrix_loopless",
        loopless,
        "adjacency matrix contains a loop on its diagonal",
    )
    symmetric = well_formed and all(
        value[left][right] == value[right][left]
        for left in range(n)
        for right in range(n)
    )
    audit.check(
        "adjacency_matrix_symmetric",
        symmetric,
        "adjacency matrix is not symmetric",
    )
    audit.check(
        "adjacency_matrix_matches_graph6",
        value == expected["adjacency_matrix_rows"],
        "adjacency matrix differs from the independently decoded graph6 graph",
    )


def _report(
    artifact_name: str,
    artifact_sha256: str,
    document: Any,
    audit: Audit,
) -> dict[str, Any]:
    graph6 = document.get("graph6") if isinstance(document, dict) else None
    report: dict[str, Any] = {
        "artifact": artifact_name,
        "artifact_sha256": artifact_sha256,
        "checks": audit.checks,
        "errors": audit.errors,
        "independence": {
            "graph6_codec": "implemented_in_validator",
            "imports_graph_io": False,
            "imports_search_code": False,
        },
        "status": "PASS" if not audit.errors else "FAIL",
        "validator": VALIDATOR,
    }
    if isinstance(document, dict):
        report["declared_n"] = document.get("n")
        report["declared_edge_count"] = document.get("edge_count")
    if isinstance(graph6, str):
        report["graph6_sha256"] = hashlib.sha256(
            graph6.encode("utf-8")
        ).hexdigest()
    return report


def _write_new_report(path: Path, report: dict[str, Any]) -> None:
    """Create a report without allowing accidental replacement of evidence."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("xb") as handle:
        handle.write(canonical_json_bytes(report))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("artifact", type=Path)
    parser.add_argument(
        "--output",
        type=Path,
        help="create this machine-readable report; refuses to overwrite",
    )
    args = parser.parse_args()

    report = validate_bytes(args.artifact.read_bytes(), str(args.artifact))
    rendered = canonical_json_bytes(report)
    if args.output is not None:
        try:
            _write_new_report(args.output, report)
        except FileExistsError:
            print(f"refusing to overwrite existing report: {args.output}", file=sys.stderr)
            return 2
    sys.stdout.buffer.write(rendered)
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
