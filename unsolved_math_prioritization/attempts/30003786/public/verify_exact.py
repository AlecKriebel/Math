#!/usr/bin/env python3
"""Dependency-free bounded exact controls for the written, all-moduli proof.

Run: python3 verify_exact.py > verify_exact_results.json
The search range is a diagnostic, not a substitute for the general theorem.
"""
from collections import deque
from math import gcd
import json

I = (1, 0, 0, 1)
A = (1, 2, 0, 1)
B = (1, 0, 2, 1)
checks = 0


def check(condition):
    global checks
    checks += 1
    if not condition:
        raise AssertionError(f"Exact assertion {checks} failed")


def mul(x, y, modulus=None):
    a, b, c, d = x
    e, f, g, h = y
    out = (a*e+b*g, a*f+b*h, c*e+d*g, c*f+d*h)
    return tuple(z % modulus for z in out) if modulus is not None else out


def inv(x, modulus=None):
    a, b, c, d = x
    out = (d, -b, -c, a)
    return tuple(z % modulus for z in out) if modulus is not None else out


def power(x, r, modulus=None):
    if r < 0:
        x, r = inv(x, modulus), -r
    ans = tuple(z % modulus for z in I) if modulus is not None else I
    while r:
        if r & 1:
            ans = mul(ans, x, modulus)
        x = mul(x, x, modulus)
        r //= 2
    return ans


def U(t):
    return (1, t, 0, 1)


def L(t):
    return (1, 0, t, 1)


def evaluate(word, modulus=None):
    gens = {'a': A, 'b': B, 'A': inv(A), 'B': inv(B)}
    ans = tuple(z % modulus for z in I) if modulus is not None else I
    for letter in word:
        ans = mul(ans, gens[letter], modulus)
    return ans


def inverse_word(word):
    return ''.join(c.swapcase() for c in word[::-1])


def chi(word):
    return (word.count('a')-word.count('A')) % 5


def witness(modulus):
    """Find a conflicting C5 label on the Cayley graph of the matrix image."""
    identity = tuple(z % modulus for z in I)
    paths = {identity: ('', 0)}
    queue = deque([identity])
    while queue:
        x = queue.popleft()
        word, value = paths[x]
        for letter, generator, delta in [('a', A, 1), ('b', B, 0)]:
            y = mul(x, generator, modulus)
            new_word, new_value = word+letter, (value+delta) % 5
            if y not in paths:
                paths[y] = (new_word, new_value)
                queue.append(y)
            elif paths[y][1] != new_value:
                w = new_word + inverse_word(paths[y][0])
                check(evaluate(w, modulus) == identity)
                check(chi(w) != 0)
                integer_matrix = evaluate(w)
                check(integer_matrix[0]*integer_matrix[3]-integer_matrix[1]*integer_matrix[2] == 1)
                check(all((z-i) % modulus == 0 for z, i in zip(integer_matrix, I)))
                return {'modulus': modulus, 'word': w, 'chi': chi(w),
                        'length': len(w), 'visited_vertices': len(paths)}
    raise AssertionError(f"No character conflict at modulus {modulus}")


def group_generated(generators, modulus):
    identity = tuple(z % modulus for z in I)
    seen = {identity}
    queue = deque([identity])
    while queue:
        x = queue.popleft()
        for g in generators:
            y = mul(x, g, modulus)
            if y not in seen:
                seen.add(y)
                queue.append(y)
    return seen


def sl2_order(n):
    value, p = 1, 2
    while p*p <= n:
        if n % p == 0:
            e = 0
            while n % p == 0:
                e += 1
                n //= p
            value *= p**(3*e-2)*(p*p-1)
        p += 1
    if n > 1:
        value *= n*(n*n-1)
    return value


# Exact identities supporting the ring argument, including composite moduli.
for n in range(3, 102, 2):
    D = (2, 0, 0, pow(2, -1, n))
    J = (0, -1, 1, 0)
    check(mul(mul(D, U(1), n), inv(D, n), n) == tuple(z % n for z in U(4)))
    check(mul(mul(J, U(-1), n), inv(J, n), n) == tuple(z % n for z in L(1)))
    for u in range(1, n):
        if gcd(u, n) == 1:
            ui = pow(u, -1, n)
            w = mul(mul(U(u), L(-ui), n), U(u), n)
            wm1 = mul(mul(U(-1), L(1), n), U(-1), n)
            check(mul(w, wm1, n) == (u, 0, 0, ui))

# Check the elementary-generated odd factors by exhaustive finite enumeration.
odd_orders = []
for n in range(1, 40, 2):
    actual = len(group_generated([A, B], n))
    expected = sl2_order(n)
    check(actual == expected)
    odd_orders.append({'modulus': n, 'image_order': actual})

# Direct tests of the exact product decomposition at mixed moduli.
mixed_orders = []
for k in range(1, 5):
    two_order = len(group_generated([A, B], 2**k))
    check(two_order > 0 and (two_order & (two_order-1)) == 0)
    for n in [1, 3, 5, 7, 9]:
        m = (2**k)*n
        actual = len(group_generated([A, B], m))
        expected = two_order*sl2_order(n)
        check(actual == expected)
        check(power(A, 2**k, 2**k) == tuple(z % (2**k) for z in I))
        check(power(B, 2**k, 2**k) == tuple(z % (2**k) for z in I))
        mixed_orders.append({'modulus': m, 'two_primary_order': two_order,
                             'odd_modulus': n, 'image_order': actual})

# P is a 5-cycle, has determinant +1, and all powers remain distinct mod 2.
perm = [1, 2, 3, 4, 0]
inversions = sum(perm[i] > perm[j] for i in range(5) for j in range(i+1, 5))
check(inversions % 2 == 0)
permutation_powers = [tuple((i+r) % 5 for i in range(5)) for r in range(5)]
check(len(set(permutation_powers)) == 5)
check(all(permutation_powers[r] != tuple(range(5)) for r in range(1, 5)))

# Exercise the level-2 condition on every reduced word through length 7.
words = ['']
frontier = ['']
for length in range(1, 8):
    frontier = [w+c for w in frontier for c in 'abAB' if not w or c != w[-1].swapcase()]
    words.extend(frontier)
for w in words:
    check(evaluate(w, 2) == I)
    lower_block_identity = permutation_powers[chi(w)] == tuple(range(5))
    check(lower_block_identity == (chi(w) == 0))
    if w:
        check(evaluate(w) != I)  # bounded ping-pong diagnostic only

witnesses = [witness(m) for m in range(1, 65)]
print(json.dumps({'status': 'PASS', 'arithmetic': 'exact integers and finite residue rings',
                  'assertions': checks, 'reduced_words_checked': len(words),
                  'odd_factor_enumerations': odd_orders,
                  'mixed_factor_enumerations': mixed_orders,
                  'noncongruence_witnesses': witnesses,
                  'scope': 'Bounded diagnostics. The written proof covers every modulus.'},
                 indent=2, sort_keys=True))
