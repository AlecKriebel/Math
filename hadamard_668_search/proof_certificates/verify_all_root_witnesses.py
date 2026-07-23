#!/usr/bin/env python3
"""Check all 12 stored shell-18 root witnesses against pinned v2 CNFs.

The checker reconstructs the artifact update chain by exact ``(shard,target)``
keys, rejects conflicting repeated witnesses, and records the unique artifact
and result index supplying each final root witness.  It then works serially in
one temporary directory:

1. export the corresponding v2 root CNF;
2. add 334 units fixing its primary flips to the stored witness;
3. require CaDiCaL to return SAT; and
4. independently check every DIMACS clause and all mathematical root layers.

No proof trace, CNF, model, or other per-case scratch is retained.
"""

from __future__ import annotations

from collections import Counter
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import time
from typing import Any


HERE = Path(__file__).resolve().parent
REPOSITORY = HERE.parent
if str(REPOSITORY) not in sys.path:
    sys.path.insert(0, str(REPOSITORY))

from verify_variable_q_seed_quad_radius import MarginTarget  # noqa: E402
from verify_variable_q_seed_shell18_artifacts import (  # noqa: E402
    ROOT_FIVE_SECONDS,
    ROOT_INITIAL,
    ROOT_ORBIT,
    ROOT_ORBIT_HARD,
    ROOT_SYMMETRY,
    ROOT_TWO_SECONDS,
    ArtifactSpec,
    load_artifact,
    result_map,
    selected_frontier,
    verify_root_witness,
    verify_selection,
)
from verify_variable_q_seed_radius import SEED  # noqa: E402


ROOT_EDGES = (
    (ROOT_TWO_SECONDS, ROOT_INITIAL, "unresolved"),
    (ROOT_FIVE_SECONDS, ROOT_TWO_SECONDS, "timeouts"),
    (ROOT_SYMMETRY, ROOT_FIVE_SECONDS, "timeouts"),
    (ROOT_ORBIT, ROOT_SYMMETRY, "timeouts"),
    (ROOT_ORBIT_HARD, ROOT_ORBIT, "timeouts"),
)


def _target(value: Any) -> MarginTarget:
    result = tuple(tuple(int(entry) for entry in pair) for pair in value)
    if len(result) != 4 or any(len(pair) != 2 for pair in result):
        raise ValueError("artifact target has the wrong shape")
    return result  # type: ignore[return-value]


def _key(result: dict[str, Any]) -> tuple[int, MarginTarget]:
    return int(result["shard"]), _target(result["target"])


def _stored_sequences(
    result: dict[str, Any]
) -> tuple[tuple[int, ...], ...]:
    stored = result.get("sequences")
    if not isinstance(stored, dict):
        raise ValueError("root witness has no stored sequences")
    sequences = tuple(
        tuple(int(value) for value in stored.get(label, ()))
        for label in "abcd"
    )
    if tuple(map(len, sequences)) != tuple(map(len, SEED)):
        raise ValueError("stored root witness has wrong sequence lengths")
    if any(value not in (-1, 1) for sequence in sequences for value in sequence):
        raise ValueError("stored root witness contains a non-sign")
    return sequences


def _witness_sha256(result: dict[str, Any]) -> str:
    sequences = _stored_sequences(result)
    return hashlib.sha256(
        json.dumps(
            {
                label: list(sequence)
                for label, sequence in zip("abcd", sequences, strict=True)
            },
            sort_keys=True,
            separators=(",", ":"),
        ).encode("ascii")
    ).hexdigest()


def _artifact_indices(
    payload: dict[str, Any]
) -> dict[tuple[int, MarginTarget], int]:
    indices = {}
    for index, result in enumerate(payload.get("results", ())):
        key = _key(result)
        if key in indices:
            raise ValueError(f"duplicate artifact result key: {key}")
        indices[key] = index
    return indices


def locate_root_witnesses() -> tuple[
    tuple[
        tuple[int, MarginTarget],
        dict[str, Any],
        ArtifactSpec,
        int,
    ],
    ...,
]:
    specs = (
        ROOT_INITIAL,
        ROOT_TWO_SECONDS,
        ROOT_FIVE_SECONDS,
        ROOT_SYMMETRY,
        ROOT_ORBIT,
        ROOT_ORBIT_HARD,
    )
    payloads = {spec: load_artifact(spec) for spec in specs}
    expected_records = {
        (record.shard, record.target): record for record in selected_frontier()
    }
    if len(expected_records) != 823:
        raise ValueError("reconstructed shell-18 frontier size changed")
    maps = {
        spec: result_map(payloads[spec], expected_records) for spec in specs
    }
    if set(maps[ROOT_INITIAL]) != set(expected_records):
        raise ValueError("initial root artifact is not frontier-complete")
    for child, parent, mode in ROOT_EDGES:
        verify_selection(
            child,
            payloads[child],
            maps[child],
            parent,
            payloads[parent],
            mode,
        )

    indices = {
        spec: _artifact_indices(payloads[spec]) for spec in specs
    }
    root_state = dict(maps[ROOT_INITIAL])
    provenance = {
        key: (ROOT_INITIAL, indices[ROOT_INITIAL][key])
        for key in maps[ROOT_INITIAL]
    }
    for child, _parent, _mode in ROOT_EDGES:
        for key, result in maps[child].items():
            previous = root_state.get(key)
            if (
                previous is not None
                and previous.get("status") in {"FEASIBLE", "OPTIMAL"}
                and result.get("status") in {"FEASIBLE", "OPTIMAL"}
                and _stored_sequences(previous) != _stored_sequences(result)
            ):
                raise ValueError(
                    f"conflicting repeated root witnesses for key {key}"
                )
            root_state[key] = result
            provenance[key] = (child, indices[child][key])
    counts = Counter(result.get("status") for result in root_state.values())
    if counts != Counter({"INFEASIBLE": 811, "OPTIMAL": 12}):
        raise ValueError(f"unexpected final root classification: {counts}")

    witnesses = []
    for key, result in sorted(root_state.items()):
        if result.get("status") != "OPTIMAL":
            continue
        verify_root_witness(key, result)
        spec, index = provenance[key]
        source_result = payloads[spec]["results"][index]
        if _key(source_result) != key or source_result != result:
            raise ValueError(f"ambiguous source mapping for root witness {key}")
        witnesses.append((key, result, spec, index))
    if len(witnesses) != 12:
        raise ValueError(f"expected 12 final root witnesses, got {len(witnesses)}")
    if len({key for key, _result, _spec, _index in witnesses}) != 12:
        raise ValueError("final root witness keys are not unique")
    return tuple(witnesses)


def _parse_primary_assignment(
    model_path: Path,
) -> tuple[bool, ...]:
    assignment: dict[int, bool] = {}
    status = None
    for line in model_path.read_text(encoding="ascii").splitlines():
        if line.startswith("s "):
            status = line[2:].strip()
        if line.startswith("v "):
            for entry in line[2:].split():
                literal = int(entry)
                if literal:
                    assignment[abs(literal)] = literal > 0
    if status != "SATISFIABLE":
        raise ValueError("CaDiCaL output does not report SATISFIABLE")
    if any(variable not in assignment for variable in range(1, 335)):
        raise ValueError("CaDiCaL omitted a primary variable")
    return tuple(assignment[variable] for variable in range(1, 335))


def _expected_primary_flips(result: dict[str, Any]) -> tuple[bool, ...]:
    sequences = _stored_sequences(result)
    return tuple(
        value != seed_value
        for sequence, seed in zip(sequences, SEED, strict=True)
        for value, seed_value in zip(sequence, seed, strict=True)
    )


def verify_one(
    ordinal: int,
    total: int,
    key: tuple[int, MarginTarget],
    result: dict[str, Any],
    spec: ArtifactSpec,
    result_index: int,
    cadical: Path,
    temporary: Path,
) -> tuple[str, float]:
    cnf = temporary / "witness.cnf"
    metadata = temporary / "witness.metadata.json"
    model = temporary / "witness.model"
    start = time.monotonic()
    exported = subprocess.run(
        [
            sys.executable,
            str(HERE / "export_seed_frontier_cnf.py"),
            "--artifact",
            str(spec.path),
            "--result-index",
            str(result_index),
            "--expect-status",
            "OPTIMAL",
            "--propagation",
            "cp-sat",
            "--exchangeable-quad-symmetry",
            "off",
            "--pin-stored-witness",
            "--output",
            str(cnf),
            "--metadata",
            str(metadata),
        ],
        cwd=REPOSITORY,
        text=True,
        capture_output=True,
    )
    if exported.returncode:
        raise ValueError(
            f"export failed for {key}:\n{exported.stdout}{exported.stderr}"
        )
    expected_sha256 = _witness_sha256(result)
    metadata_payload = json.loads(metadata.read_text(encoding="utf-8"))
    if (
        metadata_payload.get("pinned_stored_witness") is not True
        or metadata_payload.get("pinned_witness_sha256") != expected_sha256
        or metadata_payload.get("compression") != "none"
        or metadata_payload.get("exchangeable_quad_symmetry") is not False
    ):
        raise ValueError(f"wrong pinned-export metadata for {key}")

    with model.open("w", encoding="ascii", newline="\n") as output:
        solved = subprocess.run(
            [str(cadical), "--quiet", str(cnf)],
            cwd=REPOSITORY,
            stdout=output,
            stderr=subprocess.PIPE,
            text=True,
        )
    if solved.returncode != 10:
        raise ValueError(
            f"CaDiCaL did not return SAT for {key}: "
            f"exit={solved.returncode}\n{solved.stderr}"
        )
    if _parse_primary_assignment(model) != _expected_primary_flips(result):
        raise ValueError(f"SAT model differs from pinned witness for {key}")

    checked = subprocess.run(
        [
            sys.executable,
            str(HERE / "verify_seed_frontier_sat_model.py"),
            "--metadata",
            str(metadata),
            "--cnf",
            str(cnf),
            "--model",
            str(model),
        ],
        cwd=REPOSITORY,
        text=True,
        capture_output=True,
    )
    if checked.returncode or not checked.stdout.startswith("PASS:"):
        raise ValueError(
            f"independent model check failed for {key}:\n"
            f"{checked.stdout}{checked.stderr}"
        )
    elapsed = time.monotonic() - start
    print(
        f"PASS {ordinal:02d}/{total}: shard={key[0]} "
        f"source={spec.filename}[{result_index}] "
        f"witness_sha256={expected_sha256} elapsed={elapsed:.2f}s",
        flush=True,
    )
    return expected_sha256, elapsed


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cadical", type=Path, required=True)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        if not args.cadical.is_file():
            raise ValueError(f"CaDiCaL not found: {args.cadical}")
        witnesses = locate_root_witnesses()
        observed_hashes = []
        total_seconds = 0.0
        with tempfile.TemporaryDirectory(
            prefix="hadamard-668-root-witnesses-"
        ) as directory:
            temporary = Path(directory)
            for ordinal, (key, result, spec, index) in enumerate(
                witnesses, start=1
            ):
                witness_hash, elapsed = verify_one(
                    ordinal,
                    len(witnesses),
                    key,
                    result,
                    spec,
                    index,
                    args.cadical,
                    temporary,
                )
                observed_hashes.append(witness_hash)
                total_seconds += elapsed
    except (
        OSError,
        ValueError,
        KeyError,
        TypeError,
        json.JSONDecodeError,
        subprocess.SubprocessError,
    ) as error:
        print(f"FAIL: {error}", file=sys.stderr)
        return 1
    print(
        "RESULT: all 12 stored shell-18 root witnesses extend to SAT "
        "models of their pinned v2 root CNFs"
    )
    print(f"unique_witness_hashes={len(set(observed_hashes))}")
    print(f"serial_elapsed={total_seconds:.2f}s")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
