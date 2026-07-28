#!/usr/bin/env python3
"""Clean-room checks for the parameter-lifting audit.

This checker deliberately imports no campaign search or verifier code.  It:

* exhausts every labelled graph through order five;
* enumerates every optimal eternal family in each equality graph;
* checks both versions of every multi-anchor frozen projection;
* checks the static proper-palette colorings and the global static-list
  equivalence on those controls;
* checks every jointly inactive target/face suspension; and
* independently reconstructs the abstract K_(k-3) join P4 list obstruction.

The bounded graph tests are controls, not a proof of the uniform theorems.
"""

from __future__ import annotations

from itertools import combinations


def bits(mask: int):
    while mask:
        bit = mask & -mask
        yield bit.bit_length() - 1
        mask ^= bit


def subsets_of_size(universe: int, size: int):
    vertices = tuple(bits(universe))
    for choice in combinations(vertices, size):
        mask = 0
        for vertex in choice:
            mask |= 1 << vertex
        yield mask


def proper_nonempty_subsets(mask: int):
    subset = (mask - 1) & mask
    while subset:
        yield subset
        subset = (subset - 1) & mask


def graph_from_edge_code(n: int, code: int):
    adjacency = [0] * n
    position = 0
    for left in range(n):
        for right in range(left + 1, n):
            if (code >> position) & 1:
                adjacency[left] |= 1 << right
                adjacency[right] |= 1 << left
            position += 1
    return tuple(adjacency)


def dominates(adjacency, guards: int, universe: int):
    covered = guards
    for guard in bits(guards):
        covered |= adjacency[guard]
    return (covered & universe) == universe


def independent(adjacency, vertex_set: int):
    return all((adjacency[v] & vertex_set) == 0 for v in bits(vertex_set))


def clique(adjacency, vertex_set: int):
    return all(
        ((vertex_set ^ (1 << v)) & ~adjacency[v]) == 0
        for v in bits(vertex_set)
    )


def domination_number(adjacency, universe: int):
    for size in range(universe.bit_count() + 1):
        if any(
            dominates(adjacency, candidate, universe)
            for candidate in subsets_of_size(universe, size)
        ):
            return size
    raise AssertionError("finite graph has no dominating set")


def independence_number(adjacency, universe: int):
    for size in range(universe.bit_count(), -1, -1):
        if any(
            independent(adjacency, candidate)
            for candidate in subsets_of_size(universe, size)
        ):
            return size
    raise AssertionError("empty maximum search")


def clique_cover_number(adjacency, universe: int):
    if universe == 0:
        return 0
    clique_masks = {
        mask
        for size in range(1, universe.bit_count() + 1)
        for mask in subsets_of_size(universe, size)
        if clique(adjacency, mask)
    }
    memo = {0: 0}

    def solve(mask: int):
        if mask in memo:
            return memo[mask]
        first = mask & -mask
        best = mask.bit_count()
        submask = mask
        while submask:
            if (submask & first) and submask in clique_masks:
                best = min(best, 1 + solve(mask ^ submask))
            submask = (submask - 1) & mask
        memo[mask] = best
        return best

    return solve(universe)


def family_is_eternal(adjacency, universe: int, family):
    family = frozenset(family)
    if not family:
        return False
    if not all(dominates(adjacency, state, universe) for state in family):
        return False
    for state in family:
        for target in bits(universe ^ state):
            if not any(
                (adjacency[guard] >> target) & 1
                and ((state ^ (1 << guard)) | (1 << target)) in family
                for guard in bits(state)
            ):
                return False
    return True


def greatest_kernel(adjacency, universe: int, guard_count: int):
    current = {
        state
        for state in subsets_of_size(universe, guard_count)
        if dominates(adjacency, state, universe)
    }
    while True:
        kept = set()
        for state in current:
            valid = True
            for target in bits(universe ^ state):
                if not any(
                    (adjacency[guard] >> target) & 1
                    and ((state ^ (1 << guard)) | (1 << target)) in current
                    for guard in bits(state)
                ):
                    valid = False
                    break
            if valid:
                kept.add(state)
        if kept == current:
            return frozenset(current)
        current = kept


def eternal_domination_number(adjacency, universe: int):
    start = domination_number(adjacency, universe)
    for size in range(start, universe.bit_count() + 1):
        kernel = greatest_kernel(adjacency, universe, size)
        if kernel:
            return size, kernel
    raise AssertionError("placing a guard everywhere must be eternal")


def enumerate_eternal_subfamilies(adjacency, universe: int, kernel):
    states = tuple(sorted(kernel))
    for selector in range(1, 1 << len(states)):
        family = frozenset(
            states[index]
            for index in range(len(states))
            if (selector >> index) & 1
        )
        if family_is_eternal(adjacency, universe, family):
            yield family


def response_lists(adjacency, universe: int, state: int, family=None):
    answer = {}
    for target in bits(universe ^ state):
        allowed = 0
        for guard in bits(state):
            successor = (state ^ (1 << guard)) | (1 << target)
            if not ((adjacency[guard] >> target) & 1):
                continue
            if family is None:
                if dominates(adjacency, successor, universe):
                    allowed |= 1 << guard
            elif successor in family:
                allowed |= 1 << guard
        answer[target] = allowed
    return answer


def list_coloring(adjacency, vertices: int, allowed):
    """Color complement edges, using vertex labels as color labels."""
    assignment = {}
    remaining = set(bits(vertices))

    def available(vertex):
        choices = allowed[vertex]
        for other, color in assignment.items():
            if not ((adjacency[vertex] >> other) & 1):
                choices &= ~color
        return choices

    def search():
        if not remaining:
            return dict(assignment)
        vertex = min(remaining, key=lambda v: (available(v).bit_count(), v))
        choices = available(vertex)
        if not choices:
            return None
        remaining.remove(vertex)
        for color_vertex in bits(choices):
            assignment[vertex] = 1 << color_vertex
            result = search()
            if result is not None:
                return result
            del assignment[vertex]
        remaining.add(vertex)
        return None

    return search()


def common_complement_neighborhood(adjacency, universe: int, anchors: int):
    common = universe
    for anchor in bits(anchors):
        h_neighbors = universe & ~(adjacency[anchor] | (1 << anchor))
        common &= h_neighbors
    return common


def check_projected_family(adjacency, projected_vertices: int, projected):
    assert projected
    assert family_is_eternal(adjacency, projected_vertices, projected)


def check_all_small_graphs(max_n=5):
    totals = {
        "labelled_graphs": 0,
        "equality_graphs": 0,
        "eternal_families": 0,
        "reference_states": 0,
        "restoration_checks": 0,
        "frozen_projections": 0,
        "static_palette_colorings": 0,
        "inactive_suspensions": 0,
        "global_list_checks": 0,
        "gl_controls": 0,
    }

    for n in range(1, max_n + 1):
        universe = (1 << n) - 1
        edge_slots = n * (n - 1) // 2
        for edge_code in range(1 << edge_slots):
            totals["labelled_graphs"] += 1
            adjacency = graph_from_edge_code(n, edge_code)
            gamma = domination_number(adjacency, universe)
            alpha = independence_number(adjacency, universe)
            eternal, kernel = eternal_domination_number(adjacency, universe)
            theta = clique_cover_number(adjacency, universe)

            # Independently recover the parameter chain in every bounded graph.
            assert gamma <= alpha <= eternal <= theta
            if gamma != eternal:
                continue
            totals["equality_graphs"] += 1
            k = gamma
            assert alpha == k
            # This is an independently exhaustive n <= 5 positive control.
            assert theta == k

            maximum_independent_states = tuple(
                state
                for state in subsets_of_size(universe, k)
                if independent(adjacency, state)
            )
            for family in enumerate_eternal_subfamilies(
                adjacency, universe, kernel
            ):
                totals["eternal_families"] += 1
                # The independent-state forcing fact must hold family-by-family.
                assert all(state in family for state in maximum_independent_states)

                for state in maximum_independent_states:
                    totals["reference_states"] += 1
                    family_lists = response_lists(
                        adjacency, universe, state, family
                    )
                    static_lists = response_lists(
                        adjacency, universe, state, None
                    )
                    assert all(family_lists[x] for x in family_lists)
                    assert all(
                        family_lists[x] & ~static_lists[x] == 0
                        for x in family_lists
                    )
                    for configuration in family:
                        missing = state & ~configuration
                        outside_positions = configuration & ~state
                        restored_by = 0
                        for vertex in bits(outside_positions):
                            restored_by |= family_lists[vertex]
                        assert missing & ~restored_by == 0
                        totals["restoration_checks"] += 1

                    outside = universe ^ state
                    global_coloring = list_coloring(
                        adjacency, outside, static_lists
                    )
                    assert (global_coloring is not None) == (theta == k)
                    totals["global_list_checks"] += 1

                    for anchors in proper_nonempty_subsets(state):
                        t = anchors.bit_count()
                        expected = k - t
                        for lists in (family_lists, static_lists):
                            allowed_outside = 0
                            for vertex in bits(outside):
                                if lists[vertex] & anchors == 0:
                                    allowed_outside |= 1 << vertex
                            projected_vertices = (
                                state ^ anchors
                            ) | allowed_outside
                            projected = frozenset(
                                configuration ^ anchors
                                for configuration in family
                                if configuration & anchors == anchors
                                and (configuration ^ anchors)
                                & ~projected_vertices
                                == 0
                            )
                            check_projected_family(
                                adjacency, projected_vertices, projected
                            )
                            assert state ^ anchors in projected
                            assert (
                                domination_number(adjacency, projected_vertices)
                                == expected
                            )
                            assert (
                                independence_number(adjacency, projected_vertices)
                                == expected
                            )
                            projected_eternal, _ = eternal_domination_number(
                                adjacency, projected_vertices
                            )
                            assert projected_eternal == expected
                            totals["frozen_projections"] += 1

                            # At these bounded orders P(expected) is verified,
                            # so the projection has an exact clique cover.
                            assert (
                                clique_cover_number(
                                    adjacency, projected_vertices
                                )
                                == expected
                            )

                        static_outside = 0
                        for vertex in bits(outside):
                            if static_lists[vertex] & anchors == 0:
                                static_outside |= 1 << vertex
                        coloring = list_coloring(
                            adjacency, static_outside, static_lists
                        )
                        assert coloring is not None
                        assert all(
                            color & static_lists[vertex]
                            for vertex, color in coloring.items()
                        )
                        totals["static_palette_colorings"] += 1
                    # The omission-slice premise of GL(k) has just been
                    # checked for every omitted color (and more), while the
                    # global conclusion was checked above.
                    totals["gl_controls"] += 1

                    # Every jointly inactive target/face suspension.
                    for target in bits(outside):
                        inactive = state & ~family_lists[target]
                        for anchors in proper_nonempty_subsets(state):
                            if anchors & ~inactive:
                                continue
                            joint_link = (
                                1 << target
                            ) | common_complement_neighborhood(
                                adjacency, universe, anchors
                            )
                            expected = k - anchors.bit_count()
                            omega_h = independence_number(
                                adjacency, joint_link
                            )
                            chi_h = clique_cover_number(
                                adjacency, joint_link
                            )
                            assert omega_h == expected
                            assert chi_h == expected
                            totals["inactive_suspensions"] += 1

    return totals


def abstract_instance(k: int):
    assert k >= 3
    n = k + 1
    path = tuple(range(4))
    forced = tuple(range(4, n))
    adjacency = [0] * n

    def add_edge(left, right):
        adjacency[left] |= 1 << right
        adjacency[right] |= 1 << left

    for index in range(3):
        add_edge(path[index], path[index + 1])
    for left, right in combinations(forced, 2):
        add_edge(left, right)
    for z in forced:
        for x in path:
            add_edge(z, x)

    extras = sum(1 << color for color in range(3, k))
    lists = {
        path[0]: extras | (1 << 0),
        path[1]: extras | (1 << 0) | (1 << 2),
        path[2]: extras | (1 << 1) | (1 << 2),
        path[3]: extras | (1 << 1),
    }
    for index, z in enumerate(forced, start=3):
        lists[z] = 1 << index
    return tuple(adjacency), lists


def abstract_list_coloring(adjacency, vertices: int, lists):
    assignment = {}
    remaining = set(bits(vertices))

    def available(vertex):
        choices = lists[vertex]
        for neighbor in bits(adjacency[vertex]):
            if neighbor in assignment:
                choices &= ~assignment[neighbor]
        return choices

    def search():
        if not remaining:
            return dict(assignment)
        vertex = min(remaining, key=lambda v: (available(v).bit_count(), v))
        choices = available(vertex)
        if not choices:
            return None
        remaining.remove(vertex)
        for color in bits(choices):
            assignment[vertex] = 1 << color
            result = search()
            if result is not None:
                return result
            del assignment[vertex]
        remaining.add(vertex)
        return None

    return search()


def connected(adjacency, universe: int):
    if universe == 0:
        return True
    reached = universe & -universe
    frontier = reached
    while frontier:
        next_frontier = 0
        for vertex in bits(frontier):
            next_frontier |= adjacency[vertex]
        next_frontier &= universe & ~reached
        reached |= next_frontier
        frontier = next_frontier
    return reached == universe


def check_abstract_countermodels(first=3, last=11):
    rows = []
    for k in range(first, last + 1):
        adjacency, lists = abstract_instance(k)
        n = len(adjacency)
        universe = (1 << n) - 1
        palette = (1 << k) - 1

        # Reconstruct K_(k-3) join P4 exactly.
        for left in range(n):
            for right in range(left + 1, n):
                expected = (
                    (left < 4 and right < 4 and right == left + 1)
                    or right >= 4
                )
                assert bool((adjacency[left] >> right) & 1) == expected

        assert connected(adjacency, universe)
        assert all(lists[v] and lists[v] != palette for v in range(n))
        assert abstract_list_coloring(adjacency, universe, lists) is None

        for removed in range(n):
            assert (
                abstract_list_coloring(
                    adjacency, universe ^ (1 << removed), lists
                )
                is not None
            )

        slices = 0
        for proper_palette in range(palette):
            induced = 0
            for vertex in range(n):
                if lists[vertex] & ~proper_palette == 0:
                    induced |= 1 << vertex
            assert (
                abstract_list_coloring(adjacency, induced, lists)
                is not None
            )
            slices += 1

        cliques = 0
        maximum_clique = 0
        for candidate in range(1, 1 << n):
            if not clique(adjacency, candidate):
                continue
            cliques += 1
            maximum_clique = max(maximum_clique, candidate.bit_count())
            union = 0
            for vertex in bits(candidate):
                union |= lists[vertex]
            assert union.bit_count() >= candidate.bit_count()
        assert maximum_clique == k - 1

        for vertex in range(n):
            assert adjacency[vertex].bit_count() >= lists[vertex].bit_count()

        for left in range(n):
            for right in bits(adjacency[left]):
                if right <= left:
                    continue
                common = lists[left] & lists[right]
                for color in bits(common):
                    assert (lists[left] | lists[right]) & ~(1 << color)

        rows.append(
            {
                "k": k,
                "n": n,
                "m": sum(mask.bit_count() for mask in adjacency) // 2,
                "slices": slices,
                "cliques": cliques,
                "omega": maximum_clique,
            }
        )
    return rows


def main():
    small = check_all_small_graphs()
    abstract = check_abstract_countermodels()
    print("PASS: independent parameter-lifting hostile controls")
    print(
        "small "
        + " ".join(f"{key}={small[key]}" for key in sorted(small))
    )
    for row in abstract:
        print(
            "abstract k={k} n={n} m={m} slices={slices} "
            "cliques={cliques} omega={omega}".format(**row)
        )


if __name__ == "__main__":
    main()
