"""Independently reproduce the parameters of MMV (2022), Table 9."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import platform
import resource
import tempfile
import time
from collections import Counter
from itertools import combinations
from pathlib import Path

from search.differential import compare_graph
from verifier_a.core import (
    BitGraph,
    eternal_fixed_point,
    verify_eternal_result,
)
from verifier_b import (
    Graph,
    is_dominating,
    make_eternal_certificate,
    maximum_independent_set,
    minimum_dominating_set,
    minimum_independent_dominating_set,
    verify_eternal_certificate,
)


def _ordered(vertices: frozenset[int]) -> str:
    return " ".join(str(vertex) for vertex in sorted(vertices))


def _family_digest(family: frozenset[frozenset[int]]) -> str:
    digest = hashlib.sha256()
    for configuration in sorted(family, key=lambda item: tuple(sorted(item))):
        digest.update(_ordered(configuration).encode("ascii") + b"\n")
    return digest.hexdigest()


def _minimum_dominating_sets(graph: Graph, cardinality: int) -> int:
    return sum(
        is_dominating(graph, candidate)
        for candidate in combinations(graph.vertices, cardinality)
    )


def _atomic_json(path: Path, payload: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary = tempfile.mkstemp(
        prefix=path.name + ".", suffix=".partial", dir=path.parent
    )
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
            json.dump(payload, handle, indent=2, sort_keys=True)
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    except BaseException:
        try:
            os.unlink(temporary)
        except FileNotFoundError:
            pass
        raise


def _atomic_csv(
    path: Path, rows: list[dict[str, object]], fieldnames: list[str]
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary = tempfile.mkstemp(
        prefix=path.name + ".", suffix=".partial", dir=path.parent
    )
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    except BaseException:
        try:
            os.unlink(temporary)
        except FileNotFoundError:
            pass
        raise


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--catalog", type=Path, required=True)
    parser.add_argument("--parameters", type=Path, required=True)
    parser.add_argument("--log", type=Path, required=True)
    arguments = parser.parse_args()
    raw_catalog = arguments.catalog.read_bytes()
    with arguments.catalog.open(encoding="utf-8", newline="") as handle:
        catalog = list(csv.DictReader(handle))
    if len(catalog) != 56:
        raise AssertionError(f"expected 56 Table 9 records, got {len(catalog)}")
    if len({row["catalog_id"] for row in catalog}) != 56:
        raise AssertionError("duplicate catalog identifier")
    if len({row["graph6"] for row in catalog}) != 56:
        raise AssertionError("duplicate graph6 record")

    started_wall = time.time()
    started_counter = time.perf_counter()
    parameter_rows: list[dict[str, object]] = []
    histogram: Counter[tuple[int, int, int, int, int]] = Counter()
    counts: Counter[str] = Counter()
    for source_row in catalog:
        record = source_row["graph6"]
        graph_a = BitGraph.from_graph6(record)
        graph_b = Graph.from_graph6(record)
        if graph_a.n != int(source_row["n"]) or graph_b.order != int(
            source_row["n"]
        ):
            raise AssertionError(("catalog order", source_row))
        gamma, ind_dom, independence, gamma_inf, cover = compare_graph(
            record, check_all_guard_counts=True
        )
        result_a = eternal_fixed_point(graph_a, gamma_inf)
        if not verify_eternal_result(graph_a, result_a):
            raise AssertionError(("verifier A certificate", record))
        certificate_b = make_eternal_certificate(graph_b, gamma_inf)
        if certificate_b is None or not verify_eternal_certificate(
            graph_b, certificate_b
        ):
            raise AssertionError(("verifier B certificate", record))
        family_b = certificate_b.family
        normalized_a = frozenset(
            frozenset(
                vertex
                for vertex in range(graph_a.n)
                if configuration >> vertex & 1
            )
            for configuration in result_a.family
        )
        if normalized_a != family_b:
            raise AssertionError(("certificate families differ", record))

        dominating_witness = minimum_dominating_set(graph_b)
        independent_dominating_witness = minimum_independent_dominating_set(
            graph_b
        )
        independent_witness = maximum_independent_set(graph_b)
        row: dict[str, object] = {
            "catalog_id": source_row["catalog_id"],
            "n": graph_b.order,
            "m": graph_b.size,
            "graph6": record,
            "gamma": gamma,
            "i": ind_dom,
            "alpha": independence,
            "gamma_infinity_one_guard": gamma_inf,
            "theta": cover,
            "gamma_witness": _ordered(dominating_witness),
            "minimum_dominating_set_count": _minimum_dominating_sets(
                graph_b, gamma
            ),
            "i_witness": _ordered(independent_dominating_witness),
            "alpha_witness": _ordered(independent_witness),
            "greatest_eternal_family_size": len(family_b),
            "greatest_eternal_family_sha256": _family_digest(family_b),
        }
        parameter_rows.append(row)
        parameters = (gamma, ind_dom, independence, gamma_inf, cover)
        histogram[parameters] += 1
        counts["graphs"] += 1
        counts["order_10"] += graph_b.order == 10
        counts["order_11"] += graph_b.order == 11
        counts["gamma_infinity_less_than_theta"] += gamma_inf < cover
        counts["alpha_equals_gamma_infinity_less_than_theta"] += (
            independence == gamma_inf < cover
        )
        counts["gamma_equals_gamma_infinity_less_than_theta"] += (
            gamma == gamma_inf < cover
        )
        counts["gamma_less_than_alpha"] += gamma < independence

    expected = {
        "graphs": 56,
        "order_10": 2,
        "order_11": 54,
        "gamma_infinity_less_than_theta": 56,
        "alpha_equals_gamma_infinity_less_than_theta": 55,
        "gamma_equals_gamma_infinity_less_than_theta": 0,
        "gamma_less_than_alpha": 55,
    }
    if dict(counts) != expected:
        raise AssertionError(("published aggregate mismatch", dict(counts)))

    fieldnames = list(parameter_rows[0])
    _atomic_csv(arguments.parameters, parameter_rows, fieldnames)
    usage = resource.getrusage(resource.RUSAGE_SELF)
    result: dict[str, object] = {
        "status": "complete",
        "source": "MacGillivray--Mynhardt--Virgile (2022), Table 9",
        "catalog_path": str(arguments.catalog),
        "catalog_sha256": hashlib.sha256(raw_catalog).hexdigest(),
        "counts": expected,
        "parameter_histogram": {
            ",".join(map(str, parameters)): count
            for parameters, count in sorted(histogram.items())
        },
        "outcome": (
            "both independent implementations agree at every k and reproduce "
            "the published 56/55/0 aggregate"
        ),
        "started_unix": started_wall,
        "finished_unix": time.time(),
        "wall_seconds": time.perf_counter() - started_counter,
        "user_cpu_seconds": usage.ru_utime,
        "system_cpu_seconds": usage.ru_stime,
        "maximum_resident_set_size_raw": usage.ru_maxrss,
        "python": platform.python_version(),
        "platform": platform.platform(),
    }
    _atomic_json(arguments.log, result)
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
