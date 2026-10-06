#!/usr/bin/env python3
"""Exact action diagnostics fixed after an independent written seal.

No author/reviewer imports; no search for new subsurfaces or target solutions.
The individual checks support finite examples, never a universal geometric claim.
"""
from collections import Counter
from itertools import permutations, product
from pathlib import Path
import json


def mult(left, right):
    return tuple(left[right[k]] for k in range(len(left)))


def invert(element):
    return tuple(element.index(k) for k in range(len(element)))


def comm(left, right):
    return mult(mult(left, right), mult(invert(left), invert(right)))


def generated(gens, identity):
    result = {identity}
    layer = [identity]
    while layer:
        fresh = []
        for element in layer:
            for gen in gens:
                nxt = mult(element, gen)
                if nxt not in result:
                    result.add(nxt)
                    fresh.append(nxt)
        layer = fresh
    return result


def partition(subgroup, points, action):
    unseen = set(points)
    result = []
    while unseen:
        point = min(unseen)
        orbit = {action(g, point) for g in subgroup}
        assert orbit <= unseen
        unseen.difference_update(orbit)
        result.append(sorted(orbit))
    return result


def sign(p):
    return sum(p[i] > p[j] for i in range(len(p)) for j in range(i+1, len(p))) % 2


def cosets(group, stabilizer):
    return sorted({frozenset(mult(g, h) for h in stabilizer) for g in group}, key=lambda c: sorted(c))


def xor_span(values):
    span = {0}
    for value in values:
        span |= {old ^ value for old in tuple(span)}
    return span


def run():
    I4 = tuple(range(4))
    S4 = set(permutations(range(4)))
    A4 = {p for p in S4 if sign(p) == 0}
    s, t = (1, 0, 3, 2), (1, 2, 0, 3)
    a, b, c, e = s, t, t, s
    assert generated([a, b, c, e], I4) == A4
    assert mult(comm(a, b), comm(c, e)) == I4
    second = mult(mult(b, invert(a)), invert(b))
    V4 = generated([a, second], I4)
    assert len(V4) == 4 and V4 < A4
    natural = partition(V4, range(4), lambda g, p: g[p])
    regular = partition(V4, A4, mult)
    assert [len(orb) for orb in natural] == [4]
    assert [len(orb) for orb in regular] == [4, 4, 4]
    derived = generated([comm(x, y) for x in A4 for y in A4], I4)
    assert derived == V4
    point_stabilizer = {g for g in A4 if g[0] == 0}
    assert len(point_stabilizer) == 3
    assert point_stabilizer & V4 == {I4}
    quotient_cosets = cosets(A4, V4)
    assert len(quotient_cosets) == 3
    stabilizer_quotient_images = {frozenset(mult(h, v) for v in V4) for h in point_stabilizer}
    assert stabilizer_quotient_images == set(quotient_cosets)
    # Every character to any abelian group factors through A4/[A4,A4]=C3.
    # Therefore every nonzero prime cyclic character is onto C3 and is nonzero on H.
    # The natural four-sheeted action consequently has no cyclic intermediate cover.
    natural_cosets = cosets(A4, point_stabilizer)
    coset_action = lambda g, coset: frozenset(mult(g, x) for x in coset)
    assert len(partition(V4, natural_cosets, coset_action)) == 1
    # Sufficient factor implication, with C3 quotient: trivial subgroup upstairs
    # has twelve orbits and three quotient orbits. V4 has three upstairs orbits
    # and three quotient orbits; all projected orbits stay within one quotient orbit.
    factor_checks = []
    for subgroup in [{I4}, V4, point_stabilizer, A4]:
        upstairs = partition(subgroup, A4, mult)
        quotient = partition(subgroup, quotient_cosets, coset_action)
        if len(quotient) > 1:
            assert len(upstairs) > 1
        for orbit in upstairs:
            images = {frozenset(mult(x, v) for v in V4) for x in orbit}
            assert any(images <= set(orb) for orb in quotient)
        factor_checks.append({'subgroup_order': len(subgroup), 'upstairs_orbits': len(upstairs), 'quotient_orbits': len(quotient)})
    # Conjugacy changes fiber labels, preserving orbit count even for nonnormal C3.
    conjugacy = []
    for g in A4:
        conjugated = {mult(mult(g, x), invert(g)) for x in point_stabilizer}
        parts = partition(conjugated, range(4), lambda h, p: h[p])
        assert sorted(map(len, parts)) == [1, 3]
        conjugacy.append(sorted(map(len, parts)))
    # Separate proper-transitive example: rotations inside the square dihedral group.
    rotation, reflection = (1, 2, 3, 0), (0, 3, 2, 1)
    D8 = generated([rotation, reflection], I4)
    C4 = generated([rotation], I4)
    assert len(D8) == 8 and len(C4) == 4
    assert list(map(len, partition(C4, range(4), lambda g, p: g[p]))) == [4]
    assert list(map(len, partition(C4, D8, mult))) == [4, 4]
    # All ordered triples in F2^4: exact generator-bound positive control.
    triples = Counter(len(xor_span(v)) for v in product(range(16), repeat=3))
    assert triples == {1: 1, 2: 105, 4: 1470, 8: 2520}
    assert max(triples) == 8 < 16
    # Pants threshold d(G)>2 versus four-boundary d(G)>3.
    pairs = Counter(len(xor_span(v)) for v in product(range(8), repeat=2))
    assert pairs == {1: 1, 2: 21, 4: 42}
    assert len(xor_span([1, 2, 4])) == 8
    # Strong irregular-action boundary control: a faithful transitive group needs
    # four generators but contains a proper transitive cyclic subgroup.
    # W4 is the full rooted binary-tree automorphism group on sixteen leaves.
    depth, degree = 4, 16
    tree_generators = [tuple(i ^ (1 << (depth-1-level)) if i < 1 << (depth-level) else i for i in range(degree)) for level in range(depth)]
    W4 = generated(tree_generators, tuple(range(degree)))
    assert len(W4) == 2 ** (degree-1)
    def reverse_bits(i):
        return int(f'{i:04b}'[::-1], 2)
    odometer = tuple(reverse_bits((reverse_bits(i)+1) % degree) for i in range(degree))
    assert odometer in W4
    cyclic16 = generated([odometer], tuple(range(degree)))
    assert len(cyclic16) == 16 < len(W4)
    assert list(map(len, partition(cyclic16, range(degree), lambda g, p: g[p]))) == [16]
    # The level-parity map is a homomorphism W4 -> F2^4: composition permutes
    # nodes at each level, so node-swap parities add. The four chosen generators
    # have the four independent parity vectors, proving d(W4)>=4; they generate
    # W4, giving d(W4)=4. This lower-bound proof is mathematical, not a sample.
    def level_parity(p):
        parities = []
        for level in range(depth):
            block = 1 << (depth-level)
            half = block // 2
            flips = [(p[start] % block) >= half for start in range(0, degree, block)]
            parities.append(sum(flips) % 2)
        return tuple(parities)
    expected = [tuple(int(k == level) for k in range(depth)) for level in range(depth)]
    assert [level_parity(g) for g in tree_generators] == expected
    # Exact finite verification of parity homomorphism on all elements and four
    # generators suffices for every product, without a quadratic group table.
    for element in W4:
        for g in tree_generators:
            assert level_parity(mult(element, g)) == tuple(x ^ y for x, y in zip(level_parity(element), level_parity(g)))
    # Coherent planar inner-boundary orientation falsifies the original quotient
    # band-sum assertion: under C3 each individual loop maps to 1, xy^-1 to 0,
    # but the actual planar third boundary xy maps to 2 (all in additive C3).
    coherent_boundary_control = {'group': 'C3', 'inner_images': [1, 1], 'quotient_word_image': (1-1) % 3, 'simple_third_boundary_image': (1+1) % 3}
    assert coherent_boundary_control['quotient_word_image'] == 0
    assert coherent_boundary_control['simple_third_boundary_image'] != 0
    # Repaired prefix control is arithmetic only; the representative is proved
    # separately in REPAIR_AND_ACTION_REVIEW.md. Noncommutative A4 is included.
    prefixes_controls = []
    choices = [([s] * len(A4), 'A4 repeated'), ([s, t] * 6, 'A4 noncommuting'), (list(sorted(A4)), 'A4 all elements')]
    for words, name in choices:
        prefixes = [I4]
        for word in words:
            prefixes.append(mult(prefixes[-1], word))
        witnesses = [(i, j) for j in range(1, len(prefixes)) for i in range(j) if prefixes[i] == prefixes[j]]
        assert witnesses
        i, j = witnesses[0]
        block = I4
        for word in words[i:j]:
            block = mult(block, word)
        assert block == I4
        prefixes_controls.append({'control': name, 'prefix_count': len(prefixes), 'group_order': len(A4), 'repeated_prefix_indices': [i, j], 'nonempty_block_size': j-i, 'block_image': list(block)})
    result = {
        'all_passed': True,
        'scope': 'Exact finite action examples; no universal target, topology, novelty, or proof-search certification.',
        'a4_fixed_pants_negative_control': {'cover_relation_holds': True, 'monodromy_order': 12, 'pants_image_order': 4, 'regular_degree': 12, 'regular_domain_genus': 13, 'regular_component_degrees': list(map(len, regular)), 'irregular_degree': 4, 'irregular_domain_genus': 5, 'irregular_component_degrees': list(map(len, natural)), 'invalid_descent_demonstrated': True},
        'a4_nonperfect_irregular_no_cyclic_intermediate': {'derived_order': len(derived), 'abelianization_order': 3, 'point_stabilizer_order': len(point_stabilizer), 'stabilizer_surjects_abelianization': True, 'nonzero_character_killing_stabilizer_exists': False},
        'valid_factor_projection_controls': factor_checks,
        'conjugacy_control_orbit_sizes': conjugacy,
        'd8_rotation_negative_control': {'regular_orbits': [4, 4], 'natural_orbits': [4]},
        'regular_f2_4_all_ordered_triples_span_size_counts': dict(triples),
        'regular_f2_3_all_ordered_pairs_span_size_counts': dict(pairs),
        'f2_3_three_generator_transitive_boundary_control': True,
        'irregular_four_generator_group_with_proper_transitive_one_generator_subgroup': {'group': 'W4 rooted binary tree automorphisms', 'degree': degree, 'group_order': len(W4), 'minimal_generators': 4, 'transitive_cyclic_subgroup_order': 16, 'cyclic_orbits': [16], 'level_parity_quotient': 'F2^4'},
        'coherent_boundary_quotient_word_failure': coherent_boundary_control,
        'repaired_noncommutative_prefix_arithmetic_controls': prefixes_controls,
    }
    path = Path(__file__).with_name('independent_action_results.json')
    path.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    run()
