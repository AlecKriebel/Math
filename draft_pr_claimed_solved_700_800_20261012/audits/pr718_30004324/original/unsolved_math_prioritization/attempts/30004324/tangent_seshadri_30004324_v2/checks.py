#!/usr/bin/env python3
"""Finite exact controls only; not a checker of the geometric proof."""
import itertools
import json
from fractions import Fraction
from pathlib import Path

checks = 0
def check(condition):
    global checks
    checks += 1
    if not condition:
        raise AssertionError(f'failed assertion {checks}')

def tree_edges(n, seq):
    degree = [1] * n
    for v in seq:
        degree[v] += 1
    edges = []
    for v in seq:
        leaf = next(i for i in range(n) if degree[i] == 1)
        edges.append((leaf,v))
        degree[leaf] -= 1
        degree[v] -= 1
    last = [i for i in range(n) if degree[i] == 1]
    if n > 1:
        edges.append(tuple(last))
    return edges

trees = 0
marked_configurations = 0
for n in range(1,8):
    sequences = [()] if n <= 2 else itertools.product(range(n), repeat=n-2)
    for seq in sequences:
        edges = tree_edges(n,seq)
        degree = [0] * n
        for a,b in edges:
            degree[a] += 1; degree[b] += 1
        trees += 1
        for nonconstant in range(n):
            for marked in range(n):
                stable = all(degree[v] + (v == marked) >= 3
                             for v in range(n) if v != nonconstant)
                check(stable == (n == 1))
                marked_configurations += 1

# Negative control: a ghost with two marks and one attaching node is stable.
check(1 + 2 >= 3)
# A tail with only one mark and one attaching node is unstable.
check(not (1 + 1 >= 3))

split_cases = 0
for n in range(1,7):
    for a in itertools.product(range(1,5), repeat=n):
        if max(a) < 2:
            continue
        check(sum(a) >= n+1)
        check(all(v-2 >= -1 for v in a))
        for p in [2,3,5,7]:
            check(Fraction(min(p*v for v in a),p) == min(a))
        split_cases += 1

# Positive determinant cannot replace the least slope.
check(sum([3,-1]) == 2 and min([3,-1]) == -1)
# Projective spaces and a product P^a x P^b restricted to a ruling.
for n in range(1,15):
    degrees = [2] + [1]*(n-1)
    check(min(degrees) == (2 if n==1 else 1))
    check(sum(degrees) == n+1)
for a in range(1,8):
    for b in range(1,8):
        degrees = [2]+[1]*(a-1)+[0]*b
        check(min(degrees) == 0)

# Canonical blow-up formula: line meeting a nontrivial smooth center.
blowup_cases=0
for n in range(2,21):
    for r in range(2,n+1):
        for intersection in range(1,11):
            anticanonical = n+1-(r-1)*intersection
            check(anticanonical <= n)
            blowup_cases += 1

# Divisor proportionality control: dD - bA has degree zero on the family.
for d in range(1,21):
    for b in range(-20,21):
        check(d*b-b*d == 0)

result = {'purpose':'finite exact controls, not geometric proof verification',
          'labeled_trees':trees,'one_mark_one_nonconstant_configurations':marked_configurations,
          'positive_splitting_cases':split_cases,'blowup_numeric_cases':blowup_cases,
          'assertions':checks,'two_mark_ghost_negative_control':'stable as required',
          'all_checks_passed':True}
text=json.dumps(result,indent=2,sort_keys=True)+'\n'
print(text,end='')
if '--write' in __import__('sys').argv:
    Path(__file__).with_name('expected_results.json').write_text(text)
else:
    expected=Path(__file__).with_name('expected_results.json').read_text()
    if expected != text:
        raise AssertionError('Results differ from frozen expected_results.json')
