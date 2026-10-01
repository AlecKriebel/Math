#!/usr/bin/env python3
"""Exact author controls for k110. Does not implement/prove the published theorem.
No network, downloads, external executable code, or random nondeterminism.
Geometry examples D/R and H/V also appeared in campaign PRs147/148; they
are reused with credit as controls, not as new proofs of those targets.
"""
from fractions import Fraction as F
from math import isqrt
from pathlib import Path
import json

counts = {}
def check(group, condition):
    assert condition, group
    counts[group] = counts.get(group, 0) + 1

def det(p,q): return p[0]*q[1]-p[1]*q[0]
def dot(p,q): return p[0]*q[0]+p[1]*q[1]
def sub(p,q): return (p[0]-q[0],p[1]-q[1])
def area(p): return sum(det(p[i],p[(i+1)%len(p)]) for i in range(len(p)))/2

def outer(p,a2,b2):
    result=[]
    for i,v in enumerate(p):
        w=p[(i+1)%len(p)]
        n=(v[0]/a2,v[1]/b2); m=(w[0]/a2,w[1]/b2)
        d=det(n,m)
        assert d != 0
        result.append(((m[1]-n[1])/d,(n[0]-m[0])/d))
    return result

def check_orbit(p,a2,b2,alpha2,beta2,lengths):
    q=outer(p,a2,b2)
    s=[(alpha2*v[0]/a2,beta2*v[1]/b2) for v in q]
    group='rational_four_period_geometry'
    check(group,len(set(p))==len(p))
    check(group,a2-alpha2==b2-beta2 and 0<beta2<b2)
    for i,v in enumerate(p):
        w=p[(i+1)%len(p)]
        z=s[i]; t=q[i]; u=sub(w,v)
        check(group,v[0]**2/a2+v[1]**2/b2==1)
        check(group,z[0]**2/alpha2+z[1]**2/beta2==1)
        check(group,v[0]*t[0]/a2+v[1]*t[1]/b2==1)
        check(group,w[0]*t[0]/a2+w[1]*t[1]/b2==1)
        check(group,det(sub(z,v),u)==0)
        check(group,dot((z[0]/alpha2,z[1]/beta2),u)==0)
        check(group,0<dot(sub(z,v),u)<dot(u,u))
        check(group,dot(u,u)==lengths[i]**2)
        incoming=tuple(x/lengths[i-1] for x in sub(v,p[i-1]))
        outgoing=tuple(x/lengths[i] for x in u)
        normal=(v[0]/a2,v[1]/b2)
        reflected=tuple(incoming[j]-2*dot(incoming,normal)*normal[j]/dot(normal,normal) for j in range(2))
        check(group,reflected==outgoing)
    check(group,area(s)==alpha2*beta2/(a2*b2)*area(q))
    check(group,area(p)*area(s)==alpha2*beta2/(a2*b2)*area(p)*area(q))
    check(group,area(list(reversed(s)))==-area(s))
    check(group,area(s[1:]+s[:1])==area(s))
    return area(p),area(q),area(s)

four=[]
for ai in range(2,61):
    for bi in range(1,ai):
        si=isqrt(ai*ai+bi*bi)
        if si*si!=ai*ai+bi*bi: continue
        a,b,s=map(F,(ai,bi,si)); a2,b2=a*a,b*b
        alpha2,beta2=a2*a2/(s*s),b2*b2/(s*s)
        d=[(a,F(0)),(F(0),b),(-a,F(0)),(F(0),-b)]
        r=[(a2/s,b2/s),(-a2/s,b2/s),(-a2/s,-b2/s),(a2/s,-b2/s)]
        da=check_orbit(d,a2,b2,alpha2,beta2,[s]*4)
        ra=check_orbit(r,a2,b2,alpha2,beta2,[2*a2/s,2*b2/s]*2)
        target=8*a2*a2*b2*b2/(a2+b2)**2
        check('four_period_product',da[0]*da[1]==ra[0]*ra[1]==8*a2*b2)
        check('four_period_product',da[0]*da[2]==ra[0]*ra[2]==target)
        check('low_N_negative_control',target != 2*a2*a2*b2*b2/(a2+b2)**2)
        check('outer_inner_product_negative_control',da[1]*da[2] != ra[1]*ra[2])
        if (ai,bi)==(4,3): four=[list(map(str,da)),list(map(str,ra)),str(target)]

# Arbitrary rational ordered polygons: test line polarity and determinant scaling.
# S here is the pole of each chord relative to C, not asserted to lie on C.
# These include crossing orders and signed-area cancellation; they are not
# falsely described as Poncelet families.
points=[]
for k in range(1,18):
    t=F(k,19)
    points.append((4*(1-t*t)/(1+t*t),6*t/(1+t*t)))
for n in (4,5,6,7,8,9,10,11):
    for step in range(1,n):
        if __import__('math').gcd(step,n)!=1: continue
        p=[points[(step*i)%n] for i in range(n)]
        q=outer(p,F(16),F(9))
        s=[(F(7,8)*v[0],F(7,9)*v[1]) for v in q]
        for i in range(n):
            check('rational_polarity_auxiliary',p[i][0]*q[i][0]/16+p[i][1]*q[i][1]/9==1)
            check('rational_polarity_auxiliary',p[(i+1)%n][0]*s[i][0]/14+p[(i+1)%n][1]*s[i][1]/7==1)
        check('signed_shoelace_covariance',area(s)==F(49,72)*area(q))
        check('signed_shoelace_covariance',area(s*2)==2*area(s))
        check('signed_shoelace_covariance',area(list(reversed(s)))==-area(s))

# Real general-position determinant for rational confocal squared axes.
for a2 in range(2,12):
    for b2 in range(1,a2):
        for j in (1,2,3):
            lam=F(j*b2,4); al=F(a2)-lam; be=F(b2)-lam
            delta=F(1,a2)/be-F(1,b2)/al
            check('complex_transversality_coefficients',delta==lam*(a2-b2)/(a2*b2*al*be)>0)
            x2=F(a2)*al/(a2-b2); y2=-F(b2)*be/(a2-b2)
            check('complex_transversality_coefficients',x2/a2+y2/b2==1)
            check('complex_transversality_coefficients',x2/al+y2/be==1 and x2*y2!=0)

# Two exact primitive six-period controls from the geometry of PR148.
# Installed SymPy is used solely for exact quadratic-radical arithmetic.
import sympy as sp
rt=sp.sqrt; rat=sp.Rational
h=[(2,0),(rat(4,3),rt(5)/3),(-rat(4,3),rt(5)/3),(-2,0),(-rat(4,3),-rt(5)/3),(rat(4,3),-rt(5)/3)]
v=[(0,1),(-4*rt(2)/3,rat(1,3)),(-4*rt(2)/3,-rat(1,3)),(0,-1),(4*rt(2)/3,-rat(1,3)),(4*rt(2)/3,rat(1,3))]
six=[]
for p in (h,v):
    p=[tuple(map(sp.sympify,t)) for t in p]; q=outer(p,sp.Integer(4),sp.Integer(1))
    ss=[(rat(8,9)*t[0],rat(5,9)*t[1]) for t in q]
    for i,z in enumerate(ss):
        check('quadratic_six_period',sp.simplify(z[0]**2/rat(32,9)+z[1]**2/rat(5,9)-1)==0)
        check('quadratic_six_period',sp.simplify(det(sub(z,p[i]),sub(p[(i+1)%6],p[i])))==0)
    aa,aq,ass=map(sp.simplify,(area(p),area(q),area(ss)))
    check('quadratic_six_period',sp.simplify(aa*aq-rat(320,9))==0)
    check('quadratic_six_period',sp.simplify(aa*ass-rat(12800,729))==0)
    check('quadratic_six_period',sp.simplify(ass-rat(40,81)*aq)==0)
    six.append([str(aa),str(aq),str(ass),str(sp.simplify(aa*ass))])

receipt={'status':'PASS','exact_assertions':sum(counts.values()),'counts':counts,
         'four_period_axes_4_3':{'diamond_areas_A_Aprime_Adoubleprime':four[0],'rectangle_areas_A_Aprime_Adoubleprime':four[1],'common_product':four[2]},
         'six_period_controls':six,
         'limits':'Finite exact implementation/normalization controls only; general theorem is the published Chavez-Caliz input plus CANDIDATE.md proof. Auxiliary rational polygons do not assert caustic tangency.'}
print(json.dumps(receipt,indent=2))
Path(__file__).with_name('verification.json').write_text(json.dumps(receipt,indent=2)+'\n')
