#!/usr/bin/env python3
"""Negative tests for K3P certificate semantic binding (standard library only)."""
from __future__ import annotations

import copy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
from typing import Callable, List, MutableMapping, Tuple


ROOT = Path(__file__).resolve().parents[1]
VERIFIER = ROOT / "src" / "verify_k3p.py"
BASE = json.loads((ROOT / "certificate_k3p.json").read_text(encoding="utf-8"))


def synchronize_sidecars(directory: Path, certificate: MutableMapping[str, object]) -> None:
    """Write transport mirrors matching the two embedded certificate sections."""
    (directory / "jacobian_certificate_k3p.json").write_text(
        json.dumps(certificate["jacobian"], indent=2) + "\n", encoding="utf-8"
    )
    (directory / "continuous_time_certificate_k3p.json").write_text(
        json.dumps(certificate["continuous_time"], indent=2) + "\n", encoding="utf-8"
    )


def run_mutation(
    name: str,
    mutate: Callable[[MutableMapping[str, object]], None],
    expected_diagnostic: str,
) -> None:
    certificate = copy.deepcopy(BASE)
    mutate(certificate)
    with tempfile.TemporaryDirectory(prefix="k3p-semantic-mutation-") as temp_name:
        directory = Path(temp_name)
        certificate_path = directory / "certificate_k3p.json"
        certificate_path.write_text(
            json.dumps(certificate, indent=2) + "\n", encoding="utf-8"
        )
        synchronize_sidecars(directory, certificate)
        command = [sys.executable]
        if sys.flags.optimize:
            command.append("-" + "O" * sys.flags.optimize)
        command.extend([str(VERIFIER), str(certificate_path)])
        completed = subprocess.run(
            command,
            cwd=ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
    combined = completed.stdout + completed.stderr
    if completed.returncode == 0:
        raise RuntimeError(f"mutation unexpectedly passed: {name}")
    if expected_diagnostic not in combined:
        raise RuntimeError(
            f"mutation {name!r} failed for the wrong reason; expected diagnostic "
            f"{expected_diagnostic!r}\n{combined}"
        )
    print(f"[mutation rejection] PASS  {name}: {expected_diagnostic}")


def cycle_jacobian_semantics(certificate: MutableMapping[str, object]) -> None:
    jacobian = certificate["jacobian"]
    continuous_time = certificate["continuous_time"]
    columns = jacobian["column_order"]
    matrix = jacobian["matrix"]
    pivots = continuous_time["pivot_derivatives"]
    characters = [columns[index]["character"] for index in range(3)]
    for index, source in enumerate((1, 2, 0)):
        columns[index]["character"] = characters[source]
    for row in matrix:
        old = row[:3]
        row[:3] = [old[1], old[2], old[0]]
    old_pivots = pivots[:3]
    pivots[:3] = [old_pivots[1], old_pivots[2], old_pivots[0]]


def alter_free_descriptor(certificate: MutableMapping[str, object]) -> None:
    certificate["continuous_time"]["free_direction"][0]["character"] = "G"


def reverse_reticulation_order(certificate: MutableMapping[str, object]) -> None:
    certificate["rooted_network"]["reticulations"].reverse()


def swap_suppression_sources(certificate: MutableMapping[str, object]) -> None:
    rows = certificate["root_suppression"]["effective_semi_directed_edges"]
    by_id = {row["id"]: row for row in rows}
    by_id["e_u_p"]["source_edges"] = ["e_u_q"]
    by_id["e_u_q"]["source_edges"] = ["e_u_p"]


def swap_actual_p_q_endpoints(certificate: MutableMapping[str, object]) -> None:
    def swap(vertex: str) -> str:
        return {"p": "q", "q": "p"}.get(vertex, vertex)

    for row in certificate["rooted_network"]["arcs"]:
        row["parent"] = swap(row["parent"])
        row["child"] = swap(row["child"])
    for row in certificate["root_suppression"]["effective_semi_directed_edges"]:
        row["endpoints"] = [swap(vertex) for vertex in row["endpoints"]]
        if "direction" in row:
            row["direction"] = [swap(vertex) for vertex in row["direction"]]


def swap_root_arc_ids(certificate: MutableMapping[str, object]) -> None:
    rows = certificate["rooted_network"]["arcs"]
    by_id = {row["id"]: row for row in rows}
    by_id["e_rho_1"]["id"] = "e_rho_u"
    by_id["e_rho_u"]["id"] = "e_rho_1"


def insert_shadowed_duplicate_vertex(certificate: MutableMapping[str, object]) -> None:
    certificate["rooted_network"]["vertices"].insert(
        0, {"id": "rho", "type": "tree"}
    )


def contradict_reticulation_parent(certificate: MutableMapping[str, object]) -> None:
    certificate["rooted_network"]["reticulations"][0]["incoming"][0]["parent"] = "q"


def add_unknown_top_level_field(certificate: MutableMapping[str, object]) -> None:
    certificate["unverified_claim"] = True


def main() -> None:
    tests: List[Tuple[str, Callable[[MutableMapping[str, object]], None], str]] = [
        (
            "coordinated Jacobian descriptor/column/pivot cycle",
            cycle_jacobian_semantics,
            "canonical Jacobian descriptor order",
        ),
        (
            "free-direction semantic relabeling",
            alter_free_descriptor,
            "canonical continuous-time free-direction descriptors",
        ),
        (
            "reticulation-order reversal",
            reverse_reticulation_order,
            "canonical ordered reticulation descriptors",
        ),
        (
            "root-suppression source reassignment",
            swap_suppression_sources,
            "singleton root-suppression source binding for e_u_p",
        ),
        (
            "coordinated actual p/q endpoint swap with stale descriptors",
            swap_actual_p_q_endpoints,
            "canonical rooted arc ID/endpoint/vector map",
        ),
        (
            "root-adjacent arc-ID swap",
            swap_root_arc_ids,
            "canonical rooted arc ID/endpoint/vector map",
        ),
        (
            "shadowed duplicate vertex identifier",
            insert_shadowed_duplicate_vertex,
            "duplicate vertex identifier",
        ),
        (
            "reticulation parent contradicts referenced arc",
            contradict_reticulation_parent,
            "reticulation descriptor parent for e_p_r2",
        ),
        (
            "unknown top-level certificate field",
            add_unknown_top_level_field,
            "closed top-level K3P certificate schema",
        ),
    ]
    for name, mutate, expected_diagnostic in tests:
        run_mutation(name, mutate, expected_diagnostic)
    print("\nALL K3P SEMANTIC MUTATION CHECKS PASSED")


if __name__ == "__main__":
    main()
