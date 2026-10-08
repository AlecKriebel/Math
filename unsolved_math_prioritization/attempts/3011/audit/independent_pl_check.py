#!/usr/bin/env python3
"""Exact independent group-valued check; does not import the supplied checker.

The increasing interval PL group is noncommutative. This compares actual maps,
not just free-word encodings, under shrinking, simplex recursion, and factorization.
"""
from fractions import Fraction as Q
import itertools
import json
import sys


def need(ok, message):
    if not ok:
        raise RuntimeError(message)


ID = ((Q(-1),Q(-1)),(Q(1),Q(1)))


def ev(h,x):
    for (a,b),(c,d) in zip(h,h[1:]):
        if a<=x<=c:
            return b+(x-a)*(d-b)/(c-a)
    raise RuntimeError('outside domain')


def reduce(h):
    rows=[]
    for p in h:
        if rows and rows[-1]==p:continue
        rows.append(p)
        while len(rows)>=3:
            a,b,c=rows[-3:]
            if (b[1]-a[1])*(c[0]-b[0]) != (c[1]-b[1])*(b[0]-a[0]):break
            rows.pop(-2)
    return tuple(rows)


def inv(h):
    return tuple((y,x) for x,y in h)


def compose(f,g):
    gi=inv(g)
    xs=sorted(set([x for x,y in g]+[ev(gi,x) for x,y in f]))
    return reduce([(x,ev(f,ev(g,x))) for x in xs])


def alpha(t,h):
    if t==0:return ID
    return reduce([ID[0]]+[(t*x,t*y) for x,y in h]+[ID[1]])


def distance(h,g):
    return max(abs(ev(h,x)-ev(g,x)) for x in set([x for x,y in h]+[x for x,y in g]))


def interpol(vertices,p):
    if len(vertices)==1 or p[0]==1:return vertices[0]
    t=1-p[0]
    tail=interpol(vertices[1:],[x/t for x in p[1:]])
    return compose(alpha(t,compose(tail,inv(vertices[0]))),vertices[0])


def product(vertices,p,reverse=True):
    h=ID
    order=range(len(vertices)-1,-1,-1) if reverse else range(len(vertices))
    for j in order:
        s=sum(p[j:]);u=sum(p[j+1:])
        factor=compose(inv(alpha(u,vertices[j])),alpha(s,vertices[j]))
        h=compose(h,factor)
    return h


def main():
    family=[reduce([(Q(-1),Q(-1)),(Q(-1,3),Q(a,7)),(Q(1,2),Q(b,7)),(Q(1),Q(1))])
            for a,b in [(-5,2),(-4,3),(-2,5),(0,4),(-6,-1)]]
    need(compose(family[0],family[1])!=compose(family[1],family[0]),'family accidentally commutes')
    counts={'group_cases':0,'simplex_cases':0,'order_distinguished':0,'zero_face_cases':0}
    scales=[Q(0),Q(1,5),Q(2,3),Q(1)]
    for f,g in itertools.product(family,repeat=2):
        need(compose(f,inv(f))==ID,'inverse failure')
        for s,t in itertools.product(scales,repeat=2):
            need(alpha(s,alpha(t,f))==alpha(s*t,f),'semigroup failure')
            need(alpha(t,compose(f,g))==compose(alpha(t,f),alpha(t,g)),'homomorphism failure')
            need(distance(alpha(t,f),alpha(t,g))==t*distance(f,g),'metric failure')
            counts['group_cases']+=1
    for m in range(1,7):
        vertices=[family[(2*j+m)%len(family)] for j in range(m+1)]
        weights=[[Q(1,m+1)]*(m+1),[Q(2*j+1,(m+1)**2) for j in range(m+1)],
                 [Q(0)]+[Q(1,m)]*m,[Q(1)]+[Q(0)]*m]
        if m>1:weights.append([Q(1,2)]+[Q(0)]*(m-1)+[Q(1,2)])
        for p in weights:
            actual=interpol(vertices,p)
            need(actual==product(vertices,p),'actual noncommutative factor mismatch')
            center=family[-1]
            need(distance(actual,center)<=(2*m+1)*max(distance(v,center) for v in vertices),'control bound failure')
            active=[(v,w) for v,w in zip(vertices,p) if w]
            need(actual==interpol([v for v,w in active],[w for v,w in active]),'zero-face failure')
            counts['simplex_cases']+=1
            counts['zero_face_cases']+=int(any(w==0 for w in p))
            counts['order_distinguished']+=int(actual!=product(vertices,p,False))
    need(counts['order_distinguished']>0,'reverse-order negative control ineffective')
    print(json.dumps({'status':'passed','optimization':sys.flags.optimize,'arithmetic':'exact fractions',
                      'implementation':'independent actual PL maps, no imported original code','counts':counts},indent=2,sort_keys=True))


if __name__=='__main__':main()
