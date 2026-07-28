#!/usr/bin/env python3
"""Verify the palette-slice gluing countermodel from NOTE.md.

This is deliberately an ordinary finite checker.  It does not import the
campaign's eternal-domination code and it does not claim that the abstract
list instances are realized by equality graphs.
"""

from __future__ import annotations

from itertools import combinations


def instance(k: int):
    if k < 3:
        raise ValueError("k must be at least 3")

    colors = frozenset(range(k))
    extras = frozenset(range(3, k))
    path = tuple(f"x{i}" for i in range(4))
    forced = tuple(f"z{i}" for i in range(3, k))
    vertices = path + forced

    edges = {
        frozenset((path[i], path[i + 1]))
        for i in range(3)
    }
    edges.update(
        frozenset(pair)
        for pair in combinations(forced, 2)
    )
    edges.update(
        frozenset((z, x))
        for z in forced
        for x in path
    )

    lists = {
        path[0]: extras | {0},
        path[1]: extras | {0, 2},
        path[2]: extras | {1, 2},
        path[3]: extras | {1},
    }
    lists.update({f"z{i}": frozenset({i}) for i in range(3, k)})
    return colors, vertices, edges, lists


def adjacent(edges, x, y):
    return x != y and frozenset((x, y)) in edges


def list_colorable(vertices, edges, lists):
    vertices = tuple(vertices)
    remaining = set(vertices)
    assignment = {}

    def search():
        if not remaining:
            return dict(assignment)

        def available(v):
            blocked = {
                assignment[w]
                for w in assignment
                if adjacent(edges, v, w)
            }
            return lists[v] - blocked

        v = min(remaining, key=lambda w: (len(available(w)), w))
        choices = sorted(available(v))
        if not choices:
            return None
        remaining.remove(v)
        for color in choices:
            assignment[v] = color
            answer = search()
            if answer is not None:
                return answer
            del assignment[v]
        remaining.add(v)
        return None

    return search()


def is_clique(subset, edges):
    return all(adjacent(edges, x, y) for x, y in combinations(subset, 2))


def verify(k: int):
    colors, vertices, edges, lists = instance(k)
    assert all(lists[v] for v in vertices)
    assert all(lists[v] != colors for v in vertices)
    assert list_colorable(vertices, edges, lists) is None

    # Every proper-palette slice is list-colorable.
    slice_count = 0
    for mask in range((1 << k) - 1):
        palette = frozenset(i for i in range(k) if (mask >> i) & 1)
        induced = tuple(v for v in vertices if lists[v] <= palette)
        assert list_colorable(induced, edges, lists) is not None
        slice_count += 1

    # In particular, every one-color omission slice is colorable.
    for color in colors:
        induced = tuple(v for v in vertices if color not in lists[v])
        assert list_colorable(induced, edges, lists) is not None

    # The clique-wise Hall condition from eternal response lists holds.
    clique_count = 0
    for size in range(1, len(vertices) + 1):
        for subset in combinations(vertices, size):
            if not is_clique(subset, edges):
                continue
            clique_count += 1
            union = frozenset().union(*(lists[v] for v in subset))
            assert len(union) >= len(subset)

    # The standard vertex-minimal-core degree and deletion conditions hold.
    for v in vertices:
        degree = sum(adjacent(edges, v, w) for w in vertices)
        assert degree >= len(lists[v])
        induced = tuple(w for w in vertices if w != v)
        assert list_colorable(induced, edges, lists) is not None

    # C-059 collision transfer holds as a list-level necessary condition.
    for edge in edges:
        x, y = tuple(edge)
        for color in lists[x] & lists[y]:
            assert (lists[x] | lists[y]) - {color}

    # Basic graph diagnostics.
    assert len(vertices) == k + 1
    max_clique = max(
        len(subset)
        for size in range(1, len(vertices) + 1)
        for subset in combinations(vertices, size)
        if is_clique(subset, edges)
    )
    assert max_clique == k - 1

    return {
        "k": k,
        "vertices": len(vertices),
        "edges": len(edges),
        "proper_palette_slices": slice_count,
        "cliques_checked": clique_count,
        "maximum_clique": max_clique,
        "global_list_colorable": False,
        "all_lists_proper": True,
    }


def main():
    results = [verify(k) for k in range(3, 11)]
    print("PASS: abstract palette-slice gluing countermodels")
    for row in results:
        print(
            "k={k} n={vertices} m={edges} slices={proper_palette_slices} "
            "cliques={cliques_checked} omega={maximum_clique}".format(**row)
        )


if __name__ == "__main__":
    main()
