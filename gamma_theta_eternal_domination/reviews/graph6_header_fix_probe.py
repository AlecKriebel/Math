#!/usr/bin/env python3
"""Focused review of canonical graph6 order-header validation in A and B."""

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from verifier_a.core import BitGraph  # noqa: E402
from verifier_b import Graph  # noqa: E402


def digits(value: int, width: int) -> str:
    encoded = ["?"] * width
    for position in range(width - 1, -1, -1):
        value, digit = divmod(value, 64)
        encoded[position] = chr(digit + 63)
    assert value == 0
    return "".join(encoded)


def medium_header(order: int) -> str:
    return "~" + digits(order, 3)


def long_header(order: int) -> str:
    return "~~" + digits(order, 6)


PARSERS = (("A", BitGraph.from_graph6), ("B", Graph.from_graph6))


def require_rejection(record: str) -> int:
    checked = 0
    for name, parser in PARSERS:
        try:
            parser(record)
        except ValueError:
            checked += 1
            continue
        raise AssertionError(f"{name} accepted noncanonical header {record!r}")
    return checked


def require_header_recognized(record: str) -> int:
    """A canonical huge-order header may lack its payload, but is canonical."""

    checked = 0
    for name, parser in PARSERS:
        try:
            parser(record)
        except ValueError as error:
            message = str(error)
            if "noncanonical" in message or "order" in message and "truncated" in message:
                raise AssertionError(
                    f"{name} rejected canonical header {record!r}: {message}"
                )
            if "length" not in message:
                raise AssertionError(
                    f"{name} failed for an unexpected reason: {message}"
                )
            checked += 1
            continue
        raise AssertionError("header without its enormous payload was accepted")
    return checked


def main() -> None:
    rejected = 0
    noncanonical_records = (
        "~???",  # reported 18-bit order-zero reproducer
        "~~??????",  # reported 36-bit order-zero reproducer
        medium_header(1),
        medium_header(62),
        long_header(1),
        long_header(62),
        long_header(63),
        long_header(258_047),
    )
    for record in noncanonical_records:
        rejected += require_rejection(record)

    valid_boundary_records = (
        BitGraph.edgeless(0).to_graph6(),
        BitGraph.edgeless(1).to_graph6(),
        BitGraph.edgeless(62).to_graph6(),
        BitGraph.edgeless(63).to_graph6(),
    )
    accepted = 0
    for record in valid_boundary_records:
        graph_a = BitGraph.from_graph6(record)
        graph_b = Graph.from_graph6(record)
        assert graph_a.n == graph_b.order
        assert graph_a.size == graph_b.size == 0
        assert graph_a.to_graph6() == graph_b.to_graph6() == record
        assert BitGraph.from_graph6((">>graph6<<" + record).encode("ascii")) == graph_a
        assert Graph.from_graph6((">>graph6<<" + record).encode("ascii")) == graph_b
        accepted += 4

    canonical_header_only_checks = 0
    canonical_header_only_checks += require_header_recognized(
        medium_header(258_047)
    )
    canonical_header_only_checks += require_header_recognized(
        long_header(258_048)
    )

    print(
        json.dumps(
            {
                "outcome": "canonical order-header fix passes in both parsers",
                "reported_reproducers_rejected_by_both": [
                    "~???",
                    "~~??????",
                ],
                "noncanonical_records": len(noncanonical_records),
                "noncanonical_parser_rejections": rejected,
                "valid_boundary_forms_accepted": accepted,
                "canonical_large_headers_recognized_before_payload_check": (
                    canonical_header_only_checks
                ),
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
