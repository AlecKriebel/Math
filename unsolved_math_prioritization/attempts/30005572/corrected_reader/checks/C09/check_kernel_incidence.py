#!/usr/bin/env python3
"""Finite checks supporting the authored integral correspondence proof.

These tests do not prove the motivic or geometric assertions. All arithmetic
is exact; no third-party library or external data is used.
"""
from itertools import product
import json


def field(p, degree=1):
    q = p**degree
    if degree == 1:
        return q, lambda a,b:(a+b)%p, lambda a,b:a*b%p
    assert (p,degree)==(5,2)
    # F_25=F_5[t]/(t^2-2); 2 is a nonsquare modulo 5.
    def add(a,b):
        return ((a%5+b%5)%5)+5*((a//5+b//5)%5)
    def mul(a,b):
        a0,a1=a%5,a//5; b0,b1=b%5,b//5
        return (a0*b0+2*a1*b1)%5+5*((a0*b1+a1*b0)%5)
    return q,add,mul


def incidence(p, degree=1):
    q, add, mul = field(p,degree)
    vectors=list(product(range(q),repeat=2))
    lines=[{(t,mul(a,t)) for t in range(q)} for a in range(q)]
    lines.append({(0,t) for t in range(q)})
    assert len({frozenset(x) for x in lines})==q+1
    multiplicity={v:sum(v in d for d in lines) for v in vectors}
    assert multiplicity[(0,0)]==q+1
    assert all(multiplicity[v]==1 for v in vectors if v!=(0,0))
    # Every coefficient of sum_D [D] - q[0] - [V] is zero.
    defect={v:multiplicity[v]-1-q*(v==(0,0)) for v in vectors}
    assert not any(defect.values())
    return {'q':q,'lines':len(lines),'vectors':len(vectors),
            'origin_multiplicity':q+1,'nonzero_multiplicity':1,
            'correspondence_defect_zero':True}


def transfer_check():
    p=5
    G=[(a,b,c,d) for a,b,c,d in product(range(p),repeat=4)
       if (a*d-b*c)%p==1]
    one=(1,0,0,1)
    def mm(x,y):
        a,b,c,d=x; e,f,g,h=y
        return ((a*e+b*g)%p,(a*f+b*h)%p,
                (c*e+d*g)%p,(c*f+d*h)%p)
    def inv(x):
        a,b,c,d=x; return d,(-b)%p,(-c)%p,a
    def mv(x,v):
        a,b,c,d=x; u,w=v
        return ((a*u+b*w)%p,(c*u+d*w)%p)
    H={g for g in G if g[2]==0}
    reps=[]; seen=set()
    for g in sorted(G,key=lambda x:(x!=one,x)):
        if g not in seen:
            reps.append(g); seen.update(mm(g,h) for h in H)
    assert len(G)==120 and len(H)==20 and len(reps)==6 and seen==set(G)
    decompositions={mm(r,h):(r,h) for r in reps for h in H}
    V=list(product(range(p),repeat=2)); pos={v:i for i,v in enumerate(V)}
    zero=[0]*len(V)
    def plus(a,b): return [x+y for x,y in zip(a,b)]
    def minus(a,b): return [x-y for x,y in zip(a,b)]
    def ga(g,w):
        out=zero.copy()
        for v,x in zip(V,w): out[pos[mv(g,v)]]=x
        return out
    def nk(w):
        out=zero.copy()
        for a in range(p):
            for (u,v),x in zip(V,w): out[pos[((u+a)%p,v)]]+=x
        return out
    def nr(r,w): return ga(r,nk(ga(inv(r),w)))
    seed=[(u+2*v)**2+3*u*v-4*v for u,v in V]
    z={g:minus(ga(g,seed),seed) for g in G}
    correction=zero.copy()
    for r in reps: correction=plus(correction,nr(r,z[r]))
    for g in G:
        lhs=zero.copy()
        for r in reps:
            rp,h=decompositions[mm(g,r)]
            lhs=plus(lhs,ga(rp,nk(z[h])))
        rhs=zero.copy()
        for r in reps: rhs=plus(rhs,nr(r,z[g]))
        rhs=plus(rhs,minus(ga(g,correction),correction))
        assert lhs==rhs
    # Check endomorphism incidence on every basis vector, not just this z.
    for v in V:
        w=zero.copy(); w[pos[v]]=1
        actual=zero.copy()
        for r in reps: actual=plus(actual,nr(r,w))
        expected=[1+p*(x==v) for x in V]
        assert actual==expected
    # Non-Cartesian defect on [0]: 5[0]-[K] is genuinely nonzero.
    nc={v:p*(v==(0,0))-int(v[1]==0) for v in V}
    assert nc[(0,0)]==4 and sum(nc.values())==0
    assert sum(x!=0 for x in nc.values())==5
    return {'group':'SL2(F5)','group_order':len(G),'line_stabilizer_order':len(H),
            'index':len(reps),'cocycle_arguments_checked':len(G),
            'transfer_coboundary_identity':True,
            'kernel_incidence_basis_vectors_checked':len(V),
            'noncartesian_zero_cycle_defect_nonzero':True,
            'noncartesian_defect_support':sum(x!=0 for x in nc.values()),
            'limitations':'The cocycle used for the finite test is principal in the permutation module. The general cochain identity is proved algebraically in the note.'}

result={'incidence':[incidence(5),incidence(5,2),incidence(7)],
        'transfer':transfer_check(),
        'status':'all exact finite checks passed'}
print(json.dumps(result,indent=2,sort_keys=True))
