#!/usr/bin/env python3
"""Exact finite regression controls; not a solver for the original question."""
from fractions import Fraction as F
from itertools import product
import json
from pathlib import Path

counts = {}
def record(k, n=1): counts[k] = counts.get(k,0)+n

def U(v, signs):
    n=len(v)
    return [signs[i]*v[(i-1)%n] for i in range(n)]
def sub(a,b): return [x-y for x,y in zip(a,b)]
def matmul(a,b):
    return [[sum(x*y for x,y in zip(row,col)) for col in zip(*b)] for row in a]

# Every sign assignment on one cycle up to length 7, including the n=1 case.
for n in range(1,8):
    for signs in product((-1,1),repeat=n):
        s=1
        for x in signs: s*=x
        for j in range(n):
            v=[F(int(i==j)) for i in range(n)]
            z=v[:]; total=[F(0)]*n
            for k in range(n):
                total=[x+y for x,y in zip(total,z)]
                z=U(z,signs)
            assert z==[s*x for x in v]
            record('cycle_power_basis')
            if s==-1:
                x=[a/2 for a in total]
                assert sub(x,U(x,signs))==v
                record('negative_cycle_inverse_basis')
            else:
                assert sub(total,U(total,signs))==[0]*n
                record('positive_cycle_invariant_sum_basis')

# General-alpha estimate controls at alpha=1/2 and 1/3 on perfect powers.
for degree in (2,3):
    for a in range(-20,21):
        for b in range(-20,21):
            x=(1 if a>=0 else -1)*abs(a)**degree
            y=(1 if b>=0 else -1)*abs(b)**degree
            assert abs(a-b)**degree <= 2**(degree-1)*abs(x-y)
            record(f'signed_power_alpha_1_over_{degree}')

# Exact failure of applying M_{1,2} pointwise to b(n)=n.
assert 2 != 4*1  # M(b(4))=sqrt(4)=2, but 4 M(b(1))=4.
record('mazur_non_cocycle')

# Nonsingular two-atom control (masses 1 and 4).
P1=[[F(0),F(4)],[F(1,4),F(0)]]
P2=[[F(0),F(2)],[F(1,2),F(0)]]
A=[[F(1),F(0)],[F(0),F(1,2)]]
assert P1!=P2
assert matmul(A,P2)==matmul(P1,A)
record('density_multiplier_intertwining')
assert [F(1)*F(1), F(1,4)*F(4)] == [1,1]
record('density_measure_invariant')

# Finite weighted atomic normalization for p=1,2,3, masses 1 and64.
P=[[F(0),F(1)],[F(1),F(0)]]
for p,root in ((1,64),(2,8),(3,4)):
    Q=[[F(0),F(root)],[F(1,root),F(0)]]
    D=[[F(1),F(0)],[F(0),F(root)]]
    assert matmul(D,Q)==matmul(P,D)
    record('atomic_normalization')

# Exact finite sections of the divergent-primitive construction.
for p,base in ((1,2),(2,4),(3,8)):
    for K in range(1,13):
        norm_u_p=F(0); norm_v_p=F(0)
        for k in range(1,K+1):
            n=base**k
            amplitude=F(1,2**k)  # n^(1/p)=2^k
            norm_u_p+=n*amplitude**p
            norm_v_p+=(2*amplitude)**p
        assert norm_u_p==K
        assert norm_v_p==F(2**p,base-1)*(1-F(1,base**K))
        record('gluing_finite_sections')

result={
    'status':'PASS',
    'checks':counts,
    'total_exact_assertion_cases':sum(counts.values()),
    'scope':'Finite regression controls only. Infinite-family claims rely on ATTEMPTS.md proofs. The original interval problem remains unsolved.'
}
print(json.dumps(result,indent=2))
