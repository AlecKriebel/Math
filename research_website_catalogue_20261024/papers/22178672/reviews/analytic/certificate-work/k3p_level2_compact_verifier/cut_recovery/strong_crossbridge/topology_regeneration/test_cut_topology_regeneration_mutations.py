#!/usr/bin/env python3
"""Coherent topology/mask mutation tests for graph-derived cut regeneration."""

from __future__ import annotations

import copy
import hashlib
import json
import subprocess
import sys
import tempfile
from pathlib import Path

import generate_cut_topology as producer
import verify_cut_topology_regeneration as verifier


if not __debug__ or sys.flags.optimize:
    raise SystemExit("optimized Python (-O/-OO) is forbidden for exact verification")


HERE = Path(__file__).resolve().parent
REFERENCE = verifier.REFERENCE
VERIFY = HERE / "verify_cut_topology_regeneration.py"


def tensor_hash(signatures: tuple[tuple[int, ...], ...], reticulations: int) -> str:
    return hashlib.sha256(repr((reticulations, signatures)).encode()).hexdigest()


def expect_cli_rejection(name: str, payload: dict, directory: Path) -> dict:
    path = directory / f"{name}.json"
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    result = subprocess.run(
        [sys.executable, str(VERIFY), "--candidate", str(path), "--reference", str(REFERENCE)],
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode == 0:
        raise AssertionError(f"mutation accepted: {name}")
    return {"mutation": name, "rejected": True, "returncode": result.returncode}


def subdivide_witness_coherently(data: dict) -> None:
    row = next(record for record in data["one_active_wrong_split"]["records"]
               if record["witness_graph"] is not None)
    witness = row["witness_graph"]
    signatures = tuple(tuple(values) for values in row["signatures"])
    arcs = [tuple(edge) for edge in witness["arcs"]]
    tail, head = arcs[0]
    vertex = "independent_serial_subdivision"
    arcs[0:1] = [(tail, vertex), (vertex, head)]
    network = producer.Network(
        witness["core"], witness["role"], witness["root"], tuple(arcs),
        tuple(sorted(witness["selected"].items())),
        tuple(sorted(witness["full_labels"].items())),
    )
    rebuilt = producer.graph_record(network, witness["transport"], signatures)
    row["witness_graph"] = rebuilt
    # This is a genuinely coherent graph presentation: the active semantic
    # verifier reconstructs the new displayed trees and accepts it.  The
    # release comparison must nevertheless reject it because regenerated
    # bytes are required to match the bound K3P input exactly.
    verifier.verify_semantics(data)


def mutate_tree_masks_coherently(data: dict) -> None:
    row = next(record for record in data["one_active_wrong_split"]["records"]
               if record["witness_graph"] is None)
    signatures = tuple(tuple(values) for values in row["signatures"])
    altered = signatures[:-1] + ((11,),)
    row["signatures"] = [list(values) for values in altered]
    row["tensor_sha256"] = tensor_hash(altered, int(row["reticulation_count"]))
    rows = []
    for split in producer.BALANCED_SPLITS:
        displayed = all(producer.displayed_split_status(altered, split))
        item = {"split": list(split), "displayed_by_all": displayed}
        if not displayed:
            item["strict_minor"] = {"coherently_rebound_test_fixture": True}
        rows.append(item)
    row["splits"] = rows


def main() -> int:
    original = json.loads(REFERENCE.read_text())
    results = []
    with tempfile.TemporaryDirectory(prefix="k3p_cut_topology_mutations_") as temporary:
        directory = Path(temporary)

        primitive = copy.deepcopy(original)
        primitive["primitive_cores"][0]["arcs"][0] = ["X", "S"]
        results.append(expect_cli_rejection("reverse_primitive_cycle_arc", primitive, directory))

        masks = copy.deepcopy(original)
        mutate_tree_masks_coherently(masks)
        results.append(expect_cli_rejection("rebind_ordinary_tree_masks_and_hash", masks, directory))

        subdivided = copy.deepcopy(original)
        subdivide_witness_coherently(subdivided)
        results.append(expect_cli_rejection("coherent_serial_topology_subdivision", subdivided, directory))

    if not all(item["rejected"] for item in results):
        return 2
    print(json.dumps({"mutation_count": len(results), "mutations": results, "status": "PASS"},
                     indent=2, sort_keys=True))
    print("CUT_TOPOLOGY_GRAPH_REGENERATION_MUTATIONS_PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
