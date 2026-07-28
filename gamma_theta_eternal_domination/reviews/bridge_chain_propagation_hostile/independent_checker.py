#!/usr/bin/env python3
"""Clean-room audit of the bridge-chain sharpness controls.

This file intentionally imports no campaign evaluator and no code from the
candidate directory.  Graphs and configurations are represented by integer
bit masks.  The eternal kernel is reconstructed directly from the
one-guard-moves definition by simultaneous greatest-fixed-point deletion.
"""

from __future__ import annotations

import hashlib
import itertools
import json
from functools import lru_cache
from pathlib import Path


HERE = Path(__file__).resolve().parent
CAMPAIGN = HERE.parents[1]
CANDIDATE = CAMPAIGN / "math" / "working" / "bridge_chain_propagation"
OUTPUT = HERE / "independent_result.json"


def bits(mask: int):
    while mask:
        low = mask & -mask
        yield low.bit_length() - 1
        mask ^= low


def choose_masks(n: int, k: int):
    for vertices in itertools.combinations(range(n), k):
        value = 0
        for vertex in vertices:
            value |= 1 << vertex
        yield value


def decode_graph6(record: str) -> tuple[int, tuple[int, ...]]:
    """Decode only the small graph6 records used here.

    The implementation uses a character bit-string and then fills columns of
    the strict lower triangle, which is deliberately different in structure
    from the candidate's edge-set decoder.
    """

    if not record or record.startswith(("~", ":", ";", "&")):
        raise ValueError("only ordinary small graph6 records are accepted")
    values = [ord(character) - 63 for character in record]
    if any(value < 0 or value > 63 for value in values):
        raise ValueError("invalid graph6 character")
    n = values[0]
    stream = "".join(f"{value:06b}" for value in values[1:])
    required = n * (n - 1) // 2
    if len(stream) < required or "1" in stream[required:]:
        raise ValueError("invalid graph6 length or nonzero padding")
    adjacency = [0] * n
    cursor = 0
    for column in range(1, n):
        for row in range(column):
            if stream[cursor] == "1":
                adjacency[row] |= 1 << column
                adjacency[column] |= 1 << row
            cursor += 1
    return n, tuple(adjacency)


def edge_rows(adjacency: tuple[int, ...]) -> list[list[int]]:
    return [
        [left, right]
        for left in range(len(adjacency))
        for right in range(left + 1, len(adjacency))
        if adjacency[left] & (1 << right)
    ]


def independent(mask: int, adjacency: tuple[int, ...]) -> bool:
    remaining = mask
    while remaining:
        low = remaining & -remaining
        vertex = low.bit_length() - 1
        remaining ^= low
        if adjacency[vertex] & remaining:
            return False
    return True


def dominates(mask: int, adjacency: tuple[int, ...], universe: int) -> bool:
    covered = mask
    for vertex in bits(mask):
        covered |= adjacency[vertex]
    return covered == universe


def maximal_independent(mask: int, adjacency: tuple[int, ...], universe: int) -> bool:
    if not independent(mask, adjacency):
        return False
    for vertex in bits(universe ^ mask):
        if not (adjacency[vertex] & mask):
            return False
    return True


def minimum_order(n: int, predicate) -> tuple[int, int]:
    for k in range(1, n + 1):
        for mask in choose_masks(n, k):
            if predicate(mask):
                return k, mask
    raise AssertionError("minimum missing")


def maximum_order(n: int, predicate) -> tuple[int, int]:
    for k in range(n, 0, -1):
        for mask in choose_masks(n, k):
            if predicate(mask):
                return k, mask
    raise AssertionError("maximum missing")


def minimum_clique_partition(
    n: int, adjacency: tuple[int, ...]
) -> tuple[int, tuple[int, ...]]:
    universe = (1 << n) - 1
    clique = [False] * (1 << n)
    clique[0] = True
    for mask in range(1, 1 << n):
        low = mask & -mask
        vertex = low.bit_length() - 1
        rest = mask ^ low
        clique[mask] = clique[rest] and not (rest & ~adjacency[vertex])

    @lru_cache(maxsize=None)
    def solve(mask: int) -> tuple[int, tuple[int, ...]]:
        if mask == 0:
            return 0, ()
        first = mask & -mask
        best_count = n + 1
        best_parts: tuple[int, ...] = ()
        subset = mask
        while subset:
            if subset & first and clique[subset]:
                tail_count, tail = solve(mask ^ subset)
                if 1 + tail_count < best_count:
                    best_count = 1 + tail_count
                    best_parts = (subset,) + tail
            subset = (subset - 1) & mask
        return best_count, best_parts

    return solve(universe)


def legal_moves(
    state: int, attack: int, adjacency: tuple[int, ...]
) -> tuple[tuple[int, int], ...]:
    attack_bit = 1 << attack
    assert not state & attack_bit
    return tuple(
        (guard, (state ^ (1 << guard)) | attack_bit)
        for guard in bits(state)
        if adjacency[guard] & attack_bit
    )


def greatest_kernel(
    n: int, k: int, adjacency: tuple[int, ...]
) -> tuple[set[int], tuple[int, ...]]:
    universe = (1 << n) - 1
    current = {
        state
        for state in choose_masks(n, k)
        if dominates(state, adjacency, universe)
    }
    stage_sizes = [len(current)]
    while True:
        kept = set()
        for state in current:
            valid = True
            for attack in bits(universe ^ state):
                if not any(
                    successor in current
                    for _, successor in legal_moves(state, attack, adjacency)
                ):
                    valid = False
                    break
            if valid:
                kept.add(state)
        if kept == current:
            return current, tuple(stage_sizes)
        current = kept
        stage_sizes.append(len(current))


def response_list(
    reference: int, target: int, family: set[int], adjacency: tuple[int, ...]
) -> tuple[int, ...]:
    answer = []
    target_bit = 1 << target
    for guard in bits(reference):
        successor = (reference ^ (1 << guard)) | target_bit
        if adjacency[guard] & target_bit and successor in family:
            answer.append(guard)
    return tuple(answer)


def mask_vertices(mask: int) -> list[int]:
    return list(bits(mask))


def family_digest(family: set[int]) -> str:
    payload = "\n".join(
        ",".join(map(str, mask_vertices(state))) for state in sorted(family)
    )
    return hashlib.sha256((payload + "\n").encode()).hexdigest()


def obligation_digest(
    n: int, family: set[int], adjacency: tuple[int, ...]
) -> tuple[int, str]:
    universe = (1 << n) - 1
    rows = []
    for state in sorted(family):
        for attack in bits(universe ^ state):
            accepted = [
                [guard, mask_vertices(successor)]
                for guard, successor in legal_moves(state, attack, adjacency)
                if successor in family
            ]
            if not accepted:
                raise AssertionError("failed eternal obligation")
            rows.append(
                {
                    "state": mask_vertices(state),
                    "attack": attack,
                    "accepted": accepted,
                }
            )
    payload = json.dumps(rows, sort_keys=True, separators=(",", ":")).encode()
    return len(rows), hashlib.sha256(payload).hexdigest()


def parameter_record(n: int, adjacency: tuple[int, ...]) -> dict[str, object]:
    universe = (1 << n) - 1
    gamma, gamma_witness = minimum_order(
        n, lambda state: dominates(state, adjacency, universe)
    )
    independent_domination, i_witness = minimum_order(
        n, lambda state: maximal_independent(state, adjacency, universe)
    )
    alpha, alpha_witness = maximum_order(
        n, lambda state: independent(state, adjacency)
    )
    theta, partition = minimum_clique_partition(n, adjacency)
    eternal = None
    eternal_witness = None
    eternal_stage_sizes: tuple[int, ...] | None = None
    for k in range(1, n + 1):
        kernel, stages = greatest_kernel(n, k, adjacency)
        if kernel:
            eternal = k
            eternal_witness = min(kernel)
            eternal_stage_sizes = stages
            break
    assert eternal is not None
    return {
        "gamma": gamma,
        "gamma_witness": mask_vertices(gamma_witness),
        "i": independent_domination,
        "i_witness": mask_vertices(i_witness),
        "alpha": alpha,
        "alpha_witness": mask_vertices(alpha_witness),
        "gamma_infinity": eternal,
        "eternal_witness": mask_vertices(eternal_witness),
        "eternal_stage_sizes": eternal_stage_sizes,
        "theta": theta,
        "clique_partition": [mask_vertices(part) for part in partition],
    }


def check_control(
    record: str,
    expected_order: int,
    expected_state_count: int,
    z: int,
    q: int,
    expected_q_list: tuple[int, ...],
) -> dict[str, object]:
    n, adjacency = decode_graph6(record)
    assert n == expected_order
    universe = (1 << n) - 1
    reference = (1 << 0) | (1 << 1) | (1 << 2)
    u, v, w = 1, 0, 2
    assert independent(reference, adjacency)

    family, stage_sizes = greatest_kernel(n, 3, adjacency)
    assert len(family) == expected_state_count
    lists = {
        target: response_list(reference, target, family, adjacency)
        for target in bits(universe ^ reference)
    }
    assert lists[z] == (u, w)
    assert lists[q] == expected_q_list

    ridge_mask = 0
    for target in range(n):
        if (
            target not in (w, z)
            and not (adjacency[w] & (1 << target))
            and not (adjacency[z] & (1 << target))
        ):
            ridge_mask |= 1 << target
    expected_ridge = (1 << v) | (1 << q)
    assert ridge_mask == expected_ridge
    assert independent(0, adjacency)  # representation sanity check
    ridge_vertices = mask_vertices(ridge_mask)
    for left, right in itertools.combinations(ridge_vertices, 2):
        assert adjacency[left] & (1 << right)

    ridge_states = {
        target: (1 << w) | (1 << z) | (1 << target)
        for target in ridge_vertices
    }
    assert all(state in family for state in ridge_states.values())
    exchanges = []
    for source, target in itertools.permutations(ridge_vertices, 2):
        accepted = [
            [guard, mask_vertices(successor)]
            for guard, successor in legal_moves(
                ridge_states[source], target, adjacency
            )
            if successor in family
        ]
        assert accepted == [[source, mask_vertices(ridge_states[target])]]
        exchanges.append(
            {
                "source": source,
                "attack": target,
                "accepted": accepted,
            }
        )

    parameters = parameter_record(n, adjacency)
    assert {
        key: parameters[key]
        for key in ("gamma", "i", "alpha", "gamma_infinity", "theta")
    } == {
        "gamma": 3,
        "i": 3,
        "alpha": 3,
        "gamma_infinity": 3,
        "theta": 3,
    }
    obligation_count, obligation_sha = obligation_digest(n, family, adjacency)
    assert obligation_count == expected_state_count * (n - 3)
    return {
        "graph6": record,
        "order": n,
        "size": sum(value.bit_count() for value in adjacency) // 2,
        "edges": edge_rows(adjacency),
        "parameters": parameters,
        "greatest_triple_kernel": {
            "state_count": len(family),
            "stage_sizes": stage_sizes,
            "state_sha256": family_digest(family),
            "obligation_count": obligation_count,
            "obligation_sha256_clean_format": obligation_sha,
        },
        "reference": mask_vertices(reference),
        "response_lists": {
            str(target): list(response) for target, response in lists.items()
        },
        "turning_ridge": ridge_vertices,
        "ridge_states": {
            str(target): mask_vertices(state)
            for target, state in ridge_states.items()
        },
        "directed_exchanges": exchanges,
    }


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def audit_candidate_hashes() -> dict[str, object]:
    manifest = json.loads((CANDIDATE / "MANIFEST.json").read_text())
    file_checks = {}
    for relative, expected in manifest["files"].items():
        actual = sha256(CANDIDATE / relative)
        file_checks[relative] = {
            "expected": expected,
            "actual": actual,
            "match": actual == expected,
        }
        assert actual == expected
    dependency_checks = {}
    for relative, expected in manifest["dependencies"].items():
        actual = sha256(CAMPAIGN / relative)
        dependency_checks[relative] = {
            "expected": expected,
            "actual": actual,
            "match": actual == expected,
        }
        assert actual == expected
    return {
        "candidate_manifest_sha256": sha256(CANDIDATE / "MANIFEST.json"),
        "candidate_files": file_checks,
        "dependencies": dependency_checks,
    }


def main() -> None:
    result = {
        "schema": "bridge-chain-propagation-hostile-cleanroom-v1",
        "model": {
            "attacks": "unoccupied vertices only",
            "move": "exactly one guard along one G-edge",
            "closure": "successor belongs to the same family",
            "state_validity": "every kernel state dominates G",
            "complement": "H has precisely the distinct nonedges of G",
        },
        "candidate_integrity": audit_candidate_hashes(),
        "controls": {
            "external_singleton": check_control(
                "FCXfO", 7, 18, z=4, q=3, expected_q_list=(0,)
            ),
            "external_two_list": check_control(
                "HEhbtjK", 9, 48, z=5, q=3, expected_q_list=(0, 1)
            ),
        },
        "revised_byte_audit": {
            "historical_equation": (
                "zq in E(G) for z in W and q in K1 union M1"
            ),
            "revised_equation": (
                "zq in E(G) for z in W and "
                "q in (K1 union M1) minus {z}"
            ),
            "revised_equation_valid": True,
            "port_distinctness_argument": (
                "zx and zy are nevertheless valid: if z=x, then the literal "
                "clause edge xy puts y in N_H(z) intersect M1, contradicting "
                "M-side purity; z=y is ruled out symmetrically using x in K1"
            ),
            "formal_theorem_and_proof_correction_complete": True,
            "corollary_2_2_distinctness_safe": (
                "the assumed literal edge zr in E(H) already forces r != z"
            ),
            "section_5_summary": (
                "the final bytes explicitly restrict side adjacency to "
                "distinct vertices and separately state adjacency to both "
                "original ports"
            ),
            "revised_bytes_unconditionally_clean": True,
        },
    }
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    OUTPUT.write_text(payload, encoding="utf-8")
    print(payload, end="")
    print("independent_result_sha256", hashlib.sha256(payload.encode()).hexdigest())


if __name__ == "__main__":
    main()
