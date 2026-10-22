#!/usr/bin/env python3
"""Small exact diagnostics; these are not a proof of the universal theorem."""
from fractions import Fraction as Q
from itertools import combinations
import json

counts = {}
def check(name, condition):
    assert condition, name
    counts[name] = counts.get(name, 0) + 1

def pow2(n):
    return n > 0 and (n & (n - 1)) == 0

def dyadic(x):
    return pow2(x.denominator)

def slope_ok(x):
    return pow2(x.numerator) and pow2(x.denominator)

def partition(a, b):
    d = max(a.denominator, b.denominator)
    return [(Q(i,d), Q(i+1,d)) for i in range(int(a*d),int(b*d))]

def equalize(p, q):
    p, q = list(p), list(q)
    while len(p) != len(q):
        s = p if len(p) < len(q) else q
        a,b = s.pop(0); m=(a+b)/2
        s[:0] = [(a,m),(m,b)]
    return p,q

def extension(A, B, shift):
    a=list(sorted(A)); b=list(sorted(B)); n=len(a)
    b=b[shift:]+[x+1 for x in b[:shift]]
    a += [a[0]+1]; b += [b[0]+1]
    pieces=[]
    for i in range(n):
        p,q=equalize(partition(a[i],a[i+1]),partition(b[i],b[i+1]))
        pieces += [(x0,x1,y0,y1) for (x0,x1),(y0,y1) in zip(p,q)]
    return pieces

def evaluate(pieces,x):
    origin=pieces[0][0]
    while x<origin: x+=1
    while x>=origin+1: x-=1
    for a,b,c,d in pieces:
        if a<=x<=b:
            return (c+(x-a)*(d-c)/(b-a))%1
    raise AssertionError('missing segment')

def slide(U,V):
    common=set(U)&set(V)
    old=list(set(U)-common); new=list(set(V)-common)
    if len(old)!=1 or len(new)!=1:return False
    a,b=old[0],new[0]
    between=sum(0<(x-a)%1<(b-a)%1 for x in common)
    return between in (0,len(common))

def slide_path(U,V):
    n=len(U)
    q=next(Q(i,32) for i in range(32) if Q(i,32) not in set(U)|set(V))
    u=sorted((x-q)%1 for x in U);v=sorted((x-q)%1 for x in V)
    upper=min(u[0],v[0]);d=1
    while Q(n,d)>=upper:d*=2
    b=[Q(i,d) for i in range(1,n+1)]
    def half(a):
        out=[tuple(sorted((x+q)%1 for x in a))]
        a=list(a)
        for i in range(n):
            a[i]=b[i];out.append(tuple(sorted((x+q)%1 for x in a)))
        return out
    pu,pv=half(u),half(v)
    return pu+list(reversed(pv[:-1]))

grid=tuple(Q(i,8) for i in range(8))
for k in range(1,4):
    configs=list(combinations(grid,k))
    for U in configs:
        for V in configs:
            path=slide_path(U,V)
            check('slide_path_endpoints',path[0]==U and path[-1]==V)
            check('slide_path_length',len(path)-1<=2*k)
            for X,Y in zip(path,path[1:]):
                check('elementary_slide',slide(X,Y))
                check('dyadic_vertices',all(dyadic(x) for x in X+Y))

# Deterministic varied circular extension inputs, including target wraparound.
grid16=tuple(Q(i,16) for i in range(16))
for k in range(1,6):
    configs=list(combinations(grid16,k))
    for j in range(15):
        A=configs[(j*29)%len(configs)]
        B=configs[(j*47+7)%len(configs)]
        shift=j%k
        pieces=extension(A,B,shift)
        target=list(B[shift:])+list(B[:shift])
        check('extension_requested_values',[evaluate(pieces,a) for a in A]==target)
        check('extension_degree_one',pieces[-1][3]-pieces[0][2]==1)
        for a,b,c,d in pieces:
            check('extension_legal_piece',a<b and c<d and all(dyadic(x) for x in (a,b,c,d)) and slope_ok((d-c)/(b-a)))
        for P,R in zip(pieces,pieces[1:]):
            check('extension_continuity',P[1]==R[0] and P[3]==R[2])

# Explicit cyclic complements for k not restricted to powers of two.
for k in range(1,17):
    intervals=[(Q(0),Q(1))]
    while len(intervals)<k:
        a,b=intervals.pop(0);m=(a+b)/2
        intervals[:0]=[(a,m),(m,b)]
    A=tuple(a for a,b in intervals)
    pieces=[]
    for i,(a,b) in enumerate(intervals):
        c,d=intervals[(i+1)%k]
        if i==k-1:c+=1;d+=1
        pieces.append((a,b,c,d))
    for a,b,c,d in pieces:
        check('cyclic_complement_legal',slope_ok((d-c)/(b-a)))
        for x in (a,(a+b)/2,(3*a+b)/4):
            y=x
            for power in range(1,k+1):
                y=evaluate(pieces,y)
                check('cyclic_order_exact', (y==x)==(power==k))
    check('cyclic_endpoint_permutation',[evaluate(pieces,a) for a in A]==list(A[1:])+list(A[:1]))

print(json.dumps({'status':'PASS','arithmetic':'Python Fraction; integer and rational exactness','counts':counts,'total_assertions':sum(counts.values()),'scope':'Representative extension and cyclic-complement checks; all grid-8 configuration pairs for k<=3. Universal claims are proved in PROOF.md, not inferred from these checks.'},indent=2,sort_keys=True))
