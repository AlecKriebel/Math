#!/usr/bin/env python3
"""Extract semantic input-clause cores from an inactive-rim formula."""

from __future__ import annotations

import argparse
import collections
import importlib.util
import json
import subprocess
import tempfile
from pathlib import Path

PROBE_PATH = Path(__file__).with_name("probe.py")
PROBE_SPEC = importlib.util.spec_from_file_location("inactive_rim_probe", PROBE_PATH)
if PROBE_SPEC is None or PROBE_SPEC.loader is None:
    raise RuntimeError("cannot load probe.py")
PROBE = importlib.util.module_from_spec(PROBE_SPEC)
PROBE_SPEC.loader.exec_module(PROBE)
build = PROBE.build


def read_dimacs_clauses(path: Path) -> list[tuple[int, ...]]:
    result: list[tuple[int, ...]] = []
    for line in path.read_text(encoding="ascii").splitlines():
        if not line or line[0] in "cp":
            continue
        literals = tuple(map(int, line.split()))
        if literals[-1] != 0:
            raise ValueError("unterminated clause")
        result.append(literals[:-1])
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cycle-length", type=int, required=True)
    parser.add_argument("--partition", required=True)
    parser.add_argument("--solver", type=Path, required=True)
    parser.add_argument("--checker", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--force-family", action="append", default=[])
    parser.add_argument("--forbid-family", action="append", default=[])
    arguments = parser.parse_args()

    cnf, metadata = build(
        arguments.cycle_length,
        arguments.partition,
        False,
        frozenset(),
        tuple(
            tuple(map(int, value.split(",")))
            for value in arguments.force_family
        ),
        tuple(
            tuple(map(int, value.split(",")))
            for value in arguments.forbid_family
        ),
    )
    by_clause: dict[tuple[int, ...], list[str]] = collections.defaultdict(list)
    for clause, group in zip(cnf.clauses, cnf.groups):
        by_clause[tuple(sorted(clause))].append(group)

    with tempfile.TemporaryDirectory(prefix="inactive-rim-core-") as temporary:
        temporary_path = Path(temporary)
        instance = temporary_path / "instance.cnf"
        proof = temporary_path / "proof.drat"
        core = temporary_path / "core.cnf"
        instance.write_text(cnf.dimacs(), encoding="ascii")
        solved = subprocess.run(
            [str(arguments.solver.resolve()), "-q", str(instance), str(proof)],
            check=False,
            capture_output=True,
            text=True,
        )
        if solved.returncode != 20:
            raise RuntimeError("formula was not UNSAT")
        checked = subprocess.run(
            [
                str(arguments.checker.resolve()),
                str(instance),
                str(proof),
                "-c",
                str(core),
                "-O",
            ],
            check=False,
            capture_output=True,
            text=True,
        )
        if checked.returncode != 0:
            raise RuntimeError(checked.stdout + checked.stderr)
        core_clauses = read_dimacs_clauses(core)

    core_groups: list[str] = []
    core_records: list[dict[str, object]] = []
    missing: list[list[int]] = []
    for clause in core_clauses:
        choices = by_clause.get(tuple(sorted(clause)))
        if choices:
            group = choices[0]
            core_groups.append(group)
            core_records.append(
                {
                    "group": group,
                    "literals": [
                        ("" if literal > 0 else "-")
                        + cnf.names[abs(literal)]
                        for literal in clause
                    ],
                }
            )
        else:
            missing.append(list(clause))
    result = {
        "schema": "inactive-rim-semantic-core-v1",
        **metadata,
        "input_clause_count": len(cnf.clauses),
        "core_clause_count": len(core_clauses),
        "unmatched_core_clauses": missing,
        "core_group_prefix_counts": dict(
            sorted(
                collections.Counter(
                    group.split("_", 1)[0] for group in core_groups
                ).items()
            )
        ),
        "core_groups": sorted(set(core_groups)),
        "core_records": core_records,
    }
    arguments.output.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
