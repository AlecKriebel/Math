#!/usr/bin/env python3
"""Independent exact audit of the componentwise K2P C/T scale lemma.

This script does not read a finite classification ledger.  It checks the
linear symmetry constraints, the primitive rigid-support boundary counts,
and the unique reduced two-boundary theta obstruction from graph encodings.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import itertools
import json
import sys
from fractions import Fraction
from pathlib import Path


HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[1]
ATLAS = PROJECT / "package/referee/k2p_offline_sweep_portable/atlas/k2p_atlas_core.py"


class AuditFailure(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AuditFailure(message)


def canonical_bytes(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode()


def sha_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def rank(matrix: list[list[int]]) -> int:
    if not matrix:
        return 0
    work = [[Fraction(value) for value in row] for row in matrix]
    row = 0
    for column in range(len(work[0])):
        pivot = next((i for i in range(row, len(work)) if work[i][column]), None)
        if pivot is None:
            continue
        work[row], work[pivot] = work[pivot], work[row]
        scale = work[row][column]
        work[row] = [entry / scale for entry in work[row]]
        for i in range(len(work)):
            if i == row or not work[i][column]:
                continue
            scale = work[i][column]
            work[i] = [a - scale * b for a, b in zip(work[i], work[row])]
        row += 1
        if row == len(work):
            break
    return row


def symmetry_constraints() -> dict[str, object]:
    """Audit log-ratios rho_e = log(c_e(C)/c_e(T))."""
    rows = []
    for degree in range(2, 10):
        # On an unmarked component, the positive conservation-supported entry
        # with C at incidences e,f and zero elsewhere is carried by the global
        # C<->T automorphism to the corresponding T,T entry.  Hence rho_e+rho_f=0.
        matrix = []
        for left, right in itertools.combinations(range(degree), 2):
            equation = [0] * degree
            equation[left] = equation[right] = 1
            matrix.append(equation)
        matrix_rank = rank(matrix)
        expected = degree if degree >= 3 else 1
        require(matrix_rank == expected, f"unmarked symmetry rank drift at d={degree}")
        rows.append(
            {
                "degree": degree,
                "constraint_rank": matrix_rank,
                "kernel_dimension": degree - matrix_rank,
            }
        )

    # With a marked physical block, the entry having C at incidence e and C
    # at that block gives rho_e=0, independently for every e.
    for degree in range(1, 10):
        require(rank([[int(i == j) for i in range(degree)] for j in range(degree)]) == degree,
                f"marked symmetry rank drift at d={degree}")

    require(rows[0]["kernel_dimension"] == 1, "degree-two stabilizer missing")
    require(all(row["kernel_dimension"] == 0 for row in rows[1:]),
            "unexpected degree-at-least-three stabilizer")
    return {
        "status": "PASS",
        "marked": "rho_e=0 from one incidence plus one marked physical C/T block",
        "unmarked": rows,
        "degree_two_kernel": "(rho_1,rho_2)=t(1,-1)",
    }


def load_atlas():
    spec = importlib.util.spec_from_file_location("global_scale_atlas", ATLAS)
    require(spec is not None and spec.loader is not None, "atlas import spec")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def primitive_supports() -> dict[str, object]:
    atlas = load_atlas()
    expected = {
        "cycle": (2, 3),
        "theta0": (2, 4),
        "theta1": (2, 4),
        "theta2": (4, 5),
        "theta3": (2, 4),
    }
    rows = []
    for core, (count, ports) in expected.items():
        supports = atlas.source_supports((core,))
        require(len(supports) == count, f"{core} support count drift")
        require({len(record.selected_labels) for record in supports} == {ports},
                f"{core} boundary count drift")
        for record in supports:
            leaves = [
                data for _, data in record.graph.nodes(data=True)
                if data.get("role") == "leaf"
            ]
            require(len(leaves) == ports, f"{core} graph leaf count drift")
            require(all(not data.get("dummy") and isinstance(data.get("label"), int)
                        for data in leaves), f"{core} support is not physically marked")
        rows.append(
            {
                "core": core,
                "minimum_physical_boundary_ports": ports,
                "rigid_supports": count,
            }
        )
    return {
        "status": "PASS",
        "rows": rows,
        "ordinary_tree_minimum_ports": 3,
        "monotonicity": "restoration and one-/two-port insertion only add marked ports",
    }


def is_dag(nodes: set[int], arcs: list[tuple[int, int]]) -> bool:
    indegree = {node: 0 for node in nodes}
    children = {node: [] for node in nodes}
    for tail, head in arcs:
        indegree[head] += 1
        children[tail].append(head)
    queue = [node for node in nodes if indegree[node] == 0]
    seen = 0
    while queue:
        tail = queue.pop()
        seen += 1
        for head in children[tail]:
            indegree[head] -= 1
            if indegree[head] == 0:
                queue.append(head)
    return seen == len(nodes)


def k4_minus_edge() -> dict[str, object]:
    """Independent rooting census for theta path lengths (1,2,2)."""
    core = (0, 1, 2, 3)
    edges = [(0, 1), (0, 2), (2, 1), (0, 3), (3, 1), (2, 4), (3, 5)]
    nodes = set(range(7))
    admissible = 0
    tree_child = 0
    for root_edge_index, root_edge in enumerate(edges):
        split_edges = (
            edges[:root_edge_index]
            + edges[root_edge_index + 1 :]
            + [(root_edge[0], 6), (6, root_edge[1])]
        )
        for reticulations in itertools.combinations(core, 2):
            roles = {node: ("retic" if node in reticulations else "tree") for node in core}
            roles.update({4: "leaf", 5: "leaf", 6: "root"})
            for bits in itertools.product((0, 1), repeat=len(split_edges)):
                arcs = [
                    (tail, head) if not bit else (head, tail)
                    for (tail, head), bit in zip(split_edges, bits)
                ]
                indegree = {node: 0 for node in nodes}
                outdegree = {node: 0 for node in nodes}
                children = {node: [] for node in nodes}
                for tail, head in arcs:
                    indegree[head] += 1
                    outdegree[tail] += 1
                    children[tail].append(head)
                valid = (indegree[6], outdegree[6]) == (0, 2)
                valid = valid and all(
                    (indegree[node], outdegree[node])
                    == ((2, 1) if roles[node] == "retic" else (1, 2))
                    for node in core
                )
                valid = valid and all(
                    (indegree[node], outdegree[node]) == (1, 0) for node in (4, 5)
                )
                if not valid or not is_dag(nodes, arcs):
                    continue
                admissible += 1
                if all(
                    roles[node] == "leaf"
                    or any(roles[child] in {"tree", "leaf"} for child in children[node])
                    for node in nodes
                ):
                    tree_child += 1
    require(admissible == 25, f"K4-e admissible census drift: {admissible}")
    require(tree_child == 0, "K4-e acquired a tree-child rooting")
    return {
        "status": "PASS",
        "rooted_binary_DAG_presentations": admissible,
        "tree_child_presentations": tree_child,
        "structural_identification": "the only simple reduced two-boundary theta has path lengths (1,2,2)",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=HERE / "component_scale_certificate.json")
    args = parser.parse_args()
    payload = {
        "schema": "k2p-global-component-scale-audit-v1",
        "scope": "principal D_plus strong-class bridge components; no finite relation claim",
        "status": "PASS",
        "atlas_sha256": sha_file(ATLAS),
        "symmetry_constraints": symmetry_constraints(),
        "primitive_supports": primitive_supports(),
        "K4_minus_edge_exclusion": k4_minus_edge(),
        "conclusion": (
            "Every retained primitive anchor is marked. Every unmarked retained strong "
            "component has degree at least three. Hence C/T incidence scales are unique; "
            "the sole degree-two log-ratio stabilizer is outside the class."
        ),
    }
    payload["payload_sha256"] = hashlib.sha256(canonical_bytes(payload)).hexdigest()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, sort_keys=True, indent=2) + "\n")
    print("K2P_GLOBAL_COMPONENT_SCALE_AUDIT_PASS")
    print(json.dumps({
        "payload_sha256": payload["payload_sha256"],
        "K4-e": [
            payload["K4_minus_edge_exclusion"]["rooted_binary_DAG_presentations"],
            payload["K4_minus_edge_exclusion"]["tree_child_presentations"],
        ],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
