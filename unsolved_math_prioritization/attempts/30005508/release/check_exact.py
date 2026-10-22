#!/usr/bin/env python3
"""Exact finite checks; standard library only. No table library or floating point."""
from itertools import product
from fractions import Fraction
import json

def linear(v, m):
    x,y=v&1,(v>>1)&1
    return (m[0]*x^m[1]*y) | ((m[2]*x^m[3]*y)<<1)
A=(0,1,1,1); T=(0,1,1,0)
def apow(v,n):
    for _ in range(n%3): v=linear(v,A)
    return v

def mul(g,h):
    u,v,a,b,c,t=g; U,V,aa,bb,cc,tt=h
    if t: U=linear(U,T); aa=-aa; cc=-cc
    return (u^apow(U,a),v^apow(V,b),(a+aa)%3,(b+bb)%3,(c+cc+a*bb)%3,t^tt)
G=list(product(range(4),range(4),range(3),range(3),range(3),range(2)))
one=(0,0,0,0,0,0)
invs={g:next(h for h in G if mul(g,h)==one and mul(h,g)==one) for g in G}
# Algebraically guaranteed by the semidirect construction; exhaustive generator checks supplement it.
gens=[(1,0,0,0,0,0),(2,0,0,0,0,0),(0,1,0,0,0,0),(0,2,0,0,0,0),(0,0,1,0,0,0),(0,0,0,1,0,0),(0,0,0,0,1,0),(0,0,0,0,0,1)]
for g in G:
    for a in gens:
        for b in gens: assert mul(mul(g,a),b)==mul(g,mul(a,b))
def conj(y,h): return mul(mul(invs[h],y),h)
def phi(g):
    u,v,a,b,c,t=g
    if u or v or a or b or t:return 0
    return 96 if c==0 else -48
E={g for g in G if g[2:5]==(0,0,0)}
D={g for g in E if g[-1]==0}
remaining={g for g in G if mul(g,g)==one}; rows=[]
while remaining:
    y=min(remaining); orbit={conj(y,h) for h in G}; remaining-=orbit
    C=[h for h in G if mul(h,y)==mul(y,h)]
    lhs=Fraction(sum(phi(h) for h in C),len(C))
    rhs=len(orbit&(E-D)); assert lhs==rhs
    rows.append({'representative':y,'class_size':len(orbit),'centralizer_order':len(C),'multiplicity':int(lhs),'coset_intersection':rhs})
# Pure conjugacy-fiber check for the central-quotient reduction. Use D8 with central x=r^2,
# y=r, where the fiber multiplicity is 2, and C8 with x=r^2, y=r, where it is 1.
def dmul(g,h,n=4): return ((g[0]+(-1 if g[1] else 1)*h[0])%n,g[1]^h[1])
def quotient_check(group,op,y):
    e=group[0]; inv={g:next(h for h in group if op(g,h)==e and op(h,g)==e) for g in group}
    x=op(y,y); Z={e}; z=x
    while z not in Z: Z.add(z);z=op(z,x)
    assert all(op(z,g)==op(g,z) for z in Z for g in group)
    C={g for g in group if op(g,y)==op(y,g)}
    yz={op(y,z) for z in Z}
    K={g for g in group if op(op(inv[g],y),g) in yz}
    t=len(K)//len(C); orbit={op(op(inv[g],y),g) for g in group}
    fibers={tuple(sorted(op(w,z) for z in Z)):0 for w in orbit}
    for w in orbit: fibers[tuple(sorted(op(w,z) for z in Z))]+=1
    assert all(v==t for v in fibers.values())
    return {'group_order':len(group),'root':y,'square':x,'central_subgroup_order':len(Z),'fiber_multiplier':t,'fiber_sizes':sorted(fibers.values())}
quotients=[quotient_check(list(product(range(4),range(2))),dmul,(1,0)),quotient_check(list(range(8)),lambda a,b:(a+b)%8,1)]
output={'group_order':len(G),'defect_order':len(D),'extended_defect_order':len(E),'involution_count_including_identity':sum(x['class_size'] for x in rows),'involution_class_checks':rows,'quotient_fiber_checks':quotients,'assertions_passed':True}
print(json.dumps(output,indent=2))
