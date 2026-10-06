#!/usr/bin/env python3
"""Independent finite diagnostics; no import of author code and no manifold recognizer."""
import itertools
import json
from fractions import Fraction
from math import comb

CHECKS = 0

def check(value, label):
    global CHECKS
    CHECKS += 1
    if not value:
        raise RuntimeError(label)

def verts(k):
    return set().union(*map(set, k))

def faces(k, size):
    return {tuple(c) for f in k for c in itertools.combinations(f, size)}

def boundary(k):
    n = len(next(iter(k))) - 1
    counts = {}
    for f in k:
        for c in itertools.combinations(f, n):
            counts[c] = counts.get(c, 0) + 1
    check(set(counts.values()) <= {1, 2}, 'ridge incidence')
    return {f for f, count in counts.items() if count == 1}

def split(k):
    remaining = verts(k)
    out = []
    while remaining:
        part = {min(remaining)}
        change = True
        while change:
            old = set(part)
            for f in k:
                if part.intersection(f):
                    part.update(f)
            change = part != old
        out.append(part)
        remaining.difference_update(part)
    return out

def g(k):
    d = len(next(iter(k)))
    return len(faces(k, 2)) - d * len(verts(k)) + comb(d + 1, 2)

def gamma(k):
    d = len(next(iter(k)))
    bd = boundary(k)
    check(bool(bd), 'boundary domain')
    v, e = len(verts(k)), len(faces(k, 2))
    i = v - len(verts(bd))
    f = [1] + [len(faces(k, j)) for j in range(1, d + 1)]
    h = [sum((-1)**(j-r)*comb(d-r, d-j)*f[r] for r in range(j+1)) for j in range(d+1)]
    check(h[d-1] + d*h[d] == i, 'interior-vertex h identity')
    value = e - (d-1)*v + comb(d, 2) - i
    check(value == h[2]-i, 'h2 definition')
    return value

def simplex_boundary(n):
    return set(itertools.combinations(range(n+2), n+1))

def cross_boundary(n):
    return {tuple(2*j+s for j, s in enumerate(signs)) for signs in itertools.product((0,1), repeat=n+1)}

def stellar(k, f):
    v = max(verts(k)) + 1
    out = set(k)
    out.remove(f)
    out.update(tuple(sorted(set(f)-{u}|{v})) for u in f)
    return out, v

def protect_inner(k, forbidden):
    start = min(set(k) - set(forbidden))
    chosen = start
    d = len(start)
    coordinates = {v: tuple(Fraction(int(j==l)) for l in range(d)) for j,v in enumerate(start)}
    oldg = g(k)
    for omit in start:
        mean = tuple(sum(coordinates[v][j] for v in chosen)/d for j in range(d))
        k, new = stellar(k, chosen)
        coordinates[new] = mean
        chosen = tuple(sorted(set(chosen)-{omit}|{new}))
        check(g(k)==oldg, 'stellar g2 preservation')
        check(chosen in k, 'selected facet exists')
    check(set(chosen).isdisjoint(verts(forbidden)) if forbidden else True, 'protected vertex disjointness')
    check(all(t>0 for v in chosen for t in coordinates[v]), 'strict barycentric interior')
    return k, chosen

def cap(k):
    bd = boundary(k)
    out = set(k)
    fresh = max(verts(k))+1
    for part in split(bd):
        out.update(tuple(sorted((*f, fresh))) for f in bd if set(f)<=part)
        fresh += 1
    return out

def glue(k,l,boundary_mode):
    left = min(boundary(k) if boundary_mode else k)
    right = min(boundary(l) if boundary_mode else l)
    mapping = dict(zip(right,left))
    fresh=max(verts(k))+1
    for v in sorted(verts(l)-set(right)):
        mapping[v]=fresh
        fresh+=1
    lnew={tuple(sorted(mapping[v] for v in f)) for f in l if boundary_mode or f!=right}
    return (set(k) if boundary_mode else set(k)-{left}) | lnew

def product(n):
    out=set()
    for base in itertools.combinations(range(n+1), n):
        for pivot in base:
            out.add(tuple(sorted([2*u for u in base if u<=pivot]+[2*u+1 for u in base if u>=pivot])))
    return out

def rank(columns):
    basis={}
    for col in columns:
        while col:
            lead=max(col)
            if lead in basis:
                col.symmetric_difference_update(basis[lead])
            else:
                basis[lead]=set(col)
                break
    return len(basis)

def betti(k):
    d=len(next(iter(k)))
    levels=[None]+[faces(k,j) for j in range(1,d+1)]
    ranks=[0]*(d+2)
    for j in range(2,d+1):
        ranks[j]=rank([set(itertools.combinations(f,j-1)) for f in levels[j]])
    return [len(levels[j])-ranks[j]-ranks[j+1] for j in range(1,d+1)]

def run():
    puncture_rows=[]
    for n in range(3,7):
        for label,k in [('simplex sphere',simplex_boundary(n)),('cross-polytope sphere',cross_boundary(n))]:
            expected = 0 if label=='simplex sphere' else (n+1)*(n-2)//2
            check(g(k)==expected,'starting g2')
            protected=set()
            for b in range(1,5):
                k,f=protect_inner(k,protected)
                protected.add(f)
                p=k-protected
                check(len(verts(p))==len(verts(k)),'puncture retains vertices')
                check(faces(p,2)==faces(k,2),'puncture retains edges')
                check(len(verts(boundary(p)))==b*(n+1),'boundary vertices')
                check(len(split(boundary(p)))==b,'boundary components')
                value=gamma(p)
                check(value==expected+(n+1)*(b-1),'simultaneous puncture identity')
                q=cap(p)
                check(not boundary(q),'separate caps close')
                check(g(q)==expected,'cap normalization')
                if n==3:
                    check(betti(p)==[1,0,b-1,0],'punctured 3-sphere homology')
                puncture_rows.append({'n':n,'family':label,'b':b,'closed_g2':expected,'gamma':value})
    product_rows=[]
    for n in range(3,8):
        c=product(n)
        check(len(verts(c))==2*(n+1),'product vertices')
        check(len(faces(c,2))==3*comb(n+1,2)+(n+1),'product edges')
        check(gamma(c)==n+1,'cylinder gamma')
        check(g(cap(c))==0,'cylinder cap')
        ball={tuple(range(n+1))}
        check(gamma(ball)==0,'ball gamma')
        check(gamma(glue(c,ball,True))==n+1,'boundary sum normalization')
        check(gamma(c)!=gamma(ball)+gamma(ball),'reject literal interior additivity')
        cross=cross_boundary(n)
        check(g(glue(cross,cross,False))==2*g(cross),'positive g2 connected sum')
        product_rows.append({'n':n,'gamma':gamma(c),'f0':len(verts(c)),'f1':len(faces(c,2))})
    separator_rows=[]
    for n in range(3,8):
        for label,s in [('simplex',simplex_boundary(n-1)),('cross-polytope',cross_boundary(n-1))]:
            for subdivision in range(3):
                u=max(verts(s))+1
                a={tuple(sorted((*f,u))) for f in s}
                b={tuple(sorted((*f,u+1))) for f in s}
                k=a|b
                s0,s1=len(verts(s)),len(faces(s,2))
                defect=s1-(n-1)*s0+comb(n+1,2)-(n+1)
                check(defect==g(s)+s0-(n+1),'separator algebra')
                check(g(cap(a))+g(cap(b))==g(k)+defect,'separator actual complexes')
                if n==3:check(defect==s0-4,'Euler 2-sphere loss')
                separator_rows.append({'n':n,'family':label,'subdivisions':subdivision,'g2_separator':g(s),'vertices':s0,'defect':defect})
                s,_=stellar(s,min(s))
    for n in range(3,21):
        for b in range(1,9):
            v,i,e=99,7,1201
            gamma_value=e-n*v+comb(n+1,2)-i
            capped=e+v-i-(n+1)*(v+b)+comb(n+2,2)
            check(capped==gamma_value-(n+1)*(b-1),'formal cap polynomial identity')
    return {'result':'PASS','checks':CHECKS,'scope':'Independent finite counts and exact barycentric coordinates; universal topology and lower bounds are human-reviewed, not formalized.','punctures':puncture_rows,'products':product_rows,'separators':separator_rows}

if __name__=='__main__':
    print(json.dumps(run(),indent=2,sort_keys=True))
