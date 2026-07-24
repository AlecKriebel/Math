#!/usr/bin/env python3
"""Independently reconstruct and audit the C7 side-model exhaustion CNF."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import math
import time
from pathlib import Path


CHECKER_ID = "ramsey55_automorphism7_side_model_exhaustion_checker_v1"
PRIME = 7
SIDE_ORDER = 21
VARIABLE_COUNT = 30


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def side_edge_table() -> dict[tuple[int, int], int]:
    rotate = tuple(
        block * PRIME + (offset + 1) % PRIME
        for block in range(3)
        for offset in range(PRIME)
    )
    unseen = set(itertools.combinations(range(SIDE_ORDER), 2))
    orbits: list[tuple[tuple[int, int], ...]] = []
    while unseen:
        edge = min(unseen)
        orbit: set[tuple[int, int]] = set()
        while edge not in orbit:
            orbit.add(edge)
            edge = tuple(sorted((rotate[edge[0]], rotate[edge[1]])))
        unseen.difference_update(orbit)
        orbits.append(tuple(sorted(orbit)))
    orbits.sort(key=lambda orbit: orbit[0])
    table = {
        edge: variable
        for variable, orbit in enumerate(orbits, start=1)
        for edge in orbit
    }
    if len(orbits) != VARIABLE_COUNT or len(table) != math.comb(SIDE_ORDER, 2):
        raise AssertionError("bad side edge orbits")
    return table


def side_formula(
    edge_variable: dict[tuple[int, int], int],
) -> tuple[tuple[int, ...], ...]:
    clique = {
        tuple(
            sorted(
                {
                    edge_variable[edge]
                    for edge in itertools.combinations(vertices, 2)
                }
            )
        )
        for vertices in itertools.combinations(range(SIDE_ORDER), 4)
    }
    independent = {
        tuple(
            sorted(
                {
                    edge_variable[edge]
                    for edge in itertools.combinations(vertices, 2)
                }
            )
        )
        for vertices in itertools.combinations(range(SIDE_ORDER), 5)
    }
    if len(clique) != 843 or len(independent) != 2775:
        raise AssertionError("bad side signature counts")
    return tuple(
        [
            tuple(-variable for variable in signature)
            for signature in sorted(clique)
        ]
        + list(sorted(independent))
    )


def parse_models(path: Path) -> list[int]:
    models: list[int] = []
    for line_number, line in enumerate(
        path.read_text(encoding="ascii").splitlines(), start=1
    ):
        if len(line) != VARIABLE_COUNT or set(line) - {"0", "1"}:
            raise ValueError(f"bad model line {line_number}")
        models.append(int(line, 2))
    if models != sorted(set(models)):
        raise ValueError("model list is not strictly sorted and unique")
    return models


def all_models_satisfy(
    models: list[int], clauses: tuple[tuple[int, ...], ...]
) -> tuple[bool, dict[str, int] | None]:
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
    for clause_index, clause in enumerate(clauses):
        satisfied = 0
        for literal in clause:
            variable_truth = truth[abs(literal)]
            satisfied |= (
                variable_truth
                if literal > 0
                else all_positions ^ variable_truth
            )
        missing = all_positions ^ satisfied
        if missing:
            position = (missing & -missing).bit_length() - 1
            return False, {
                "clause_index": clause_index,
                "model_position": position,
                "model": models[position],
            }
    return True, None


def blocker(model: int) -> tuple[int, ...]:
    return tuple(
        -variable if model >> (variable - 1) & 1 else variable
        for variable in range(1, VARIABLE_COUNT + 1)
    )


def expected_cnf_bytes(
    clauses: tuple[tuple[int, ...], ...],
) -> bytes:
    return (
        f"p cnf {VARIABLE_COUNT} {len(clauses)}\n"
        + "".join(
            " ".join(map(str, clause)) + " 0\n" for clause in clauses
        )
    ).encode("ascii")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--models", type=Path, required=True)
    parser.add_argument("--cnf", type=Path, required=True)
    parser.add_argument("--metadata", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        raise SystemExit("refusing to overwrite output")
    started = time.monotonic()
    metadata = json.loads(args.metadata.read_text(encoding="utf-8"))
    models = parse_models(args.models)
    side_clauses = side_formula(side_edge_table())
    replay_valid, first_failure = all_models_satisfy(models, side_clauses)
    blockers = tuple(blocker(model) for model in models)
    clauses = side_clauses + blockers
    expected = expected_cnf_bytes(clauses)
    actual = args.cnf.read_bytes()
    metadata_valid = (
        metadata.get("variable_count") == VARIABLE_COUNT
        and metadata.get("side_clause_count") == len(side_clauses)
        and metadata.get("model_count") == len(models)
        and metadata.get("model_blocker_count") == len(blockers)
        and metadata.get("clause_count") == len(clauses)
        and Path(str(metadata.get("model_list_path", ""))).resolve()
        == args.models.resolve()
        and metadata.get("model_list_sha256") == sha256_file(args.models)
        and metadata.get("model_list_bytes") == args.models.stat().st_size
        and Path(str(metadata.get("cnf_path", ""))).resolve()
        == args.cnf.resolve()
        and metadata.get("cnf_sha256") == sha256_file(args.cnf)
        and metadata.get("cnf_bytes") == args.cnf.stat().st_size
    )
    valid = (
        len(models) == 191394
        and replay_valid
        and actual == expected
        and metadata_valid
    )
    result = {
        "checker": CHECKER_ID,
        "valid": valid,
        "evidence_label": "INDEPENDENT MODEL REPLAY AND BYTE-EXACT CNF REBUILD",
        "claim_boundary": (
            "This checks the listed assignments and exhaustion encoding. "
            "Completeness requires a separately checked UNSAT proof for the "
            "encoded CNF."
        ),
        "variable_count": VARIABLE_COUNT,
        "side_clause_count": len(side_clauses),
        "model_count": len(models),
        "model_blocker_count": len(blockers),
        "clause_count": len(clauses),
        "all_listed_models_satisfy": replay_valid,
        "first_model_replay_failure": first_failure,
        "model_list_sha256": sha256_file(args.models),
        "model_list_bytes": args.models.stat().st_size,
        "cnf_sha256": sha256_file(args.cnf),
        "cnf_bytes": args.cnf.stat().st_size,
        "cnf_reconstruction_exact": actual == expected,
        "metadata_valid": metadata_valid,
        "runtime_seconds": time.monotonic() - started,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(result, sort_keys=True))
    return 0 if valid else 1


if __name__ == "__main__":
    raise SystemExit(main())
