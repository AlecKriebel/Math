#!/usr/bin/env python3
"""Independent quotient-step integral factor construction and exact controls."""
from fractions import Fraction
import json
from random import Random


def require(ok, reason):
    if not ok:raise ValueError(reason)


def mm(a,b):return [[sum(x*y for x,y in zip(r,c)) for c in zip(*b)] for r in a]


def factor(a,b,c):
    require(all(type(x) is int and x>=0 for x in (a,b,c)) and a*c>=b*b,'integral PSD input')
    original=[[a,b],[b,c]];P=[[1,0],[0,1]];steps=0
    while min(a,c)<b:
        old_trace=a+c
        if c<a:
            a,c=c,a;P=mm(P,[[0,1],[1,0]])
        require(a>0,'zero diagonal with positive off diagonal')
        q,bnew=divmod(b,a)
        cnew=c-2*q*b+q*q*a
        a,b,c=a,bnew,cnew
        P=mm(P,[[1,0],[q,1]])
        require(min(a,b,c)>=0 and a*c>=b*b and a+c<old_trace,'quotient descent invariant')
        steps+=1
    terms=[]
    for weight,base in [(a-b,[1,0]),(b,[1,1]),(c-b,[0,1])]:
        if weight:terms.append((weight,[sum(x*y for x,y in zip(row,base)) for row in P]))
    gram=[[sum(n*v[i]*v[j] for n,v in terms) for j in range(2)] for i in range(2)]
    require(gram==original,'exact factor reconstruction')
    require(all(type(n) is int and n>0 and all(type(x) is int and x>=0 for x in v) for n,v in terms),'integral nonnegative columns')
    return steps


def run():
    exhaustive=0;maxsteps=0
    for a in range(81):
        for b in range(81):
            for c in range(81):
                if a*c>=b*b:
                    maxsteps=max(maxsteps,factor(a,b,c));exhaustive+=1
    rng=Random(30003649);large=0
    for _ in range(5000):
        a=rng.randrange(1,10**40);b=rng.randrange(10**40)
        c=(b*b+a-1)//a+rng.randrange(10**20)
        maxsteps=max(maxsteps,factor(a,b,c));large+=1
    for n in [1,2,3,10**20,10**60]:
        for t in [(0,0,n),(n,0,0),(n*n,n*(n+1),(n+1)**2),(1,n,n*n)]:factor(*t)
    for triple in [(0,1,0),(1,2,1),(-1,0,0),(Fraction(1,2),0,1)]:
        try:factor(*triple)
        except ValueError:pass
        else:raise RuntimeError('invalid input accepted')
    return {'status':'PASS','method':'quotient-step congruence, different from frozen single-step descent','exhaustive_entry_bound':80,'exhaustive_PSD_inputs':exhaustive,'large_generated_inputs':large,'additional_degenerate_rank_one_inputs':20,'invalid_inputs_rejected':4,'maximum_quotient_steps':maxsteps,'scope':'Finite corroboration only; the universal theorem follows from the separately audited induction.'}


if __name__=='__main__':print(json.dumps(run(),sort_keys=True,indent=2))
