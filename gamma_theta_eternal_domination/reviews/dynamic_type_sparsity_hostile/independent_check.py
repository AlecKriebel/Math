#!/usr/bin/env python3
"""Clean-room checker for the dynamic-type-sparsity sharpness control.

No candidate verifier, search implementation, graph library, or campaign
evaluator is imported.
"""

from __future__ import annotations

from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path


CAMPAIGN = Path(__file__).resolve().parents[2]
CANDIDATE = CAMPAIGN / "math/working/dynamic_type_sparsity"


def digest(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def bits(mask: int):
    while mask:
        bit = mask & -mask
        yield bit.bit_length() - 1
        mask ^= bit


def mask_of(items) -> int:
    mask = 0
    for item in items:
        bit = 1 << int(item)
        assert not (mask & bit)
        mask |= bit
    return mask


def decode_graph6(record: str) -> tuple[int, list[int]]:
    raw = record.encode("ascii")
    assert raw and raw[0] != 126
    n = raw[0] - 63
    stream = []
    for char in raw[1:]:
        value = char - 63
        assert 0 <= value < 64
        stream.extend((value >> shift) & 1 for shift in range(5, -1, -1))
    pairs = [(u, v) for v in range(1, n) for u in range(v)]
    assert len(stream) >= len(pairs)
    assert not any(stream[len(pairs) :])
    adjacency = [0] * n
    for present, (u, v) in zip(stream, pairs):
        if present:
            adjacency[u] |= 1 << v
            adjacency[v] |= 1 << u
    return n, adjacency


def adjacent(adjacency: list[int], u: int, v: int) -> bool:
    return bool(adjacency[u] & (1 << v))


def dominates(adjacency: list[int], state: int) -> bool:
    covered = state
    for guard in bits(state):
        covered |= adjacency[guard]
    return covered == (1 << len(adjacency)) - 1


def independent(adjacency: list[int], state: int) -> bool:
    return all(not (adjacency[u] & state) for u in bits(state))


def successor(state: int, mover: int, attacked: int) -> int:
    return (state ^ (1 << mover)) | (1 << attacked)


def greatest_kernel(adjacency: list[int], k: int) -> tuple[set[int], int]:
    n = len(adjacency)
    alive = {
        mask_of(state)
        for state in combinations(range(n), k)
        if dominates(adjacency, mask_of(state))
    }
    rounds = 0
    while True:
        remove = set()
        for state in alive:
            for attacked in range(n):
                if state & (1 << attacked):
                    continue
                if not any(
                    adjacent(adjacency, mover, attacked)
                    and successor(state, mover, attacked) in alive
                    for mover in bits(state)
                ):
                    remove.add(state)
                    break
        if not remove:
            return alive, rounds
        alive.difference_update(remove)
        rounds += 1


def exact_parameters(adjacency: list[int]) -> dict[str, int]:
    n = len(adjacency)
    states = list(range(1 << n))
    gamma = min(state.bit_count() for state in states if dominates(adjacency, state))
    independent_domination = min(
        state.bit_count()
        for state in states
        if independent(adjacency, state) and dominates(adjacency, state)
    )
    alpha = max(state.bit_count() for state in states if independent(adjacency, state))

    h_edges = [
        (u, v)
        for u in range(n)
        for v in range(u + 1, n)
        if not adjacent(adjacency, u, v)
    ]
    theta = None
    for k in range(1, n + 1):
        if any(
            all(colors[u] != colors[v] for u, v in h_edges)
            for colors in product(range(k), repeat=n)
        ):
            theta = k
            break
    assert theta is not None

    kernels = [greatest_kernel(adjacency, k) for k in range(1, n + 1)]
    gamma_infinity = next(k for k, (kernel, _rounds) in enumerate(kernels, 1) if kernel)
    return {
        "gamma": gamma,
        "i": independent_domination,
        "alpha": alpha,
        "gamma_infinity": gamma_infinity,
        "theta": theta,
        "kernels": kernels,
    }


def check_control(data: dict) -> dict:
    n, g_adj = decode_graph6("EFnG")
    assert n == int(data["order"]) == 6
    full = (1 << n) - 1
    h_adj = [full ^ (1 << u) ^ g_adj[u] for u in range(n)]
    decoded_h = {
        (u, v)
        for u in range(n)
        for v in range(u + 1, n)
        if adjacent(h_adj, u, v)
    }
    declared_h = {tuple(sorted(map(int, edge))) for edge in data["h_edges"]}
    assert decoded_h == declared_h == {
        (0, 1),
        (0, 2),
        (1, 2),
        (1, 4),
        (2, 5),
        (3, 5),
    }
    size = sum(mask.bit_count() for mask in g_adj) // 2
    assert size == 9

    raw_family = [tuple(map(int, state)) for state in data["selected_family"]]
    assert all(tuple(sorted(state)) == state and len(state) == 3 for state in raw_family)
    assert len(raw_family) == len(set(raw_family)) == 12
    payload = "\n".join(",".join(map(str, state)) for state in sorted(raw_family))
    assert sha256(payload.encode("ascii")).hexdigest() == data[
        "selected_family_sha256"
    ]
    family = {mask_of(state) for state in raw_family}
    assert all(dominates(g_adj, state) for state in family)

    obligations = 0
    legal_responses = 0
    for state in family:
        for attacked in range(n):
            if state & (1 << attacked):
                continue
            obligations += 1
            responses = [
                successor(state, mover, attacked)
                for mover in bits(state)
                if adjacent(g_adj, mover, attacked)
                and successor(state, mover, attacked) in family
            ]
            assert responses
            legal_responses += len(responses)
    assert obligations == 36

    parameters = exact_parameters(g_adj)
    kernel_sizes = [len(kernel) for kernel, _rounds in parameters["kernels"]]
    kernel_rounds = [rounds for _kernel, rounds in parameters["kernels"]]
    assert parameters["gamma"] == 2
    assert parameters["i"] == 2
    assert parameters["alpha"] == 3
    assert parameters["gamma_infinity"] == 3
    assert parameters["theta"] == 3
    assert kernel_sizes[:3] == [0, 0, 18]
    assert family <= parameters["kernels"][2][0]

    anchor = mask_of((0, 1, 2))
    assert anchor in family and independent(g_adj, anchor)
    lists = {}
    for outside in (3, 4, 5):
        lists[outside] = [
            omitted
            for omitted in range(3)
            if (anchor ^ (1 << omitted)) | (1 << outside) in family
        ]
    assert lists == {3: [1, 2], 4: [0, 2], 5: [0, 1]}

    omitted = {3: 0, 4: 1, 5: 2}
    dynamic = [
        outside
        for outside in omitted
        if adjacent(g_adj, omitted[outside], outside)
    ]
    physical = [
        outside
        for outside in omitted
        if adjacent(h_adj, omitted[outside], outside)
    ]
    assert dynamic == [3]
    assert physical == [4, 5]

    return {
        "graph6": "EFnG",
        "order": n,
        "size": size,
        "parameters": {
            key: parameters[key]
            for key in ("gamma", "i", "alpha", "gamma_infinity", "theta")
        },
        "selected_family_size": len(family),
        "attack_obligations": obligations,
        "legal_retained_responses": legal_responses,
        "greatest_kernel_sizes_k1_to_k6": kernel_sizes,
        "greatest_kernel_rounds_k1_to_k6": kernel_rounds,
        "lists": {str(key): value for key, value in lists.items()},
        "dynamic_vertices": dynamic,
        "physical_vertices": physical,
    }


def main() -> None:
    manifest = json.loads((CANDIDATE / "MANIFEST.json").read_text())
    for name, expected in manifest["files_sha256"].items():
        assert digest(CANDIDATE / name) == expected
    note_hash = digest(CANDIDATE / "NOTE.md")
    assert note_hash == "f3309daa2497a10c978fac28286959d6ec2fb52e8438c727cdf2eafce89aa1a7"
    data = json.loads((CANDIDATE / "control.json").read_text())
    result = {
        "verdict": "PASS",
        "candidate_note_sha256": note_hash,
        "manifest_sha256": digest(CANDIDATE / "MANIFEST.json"),
        "control": check_control(data),
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
