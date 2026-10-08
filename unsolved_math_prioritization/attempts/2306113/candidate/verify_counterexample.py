#!/usr/bin/env python3
"""Exact rational certificate; see PROOF.md for the analytic implications."""
import argparse
from fractions import Fraction as Q
import hashlib
import json
from math import comb,isqrt
from pathlib import Path
import re
import sys

class Invalid(ValueError):pass

def need(test,message):
    if not test:raise Invalid(message)

def pairs(items):
    result={}
    for key,value in items:
        need(key not in result,'duplicate JSON key')
        result[key]=value
    return result

def rational(s):
    need(type(s) is str and len(s)<=80 and re.fullmatch(r'-?(?:0|[1-9][0-9]*)(?:/[1-9][0-9]*)?',s) is not None,'invalid rational encoding')
    out=Q(s)
    need(str(out)==s,'noncanonical rational')
    need(abs(out)<=10**12,'rational size limit')
    return out

Z=(Q(0),Q(0));O=(Q(1),Q(0))
def add(a,b):return(a[0]+b[0],a[1]+b[1])
def neg(a):return(-a[0],-a[1])
def mul(a,b):return(a[0]*b[0]-a[1]*b[1],a[0]*b[1]+a[1]*b[0])
def scale(a,b):return(a[0]*b,a[1]*b)
def norm2(a):return a[0]*a[0]+a[1]*a[1]
def unit(t):return (-(1-t*t)/(1+t*t),-2*t/(1+t*t))
def conv(a,b,d):
    out=[Z]*(d+1)
    for i,x in enumerate(a):
        for j,y in enumerate(b[:d+1-i]):out[i+j]=add(out[i+j],mul(x,y))
    return out

def compose(a,b,d):
    out=[Z]*(d+1);power=[O]+[Z]*d
    for x in a:
        out=[add(y,mul(x,z)) for y,z in zip(out,power)]
        power=conv(power,b,d)
    return out

def koebe(u,d):
    out=[Z];power=O
    for n in range(1,d+1):
        out.append(scale(power,Q(n)));power=mul(power,neg(u))
    return out

def slit(q,u,d):
    inv=[Z];power=O
    for n in range(1,d+1):
        inv.append(scale(power,Q(comb(2*n,n),n+1)));power=mul(power,u)
    result=compose(inv,[scale(c,q) for c in koebe(u,d)],d)
    # Independently test the defining formal-series equation k_u(phi)=q k_u.
    need(compose(koebe(u,d),result,d)==[scale(c,q) for c in koebe(u,d)],'slit inverse composition mismatch')
    return result

def evalpoly(a,z):
    v=Z
    for c in reversed(a):v=add(mul(v,z),c)
    return v

def sqrt_upper(x,s):
    need(x>=0,'negative square')
    k=isqrt((x.numerator*s*s)//x.denominator)
    if Q(k*k,s*s)<x:k+=1
    bound=Q(k,s)
    need(bound*bound>=x,'square-root enclosure failure')
    return bound

def verify(data):
    keys={'degree','q1','q2','t1','t2','t3','radius','coefficients','norm_upper','grid_N','sqrt_scale','rho','convolution_lower'}
    need(type(data) is dict and set(data)==keys,'wrong schema keys')
    d=data['degree'];N=data['grid_N'];ss=data['sqrt_scale']
    need(type(d) is int and 2<=d<=16,'degree range')
    need(type(N) is int and 64<=N<=16384,'grid range')
    need(type(ss) is int and 1000<=ss<=10**12,'sqrt scale range')
    q1=rational(data['q1']);q2=rational(data['q2']);r=rational(data['radius']);U=rational(data['norm_upper'])
    need(0<q1<1 and 0<q2<1,'slit parameters outside (0,1)')
    need(0<r<1,'radius outside (0,1)')
    need(0<U<=10,'invalid norm upper bound')
    rho=rational(data['rho']);B=rational(data['convolution_lower'])
    need(0<=rho<=1,'rho outside [0,1]')
    need(B>U*(1+rho)**2,'parameterized neighborhood separation fails')
    us=[unit(rational(data['t'+str(j)])) for j in (1,2,3)]
    need(all(norm2(u)==1 for u in us),'unit-circle parameter failure')
    cs=data['coefficients'];need(type(cs) is list and len(cs)==d-1,'coefficient count')
    c=[Z,Z]
    for pair in cs:
        need(type(pair) is list and len(pair)==2,'complex coefficient schema')
        c.append((rational(pair[0]),rational(pair[1])))
    need(any(x!=Z for x in c),'zero perturbation')
    a=[scale(x,1/(q1*q2)) for x in compose(koebe(us[2],d),compose(slit(q2,us[1],d),slit(q1,us[0],d),d),d)]
    need(a[0]==Z and a[1]==O,'normalization failed')
    L=Z
    for n in range(2,d+1):L=add(L,scale(mul(c[n],a[n]),r**(n-1)))
    need(L[0]>B,'convolution lower bound fails')
    lip=sum(Q(n*(n-1))*(abs(c[n][0])+abs(c[n][1])) for n in range(2,d+1))
    plus=[scale(c[n],Q(n+1)) for n in range(1,d+1)]
    minus=[scale(c[n],Q(n-1)) for n in range(1,d+1)]
    maximum=Q(0);count=0
    for j in range(-N,N+1):
        t=Q(j,N);v=((1-t*t)/(1+t*t),2*t/(1+t*t))
        for z in (v,neg(v)):
            p=evalpoly(plus,z);m=evalpoly(minus,z)
            bound=(sqrt_upper(norm2(p),ss)+sqrt_upper(norm2(m),ss))/2
            maximum=max(maximum,bound);count+=1
    certified=maximum+lip/N
    need(certified<U,'global neighborhood bound fails')
    return {'status':'PASS','arithmetic':'exact fractions and integer square-root enclosures','degree':d,'grid_points':count,'sample_norm_upper':str(maximum),'angular_lipschitz_upper':str(lip),'covering_norm_upper':str(certified),'chosen_norm_upper':str(U),'chosen_convolution_lower':str(B),'rho':str(rho),'gamma':str(1/(1+rho)**2),'real_convolution_exceeds_norm_upper':True,'real_convolution_numerator':str(L[0].numerator),'real_convolution_denominator':str(L[0].denominator),'coefficient_sha256':hashlib.sha256(json.dumps([[str(x),str(y)] for x,y in a],separators=(',',':')).encode()).hexdigest(),'scope':'Exact arithmetic certificate; PROOF.md supplies the universal analytic and covering arguments.'}

def main():
    p=argparse.ArgumentParser();p.add_argument('certificate',type=Path);args=p.parse_args()
    try:
        raw=args.certificate.read_bytes();need(len(raw)<=10000,'certificate size limit')
        data=json.loads(raw,object_pairs_hook=pairs,parse_constant=lambda x:(_ for _ in ()).throw(Invalid('nonfinite JSON constant')))
        result=verify(data)
    except (ValueError,OSError,UnicodeError,json.JSONDecodeError,ZeroDivisionError) as e:
        print(json.dumps({'status':'REJECT','reason':str(e)}));return 2
    print(json.dumps(result,sort_keys=True,indent=2));return 0
if __name__=='__main__':sys.exit(main())
