#!/usr/bin/env python3
"""Prepare and independently verify storage-light conflict-block starts."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path

from graph_io import encode_graph6, read_graph


ROOT = Path(__file__).resolve().parents[1]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_json(path: Path, value: object) -> str:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, sort_keys=True, indent=2) + "\n",
        encoding="utf-8",
    )
    return sha256(path)


def checked_process(command: list[str]) -> dict[str, object]:
    run = subprocess.run(
        command,
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
        timeout=120,
    )
    if run.returncode not in (0, 1):
        raise RuntimeError(
            f"verifier failed with {run.returncode}: {command}\n"
            f"{run.stdout}\n{run.stderr}"
        )
    value = json.loads(run.stdout)
    if not isinstance(value, dict):
        raise RuntimeError("verifier JSON root is not an object")
    return value


def extend_catalog_graph(catalog: Path, line: int, output: Path) -> dict:
    base = read_graph(catalog, line)
    if len(base) != 42:
        raise ValueError("catalog seed must have order 42")
    degrees = [neighbors.bit_count() for neighbors in base]
    selected = sorted(range(42), key=lambda vertex: (degrees[vertex], vertex))[
        :21
    ]
    adjacency = list(base) + [0]
    for vertex in selected:
        adjacency[vertex] |= 1 << 42
        adjacency[42] |= 1 << vertex
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(encode_graph6(adjacency) + "\n", encoding="ascii")
    return {
        "schema": "ramsey55.catalog_balanced_extension_seed.v1",
        "catalog": str(catalog),
        "catalog_sha256": sha256(catalog),
        "catalog_line_one_based": line,
        "construction": (
            "Add vertex 42 adjacent to the 21 catalog vertices with the "
            "lowest (degree,label) lexicographic keys."
        ),
        "base_degree_vector": degrees,
        "new_vertex_neighbors": selected,
        "new_vertex_degree": len(selected),
        "output": str(output),
        "output_sha256": sha256(output),
    }


def verify_start(label: str, graph: Path) -> dict[str, object]:
    python_result = checked_process(
        [sys.executable, "verify/exhaustive_verify.py", str(graph)]
    )
    cpp_result = checked_process(["build/bitset_verify", str(graph)])
    python_path = (
        ROOT / f"results/verification/conflict_block_{label}_python.json"
    )
    cpp_path = ROOT / f"results/verification/conflict_block_{label}_cpp.json"
    python_sha = write_json(python_path, python_result)
    cpp_sha = write_json(cpp_path, cpp_result)
    if (
        python_result["n"] != 43
        or cpp_result["n"] != 43
        or python_result["edge_count"] != cpp_result["edge_count"]
        or python_result["degree_sequence"] != cpp_result["degree_sequence"]
        or cpp_result["clique_k_found"]
        != (python_result["clique_count"] > 0)
        or cpp_result["independent_k_found"]
        != (python_result["independent_count"] > 0)
    ):
        raise RuntimeError(f"start verifiers disagree for {label}")
    return {
        "label": label,
        "path": str(graph),
        "sha256": sha256(graph),
        "C5": python_result["clique_count"],
        "I5": python_result["independent_count"],
        "E": python_result["objective"],
        "edge_count": python_result["edge_count"],
        "degree_sequence": python_result["degree_sequence"],
        "python_verification": str(python_path.relative_to(ROOT)),
        "python_verification_sha256": python_sha,
        "cpp_verification": str(cpp_path.relative_to(ROOT)),
        "cpp_verification_sha256": cpp_sha,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--catalog-line", type=int, default=1)
    args = parser.parse_args()
    catalog = ROOT / "data/r55_42some.g6"
    catalog_seed = (
        ROOT / "results/best_candidates/catalog_line1_balanced_extension.g6"
    )
    metadata = extend_catalog_graph(catalog, args.catalog_line, catalog_seed)
    metadata_path = (
        ROOT
        / "results/constructive/conflict_block_catalog_line1_seed.metadata.json"
    )
    write_json(metadata_path, metadata)

    starts = [
        verify_start(
            "exoo", ROOT / "results/best_candidates/exoo_seed_20260724.g6"
        ),
        verify_start(
            "incident",
            ROOT / "results/best_candidates/incident_lns_seed_20260726.g6",
        ),
        verify_start(
            "core_kick",
            ROOT / "results/best_candidates/core_kick_seed_20260731.g6",
        ),
        verify_start("catalog_line1", catalog_seed),
        verify_start(
            "global_baseline",
            ROOT / "results/best_candidates/baseline_seed_20260723.g6",
        ),
    ]
    manifest = {
        "schema": "ramsey55.conflict_block_start_manifest.v1",
        "generator": str(Path(__file__).relative_to(ROOT)),
        "generator_sha256": sha256(Path(__file__)),
        "catalog_seed_metadata": str(metadata_path.relative_to(ROOT)),
        "catalog_seed_metadata_sha256": sha256(metadata_path),
        "all_dual_verifications_agree": True,
        "starts": starts,
    }
    manifest_path = (
        ROOT / "results/verification/conflict_block_start_manifest.json"
    )
    write_json(manifest_path, manifest)
    print(json.dumps(manifest, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
