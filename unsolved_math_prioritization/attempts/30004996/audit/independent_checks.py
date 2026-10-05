#!/usr/bin/env python3
"""Independent finite controls. No external packages or source-code imports.
These are consistency checks, not proofs of the infinite Borel assertions.
"""
import json
from itertools import product, combinations
from fractions import Fraction

counts = {}
def check(name, condition):
    if not condition:
        raise AssertionError(name)
    counts[name] = counts.get(name, 0) + 1

# D_8, using a different group and representation than the packet's S_3.
G = tuple(product(range(4), range(2)))
e = (0, 0)
idx = {g: i for i, g in enumerate(G)}
def mul(g, h):
    r, f = g; s, t = h
    return ((r + (-1 if f else 1) * s) % 4, f ^ t)
def inv(g):
    return next(h for h in G if mul(g, h) == e == mul(h, g))
def right(g, y):
    return tuple(y[idx[mul(d, g)]] for d in G)
def left(g, y):
    return tuple(y[idx[mul(inv(g), d)]] for d in G)
def invert_coords(y):
    return tuple(y[idx[inv(d)]] for d in G)
words = tuple(product((0, 1), repeat=8))
noncentral_failures = []
for g, h, d in product(G, repeat=3):
    check('group_associativity', mul(mul(g, h), d) == mul(g, mul(h, d)))
    if mul(g, h) != mul(h, g):
        a, b = mul(mul(d, g), h), mul(mul(d, h), g)
        check('noncentral_rearrangement_fails', a != b)
        if not noncentral_failures:
            noncentral_failures.append({'g': g, 'h': h, 'd': d, 'dgh': a, 'dhg': b})
for y in words:
    for g in G:
        check('left_right_conjugacy', invert_coords(left(g, y)) == right(g, invert_coords(y)))
        for h in G:
            check('right_shift_action', right(g, right(h, y)) == right(mul(g, h), y))
            if mul(g, h) == mul(h, g):
                for d in G:
                    moved_after_h = right(h, y)[idx[d]] != right(h, y)[idx[mul(d, g)]]
                    new_d = mul(d, h)
                    check('centralizer_witness_transfer', moved_after_h == (y[idx[new_d]] != y[idx[mul(new_d, g)]]))

# Translated finite-window constraints must define invariant subsets,
# including for a genuinely noncommutative group.
D_cases = [(e,), ((1, 0),), (e, (0, 1)), ((1, 0), (2, 1), (3, 0)), G]
constraint_targets = 0
for g in G:
    if g == e:
        continue
    for D in D_cases:
        def legal(y):
            return all(any(y[idx[mul(d, h)]] != y[idx[mul(mul(d, g), h)]] for d in D) for h in G)
        accepted = {y for y in words if legal(y)}
        constraint_targets += 1
        for y in accepted:
            for h in G:
                check('translated_constraint_invariance', right(h, y) in accepted)
        for y in accepted:
            check('identity_translate_separates', right(g, y) != y)

# All finite families of C_3 binary words: exact uniform-witness criterion.
Cwords = tuple(product((0, 1), repeat=3))
for mask in range(1, 1 << len(Cwords)):
    family = [w for i, w in enumerate(Cwords) if mask & (1 << i)]
    is_free = all(all(tuple(w[(d+g)%3] for d in range(3)) != w for g in (1,2)) for w in family)
    witnesses_exist = True
    for g in (1, 2):
        found = any(all(any(w[d] != w[(d+g)%3] for d in D) for w in family)
                    for r in range(4) for D in combinations(range(3), r))
        witnesses_exist &= found
    check('finite_family_uniform_witness_equivalence', is_free == witnesses_exist)

# Exhaustive finite monotone languages via an independent transition-matrix count.
M = ((1, 1), (0, 1))
v = (1, 1)
monotone_counts = {}
for n in range(1, 15):
    legal = [w for w in product((0,1), repeat=n) if all(a <= b for a, b in zip(w,w[1:]))]
    check('monotone_transfer_count', len(legal) == sum(v) == n+1)
    check('monotone_cycle_constants', all(len(set(w)) == 1 for w in legal if w[-1] <= w[0]))
    monotone_counts[str(n)] = sum(v)
    v = tuple(sum(v[i]*M[i][j] for i in (0,1)) for j in (0,1))

# Even shifts separate finite coordinate supports, yielding exact independent
# cylinder probabilities. This checks the algebra used in the mixing proof.
for F in [(-2,0,2), (0,), (-3,-1,2,4)]:
    for H in [(-1,1), (0,2,3)]:
        for shift in [20,22,40]:
            for a in product((0,1), repeat=len(F)):
                for b in product((0,1), repeat=len(H)):
                    constraints = dict(zip(F,a)); constraints.update(zip((x+shift for x in H),b))
                    check('disjoint_cylinder_probability', Fraction(1,2**len(constraints)) == Fraction(1,2**len(F))*Fraction(1,2**len(H)))
for a in (0,1):
    check('parity_square_invariance', 1-(1-a) == a)
check('parity_ergodicity_contradiction', Fraction(1,2) not in (Fraction(0),Fraction(1)))

# A phase of an n-dilated support misses each tested central window. The
# underlying sequence is arbitrary here: only the zero-limit mechanism is tested.
for R in range(51):
    n = 2*R+3; phase = R+1
    check('dilated_phase_zero_window', all((j-phase)%n != 0 for j in range(-R,R+1)))
for R in range(31):
    for g in range(-15,16):
        if not g:
            continue
        D = range(-R,R+1); marker = R+abs(g)+1
        check('escaping_marker_uniform_failure', all(int(d==marker)==int(d+g==marker) for d in D))
        check('escaping_marker_is_moved', int(marker==marker)!=int(marker+g==marker))

print(json.dumps({
    'all_passed': True, 'assertions': sum(counts.values()), 'checks_by_family': counts,
    'finite_group': 'D_8 (dihedral group of order eight)', 'binary_words': len(words),
    'finite_constraint_targets': constraint_targets, 'monotone_word_counts': monotone_counts,
    'noncentral_rearrangement_counterexample': noncentral_failures[0],
    'scope': 'Finite controls only. Baire category, compactness, freeness of infinite flows, and ergodicity are audited in the written proof.'
}, indent=2, sort_keys=True))
