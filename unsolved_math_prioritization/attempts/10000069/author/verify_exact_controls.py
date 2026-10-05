#!/usr/bin/env python3
"""Finite exact-arithmetic controls; not a proof of an asymptotic theorem."""
from fractions import Fraction as F
from itertools import product, combinations_with_replacement
from collections import defaultdict
import json

checks=0

def check(v):
    global checks
    assert v
    checks+=1

def transform(law,p):
    z=defaultdict(F)
    for x,px in law.items():
        for y,py in law.items():
            z[x+y]+=p*px*py
            z[min(x,y)]+=(1-p)*px*py
    return {x:w for x,w in z.items() if w}

def moment(law,k=1):return sum((w*x**k for x,w in law.items()),F(0))
def minlaw(law):
    z=defaultdict(F)
    for x,px in law.items():
        for y,py in law.items():z[min(x,y)]+=px*py
    return z

def enumerate_tree(n,p):
    nodes=2**n-1
    z=defaultdict(F)
    for gates in product((0,1),repeat=nodes):
        def ev(i,depth):
            if depth==n:return 1
            a,b=ev(2*i+1,depth+1),ev(2*i+2,depth+1)
            return a+b if gates[i] else min(a,b)
        k=sum(gates);z[ev(0,0)]+=p**k*(1-p)**(nodes-k)
    return {x:w for x,w in z.items() if w}

parameters=[F(0),F(1,4),F(1,2),F(3,5),F(3,4),F(9,10),F(1)]
samples=[]
for p in parameters:
    laws=[{F(1):F(1)}]
    for n in range(6):laws.append(transform(laws[-1],p))
    means=[moment(l) for l in laws]
    for n,law in enumerate(laws):
        check(sum(law.values())==1)
        check(all(1<=x<=2**n and w>0 for x,w in law.items()))
        if p>F(1,2):check(moment(law,2)/means[n]**2<=1/(2*p-1))
        check(means[n]<=(1+p)**n)
        check(means[n]>=(2*p)**n)
        for k in range(7-n):check(means[n+k]<=means[n]*means[k])
        if n:
            old=laws[n-1];ml=minlaw(old)
            check(means[n]==2*p*means[n-1]+(1-p)*moment(ml))
            check(moment(law,2)==2*p*moment(old,2)+2*p*means[n-1]**2+(1-p)*moment(ml,2))
    check(laws[3]==enumerate_tree(3,p))
    check(means[2]==1+p+3*p*p-p**3)
    check(means[1]**2-means[2]==p*(1-p)**2)
    samples.append({'p':str(p),'m6':str(means[6]),'second_moment_ratio6':str(moment(laws[6],2)/means[6]**2)})

profiles=0
# Uniform atomic laws give step quantiles; include zero-valued steps deliberately.
for values in combinations_with_replacement(range(5),5):
    if not sum(values):continue
    profiles+=1
    law=defaultdict(F)
    for v in values:law[F(v)]+=F(1,5)
    M,S=moment(law),moment(law,2)
    ml=minlaw(law);A,C=moment(ml),moment(ml,2)
    check(C*M<=A*S)
    normalized={x/M:w for x,w in law.items()}
    R=moment(normalized,2)
    for p in (F(3,5),F(3,4),F(9,10)):
        out=transform(normalized,p);d=moment(out)
        check(moment(out,2)/d**2<=(R+1)/(2*p))
        for c in (F(0),F(1,4),F(2)):
            check((moment(out,2)+2*c*d+c*c)/(d+c)**2<=moment(out,2)/d**2)

# Mean-only closure is false, even on strictly positive laws.
p=F(3,4);a={F(1):F(1)};b={F(1,2):F(1,2),F(3,2):F(1,2)}
check(moment(a)==moment(b)==1)
check(moment(transform(a,p))==F(7,4))
check(moment(transform(b,p))==F(27,16))
check(moment(transform(a,p))!=moment(transform(b,p)))
# Reversed Jensen and reciprocal second-moment bound are both false.
check(moment(transform(transform(a,p),p)) < moment(transform(a,p))**2)
check(moment(a,2)/moment(a)**2 > 2*p-1)
# Constant mean-one profile is not an eigenprofile when 0<p<1.
check(len(transform(a,p))==2)
# Distinguish parallel graph distance and effective resistance at generation 1.
check(min(F(1),F(1)) != 1/(1/F(1)+1/F(1)))

print(json.dumps({'status':'PASS','arithmetic':'fractions.Fraction','assertions':checks,'parameters':[str(x) for x in parameters],'max_recursive_depth':6,'independent_tree_enumeration_depth':3,'uniform_atomic_profiles':profiles,'samples':samples,'negative_controls':['mean-only closure','reverse Jensen','reciprocal L2 bound','constant eigenprofile','resistance confused with distance'],'scope':'finite identities and counterexamples only; no simulation; not an asymptotic proof'},indent=2,sort_keys=True))
