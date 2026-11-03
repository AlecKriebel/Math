#!/usr/bin/env python3
"""Exact finite sanity checks. Not a proof of the continuum assertion."""
from itertools import combinations
from fractions import Fraction
import json

def sumset(A,B=None):
    if B is None: B=A
    return {a+b for a in A for b in B}
def sumfree(S): return not (S & sumset(S))
def witness(S,A): return not (S&A or S&sumset(A))
def powerset(U):
    for mask in range(1<<len(U)):
        yield {x for i,x in enumerate(U) if mask>>i&1}

counts={'sumfree_sets':0,'diagonal_dilate_instances':0,'reflection_cores':0}
for S in powerset(list(range(-6,7))):
    if not sumfree(S): continue
    counts['sumfree_sets']+=1
    for s in S:
        assert any(k*s not in S and 2*k*s not in S for k in (2,3,5))
        counts['diagonal_dilate_instances']+=1
        C={x for x in S if 2*s-x in S}
        A={x-s for x in C}
        assert witness(S,A)
        counts['reflection_cores']+=1

# Three attractive formulas fail, for different reasons.
S={1,4}; A={2*s for s in S}
assert sumfree(S) and not witness(S,A)
S={1,5,8}; A={x-y for x in S for y in S}
assert sumfree(S) and not (S&A) and 8 in S&sumset(A)
S={1,3,5}; anchor=1; A={Fraction(x)-Fraction(anchor,2) for x in S if x!=anchor}
assert sumfree(S) and not (S&A) and 5 in sumset(A)

# Every graph on 5 designated vertices is realizable by a sumfree S.
n=5; M=10*3**n; V=[M+3**i for i in range(n)]
edges=list(combinations(range(n),2))
for mask in range(1<<len(edges)):
    E={edge for i,edge in enumerate(edges) if mask>>i&1}
    S={V[i]+V[j] for i,j in E}
    assert sumfree(S)
    assert all(x not in S and 2*x not in S for x in V)
    assert {(i,j) for i,j in edges if V[i]+V[j] in S}==E

# Finite coefficient model of B+B: base 5 avoids all coefficient collisions.
n=8; M=10*5**n; B={M+5**i for i in range(n)}; S=sumset(B)
assert sumfree(S)
cores={a:len({x for x in S if 2*a-x in S}) for a in S}
assert max(cores.values())==3
b,bp=sorted(B)[:2]; d=b-bp
fiber=S&{x+d for x in S}
assert len(fiber)>=n
result={'scope':'finite exact checks only; not a continuum theorem',
        'exhaustive_interval':[-6,6], 'counts':counts,
        'graphs_realized':1<<len(edges), 'graph_vertex_count':5,
        'naive_formula_counterexamples_verified':3,
        'sumset_model':{'base_points':n,'sumset_size':len(S),
                        'max_reflection_core':max(cores.values()),
                        'selected_difference_fiber':len(fiber)}, 'all_passed':True}
print(json.dumps(result,indent=2))
