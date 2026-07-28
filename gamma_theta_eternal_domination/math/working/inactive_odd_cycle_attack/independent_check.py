#!/usr/bin/env python3
"""Clean-room replay of the inactive-C5 local certificate bundle.

This checker does not import the certificate generator.  It reconstructs each
DIMACS formula from the mathematical template, audits all hashes and all 52
set-partition cases, and invokes the pinned DRAT checker on every proof.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import subprocess
from pathlib import Path


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as source:
        while block := source.read(1 << 20):
            value.update(block)
    return value.hexdigest()


def all_rgs() -> tuple[str, ...]:
    rows: list[str] = []
    for values in itertools.product(range(5), repeat=4):
        row = (0, *values)
        maximum = 0
        valid = True
        for value in row[1:]:
            if value > maximum + 1:
                valid = False
                break
            maximum = max(maximum, value)
        if valid:
            rows.append("".join(map(str, row)))
    return tuple(rows)


def expected_dimacs(partition: str) -> tuple[bytes, dict[str, int]]:
    labels = tuple(int(character) for character in partition)
    blocks = max(labels) + 1
    order = blocks + 6
    target = order - 1
    vertices = tuple(range(order))
    triples = tuple(itertools.combinations(vertices, 3))

    next_variable = 1
    edge: dict[tuple[int, int], int] = {}
    for first, second in itertools.combinations(vertices, 2):
        edge[(first, second)] = next_variable
        next_variable += 1
    family: dict[tuple[int, int, int], int] = {}
    for state in triples:
        family[state] = next_variable
        next_variable += 1
    move: dict[tuple[tuple[int, int, int], int, int], int] = {}
    for state in triples:
        for attacked in vertices:
            if attacked in state:
                continue
            for guard in state:
                move[(state, attacked, guard)] = next_variable
                next_variable += 1

    def h(first: int, second: int) -> int:
        return edge[tuple(sorted((first, second)))]

    clauses: list[tuple[int, ...]] = []

    # State domination in G: an outside vertex cannot have H-edges to all
    # three occupied vertices.
    for state in triples:
        selected = family[state]
        for attacked in vertices:
            if attacked not in state:
                clauses.append(
                    (
                        -selected,
                        -h(attacked, state[0]),
                        -h(attacked, state[1]),
                        -h(attacked, state[2]),
                    )
                )

    # For each selected state and each unoccupied attack, at least one current
    # guard makes one G-edge move and the resulting state is selected.
    for state in triples:
        selected = family[state]
        for attacked in vertices:
            if attacked in state:
                continue
            replies: list[int] = []
            for guard in state:
                response = move[(state, attacked, guard)]
                successor = tuple(
                    sorted((set(state) - {guard}) | {attacked})
                )
                replies.append(response)
                clauses.append((-response, -h(guard, attacked)))
                clauses.append((-response, family[successor]))
            clauses.append((-selected, *replies))

    rim = {
        tuple(sorted((vertex, (vertex + 1) % 5)))
        for vertex in range(5)
    }
    for candidate in itertools.combinations(range(5), 2):
        clauses.append((h(*candidate) if candidate in rim else -h(*candidate),))

    for vertex, label in enumerate(labels):
        following = (vertex + 1) % 5
        witness = 5 + label
        triangle = tuple(sorted((vertex, following, witness)))
        clauses.extend(
            (
                (h(vertex, witness),),
                (h(following, witness),),
                (family[triangle],),
                (-family[tuple(sorted((following, witness, target)))],),
                (-family[tuple(sorted((vertex, witness, target)))],),
            )
        )

    variable_count = next_variable - 1
    lines = [f"p cnf {variable_count} {len(clauses)}"]
    lines.extend(" ".join(map(str, clause)) + " 0" for clause in clauses)
    encoded = ("\n".join(lines) + "\n").encode("ascii")
    return encoded, {
        "order": order,
        "block_count": blocks,
        "variables": variable_count,
        "clauses": len(clauses),
        "literal_count": sum(map(len, clauses)),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--bundle",
        type=Path,
        default=Path(__file__).resolve().parent / "certificates",
    )
    arguments = parser.parse_args()
    bundle = arguments.bundle.resolve()
    manifest_path = bundle / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))

    expected_partitions = all_rgs()
    assert len(expected_partitions) == 52
    assert manifest["schema"] == "inactive-c5-local-certificates-v1"
    assert manifest["partition_count"] == 52
    assert tuple(manifest["partitions"]) == expected_partitions
    records = manifest["cases"]
    assert len(records) == 52
    assert tuple(record["partition"] for record in records) == expected_partitions

    checker = Path(manifest["checker"]["path"]).resolve()
    solver = Path(manifest["solver"]["path"]).resolve()
    assert digest(checker) == manifest["checker"]["sha256"]
    assert digest(solver) == manifest["solver"]["sha256"]

    total_clauses = 0
    total_proof_bytes = 0
    orders: dict[int, int] = {}
    for record in records:
        partition = record["partition"]
        instance = bundle / record["instance"]
        proof = bundle / record["proof"]
        solver_log = bundle / record["solver_log"]
        checker_log = bundle / record["checker_log"]
        for path, key in (
            (instance, "instance_sha256"),
            (proof, "proof_sha256"),
            (solver_log, "solver_log_sha256"),
            (checker_log, "checker_log_sha256"),
        ):
            assert digest(path) == record[key]

        expected, statistics = expected_dimacs(partition)
        assert instance.read_bytes() == expected
        for key, value in statistics.items():
            assert record[key] == value
        assert record["witness_vertices"] == [
            5 + int(character) for character in partition
        ]
        assert record["target"] == record["order"] - 1
        assert record["solver_returncode"] == 20
        assert record["checker_returncode"] == 0
        assert record["checker_verified"] is True
        assert "s UNSATISFIABLE" in solver_log.read_text(encoding="utf-8")
        assert "s VERIFIED" in checker_log.read_text(encoding="utf-8")

        replay = subprocess.run(
            [str(checker), str(instance), str(proof)],
            check=False,
            capture_output=True,
            text=True,
        )
        assert replay.returncode == 0
        assert "s VERIFIED" in replay.stdout + replay.stderr
        total_clauses += statistics["clauses"]
        total_proof_bytes += proof.stat().st_size
        orders[statistics["order"]] = orders.get(statistics["order"], 0) + 1

    payload = {
        "schema": "inactive-c5-independent-audit-v1",
        "partition_count": 52,
        "partition_coverage": "all length-five set partitions",
        "orders_histogram": dict(sorted(orders.items())),
        "total_clauses_reconstructed": total_clauses,
        "total_proof_bytes": total_proof_bytes,
        "all_instance_bytes_match": True,
        "all_drat_proofs_verified": True,
        "one_guard_semantics": {
            "attacks_only_unoccupied": True,
            "exactly_one_current_guard_moves": True,
            "move_requires_G_edge": True,
            "successor_must_be_retained": True,
            "every_retained_state_dominates": True,
        },
    }
    encoded = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    result = Path(__file__).resolve().parent / "independent_result.json"
    result.write_text(encoded, encoding="utf-8")
    print(encoded, end="")
    print("sha256", hashlib.sha256(encoded.encode()).hexdigest())


if __name__ == "__main__":
    main()
