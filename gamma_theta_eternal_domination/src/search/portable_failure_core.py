#!/usr/bin/env python3
"""Generate and audit portable three-guard obstruction-core artifacts.

The generator uses the standard-library bitset implementation in
``search.three_step_kernel``.  The audit path separately recomputes kernel
levels with ordinary ``frozenset`` configurations and verifies ranked attack
DAGs directly.  Exact bounded graph isomorphisms use the independently frozen
``coverage_checker.graph`` backtracker.

The one-vertex-extension table uses pinned nauty 2.9.3 ``labelg`` only to
produce unmarked canonical keys.  Its 623-class conclusion is deliberately
classified as OBSERVED: the audit verifies every raw-to-key isomorphism but
does not independently derive a canonical normal form or prove distinct keys
nonisomorphic.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import csv
from dataclasses import dataclass
from functools import lru_cache
from hashlib import sha256
from itertools import combinations
import json
import os
from pathlib import Path
import subprocess
import tempfile
from typing import Iterable, Iterator, Mapping, Sequence

from coverage_checker.graph import (
    Graph as AuditGraph,
    find_isomorphism,
)
from search.three_step_kernel import (
    KernelGraph,
    adjacent_guards,
    combination_masks,
    first_undominated,
    independence_number,
    is_dominating,
    is_independent,
    kernel_profile,
    maximum_independent_states,
    successor,
)


CAMPAIGN_ROOT = Path(__file__).resolve().parents[2]
CERTIFICATE_FORMAT = "gamma-theta-portable-failure-cores-v1"
RESULT_FORMAT = "gamma-theta-portable-failure-core-measurement-v1"
EXTENSION_COLUMNS = (
    "canonical_graph6",
    "n",
    "m",
    "origin_count",
    "gamma",
    "alpha",
    "earliest_forced_rank",
    "latest_forced_rank",
    "full_kernel_deletion_depth",
)

J_GRAPH6 = "J@l|bfNuVK_"
Q_GRAPH6 = "Kun_w{vRrblV"
GUARD_COUNT = 3

EXPECTED_LABELG_SHA256 = (
    "ae8b1e7ef173c1665725e708bd7abd00b08ee4230ba2bd04117ec63d441274a0"
)
NAUTY_ARCHIVE_SHA256 = (
    "9fc4edae04f88a0f5883985be3b39cf7f898fd6cc96e96b9ee25452743cc1b5b"
)

EXPECTED_CORE_DATA = {
    J_GRAPH6: {
        "id": "J",
        "order": 11,
        "size": 32,
        "root": (1, 4, 6),
        "kernel_3": (110, 105, 100, 88, 64, 10, 0),
        "kernel_4": (311, 311),
        "dag_attack_states": 8,
        "dag_terminal_states": 9,
        "dag_nodes": 17,
        "tree_nodes": 19,
        "tree_leaves": 10,
        "tree_depth": 5,
    },
    Q_GRAPH6: {
        "id": "Q",
        "order": 12,
        "size": 40,
        "root": (1, 2, 6),
        "kernel_3": (147, 143, 136, 128, 119, 93, 28, 0),
        "kernel_4": (461, 461),
        "dag_attack_states": 9,
        "dag_terminal_states": 11,
        "dag_nodes": 20,
        "tree_nodes": 27,
        "tree_leaves": 16,
        "tree_depth": 6,
    },
}


@dataclass(frozen=True, slots=True)
class EmbeddingSpec:
    host_graph6: str
    deleted_vertex: int
    base_to_host: tuple[int, ...]
    extension_kind: str
    reference_vertex: int | None
    extra_neighbor: int | None


EMBEDDING_SPECS = (
    EmbeddingSpec(
        "K]?H[|]nj}\\k",
        4,
        (0, 1, 5, 6, 9, 8, 7, 10, 3, 2, 11),
        "true_twin",
        2,
        None,
    ),
    EmbeddingSpec(
        "KoDbMyz}@}ju",
        3,
        (0, 4, 5, 6, 2, 10, 1, 11, 9, 8, 7),
        "true_twin",
        1,
        None,
    ),
    EmbeddingSpec(
        "KoYu~_VMyzLf",
        8,
        (0, 3, 4, 11, 2, 9, 1, 10, 7, 5, 6),
        "near_twin",
        1,
        3,
    ),
    EmbeddingSpec(
        "Kp]e~_VDyZlf",
        8,
        (0, 3, 10, 11, 5, 9, 1, 4, 6, 2, 7),
        "true_twin",
        5,
        None,
    ),
    EmbeddingSpec(
        "Krqb}iw[W^`~",
        10,
        (4, 5, 3, 9, 8, 2, 1, 7, 0, 11, 6),
        "true_twin",
        9,
        None,
    ),
    EmbeddingSpec(
        "KrrDthx\\_^`~",
        10,
        (4, 5, 2, 3, 8, 7, 6, 9, 11, 1, 0),
        "true_twin",
        8,
        None,
    ),
)

EXPECTED_EXTENSION_PARAMETER_COUNTS = {
    (1, 3): 1,
    (2, 3): 176,
    (2, 4): 60,
    (3, 3): 89,
    (3, 4): 297,
}
EXPECTED_EXTENSION_RANK_COUNTS = {1: 12, 2: 32, 3: 36, 4: 3, 5: 6}
EXPECTED_DEEP_EXTENSION_KEYS = tuple(
    sorted(spec.host_graph6 for spec in EMBEDDING_SPECS)
)

RUNTIME_SOURCE_PATHS = (
    "src/search/portable_failure_core.py",
    "src/search/three_step_kernel.py",
    "src/coverage_checker/graph.py",
)
SUPPORTING_ARTIFACT_PATHS = (
    "math/lemmas/portable_failure_core.md",
    "tests/test_portable_failure_core.py",
)
INPUT_PATHS = (
    "certificates/k3_three_step_edge_toggle.ndjson",
    "results/three_step_kernel_measurement.json",
    "results/edge_toggles_unique.csv",
)


class PortableCoreError(ValueError):
    """Raised when a portable-core artifact or input is invalid."""


def sha256_file(path: Path) -> str:
    digest = sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def graph6_sha256(record: str) -> str:
    return sha256((record + "\n").encode("ascii")).hexdigest()


def canonical_json(value: object) -> bytes:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
        allow_nan=False,
    ).encode("ascii")


def object_sha256(value: object) -> str:
    return sha256(canonical_json(value)).hexdigest()


def _strict_object(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if not isinstance(key, str) or key in result:
            raise PortableCoreError("duplicate or non-text JSON key")
        result[key] = value
    return result


def strict_json_load(path: Path) -> object:
    try:
        with path.open(encoding="ascii") as handle:
            return json.load(
                handle,
                object_pairs_hook=_strict_object,
                parse_constant=lambda value: (_ for _ in ()).throw(
                    PortableCoreError(
                        f"non-finite JSON constant {value!r}"
                    )
                ),
            )
    except (json.JSONDecodeError, UnicodeError) as error:
        raise PortableCoreError(f"invalid JSON in {path}: {error}") from error


def atomic_bytes(path: Path, content: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary = tempfile.mkstemp(
        prefix=path.name + ".", suffix=".partial", dir=path.parent
    )
    try:
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(content)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
        directory = os.open(path.parent, os.O_RDONLY)
        try:
            os.fsync(directory)
        finally:
            os.close(directory)
    except BaseException:
        try:
            os.unlink(temporary)
        except FileNotFoundError:
            pass
        raise


def atomic_json(path: Path, value: object) -> None:
    atomic_bytes(
        path,
        json.dumps(
            value,
            indent=2,
            sort_keys=True,
            ensure_ascii=True,
            allow_nan=False,
        ).encode("ascii")
        + b"\n",
    )


def source_manifest(
    campaign_root: Path, relative_paths: Sequence[str]
) -> tuple[dict[str, str], ...]:
    rows: list[dict[str, str]] = []
    for relative in relative_paths:
        path = campaign_root / relative
        if not path.is_file():
            raise PortableCoreError(f"missing bound file: {relative}")
        rows.append({"path": relative, "sha256": sha256_file(path)})
    return tuple(rows)


def validate_source_manifest(
    value: object,
    *,
    campaign_root: Path,
    expected_paths: Sequence[str],
) -> tuple[dict[str, str], ...]:
    if not isinstance(value, list) or len(value) != len(expected_paths):
        raise PortableCoreError("source manifest length differs")
    rows: list[dict[str, str]] = []
    for expected, item in zip(expected_paths, value):
        if (
            not isinstance(item, dict)
            or set(item) != {"path", "sha256"}
            or item.get("path") != expected
            or not isinstance(item.get("sha256"), str)
        ):
            raise PortableCoreError("source manifest schema differs")
        actual = sha256_file(campaign_root / expected)
        if item["sha256"] != actual:
            raise PortableCoreError(f"source hash mismatch: {expected}")
        rows.append({"path": expected, "sha256": actual})
    return tuple(rows)


def mask_vertices(mask: int) -> tuple[int, ...]:
    return tuple(
        vertex for vertex in range(mask.bit_length()) if mask & (1 << vertex)
    )


def vertices_mask(vertices: Iterable[int]) -> int:
    result = 0
    for vertex in vertices:
        result |= 1 << vertex
    return result


def induced_kernel_graph(
    graph: KernelGraph, keep: Sequence[int]
) -> KernelGraph:
    vertices = tuple(keep)
    if (
        len(set(vertices)) != len(vertices)
        or any(
            type(vertex) is not int
            or not 0 <= vertex < graph.order
            for vertex in vertices
        )
    ):
        raise PortableCoreError("invalid induced-subgraph vertex sequence")
    old_to_new = {vertex: index for index, vertex in enumerate(vertices)}
    return KernelGraph.from_edges(
        len(vertices),
        (
            (old_to_new[first], old_to_new[second])
            for index, first in enumerate(vertices)
            for second in vertices[index + 1 :]
            if graph.neighbors[first] & (1 << second)
        ),
    )


def induced_audit_graph(
    graph: AuditGraph, keep: Sequence[int]
) -> AuditGraph:
    vertices = tuple(keep)
    old_to_new = {vertex: index for index, vertex in enumerate(vertices)}
    return AuditGraph.from_edges(
        len(vertices),
        (
            (old_to_new[first], old_to_new[second])
            for index, first in enumerate(vertices)
            for second in vertices[index + 1 :]
            if graph.neighbors[first] & (1 << second)
        ),
    )


def extend_kernel_graph(graph: KernelGraph, neighborhood: int) -> KernelGraph:
    if (
        type(neighborhood) is not int
        or neighborhood <= 0
        or neighborhood & ~graph.full
    ):
        raise PortableCoreError("extension neighborhood is invalid")
    new_vertex = graph.order
    return KernelGraph.from_edges(
        graph.order + 1,
        tuple(
            (first, second)
            for first in range(graph.order)
            for second in range(first + 1, graph.order)
            if graph.neighbors[first] & (1 << second)
        )
        + tuple(
            (vertex, new_vertex)
            for vertex in range(graph.order)
            if neighborhood & (1 << vertex)
        ),
    )


def domination_number(graph: KernelGraph) -> int:
    for cardinality in range(graph.order + 1):
        if any(
            is_dominating(graph, state)
            for state in combination_masks(graph.order, cardinality)
        ):
            return cardinality
    raise AssertionError("the full vertex set dominates")


RankTree = tuple[object, ...]


def _ranked_failure_tree(
    graph: KernelGraph, root: int
) -> tuple[tuple[int, int, int, RankTree], Mapping[int, RankTree]]:
    profile = kernel_profile(graph, GUARD_COUNT)
    if root not in profile.deletion_rank:
        raise PortableCoreError("root does not have a finite deletion rank")

    @lru_cache(maxsize=None)
    def solve(state: int) -> tuple[int, int, int, RankTree]:
        witness = first_undominated(graph, state)
        if witness is not None:
            return 1, 1, 0, ("terminal", state, witness)
        rank = profile.deletion_rank.get(state)
        if rank is None:
            raise PortableCoreError("reachable state survives eternally")
        choices: list[tuple[int, int, int, RankTree]] = []
        for attacked in range(graph.order):
            if state & (1 << attacked):
                continue
            children: list[
                tuple[int, tuple[int, int, int, RankTree]]
            ] = []
            for guard in adjacent_guards(graph, state, attacked):
                child_state = successor(state, guard, attacked)
                child_rank = profile.deletion_rank.get(child_state, 0)
                if is_dominating(graph, child_state) and (
                    child_rank == 0 or child_rank >= rank
                ):
                    break
                children.append((guard, solve(child_state)))
            else:
                choices.append(
                    (
                        1 + sum(child[0] for _, child in children),
                        sum(child[1] for _, child in children),
                        1
                        + max(
                            (child[2] for _, child in children),
                            default=-1,
                        ),
                        (
                            "attack",
                            state,
                            rank,
                            attacked,
                            tuple(
                                (guard, child[3])
                                for guard, child in children
                            ),
                        ),
                    )
                )
        if not choices:
            raise PortableCoreError("deleted state has no defeating attack")
        return min(choices)

    tree = solve(root)
    attack_nodes: dict[int, RankTree] = {}

    def collect(node: RankTree) -> None:
        if node[0] == "terminal":
            return
        state = node[1]
        if not isinstance(state, int):
            raise AssertionError("rank-tree state is not an integer")
        prior = attack_nodes.get(state)
        if prior is not None:
            if prior != node:
                raise PortableCoreError(
                    "same ranked state received two attack choices"
                )
            return
        attack_nodes[state] = node
        branches = node[4]
        if not isinstance(branches, tuple):
            raise AssertionError("rank-tree branches are not a tuple")
        for _, child in branches:
            collect(child)

    collect(tree[3])
    return tree, attack_nodes


def _core_certificate(record: str) -> dict[str, object]:
    expected = EXPECTED_CORE_DATA[record]
    graph = KernelGraph.from_graph6(record)
    root = vertices_mask(expected["root"])
    if (
        graph.order != expected["order"]
        or graph.size != expected["size"]
        or not is_independent(graph, root)
    ):
        raise PortableCoreError("fixed core metadata differs")

    profile_3 = kernel_profile(graph, 3)
    profile_4 = kernel_profile(graph, 4)
    sizes_3 = tuple(len(level) for level in profile_3.levels)
    sizes_4 = tuple(len(level) for level in profile_4.levels)
    if (
        sizes_3 != expected["kernel_3"]
        or sizes_4 != expected["kernel_4"]
        or profile_3.stable_family
        or not profile_4.stable_family
        or domination_number(graph) != 3
        or independence_number(graph) != 3
    ):
        raise PortableCoreError("fixed core parameters differ")

    tree, nodes = _ranked_failure_tree(graph, root)
    terminals: dict[int, int] = {}
    rows: list[dict[str, object]] = []
    for state, node in sorted(
        nodes.items(), key=lambda item: (-int(item[1][2]), item[0])
    ):
        _, node_state, rank, attacked, branches = node
        if node_state != state:
            raise AssertionError("rank-tree key mismatch")
        responses: list[dict[str, object]] = []
        for guard, child in branches:
            child_kind = child[0]
            child_state = child[1]
            response: dict[str, object] = {
                "guard": guard,
                "successor": list(mask_vertices(int(child_state))),
            }
            if child_kind == "terminal":
                witness = child[2]
                response["undominated"] = witness
                terminals[int(child_state)] = int(witness)
            else:
                response["successor_rank"] = child[2]
            responses.append(response)
        rows.append(
            {
                "configuration": list(mask_vertices(state)),
                "rank": rank,
                "attack": attacked,
                "responses": responses,
            }
        )

    statistics = {
        "attack_states": len(nodes),
        "distinct_terminal_states": len(terminals),
        "dag_nodes": len(nodes) + len(terminals),
        "unrolled_tree_nodes": tree[0],
        "unrolled_tree_leaves": tree[1],
        "unrolled_tree_depth": tree[2],
    }
    for key, expected_key in (
        ("attack_states", "dag_attack_states"),
        ("distinct_terminal_states", "dag_terminal_states"),
        ("dag_nodes", "dag_nodes"),
        ("unrolled_tree_nodes", "tree_nodes"),
        ("unrolled_tree_leaves", "tree_leaves"),
        ("unrolled_tree_depth", "tree_depth"),
    ):
        if statistics[key] != expected[expected_key]:
            raise PortableCoreError(f"unexpected {record} statistic {key}")

    return {
        "id": expected["id"],
        "graph6": record,
        "graph6_sha256": graph6_sha256(record),
        "order": graph.order,
        "size": graph.size,
        "guard_count": GUARD_COUNT,
        "gamma": 3,
        "alpha": 3,
        "gamma_infinity": 4,
        "kernel_sizes": {
            "3": list(sizes_3),
            "4": list(sizes_4),
        },
        "root": list(expected["root"]),
        "root_rank": profile_3.deletion_rank[root],
        "ranked_attack_dag": rows,
        "statistics": statistics,
    }


def _embedding_record(spec: EmbeddingSpec) -> dict[str, object]:
    base = KernelGraph.from_graph6(J_GRAPH6)
    host = KernelGraph.from_graph6(spec.host_graph6)
    mapping = spec.base_to_host
    if (
        host.order != 12
        or host.size not in (38, 39)
        or len(mapping) != base.order
        or len(set(mapping)) != base.order
        or set(mapping) != set(range(host.order)) - {spec.deleted_vertex}
    ):
        raise PortableCoreError("fixed embedding metadata differs")
    for first in range(base.order):
        for second in range(first + 1, base.order):
            base_edge = bool(base.neighbors[first] & (1 << second))
            host_edge = bool(
                host.neighbors[mapping[first]] & (1 << mapping[second])
            )
            if base_edge != host_edge:
                raise PortableCoreError("fixed embedding is not induced")

    neighborhood = tuple(
        vertex
        for vertex, image in enumerate(mapping)
        if host.neighbors[spec.deleted_vertex] & (1 << image)
    )
    if spec.reference_vertex is not None:
        reference_closed = set(
            mask_vertices(
                base.neighbors[spec.reference_vertex]
                | (1 << spec.reference_vertex)
            )
        )
        expected_neighbors = set(reference_closed)
        if spec.extension_kind == "near_twin":
            if spec.extra_neighbor is None:
                raise AssertionError("near-twin extra neighbor is missing")
            expected_neighbors.add(spec.extra_neighbor)
        elif spec.extension_kind != "true_twin":
            raise AssertionError("unknown extension kind")
        if set(neighborhood) != expected_neighbors:
            raise PortableCoreError("extension-kind annotation differs")

    payload = {
        "host_graph6": spec.host_graph6,
        "host_graph6_sha256": graph6_sha256(spec.host_graph6),
        "host_order": host.order,
        "host_size": host.size,
        "deleted_vertex": spec.deleted_vertex,
        "base_to_host": list(mapping),
        "extension_neighborhood_in_J_labels": list(neighborhood),
        "extension_kind": spec.extension_kind,
        "reference_vertex_in_J": spec.reference_vertex,
        "extra_neighbor_in_J": spec.extra_neighbor,
    }
    payload["embedding_sha256"] = object_sha256(payload)
    return payload


def verify_labelg(labelg_path: Path) -> str:
    if not labelg_path.is_file():
        raise PortableCoreError(f"missing labelg executable: {labelg_path}")
    digest = sha256_file(labelg_path)
    if digest != EXPECTED_LABELG_SHA256:
        raise PortableCoreError("labelg hash differs from pinned nauty 2.9.3")
    return digest


def canonicalize_graph6(
    records: Sequence[str], labelg_path: Path
) -> tuple[str, ...]:
    verify_labelg(labelg_path)
    if not records:
        return ()
    for record in records:
        graph = KernelGraph.from_graph6(record)
        if graph.to_graph6() != record:
            raise PortableCoreError("labelg input is not strict graph6")
    process = subprocess.run(
        (str(labelg_path), "-q", "-g"),
        input=("".join(record + "\n" for record in records)).encode("ascii"),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if process.returncode != 0:
        raise PortableCoreError(
            "labelg failed: "
            + process.stderr.decode("utf-8", errors="replace")[-1000:]
        )
    try:
        output = process.stdout.decode("ascii").splitlines()
    except UnicodeDecodeError as error:
        raise PortableCoreError("labelg output is not ASCII") from error
    if len(output) != len(records):
        raise PortableCoreError("labelg changed the graph count")
    for record in output:
        graph = KernelGraph.from_graph6(record)
        if graph.to_graph6() != record:
            raise PortableCoreError("labelg output is not strict graph6")
    return tuple(output)


def _extension_rows(
    labelg_path: Path,
) -> tuple[tuple[dict[str, object], ...], dict[str, object]]:
    base = KernelGraph.from_graph6(J_GRAPH6)
    raw_records = tuple(
        extend_kernel_graph(base, neighborhood).to_graph6()
        for neighborhood in range(1, 1 << base.order)
    )
    if len(raw_records) != 2047 or len(set(raw_records)) != 2047:
        raise PortableCoreError("extension raw coverage differs")
    canonical_records = canonicalize_graph6(raw_records, labelg_path)
    multiplicities = Counter(canonical_records)
    if len(multiplicities) != 623 or sum(multiplicities.values()) != 2047:
        raise PortableCoreError("extension canonical counts differ")

    parameter_counts: Counter[tuple[int, int]] = Counter()
    rank_counts: Counter[int] = Counter()
    rows: list[dict[str, object]] = []
    deep_keys: list[str] = []
    for record in sorted(multiplicities):
        graph = KernelGraph.from_graph6(record)
        gamma = domination_number(graph)
        alpha = independence_number(graph)
        parameter_counts[(gamma, alpha)] += 1
        earliest: int | str = ""
        latest: int | str = ""
        full_depth: int | str = ""
        if gamma == alpha == 3:
            profile = kernel_profile(graph, 3)
            independent = maximum_independent_states(graph, 3)
            ranks = tuple(profile.deletion_rank[state] for state in independent)
            earliest = min(ranks)
            latest = max(ranks)
            full_depth = profile.full_deletion_depth
            if full_depth is None:
                raise PortableCoreError(
                    "J extension unexpectedly has an eternal 3-family"
                )
            rank_counts[int(earliest)] += 1
            if earliest >= 5:
                deep_keys.append(record)
        rows.append(
            {
                "canonical_graph6": record,
                "n": graph.order,
                "m": graph.size,
                "origin_count": multiplicities[record],
                "gamma": gamma,
                "alpha": alpha,
                "earliest_forced_rank": earliest,
                "latest_forced_rank": latest,
                "full_kernel_deletion_depth": full_depth,
            }
        )

    if dict(parameter_counts) != EXPECTED_EXTENSION_PARAMETER_COUNTS:
        raise PortableCoreError("extension parameter histogram differs")
    if dict(rank_counts) != EXPECTED_EXTENSION_RANK_COUNTS:
        raise PortableCoreError("extension rank histogram differs")
    if tuple(sorted(deep_keys)) != EXPECTED_DEEP_EXTENSION_KEYS:
        raise PortableCoreError("deep extension keys differ")

    origin_stream = "".join(
        f"{index}\t{record}\t{canonical}\n"
        for index, (record, canonical) in enumerate(
            zip(raw_records, canonical_records), start=1
        )
    ).encode("ascii")
    summary = {
        "claim_classification": "OBSERVED",
        "base_graph6": J_GRAPH6,
        "base_graph6_sha256": graph6_sha256(J_GRAPH6),
        "raw_nonempty_neighborhood_count": len(raw_records),
        "reported_canonical_class_count": len(multiplicities),
        "canonical_multiplicity_sum": sum(multiplicities.values()),
        "canonical_multiplicity_histogram": {
            str(key): value
            for key, value in sorted(
                Counter(multiplicities.values()).items()
            )
        },
        "parameter_histogram_fields": ["gamma", "alpha"],
        "parameter_histogram": [
            {"values": list(key), "count": value}
            for key, value in sorted(parameter_counts.items())
        ],
        "gamma_alpha_3_class_count": sum(rank_counts.values()),
        "earliest_forced_rank_histogram": {
            str(key): value for key, value in sorted(rank_counts.items())
        },
        "deep_extension_graph6": sorted(deep_keys),
        "origin_to_key_stream_sha256": sha256(origin_stream).hexdigest(),
        "limitations": [
            "labelg supplies the unmarked canonical keys",
            (
                "the checker verifies every raw-to-key isomorphism but does "
                "not independently derive canonical normal forms or prove "
                "that distinct reported keys are nonisomorphic"
            ),
            "this is a one-vertex-extension slice over one fixed graph",
        ],
    }
    return tuple(rows), summary


def extension_csv_bytes(rows: Sequence[Mapping[str, object]]) -> bytes:
    lines = [",".join(EXTENSION_COLUMNS)]
    for row in rows:
        fields: list[str] = []
        for column in EXTENSION_COLUMNS:
            value = row[column]
            text = str(value)
            if any(character in text for character in ',\"\r\n'):
                text = '"' + text.replace('"', '""') + '"'
            fields.append(text)
        lines.append(",".join(fields))
    return ("\n".join(lines) + "\n").encode("ascii")


def read_extension_csv(path: Path) -> tuple[dict[str, object], ...]:
    rows: list[dict[str, object]] = []
    with path.open(newline="", encoding="ascii") as handle:
        reader = csv.DictReader(handle)
        if tuple(reader.fieldnames or ()) != EXTENSION_COLUMNS:
            raise PortableCoreError("extension CSV header differs")
        previous: str | None = None
        for raw in reader:
            if (
                None in raw
                or set(raw) != set(EXTENSION_COLUMNS)
                or any(value is None for value in raw.values())
            ):
                raise PortableCoreError(
                    "extension CSV row has missing or surplus fields"
                )
            record = raw["canonical_graph6"]
            if previous is not None and record <= previous:
                raise PortableCoreError("extension CSV keys are not increasing")
            previous = record
            row: dict[str, object] = {"canonical_graph6": record}
            for field in ("n", "m", "origin_count", "gamma", "alpha"):
                text = raw[field]
                if not text.isascii() or not text.isdecimal():
                    raise PortableCoreError(
                        f"extension CSV {field} is not canonical integer text"
                    )
                row[field] = int(text)
            for field in (
                "earliest_forced_rank",
                "latest_forced_rank",
                "full_kernel_deletion_depth",
            ):
                text = raw[field]
                if text == "":
                    row[field] = ""
                elif text.isascii() and text.isdecimal():
                    row[field] = int(text)
                else:
                    raise PortableCoreError(
                        f"extension CSV {field} is malformed"
                    )
            rows.append(row)
    return tuple(rows)


def _read_source_population(campaign_root: Path) -> tuple[tuple[str, int], ...]:
    certificate_path = (
        campaign_root / "certificates/k3_three_step_edge_toggle.ndjson"
    )
    shallow: list[tuple[str, int]] = []
    header_seen = False
    trailer_seen = False
    with certificate_path.open(encoding="ascii") as handle:
        for line_index, line in enumerate(handle):
            try:
                value = json.loads(line, object_pairs_hook=_strict_object)
            except json.JSONDecodeError as error:
                raise PortableCoreError(
                    f"invalid source certificate line {line_index + 1}"
                ) from error
            if not isinstance(value, dict):
                raise PortableCoreError("source certificate row is not object")
            kind = value.get("type")
            if kind == "header":
                if header_seen or shallow or trailer_seen:
                    raise PortableCoreError("source header position differs")
                header_seen = True
            elif kind == "row":
                if not header_seen or trailer_seen:
                    raise PortableCoreError("source row position differs")
                record = value.get("graph6")
                if not isinstance(record, str):
                    raise PortableCoreError("source row graph6 is not text")
                KernelGraph.from_graph6(record)
                shallow.append((record, 3))
            elif kind == "trailer":
                if not header_seen or trailer_seen:
                    raise PortableCoreError("source trailer position differs")
                trailer_seen = True
            else:
                raise PortableCoreError("unknown source certificate row type")
    if not header_seen or not trailer_seen or len(shallow) != 518:
        raise PortableCoreError("source certificate population differs")

    measurement_path = (
        campaign_root / "results/three_step_kernel_measurement.json"
    )
    measurement = strict_json_load(measurement_path)
    if not isinstance(measurement, dict):
        raise PortableCoreError("three-step measurement is not an object")
    try:
        deep_rows = measurement["population"]["deep_rows"]
    except (KeyError, TypeError) as error:
        raise PortableCoreError("deep-row source schema differs") from error
    if not isinstance(deep_rows, list) or len(deep_rows) != 8:
        raise PortableCoreError("deep-row source count differs")
    deep: list[tuple[str, int]] = []
    for row in deep_rows:
        if not isinstance(row, dict):
            raise PortableCoreError("deep row is not an object")
        record = row.get("graph6")
        rank = row.get("earliest_forced_rank")
        if not isinstance(record, str) or type(rank) is not int:
            raise PortableCoreError("deep-row field type differs")
        KernelGraph.from_graph6(record)
        deep.append((record, rank))

    population = tuple(sorted(shallow + deep))
    if len(population) != 526 or len({record for record, _ in population}) != 526:
        raise PortableCoreError("combined source population differs")
    return population


def _find_J_embeddings(record: str) -> tuple[dict[str, object], ...]:
    base = AuditGraph.from_graph6(J_GRAPH6)
    host = AuditGraph.from_graph6(record)
    embeddings: list[dict[str, object]] = []
    if host.order == base.order:
        mapping = find_isomorphism(base, host)
        if mapping is not None:
            embeddings.append(
                {
                    "deleted_vertex": None,
                    "base_to_host": list(mapping),
                }
            )
        return tuple(embeddings)
    if host.order != base.order + 1:
        return ()
    for deleted in range(host.order):
        keep = tuple(
            vertex for vertex in range(host.order) if vertex != deleted
        )
        subgraph = induced_audit_graph(host, keep)
        sub_mapping = find_isomorphism(base, subgraph)
        if sub_mapping is None:
            continue
        embeddings.append(
            {
                "deleted_vertex": deleted,
                "base_to_host": [keep[image] for image in sub_mapping],
            }
        )
    return tuple(embeddings)


def _occurrence_summary(campaign_root: Path) -> dict[str, object]:
    population = _read_source_population(campaign_root)
    occurrences: list[dict[str, object]] = []
    rank_counts: Counter[int] = Counter()
    for record, rank in population:
        embeddings = _find_J_embeddings(record)
        if not embeddings:
            continue
        occurrences.append(
            {
                "graph6": record,
                "graph6_sha256": graph6_sha256(record),
                "earliest_forced_rank": rank,
                "embeddings": list(embeddings),
            }
        )
        rank_counts[rank] += 1
    if len(occurrences) != 37 or rank_counts != Counter({3: 30, 5: 7}):
        raise PortableCoreError("J occurrence count differs")

    deep = tuple(
        sorted(
            (record, rank)
            for record, rank in population
            if rank > 3
        )
    )
    expected_deep = tuple(
        sorted(
            ((J_GRAPH6, 5),)
            + tuple((spec.host_graph6, 5) for spec in EMBEDDING_SPECS)
            + ((Q_GRAPH6, 6),)
        )
    )
    if deep != expected_deep:
        raise PortableCoreError("deep-tail core classification differs")

    return {
        "claim_classification": "CERTIFIED-FINITE",
        "population_size": len(population),
        "population_scope": (
            "the fixed 526 K2 survivors in the recorded edge-toggle "
            "near-miss population; not all graphs of orders 11 or 12"
        ),
        "induced_J_occurrence_count": len(occurrences),
        "occurrence_earliest_rank_histogram": {
            str(key): value for key, value in sorted(rank_counts.items())
        },
        "occurrences": occurrences,
        "deep_tail": [
            {
                "graph6": record,
                "earliest_forced_rank": rank,
                "portable_core": (
                    "Q" if record == Q_GRAPH6 else "J"
                ),
            }
            for record, rank in deep
        ],
    }


def _certificate_payload(campaign_root: Path) -> dict[str, object]:
    source_rows = source_manifest(campaign_root, RUNTIME_SOURCE_PATHS)
    support_rows = source_manifest(campaign_root, SUPPORTING_ARTIFACT_PATHS)
    cores = [_core_certificate(J_GRAPH6), _core_certificate(Q_GRAPH6)]
    embeddings = [_embedding_record(spec) for spec in EMBEDDING_SPECS]
    return {
        "format": CERTIFICATE_FORMAT,
        "model": {
            "attacks": "unoccupied vertices only",
            "movement": "exactly one guard along one edge",
            "configuration_requirement": "every retained state dominates",
        },
        "claim_classification": "CERTIFIED-FINITE",
        "theorem_dependency": (
            "math/lemmas/portable_failure_core.md, Theorem 3 and Lemma 6"
        ),
        "bindings": {
            "runtime_source_manifest": list(source_rows),
            "runtime_source_set_sha256": object_sha256(source_rows),
            "supporting_artifact_manifest": list(support_rows),
            "supporting_artifact_set_sha256": object_sha256(support_rows),
        },
        "cores": cores,
        "J_induced_embeddings": embeddings,
    }


def _result_payload(
    campaign_root: Path,
    certificate_path: Path,
    extension_path: Path,
    extension_summary: Mapping[str, object],
    occurrence_summary: Mapping[str, object],
    labelg_path: Path,
) -> dict[str, object]:
    source_rows = source_manifest(campaign_root, RUNTIME_SOURCE_PATHS)
    support_rows = source_manifest(campaign_root, SUPPORTING_ARTIFACT_PATHS)
    input_rows = source_manifest(campaign_root, INPUT_PATHS)
    return {
        "format": RESULT_FORMAT,
        "status": "complete",
        "claim_classification": {
            "portable_failure_core_theorems": "PROVED",
            "core_profiles_ranked_DAGs_and_embeddings": "CERTIFIED-FINITE",
            "J_occurrences_in_fixed_526_population": "CERTIFIED-FINITE",
            "J_one_vertex_unmarked_class_measurement": "OBSERVED",
        },
        "bindings": {
            "runtime_source_manifest": list(source_rows),
            "runtime_source_set_sha256": object_sha256(source_rows),
            "supporting_artifact_manifest": list(support_rows),
            "supporting_artifact_set_sha256": object_sha256(support_rows),
            "input_manifest": list(input_rows),
            "input_set_sha256": object_sha256(input_rows),
            "certificate_path": str(
                certificate_path.relative_to(campaign_root)
            ),
            "certificate_sha256": sha256_file(certificate_path),
            "extension_table_path": str(
                extension_path.relative_to(campaign_root)
            ),
            "extension_table_sha256": sha256_file(extension_path),
            "labelg_path": str(labelg_path.relative_to(campaign_root)),
            "labelg_sha256": verify_labelg(labelg_path),
            "nauty_archive_sha256": NAUTY_ARCHIVE_SHA256,
        },
        "core_summary": {
            "J": {
                "graph6": J_GRAPH6,
                "kernel_sizes_3": list(
                    EXPECTED_CORE_DATA[J_GRAPH6]["kernel_3"]
                ),
                "root_rank": 5,
                "ranked_DAG_nodes": 17,
            },
            "Q": {
                "graph6": Q_GRAPH6,
                "kernel_sizes_3": list(
                    EXPECTED_CORE_DATA[Q_GRAPH6]["kernel_3"]
                ),
                "root_rank": 6,
                "ranked_DAG_nodes": 20,
            },
            "deep_rows_explained_by_J": 7,
            "deep_rows_explained_by_Q": 1,
        },
        "fixed_population": dict(occurrence_summary),
        "J_one_vertex_extensions": dict(extension_summary),
        "limitations": [
            "the two portable-core theorems do not resolve the conjecture",
            (
                "the 526-row occurrence claim concerns a fixed derived "
                "edge-toggle population"
            ),
            (
                "the 623-key one-vertex-extension result remains OBSERVED "
                "because canonical-key distinctness has no independent "
                "normal-form proof"
            ),
        ],
    }


def generate_artifacts(
    *,
    campaign_root: Path,
    certificate_path: Path,
    result_path: Path,
    extension_path: Path,
    labelg_path: Path,
) -> dict[str, str]:
    campaign_root = campaign_root.resolve()
    certificate_path = certificate_path.resolve()
    result_path = result_path.resolve()
    extension_path = extension_path.resolve()
    labelg_path = labelg_path.resolve()
    for path in (certificate_path, result_path, extension_path):
        if campaign_root not in path.parents:
            raise PortableCoreError("output path is outside campaign root")
    verify_labelg(labelg_path)

    certificate = _certificate_payload(campaign_root)
    atomic_json(certificate_path, certificate)

    extension_rows, extension_summary = _extension_rows(labelg_path)
    atomic_bytes(extension_path, extension_csv_bytes(extension_rows))

    occurrence_summary = _occurrence_summary(campaign_root)
    result = _result_payload(
        campaign_root,
        certificate_path,
        extension_path,
        extension_summary,
        occurrence_summary,
        labelg_path,
    )
    atomic_json(result_path, result)
    return {
        "certificate_sha256": sha256_file(certificate_path),
        "extension_table_sha256": sha256_file(extension_path),
        "result_sha256": sha256_file(result_path),
    }


def _audit_state(state: object, order: int) -> frozenset[int]:
    if (
        not isinstance(state, list)
        or len(state) != GUARD_COUNT
        or any(type(vertex) is not int for vertex in state)
        or len(set(state)) != GUARD_COUNT
        or any(not 0 <= vertex < order for vertex in state)
        or state != sorted(state)
    ):
        raise PortableCoreError("configuration is not a canonical 3-set")
    return frozenset(state)


def _audit_dominates(graph: AuditGraph, state: frozenset[int]) -> bool:
    return all(
        vertex in state
        or any(graph.neighbors[vertex] & (1 << guard) for guard in state)
        for vertex in range(graph.order)
    )


def _audit_independent(graph: AuditGraph, state: frozenset[int]) -> bool:
    return all(
        not graph.neighbors[first] & (1 << second)
        for first, second in combinations(sorted(state), 2)
    )


def _audit_kernel_levels(
    graph: AuditGraph, cardinality: int
) -> tuple[tuple[frozenset[frozenset[int]], ...], frozenset[frozenset[int]]]:
    configurations = frozenset(
        frozenset(vertices)
        for vertices in combinations(range(graph.order), cardinality)
        if _audit_dominates(graph, frozenset(vertices))
    )
    levels = [configurations]
    active = configurations
    while active:
        following: set[frozenset[int]] = set()
        for state in configurations:
            for attacked in range(graph.order):
                if attacked in state:
                    continue
                responses = (
                    (state - {guard}) | {attacked}
                    for guard in state
                    if graph.neighbors[attacked] & (1 << guard)
                )
                if not any(response in active for response in responses):
                    break
            else:
                following.add(state)
        frozen = frozenset(following)
        levels.append(frozen)
        if frozen == active:
            return tuple(levels), frozen
        active = frozen
    return tuple(levels), frozenset()


def _audit_gamma(graph: AuditGraph) -> int:
    for cardinality in range(graph.order + 1):
        if any(
            _audit_dominates(graph, frozenset(vertices))
            for vertices in combinations(range(graph.order), cardinality)
        ):
            return cardinality
    raise AssertionError("the full vertex set dominates")


def _audit_alpha(graph: AuditGraph) -> int:
    for cardinality in range(graph.order, -1, -1):
        if any(
            _audit_independent(graph, frozenset(vertices))
            for vertices in combinations(range(graph.order), cardinality)
        ):
            return cardinality
    raise AssertionError("the empty set is independent")


def _verify_ranked_dag(
    graph: AuditGraph,
    core: Mapping[str, object],
) -> dict[str, int]:
    root = _audit_state(core.get("root"), graph.order)
    if not _audit_independent(graph, root):
        raise PortableCoreError("ranked-DAG root is not independent")
    rows = core.get("ranked_attack_dag")
    if not isinstance(rows, list) or not rows:
        raise PortableCoreError("ranked attack DAG is empty")

    records: dict[frozenset[int], dict[str, object]] = {}
    for row in rows:
        if not isinstance(row, dict) or set(row) != {
            "configuration",
            "rank",
            "attack",
            "responses",
        }:
            raise PortableCoreError("ranked-DAG row schema differs")
        state = _audit_state(row["configuration"], graph.order)
        if state in records:
            raise PortableCoreError("duplicate ranked-DAG configuration")
        if not _audit_dominates(graph, state):
            raise PortableCoreError("ranked-DAG state does not dominate")
        rank = row["rank"]
        attacked = row["attack"]
        if (
            type(rank) is not int
            or rank < 1
            or type(attacked) is not int
            or not 0 <= attacked < graph.order
            or attacked in state
            or not isinstance(row["responses"], list)
        ):
            raise PortableCoreError("ranked-DAG rank or attack is invalid")
        records[state] = row
    if root not in records:
        raise PortableCoreError("ranked-DAG root is absent")
    if records[root]["rank"] != core.get("root_rank"):
        raise PortableCoreError("ranked-DAG root rank differs")

    terminal_states: dict[frozenset[int], int] = {}
    arcs: dict[frozenset[int], tuple[frozenset[int] | None, ...]] = {}
    for state, row in records.items():
        attacked = int(row["attack"])
        expected_guards = tuple(
            guard
            for guard in sorted(state)
            if graph.neighbors[attacked] & (1 << guard)
        )
        responses = row["responses"]
        assert isinstance(responses, list)
        if len(responses) != len(expected_guards):
            raise PortableCoreError("ranked-DAG response count differs")
        response_guards: list[int] = []
        targets: list[frozenset[int] | None] = []
        for response in responses:
            if not isinstance(response, dict):
                raise PortableCoreError("ranked-DAG response is not object")
            fields = set(response)
            if fields not in (
                {"guard", "successor", "undominated"},
                {"guard", "successor", "successor_rank"},
            ):
                raise PortableCoreError("ranked-DAG response schema differs")
            guard = response["guard"]
            if type(guard) is not int:
                raise PortableCoreError("response guard is not an integer")
            response_guards.append(guard)
            successor_state = _audit_state(response["successor"], graph.order)
            expected_successor = (state - {guard}) | {attacked}
            if successor_state != expected_successor:
                raise PortableCoreError("ranked-DAG successor differs")
            if "undominated" in response:
                witness = response["undominated"]
                if (
                    type(witness) is not int
                    or not 0 <= witness < graph.order
                    or witness in successor_state
                    or any(
                        graph.neighbors[witness] & (1 << occupied)
                        for occupied in successor_state
                    )
                    or _audit_dominates(graph, successor_state)
                ):
                    raise PortableCoreError("terminal witness is invalid")
                prior = terminal_states.setdefault(successor_state, witness)
                if prior != witness:
                    raise PortableCoreError(
                        "terminal state has inconsistent witnesses"
                    )
                targets.append(None)
            else:
                target = records.get(successor_state)
                if target is None:
                    raise PortableCoreError("successor state is not listed")
                successor_rank = response["successor_rank"]
                if (
                    type(successor_rank) is not int
                    or successor_rank != target["rank"]
                    or successor_rank >= row["rank"]
                ):
                    raise PortableCoreError("rank does not strictly decrease")
                targets.append(successor_state)
        if tuple(response_guards) != expected_guards:
            raise PortableCoreError("response guards are not exhaustive/sorted")
        arcs[state] = tuple(targets)

    reached: set[frozenset[int]] = set()

    def visit(state: frozenset[int]) -> None:
        if state in reached:
            return
        reached.add(state)
        for target in arcs[state]:
            if target is not None:
                visit(target)

    visit(root)
    if reached != set(records):
        raise PortableCoreError("ranked-DAG contains unreachable attack states")

    @lru_cache(maxsize=None)
    def unrolled(state: frozenset[int]) -> tuple[int, int, int]:
        child_costs: list[tuple[int, int, int]] = []
        for target in arcs[state]:
            if target is None:
                child_costs.append((1, 1, 0))
            else:
                child_costs.append(unrolled(target))
        return (
            1 + sum(cost[0] for cost in child_costs),
            sum(cost[1] for cost in child_costs),
            1 + max((cost[2] for cost in child_costs), default=-1),
        )

    tree_nodes, tree_leaves, tree_depth = unrolled(root)
    return {
        "attack_states": len(records),
        "distinct_terminal_states": len(terminal_states),
        "dag_nodes": len(records) + len(terminal_states),
        "unrolled_tree_nodes": tree_nodes,
        "unrolled_tree_leaves": tree_leaves,
        "unrolled_tree_depth": tree_depth,
    }


def _verify_core(
    core: object,
    expected_record: str,
) -> None:
    if not isinstance(core, dict) or set(core) != {
        "id",
        "graph6",
        "graph6_sha256",
        "order",
        "size",
        "guard_count",
        "gamma",
        "alpha",
        "gamma_infinity",
        "kernel_sizes",
        "root",
        "root_rank",
        "ranked_attack_dag",
        "statistics",
    }:
        raise PortableCoreError("core certificate schema differs")
    expected = EXPECTED_CORE_DATA[expected_record]
    if (
        core["id"] != expected["id"]
        or core["graph6"] != expected_record
        or core["graph6_sha256"] != graph6_sha256(expected_record)
        or core["order"] != expected["order"]
        or core["size"] != expected["size"]
        or core["guard_count"] != 3
        or core["gamma"] != 3
        or core["alpha"] != 3
        or core["gamma_infinity"] != 4
        or core["root"] != list(expected["root"])
    ):
        raise PortableCoreError("core fixed metadata differs")
    graph = AuditGraph.from_graph6(expected_record)
    if (
        graph.order != expected["order"]
        or graph.size != expected["size"]
        or _audit_gamma(graph) != 3
        or _audit_alpha(graph) != 3
    ):
        raise PortableCoreError("independent core parameters differ")
    levels_3, stable_3 = _audit_kernel_levels(graph, 3)
    levels_4, stable_4 = _audit_kernel_levels(graph, 4)
    if (
        tuple(len(level) for level in levels_3) != expected["kernel_3"]
        or tuple(len(level) for level in levels_4) != expected["kernel_4"]
        or stable_3
        or not stable_4
        or core["kernel_sizes"]
        != {
            "3": list(expected["kernel_3"]),
            "4": list(expected["kernel_4"]),
        }
    ):
        raise PortableCoreError("independent kernel profile differs")

    statistics = _verify_ranked_dag(graph, core)
    if core["statistics"] != statistics:
        raise PortableCoreError("ranked-DAG statistics differ")
    root = frozenset(expected["root"])
    deletion_rank: int | None = None
    for index, level in enumerate(levels_3):
        if root not in level:
            deletion_rank = index
            break
    if deletion_rank != core["root_rank"]:
        raise PortableCoreError("root deletion rank differs")
    for row in core["ranked_attack_dag"]:
        state = _audit_state(row["configuration"], graph.order)
        exact_rank: int | None = None
        for index, level in enumerate(levels_3):
            if state not in level:
                exact_rank = index
                break
        if exact_rank != row["rank"]:
            raise PortableCoreError(
                "ranked-DAG state rank differs from exact kernel rank"
            )


def _verify_embedding(value: object, spec: EmbeddingSpec) -> None:
    if not isinstance(value, dict) or set(value) != {
        "host_graph6",
        "host_graph6_sha256",
        "host_order",
        "host_size",
        "deleted_vertex",
        "base_to_host",
        "extension_neighborhood_in_J_labels",
        "extension_kind",
        "reference_vertex_in_J",
        "extra_neighbor_in_J",
        "embedding_sha256",
    }:
        raise PortableCoreError("embedding certificate schema differs")
    digest_payload = dict(value)
    claimed_digest = digest_payload.pop("embedding_sha256")
    if claimed_digest != object_sha256(digest_payload):
        raise PortableCoreError("embedding digest differs")
    if (
        value["host_graph6"] != spec.host_graph6
        or value["host_graph6_sha256"]
        != graph6_sha256(spec.host_graph6)
        or value["deleted_vertex"] != spec.deleted_vertex
        or value["base_to_host"] != list(spec.base_to_host)
        or value["extension_kind"] != spec.extension_kind
        or value["reference_vertex_in_J"] != spec.reference_vertex
        or value["extra_neighbor_in_J"] != spec.extra_neighbor
    ):
        raise PortableCoreError("embedding fixed data differs")
    regenerated = _embedding_record(spec)
    if value != regenerated:
        raise PortableCoreError("embedding direct replay differs")


def verify_certificate(
    value: object, *, campaign_root: Path
) -> None:
    if not isinstance(value, dict) or set(value) != {
        "format",
        "model",
        "claim_classification",
        "theorem_dependency",
        "bindings",
        "cores",
        "J_induced_embeddings",
    }:
        raise PortableCoreError("certificate top-level schema differs")
    if (
        value["format"] != CERTIFICATE_FORMAT
        or value["claim_classification"] != "CERTIFIED-FINITE"
        or value["theorem_dependency"]
        != "math/lemmas/portable_failure_core.md, Theorem 3 and Lemma 6"
        or value["model"]
        != {
            "attacks": "unoccupied vertices only",
            "movement": "exactly one guard along one edge",
            "configuration_requirement": "every retained state dominates",
        }
    ):
        raise PortableCoreError("certificate header differs")
    bindings = value["bindings"]
    if not isinstance(bindings, dict) or set(bindings) != {
        "runtime_source_manifest",
        "runtime_source_set_sha256",
        "supporting_artifact_manifest",
        "supporting_artifact_set_sha256",
    }:
        raise PortableCoreError("certificate bindings schema differs")
    sources = validate_source_manifest(
        bindings["runtime_source_manifest"],
        campaign_root=campaign_root,
        expected_paths=RUNTIME_SOURCE_PATHS,
    )
    support = validate_source_manifest(
        bindings["supporting_artifact_manifest"],
        campaign_root=campaign_root,
        expected_paths=SUPPORTING_ARTIFACT_PATHS,
    )
    if (
        bindings["runtime_source_set_sha256"] != object_sha256(sources)
        or bindings["supporting_artifact_set_sha256"]
        != object_sha256(support)
    ):
        raise PortableCoreError("certificate manifest-set digest differs")
    cores = value["cores"]
    embeddings = value["J_induced_embeddings"]
    if (
        not isinstance(cores, list)
        or len(cores) != 2
        or not isinstance(embeddings, list)
        or len(embeddings) != len(EMBEDDING_SPECS)
    ):
        raise PortableCoreError("certificate row count differs")
    _verify_core(cores[0], J_GRAPH6)
    _verify_core(cores[1], Q_GRAPH6)
    for row, spec in zip(embeddings, EMBEDDING_SPECS):
        _verify_embedding(row, spec)


def _audit_extension_rows(
    rows: Sequence[Mapping[str, object]],
    *,
    labelg_path: Path,
) -> dict[str, object]:
    generated_rows, summary = _extension_rows(labelg_path)
    if tuple(rows) != generated_rows:
        raise PortableCoreError("extension CSV differs from exact replay")

    base = AuditGraph.from_graph6(J_GRAPH6)
    raw_graphs = tuple(
        AuditGraph.from_graph6(
            extend_kernel_graph(
                KernelGraph.from_graph6(J_GRAPH6), neighborhood
            ).to_graph6()
        )
        for neighborhood in range(1, 1 << base.order)
    )
    row_by_key = {
        str(row["canonical_graph6"]): row for row in generated_rows
    }
    raw_records = tuple(graph.to_graph6() for graph in raw_graphs)
    canonical_records = canonicalize_graph6(raw_records, labelg_path)
    for index, (raw, key) in enumerate(
        zip(raw_graphs, canonical_records), start=1
    ):
        canonical = AuditGraph.from_graph6(key)
        if find_isomorphism(raw, canonical) is None:
            raise PortableCoreError(
                f"extension origin {index} is nonisomorphic to its key"
            )
        if key not in row_by_key:
            raise PortableCoreError("extension key is absent from CSV")

    for row in generated_rows:
        graph = AuditGraph.from_graph6(str(row["canonical_graph6"]))
        if (
            graph.order != row["n"]
            or graph.size != row["m"]
            or _audit_gamma(graph) != row["gamma"]
            or _audit_alpha(graph) != row["alpha"]
        ):
            raise PortableCoreError("extension independent parameters differ")
        if row["gamma"] == row["alpha"] == 3:
            levels, stable = _audit_kernel_levels(graph, 3)
            independent = tuple(
                state
                for state in levels[0]
                if _audit_independent(graph, state)
            )
            ranks: list[int] = []
            for state in independent:
                for rank, level in enumerate(levels):
                    if state not in level:
                        ranks.append(rank)
                        break
                else:
                    raise PortableCoreError(
                        "extension independent state survives eternally"
                    )
            if (
                stable
                or min(ranks) != row["earliest_forced_rank"]
                or max(ranks) != row["latest_forced_rank"]
                or len(levels) - 1
                != row["full_kernel_deletion_depth"]
            ):
                raise PortableCoreError(
                    "extension independent kernel data differs"
                )
    return summary


def verify_result(
    value: object,
    *,
    campaign_root: Path,
    certificate_path: Path,
    extension_path: Path,
    labelg_path: Path,
) -> None:
    if not isinstance(value, dict) or set(value) != {
        "format",
        "status",
        "claim_classification",
        "bindings",
        "core_summary",
        "fixed_population",
        "J_one_vertex_extensions",
        "limitations",
    }:
        raise PortableCoreError("result top-level schema differs")
    if value["format"] != RESULT_FORMAT or value["status"] != "complete":
        raise PortableCoreError("result header differs")
    expected_classification = {
        "portable_failure_core_theorems": "PROVED",
        "core_profiles_ranked_DAGs_and_embeddings": "CERTIFIED-FINITE",
        "J_occurrences_in_fixed_526_population": "CERTIFIED-FINITE",
        "J_one_vertex_unmarked_class_measurement": "OBSERVED",
    }
    if value["claim_classification"] != expected_classification:
        raise PortableCoreError("result claim classification differs")

    bindings = value["bindings"]
    if not isinstance(bindings, dict) or set(bindings) != {
        "runtime_source_manifest",
        "runtime_source_set_sha256",
        "supporting_artifact_manifest",
        "supporting_artifact_set_sha256",
        "input_manifest",
        "input_set_sha256",
        "certificate_path",
        "certificate_sha256",
        "extension_table_path",
        "extension_table_sha256",
        "labelg_path",
        "labelg_sha256",
        "nauty_archive_sha256",
    }:
        raise PortableCoreError("result bindings schema differs")
    sources = validate_source_manifest(
        bindings["runtime_source_manifest"],
        campaign_root=campaign_root,
        expected_paths=RUNTIME_SOURCE_PATHS,
    )
    support = validate_source_manifest(
        bindings["supporting_artifact_manifest"],
        campaign_root=campaign_root,
        expected_paths=SUPPORTING_ARTIFACT_PATHS,
    )
    inputs = validate_source_manifest(
        bindings["input_manifest"],
        campaign_root=campaign_root,
        expected_paths=INPUT_PATHS,
    )
    if (
        bindings["runtime_source_set_sha256"] != object_sha256(sources)
        or bindings["supporting_artifact_set_sha256"]
        != object_sha256(support)
        or bindings["input_set_sha256"] != object_sha256(inputs)
        or bindings["certificate_sha256"] != sha256_file(certificate_path)
        or bindings["extension_table_sha256"] != sha256_file(extension_path)
        or bindings["labelg_sha256"] != verify_labelg(labelg_path)
        or bindings["nauty_archive_sha256"] != NAUTY_ARCHIVE_SHA256
        or campaign_root / bindings["certificate_path"]
        != certificate_path.resolve()
        or campaign_root / bindings["extension_table_path"]
        != extension_path.resolve()
        or campaign_root / bindings["labelg_path"] != labelg_path.resolve()
    ):
        raise PortableCoreError("result binding differs")

    expected_core_summary = _result_payload(
        campaign_root,
        certificate_path,
        extension_path,
        value["J_one_vertex_extensions"],
        value["fixed_population"],
        labelg_path,
    )["core_summary"]
    if value["core_summary"] != expected_core_summary:
        raise PortableCoreError("result core summary differs")

    occurrence = _occurrence_summary(campaign_root)
    if value["fixed_population"] != occurrence:
        raise PortableCoreError("result occurrence summary differs")
    extension_rows = read_extension_csv(extension_path)
    extension_summary = _audit_extension_rows(
        extension_rows, labelg_path=labelg_path
    )
    if extension_path.read_bytes() != extension_csv_bytes(extension_rows):
        raise PortableCoreError("extension CSV bytes are not canonical")
    if value["J_one_vertex_extensions"] != extension_summary:
        raise PortableCoreError("result extension summary differs")
    expected = _result_payload(
        campaign_root,
        certificate_path,
        extension_path,
        extension_summary,
        occurrence,
        labelg_path,
    )
    if value != expected:
        raise PortableCoreError("result payload differs from exact replay")


def audit_artifacts(
    *,
    campaign_root: Path,
    certificate_path: Path,
    result_path: Path,
    extension_path: Path,
    labelg_path: Path,
) -> dict[str, str]:
    campaign_root = campaign_root.resolve()
    certificate_path = certificate_path.resolve()
    result_path = result_path.resolve()
    extension_path = extension_path.resolve()
    labelg_path = labelg_path.resolve()
    certificate = strict_json_load(certificate_path)
    verify_certificate(certificate, campaign_root=campaign_root)
    result = strict_json_load(result_path)
    verify_result(
        result,
        campaign_root=campaign_root,
        certificate_path=certificate_path,
        extension_path=extension_path,
        labelg_path=labelg_path,
    )
    return {
        "certificate_sha256": sha256_file(certificate_path),
        "extension_table_sha256": sha256_file(extension_path),
        "result_sha256": sha256_file(result_path),
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "action",
        choices=("generate", "audit"),
        help="write deterministic artifacts or replay them",
    )
    parser.add_argument(
        "--campaign-root",
        type=Path,
        default=CAMPAIGN_ROOT,
    )
    parser.add_argument(
        "--certificate",
        type=Path,
        default=CAMPAIGN_ROOT
        / "certificates/portable_failure_cores.json",
    )
    parser.add_argument(
        "--result",
        type=Path,
        default=CAMPAIGN_ROOT
        / "results/portable_failure_core_measurement.json",
    )
    parser.add_argument(
        "--extension-table",
        type=Path,
        default=CAMPAIGN_ROOT
        / "results/portable_failure_core_J_extensions.csv",
    )
    parser.add_argument(
        "--labelg",
        type=Path,
        default=CAMPAIGN_ROOT / "tools/nauty2_9_3/labelg",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    arguments = build_parser().parse_args(argv)
    kwargs = {
        "campaign_root": arguments.campaign_root,
        "certificate_path": arguments.certificate,
        "result_path": arguments.result,
        "extension_path": arguments.extension_table,
        "labelg_path": arguments.labelg,
    }
    if arguments.action == "generate":
        hashes = generate_artifacts(**kwargs)
    else:
        hashes = audit_artifacts(**kwargs)
    print(
        json.dumps(
            {"action": arguments.action, "status": "passed", **hashes},
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
