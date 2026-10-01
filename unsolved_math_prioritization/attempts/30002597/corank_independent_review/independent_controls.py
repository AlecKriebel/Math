#!/usr/bin/env python3
"""Independent finite edge-case controls. Not a corank-algorithm implementation."""
from math import gcd
from itertools import product
import json

checks=0
def assert_ok(condition):
    global checks
    checks+=1
    assert condition

def reduce(w):
    # Repeated adjacent-pair cancellation, independently of the author's stack routine.
    w=list(w)
    while True:
        for j in range(len(w)-1):
            if w[j]==-w[j+1]:
                del w[j:j+2]
                break
        else:return tuple(w)

def inv(w):return tuple(-a for a in reversed(w))
def image(w,hom):
    result=()
    for a in w:
        x=hom[abs(a)]
        result += x if a>0 else inv(x)
    return reduce(result)
def comm(a,b):return a+b+inv(a)+inv(b)
def relator(g):return sum((comm((2*i+1,),(2*i+2,)) for i in range(g)),())
def bezout(a,b):
    oldr,r=a,b; olds,s=1,0; oldt,t=0,1
    while r:
        q=oldr//r;oldr,r=r,oldr-q*r;olds,s=s,olds-q*s;oldt,t=t,oldt-q*t
    if oldr<0:return -oldr,-olds,-oldt
    return oldr,olds,oldt

for p,q in product(range(-20,21),repeat=2):
    d=gcd(p,q)
    u,v=(q//d,-p//d) if d else (1,0)
    e,s,t=bezout(u,v)
    assert_ok(e==1 and s*u+t*v==1)
    assert_ok(p*u+q*v==0)
    word=(1 if p>=0 else -1,)*abs(p)+(2 if q>=0 else -2,)*abs(q)
    phi={1:(1 if u>=0 else -1,)*abs(u),2:(1 if v>=0 else -1,)*abs(v)}
    assert_ok(image(word,phi)==())
    assert_ok(image(relator(1),phi)==())

for g in range(1,13):
    # a_i -> 1, b_i -> free basis: gamma=a_1 still allows full target rank g.
    phi={2*i+1:() for i in range(g)}
    phi.update({2*i+2:(i+1,) for i in range(g)})
    assert_ok(len(phi)==2*g)
    assert_ok(image(relator(g),phi)==())
    assert_ok(image((1,),phi)==())
    assert_ok([phi[2*i+2] for i in range(g)]==[(i+1,) for i in range(g)])
    for c in [(),(1,2,-1),(2*g,),relator(g)]:
        w=c+(1,)*3+inv(c)
        assert_ok(image(w,phi)==())
        assert_ok(image(inv(w),phi)==())
    # Vary a nonprimitive killed word without changing the meridional mechanism.
    assert_ok(image((1,)*8,phi)==())

assert_ok(relator(0)==())
print(json.dumps({'status':'PASS','assertions':checks,'torus_homology_vectors':41**2,
                  'surface_genera':list(range(1,13)),
                  'scope':'Independent arithmetic and coefficient-free word controls only',
                  'not_tested':'Razborov implementation, general corank calculation, smooth-map construction'},indent=2))
