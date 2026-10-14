#!/usr/bin/env python3
"""Independent standard-library reconstruction of the PR734 finite obstruction.

No author code, external algebra package, source PDF, or other audit is imported.
Functions on F2^2 are four-bit masks; permutations use zero-based point labels.
The check exhausts the subgroup lattice of the 32-element candidate group and
also verifies the Frattini calculation from group operations, not a classification.
"""
from __future__ import annotations

from collections import Counter, deque
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import platform
import sys


PointPerm = tuple[int, ...]
Elt = tuple[int, int]
IDENTITY: Elt = (0, 0)


def parity(mask: int) -> int:
    return mask.bit_count() % 2


def tau(mask: int, t: int) -> int:
    """The mask of the function v -> f(v+t); addition is XOR."""
    return sum(((mask >> (v ^ t)) & 1) << v for v in range(4))


def mul(a: Elt, b: Elt) -> Elt:
    f, t = a
    g, u = b
    return f ^ tau(g, t), t ^ u


def inv(a: Elt) -> Elt:
    f, t = a
    return tau(f, t), t


def comm(a: Elt, b: Elt) -> Elt:
    return mul(mul(mul(a, b), inv(a)), inv(b))


def perm(a: Elt) -> PointPerm:
    f, t = a
    return tuple(2 * ((i // 2) ^ t) + ((i % 2) ^ ((f >> ((i // 2) ^ t)) & 1))
                 for i in range(8))


def compose(a: PointPerm, b: PointPerm) -> PointPerm:
    return tuple(a[j] for j in b)


def generated(gens: tuple[Elt, ...] | list[Elt]) -> frozenset[Elt]:
    steps = tuple(set(gens) | {inv(a) for a in gens})
    found = {IDENTITY}
    queue = deque([IDENTITY])
    while queue:
        a = queue.popleft()
        for b in steps:
            c = mul(a, b)
            if c not in found:
                found.add(c)
                queue.append(c)
    return frozenset(found)


def subgroups(group: frozenset[Elt]) -> set[frozenset[Elt]]:
    start = frozenset([IDENTITY])
    found = {start}
    queue = deque([start])
    while queue:
        h = queue.popleft()
        for a in group - h:
            k = generated(list(h) + [a])
            assert k <= group
            if k not in found:
                found.add(k)
                queue.append(k)
    return found


def orbit(group: frozenset[Elt], point: int = 0) -> frozenset[int]:
    return frozenset(perm(a)[point] for a in group)


def cycles(p: PointPerm) -> tuple[frozenset[int], ...]:
    remaining = set(range(len(p)))
    out = []
    while remaining:
        start = min(remaining)
        cycle = {start}
        next_point = p[start]
        while next_point != start:
            assert next_point not in cycle
            cycle.add(next_point)
            next_point = p[next_point]
        remaining -= cycle
        out.append(frozenset(cycle))
    return tuple(out)


def is_block(c: frozenset[int], permutations: tuple[PointPerm, ...]) -> bool:
    assert c
    for p in permutations:
        image = frozenset(p[i] for i in c)
        if image & c and image != c:
            return False
    return True


def cycle_property(group: frozenset[Elt]) -> bool:
    permutations = tuple(perm(a) for a in group)
    return all(is_block(c, permutations) for p in permutations for c in cycles(p))


def wreath_perm(left: Elt, right: Elt, swap: int) -> PointPerm:
    # Apply swap first, then independent base actions in the destination copies.
    p0, p1 = perm(left), perm(right)
    output = []
    for i in range(16):
        src_copy, point = divmod(i, 8)
        dest_copy = src_copy ^ swap
        p = p0 if dest_copy == 0 else p1
        output.append(8 * dest_copy + p[point])
    return tuple(output)


def main() -> dict:
    full = frozenset((f, t) for f in range(16) for t in range(4))
    p = frozenset((f, t) for f, t in full if parity(f) == (t & 1))
    base = frozenset((f, 0) for f in range(16) if parity(f) == 0)
    assert len(full) == 64 and len(p) == 32 and len(base) == 8
    assert len({perm(a) for a in full}) == 64  # faithfulness
    for a in full:
        assert mul(a, inv(a)) == IDENTITY == mul(inv(a), a)
        for b in full:
            assert compose(perm(a), perm(b)) == perm(mul(a, b))
            character_a = parity(a[0]) ^ (a[1] & 1)
            character_b = parity(b[0]) ^ (b[1] & 1)
            c = mul(a, b)
            assert (parity(c[0]) ^ (c[1] & 1)) == character_a ^ character_b
    assert orbit(p) == frozenset(range(8))
    assert generated([(1, 1), (0, 2)]) == p

    # Exhaustive lattice independently checks the universal transitive-subgroup claim.
    lattice = subgroups(p)
    transitive = [h for h in lattice if len(orbit(h)) == 8]
    assert transitive == [p]
    assert all({t for f, t in h} != set(range(4)) for h in lattice if h != p)
    proper = lattice - {p}
    maximal = [h for h in proper if not any(h < k < p for k in lattice)]
    frattini = frozenset.intersection(*maximal)
    assert frattini == base and len(maximal) == 3
    squares_commutators = [mul(a, a) for a in p]
    squares_commutators += [comm(a, b) for a in p for b in p]
    assert generated(squares_commutators) == base
    derived = generated([comm(a, b) for a in p for b in p])
    assert len(derived) == 4

    # Universal lift test, independent of a preferred generating pair.
    lifts1 = [a for a in p if a[1] == 1]
    lifts2 = [a for a in p if a[1] == 2]
    lift_receipts = []
    for q1 in lifts1:
        for q2 in lifts2:
            a2 = mul(q1, q1)
            c = comm(q1, q2)
            nested = comm(a2, q2)
            assert nested == (15, 0)
            assert a2[1] == c[1] == 0
            assert generated([a2, c, nested]) == base
            assert generated([q1, q2]) == p
            lift_receipts.append({'q1': q1, 'q2': q2, 'q1_square': a2,
                                  'commutator': c, 'nested_commutator': nested})
    assert len(lift_receipts) == 64

    # A complete cycle of b and an intersecting, unequal translate under z.
    b, z = (0, 2), (6, 0)
    crossing = frozenset([0, 4])  # one-based {1,5}
    image = frozenset(perm(z)[i] for i in crossing)
    assert b in p and z in p
    assert crossing in cycles(perm(b))
    assert image == frozenset([0, 5])  # one-based {1,6}
    assert image & crossing == frozenset([0]) and image != crossing
    assert not is_block(crossing, tuple(perm(a) for a in p))
    assert not cycle_property(p)
    # Identity is deliberately not a witness.
    assert frozenset(perm(IDENTITY)[i] for i in crossing) == crossing

    # Positive controls: the untwisted ambient group and even-parity kernel both
    # contain a regular elementary-abelian subgroup with the cycle property.
    regular = frozenset((f, t) for f in (0, 15) for t in range(4))
    untwisted = frozenset((f, t) for f, t in full if parity(f) == 0)
    assert generated(list(regular)) == regular and len(regular) == 8
    assert regular <= full and regular <= untwisted
    assert len(orbit(regular)) == 8 and cycle_property(regular)
    assert not regular <= p
    assert cycle_property(frozenset([IDENTITY]))

    # Exhaustive first-wreath action: B is a block and its stabilizer image is P.
    wreath = tuple(wreath_perm(a, b, s) for a in p for b in p for s in (0, 1))
    assert len(wreath) == len(set(wreath)) == 2048
    b0 = frozenset(range(8))
    b1 = frozenset(range(8, 16))
    restrictions = set()
    for action in wreath:
        target = frozenset(action[i] for i in b0)
        assert target in (b0, b1)
        if target == b0:
            restrictions.add(tuple(action[i] for i in range(8)))
    assert restrictions == {perm(a) for a in p}
    assert frozenset(action[0] for action in wreath) == frozenset(range(16))

    return {
        'timestamp_utc': datetime.now(timezone.utc).isoformat(),
        'python_version': platform.python_version(),
        'python_executable': sys.executable,
        'standard_library_only': True,
        'author_verifier_imported': False,
        'group_order': len(p),
        'ambient_order': len(full),
        'faithful': True,
        'transitive': True,
        'subgroup_count': len(lattice),
        'subgroup_order_counts': dict(sorted(Counter(len(h) for h in lattice).items())),
        'transitive_subgroup_count': len(transitive),
        'sole_transitive_subgroup_order': len(transitive[0]),
        'maximal_subgroup_count': len(maximal),
        'maximal_subgroup_orders': sorted(len(h) for h in maximal),
        'maximal_subgroup_orbit_sizes': sorted(len(orbit(h)) for h in maximal),
        'frattini_equals_parity_kernel': True,
        'frattini_order': len(frattini),
        'derived_order': len(derived),
        'full_fibre_projection_forces_whole_group': True,
        'arbitrary_lift_pair_count': len(lift_receipts),
        'all_lift_pairs_generate_group': True,
        'lift_receipts': lift_receipts,
        'crossing_cycle_one_based': [1, 5],
        'crossing_image_one_based': [1, 6],
        'cycle_support_property': False,
        'regular_positive_control_order': len(regular),
        'regular_positive_control_cycle_property': True,
        'identity_negative_witness_control': True,
        'first_wreath_order': len(wreath),
        'first_wreath_transitive': True,
        'first_wreath_bottom_block': True,
        'first_wreath_bottom_stabilizer_image_order': len(restrictions),
        'all_assertions_passed': True,
    }


if __name__ == '__main__':
    result = main()
    here = Path(__file__).resolve().parent
    result['verifier_sha256'] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    (here / 'finite_receipts.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({k: v for k, v in result.items() if k != 'lift_receipts'}, indent=2))
