"""Finite algebra supporting the separately written topological deduction.

No source checker is imported, no certificate is rewritten, and no theorem
about the exact genus or an unread published article is machine-certified.
"""
from itertools import product
import json

H = list(product(range(3), repeat=3))
I = (0, 0, 0)


def mul(g, h):
    a, b, t = g
    d, e, s = h
    return ((a+d) % 3, (b+e) % 3, (t+s+b*d) % 3)


def matrix(g):
    a, b, t = g
    # Column j is omega**(t+b*j) times the (j+a)-th basis vector.
    return tuple(((j+a) % 3, (t+b*j) % 3) for j in range(3))


def mmul(g, h):
    return tuple((g[h[j][0]][0], (h[j][1]+g[h[j][0]][1]) % 3)
                 for j in range(3))


def f(g):
    a, b, t = g
    return (t-a*b) % 3


def delta(fn, g, h):
    return (fn(h)-fn(mul(g, h))+fn(g)) % 3


def need(ok, label):
    if not ok:
        raise RuntimeError(label)


def main():
    need(len({matrix(g) for g in H}) == 27, 'matrix representation not faithful')
    inv = {}
    for g in H:
        need(mul(g, I) == mul(I, g) == g, 'identity')
        matches = [h for h in H if mul(g, h) == mul(h, g) == I]
        need(len(matches) == 1, 'inverse')
        inv[g] = matches[0]
    pair_count = 0
    for g, h in product(H, repeat=2):
        need(matrix(mul(g, h)) == mmul(matrix(g), matrix(h)), 'matrix law')
        need(delta(f, g, h) == g[0]*h[1] % 3, 'cup/coboundary identity')
        need(mul(g, h)[:2] == ((g[0]+h[0]) % 3, (g[1]+h[1]) % 3),
             'quotient map')
        pair_count += 1
    for g, h, k in product(H, repeat=3):
        need(mul(mul(g, h), k) == mul(g, mul(h, k)), 'associativity')
    center = {g for g in H if all(mul(g, h) == mul(h, g) for h in H)}
    commutators = {mul(mul(mul(g, h), inv[g]), inv[h])
                   for g, h in product(H, repeat=2)}
    need(center == commutators == {(0, 0, t) for t in range(3)},
         'actual central extension/abelianization')
    homs = [lambda g, u=u, v=v: (u*g[0]+v*g[1]) % 3
            for u, v in product(range(3), repeat=2)]
    for hom, g, h in product(homs, H, H):
        need(hom(mul(g, h)) == (hom(g)+hom(h)) % 3, 'H1 coordinates')
    # All homomorphisms to the abelian additive F3 factor through H/[H,H]
    # and hence these nine coordinate maps exhaust them; topology is separate.
    wrong_sign = lambda g: (g[2]+g[0]*g[1]) % 3
    wrong_sign_failures = sum(delta(wrong_sign, g, h) != g[0]*h[1] % 3
                              for g, h in product(H, repeat=2))
    zero_primitive_failures = sum(g[0]*h[1] % 3 != 0 for g, h in product(H, repeat=2))
    need(wrong_sign_failures > 0 and zero_primitive_failures > 0,
         'false cochain controls escaped')
    need(mul((1, 0, 0), (0, 1, 0)) != mul((0, 1, 0), (1, 0, 0)),
         'central extension confused with split abelian product')
    print(json.dumps({
        'status': 'PASS_FINITE_ALGEBRA_ONLY', 'group_elements': 27,
        'matrix_cup_quotient_pairs': pair_count, 'associativity_triples': 19683,
        'center_and_commutator_size': len(center), 'H1_dimension': 2,
        'wrong_sign_cochain_rejected_pairs': wrong_sign_failures,
        'zero_primitive_rejected_pairs': zero_primitive_failures,
        'noncommutative_extension_guard': True,
        'topological_duality_and_classifying_map_are_separate_deductions': True,
        'genus_equality_or_published_final_theorem_not_certified': True
    }, sort_keys=True, indent=2))


if __name__ == '__main__':
    main()
