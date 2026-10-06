#!/usr/bin/env python3
"""Exact finite controls for PROOF.md; these do not prove infinite tail triviality."""

import itertools
import json


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def multiply(x, y, n):
    mask = (1 << n) - 1
    a, b, c = x & mask, (x >> n) & mask, x >> (2 * n)
    d, e, f = y & mask, (y >> n) & mask, y >> (2 * n)
    cross = a & (e ^ (mask if e.bit_count() % 2 else 0))
    return (a ^ d) | ((b ^ e) << n) | ((c ^ f ^ cross) << (2 * n))


def multiply_coordinates(x, y, n):
    """A deliberately different, coordinate-loop implementation of formula (1)."""
    out = 0
    for i in range(n):
        ai, bi, ci = ((x >> (i + k * n)) & 1 for k in range(3))
        di, ei, fi = ((y >> (i + k * n)) & 1 for k in range(3))
        cross = sum((y >> (j + n)) & 1 for j in range(n) if j != i) % 2
        out |= (ai ^ di) << i
        out |= (bi ^ ei) << (i + n)
        out |= (ci ^ fi ^ (ai & cross)) << (i + 2 * n)
    return out


def inverse(x, n):
    mask = (1 << n) - 1
    a, b = x & mask, (x >> n) & mask
    cross = a & (b ^ (mask if b.bit_count() % 2 else 0))
    return x ^ (cross << (2 * n))


def support(x, n):
    mask = (1 << n) - 1
    return (x | (x >> n) | (x >> (2 * n))) & mask


def relabel(x, permutation, n):
    y = 0
    for i, j in enumerate(permutation):
        for k in range(3):
            y |= ((x >> (i + k * n)) & 1) << (j + k * n)
    return y


def generated(indices, n):
    generators = [1 << (i + k * n) for i in range(n)
                  if indices & (1 << i) for k in range(2)]
    seen, pending = {0}, [0]
    while pending:
        x = pending.pop()
        for g in generators:
            y = multiply(x, g, n)
            if y not in seen:
                seen.add(y)
                pending.append(y)
    return seen


def run():
    counts = {}
    n = 3
    size = 1 << (3 * n)
    table = [[multiply(x, y, n) for y in range(size)] for x in range(size)]
    count = 0
    for x in range(size):
        inv = inverse(x, n)
        require(table[0][x] == table[x][0] == x, "identity")
        require(table[x][inv] == table[inv][x] == 0, "two-sided inverse")
        count += 2
        for y in range(size):
            require(table[x][y] == multiply_coordinates(x, y, n), "coordinate agreement")
            require(support(table[x][y], n) & ~(support(x, n) | support(y, n)) == 0,
                    "support escaped union")
            count += 2
    counts["identity_inverse_coordinate_and_support_checks"] = count

    # Exhaust all triples in the 64-element two-site group.
    n2, size2 = 2, 64
    t2 = [[multiply(x, y, n2) for y in range(size2)] for x in range(size2)]
    count = 0
    for x, y, z in itertools.product(range(size2), repeat=3):
        require(t2[t2[x][y]][z] == t2[x][t2[y][z]], "associativity")
        count += 1
    counts["two_site_associativity_triples"] = count

    # For three sites, central coordinates cancel from the cocycle identity.
    # All 64 possible (a,b) coordinates in each position therefore suffice.
    count = 0
    for x, y, z in itertools.product(range(64), repeat=3):
        require(table[table[x][y]][z] == table[x][table[y][z]], "three-site cocycle")
        count += 1
    counts["three_site_cocycle_triples"] = count

    count = 0
    for perm in itertools.permutations(range(n)):
        rel = [relabel(x, perm, n) for x in range(size)]
        require(len(set(rel)) == size, "permutation not bijective")
        count += 1
        for x in range(size):
            for y in range(size):
                require(rel[table[x][y]] == table[rel[x]][rel[y]], "equivariance")
                count += 1
    counts["three_site_permutation_checks"] = count

    subgroups = {mask: generated(mask, n) for mask in range(1 << n)}
    count, sizes = 0, {}
    for mask, group in subgroups.items():
        expected = {x for x in range(size) if support(x, n) & ~mask == 0
                    and (mask.bit_count() >= 2 or (x >> (2 * n)) == 0)}
        require(group == expected, "local subgroup formula")
        sizes[str(mask)] = len(group)
        count += 1
        for x in group:
            require(inverse(x, n) in group, "subgroup inverse closure")
            count += 1
            for y in group:
                require(table[x][y] in group, "subgroup multiplication closure")
                count += 1
    counts["subgroup_formula_and_closure_checks"] = count

    count, disjoint_count, failures = 0, 0, []
    for imask, jmask in itertools.product(range(1 << n), repeat=2):
        common = subgroups[imask] & subgroups[jmask]
        target = subgroups[imask & jmask]
        require(target <= common, "monotonicity")
        count += 1
        if common != target:
            failures.append({"I_mask": imask, "J_mask": jmask,
                             "intersection_order": len(common), "target_order": len(target)})
        if imask & jmask == 0:
            require(common == {0}, "disjoint subgroup intersection")
            disjoint_count += 1
            for x in subgroups[imask]:
                for y in subgroups[jmask]:
                    require((table[x][y] == 0) == (x == y == 0), "trace factorization")
                    disjoint_count += 1
    require(len(failures) == 6, "unexpected number of meet failures")
    count += 1
    counts["index_pair_intersection_checks"] = count
    counts["disjoint_trace_basis_checks"] = disjoint_count

    p0, q0, q1, q2, z0 = 1, 1 << 3, 1 << 4, 1 << 5, 1 << 6
    def commutator(x, y):
        return table[table[table[x][y]][inverse(x, n)]][inverse(y, n)]
    require(commutator(p0, q0) == 0, "same-site commutation")
    require(commutator(p0, q1) == commutator(p0, q2) == z0, "central witness")
    require(z0 in subgroups[3] & subgroups[5] and z0 not in subgroups[1], "witness membership")
    word = 0
    for g in [p0, q1] * 4:
        word = table[word][g]
    require(word == 0, "nonfree alternating moment")
    counts["explicit_witness_checks"] = 4

    spectral_values = sorted(a + 2 * b for a, b in itertools.product((-1, 1), repeat=2))
    require(spectral_values == [-3, -1, 1, 3], "selfadjoint spectrum")
    for a, b in itertools.product((-1, 1), repeat=2):
        x = a + 2 * b
        sign = 1 if x > 0 else -1
        require(sign == b and x - 2 * sign == a, "functional calculus recovery")
    counts["selfadjoint_recovery_checks"] = 5

    return {"schema": 1, "problem_id": "30001176", "finite_sites": 3,
            "group_order": size, "local_subgroup_orders_by_bitmask": sizes,
            "meet_failures": failures, "witness": {"p0": p0, "q1": q1, "q2": q2, "z0": z0},
            "checks": counts, "total_checks": sum(counts.values()),
            "status": "PASS_FINITE_SUPPLEMENT",
            "scope": "Exact finite controls only; the infinite W*-argument is in PROOF.md."}


if __name__ == "__main__":
    print(json.dumps(run(), sort_keys=True, indent=2))
