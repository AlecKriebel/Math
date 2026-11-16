#!/usr/bin/env python3
"""Own finite integer/dual-number controls; stdout only, no files/imported inputs."""
import json
from math import comb

def trim(p):
    while len(p)>1 and p[-1]==0: p.pop()
    return p
def add(a,b):
    c=[0]*max(len(a),len(b))
    for i,x in enumerate(a): c[i]+=x
    for i,x in enumerate(b): c[i]+=x
    return trim(c)
def neg(p): return [-x for x in p]
def mul(a,b):
    c=[0]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b): c[i+j]+=x*y
    return trim(c)
def monomial(k): return [0]*k+[1]
def remainder(a,b):
    a=a[:]
    while len(a)>=len(b) and a!=[0]:
        k=len(a)-len(b); c=a[-1]; assert b[-1]==1
        for j,x in enumerate(b): a[k+j]-=c*x
        trim(a)
    return a
def dm(a,b): return (a[0]*b[0],a[0]*b[1]+a[1]*b[0])
def da(a,b): return (a[0]+b[0],a[1]+b[1])
def dp(k):
    r=(1,0); q=(1,1) if k>=0 else (1,-1)
    for unused in range(abs(k)): r=dm(r,q)
    return r
def evaluate(coefficients,n):
    r=(0,0)
    for k,c in enumerate(coefficients): r=da(r,dm(c,dp(n*k)))
    return r
def jet(p,d=3): return [sum(a*comb(i,j) for i,a in enumerate(p) if i>=j) for j in range(d+1)]
def summand(k):
    p=mul(monomial(k),[1]*(k+1))
    for j in range(k+2,2*k+2): p=mul(p,add([1],neg(monomial(j))))
    return p

I2=mul([-1,1],[-1,0,1]); assert I2==[1,-1,-1,1]
weighted=[]
for r in range(1,6):
    for k in range(11):
        p=add(add(monomial((r+2)*k),neg(mul([1,1],monomial((r+1)*k)))),monomial(r*k+1))
        assert remainder(p,I2)==[0]
        weighted.append([r,k])
images=[]
for basis in range(6):
    coeff=[(0,0)]*3; pair=[0,0]; pair[basis%2]=1; coeff[basis//2]=tuple(pair)
    values=[evaluate(coeff,n) for n in (1,2,3)]
    assert len({x[0] for x in values})==1 and values[2][1]-2*values[1][1]+values[0][1]==0
    images.append(values)
mixed=[evaluate([(7,-11),(-3,5),(2,-13)],n) for n in (1,2,3)]
assert mixed==[(6,-18),(6,-17),(6,-16)] and dm(dp(1),dp(-1))==(1,0)
terms=[jet(summand(k)) for k in range(8)]
total=[sum(terms[k][j] for k in range(4)) for j in range(4)]
assert total==[1,-6,45,-464]
assert all(remainder(summand(k),I2)==[0] for k in range(2,8))
assert all(all(x==0 for x in row) for row in terms[4:])
triples=[]
for C in (-3,-2,-1,0,1,2,3):
    v=[n*(n*n-1)*C for n in (1,2,3,4)]
    a=v[2]-2*v[1]+v[0]; b=v[3]-2*v[2]+v[1]
    assert a==12*C and b==18*C
    triples.append({'C':C,'values':v,'delta123':a,'delta234':b})
print(json.dumps({'status':'PASS_OWN_SOURCE_FIRST_CONTROLS','weighted_congruence_cases':weighted,'integral_basis_images':images,'mixed_jet':mixed,'printed_series_summand_jets':terms,'series_jet_through_degree3':total,'coefficient_formula_conditional_checks':triples,'limits':'Finite controls accompany written universal proofs; no native code or foreign theorem/normalization certification.'},indent=2))
