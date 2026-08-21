#!/usr/bin/env python3
"""Search exact homogeneous separators for unresolved four-port records.

This is a research-side extension of the locked production sweep.  It reads the
same descriptor pickle, binds every requested case to the semantic record, and
emits replayable separator metadata without modifying the referee package.
"""

from __future__ import annotations

import argparse
import datetime
import gc
import hashlib
import importlib.util
import json
import pickle
import sys
import time
from pathlib import Path


def sha_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def parse_case(value: str) -> tuple[int, int]:
    try:
        source, class_id = value.split(":", 1)
        return int(source), int(class_id)
    except (ValueError, TypeError) as exc:
        raise argparse.ArgumentTypeError("case must have form SOURCE:CLASS") from exc


def record_path(run_root: Path, source: int, class_id: int) -> Path:
    return run_root / f"source_{source}" / "records" / f"class_{class_id:06d}.json"


def homogeneous_separator_streaming(
    atlas, source, target, degree: int, min_block_size: int, max_block_size: int
):
    """Exact degree-d search retaining products for only one weight block.

    Every coordinate monomial belongs to exactly one multihomogeneous weight
    block, so cross-block product caches cannot provide reuse.  Keeping them
    caused the exploratory quartic engine to exceed the local memory guard.
    """
    if source.k != target.k:
        raise AssertionError("source and target port counts differ")
    source_outputs = atlas.output_sparse_polynomials_cached(source)
    target_outputs = atlas.output_sparse_polynomials_cached(target)
    blocks = sorted(atlas.homogeneous_blocks(source.k, degree), key=lambda row: (len(row[1]), row[0]))
    for weight, block in blocks:
        if len(block) < min_block_size or len(block) > max_block_size:
            continue
        source_columns = [
            atlas.sparse_mul_many([source_outputs[index] for index in indices])
            for indices in block
        ]
        target_columns = [
            atlas.sparse_mul_many([target_outputs[index] for index in indices])
            for indices in block
        ]
        for vector in atlas.kernel_sparse_columns_fast(target_columns):
            source_pullback = atlas.sparse_lincomb(source_columns, vector)
            if source_pullback:
                if atlas.sparse_lincomb(target_columns, vector):
                    raise AssertionError("candidate does not vanish on target")
                return {
                    "degree": degree,
                    "weight": weight,
                    "coordinate_monomials": block,
                    "coefficients": vector,
                    "source_nonzero_terms": len(source_pullback),
                    "source_pullback": source_pullback,
                }
    return None


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--package-root", type=Path, required=True)
    parser.add_argument("--run-root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--degree", type=int, default=3)
    parser.add_argument("--max-block-size", type=int, default=40)
    parser.add_argument("--min-block-size", type=int, default=2)
    parser.add_argument("--direction", choices=("forward", "reverse"), default="forward")
    parser.add_argument("--streaming", action="store_true")
    parser.add_argument("--case", action="append", type=parse_case, default=[])
    args = parser.parse_args()
    if args.degree < 2:
        raise SystemExit("degree must be at least two")
    if not 2 <= args.min_block_size <= args.max_block_size:
        raise SystemExit("block-size bounds must satisfy 2 <= min <= max")

    package_root = args.package_root.resolve()
    run_root = args.run_root.resolve()
    lock_path = package_root / "INPUT_LOCK.json"
    lock = json.loads(lock_path.read_text())
    descriptor_path = package_root / "atlas" / "descriptors_4.pkl"
    expected_descriptor_hash = lock["files"]["atlas/descriptors_4.pkl"]
    observed_descriptor_hash = sha_file(descriptor_path)
    if observed_descriptor_hash != expected_descriptor_hash:
        raise SystemExit("descriptor pickle does not match INPUT_LOCK")

    atlas = load_module("k2p_atlas_core", package_root / "atlas" / "k2p_atlas_core.py")
    driver = load_module("k2p_four_port_driver_analysis", package_root / "resumable_four_port_driver.py")
    with descriptor_path.open("rb") as handle:
        _sources, _targets, _rows, source_descriptors, cache = pickle.load(handle)

    descriptor_by_hash = {}
    for descriptor in list(source_descriptors) + list(cache.values()):
        descriptor_hash = driver.sha_object(descriptor)
        incumbent = descriptor_by_hash.setdefault(descriptor_hash, descriptor)
        if incumbent != descriptor:
            raise RuntimeError(f"descriptor hash collision: {descriptor_hash}")

    merged = json.loads((run_root / "FOUR_PORT_SWEEP_MERGED_STATUS.json").read_text())
    requested = args.case or [
        (int(source), int(class_id))
        for source, class_ids in sorted(merged["unresolved_by_source"].items(), key=lambda row: int(row[0]))
        for class_id in class_ids
    ]
    results = []
    for source, class_id in requested:
        path = record_path(run_root, source, class_id)
        record = json.loads(path.read_text())
        if record["source_index"] != source or record["canonical_class_id"] != class_id:
            raise RuntimeError(f"record identity mismatch: {path}")
        if record["status"] != "unresolved" or record["stratum"] != "direct_no_dummy":
            raise RuntimeError(f"case is not an unresolved direct record: {source}:{class_id}")
        target = descriptor_by_hash.get(record["descriptor_sha256"])
        if target is None:
            raise RuntimeError(f"missing descriptor: {record['descriptor_sha256']}")
        source_descriptor = source_descriptors[source]
        left, right = (
            (source_descriptor, target)
            if args.direction == "forward"
            else (target, source_descriptor)
        )

        print(json.dumps({"event": "start", "source_index": source, "class_id": class_id}), flush=True)
        started = time.perf_counter()
        if args.degree == 2:
            separator = atlas.quadratic_separator_fast(
                left, right, max_block_size=args.max_block_size
            )
        elif args.streaming:
            separator = homogeneous_separator_streaming(
                atlas,
                left,
                right,
                args.degree,
                args.min_block_size,
                args.max_block_size,
            )
        elif args.degree == 3:
            separator = atlas.cubic_separator_fast(
                left, right, max_block_size=args.max_block_size
            )
        else:
            separator = atlas.homogeneous_separator_fast(
                left,
                right,
                degree=args.degree,
                max_block_size=args.max_block_size,
            )
        elapsed = time.perf_counter() - started
        if separator is None:
            certificate = None
        else:
            pullback = separator.pop("source_pullback")
            certificate = driver.canonical_data(separator)
            certificate["source_pullback_sha256"] = driver.sha_object(pullback)
        row = {
            "source_index": source,
            "canonical_class_id": class_id,
            "semantic_record_sha256": record["semantic_record_sha256"],
            "source_graph_sha256": record["source_graph_sha256"],
            "target_graph_sha256": record["target_graph_sha256"],
            "descriptor_sha256": record["descriptor_sha256"],
            "degree": args.degree,
            "direction": args.direction,
            "streaming": args.streaming,
            "max_block_size": args.max_block_size,
            "min_block_size": args.min_block_size,
            "elapsed_seconds": elapsed,
            "separated": certificate is not None,
            "certificate": certificate,
        }
        results.append(row)
        print(
            json.dumps(
                {
                    "event": "done",
                    "source_index": source,
                    "class_id": class_id,
                    "separated": row["separated"],
                    "seconds": elapsed,
                }
            ),
            flush=True,
        )
        gc.collect()

    semantic_rows = [
        {key: value for key, value in row.items() if key != "elapsed_seconds"}
        for row in results
    ]
    payload = {
        "schema": "k2p-four-port-homogeneous-separator-scan-v1",
        "generated_at_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "degree": args.degree,
        "direction": args.direction,
        "streaming": args.streaming,
        "max_block_size": args.max_block_size,
        "min_block_size": args.min_block_size,
        "input_lock_sha256": sha_file(lock_path),
        "descriptor_pickle_sha256": observed_descriptor_hash,
        "run_semantic_sweep_sha256": merged["semantic_sweep_sha256"],
        "case_count": len(results),
        "separated_count": sum(row["separated"] for row in results),
        "unseparated_count": sum(not row["separated"] for row in results),
        "semantic_scan_sha256": driver.sha_object(semantic_rows),
        "results": results,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(json.dumps({key: payload[key] for key in (
        "case_count", "separated_count", "unseparated_count", "semantic_scan_sha256"
    )}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
