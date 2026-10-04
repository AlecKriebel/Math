#!/usr/bin/env python3
"""Finite checks for an unsolved Borel-dynamics research packet.

These controls are not a finite proof of any infinite Borel existence assertion.
No input files, downloads, credentials or external packages are used.
"""
from itertools import product, permutations
import json

checks = 0

def check(condition):
    global checks
    assert condition
    checks += 1

# Noncommutative orientation controls using S_3 with composition (a b)(i)=a(b(i)).
G = tuple(permutations(range(3)))
e = tuple(range(3))
index = {g: i for i, g in enumerate(G)}
def mul(a, b):
    return tuple(a[b[i]] for i in range(3))
def shift(g, y):
    return tuple(y[index[mul(d, g)]] for d in G)
def stab(y):
    return {g for g in G if shift(g, y) == y}

words = tuple(product(range(2), repeat=len(G)))
for y in words:
    for g in G:
        moved = any(y[index[d]] != y[index[mul(d, g)]] for d in G)
        check(moved == (shift(g, y) != y))
        for h in G:
            check(shift(g, shift(h, y)) == shift(mul(g, h), y))
            # Coding pi_f for the left-regular source action x -> g*x.
            code_gx = tuple(y[index[mul(d, mul(g, h))]] for d in G)
            code_x = tuple(y[index[mul(d, h)]] for d in G)
            check(code_gx == shift(g, code_x))
            if mul(g, h) == mul(h, g):
                for d in G:
                    # This is precisely the centralizer rearrangement in Lemma 2.
                    check(mul(mul(d, g), h) == mul(mul(d, h), g))

# Product-stabilizer identity and loss under projection.
product_examples = 0
projection_loss_examples = 0
for y in words:
    for z in words:
        pair = tuple(zip(y, z))
        check(stab(pair) == stab(y) & stab(z))
        product_examples += 1
        if stab(z) == {e}:
            check(stab(pair) == {e})
            if stab(y) != {e}:
                projection_loss_examples += 1
check(projection_loss_examples > 0)

# Faithfulness is weaker than pointwise freeness: S_3 acts on its three points.
point_stabs = [{g for g in G if g[i] == i} for i in range(3)]
check(set.intersection(*point_stabs) == {e})
check(all(len(s) == 2 for s in point_stabs))

# The finite language of the monotone SFT consists of zeros followed by ones.
monotone_counts = {}
for n in range(1, 13):
    legal = [w for w in product(range(2), repeat=n)
             if all(w[i:i+2] != (1, 0) for i in range(n-1))]
    predicted = [(0,) * t + (1,) * (n-t) for t in range(n+1)]
    check(set(legal) == set(predicted))
    monotone_counts[str(n)] = len(legal)
    cyclic_legal = [w for w in product(range(2), repeat=n)
                   if all((w[i], w[(i+1) % n]) != (1, 0) for i in range(n))]
    check(cyclic_legal == [(0,) * n, (1,) * n])

# For each sampled finite witness window and nonzero shift, move a single marker
# outside all queried coordinates. The infinite sequence is exactly free.
sparse_tests = 0
for radius in range(26):
    D = set(range(-radius, radius+1))
    for g in range(-10, 11):
        if g == 0:
            continue
        queried = D | {d+g for d in D}
        marker = max(queried) + 1
        y = lambda t: int(t == marker)
        check(all(y(d) == y(d+g) for d in D))
        check(y(marker) != y(marker+g))
        sparse_tests += 1

# Translated interfaces obey the SFT but look fixed on every finite window.
interface_tests = 0
for radius in range(26):
    for sign in [-1, 1]:
        t = sign * (radius+2)
        b = lambda j: int(j >= t)
        check(all(not (b(j) == 1 and b(j+1) == 0)
                  for j in range(-radius-1, radius+2)))
        check(len({b(j) for j in range(-radius, radius+1)}) == 1)
        interface_tests += 1

# Parity-factor obstruction has local relation a(sigma x)=1-a(x), hence
# a(sigma^2 x)=a(x). This checks the elementary algebra, not ergodicity itself.
for a in [0, 1]:
    check(1-(1-a) == a)

print(json.dumps({
    "all_passed": True,
    "assertions": checks,
    "finite_group": "S_3",
    "binary_configurations_on_group": len(words),
    "product_stabilizer_pairs": product_examples,
    "projection_loss_examples": projection_loss_examples,
    "monotone_word_counts": monotone_counts,
    "sparse_witness_tests": sparse_tests,
    "interface_window_tests": interface_tests,
    "scope": "Finite algebra and local-language controls only; infinite and Borel claims require the written proofs."
}, indent=2, sort_keys=True))
