#!/usr/bin/env python3
"""Extract a semantic input core for one inactive-path endpoint formula."""

from __future__ import annotations

import argparse
import collections
import importlib.util
import json
import subprocess
import tempfile
from pathlib import Path


PROBE_PATH = Path(__file__).with_name("probe_path5.py")
SPEC = importlib.util.spec_from_file_location("inactive_path_probe", PROBE_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("cannot load path probe")
PROBE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(PROBE)


def read_clauses(path: Path) -> list[tuple[int, ...]]:
    clauses: list[tuple[int, ...]] = []
    for line in path.read_text(encoding="ascii").splitlines():
        if not line or line[0] in "cp":
            continue
        row = tuple(map(int, line.split()))
        if row[-1] != 0:
            raise ValueError("unterminated DIMACS clause")
        clauses.append(row[:-1])
    return clauses


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--partition", required=True)
    parser.add_argument("--solver", type=Path, required=True)
    parser.add_argument("--checker", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    arguments = parser.parse_args()

    cnf, metadata = PROBE.build(arguments.partition)
    groups: dict[tuple[int, ...], list[str]] = collections.defaultdict(list)
    for clause, group in zip(cnf.clauses, cnf.groups):
        groups[tuple(sorted(clause))].append(group)

    with tempfile.TemporaryDirectory(prefix="inactive-path-core-") as temporary:
        root = Path(temporary)
        instance = root / "instance.cnf"
        proof = root / "proof.drat"
        core = root / "core.cnf"
        instance.write_text(cnf.dimacs(), encoding="ascii")
        solved = subprocess.run(
            [str(arguments.solver.resolve()), "-q", str(instance), str(proof)],
            check=False,
            capture_output=True,
            text=True,
        )
        if solved.returncode != 20:
            raise RuntimeError("formula is not UNSAT")
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
        core_clauses = read_clauses(core)

    records: list[dict[str, object]] = []
    unmatched: list[list[int]] = []
    for clause in core_clauses:
        choices = groups.get(tuple(sorted(clause)))
        if choices:
            records.append(
                {
                    "group": choices[0],
                    "literals": [
                        ("" if literal > 0 else "-")
                        + cnf.names[abs(literal)]
                        for literal in clause
                    ],
                }
            )
        else:
            unmatched.append(list(clause))

    result = {
        "schema": "inactive-path-semantic-core-v1",
        **metadata,
        "input_clause_count": len(cnf.clauses),
        "core_clause_count": len(core_clauses),
        "core_group_prefix_counts": dict(
            sorted(
                collections.Counter(
                    record["group"].split("_", 1)[0] for record in records
                ).items()
            )
        ),
        "core_groups": sorted({record["group"] for record in records}),
        "core_records": records,
        "unmatched_core_clauses": unmatched,
    }
    arguments.output.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
