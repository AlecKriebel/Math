#!/usr/bin/env python3
"""Exact finite controls only. This does not prove the Hodge conjecture."""
from fractions import Fraction as F
from itertools import combinations
from math import lcm
import json

checks = 0

def check(x):
    global checks
    checks += 1
    if not x:
        raise AssertionError(f'Exact check {checks} failed')

def mv(A, v):
    return [sum((F(x)*y for x,y in zip(row,v)), F(0)) for row in A]

def det(A):
    A = [[F(x) for x in row] for row in A]
    n = len(A)
    d = F(1)
    for j in range(n):
        k = next((i for i in range(j,n) if A[i][j]), None)
        if k is None:
            return F(0)
        if k != j:
            A[k], A[j] = A[j], A[k]
            d = -d
        p = A[j][j]
        d *= p
        for i in range(j+1,n):
            r = A[i][j]/p
            for h in range(j,n):
                A[i][h] -= r*A[j][h]
    return d

def solve(A, b):
    A = [[F(x) for x in row]+[F(y)] for row,y in zip(A,b)]
    n = len(A)
    for j in range(n):
        k = next(i for i in range(j,n) if A[i][j])
        A[k], A[j] = A[j], A[k]
        p=A[j][j]
        A[j] = [x/p for x in A[j]]
        for i in range(n):
            if i != j:
                p=A[i][j]
                A[i] = [x-p*y for x,y in zip(A[i],A[j])]
    return [row[-1] for row in A]

def coefficient_test(P):
    n=len(P)
    check(all(P[i][j]==P[j][i] for i in range(n) for j in range(n)))
    check(all(P[i][j]<=0 for i in range(n) for j in range(n) if i!=j))
    check(all(det([r[:k] for r in P[:k]])>0 for k in range(1,n+1)))
    a=solve(P,[1]*n)
    check(all(x>0 for x in a))
    check(mv(P,a)==[F(1)]*n)
    q=lcm(*(x.denominator for x in a))
    b=[q*x for x in a]
    check(all(x.denominator==1 and x>0 for x in b))
    check(mv([[-x for x in row] for row in P],b)==[-q]*n)
    return a,q,b

# Exhaust all simple graphs on up to five vertices, including disconnected graphs.
# P= D (I + graph Laplacian) D is positive definite by a sum-of-squares identity.
# Two scalings also test matrices that need not be diagonally dominant.
matrices=0
for n in range(1,6):
    pairs=list(combinations(range(n),2))
    for mask in range(1<<len(pairs)):
        P=[[int(i==j) for j in range(n)] for i in range(n)]
        for k,(i,j) in enumerate(pairs):
            if mask>>k&1:
                P[i][i]+=1;P[j][j]+=1;P[i][j]-=1;P[j][i]-=1
        for scales in ([1]*n,list(range(1,n+1))):
            Q=[[scales[i]*P[i][j]*scales[j] for j in range(n)] for i in range(n)]
            coefficient_test(Q);matrices+=1

A=[[-5,2],[2,-1]]
a,q,b=coefficient_test([[-x for x in row] for row in A]);matrices+=1
check(a==[3,7] and q==1)
check(mv(A,[1,1])==[-3,1])
check(mv(A,b)==[-1,-1])
# Literal disconnected eigenvector claim fails: a positive eigenvector would
# force the eigenvalue to be both -1 and -2.
check(F(-1)!=F(-2))
a2,q2,b2=coefficient_test([[1,0],[0,2]]);matrices+=1
check(a2==[1,F(1,2)] and b2==[2,1])

# Null-face feasibility and dual certificate.
B=[[1,-1],[-1,1]]
check(mv(B,[0,1])[0]<0)
check(mv(B,[1,0])[1]<0)
y=[1,1]
check([sum(y[j]*B[j][i] for j in range(2)) for i in range(2)]==[0,0])
for c1 in range(31):
    for c2 in range(31):
        check(not all(x<0 for x in mv(B,[c1,c2])))

# Pointwise versus uniform threshold on a closed curved cone.
for m in range(1,1001):
    t=F(1,2*m)
    x,y,z=t*t,t,F(1)
    check(y*y==x*z and x>=0 and z>=0)
    check(m*x-y==-F(1,4*m))

# Full Griffiths determinant product, reduced using d_p=d_(n+1-p)*T^-1.
# This checks exponent bookkeeping, not the geometric duality theorem.
parity=[]
for n in range(1,41):
    first=(n+2)//2
    exp={p:0 for p in range(first,n+1)}
    torsion=0
    for p in range(1,n+1):
        if p<first:
            exp[n+1-p]+=1;torsion-=1
        else:
            exp[p]+=1
    expected={p:2 for p in exp}
    if n%2:
        expected[first]=1
    check(exp==expected)
    check(torsion==-(n//2))
    parity.append({'weight':n,'upper_exponents':exp,'det_V_exponent':torsion})

# Explicit finite-polyhedral all-m threshold example.
# Two null rays have matrix A above; two positive rays have L-intersections 1,2.
full_B=A+[[2,3],[-4,5]]
ell=[0,0,1,2]
E=mv(full_B,b)
m0=max([1]+[int(E[j]//ell[j])+1 for j in range(4) if ell[j]>0])
for m in range(m0,m0+100):
    check(all(m*ell[j]-E[j]>0 for j in range(4)))

print(json.dumps({
 'problem_id':'30004494',
 'verdict':'PASS_EXACT_FINITE_CONTROLS_ONLY',
 'checks':checks,
 'matrices_tested':matrices,
 'matrix_example':{'A':A,'rational_coefficients':[str(x) for x in a],
                   'integral_coefficients':[int(x) for x in b],'common_margin':q},
 'disconnected_example':{'rational_coefficients':[str(x) for x in a2],
                         'integral_coefficients':[int(x) for x in b2]},
 'simultaneity_obstruction':{'B':B,'dual':[1,1]},
 'curved_cone_tests':1000,
 'parity_weights_checked':[1,40],
 'finite_cone_threshold':m0,
 'scope':'Exact arithmetic controls supplement the written proofs. No formal verification of Hodge-theoretic inputs, cone realization, or the original conjecture.'
},sort_keys=True,indent=2))
