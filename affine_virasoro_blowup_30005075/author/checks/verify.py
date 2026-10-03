#!/usr/bin/env python3
"""Exact checks, not a substitute for the proof in NORMALIZATION.md."""
import json, platform, sys
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import sympy as s
sys.path.insert(0,str(Path(__file__).parent))
from normalization import char, R, E, C, norm, t, p,q,u,v,w
checks={}
raw=s.factor(char('sl',p,q,u,v,w,False)-char('sl',p,q/p,u,v,w,False)-char('vir',p/q,q,u,v,w))
expected=-p*p*q*(u*u-w*w)/((p-q)*(q-1))
assert s.cancel(raw-expected)==0
checks['printed_B10_character_residual']=str(raw)
assert s.cancel(char('sl',p,q,u,v,w)-char('sl',p,q/p,u,v,w)-char('vir',p/q,q,u,v,w))==0
checks['corrected_character_splitting']=True
D1=(1-p)*(1-q/p);D2=(1-p/q)*(1-q)
def Afin(n):
 if n>0:return -sum(p**i*q**j for i in range(n) for j in range(n-i))
 return -sum(p**(-i)*q**(-j) for i in range(1,-n) for j in range(1,-n-i+1))
for n in range(-10,11):
 A=(p**n-1)/D1+(q**n-1)/D2
 B=q/p*(p**n-1)/D1+(q**n-1)/D2
 assert s.cancel(A-Afin(n))==0
 assert s.cancel(B-q*Afin(n-1))==0
checks['triangle_character_identities_checked']=42
l,n,m=s.symbols('l n m',integer=True);d=lambda x:x*(x+1)/2
rs=(l-n-m,-l+n-m,-l-n+m)
assert s.expand(d(-l-n-m)+sum(d(r) for r in rs)-d(-2*l)-d(-2*n)-d(-2*m))==0
sig=sum(d(r) for r in rs)-d(-2*l)
S=d(l-m+n)+4*n*(m-n)*(m-n-s.Rational(1,2))
# Exact symbolic parity decomposition: all terms here are even for integer l,m,n.
even=-l*(l+1)+m*(m-1)-n*(n+1)-2*l*n-4*m*m*n+8*m*n*n+2*m*n-4*n**3
assert s.expand(sig-S-l-m-even)==0
checks['degree_zero_and_sign_parity_polynomial']=True
K,h,j=s.symbols('K h j');b2=-K/(K+1);Pb=-(h+1)*b2/(2*K)
ha=lambda h,K:h*(h+2)/(4*K)
grade=s.factor(ha(h+2*j,K+1)-ha(h,K+1)-2*j*Pb-j*j*b2)
assert grade==j*j
source_b2=-(K+1)/K;source_Pb=(h+1)/(2*K)
source_grade=s.factor(ha(h+2*j,K+1)-ha(h,K+1)-2*j*source_Pb-j*j*source_b2)
checks['correct_coset_grade']=str(grade)
checks['printed_OWR_grade_residual']=str(s.factor(source_grade-j*j))
# Check full triple normalizer products using the finite triangle formula, independent
# of the rational-character expansion used in the additional spot checks below.
def ratio_triangle(l,n,m,mu,nu,la,K):
 ep1=s.Integer(1);ep2=-K;a1=la/2;a2=nu/2;a3=mu/2
 T=lambda n,a:t(n,a,ep1,ep2)
 r1=l-n-m;r2=-l+n-m;r3=-l-n+m
 sigma=(r1*(r1+1)+r2*(r2+1)+r3*(r3+1)-(-2*l)*(-2*l+1))//2
 return s.Integer(-1)**sigma*T(-l-n-m,a1+a2+a3+ep1)*T(r1,-a1+a2+a3)*T(r2,a1-a2+a3)*T(r3,a1+a2-a3)/(T(-2*l,2*a1)*T(-2*n,2*a2+ep1)*T(-2*m,2*a3+ep1))
samples=[(s.Rational(7,3),s.Rational(11,7),s.Rational(13,11),s.Rational(17,13)),(s.Rational(13,7),s.Rational(5,11),s.Rational(17,19),s.Rational(23,29))]
count=0
for K,la,nu,mu in samples:
 for l,n,m in product(range(-3,4),repeat=3):
  r=ratio_triangle(l,n,m,mu,nu,la,K)
  target=s.Integer(-1)**(l+m)*C(m,n,l,mu,nu,la,K)/norm(l,la,K)
  assert s.cancel(r-target)==0,(K,l,n,m,r,target)
  count+=1
checks['exact_three_point_instances']=count
spots=[(1,0,0),(-1,0,0),(0,0,1),(0,0,-1),(1,0,1),(0,1,0),(2,0,0),(-2,1,0),(1,-1,2)]
K,la,nu,mu=samples[0]
for l,n,m in spots:
 actual=E(R(l,n,m),(1,-K,la/2,nu/2,mu/2))
 assert s.cancel(actual-ratio_triangle(l,n,m,mu,nu,la,K))==0
checks['independent_Laurent_character_spot_checks']=len(spots)
mu1,mu2,mu3,mu4=map(s.Rational,('11/7','13/11','17/13','23/19'))
for j in range(-5,6):
 ratio1=ratio_triangle(0,0,j,la,mu2,mu1,K)
 ratio2=ratio_triangle(j,0,0,mu4,mu3,la,K)
 coefficient=C(0,0,j,mu4,mu3,la,K)*C(j,0,0,la,mu2,mu1,K)/norm(j,la,K)
 assert s.cancel(ratio1*ratio2-coefficient)==0
checks['four_point_sewing_instances']=11
# Scale-free blowup chart dictionary.
e1,e2,a,j=s.symbols('e1 e2 a j');K=-e2/e1
lam=2*a/e1-1
assert s.simplify(-(e2-e1)/e1-(K+1))==0
assert s.simplify((2*(a+e1*j)/e1-1)-(lam+2*j))==0
assert s.simplify((e1-e2)/e2+(K+1)/K)==0
checks['epsilon_level_and_affine_shift_dictionary']=True
result={'status':'PASS','python':platform.python_version(),'sympy':s.__version__,'checks':checks,
 'scope':'Exact algebraic normalization and grading checks only. Does not prove AGT, analytic convergence, or equality to an independently fixed gauge-theory normalization.'}
print(json.dumps(result,indent=2))
