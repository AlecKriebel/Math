#!/usr/bin/env python3
"""Generate a proof-ready exact exhaustion instance for the C7 side formula."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import time
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VERIFY = ROOT / "verify"
if str(VERIFY) not in sys.path:
    sys.path.insert(0, str(VERIFY))

import automorphism7_side_orbit_cover as side  # noqa: E402


GENERATOR_ID = "ramsey55_automorphism7_side_model_exhaustion_generator_v1"
VARIABLE_COUNT = 30


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def model_blocker(model: int) -> tuple[int, ...]:
    return tuple(
        -variable if model >> (variable - 1) & 1 else variable
        for variable in range(1, VARIABLE_COUNT + 1)
    )


def model_satisfies(model: int, clauses: tuple[tuple[int, ...], ...]) -> bool:
    return all(
        any(
            (literal > 0) == bool(model >> (abs(literal) - 1) & 1)
            for literal in clause
        )
        for clause in clauses
    )


def all_models_satisfy(
    models: list[int], clauses: tuple[tuple[int, ...], ...]
) -> bool:
    """Replay all models with Python-integer bitsets across model positions."""

    byte_count = (len(models) + 7) // 8
    truth_bytes = [bytearray(byte_count) for _ in range(VARIABLE_COUNT + 1)]
    for position, model in enumerate(models):
        byte_index, bit_index = divmod(position, 8)
        remaining = model
        while remaining:
            lowest = remaining & -remaining
            variable = lowest.bit_length()
            truth_bytes[variable][byte_index] |= 1 << bit_index
            remaining -= lowest
    truth = [
        int.from_bytes(buffer, "little") for buffer in truth_bytes
    ]
    all_positions = (1 << len(models)) - 1
    for clause in clauses:
        satisfied = 0
        for literal in clause:
            variable_truth = truth[abs(literal)]
            satisfied |= (
                variable_truth
                if literal > 0
                else all_positions ^ variable_truth
            )
        if satisfied != all_positions:
            return False
    return True


def write_text_atomic(path: Path, payload: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + f".tmp.{os.getpid()}")
    if temporary.exists():
        raise FileExistsError(temporary)
    try:
        with temporary.open("w", encoding="ascii", newline="\n") as stream:
            stream.write(payload)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    finally:
        temporary.unlink(missing_ok=True)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--models", type=Path, required=True)
    parser.add_argument("--cnf", type=Path, required=True)
    parser.add_argument("--metadata", type=Path, required=True)
    args = parser.parse_args()
    if any(path.exists() for path in (args.models, args.cnf, args.metadata)):
        raise SystemExit("refusing to overwrite output")
    started = time.monotonic()

    _, table = side.side_edge_orbits()
    side_clauses = side.side_formula(table)
    models = sorted(side.enumerate_models(side_clauses))
    if len(models) != 191394 or len(set(models)) != len(models):
        raise AssertionError("unexpected side-model enumeration")
    # This direct replay is redundant with solver enumeration but catches
    # serialization/sign mistakes before the independent checker runs.
    if not all_models_satisfy(models, side_clauses):
        raise AssertionError("enumerated assignment fails the side formula")

    model_payload = "".join(format(model, "030b") + "\n" for model in models)
    write_text_atomic(args.models, model_payload)
    blockers = tuple(model_blocker(model) for model in models)
    clauses = side_clauses + blockers
    cnf_payload = (
        f"p cnf {VARIABLE_COUNT} {len(clauses)}\n"
        + "".join(
            " ".join(map(str, clause)) + " 0\n" for clause in clauses
        )
    )
    write_text_atomic(args.cnf, cnf_payload)

    source = Path(__file__).resolve()
    dependency = Path(side.__file__).resolve()
    metadata = {
        "generator": GENERATOR_ID,
        "variable_count": VARIABLE_COUNT,
        "side_clause_count": len(side_clauses),
        "model_count": len(models),
        "model_blocker_count": len(blockers),
        "clause_count": len(clauses),
        "model_list_path": str(args.models.resolve()),
        "model_list_sha256": sha256_file(args.models),
        "model_list_bytes": args.models.stat().st_size,
        "cnf_path": str(args.cnf.resolve()),
        "cnf_sha256": sha256_file(args.cnf),
        "cnf_bytes": args.cnf.stat().st_size,
        "generator_path": str(source),
        "generator_sha256": sha256_file(source),
        "enumerator_dependency_path": str(dependency),
        "enumerator_dependency_sha256": sha256_file(dependency),
        "semantics": (
            "The first 3,618 clauses are the C7 side formula. Each remaining "
            "30-literal clause blocks exactly one listed satisfying "
            "assignment. UNSAT therefore certifies list completeness once "
            "every listed assignment is independently replayed."
        ),
        "runtime_seconds": time.monotonic() - started,
    }
    args.metadata.parent.mkdir(parents=True, exist_ok=True)
    args.metadata.write_text(
        json.dumps(metadata, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(metadata, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
