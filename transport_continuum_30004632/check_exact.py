"""Exact algebra and rational finite checks; not a replacement for the proofs."""
import json
from fractions import Fraction as Q
import sympy as s

def require(ok, message):
    if not ok: raise RuntimeError('MATHEMATICAL CHECK: '+message)

p,r,z,h,d,gamma,eta=s.symbols('p r z h d gamma eta', positive=True)
f=(r-s.sqrt(r*r-4*p*(1-p)))/2
require(s.simplify(f*f-r*f+p*(1-p))==0,'flux root equation')
require(s.simplify(s.diff(f,p)-(1-2*p)/s.sqrt(r*r-4*p*(1-p)))==0,'flux derivative')
require(s.simplify(s.diff(f,p,2)+2*(r*r-1)/(r*r-4*p*(1-p))**s.Rational(3,2))==0,'flux concavity derivative')
ratio=(p+z)*(1-p+z)/((p-z)*(1-p-z))
# The cross ratio is (r+1)/(r-1) after the exact quadratic relation.
num=s.together(ratio-(r+1)/(r-1)).as_numer_denom()[0]
require(s.rem(num,z*z-r*z+p*(1-p),z)==0,'cross ratio normalization')
x,a,b=s.symbols('x a b',real=True)
D=(x-b)**2-(x-a)**2
cost_derivative=h*(D.subs(x,x+h)-D)
require(s.expand(cost_derivative+2*h*h*(b-a))==0,'quadratic pair cost normalization')
# For D(x)=-2x-x^2 the midpoint divided difference is exactly 2+2ih.
i=s.symbols('i',integer=True)
Dgeneral=-2*x-x*x
gamma_n=(Dgeneral.subs(x,(i-s.Rational(1,2))*h)-Dgeneral.subs(x,(i+s.Rational(1,2))*h))/h
require(s.expand(gamma_n-(2+2*i*h))==0,'C1 midpoint normalization')
checks=0
for den in range(2,17):
 for j in range(1,den):
  pp=Q(j,den)
  for div in (2,3,4):
   ff=min(pp,1-pp)/div
   rr=(pp*(1-pp)+ff*ff)/ff
   require(rr>1,'r positivity')
   require((pp+ff)*(1-pp+ff)/((pp-ff)*(1-pp-ff))==(rr+1)/(rr-1),'rational Euler equation')
   A=Q(1,7);hh=Q(1,13);B=A+2*hh*pp
   U=(A+B)/2-hh*ff
   require(U-A==hh*(pp-ff) and B-U==hh*(pp+ff),'cumulative pair identity')
   require(max(A,B-hh)<=U<=min(A+hh,B),'pair feasibility')
   checks+=1
# Exact triangular lower barrier, convex combinations of its three planes.
barriers=0
for k in range(1,9):
 kk=Q(k,8)
 for v in range(9):
  for w in range(9-v):
   theta1=Q(v,8);theta2=Q(w,8)
   slope=theta1+theta2/2; tau=-theta2*kk/2
   require(tau+kk*min(slope,1-slope)>=0,'barrier convex contact')
   barriers+=1
for mm in range(1,10):
 for xx in range(11):
  m=Q(mm,10);xq=Q(xx,10)
  B=max(0,m+xq-1,(m+xq-1)/2)
  require(B==max(0,m+xq-1),'finite time barrier collapse')
print(json.dumps({'symbolic_identities':6,'rational_pair_checks':checks,'barrier_contact_checks':barriers,'barrier_collapse_checks':99,'result':'PASS','role':'finite and symbolic checks supplement analytical proof'},sort_keys=True,indent=2))
