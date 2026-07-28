#!/usr/bin/env python3
"""Generate and verify the 52 local certificates for the inactive-C5 lemma.

The graph variables encode H = complement(G) on a finite template consisting
of a named induced C5, one common-neighbor witness for each rim edge (with all
possible identifications), and a target x.  Family variables encode membership
in an arbitrary family of dominating triples.  Closure is the literal
one-guard-moves rule, restricted to attacks at template vertices.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import subprocess
from pathlib import Path


Pair = tuple[int, int]
Triple = tuple[int, int, int]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def restricted_growth_strings(length: int) -> tuple[str, ...]:
    rows: list[str] = []

    def visit(prefix: tuple[int, ...], maximum: int) -> None:
        if len(prefix) == length:
            rows.append("".join(map(str, prefix)))
            return
        for value in range(maximum + 2):
            visit(prefix + (value,), max(maximum, value))

    visit((0,), 0)
    return tuple(rows)


class CNF:
    def __init__(self) -> None:
        self.names: list[str] = [""]
        self.clauses: list[tuple[int, ...]] = []

    def variable(self, name: str) -> int:
        self.names.append(name)
        return len(self.names) - 1

    def add(self, *literals: int) -> None:
        clause = tuple(literals)
        if (
            not clause
            or any(type(literal) is not int or literal == 0 for literal in clause)
            or len(set(clause)) != len(clause)
            or any(-literal in clause for literal in clause)
        ):
            raise ValueError("malformed clause")
        self.clauses.append(clause)

    def dimacs(self) -> bytes:
        rows = [f"p cnf {len(self.names) - 1} {len(self.clauses)}"]
        rows.extend(" ".join(map(str, clause)) + " 0" for clause in self.clauses)
        return ("\n".join(rows) + "\n").encode("ascii")


def build(partition: str) -> tuple[CNF, dict[str, object]]:
    if partition not in restricted_growth_strings(5):
        raise ValueError("partition is not a length-five RGS")
    labels = tuple(map(int, partition))
    block_count = max(labels) + 1
    n = 5 + block_count + 1
    target = n - 1
    vertices = range(n)
    triples = tuple(itertools.combinations(vertices, 3))

    cnf = CNF()
    edge = {
        pair: cnf.variable(f"h_{pair[0]}_{pair[1]}")
        for pair in itertools.combinations(vertices, 2)
    }
    family = {
        state: cnf.variable("f_" + "_".join(map(str, state)))
        for state in triples
    }
    move = {
        (state, attacked, guard): cnf.variable(
            "m_"
            + "_".join(map(str, state))
            + f"__{attacked}_{guard}"
        )
        for state in triples
        for attacked in vertices
        if attacked not in state
        for guard in state
    }

    def h(first: int, second: int) -> int:
        return edge[tuple(sorted((first, second)))]

    # Every retained state dominates the template in G.
    for state in triples:
        for attacked in vertices:
            if attacked not in state:
                cnf.add(
                    -family[state],
                    -h(attacked, state[0]),
                    -h(attacked, state[1]),
                    -h(attacked, state[2]),
                )

    # Literal one-guard closure for every unoccupied template attack.
    for state in triples:
        for attacked in vertices:
            if attacked in state:
                continue
            choices: list[int] = []
            for guard in state:
                response = move[(state, attacked, guard)]
                successor = tuple(
                    sorted((set(state) - {guard}) | {attacked})
                )
                choices.append(response)
                cnf.add(-response, -h(guard, attacked))
                cnf.add(-response, family[successor])
            cnf.add(-family[state], *choices)

    # The named rim is an induced C5 in H.
    rim_edges = {
        tuple(sorted((index, (index + 1) % 5)))
        for index in range(5)
    }
    for pair in itertools.combinations(range(5), 2):
        cnf.add(h(*pair) if pair in rim_edges else -h(*pair))

    # Each rim edge has a selected independent-triple witness.  Both rim
    # endpoints are inactive at x, so neither corresponding successor is
    # retained.
    witness_vertices: list[int] = []
    for index, label in enumerate(labels):
        witness = 5 + label
        witness_vertices.append(witness)
        following = (index + 1) % 5
        triangle = tuple(sorted((index, following, witness)))
        cnf.add(h(index, witness))
        cnf.add(h(following, witness))
        cnf.add(family[triangle])
        cnf.add(-family[tuple(sorted((following, witness, target)))])
        cnf.add(-family[tuple(sorted((index, witness, target)))])

    metadata = {
        "partition": partition,
        "block_count": block_count,
        "order": n,
        "target": target,
        "witness_vertices": witness_vertices,
        "variables": len(cnf.names) - 1,
        "clauses": len(cnf.clauses),
        "literal_count": sum(map(len, cnf.clauses)),
    }
    return cnf, metadata


def run_checked(command: list[str], output: Path) -> subprocess.CompletedProcess[str]:
    completed = subprocess.run(
        command,
        check=False,
        capture_output=True,
        text=True,
    )
    output.write_text(completed.stdout + completed.stderr, encoding="utf-8")
    return completed


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--solver", type=Path, required=True)
    parser.add_argument("--checker", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    arguments = parser.parse_args()

    solver = arguments.solver.resolve()
    checker = arguments.checker.resolve()
    output = arguments.output.resolve()
    output.mkdir(parents=True, exist_ok=True)
    cases_dir = output / "cases"
    cases_dir.mkdir(exist_ok=True)

    records: list[dict[str, object]] = []
    for partition in restricted_growth_strings(5):
        cnf, metadata = build(partition)
        stem = cases_dir / partition
        instance = stem.with_suffix(".cnf")
        proof = stem.with_suffix(".drat")
        solver_log = stem.with_suffix(".solver.txt")
        checker_log = stem.with_suffix(".checker.txt")
        instance.write_bytes(cnf.dimacs())

        solved = run_checked(
            [str(solver), str(instance), str(proof)],
            solver_log,
        )
        if solved.returncode != 20 or "s UNSATISFIABLE" not in solved.stdout:
            raise RuntimeError(f"solver did not prove UNSAT for {partition}")
        checked = run_checked(
            [str(checker), str(instance), str(proof)],
            checker_log,
        )
        checker_text = checked.stdout + checked.stderr
        if checked.returncode != 0 or "s VERIFIED" not in checker_text:
            raise RuntimeError(f"proof checker rejected {partition}")

        record = dict(metadata)
        record.update(
            {
                "instance": instance.relative_to(output).as_posix(),
                "instance_sha256": sha256(instance),
                "proof": proof.relative_to(output).as_posix(),
                "proof_sha256": sha256(proof),
                "proof_size_bytes": proof.stat().st_size,
                "solver_log": solver_log.relative_to(output).as_posix(),
                "solver_log_sha256": sha256(solver_log),
                "checker_log": checker_log.relative_to(output).as_posix(),
                "checker_log_sha256": sha256(checker_log),
                "solver_returncode": solved.returncode,
                "checker_returncode": checked.returncode,
                "checker_verified": True,
            }
        )
        records.append(record)

    manifest = {
        "schema": "inactive-c5-local-certificates-v1",
        "model": "one-guard-moves; unoccupied attacks only",
        "scope": (
            "all 52 equality patterns of five rim-edge witnesses; "
            "template domination and attacks only"
        ),
        "partition_count": len(records),
        "partitions": list(restricted_growth_strings(5)),
        "solver": {
            "path": str(solver),
            "sha256": sha256(solver),
        },
        "checker": {
            "path": str(checker),
            "sha256": sha256(checker),
        },
        "cases": records,
    }
    manifest_path = output / "manifest.json"
    manifest_path.write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(
        json.dumps(
            {
                "manifest": str(manifest_path),
                "manifest_sha256": sha256(manifest_path),
                "partition_count": len(records),
                "all_verified": True,
                "total_proof_bytes": sum(
                    int(record["proof_size_bytes"]) for record in records
                ),
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
