#!/usr/bin/env python3
"""Fresh finite checks of profile boundaries, modular shifts, and common monoids.
These are finite controls, not a proof of the imported theorem or a general solver.
"""
from collections import deque
from itertools import product
import json

checks = 0

def need(condition, label):
    global checks
    checks += 1
    if not condition:
        raise RuntimeError(label)

def words(n):
    return [''.join(x) for x in product('01', repeat=n)]

def profiles(w, k):
    left = k // 2
    right = k - left
    return {(w[max(0, i-left):i], w[i:min(len(w), i+right)])
            for i in range(len(w))}

def factors(w, n):
    return {w[i:i+n] for i in range(len(w)-n+1)}

def decomposed_profiles(w, k):
    left, right = k//2, k-k//2
    result = {(v[:left], v[left:]) for v in factors(w, k)}
    result.update((w[:i], w[i:i+right]) for i in range(left))
    result.update((w[-t-left:-t], w[-t:]) for t in range(1, right))
    return result

def advance(graph, states, w):
    for a in w:
        states = {t for q in states for letter, t in graph[q] if letter == a}
    return frozenset(states)

def allowed(graph, w):
    return bool(advance(graph, set(graph), w))

def join(graph, first, last):
    initial = advance(graph, set(graph), first)
    queue = deque([(initial, '')])
    seen = {initial}
    while queue:
        state, c = queue.popleft()
        if advance(graph, state, last):
            return first + c + last
        for letter in '01':
            nxt = advance(graph, state, letter)
            if nxt and nxt not in seen:
                seen.add(nxt)
                queue.append((nxt, c + letter))
    raise RuntimeError('connector missing')

def approximation(graph, n):
    allowed_n = [w for w in words(n) if allowed(graph, w)]
    vertices = {w[:-1] for w in allowed_n} | {w[1:] for w in allowed_n}
    return {v: [(w[-1], w[1:]) for w in allowed_n if w[:-1] == v]
            for v in vertices}

def main():
    profile_cases = 0
    for k in range(1, 6):
        for length in range(2*k, 12):
            for w in words(length):
                need(profiles(w, k) == decomposed_profiles(w, k), 'profile boundary formula')
                profile_cases += 1
    need(factors('0010', 2) == factors('1001', 2), 'factor-only countercontrol premise')
    need(profiles('0010', 2) != profiles('1001', 2), 'factor-only countercontrol conclusion')
    need(profiles('', 4) == set(), 'empty word has no letter positions')

    saturation_cases = 0
    maximum_padded_length = 0
    short = sum((words(i) for i in range(7)), [])
    for modulus in range(2, 6):
        g = {i: [('1', (i+1) % modulus)] for i in range(modulus)}
        g[0].append(('0', 0))
        for n in range(2, 8):
            h = approximation(g, n)
            for w in short:
                expected = (allowed(g, w) if len(w) < n else
                            all(allowed(g, v) for v in factors(w, n)))
                need(allowed(h, w) == expected, 'actual language includes short-word condition')
            bad_exponent = n
            while bad_exponent % modulus == 0:
                bad_exponent += 1
            bad = '0' + '1' * bad_exponent + '0'
            need(not allowed(g, bad), 'modular forbidden word')
            need(allowed(h, bad), 'forbidden word appears in canonical approximation')
            U = ''
            nwords = {w for w in words(n) if allowed(g, w)}
            for w in sorted(nwords):
                U = join(g, U, w)
            while len(U) < 2*n:
                U = join(g, U, U)
            V = join(g, U, U)
            W = join(h, join(h, U, bad), U)
            need(allowed(g, V), 'padded good word')
            need(allowed(h, W), 'padded bad word in approximation')
            need(not allowed(g, W), 'two-sided bad ideal')
            need(factors(V, n) == nwords == factors(W, n), 'saturated factor sets')
            for k in range(1, n+1):
                need(profiles(V, k) == profiles(W, k), 'exact published profile collision')
            saturation_cases += 1
            maximum_padded_length = max(maximum_padded_length, len(V), len(W))

    singleton = {0: [('0', 0)]}
    for n in range(2, 6):
        h = approximation(singleton, n)
        need(not allowed(h, '1'), 'unused alphabet letter not vacuously admitted')
        need(allowed(h, ''), 'empty word admitted by nonempty approximation')
    # A reducible presentation can present an irreducible shift: all zero points.
    redundant = {0: [('0', 0), ('0', 1)], 1: [('0', 1)]}
    for w in short:
        need(allowed(redundant, w) == allowed(singleton, w), 'presentation need not be strongly connected')

    # Language of the even shift, states both vertices, even, odd, empty.
    delta = [(1, 0), (1, 2), (3, 1), (3, 3)]
    letters = [tuple(delta[q][a] for q in range(4)) +
               tuple(4 + delta[q][a] for q in range(4)) for a in range(2)]
    identity = tuple(range(8))
    monoid = {identity}
    queue = [identity]
    for transformation in queue:
        for generator in letters:
            new = tuple(generator[transformation[q]] for q in range(8))
            if new not in monoid:
                monoid.add(new)
                queue.append(new)
    for x in monoid:
        for y in monoid:
            need(tuple(y[x[q]] for q in range(8)) in monoid, 'transformation monoid closed')
    for w in short:
        trans = identity
        for a in w:
            trans = tuple(letters[int(a)][trans[q]] for q in range(8))
        good = trans[0] != 3
        bad = trans[4] == 7
        need(good == allowed({0: [('0', 0), ('1', 1)], 1: [('1', 0)]}, w), 'common morphism recognizes L')
        need(bad == (not good), 'same morphism recognizes bad ideal for identity')
    bound = 4 * (len(monoid) + 1)
    exponent = bound if bound % 2 else bound+1
    witness = '0' + '1'*exponent + '0'
    need(not allowed({0: [('0', 0), ('1', 1)], 1: [('1', 0)]}, witness), 'bound-order negative witness')
    need(all(allowed({0: [('0', 0), ('1', 1)], 1: [('1', 0)]}, v)
             for v in factors(witness, bound)), 'all bound-length factors allowed')
    print(json.dumps({'checks': checks, 'profile_formula_cases': profile_cases,
                      'modular_saturation_cases': saturation_cases,
                      'maximum_padded_length': maximum_padded_length,
                      'even_identity_common_monoid_size': len(monoid),
                      'even_identity_PRZ_bound': bound,
                      'even_identity_bound_witness_length': len(witness),
                      'scope': 'finite controls only', 'status': 'PASS'}, sort_keys=True, indent=2))

if __name__ == '__main__':
    main()
