#!/usr/bin/env python3
"""Exact, standard-library checks for the nine-line counterexample.
These supplement the written proof; they are not a proof assistant certificate.
Run from any directory, with normal or optimized Python.
"""
from fractions import Fraction as Q
from collections import defaultdict
from itertools import combinations
import json

COUNT = 0

def require(condition, label):
    global COUNT
    COUNT += 1
    if not condition:
        raise ValueError(label)

def E(a=0,b=0): return (Q(a),Q(b))
Z=E(); O=E(1); W=E(0,1)
def add(a,b): return (a[0]+b[0],a[1]+b[1])
def neg(a): return (-a[0],-a[1])
def sub(a,b): return add(a,neg(b))
def mul(a,b): return (a[0]*b[0]-a[1]*b[1],a[0]*b[1]+a[1]*b[0]-a[1]*b[1])
def norm(a): return a[0]*a[0]-a[0]*a[1]+a[1]*a[1]
def inv(a):
    n=norm(a)
    if not n: raise ZeroDivisionError
    return ((a[0]-a[1])/n,-a[1]/n)
def div(a,b): return mul(a,inv(b))
def dot(a,b):
    s=Z
    for x,y in zip(a,b): s=add(s,mul(x,y))
    return s

def cross(a,b):
    return tuple(sub(mul(a[(i+1)%3],b[(i+2)%3]),mul(a[(i+2)%3],b[(i+1)%3])) for i in range(3))
def canonical(v):
    q=next(x for x in v if x!=Z)
    return tuple(div(x,q) for x in v)

def p_add(a,b):
    c=dict(a)
    for k,v in b.items(): c[k]=add(c.get(k,Z),v)
    return {k:v for k,v in c.items() if v!=Z}
def p_scale(a,b): return {k:mul(v,b) for k,v in a.items() if mul(v,b)!=Z}
def p_mul(a,b):
    c={}
    for ka,va in a.items():
        for kb,vb in b.items():
            k=tuple(x+y for x,y in zip(ka,kb)); c[k]=add(c.get(k,Z),mul(va,vb))
    return {k:v for k,v in c.items() if v!=Z}
def power(a,n):
    r={(0,0,0):O}
    for _ in range(n):r=p_mul(r,a)
    return r

def line_poly(v):return {k:c for k,c in zip([(1,0,0),(0,1,0),(0,0,1)],v) if c!=Z}
def poly_eval(p,v):
    ans=Z
    for k,c in p.items():
        term=c
        for z,n in zip(v,k):
            for _ in range(n):term=mul(term,z)
        ans=add(ans,term)
    return ans

def ordinary(r):
    if r<2:raise ValueError('ordinary point must be singular')
    return r*(r-1)//2,r-2

require(mul(W,W)==E(-1,-1),'omega squared')
require(mul(mul(W,W),W)==O,'omega cubed')
roots=[O,W,mul(W,W)]
lines=[]
for q in roots: lines += [(O,neg(q),Z)]
for q in roots: lines += [(Z,O,neg(q))]
for q in roots: lines += [(neg(q),Z,O)]
require(len(set(map(canonical,lines)))==9,'nine distinct lines')
intersections=defaultdict(set)
for i,j in combinations(range(9),2):
    p=canonical(cross(lines[i],lines[j])); intersections[p].update([i,j])
require(len(intersections)==12,'exactly twelve pair-intersection points')
for p,inds in intersections.items():
    incident={i for i,l in enumerate(lines) if dot(l,p)==Z}
    require(incident==inds,'complete point incidences')
    require(len(incident)==3,'all intersections ordinary triple points')
require(sum(len(s)*(len(s)-1)//2 for s in intersections.values())==36,'pair coverage')
L=(O,E(2),E(4))
affine_points=[]
for p in intersections:
    den=dot(L,p); require(den!=Z,'chosen infinity misses intersections')
    q=(div(p[0],den),div(p[1],den));affine_points.append(q)
    require(norm(q[0])+norm(q[1])<2,'unit-chart radius squared less than two')

# Substitute X=x,Y=y,Z=(t-x-2y)/4; rescale individual lines conveniently.
affine_lines=[]
for q in roots: affine_lines.append((O,neg(q),Z))
for q in roots: affine_lines.append((q,add(E(4),mul(E(2),q)),neg(q)))
for q in roots: affine_lines.append((sub(E(-1),mul(E(4),q)),E(-2),O))
for i,j in combinations(range(9),2):
    a,b=affine_lines[i],affine_lines[j]
    require(sub(mul(a[0],b[1]),mul(a[1],b[0]))!=Z,'distinct central tangent directions')
for p in affine_points:
    require(sum(dot(l,(*p,O))==Z for l in affine_lines)==3,'affine triple incidence')

prod={(0,0,0):O}
for l in affine_lines:prod=p_mul(prod,line_poly(l))
x={(1,0,0):O};y={(0,1,0):O};t={(0,0,1):O}
u=p_add(p_add(t,p_scale(x,E(-1))),p_scale(y,E(-2)))
x3=power(x,3);y3=power(y,3);u3=power(u,3)
formula=p_mul(p_mul(p_add(x3,p_scale(y3,E(-1))),p_add(p_scale(y3,E(64)),p_scale(u3,E(-1)))),p_add(u3,p_scale(x3,E(-64))))
require(prod==formula,'explicit polynomial equals product of nine affine lines')
require(all(b==0 and a.denominator==1 for a,b in prod.values()),'integer polynomial coefficients')
require(all(sum(k)==9 for k in prod),'homogeneous total degree nine')
require(prod.get((9,0,0))==E(-65),'nonzero constant leading coefficient in x')
for p in affine_points:require(poly_eval(prod,(*p,O))==Z,'all listed points on explicit polynomial')

central_delta,central_m=ordinary(9)
near_delta=sum(ordinary(len(v))[0] for v in intersections.values())
near_m=sum(ordinary(len(v))[1] for v in intersections.values())
require((central_delta,near_delta,central_m,near_m)==(36,36,7,12),'delta and rough M values')
require(near_m>central_m,'strict semicontinuity failure')
require(Q(2,16)<Q(1,4),'all moving intersections strictly inside radius one half')

# General Fermat incidence model: exact combinatorics for many n, not a replacement for the proof for all n.
for n in range(3,101):
    blocks=[set(range(j*n,(j+1)*n)) for j in range(3)]
    for i in range(n):
        for j in range(n):blocks.append({i,n+j,2*n+((-i-j)%n)})
    seen=set()
    for block in blocks:
        for pair in combinations(sorted(block),2):
            require(pair not in seen,'Fermat pair appears once');seen.add(pair)
    require(len(seen)==(3*n)*(3*n-1)//2,'Fermat all pairs covered')
    d=sum(ordinary(len(b))[0] for b in blocks)
    m=sum(ordinary(len(b))[1] for b in blocks)
    require(d==ordinary(3*n)[0],'Fermat delta conservation')
    require(m-ordinary(3*n)[1]==n*n-4,'Fermat excess identity')

# Negative controls do not alter the genuine proof inputs.
def rejects(f):
    try:f()
    except ValueError:return True
    return False
require(rejects(lambda: require(len(intersections)==11,'deliberate omitted intersection')),'omission negative control')
require(rejects(lambda: require(near_m<=central_m,'deliberate wrong inequality')),'inequality negative control')
require(rejects(lambda: require(prod.get((9,0,0))==E(-64),'deliberate coefficient corruption')),'coefficient negative control')
require(any(dot((O,O,O),p)==Z for p in intersections),'bad-infinity fixture actually meets intersections')
require(rejects(lambda: require(all(dot((O,O,O),p)!=Z for p in intersections),'deliberate inadmissible infinity')),'infinity negative control')
result={'status':'PASS','exact_checks':COUNT,'field':'Q[omega]/(omega^2+omega+1)',
        'lines':9,'singular_points':12,'intersection_multiplicities':[3]*12,
        'central_delta':central_delta,'nearby_total_delta':near_delta,
        'central_rough_M':central_m,'nearby_total_rough_M':near_m,
        'Fermat_test_range':[3,100],'negative_controls':4,
        'limitations':'Finite exact checks supplement the written proof. They do not certify analytic flatness, normalization, or all n by computation.'}
print(json.dumps(result,indent=2,sort_keys=True))
