#!/usr/bin/env python3
"""Exact, bounded controls for the candidate proof. Standard library only.

This is NOT an extremal-function solver or a formalization of the Schiffer,
area, Bieberbach, or compactness theorems. It checks the finite algebra and
rational constants used after those classical analytic inputs.
"""
from fractions import Fraction as F
import json
from pathlib import Path

checks = []
def require(name, condition):
    if not condition:
        raise AssertionError(name)
    checks.append(name)

# Small exact polynomial ring in (z, a2, a3, u), u = 1/w.
def add(p,q):
    r=dict(p)
    for m,c in q.items():
        r[m]=r.get(m,F(0))+c
        if not r[m]: del r[m]
    return r
def scale(p,c): return {m:c*a for m,a in p.items() if c*a}
def mul(p,q):
    r={}
    for m,c in p.items():
        for n,d in q.items():
            k=tuple(a+b for a,b in zip(m,n))
            if k[0] <= 4:
                r[k]=r.get(k,F(0))+c*d
    return {m:c for m,c in r.items() if c}
def power(p,n):
    r={(0,0,0,0):F(1)}
    for _ in range(n):r=mul(r,p)
    return r
def coeff_z(p,n):return {m[1:]:c for m,c in p.items() if m[0]==n}
f={(1,0,0,0):F(1),(2,1,0,0):F(1),(3,0,1,0):F(1)}
u={(0,0,0,1):F(1)}
series={}
for m in range(3):
    series=add(series,scale(mul(power(f,m+2),power(u,m+1)),-1))
require('Schiffer z^2 coefficient',coeff_z(series,2)=={(0,0,1):F(-1)})
require('Schiffer z^3 coefficient',coeff_z(series,3)=={(1,0,1):F(-2),(0,0,2):F(-1)})
require('Schiffer z^4 coefficient',coeff_z(series,4)=={(2,0,1):F(-1),(0,1,1):F(-2),(1,0,2):F(-3),(0,0,3):F(-1)})
require('Koebe coefficient limits A=-2, B=3',2*3+2**2-6*2==-2 and 3*2-3==3)
# Laurent change w=-v^-2, dw=2v^-3 dv. q is -a/w^3-b/w^4-c/w^5.
transformed=[]
for exponent in (3,4,5):
    transformed.append((-4*((-1)**exponent),2*exponent-6))
require('Q dw^2 = 4(a-bv^2+cv^4)dv^2',transformed==[(4,0),(-4,2),(4,4)])

# Exact univariate polynomials, keys are exponents.
def derivative(p):return {n-1:c*n for n,c in p.items() if n}
def evaluate(p,x):return sum((c*x**n for n,c in p.items()),F(0))
def sum_poly(p,q):
    out=dict(p)
    for n,c in q.items():out[n]=out.get(n,F(0))+c
    return {n:c for n,c in out.items() if c}
P0={0:F(-2),2:F(-3),4:F(1)}
d={1:F(1),3:F(1,2),5:F(-1,10)}
require('inverse first-order derivative',derivative(d)=={n:-c/2 for n,c in P0.items()})
q=sum_poly(derivative(d),{n-1:-c for n,c in d.items()})
require('radial-angle first-order polynomial',q=={2:F(1),4:F(-2,5)})
T=F(7,4)
require('first positive sign',evaluate(q,F(1))==F(3,5))
require('second negative sign',evaluate(q,T)==-F(441,640))

E=F(1,10**24); H=F(1,10**12)
require('exact parameter relation',H*H==E)
require('maximizer real-part lower bound positive',2-13*E>0)
require('a2 deviation simplification',52<8**2)
require('a3 area deviation simplification',4*F(13,3)<5**2)
require('a3 total deviation constant',3*8+5==29)
require('A deviation constant',2*29+6*8==106)
require('B deviation constant',3*8==24)
r=F(2,3)
require('H Cauchy-Schwarz tail bound',r**4/(3*(1-r*r))==F(16,135)<F(1,4))
require('H total error below 5 eta',4*r+2<5)
require('H derivative tail bound',1/(1-r*r)**2-1==F(56,25)<F(9,4))
require('sqrt13 below 4',13<16)
require('H bounds at z=-2/3',5*H<F(1,6))
require('f value error below 2 eta',F(2,3)*5*F(7,2)/(F(3,2)**2*F(5,3)**2)<2)
require('f derivative numerator error below 19 eta',5+F(4,3)*10<19)
require('f derivative numerator contribution below 6 eta',19/(F(3,2)**3)<6)
require('f derivative reciprocal contribution below 2 eta',F(1,3)*5*11/(F(3,2)**3*F(5,3)**3)<2)
require('Koebe endpoint distance base',F(6,25)+F(5,9)*F(9,125)==F(7,25))
require('endpoint perturbation below 7 eta',2+F(5,9)*8<7)
require('tip radius below 3/10',F(7,25)+7*H<F(3,10))
require('P0 bound on v-disk',2+3*3**2+3**4==110)
require('P0 derivative bound on v-disk',6*3+4*3**3==126)
require('P error coefficient',106+24*3**2==322)
require('P closeness bound',110+322*H<=111)
require('sqrt remainder bound',F(111**2,2)*H<1)
require('sqrt expansion error bound',161+F(111**2,2)*H<162)
require('G closeness bound',3*111==333)
require('Rouche inverse disk',333*E<1)
require('inverse expansion error bound',486+18315*H<487)
require('inverse square-root Taylor radius',111*E<F(1,4))
require('derivative composition quadratic cost',F(1,2)*126*333==20979)
require('inverse-square-root quadratic cost',2*111**2==24642)
require('derivative expansion error bound',161+(20979+24642)*H<162)
require('natural-coordinate radius gate',T+333*E<F(9,5))
require('candidate trajectory outside tip radius',F(25,81)>F(3,10))
require('inverse denominator bound',1-333*E>F(1,2))
require('q absolute bound',T**2+F(2,5)*T**4<7)
require('Z linear error constant',2*(T*162+487)==1541)
require('Z quadratic error constant',2*7*333==4662)
require('Z final error budget',1541+4662*H<2000)
require('Z positive real part',1-2000*E*H>0)
require('positive sign robust to full error',F(3,5)-2000*H>F(1,2))
require('negative sign robust to full error',-F(441,640)+2000*H<-F(1,2))

# Controls: the checker must distinguish a forced reversal from ordinary
# first-order support perturbations, and expose the degeneracy at epsilon=0.
q_a3={2:F(1,3)}
q_a4={2:F(2),4:F(-2,5)}
def opposite_at_test_points(poly):
    return evaluate(poly,F(1))*evaluate(poly,T)<0
require('positive control: selected perturbation has opposite signs',opposite_at_test_points(q))
require('negative control: a3-only perturbation rejected',not opposite_at_test_points(q_a3))
require('negative control: a4-only perturbation rejected',not opposite_at_test_points(q_a4))
require('zero-perturbation control: no strict reversal',not opposite_at_test_points({}))
# Any error budget >=3/5 invalidates the first sign, unlike our proved bound.
require('negative control: oversized error cannot certify first sign',not (F(3,5)-F(3,5)>0))

result={
 'status':'passed',
 'arithmetic':'Python standard-library Fraction; no floating-point comparisons',
 'checks_passed':len(checks),
 'checks':checks,
 'epsilon':'1/1000000000000000000000000',
 'eta':'1/1000000000000',
 'first_order_values':['3/5','-441/640'],
 'relative_error_bound':'2000/1000000000000',
 'scope':'Finite coefficient extraction, coordinate algebra, rational remainder bounds, endpoint gate, and positive/negative controls.',
 'not_verified_by_code':['compactness and existence of maximizers','classical coefficient and area theorems','support-slit/Schiffer theorem and its applicability','trajectory uniqueness and identification argument','historical novelty','independent peer review']
}
if __name__=='__main__':
    print(json.dumps(result,indent=2))
