#!/usr/bin/env python3
"""Hostile certificate mutations for the v1.2.4 K3P verifier audit."""

from __future__ import annotations

import copy
import json
from pathlib import Path
import shutil
import subprocess
import tempfile


AUDIT = Path(__file__).resolve().parents[1]
MATERIALS = AUDIT / "packet_copy" / "materials"
VERIFIER = MATERIALS / "src" / "verify_k3p.py"
BASE = json.loads((MATERIALS / "certificate_k3p.json").read_text())


def run(name: str, mutation) -> None:
    certificate = copy.deepcopy(BASE)
    mutation(certificate)
    with tempfile.TemporaryDirectory(prefix=f"v124-{name}-") as raw:
        directory = Path(raw)
        target = directory / "certificate_k3p.json"
        target.write_text(json.dumps(certificate, indent=2) + "\n")
        for sidecar in ("jacobian_certificate_k3p.json", "continuous_time_certificate_k3p.json"):
            shutil.copyfile(MATERIALS / sidecar, directory / sidecar)
        result = subprocess.run(
            ["python3", str(VERIFIER), str(target)],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=False,
        )
    last = result.stdout.strip().splitlines()[-1] if result.stdout.strip() else "<no output>"
    print(f"{name}: exit={result.returncode}; {last}")


def duplicate_conflicting_vertex(certificate) -> None:
    certificate["rooted_network"]["vertices"].insert(0, {"id": "rho", "type": "leaf", "label": 99})


def duplicate_leaf_label(certificate) -> None:
    for row in certificate["rooted_network"]["vertices"]:
        if row["id"] == "1":
            row["label"] = 2


def swap_root_arc_ids(certificate) -> None:
    arcs = certificate["rooted_network"]["arcs"]
    by_id = {row["id"]: row for row in arcs}
    by_id["e_rho_1"]["id"], by_id["e_rho_u"]["id"] = "e_rho_u", "e_rho_1"


def swap_r2_endpoints(certificate) -> None:
    arcs = {row["id"]: row for row in certificate["rooted_network"]["arcs"]}
    arcs["e_p_r2"]["parent"], arcs["e_q_r2"]["parent"] = "q", "p"
    semi = {row["id"]: row for row in certificate["root_suppression"]["effective_semi_directed_edges"]}
    for edge_id, parent in (("e_p_r2", "q"), ("e_q_r2", "p")):
        semi[edge_id]["endpoints"][0] = parent
        semi[edge_id]["direction"][0] = parent


def swap_u_endpoints(certificate) -> None:
    arcs = {row["id"]: row for row in certificate["rooted_network"]["arcs"]}
    arcs["e_u_p"]["child"], arcs["e_u_q"]["child"] = "q", "p"
    semi = {row["id"]: row for row in certificate["root_suppression"]["effective_semi_directed_edges"]}
    semi["e_u_p"]["endpoints"][1] = "q"
    semi["e_u_q"]["endpoints"][1] = "p"


def swap_r2_id_meanings(certificate) -> None:
    arcs = {row["id"]: row for row in certificate["rooted_network"]["arcs"]}
    arcs["e_p_r2"]["id"], arcs["e_q_r2"]["id"] = "e_q_r2", "e_p_r2"
    # Keep the suppressed rows internally matched to the renamed source rows.
    semi = {row["id"]: row for row in certificate["root_suppression"]["effective_semi_directed_edges"]}
    semi["e_p_r2"]["id"], semi["e_q_r2"]["id"] = "e_q_r2", "e_p_r2"
    semi["e_p_r2"]["source_edges"] = ["e_q_r2"]
    semi["e_q_r2"]["source_edges"] = ["e_p_r2"]


for case_name, case_mutation in (
    ("duplicate_conflicting_vertex", duplicate_conflicting_vertex),
    ("duplicate_leaf_label", duplicate_leaf_label),
    ("swap_root_arc_ids", swap_root_arc_ids),
    ("swap_r2_endpoints", swap_r2_endpoints),
    ("swap_u_endpoints", swap_u_endpoints),
    ("swap_r2_id_meanings", swap_r2_id_meanings),
):
    run(case_name, case_mutation)


def run_direct_pruning_source_mutation() -> None:
    source = VERIFIER.read_text()
    old = "transitions[edge_id][parent_state ^ child_state]"
    new = "transitions[edge_id][(parent_state + child_state) % 4]"
    assert source.count(old) == 1
    with tempfile.TemporaryDirectory(prefix="v124-direct-pruning-source-") as raw:
        directory = Path(raw)
        mutant = directory / "verify_k3p.py"
        mutant.write_text(source.replace(old, new))
        result = subprocess.run(
            ["python3", str(mutant), str(MATERIALS / "certificate_k3p.json")],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=False,
        )
    lines = result.stdout.strip().splitlines()
    diagnostic = next(
        (line for line in lines if "direct K3P" in line or "AssertionError" in line),
        lines[-1] if lines else "<no output>",
    )
    print(f"direct_pruning_xor_to_cyclic: exit={result.returncode}; {diagnostic}")


run_direct_pruning_source_mutation()
