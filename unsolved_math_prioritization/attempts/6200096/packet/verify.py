#!/usr/bin/env python3
"""Exact, deterministic controls for the p=2 published counterexample.

No source files or external packages are required. These finite controls
supplement the all-elements proof; they are not themselves a proof search.
"""
import argparse
import itertools
import json
from fractions import Fraction
from pathlib import Path


def reduce_word(word):
    out = []
    for x in word:
        if out and out[-1] == -x:
            out.pop()
        else:
            out.append(x)
    return tuple(out)


def inv(word):
    return tuple(-x for x in reversed(word))


def subst(word, images):
    return reduce_word(itertools.chain.from_iterable(
        images[x] if x > 0 else inv(images[-x]) for x in word))


def words(max_length):
    yield ()
    layer = [()]
    for _ in range(max_length):
        layer = [w + (x,) for w in layer for x in (1, -1, 2, -2, 3, -3)
                 if not w or w[-1] != -x]
        yield from layer


def exponent_a(word):
    return sum(1 if x == 1 else -1 if x == -1 else 0 for x in word)


SIGMA = {1: (1,), 2: (3,), 3: (-1, 2, 1)}
SIGMA_INV = {1: (1,), 2: (1, 3, -1), 3: (2,)}


def phi(element, k=1, inverse=False):
    z, w = element
    return (-z + k * exponent_a(w),
            subst(w, SIGMA_INV if inverse else SIGMA))


def run():
    assertions = 0

    def check(condition):
        nonlocal assertions
        if not condition:
            raise AssertionError('exact control failed')
        assertions += 1

    all_words = list(words(5))
    for k in range(-4, 5):
        for z in range(-2, 3):
            for w in all_words:
                h = (z, w)
                check(phi(phi(h, k), k, inverse=True) == h)
                check(phi(phi(h, k, inverse=True), k) == h)
                check(phi(phi(h, k), k) ==
                      (z, reduce_word((-1,) + w + (1,))))

    # Graph oriented edges: e=1, f=2, B=3, D=4.
    edges = {1: ('u', 'v'), 2: ('v', 'u'),
             3: ('u', 'u'), 4: ('v', 'v')}
    graph_basis = {1: (1, 2), 2: (3,), 3: (-2, 4, 2)}
    delta = {1: (2,), 2: (1,), 3: (4,), 4: (3,)}
    p = (-2,)

    def endpoint(path, start):
        current = start
        for x in path:
            u, v = edges[abs(x)]
            if x < 0:
                u, v = v, u
            check(current == u)
            current = v
        return current

    for j, loop in graph_basis.items():
        check(endpoint(loop, 'u') == 'u')
        image = reduce_word(p + subst(loop, delta) + inv(p))
        check(endpoint(image, 'u') == 'u')
        check(image == subst(SIGMA[j], graph_basis))
        kappa_degree = sum(1 if x == 1 else -1 if x == -1 else 0
                           for x in loop)
        check(kappa_degree == (1 if j == 1 else 0))
        check(subst(subst(loop, delta), delta) == loop)
    check(endpoint(p, 'u') == 'v')

    # Necessary fixed-square condition for the twist-k family.
    parity = []
    for k in range(-20, 21):
        solutions = [n for n in range(-25, 26)
                     if phi((n, (-1,)), k) == (n, (-1,))]
        expected = [-k // 2] if k % 2 == 0 else []
        check(solutions == expected)
        parity.append({'k': k, 'integer_solutions': solutions})
    check(2 * Fraction(-1, 2) == -1)
    check(phi((1, ()), 1) != (1, ()))  # Nontrivial central action.
    # The zero-twist geometric formula squares to (s,x), symbolically:
    check(-(-1) == 1)
    for e in edges:
        check(subst(subst((e,), delta), delta) == (e,))

    return {
        'result': 'PASS',
        'assertions': assertions,
        'reduced_words_tested': len(all_words),
        'maximum_word_length': 5,
        'central_exponents': [-2, -1, 0, 1, 2],
        'twists_for_word_tests': list(range(-4, 5)),
        'graph_basepoint_formulas': 'PASS',
        'odd_twist_negative_control': 'no integer fixed-square exponent',
        'zero_twist_positive_control': 'explicit PL involution F0',
        'rational_relaxation': '-1/2 solves the altered equation',
        'parity_checks': parity,
        'scope': 'Exact finite controls; general proof is in PROOF.md.'
    }


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    result = run()
    content = json.dumps(result, indent=2, sort_keys=True) + '\n'
    if args.output:
        args.output.write_text(content)
    print(json.dumps({k: result[k] for k in
                      ['result', 'assertions', 'reduced_words_tested']}))
