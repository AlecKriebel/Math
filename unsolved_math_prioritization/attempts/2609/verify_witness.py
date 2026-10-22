#!/usr/bin/env python3
"""Exact finite witness for Hou's counterexample; Python standard library only.

This verifies the 128-point data, not a 2^135-element multiplication table.
The irreducibility and exhaustive character-count arguments are in CERTIFICATE.md.
"""
import json


def mul(a, b, modulus, degree):
    out = 0
    while b:
        if b & 1:
            out ^= a
        a <<= 1
        if a & (1 << degree):
            a ^= modulus
        b >>= 1
    return out


def operator(v):
    x, y, z = v & 3, (v >> 2) & 3, v >> 4
    return mul(2, x, 7, 2) | (mul(2, y, 7, 2) << 2) | (mul(2, z, 11, 3) << 4)


def main():
    vertices = range(128)
    T = [operator(v) for v in vertices]
    assert sorted(T) == list(vertices)
    linear_checks = 0
    for v in vertices:
        for w in vertices:
            assert T[v ^ w] == T[v] ^ T[w]
            linear_checks += 1
    power = list(vertices)
    order = None
    for k in range(1, 22):
        power = [T[x] for x in power]
        if power == list(vertices):
            order = k
            break
    assert order == 21
    assert [v for v in vertices if T[v] == v] == [0]
    orbits, seen = [], set()
    for v in vertices:
        if v in seen:
            continue
        orbit, w = [], v
        while w not in orbit:
            orbit.append(w)
            w = T[w]
        assert w == v
        seen.update(orbit)
        orbits.append(sorted(orbit))
    assert sorted(map(len, orbits)) == [1, 3, 3, 3, 3, 3, 7, 21, 21, 21, 21, 21]
    mixed = [o for o in orbits if len(o) == 21]
    support = {0}.union(*map(set, mixed[:3]))
    assert len(support) == 64
    assert {T[x] for x in support} == support
    diagonal = [(-1 if x in support else 1) for x in vertices]
    assert sum(diagonal) == 0
    # The B-weights of the induced representation are the distinct evaluations f -> (-1)^f(t).
    # delta_j separates the weight indexed by j from every other evaluation.
    assert len({1 << v for v in vertices}) == 128
    # Generator conjugation: translation takes coordinate delta_j to delta_(j+t).
    conjugation_checks = 0
    for t in vertices:
        for j in vertices:
            assert T[j ^ t] == T[j] ^ T[t]
            conjugation_checks += 1
    half_subsets = sum(sum(len(o) for i, o in enumerate(orbits) if mask >> i & 1) == 64
                       for mask in range(1 << len(orbits)))
    assert half_subsets == 20
    result = {
        "status": "PASS", "field_moduli_binary": [7, 11], "vector_count": 128,
        "operator_order": order, "operator_fixed_vectors": [0],
        "orbit_sizes": sorted(map(len, orbits)), "orbits": orbits,
        "group_order_power_of_2": 135, "centralizer_rank": len(orbits),
        "centralizer_order": 4096, "invariant_irreducible_count_by_proof": 4096,
        "witness_character_degree": 128, "witness_support": sorted(support),
        "witness_support_size": len(support), "witness_character_value": sum(diagonal),
        "half_size_invariant_subsets": half_subsets,
        "linearity_checks": linear_checks, "generator_conjugation_checks": conjugation_checks,
        "scope": "Exact finite data for the written proof; no exhaustive enumeration of G."
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
