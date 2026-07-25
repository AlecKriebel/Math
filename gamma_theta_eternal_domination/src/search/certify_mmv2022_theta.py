"""Generate and replay exact theta=4 certificates for MMV (2022), Table 9."""

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
from pathlib import Path

from verifier_b.coloring_trace_checker import check_uncolorability_trace
from verifier_b.coloring_trace_generator import write_uncolorability_trace
from verifier_b.graph import Graph
from verifier_b.invariants import find_coloring


FIELDS = [
    "catalog_id",
    "n",
    "graph6",
    "k",
    "claim",
    "four_coloring_of_complement",
    "node_count",
    "trace_sha256",
    "claim_sha256",
    "certificate_sha256",
    "certificate_bytes",
    "certificate_path",
    "verified",
]


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


def _atomic_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary = tempfile.mkstemp(
        prefix=path.name + ".", suffix=".partial", dir=path.parent
    )
    try:
        with os.fdopen(
            descriptor, "w", encoding="utf-8", newline=""
        ) as handle:
            writer = csv.DictWriter(handle, fieldnames=FIELDS)
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


def _direct_coloring_check(graph: Graph, coloring: tuple[int, ...]) -> bool:
    return (
        len(coloring) == graph.order
        and all(type(color) is int and 0 <= color < 4 for color in coloring)
        and all(
            coloring[first] != coloring[second]
            for first, second in graph.edges()
        )
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--catalog", type=Path, required=True)
    parser.add_argument("--certificate-dir", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--log", type=Path, required=True)
    arguments = parser.parse_args()

    with arguments.catalog.open(encoding="utf-8", newline="") as handle:
        catalog = list(csv.DictReader(handle))
    if len(catalog) != 56:
        raise AssertionError(f"expected 56 catalog rows, got {len(catalog)}")
    if len({row["catalog_id"] for row in catalog}) != len(catalog):
        raise AssertionError("duplicate catalog identifier")
    if len({row["graph6"] for row in catalog}) != len(catalog):
        raise AssertionError("duplicate catalog graph6 record")
    arguments.certificate_dir.mkdir(parents=True, exist_ok=True)

    started_wall = time.time()
    started_counter = time.perf_counter()
    generated = 0
    reused = 0
    rows: list[dict[str, object]] = []
    aggregate_digest = hashlib.sha256()
    total_nodes = 0
    total_bytes = 0

    for source in catalog:
        catalog_id = source["catalog_id"]
        record = source["graph6"]
        graph = Graph.from_graph6(record)
        if graph.to_graph6() != record or graph.order != int(source["n"]):
            raise AssertionError(("catalog graph mismatch", source))

        certificate = (
            arguments.certificate_dir / f"{catalog_id}-theta-gt-3.ndjson"
        )
        if certificate.exists():
            reused += 1
        else:
            write_uncolorability_trace(graph, 3, certificate)
            generated += 1
        checked = check_uncolorability_trace(
            certificate, expected_graph=graph, expected_k=3
        )
        raw_certificate = certificate.read_bytes()
        raw_digest = hashlib.sha256(raw_certificate).hexdigest()
        if raw_digest != checked.certificate_sha256:
            raise AssertionError(("certificate byte hash", catalog_id))

        complement = graph.complement()
        four_coloring = find_coloring(complement, 4)
        if four_coloring is None or not _direct_coloring_check(
            complement, four_coloring
        ):
            raise AssertionError(("missing direct four-coloring", catalog_id))

        certificate_bytes = len(raw_certificate)
        total_nodes += checked.node_count
        total_bytes += certificate_bytes
        aggregate_digest.update(catalog_id.encode("ascii") + b"\0")
        aggregate_digest.update(raw_digest.encode("ascii") + b"\n")
        rows.append(
            {
                "catalog_id": catalog_id,
                "n": graph.order,
                "graph6": record,
                "k": 3,
                "claim": "theta=4",
                "four_coloring_of_complement": " ".join(
                    str(color) for color in four_coloring
                ),
                "node_count": checked.node_count,
                "trace_sha256": checked.trace_sha256,
                "claim_sha256": checked.claim_sha256,
                "certificate_sha256": raw_digest,
                "certificate_bytes": certificate_bytes,
                "certificate_path": str(certificate),
                "verified": "yes",
            }
        )

    _atomic_csv(arguments.manifest, rows)
    usage = resource.getrusage(resource.RUSAGE_SELF)
    result: dict[str, object] = {
        "status": "complete",
        "claim": (
            "all 56 MMV (2022) Table 9 graphs have theta=4: each complement "
            "has a direct four-coloring and a replayed exhaustive "
            "non-three-colorability trace"
        ),
        "catalog_path": str(arguments.catalog),
        "catalog_sha256": hashlib.sha256(
            arguments.catalog.read_bytes()
        ).hexdigest(),
        "certificate_count": len(rows),
        "certificates_generated": generated,
        "certificates_reused": reused,
        "total_trace_nodes": total_nodes,
        "total_certificate_bytes": total_bytes,
        "ordered_certificate_set_sha256": aggregate_digest.hexdigest(),
        "manifest_path": str(arguments.manifest),
        "manifest_sha256": hashlib.sha256(
            arguments.manifest.read_bytes()
        ).hexdigest(),
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
