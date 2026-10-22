#!/usr/bin/env python3
"""Exact finite controls for the partial 6j/TQFT investigation.

No network, third-party packages, floating-point acceptance, or dataset inputs.
These tests support the written lemmas; they do not solve the general target.
"""
from fractions import Fraction as F
from itertools import product
from math import gcd, prod
import json
from pathlib import Path

checks = {}


def matmul(a,b):
    return [[sum((a[i][k]*b[k][j] for k in range(len(b))), F(0))
             for j in range(len(b[0]))] for i in range(len(a))]


def vecmul(a,v):
    return [sum((a[i][j]*v[j] for j in range(len(v))),F(0)) for i in range(len(a))]


def convolution(u,v,labels):
    out=[F(0)]*len(labels)
    index={x:i for i,x in enumerate(labels)}
    for i,x in enumerate(labels):
        for j,y in enumerate(labels):
            out[index[tuple((a+b)%2 for a,b in zip(x,y))]] += u[i]*v[j]
    return out


def torus_controls():
    labels=list(product(range(2),repeat=2))
    I=[[F(i==j) for j in range(4)] for i in range(4)]
    out={}
    for kind in ['toric_code','double_semion']:
        def bichar(x,y):
            e=x[0]*y[1]+x[1]*y[0] if kind=='toric_code' else x[0]*y[0]+x[1]*y[1]
            return (-1)**e
        S=[[F(bichar(x,y),2) for y in labels] for x in labels]
        assert matmul(S,S)==I
        ps=[[S[i][j]/2 for i in range(4)] for j in range(4)]
        assert [sum(p[i] for p in ps) for i in range(4)]==I[0]
        for j,p in enumerate(ps):
            assert p[0]==F(1,4)
            assert [2*x for x in vecmul(S,p)]==I[j]
            for k,q in enumerate(ps):
                assert convolution(p,q,labels)==(p if j==k else [F(0)]*4)
        # T is encoded by exponents of i, avoiding approximate complex numbers.
        twist=[(2*a*b)%4 if kind=='toric_code' else (a-b)%4 for a,b in labels]
        out[kind]={'rank':4,'primitive_idempotents':4,'trace_weights':['1/4']*4,
                   'twist_exponents_mod_4':twist}
    assert sorted(out['toric_code']['twist_exponents_mod_4'])!=sorted(out['double_semion']['twist_exponents_mod_4'])
    out['negative_control']='Both torus dimensions equal 4; twist spectra differ exactly.'
    return out


def s3_control():
    chars=[[1,1,1],[1,-1,1],[2,0,-1]]
    sizes=[1,3,2]
    inner=lambda u,v:sum(F(w*x*y,6) for w,x,y in zip(sizes,u,v))
    for i in range(3):
        for j in range(3):assert inner(chars[i],chars[j])==int(i==j)
    fusion=[]
    for u in chars:
        row=[]
        for v in chars:
            coefficients=[inner([x*y for x,y in zip(u,v)],w) for w in chars]
            assert all(x.denominator==1 and x>=0 for x in coefficients)
            assert u[0]*v[0]==sum(c*w[0] for c,w in zip(coefficients,chars))
            row.append([int(x) for x in coefficients])
        fusion.append(row)
    assert fusion[2][2]==[1,1,1] and fusion[1][1]==[1,0,0]
    assert sum(x[0]**2 for x in chars)==6
    return {'Vec_S3_rank':6,'Rep_S3_rank':3,'common_global_dimension':6,'Rep_S3_fusion':fusion}


def partitions(n,lo=1):
    if n==0:
        yield ()
    for k in range(lo,n+1):
        for tail in partitions(n-k,k):yield (k,)+tail


def factor(n):
    result={};p=2
    while p*p<=n:
        while n%p==0:result[p]=result.get(p,0)+1;n//=p
        p+=1
    if n>1:result[n]=result.get(n,0)+1
    return result


def ilog(n,p):
    k=0
    while n>1:
        assert n%p==0
        n//=p;k+=1
    return k


def abelian_controls():
    count=0;direct_counts=0;distinct_signatures={}
    for order in range(1,65):
        fac=factor(order); primes=list(fac)
        for parts in product(*(list(partitions(fac[p])) for p in primes)):
            elementary=tuple((p,part) for p,part in zip(primes,parts))
            cyclic=[p**e for p,part in elementary for e in part]
            assert prod(cyclic)==order
            signature=[F(1,order)]
            for p,E in fac.items():
                a=[1]
                for k in range(1,E+1):
                    direct=sum(1 for x in product(*(range(n) for n in cyclic))
                               if all((p**k)*v%n==0 for v,n in zip(x,cyclic)))
                    formula=prod(gcd(n,p**k) for n in cyclic)
                    assert direct==formula;direct_counts+=1
                    a.append(direct);signature.append(F(direct,order))
                r=[ilog(a[k]//a[k-1],p) for k in range(1,E+1)]+[0]
                recovered=tuple(k for k in range(1,E+1) for _ in range(r[k-1]-r[k]))
                expected=dict(elementary)[p]
                assert recovered==expected
            sig=tuple(signature)
            assert sig not in distinct_signatures or distinct_signatures[sig]==elementary
            distinct_signatures[sig]=elementary;count+=1
    assert F(gcd(4,2),4)==F(1,2)
    assert F(gcd(2,2)**2,4)==1
    return {'max_group_order':64,'abelian_isomorphism_types':count,'direct_torsion_counts':direct_counts,
            'negative_control_C4_vs_C2xC2_L2':['1/2','1']}


def cyclic_cocycle_controls():
    primes=[2,3,5,7,11,13,17,19,23,29]
    cocycle_checks=0;lens_checks=0;pair_checks=0;out=[]
    def exponent(p,u,a,b,c):return (u*a*((b+c)//p))%p
    for p in primes:
        if p<=7:
            for u,a,b,c,d in product(range(p),repeat=5):
                E=lambda x,y,z:exponent(p,u,x,y,z)
                delta=E(b,c,d)-E((a+b)%p,c,d)+E(a,(b+c)%p,d)-E(a,b,(c+d)%p)+E(a,b,c)
                assert delta%p==0;cocycle_checks+=1
        signatures=[]
        for u in range(p):
            counts=[0]*p
            for x in range(p):
                lens_exp=sum(exponent(p,u,x,(j*x)%p,x) for j in range(p))%p
                assert lens_exp==(u*x*x)%p;lens_checks+=1
                counts[lens_exp]+=1
            # Canonical coefficients in Q[z]/(1+z+...+z^(p-1)).
            signatures.append(tuple(F(c-counts[-1],p) for c in counts[:-1]))
        squares={a*a%p for a in range(1,p)}
        for u in range(p):
            for v in range(p):
                same_orbit=(u==v==0) or (u!=0 and v!=0 and (u*pow(v,-1,p))%p in squares)
                assert (signatures[u]==signatures[v])==same_orbit;pair_checks+=1
        out.append({'prime':p,'distinct_lens_values':len(set(signatures)),
                    'square_orbits':2 if p==2 else 3})
    return {'cocycle_checks_small_primes':cocycle_checks,'lens_exponent_checks':lens_checks,
            'orbit_pair_checks':pair_checks,'primes':out,
            'method':'Exact rational coefficients modulo the prime cyclotomic polynomial; no floating point.'}


def main():
    checks.update(torus=torus_controls(),s3=s3_control(),abelian=abelian_controls(),cyclic=cyclic_cocycle_controls())
    result={'status':'passed','scope':'Exact finite controls only; general Problem 9.3 remains unresolved.','checks':checks}
    text=json.dumps(result,indent=2,sort_keys=True)+'\n'
    (Path(__file__).parent/'verification.json').write_text(text)
    print(text,end='')

if __name__=='__main__':main()
