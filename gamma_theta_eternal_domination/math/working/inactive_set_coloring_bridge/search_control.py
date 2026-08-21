#!/usr/bin/env python3
"""Deterministic bounded search for an active-set coloring countercontrol.

The generated complement graphs H are explicitly tripartite.  Thus
G = complement(H) has theta(G) <= 3.  We retain only graphs for which every
pair in H has a common neighbor, which proves gamma(G) = alpha(G) = 3; the
fixed clique partition then also proves gamma_infinity(G) = 3.

For each full response incidence (S,x) in the literal greatest eternal
triple-family, the script forms the physical active set A_x, puts
R = V(G-x) - A_x, enumerates every proper 3-coloring of H-x, and asks whether
some coloring uses at most two colors on R.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import random
from pathlib import Path


HERE = Path(__file__).resolve().parent


def vertices(mask: int):
    while mask:
        bit = mask & -mask
        yield bit.bit_length() - 1
        mask ^= bit


def masks_of_size(n: int, k: int):
    for group in itertools.combinations(range(n), k):
        yield sum(1 << v for v in group)


def complement_graph(h: tuple[int, ...]) -> tuple[int, ...]:
    all_vertices = (1 << len(h)) - 1
    return tuple(all_vertices ^ (1 << v) ^ h[v] for v in range(len(h)))


def closed_masks(g: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(row | (1 << v) for v, row in enumerate(g))


def dominates(closed: tuple[int, ...], state: int) -> bool:
    covered = 0
    for v in vertices(state):
        covered |= closed[v]
    return covered == (1 << len(closed)) - 1


def triangles(h: tuple[int, ...], allowed: int | None = None) -> tuple[int, ...]:
    if allowed is None:
        allowed = (1 << len(h)) - 1
    answer = []
    for a, b, c in itertools.combinations(vertices(allowed), 3):
        if (
            (h[a] & (1 << b))
            and (h[a] & (1 << c))
            and (h[b] & (1 << c))
        ):
            answer.append((1 << a) | (1 << b) | (1 << c))
    return tuple(answer)


def every_pair_has_common_neighbor(
    h: tuple[int, ...], allowed: int | None = None
) -> bool:
    if allowed is None:
        allowed = (1 << len(h)) - 1
    verts = tuple(vertices(allowed))
    return all(h[u] & h[v] & allowed for u, v in itertools.combinations(verts, 2))


def greatest_family(g: tuple[int, ...], k: int = 3) -> frozenset[int]:
    n = len(g)
    all_vertices = (1 << n) - 1
    closed = closed_masks(g)
    family = frozenset(
        state for state in masks_of_size(n, k) if dominates(closed, state)
    )
    while True:
        retained = set()
        for state in family:
            if all(
                any(
                    ((state ^ (1 << guard)) | (1 << attack)) in family
                    for guard in vertices(state & g[attack])
                )
                for attack in vertices(all_vertices ^ state)
            ):
                retained.add(state)
        next_family = frozenset(retained)
        if next_family == family:
            return family
        family = next_family


def response_list(
    g: tuple[int, ...], family: frozenset[int], state: int, target: int
) -> tuple[int, ...]:
    return tuple(
        guard
        for guard in vertices(state & g[target])
        if ((state ^ (1 << guard)) | (1 << target)) in family
    )


def colorings_three(h: tuple[int, ...], omitted: int) -> tuple[tuple[int, ...], ...]:
    """Enumerate proper 3-colorings of H-omitted, modulo no color symmetry."""

    n = len(h)
    active = tuple(v for v in range(n) if v != omitted)
    colors = [-1] * n
    answer: list[tuple[int, ...]] = []

    def choose_vertex() -> int | None:
        candidates = [v for v in active if colors[v] < 0]
        if not candidates:
            return None
        return max(
            candidates,
            key=lambda v: (
                len({colors[u] for u in vertices(h[v]) if colors[u] >= 0}),
                (h[v] & sum(1 << u for u in candidates)).bit_count(),
            ),
        )

    def visit() -> None:
        v = choose_vertex()
        if v is None:
            answer.append(tuple(colors))
            return
        forbidden = {colors[u] for u in vertices(h[v]) if colors[u] >= 0}
        for color in range(3):
            if color not in forbidden:
                colors[v] = color
                visit()
                colors[v] = -1

    visit()
    return tuple(answer)


def graph6_short(g: tuple[int, ...]) -> str:
    n = len(g)
    bits = []
    for high in range(1, n):
        for low in range(high):
            bits.append(1 if g[low] & (1 << high) else 0)
    while len(bits) % 6:
        bits.append(0)
    payload = []
    for start in range(0, len(bits), 6):
        value = 0
        for bit in bits[start : start + 6]:
            value = (value << 1) | bit
        payload.append(chr(value + 63))
    return chr(n + 63) + "".join(payload)


def generate_h(
    rng: random.Random, class_sizes: tuple[int, int, int], probability: float
) -> tuple[tuple[int, ...], tuple[int, ...]]:
    classes = []
    cursor = 0
    for size in class_sizes:
        classes.append(tuple(range(cursor, cursor + size)))
        cursor += size
    h = [0] * cursor
    for left, right in itertools.combinations(classes, 2):
        for u in left:
            for v in right:
                if rng.random() < probability:
                    h[u] |= 1 << v
                    h[v] |= 1 << u
    coloring = tuple(
        color for color, part in enumerate(classes) for _vertex in part
    )
    return tuple(h), coloring


def analyze(
    h: tuple[int, ...], planted_coloring: tuple[int, ...]
) -> dict[str, object] | None:
    n = len(h)
    all_vertices = (1 << n) - 1
    if not every_pair_has_common_neighbor(h) or not triangles(h):
        return None
    g = complement_graph(h)
    family = greatest_family(g)
    if not family:
        raise AssertionError("planted clique partition must be an eternal family")
    facets = triangles(h)
    for x in range(n):
        allowed = all_vertices ^ (1 << x)
        if not every_pair_has_common_neighbor(h, allowed) or not triangles(h, allowed):
            continue
        deletion_facets = tuple(t for t in facets if not (t & (1 << x)))
        colorings = colorings_three(h, x)
        for state in deletion_facets:
            if set(response_list(g, family, state, x)) != set(vertices(state)):
                continue
            activity: dict[int, bool] = {}
            for v in vertices(allowed):
                containing = [t for t in deletion_facets if t & (1 << v)]
                statuses = [
                    v in response_list(g, family, t, x) for t in containing
                ]
                if not statuses or len(set(statuses)) != 1:
                    raise AssertionError(
                        f"vertex-star propagation failure at x={x}, v={v}"
                    )
                activity[v] = statuses[0]
            active_mask = sum(1 << v for v, status in activity.items() if status)
            r_mask = allowed ^ active_mask
            min_colors = min(
                len({coloring[v] for v in vertices(r_mask)})
                for coloring in colorings
            )
            if min_colors == 3:
                return {
                    "order": n,
                    "g_graph6_labeled": graph6_short(g),
                    "h_edges": [
                        [u, v]
                        for u in range(n)
                        for v in range(u + 1, n)
                        if h[u] & (1 << v)
                    ],
                    "planted_coloring": list(planted_coloring),
                    "greatest_family_states": len(family),
                    "target": x,
                    "full_state": list(vertices(state)),
                    "active_set": list(vertices(active_mask)),
                    "inactive_set_R": list(vertices(r_mask)),
                    "deletion_colorings": len(colorings),
                    "minimum_colors_on_R": min_colors,
                    "R_edges_in_H_prime": [
                        [u, v]
                        for u, v in itertools.combinations(vertices(r_mask), 2)
                        if h[u] & (1 << v)
                    ],
                }
    return None


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--trials", type=int, default=200_000)
    parser.add_argument("--seed", type=int, default=20260728)
    parser.add_argument("--sizes", default="4,4,4")
    parser.add_argument("--probability", type=float, default=0.72)
    parser.add_argument(
        "--output", type=Path, default=HERE / "random_search_result.json"
    )
    args = parser.parse_args()
    sizes = tuple(int(piece) for piece in args.sizes.split(","))
    if len(sizes) != 3:
        raise SystemExit("--sizes must contain three comma-separated integers")
    rng = random.Random(args.seed)
    result = None
    retained = 0
    for trial in range(1, args.trials + 1):
        h, planted = generate_h(rng, sizes, args.probability)
        if every_pair_has_common_neighbor(h):
            retained += 1
        result = analyze(h, planted)
        if result is not None:
            result["trial"] = trial
            break
    payload = {
        "schema": "inactive-set-coloring-control-v1",
        "seed": args.seed,
        "trials_requested": args.trials,
        "trials_completed": trial,
        "class_sizes": list(sizes),
        "edge_probability": args.probability,
        "pair_common_neighbor_graphs": retained,
        "result": result,
    }
    encoded = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    args.output.write_text(encoded, encoding="utf-8")
    print(encoded, end="")
    print("sha256", hashlib.sha256(encoded.encode()).hexdigest())


if __name__ == "__main__":
    main()
