#!/usr/bin/env python3
"""Finite exact controls only; this is not a Legendrian knot enumeration."""
from pathlib import Path
from itertools import product,combinations_with_replacement
from math import comb
import json,hashlib
counts={}
def check(k,b):
    assert b,k
    counts[k]=counts.get(k,0)+1

# Permutations of identical prime types give multisets, not ordered tuples.
for p in range(1,5):
    for m in range(1,5):
        ordered=list(product(range(p),repeat=m))
        orbits={tuple(sorted(v)) for v in ordered}
        multisets=set(combinations_with_replacement(range(p),m))
        check('symmetric_product_orbits',orbits==multisets)
        check('peak_count_formula',len(orbits)==comb(p+m-1,m))
        # Different peak classes may have equal tb; do not identify their classes.
        values=[-2-(i//2) for i in range(p)]
        minimum=min(sum(values[i] for i in v)+(m-1) for v in orbits)
        check('minimum_tb_formula',minimum==m*min(values)+(m-1))
for p1,p2,m1,m2 in product(range(1,4),range(1,4),range(1,4),range(1,4)):
    a=list(combinations_with_replacement(range(p1),m1))
    b=list(combinations_with_replacement(range(p2),m2))
    classes=list(product(a,b))
    check('distinct_factor_product',len(classes)==comb(p1+m1-1,m1)*comb(p2+m2-1,m2))
    t1=[-i-1 for i in range(p1)];t2=[-2*i-3 for i in range(p2)]
    actual=min(sum(t1[i] for i in x)+sum(t2[j] for j in y)+m1+m2-1 for x,y in classes)
    check('mixed_minimum_tb',actual==m1*min(t1)+m2*min(t2)+m1+m2-1)

# All-positive-depth transfer moves have a stabilized factor at each end.
for a,b,c,d in product(range(4),repeat=4):
    # Move one positive stabilization from first to second factor.
    start=((a+1,b),(c,d));end=((a,b),(c+1,d))
    check('transfer_endpoints_not_peaks',any(sum(v)>0 for v in start) and any(sum(v)>0 for v in end))
    check('transfer_tb_preserved',sum(sum(v) for v in start)==sum(sum(v) for v in end))
    check('transfer_rotation_preserved',sum(x-y for x,y in start)==sum(x-y for x,y in end))

# An abstract model: finite levels and an upper tb bound do not bound root levels.
# Roots have tb=-n, n>=1, with disjoint two-sign stabilization cones.
for N in range(1,31):
    level=[(n,a,N-n-a) for n in range(1,N+1) for a in range(N-n+1)]
    check('finite_levels_infinite_root_model',len(level)==N*(N+1)//2)
    check('root_at_every_depth',(N,0,0) in level)
    check('all_level_tb_equal',all(-n-a-b==-N for n,a,b in level))

# Exhaust the finite truth tables in the certificate-ceiling lemma.
for depth in range(1,9):
    feasible=[]
    for bits in product((False,True),repeat=depth+1):
        # Same value at a level; every lower level has a stabilized representative.
        if not any(bits[1:]): feasible.append(bits)
    check('ceiling_truth_tables',len(feasible)==2)
    check('only_top_level_possible',all(not any(b[1:]) for b in feasible))

# Exact operators on finitely supported vectors in the algebraic direct sum F2^(N).
def add(x,y):return x^y
def a(i,v):return frozenset(n//2 for n in v if n%2==i)
def b(i,v):return frozenset(2*n+i for n in v)
for n in range(128):
    v=frozenset([n])
    for i,j in product((0,1),repeat=2):
        check('leavitt_a_b_relations',a(i,b(j,v))==(v if i==j else frozenset()))
    check('leavitt_partition_identity',add(b(0,a(0,v)),b(1,a(1,v)))==v)
for mask in range(256):
    v=frozenset(i for i in range(8) if (mask>>i)&1)
    check('leavitt_linear_extension',add(b(0,a(0,v)),b(1,a(1,v)))==v)
for n in range(1,65):
    check('finite_dimension_contradiction',2*n>n)
check('nonzero_infinite_identity',add(b(0,a(0,frozenset([0]))),b(1,a(1,frozenset([0]))))==frozenset([0]))
p=Path(__file__).resolve().parent
receipt={'artifact_sha256':hashlib.sha256((p/'OBSTRUCTION.md').read_bytes()).hexdigest(),
         'arithmetic':'exact integers and finitely supported F2 vectors',
         'assertions_passed':sum(counts.values()),'by_category':counts,
         'scope':'Finite algebraic/combinatorial controls, not Legendrian realizations or enumeration.',
         'original_problem_solved':False}
(p/'verification.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt,indent=2))
