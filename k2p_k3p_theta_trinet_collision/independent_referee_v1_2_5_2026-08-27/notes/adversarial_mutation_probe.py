#!/usr/bin/env python3
"""Independent hostile-mutation probes for referee packet v1.2.5.

The probes deliberately mutate disposable JSON copies.  Packet files are never
modified.  A test passes only when the advertised verifier exits nonzero; for
the repairs inherited from the v1.2.4 review it must also emit the expected
semantic diagnostic.
"""

from __future__ import annotations

import copy
import json
from pathlib import Path
import shutil
import subprocess
import tempfile


AUDIT = Path(__file__).resolve().parents[1]
MATERIALS = (
    AUDIT
    / "packet_copy"
    / "k2p-k3p-theta-ai-referee-v1.2.5"
    / "materials"
)
K3P_VERIFIER = MATERIALS / "src" / "verify_k3p.py"
K3P_BASE = json.loads((MATERIALS / "certificate_k3p.json").read_text())
K2P_BASE = json.loads((MATERIALS / "certificate_k2p_simple.json").read_text())


def execute(command: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command,
        cwd=cwd,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
        timeout=120,
    )


def require_rejection(
    name: str,
    result: subprocess.CompletedProcess[str],
    expected: str | None = None,
) -> None:
    if result.returncode == 0:
        raise RuntimeError(f"{name}: mutated artifact unexpectedly passed")
    if expected is not None and expected not in result.stdout:
        raise RuntimeError(
            f"{name}: rejected for the wrong reason; expected {expected!r}\n"
            f"{result.stdout}"
        )
    lines = [line for line in result.stdout.splitlines() if line.strip()]
    diagnostic = next(
        (line for line in reversed(lines) if "EXACT VERIFICATION FAILED" in line),
        lines[-1] if lines else "<no output>",
    )
    print(f"PASS  {name}: {diagnostic}")


def run_k3p(name: str, mutation, expected: str | None = None) -> None:
    certificate = copy.deepcopy(K3P_BASE)
    mutation(certificate)
    safe_name = "".join(character if character.isalnum() else "-" for character in name)
    with tempfile.TemporaryDirectory(prefix=f"v125-k3p-{safe_name}-") as raw:
        directory = Path(raw)
        certificate_path = directory / "certificate_k3p.json"
        certificate_path.write_text(json.dumps(certificate, indent=2) + "\n")
        # Mirror mutated embedded sections so determinant/tangent probes cannot
        # fail early merely because a transport copy is stale.
        (directory / "jacobian_certificate_k3p.json").write_text(
            json.dumps(certificate["jacobian"], indent=2) + "\n"
        )
        (directory / "continuous_time_certificate_k3p.json").write_text(
            json.dumps(certificate["continuous_time"], indent=2) + "\n"
        )
        result = execute(["python3", str(K3P_VERIFIER), str(certificate_path)], directory)
    require_rejection(name, result, expected)


def swap_vertex(value: str) -> str:
    return {"p": "q", "q": "p"}.get(value, value)


def duplicate_conflicting_vertex(certificate) -> None:
    certificate["rooted_network"]["vertices"].insert(
        0, {"id": "rho", "type": "leaf", "label": 99}
    )


def duplicate_leaf_label(certificate) -> None:
    certificate["rooted_network"]["vertices"][-3]["label"] = 2


def swap_root_arc_ids(certificate) -> None:
    arcs = {row["id"]: row for row in certificate["rooted_network"]["arcs"]}
    arcs["e_rho_1"]["id"], arcs["e_rho_u"]["id"] = "e_rho_u", "e_rho_1"


def global_p_q_endpoint_swap(certificate) -> None:
    for row in certificate["rooted_network"]["arcs"]:
        row["parent"] = swap_vertex(row["parent"])
        row["child"] = swap_vertex(row["child"])
    for row in certificate["root_suppression"]["effective_semi_directed_edges"]:
        row["endpoints"] = [swap_vertex(x) for x in row["endpoints"]]
        if "direction" in row:
            row["direction"] = [swap_vertex(x) for x in row["direction"]]


def swap_r2_endpoints(certificate) -> None:
    arcs = {row["id"]: row for row in certificate["rooted_network"]["arcs"]}
    arcs["e_p_r2"]["parent"], arcs["e_q_r2"]["parent"] = "q", "p"
    semi = {
        row["id"]: row
        for row in certificate["root_suppression"]["effective_semi_directed_edges"]
    }
    for edge_id, parent in (("e_p_r2", "q"), ("e_q_r2", "p")):
        semi[edge_id]["endpoints"][0] = parent
        semi[edge_id]["direction"][0] = parent


def swap_u_endpoints(certificate) -> None:
    arcs = {row["id"]: row for row in certificate["rooted_network"]["arcs"]}
    arcs["e_u_p"]["child"], arcs["e_u_q"]["child"] = "q", "p"
    semi = {
        row["id"]: row
        for row in certificate["root_suppression"]["effective_semi_directed_edges"]
    }
    semi["e_u_p"]["endpoints"][1] = "q"
    semi["e_u_q"]["endpoints"][1] = "p"


def swap_r2_id_meanings(certificate) -> None:
    arcs = {row["id"]: row for row in certificate["rooted_network"]["arcs"]}
    arcs["e_p_r2"]["id"], arcs["e_q_r2"]["id"] = "e_q_r2", "e_p_r2"
    semi = {
        row["id"]: row
        for row in certificate["root_suppression"]["effective_semi_directed_edges"]
    }
    semi["e_p_r2"]["id"], semi["e_q_r2"]["id"] = "e_q_r2", "e_p_r2"
    semi["e_p_r2"]["source_edges"] = ["e_q_r2"]
    semi["e_q_r2"]["source_edges"] = ["e_p_r2"]


def contradict_retic_parent(certificate) -> None:
    certificate["rooted_network"]["reticulations"][0]["incoming"][0]["parent"] = "q"


def contradict_retic_choice(certificate) -> None:
    certificate["rooted_network"]["reticulations"][0]["incoming"][0]["choice"] = "q"


def swap_arc_vector_name(certificate) -> None:
    certificate["rooted_network"]["arcs"][2]["vector_name"] = "V"


def add_arc_field(certificate) -> None:
    certificate["rooted_network"]["arcs"][0]["unverified"] = True


def corrupt_suppressed_vector_name(certificate) -> None:
    certificate["root_suppression"]["effective_semi_directed_edges"][0][
        "vector_name"
    ] = "K"


def corrupt_arc_eigen(certificate) -> None:
    certificate["rooted_network"]["arcs"][2]["eigen"][1][0] = "999"


def corrupt_fourier_coordinate(certificate) -> None:
    certificate["fourier_coordinates"]["network"][5][0] = "999"


def corrupt_leaf_pattern(certificate) -> None:
    certificate["leaf_pattern_probabilities"]["network"][0][0] = "999"


def corrupt_jacobian_entry(certificate) -> None:
    certificate["jacobian"]["matrix"][0][0] = ["1", "0", "0", "0"]


def corrupt_pivot_tangent(certificate) -> None:
    certificate["continuous_time"]["pivot_derivatives"][0]["value"][0] = "1"


K3P_CASES = (
    ("duplicate conflicting vertex", duplicate_conflicting_vertex, "duplicate vertex identifier"),
    ("duplicate leaf label", duplicate_leaf_label, "canonical ordered vertex schema"),
    ("root-arc ID swap", swap_root_arc_ids, "canonical rooted arc ID/endpoint/vector map"),
    ("coordinated p/q endpoint swap", global_p_q_endpoint_swap, "canonical rooted arc ID/endpoint/vector map"),
    ("r2 parent-endpoint swap", swap_r2_endpoints, "canonical rooted arc ID/endpoint/vector map"),
    ("u-child endpoint swap", swap_u_endpoints, "canonical rooted arc ID/endpoint/vector map"),
    ("r2 arc-ID meaning swap", swap_r2_id_meanings, "canonical rooted arc ID/endpoint/vector map"),
    ("reticulation parent contradiction", contradict_retic_parent, "reticulation descriptor parent for e_p_r2"),
    ("reticulation choice contradiction", contradict_retic_choice, "reticulation descriptor choice for e_p_r2"),
    ("rooted arc vector-name swap", swap_arc_vector_name, "canonical rooted arc ID/endpoint/vector map"),
    ("unexpected rooted arc field", add_arc_field, "closed rooted arc row schema"),
    ("suppressed K-odot-K vector name", corrupt_suppressed_vector_name, "suppressed edge vector name"),
    ("operative arc eigenvalue", corrupt_arc_eigen, None),
    ("stored collision coordinate", corrupt_fourier_coordinate, None),
    ("stored ordinary-state pattern", corrupt_leaf_pattern, None),
    ("stored Jacobian entry", corrupt_jacobian_entry, None),
    ("stored fixed-output pivot tangent", corrupt_pivot_tangent, "linearized fixed-output identity"),
)


def run_direct_pruning_source_mutation() -> None:
    source = K3P_VERIFIER.read_text()
    old = "transitions[edge_id][parent_state ^ child_state]"
    new = "transitions[edge_id][(parent_state + child_state) % 4]"
    if source.count(old) != 1:
        raise RuntimeError("direct-pruning source pattern changed unexpectedly")
    with tempfile.TemporaryDirectory(prefix="v125-direct-pruning-") as raw:
        directory = Path(raw)
        mutant = directory / "verify_k3p_mutated.py"
        mutant.write_text(source.replace(old, new))
        result = execute(
            ["python3", str(mutant), str(MATERIALS / "certificate_k3p.json")],
            directory,
        )
    require_rejection("direct pruning XOR changed to cyclic addition", result, "direct K3P")


def run_k2p_transition_rows() -> None:
    cases: list[tuple[str, str, str]] = []
    for name in K2P_BASE["network_transition_probabilities"]:
        cases.append(("network", name, f"{name} stored transition row"))
    for name in K2P_BASE["comparison_tree"]["transition_probabilities"]:
        cases.append(("tree", name, f"{name} stored tree transition row"))
    for section, name, expected in cases:
        certificate = copy.deepcopy(K2P_BASE)
        if section == "network":
            rows = certificate["network_transition_probabilities"]
        else:
            rows = certificate["comparison_tree"]["transition_probabilities"]
        rows[name][0][0] = "999"
        with tempfile.TemporaryDirectory(prefix=f"v125-k2p-{section}-{name}-") as raw:
            directory = Path(raw)
            shutil.copy2(MATERIALS / "verify_k2p_simple.py", directory)
            (directory / "certificate_k2p_simple.json").write_text(
                json.dumps(certificate, indent=2) + "\n"
            )
            result = execute(["python3", "verify_k2p_simple.py"], directory)
        require_rejection(f"compact K2P {section} row {name}", result, expected)


def main() -> None:
    for name, mutation, expected in K3P_CASES:
        run_k3p(name, mutation, expected)
    run_direct_pruning_source_mutation()
    run_k2p_transition_rows()
    print("ALL INDEPENDENT HOSTILE MUTATION PROBES PASSED")


if __name__ == "__main__":
    main()
