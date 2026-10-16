#!/usr/bin/env python3
"""Exact finite checks for the counterexample; Python standard library only."""
import argparse
from collections import Counter, deque
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent

def require(condition, message):
    if not condition:
        raise RuntimeError(message)

def identity(n):
    return tuple(range(n))

def compose(a, b):
    return tuple(a[b[i]] for i in range(len(a)))

def inverse(a):
    return tuple(a.index(i) for i in range(len(a)))

def generated(generators, n):
    e = identity(n)
    group, todo = {e}, [e]
    while todo:
        a = todo.pop()
        for b in generators:
            c = compose(a, b)
            if c not in group:
                group.add(c)
                todo.append(c)
    return frozenset(group)

def cycles(a):
    seen, answer = set(), []
    for i in range(len(a)):
        if i in seen:
            continue
        c, j = [], i
        while j not in seen:
            seen.add(j)
            c.append(j)
            j = a[j]
        if len(c) > 1:
            answer.append(frozenset(c))
    return answer

def is_block(block, group):
    return all(not block.intersection(a[i] for i in block)
               or block == frozenset(a[i] for i in block) for a in group)

def cycle_block(group):
    return all(is_block(c, group) for a in group for c in cycles(a))

def transitive(group, n):
    return {a[0] for a in group} == set(range(n))

def parity(mask):
    return mask.bit_count() % 2

def shift(mask, t):
    return sum(((mask >> (v ^ t)) & 1) << v for v in range(4))

def action(mask, t):
    # Destination-indexed f, matching the proof.
    return tuple(2 * (v ^ t) + (epsilon ^ ((mask >> (v ^ t)) & 1))
                 for v in range(4) for epsilon in range(2))

def from_cycles(n, *cs):
    a = list(range(n))
    for c in cs:
        for i, j in zip(c, c[1:] + c[:1]):
            a[i - 1] = j - 1
    return tuple(a)

def subgroup_lattice(group):
    elems = sorted(group)
    index = {g: i for i, g in enumerate(elems)}
    e = index[identity(len(elems[0]))]
    table = [[index[compose(a, b)] for b in elems] for a in elems]
    initial = frozenset([e])
    known, todo = {initial}, deque([initial])
    while todo:
        H = todo.popleft()
        for x in range(len(elems)):
            if x in H:
                continue
            gens = list(H) + [x]
            K, pending = {e}, [e]
            while pending:
                a = pending.pop()
                for b in gens:
                    c = table[a][b]
                    if c not in K:
                        K.add(c)
                        pending.append(c)
            K = frozenset(K)
            if K not in known:
                known.add(K)
                todo.append(K)
    return elems, sorted(known, key=lambda H: (len(H), sorted(H)))

def run():
    params = [(f, t) for f in range(16) for t in range(4)
              if parity(f) == (t & 1)]
    P = frozenset(action(f, t) for f, t in params)
    require(len(P) == 32, 'P order')
    require(all(compose(a, b) in P for a in P for b in P), 'P closure')
    require(transitive(P, 8), 'P transitivity')
    # Independently verify the semidirect product law for every ambient pair.
    ambient_params = [(f, t) for f in range(16) for t in range(4)]
    for f, t in ambient_params:
        for g, u in ambient_params:
            require(compose(action(f, t), action(g, u))
                    == action(f ^ shift(g, t), t ^ u), 'action law')

    a, b, z = action(1, 1), action(0, 2), action((1 << 1) | (1 << 2), 0)
    require(a == from_cycles(8, (1, 3, 2, 4), (5, 7), (6, 8)), 'a labels')
    require(b == from_cycles(8, (1, 5), (2, 6), (3, 7), (4, 8)), 'b labels')
    require(z == from_cycles(8, (3, 4), (5, 6)), 'z labels')
    require(generated([a, b], 8) == P, 'generators')
    C = frozenset([0, 4])
    zC = frozenset(z[i] for i in C)
    require(C in cycles(b), 'C is complete b cycle')
    require(zC == frozenset([0, 5]) and len(C & zC) == 1, 'crossing witness')
    require(not cycle_block(P), 'P must fail cycle-block')

    elems, lattice = subgroup_lattice(P)
    transitive_indices = [i for i, H in enumerate(lattice)
                          if {elems[k][0] for k in H} == set(range(8))]
    require(len(transitive_indices) == 1, 'unique transitive subgroup')
    require(len(lattice[transitive_indices[0]]) == 32, 'transitive subgroup is P')

    # Frattini cross-check, independent of the difference-operator proof.
    phi_gens = [compose(g, g) for g in P]
    phi_gens += [compose(compose(compose(g, h), inverse(g)), inverse(h))
                 for g in P for h in P]
    Phi = generated(phi_gens, 8)
    E0 = frozenset(action(f, 0) for f in range(16) if parity(f) == 0)
    stabilizer = frozenset(g for g in P if g[0] == 0)
    require(Phi == E0 and len(Phi) == 8, 'Frattini kernel')
    require(len(stabilizer) == 4 and stabilizer <= Phi, 'point stabilizer')

    pair_count = 0
    for f in range(16):
        if parity(f) != 1:
            continue
        for g in range(16):
            if parity(g) != 0:
                continue
            h = f ^ shift(f, 1)
            c = f ^ shift(f, 2) ^ g ^ shift(g, 1)
            require(c ^ shift(c, 1) == 15, 'D1 commutator identity')
            require(generated([action(f, 1), action(g, 2)], 8) == P,
                    'arbitrary e1/e2 lifts generate P')
            pair_count += 1
    require(pair_count == 64, 'lift pair count')

    # Full first wreath stage: two independent P copies and a copy swap.
    W1 = set()
    for x in P:
        for y in P:
            base = tuple(x) + tuple(8 + i for i in y)
            W1.add(base)
            W1.add(tuple((i + 8) % 16 for i in base))
    W1 = frozenset(W1)
    swap = tuple((i + 8) % 16 for i in range(16))
    first_a = tuple(a) + tuple(range(8, 16))
    first_b = tuple(b) + tuple(range(8, 16))
    require(generated([first_a, first_b, swap], 16) == W1, 'wreath generation')
    require(len(W1) == 2048 and transitive(W1, 16), 'wreath order/transitivity')
    B = frozenset(range(8))
    require(is_block(B, W1), 'bottom block')
    restricted = frozenset(tuple(g[i] for i in range(8))
                          for g in W1 if frozenset(g[i] for i in B) == B)
    require(restricted == P, 'exact bottom block induced action')

    # Negative controls: checker must not label everything as an obstruction.
    full = frozenset(action(f, t) for f, t in ambient_params)
    R = generated([action(15, 0), action(0, 1), action(0, 2)], 8)
    require(len(full) == 64 and R <= full and len(R) == 8, 'untwisted control')
    require(transitive(R, 8) and cycle_block(R), 'regular positive control')
    require(is_block(C, [identity(8)]), 'identity is not a crossing witness')
    d, r = from_cycles(4, (1, 2)), from_cycles(4, (1, 3, 2, 4))
    D8 = generated([d, r], 4)
    require(len(D8) == 8, 'dihedral order')
    require(all(is_block(c, D8) for q in [d, r] for c in cycles(q)),
            'dihedral selected generators pass')
    require(not cycle_block(D8), 'dihedral all-elements rejection')
    require(any(not is_block(c, D8) for c in cycles(compose(d, r))),
            'dihedral product witness')

    certificate = {
        'point_labels': '1 through 8, pair (v,epsilon) labelled 2v+epsilon+1',
        'elements_one_based': [[i + 1 for i in x] for x in elems],
        'generators_one_based': [[i + 1 for i in x] for x in [a, b]],
        'subgroup_masks': [sum(1 << k for k in H) for H in lattice],
        'mask_convention': 'bit k means element k in elements_one_based; lattice sorted by order then indices',
        'transitive_subgroup_indices': transitive_indices,
        'crossing_witness': {'b': [i + 1 for i in b], 'z': [i + 1 for i in z],
                             'C': [1, 5], 'zC': [1, 6]},
    }
    results = {
        'status': 'PASS', 'exact_arithmetic': True,
        'ambient_action_law_pairs_checked': 4096,
        'P_order': len(P), 'P_transitive': True,
        'all_subgroups_count': len(lattice),
        'subgroup_order_histogram': dict(sorted(Counter(str(len(H)) for H in lattice).items(),
                                              key=lambda item: int(item[0]))),
        'transitive_subgroup_count': len(transitive_indices),
        'only_transitive_subgroup_is_P': True, 'P_cycle_block_property': False,
        'Frattini_order': len(Phi), 'point_stabilizer_order': len(stabilizer),
        'point_stabilizer_in_Frattini': True,
        'all_e1_e2_lift_pairs_generate_P': pair_count,
        'first_wreath_stage_order': len(W1), 'first_wreath_stage_transitive': True,
        'bottom_fibre_is_block': True, 'bottom_induced_action_equals_P': True,
        'negative_controls': {
            'untwisted_ambient_contains_regular_cycle_block_group': True,
            'identity_is_rejected_as_crossing_witness': True,
            'generator_only_test_false_positive_exhibited': True,
        },
        'infinite_limit': 'Proved in PROOFS.md, not inferred from finite enumeration',
    }
    return results, certificate

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true', help='compare to frozen JSON outputs')
    args = parser.parse_args()
    results, certificate = run()
    for filename, obj in [('CHECK_RESULTS.json', results), ('FINITE_CERTIFICATE.json', certificate)]:
        if args.check:
            require(json.loads((ROOT / filename).read_text()) == obj, filename + ' mismatch')
        else:
            (ROOT / filename).write_text(json.dumps(obj, indent=2, sort_keys=True) + '\n')
    print(json.dumps(results, indent=2, sort_keys=True))

if __name__ == '__main__':
    main()
