#!/usr/bin/env python3
"""Certify the 80 exact internal orientations of the order-5 all-ones leaf.

The parent fixed-vertex split leaves one observational survivor: the
``one_edge`` fixed graph with membership-count vector ``(1,)*8``.  The two
internal edge orbits of every moved C5 must have opposite colors.  Quotienting
the resulting 2^8 assignments by the exact residual endpoint swap and global
multiplier gives 80 leaves.

This workflow freezes those leaves in a plan, solves every residual CNF with
Glucose3 without a conflict or wall-clock budget, converts the emitted DRAT
trace to a trimmed DRAT core and LRAT, checks both, and stores compressed
proofs.  It is resume-safe at leaf granularity.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
from collections import Counter
from pathlib import Path
from typing import Iterable, Mapping, Sequence


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

import automorphism5_fixed_split_search as split  # noqa: E402
from residual_completion import checker_says_verified  # noqa: E402


PLAN_ID = "ramsey55_order5_allones_internal80_certificate_plan_v1"
WORKFLOW_ID = "ramsey55_order5_allones_internal80_certificate_bundle_v1"
RESULT_ID = "ramsey55_order5_allones_internal80_certificate_result_v1"

DEFAULT_BASE_CNF = (
    ROOT / "certificates" / "order43_automorphism5_eight_cycles.cnf"
)
DEFAULT_BASE_METADATA = (
    ROOT / "certificates" / "order43_automorphism5_eight_cycles.metadata.json"
)
DEFAULT_PLAN = (
    ROOT
    / "results"
    / "benchmark_plans"
    / "automorphism5_allones_internal80_certification_v1.json"
)
DEFAULT_OUTPUT = (
    ROOT
    / "certificates"
    / "order43_automorphism5_allones_internal80"
)
DEFAULT_SUMMARY = (
    ROOT
    / "results"
    / "global_exact"
    / "automorphism5_allones_internal80_certification_v1.json"
)
DEFAULT_MODEL = (
    ROOT
    / "results"
    / "best_candidates"
    / "order43_automorphism5_allones.g6"
)

DEFAULT_PYTHON = Path("/opt/homebrew/opt/python@3.11/bin/python3.11")
DEFAULT_PYSAT_PATH = Path("/tmp/ramsey55-pysat.4YSXId")
DEFAULT_DRAT_TRIM = Path("/tmp/ramsey55-drat-trim.x3nb3p/src/drat-trim")
DEFAULT_LRAT_CHECK = Path("/tmp/ramsey55-drat-trim.x3nb3p/src/lrat-check")
DEFAULT_ZSTD = Path("/opt/homebrew/bin/zstd")

PINNED_PYSAT_VERSION = "1.9.dev7"
PINNED_HASHES = {
    "python": "831365631dac62f232a720858703d0b2ddca5eed33e0a51986cf06aac9d38bc0",
    "pysat_solvers_py": "253654d8efabae650a0d136ad2f2e6d30b57206b1fb70846c714197468a28f7e",
    "pysolvers_extension": "e9828032a114da49429305e5afcf58db259034687a9c098c996da65e5e099ded",
    "drat_trim": "f58f63b0f76945d4c4c9ff6e87afaf870f579e67c0f7cca589492df8fc7ebd47",
    "lrat_check": "bd7eb8052623525814a0a37502b47f05375d9d9dfaf96ddc2fcd858958517cea",
    "zstd": "aff8169fb421bb925fb16c44a7e0143fa2c7a941dc45cce76b15062a2ce54917",
}

MAXIMUM_TOTAL_ARTIFACT_BYTES = 3_000_000_000
MAXIMUM_TRANSIENT_BYTES = 2_000_000_000
MINIMUM_FREE_BYTES_AFTER_COMPLETION = 2_147_483_648


class BundleError(RuntimeError):
    """A deterministic workflow invariant failed."""


def parse_dimacs(path: Path) -> tuple[int, list[list[int]]]:
    variable_count: int | None = None
    declared: int | None = None
    clauses: list[list[int]] = []
    pending: list[int] = []
    with path.open("r", encoding="ascii") as stream:
        for line_number, raw in enumerate(stream, start=1):
            fields = raw.split()
            if not fields or fields[0] == "c":
                continue
            if fields[0] == "p":
                if (
                    variable_count is not None
                    or len(fields) != 4
                    or fields[1] != "cnf"
                ):
                    raise BundleError(
                        f"invalid DIMACS header at line {line_number}"
                    )
                variable_count = int(fields[2])
                declared = int(fields[3])
                continue
            if variable_count is None:
                raise BundleError("DIMACS clause precedes its header")
            for field in fields:
                literal = int(field)
                if literal:
                    if not 1 <= abs(literal) <= variable_count:
                        raise BundleError("DIMACS literal is out of range")
                    pending.append(literal)
                else:
                    if not pending:
                        raise BundleError("unexpected empty DIMACS clause")
                    clauses.append(pending)
                    pending = []
    if (
        variable_count is None
        or declared is None
        or pending
        or len(clauses) != declared
    ):
        raise BundleError("malformed or incomplete DIMACS")
    return variable_count, clauses


def sha256_file(path: Path) -> str:
    state = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            state.update(block)
    return state.hexdigest()


def sha256_json(value: object) -> str:
    return hashlib.sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()


def atomic_json(path: Path, value: Mapping[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary: str | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            newline="\n",
            prefix=path.name + ".",
            suffix=".tmp",
            dir=path.parent,
            delete=False,
        ) as stream:
            temporary = stream.name
            json.dump(value, stream, indent=2, sort_keys=True)
            stream.write("\n")
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
        temporary = None
    finally:
        if temporary is not None:
            Path(temporary).unlink(missing_ok=True)


def residual_clauses(
    clauses: Iterable[Sequence[int]], assumptions: Sequence[int]
) -> tuple[tuple[int, ...], ...]:
    """Restrict, deduplicate, and lexicographically sort a CNF."""
    assignment: dict[int, bool] = {}
    for literal in assumptions:
        variable = abs(literal)
        value = literal > 0
        if variable in assignment and assignment[variable] != value:
            raise BundleError("contradictory cube assumptions")
        assignment[variable] = value
    residual: set[tuple[int, ...]] = set()
    for original in clauses:
        if any(
            assignment.get(abs(literal)) == (literal > 0)
            for literal in original
            if abs(literal) in assignment
        ):
            continue
        clause = tuple(
            literal for literal in original if abs(literal) not in assignment
        )
        if not clause:
            raise BundleError("cube directly falsifies a base clause")
        residual.add(clause)
    return tuple(sorted(residual))


def dimacs_digest(
    variable_count: int, clauses: Sequence[Sequence[int]]
) -> tuple[str, int]:
    state = hashlib.sha256()
    byte_count = 0
    header = f"p cnf {variable_count} {len(clauses)}\n".encode("ascii")
    state.update(header)
    byte_count += len(header)
    for clause in clauses:
        line = (" ".join(map(str, clause)) + " 0\n").encode("ascii")
        state.update(line)
        byte_count += len(line)
    return state.hexdigest(), byte_count


def write_dimacs_atomic(
    path: Path, variable_count: int, clauses: Sequence[Sequence[int]]
) -> tuple[str, int]:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary: str | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="ascii",
            newline="\n",
            prefix=path.name + ".",
            suffix=".tmp",
            dir=path.parent,
            delete=False,
        ) as stream:
            temporary = stream.name
            stream.write(f"p cnf {variable_count} {len(clauses)}\n")
            for clause in clauses:
                stream.write(" ".join(map(str, clause)) + " 0\n")
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
        temporary = None
    finally:
        if temporary is not None:
            Path(temporary).unlink(missing_ok=True)
    return sha256_file(path), path.stat().st_size


def cube_data() -> tuple[
    dict[tuple[int, int], int],
    tuple[int, ...],
    tuple[tuple[bool, ...], ...],
]:
    edge_variable, _ = split.edge_orbits()
    fixed = split.assumptions_for_split(
        "one_edge", (1,) * split.CYCLE_COUNT, edge_variable
    )
    orientations = split.internal_orientation_types((1,) * split.CYCLE_COUNT)
    if len(fixed) != 27 or len(orientations) != 80:
        raise BundleError("all-ones cover has an unexpected size")
    return edge_variable, fixed, orientations


def orientation_id(index: int, orientation: Sequence[bool]) -> str:
    bits = "".join("1" if value else "0" for value in orientation)
    return f"orbit_{index:03d}_{bits}"


def source_paths() -> dict[str, Path]:
    return {
        "producer": Path(__file__).resolve(),
        "split_source": (ROOT / "src" / "automorphism5_fixed_split_search.py"),
        "solver_worker": (ROOT / "src" / "residual_completion_glucose.py"),
        "checker": (
            ROOT
            / "verify"
            / "automorphism5_allones_certificate_bundle_check.py"
        ),
        "tests": (
            ROOT / "tests" / "automorphism5_allones_certificate_tests.py"
        ),
        "independent_formula_checker": (
            ROOT / "verify" / "automorphism_orbit_cnf_check.py"
        ),
    }


def pysat_files(pysat_path: Path) -> tuple[Path, Path]:
    solver_source = pysat_path / "pysat" / "solvers.py"
    extensions = sorted(pysat_path.glob("pysolvers*.so"))
    if len(extensions) != 1:
        raise BundleError("could not identify the pinned PySAT extension")
    return solver_source, extensions[0]


def tool_paths(
    python: Path,
    pysat_path: Path,
    drat_trim: Path,
    lrat_check: Path,
    zstd: Path,
) -> dict[str, Path]:
    solvers_py, extension = pysat_files(pysat_path)
    return {
        "python": python,
        "pysat_solvers_py": solvers_py,
        "pysolvers_extension": extension,
        "drat_trim": drat_trim,
        "lrat_check": lrat_check,
        "zstd": zstd,
    }


def validate_pinned_tools(paths: Mapping[str, Path]) -> dict[str, object]:
    metadata: dict[str, object] = {}
    for name, expected in PINNED_HASHES.items():
        path = paths[name]
        if not path.is_file():
            raise BundleError(f"pinned tool is missing: {path}")
        actual = sha256_file(path)
        if actual != expected:
            raise BundleError(
                f"pinned {name} hash mismatch: {actual} != {expected}"
            )
        metadata[name] = {
            "path": str(path.resolve()),
            "sha256": actual,
            "bytes": path.stat().st_size,
        }
    return metadata


def build_plan(
    *,
    base_cnf: Path,
    base_metadata: Path,
    output: Path,
    python: Path,
    pysat_path: Path,
    drat_trim: Path,
    lrat_check: Path,
    zstd: Path,
) -> dict[str, object]:
    variable_count, parsed = parse_dimacs(base_cnf)
    clauses = tuple(tuple(clause) for clause in parsed)
    if (
        variable_count != split.EXPECTED_VARIABLES
        or len(clauses) != split.EXPECTED_CLAUSES
        or sha256_file(base_cnf) != split.EXPECTED_DIMACS_SHA256
    ):
        raise BundleError("shared order-5 formula fingerprint mismatch")
    metadata = json.loads(base_metadata.read_text(encoding="utf-8"))
    if metadata.get("cnf_sha256") != split.EXPECTED_DIMACS_SHA256:
        raise BundleError("shared order-5 metadata does not pin the base CNF")

    tools = validate_pinned_tools(
        tool_paths(python, pysat_path, drat_trim, lrat_check, zstd)
    )
    sources: dict[str, object] = {}
    for name, path in source_paths().items():
        if not path.is_file():
            raise BundleError(f"required source is missing: {path}")
        sources[name] = {
            "path": str(path.resolve()),
            "sha256": sha256_file(path),
            "bytes": path.stat().st_size,
        }

    edge_variable, fixed, orientations = cube_data()
    records: list[dict[str, object]] = []
    for index, orientation in enumerate(orientations):
        internal = split.internal_orientation_assumptions(
            orientation, edge_variable
        )
        assumptions = (*fixed, *internal)
        if len(assumptions) != 43 or len(set(map(abs, assumptions))) != 43:
            raise BundleError("leaf cube does not assign 43 distinct variables")
        residual = residual_clauses(clauses, assumptions)
        digest, byte_count = dimacs_digest(variable_count, residual)
        records.append(
            {
                "index": index,
                "id": orientation_id(index, orientation),
                "orientation": [int(value) for value in orientation],
                "assumptions": list(assumptions),
                "residual_variable_count": variable_count,
                "residual_clause_count": len(residual),
                "residual_dimacs_sha256": digest,
                "residual_dimacs_bytes": byte_count,
            }
        )

    orientation_lists = [
        [int(value) for value in orientation] for orientation in orientations
    ]
    required = (
        MAXIMUM_TOTAL_ARTIFACT_BYTES
        + MAXIMUM_TRANSIENT_BYTES
        + MINIMUM_FREE_BYTES_AFTER_COMPLETION
    )
    subsets = split.subsets_from_counts((1,) * 8)
    return {
        "plan": PLAN_ID,
        "claim_scope": (
            "Exact certificate cover of the sole surviving normalized "
            "order-5 leaf: cycle type 5^8 1^3, one fixed edge, all eight "
            "fixed-adjacency masks occurring once, and all internal C5 "
            "orientations."
        ),
        "negative_claim_boundary": (
            "A complete CERTIFIED_UNSAT result excludes this normalized leaf "
            "only.  The other 58 fixed-split types remain observational "
            "unless separately certified."
        ),
        "base_formula": {
            "path": str(base_cnf.resolve()),
            "metadata_path": str(base_metadata.resolve()),
            "variable_count": variable_count,
            "clause_count": len(clauses),
            "sha256": sha256_file(base_cnf),
            "bytes": base_cnf.stat().st_size,
        },
        "normalization": {
            "fixed_graph": "one_edge",
            "fixed_edge": [40, 41],
            "nonedges": [[40, 42], [41, 42]],
            "membership_counts": [1] * 8,
            "membership_subsets": [sorted(subset) for subset in subsets],
            "fixed_assumptions": list(fixed),
            "internal_rule": (
                "Each moved C5 has opposite colors on its distance-1 and "
                "distance-2 internal edge orbits."
            ),
        },
        "exact_cover": {
            "labeled_orientation_count": 256,
            "group_order": 4,
            "actions": [
                "identity",
                "swap endpoints 40 and 41",
                "global multiplier x->2x",
                "their product",
            ],
            "representative_count": len(orientations),
            "representatives": orientation_lists,
            "representatives_sha256": sha256_json(orientation_lists),
            "ordering": "lexicographic Boolean order, False before True",
        },
        "residual_construction": {
            "algorithm": (
                "Substitute all 43 cube literals, discard satisfied clauses, "
                "remove assigned false literals, reject empty clauses, "
                "deduplicate, and lexicographically sort clause tuples."
            ),
            "unit_clause_materialization": False,
            "variable_numbering_preserved": True,
        },
        "orbits": records,
        "solver": {
            "name": "Glucose3",
            "pysat_version": PINNED_PYSAT_VERSION,
            "conflict_budget": None,
            "wall_clock_timeout_seconds": None,
            "determinism_environment": {
                "PYTHONHASHSEED": "0",
                "LC_ALL": "C",
            },
        },
        "proof_pipeline": {
            "raw_solver_trace": "temporary ASCII DRAT",
            "conversion": "drat-trim -I -l <core.drat> -L <proof.lrat>",
            "stored_drat": "independently rechecked trimmed DRAT core",
            "stored_lrat": "independently checked LRAT",
            "compression": "zstd",
            "zstd_level": 9,
            "zstd_threads": 0,
        },
        "tools": tools,
        "pysat_path": str(pysat_path.resolve()),
        "sources": sources,
        "output_directory": str(output.resolve()),
        "storage_gate": {
            "maximum_total_artifact_bytes": MAXIMUM_TOTAL_ARTIFACT_BYTES,
            "maximum_transient_bytes": MAXIMUM_TRANSIENT_BYTES,
            "minimum_free_bytes_after_completion": (
                MINIMUM_FREE_BYTES_AFTER_COMPLETION
            ),
            "required_prelaunch_free_bytes": required,
        },
    }


def validate_plan(
    plan: Mapping[str, object],
    *,
    base_cnf: Path,
    base_metadata: Path,
    output: Path,
) -> None:
    if plan.get("plan") != PLAN_ID:
        raise BundleError("unexpected plan identifier")
    base = plan.get("base_formula")
    exact = plan.get("exact_cover")
    solver = plan.get("solver")
    proof = plan.get("proof_pipeline")
    storage = plan.get("storage_gate")
    if not all(
        isinstance(item, dict)
        for item in (base, exact, solver, proof, storage)
    ):
        raise BundleError("plan is missing a required mapping")
    assert isinstance(base, dict)
    assert isinstance(exact, dict)
    assert isinstance(solver, dict)
    assert isinstance(proof, dict)
    assert isinstance(storage, dict)
    if (
        Path(str(base.get("path"))).resolve() != base_cnf.resolve()
        or Path(str(base.get("metadata_path"))).resolve()
        != base_metadata.resolve()
        or base.get("sha256") != sha256_file(base_cnf)
        or base.get("bytes") != base_cnf.stat().st_size
        or plan.get("output_directory") != str(output.resolve())
    ):
        raise BundleError("plan inputs or output path no longer match")
    if (
        solver.get("name") != "Glucose3"
        or solver.get("conflict_budget") is not None
        or solver.get("wall_clock_timeout_seconds") is not None
        or proof.get("zstd_level") != 9
    ):
        raise BundleError("plan weakens the unbounded proof protocol")
    orbits = plan.get("orbits")
    if not isinstance(orbits, list) or len(orbits) != 80:
        raise BundleError("plan does not contain exactly 80 leaves")
    if exact.get("representative_count") != 80:
        raise BundleError("plan exact-cover count is not 80")
    sources = plan.get("sources")
    tools = plan.get("tools")
    if not isinstance(sources, dict) or not isinstance(tools, dict):
        raise BundleError("plan source/tool pins are missing")
    for collection, label in ((sources, "source"), (tools, "tool")):
        for name, raw in collection.items():
            if not isinstance(raw, dict):
                raise BundleError(f"malformed {label} pin: {name}")
            path = Path(str(raw.get("path")))
            if (
                not path.is_file()
                or raw.get("sha256") != sha256_file(path)
                or raw.get("bytes") != path.stat().st_size
            ):
                raise BundleError(f"{label} pin changed: {name}")


def artifact_paths(output: Path, leaf_id: str) -> dict[str, Path]:
    return {
        "record": output / f"{leaf_id}.result.json",
        "drat": output / f"{leaf_id}.drat.zst",
        "lrat": output / f"{leaf_id}.lrat.zst",
    }


def artifact_bytes(output: Path) -> int:
    if not output.exists():
        return 0
    return sum(
        path.stat().st_size
        for path in output.iterdir()
        if path.is_file() and path.suffix in {".zst", ".json"}
    )


def validate_storage(
    output: Path, storage: Mapping[str, object], *, prelaunch: bool
) -> dict[str, int]:
    maximum_total = int(storage["maximum_total_artifact_bytes"])
    maximum_transient = int(storage["maximum_transient_bytes"])
    reserve = int(storage["minimum_free_bytes_after_completion"])
    required = int(storage["required_prelaunch_free_bytes"])
    if required != maximum_total + maximum_transient + reserve:
        raise BundleError("storage-gate arithmetic is inconsistent")
    used = artifact_bytes(output)
    if used > maximum_total:
        raise BundleError("certificate artifacts exceed their frozen cap")
    available = shutil.disk_usage(output.parent if output.parent.exists() else ROOT).free
    needed = maximum_total - used + maximum_transient + reserve
    if prelaunch and available < required:
        raise BundleError(
            f"storage preflight failed: {available} free < {required} required"
        )
    if not prelaunch and available < needed:
        raise BundleError(
            f"storage reserve failed: {available} free < {needed} required"
        )
    return {
        "artifact_bytes": used,
        "available_bytes": available,
        "required_bytes": required if prelaunch else needed,
    }


def completed_record_valid(
    record_path: Path,
    paths: Mapping[str, Path],
    expected: Mapping[str, object],
) -> dict[str, object] | None:
    if not record_path.is_file():
        return None
    try:
        record = json.loads(record_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError):
        return None
    if (
        record.get("result") != RESULT_ID
        or record.get("status") != "CERTIFIED_UNSAT"
        or record.get("id") != expected.get("id")
        or record.get("orientation") != expected.get("orientation")
        or record.get("assumptions") != expected.get("assumptions")
        or record.get("residual_dimacs_sha256")
        != expected.get("residual_dimacs_sha256")
        or record.get("residual_clause_count")
        != expected.get("residual_clause_count")
        or not record.get("drat_trim_core_valid")
        or not record.get("lrat_check_valid")
    ):
        return None
    for key in ("drat", "lrat"):
        archive = paths[key]
        archive_record = record.get(f"{key}_zstd")
        if (
            not archive.is_file()
            or not isinstance(archive_record, dict)
            or archive_record.get("sha256") != sha256_file(archive)
            or archive_record.get("bytes") != archive.stat().st_size
        ):
            return None
    return record


def run_command(
    command: Sequence[str],
    *,
    environment: Mapping[str, str] | None = None,
    accepted: set[int] = {0},
) -> tuple[subprocess.CompletedProcess[str], float]:
    started = time.monotonic()
    completed = subprocess.run(
        list(command),
        text=True,
        capture_output=True,
        check=False,
        env=dict(environment) if environment is not None else None,
    )
    elapsed = time.monotonic() - started
    if completed.returncode not in accepted:
        raise BundleError(
            f"command failed ({completed.returncode}): {' '.join(command)}\n"
            f"{completed.stdout[-2000:]}\n{completed.stderr[-2000:]}"
        )
    return completed, elapsed


def compress_atomic(source: Path, target: Path, zstd: Path) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    temporary = target.with_name(target.name + ".tmp")
    temporary.unlink(missing_ok=True)
    try:
        run_command(
            (
                str(zstd),
                "-9",
                "-T0",
                "-q",
                "-f",
                str(source),
                "-o",
                str(temporary),
            )
        )
        os.replace(temporary, target)
    finally:
        temporary.unlink(missing_ok=True)


def parse_worker(stdout: str) -> dict[str, object]:
    lines = [line for line in stdout.splitlines() if line.strip()]
    if len(lines) != 1:
        raise BundleError("solver worker did not emit exactly one JSON object")
    value = json.loads(lines[0])
    if not isinstance(value, dict):
        raise BundleError("solver worker result is not an object")
    return value


def check_sat_model(
    worker: Mapping[str, object],
    residual: Sequence[Sequence[int]],
    assumptions: Sequence[int],
    edge_variable: Mapping[tuple[int, int], int],
    model_path: Path,
) -> dict[str, object]:
    values = worker.get("true_variables")
    if (
        not isinstance(values, list)
        or any(type(value) is not int for value in values)
        or values != sorted(set(values))
    ):
        raise BundleError("SAT worker model is malformed")
    truth = {variable: variable in set(values) for variable in range(1, 184)}
    if not all(
        any(truth[abs(literal)] == (literal > 0) for literal in clause)
        for clause in residual
    ):
        raise BundleError("SAT model does not satisfy the residual formula")
    if any(truth[abs(literal)] != (literal > 0) for literal in assumptions):
        raise BundleError("SAT model violates its cube")
    complete_model = [
        variable if truth[variable] else -variable for variable in range(1, 184)
    ]
    adjacency = split.decode_model(complete_model, dict(edge_variable))
    forbidden = split.forbidden_counts(adjacency)
    if forbidden != (0, 0) or not split.automorphism_valid(adjacency):
        raise BundleError("SAT model failed exhaustive graph replay")
    graph6 = split.encode_graph6(adjacency)
    model_path.parent.mkdir(parents=True, exist_ok=True)
    model_path.write_text(graph6 + "\n", encoding="ascii", newline="\n")
    return {
        "graph6": graph6,
        "graph6_line_sha256": sha256_file(model_path),
        "true_variables": values,
        "forbidden_counts": {
            "clique_5": forbidden[0],
            "independent_5": forbidden[1],
        },
        "automorphism_replay": True,
        "model_path": str(model_path.resolve()),
    }


def summary_payload(
    plan_path: Path,
    output: Path,
    records: Sequence[Mapping[str, object]],
    *,
    status: str,
    started: float,
    storage_preflight: Mapping[str, int],
    construction: Mapping[str, object] | None = None,
) -> dict[str, object]:
    counts = Counter(str(record.get("status")) for record in records)
    return {
        "workflow": WORKFLOW_ID,
        "status": status,
        "claim_scope": (
            "The exact 80-orbit internal-orientation cover of the normalized "
            "order-5 all-ones fixed-split leaf only."
        ),
        "plan_path": str(plan_path.resolve()),
        "plan_sha256": sha256_file(plan_path),
        "output_directory": str(output.resolve()),
        "scheduled_orbit_count": 80,
        "completed_orbit_count": len(records),
        "status_counts": dict(sorted(counts.items())),
        "all_orbits_certified_unsat": (
            len(records) == 80
            and all(record.get("status") == "CERTIFIED_UNSAT" for record in records)
        ),
        "construction": construction,
        "storage_preflight": dict(storage_preflight),
        "stored_artifact_bytes": artifact_bytes(output),
        "records": list(records),
        "runtime_seconds": time.monotonic() - started,
    }


def run_bundle(
    *,
    plan_path: Path,
    base_cnf: Path,
    base_metadata: Path,
    output: Path,
    summary: Path,
    model_path: Path,
) -> int:
    started = time.monotonic()
    plan = json.loads(plan_path.read_text(encoding="utf-8"))
    validate_plan(
        plan,
        base_cnf=base_cnf,
        base_metadata=base_metadata,
        output=output,
    )
    output.mkdir(parents=True, exist_ok=True)
    work_root = output / ".work"
    work_root.mkdir(parents=True, exist_ok=True)
    storage = plan["storage_gate"]
    assert isinstance(storage, dict)
    preflight = validate_storage(output, storage, prelaunch=True)

    variable_count, parsed = parse_dimacs(base_cnf)
    clauses = tuple(tuple(clause) for clause in parsed)
    edge_variable, fixed, orientations = cube_data()
    expected_records = plan["orbits"]
    assert isinstance(expected_records, list)

    tools = plan["tools"]
    assert isinstance(tools, dict)
    python = Path(str(tools["python"]["path"]))
    drat_trim = Path(str(tools["drat_trim"]["path"]))
    lrat_check = Path(str(tools["lrat_check"]["path"]))
    zstd = Path(str(tools["zstd"]["path"]))
    pysat_path = Path(str(plan["pysat_path"]))
    worker = ROOT / "src" / "residual_completion_glucose.py"
    environment = os.environ.copy()
    environment.update(
        {
            "PYTHONPATH": str(pysat_path),
            "PYTHONHASHSEED": "0",
            "LC_ALL": "C",
        }
    )

    records: list[dict[str, object]] = []
    construction: dict[str, object] | None = None
    for expected, orientation in zip(expected_records, orientations, strict=True):
        if not isinstance(expected, dict):
            raise BundleError("malformed orbit record in plan")
        leaf_id = str(expected["id"])
        paths = artifact_paths(output, leaf_id)
        resumed = completed_record_valid(paths["record"], paths, expected)
        if resumed is not None:
            resumed = dict(resumed)
            resumed["resumed"] = True
            records.append(resumed)
            print(
                json.dumps(
                    {
                        "event": "orbit_resumed",
                        "id": leaf_id,
                        "completed": len(records),
                        "scheduled": 80,
                    },
                    sort_keys=True,
                ),
                flush=True,
            )
            continue

        validate_storage(output, storage, prelaunch=False)
        leaf_work = work_root / leaf_id
        if leaf_work.exists():
            shutil.rmtree(leaf_work)
        leaf_work.mkdir(parents=True)
        residual_path = leaf_work / "residual.cnf"
        raw_path = leaf_work / "raw.drat"
        core_path = leaf_work / "core.drat"
        lrat_path = leaf_work / "proof.lrat"

        assumptions = tuple(int(value) for value in expected["assumptions"])
        internal = split.internal_orientation_assumptions(
            orientation, edge_variable
        )
        if assumptions != (*fixed, *internal):
            raise BundleError("plan leaf assumptions do not reconstruct")
        residual = residual_clauses(clauses, assumptions)
        actual_hash, actual_bytes = write_dimacs_atomic(
            residual_path, variable_count, residual
        )
        if (
            actual_hash != expected["residual_dimacs_sha256"]
            or actual_bytes != expected["residual_dimacs_bytes"]
            or len(residual) != expected["residual_clause_count"]
        ):
            raise BundleError("residual formula differs from frozen plan")

        print(
            json.dumps(
                {
                    "event": "orbit_started",
                    "id": leaf_id,
                    "completed": len(records),
                    "scheduled": 80,
                    "residual_clause_count": len(residual),
                },
                sort_keys=True,
            ),
            flush=True,
        )
        solver_completed, solver_wall = run_command(
            (
                str(python),
                str(worker),
                str(residual_path),
                "--proof",
                str(raw_path),
            ),
            environment=environment,
            accepted={10, 20},
        )
        worker_result = parse_worker(solver_completed.stdout)
        if (
            worker_result.get("cnf_sha256") != actual_hash
            or worker_result.get("pysat_version") != PINNED_PYSAT_VERSION
            or worker_result.get("variable_count") != variable_count
            or worker_result.get("clause_count") != len(residual)
        ):
            raise BundleError("solver worker metadata mismatch")

        if solver_completed.returncode == 10:
            construction = check_sat_model(
                worker_result,
                residual,
                assumptions,
                edge_variable,
                model_path,
            )
            record = {
                "result": RESULT_ID,
                "status": "CERTIFIED_CONSTRUCTION",
                "id": leaf_id,
                "index": expected["index"],
                "orientation": expected["orientation"],
                "assumptions": list(assumptions),
                "residual_dimacs_sha256": actual_hash,
                "residual_clause_count": len(residual),
                "solver_wall_seconds": solver_wall,
                "solver_result": worker_result,
                "construction": construction,
            }
            atomic_json(paths["record"], record)
            records.append(record)
            atomic_json(
                summary,
                summary_payload(
                    plan_path,
                    output,
                    records,
                    status="CERTIFIED_CONSTRUCTION",
                    started=started,
                    storage_preflight=preflight,
                    construction=construction,
                ),
            )
            shutil.rmtree(leaf_work)
            return 10

        if (
            worker_result.get("status") != "UNSAT"
            or not raw_path.is_file()
            or worker_result.get("proof_sha256") != sha256_file(raw_path)
        ):
            raise BundleError("UNSAT worker did not produce its promised trace")

        converted, convert_wall = run_command(
            (
                str(drat_trim),
                str(residual_path),
                str(raw_path),
                "-I",
                "-l",
                str(core_path),
                "-L",
                str(lrat_path),
            )
        )
        if not checker_says_verified(converted.stdout + converted.stderr):
            raise BundleError("drat-trim rejected the raw solver trace")
        core_checked, core_wall = run_command(
            (
                str(drat_trim),
                str(residual_path),
                str(core_path),
                "-I",
            )
        )
        core_valid = checker_says_verified(
            core_checked.stdout + core_checked.stderr
        )
        if not core_valid:
            raise BundleError("drat-trim rejected the stored DRAT core")
        lrat_checked, lrat_wall = run_command(
            (str(lrat_check), str(residual_path), str(lrat_path))
        )
        lrat_valid = checker_says_verified(
            lrat_checked.stdout + lrat_checked.stderr
        )
        if not lrat_valid:
            raise BundleError("lrat-check rejected the generated LRAT")

        compress_atomic(core_path, paths["drat"], zstd)
        compress_atomic(lrat_path, paths["lrat"], zstd)
        record = {
            "result": RESULT_ID,
            "status": "CERTIFIED_UNSAT",
            "id": leaf_id,
            "index": expected["index"],
            "orientation": expected["orientation"],
            "assumptions": list(assumptions),
            "residual_dimacs_sha256": actual_hash,
            "residual_dimacs_bytes": actual_bytes,
            "residual_clause_count": len(residual),
            "solver": {
                "name": "Glucose3",
                "conflict_budget": None,
                "wall_clock_timeout_seconds": None,
            },
            "solver_wall_seconds": solver_wall,
            "solver_result": worker_result,
            "raw_drat": {
                "sha256": sha256_file(raw_path),
                "bytes": raw_path.stat().st_size,
            },
            "drat_trim_conversion_valid": True,
            "drat_trim_conversion_wall_seconds": convert_wall,
            "drat_trim_core_valid": core_valid,
            "drat_trim_core_wall_seconds": core_wall,
            "lrat_check_valid": lrat_valid,
            "lrat_check_wall_seconds": lrat_wall,
            "drat_uncompressed": {
                "sha256": sha256_file(core_path),
                "bytes": core_path.stat().st_size,
            },
            "drat_zstd": {
                "path": str(paths["drat"].resolve()),
                "sha256": sha256_file(paths["drat"]),
                "bytes": paths["drat"].stat().st_size,
                "level": 9,
            },
            "lrat_uncompressed": {
                "sha256": sha256_file(lrat_path),
                "bytes": lrat_path.stat().st_size,
            },
            "lrat_zstd": {
                "path": str(paths["lrat"].resolve()),
                "sha256": sha256_file(paths["lrat"]),
                "bytes": paths["lrat"].stat().st_size,
                "level": 9,
            },
            "resumed": False,
        }
        atomic_json(paths["record"], record)
        records.append(record)
        shutil.rmtree(leaf_work)
        validate_storage(output, storage, prelaunch=False)
        atomic_json(
            summary,
            summary_payload(
                plan_path,
                output,
                records,
                status="IN_PROGRESS",
                started=started,
                storage_preflight=preflight,
            ),
        )
        print(
            json.dumps(
                {
                    "event": "orbit_certified",
                    "id": leaf_id,
                    "completed": len(records),
                    "scheduled": 80,
                    "solver_wall_seconds": solver_wall,
                    "stored_bytes": (
                        paths["drat"].stat().st_size
                        + paths["lrat"].stat().st_size
                    ),
                },
                sort_keys=True,
            ),
            flush=True,
        )

    final = summary_payload(
        plan_path,
        output,
        records,
        status="CERTIFIED_UNSAT",
        started=started,
        storage_preflight=preflight,
    )
    if not final["all_orbits_certified_unsat"]:
        raise BundleError("the 80-leaf bundle did not finish certified UNSAT")
    atomic_json(summary, final)
    try:
        work_root.rmdir()
    except OSError:
        pass
    print(json.dumps({"event": "bundle_complete", **final}, sort_keys=True))
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--prepare-plan", action="store_true")
    parser.add_argument("--run", action="store_true")
    parser.add_argument("--base-cnf", type=Path, default=DEFAULT_BASE_CNF)
    parser.add_argument(
        "--base-metadata", type=Path, default=DEFAULT_BASE_METADATA
    )
    parser.add_argument("--plan", type=Path, default=DEFAULT_PLAN)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--summary", type=Path, default=DEFAULT_SUMMARY)
    parser.add_argument("--model", type=Path, default=DEFAULT_MODEL)
    parser.add_argument("--python", type=Path, default=DEFAULT_PYTHON)
    parser.add_argument("--pysat-path", type=Path, default=DEFAULT_PYSAT_PATH)
    parser.add_argument("--drat-trim", type=Path, default=DEFAULT_DRAT_TRIM)
    parser.add_argument("--lrat-check", type=Path, default=DEFAULT_LRAT_CHECK)
    parser.add_argument("--zstd", type=Path, default=DEFAULT_ZSTD)
    args = parser.parse_args()
    if not args.prepare_plan and not args.run:
        parser.error("select --prepare-plan and/or --run")
    if args.prepare_plan:
        plan = build_plan(
            base_cnf=args.base_cnf,
            base_metadata=args.base_metadata,
            output=args.output,
            python=args.python,
            pysat_path=args.pysat_path,
            drat_trim=args.drat_trim,
            lrat_check=args.lrat_check,
            zstd=args.zstd,
        )
        atomic_json(args.plan, plan)
        print(
            json.dumps(
                {
                    "event": "plan_prepared",
                    "path": str(args.plan.resolve()),
                    "sha256": sha256_file(args.plan),
                    "orbit_count": 80,
                },
                sort_keys=True,
            ),
            flush=True,
        )
    if args.run:
        return run_bundle(
            plan_path=args.plan,
            base_cnf=args.base_cnf,
            base_metadata=args.base_metadata,
            output=args.output,
            summary=args.summary,
            model_path=args.model,
        )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except BundleError as error:
        print(
            json.dumps(
                {"workflow": WORKFLOW_ID, "status": "ERROR", "error": str(error)},
                sort_keys=True,
            ),
            file=sys.stderr,
        )
        raise SystemExit(1)
