#!/usr/bin/env python3
"""Exact finite checks for the Dickson frontier and exponent-cover argument."""
import itertools,json
from pathlib import Path


def leq(a,b):
    return a[0]<=b[0] and a[1]<=b[1]


def frontier(s):
    return {a for a in s if not any(b!=a and leq(b,a) for b in s)}


def check_all_subsets():
    grid=list(itertools.product(range(4),repeat=2))
    for mask in range(1<<len(grid)):
        s={a for j,a in enumerate(grid) if mask>>j&1}
        f=frontier(s)
        assert all(any(leq(b,a) for b in f) for a in s)
        assert not any(a!=b and leq(a,b) for a in f for b in f)
        assert {a for a in grid if any(leq(b,a) for b in s)} == \
               {a for a in grid if any(leq(b,a) for b in f)}
    return 1<<len(grid)


if __name__=='__main__':
    total=check_all_subsets()
    exponent_checks=[]
    for e in range(1,65):
        n=2*e-1
        assert all(i>=e or n-i>=e for i in range(n+1))
        lower=2*e-2
        i=e-1
        assert i<e and lower-i<e
        exponent_checks.append({'e':e,'sufficient_n':n,'lower_diagonal_witness':[i,lower-i]})
    data={'scope':'Finite combinatorial tests; the infinite statements require the written proof.',
          'grid':[4,4],'subsets_checked':total,'exponent_cover_checks':exponent_checks,
          'passed':True}
    Path(__file__).with_name('power_commutator_frontier_results.json').write_text(json.dumps(data,indent=2)+'\n')
    print(json.dumps({'frontier_subsets':total,'exponent_checks':len(exponent_checks),'passed':True}))
