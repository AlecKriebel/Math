#!/usr/bin/env python3
"""Clean-room checks for the all-k Y_k dynamic candidate.

This verifier has two independent tasks.

1. It exhausts the finite restoration/closure skeleton used in the
   carried-rigidity proof.  All 64 choices for the unspecified
   base-to-path graph edges and all eight nonexact nonempty family-list
   subpatterns are tested.  The installed base state is deleted from the
   greatest restoration-compatible local kernel in every case.
2. It decodes and checks the seven-vertex static-repair control without
   importing the candidate verifier.  Domination, independent domination,
   independence, the eternal kernel, and clique partition are all
   recomputed by exhaustive bit-mask routines.  Clique partition is
   checked directly, rather than by complement coloring.
"""

from hashlib import sha256
from itertools import combinations
from pathlib import Path


HERE = Path(__file__).resolve().parent
CANDIDATE = HERE.parents[1] / "math" / "working" / "all_k_yk_dynamic"
EXPECTED_CANDIDATE_MANIFEST = (
    "ae7ec69d98efa2386704912782b3c61083ec2d29c493eb1b38327e696a812e98"
)
EXPECTED_FILES = {
    "NOTE.md": "98a56786a8db1f78c4f6328871b1926795928997389f441e4637e6e3d801d6e0",
    "RESEARCH_LOG.md": (
        "6590c081b3be6cc8c27ac5ece93ece672bb589d542e588fb8cbac87ef06e61a3"
    ),
    "verify.py": "3808fdfad8b968e02866f488af6d336019785dc9cdefc7c07312c46e3b448af2",
    "verify.stdout": (
        "1df3c8614206de98dfa67904b684de35567222e17840e597bcd8b256b852f785"
    ),
}


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def check_candidate_manifest():
    assert digest(CANDIDATE / "MANIFEST.sha256") == EXPECTED_CANDIDATE_MANIFEST
    for name, expected in EXPECTED_FILES.items():
        assert digest(CANDIDATE / name) == expected


def restoration_ok(state, lists):
    """Base-color part of restoration after the singleton clique is installed."""
    base = frozenset(range(3))
    missing = base - state
    supplied = set()
    for x in state - base:
        supplied.update(lists[x])
    return missing <= supplied


def local_kernel(graph_edges, lists):
    """Overapproximate installed states using only restoration and X-attacks."""
    vertices = frozenset(range(7))
    targets = frozenset(range(3, 7))
    states = {
        frozenset(state)
        for state in combinations(vertices, 3)
        if restoration_ok(frozenset(state), lists)
    }
    while True:
        doomed = set()
        for state in states:
            for target in targets - state:
                successors = {
                    (state - {guard}) | {target}
                    for guard in state
                    if tuple(sorted((guard, target))) in graph_edges
                }
                if not any(successor in states for successor in successors):
                    doomed.add(state)
                    break
        if not doomed:
            return states
        states -= doomed


def check_carried_rigidity_skeleton():
    """Test every graph-edge completion and every nonexact list subpattern."""
    a, b, c = 0, 1, 2
    x0, x1, x2, x3 = 3, 4, 5, 6
    caps = {
        x0: frozenset({a}),
        x1: frozenset({a, c}),
        x2: frozenset({b, c}),
        x3: frozenset({b}),
    }

    fixed_edges = {
        tuple(sorted(edge))
        for edge in (
            (x0, x2),
            (x0, x3),
            (x1, x3),
            *(
                (anchor, target)
                for target, cap in caps.items()
                for anchor in cap
            ),
        )
    }
    optional_edges = [
        (anchor, target)
        for target, cap in caps.items()
        for anchor in (a, b, c)
        if anchor not in cap
    ]
    assert len(optional_edges) == 6

    nonempty_subsets = {
        target: [
            frozenset(choice)
            for size in range(1, len(cap) + 1)
            for choice in combinations(sorted(cap), size)
        ]
        for target, cap in caps.items()
    }

    tested_nonexact = 0
    exact_survivors = 0
    base = frozenset({a, b, c})
    for edge_mask in range(1 << len(optional_edges)):
        edges = set(fixed_edges)
        edges.update(
            tuple(sorted(edge))
            for bit, edge in enumerate(optional_edges)
            if edge_mask & (1 << bit)
        )
        for l1 in nonempty_subsets[x1]:
            for l2 in nonempty_subsets[x2]:
                lists = {
                    x0: caps[x0],
                    x1: l1,
                    x2: l2,
                    x3: caps[x3],
                }
                kernel = local_kernel(edges, lists)
                if l1 == caps[x1] and l2 == caps[x2]:
                    exact_survivors += base in kernel
                else:
                    tested_nonexact += 1
                    assert base not in kernel

    assert tested_nonexact == 64 * 8
    assert exact_survivors > 0
    return tested_nonexact, exact_survivors


def decode_graph6(text):
    """Decode the small-order graph6 representation from first principles."""
    raw = [ord(ch) - 63 for ch in text.strip()]
    assert raw and 0 <= raw[0] <= 62
    n = raw[0]
    bits = [
        (value >> shift) & 1
        for value in raw[1:]
        for shift in range(5, -1, -1)
    ]
    adjacency = [0] * n
    position = 0
    for high in range(1, n):
        for low in range(high):
            if bits[position]:
                adjacency[low] |= 1 << high
                adjacency[high] |= 1 << low
            position += 1
    return adjacency


def masks_of_size(n, size):
    for vertices in combinations(range(n), size):
        mask = 0
        for vertex in vertices:
            mask |= 1 << vertex
        yield mask


def is_dominating(mask, adjacency, universe):
    covered = mask
    remaining = mask
    while remaining:
        bit = remaining & -remaining
        vertex = bit.bit_length() - 1
        covered |= adjacency[vertex]
        remaining ^= bit
    return covered & universe == universe


def is_independent(mask, adjacency):
    remaining = mask
    while remaining:
        bit = remaining & -remaining
        vertex = bit.bit_length() - 1
        if adjacency[vertex] & (remaining ^ bit):
            return False
        remaining ^= bit
    return True


def minimum_size(n, predicate):
    for size in range(n + 1):
        if any(predicate(mask) for mask in masks_of_size(n, size)):
            return size
    raise AssertionError("finite search exhausted")


def maximum_size(n, predicate):
    for size in range(n, -1, -1):
        if any(predicate(mask) for mask in masks_of_size(n, size)):
            return size
    raise AssertionError("finite search exhausted")


def clique_partition_number(adjacency, universe):
    """Direct set-partition dynamic program; no complement coloring."""
    clique = {0}
    submask = universe
    while submask:
        if is_clique(submask, adjacency):
            clique.add(submask)
        submask = (submask - 1) & universe

    memo = {0: 0}

    def solve(mask):
        if mask in memo:
            return memo[mask]
        first = mask & -mask
        best = mask.bit_count()
        subset = mask
        while subset:
            if subset & first and subset in clique:
                best = min(best, 1 + solve(mask ^ subset))
            subset = (subset - 1) & mask
        memo[mask] = best
        return best

    return solve(universe)


def is_clique(mask, adjacency):
    remaining = mask
    while remaining:
        bit = remaining & -remaining
        vertex = bit.bit_length() - 1
        others = remaining ^ bit
        if others & ~adjacency[vertex]:
            return False
        remaining = others
    return True


def induced(adjacency, keep):
    old_vertices = [v for v in range(len(adjacency)) if keep & (1 << v)]
    position = {old: new for new, old in enumerate(old_vertices)}
    result = [0] * len(old_vertices)
    for old, new in position.items():
        for neighbor in old_vertices:
            if adjacency[old] & (1 << neighbor):
                result[new] |= 1 << position[neighbor]
    return result, old_vertices


def greatest_eternal_kernel(adjacency, k):
    """Queue deletion using predecessor support counts."""
    n = len(adjacency)
    universe = (1 << n) - 1
    alive = {
        mask
        for mask in masks_of_size(n, k)
        if is_dominating(mask, adjacency, universe)
    }
    obligations = {}
    reverse = {state: [] for state in alive}

    for state in alive:
        for attack in range(n):
            attack_bit = 1 << attack
            if state & attack_bit:
                continue
            successors = set()
            guards = state & adjacency[attack]
            while guards:
                guard_bit = guards & -guards
                successor = (state ^ guard_bit) | attack_bit
                if successor in alive:
                    successors.add(successor)
                    reverse[successor].append((state, attack))
                guards ^= guard_bit
            obligations[(state, attack)] = len(successors)

    queue = []
    queued = set()
    for (state, _attack), count in obligations.items():
        if count == 0 and state not in queued:
            queue.append(state)
            queued.add(state)

    while queue:
        removed = queue.pop()
        if removed not in alive:
            continue
        alive.remove(removed)
        for predecessor, attack in reverse[removed]:
            if predecessor not in alive:
                continue
            key = (predecessor, attack)
            obligations[key] -= 1
            if obligations[key] == 0 and predecessor not in queued:
                queue.append(predecessor)
                queued.add(predecessor)
    return alive


def eternal_number(adjacency):
    for k in range(len(adjacency) + 1):
        kernel = greatest_eternal_kernel(adjacency, k)
        if kernel:
            return k
    raise AssertionError("finite eternal search exhausted")


def static_list(reference, target, adjacency):
    result = set()
    universe = (1 << len(adjacency)) - 1
    target_bit = 1 << target
    guards = reference & adjacency[target]
    while guards:
        guard_bit = guards & -guards
        successor = (reference ^ guard_bit) | target_bit
        if is_dominating(successor, adjacency, universe):
            result.add(guard_bit.bit_length() - 1)
        guards ^= guard_bit
    return frozenset(result)


def family_list(reference, target, adjacency, family):
    result = set()
    target_bit = 1 << target
    guards = reference & adjacency[target]
    while guards:
        guard_bit = guards & -guards
        if (reference ^ guard_bit) | target_bit in family:
            result.add(guard_bit.bit_length() - 1)
        guards ^= guard_bit
    return frozenset(result)


def check_family(family, adjacency):
    n = len(adjacency)
    universe = (1 << n) - 1
    obligations = 0
    for state in family:
        assert is_dominating(state, adjacency, universe)
        for attack in range(n):
            attack_bit = 1 << attack
            if state & attack_bit:
                continue
            obligations += 1
            guards = state & adjacency[attack]
            assert any(
                ((state ^ (1 << guard)) | attack_bit) in family
                for guard in range(n)
                if guards & (1 << guard)
            )
    return obligations


def graph_parameters(adjacency):
    n = len(adjacency)
    universe = (1 << n) - 1
    gamma = minimum_size(
        n, lambda mask: is_dominating(mask, adjacency, universe)
    )
    independent_domination = minimum_size(
        n,
        lambda mask: is_independent(mask, adjacency)
        and is_dominating(mask, adjacency, universe),
    )
    alpha = maximum_size(n, lambda mask: is_independent(mask, adjacency))
    eternal = eternal_number(adjacency)
    theta = clique_partition_number(adjacency, universe)
    return gamma, independent_domination, alpha, eternal, theta


def check_static_repair_control():
    adjacency = decode_graph6("F?E`O")
    decoded_edges = {
        (u, v)
        for u in range(7)
        for v in range(u + 1, 7)
        if adjacency[u] & (1 << v)
    }
    expected_edges = {(0, 5), (2, 5), (2, 6), (3, 4), (4, 6)}
    assert decoded_edges == expected_edges

    assert graph_parameters(adjacency) == (3, 3, 4, 4, 4)
    family = greatest_eternal_kernel(adjacency, 4)
    expected_family = {
        sum(1 << v for v in state)
        for state in (
            (0, 1, 2, 3),
            (0, 1, 2, 4),
            (0, 1, 3, 6),
            (0, 1, 4, 6),
            (1, 2, 3, 5),
            (1, 2, 4, 5),
            (1, 3, 5, 6),
            (1, 4, 5, 6),
        )
    }
    assert family == expected_family
    assert check_family(family, adjacency) == 24

    s = sum(1 << v for v in (0, 1, 2, 3))
    t = sum(1 << v for v in (0, 1, 2, 4))
    assert is_independent(s, adjacency)
    assert is_independent(t, adjacency)
    assert static_list(s, 4, adjacency) == frozenset({3})
    assert family_list(s, 4, adjacency, family) == frozenset({3})
    assert static_list(s, 5, adjacency) == frozenset({0})
    assert family_list(s, 5, adjacency, family) == frozenset({0})
    assert static_list(t, 5, adjacency) == frozenset({0, 2})
    assert family_list(t, 5, adjacency, family) == frozenset({0})

    old_swap = (s ^ (1 << 2)) | (1 << 5)
    new_swap = (t ^ (1 << 2)) | (1 << 5)
    universe = (1 << 7) - 1
    assert not is_dominating(old_swap, adjacency, universe)
    assert is_dominating(new_swap, adjacency, universe)
    assert not old_swap & (1 << 6)
    assert adjacency[6] & old_swap == 0
    assert adjacency[6] & (1 << 4)

    keep = sum(1 << v for v in (0, 1, 2, 5))
    projected, old_vertices = induced(adjacency, keep)
    assert old_vertices == [0, 1, 2, 5]
    assert graph_parameters(projected) == (2, 2, 3, 3, 3)

    projected_family = {
        (1 << 0) | (1 << 1) | (1 << 2),
        (1 << 1) | (1 << 2) | (1 << 3),
    }
    assert projected_family <= greatest_eternal_kernel(projected, 3)
    assert check_family(projected_family, projected) == 2
    return len(family)


def main():
    check_candidate_manifest()
    tested_nonexact, exact_survivors = check_carried_rigidity_skeleton()
    family_size = check_static_repair_control()
    print("PASS: hostile all-k Y_k audit checks")
    print(
        "candidate_manifest_sha256="
        f"{EXPECTED_CANDIDATE_MANIFEST}"
    )
    print(
        f"rigidity_nonexact_cases={tested_nonexact} "
        f"exact_pattern_survivors={exact_survivors}"
    )
    print(f"control_kernel_states={family_size}")
    print("control_parameters=(gamma,i,alpha,gamma_infinity,theta)=(3,3,4,4,4)")
    print("projection_parameters=(gamma,i,alpha,gamma_infinity,theta)=(2,2,3,3,3)")


if __name__ == "__main__":
    main()
