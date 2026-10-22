#!/usr/bin/env python3
"""Exact finite controls; the infinite theorem is the written proof plus PRZ 4.2.
Run with python3 -I -B verify_math.py. No local imports or third-party modules.
"""
import itertools
import json
from collections import deque

COUNT = 0

def check(condition, message):
    global COUNT
    COUNT += 1
    if not condition:
        raise RuntimeError(message)

A = ('0', '1')
E = {0: {'0': {0}, '1': {1}}, 1: {'1': {0}}}
G = {0: {'0': {0}, '1': {1}}, 1: {'0': {0}}}
FULL = {0: {'0': {0}, '1': {0}}}

def step(graph, states, a):
    return frozenset(t for s in states for t in graph[s].get(a, ()))

def accepts(graph, word):
    states = frozenset(graph)
    for a in word:
        states = step(graph, states, a)
    return bool(states)

def words(n):
    return (''.join(t) for t in itertools.product(A, repeat=n))

def factors(word, n):
    return {word[i:i+n] for i in range(len(word)-n+1)}

def approximation(graph, n):
    allowed = [w for w in words(n) if accepts(graph, w)]
    vertices = sorted({w[:-1] for w in allowed} | {w[1:] for w in allowed})
    out = {v: {} for v in vertices}
    for w in allowed:
        out[w[:-1]].setdefault(w[-1], set()).add(w[1:])
    return out

def connected(graph):
    for start in graph:
        seen, todo = {start}, [start]
        for v in todo:
            for successors in graph[v].values():
                for t in successors:
                    if t not in seen:
                        seen.add(t); todo.append(t)
        if seen != set(graph):
            return False
    return True

def image_word(word, ell, rule):
    return ''.join(rule(word[i:i+ell]) for i in range(len(word)-ell+1))

def bad_witness(domain, target, ell, rule):
    """Finite reachability: exists ANY finite domain word with bad output?
    All domain vertices must lie on bi-infinite paths, as all examples do.
    Return shortest witness, or None when the whole regular intersection is empty.
    """
    initial = [(v, '', frozenset(target)) for v in domain]
    todo = deque(initial)
    previous = {s: None for s in initial}
    while todo:
        state = todo.popleft()
        vertex, buffer, output_states = state
        for a in A:
            for nxt in sorted(domain[vertex].get(a, ())):
                full_buffer = buffer + a
                if len(full_buffer) == ell:
                    out = step(target, output_states, rule(full_buffer))
                    new_buffer = full_buffer[1:]
                else:
                    out, new_buffer = output_states, full_buffer
                new = (nxt, new_buffer, out)
                if new not in previous:
                    previous[new] = (state, a)
                    if not out:
                        letters = []
                        z = new
                        while previous[z] is not None:
                            z, label = previous[z]
                            letters.append(label)
                        return ''.join(reversed(letters))
                    todo.append(new)
    return None

def join(graph, left, right):
    # Finite BFS for a connector. Tested graphs are irreducible.
    initial = frozenset(graph)
    for a in left:
        initial = step(graph, initial, a)
    check(bool(initial), 'left word is allowed')
    todo = deque([(initial, '')]); seen = {initial}
    while todo:
        states, middle = todo.popleft()
        final = states
        for a in right:
            final = step(graph, final, a)
        if final:
            result = left + middle + right
            check(accepts(graph, result), 'connector membership')
            return result
        for a in A:
            nxt = step(graph, states, a)
            if nxt and nxt not in seen:
                seen.add(nxt); todo.append((nxt, middle+a))
    raise RuntimeError('no connector in purported irreducible graph')

def profiles(word, k):
    left = k // 2; right = k-left
    return {(word[max(0,i-left):i], word[i:min(len(word),i+right)])
            for i in range(len(word))}

def complete_dfa(graph):
    initial = frozenset(graph)
    order, index = [initial], {initial: 0}
    transitions = []
    for state in order:
        row = []
        for a in A:
            nxt = step(graph, state, a)
            if nxt not in index:
                index[nxt] = len(order); order.append(nxt)
            row.append(index[nxt])
        transitions.append(row)
    return order, transitions

def monoid_size(transitions):
    size = len(transitions)
    identity = tuple(range(size))
    generators = [tuple(row[i] for row in transitions) for i in range(len(A))]
    seen, order = {identity}, [identity]
    for t in order:
        for g in generators:
            nxt = tuple(g[t[i]] for i in range(size))
            if nxt not in seen:
                seen.add(nxt); order.append(nxt)
    return len(seen)

def main():
    reports = {}
    for graph in [E, G, FULL]:
        check(connected(graph), 'test graph strongly connected')
    for n in range(2, 9):
        approx = approximation(E, n)
        check(connected(approx), 'canonical graph strongly connected')
        for w in words(n):
            check(accepts(approx,w) == accepts(E,w), 'exact n-block language')
        identity_bad = bad_witness(approx, E, 1, lambda x:x)
        check(identity_bad is not None, 'even-shift identity negative')
        check(accepts(approx, identity_bad), 'witness domain membership')
        check(not accepts(E, identity_bad), 'witness output nonmembership')
        check(len(identity_bad) > n, 'no false bounded obstruction')
        const_bad = bad_witness(approx, E, 1, lambda x:'0')
        check(const_bad is None, 'constant map extends but is not onto E')
        check(bad_witness(approximation(G,n), G, 1, lambda x:x) is None,
              'golden-mean identity positive at all n>=2')
        m = n if n % 2 else n+1
        obstruction = '0' + '1'*m + '0'
        check(not accepts(E, obstruction), 'odd gap forbidden')
        check(accepts(approx, obstruction), 'long forbidden gap locally admissible')
        for r in range(1, len(obstruction)):
            for v in factors(obstruction,r):
                check(accepts(E,v), 'all proper obstruction factors allowed')
        universal = ''
        for w in words(n):
            if accepts(E,w):
                universal = join(E, universal, w)
        while len(universal) < 2*n:
            universal = join(E, universal, universal)
        W = join(approx, join(approx, universal, obstruction), universal)
        V = join(E, universal, universal)
        check(accepts(approx,W) and not accepts(E,W), 'padded bad word')
        check(accepts(E,V), 'padded good word')
        check(factors(V,n)==factors(W,n), 'saturated n-factor sets')
        check(V[:n-1]==W[:n-1] and V[-n+1:]==W[-n+1:], 'equal boundaries')
        check(profiles(V,n)==profiles(W,n), 'published profile equivalence')
        reports[str(n)] = {'shortest_identity_obstruction':identity_bad,
            'universal_length':len(universal),'good_length':len(V),
            'bad_length':len(W),'profile_count':len(profiles(V,n))}
    # Every one of the 256 binary width-three local rules: exact product
    # reachability versus brute-force words through length ten, in three domains.
    rules_checked = 0
    brute_words = [w for n in range(11) for w in words(n)]
    for bit_table in itertools.product(A, repeat=8):
        table = dict(zip(words(3),bit_table))
        rule = table.__getitem__
        for domain in [FULL,E,approximation(E,3)]:
            witness = bad_witness(domain,E,3,rule)
            brute_bad = next((w for w in brute_words if accepts(domain,w)
                and not accepts(E,image_word(w,3,rule))), None)
            if witness is None:
                check(brute_bad is None,'exact emptiness implies bounded emptiness')
            else:
                check(accepts(domain,witness),'rule witness domain')
                check(not accepts(E,image_word(witness,3,rule)),'rule witness bad')
                if len(witness)<=10:
                    check(brute_bad is not None,'bounded witness found')
            rules_checked += 1
    # Independent DFA/transition-monoid construction for the identity controls.
    monoids = {}
    for name, graph in [('full',FULL),('golden_mean',G),('even',E)]:
        states, transitions = complete_dfa(graph)
        monoids[name]={'reachable_dfa_states':len(states),
                      'monoid_size':monoid_size(transitions)}
        monoids[name]['PRZ_k']=4*(monoids[name]['monoid_size']+1)
    # For identity, B is the complement of L(T), so the same DFA/monoid
    # recognizes both. The full shift is explicitly tested at its universal k.
    full_k = monoids['full']['PRZ_k']
    check(bad_witness(approximation(FULL,full_k),FULL,1,lambda x:x) is None,
          'full-shift exact finite criterion at PRZ bound')
    result={'status':'PASS','checks':COUNT,'local_rule_domain_cases':rules_checked,
        'canonical_even_shift_controls':reports,'identity_monoids':monoids,
        'scope':'Exact finite automata checks and bounded control families; not a proof of the infinite theorem or PRZ theorem.'}
    print(json.dumps(result,sort_keys=True,indent=2))

if __name__ == '__main__':
    main()
