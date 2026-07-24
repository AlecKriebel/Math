#!/usr/bin/env python3
"""Deterministic exact completion under a partial residual-LNS assignment.

Candidate values are materialized as sorted unit clauses in a new CNF.  The
remaining variables stay free.  A pinned PySAT/Glucose3 worker produces a SAT
model or DRAT trace; UNSAT is called certified only after both drat-trim and
lrat-check independently accept the proof chain.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import os
import subprocess
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Mapping, Sequence

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from extension_sat_solver import parse_dimacs  # noqa: E402
from graph_io import decode_graph6, encode_graph6, read_graph, validate_simple  # noqa: E402
from residual_lns_sat import apply_assignment, count_forbidden_sets  # noqa: E402


WORKFLOW_ID = "ramsey55_residual_partial_assignment_completion_v1"
ASSUMPTION_CNF_ID = "ramsey55_materialized_candidate_units_v1"

DEFAULT_PYTHON = Path("/opt/homebrew/opt/python@3.11/bin/python3.11")
DEFAULT_PYSAT_PATH = Path("/tmp/ramsey55-pysat.4YSXId")
DEFAULT_DRAT_TRIM = Path("/tmp/ramsey55-drat-trim.x3nb3p/src/drat-trim")
DEFAULT_LRAT_CHECK = Path("/tmp/ramsey55-drat-trim.x3nb3p/src/lrat-check")

PINNED_HASHES = {
    "python": "831365631dac62f232a720858703d0b2ddca5eed33e0a51986cf06aac9d38bc0",
    "pysat_solvers_py": "253654d8efabae650a0d136ad2f2e6d30b57206b1fb70846c714197468a28f7e",
    "pysolvers_extension": "e9828032a114da49429305e5afcf58db259034687a9c098c996da65e5e099ded",
    "drat_trim": "f58f63b0f76945d4c4c9ff6e87afaf870f579e67c0f7cca589492df8fc7ebd47",
    "lrat_check": "bd7eb8052623525814a0a37502b47f05375d9d9dfaf96ddc2fcd858958517cea",
}
PINNED_PYSAT_VERSION = "1.9.dev7"
PINNED_DRAT_TRIM_COMMIT = "2e3b2dc0ecf938addbd779d42877b6ed69d9a985"


class WorkflowError(ValueError):
    pass


@dataclass(frozen=True)
class Candidate:
    assignment: tuple[bool, ...]
    source_path: Path
    source_sha256: str
    assignment_sha256: str
    graph6: str | None
    fixed_boundary_mismatch_count: int | None


@dataclass(frozen=True)
class Toolchain:
    python: Path
    pysat_path: Path
    drat_trim: Path
    lrat_check: Path
    hashes: Mapping[str, str]


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def parse_variable_csv(text: str) -> tuple[int, ...]:
    if not text:
        return ()
    try:
        values = tuple(int(field) for field in text.split(","))
    except ValueError as error:
        raise argparse.ArgumentTypeError("variables must be comma-separated integers") from error
    if len(values) != len(set(values)):
        raise argparse.ArgumentTypeError("variable list contains duplicates")
    return tuple(sorted(values))


def validate_variables(
    variables: Iterable[int], variable_count: int
) -> tuple[int, ...]:
    values = tuple(sorted(set(variables)))
    if any(not 1 <= variable <= variable_count for variable in values):
        raise WorkflowError(
            f"variable selection must be inside 1..{variable_count}"
        )
    return values


def load_metadata(path: Path, cnf_path: Path) -> dict[str, object]:
    metadata = json.loads(path.read_text(encoding="utf-8"))
    required = {
        "cnf_sha256",
        "variable_count",
        "free_edges",
        "base_graph6",
        "order",
    }
    missing = required - metadata.keys()
    if missing:
        raise WorkflowError(f"metadata is missing fields: {sorted(missing)}")
    actual_hash = sha256_file(cnf_path)
    if metadata["cnf_sha256"] != actual_hash:
        raise WorkflowError("base CNF hash does not match its metadata")
    variable_count, _ = parse_dimacs(cnf_path)
    if metadata["variable_count"] != variable_count:
        raise WorkflowError("base CNF variable count does not match metadata")
    free_edges = metadata["free_edges"]
    if not isinstance(free_edges, list) or len(free_edges) != variable_count:
        raise WorkflowError("metadata free-edge map has the wrong length")
    return metadata


def assignment_digest(assignment: Sequence[bool]) -> str:
    return hashlib.sha256(
        bytes(1 if value else 0 for value in assignment)
    ).hexdigest()


def _graph_assignment(
    adjacency: list[int],
    metadata: Mapping[str, object],
) -> tuple[tuple[bool, ...], int]:
    order = int(metadata["order"])
    if len(adjacency) != order:
        raise WorkflowError(
            f"candidate graph has order {len(adjacency)}, expected {order}"
        )
    validate_simple(adjacency)
    free_edges = tuple(
        (int(edge[0]), int(edge[1])) for edge in metadata["free_edges"]  # type: ignore[index]
    )
    assignment = tuple(
        bool((adjacency[left] >> right) & 1) for left, right in free_edges
    )
    free_set = set(free_edges)
    base = decode_graph6(str(metadata["base_graph6"]))
    mismatches = sum(
        ((adjacency[left] >> right) & 1) != ((base[left] >> right) & 1)
        for left, right in itertools.combinations(range(order), 2)
        if (left, right) not in free_set
    )
    return assignment, mismatches


def load_candidate(
    path: Path,
    metadata: Mapping[str, object],
    variable_count: int,
) -> Candidate:
    raw = path.read_bytes()
    source_hash = hashlib.sha256(raw).hexdigest()
    graph6: str | None = None
    mismatches: int | None = None

    if path.suffix.lower() == ".json":
        data = json.loads(raw.decode("utf-8"))
        if "graph6" in data:
            adjacency = decode_graph6(str(data["graph6"]))
            assignment, mismatches = _graph_assignment(adjacency, metadata)
            graph6 = encode_graph6(adjacency)
        elif "assignment" in data:
            values = data["assignment"]
            if (
                not isinstance(values, list)
                or len(values) != variable_count
                or any(type(value) is not bool for value in values)
            ):
                raise WorkflowError(
                    "candidate JSON assignment must be a full Boolean list"
                )
            assignment = tuple(values)
        else:
            keys = (
                "true_variables",
                "best_true_variables",
                "base_true_variables",
            )
            selected_key = next((key for key in keys if key in data), None)
            if selected_key is None:
                raise WorkflowError(
                    "candidate JSON needs graph6, assignment, or true_variables"
                )
            true_variables = validate_variables(
                data[selected_key], variable_count
            )
            true_set = set(true_variables)
            assignment = tuple(
                variable in true_set
                for variable in range(1, variable_count + 1)
            )
    else:
        adjacency = read_graph(path)
        assignment, mismatches = _graph_assignment(adjacency, metadata)
        graph6 = encode_graph6(adjacency)

    if len(assignment) != variable_count:
        raise WorkflowError("candidate assignment has the wrong length")
    if mismatches:
        raise WorkflowError(
            f"candidate changes {mismatches} edges outside the 237-variable boundary"
        )
    return Candidate(
        assignment=assignment,
        source_path=path,
        source_sha256=source_hash,
        assignment_sha256=assignment_digest(assignment),
        graph6=graph6,
        fixed_boundary_mismatch_count=mismatches,
    )


def unsatisfied_clause_indices(
    clauses: Sequence[Sequence[int]], assignment: Sequence[bool]
) -> tuple[int, ...]:
    return tuple(
        index
        for index, clause in enumerate(clauses, start=1)
        if not any(
            assignment[abs(literal) - 1] == (literal > 0)
            for literal in clause
        )
    )


def select_fixed_variables(
    variable_count: int,
    clauses: Sequence[Sequence[int]],
    assignment: Sequence[bool],
    *,
    mode: str,
    explicit_variables: Iterable[int] = (),
) -> tuple[tuple[int, ...], tuple[int, ...], tuple[int, ...]]:
    all_variables = set(range(1, variable_count + 1))
    explicit = set(validate_variables(explicit_variables, variable_count))
    conflicts = unsatisfied_clause_indices(clauses, assignment)
    if mode == "conflict-union":
        free = {
            abs(literal)
            for clause_index in conflicts
            for literal in clauses[clause_index - 1]
        }
        fixed = all_variables - free
    elif mode == "explicit-fixed":
        fixed = explicit
        free = all_variables - fixed
    elif mode == "explicit-free":
        free = explicit
        fixed = all_variables - free
    elif mode == "all-free":
        fixed = set()
        free = all_variables
    elif mode == "all-fixed":
        fixed = all_variables
        free = set()
    else:
        raise WorkflowError(f"unknown selection mode {mode}")
    return tuple(sorted(fixed)), tuple(sorted(free)), conflicts


def render_completion_cnf(
    variable_count: int,
    base_clauses: Sequence[Sequence[int]],
    fixed_variables: Sequence[int],
    assignment: Sequence[bool],
    *,
    base_cnf_sha256: str,
    candidate_assignment_sha256: str,
    selection_mode: str,
) -> str:
    units = tuple(
        variable if assignment[variable - 1] else -variable
        for variable in fixed_variables
    )
    lines = [
        f"c generator {ASSUMPTION_CNF_ID}",
        f"c base_cnf_sha256 {base_cnf_sha256}",
        f"c candidate_assignment_sha256 {candidate_assignment_sha256}",
        f"c selection_mode {selection_mode}",
        f"c fixed_variable_count {len(fixed_variables)}",
        f"c free_variable_count {variable_count - len(fixed_variables)}",
        "c original clauses first, then sorted candidate-value unit clauses",
        f"p cnf {variable_count} {len(base_clauses) + len(units)}",
    ]
    lines.extend(
        " ".join(map(str, clause)) + (" " if clause else "") + "0"
        for clause in base_clauses
    )
    lines.extend(f"{literal} 0" for literal in units)
    return "\n".join(lines) + "\n"


def verify_toolchain(toolchain: Toolchain) -> dict[str, object]:
    paths = {
        "python": toolchain.python,
        "pysat_solvers_py": toolchain.pysat_path / "pysat" / "solvers.py",
        "pysolvers_extension": (
            toolchain.pysat_path / "pysolvers.cpython-311-darwin.so"
        ),
        "drat_trim": toolchain.drat_trim,
        "lrat_check": toolchain.lrat_check,
    }
    observed: dict[str, str] = {}
    for name, path in paths.items():
        if not path.is_file():
            raise WorkflowError(f"required pinned tool is missing: {path}")
        observed[name] = sha256_file(path)
        expected = toolchain.hashes[name]
        if observed[name] != expected:
            raise WorkflowError(
                f"pinned tool hash mismatch for {name}: "
                f"{observed[name]} != {expected}"
            )
    return {
        "python_path": str(toolchain.python),
        "pysat_path": str(toolchain.pysat_path),
        "drat_trim_path": str(toolchain.drat_trim),
        "lrat_check_path": str(toolchain.lrat_check),
        "pysat_version": PINNED_PYSAT_VERSION,
        "drat_trim_commit": PINNED_DRAT_TRIM_COMMIT,
        "sha256": observed,
    }


def run_bounded(
    command: Sequence[str],
    *,
    timeout: float,
    environment: Mapping[str, str] | None = None,
) -> tuple[str, subprocess.CompletedProcess[str] | None, float]:
    started = time.monotonic()
    try:
        completed = subprocess.run(
            list(command),
            text=True,
            capture_output=True,
            check=False,
            timeout=timeout,
            env=dict(environment) if environment is not None else None,
        )
    except subprocess.TimeoutExpired:
        return "TIMEOUT", None, time.monotonic() - started
    return "COMPLETED", completed, time.monotonic() - started


def parse_single_json_line(stdout: str) -> dict[str, object]:
    lines = [line for line in stdout.splitlines() if line.strip()]
    if len(lines) != 1:
        raise WorkflowError("solver worker did not emit exactly one JSON line")
    value = json.loads(lines[0])
    if not isinstance(value, dict):
        raise WorkflowError("solver worker JSON is not an object")
    return value


def checker_says_verified(output: str) -> bool:
    return any(
        "VERIFIED" in line and "NOT VERIFIED" not in line
        for line in output.splitlines()
    )


def check_formula_model(
    clauses: Sequence[Sequence[int]], true_variables: Iterable[int]
) -> bool:
    true_set = set(true_variables)
    return all(
        any((literal > 0) == (abs(literal) in true_set) for literal in clause)
        for clause in clauses
    )


def write_json(path: Path, value: Mapping[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, sort_keys=True, indent=2) + "\n",
        encoding="utf-8",
    )


def _remove_stale(paths: Iterable[Path | None]) -> None:
    for path in paths:
        if path is not None:
            path.unlink(missing_ok=True)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-cnf", type=Path, required=True)
    parser.add_argument("--base-metadata", type=Path, required=True)
    parser.add_argument("--candidate", type=Path, required=True)
    selection = parser.add_mutually_exclusive_group()
    selection.add_argument("--fix-variables", type=parse_variable_csv)
    selection.add_argument("--leave-free-variables", type=parse_variable_csv)
    selection.add_argument("--all-free", action="store_true")
    selection.add_argument("--all-fixed", action="store_true")
    parser.add_argument("--completion-cnf", type=Path, required=True)
    parser.add_argument("--proof", type=Path, required=True)
    parser.add_argument("--lrat", type=Path, required=True)
    parser.add_argument("--result", type=Path, required=True)
    parser.add_argument("--model-graph", type=Path)
    parser.add_argument("--time-limit", type=float, default=60.0)
    parser.add_argument("--proof-check-time-limit", type=float, default=600.0)
    parser.add_argument("--python", type=Path, default=DEFAULT_PYTHON)
    parser.add_argument("--pysat-path", type=Path, default=DEFAULT_PYSAT_PATH)
    parser.add_argument("--drat-trim", type=Path, default=DEFAULT_DRAT_TRIM)
    parser.add_argument("--lrat-check", type=Path, default=DEFAULT_LRAT_CHECK)
    args = parser.parse_args()
    if args.time_limit <= 0 or args.proof_check_time_limit <= 0:
        raise SystemExit("time limits must be positive")

    toolchain = Toolchain(
        python=args.python,
        pysat_path=args.pysat_path,
        drat_trim=args.drat_trim,
        lrat_check=args.lrat_check,
        hashes=PINNED_HASHES,
    )
    tool_metadata = verify_toolchain(toolchain)
    metadata = load_metadata(args.base_metadata, args.base_cnf)
    variable_count, base_clauses = parse_dimacs(args.base_cnf)
    candidate = load_candidate(args.candidate, metadata, variable_count)

    if args.fix_variables is not None:
        mode = "explicit-fixed"
        explicit = args.fix_variables
    elif args.leave_free_variables is not None:
        mode = "explicit-free"
        explicit = args.leave_free_variables
    elif args.all_free:
        mode = "all-free"
        explicit = ()
    elif args.all_fixed:
        mode = "all-fixed"
        explicit = ()
    else:
        mode = "conflict-union"
        explicit = ()

    fixed, free, candidate_conflicts = select_fixed_variables(
        variable_count,
        base_clauses,
        candidate.assignment,
        mode=mode,
        explicit_variables=explicit,
    )
    base_cnf_sha256 = sha256_file(args.base_cnf)
    rendered = render_completion_cnf(
        variable_count,
        base_clauses,
        fixed,
        candidate.assignment,
        base_cnf_sha256=base_cnf_sha256,
        candidate_assignment_sha256=candidate.assignment_sha256,
        selection_mode=mode,
    )
    args.completion_cnf.parent.mkdir(parents=True, exist_ok=True)
    args.completion_cnf.write_text(rendered, encoding="ascii", newline="\n")
    completion_sha256 = hashlib.sha256(rendered.encode("ascii")).hexdigest()
    _, completion_clauses = parse_dimacs(args.completion_cnf)

    _remove_stale((args.proof, args.lrat, args.model_graph))
    base_result: dict[str, object] = {
        "workflow": WORKFLOW_ID,
        "base_cnf_path": str(args.base_cnf.resolve()),
        "base_cnf_sha256": base_cnf_sha256,
        "base_metadata_path": str(args.base_metadata.resolve()),
        "candidate_path": str(candidate.source_path.resolve()),
        "candidate_sha256": candidate.source_sha256,
        "candidate_assignment_sha256": candidate.assignment_sha256,
        "candidate_graph6": candidate.graph6,
        "candidate_fixed_boundary_mismatch_count": (
            candidate.fixed_boundary_mismatch_count
        ),
        "candidate_unsatisfied_clause_count": len(candidate_conflicts),
        "candidate_unsatisfied_clause_indices": list(candidate_conflicts),
        "selection_mode": mode,
        "fixed_variable_count": len(fixed),
        "fixed_variables": list(fixed),
        "free_variable_count": len(free),
        "free_variables": list(free),
        "completion_cnf_path": str(args.completion_cnf.resolve()),
        "completion_cnf_sha256": completion_sha256,
        "completion_variable_count": variable_count,
        "base_clause_count": len(base_clauses),
        "assumption_unit_count": len(fixed),
        "completion_clause_count": len(completion_clauses),
        "time_limit_seconds": args.time_limit,
        "proof_check_time_limit_seconds": args.proof_check_time_limit,
        "toolchain": tool_metadata,
    }

    environment = os.environ.copy()
    environment.update(
        {
            "PYTHONPATH": str(toolchain.pysat_path),
            "PYTHONHASHSEED": "0",
            "LC_ALL": "C",
        }
    )
    worker = ROOT / "src" / "residual_completion_glucose.py"
    solver_command = (
        str(toolchain.python),
        str(worker),
        str(args.completion_cnf),
        "--proof",
        str(args.proof),
    )
    run_state, completed, solver_wall = run_bounded(
        solver_command,
        timeout=args.time_limit,
        environment=environment,
    )
    if run_state == "TIMEOUT":
        _remove_stale((args.proof, args.lrat, args.model_graph))
        result = {
            **base_result,
            "status": "TIMEOUT",
            "solver_wall_seconds": solver_wall,
            "proof_written": False,
            "lrat_written": False,
            "model_written": False,
        }
        write_json(args.result, result)
        print(json.dumps(result, sort_keys=True))
        return 2

    assert completed is not None
    if completed.returncode not in {10, 20}:
        raise WorkflowError(
            "solver worker failed: "
            f"exit={completed.returncode} stderr={completed.stderr.strip()}"
        )
    solver_result = parse_single_json_line(completed.stdout)
    if solver_result.get("pysat_version") != PINNED_PYSAT_VERSION:
        raise WorkflowError("solver worker loaded an unexpected PySAT version")
    if solver_result.get("cnf_sha256") != completion_sha256:
        raise WorkflowError("solver worker solved a different CNF")

    if completed.returncode == 10:
        true_variables = validate_variables(
            solver_result.get("true_variables", []), variable_count
        )
        if not check_formula_model(completion_clauses, true_variables):
            raise WorkflowError("reported SAT model does not satisfy completion CNF")
        true_set = set(true_variables)
        assignment = tuple(
            variable in true_set for variable in range(1, variable_count + 1)
        )
        base_graph = decode_graph6(str(metadata["base_graph6"]))
        free_edges = tuple(
            (int(edge[0]), int(edge[1]))
            for edge in metadata["free_edges"]  # type: ignore[index]
        )
        model_adjacency = apply_assignment(base_graph, free_edges, assignment)
        forbidden = count_forbidden_sets(model_adjacency)
        if forbidden != (0, 0):
            raise WorkflowError(
                "SAT model reconstructs a graph with forbidden five-sets"
            )
        model_graph6 = encode_graph6(model_adjacency)
        model_sha256: str | None = None
        if args.model_graph:
            args.model_graph.parent.mkdir(parents=True, exist_ok=True)
            args.model_graph.write_text(model_graph6 + "\n", encoding="ascii")
            model_sha256 = sha256_file(args.model_graph)
        _remove_stale((args.proof, args.lrat))
        result = {
            **base_result,
            "status": "SAT",
            "solver_wall_seconds": solver_wall,
            "solver_result": solver_result,
            "true_variables": list(true_variables),
            "model_graph6": model_graph6,
            "model_graph_sha256": model_sha256,
            "model_forbidden_cliques": forbidden[0],
            "model_forbidden_independent_sets": forbidden[1],
            "proof_written": False,
            "lrat_written": False,
            "model_written": args.model_graph is not None,
        }
        write_json(args.result, result)
        print(json.dumps(result, sort_keys=True))
        return 10

    if solver_result.get("status") != "UNSAT" or not args.proof.is_file():
        raise WorkflowError("UNSAT worker did not produce its promised proof")
    proof_sha256 = sha256_file(args.proof)
    if proof_sha256 != solver_result.get("proof_sha256"):
        raise WorkflowError("proof hash differs from solver result")

    drat_command = (
        str(toolchain.drat_trim),
        str(args.completion_cnf),
        str(args.proof),
        "-I",
        "-L",
        str(args.lrat),
    )
    drat_state, drat_result, drat_wall = run_bounded(
        drat_command, timeout=args.proof_check_time_limit
    )
    if drat_state == "TIMEOUT":
        status = "UNSAT_PROOF_CHECK_TIMEOUT"
        drat_valid = False
    else:
        assert drat_result is not None
        drat_text = drat_result.stdout + drat_result.stderr
        drat_valid = (
            drat_result.returncode == 0 and checker_says_verified(drat_text)
        )
        status = "UNSAT_PENDING_LRAT" if drat_valid else "UNSAT_PROOF_REJECTED"

    lrat_result: subprocess.CompletedProcess[str] | None = None
    lrat_wall: float | None = None
    lrat_valid = False
    if drat_valid and args.lrat.is_file():
        lrat_state, lrat_result, lrat_wall = run_bounded(
            (
                str(toolchain.lrat_check),
                str(args.completion_cnf),
                str(args.lrat),
            ),
            timeout=args.proof_check_time_limit,
        )
        if lrat_state == "TIMEOUT":
            status = "UNSAT_LRAT_CHECK_TIMEOUT"
        else:
            assert lrat_result is not None
            lrat_text = lrat_result.stdout + lrat_result.stderr
            lrat_valid = (
                lrat_result.returncode == 0
                and checker_says_verified(lrat_text)
            )
            status = "CERTIFIED_UNSAT" if lrat_valid else "UNSAT_LRAT_REJECTED"

    result = {
        **base_result,
        "status": status,
        "solver_wall_seconds": solver_wall,
        "solver_result": solver_result,
        "proof_written": args.proof.is_file(),
        "proof_path": str(args.proof.resolve()),
        "proof_sha256": proof_sha256,
        "proof_bytes": args.proof.stat().st_size,
        "drat_trim_valid": drat_valid,
        "drat_trim_wall_seconds": drat_wall,
        "drat_trim_returncode": (
            drat_result.returncode if drat_result is not None else None
        ),
        "drat_trim_stdout": (
            drat_result.stdout if drat_result is not None else None
        ),
        "drat_trim_stderr": (
            drat_result.stderr if drat_result is not None else None
        ),
        "lrat_written": args.lrat.is_file(),
        "lrat_path": str(args.lrat.resolve()),
        "lrat_sha256": sha256_file(args.lrat) if args.lrat.is_file() else None,
        "lrat_bytes": args.lrat.stat().st_size if args.lrat.is_file() else None,
        "lrat_check_valid": lrat_valid,
        "lrat_check_wall_seconds": lrat_wall,
        "lrat_check_returncode": (
            lrat_result.returncode if lrat_result is not None else None
        ),
        "lrat_check_stdout": (
            lrat_result.stdout if lrat_result is not None else None
        ),
        "lrat_check_stderr": (
            lrat_result.stderr if lrat_result is not None else None
        ),
        "model_written": False,
    }
    write_json(args.result, result)
    print(json.dumps(result, sort_keys=True))
    return 20 if status == "CERTIFIED_UNSAT" else 3


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except WorkflowError as error:
        print(
            json.dumps(
                {
                    "workflow": WORKFLOW_ID,
                    "status": "ERROR",
                    "error": str(error),
                },
                sort_keys=True,
            ),
            file=sys.stderr,
        )
        raise SystemExit(1)
