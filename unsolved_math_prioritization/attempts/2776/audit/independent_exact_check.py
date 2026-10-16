#!/usr/bin/env python3
"""Independent source-free finite checks. No import of the report's verifier."""
import itertools
import json
from collections import deque
from fractions import Fraction


def check(value, description):
    if not value:
        raise RuntimeError(description)


def reachable(vertices, edge_set):
    if not vertices:
        return False
    seen = {min(vertices)}
    frontier = list(seen)
    while frontier:
        u = frontier.pop()
        for v in vertices - seen:
            if frozenset((u, v)) in edge_set:
                seen.add(v)
                frontier.append(v)
    return seen == vertices


def closed_connected_dominates(vertices, universe, edges):
    return reachable(vertices, edges) and all(
        any(frozenset((u, v)) in edges for u in vertices)
        for v in universe - vertices)


def all_subsets(vertices, nonempty=False):
    ordered = sorted(vertices)
    for size in range(1 if nonempty else 0, len(ordered)+1):
        for subset in itertools.combinations(ordered, size):
            yield frozenset(subset)


def graph_tests():
    graphs = supports = 0
    for n in range(1, 6):
        universe = frozenset(range(n))
        possible = list(itertools.combinations(range(n), 2))
        subsets = list(all_subsets(universe, nonempty=True))
        for mask in range(1 << len(possible)):
            gamma = {frozenset(pair) for i, pair in enumerate(possible)
                     if mask & (1 << i)}
            opposite = {frozenset(pair) for pair in possible} - gamma
            # Enumerate induced candidate joins and their bipartitions directly.
            joins = []
            for candidate in subsets:
                anchor = min(candidate)
                for left in all_subsets(candidate, nonempty=True):
                    right = candidate - left
                    if anchor in left and right and all(
                            frozenset((u, v)) in gamma for u in left for v in right):
                        joins.append(candidate)
                        break
            for support in subsets:
                contained = any(support <= candidate for candidate in joins)
                criterion = closed_connected_dominates(support, universe, opposite)
                check(criterion != contained, 'Join/CDS mismatch')
                supports += 1
            graphs += 1
    check((graphs, supports) == (1099, 32767), 'Graph totals')
    return {'graphs': graphs, 'supports': supports, 'mismatches': 0}


def cycle_tests():
    count = 0
    for n in range(5, 21):
        vertices = frozenset(range(n))
        cycle = {frozenset((i, (i+1) % n)) for i in vertices}
        support = vertices - {1, 2}
        check(closed_connected_dominates(support, vertices, cycle), 'Cycle source')
        for length in range(n, 4*n+1):
            path = {frozenset((i, i+1)) for i in range(length-1)}
            lift = frozenset(i for i in range(length) if i % n in support)
            check({0, 3} <= lift, 'Cycle endpoint witnesses')
            check(not reachable(lift, path), 'Cycle lift remains disconnected')
            count += 1
    check(count == 616, 'Cycle count')
    vertices = frozenset(range(5))
    cycle = {frozenset((i, (i+1) % 5)) for i in vertices}
    dominating = [s for s in all_subsets(vertices, True)
                  if closed_connected_dominates(s, vertices, cycle)]
    minimal = [s for s in dominating if not any(t < s for t in dominating)]
    cliques = [s for s in all_subsets(vertices, True)
               if all(frozenset(pair) in cycle for pair in itertools.combinations(s, 2))]
    check(len(minimal) == 5 and all(len(s) == 3 for s in minimal), 'C5 minimal family')
    check(len(cliques) == 10, 'C5 cliques')
    check(all(any(not (s & clique) for s in minimal) for clique in cliques), 'C5 avoidance')
    return {'cycle_cover_cases': count, 'c5_minimal_sets': sorted(sorted(s) for s in minimal),
            'c5_nonempty_cliques': len(cliques), 'c5_clique_transversals': 0}


COMMUTING = {frozenset((1, 2)), frozenset((2, 3)), frozenset((3, 4))}


def commute(a, b):
    return abs(a) == abs(b) or frozenset((abs(a), abs(b))) in COMMUTING


def inverse(word):
    return tuple(-x for x in word[::-1])


def commutator(x, y):
    return tuple(x) + tuple(y) + inverse(x) + inverse(y)


def reduce_word(word):
    """Append letters, cancel through a suffix of commuting letters only."""
    reduced = []
    for letter in word:
        cancelled = False
        for j in range(len(reduced)-1, -1, -1):
            old = reduced[j]
            if abs(old) == abs(letter):
                if old == -letter:
                    del reduced[j]
                    cancelled = True
                break
            if not commute(old, letter):
                break
        if not cancelled:
            reduced.append(letter)
    return tuple(reduced)


def word_tests():
    w = commutator(commutator((1,), (3,)), commutator((2,), (4,)))
    z = (-1,4,-2,-4,1,-3,-1,4,2,-4,1,3)
    q = (2,1,3)
    check(reduce_word(inverse(q) + w + q + inverse(z)) == (), 'Explicit conjugator q=b a c')
    check(len(reduce_word(z)) == 12, 'Reduced length')
    blocked = 0
    for i, x in enumerate(z):
        for offset in range(1, len(z)):
            if z[(i+offset) % len(z)] == -x:
                arc = [z[(i+k) % len(z)] for k in range(1, offset)]
                check(any(not commute(x, y) for y in arc), 'Circular inverse pair has blocker')
                blocked += 1
    check(blocked == 20, 'Circular blocker count')
    check(set(map(abs, z)) == {1,2,3,4}, 'Full P4 support')
    # Independent enumeration supplements the explicit conjugacy certificate.
    visited = {w}
    pending = deque([w])
    while pending:
        item = pending.popleft()
        neighbors = [item[1:] + item[:1]] if item else []
        for i, (x, y) in enumerate(zip(item, item[1:])):
            if x == -y:
                neighbors.append(item[:i] + item[i+2:])
            elif abs(x) != abs(y) and commute(x, y):
                neighbors.append(item[:i] + (y, x) + item[i+2:])
        for nxt in neighbors:
            if nxt not in visited:
                visited.add(nxt)
                pending.append(nxt)
    check(z in visited and min(map(len, visited)) == 12, 'Cyclic search witness')
    check(len(visited) == 2308, 'Cyclic search state count')
    return {'conjugator': 'bac', 'cyclic_representative': 'AdBDaCAdbDac',
            'states': len(visited), 'minimum_cyclic_length': 12, 'blocked_inverse_arcs': blocked}


def multiply(x, y):
    a,b,c,d = x
    e,f,g,h = y
    return (a*e+b*g, a*f+b*h, c*e+d*g, c*f+d*h)


def matrix_inverse(x):
    a,b,c,d = x
    check(a*d-b*c == 1, 'Matrix determinant')
    return (d,-b,-c,a)


def project(x, t):
    a,b,c,d = x
    return (a*t+b)/(c*t+d)


def matrix_tests():
    a = (34,21,21,13)
    inverse_a = matrix_inverse(a)
    plus = (Fraction(3,2), Fraction(7,4))
    minus = (Fraction(-3,4), Fraction(-1,2))
    forward = sorted(project(a,t) for t in minus)
    backward = sorted(project(inverse_a,t) for t in plus)
    check(forward == [Fraction(8,5), Fraction(18,11)], 'Forward rational endpoints')
    check(backward == [Fraction(-7,11), Fraction(-3,5)], 'Inverse rational endpoints')
    check(plus[0] < forward[0] < forward[1] < plus[1], 'Forward strict containment')
    check(minus[0] < backward[0] < backward[1] < minus[1], 'Inverse strict containment')
    check(minus[0] < Fraction(-13,21) < minus[1], 'Forward pole')
    check(plus[0] < Fraction(34,21) < plus[1], 'Inverse pole')
    matrices=[]
    for i in range(3):
        matrices.append(multiply(multiply((1,10*i,0,1), a), (1,-10*i,0,1)))
    matrices += [matrix_inverse(x) for x in matrices]
    count=0
    minimum=None
    for length in range(1,6):
        for labels in itertools.product(range(6), repeat=length):
            if any((x+3)%6 == y for x,y in zip(labels, labels[1:])):
                continue
            if (labels[-1]+3)%6 == labels[0]:
                continue
            product=(1,0,0,1)
            for i in labels:
                product=multiply(product,matrices[i])
            trace=abs(product[0]+product[3])
            check(trace>2,'Sample trace')
            minimum=trace if minimum is None else min(minimum,trace)
            count+=1
    check((count,minimum)==(3918,47),'Matrix sample totals')
    return {'forward_endpoints':list(map(str,forward)), 'inverse_endpoints':list(map(str,backward)),
            'cyclic_words':count, 'minimum_absolute_trace':minimum}


def main():
    result={'graph':graph_tests(), 'cycles':cycle_tests(), 'word':word_tests(),
            'matrices':matrix_tests(), 'all_checks_passed':True,
            'limits':'Finite checks only; universal centralizer, Schottky, cover and support arguments require the written proofs.'}
    print(json.dumps(result,indent=2))


if __name__=='__main__':
    main()
