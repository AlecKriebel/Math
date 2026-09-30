#!/usr/bin/env python3
"""Finite exact diagnostics; covering/compactness conclusions use written proofs."""
from fractions import Fraction as Q
from itertools import product,permutations
from math import factorial,lcm
from pathlib import Path
from hashlib import sha256
from collections import Counter
import json
C=Counter()
def ck(cat,x):
    assert bool(x),cat
    C[cat]+=1
I=((1,0),(0,1))
def mm(a,b):return tuple(tuple(sum(a[i][k]*b[k][j] for k in range(2)) for j in range(2)) for i in range(2))
def mv(a,x):return tuple(sum(a[i][k]*x[k] for k in range(2)) for i in range(2))
def det(a):return a[0][0]*a[1][1]-a[0][1]*a[1][0]
def inverse(a):
    d=det(a)
    return ((Q(a[1][1],d),Q(-a[0][1],d)),(Q(-a[1][0],d),Q(a[0][0],d)))
def power(a,k):
    b=I
    for _ in range(k):b=mm(b,a)
    return b
def subtract(a,b):return tuple(tuple(a[i][j]-b[i][j] for j in range(2)) for i in range(2))
def integral(v):return all(Q(x).denominator==1 for x in v)
As=[((a,b),(c,d)) for a,b,c,d in product(range(-3,4),repeat=4) if a*d-b*c==1 and abs(a+d)>2]
for A in As:
    b=(Q(1,3),Q(-2,5));fixed=mv(inverse(subtract(I,A)),b)
    ck('affine_fixed_point',tuple(x+y for x,y in zip(mv(A,fixed),b))==fixed)
    for k in range(1,5):
        B=subtract(power(A,k),I)
        ck('period_matrix_invertibility',det(B)!=0)
        for z in ((0,0),(1,0),(0,1),(1,-1),(-2,3)):
            x=mv(inverse(B),z)
            ck('periodic_point_rationality',mv(B,x)==z and integral(mv(B,x)))
            ck('periodic_denominator_bound',all(abs(det(B))%v.denominator==0 for v in x))
            N=lcm(*(v.denominator for v in x))
            for M in (((1,N),(0,1)),((1,0),(N,1))):
                ck('principal_congruence_fixes_point',integral(tuple(t-u for t,u in zip(mv(M,x),x))))
            y=tuple(t+u for t,u in zip(x,fixed));iterate=y
            for _ in range(k):iterate=tuple(t+u for t,u in zip(mv(A,iterate),b))
            ck('affine_periodic_coset',integral(tuple(t-u for t,u in zip(iterate,y))))
for N,a,b in product(range(1,13),range(1,6),range(1,6)):
    U=((1,a*N),(0,1));L=((1,0),(b*N,1))
    ck('parabolic_classification',det(U)==det(L)==1 and U[0][0]+U[1][1]==L[0][0]+L[1][1]==2 and U!=I and L!=I)
    P=mm(U,L);R=mm(L,U)
    ck('projectively_noncommuting_parabolics',P!=R and P!=tuple(tuple(-x for x in row) for row in R))
    ck('hyperbolic_product',P[0][0]+P[1][1]==2+a*b*N*N>2)

# Explicit punctured-torus monodromies; Nielsen twists preserve connected covers.
def comp(a,b):return tuple(a[b[i]] for i in range(len(a)))
def pinv(a):return tuple(a.index(i) for i in range(len(a)))
def ppow(a,k):
    b=tuple(range(len(a)))
    for _ in range(k):b=comp(b,a)
    return b
def order(a):
    b=tuple(range(len(a)))
    for k in range(1,factorial(len(a))+1):
        b=comp(b,a)
        if b==tuple(range(len(a))):return k
    raise AssertionError
def connected(a,b):
    seen={0};old=set()
    while old!=seen:
        old=set(seen)
        seen|={g[i] for g in (a,b,pinv(a),pinv(b)) for i in list(seen)}
    return len(seen)==len(a)
def commutator(a,b):return comp(comp(comp(a,b),pinv(a)),pinv(b))
covers=0
for D in (2,3,4):
    perms=list(permutations(range(D)))
    for a,b in product(perms,repeat=2):
        if not connected(a,b):continue
        covers+=1;oa,ob=order(a),order(b)
        ck('finite_monodromy_return_bound',1<=oa<=factorial(D)<=factorial(D)**3 and 1<=ob<=factorial(D))
        # U acts b -> b a; L acts a -> a b. Both have exact finite returns.
        ck('horizontal_monodromy_lift',comp(b,ppow(a,oa))==b)
        ck('vertical_monodromy_lift',comp(a,ppow(b,ob))==a)
        ck('peripheral_monodromy_preserved',commutator(a,comp(b,a))==commutator(a,b))
        ck('peripheral_monodromy_preserved',commutator(comp(a,b),b)==commutator(a,b))
        ck('connectedness_preserved',connected(a,comp(b,a)) and connected(comp(a,b),b))
# A finite cyclic orbit alone does not force its setwise stabilizer to be cyclic.
for k in range(3,15):
    rot=tuple((i+1)%k for i in range(k));ref=tuple((-i)%k for i in range(k))
    orbit={ppow(rot,j)[0] for j in range(k)}
    ck('marked_orbit_missing_hypothesis',orbit==set(range(k)) and ref[0]==0 and ref!=tuple(range(k)))
    ck('marked_orbit_extra_symmetry',comp(rot,ref)!=comp(ref,rot))
root=Path(__file__).resolve().parent
out={'verdict':'PASS','assertions':sum(C.values()),'categories':dict(C),'hyperbolic_integer_matrices':len(As),
 'connected_punctured_torus_monodromy_pairs':covers,
 'artifact_sha256':sha256((root/'PARTIAL.md').read_bytes()).hexdigest(),
 'scope':'Finite rational/permutation controls only. No compact purely cyclic Veech surface is constructed or ruled out in general.'}
(root/'verification.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))

