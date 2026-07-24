#!/usr/bin/env python3
"""Run the preregistered SMS validation suite and bounded order-43 pilot."""

from __future__ import annotations

import argparse
import ast
import hashlib
import itertools
import json
import os
import subprocess
import sys
import time
from pathlib import Path

from graph_io import encode_graph6


ROOT = Path(__file__).resolve().parents[1]


def resolve(path: str) -> Path:
    value = Path(path)
    return value if value.is_absolute() else ROOT / value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_json(path: Path, value: object) -> str:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, sort_keys=True, indent=2) + "\n",
        encoding="utf-8",
    )
    return sha256(path)


def run(
    command: list[str],
    *,
    environment: dict[str, str],
    timeout: float,
) -> dict[str, object]:
    started = time.monotonic()
    try:
        completed = subprocess.run(
            command,
            cwd=ROOT,
            env=environment,
            text=True,
            capture_output=True,
            check=False,
            timeout=timeout,
        )
        return {
            "command": command,
            "returncode": completed.returncode,
            "outer_timeout": False,
            "wall_seconds": time.monotonic() - started,
            "stdout": completed.stdout,
            "stderr": completed.stderr,
        }
    except subprocess.TimeoutExpired as error:
        stdout = error.stdout or ""
        stderr = error.stderr or ""
        if isinstance(stdout, bytes):
            stdout = stdout.decode("utf-8", "replace")
        if isinstance(stderr, bytes):
            stderr = stderr.decode("utf-8", "replace")
        return {
            "command": command,
            "returncode": None,
            "outer_timeout": True,
            "wall_seconds": time.monotonic() - started,
            "stdout": stdout,
            "stderr": stderr,
        }


def parse_edge_list(stdout: str) -> list[tuple[int, int]]:
    for line in stdout.splitlines():
        if not line.startswith("[") or not line.endswith("]"):
            continue
        value = ast.literal_eval(line)
        if isinstance(value, list):
            return [tuple(edge) for edge in value]
    raise ValueError("solver output contains no edge-list model")


def inspect_graph(
    edges: list[tuple[int, int]],
    *,
    order: int,
    forbidden_size: int,
    degree_lower: int,
    degree_upper: int,
) -> tuple[dict[str, object], list[int]]:
    normalized: set[tuple[int, int]] = set()
    adjacency = [0] * order
    for value in edges:
        if (
            len(value) != 2
            or not all(isinstance(vertex, int) for vertex in value)
        ):
            raise ValueError("malformed model edge")
        left, right = sorted(value)
        if not 0 <= left < right < order or (left, right) in normalized:
            raise ValueError("model is not a simple graph")
        normalized.add((left, right))
        adjacency[left] |= 1 << right
        adjacency[right] |= 1 << left
    degrees = [neighbors.bit_count() for neighbors in adjacency]
    clique_count = 0
    independent_count = 0
    for vertices in itertools.combinations(range(order), forbidden_size):
        edge_count = sum(
            int((adjacency[left] >> right) & 1)
            for left, right in itertools.combinations(vertices, 2)
        )
        pair_count = forbidden_size * (forbidden_size - 1) // 2
        clique_count += edge_count == pair_count
        independent_count += edge_count == 0
    valid = (
        all(degree_lower <= degree <= degree_upper for degree in degrees)
        and clique_count == 0
        and independent_count == 0
    )
    return (
        {
            "valid": valid,
            "order": order,
            "edge_count": len(normalized),
            "degree_sequence": sorted(degrees),
            "degree_bounds_valid": all(
                degree_lower <= degree <= degree_upper for degree in degrees
            ),
            "clique_count": clique_count,
            "independent_count": independent_count,
            "objective": clique_count + independent_count,
        },
        adjacency,
    )


def symmetry_check(
    path: Path, order: int, output: Path
) -> dict[str, object]:
    completed = subprocess.run(
        [
            sys.executable,
            "verify/sms_symmetry_clauses_check.py",
            str(path),
            "--order",
            str(order),
            "--output",
            str(output),
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
        timeout=120,
    )
    try:
        result = json.loads(completed.stdout)
    except json.JSONDecodeError:
        result = {
            "valid": False,
            "error": "symmetry checker did not emit JSON",
            "stdout": completed.stdout,
            "stderr": completed.stderr,
        }
    result["returncode"] = completed.returncode
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--plan", type=Path, required=True)
    args = parser.parse_args()
    plan = json.loads(args.plan.read_text(encoding="utf-8"))
    if plan["status"] != "PREREGISTERED_BEFORE_ORDER43_PILOT":
        raise SystemExit("plan status does not authorize a production pilot")
    for record in plan["pinned_files"]:
        path = resolve(record["path"])
        if sha256(path) != record["sha256"]:
            raise SystemExit(f"pinned hash mismatch: {path}")

    results_dir = resolve(plan["results_dir"])
    results_dir.mkdir(parents=True, exist_ok=True)
    binary = str(resolve(plan["solver"]["binary"]))
    environment = os.environ.copy()
    environment["DYLD_LIBRARY_PATH"] = plan["solver"]["dyld_library_path"]

    # Enumerate all unlabeled order-four graphs.  This deliberately exercises
    # dynamic symmetry clause production and its permutation-witness audit.
    n4_symmetry = results_dir / "validation_n4_symmetry.json"
    n4_run = run(
        [
            binary,
            "-v",
            "4",
            "--dimacs",
            plan["validation"]["n4_cnf"],
            "--all-graphs",
            "--hide-graphs",
            "--cutoff",
            "0",
            "--frequency",
            "1",
            "--sym-break-clauses",
            str(n4_symmetry),
        ],
        environment=environment,
        timeout=30,
    )
    n4_symmetry_result = symmetry_check(
        n4_symmetry,
        4,
        results_dir / "validation_n4_symmetry.check.json",
    )
    n4_valid = (
        n4_run["returncode"] == 20
        and not n4_run["outer_timeout"]
        and "Number of graphs: 11" in str(n4_run["stdout"])
        and n4_symmetry_result.get("valid") is True
        and n4_symmetry_result.get("symmetry_clause_count") == 11
    )
    n4_result = {
        **n4_run,
        "expected_unlabeled_graph_count": 11,
        "symmetry_check": n4_symmetry_result,
        "valid": n4_valid,
    }
    write_json(results_dir / "validation_n4_result.json", n4_result)
    if not n4_valid:
        raise RuntimeError("order-four symmetry validation failed")

    # R(3,3)>5: obtain and directly inspect a C5 model with standard SMS.
    n5_symmetry = results_dir / "validation_r33_n5_symmetry.json"
    n5_run = run(
        [
            binary,
            "-v",
            "5",
            "--dimacs",
            plan["validation"]["n5_cnf"],
            "--cutoff",
            "0",
            "--frequency",
            "1",
            "--sym-break-clauses",
            str(n5_symmetry),
        ],
        environment=environment,
        timeout=30,
    )
    n5_edges = parse_edge_list(str(n5_run["stdout"]))
    n5_graph, _ = inspect_graph(
        n5_edges,
        order=5,
        forbidden_size=3,
        degree_lower=2,
        degree_upper=2,
    )
    n5_symmetry_result = symmetry_check(
        n5_symmetry,
        5,
        results_dir / "validation_r33_n5_symmetry.check.json",
    )
    n5_valid = (
        n5_run["returncode"] == 10
        and not n5_run["outer_timeout"]
        and n5_graph["valid"]
        and n5_symmetry_result.get("valid") is True
    )
    n5_result = {
        **n5_run,
        "model_edges": [list(edge) for edge in n5_edges],
        "model_check": n5_graph,
        "symmetry_check": n5_symmetry_result,
        "valid": n5_valid,
    }
    write_json(results_dir / "validation_r33_n5_result.json", n5_result)
    if not n5_valid:
        raise RuntimeError("R(3,3;5) SAT validation failed")

    # R(3,3)=6: turn SMS off so the LRAT proves the original CNF directly.
    n6_lrat = results_dir / "validation_r33_n6_nosms.lrat"
    n6_run = run(
        [
            binary,
            "-v",
            "6",
            "--dimacs",
            plan["validation"]["n6_cnf"],
            "--no-SMS",
            "--lrat-output",
            str(n6_lrat),
            "--cadical-config",
            "binary=0",
        ],
        environment=environment,
        timeout=30,
    )
    lrat_check = run(
        [
            str(resolve(plan["validation"]["lrat_checker"])),
            plan["validation"]["n6_cnf"],
            str(n6_lrat),
        ],
        environment=environment,
        timeout=30,
    )
    n6_valid = (
        n6_run["returncode"] == 20
        and not n6_run["outer_timeout"]
        and lrat_check["returncode"] == 0
        and "VERIFIED" in str(lrat_check["stdout"])
        and "NOT VERIFIED" not in str(lrat_check["stdout"])
    )
    n6_result = {
        **n6_run,
        "lrat_path": str(n6_lrat.relative_to(ROOT)),
        "lrat_sha256": sha256(n6_lrat),
        "lrat_bytes": n6_lrat.stat().st_size,
        "lrat_check": lrat_check,
        "valid": n6_valid,
    }
    write_json(results_dir / "validation_r33_n6_result.json", n6_result)
    if not n6_valid:
        raise RuntimeError("R(3,3;6) proof validation failed")

    # Bounded global pilot.  A finite minimality cutoff may skip symmetry
    # checks, but every emitted lex-leader clause remains witness-auditable.
    pilot = plan["pilot"]
    pilot_symmetry = results_dir / "order43_pilot_symmetry.json"
    pilot_run = run(
        [
            binary,
            "-v",
            "43",
            "--dimacs",
            pilot["cnf"],
            "--cutoff",
            str(pilot["minimality_cutoff"]),
            "--frequency",
            str(pilot["minimality_frequency"]),
            "--timeout",
            str(pilot["internal_timeout_seconds"]),
            "--sym-break-clauses",
            str(pilot_symmetry),
        ],
        environment=environment,
        timeout=float(pilot["outer_timeout_seconds"]),
    )
    pilot_symmetry_result = symmetry_check(
        pilot_symmetry,
        43,
        results_dir / "order43_pilot_symmetry.check.json",
    )
    returncode = pilot_run["returncode"]
    if pilot_run["outer_timeout"]:
        status = "EXTERNAL_TIMEOUT_UNKNOWN"
    elif returncode == 0:
        status = "INTERNAL_TIMEOUT_UNKNOWN"
    elif returncode == 10:
        status = "SAT"
    elif returncode == 20:
        status = "UNVERIFIED_SOLVER_UNSAT"
    else:
        status = "ERROR"

    candidate: dict[str, object] | None = None
    if status == "SAT":
        edges = parse_edge_list(str(pilot_run["stdout"]))
        model_check, adjacency = inspect_graph(
            edges,
            order=43,
            forbidden_size=5,
            degree_lower=18,
            degree_upper=24,
        )
        graph6 = encode_graph6(adjacency)
        graph_path = results_dir / "order43_sms_candidate.g6"
        graph_path.write_text(graph6 + "\n", encoding="ascii")
        python_verify = run(
            [sys.executable, "verify/exhaustive_verify.py", str(graph_path)],
            environment=environment,
            timeout=120,
        )
        cpp_verify = run(
            ["build/bitset_verify", str(graph_path)],
            environment=environment,
            timeout=120,
        )
        candidate = {
            "graph6_path": str(graph_path.relative_to(ROOT)),
            "graph6_sha256": sha256(graph_path),
            "direct_model_check": model_check,
            "python_verifier": python_verify,
            "cpp_verifier": cpp_verify,
        }

    if status == "SAT" and candidate is not None:
        certified = (
            candidate["direct_model_check"]["valid"]
            and json.loads(candidate["python_verifier"]["stdout"])["valid"]
            and json.loads(candidate["cpp_verifier"]["stdout"])["valid"]
        )
    else:
        certified = False
    result = {
        "schema": "ramsey55.sms_global_pilot_result.v1",
        "status": status,
        "evidence_label": (
            "CERTIFIED"
            if certified
            else "REPRODUCIBLE COMPUTATIONAL OBSERVATION"
        ),
        "claim_boundary": (
            "Only an independently verified SAT graph is a certified "
            "construction. An UNSAT return has no mathematical force without "
            "a complete independently checked proof covering symmetry "
            "reasoning. Timeout/unknown is neither SAT nor UNSAT."
        ),
        "plan": str(args.plan),
        "plan_sha256": sha256(args.plan),
        "solver_run": pilot_run,
        "symmetry_check": pilot_symmetry_result,
        "candidate": candidate,
        "certified_construction": certified,
        "small_order_validation": {
            "all_order4_unlabeled_graphs": True,
            "R33_order5_sat_model": True,
            "R33_order6_unsat_lrat_verified": True,
        },
    }
    write_json(results_dir / "order43_pilot_result.json", result)
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
