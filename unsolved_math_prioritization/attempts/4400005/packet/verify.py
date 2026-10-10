#!/usr/bin/env python3
"""Exact finite sanity controls; not a proof of the cited embedding theorems."""
import itertools
import json
from fractions import Fraction
from pathlib import Path

checks = 0
def check(v):
    global checks
    assert v
    checks += 1

def square(p):
    return tuple(p[p[i]] for i in range(len(p)))

cycle_rows = []
permutations = 0
for n in range(1, 9):
    target = tuple((i+1) % n for i in range(n))
    roots = []
    for p in itertools.permutations(range(n)):
        permutations += 1
        if square(p) == target:
            roots.append(p)
    check(bool(roots) == bool(n % 2))
    # An n-cycle's centralizer consists of its powers; 2k=1 mod n.
    modular_roots = [k for k in range(n) if (2*k-1) % n == 0]
    check(len(roots) == len(modular_roots))
    cycle_rows.append({'n': n, 'square_roots': len(roots)})

quotient_rows = []
for k in range(1, 13):
    n = 2**k
    f = [(-1)**i for i in range(n)]
    check(all(f[(i+1) % n] == -f[i] for i in range(n)))
    check(not any((2*r-1) % n == 0 for r in range(n)))
    check(len({i % n for i in range(n)}) == n)
    if k > 1:
        check(all(((i+1) % n) % (n//2) == (i % (n//2)+1) % (n//2) for i in range(n)))
    quotient_rows.append({'k':k, 'size':n, 'parity_obstruction':True})

# Ergodicity really matters: two 2-cycles have a square root, a 4-cycle.
pair_flip = (1,0,3,2)
root = (2,3,1,0)
check(square(root) == pair_flip)
check(set(root) == set(range(4)))

# Complex operator square roots exist, so positivity/real preservation matters.
check(1j * 1j == -1)
check(1j not in {-1,1})

# Rational closed orbit of length p/q: exactly p points under time one.
periodic_cases = 0
for p in range(1,16):
    for q in range(1,16):
        ell = Fraction(p,q)
        p0,q0 = ell.numerator,ell.denominator
        support = {Fraction(j) % ell for j in range(p0)}
        check(len(support) == p0)
        check({(s+1) % ell for s in support} == support)
        # Support is {j/q0: 0<=j<p0}; a half grid step moves it disjointly.
        shift = Fraction(1, 2*q0)
        check(not ({(s+shift) % ell for s in support} & support))
        periodic_cases += 1

# A no-root system may have a root-admitting factor: collapse a 2-cycle.
check(square((0,)) == (0,))
check(not any(square(p) == (1,0) for p in itertools.permutations(range(2))))

# Flow averaging does not recover the input measure (finite circle analogue).
for n in (2,3,5,8,16):
    atomic = [Fraction(int(i==0)) for i in range(n)]
    average = [sum(atomic[(i-j) % n] for j in range(n))/n for i in range(n)]
    check(average == [Fraction(1,n)]*n)
    check(average != atomic)

result = {
    'all_passed': True,
    'assertions': checks,
    'permutations_enumerated': permutations,
    'cyclic_root_tests': cycle_rows,
    'dyadic_quotients': quotient_rows,
    'rational_periodic_orbit_cases': periodic_cases,
    'negative_controls': ['two 2-cycles admit a square root', 'complex scalar i squares to -1', 'a trivial factor loses the no-root obstruction', 'averaging need not fix an invariant input'],
    'scope': 'Exact finite algebra and rational circle controls. Infinite ergodic theory and literature theorem application require the written argument and independent review.'
}
text = json.dumps(result, indent=2, sort_keys=True)+'\n'
if __name__ == '__main__':
    print(text, end='')
