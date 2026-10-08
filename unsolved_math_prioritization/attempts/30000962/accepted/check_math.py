#!/usr/bin/env python3
"""Exact finite diagnostics for PROOF.md. These do not prove the infinite claims."""
from fractions import Fraction as F
from itertools import product
import json

counts = {}
def check(ok, family):
    if not ok:
        raise ValueError('failed diagnostic: '+family)
    counts[family] = counts.get(family, 0) + 1

def matmul(a,b):
    return tuple(tuple(sum(a[i][k]*b[k][j] for k in range(len(a))) for j in range(len(a))) for i in range(len(a)))
def mv(a,v): return tuple(sum(row[j]*v[j] for j in range(len(v))) for row in a)
def add(a,b): return tuple(x+y for x,y in zip(a,b))
def neg(a): return tuple(-x for x in a)
def sub(a,b): return add(a,neg(b))
def det(a): return a[0][0] if len(a)==1 else a[0][0]*a[1][1]-a[0][1]*a[1][0]
def inner(a,b,g): return sum(x*y for x,y in zip(a,mv(g,b)))
def rank(rows):
    a=[[F(x) for x in row] for row in rows]; p=0
    for j in range(len(a[0]) if a else 0):
        k=next((k for k in range(p,len(a)) if a[k][j]),None)
        if k is None: continue
        a[p],a[k]=a[k],a[p];z=a[p][j];a[p]=[x/z for x in a[p]]
        for k in range(len(a)):
            if k!=p and a[k][j]:
                z=a[k][j];a[k]=[x-z*y for x,y in zip(a[k],a[p])]
        p+=1
    return p

def group(c):
    r=len(c);eye=tuple(tuple(int(i==j) for j in range(r)) for i in range(r));gens=[]
    for k in range(r):
        s=[list(row) for row in eye];s[k]=[s[k][j]-c[k][j] for j in range(r)];gens.append(tuple(map(tuple,s)))
    out={eye};todo=[eye]
    while todo:
        w=todo.pop()
        for s in gens:
            v=matmul(s,w)
            if v not in out:out.add(v);todo.append(v)
    return sorted(out),gens,eye

root_data=[
 ('A1',((2,),),((2,),),(1,),2),
 ('A2',((2,-1),(-1,2)),((2,-1),(-1,2)),(1,1),6),
 ('B2',((2,-2),(-1,2)),((2,-2),(-2,4)),(4,3),8),
 ('G2',((2,-3),(-1,2)),((2,-3),(-3,6)),(5,3),12),
]
root_receipts=[]
for name,c,g,beta,order in root_data:
    W,gens,eye=group(c);r=len(beta);zero=(0,)*r
    check(len(W)==order,'weyl_group_orders')
    orbit=[mv(w,beta) for w in W]
    check(len(set(orbit))==order,'regular_orbits')
    for w in W:
        check(det(w) in (-1,1),'weyl_determinants')
        for x in product(range(-1,2),repeat=r):
            for y in product(range(-1,2),repeat=r):
                check(inner(mv(w,x),mv(w,y),g)==inner(x,y,g),'bilinear_invariance')
    alpha=None
    for a in product(range(1,20),repeat=r):
        if len({inner(a,x,g) for x in orbit})==order:alpha=a;break
    check(alpha is not None,'orbit_separator')
    exp={w:inner(alpha,mv(w,beta),g) for w in W}
    vals={w:F(2)**exp[w] for w in W}
    def dval(w):
        u=F(2)**inner(mv(w,alpha),beta,g);v=F(1)
        for z in W:
            if z!=eye:v*=u-vals[z]
        return v
    for w in W:check((dval(w)!=0)==(w==eye),'interpolation_mask')
    hv={}
    for scale,coeff in [(1,1),(2,3)]:
        for w in W:hv[tuple(scale*x for x in mv(w,beta))]=coeff*det(w)
    def h(n):return F(hv.get(n,0))
    P=[(2,(1,)*r,beta),(-3,neg(alpha),neg(beta)),(1,zero,zero)]
    def ph(n):return sum(F(coef)*F(2)**inner(nu,n,g)*h(add(n,delta)) for coef,nu,delta in P)
    targets=[zero,beta,tuple(3*x for x in beta)]+list(product(range(-2,3),repeat=r))
    for lam in targets:
        gamma=sub(lam,beta);lhs=F(0)
        for w in W:
            if not dval(w):continue
            n=add(beta,mv(w,gamma))
            shifted=sum(F(coef)*F(2)**inner(mv(w,nu),n,g)*h(add(n,mv(w,delta))) for coef,nu,delta in P)
            lhs+=dval(w)*shifted
        check(lhs==dval(eye)*ph(lam),'shifted_reynolds_identity')
    # Singular target 0 is included and has a nonzero extracted residue.
    check(ph(zero)!=0,'singular_target_nonzero_residue')
    # Spectral interpolation on the separating line.
    xs=[vals[w] for w in W]
    for j,x in enumerate(xs):
        for k,y in enumerate(xs):
            numerator=denominator=F(1)
            for ell,z in enumerate(xs):
                if ell!=j:numerator*=y-z;denominator*=x-z
            check(numerator/denominator==int(j==k),'spectral_projectors')
    ix={w:i for i,w in enumerate(W)};rows=[]
    for s in gens:
        for w in W:
            row=[0]*order;row[ix[matmul(s,w)]]+=1;row[ix[w]]-=det(s);rows.append(row)
    check(rank(rows)==order-1,'sign_spectral_dimension_one')
    root_receipts.append({'root_system':name,'order':order,'beta':beta,'separator':alpha,'distinct_exponents':sorted(exp.values())})

# Unweighted Reynolds sum of E_1-E_-1 vanishes under inversion, while its
# residue on an odd orbit function at the singular point is nonzero.
def odd(n): return int(n==1)-int(n==-1)
check((odd(1)-odd(-1))==2,'unweighted_average_negative_control')
check((odd(1)-odd(-1))+(odd(-1)-odd(1))==0,'unweighted_average_negative_control')

# Singular-strip equations allow independent unsampled line values.
for m0 in (3,5,7):
    def strip(n,m):return F(int(n==0 and m==m0))
    for n,m in product(range(-4,5),range(-9,10)):
        p1=(F(2)**n-1)*(F(2)**(n+1)-1)*(strip(n+1,m)-strip(n,m))
        p2=(F(2)**n-1)*(strip(n,m+1)-strip(n,m))
        check(p1==0 and p2==0,'singular_strip_recursions')
    check(strip(0,m0)==1,'singular_strip_nonzero')
    for n,m in product(range(-2,3),repeat=2):check(strip(n,m)==0,'singular_strip_zero_seeds')

# Product box: a full four-dimensional separated solution family.
freqx=(F(2),F(3));freqy=(F(5),F(7));coeff=(F(2),F(-1),F(4),F(3))
def u(n,m):return sum(coeff[2*i+j]*freqx[i]**n*freqy[j]**m for i,j in product(range(2),repeat=2))
seed_matrix=[[freqx[i]**n*freqy[j]**m for i,j in product(range(2),repeat=2)] for n,m in product(range(2),repeat=2)]
check(rank(seed_matrix)==4,'product_seed_rank')
for n,m in product(range(-6,7),repeat=2):
    check(u(n+2,m)-5*u(n+1,m)+6*u(n,m)==0,'box_propagation_equations')
    check(u(n,m+2)-12*u(n,m+1)+35*u(n,m)==0,'box_propagation_equations')
# Central Gaussian ratios are monomials, in a concrete cross-term case.
def Q(n,m):return n*n+2*n*m+3*m*m+4*n-2*m
for n,m in product(range(-5,6),repeat=2):
    check(Q(n+1,m)-Q(n,m)==2*n+2*m+5,'central_gaussian_ratios')
    check(Q(n,m+1)-Q(n,m)==2*n+6*m+1,'central_gaussian_ratios')

# G2 two-term noncommutation, independently evaluate both composition orders.
def qi(n,q):return (q**n-q**(-n))/(q-q**(-1))
da=(0,0,-1,2,0,0);db=(0,-2,1,0,0,0)
def ca(n,q):
    a,b,c,d,e,f=n
    return -(q-q**-1)*qi(c,q**3)*q**(3*a+b-3*c+2)
def cb(n,q):
    a,b,c,d,e,f=n
    return qi(3,q)*qi(b-1,q)*qi(b,q)*q**(3*a-b+2)
for q in (F(2),F(3)):
    for a,b,c in product(range(4),range(2,7),range(1,9)):
        n=(a,b,c,1,1,0)
        ab=cb(n,q)*ca(add(n,db),q);ba=ca(n,q)*cb(add(n,da),q)
        check(ba!=0 and ab/ba==q**-5*qi(c+1,q**3)/qi(c,q**3),'g2_composition_ratio')
check(F(2)**-5*qi(2,F(8))/qi(1,F(8))==F(65,256),'g2_exact_ratio_witness')
check(F(2)**-5*qi(3,F(8))/qi(2,F(8))==F(4161,16640),'g2_exact_ratio_witness')
check(F(65,256)!=F(4161,16640),'g2_constant_qcommutation_rejected')
roots=((0,1),(1,1),(3,2),(2,1),(3,1),(1,0))
shifts=(da,db,(0,0,0,-1,1,0),(0,0,0,0,0,1),(0,-1,0,1,0,0),(-1,1,0,0,0,0))
for step in shifts:
    check(tuple(sum(step[i]*roots[i][j] for i in range(6)) for j in range(2))==(1,0),'g2_step_weights')

print(json.dumps({'passed':True,'total_checks':sum(counts.values()),'checks_by_family':counts,'root_receipts':root_receipts,'limits':'Exact bounded algebraic diagnostics at rational q. Not proof of knot q-holonomicity, universal reconstruction, source correctness, novelty, or the full conjecture.'},sort_keys=True,indent=2))
