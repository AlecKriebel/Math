#!/usr/bin/env python3
"""Independent ribbon/gluing controls; not a universal surface-proof engine.

No import from either old checker. All gluings are orientation reversing,
all ribbon bands untwisted. Boundary permutations record actual oriented
thickenings; connectivity comes from the gluing graph, then genus from chi.
The universal hypotheses/embedding arguments remain in REPORT.md.
"""
from pathlib import Path
from itertools import product
from collections import defaultdict
import hashlib
import json

ROOT = Path(__file__).resolve().parent
checks = 0

def check(value, label):
    global checks
    checks += 1
    if not value:
        raise AssertionError(label)


def cycles(permutation):
    unseen = set(permutation)
    answer = []
    while unseen:
        start = min(unseen)
        current = start
        cycle = []
        while current not in cycle:
            if current not in unseen:
                raise ValueError('not a permutation')
            unseen.remove(current)
            cycle.append(current)
            current = permutation[current]
        if current != start:
            raise ValueError('not a disjoint cycle')
        answer.append(cycle)
    return answer


def ribbon_surface(rotations, pairs):
    """Thicken a connected graph with vertex rotations and paired darts."""
    sigma = {}
    owner = {}
    for i, rotation in enumerate(rotations):
        if not rotation:
            raise ValueError('empty vertex')
        for j, dart in enumerate(rotation):
            if dart in owner:
                raise ValueError('duplicate dart')
            owner[dart] = i
            sigma[dart] = rotation[(j + 1) % len(rotation)]
    alpha = {}
    adjacency = defaultdict(set)
    for x, y in pairs:
        if x == y or x in alpha or y in alpha:
            raise ValueError('invalid dart pairing')
        alpha[x], alpha[y] = y, x
        adjacency[owner[x]].add(owner[y])
        adjacency[owner[y]].add(owner[x])
    if set(alpha) != set(sigma):
        raise ValueError('unpaired dart')
    visited = {0}
    todo = [0]
    while todo:
        i = todo.pop()
        for j in adjacency[i] - visited:
            visited.add(j)
            todo.append(j)
    if len(visited) != len(rotations):
        raise ValueError('disconnected ribbon graph')
    boundary_cycles = cycles({d: sigma[alpha[d]] for d in sigma})
    chi = len(rotations) - len(pairs)
    b = len(boundary_cycles)
    numerator = 2 - b - chi
    if numerator < 0 or numerator % 2:
        raise ValueError('invalid oriented surface')
    return {'genus': numerator // 2, 'boundary': b, 'chi': chi,
            'boundary_cycles': boundary_cycles}


def piece(genus, labels):
    return (genus, tuple(labels))


def assembled(pieces, gluings):
    """Return all connected surface types for labelled boundary gluings."""
    parent = {name: name for name in pieces}
    def find(x):
        while parent[x] != x:
            x = parent[x]
        return x
    owner = {}
    for name, (g, labels) in pieces.items():
        if g < 0 or not labels:
            raise ValueError('pieces must have nonempty boundary')
        for label in labels:
            if label in owner:
                raise ValueError('duplicate boundary label')
            owner[label] = name
    used = set()
    for x, y in gluings:
        if x == y or x in used or y in used or x not in owner or y not in owner:
            raise ValueError('illegal boundary gluing')
        used.update((x, y))
        a, b = find(owner[x]), find(owner[y])
        parent[b] = a
    groups = defaultdict(list)
    for name in pieces:
        groups[find(name)].append(name)
    results = []
    for names in groups.values():
        chi = sum(2 - 2 * pieces[n][0] - len(pieces[n][1]) for n in names)
        boundaries = sorted(label for n in names for label in pieces[n][1] if label not in used)
        numerator = 2 - len(boundaries) - chi
        if numerator < 0 or numerator % 2:
            raise ValueError('invalid oriented gluing')
        results.append({'pieces': sorted(names), 'genus': numerator // 2,
                        'boundary': len(boundaries), 'chi': chi,
                        'boundary_labels': boundaries})
    return sorted(results, key=lambda c: c['pieces'])


def is_essential_cut(pieces, gluings, index):
    cut = assembled(pieces, gluings[:index] + gluings[index + 1:])
    return not any(c['genus'] == 0 and c['boundary'] == 1 for c in cut), cut


def four_partitions(n):
    """Restricted-growth strings: each unlabelled partition exactly once."""
    def visit(values, largest):
        if len(values) == n:
            if largest == 3:
                yield tuple(values)
            return
        for value in range(min(largest + 1, 3) + 1):
            if largest == 3 or n - len(values) >= 3 - largest:
                yield from visit(values + [value], max(largest, value))
    yield from visit([0], 0)


def central_planar_model(g, partition):
    counts = [partition.count(i) for i in range(4)]
    if not all(counts):
        raise ValueError('empty peripheral group')
    pieces = {'H': piece(0, ['h' + str(i) for i in range(4)])}
    gluings = []
    for i in range(4):
        labels = ['q' + str(i)] + ['c' + str(j) for j in range(2 * g) if partition[j] == i]
        pieces['Q' + str(i)] = piece(0, labels)
        gluings.append(('h' + str(i), 'q' + str(i)))
    gluings += [('c' + str(2 * j), 'c' + str(2 * j + 1)) for j in range(g)]
    return pieces, gluings


def large_genus_final_model(g):
    # P contains the alpha pair; H contains the beta pair. E is T's exterior.
    pieces = {'P': piece(0, ['ap', 'am', 'pdelta']),
              'H': piece(0, ['bp', 'bm', 'hdelta', 'houter']),
              'E': piece(g - 2, ['eouter'])}
    gluings = [('ap', 'am'), ('bp', 'bm'), ('pdelta', 'hdelta'), ('houter', 'eouter')]
    return pieces, gluings


def main():
    global checks
    ribbon_results = {}
    torus = ribbon_surface([['ap', 'bp', 'am', 'bm']], [('ap', 'am'), ('bp', 'bm')])
    check((torus['genus'], torus['boundary']) == (1, 1), 'alternating dual curves thicken to one-holed torus')
    ribbon_results['dual_pair'] = torus
    planar = ribbon_surface([['ap', 'am', 'bp', 'bm']], [('ap', 'am'), ('bp', 'bm')])
    check((planar['genus'], planar['boundary']) == (0, 3), 'wrong rotation is pants, not torus')
    ribbon_results['wrong_rotation_negative_control'] = planar
    pairs = [('ap', 'am'), ('bp', 'bm'), ('cp', 'cm'), ('dp', 'dm'), ('xp', 'xm')]
    bridge_controls = []
    # Every slot on each of the two torus boundaries gives the same type.
    for i in range(5):
        for j in range(5):
            left = ['ap', 'bp', 'am', 'bm']; left.insert(i, 'xp')
            right = ['cp', 'dp', 'cm', 'dm']; right.insert(j, 'xm')
            result = ribbon_surface([left, right], pairs)
            check((result['genus'], result['boundary'], result['chi']) == (2, 1, -3), 'distinct-torus bridge')
            bridge_controls.append(result)
    ribbon_results['two_tori_bridge_slots'] = len(bridge_controls)
    ribbon_results['representative_two_tori_bridge'] = bridge_controls[0]

    # Critical same-tree counterexample: two disjoint circles plus their
    # connecting tree arc thicken to pants. Coherent peripheral orientations
    # have simple classes x,y,xy (up to inversion), never x*y^-1.
    tree_pants = ribbon_surface([['xp', 'xm', 'zp'], ['yp', 'ym', 'zm']],
                                [('xp', 'xm'), ('yp', 'ym'), ('zp', 'zm')])
    check((tree_pants['genus'], tree_pants['boundary']) == (0, 3), 'two disjoint loops plus tree arc are pants')
    peripheral_vectors = {(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1)}
    check((1, -1) not in peripheral_vectors, 'quotient homology is not any simple pants boundary')
    ribbon_results['same_tree_pants_counterexample'] = tree_pants

    # Repair control, using additive C_m as a finite diagnostic only.
    # m+1 prefixes force a nonempty interval product to vanish. Universal
    # nonabelian prefix argument and interval embeddedness are in REPORT.md.
    prefix_tuples = 0
    for m in range(2, 7):
        for values in product(range(m), repeat=m):
            prefixes = [0]
            for value in values:
                prefixes.append((prefixes[-1] + value) % m)
            witnesses = [(i, j) for i in range(m + 1) for j in range(i + 1, m + 1)
                         if prefixes[i] == prefixes[j]]
            check(bool(witnesses), 'prefix pigeonhole interval exists')
            i, j = witnesses[0]
            check(sum(values[i:j]) % m == 0 and j > i, 'nonempty interval killed')
            check(any(int(i <= k < j) for k in range(m)), 'interval homology nonzero')
            prefix_tuples += 1

    partitions_tested = []
    for g in (2, 3, 4):
        count = 0
        for partition in four_partitions(2 * g):
            pieces, gluings = central_planar_model(g, partition)
            whole = assembled(pieces, gluings)
            check(len(whole) == 1 and (whole[0]['genus'], whole[0]['boundary']) == (g, 0), 'closed cut-system reconstruction')
            for index in range(4):
                essential, cut = is_essential_cut(pieces, gluings, index)
                check(essential, 'all four central boundaries essential')
            count += 1
        partitions_tested.append({'genus': g, 'partitions': count})
    check(partitions_tested[0]['partitions'] == 1, 'minimum genus2 cut complement')

    large_controls = []
    for g in range(4, 65):
        pieces, gluings = large_genus_final_model(g)
        reconstructed = assembled(pieces, gluings)
        check(len(reconstructed) == 1 and reconstructed[0]['genus'] == g and reconstructed[0]['boundary'] == 0, 'closed large-genus reconstruction')
        types = []
        for index in range(4):
            essential, cut = is_essential_cut(pieces, gluings, index)
            check(essential, 'alpha beta new old separating boundary essential')
            types.append([(c['genus'], c['boundary']) for c in cut])
        check(sorted(types[2]) == [(1, 1), (g - 1, 1)], 'new H boundary separates genus1')
        check(sorted(types[3]) == [(2, 1), (g - 2, 1)], 'old T boundary separates genus2')
        check(types[1] == [(g - 1, 2)], 'beta boundary nonseparating')
        large_controls.append({'genus': g, 'cut_types': types})
    # Deliberately violating g>=4: at g2 the old T boundary bounds a disk.
    p2, gl2 = large_genus_final_model(2)
    essential2, cut2 = is_essential_cut(p2, gl2, 3)
    check(not essential2 and any(c['genus'] == 0 and c['boundary'] == 1 for c in cut2), 'genus2 extension rejected: delta_T inessential')

    # Fully independent algebraic controls for two tempting invalid shortcuts.
    def compose(p, q):
        return tuple(p[q[i]] for i in range(len(p)))
    def inverse(p):
        return tuple(p.index(i) for i in range(len(p)))
    r, t, ident = (1, 2, 0), (1, 0, 2), (0, 1, 2)
    correct = compose(r, inverse(r))
    wrong_orientation = compose(r, r)
    hidden_conjugator = compose(compose(compose(r, t), inverse(r)), inverse(t))
    check(correct == ident, 'equal coherent based images give killed difference')
    check(wrong_orientation != ident, 'same orientation product can survive')
    check(hidden_conjugator != ident, 'extra relative whisker conjugator can survive')
    # Nonplanar boundary-only test: free F2 -> C2 with a nonzero,b zero.
    # The boundary word [a,b] has exponent sum zero, yet a survives.
    boundary_word = [('a', 1), ('b', 1), ('a', -1), ('b', -1)]
    character = {'a': 1, 'b': 0}
    boundary_image = sum(character[x] * e for x, e in boundary_word) % 2
    check(boundary_image == 0 and character['a'] != 0, 'killed torus boundary does not kill its fundamental group')

    invalid = []
    for name, thunk in [
        ('reused_boundary', lambda: assembled({'A': piece(0, ['a', 'b', 'c'])}, [('a', 'b'), ('a', 'c')])),
        ('empty_partition_group', lambda: central_planar_model(2, (0, 1, 2, 2))),
        ('duplicate_dart', lambda: ribbon_surface([['a', 'a']], [('a', 'b')])),
    ]:
        try:
            thunk()
        except (ValueError, KeyError) as error:
            invalid.append({'name': name, 'exception': type(error).__name__, 'message': str(error)})
        else:
            raise AssertionError('invalid input accepted: ' + name)
    check(len(invalid) == 3, 'invalid combinatorial inputs rejected')
    output = {'status': 'PASS_SUPPLEMENTARY_CONTROLS_ONLY', 'assertions': checks,
              'ribbon_results': ribbon_results, 'central_planar_partitions': partitions_tested,
              'large_genus_controls': large_controls,
              'g2_out_of_hypothesis_counterexample': cut2,
              'algebra_negative_controls': {'correct_difference': correct, 'wrong_orientation': wrong_orientation,
                  'hidden_conjugator': hidden_conjugator, 'nonplanar_boundary_image': boundary_image,
                  'nonplanar_generator_image': character['a']},
              'input_rejections': invalid,
              'prefix_repair_tuples': prefix_tuples,
              'original_same_tree_quotient_step': 'REQUIRES_REPAIR: quotient is not always a simple pants-neighborhood class',
              'limitations': 'Finite ribbon/gluing templates certify their encoded surfaces only. They do not prove universal embedding or representation lemmas; REPORT.md supplies those. No subsurface existence search, no source-question resolution.',
              'code_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    (ROOT/'geometric_control_results.json').write_text(json.dumps(output, indent=2)+'\n')
    print(json.dumps({'status': output['status'], 'assertions': checks, 'partitions': partitions_tested,
                      'large_genus_values': len(large_controls), 'invalid_inputs_rejected': len(invalid)}, indent=2))

if __name__ == '__main__':
    main()
