#!/usr/bin/env python3
"""Independent exact diagnostics. No imports from author diagnostics."""
from fractions import Fraction as F
from itertools import permutations, product
from math import gcd
import json

counts = {}
def check(value, family):
    if not value:
        raise RuntimeError(family)
    counts[family] = counts.get(family, 0) + 1

def dot(x,y):return sum(a*b for a,b in zip(x,y))
def add(x,y):return tuple(a+b for a,b in zip(x,y))
def sub(x,y):return tuple(a-b for a,b in zip(x,y))
def perm(p,x):return tuple(x[i] for i in p)

# Complete conjugated Reynolds evaluation, with an arbitrary non-equivariant h.
W=list(permutations(range(3)));identity=(0,1,2)
beta=(1,2,-3);alpha=(1,4,-5)
check(len({dot(alpha,perm(w,beta)) for w in W})==6,'a2_separation')
operators=[(2,(1,-1,0),(1,0,-1)),(-3,(0,1,-1),(0,-1,1)),(1,(0,0,0),(0,0,0))]
def h(n):return n[0]**3+2*n[1]**2-n[2]+7
for q in (F(2),F(3)):
    def mask_at(w):
        value=q**dot(perm(w,alpha),beta)
        out=F(1)
        for v in W:
            if v!=identity:out*=value-q**dot(alpha,perm(v,beta))
        return out
    for a,b in product(range(-3,4),repeat=2):
        target=(a,b,-a-b);gamma=sub(target,beta);lhs=F(0)
        for w in W:
            point=add(beta,perm(w,gamma))
            residue=sum(c*q**dot(perm(w,nu),point)*h(add(point,perm(w,delta))) for c,nu,delta in operators)
            lhs+=mask_at(w)*residue
        rhs=mask_at(identity)*sum(c*q**dot(nu,target)*h(add(target,delta)) for c,nu,delta in operators)
        check(lhs==rhs,'complete_reynolds_evaluation')
    check(mask_at(identity)!=0,'regular_mask_nonzero')
    for w in W:
        check((mask_at(w)!=0)==(w==identity),'regular_mask_support')

# An omitted shift fails exactly at a singular target, not merely asymptotically.
for q in (F(2),F(3),F(5)):
    residue=lambda n:(n+1)**3-(n-1)**3
    d=q-q**-1
    check(d*residue(0)!=d*residue(1),'omitted_shift_rejected')
    check(residue(0)!=0 and residue(0)-residue(0)==0,'plain_average_rejected')

# Rational-form coordinate subtorus: B*v_i=c*e_i, no added multipliers.
def inv(matrix):
    n=len(matrix);a=[[F(x) for x in row]+[F(i==j) for j in range(n)] for i,row in enumerate(matrix)]
    for j in range(n):
        p=next(i for i in range(j,n) if a[i][j]);a[j],a[p]=a[p],a[j]
        s=a[j][j];a[j]=[x/s for x in a[j]]
        for i in range(n):
            if i!=j:
                s=a[i][j];a[i]=[x-s*y for x,y in zip(a[i],a[j])]
    return [row[n:] for row in a]
forms=[[[F(2)]],[[F(2,3),F(1,2)],[F(1,2),F(5,7)]],[[F(0),F(1,2)],[F(1,2),F(0)]],[[2,1,0],[1,3,1],[0,1,2]]]
bridge=[]
for matrix in forms:
    inverse=inv(matrix);c=1;r=len(matrix)
    for row in inverse:
        for x in row:c=c*x.denominator//gcd(c,x.denominator)
    vectors=[tuple(c*inverse[j][i] for j in range(r)) for i in range(r)]
    for i,v in enumerate(vectors):
        check(all(x.denominator==1 for x in v),'integral_subtorus_vectors')
        for j,row in enumerate(matrix):check(dot(row,v)==c*int(i==j),'diagonal_commutation')
        for point in product(range(-2,3),repeat=r):
            check(dot(v,tuple(dot(row,point) for row in matrix))==c*point[i],'coordinate_multiplier')
    bridge.append({'rank':r,'c':c,'vectors':[[int(x) for x in v] for v in vectors]})

# Full-ideal Gaussian counterexample. These generators span every character
# cancellation block in the normal-ordered action of an annihilator on f.
for t in (F(2),F(3)):
    f=lambda n:t**(n*n)
    h=lambda n:(1 if n%2==0 else 3)*f(n)
    check(h(0)==f(0) and h(1)!=f(1),'gaussian_one_seed_rejected')
    for n in range(-12,13):
        check(f(n+2)==t**(4*n+4)*f(n),'gaussian_two_step')
        check(h(n+2)==t**(4*n+4)*h(n),'gaussian_parity_rescaling')
    for k,a1,a2,n in product(range(-3,4),range(-2,3),range(-2,3),range(-3,4)):
        b1=k-2*a1;b2=k-2*a2
        check(b1%2==b2%2,'equal_slope_forces_parity')
        pf=t**(-b1*b1+4*a1*n)*f(n+b1)-t**(-b2*b2+4*a2*n)*f(n+b2)
        ph=t**(-b1*b1+4*a1*n)*h(n+b1)-t**(-b2*b2+4*a2*n)*h(n+b2)
        check(pf==0 and ph==0,'whole_annihilator_block_controls')

# PBW pair: composition evaluated separately, including the b-coordinate shift.
def integer(n,q):return (q**n-q**-n)/(q-q**-1)
def A(a,b,c,q):return -(q-q**-1)*integer(c,q**3)*q**(3*a+b-3*c+2)
def B(a,b,c,q):return integer(3,q)*integer(b-1,q)*integer(b,q)*q**(3*a-b+2)
for q,a,b,c in product((F(2),F(3)),range(3),range(2,5),range(1,5)):
    ab=B(a,b,c,q)*A(a,b-2,c+1,q)
    ba=A(a,b,c,q)*B(a,b,c-1,q)
    correct=q**-5*integer(c+1,q**3)/integer(c,q**3)
    wrong=q**-3*integer(c+1,q**3)/integer(c,q**3)
    check(ab/ba==correct,'pbw_ratio')
    check(ab/ba!=wrong,'pbw_wrong_exponent_rejected')

# Strip family tests on a different support set and at a different q.
q=F(3)
for m0 in (-8,0,11):
    def strip(n,m):return int(n==0 and m==m0)
    for n,m in product(range(-5,6),range(-12,13)):
        check((q**n-1)*(q**(n+1)-1)*(strip(n+1,m)-strip(n,m))==0,'strip_first_equation')
        check((q**n-1)*(strip(n,m+1)-strip(n,m))==0,'strip_second_equation')

print(json.dumps({'passed':True,'total_checks':sum(counts.values()),'families':counts,'coordinate_bridges':bridge,'scope':'Independent finite exact algebra diagnostics; universal claims are justified separately in AUDIT.md.'},sort_keys=True,indent=2))
