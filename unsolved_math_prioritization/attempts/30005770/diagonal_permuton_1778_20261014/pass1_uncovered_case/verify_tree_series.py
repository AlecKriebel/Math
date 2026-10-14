#!/usr/bin/env python3
"""Exact finite checks of the authored tree GF; not an asymptotic proof."""
from fractions import Fraction
from math import factorial
import json
from pathlib import Path

N = 40

def add(a, b):
    out = [0] * max(len(a), len(b))
    for i, x in enumerate(a): out[i] += x
    for i, x in enumerate(b): out[i] += x
    return out

def mul(a,b):
    out = [0] * (len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b): out[i+j] += x*y
    while len(out)>1 and out[-1]==0: out.pop()
    return out

# B_n is the polynomial counting relaxed-root trees by root label.
# G_n is the polynomial counting their sequences by total root label.
B = [[0] for _ in range(N+1)]
G = [[1]] + [[0] for _ in range(N)]
T = [0]*(N+1)
for n in range(1,N+1):
    T[n] = sum(G[n-1])
    if n == 1:
        B[n] = [1]
    else:
        # Nonempty child forest of positive total size n-1.
        B[n] = [0]*(len(G[n-1])+1)
        for S, ways in enumerate(G[n-1]):
            for label in range(S+2): B[n][label] += ways
    G[n] = [0]
    for k in range(1,n+1): G[n] = add(G[n], mul(B[k],G[n-k]))

formula = [0,1]+[3*2**(n-2)*factorial(2*n-2)//(factorial(n+1)*factorial(n-1)) for n in range(2,N+1)]
assert T == formula
# Exact sequence identity T=z/(1-B(z,1)).
for n in range(2,N+1):
    assert T[n] == sum(sum(B[k])*T[n-k] for k in range(1,n))

# Check the quadratic at u=3/2 to the full truncation.
u=Fraction(3,2)
b = [sum(Fraction(c)*u**i for i,c in enumerate(p)) for p in B]
c = [Fraction(0)] + [Fraction(sum(p)) for p in G[1:]]
def seriesmul(a,b):
    return [sum(a[k]*b[n-k] for k in range(n+1)) for n in range(N+1)]
def scaled(a,x): return [v*x for v in a]
def plus(a,b): return [x+y for x,y in zip(a,b)]
def shifted(a): return [Fraction(0)]+a[:-1]
one=[Fraction(1)]+[Fraction(0)]*N
z=[Fraction(0),Fraction(1)]+[Fraction(0)]*(N-1)
one_minus_b=plus(one,scaled(b,-1))
P=plus(scaled(seriesmul(plus(b,scaled(z,-1)),one_minus_b),1-u), scaled(shifted(seriesmul(c,one_minus_b)),-1))
P=plus(P,scaled(shifted(b),u*u))
assert P == [0]*(N+1)

out={
    'status':'PASS',
    'interpretation':'Exact finite identity checks only, not evidence establishing the asymptotic theorem.',
    'maximum_vertex_count':N,
    'tree_counts_first_12':T[1:13],
    'relaxed_root_polynomials_first_6':B[1:7],
    'beta_tree_formula_matches':True,
    'root_sequence_identity_matches':True,
    'quadratic_at_u_3_over_2_matches':True,
    'coefficient_arithmetic':'unbounded integers and fractions only',
}
path=Path(__file__).with_name('TREE_SERIES_VERIFICATION.json')
path.write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
