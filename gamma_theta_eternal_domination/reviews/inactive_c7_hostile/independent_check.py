#!/usr/bin/env python3
"""Hostile clean-room audit of the inactive witnessed-C7 certificate.

This file deliberately imports no campaign evaluator, candidate generator,
or candidate reconstruction code.  It derives the D7 action from vertex
maps of the cycle, constructs every representative CNF from the literal
one-guard definition, replays every DRAT proof, and performs a separate
bounded audit of the two human propagation statements.
"""

from __future__ import annotations

import collections
import hashlib
import itertools
import json
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
CAMPAIGN = HERE.parents[1]
CANDIDATE = CAMPAIGN / "math" / "working" / "inactive_odd_cycle_generalization"
BUNDLE = CANDIDATE / "certificates_c7"

FROZEN_HASHES = {
    "NOTE.md": "59b328983b2d240ec2b7aa078a474d9d4a1c18c307ceefd5a0c64da161997883",
    "RESEARCH_LOG.md": "20975c756cedbe0800f3457be10aefa453954b20ccaa5a4866d3609df0c66787",
    "MANIFEST.json": "f9b367c1f15e3691a2257ff28562c5d2cd0b89c043d44ac16e48b5095d473f4e",
    "certify_c7.py": "c34558a27e5e54ef31272c6368e5672d02acf021b2eb5046930dc337aa28c9c3",
    "independent_check.py": "3f6d65361f65bc79b27dc78fa8ab6a824dc706847db5c753a3688f94c632c78e",
    "independent_c7_result.json": "37450e8a8f5b56e2023ee924fd2fa9263b1fe10ad675049ccedc1885e42eb29b",
    "certificates_c7/manifest.json": "d5187e0a35595865f79063b02f74e6fa819aa5b0fe0b78c2c09bbdb15d148ee4",
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def word_from_blocks(blocks: tuple[tuple[int, ...], ...], length: int) -> str:
    labels = [-1] * length
    ordered = sorted(blocks, key=lambda block: min(block))
    for label, block in enumerate(ordered):
        for position in block:
            labels[position] = label
    assert all(label >= 0 for label in labels)
    return "".join(str(label) for label in labels)


def set_partition_words(length: int) -> tuple[str, ...]:
    """Generate set partitions by inserting each new point into blocks.

    This is intentionally different from restricted-growth-word scanning.
    """

    current: list[tuple[tuple[int, ...], ...]] = [((0,),)]
    for point in range(1, length):
        following: list[tuple[tuple[int, ...], ...]] = []
        for blocks in current:
            for chosen in range(len(blocks)):
                changed = list(blocks)
                changed[chosen] = changed[chosen] + (point,)
                following.append(tuple(changed))
            following.append(blocks + ((point,),))
        current = following
    words = {word_from_blocks(blocks, length) for blocks in current}
    return tuple(sorted(words))


def first_occurrence_labels(raw: tuple[int, ...]) -> tuple[str, dict[int, int]]:
    conversion: dict[int, int] = {}
    normalized: list[str] = []
    for label in raw:
        if label not in conversion:
            conversion[label] = len(conversion)
        normalized.append(str(conversion[label]))
    return "".join(normalized), conversion


def cycle_image(
    word: str, orientation: int, offset: int
) -> tuple[str, dict[int, int], tuple[int, ...]]:
    """Apply v -> orientation*v+offset and its induced edge action.

    Edge position i denotes {i,i+1}.  It maps to position i+offset for
    orientation +1 and offset-i-1 for orientation -1.
    """

    old = tuple(int(character) for character in word)
    raw_new = [-1] * 7
    rim_map = []
    for edge_position, label in enumerate(old):
        if orientation == 1:
            new_edge_position = (edge_position + offset) % 7
        else:
            new_edge_position = (offset - edge_position - 1) % 7
        raw_new[new_edge_position] = label
    for vertex in range(7):
        rim_map.append((orientation * vertex + offset) % 7)
    normalized, witness_map = first_occurrence_labels(tuple(raw_new))
    return normalized, witness_map, tuple(rim_map)


def orbit(word: str) -> frozenset[str]:
    return frozenset(
        cycle_image(word, orientation, offset)[0]
        for orientation in (1, -1)
        for offset in range(7)
    )


def hypotheses(word: str) -> dict[str, frozenset[tuple[int, ...]]]:
    labels = tuple(int(character) for character in word)
    order = 9 + max(labels)
    target = order - 1
    rim_edges = {
        tuple(sorted((index, (index + 1) % 7))) for index in range(7)
    }
    rim_nonedges = (
        set(itertools.combinations(range(7), 2)) - rim_edges
    )
    spokes: set[tuple[int, int]] = set()
    named: set[tuple[int, int, int]] = set()
    absent: set[tuple[int, int, int]] = set()
    for index, label in enumerate(labels):
        following = (index + 1) % 7
        witness = 7 + label
        spokes.add(tuple(sorted((index, witness))))
        spokes.add(tuple(sorted((following, witness))))
        named.add(tuple(sorted((index, following, witness))))
        absent.add(tuple(sorted((following, witness, target))))
        absent.add(tuple(sorted((index, witness, target))))
    return {
        "rim_edges": frozenset(rim_edges),
        "rim_nonedges": frozenset(rim_nonedges),
        "spokes": frozenset(spokes),
        "named": frozenset(named),
        "absent": frozenset(absent),
    }


def mapped_hypotheses(
    word: str, orientation: int, offset: int
) -> tuple[str, dict[str, frozenset[tuple[int, ...]]]]:
    image, witness_map, rim_map = cycle_image(word, orientation, offset)
    old_blocks = max(map(int, word)) + 1
    order = 9 + max(map(int, image))
    assert order == 8 + old_blocks
    vertex_map = {
        old: rim_map[old] for old in range(7)
    }
    for old_label, new_label in witness_map.items():
        vertex_map[7 + old_label] = 7 + new_label
    vertex_map[order - 1] = order - 1

    mapped: dict[str, frozenset[tuple[int, ...]]] = {}
    for key, records in hypotheses(word).items():
        mapped[key] = frozenset(
            tuple(sorted(vertex_map[vertex] for vertex in record))
            for record in records
        )
    return image, mapped


def reconstruct_dimacs(word: str) -> tuple[bytes, dict[str, object]]:
    labels = tuple(int(character) for character in word)
    block_count = max(labels) + 1
    order = 8 + block_count
    target = order - 1
    vertices = tuple(range(order))
    states = tuple(itertools.combinations(vertices, 3))

    next_variable = 1
    h_variable: dict[tuple[int, int], int] = {}
    for pair in itertools.combinations(vertices, 2):
        h_variable[pair] = next_variable
        next_variable += 1
    f_variable: dict[tuple[int, int, int], int] = {}
    for state in states:
        f_variable[state] = next_variable
        next_variable += 1
    response_variable: dict[
        tuple[tuple[int, int, int], int, int], int
    ] = {}
    for state in states:
        for attacked in vertices:
            if attacked in state:
                continue
            for guard in state:
                response_variable[(state, attacked, guard)] = next_variable
                next_variable += 1

    def h(first: int, second: int) -> int:
        return h_variable[tuple(sorted((first, second)))]

    clauses: list[tuple[int, ...]] = []

    # A retained state dominates an outside vertex in G iff not all three
    # guard/vertex pairs are H-edges.
    for state in states:
        for outside in vertices:
            if outside not in state:
                clauses.append(
                    (
                        -f_variable[state],
                        -h(outside, state[0]),
                        -h(outside, state[1]),
                        -h(outside, state[2]),
                    )
                )

    # Each unoccupied attack has a one-current-guard response.  A selected
    # response crosses a G-edge (an H-nonedge) and retains the one-swap state.
    for state in states:
        for attacked in vertices:
            if attacked in state:
                continue
            available: list[int] = []
            for guard in state:
                marker = response_variable[(state, attacked, guard)]
                successor = tuple(
                    sorted((set(state) - {guard}) | {attacked})
                )
                available.append(marker)
                clauses.append((-marker, -h(guard, attacked)))
                clauses.append((-marker, f_variable[successor]))
            clauses.append((-f_variable[state], *available))

    required = hypotheses(word)
    for pair in itertools.combinations(range(7), 2):
        if pair in required["rim_edges"]:
            clauses.append((h(*pair),))
        else:
            assert pair in required["rim_nonedges"]
            clauses.append((-h(*pair),))

    witness_vertices: list[int] = []
    named_states: list[list[int]] = []
    forbidden_successors: list[list[int]] = []
    for index, label in enumerate(labels):
        following = (index + 1) % 7
        witness = 7 + label
        named = tuple(sorted((index, following, witness)))
        first_absent = tuple(sorted((following, witness, target)))
        second_absent = tuple(sorted((index, witness, target)))
        witness_vertices.append(witness)
        named_states.append(list(named))
        forbidden_successors.extend(
            (list(first_absent), list(second_absent))
        )
        clauses.extend(
            (
                (h(index, witness),),
                (h(following, witness),),
                (f_variable[named],),
                (-f_variable[first_absent],),
                (-f_variable[second_absent],),
            )
        )

    rows = [f"p cnf {next_variable - 1} {len(clauses)}"]
    rows.extend(" ".join(map(str, clause)) + " 0" for clause in clauses)
    encoded = ("\n".join(rows) + "\n").encode("ascii")
    return encoded, {
        "cycle_length": 7,
        "partition": word,
        "block_count": block_count,
        "order": order,
        "target": target,
        "witness_vertices": witness_vertices,
        "named_states": named_states,
        "forbidden_successors": forbidden_successors,
        "gamma_at_least_three": False,
        "allowed_forbidden_indices": [],
        "forced_family_states": [],
        "forbidden_family_states": [],
        "variables": next_variable - 1,
        "clauses": len(clauses),
    }


def positive_even_control(length: int) -> dict[str, int]:
    """Validate the explicit three-clique product family for even rims."""

    assert length >= 4 and length % 2 == 0
    order = 2 * length + 1
    target = order - 1
    rim = tuple(range(length))
    witnesses = tuple(range(length, 2 * length))
    h_edges = {
        tuple(sorted((index, (index + 1) % length)))
        for index in rim
    }
    for index in rim:
        h_edges.add(tuple(sorted((index, length + index))))
        h_edges.add(
            tuple(sorted(((index + 1) % length, length + index)))
        )

    def adjacent_g(first: int, second: int) -> bool:
        return first != second and tuple(sorted((first, second))) not in h_edges

    parts = (
        tuple(index for index in rim if index % 2 == 0),
        tuple(index for index in rim if index % 2 == 1),
        witnesses + (target,),
    )
    assert set().union(*(set(part) for part in parts)) == set(range(order))
    for part in parts:
        assert all(adjacent_g(*pair) for pair in itertools.combinations(part, 2))

    family = {
        frozenset(choice) for choice in itertools.product(*parts)
    }
    domination_checks = 0
    closure_checks = 0
    for state in family:
        for vertex in range(order):
            assert vertex in state or any(
                adjacent_g(vertex, guard) for guard in state
            )
            domination_checks += 1
        for attacked in set(range(order)) - state:
            responses = []
            for guard in state:
                successor = frozenset((state - {guard}) | {attacked})
                if adjacent_g(guard, attacked) and successor in family:
                    responses.append(guard)
            assert responses
            closure_checks += 1
    for index in rim:
        following = (index + 1) % length
        witness = length + index
        named = frozenset((index, following, witness))
        assert named in family
        assert frozenset((following, witness, target)) not in family
        assert frozenset((index, witness, target)) not in family
    return {
        "length": length,
        "order": order,
        "family_size": len(family),
        "domination_checks": domination_checks,
        "closure_checks": closure_checks,
    }


def all_labeled_graphs(order: int):
    pairs = tuple(itertools.combinations(range(order), 2))
    for mask in range(1 << len(pairs)):
        adjacency = [set() for _ in range(order)]
        for bit, (first, second) in enumerate(pairs):
            if mask & (1 << bit):
                adjacency[first].add(second)
                adjacency[second].add(first)
        yield tuple(frozenset(row) for row in adjacency)


def dominates(
    state: frozenset[int],
    adjacency: tuple[frozenset[int], ...],
) -> bool:
    return all(
        vertex in state
        or any(vertex in adjacency[guard] for guard in state)
        for vertex in range(len(adjacency))
    )


def eternal_families(
    adjacency: tuple[frozenset[int], ...], guard_count: int
):
    vertices = set(range(len(adjacency)))
    states = tuple(
        frozenset(state)
        for state in itertools.combinations(range(len(adjacency)), guard_count)
        if dominates(frozenset(state), adjacency)
    )
    for mask in range(1, 1 << len(states)):
        family = frozenset(
            states[index]
            for index in range(len(states))
            if mask & (1 << index)
        )
        closed = True
        for state in family:
            for attacked in vertices - state:
                if not any(
                    attacked in adjacency[guard]
                    and frozenset((state - {guard}) | {attacked}) in family
                    for guard in state
                ):
                    closed = False
                    break
            if not closed:
                break
        if closed:
            yield family


def audit_human_lemmas() -> dict[str, int]:
    graph_count = 0
    family_count = 0
    private_star_premises = 0
    distance_two_contexts = 0
    distance_two_premises = 0
    failures = 0
    for order in range(1, 6):
        vertices = set(range(order))
        for adjacency in all_labeled_graphs(order):
            graph_count += 1
            for guard_count in range(1, order + 1):
                for family in eternal_families(adjacency, guard_count):
                    family_count += 1
                    for e_state in family:
                        for t_state in family:
                            if any(
                                other in adjacency[vertex]
                                for vertex, other in itertools.combinations(
                                    t_state, 2
                                )
                            ):
                                continue
                            for vertex in e_state & t_state:
                                if any(
                                    other in adjacency[vertex]
                                    for other in e_state - {vertex}
                                ):
                                    continue
                                for target in vertices - e_state - t_state:
                                    if target not in adjacency[vertex]:
                                        continue
                                    start = frozenset(
                                        (e_state - {vertex}) | {target}
                                    )
                                    if start not in family:
                                        continue
                                    private_star_premises += 1
                                    destination = frozenset(
                                        (t_state - {vertex}) | {target}
                                    )
                                    if destination not in family:
                                        failures += 1

                    if guard_count != 3:
                        continue
                    for t_state in family:
                        if any(
                            other in adjacency[vertex]
                            for vertex, other in itertools.combinations(
                                t_state, 2
                            )
                        ):
                            continue
                        for vertex in t_state:
                            for target in vertices - t_state:
                                inactive = frozenset(
                                    (t_state - {vertex}) | {target}
                                )
                                if inactive in family:
                                    continue
                                available = vertices - {vertex, target}
                                for first, second in itertools.combinations(
                                    available, 2
                                ):
                                    if (
                                        first in adjacency[vertex]
                                        or second in adjacency[vertex]
                                    ):
                                        continue
                                    alleged = frozenset(
                                        (first, second, target)
                                    )
                                    distance_two_contexts += 1
                                    if alleged in family:
                                        distance_two_premises += 1
                                        failures += 1
    assert failures == 0
    return {
        "labeled_graphs_through_order_5": graph_count,
        "arbitrary_eternal_families": family_count,
        "private_star_premises_checked": private_star_premises,
        "distance_two_contexts_checked": distance_two_contexts,
        "distance_two_forbidden_premises_found": distance_two_premises,
        "failures": failures,
    }


def main() -> None:
    for relative, expected in FROZEN_HASHES.items():
        actual = sha256(CANDIDATE / relative)
        assert actual == expected, (relative, expected, actual)

    manifest_path = BUNDLE / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    assert manifest["schema"] == "inactive-c7-dihedral-certificates-v1"
    assert manifest["model"] == "one-guard-moves; unoccupied attacks only"

    partitions = set_partition_words(7)
    assert len(partitions) == 877
    stirling = collections.Counter(
        max(map(int, word)) + 1 for word in partitions
    )
    assert stirling == {1: 1, 2: 63, 3: 301, 4: 350, 5: 140, 6: 21, 7: 1}

    orbit_map = {word: min(orbit(word)) for word in partitions}
    representatives = tuple(sorted(set(orbit_map.values())))
    assert len(representatives) == 93
    orbit_histogram = collections.Counter(
        len(orbit(word)) for word in representatives
    )
    assert orbit_histogram == {1: 2, 7: 57, 14: 34}
    assert sum(
        size * count for size, count in orbit_histogram.items()
    ) == 877

    # For every one of the 877 words, find an explicit cycle automorphism
    # taking its complete hypothesis signature to the representative.
    quotient_isomorphisms = 0
    for word in partitions:
        wanted = orbit_map[word]
        found = False
        for orientation in (1, -1):
            for offset in range(7):
                image, mapped = mapped_hypotheses(
                    word, orientation, offset
                )
                if image == wanted:
                    assert mapped == hypotheses(wanted)
                    found = True
                    break
            if found:
                break
        assert found
        quotient_isomorphisms += 1

    coverage = manifest["coverage"]
    assert coverage["partition_count"] == len(partitions)
    assert coverage["representative_count"] == len(representatives)
    assert tuple(coverage["partitions"]) == partitions
    assert tuple(coverage["representatives"]) == representatives
    assert coverage["orbit_map"] == orbit_map
    assert coverage["group"] == "D_7 generated by cyclic shift and reversal"

    proof_checker = Path(manifest["checker"]["path"]).resolve()
    solver = Path(manifest["solver"]["path"]).resolve()
    assert sha256(proof_checker) == manifest["checker"]["sha256"]
    assert sha256(solver) == manifest["solver"]["sha256"]
    assert manifest["checker"]["sha256"] == (
        "31df522b8b2b71acd357723b0e826cf488826ed78ad9e3a7bcad241271812beb"
    )
    assert manifest["solver"]["sha256"] == (
        "51c3c82b354f455c925fc60b37c701e8498afcf0f3bfab9a06e62149485df5f6"
    )

    expected_inventory = {"manifest.json"}
    for word in representatives:
        for suffix in (".cnf", ".drat", ".solver.txt", ".checker.txt"):
            expected_inventory.add(f"cases/{word}{suffix}")
    actual_inventory = {
        path.relative_to(BUNDLE).as_posix()
        for path in BUNDLE.rglob("*")
        if path.is_file()
    }
    assert actual_inventory == expected_inventory

    records = manifest["cases"]
    assert len(records) == len(representatives)
    assert tuple(record["partition"] for record in records) == representatives
    order_histogram: collections.Counter[int] = collections.Counter()
    clauses_by_group = collections.Counter()
    total_clauses = 0
    total_literals = 0
    total_proof_bytes = 0
    proof_replays = 0

    for record in records:
        word = record["partition"]
        stem = f"cases/{word}"
        expected_paths = {
            "instance": stem + ".cnf",
            "proof": stem + ".drat",
            "solver_log": stem + ".solver.txt",
            "checker_log": stem + ".checker.txt",
        }
        for key, relative in expected_paths.items():
            assert record[key] == relative
            path = (BUNDLE / relative).resolve()
            assert path.is_relative_to(BUNDLE.resolve())
            assert sha256(path) == record[key + "_sha256"]

        expected_dimacs, metadata = reconstruct_dimacs(word)
        instance = BUNDLE / record["instance"]
        assert instance.read_bytes() == expected_dimacs
        for key, value in metadata.items():
            assert record[key] == value
        assert record["orbit_size"] == sum(
            representative == word
            for representative in orbit_map.values()
        )
        assert record["solver_returncode"] == 20
        assert record["checker_returncode"] == 0
        assert record["checker_verified"] is True

        solver_log = (BUNDLE / record["solver_log"]).read_text(
            encoding="utf-8"
        )
        checker_log = (BUNDLE / record["checker_log"]).read_text(
            encoding="utf-8"
        )
        assert "s UNSATISFIABLE" in solver_log
        assert "s VERIFIED" in checker_log

        proof = BUNDLE / record["proof"]
        replay = subprocess.run(
            [str(proof_checker), str(instance), str(proof)],
            check=False,
            capture_output=True,
            text=True,
        )
        assert replay.returncode == 0
        assert "s VERIFIED" in replay.stdout + replay.stderr
        proof_replays += 1

        order = int(metadata["order"])
        state_attack_count = (
            len(tuple(itertools.combinations(range(order), 3)))
            * (order - 3)
        )
        clauses_by_group["domination"] += state_attack_count
        clauses_by_group["closure"] += 7 * state_attack_count
        clauses_by_group["induced_rim"] += 21
        clauses_by_group["named_witness_and_inactivity"] += 35
        total_clauses += int(metadata["clauses"])
        total_literals += (
            4 * state_attack_count
            + 16 * state_attack_count
            + 21
            + 35
        )
        total_proof_bytes += proof.stat().st_size
        assert record["proof_size_bytes"] == proof.stat().st_size
        order_histogram[order] += 1

    assert clauses_by_group == {
        "domination": 176716,
        "closure": 1237012,
        "induced_rim": 1953,
        "named_witness_and_inactivity": 3255,
    }
    assert total_clauses == 1418936
    assert total_literals == 3539528
    assert total_proof_bytes == 1739039
    assert order_histogram == {9: 1, 10: 8, 11: 31, 12: 33, 13: 16, 14: 3, 15: 1}

    even_controls = [
        positive_even_control(length) for length in (4, 6, 8)
    ]
    human_audit = audit_human_lemmas()

    result = {
        "schema": "inactive-c7-hostile-audit-v1",
        "verdict": "UNCONDITIONAL PASS",
        "candidate_hashes": FROZEN_HASHES,
        "coverage": {
            "partition_count": len(partitions),
            "stirling_block_histogram": dict(sorted(stirling.items())),
            "representative_count": len(representatives),
            "orbit_size_histogram": dict(sorted(orbit_histogram.items())),
            "explicit_hypothesis_isomorphisms_checked": quotient_isomorphisms,
            "order_histogram": dict(sorted(order_histogram.items())),
            "bundle_files": len(actual_inventory),
        },
        "cnf": {
            "all_representative_bytes_reconstructed": True,
            "clause_groups": dict(clauses_by_group),
            "total_clauses": total_clauses,
            "total_literals": total_literals,
        },
        "certificates": {
            "drat_proofs_replayed": proof_replays,
            "all_verified": True,
            "total_proof_bytes": total_proof_bytes,
            "proof_checker_sha256": sha256(proof_checker),
            "solver_sha256": sha256(solver),
        },
        "model": {
            "attacks_only_unoccupied": True,
            "one_current_guard_per_response": True,
            "move_along_G_edge": True,
            "successor_retained": True,
            "every_retained_state_dominates": True,
            "outside_template_omission_is_a_relaxation": True,
        },
        "positive_even_controls": even_controls,
        "human_lemma_bounded_audit": human_audit,
        "scope": {
            "inactive_induced_C7_excluded": True,
            "inactive_induced_C9_excluded": False,
            "all_inactive_odd_cycles_excluded": False,
            "complete_k3_case": False,
            "universal_conjecture_resolved": False,
        },
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
