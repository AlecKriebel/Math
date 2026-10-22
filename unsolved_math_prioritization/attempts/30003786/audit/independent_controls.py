#!/usr/bin/env python3
"""Auditor controls. No import or reuse of the author's verifier.
Finite diagnostics only; see AUDIT.md for the infinite proofs.
"""
from collections import deque
from fractions import Fraction
from math import gcd
import hashlib
import json
from pathlib import Path

checks = 0

def require(x):
    global checks
    checks += 1
    if not x:
        raise AssertionError(checks)

def eye(d):
    return tuple(tuple(int(i == j) for j in range(d)) for i in range(d))

def product(x, y, m=None):
    z = tuple(tuple(sum(x[i][k]*y[k][j] for k in range(len(y)))
                    for j in range(len(y[0]))) for i in range(len(x)))
    return tuple(tuple(a % m for a in row) for row in z) if m is not None else z

def inverse2(x):
    return ((x[1][1], -x[0][1]), (-x[1][0], x[0][0]))

def power(x, e, m=None):
    if e < 0:
        x, e = inverse2(x), -e
    r = eye(len(x))
    if m is not None:
        r = tuple(tuple(a % m for a in row) for row in r)
    while e:
        if e % 2:
            r = product(r, x, m)
        x = product(x, x, m)
        e //= 2
    return r

def determinant(x):
    x = [list(map(Fraction, row)) for row in x]
    d = Fraction(1)
    for i in range(len(x)):
        j = next((j for j in range(i, len(x)) if x[j][i]), None)
        if j is None:
            return 0
        if j != i:
            x[i], x[j] = x[j], x[i]
            d = -d
        pivot = x[i][i]
        d *= pivot
        for j in range(i+1, len(x)):
            t = x[j][i]/pivot
            x[j] = [a-t*b for a, b in zip(x[j], x[i])]
    return d

A = ((1, 2), (0, 1))
B = ((1, 0), (2, 1))
I2 = eye(2)

# Analytically constructed witnesses, independent of Cayley-graph searching.
# If 5 does not divide m, A^m works. Otherwise m=2^k n (n odd),
# r=2^k*(2^(k+1))^-1 mod n. C=A^r, E=B^r both have trivial
# 2-primary component and odd components U(1),L(1). Build D=diag(2,1/2)
# in that component, then D C D^-1 C^-4 is a kernel word of chi=-3r.
moduli = list(range(1, 10001))
moduli += [2**k * 5**e * 3**f for k,e,f in [(0,20,0),(1,19,2),(17,1,9),(80,50,20),(130,0,20)]]
constructive = []
for m in moduli:
    identity = tuple(tuple(a % m for a in row) for row in I2)
    if m % 5:
        w = power(A, m, m)
        label = m % 5
        r = None
    else:
        n, h = m, 1
        while n % 2 == 0:
            n //= 2
            h *= 2
        r = h*pow(2*h, -1, n)
        C, E = power(A, r, m), power(B, r, m)
        v = pow(2, -1, n)
        D = eye(2)
        for factor in [power(C,2,m),power(E,-v,m),C,E,power(C,-1,m)]:
            D = product(D, factor, m)
        require(tuple(tuple(a % n for a in row) for row in D) == ((2 % n,0),(0,v)))
        w = product(product(product(D,C,m),inverse2(D),m),power(C,-4,m),m)
        label = (-3*r) % 5
    require(w == identity)
    require(label != 0)
    if m > 10000 or m in [5,10,25,40,100,10000]:
        constructive.append({'modulus': str(m), 'r': str(r), 'character': label})

# Full finite-image relation constraints over F5, independently killing BOTH
# potential generator values. Tree paths label vertices in Z^2. Non-tree
# edges give exact relation exponent sums; rank two precludes any C5 map.
relation_results = []
for m in list(range(1,49)) + [60,75,80,100]:
    identity = tuple(tuple(a % m for a in row) for row in I2)
    labels = {identity:(0,0)}
    queue = deque([identity])
    relations = set()
    while queue:
        x = queue.popleft()
        p,q = labels[x]
        for generator, dp,dq in [(A,1,0),(B,0,1),(inverse2(A),-1,0),(inverse2(B),0,-1)]:
            y = product(x,generator,m)
            label = ((p+dp)%5,(q+dq)%5)
            if y not in labels:
                labels[y] = label
                queue.append(y)
            else:
                relations.add(((label[0]-labels[y][0])%5,(label[1]-labels[y][1])%5))
    nonzero = next((v for v in relations if v != (0,0)), None)
    require(nonzero is not None)
    independent = next((v for v in relations if (v[0]*nonzero[1]-v[1]*nonzero[0])%5), None)
    require(independent is not None)
    relation_results.append({'modulus':m,'image_order':len(labels),'relation_rank_over_F5':2})

# Explicit 7x7 matrices, exact determinants, inverse generators, and all
# group words through length 5, without symbolic permutation shortcuts.
P = tuple(tuple(int(i==(j+1)%5) for j in range(5)) for i in range(5))
require(determinant(P)==1)
require(power(P,5)==eye(5))
require(len({power(P,t,2) for t in range(5)})==5)
def block(x,y):
    return tuple(tuple(x[i][j] if i<2 and j<2 else y[i-2][j-2] if i>=2 and j>=2 else 0
                       for j in range(7)) for i in range(7))
gens = [(A,1),(B,0),(inverse2(A),-1),(inverse2(B),0)]
for x,c in gens:
    require(determinant(block(x,power(P,c%5)))==1)
count_words = 0
frontier = [(eye(2),eye(7),0)]
for length in range(6):
    next_frontier = []
    for x,y,c in frontier:
        require(y == block(x,power(P,c%5)))
        require((tuple(tuple(a%2 for a in row) for row in y)==eye(7)) == (c%5==0))
        count_words += 1
        if length < 5:
            for g,d in gens:
                next_frontier.append((product(x,g),product(y,block(g,power(P,d%5))),c+d))
    frontier = next_frontier

# Verify all 64 supplied witness words with this independent matrix engine.
author = json.loads((Path(__file__).resolve().parent.parent / 'public' / 'verify_exact_results.json').read_text())
lookup={'a':A,'b':B,'A':inverse2(A),'B':inverse2(B)}
for record in author['noncongruence_witnesses']:
    x=eye(2)
    for c in record['word']:
        x=product(x,lookup[c])
    m=record['modulus']
    require(all((x[i][j]-int(i==j))%m==0 for i in range(2) for j in range(2)))
    require((record['word'].count('a')-record['word'].count('A'))%5==record['chi']!=0)
    require(determinant(x)==1)

# Exact identities used in the prior-theorem transfer, not numerical traces.
require(product(A,B)==((5,2),(2,1)))
require((A[0][0]+A[1][1])**2==4)
require((product(A,B)[0][0]+product(A,B)[1][1])**2==36)
require(all(g[i][i]%4==1 for g,d in gens for i in range(2)))

print(json.dumps({'status':'PASS','assertions':checks,
                  'constructed_witness_moduli_count':len(moduli),
                  'constructed_witness_examples':constructive,
                  'relation_rank_tests':relation_results,
                  'explicit_block_words_checked':count_words,
                  'supplied_witnesses_independently_checked':64,
                  'scope':'Finite exact controls; infinite proofs remain written arguments.'},indent=2,sort_keys=True))
