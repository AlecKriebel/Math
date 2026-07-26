"""Exact bounded edge-toggle probe around the deepest known local survivor.

This module studies one fixed labeled graph,

    ``Kun_w{vRrblV``,

and exactly the graphs obtained by toggling zero, one, or two of its 66
unordered vertex pairs.  It is deliberately a bounded robustness experiment,
not an exhaustive order-12 search and not a certificate of nonexistence.

The raw labeled origins are canonicalized by the pinned nauty 2.9.3
``labelg`` executable.  Every resulting canonical class is evaluated by both
campaign evaluator stacks for gamma, independent domination, alpha,
one-guard eternal domination, and theta.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import platform
import resource
import subprocess
import sys
import tempfile
import time
from collections import Counter
from dataclasses import dataclass
from datetime import datetime, timezone
from itertools import combinations
from pathlib import Path
from typing import Iterable, Mapping, Sequence

from search.extension_killtest import (
    EXPECTED_LABELG_SHA256,
    NAUTY_ARCHIVE_SHA256,
    canonicalize_graph6_batch,
    sha256_file,
    verify_pinned_labelg,
)
from verifier_a.core import (
    BitGraph,
    alpha,
    domination_number,
    eternal_fixed_point,
    independent_domination_number,
    theta,
    verify_eternal_result,
)
from verifier_b import (
    Graph,
    clique_cover_number,
    domination_number as domination_number_b,
    find_eternal_family,
    independence_number,
    independent_domination_number as independent_domination_number_b,
    verify_eternal_family,
)


SCHEMA_VERSION = 1
BASE_GRAPH6 = "Kun_w{vRrblV"
BASE_ORDER = 12
BASE_SIZE = 40
MAX_TOGGLE_RADIUS = 2
PAIR_COUNT = math.comb(BASE_ORDER, 2)
RAW_ORIGIN_COUNT = sum(
    math.comb(PAIR_COUNT, radius)
    for radius in range(MAX_TOGGLE_RADIUS + 1)
)
EXPECTED_CANONICAL_CLASS_COUNT = 1_076
CLAIM_CLASSIFICATION = "OBSERVED"

EXPECTED_PROJECTED_HISTOGRAM = {
    (2, 3, 3, 3): 230,
    (2, 3, 3, 4): 53,
    (2, 3, 4, 4): 371,
    (2, 4, 4, 4): 11,
    (3, 3, 4, 4): 354,
    (3, 4, 4, 4): 57,
}
EXPECTED_FULL_HISTOGRAM = {
    (2, 2, 3, 3, 3): 229,
    (2, 2, 3, 3, 4): 52,
    (2, 2, 3, 4, 4): 366,
    (2, 2, 4, 4, 4): 11,
    (2, 3, 3, 3, 3): 1,
    (2, 3, 3, 3, 4): 1,
    (2, 3, 3, 4, 4): 5,
    (3, 3, 3, 4, 4): 354,
    (3, 3, 4, 4, 4): 57,
}

RUNTIME_SOURCE_RELATIVE_PATHS = (
    "src/search/deep_survivor_radius2.py",
    "src/search/extension_killtest.py",
    "src/search/private_obstruction.py",
    "src/verifier_a/core.py",
    "src/verifier_b/__init__.py",
    "src/verifier_b/graph.py",
    "src/verifier_b/invariants.py",
    "src/verifier_b/eternal.py",
)
SUPPORTING_ARTIFACT_RELATIVE_PATHS = (
    "tests/test_deep_survivor_radius2.py",
    "math/deep_survivor_radius2_search_scope.md",
)

HASH_STREAM_FORMATS = {
    "origin_spec": (
        "origin_index<TAB>comma-separated pair indices<TAB>"
        "comma-separated u-v pairs<LF>"
    ),
    "raw_graph6": "origin_index<TAB>raw_graph6<LF>",
    "canonical_origin": "origin_index<TAB>canonical_graph6<LF>",
    "labelg_input": "raw_graph6<LF>, in origin order",
    "labelg_output": "canonical_graph6<LF>, in origin order",
    "canonical_unique": "canonical_graph6<LF>, lexicographic order",
    "canonical_multiplicity": (
        "canonical_graph6<TAB>decimal multiplicity<LF>, lexicographic order"
    ),
    "evaluation": (
        "canonical_graph6<TAB>multiplicity<TAB>gamma<TAB>i<TAB>alpha"
        "<TAB>gamma_infinity<TAB>theta<TAB>compact decisions JSON<LF>, "
        "lexicographic graph6 order"
    ),
}


@dataclass(frozen=True, slots=True)
class Origin:
    index: int
    toggle_indices: tuple[int, ...]
    toggle_edges: tuple[tuple[int, int], ...]
    raw_graph6: str
    canonical_graph6: str | None = None

    def as_json(self) -> dict[str, object]:
        return {
            "index": self.index,
            "toggle_indices": list(self.toggle_indices),
            "toggle_edges": [list(edge) for edge in self.toggle_edges],
            "raw_graph6": self.raw_graph6,
            "canonical_graph6": self.canonical_graph6,
        }


def _sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _sha256_text(text: str) -> str:
    return _sha256_bytes(text.encode("utf-8"))


def _canonical_json(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def _source_set_sha256(
    manifest: Sequence[tuple[str, str]],
) -> str:
    return _sha256_text(
        "".join(f"{relative}\t{digest}\n" for relative, digest in manifest)
    )


def runtime_source_manifest(
    campaign_root: Path | None = None,
) -> tuple[tuple[str, str], ...]:
    root = (
        campaign_root.resolve()
        if campaign_root is not None
        else Path(__file__).resolve().parents[2]
    )
    manifest: list[tuple[str, str]] = []
    for relative in RUNTIME_SOURCE_RELATIVE_PATHS:
        path = root / relative
        if not path.is_file():
            raise ValueError(f"runtime dependency is missing: {path}")
        manifest.append((relative, sha256_file(path)))
    return tuple(manifest)


def supporting_artifact_manifest(
    campaign_root: Path | None = None,
) -> tuple[tuple[str, str], ...]:
    root = (
        campaign_root.resolve()
        if campaign_root is not None
        else Path(__file__).resolve().parents[2]
    )
    manifest: list[tuple[str, str]] = []
    for relative in SUPPORTING_ARTIFACT_RELATIVE_PATHS:
        path = root / relative
        if not path.is_file():
            raise ValueError(f"supporting artifact is missing: {path}")
        manifest.append((relative, sha256_file(path)))
    return tuple(manifest)


def validate_current_manifest(
    manifest: Sequence[Sequence[str]],
    *,
    campaign_root: Path | None = None,
    expected_paths: Sequence[str] = RUNTIME_SOURCE_RELATIVE_PATHS,
) -> None:
    """Reject missing, reordered, duplicated, or hash-mismatched bindings."""

    root = (
        campaign_root.resolve()
        if campaign_root is not None
        else Path(__file__).resolve().parents[2]
    )
    normalized: list[tuple[str, str]] = []
    for entry in manifest:
        if (
            not isinstance(entry, (list, tuple))
            or len(entry) != 2
            or not all(isinstance(value, str) for value in entry)
        ):
            raise ValueError("source manifest entries must be [path, sha256]")
        normalized.append((entry[0], entry[1]))
    if tuple(relative for relative, _ in normalized) != tuple(expected_paths):
        raise ValueError("source manifest path sequence is not exact")
    if len(set(relative for relative, _ in normalized)) != len(normalized):
        raise ValueError("source manifest repeats a path")
    for relative, recorded_hash in normalized:
        path = root / relative
        if not path.is_file():
            raise ValueError(f"bound file is missing: {path}")
        current_hash = sha256_file(path)
        if current_hash != recorded_hash:
            raise ValueError(
                f"source hash mismatch for {relative}: "
                f"{current_hash} != {recorded_hash}"
            )


def validate_fixed_base(graph6: object) -> BitGraph:
    if not isinstance(graph6, str):
        raise ValueError("base graph6 must be a string")
    if graph6 != BASE_GRAPH6:
        raise ValueError(
            f"base graph6 must be the exact fixed labeled record {BASE_GRAPH6!r}"
        )
    try:
        graph_a = BitGraph.from_graph6(graph6)
        graph_b = Graph.from_graph6(graph6)
    except (TypeError, UnicodeError, ValueError) as error:
        raise ValueError("fixed base graph6 is malformed") from error
    if (
        graph_a.n != BASE_ORDER
        or graph_b.order != BASE_ORDER
        or graph_a.size != BASE_SIZE
        or graph_b.size != BASE_SIZE
        or graph_a.to_graph6() != graph6
        or graph_b.to_graph6() != graph6
    ):
        raise ValueError("fixed base graph fails its order/size/round-trip pin")
    return graph_a


def toggle_pairs(order: int = BASE_ORDER) -> tuple[tuple[int, int], ...]:
    if type(order) is not int or order < 0:
        raise ValueError("order must be a nonnegative integer")
    return tuple(combinations(range(order), 2))


def origin_toggle_index_sets(
    *,
    pair_count: int = PAIR_COUNT,
    max_radius: int = MAX_TOGGLE_RADIUS,
) -> tuple[tuple[int, ...], ...]:
    if type(pair_count) is not int or pair_count < 0:
        raise ValueError("pair_count must be a nonnegative integer")
    if type(max_radius) is not int or not 0 <= max_radius <= pair_count:
        raise ValueError("max_radius must lie between zero and pair_count")
    return tuple(
        selected
        for radius in range(max_radius + 1)
        for selected in combinations(range(pair_count), radius)
    )


def toggle_graph(
    base: BitGraph,
    selected_indices: Sequence[int],
    pairs: Sequence[tuple[int, int]],
) -> BitGraph:
    indices = tuple(selected_indices)
    if (
        any(type(index) is not int for index in indices)
        or tuple(sorted(set(indices))) != indices
        or any(not 0 <= index < len(pairs) for index in indices)
    ):
        raise ValueError("toggle indices must be distinct, sorted, and in range")
    adjacency = list(base.adj)
    for index in indices:
        first, second = pairs[index]
        adjacency[first] ^= 1 << second
        adjacency[second] ^= 1 << first
    return BitGraph(base.n, tuple(adjacency))


def generate_raw_origins(
    base_graph6: str = BASE_GRAPH6,
) -> tuple[Origin, ...]:
    base = validate_fixed_base(base_graph6)
    pairs = toggle_pairs(base.n)
    selections = origin_toggle_index_sets(
        pair_count=len(pairs), max_radius=MAX_TOGGLE_RADIUS
    )
    origins = tuple(
        Origin(
            index=index,
            toggle_indices=selected,
            toggle_edges=tuple(pairs[pair_index] for pair_index in selected),
            raw_graph6=toggle_graph(base, selected, pairs).to_graph6(),
        )
        for index, selected in enumerate(selections)
    )
    validate_origin_coverage(origins, require_canonical=False)
    return origins


def canonicalize_origins(
    origins: Sequence[Origin], labelg_path: Path
) -> tuple[Origin, ...]:
    if not origins:
        raise ValueError("the origin sequence must be nonempty")
    canonical = canonicalize_graph6_batch(
        tuple(origin.raw_graph6 for origin in origins), labelg_path
    )
    if len(canonical) != len(origins):
        raise ValueError("canonicalizer changed the origin count")
    result = tuple(
        Origin(
            index=origin.index,
            toggle_indices=origin.toggle_indices,
            toggle_edges=origin.toggle_edges,
            raw_graph6=origin.raw_graph6,
            canonical_graph6=canonical_graph6,
        )
        for origin, canonical_graph6 in zip(origins, canonical, strict=True)
    )
    validate_origin_coverage(result, require_canonical=True)
    return result


def validate_origin_coverage(
    origins: Sequence[Origin], *, require_canonical: bool
) -> None:
    """Reconstruct and check every raw origin in the exact radius-two ball."""

    if len(origins) != RAW_ORIGIN_COUNT:
        raise ValueError(
            f"origin count mismatch: {len(origins)} != {RAW_ORIGIN_COUNT}"
        )
    base = validate_fixed_base(BASE_GRAPH6)
    pairs = toggle_pairs(base.n)
    expected_selections = origin_toggle_index_sets(
        pair_count=len(pairs), max_radius=MAX_TOGGLE_RADIUS
    )
    canonical_records: list[str] = []
    for expected_index, (origin, expected_selection) in enumerate(
        zip(origins, expected_selections, strict=True)
    ):
        if type(origin.index) is not int or origin.index != expected_index:
            raise ValueError(f"origin index mismatch at position {expected_index}")
        if origin.toggle_indices != expected_selection:
            raise ValueError(f"toggle-index mismatch at origin {expected_index}")
        expected_edges = tuple(pairs[index] for index in expected_selection)
        if origin.toggle_edges != expected_edges:
            raise ValueError(f"toggle-edge mismatch at origin {expected_index}")
        expected_graph6 = toggle_graph(
            base, expected_selection, pairs
        ).to_graph6()
        if origin.raw_graph6 != expected_graph6:
            raise ValueError(f"raw graph6 mismatch at origin {expected_index}")
        if require_canonical:
            if not isinstance(origin.canonical_graph6, str):
                raise ValueError(
                    f"missing canonical graph6 at origin {expected_index}"
                )
            canonical_graph = BitGraph.from_graph6(origin.canonical_graph6)
            if (
                canonical_graph.n != base.n
                or canonical_graph.size
                != BitGraph.from_graph6(origin.raw_graph6).size
            ):
                raise ValueError(
                    f"canonical graph changed order/size at origin {expected_index}"
                )
            canonical_records.append(origin.canonical_graph6)
        elif origin.canonical_graph6 is not None:
            raise ValueError("raw origins must not contain canonical records")
    if require_canonical:
        multiplicities = Counter(canonical_records)
        if sum(multiplicities.values()) != RAW_ORIGIN_COUNT:
            raise AssertionError("canonical multiplicities do not cover all origins")
        if len(multiplicities) != EXPECTED_CANONICAL_CLASS_COUNT:
            raise ValueError(
                "canonical class count mismatch: "
                f"{len(multiplicities)} != {EXPECTED_CANONICAL_CLASS_COUNT}"
            )


def _normalize_mask_family(
    family: Iterable[int], order: int
) -> frozenset[frozenset[int]]:
    return frozenset(
        frozenset(
            vertex for vertex in range(order) if mask & (1 << vertex)
        )
        for mask in family
    )


def _family_sha256(family: Iterable[frozenset[int]]) -> str:
    return _sha256_text(
        "".join(
            " ".join(map(str, sorted(configuration))) + "\n"
            for configuration in sorted(
                family, key=lambda value: tuple(sorted(value))
            )
        )
    )


def evaluate_canonical_graph(graph6: str) -> dict[str, object]:
    """Evaluate one class with both independent exact campaign stacks."""

    if not isinstance(graph6, str):
        raise ValueError("canonical graph6 must be a string")
    graph_a = BitGraph.from_graph6(graph6)
    graph_b = Graph.from_graph6(graph6)
    if (
        graph_a.n != graph_b.order
        or graph_a.size != graph_b.size
        or graph_a.to_graph6() != graph6
        or graph_b.to_graph6() != graph6
    ):
        raise AssertionError("A/B graph parser or round-trip disagreement")

    stack_a = {
        "gamma": domination_number(graph_a),
        "i": independent_domination_number(graph_a),
        "alpha": alpha(graph_a),
        "theta": theta(graph_a),
    }
    stack_b = {
        "gamma": domination_number_b(graph_b),
        "i": independent_domination_number_b(graph_b),
        "alpha": independence_number(graph_b),
        "theta": clique_cover_number(graph_b),
    }
    if stack_a != stack_b:
        raise AssertionError(("A/B static-parameter disagreement", graph6))

    decisions: list[dict[str, object]] = []
    winning_family_size: int | None = None
    winning_family_sha256: str | None = None
    gamma_infinity: int | None = None
    for guard_count in range(stack_a["gamma"], graph_a.n + 1):
        result_a = eternal_fixed_point(graph_a, guard_count)
        family_b = find_eternal_family(graph_b, guard_count)
        decision_a = result_a.exists
        decision_b = family_b is not None
        if decision_a != decision_b:
            raise AssertionError(
                (
                    "A/B eternal-decision disagreement",
                    graph6,
                    guard_count,
                )
            )
        greatest_family_equal: bool | None = None
        family_size: int | None = None
        family_sha256: str | None = None
        if decision_a:
            assert family_b is not None
            normalized_a = _normalize_mask_family(
                result_a.family, graph_a.n
            )
            greatest_family_equal = normalized_a == family_b
            if not greatest_family_equal:
                raise AssertionError(
                    (
                        "A/B greatest-eternal-family disagreement",
                        graph6,
                        guard_count,
                    )
                )
            if not verify_eternal_result(graph_a, result_a):
                raise AssertionError(
                    "verifier A rejected its explicit eternal responses"
                )
            if not verify_eternal_family(graph_b, guard_count, family_b):
                raise AssertionError(
                    "verifier B rejected the greatest eternal family"
                )
            family_size = len(family_b)
            family_sha256 = _family_sha256(family_b)
            gamma_infinity = guard_count
            winning_family_size = family_size
            winning_family_sha256 = family_sha256
        decisions.append(
            {
                "k": guard_count,
                "stack_a": decision_a,
                "stack_b": decision_b,
                "greatest_family_equal": greatest_family_equal,
                "family_size": family_size,
                "family_sha256": family_sha256,
            }
        )
        if decision_a:
            break
    if gamma_infinity is None:
        raise AssertionError("the full vertex set must be eternal")

    stack_a["gamma_infinity"] = gamma_infinity
    stack_b["gamma_infinity"] = gamma_infinity
    parameters = {
        "gamma": stack_a["gamma"],
        "i": stack_a["i"],
        "alpha": stack_a["alpha"],
        "gamma_infinity": gamma_infinity,
        "theta": stack_a["theta"],
    }
    if not (
        parameters["gamma"]
        <= parameters["i"]
        <= parameters["alpha"]
        <= parameters["gamma_infinity"]
        <= parameters["theta"]
    ):
        raise AssertionError(("parameter-chain failure", graph6, parameters))

    is_candidate = (
        parameters["gamma"]
        == parameters["gamma_infinity"]
        < parameters["theta"]
    )
    if is_candidate:
        category = "candidate_gamma_equals_eternal_below_theta"
    elif parameters["gamma"] == parameters["gamma_infinity"]:
        category = "equality_without_theta_gap"
    else:
        category = "gamma_below_eternal"
    return {
        "graph6": graph6,
        "n": graph_a.n,
        "m": graph_a.size,
        "parameters": parameters,
        "stack_a": stack_a,
        "stack_b": stack_b,
        "eternal_decisions": decisions,
        "winning_family_size": winning_family_size,
        "winning_family_sha256": winning_family_sha256,
        "category": category,
        "is_candidate": is_candidate,
    }


def _origin_spec_text(origins: Sequence[Origin]) -> str:
    return "".join(
        f"{origin.index}\t"
        f"{','.join(map(str, origin.toggle_indices))}\t"
        f"{','.join(f'{first}-{second}' for first, second in origin.toggle_edges)}\n"
        for origin in origins
    )


def _raw_graph6_text(origins: Sequence[Origin]) -> str:
    return "".join(
        f"{origin.index}\t{origin.raw_graph6}\n" for origin in origins
    )


def _canonical_origin_text(origins: Sequence[Origin]) -> str:
    return "".join(
        f"{origin.index}\t{origin.canonical_graph6}\n"
        for origin in origins
    )


def _labelg_input_text(origins: Sequence[Origin]) -> str:
    return "".join(f"{origin.raw_graph6}\n" for origin in origins)


def _labelg_output_text(origins: Sequence[Origin]) -> str:
    return "".join(f"{origin.canonical_graph6}\n" for origin in origins)


def _canonical_unique_text(classes: Sequence[Mapping[str, object]]) -> str:
    return "".join(f"{record['graph6']}\n" for record in classes)


def _canonical_multiplicity_text(
    classes: Sequence[Mapping[str, object]],
) -> str:
    return "".join(
        f"{record['graph6']}\t{record['multiplicity']}\n"
        for record in classes
    )


def _evaluation_text(classes: Sequence[Mapping[str, object]]) -> str:
    lines: list[str] = []
    for record in classes:
        parameters = record["parameters"]
        if not isinstance(parameters, Mapping):
            raise ValueError("class parameters must be an object")
        lines.append(
            f"{record['graph6']}\t{record['multiplicity']}\t"
            f"{parameters['gamma']}\t{parameters['i']}\t"
            f"{parameters['alpha']}\t{parameters['gamma_infinity']}\t"
            f"{parameters['theta']}\t"
            f"{_canonical_json(record['eternal_decisions'])}\n"
        )
    return "".join(lines)


def coverage_hashes(origins: Sequence[Origin]) -> dict[str, str]:
    return {
        "origin_spec_stream_sha256": _sha256_text(
            _origin_spec_text(origins)
        ),
        "raw_graph6_stream_sha256": _sha256_text(
            _raw_graph6_text(origins)
        ),
        "canonical_origin_stream_sha256": _sha256_text(
            _canonical_origin_text(origins)
        ),
        "labelg_input_stream_sha256": _sha256_text(
            _labelg_input_text(origins)
        ),
        "labelg_output_stream_sha256": _sha256_text(
            _labelg_output_text(origins)
        ),
    }


def class_hashes(
    classes: Sequence[Mapping[str, object]],
) -> dict[str, str]:
    return {
        "canonical_unique_stream_sha256": _sha256_text(
            _canonical_unique_text(classes)
        ),
        "canonical_multiplicity_stream_sha256": _sha256_text(
            _canonical_multiplicity_text(classes)
        ),
        "evaluation_stream_sha256": _sha256_text(
            _evaluation_text(classes)
        ),
    }


def _histogram(
    classes: Sequence[Mapping[str, object]],
    keys: Sequence[str],
) -> Counter[tuple[int, ...]]:
    counts: Counter[tuple[int, ...]] = Counter()
    for record in classes:
        parameters = record["parameters"]
        if not isinstance(parameters, Mapping):
            raise ValueError("class parameters must be an object")
        values = tuple(parameters[key] for key in keys)
        if any(type(value) is not int for value in values):
            raise ValueError("parameter values must be integers")
        counts[values] += 1
    return counts


def _histogram_json(
    histogram: Mapping[tuple[int, ...], int], keys: Sequence[str]
) -> list[dict[str, int]]:
    return [
        {
            **dict(zip(keys, values, strict=True)),
            "count": count,
        }
        for values, count in sorted(histogram.items())
    ]


def _decode_histogram(
    records: object, keys: Sequence[str]
) -> Counter[tuple[int, ...]]:
    if not isinstance(records, list):
        raise ValueError("histogram must be a list")
    result: Counter[tuple[int, ...]] = Counter()
    expected_fields = set(keys) | {"count"}
    for record in records:
        if not isinstance(record, dict) or set(record) != expected_fields:
            raise ValueError("histogram row has an unexpected schema")
        values = tuple(record[key] for key in keys)
        count = record["count"]
        if any(type(value) is not int for value in values):
            raise ValueError("histogram parameter is not an integer")
        if type(count) is not int or count <= 0:
            raise ValueError("histogram count must be a positive integer")
        if values in result:
            raise ValueError("histogram repeats a parameter tuple")
        result[values] = count
    return result


def _origin_from_json(record: object) -> Origin:
    expected = {
        "index",
        "toggle_indices",
        "toggle_edges",
        "raw_graph6",
        "canonical_graph6",
    }
    if not isinstance(record, dict) or set(record) != expected:
        raise ValueError("origin row has an unexpected schema")
    if type(record["index"]) is not int:
        raise ValueError("origin index must be an integer")
    toggle_indices = record["toggle_indices"]
    toggle_edges = record["toggle_edges"]
    if (
        not isinstance(toggle_indices, list)
        or any(type(value) is not int for value in toggle_indices)
        or not isinstance(toggle_edges, list)
        or any(
            not isinstance(edge, list)
            or len(edge) != 2
            or any(type(value) is not int for value in edge)
            for edge in toggle_edges
        )
        or not isinstance(record["raw_graph6"], str)
        or not isinstance(record["canonical_graph6"], str)
    ):
        raise ValueError("origin row contains malformed values")
    return Origin(
        index=record["index"],
        toggle_indices=tuple(toggle_indices),
        toggle_edges=tuple(tuple(edge) for edge in toggle_edges),
        raw_graph6=record["raw_graph6"],
        canonical_graph6=record["canonical_graph6"],
    )


def validate_result_payload(payload: object) -> None:
    """Check all internally reproducible claims and hashes in a result."""

    if not isinstance(payload, dict):
        raise ValueError("result must be a JSON object")
    if payload.get("schema_version") != SCHEMA_VERSION:
        raise ValueError("result schema version mismatch")
    if payload.get("status") != "complete":
        raise ValueError("result is not complete")
    if payload.get("claim_classification") != CLAIM_CLASSIFICATION:
        raise ValueError("claim classification mismatch")

    scope = payload.get("scope")
    if not isinstance(scope, dict):
        raise ValueError("missing scope object")
    exact_scope = {
        "base_graph6": BASE_GRAPH6,
        "base_order": BASE_ORDER,
        "base_size": BASE_SIZE,
        "toggle_pair_count": PAIR_COUNT,
        "maximum_toggle_radius": MAX_TOGGLE_RADIUS,
        "raw_origin_count": RAW_ORIGIN_COUNT,
        "expected_canonical_class_count": EXPECTED_CANONICAL_CLASS_COUNT,
    }
    for key, expected in exact_scope.items():
        if scope.get(key) != expected:
            raise ValueError(f"scope mismatch for {key}")

    origin_rows = payload.get("origins")
    if not isinstance(origin_rows, list):
        raise ValueError("origins must be a list")
    origins = tuple(_origin_from_json(record) for record in origin_rows)
    validate_origin_coverage(origins, require_canonical=True)

    class_rows = payload.get("canonical_classes")
    if not isinstance(class_rows, list):
        raise ValueError("canonical_classes must be a list")
    graph6_sequence: list[str] = []
    multiplicities: Counter[str] = Counter(
        origin.canonical_graph6 for origin in origins
    )
    for record in class_rows:
        if not isinstance(record, dict):
            raise ValueError("canonical class row must be an object")
        graph6 = record.get("graph6")
        multiplicity = record.get("multiplicity")
        parameters = record.get("parameters")
        stack_a = record.get("stack_a")
        stack_b = record.get("stack_b")
        decisions = record.get("eternal_decisions")
        if not isinstance(graph6, str):
            raise ValueError("canonical class graph6 must be a string")
        if type(multiplicity) is not int or multiplicity <= 0:
            raise ValueError("class multiplicity must be positive")
        if not isinstance(parameters, dict):
            raise ValueError("class parameters must be an object")
        required_parameters = {
            "gamma",
            "i",
            "alpha",
            "gamma_infinity",
            "theta",
        }
        if set(parameters) != required_parameters or any(
            type(parameters[key]) is not int for key in required_parameters
        ):
            raise ValueError("class parameter schema is malformed")
        if not isinstance(stack_a, dict) or not isinstance(stack_b, dict):
            raise ValueError("class stack results must be objects")
        if stack_a != parameters or stack_b != parameters:
            raise ValueError("A/B parameter results do not agree")
        if not (
            parameters["gamma"]
            <= parameters["i"]
            <= parameters["alpha"]
            <= parameters["gamma_infinity"]
            <= parameters["theta"]
        ):
            raise ValueError("class violates the parameter chain")
        if not isinstance(decisions, list) or not decisions:
            raise ValueError("eternal decision trace must be nonempty")
        expected_k = parameters["gamma"]
        for position, decision in enumerate(decisions):
            if not isinstance(decision, dict):
                raise ValueError("eternal decision row must be an object")
            if decision.get("k") != expected_k + position:
                raise ValueError("eternal decisions skip a guard count")
            if (
                type(decision.get("stack_a")) is not bool
                or type(decision.get("stack_b")) is not bool
                or decision["stack_a"] != decision["stack_b"]
            ):
                raise ValueError("A/B eternal decision mismatch")
            is_final = position == len(decisions) - 1
            if decision["stack_a"] != is_final:
                raise ValueError("only the terminal eternal decision may pass")
            if is_final:
                if (
                    decision.get("greatest_family_equal") is not True
                    or type(decision.get("family_size")) is not int
                    or decision["family_size"] <= 0
                    or not isinstance(decision.get("family_sha256"), str)
                    or len(decision["family_sha256"]) != 64
                    or parameters["gamma_infinity"] != decision["k"]
                    or record.get("winning_family_size")
                    != decision["family_size"]
                    or record.get("winning_family_sha256")
                    != decision["family_sha256"]
                ):
                    raise ValueError("winning eternal-family record is malformed")
            elif any(
                decision.get(key) is not None
                for key in (
                    "greatest_family_equal",
                    "family_size",
                    "family_sha256",
                )
            ):
                raise ValueError("failed decision contains a family claim")
        is_candidate = (
            parameters["gamma"]
            == parameters["gamma_infinity"]
            < parameters["theta"]
        )
        if record.get("is_candidate") is not is_candidate:
            raise ValueError("candidate flag disagrees with parameters")
        expected_category = (
            "candidate_gamma_equals_eternal_below_theta"
            if is_candidate
            else (
                "equality_without_theta_gap"
                if parameters["gamma"] == parameters["gamma_infinity"]
                else "gamma_below_eternal"
            )
        )
        if record.get("category") != expected_category:
            raise ValueError("class category disagrees with parameters")
        parsed = BitGraph.from_graph6(graph6)
        if parsed.n != record.get("n") or parsed.size != record.get("m"):
            raise ValueError("class order/size disagrees with graph6")
        if multiplicity != multiplicities[graph6]:
            raise ValueError("class multiplicity disagrees with origins")
        graph6_sequence.append(graph6)

    expected_graph6_sequence = sorted(multiplicities)
    if graph6_sequence != expected_graph6_sequence:
        raise ValueError("canonical classes are missing, repeated, or unsorted")
    if len(class_rows) != EXPECTED_CANONICAL_CLASS_COUNT:
        raise ValueError("canonical class count mismatch")
    if sum(record["multiplicity"] for record in class_rows) != RAW_ORIGIN_COUNT:
        raise ValueError("class multiplicities do not sum to the raw universe")

    projected_keys = ("gamma", "alpha", "gamma_infinity", "theta")
    full_keys = ("gamma", "i", "alpha", "gamma_infinity", "theta")
    projected = _histogram(class_rows, projected_keys)
    full = _histogram(class_rows, full_keys)
    if projected != Counter(EXPECTED_PROJECTED_HISTOGRAM):
        raise ValueError("projected parameter histogram mismatch")
    if full != Counter(EXPECTED_FULL_HISTOGRAM):
        raise ValueError("full parameter histogram mismatch")
    evaluation = payload.get("evaluation")
    if not isinstance(evaluation, dict):
        raise ValueError("missing evaluation summary")
    if _decode_histogram(
        evaluation.get("projected_histogram"), projected_keys
    ) != projected:
        raise ValueError("recorded projected histogram mismatch")
    if _decode_histogram(
        evaluation.get("full_histogram"), full_keys
    ) != full:
        raise ValueError("recorded full histogram mismatch")
    candidate_count = sum(
        bool(record["is_candidate"]) for record in class_rows
    )
    if (
        evaluation.get("all_stack_results_agree") is not True
        or evaluation.get("evaluated_canonical_classes")
        != EXPECTED_CANONICAL_CLASS_COUNT
        or evaluation.get("candidate_count") != candidate_count
        or candidate_count != 0
    ):
        raise ValueError("evaluation summary mismatch")

    canonicalization = payload.get("canonicalization")
    if not isinstance(canonicalization, dict):
        raise ValueError("missing canonicalization summary")
    expected_counts = {
        "raw_origin_count": RAW_ORIGIN_COUNT,
        "canonical_class_count": EXPECTED_CANONICAL_CLASS_COUNT,
        "multiplicity_sum": RAW_ORIGIN_COUNT,
    }
    for key, expected in expected_counts.items():
        if canonicalization.get(key) != expected:
            raise ValueError(f"canonicalization count mismatch for {key}")
    recorded_coverage_hashes = canonicalization.get("coverage_hashes")
    recorded_class_hashes = evaluation.get("class_hashes")
    if recorded_coverage_hashes != coverage_hashes(origins):
        raise ValueError("coverage stream hash mismatch")
    if recorded_class_hashes != class_hashes(class_rows):
        raise ValueError("class/evaluation stream hash mismatch")
    multiplicity_histogram = Counter(multiplicities.values())
    expected_multiplicity_histogram = [
        {"multiplicity": multiplicity, "class_count": count}
        for multiplicity, count in sorted(multiplicity_histogram.items())
    ]
    if (
        canonicalization.get("multiplicity_histogram")
        != expected_multiplicity_histogram
    ):
        raise ValueError("canonical multiplicity histogram mismatch")


def _maximum_rss_bytes(usage: resource.struct_rusage) -> int:
    # Darwin reports bytes; Linux and most BSD-derived CI images report KiB.
    value = int(usage.ru_maxrss)
    return value if platform.system() == "Darwin" else value * 1024


def _sysctl_integer(name: str) -> int | None:
    if platform.system() != "Darwin":
        return None
    completed = subprocess.run(
        ["/usr/sbin/sysctl", "-n", name],
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        text=True,
    )
    if completed.returncode != 0:
        return None
    try:
        return int(completed.stdout.strip())
    except ValueError:
        return None


def _git_commit(campaign_root: Path) -> str | None:
    completed = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=campaign_root,
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        text=True,
    )
    commit = completed.stdout.strip()
    return commit if completed.returncode == 0 and len(commit) == 40 else None


def _atomic_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=path.name + ".", suffix=".partial", dir=path.parent
    )
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
            json.dump(payload, handle, indent=2, sort_keys=True)
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary_name, path)
        directory_descriptor = os.open(path.parent, os.O_RDONLY)
        try:
            os.fsync(directory_descriptor)
        finally:
            os.close(directory_descriptor)
    except BaseException:
        try:
            os.unlink(temporary_name)
        except FileNotFoundError:
            pass
        raise


def _validate_output_path(path: Path, campaign_root: Path) -> Path:
    resolved = path.resolve()
    if resolved.suffix.lower() != ".json":
        raise ValueError("result output must have a .json suffix")
    protected = {
        (campaign_root / relative).resolve()
        for relative in (
            *RUNTIME_SOURCE_RELATIVE_PATHS,
            *SUPPORTING_ARTIFACT_RELATIVE_PATHS,
        )
    }
    if resolved in protected:
        raise ValueError("result output aliases a bound source/support file")
    return resolved


def run_measurement(
    *,
    labelg_path: Path,
    output_path: Path,
) -> dict[str, object]:
    campaign_root = Path(__file__).resolve().parents[2]
    output = _validate_output_path(output_path, campaign_root)
    start_wall = time.perf_counter()
    start_self = resource.getrusage(resource.RUSAGE_SELF)
    start_children = resource.getrusage(resource.RUSAGE_CHILDREN)

    labelg_hash = verify_pinned_labelg(labelg_path)
    if labelg_hash != EXPECTED_LABELG_SHA256:
        raise AssertionError("pinned labelg hash constant is inconsistent")
    runtime_manifest = runtime_source_manifest(campaign_root)
    support_manifest = supporting_artifact_manifest(campaign_root)
    base = validate_fixed_base(BASE_GRAPH6)
    if canonicalize_graph6_batch((BASE_GRAPH6,), labelg_path) != (
        BASE_GRAPH6,
    ):
        raise ValueError("the fixed base record is not canonical under labelg")

    raw_origins = generate_raw_origins()
    origins = canonicalize_origins(raw_origins, labelg_path)
    multiplicities = Counter(
        origin.canonical_graph6 for origin in origins
    )
    classes: list[dict[str, object]] = []
    for graph6 in sorted(multiplicities):
        if graph6 is None:
            raise AssertionError("canonical origin unexpectedly missing")
        evaluation = evaluate_canonical_graph(graph6)
        evaluation["multiplicity"] = multiplicities[graph6]
        classes.append(evaluation)

    projected_keys = ("gamma", "alpha", "gamma_infinity", "theta")
    full_keys = ("gamma", "i", "alpha", "gamma_infinity", "theta")
    projected = _histogram(classes, projected_keys)
    full = _histogram(classes, full_keys)
    if projected != Counter(EXPECTED_PROJECTED_HISTOGRAM):
        raise AssertionError(("unexpected projected histogram", projected))
    if full != Counter(EXPECTED_FULL_HISTOGRAM):
        raise AssertionError(("unexpected full histogram", full))

    end_self = resource.getrusage(resource.RUSAGE_SELF)
    end_children = resource.getrusage(resource.RUSAGE_CHILDREN)
    elapsed = time.perf_counter() - start_wall
    payload: dict[str, object] = {
        "schema_version": SCHEMA_VERSION,
        "status": "complete",
        "claim_classification": CLAIM_CLASSIFICATION,
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "scope": {
            "base_graph6": BASE_GRAPH6,
            "base_graph6_sha256": _sha256_text(BASE_GRAPH6 + "\n"),
            "base_order": base.n,
            "base_size": base.size,
            "toggle_pair_count": PAIR_COUNT,
            "maximum_toggle_radius": MAX_TOGGLE_RADIUS,
            "raw_origin_count": RAW_ORIGIN_COUNT,
            "expected_canonical_class_count": (
                EXPECTED_CANONICAL_CLASS_COUNT
            ),
            "origin_order": (
                "radius 0, then radius 1, then radius 2; within each "
                "radius lexicographic combinations of pair indices, where "
                "pairs are lexicographic combinations(range(12), 2)"
            ),
            "limitations": [
                "This is only the exact edge-toggle ball of radius at most "
                "two around one fixed graph.",
                "It does not cover other order-12 graphs or any graph at "
                "greater edit distance.",
                "Canonical coverage and evaluation are source-bound but not "
                "backed here by an independent coverage checker or SAT proof "
                "logs, so the result is classified OBSERVED.",
                "Zero candidates in this ball neither resolves the conjecture "
                "nor certifies the n=12,k=3 slice.",
            ],
        },
        "bindings": {
            "git_commit_at_run": _git_commit(campaign_root),
            "labelg_path": str(labelg_path.resolve()),
            "labelg_sha256": labelg_hash,
            "nauty_archive_sha256": NAUTY_ARCHIVE_SHA256,
            "runtime_source_manifest": [
                list(entry) for entry in runtime_manifest
            ],
            "runtime_source_set_sha256": _source_set_sha256(
                runtime_manifest
            ),
            "supporting_artifact_manifest": [
                list(entry) for entry in support_manifest
            ],
            "supporting_artifact_set_sha256": _source_set_sha256(
                support_manifest
            ),
        },
        "canonicalization": {
            "tool": "nauty 2.9.3 labelg -q -g",
            "raw_origin_count": len(origins),
            "canonical_class_count": len(multiplicities),
            "multiplicity_sum": sum(multiplicities.values()),
            "multiplicity_histogram": [
                {
                    "multiplicity": multiplicity,
                    "class_count": count,
                }
                for multiplicity, count in sorted(
                    Counter(multiplicities.values()).items()
                )
            ],
            "coverage_hashes": coverage_hashes(origins),
            "hash_stream_formats": HASH_STREAM_FORMATS,
        },
        "evaluation": {
            "model": (
                "one guard moves along one edge; attacks only at unoccupied "
                "vertices; every family state dominates"
            ),
            "stack_a": (
                "bitset subset invariants, subset-DP clique cover, "
                "greatest-fixed-point eternal deletion"
            ),
            "stack_b": (
                "frozenset subset invariants, complement DSATUR coloring, "
                "explicit colored configuration digraph"
            ),
            "all_stack_results_agree": True,
            "evaluated_canonical_classes": len(classes),
            "candidate_count": sum(
                bool(record["is_candidate"]) for record in classes
            ),
            "projected_histogram_fields": list(projected_keys),
            "projected_histogram": _histogram_json(
                projected, projected_keys
            ),
            "full_histogram_fields": list(full_keys),
            "full_histogram": _histogram_json(full, full_keys),
            "class_hashes": class_hashes(classes),
        },
        "resources": {
            "checkpointing": (
                "not used: measured wall time is below one minute and the "
                "entire deterministic run is safely rerunnable"
            ),
            "wall_seconds": round(elapsed, 6),
            "self_user_cpu_seconds": round(
                end_self.ru_utime - start_self.ru_utime, 6
            ),
            "self_system_cpu_seconds": round(
                end_self.ru_stime - start_self.ru_stime, 6
            ),
            "child_user_cpu_seconds": round(
                end_children.ru_utime - start_children.ru_utime, 6
            ),
            "child_system_cpu_seconds": round(
                end_children.ru_stime - start_children.ru_stime, 6
            ),
            "self_max_rss_bytes": _maximum_rss_bytes(end_self),
            "child_max_rss_bytes": _maximum_rss_bytes(end_children),
            "logical_cpu_count": os.cpu_count(),
            "physical_cpu_count": _sysctl_integer("hw.physicalcpu"),
            "physical_memory_bytes": _sysctl_integer("hw.memsize"),
            "platform": platform.platform(),
            "machine": platform.machine(),
            "python_implementation": platform.python_implementation(),
            "python_version": platform.python_version(),
            "python_executable": str(Path(sys.executable).resolve()),
        },
        "reproduction": {
            "focused_tests": (
                "PYTHONPATH=src python3 -m unittest -v "
                "tests.test_deep_survivor_radius2"
            ),
            "measurement": (
                "PYTHONPATH=src python3 -m search.deep_survivor_radius2 "
                "--validation-gate-open "
                "--output results/deep_survivor_radius2_measurement.json "
                "--labelg tools/nauty2_9_3/labelg"
            ),
            "deep_audit": (
                "PYTHONPATH=src python3 -m search.deep_survivor_radius2 "
                "--audit-result "
                "results/deep_survivor_radius2_measurement.json "
                "--deep --labelg tools/nauty2_9_3/labelg"
            ),
        },
        "origins": [origin.as_json() for origin in origins],
        "canonical_classes": classes,
    }
    validate_result_payload(payload)
    _atomic_json(output, payload)
    return payload


def validate_bound_environment(
    payload: Mapping[str, object],
    *,
    labelg_path: Path,
    campaign_root: Path | None = None,
) -> None:
    root = (
        campaign_root.resolve()
        if campaign_root is not None
        else Path(__file__).resolve().parents[2]
    )
    bindings = payload.get("bindings")
    if not isinstance(bindings, dict):
        raise ValueError("missing bindings object")
    labelg_hash = verify_pinned_labelg(labelg_path)
    if (
        bindings.get("labelg_sha256") != labelg_hash
        or bindings.get("nauty_archive_sha256") != NAUTY_ARCHIVE_SHA256
    ):
        raise ValueError("labelg/nauty binding mismatch")
    runtime_manifest = bindings.get("runtime_source_manifest")
    support_manifest = bindings.get("supporting_artifact_manifest")
    if not isinstance(runtime_manifest, list) or not isinstance(
        support_manifest, list
    ):
        raise ValueError("source/support manifests must be lists")
    validate_current_manifest(
        runtime_manifest,
        campaign_root=root,
        expected_paths=RUNTIME_SOURCE_RELATIVE_PATHS,
    )
    validate_current_manifest(
        support_manifest,
        campaign_root=root,
        expected_paths=SUPPORTING_ARTIFACT_RELATIVE_PATHS,
    )
    normalized_runtime = tuple(
        (entry[0], entry[1]) for entry in runtime_manifest
    )
    normalized_support = tuple(
        (entry[0], entry[1]) for entry in support_manifest
    )
    if bindings.get("runtime_source_set_sha256") != _source_set_sha256(
        normalized_runtime
    ):
        raise ValueError("runtime source-set hash mismatch")
    if bindings.get("supporting_artifact_set_sha256") != _source_set_sha256(
        normalized_support
    ):
        raise ValueError("supporting artifact-set hash mismatch")


def audit_result(
    result_path: Path, *, labelg_path: Path, deep: bool
) -> dict[str, object]:
    with result_path.open(encoding="utf-8") as handle:
        payload = json.load(handle)
    validate_result_payload(payload)
    validate_bound_environment(payload, labelg_path=labelg_path)

    deep_checks = {
        "live_labelg_recanonicalization": False,
        "live_two_stack_reevaluation": False,
    }
    if deep:
        origins = tuple(
            _origin_from_json(record) for record in payload["origins"]
        )
        recanonicalized = canonicalize_graph6_batch(
            tuple(origin.raw_graph6 for origin in origins), labelg_path
        )
        recorded = tuple(origin.canonical_graph6 for origin in origins)
        if recanonicalized != recorded:
            raise ValueError("live labelg output differs from the result")
        deep_checks["live_labelg_recanonicalization"] = True

        classes = payload["canonical_classes"]
        assert isinstance(classes, list)
        for recorded_class in classes:
            graph6 = recorded_class["graph6"]
            reevaluated = evaluate_canonical_graph(graph6)
            reevaluated["multiplicity"] = recorded_class["multiplicity"]
            if reevaluated != recorded_class:
                raise ValueError(
                    f"live reevaluation differs for {graph6!r}"
                )
        deep_checks["live_two_stack_reevaluation"] = True
    return {
        "status": "passed",
        "result_path": str(result_path.resolve()),
        "result_sha256": sha256_file(result_path),
        "deep": deep,
        **deep_checks,
    }


def _parser() -> argparse.ArgumentParser:
    campaign = Path(__file__).resolve().parents[2]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--labelg",
        type=Path,
        default=campaign / "tools" / "nauty2_9_3" / "labelg",
        help="pinned nauty 2.9.3 labelg executable",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=campaign
        / "results"
        / "deep_survivor_radius2_measurement.json",
    )
    parser.add_argument(
        "--validation-gate-open",
        action="store_true",
        help="required before writing a production measurement",
    )
    parser.add_argument(
        "--audit-result",
        type=Path,
        help="read-only audit of an existing result instead of generation",
    )
    parser.add_argument(
        "--deep",
        action="store_true",
        help="with --audit-result, rerun labelg and both evaluator stacks",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    arguments = _parser().parse_args(argv)
    if arguments.audit_result is not None:
        summary = audit_result(
            arguments.audit_result,
            labelg_path=arguments.labelg,
            deep=arguments.deep,
        )
        print(_canonical_json(summary))
        return 0
    if arguments.deep:
        raise SystemExit("--deep requires --audit-result")
    if not arguments.validation_gate_open:
        raise SystemExit(
            "refusing to write a measurement without --validation-gate-open"
        )
    payload = run_measurement(
        labelg_path=arguments.labelg,
        output_path=arguments.output,
    )
    summary = {
        "status": payload["status"],
        "claim_classification": payload["claim_classification"],
        "raw_origin_count": payload["scope"]["raw_origin_count"],
        "canonical_class_count": payload["canonicalization"][
            "canonical_class_count"
        ],
        "candidate_count": payload["evaluation"]["candidate_count"],
        "output": str(arguments.output.resolve()),
        "output_sha256": sha256_file(arguments.output),
    }
    print(_canonical_json(summary))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
