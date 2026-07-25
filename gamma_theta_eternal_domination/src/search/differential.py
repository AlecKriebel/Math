"""Deterministic, resumable differential testing of verifiers A and B."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import random
import resource
import tempfile
import time
from collections.abc import Iterator
from itertools import combinations
from pathlib import Path

from verifier_a.core import (
    BitGraph,
    alpha,
    domination_number,
    eternal_domination_number,
    eternal_fixed_point,
    independent_domination_number,
    theta,
)
from verifier_b import (
    Graph,
    clique_cover_number,
    domination_number as domination_number_b,
    eternal_domination_decision,
    eternal_domination_number as eternal_domination_number_b,
    find_eternal_family,
    independence_number,
    independent_domination_number as independent_domination_number_b,
)


def _all_labeled_records(max_order: int) -> Iterator[tuple[str, str]]:
    for order in range(max_order + 1):
        edges = tuple(combinations(range(order), 2))
        for code in range(1 << len(edges)):
            graph = BitGraph.from_edges(
                order,
                (
                    edge
                    for position, edge in enumerate(edges)
                    if code >> position & 1
                ),
            )
            yield ("labeled", graph.to_graph6())


def _random_records(
    count: int, minimum_order: int, maximum_order: int, seed: int
) -> Iterator[tuple[str, str]]:
    generator = random.Random(seed)
    probabilities = (0.12, 0.25, 0.4, 0.5, 0.6, 0.75, 0.88)
    for _ in range(count):
        order = generator.randint(minimum_order, maximum_order)
        probability = generator.choice(probabilities)
        edges = (
            (first, second)
            for first in range(order)
            for second in range(first + 1, order)
            if generator.random() < probability
        )
        yield ("random", BitGraph.from_edges(order, edges).to_graph6())


def _mask_as_configuration(mask: int, order: int) -> frozenset[int]:
    return frozenset(vertex for vertex in range(order) if mask >> vertex & 1)


def compare_graph(
    record: str, check_all_guard_counts: bool = True
) -> tuple[int, int, int, int, int]:
    """Return agreed parameters or raise on any disagreement."""

    graph_a = BitGraph.from_graph6(record)
    graph_b = Graph.from_graph6(record)
    if graph_a.to_graph6() != graph_b.to_graph6():
        raise AssertionError(("graph6", record))
    if tuple(
        (first, second)
        for first in range(graph_a.n)
        for second in range(first + 1, graph_a.n)
        if graph_a.adj[first] >> second & 1
    ) != tuple(graph_b.edges()):
        raise AssertionError(("edge set", record))

    parameters_a = (
        domination_number(graph_a),
        independent_domination_number(graph_a),
        alpha(graph_a),
        eternal_domination_number(graph_a),
        theta(graph_a),
    )
    parameters_b = (
        domination_number_b(graph_b),
        independent_domination_number_b(graph_b),
        independence_number(graph_b),
        eternal_domination_number_b(graph_b),
        clique_cover_number(graph_b),
    )
    if parameters_a != parameters_b:
        raise AssertionError(("parameters", record, parameters_a, parameters_b))

    if check_all_guard_counts:
        for guard_count in range(graph_a.n + 1):
            result_a = eternal_fixed_point(graph_a, guard_count)
            family_b = find_eternal_family(graph_b, guard_count)
            decision_b = eternal_domination_decision(graph_b, guard_count)
            if result_a.exists != decision_b:
                raise AssertionError(
                    ("decision", record, guard_count, result_a.exists, decision_b)
                )
            normalized_a = frozenset(
                _mask_as_configuration(mask, graph_a.n)
                for mask in result_a.family
            )
            normalized_b = family_b or frozenset()
            if normalized_a != normalized_b:
                raise AssertionError(
                    (
                        "greatest family",
                        record,
                        guard_count,
                        len(normalized_a),
                        len(normalized_b),
                    )
                )
    return parameters_a


def _atomic_json(path: Path, payload: dict[str, object]) -> None:
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
    except BaseException:
        try:
            os.unlink(temporary_name)
        except FileNotFoundError:
            pass
        raise


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--labeled-max", type=int, default=5)
    parser.add_argument("--random-count", type=int, default=1000)
    parser.add_argument("--random-min", type=int, default=6)
    parser.add_argument("--random-max", type=int, default=10)
    parser.add_argument("--seed", type=int, default=20260725)
    parser.add_argument("--checkpoint-every", type=int, default=50)
    parser.add_argument("--checkpoint", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument(
        "--optimum-only",
        action="store_true",
        help="skip comparison of greatest families at every k",
    )
    arguments = parser.parse_args()
    configuration = {
        "labeled_max": arguments.labeled_max,
        "random_count": arguments.random_count,
        "random_min": arguments.random_min,
        "random_max": arguments.random_max,
        "seed": arguments.seed,
        "check_all_guard_counts": not arguments.optimum_only,
    }

    resume_at = 0
    if arguments.checkpoint.exists():
        with arguments.checkpoint.open(encoding="utf-8") as handle:
            previous = json.load(handle)
        if previous.get("configuration") != configuration:
            raise SystemExit("checkpoint configuration does not match this run")
        if previous.get("status") == "complete":
            resume_at = 0
        else:
            resume_at = int(previous.get("processed", 0))

    cases = (
        *_all_labeled_records(arguments.labeled_max),
        *_random_records(
            arguments.random_count,
            arguments.random_min,
            arguments.random_max,
            arguments.seed,
        ),
    )
    started_wall = time.time()
    started_counter = time.perf_counter()
    digest = hashlib.sha256()
    processed = 0
    for index, (kind, record) in enumerate(cases):
        digest.update(kind.encode("ascii") + b":" + record.encode("ascii") + b"\n")
        if index < resume_at:
            processed = index + 1
            continue
        compare_graph(record, not arguments.optimum_only)
        processed = index + 1
        if processed % arguments.checkpoint_every == 0:
            _atomic_json(
                arguments.checkpoint,
                {
                    "status": "running",
                    "configuration": configuration,
                    "processed": processed,
                    "last_kind": kind,
                    "last_graph6": record,
                    "graph_stream_sha256_prefix": digest.hexdigest(),
                    "elapsed_seconds_this_process": time.perf_counter()
                    - started_counter,
                },
            )

    usage = resource.getrusage(resource.RUSAGE_SELF)
    result: dict[str, object] = {
        "status": "complete",
        "configuration": configuration,
        "processed": processed,
        "graph_stream_sha256": digest.hexdigest(),
        "started_unix": started_wall,
        "finished_unix": time.time(),
        "wall_seconds_this_process": time.perf_counter() - started_counter,
        "user_cpu_seconds_this_process": usage.ru_utime,
        "system_cpu_seconds_this_process": usage.ru_stime,
        "maximum_resident_set_size_raw": usage.ru_maxrss,
        "python": platform.python_version(),
        "platform": platform.platform(),
        "outcome": "all comparisons agreed",
    }
    _atomic_json(arguments.checkpoint, result)
    _atomic_json(arguments.output, result)
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
