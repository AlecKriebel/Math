"""Definition-level audit of the C7 argument in k3_antihole_elimination.md.

This probe imports no campaign graph or eternal-domination implementation.
"""

from __future__ import annotations

from itertools import combinations


N = 7
VERTICES = frozenset(range(N))
ADJ = {
    vertex: frozenset(((vertex - 1) % N, (vertex + 1) % N))
    for vertex in VERTICES
}


def dominates(configuration: frozenset[int]) -> bool:
    covered = set(configuration)
    for guard in configuration:
        covered.update(ADJ[guard])
    return covered == set(VERTICES)


def independent(configuration: frozenset[int]) -> bool:
    return all(
        second not in ADJ[first]
        for first, second in combinations(configuration, 2)
    )


def dominating_configurations(k: int) -> set[frozenset[int]]:
    return {
        frozenset(configuration)
        for configuration in combinations(VERTICES, k)
        if dominates(frozenset(configuration))
    }


def greatest_closed_family(k: int) -> set[frozenset[int]]:
    alive = dominating_configurations(k)
    changed = True
    while changed:
        changed = False
        remove: set[frozenset[int]] = set()
        for source in alive:
            for attack in VERTICES - source:
                if not any(
                    frozenset((source - {guard}) | {attack}) in alive
                    for guard in source
                    if attack in ADJ[guard]
                ):
                    remove.add(source)
                    break
        if remove:
            alive -= remove
            changed = True
    return alive


def gap_multiset(configuration: frozenset[int]) -> tuple[int, ...]:
    guards = sorted(configuration)
    gaps = []
    for index, guard in enumerate(guards):
        successor = guards[(index + 1) % len(guards)]
        gaps.append((successor - guard - 1) % N)
    return tuple(sorted(gaps))


def dihedral_images(configuration: frozenset[int]) -> set[frozenset[int]]:
    return {
        frozenset((sign * vertex + shift) % N for vertex in configuration)
        for sign in (-1, 1)
        for shift in range(N)
    }


def main() -> None:
    triples = dominating_configurations(3)
    type_counts: dict[tuple[int, ...], int] = {}
    for configuration in triples:
        gap_type = gap_multiset(configuration)
        type_counts[gap_type] = type_counts.get(gap_type, 0) + 1
    assert set(type_counts) == {(1, 1, 2), (0, 2, 2)}
    type_b = {
        configuration
        for configuration in triples
        if gap_multiset(configuration) == (0, 2, 2)
    }
    assert type_b <= dihedral_images(frozenset((0, 1, 4)))

    source_b = frozenset((0, 1, 4))
    attack_b = 3
    legal_b = [
        frozenset((source_b - {guard}) | {attack_b})
        for guard in source_b
        if attack_b in ADJ[guard]
    ]
    assert legal_b == [frozenset((0, 1, 3))]
    assert not dominates(legal_b[0])
    assert 5 not in (
        set(legal_b[0])
        | set().union(*(ADJ[guard] for guard in legal_b[0]))
    )

    maximum_independent = frozenset((0, 2, 4))
    assert independent(maximum_independent)
    assert not any(
        independent(frozenset(configuration))
        for configuration in combinations(VERTICES, 4)
    )
    successors = {
        guard: frozenset(
            (maximum_independent - {guard}) | {1}
        )
        for guard in maximum_independent
        if 1 in ADJ[guard]
    }
    assert successors == {
        0: frozenset((1, 2, 4)),
        2: frozenset((0, 1, 4)),
    }
    assert not dominates(successors[0])
    assert gap_multiset(successors[2]) == (0, 2, 2)

    assert greatest_closed_family(3) == set()
    family4 = greatest_closed_family(4)
    assert family4
    assert all(dominates(configuration) for configuration in family4)

    clique_partition = (
        frozenset((0, 1)),
        frozenset((2, 3)),
        frozenset((4, 5)),
        frozenset((6,)),
    )
    assert set().union(*clique_partition) == set(VERTICES)
    assert all(
        all(second in ADJ[first] for first, second in combinations(part, 2))
        for part in clique_partition
    )

    print(
        {
            "dominating_triples": len(triples),
            "gap_type_counts": type_counts,
            "eternal_3_family_size": 0,
            "greatest_eternal_4_family_size": len(family4),
        }
    )


if __name__ == "__main__":
    main()
