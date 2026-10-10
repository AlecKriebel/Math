#!/usr/bin/env python3
"""Independent exact finite checks. Does not calculate invariant functionals."""
import hashlib, itertools, json, sys
from pathlib import Path
from fractions import Fraction
import sympy as sp  # Loaded by the version-pinned isolated adapter.
S={'A':(0,2),'B':(1,4),'C':(3,3),'D':(2,5),'E':(4,6)}

def prec(a,b):
    return a[0]<b[0]<=a[1]+1 and a[1]<b[1]

def ladder(labels):
    return all(not (S[x][0]<=S[y][0] and S[y][1]<=S[x][1])
               for x,y in itertools.permutations(labels,2))

def lc_data(m,n):
    X=[(a,b) for a in m for b in n if prec(S[a],S[b])]
    Y=[(a,b) for a in m for b in n if prec(tuple(t-1 for t in S[a]),S[b])]
    adj={x:[y for y in Y if (x[0]==y[0] and prec(S[y[1]],S[x[1]])) or
         (x[1]==y[1] and prec(S[x[0]],S[y[0]]))] for x in X}
    return X,Y,adj

def hall():
    out=[]
    for r in (1,2):
        for m in itertools.combinations(S,r):
            n=tuple(t for t in S if t not in m)
            if not (ladder(m) or ladder(n)):
                raise RuntimeError('Missing ladder hypothesis')
            witnesses=[]
            for l,r in ((m,n),(n,m)):
                X,Y,adj=lc_data(l,r)
                isolated=[x for x in X if not adj[x]]
                if isolated:
                    witnesses.append({'directed_LC':[''.join(l),''.join(r)],'X':X,'Y':Y,'isolated_X_vertices':isolated})
            if not witnesses: raise RuntimeError('No singleton obstruction')
            out.append({'partition':[''.join(m),''.join(n)],'ladder_sides':[''.join(t) for t in (m,n) if ladder(t)],'witnesses':witnesses})
    if len(out)!=15: raise RuntimeError('Partition coverage')
    return out

# Independently obtain pair L exponents from the Clebsch-Gordan decomposition
# of the two special Weil-Deligne representations. The highest weights of
# Sp_r tensor Sp_s are r+s-2, r+s-4, ..., abs(r-s).
def wd_exponents(a,b):
    r=a[1]-a[0]+1; s=b[1]-b[0]+1
    center=Fraction(sum(a)-sum(b),2)
    return [int(center+Fraction(k,2)) for k in range(r+s-2,abs(r-s)-1,-2)]

z=sp.Symbol('z')
def gamma(a,b,chi,q):
    return sp.prod(1-chi*sp.Rational(q)**(-e)*z for e in wd_exponents(a,b))/sp.prod(1-chi*sp.Rational(q)**(-1-e)/z for e in wd_exponents(b,a))

def valuation_at_one(f):
    num,den=sp.fraction(sp.cancel(f))
    def mult(p):
        p=sp.Poly(p,z); v=0
        while p.eval(1)==0:
            p=sp.div(p,sp.Poly(z-1,z))[0];v+=1
        return v
    return mult(num)-mult(den)

def scalars():
    out=[]
    for kind,pairs in [('linked',[('E','D'),('D','B'),('B','A'),('E','C'),('C','A')]),('nested',[('D','C'),('C','B')])]:
        for a,b in pairs:
            for chi in (1,-1):
                f=sp.cancel(gamma(S[b],S[a],chi,3).subs(z,1/z)/gamma(S[a],S[b],chi,3))
                v=valuation_at_one(f); lim=sp.limit(f,z,1)
                expected=0 if chi==-1 or kind=='nested' else (1 if len(wd_exponents(S[a],S[b]))==1 else 2)
                if v!=expected: raise RuntimeError('Bad scalar valuation')
                if v==0 and lim in (0,sp.oo,-sp.oo,sp.zoo): raise RuntimeError('Bad unit')
                out.append({'kind':kind,'pair':[a,b],'character_at_3':chi,'forward_L_exponents':wd_exponents(S[a],S[b]),'reverse_L_exponents':wd_exponents(S[b],S[a]),'coefficient_valuation':v,'coefficient_limit_up_to_epsilon_unit':str(lim)})
            if kind=='nested':
                for a,b in ((a,b),(b,a)):
                    g=gamma(S[a],S[b],1,9)
                    if valuation_at_one(g)!=0: raise RuntimeError('Bad E-side gamma')
    return out

orders=['EDCBA','ECDBA','EDBCA']
order_checks=[]
for order in orders:
    flo_bad=[];lm_bad=[]
    for a,b in itertools.combinations(order,2):
        if S[a][0]<=S[b][0]<=S[a][1]<=S[b][1]: flo_bad.append([a,b])
        if prec(S[a],S[b]):lm_bad.append([a,b])
    if flo_bad or lm_bad:raise RuntimeError('Invalid order')
    order_checks.append({'order':order,'FLO_forbidden_pairs':flo_bad,'LM_forbidden_pairs':lm_bad})
edges=[('E','D'),('D','B'),('B','A'),('A','C'),('C','E')]
survivors=[]
for v in itertools.product((0,1),repeat=4):
    d=dict(zip('DCBA',v));d['E']=0
    if all(d[a]!=d[b] for a,b in edges): survivors.append(d)
if survivors:raise RuntimeError('Parity obstruction absent')
# Positive source-relation controls make wrong orientation/shift detectable even
# if an erroneous graph happens to retain some isolated Hall witnesses.
_, shift_Y, _=lc_data(('D',),('E',))
if ('D','E') not in shift_Y:
    raise RuntimeError('SHIFT_DIRECTION: D shifted left must precede E')
cal_X, cal_Y, cal_adj=lc_data(('A',),('B','D'))
if ('A','B') not in cal_adj.get(('A','D'),[]):
    raise RuntimeError('MATCHING_ORIENTATION: Y(A,B) must cover X(A,D)')
report={'audit_kind':'INDEPENDENT_FINITE_CHECKS_NOT_HOM_COMPUTATION','degree':sum(b-a+1 for a,b in S.values()),'partitions':hall(),'orders':order_checks,'scalar_checks':scalars(),'parity_survivors':survivors}
print(json.dumps(report, indent=2, sort_keys=True))
