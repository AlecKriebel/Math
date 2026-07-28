#!/usr/bin/env python3
"""Clean-room coverage, reconstruction, and DRAT replay for inactive C7.

This checker intentionally does not import the certificate generator or
``probe.py``.  It enumerates the 877 set partitions independently, rebuilds
the D7 orbit map, reconstructs every representative DIMACS instance, checks
all hashes, and replays all 93 proofs.
"""

from __future__ import annotations

import argparse
import collections
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
    for suffix in itertools.product(range(7), repeat=6):
        row = (0, *suffix)
        maximum = 0
        for index, value in enumerate(row[1:], 1):
            if value > maximum + 1:
                break
            maximum = max(maximum, value)
        else:
            rows.append("".join(map(str, row)))
    return tuple(rows)


def relabel(values: tuple[int, ...]) -> str:
    old_to_new: dict[int, int] = {}
    row: list[str] = []
    for value in values:
        if value not in old_to_new:
            old_to_new[value] = len(old_to_new)
        row.append(str(old_to_new[value]))
    return "".join(row)


def orbit(partition: str) -> frozenset[str]:
    values = tuple(map(int, partition))
    result: set[str] = set()
    for direction in (values, tuple(reversed(values))):
        for offset in range(7):
            result.add(relabel(direction[offset:] + direction[:offset]))
    return frozenset(result)


def representative(partition: str) -> str:
    return min(orbit(partition))


def expected_dimacs(partition: str) -> tuple[bytes, dict[str, int]]:
    labels = tuple(map(int, partition))
    blocks = max(labels) + 1
    order = 8 + blocks
    target = order - 1
    vertices = tuple(range(order))
    triples = tuple(itertools.combinations(vertices, 3))

    variable = 1
    edge: dict[tuple[int, int], int] = {}
    for pair in itertools.combinations(vertices, 2):
        edge[pair] = variable
        variable += 1
    family: dict[tuple[int, int, int], int] = {}
    for state in triples:
        family[state] = variable
        variable += 1
    move: dict[tuple[tuple[int, int, int], int, int], int] = {}
    for state in triples:
        for attacked in vertices:
            if attacked in state:
                continue
            for guard in state:
                move[(state, attacked, guard)] = variable
                variable += 1

    def h(first: int, second: int) -> int:
        return edge[tuple(sorted((first, second)))]

    clauses: list[tuple[int, ...]] = []

    # Every retained triple dominates the finite template in G.
    for state in triples:
        for attacked in vertices:
            if attacked in state:
                continue
            clauses.append(
                (
                    -family[state],
                    -h(attacked, state[0]),
                    -h(attacked, state[1]),
                    -h(attacked, state[2]),
                )
            )

    # For every unoccupied attack, one current guard follows a G-edge and
    # the resulting triple remains retained.
    for state in triples:
        for attacked in vertices:
            if attacked in state:
                continue
            choices: list[int] = []
            for guard in state:
                response = move[(state, attacked, guard)]
                successor = tuple(sorted((set(state) - {guard}) | {attacked}))
                choices.append(response)
                clauses.append((-response, -h(guard, attacked)))
                clauses.append((-response, family[successor]))
            clauses.append((-family[state], *choices))

    rim_edges = {
        tuple(sorted((vertex, (vertex + 1) % 7)))
        for vertex in range(7)
    }
    for pair in itertools.combinations(range(7), 2):
        clauses.append((h(*pair) if pair in rim_edges else -h(*pair),))

    for index, label in enumerate(labels):
        following = (index + 1) % 7
        witness = 7 + label
        named = tuple(sorted((index, following, witness)))
        clauses.extend(
            (
                (h(index, witness),),
                (h(following, witness),),
                (family[named],),
                (-family[tuple(sorted((following, witness, target)))],),
                (-family[tuple(sorted((index, witness, target)))],),
            )
        )

    variable_count = variable - 1
    rows = [f"p cnf {variable_count} {len(clauses)}"]
    rows.extend(" ".join(map(str, clause)) + " 0" for clause in clauses)
    return ("\n".join(rows) + "\n").encode("ascii"), {
        "order": order,
        "block_count": blocks,
        "variables": variable_count,
        "clauses": len(clauses),
        "target": target,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--bundle",
        type=Path,
        default=Path(__file__).resolve().parent / "certificates_c7",
    )
    arguments = parser.parse_args()
    bundle = arguments.bundle.resolve()
    manifest_path = bundle / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))

    partitions = all_rgs()
    assert len(partitions) == 877
    orbit_map = {
        partition: representative(partition) for partition in partitions
    }
    representatives = tuple(sorted(set(orbit_map.values())))
    assert len(representatives) == 93
    orbit_size_histogram = collections.Counter(
        len(orbit(row)) for row in representatives
    )
    assert orbit_size_histogram == {1: 2, 7: 57, 14: 34}

    assert manifest["schema"] == "inactive-c7-dihedral-certificates-v1"
    coverage = manifest["coverage"]
    assert coverage["partition_count"] == 877
    assert coverage["representative_count"] == 93
    assert tuple(coverage["partitions"]) == partitions
    assert tuple(coverage["representatives"]) == representatives
    assert coverage["orbit_map"] == orbit_map
    assert coverage["group"] == "D_7 generated by cyclic shift and reversal"

    checker = Path(manifest["checker"]["path"]).resolve()
    solver = Path(manifest["solver"]["path"]).resolve()
    assert digest(checker) == manifest["checker"]["sha256"]
    assert digest(solver) == manifest["solver"]["sha256"]

    records = manifest["cases"]
    assert len(records) == 93
    assert tuple(record["partition"] for record in records) == representatives
    total_clauses = 0
    total_proof_bytes = 0
    orders: collections.Counter[int] = collections.Counter()

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
            7 + int(character) for character in partition
        ]
        assert record["orbit_size"] == sum(
            value == partition for value in orbit_map.values()
        )
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
        orders[statistics["order"]] += 1

    result = {
        "schema": "inactive-c7-independent-audit-v1",
        "partition_count": 877,
        "representative_count": 93,
        "orbit_size_histogram": dict(sorted(orbit_size_histogram.items())),
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
    encoded = json.dumps(result, indent=2, sort_keys=True) + "\n"
    result_path = Path(__file__).with_name("independent_c7_result.json")
    result_path.write_text(encoded, encoding="utf-8")
    print(encoded, end="")
    print("sha256", hashlib.sha256(encoded.encode()).hexdigest())


if __name__ == "__main__":
    main()
